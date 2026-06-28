# Source Baseline Plan

M1 Protocol Core requires reviewed source baseline records before implementation begins. Actual source files remain outside this repository.

## Minimum M1 Sources

| Source ID | Required fields before M1 | Current state |
| --- | --- | --- |
| `SRC-PROTO-001` | revision, external path alias, SHA-256, owner, review state | `approved` |
| `SRC-K117-001` | catalog revision, external path alias, SHA-256, owner, review state | `approved` |
| `SRC-TIME-001` | actual configuration source revision, external path alias, SHA-256, owner, review state | `approved` |

## Deferred M2+ Sources

| Source ID | Deferred role | Current state |
| --- | --- | --- |
| `SRC-NA-001` | NetArrays project or DBN identity for tag mapping and simulator-adapter phases | `M2+ deferred` |

## Collection Rules

- Do not copy actual source packages, DBN files, configurations, captures, or documents into Git.
- Store reviewed local copies under the external local artifact root when owner approval exists.
- Record only source identity, path alias, SHA-256, owner, review state, and non-sensitive notes in `references/source_register.csv`.
- Leave rows as `TBD` and `not_collected` until the source owner provides reviewable material.
- Do not infer revision or hash values from document names, memory, or generated files.
- Use path aliases only. Do not record Windows absolute paths, UNC paths, URLs, endpoints, or credential-bearing locations in `external_path`.
- Before M1, `sha256` must be a 64-character hexadecimal digest and `review_state` must be `reviewed` or `approved`.

## Missing Source Report

Current missing M1 baseline items:

- None for direct M1 source identity metadata.

Actual timing, retry, endpoint, channel, and configuration values remain external and deferred to M2 behavior review.

## Owner Evidence Checklist

When a source owner provides material, record only this metadata in Git:

| Field | Requirement |
| --- | --- |
| `revision` | Source-backed revision identifier or owner-provided version label. |
| `external_path` | Non-absolute path alias under the approved external artifact root. |
| `sha256` | 64-character hexadecimal SHA-256 digest of the reviewed source material. |
| `owner` | Responsible source owner role or approved owner label. |
| `review_state` | `reviewed` or `approved` only when owner review is complete. |

Do not record the real filesystem path, network location, endpoint, credential, packet capture, actual configuration content, or binary/package content in this repository. If the source is not available for review, keep the row as `TBD` and `not_collected`.
