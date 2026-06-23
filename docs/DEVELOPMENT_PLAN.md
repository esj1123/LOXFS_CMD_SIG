# Development Plan

## Document Role

This document is the canonical delivery roadmap for M0 through M6.

It owns:

- phase objectives
- phase sequence
- entry conditions
- work scope
- exit conditions

It does not own:

- current phase
- current blockers
- readiness result
- decision status
- source collection status
- validation result
- execution commands

Canonical references:

- Current state: ../STATUS.md
- M1 entry definition: M1_READINESS.md
- Decision state: ../references/decision_register.csv
- Source state: ../references/source_register.csv
- Validation evidence: ../ACCEPTANCE_TRACE.md
- Commands: RUNBOOK.md
- Architecture: ARCHITECTURE.md

## Build-Stage Governance Imports

During M0, the project may adopt lightweight external harness governance patterns when they improve repository construction without changing phase scope. The approved build-stage imports are task contract discipline, change class discipline, verification hygiene, and closeout receipt discipline. These practices do not authorize protocol implementation, CI setup, release automation, profile/render systems, RAG tooling, or artifact publishing.

## Target Capability Flow

Static Review Candidate
-> Scenario Definition
-> Protocol Emulation
-> Legacy RSID or Gateway Mock
-> NetArrays Simulator
-> Packet/Tag Trace
-> Independent Oracle
-> Regression and Fault Injection

This flow records the long-term target shape only. It does not state current progress.

## M0: Repository and Source Baseline Hardening

Entry: Phase 0 bootstrap request is approved.

Work: Create repository governance, source registers, safety boundary, seed specs, profiles, scenarios, validation scripts, fail-closed quality gate, external storage boundary, and regression tests.

Exit criteria: `repo.ps1 validate`, `repo.ps1 test`, and `repo.ps1 quality-gate` either pass or fail only for explicit external blockers that are recorded in `STATUS.md` and `ACCEPTANCE_TRACE.md`.

## M1: Protocol Core

Entry: The M1 readiness gate permits M1 entry; see `docs/M1_READINESS.md` and `scripts/m1_readiness.py`.

Work: Implement 48-byte header and 10-byte data block encode/decode, packet type handling, session controls, placeholder CRC interfaces, synthetic golden vectors, and unit/contract tests.

Exit criteria: Syntax/build checks, unit tests, contract tests, and existing quality gate pass without UDP, NetArrays, or legacy RSID integration.

## M2: Local UDP Loopback

Entry: Protocol core behavior is covered by tests.

Work: Add local loopback-only UDP transport, channel manager skeleton, trace recording, and controlled local scenarios.

Exit criteria: Local loopback scenarios produce observed or reproduced results only, with no non-loopback endpoint allowed.

## M3: Legacy RSID Black-Box Characterization

Entry: Isolated environment and approval gate are defined.

Work: Inventory legacy packages, observe process and port behavior in isolation, compare packets and logs, and document ACK/retry/session behavior.

Exit criteria: Observations are evidence-linked and do not treat unverified binaries as implementation source.

## M4: NetArrays Simulator Tag Mapping PoC

Entry: Simulator-only approval gate is granted.

Work: Build manual CSV or simulator adapter proof of concept for tag read/write mapping without Force against operational systems.

Exit criteria: Mapping behavior is observed in simulator mode only and remains source-separated from actual configuration.

## M5: Closed-Loop Representative Scenario

Entry: Loopback transport, trace schema, and oracle boundaries are validated.

Work: Execute a representative synthetic scenario through runner, protocol core, transport, trace recorder, and independent oracle.

Exit criteria: Scenario output is categorized only as observed, reproduced, not_reproduced, or inconclusive.

## M6: Pattern-Based Regression and Fault Injection

Entry: Representative scenarios and fault schema are stable.

Work: Add regression suite candidates and fault injection cases for drop, duplicate, delay, reorder, corrupt, channel disagreement, disconnect, reconnect, stop, and reset cases.

Exit criteria: Regression output remains evidence-linked and avoids automatic final acceptance judgment.
