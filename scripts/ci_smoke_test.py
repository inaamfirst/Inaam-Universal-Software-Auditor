#!/usr/bin/env python3
"""Run dependency-free smoke tests for the reusable audit helper scripts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REQUIRED_DOCUMENTS = [
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


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(script), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"{script.name} failed with exit code {result.returncode}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def run_validator_expect_failure(script: Path, directory: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(script), str(directory)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        raise AssertionError("The documentation validator accepted an invalid fixture")
    return result


def test_inventory(inventory_script: Path, root: Path) -> None:
    sample = root / "inventory-sample"
    (sample / "node_modules").mkdir(parents=True)
    (sample / "main.py").write_text("print('sample')\n", encoding="utf-8")
    (sample / "requirements.txt").write_text("example-package==1.0\n", encoding="utf-8")
    (sample / "node_modules" / "ignored.js").write_text("ignored\n", encoding="utf-8")

    output = root / "inventory.json"
    run_script(inventory_script, str(sample), "--output", str(output))
    data = json.loads(output.read_text(encoding="utf-8"))

    assert "main.py" in data["candidate_entry_points"]
    assert {item["path"] for item in data["manifests"]} == {"requirements.txt"}
    assert "node_modules" in data["observed_excluded_directories"]
    assert data["file_count"] == 2, data["files"]
    assert all(not item["path"].startswith("node_modules/") for item in data["files"])


def test_documentation_validator(validator_script: Path, root: Path) -> None:
    fixture = root / "documentation-fixture"
    fixture.mkdir()
    for name in REQUIRED_DOCUMENTS:
        content = "# Temporary audit fixture\n\nEvidence: fixture-only verification.\n"
        if name == "COMPLETE_FEATURE_INVENTORY.md":
            content += "\nStatus: IMPLEMENTED\n"
        (fixture / name).write_text(content, encoding="utf-8")

    run_script(validator_script, str(fixture))

    invalid_document = fixture / "PROJECT_OVERVIEW.md"
    invalid_document.write_text("", encoding="utf-8")
    result = run_validator_expect_failure(validator_script, fixture)
    combined_output = result.stdout + result.stderr
    assert "empty: PROJECT_OVERVIEW.md" in combined_output, combined_output


def main() -> int:
    scripts_dir = Path(__file__).resolve().parent
    inventory_script = scripts_dir / "inventory_project.py"
    validator_script = scripts_dir / "validate_audit_docs.py"
    with tempfile.TemporaryDirectory(prefix="inaam-auditor-ci-") as temporary:
        root = Path(temporary)
        test_inventory(inventory_script, root)
        test_documentation_validator(validator_script, root)
    print("CI smoke tests passed: inventory and documentation validator behavior verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
