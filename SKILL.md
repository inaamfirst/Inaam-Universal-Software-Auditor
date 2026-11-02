---
name: inaam-universal-software-auditor
description: Audit software projects across languages, platforms, and deployment models, producing evidence-based architecture, feature, security, testing, and operational documentation without changing application code.
metadata:
  short-description: Evidence-based software audits and documentation
---

# Inaam's Universal Software Auditor

Use this skill when the user needs source-code discovery, a technical audit, a feature inventory, architecture documentation, or maintained software reference documentation. It applies to web, desktop, mobile, Flutter, offline/local-first, server, SaaS, API, and hybrid projects.

## Operating contract

- Treat source code, manifests, configuration, migrations, tests, build files, and executed commands as evidence.
- Never claim a feature exists because it appears only in a README, comment, roadmap, label, or unused route. Trace the implementation and record the evidence.
- Separate source-verified, test-verified, runtime-verified, inferred, and unknown findings. Include confidence when it helps the reader judge risk.
- Never print passwords, API keys, private tokens, cookies, private user data, or secret values. Record variable names and redacted locations only.
- Do not modify application source code, databases, production configuration, deployment settings, dependencies, or unrelated documentation. The only normal output is requested audit documentation and skill-owned working data.
- Read and obey project-local `AGENTS.md` or equivalent instructions before auditing. Preserve user-authored documentation and do not overwrite existing files without an explicit incremental-audit request.
- Never run migrations, destructive commands, production deployments, or services that can alter external state.

## Modes

Choose one mode from the user request:

- **FULL AUDIT**: discover the project recursively, build the evidence index, inspect all relevant layers, run safe checks where practical, and produce the complete documentation set.
- **INCREMENTAL AUDIT**: compare current source and inventory evidence with `docs/software-audit/`, update only changed audit sections, preserve user-authored material, and record what changed.
- **FEATURE AUDIT**: trace one named feature through UI, business logic, persistence, APIs, integrations, tests, configuration, and deployment. Do not imply a project-wide audit.

If the mode is not stated, use FULL AUDIT for a new project and INCREMENTAL AUDIT when the target audit directory already exists. If a feature name is supplied, use FEATURE AUDIT unless the user explicitly asks for a full audit.

Read the relevant supporting guidance before writing output:

- [Audit workflow](references/audit-workflow.md) for discovery order, platform coverage, and mode behavior.
- [Evidence schema](references/evidence-schema.md) for feature records, statuses, confidence, and verification labels.
- [Document contract](references/document-contract.md) for the required output files and content rules.
- [Safe operation](references/safe-operation.md) for exclusions, test execution, redaction, and preservation rules.

## Discovery and analysis

1. Establish the project root and inspect local instructions.
2. Run `scripts/inventory_project.py` into a skill-owned temporary or audit working directory. Use its JSON as the starting evidence index; do not paste whole source files into context.
3. Identify languages, runtimes, frameworks, package managers, workspaces, build systems, entry points, applications, services, modules, databases, migrations, tests, environment-variable names, deployment files, and external integrations.
4. Inspect relevant source in manageable groups. Follow call paths and data flows from user-facing surfaces through business logic and persistence. Mark unsupported or inaccessible claims as unknown.
5. Run only safe, relevant checks. Record the exact command, working directory, result, and limitations. A test is passed only when it actually exits successfully.
6. Build a feature inventory with one record per discovered capability. Use the statuses `IMPLEMENTED`, `PARTIALLY_IMPLEMENTED`, `BACKEND_ONLY`, `CONFIGURATION_DEPENDENT`, `NOT_IMPLEMENTED`, `BROKEN`, and `UNVERIFIED`.
7. Produce the documents in [Document contract](references/document-contract.md). Do not create empty files; an applicable document with no verified evidence must contain a concise unknown/not-discovered finding and its evidence boundary.
8. Run `scripts/validate_audit_docs.py` against the output directory and fix validation failures without weakening evidence requirements.

## Feature inventory minimum

Each feature record must include its name, description, user-facing purpose, implementation layers, related files and symbols, data tables/relationships, APIs and integrations, tests and actual results, configuration/dependencies, status, evidence classification, confidence, and known gaps. Use line references when practical. Distinguish an endpoint declaration from a reachable, authorized, tested behavior.

## Architecture and diagrams

Document client/server boundaries, process startup, frontend/backend communication, authentication and authorization, persistence, background jobs, synchronization, offline/online behavior, external services, build/package flow, and deployment topology. Use Mermaid only where it clarifies a relationship or sequence, and ensure every diagram reflects observed evidence.

## Installation and invocation

For a global installation, place this complete folder under `%USERPROFILE%\\.agents\\skills\\inaam-universal-software-auditor` or the equivalent skills directory configured by the Codex client. For a project-specific installation, place it under `<project-root>/.agents/skills/inaam-universal-software-auditor` when project-local skills are enabled. Do not overwrite an existing installation.

Invoke it explicitly with `$inaam-universal-software-auditor` or, where the client exposes slash commands, `/inaam-universal-software-auditor`, for example:

```text
Use $inaam-universal-software-auditor in FULL AUDIT mode on <project-root> and write the audit to docs/software-audit/.
```

For an existing audit:

```text
Use $inaam-universal-software-auditor in INCREMENTAL AUDIT mode on <project-root>, preserving user-authored documentation.
```

For a focused investigation:

```text
Use $inaam-universal-software-auditor in FEATURE AUDIT mode to trace offline order synchronization in <project-root>.
```
