# Tests

Phase 0 includes standard-library `unittest` regression tests for validator, quality gate, storage boundary, reference integrity, protocol table structure, and document authority.

Run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 test
```

Tests create independent temporary Git repositories and do not mutate the current repository.

Synthetic fixtures may use text or generated strings only. Actual binaries, operational configurations, captures, deployment packages, credentials, endpoints, and Office/PDF artifacts must not be committed.
