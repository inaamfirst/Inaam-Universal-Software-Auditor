#!/usr/bin/env python3
"""Create a deterministic, secret-safe project inventory for software audits."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

DEFAULT_EXCLUDES = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    "coverage",
    "target",
    ".next",
    ".gradle",
    ".dart_tool",
    "release_builds",
}

MANIFEST_NAMES = {
    "package.json": "npm",
    "package-lock.json": "npm-lock",
    "pnpm-lock.yaml": "pnpm-lock",
    "yarn.lock": "yarn-lock",
    "pyproject.toml": "python",
    "requirements.txt": "python-requirements",
    "requirements-dev.txt": "python-requirements",
    "go.mod": "go",
    "Cargo.toml": "rust",
    "composer.json": "php",
    "Gemfile": "ruby",
    "pubspec.yaml": "flutter-dart",
    "build.gradle": "gradle",
    "build.gradle.kts": "gradle-kotlin",
    "pom.xml": "maven",
    "Podfile": "cocoapods",
    "Dockerfile": "docker",
    "docker-compose.yml": "compose",
    "docker-compose.yaml": "compose",
    "Makefile": "make",
}

TEXT_SUFFIXES = {
    ".c", ".cc", ".cpp", ".cs", ".dart", ".go", ".h", ".hpp", ".html",
    ".java", ".js", ".jsx", ".json", ".kt", ".m", ".mm", ".php", ".py",
    ".rb", ".rs", ".sql", ".swift", ".toml", ".ts", ".tsx", ".vue", ".xml",
    ".yaml", ".yml", ".ini", ".cfg", ".conf", ".md", ".txt", ".sh", ".ps1",
}

ENTRY_NAMES = {
    "main.py", "app.py", "manage.py", "main.ts", "main.tsx", "index.ts",
    "index.tsx", "main.js", "index.js", "main.dart", "App.tsx", "App.jsx",
    "Program.cs", "Main.java", "main.go", "main.rs", "server.js", "wsgi.py",
}

INTEGRATION_TERMS = {
    "stripe": "payments",
    "paypal": "payments",
    "firebase": "firebase",
    "sentry": "monitoring",
    "redis": "cache/queue",
    "celery": "background jobs",
    "rabbitmq": "messaging",
    "kafka": "messaging",
    "smtp": "email",
    "twilio": "messaging",
    "s3": "object storage",
    "aws": "cloud provider",
    "azure": "cloud provider",
    "gcp": "cloud provider",
    "postgres": "database",
    "mysql": "database",
    "sqlite": "database",
    "mongodb": "database",
    "sqlalchemy": "database ORM",
    "firebase": "backend service",
}

ENV_RE = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")
SECRET_NAME_RE = re.compile(r"(?:KEY|TOKEN|SECRET|PASSWORD|PASSWD|PRIVATE|CREDENTIAL)", re.I)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Project root to inventory")
    parser.add_argument("--output", type=Path, help="JSON output path; stdout when omitted")
    parser.add_argument("--include-generated", action="store_true", help="Include default generated/vendor directories")
    parser.add_argument("--exclude", action="append", default=[], help="Additional directory name to exclude")
    return parser.parse_args()


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_binary(path: Path) -> bool:
    try:
        sample = path.read_bytes()[:2048]
    except OSError:
        return True
    return b"\x00" in sample


def safe_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def file_digest(path: Path) -> str | None:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Project root is not a directory: {root}")

    excludes = set(args.exclude) | (set() if args.include_generated else DEFAULT_EXCLUDES)
    files: list[dict[str, object]] = []
    manifests: list[dict[str, str]] = []
    entries: list[str] = []
    env_names: set[str] = set()
    integration_hits: dict[str, set[str]] = {}
    language_counts: Counter[str] = Counter()
    excluded_paths: set[str] = set()

    for path in sorted(root.rglob("*"), key=lambda p: p.as_posix().lower()):
        if not path.is_file():
            continue
        parts = path.relative_to(root).parts
        excluded = next((part for part in parts if part in excludes), None)
        if excluded:
            excluded_paths.add(excluded)
            continue

        rel = relative(path, root)
        suffix = path.suffix.lower()
        record: dict[str, object] = {
            "path": rel,
            "size": path.stat().st_size,
            "suffix": suffix,
        }
        digest = file_digest(path)
        if digest:
            record["sha256"] = digest
        files.append(record)

        if path.name in MANIFEST_NAMES:
            manifests.append({"path": rel, "type": MANIFEST_NAMES[path.name]})
        if path.name in ENTRY_NAMES:
            entries.append(rel)

        language = suffix.lstrip(".") or "extensionless"
        if path.name in {"Dockerfile", "Makefile", "Gemfile"}:
            language = path.name.lower()
        language_counts[language] += 1

        if suffix in TEXT_SUFFIXES and path.stat().st_size <= 2 * 1024 * 1024 and not is_binary(path):
            content = safe_text(path)
            for name in ENV_RE.findall(content):
                if SECRET_NAME_RE.search(name):
                    env_names.add(name)
            lowered = content.lower()
            for term, category in INTEGRATION_TERMS.items():
                if term in lowered:
                    integration_hits.setdefault(category, set()).add(rel)

    result = {
        "schema_version": 1,
        "project_root": str(root),
        "excluded_directory_names": sorted(excludes),
        "observed_excluded_directories": sorted(excluded_paths),
        "file_count": len(files),
        "files": files,
        "languages_by_extension": dict(sorted(language_counts.items())),
        "manifests": sorted(manifests, key=lambda item: item["path"]),
        "candidate_entry_points": sorted(set(entries)),
        "environment_variable_names": sorted(env_names),
        "integration_candidates": {
            category: sorted(paths) for category, paths in sorted(integration_hits.items())
        },
    }

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
