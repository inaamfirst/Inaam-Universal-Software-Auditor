# Inaam's Universal Software Auditor

`inaam-universal-software-auditor` is a reusable Codex Agent Skill for evidence-based software discovery, technical auditing, feature tracing, architecture analysis, and documentation generation.

It is designed to work across web, desktop, mobile, Flutter, offline/local-first, server-hosted, SaaS, REST API, backend, and hybrid projects.

## What it does

The Skill recursively inspects project source, manifests, configuration, tests, databases, APIs, integrations, deployment files, and existing documentation. It distinguishes source-verified, test-verified, runtime-verified, inferred, and unknown findings, and records confidence and evidence paths where practical.

It can produce a structured `docs/software-audit/` reference containing project overview, feature inventory, architecture, technology stack, database schema, API reference, modules, data flows, security, deployment, installation, user/developer guides, test coverage, known issues, roadmap, changelog, and a consolidated reference.

The Skill is an audit and documentation system. It does not refactor application code, run migrations, deploy services, alter production configuration, or expose secrets.

## Audit modes

### FULL AUDIT

Performs complete project discovery and generates the full audit documentation set. Use this for a new project or when no audit exists.

```text
Use $inaam-universal-software-auditor in FULL AUDIT mode on <project-root> and write the audit to docs/software-audit/.
```

### INCREMENTAL AUDIT

Compares current source and evidence with an existing `docs/software-audit/` directory, updates changed findings, preserves user-authored documentation, and records changes in the audit changelog.

```text
Use $inaam-universal-software-auditor in INCREMENTAL AUDIT mode on <project-root>.
```

### FEATURE AUDIT

Traces one feature through UI/client code, business logic, persistence, APIs, integrations, configuration, tests, and deployment without implying a project-wide audit.

```text
Use $inaam-universal-software-auditor in FEATURE AUDIT mode to trace <feature> in <project-root>.
```

The same canonical identifier may appear as `/inaam-universal-software-auditor` in clients that expose skills through slash commands.

## Installation in Codex

### Global installation

Copy the complete repository folder into the global skills directory used by your Codex client:

```powershell
$source = (Get-Location).Path
$destination = Join-Path $env:USERPROFILE '.agents\skills\inaam-universal-software-auditor'
if (Test-Path -LiteralPath $destination) {
  throw "Destination already exists; compare it before replacing it."
}
New-Item -ItemType Directory -Force -Path (Split-Path $destination) | Out-Null
New-Item -ItemType Directory -Path $destination | Out-Null
Get-ChildItem -LiteralPath $source -Force |
  Where-Object { $_.Name -ne '.git' } |
  Copy-Item -Destination $destination -Recurse
```

If your client uses `CODEX_HOME`, install under `$CODEX_HOME/skills/inaam-universal-software-auditor` instead. Do not overwrite an existing skill without comparing it first.

### Project-specific installation

Place the complete folder inside the project when project-local skills are supported:

```text
<project-root>/.agents/skills/inaam-universal-software-auditor/
```

Project-local installation is useful when a team wants a pinned Skill version or repository-specific customization. Keep project-local instructions and audit output separate from the Skill package.

After installation, start a new Codex turn. Restart the Codex extension or VS Code only if the Skill does not appear in the client’s skill or slash-command menu.

## Helper scripts

Generate a deterministic, secret-safe project inventory:

```powershell
python scripts/inventory_project.py <project-root> --output <audit-dir>/project-inventory.json
```

Useful options are `--include-generated` and repeatable `--exclude DIRECTORY_NAME`.

Validate the required evidence-bearing audit documents:

```powershell
python scripts/validate_audit_docs.py <audit-dir>
```

The scripts are helpers; Codex performs the source analysis and documentation synthesis using `SKILL.md` and the linked references.

## Continuous integration

GitHub Actions validates every push to `main`, pull request targeting `main`, and manually dispatched workflow run. The workflow tests Python 3.10 through 3.13 and checks repository structure, dependency-free `SKILL.md` frontmatter, Python compilation, inventory behavior, successful documentation validation, and rejection of an invalid documentation fixture.

Run the same helper smoke tests locally with:

```powershell
python scripts/ci_smoke_test.py
```

The workflow is defined in `.github/workflows/validate-skill.yml` and uses only the official checkout and setup-python actions. It requires no third-party Python dependencies.

## Customization and extension

- Update `references/audit-workflow.md` for discovery or platform-specific workflow guidance.
- Update `references/evidence-schema.md` when adding evidence labels or feature-record fields.
- Update `references/document-contract.md` when changing the generated documentation set.
- Add deterministic, dependency-light helpers under `scripts/` when repeated analysis benefits from automation.
- Keep `agents/openai.yaml` display metadata aligned with the frontmatter name.
- Preserve the safety contract: redact secrets, preserve user-authored documentation, and avoid application mutations.

## Supported project types

- Web applications and SaaS platforms
- Desktop applications and Electron projects
- Android and iOS applications
- Flutter applications
- Offline/local-first systems
- Server-hosted applications and REST APIs
- Python, JavaScript/TypeScript, Java, Kotlin, C#, Go, Rust, PHP, Ruby, Swift, Dart, and mixed-language repositories
- Hybrid projects containing multiple clients, services, deployment modes, or workspaces

## Repository contents

```text
SKILL.md                         Core Codex instructions
agents/openai.yaml               UI metadata and invocation policy
references/                      Workflow, evidence, document, and safety guidance
scripts/                         Deterministic inventory and documentation validators
README.md                        Installation and usage guide
CHANGELOG.md                     Package history
.gitignore                       Repository hygiene rules
```

## Safety and evidence

The Skill never treats a README, comment, UI label, or roadmap item as proof that a feature exists. Findings must be traced to implementation evidence, actual test execution, safe runtime inspection, or explicitly marked inference/unknown status. Secrets and private data must never be printed.
