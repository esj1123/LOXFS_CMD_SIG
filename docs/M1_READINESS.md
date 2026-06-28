# M1 Readiness

M1 Protocol Core must not start until the readiness gate reports `M1_READINESS_READY`.

Run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 m1-readiness
```

## Ready Conditions

- Quality gate passes.
- Safety, secret, network, storage, and forbidden artifact errors are zero.
- No unapproved Git remote is configured. The owner-designated GitHub `origin` may exist only as a backup/publication remote and must not be used as an operational dependency or source-baseline substitute.
- Nested repository disposition is resolved by owner review.
- `DEC-DEV-001` is resolved before choosing implementation runtime.
- `DEC-STORAGE-001` is resolved before relying on external artifact storage.
- `SRC-PROTO-001`, `SRC-K117-001`, and `SRC-TIME-001` have reviewed revision, non-absolute path alias, 64-hex SHA-256, owner, and `reviewed` or `approved` review state.
- `SRC-NA-001` is deferred to M2+ unless an owner later promotes exact NetArrays evidence into the M1 source baseline.
- Protocol table source references are valid.
- Validator regression tests pass.
- Acceptance trace records the hardening checks.

## Blocked Output

When blocked, `scripts/m1_readiness.py` prints:

```text
M1_READINESS_BLOCKED
<blocker ID> | <file> | <owner action>
```

The script does not close Open decisions, invent source values, print secret values, or print actual endpoint values.

## Source Metadata Rules

M1 source baseline rows must not use actual local absolute paths, UNC paths, URLs, endpoint strings, or credentials. The `external_path` field is a path alias only, for example a relative alias under the approved external root.

The `sha256` field must be a 64-character hexadecimal digest from owner-reviewed source material. Placeholder, candidate, or memory-derived values are not readiness-complete.

## Owner Review Packet

The readiness gate can report blockers, but it does not decide them. Before M1 Protocol Core starts, the owner review packet should resolve or explicitly defer the following items.

| Blocker | Owner decision or evidence needed | Where to record after review |
| --- | --- | --- |
| `DEC-DEV-001` | Approved implementation runtime and language for M1 Protocol Core. | `references/decision_register.csv` |
| `DEC-STORAGE-001` | Approved external artifact root policy and accepted non-repository storage location class. | `references/decision_register.csv` |
| `DEC-REPO-001` | Approved repository topology, including Desktop worktree retention and nested parent Git disposition. | `references/decision_register.csv` |
| `SRC-PROTO-001` | Reviewed protocol source revision, path alias, SHA-256, owner, and review state. | `references/source_register.csv` |
| `SRC-K117-001` | Reviewed K117 command/signal catalog revision, path alias, SHA-256, owner, and review state. | `references/source_register.csv` |
| `SRC-TIME-001` | Reviewed scan-cycle configuration source identity, path alias, SHA-256, owner, and review state. | `references/source_register.csv` |

Owner review must not put actual source files, actual absolute paths, operational endpoints, credentials, DBN files, package files, captures, or actual configurations into Git. If evidence is unavailable, leave the blocker Open instead of inventing values.

## Deferred Source Rows

`SRC-NA-001` remains important for NetArrays simulator adapter and tag-mapping work, but the owner deferred it from direct M1 readiness on 2026-06-28. M1 Protocol Core must not treat NetArrays, iFIX, DBN, HMI screen, tag-map, or driver evidence as packet authority unless a later owner review promotes exact aliases and updates this gate.
