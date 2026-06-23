# Safety Boundary

## Default Gates

- `local loopback only`
- `allow_physical_controller = false`
- `allow_non_loopback = false`
- `allow_legacy_binary_execution = false`
- `allow_netarrays_force = false`
- `allow_actual_configuration = false`
- Actual IP, port, and credential material in Git is prohibited.
- Actual artifacts and runtime output inside the repository are prohibited even when ignored by Git.
- Active profiles must not contain non-loopback endpoints, `0.0.0.0` binds, UNC network paths, or actual HTTP endpoints.

## Phase 0 Boundary

Phase 0 does not execute NetArrays or any RSID program.

Future NetArrays work may use only a simulator mode and requires a separate approval gate before any execution path is added.

## GitHub Backup Boundary

The owner-designated GitHub `origin` remote may be used only for source backup and publication.

It is not an operational endpoint, runtime dependency, source baseline authority, validation evidence source, artifact store, or readiness substitute. Any additional remote or changed remote URL is a repository safety error until separately reviewed.

## Validation Boundary

`scripts/validate_repo.py` and `scripts/quality_gate.py` are safety tooling only. They must not access controllers, operational networks, external APIs, cloud services, package registries, NetArrays, or legacy RSID binaries.

Credential detections report only:

```text
file:line:key_name
```

Detected values must not be printed.
