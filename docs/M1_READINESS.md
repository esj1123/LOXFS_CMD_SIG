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
- `SRC-PROTO-001`, `SRC-K117-001`, `SRC-NA-001`, and `SRC-TIME-001` have reviewed revision, path alias, SHA-256, owner, and review state.
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
