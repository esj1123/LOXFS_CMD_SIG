# Storage Boundary

## Source Repository

This Git repository stores governance, templates, source registers, protocol tables, scripts, and synthetic test fixtures only.

The repository must not store actual binaries, DBN files, PGM files, deployment packages, Office/PDF references, captures, actual configurations, credentials, operational endpoints, or runtime outputs.

## External Local Root

Actual local artifacts and runtime outputs must be stored outside the Git repository under `LOXFS_CMD_SIG_LOCAL_ROOT`.

Recommended template path:

```text
C:\LOXFS_CMD_SIG_LOCAL
```

The actual approved path is an owner decision and must not be hard-coded in source files.

Target directory shape:

```text
<LOXFS_CMD_SIG_LOCAL_ROOT>\
  artifacts\
    documents\
    legacy_rsid\
    netarrays\
    configurations\
    reference_logs\
  runtime\
    harness\
    legacy_rsid\
    netarrays\
  runs\
  config\
```

## Boundary Rules

- Git source repo and actual artifact root are separate.
- The actual artifact root must not be inside this repository.
- The actual artifact root should be outside known sync roots when possible.
- Git ignore rules do not replace storage boundary enforcement.
- Actual files are not copied into the source repository.
- Source registers record path aliases, source identity, and SHA-256 values only.
- Credential values and actual endpoint values are not recorded in registers or notes.

## Scripts

- `scripts/bootstrap_local_workspace.py` plans or creates the external directory skeleton.
- `scripts/migrate_local_workspace.py` inventories and plans movement from legacy `repo/local` content to the external root.
- `scripts/inventory_local_artifacts.py` resolves relative output paths under the external local root and rejects output inside the source repository.
- Both scripts are dry-run by default and require explicit `--apply` for file-system changes.
