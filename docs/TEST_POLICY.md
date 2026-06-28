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

Environmental decoy handling also requires regression coverage. Tests must prove that a classified decoy candidate does not become a storage ERROR, while tracked or openable forbidden artifacts still fail.

Local path leak detection requires regression coverage. Tests must prove that Markdown or CSV local absolute path candidates fail without printing the path value, while documented template paths remain allowed.

M1 readiness changes require regression coverage for source metadata completeness. Tests must prove that placeholder source fields, invalid SHA-256 values, absolute paths, URLs, and unreviewed states do not satisfy readiness.

Owner review reporting changes require regression coverage that proves required actions are reported from register state without printing source field values that may contain actual paths.

Source review recheck changes require regression coverage that proves provisional alias, size, and SHA-256 metadata can be matched against synthetic external files, missing files are reported without printing the external root path, and repository-internal local roots are blocked.

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
