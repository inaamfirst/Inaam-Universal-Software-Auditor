#!/usr/bin/env python3
"""Validate the required, evidence-bearing audit documentation set."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED = [
    "PROJECT_OVERVIEW.md",
    "COMPLETE_FEATURE_INVENTORY.md",
    "ARCHITECTURE.md",
    "TECH_STACK.md",
    "DATABASE_SCHEMA.md",
    "API_REFERENCE.md",
    "MODULES.md",
    "DATA_FLOW.md",
    "SECURITY_AUDIT.md",
    "DEPLOYMENT_GUIDE.md",
    "INSTALLATION_GUIDE.md",
    "USER_GUIDE.md",
    "DEVELOPER_GUIDE.md",
    "TEST_COVERAGE.md",
    "KNOWN_ISSUES.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "COMPLETE_SOFTWARE_REFERENCE.md",
]
STATUSES = {
    "IMPLEMENTED",
    "PARTIALLY_IMPLEMENTED",
    "BACKEND_ONLY",
    "CONFIGURATION_DEPENDENT",
    "NOT_IMPLEMENTED",
    "BROKEN",
    "UNVERIFIED",
}
EVIDENCE_RE = re.compile(r"\b(?:SOURCE_VERIFIED|TEST_VERIFIED|RUNTIME_VERIFIED|INFERRED|UNKNOWN|Evidence|Source|Verification)\b", re.I)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Audit documentation directory")
    args = parser.parse_args()
    directory = args.directory.expanduser().resolve()
    errors: list[str] = []

    for name in REQUIRED:
        path = directory / name
        if not path.is_file():
            errors.append(f"missing: {name}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace").strip()
        if not text:
            errors.append(f"empty: {name}")
        elif not EVIDENCE_RE.search(text):
            errors.append(f"no evidence marker: {name}")

    inventory = directory / "COMPLETE_FEATURE_INVENTORY.md"
    if inventory.is_file():
        text = inventory.read_text(encoding="utf-8", errors="replace")
        found = set(re.findall(r"\b[A-Z][A-Z_]+\b", text)) & STATUSES
        if not found:
            errors.append("feature inventory contains no recognized status")

    if errors:
        print("Audit documentation validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print(f"Audit documentation valid: {len(REQUIRED)} required files checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
