"""Validate notebook CLI examples against configured safe command contracts."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None  # type: ignore[assignment]


FLAG_RE = re.compile(r"(?<![\w-])--[A-Za-z0-9][A-Za-z0-9-]*")


@dataclass(frozen=True)
class CommandExample:
    path: Path
    cell_index: int
    command: str
    subcommand: str | None
    flags: set[str]
    source_kind: str
    is_help: bool = False

    def command_display(self) -> str:
        if self.subcommand:
            return f"{self.command} {self.subcommand}"
        return self.command


@dataclass(frozen=True)
class Finding:
    path: Path | None
    cell_index: int | None
    reason: str


@dataclass
class ValidationReport:
    targets_checked: int = 0
    examples: list[CommandExample] = field(default_factory=list)
    help_checks: int = 0
    warnings: list[str] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate notebook CLI examples against safe configured contracts.",
        epilog=(
            "Usage: python scripts/validate_notebook_cli_contracts.py "
            "--config config/notebook_cli_contracts.toml"
        ),
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Notebook files to validate. Defaults to config targets.",
    )
    parser.add_argument(
        "--config",
        default="config/notebook_cli_contracts.toml",
        help="TOML CLI contract config path.",
    )
    return parser.parse_args()


def load_config(path: Path) -> dict[str, Any]:
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


def command_contracts(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {entry["name"]: entry for entry in config.get("commands", [])}


def subcommand_contracts(config: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (entry["command"], entry["subcommand"]): entry
        for entry in config.get("command_subcommands", [])
    }


def normalize_shell_line(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("!"):
        stripped = stripped[1:].strip()
    return stripped.replace("\\\n", " ")


def tokenize_command(text: str) -> list[str]:
    try:
        return shlex.split(text, posix=False)
    except ValueError:
        return text.split()


def flags_from_parts(parts: list[str]) -> set[str]:
    return {part for part in parts if part.startswith("--")}


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

    return [block.replace("\\", " ") for block in blocks]


def parse_tokens(
    path: Path,
    cell_index: int,
    parts: list[str],
    source_kind: str,
    known_commands: set[str],
    contracts: dict[str, dict[str, Any]],
) -> CommandExample | None:
    if not parts:
        return None
    command = parts[0]
    if command not in known_commands:
        return None

    allowed_subcommands = set(contracts.get(command, {}).get("subcommands", []))
    subcommand: str | None = None
    rest = parts[1:]
    if allowed_subcommands and rest and not rest[0].startswith("-"):
        subcommand = rest[0]
        rest = rest[1:]

    flags = flags_from_parts(rest)
    is_help = "--help" in flags or "-h" in rest
    return CommandExample(path, cell_index, command, subcommand, flags, source_kind, is_help)


def extract_shell_examples(
    path: Path,
    cell_index: int,
    source: str,
    known_commands: set[str],
    contracts: dict[str, dict[str, Any]],
) -> list[CommandExample]:
    examples: list[CommandExample] = []
    for block in shell_command_blocks(source):
        parts = tokenize_command(normalize_shell_line(block))
        example = parse_tokens(path, cell_index, parts, "shell", known_commands, contracts)
        if example is not None:
            examples.append(example)
    return examples


def extract_preview_examples(
    path: Path,
    cell_index: int,
    source: str,
    known_commands: set[str],
    contracts: dict[str, dict[str, Any]],
) -> list[CommandExample]:
    examples: list[CommandExample] = []
    for command in sorted(known_commands):
        if command not in source:
            continue

        command_position = -1
        line_offset = 0
        for line in source.splitlines(keepends=True):
            stripped = line.lstrip()
            if stripped.startswith("#") or command not in line:
                line_offset += len(line)
                continue
            command_position = line_offset + line.find(command)
            break
        if command_position < 0:
            continue

        after_command = source[command_position + len(command) :]
        parts = [command]
        for token in re.findall(r"[A-Za-z0-9_-]+|--[A-Za-z0-9-]+", after_command):
            if token.startswith("--"):
                parts.append(token)
            elif not parts[1:] and token in contracts.get(command, {}).get("subcommands", []):
                parts.append(token)

        flags = set(FLAG_RE.findall(source[command_position:]))
        allowed_subcommands = set(contracts.get(command, {}).get("subcommands", []))
        subcommand = None
        text_after_command = source[command_position + len(command) :].lstrip()
        for candidate in allowed_subcommands:
            if text_after_command.startswith(candidate):
                subcommand = candidate
                break

        if not flags and subcommand is None:
            continue

        examples.append(
            CommandExample(
                path=path,
                cell_index=cell_index,
                command=command,
                subcommand=subcommand,
                flags=flags,
                source_kind="preview",
                is_help="--help" in flags,
            )
        )
    return examples


def extract_examples(path: Path, config: dict[str, Any]) -> tuple[list[CommandExample], list[Finding]]:
    findings: list[Finding] = []
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

    contracts = command_contracts(config)
    known_commands = set(contracts)
    examples: list[CommandExample] = []
    for cell_index, cell in enumerate(cells):
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        source = source_text(cell)
        shell_examples = extract_shell_examples(path, cell_index, source, known_commands, contracts)
        examples.extend(shell_examples)
        if not shell_examples:
            examples.extend(extract_preview_examples(path, cell_index, source, known_commands, contracts))

    return examples, findings


def validate_example(
    example: CommandExample,
    contracts: dict[str, dict[str, Any]],
    subcontracts: dict[tuple[str, str], dict[str, Any]],
) -> list[Finding]:
    findings: list[Finding] = []
    command_contract = contracts.get(example.command)
    if command_contract is None:
        return [Finding(example.path, example.cell_index, f"unknown command: {example.command}")]

    allowed_subcommands = set(command_contract.get("subcommands", []))
    if example.subcommand and example.subcommand not in allowed_subcommands:
        findings.append(
            Finding(
                example.path,
                example.cell_index,
                f"unknown subcommand for {example.command}: {example.subcommand}",
            )
        )

    if example.is_help:
        return findings

    if example.subcommand:
        contract = subcontracts.get((example.command, example.subcommand))
        if contract is None:
            findings.append(
                Finding(
                    example.path,
                    example.cell_index,
                    f"missing contract for {example.command} {example.subcommand}",
                )
            )
            return findings
    else:
        contract = command_contract

    required_flags = set(contract.get("required_flags", []))
    missing_flags = sorted(required_flags - example.flags)
    for flag in missing_flags:
        findings.append(
            Finding(
                example.path,
                example.cell_index,
                f"missing expected flag for {example.command_display()}: {flag}",
            )
        )

    known_flags = set(command_contract.get("required_flags", []))
    known_flags.update(command_contract.get("optional_flags", []))
    if example.subcommand:
        subcommand_contract = subcontracts.get((example.command, example.subcommand), {})
        known_flags.update(subcommand_contract.get("required_flags", []))
        known_flags.update(subcommand_contract.get("optional_flags", []))
    unknown_flags = sorted(flag for flag in example.flags if flag != "--help" and flag not in known_flags)
    for flag in unknown_flags:
        findings.append(
            Finding(
                example.path,
                example.cell_index,
                f"unknown flag for {example.command_display()}: {flag}",
            )
        )
    return findings


def help_commands(config: dict[str, Any]) -> list[tuple[str, ...]]:
    commands: list[tuple[str, ...]] = []
    for entry in config.get("commands", []):
        command = entry["name"]
        commands.append((command, "--help"))
    for entry in config.get("command_subcommands", []):
        commands.append((entry["command"], entry["subcommand"], "--help"))
    return commands


def run_help_checks(config: dict[str, Any], report: ValidationReport) -> None:
    settings = config.get("notebook_cli_contracts", {})
    if not settings.get("safe_help_only", True):
        report.findings.append(Finding(None, None, "safe_help_only must remain true"))
        return

    require_installed = bool(settings.get("require_installed_commands", False))
    allow_missing = bool(settings.get("allow_missing_commands", True))

    subcontracts = subcommand_contracts(config)
    contracts = command_contracts(config)
    for command_tuple in help_commands(config):
        executable = shutil.which(command_tuple[0])
        if executable is None:
            message = f"local command not installed, skipped help check: {command_tuple[0]}"
            if require_installed or not allow_missing:
                report.findings.append(Finding(None, None, message))
            elif message not in report.warnings:
                report.warnings.append(message)
            continue

        result = subprocess.run(
            [executable, *command_tuple[1:]],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        report.help_checks += 1
        if result.returncode != 0:
            report.findings.append(
                Finding(None, None, f"help command failed: {' '.join(command_tuple)}")
            )
            continue

        help_text = f"{result.stdout}\n{result.stderr}"
        if len(command_tuple) == 2:
            required_flags = set(contracts[command_tuple[0]].get("required_flags", []))
            display = command_tuple[0]
        else:
            required_flags = set(subcontracts.get((command_tuple[0], command_tuple[1]), {}).get("required_flags", []))
            display = f"{command_tuple[0]} {command_tuple[1]}"
        for flag in sorted(required_flags):
            if flag not in help_text:
                report.findings.append(Finding(None, None, f"help output missing {display} flag: {flag}"))


def validate_targets(targets: list[Path], config: dict[str, Any]) -> ValidationReport:
    report = ValidationReport(targets_checked=len(targets))
    contracts = command_contracts(config)
    subcontracts = subcommand_contracts(config)

    for target in targets:
        examples, findings = extract_examples(target, config)
        report.examples.extend(examples)
        report.findings.extend(findings)
        for example in examples:
            report.findings.extend(validate_example(example, contracts, subcontracts))

    run_help_checks(config, report)
    return report


def format_finding(finding: Finding) -> str:
    if finding.path is None:
        return finding.reason
    if finding.cell_index is None:
        return f"{finding.path}: {finding.reason}"
    return f"{finding.path}: cell {finding.cell_index}: {finding.reason}"


def print_report(report: ValidationReport) -> None:
    print("Notebook CLI contract validation report:")
    print(f"- notebook targets checked: {report.targets_checked}")
    print(f"- command examples found: {len(report.examples)}")
    print(f"- help-surface checks performed: {report.help_checks}")

    if report.examples:
        print("- examples:")
        for example in report.examples:
            flags = " ".join(sorted(example.flags)) or "<none>"
            print(
                f"  - {example.path}: cell {example.cell_index}: "
                f"{example.command_display()} [{example.source_kind}] flags={flags}"
            )

    if report.warnings:
        print("- warnings:")
        for warning in report.warnings:
            print(f"  - {warning}")

    if report.findings:
        print("- failures:")
        for finding in report.findings:
            print(f"  - {format_finding(finding)}")
    else:
        print("- failures: none")


def main() -> int:
    args = parse_args()
    try:
        config = load_config(Path(args.config))
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    targets = args.targets or config.get("notebook_cli_contracts", {}).get("default_targets", [])
    if not targets:
        print("No notebook targets provided and config default_targets is empty.", file=sys.stderr)
        return 2

    report = validate_targets([Path(target) for target in targets], config)
    print_report(report)
    return 1 if report.findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
