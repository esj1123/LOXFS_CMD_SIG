# Source Baseline Plan

M1 Protocol Core requires reviewed source baseline records before implementation begins. Actual source files remain outside this repository.

## Minimum M1 Sources

| Source ID | Required fields before M1 | Current state |
| --- | --- | --- |
| `SRC-PROTO-001` | revision, external path alias, SHA-256, owner, review state | `not_collected` |
| `SRC-K117-001` | catalog revision, external path alias, SHA-256, owner, review state | `not_collected` |
| `SRC-NA-001` | project or DBN revision, external path alias, SHA-256, owner, review state | `not_collected` |
| `SRC-TIME-001` | actual configuration source revision, external path alias, SHA-256, owner, review state | `not_collected` |

## Collection Rules

- Do not copy actual source packages, DBN files, configurations, captures, or documents into Git.
- Store reviewed local copies under the external local artifact root when owner approval exists.
- Record only source identity, path alias, SHA-256, owner, review state, and non-sensitive notes in `references/source_register.csv`.
- Leave rows as `TBD` and `not_collected` until the source owner provides reviewable material.
- Do not infer revision or hash values from document names, memory, or generated files.

## Missing Source Report

Current missing M1 baseline items:

- `SRC-PROTO-001`: revision, external path alias, SHA-256, owner, review state.
- `SRC-K117-001`: catalog revision, external path alias, SHA-256, owner, review state.
- `SRC-NA-001`: project or DBN revision, external path alias, SHA-256, owner, review state.
- `SRC-TIME-001`: actual configuration source revision, external path alias, SHA-256, owner, review state.
