# Changelog

## Unreleased

- Added GitHub Actions CI for pushes to `main`, pull requests targeting `main`, and manual runs.
- Added a Python 3.10–3.13 test matrix with structural, frontmatter, compilation, and helper smoke checks.
- Added `scripts/ci_smoke_test.py` to verify inventory behavior and documentation-validator success/failure behavior using temporary fixtures.
- Documented local CI smoke-test execution in `README.md`.

## 2026-11-02 — GitHub-ready package prepared

- Packaged the latest validated global installation as `inaam-universal-software-auditor`.
- Preserved `SKILL.md`, `agents/openai.yaml`, all references, and reusable Python scripts.
- Added portable README documentation for global and project-specific Codex installation.
- Added repository hygiene rules in `.gitignore`.
- Removed Python cache files, generated audit reports, temporary files, local absolute paths, credentials, tokens, and secrets from the publishable package.
- No remote repository was created and no files were pushed.
