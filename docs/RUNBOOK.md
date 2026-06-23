# Runbook

## Startup

1. Read `README.md`, `AGENTS.md`, `STATUS.md`, `docs/SAFETY_BOUNDARY.md`, and `references/decision_register.csv`.
2. Review Open decisions before changing behavior.
3. Keep actual artifacts outside the repository under an approved `LOXFS_CMD_SIG_LOCAL_ROOT`.
4. Use `scripts\repo.ps1` for routine commands.

If `py -3` and `python` are unavailable, set `LOXFS_HARNESS_PYTHON` to an approved Python 3 standard-library interpreter for the current shell session.

## Status

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 status
```

## Bootstrap External Local Workspace

Dry-run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 bootstrap --local-root C:\LOXFS_CMD_SIG_LOCAL
```

Apply directory creation only after owner approval:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 bootstrap --local-root C:\LOXFS_CMD_SIG_LOCAL --apply
```

The actual approved path must be outside the repository and outside known sync roots.

## Inventory External Local Artifacts

Dry-run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 inventory --local-root C:\LOXFS_CMD_SIG_LOCAL
```

Write an inventory CSV only when an explicit output path is provided:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 inventory --local-root C:\LOXFS_CMD_SIG_LOCAL --apply --output runs\artifact_inventory.csv
```

Relative `--output` paths resolve under `LOXFS_CMD_SIG_LOCAL_ROOT`. Do not write generated inventories into the source repository.

## Migration Planning

Dry-run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 migrate-plan --local-root C:\LOXFS_CMD_SIG_LOCAL
```

`--apply` copies to the external root first, verifies SHA-256, and removes only source files with matching destination hashes. Do not use `--apply` until the destination is approved.

## Validate

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 validate
```

## Test

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 test
```

## Quality Gate

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 quality-gate
```

`QUALITY_GATE_PASS` means repository hardening checks passed. It is not protocol behavior acceptance.

## M1 Readiness

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 m1-readiness
```

Do not begin M1 Protocol Core unless the output is `M1_READINESS_READY`.

## Closeout Receipt

Every implementation closeout should include:

- changed files or artifacts
- commands run
- commands not run, each marked `NOT RUN` with a reason
- validation, test, quality gate, and readiness results
- storage and safety confirmation
- unresolved risks, blockers, and assumptions
- required owner actions

Use repository-relative evidence references where possible. Do not include secrets, credential values, operational endpoints, raw local absolute artifact paths, or unnecessary raw logs in the receipt.
