"""Validate that notebooks have no outputs or execution counts."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SKIP_DIRS = {
    ".git",
    ".ipynb_checkpoints",
    ".venv",
    "__pycache__",
    "archive",
    "archive_packs",
    "artifact",
    "artifacts",
    "archives",
    "colab_tmp",
    "content",
    "curated",
    "data",
    "drive",
    "feature_store",
    "features",
    "fintech-market-ingestion-demo",
    "marketlake",
    "MyDrive",
    "processed",
    "raw",
    "restore_packs",
    "sessions",
    "stratlake",
    "stratlake-trade-engine-demo",
    "tmp",
    "venv",
    "workspace",
    "workspaces",
}

SUSPICIOUS_OUTPUT_TERMS = (
    "ALPACA",
    "SECRET",
    "TOKEN",
    "PASSWORD",
    "Bearer",
    "os.environ",
)


@dataclass(frozen=True)
class Finding:
    path: Path
    cell_index: int | None
    reason: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check notebooks for outputs, execution counts, and unsafe output text.",
        epilog="Usage: python scripts/check_notebooks_no_outputs.py notebooks",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="notebooks",
        help="Notebook file or directory to scan. Defaults to notebooks.",
    )
    return parser.parse_args()


def iter_notebooks(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix.lower() == ".ipynb" else []
    if not root.exists():
        return []

    notebooks: list[Path] = []
    for current_root, dirs, filenames in os.walk(root):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        current_path = Path(current_root)
        for filename in filenames:
            path = current_path / filename
            if path.suffix.lower() == ".ipynb":
                notebooks.append(path)
    return sorted(notebooks)


def stringify_output(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(stringify_output(item) for item in value)
    if isinstance(value, dict):
        return "\n".join(stringify_output(item) for item in value.values())
    return str(value)


def output_text(output: dict[str, Any]) -> str:
    chunks: list[str] = []
    for key in ("name", "text", "ename", "evalue", "traceback"):
        chunks.append(stringify_output(output.get(key)))
    chunks.append(stringify_output(output.get("data")))
    return "\n".join(chunk for chunk in chunks if chunk)


def scan_notebook(path: Path) -> list[Finding]:
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [Finding(path, None, f"malformed notebook JSON: {exc}")]
    except UnicodeDecodeError as exc:
        return [Finding(path, None, f"could not decode notebook as UTF-8: {exc}")]

    cells = notebook.get("cells", [])
    if not isinstance(cells, list):
        return [Finding(path, None, "notebook JSON has no valid cells list")]

    findings: list[Finding] = []
    for cell_index, cell in enumerate(cells):
        if not isinstance(cell, dict):
            findings.append(Finding(path, cell_index, "cell is not a JSON object"))
            continue

        if cell.get("execution_count") is not None:
            findings.append(Finding(path, cell_index, "non-null execution_count"))

        outputs = cell.get("outputs", [])
        if outputs:
            findings.append(Finding(path, cell_index, "non-empty outputs"))

        if not isinstance(outputs, list):
            findings.append(Finding(path, cell_index, "outputs field is not a list"))
            continue

        for output in outputs:
            if not isinstance(output, dict):
                findings.append(Finding(path, cell_index, "output is not a JSON object"))
                continue
            if output.get("output_type") == "error" or output.get("traceback"):
                findings.append(Finding(path, cell_index, "traceback or error output"))

            text = output_text(output)
            upper_text = text.upper()
            for term in SUSPICIOUS_OUTPUT_TERMS:
                if term.upper() in upper_text:
                    findings.append(
                        Finding(
                            path,
                            cell_index,
                            f"output text contains suspicious term: {term}",
                        )
                    )
                    break

    return findings


def format_finding(finding: Finding) -> str:
    if finding.cell_index is None:
        return f"{finding.path}: {finding.reason}"
    return f"{finding.path}: cell {finding.cell_index}: {finding.reason}"


def main() -> int:
    args = parse_args()
    root = Path(args.path)
    if not root.exists():
        print(f"Path does not exist: {root}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    notebooks = iter_notebooks(root)
    for notebook in notebooks:
        findings.extend(scan_notebook(notebook))

    if findings:
        print("Notebook output check failed:")
        for finding in findings:
            print(f"- {format_finding(finding)}")
        return 1

    print(f"Notebook output check passed. Checked {len(notebooks)} notebook(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
