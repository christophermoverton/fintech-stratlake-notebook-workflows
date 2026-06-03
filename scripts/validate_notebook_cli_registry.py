"""Validate notebook CLI examples against the argument-aware command registry."""

from __future__ import annotations

import argparse
import ast
import json
import re
import shlex
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None  # type: ignore[assignment]


FLAG_RE = re.compile(r"(?<![\w-])--[A-Za-z0-9][A-Za-z0-9-]*")
VALUE_PLACEHOLDER = "__VALUE__"


@dataclass(frozen=True)
class RegistryFlag:
    name: str
    kind: str
    argparse_required: bool = False
    notebook_contract_required: bool = False
    required_when: str | None = None
    allowed_values: tuple[str, ...] = ()
    classifications: tuple[str, ...] = ()


@dataclass(frozen=True)
class RegistryEntry:
    command: str
    subcommand: str | None
    flags: dict[str, RegistryFlag]
    subcommands: tuple[str, ...] = ()
    unsupported_flags: tuple[str, ...] = ()
    unsupported_patterns: tuple[str, ...] = ()
    classifications: tuple[str, ...] = ()

    def display(self) -> str:
        if self.subcommand:
            return f"{self.command} {self.subcommand}"
        return self.command


@dataclass(frozen=True)
class ParsedFlag:
    name: str
    value: str | None = None
    uses_equals: bool = False


@dataclass(frozen=True)
class CommandExample:
    path: Path
    cell_index: int
    command: str
    subcommand: str | None
    parts: tuple[str, ...]
    flags: tuple[ParsedFlag, ...]
    source_kind: str
    is_help: bool = False
    classification: str = "unknown"

    def command_display(self) -> str:
        if self.subcommand:
            return f"{self.command} {self.subcommand}"
        return self.command

    def flag_names(self) -> set[str]:
        return {flag.name for flag in self.flags}

    def command_text(self) -> str:
        return " ".join(self.parts)


@dataclass(frozen=True)
class Finding:
    path: Path | None
    cell_index: int | None
    reason: str


@dataclass
class ValidationReport:
    targets_checked: int = 0
    examples: list[CommandExample] = field(default_factory=list)
    registry_examples_validated: int = 0
    safe_help_examples: int = 0
    safe_preview_examples: int = 0
    dry_run_examples: int = 0
    manual_only_live_examples: int = 0
    unsafe_live_examples: int = 0
    warnings: list[str] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)


@dataclass(frozen=True)
class RegistryModel:
    commands: dict[str, RegistryEntry]
    subcommands: dict[tuple[str, str], RegistryEntry]
    excluded: dict[str, dict[str, Any]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate notebook CLI examples against the argument-aware CLI registry.",
        epilog=(
            "Usage: python scripts/validate_notebook_cli_registry.py "
            "--config config/notebook_cli_registry.toml"
        ),
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Notebook files to validate. Defaults to config targets.",
    )
    parser.add_argument(
        "--config",
        default="config/notebook_cli_registry.toml",
        help="TOML notebook CLI registry validator config path.",
    )
    return parser.parse_args()


def load_toml(path: Path) -> dict[str, Any]:
    if tomllib is None:
        raise RuntimeError("Python 3.11 or newer is required for tomllib TOML parsing.")
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"Config file does not exist: {path}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise RuntimeError(f"Malformed TOML config {path}: {exc}") from exc


def source_text(cell: dict[str, Any]) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    return str(source)


def registry_flag(name: str, data: dict[str, Any]) -> RegistryFlag:
    return RegistryFlag(
        name=name,
        kind=str(data.get("kind", "")),
        argparse_required=bool(data.get("argparse_required", False)),
        notebook_contract_required=bool(data.get("notebook_contract_required", False)),
        required_when=data.get("required_when"),
        allowed_values=tuple(str(value) for value in data.get("allowed_values", [])),
        classifications=tuple(str(value) for value in data.get("classifications", [])),
    )


