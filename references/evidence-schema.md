# Evidence and feature schema

## Verification labels

Use one or more of these labels for each important finding:

- **SOURCE_VERIFIED**: directly supported by inspected source, configuration, schema, or manifest.
- **TEST_VERIFIED**: supported by a test command that was actually executed successfully.
- **RUNTIME_VERIFIED**: observed during a safe runtime inspection or request.
- **INFERRED**: a reasoned interpretation with supporting clues but no direct proof.
- **UNKNOWN**: evidence was unavailable, inaccessible, contradictory, or not safely executable.

Never convert an inferred or documented claim into a verified claim without new evidence.

## Confidence

Use HIGH when multiple direct sources agree, MEDIUM when one direct source or a limited test supports the finding, and LOW when the finding is inferred or coverage is incomplete. Explain meaningful limitations.

## Feature record

Represent each feature in the inventory with these fields:

```text
name
description
user_purpose
status
confidence
verification
ui_or_client_evidence
business_logic_evidence
data_evidence
api_and_integration_evidence
source_files_and_symbols
tests_and_results
configuration_and_dependencies
known_gaps
```

Use only these statuses:

`IMPLEMENTED`, `PARTIALLY_IMPLEMENTED`, `BACKEND_ONLY`, `CONFIGURATION_DEPENDENT`, `NOT_IMPLEMENTED`, `BROKEN`, `UNVERIFIED`.

## Evidence references

Prefer references such as `backend/app/orders/service.py:142`, `frontend/src/routes/orders.tsx:38`, a migration name, a test node id, or an exact executed command. Redact secret values and private data. For generated inventories, reference the inventory record rather than copying source content.
