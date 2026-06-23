# LOXFS Command & Signal Test Harness

This repository is the local-only source area for the LOXFS Command & Signal Test Harness.

The repository contains governance, source registers, protocol seed tables, local profile defaults, storage boundary checks, validation tooling, regression tests, and readiness gating. It does not implement protocol logic, run NetArrays, run RSID binaries, or test against any actual controller or operational network.

README.md is a navigation document, not the live status source.

## Project Path

M0 Repository and Source Baseline
-> M1 Protocol Core
-> M2 Local UDP Loopback
-> M3 Legacy RSID Characterization
-> M4 NetArrays Simulator Adapter PoC
-> M5 Closed-loop Representative Scenario
-> M6 Pattern-based Regression and Fault Injection

- Detailed phase definitions: [docs/DEVELOPMENT_PLAN.md](docs/DEVELOPMENT_PLAN.md)
- Current phase and blockers: [STATUS.md](STATUS.md)
- M1 entry conditions: [docs/M1_READINESS.md](docs/M1_READINESS.md)
- Validation evidence: [ACCEPTANCE_TRACE.md](ACCEPTANCE_TRACE.md)
- Commands: [docs/RUNBOOK.md](docs/RUNBOOK.md)

## Document Authority

| Information | Canonical source |
|---|---|
| Project purpose and scope | README.md, docs/SCOPE.md |
| M0-M6 phase definitions and delivery path | docs/DEVELOPMENT_PLAN.md |
| Current phase and blockers | STATUS.md |
| M1 entry conditions | docs/M1_READINESS.md, scripts/m1_readiness.py |
| Decision state | references/decision_register.csv |
| Source baseline state | references/source_register.csv |
| Validation evidence | ACCEPTANCE_TRACE.md |
| Commands | docs/RUNBOOK.md |
| Target architecture | docs/ARCHITECTURE.md |

## Source and Artifact Split

Source files in this repository contain only governance, specifications, templates, scripts, and synthetic fixtures.

Actual artifacts are external reference materials, deployment packages, actual configurations, captures, logs, and runtime outputs. They must stay outside this repository under an owner-approved `LOXFS_CMD_SIG_LOCAL_ROOT`.

Recommended template path only:

```text
C:\LOXFS_CMD_SIG_LOCAL
```

The actual local root is not hard-coded in source.

## Unsupported Work

- Actual controller access
- Mission Network or Control Network access
- Physical I/O
- NetArrays execution or Force operations
- RSIDGW, RSIDSIM, RSIDLOG, or RSID DB Tool execution
- Download, Compile, Debug, or Force actions against operational systems
- Binary reverse engineering
- Final acceptance judgment
- M1 Protocol Core implementation before readiness is resolved

## Default Workflow

Use `scripts\repo.ps1` as the primary entrypoint:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 status
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 bootstrap
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 inventory
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 validate
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 test
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 quality-gate
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 m1-readiness
```

`repo.ps1` searches for Python in this order:

1. `LOXFS_HARNESS_PYTHON`
2. `py -3`
3. `python`

If no interpreter is available, set `LOXFS_HARNESS_PYTHON` to an approved Python 3 standard-library interpreter. The repository does not hard-code personal Codex cache paths.

## Validation Commands

Primary:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 validate
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 test
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 quality-gate
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 m1-readiness
```

Direct Python remains a fallback for environments that cannot run the PowerShell entrypoint.
