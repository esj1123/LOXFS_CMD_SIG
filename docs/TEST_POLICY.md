# Test Policy

## Test Classes

- Unit
- Contract
- Integration
- Regression
- Fault Injection
- Replay
- Endurance candidate

## Allowed Automated Result Labels

Automated scripts may only assign these result labels:

- `observed`
- `reproduced`
- `not_reproduced`
- `inconclusive`

Automated scripts must not declare `pass`, `normal`, `problem`, or `accepted` as final judgments.

## Evidence Rule

Expected results must come from independent source review, synthetic golden vectors, or an independent oracle. Results produced by the implementation under test must not be copied directly into expected outputs.

## Validator Regression Rule

Validator and quality gate rule changes require standard-library `unittest` coverage.

Required negative coverage includes forbidden tracked artifacts, worktree artifacts, credential assignments, non-loopback endpoints, unapproved Git remotes, approved backup-only remote handling, missing `.gitignore` patterns, source-reference orphans, malformed protocol offsets, malformed ACK pairs, unsafe profile flags, and invalid external local roots.

Tests must create independent temporary Git repositories under `tempfile` and must not mutate the current repository. Synthetic strings may be used only as generated fixture contents; actual credentials, endpoints, binaries, captures, configurations, and Office/PDF artifacts must not be committed.

Run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 test
```

## Verification Hygiene

- Report every check that was intentionally skipped as `NOT RUN` with the reason.
- Do not imply success for a check that was not executed.
- Focused verification is acceptable for narrow documentation or validator changes only when the changed surface and omitted checks are named.
- Existing storage, safety, reference, protocol, and readiness blockers must remain visible; tests must not weaken a validator rule to force a clean result.
- Negative tests should prove that unsafe or malformed examples fail before reporting a validator or quality-gate change complete.
