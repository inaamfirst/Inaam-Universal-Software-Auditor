# Documentation contract

The audit directory is normally `docs/software-audit/`. Generate these files when performing a full audit:

| File | Required focus |
| --- | --- |
| `PROJECT_OVERVIEW.md` | Product purpose, scope, clients, services, and evidence boundary. |
| `COMPLETE_FEATURE_INVENTORY.md` | One evidence-backed record per feature and status totals. |
| `ARCHITECTURE.md` | Components, boundaries, startup, communication, and deployment topology. |
| `TECH_STACK.md` | Languages, runtimes, frameworks, libraries, versions, and build tools. |
| `DATABASE_SCHEMA.md` | Engines, tables, relationships, migrations, constraints, indexes, and backups. |
| `API_REFERENCE.md` | Verified endpoints, methods, auth, payload evidence, integrations, and gaps. |
| `MODULES.md` | Modules, ownership/role, entry points, dependencies, and dead/duplicate evidence. |
| `DATA_FLOW.md` | Important user-to-storage, sync, job, and external-service flows. |
| `SECURITY_AUDIT.md` | Auth, authorization, secrets, validation, encryption, dependencies, logging, and data protection. |
| `DEPLOYMENT_GUIDE.md` | Build, packaging, runtime topology, deployment configuration, and operational limits. |
| `INSTALLATION_GUIDE.md` | Verified prerequisites, setup, initialization, and configuration steps. |
| `USER_GUIDE.md` | User-visible workflows supported by source evidence; mark unverified workflows. |
| `DEVELOPER_GUIDE.md` | Local development, code organization, tests, extension points, and conventions. |
| `TEST_COVERAGE.md` | Test inventory, executed commands/results, coverage evidence, and missing tests. |
| `KNOWN_ISSUES.md` | Broken, partial, risky, contradictory, or inaccessible areas with evidence. |
| `ROADMAP.md` | Evidence-backed gaps and suggested priorities; label recommendations clearly. |
| `CHANGELOG.md` | Audit dates/modes, changed findings, and source/test evidence for each update. |
| `COMPLETE_SOFTWARE_REFERENCE.md` | Navigable consolidated index linking the other documents and key evidence. |

Every file must be non-empty and include an evidence basis. If a category has no verified evidence, say so explicitly with `UNKNOWN` or `NOT_IMPLEMENTED` and describe what was inspected. Do not invent versions, endpoints, tables, workflows, users, or deployment steps.

For incremental audits, update only the requested audit directory and append to `CHANGELOG.md`; preserve unrelated project documentation. For feature audits, create or update only documents needed to explain the requested feature unless the user requests the complete set.
