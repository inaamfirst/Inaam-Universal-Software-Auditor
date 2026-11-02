# Audit workflow

## Discovery order

Start with the project root, local instructions, and the deterministic inventory. Then inspect in this order:

1. Manifests, lockfiles, workspaces, runtime declarations, and build configuration.
2. Application entry points and process startup paths.
3. UI routes, screens, commands, controllers, handlers, and public API declarations.
4. Domain services, business rules, jobs, queues, and synchronization code.
5. Models, schemas, migrations, repositories, database adapters, and backup/restore code.
6. Authentication, authorization, validation, secrets/configuration, logging, and error handling.
7. Tests, fixtures, CI, packaging, deployment, and operational documentation.

Do not treat directory names as proof of behavior. Follow references between layers and cite the smallest useful source location.

## Platform coverage

For web and SaaS systems, trace browser/client routes through API handlers, authorization, persistence, and deployment. For desktop and mobile systems, include process boundaries, packaging, local storage, native bridges, permissions, and update paths. For offline/local-first systems, document queues, conflict handling, retry behavior, synchronization authority, and recovery. For hybrid projects, map each client to shared and server components.

## Modes

### FULL AUDIT

Create a fresh evidence index and inspect all in-scope components. Compare claims across source, tests, configuration, and existing documentation. Existing documentation is evidence to assess, not permission to repeat unverified claims.

### INCREMENTAL AUDIT

Load the previous audit only after inspecting current source. Compare file paths, hashes or timestamps where available, manifests, test results, and documented findings. Update changed sections and add a changelog entry. Preserve unrelated and user-authored files. If evidence was removed, mark the finding stale or unknown instead of silently retaining it.

### FEATURE AUDIT

Build a narrow evidence graph around the requested feature. Include adjacent shared components when they affect behavior, but do not expand into a project-wide inventory unless required to verify the feature. Report missing layers explicitly.

## Output discipline

Use the required filenames in `document-contract.md`. Prefer concise tables for inventories and evidence. Include a source/evidence section in every document. Keep generated claims internally consistent by using the same feature status, terminology, and evidence index across all documents.
