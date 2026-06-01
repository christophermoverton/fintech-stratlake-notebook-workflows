"""Scan repository text files for likely secrets and credential dumps."""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_SUFFIXES = {
    ".ipynb",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

SKIP_DIRS = {
    ".git",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
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

SAFE_PLACEHOLDER_NAMES = {
    "ALPACA_API_KEY_ID",
    "ALPACA_API_SECRET_KEY",
    "ALPACA_DATA_BASE_URL",
    "ALPACA_FEED",
}

PRIVATE_KEY_MARKERS = (
    "PRIVATE" + " KEY",
    "BEGIN " + "RSA " + "PRIVATE" + " KEY",
    "BEGIN " + "OPENSSH " + "PRIVATE" + " KEY",
)

ALPACA_ENV_ASSIGNMENT = re.compile(
    r"\b(ALPACA_API_KEY_ID|ALPACA_API_SECRET_KEY)\s*=\s*([^\s#]+)"
)
ALPACA_OS_LITERAL_ASSIGNMENT = re.compile(
    r"os\.environ\[\s*[\"'](ALPACA_API_KEY_ID|ALPACA_API_SECRET_KEY)[\"']\s*\]"
    r"\s*=\s*[\"']([^\"']{4,})[\"']"
)
GENERIC_SECRET_LITERAL_ASSIGNMENT = re.compile(
    r"\b(api_secret|secret_key|password|token)\b\s*[:=]\s*[\"']([^\"']{8,})[\"']",
    re.IGNORECASE,
)
BEARER_TOKEN = re.compile(
    r"\bAuthorization\s*:\s*Bearer\s+([A-Za-z0-9._~+/\-]{8,})",
    re.IGNORECASE,
)
ENV_DUMP_SECRET_VALUE = re.compile(
    r"[\"']?([A-Z0-9_]*(?:SECRET|TOKEN|PASSWORD|CREDENTIAL)[A-Z0-9_]*)[\"']?"
    r"\s*[:=]\s*[\"']?([^\"'\s,}]{8,})",
    re.IGNORECASE,
)
TOKEN_LIKE_STRING = re.compile(
    r"(?<![A-Za-z0-9_])[A-Za-z0-9][A-Za-z0-9._~+/\-]{31,}(?![A-Za-z0-9_])"
)


@dataclass(frozen=True)
class Finding:
    path: Path
    line_number: int
    reason: str
    sample: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan text-like repository files for likely secrets.",
        epilog="Usage: python scripts/scan_for_secret_patterns.py .",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="File or directory to scan. Defaults to the current directory.",
    )
    return parser.parse_args()


def is_text_like(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


def iter_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if is_text_like(root) else []

    files: list[Path] = []
    for current_root, dirs, filenames in os.walk(root):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        current_path = Path(current_root)
        for filename in filenames:
            path = current_path / filename
            if is_text_like(path):
                files.append(path)
    return sorted(files)


def redact(value: str) -> str:
    value = value.strip().strip("\"'")
    if len(value) <= 8:
        return "<redacted>"
    return f"{value[:4]}...{value[-2:]}"


def is_safe_placeholder_reference(line: str) -> bool:
    stripped = line.strip()
    return stripped in SAFE_PLACEHOLDER_NAMES


def is_variable_or_approved_placeholder(value: str) -> bool:
    cleaned = value.strip().strip("\"',}")
    if cleaned in SAFE_PLACEHOLDER_NAMES:
        return True
    if cleaned.startswith(("bool(", "re.", "re(", "Path(")):
        return True
    if re.fullmatch(r"[a-z_][a-z0-9_]*", cleaned):
        return True
    if cleaned.startswith("get_secret_or_prompt("):
        return True
    return False


def is_approved_placeholder_value(value: str) -> bool:
    return value.strip().strip("\"',}") in SAFE_PLACEHOLDER_NAMES


def looks_like_token(value: str) -> bool:
    if value in SAFE_PLACEHOLDER_NAMES:
        return False
    if value.startswith(("http://", "https://")):
        return False
    if value.startswith(("/content/", "content/")) or value.lower().endswith(".ipynb"):
        return False
    if value == value.lower():
        return False
    has_letter = bool(re.search(r"[A-Za-z]", value))
    has_digit = bool(re.search(r"\d", value))
    has_mixed_case = bool(re.search(r"[a-z]", value)) and bool(re.search(r"[A-Z]", value))
    has_token_symbol = bool(re.search(r"[._~+/\-]", value))
    return has_letter and has_digit and (has_mixed_case or has_token_symbol)


def scan_line(path: Path, line_number: int, line: str) -> list[Finding]:
    findings: list[Finding] = []

    if is_safe_placeholder_reference(line):
        return findings

    alpaca_assignment = ALPACA_ENV_ASSIGNMENT.search(line)
    if alpaca_assignment:
        value = alpaca_assignment.group(2)
        if not is_approved_placeholder_value(value):
            findings.append(
                Finding(
                    path,
                    line_number,
                    "literal Alpaca environment assignment",
                    redact(value),
                )
            )

    os_literal = ALPACA_OS_LITERAL_ASSIGNMENT.search(line)
    if os_literal:
        findings.append(
            Finding(
                path,
                line_number,
                "literal os.environ Alpaca credential assignment",
                redact(os_literal.group(2)),
            )
        )

    generic_assignment = GENERIC_SECRET_LITERAL_ASSIGNMENT.search(line)
    if generic_assignment:
        value = generic_assignment.group(2)
        if not is_approved_placeholder_value(value):
            findings.append(
                Finding(
                    path,
                    line_number,
                    f"literal {generic_assignment.group(1)} assignment",
                    redact(value),
                )
            )

    bearer = BEARER_TOKEN.search(line)
    if bearer:
        findings.append(
            Finding(path, line_number, "bearer token value", redact(bearer.group(1)))
        )

    for marker in PRIVATE_KEY_MARKERS:
        if marker in line:
            findings.append(Finding(path, line_number, f"private key marker: {marker}"))

    env_dump = ENV_DUMP_SECRET_VALUE.search(line)
    if env_dump:
        value = env_dump.group(2)
        if not is_variable_or_approved_placeholder(value):
            findings.append(
                Finding(
                    path,
                    line_number,
                    f"credential-looking environment dump: {env_dump.group(1)}",
                    redact(value),
                )
            )

    for token_match in TOKEN_LIKE_STRING.finditer(line):
        value = token_match.group(0)
        if looks_like_token(value):
            findings.append(
                Finding(path, line_number, "token-like long string", redact(value))
            )

    return findings


def scan_file(path: Path) -> list[Finding]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        try:
            lines = path.read_text(encoding="utf-8-sig").splitlines()
        except UnicodeDecodeError:
            return [
                Finding(
                    path,
                    0,
                    "could not decode text-like file as UTF-8",
                )
            ]

    findings: list[Finding] = []
    for index, line in enumerate(lines, start=1):
        findings.extend(scan_line(path, index, line))
    return findings


def format_finding(finding: Finding) -> str:
    location = str(finding.path)
    if finding.line_number:
        location = f"{location}:{finding.line_number}"
    message = f"{location}: {finding.reason}"
    if finding.sample:
        message = f"{message} ({finding.sample})"
    return message


def main() -> int:
    args = parse_args()
    root = Path(args.path)
    if not root.exists():
        print(f"Path does not exist: {root}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    for path in iter_files(root):
        findings.extend(scan_file(path))

    if findings:
        print("Secret pattern scan failed:")
        for finding in findings:
            print(f"- {format_finding(finding)}")
        return 1

    print("Secret pattern scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