def build_registry_model(registry: dict[str, Any]) -> RegistryModel:
    commands: dict[str, RegistryEntry] = {}
    subcommands: dict[tuple[str, str], RegistryEntry] = {}

    for entry in registry.get("commands", []):
        command = str(entry["name"])
        flags = {
            name: registry_flag(name, data)
            for name, data in entry.get("flags", {}).items()
        }
        commands[command] = RegistryEntry(
            command=command,
            subcommand=None,
            flags=flags,
            subcommands=tuple(str(value) for value in entry.get("subcommands", [])),
            unsupported_flags=tuple(str(value) for value in entry.get("unsupported_flags", [])),
            unsupported_patterns=tuple(
                str(value.get("pattern", value))
                for value in entry.get("unsupported_patterns", [])
            ),
            classifications=tuple(str(value) for value in entry.get("classifications", [])),
        )

    for entry in registry.get("command_subcommands", []):
        command = str(entry["command"])
        subcommand = str(entry["subcommand"])
        flags = {
            name: registry_flag(name, data)
            for name, data in entry.get("flags", {}).items()
        }
        subcommands[(command, subcommand)] = RegistryEntry(
            command=command,
            subcommand=subcommand,
            flags=flags,
            unsupported_flags=tuple(str(value) for value in entry.get("unsupported_flags", [])),
            unsupported_patterns=tuple(
                str(value.get("pattern", value))
                for value in entry.get("unsupported_patterns", [])
            ),
            classifications=tuple(str(value) for value in entry.get("classifications", [])),
        )

    excluded = {
        str(entry["name"]): entry
        for entry in registry.get("excluded_candidates", [])
        if "name" in entry
    }
    return RegistryModel(commands=commands, subcommands=subcommands, excluded=excluded)


def split_command(text: str) -> list[str]:
    try:
        return shlex.split(text, posix=True)
    except ValueError:
        return text.split()


