# Safe operation

## Scope and exclusions

Default inventory exclusions are generated or dependency-heavy directories such as `.git`, `node_modules`, virtual environments, caches, build output, coverage output, and package-manager caches. Record exclusions and inspect them when they are relevant to packaging or deployment. Never assume an excluded directory is absent; state the boundary.

Do not execute migrations, seed production data, delete files, change permissions, install dependencies, deploy, publish, or start an external-facing service. Do not edit application code or configuration. Use isolated temporary directories for generated intermediate data.

## Tests and runtime checks

Prefer existing read-only test commands, static checks, local health checks, and disposable fixtures. Capture command, directory, exit code, duration when relevant, and limitations. A failed or skipped check is evidence about verification scope, not proof that the application is broken unless the failure supports that conclusion.

## Secret handling

Inspect variable names, configuration keys, secret-manager references, and redacted file locations. Never print values. Avoid loading binary databases or user datasets into context. If a source file contains a token-like value, report only its path, line, category, and remediation need.

## Documentation preservation

Before an incremental update, list existing files and determine whether they are generated audit outputs or user-authored material. Never overwrite unrelated files. If an audit output already exists and the user did not authorize replacement, write a new clearly named report or stop before mutation.
