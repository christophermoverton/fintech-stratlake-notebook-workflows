"""Validate notebook execution readiness without executing notebook cells."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None  # type: ignore[assignment]


@dataclass(frozen=True)
class Finding:
    path: Path
    cell_index: int | None
    reason: str


@dataclass
class NotebookReport:
    path: Path
    code_cells: int = 0
    compiled_cells: int = 0
    skipped_cells: int = 0
    skip_reasons: dict[str, int] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Statically validate notebook execution readiness.",
        epilog=(
            "Usage: python scripts/validate_notebook_execution_readiness.py "
            "--config config/notebook_test.toml"
        ),
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Notebook files to validate. Defaults to config targets.",
    )
    parser.add_argument(
        "--config",
        default="config/notebook_test.toml",
        help="TOML validation config path.",
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


def is_shell_or_magic(source: str) -> bool:
    stripped = source.lstrip()
    if stripped.startswith(("!", "%")):
        return True
    return any(line.lstrip().startswith(("!", "%")) for line in source.splitlines())


def classify_cell(source: str, config: dict[str, Any]) -> list[str]:
    validation = config.get("notebook_validation", {})
    unsafe_patterns = config.get("unsafe_patterns", {}).get("cell_source_contains", [])
    reasons: list[str] = []

    if is_shell_or_magic(source):
        reasons.append("shell_or_magic")
    if "google.colab" in source:
        reasons.append("colab_only")
    if "drive.mount(" in source:
        reasons.append("drive_mount")
    if "userdata.get(" in source or "getpass.getpass(" in source:
        reasons.append("credential_or_prompt")
    if any(pattern in source for pattern in ("pip install", "requests.get(", "requests.post(")):
        reasons.append("network_or_package_install")
    artifact_patterns = (
        "!fintech-backup-data pack",
        "!fintech-backup-data restore",
        "!fintech-backfill",
        "!fintech-run",
        "!stratlake",
    )
    if any(pattern in source for pattern in artifact_patterns):
        reasons.append("artifact_or_upstream_command")

    for pattern in unsafe_patterns:
        if pattern in source:
            reasons.append(f"configured_pattern:{pattern}")

    if not validation.get("skip_shell_cells", True):
        reasons = [reason for reason in reasons if reason != "shell_or_magic"]
    if not validation.get("skip_colab_cells", True):
        reasons = [reason for reason in reasons if reason != "colab_only"]
    if not validation.get("skip_drive_mount_cells", True):
        reasons = [reason for reason in reasons if reason != "drive_mount"]
    if not validation.get("skip_credential_cells", True):
        reasons = [reason for reason in reasons if reason != "credential_or_prompt"]
    if not validation.get("skip_network_cells", True):
        reasons = [reason for reason in reasons if reason != "network_or_package_install"]
    if not validation.get("skip_artifact_commands", True):
        reasons = [reason for reason in reasons if reason != "artifact_or_upstream_command"]

    return list(dict.fromkeys(reasons))


def check_forbidden_paths(path: Path, raw_text: str, config: dict[str, Any]) -> list[Finding]:
    fragments = config.get("paths", {}).get("forbidden_committed_path_fragments", [])
    findings: list[Finding] = []
    for fragment in fragments:
        if fragment and fragment in raw_text:
            findings.append(Finding(path, None, f"forbidden path fragment: {fragment}"))
    return findings


def validate_notebook(path: Path, config: dict[str, Any]) -> NotebookReport:
    report = NotebookReport(path=path)
    validation = config.get("notebook_validation", {})

    try:
        raw_text = path.read_text(encoding="utf-8")
        notebook = json.loads(raw_text)
    except FileNotFoundError:
        report.findings.append(Finding(path, None, "notebook file does not exist"))
        return report
    except UnicodeDecodeError as exc:
        report.findings.append(Finding(path, None, f"could not decode as UTF-8: {exc}"))
        return report
    except json.JSONDecodeError as exc:
        report.findings.append(Finding(path, None, f"malformed notebook JSON: {exc}"))
        return report

    if not isinstance(notebook, dict):
        report.findings.append(Finding(path, None, "notebook JSON root is not an object"))
        return report

    cells = notebook.get("cells")
    if not isinstance(cells, list):
        report.findings.append(Finding(path, None, "notebook JSON has no valid cells list"))
        return report

    report.findings.extend(check_forbidden_paths(path, raw_text, config))

    for cell_index, cell in enumerate(cells):
        if not isinstance(cell, dict):
            report.findings.append(Finding(path, cell_index, "cell is not a JSON object"))
            continue
        if cell.get("cell_type") != "code":
            continue

        report.code_cells += 1

        outputs = cell.get("outputs", [])
        if validation.get("require_no_outputs", True) and outputs:
            report.findings.append(Finding(path, cell_index, "non-empty outputs"))
        if not isinstance(outputs, list):
            report.findings.append(Finding(path, cell_index, "outputs field is not a list"))

        if (
            validation.get("require_null_execution_counts", True)
            and cell.get("execution_count") is not None
        ):
            report.findings.append(Finding(path, cell_index, "non-null execution_count"))

        source = source_text(cell)
        skip_reasons = classify_cell(source, config)
        if skip_reasons:
            report.skipped_cells += 1
            for reason in skip_reasons:
                report.skip_reasons[reason] = report.skip_reasons.get(reason, 0) + 1
            continue

        if validation.get("compile_python_cells", True):
            try:
                compile(source, f"{path}:cell-{cell_index}", "exec")
                ast.parse(source)
            except SyntaxError as exc:
                report.findings.append(
                    Finding(
                        path,
                        cell_index,
                        f"Python syntax failure: {exc.msg} at line {exc.lineno}",
                    )
                )
            else:
                report.compiled_cells += 1

    return report


def format_finding(finding: Finding) -> str:
    if finding.cell_index is None:
        return f"{finding.path}: {finding.reason}"
    return f"{finding.path}: cell {finding.cell_index}: {finding.reason}"


def print_report(reports: list[NotebookReport]) -> None:
    total_code = sum(report.code_cells for report in reports)
    total_compiled = sum(report.compiled_cells for report in reports)
    total_skipped = sum(report.skipped_cells for report in reports)
    skip_reasons: dict[str, int] = {}
    findings: list[Finding] = []

    for report in reports:
        findings.extend(report.findings)
        for reason, count in report.skip_reasons.items():
            skip_reasons[reason] = skip_reasons.get(reason, 0) + count

    print("Notebook execution-readiness report:")
    print(f"- notebooks checked: {len(reports)}")
    print(f"- code cells checked: {total_code}")
    print(f"- code cells compiled: {total_compiled}")
    print(f"- code cells skipped: {total_skipped}")

    if skip_reasons:
        print("- skip reasons:")
        for reason, count in sorted(skip_reasons.items()):
            print(f"  - {reason}: {count}")

    if findings:
        print("- failures:")
        for finding in findings:
            print(f"  - {format_finding(finding)}")
    else:
        print("- failures: none")


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)

    try:
        config = load_config(config_path)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    validation = config.get("notebook_validation", {})
    targets = args.targets or validation.get("default_targets", [])
    if not targets:
        print("No notebook targets provided and config default_targets is empty.", file=sys.stderr)
        return 2

    smoke_enabled = bool(validation.get("smoke_execution_enabled", False))
    if smoke_enabled:
        print(
            "Smoke execution is not implemented in this safe readiness harness.",
            file=sys.stderr,
        )
        return 2

    reports = [validate_notebook(Path(target), config) for target in targets]
    print_report(reports)

    if any(report.findings for report in reports):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