def shell_command_blocks(source: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []

    for line in source.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("!"):
            if current:
                blocks.append(" ".join(current))
            current = [stripped[1:].strip()]
            if not stripped.rstrip().endswith("\\"):
                blocks.append(" ".join(current))
                current = []
            continue

        if current:
            current.append(stripped.strip())
            if not stripped.rstrip().endswith("\\"):
                blocks.append(" ".join(current))
                current = []

    if current:
        blocks.append(" ".join(current))

    return [block.replace("\\", " ").strip() for block in blocks if block.strip()]


def flag_base(part: str) -> str:
    return part.split("=", 1)[0]


def parsed_flags(parts: list[str]) -> tuple[ParsedFlag, ...]:
    flags: list[ParsedFlag] = []
    index = 0
    while index < len(parts):
        part = parts[index]
        if not part.startswith("--"):
            index += 1
            continue

        if "=" in part:
            name, value = part.split("=", 1)
            flags.append(ParsedFlag(name=name, value=value, uses_equals=True))
            index += 1
            continue

        value = None
        if index + 1 < len(parts) and not parts[index + 1].startswith("-"):
            value = parts[index + 1]
        flags.append(ParsedFlag(name=part, value=value))
        index += 1
    return tuple(flags)


def is_help(parts: list[str]) -> bool:
    return "--help" in {flag_base(part) for part in parts if part.startswith("--")} or "-h" in parts


def parse_parts(
    path: Path,
    cell_index: int,
    parts: list[str],
    source_kind: str,
    model: RegistryModel,
) -> CommandExample | None:
    if not parts:
        return None
    command = parts[0]
    if command not in model.commands and command not in model.excluded:
        return CommandExample(
            path=path,
            cell_index=cell_index,
            command=command,
            subcommand=None,
            parts=tuple(parts),
            flags=parsed_flags(parts[1:]),
            source_kind=source_kind,
            is_help=is_help(parts[1:]),
        )

    subcommand = None
    rest = parts[1:]
    command_entry = model.commands.get(command)
    if command_entry and command_entry.subcommands and rest and not rest[0].startswith("-"):
        subcommand = rest[0]
        rest = rest[1:]

    return CommandExample(
        path=path,
        cell_index=cell_index,
        command=command,
        subcommand=subcommand,
        parts=tuple(parts),
        flags=parsed_flags(rest),
        source_kind=source_kind,
        is_help=is_help(rest),
    )


def ignored_shell(block: str, settings: dict[str, Any]) -> bool:
    stripped = block.strip()
    for prefix in settings.get("ignored_shell_prefixes", []):
        if stripped.startswith(str(prefix)):
            return True
    parts = split_command(stripped)
    if not parts:
        return True
    return any(parts[0].startswith(str(prefix)) for prefix in settings.get("ignored_command_prefixes", []))


def watched_unknown(command: str, settings: dict[str, Any]) -> bool:
    return any(command.startswith(str(prefix)) for prefix in settings.get("watched_command_prefixes", []))


def extract_shell_examples(
    path: Path,
    cell_index: int,
    source: str,
    model: RegistryModel,
    settings: dict[str, Any],
) -> list[CommandExample]:
    examples: list[CommandExample] = []
    for block in shell_command_blocks(source):
        if ignored_shell(block, settings):
            continue
        example = parse_parts(path, cell_index, split_command(block), "shell", model)
        if example is not None and (
            example.command in model.commands
            or example.command in model.excluded
            or watched_unknown(example.command, settings)
        ):
            examples.append(example)
    return examples


def variable_is_preview(name: str, settings: dict[str, Any]) -> bool:
    if not name.isupper():
        return False
    suffixes = tuple(str(value) for value in settings.get("preview_variable_suffixes", []))
    return name.endswith(suffixes)


def stringish_parts(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
            elif isinstance(value, ast.FormattedValue):
                parts.append(VALUE_PLACEHOLDER)
        return parts
    if isinstance(node, ast.List | ast.Tuple):
        parts = []
        for element in node.elts:
            nested = stringish_parts(element)
            if nested:
                parts.extend(nested)
            elif isinstance(element, ast.AST):
                parts.append(VALUE_PLACEHOLDER)
        return parts
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return stringish_parts(node.left) + stringish_parts(node.right)
    return []


def preview_text_from_value(node: ast.AST) -> str | None:
    parts = stringish_parts(node)
    if not parts:
        return None
    return " ".join(part.strip() for part in parts if part.strip())


def extract_preview_examples(
    path: Path,
    cell_index: int,
    source: str,
    model: RegistryModel,
    settings: dict[str, Any],
) -> list[CommandExample]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    examples: list[CommandExample] = []
    known = set(model.commands) | set(model.excluded)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and variable_is_preview(target.id, settings)
            for target in node.targets
        ):
            continue
        text = preview_text_from_value(node.value)
        if not text or not any(command in text for command in known):
            continue
        parts = split_command(text)
        if not parts or parts[0] not in known:
            continue
        example = parse_parts(path, cell_index, parts, "preview", model)
        if example is not None:
            examples.append(example)
    return examples


def extract_examples(
    path: Path,
    model: RegistryModel,
    settings: dict[str, Any],
) -> tuple[list[CommandExample], list[Finding]]:
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [], [Finding(path, None, "notebook file does not exist")]
    except json.JSONDecodeError as exc:
        return [], [Finding(path, None, f"malformed notebook JSON: {exc}")]
    except UnicodeDecodeError as exc:
        return [], [Finding(path, None, f"could not decode as UTF-8: {exc}")]

    cells = notebook.get("cells")
    if not isinstance(cells, list):
        return [], [Finding(path, None, "notebook JSON has no valid cells list")]

    examples: list[CommandExample] = []
    findings: list[Finding] = []
    for cell_index, cell in enumerate(cells):
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        source = source_text(cell)
        examples.extend(extract_shell_examples(path, cell_index, source, model, settings))
        examples.extend(extract_preview_examples(path, cell_index, source, model, settings))
    return examples, findings


def entry_for(example: CommandExample, model: RegistryModel) -> RegistryEntry | None:
    if example.subcommand is not None:
        return model.subcommands.get((example.command, example.subcommand))
    return model.commands.get(example.command)


def required_flags(entry: RegistryEntry, key: str) -> set[str]:
    return {name for name, flag in entry.flags.items() if getattr(flag, key)}


def has_dry_run(example: CommandExample) -> bool:
    return "--dry-run" in example.flag_names()


def classify_example(example: CommandExample, entry: RegistryEntry | None) -> str:
    if example.is_help:
        return "safe_help"
    if has_dry_run(example):
        return "dry_run"
    if example.source_kind == "preview":
        return "safe_preview"
    if entry and "unsafe_live" in entry.classifications:
        return "unsafe_live"
    if entry and "manual_only_live" in entry.classifications:
        return "manual_only_live"
    return "manual_only_live"


def flag_values(example: CommandExample, name: str) -> list[str]:
    return [flag.value for flag in example.flags if flag.name == name and flag.value is not None]


def unsupported_pattern_matches(pattern: str, example: CommandExample) -> bool:
    parts = split_command(pattern)
    if not parts:
        return False
    actual = list(example.parts)
    position = 0
    for part in parts:
        if part.startswith("<") and part.endswith(">"):
            if position >= len(actual) or actual[position].startswith("-"):
                return False
            position += 1
            continue
        try:
            found = actual.index(part, position)
        except ValueError:
            return False
        position = found + 1
    return True


def validate_example(
    example: CommandExample,
    model: RegistryModel,
    settings: dict[str, Any],
) -> tuple[CommandExample, list[Finding], list[str]]:
    findings: list[Finding] = []
    warnings: list[str] = []

    if example.command in model.excluded:
        findings.append(
            Finding(
                example.path,
                example.cell_index,
                f"{example.command} is excluded from valid current notebook syntax",
            )
        )
        for pattern in model.excluded[example.command].get("unsupported_patterns", []):
            pattern_text = str(pattern.get("pattern", pattern))
            if unsupported_pattern_matches(pattern_text, example):
                findings.append(
                    Finding(
                        example.path,
                        example.cell_index,
                        f"unsupported excluded-command pattern for {example.command}: {pattern_text}",
                    )
                )
        return example, findings, warnings

    command_entry = model.commands.get(example.command)
    if command_entry is None:
        policy = str(settings.get("unknown_command_policy", "warn"))
        message = f"unknown command: {example.command}"
        if policy == "fail":
            findings.append(Finding(example.path, example.cell_index, message))
        elif policy == "warn":
            warnings.append(f"{example.path}: cell {example.cell_index}: {message}")
        return example, findings, warnings

    if example.subcommand is not None and example.subcommand not in command_entry.subcommands:
        findings.append(
            Finding(
                example.path,
                example.cell_index,
                f"unknown subcommand for {example.command}: {example.subcommand}",
            )
        )
        return example, findings, warnings

    if (
        command_entry.subcommands
        and example.subcommand is None
        and not example.is_help
        and settings.get("fail_on_invalid_known_command", True)
    ):
        findings.append(
            Finding(
                example.path,
                example.cell_index,
                f"missing subcommand for {example.command}",
            )
        )
        return example, findings, warnings

    entry = entry_for(example, model)
    if entry is None:
        findings.append(
            Finding(
                example.path,
                example.cell_index,
                f"missing registry entry for {example.command_display()}",
            )
        )
        return example, findings, warnings

    classification = classify_example(example, entry)
    example = CommandExample(
        path=example.path,
        cell_index=example.cell_index,
        command=example.command,
        subcommand=example.subcommand,
        parts=example.parts,
        flags=example.flags,
        source_kind=example.source_kind,
        is_help=example.is_help,
        classification=classification,
    )

    if settings.get("safe_help_only", False) and not example.is_help:
        findings.append(
            Finding(
                example.path,
                example.cell_index,
                f"non-help example is not allowed when safe_help_only is true: {example.command_display()}",
            )
        )

    if example.is_help:
        return example, findings, warnings

    flag_names = example.flag_names()
    known_flags = set(command_entry.flags) | set(entry.flags) | {"--help"}
    for flag in sorted(flag_names):
        if flag in entry.unsupported_flags:
            findings.append(
                Finding(
                    example.path,
                    example.cell_index,
                    f"unsupported flag for {example.command_display()}: {flag}",
                )
            )
        elif settings.get("fail_on_invalid_known_flag", True) and flag not in known_flags:
            findings.append(
                Finding(
                    example.path,
                    example.cell_index,
                    f"unknown flag for {example.command_display()}: {flag}",
                )
            )

    for pattern in entry.unsupported_patterns:
        if unsupported_pattern_matches(pattern, example):
            findings.append(
                Finding(
                    example.path,
                    example.cell_index,
                    f"unsupported pattern for {example.command_display()}: {pattern}",
                )
            )

    for parsed in example.flags:
        flag = entry.flags.get(parsed.name) or command_entry.flags.get(parsed.name)
        if flag is None:
            continue
        if flag.kind == "boolean" and parsed.value is not None:
            findings.append(
                Finding(
                    example.path,
                    example.cell_index,
                    f"boolean flag for {example.command_display()} must not receive a value: {parsed.name}",
                )
            )
        if flag.kind == "value" and parsed.value is None:
            findings.append(
                Finding(
                    example.path,
                    example.cell_index,
                    f"value flag for {example.command_display()} is missing a value: {parsed.name}",
                )
            )
        if flag.allowed_values:
            for value in flag_values(example, parsed.name):
                if value == VALUE_PLACEHOLDER:
                    continue
                if settings.get("fail_on_invalid_flag_value", True) and value not in flag.allowed_values:
                    allowed = ", ".join(flag.allowed_values)
                    findings.append(
                        Finding(
                            example.path,
                            example.cell_index,
                            f"invalid value for {example.command_display()} {parsed.name}: {value} (allowed: {allowed})",
                        )
                    )

    if settings.get("fail_on_missing_argparse_required", True):
        for flag in sorted(required_flags(entry, "argparse_required") - flag_names):
            findings.append(
                Finding(
                    example.path,
                    example.cell_index,
                    f"missing argparse-required flag for {example.command_display()}: {flag}",
                )
            )

    if settings.get("fail_on_missing_notebook_contract_required", True):
        for flag in sorted(required_flags(entry, "notebook_contract_required") - flag_names):
            findings.append(
                Finding(
                    example.path,
                    example.cell_index,
                    f"missing notebook-contract-required flag for {example.command_display()}: {flag}",
                )
            )

    for name, flag in sorted(entry.flags.items()):
        if flag.required_when == "not_dry_run" and name not in flag_names and not has_dry_run(example):
            findings.append(
                Finding(
                    example.path,
                    example.cell_index,
                    f"missing conditionally required flag for {example.command_display()} when --dry-run is absent: {name}",
                )
            )

    return example, findings, warnings


def validate_targets(
    targets: list[Path],
    model: RegistryModel,
    settings: dict[str, Any],
) -> ValidationReport:
    report = ValidationReport(targets_checked=len(targets))
    for target in targets:
        examples, findings = extract_examples(target, model, settings)
        report.findings.extend(findings)
        for raw_example in examples:
            example, example_findings, example_warnings = validate_example(raw_example, model, settings)
            report.examples.append(example)
            if example.command in model.commands:
                report.registry_examples_validated += 1
            report.findings.extend(example_findings)
            report.warnings.extend(example_warnings)

            if example.classification == "safe_help":
                report.safe_help_examples += 1
            elif example.classification == "safe_preview":
                report.safe_preview_examples += 1
            elif example.classification == "dry_run":
                report.dry_run_examples += 1
            elif example.classification == "manual_only_live":
                report.manual_only_live_examples += 1
            elif example.classification == "unsafe_live":
                report.unsafe_live_examples += 1
    return report


def format_finding(finding: Finding) -> str:
    if finding.path is None:
        return finding.reason
    if finding.cell_index is None:
        return f"{finding.path}: {finding.reason}"
    return f"{finding.path}: cell {finding.cell_index}: {finding.reason}"


def print_report(report: ValidationReport) -> None:
    print("Notebook CLI registry validation report:")
    print(f"- notebook targets checked: {report.targets_checked}")
    print(f"- command examples found: {len(report.examples)}")
    print(f"- registry command examples validated: {report.registry_examples_validated}")
    print(f"- safe help examples: {report.safe_help_examples}")
    print(f"- safe preview examples: {report.safe_preview_examples}")
    print(f"- dry-run examples: {report.dry_run_examples}")
    print(f"- manual-only live examples: {report.manual_only_live_examples}")
    print(f"- unsafe live examples: {report.unsafe_live_examples}")

    if report.examples:
        print("- examples:")
        for example in report.examples:
            flags = " ".join(sorted(example.flag_names())) or "<none>"
            print(
                f"  - {example.path}: cell {example.cell_index}: "
                f"{example.command_display()} [{example.source_kind}] "
                f"classification={example.classification} flags={flags}"
            )

    if report.warnings:
        print("- warnings:")
        for warning in sorted(set(report.warnings)):
            print(f"  - {warning}")

    if report.findings:
        print("- failures:")
        for finding in report.findings:
            print(f"  - {format_finding(finding)}")
    else:
        print("- failures: none")


def resolve_registry_path(config_path: Path, settings: dict[str, Any]) -> Path:
    registry_path = Path(str(settings.get("registry_path", "")))
    if not registry_path:
        raise RuntimeError("notebook_cli_registry.registry_path is required")
    if registry_path.is_absolute():
        return registry_path
    candidate = config_path.parent / registry_path
    if candidate.exists():
        return candidate
    return Path.cwd() / registry_path


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    try:
        config = load_toml(config_path)
        settings = config.get("notebook_cli_registry", {})
        if not isinstance(settings, dict):
            raise RuntimeError("Missing [notebook_cli_registry] config section.")
        registry = load_toml(resolve_registry_path(config_path, settings))
        model = build_registry_model(registry)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    targets = args.targets or settings.get("default_targets", [])
    if not targets:
        print("No notebook targets provided and config default_targets is empty.", file=sys.stderr)
        return 2

    report = validate_targets([Path(target) for target in targets], model, settings)
    print_report(report)
    return 1 if report.findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
