from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

if sys.version_info < (3, 11):  # pragma: no cover - Python < 3.11
    pytest.skip(
        "Python 3.11+ is required for TOML-based notebook execution tests.",
        allow_module_level=True,
    )

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None  # type: ignore[assignment]


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_NOTEBOOK = REPO_ROOT / "notebooks" / "00_setup_and_storage_overview.ipynb"
EXECUTION_CONFIG = REPO_ROOT / "config" / "notebook_execution_test.toml"
READINESS_CONFIG = REPO_ROOT / "config" / "notebook_test.toml"


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_toml(path: Path) -> dict:
    if tomllib is None:
        raise AssertionError("Python 3.11 or newer is required for TOML parsing.")
    return tomllib.loads(path.read_text(encoding="utf-8"))


def notebook_code_cells(nb) -> list:
    return [cell for cell in nb.cells if cell.get("cell_type") == "code"]


def cell_source(cell) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    return str(source)


def assert_source_notebook_clean(path: Path) -> None:
    nb = nbformat.read(path, as_version=4)
    for index, cell in enumerate(notebook_code_cells(nb)):
        assert cell.get("outputs", []) == [], f"cell {index} has outputs"
        assert cell.get("execution_count") is None, f"cell {index} has execution_count"


def should_skip_cell(source: str, config: dict) -> bool:
    if any(line.lstrip().startswith(("!", "%")) for line in source.splitlines()):
        return True
    if ".mkdir" in source:
        return True
    patterns = config["skip_patterns"]["cell_source_contains"]
    return any(pattern in source for pattern in patterns)


def safe_prefix_lines(source: str) -> list[str]:
    if ".mkdir" in source:
        return []

    safe_lines: list[str] = []
    for line in source.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("!", "%")):
            break
        if "import " in stripped or "from " in stripped:
            break
        if re.match(r"^[A-Z_][A-Z0-9_]*\s*=", stripped) and not any(
            token in line for token in ("os.environ", "userdata", "getpass")
        ):
            safe_lines.append(line)
            continue
        if stripped == "":
            safe_lines.append(line)
            continue
        break
    return safe_lines


def sanitized_code_cell(source: str):
    prefix = safe_prefix_lines(source)
    if prefix:
        cleaned_source = "\n".join(prefix).strip() + "\n"
    else:
        cleaned_source = "# Skipped by pytest sanitized notebook execution harness.\n"
    return nbformat.v4.new_code_cell(source=cleaned_source)


def build_sanitized_notebook(source_path: Path, config: dict):
    source_nb = nbformat.read(source_path, as_version=4)
    sanitized = nbformat.v4.new_notebook()
    sanitized.metadata = {
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"},
    }

    skipped = 0
    kept_code = 0
    for cell in source_nb.cells:
        if cell.get("cell_type") == "markdown":
            sanitized.cells.append(nbformat.v4.new_markdown_cell(source=cell.get("source", "")))
            continue
        if cell.get("cell_type") != "code":
            continue

        source = cell_source(cell)
        if should_skip_cell(source, config):
            sanitized.cells.append(sanitized_code_cell(source))
            skipped += 1
        else:
            sanitized.cells.append(nbformat.v4.new_code_cell(source=source))
            kept_code += 1

    return sanitized, skipped, kept_code


def test_notebook_00_exists_and_loads_with_nbformat():
    assert SOURCE_NOTEBOOK.exists()
    nb = nbformat.read(SOURCE_NOTEBOOK, as_version=4)
    assert nb.nbformat == 4
    assert nb.cells


def test_notebook_00_source_is_output_free_and_unexecuted():
    assert_source_notebook_clean(SOURCE_NOTEBOOK)


def test_issue_14_readiness_command_remains_compatible():
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate_notebook_execution_readiness.py"),
            "--config",
            str(READINESS_CONFIG),
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_notebook_00_sanitized_execution_does_not_mutate_source(tmp_path):
    config = load_toml(EXECUTION_CONFIG)
    execution = config["notebook_execution"]
    assert execution["execute_sanitized_copy"] is True
    assert execution["full_notebook_execution_enabled"] is False
    assert execution["write_outputs_to_source"] is False

    before = file_digest(SOURCE_NOTEBOOK)
    source_nb = nbformat.read(SOURCE_NOTEBOOK, as_version=4)
    sanitized, skipped, kept_code = build_sanitized_notebook(SOURCE_NOTEBOOK, config)

    assert skipped > 0
    assert kept_code > 0

    sanitized_path = tmp_path / "00_setup_and_storage_overview.sanitized.ipynb"
    nbformat.write(sanitized, sanitized_path)

    client = NotebookClient(
        sanitized,
        timeout=execution["timeout_seconds"],
        allow_errors=execution["allow_errors"],
        resources={"metadata": {"path": str(tmp_path)}},
    )
    executed = client.execute()

    executed_path = tmp_path / "00_setup_and_storage_overview.executed.ipynb"
    nbformat.write(executed, executed_path)

    after = file_digest(SOURCE_NOTEBOOK)
    assert before == after
    assert_source_notebook_clean(SOURCE_NOTEBOOK)

    source_outputs = sum(len(cell.get("outputs", [])) for cell in notebook_code_cells(source_nb))
    assert source_outputs == 0
    assert sanitized_path.exists()
    assert executed_path.exists()
