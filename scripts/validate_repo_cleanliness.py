"""Run repository validation guardrails for secrets and notebook outputs."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run repository cleanliness validation checks.",
        epilog="Usage: python scripts/validate_repo_cleanliness.py .",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Repository root to validate. Defaults to the current directory.",
    )
    return parser.parse_args()


def run_check(script: Path, target: Path) -> int:
    print(f"\nRunning {script.name} {target}")
    result = subprocess.run([sys.executable, str(script), str(target)], check=False)
    return result.returncode


def main() -> int:
    args = parse_args()
    root = Path(args.path)
    if not root.exists():
        print(f"Path does not exist: {root}", file=sys.stderr)
        return 2

    script_dir = Path(__file__).resolve().parent
    failures = 0
    checks = [
        (script_dir / "scan_for_secret_patterns.py", root),
        (
            script_dir / "check_notebooks_no_outputs.py",
            (root / "notebooks") if (root / "notebooks").exists() else root,
        ),
    ]
    for script, target in checks:
        return_code = run_check(script, target)
        if return_code != 0:
            failures += 1

    if failures:
        print(f"\nRepository validation failed: {failures} check(s) failed.")
        return 1

    print("\nRepository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
