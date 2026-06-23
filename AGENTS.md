# Codex Working Rules

These rules apply to future work in this repository.

## Required Startup Read

Before changing files, read:

- `README.md`
- `AGENTS.md`
- `STATUS.md`
- `docs/SAFETY_BOUNDARY.md`
- `references/decision_register.csv`

For work that changes or interprets phase path, phase scope, or delivery sequence, also read `docs/DEVELOPMENT_PLAN.md` before changing files.

## Document Authority and Conflict Resolution

- Phase definitions and phase sequence follow `docs/DEVELOPMENT_PLAN.md`.
- Current phase and blockers follow `STATUS.md` only.
- M1 entry judgment follows the `scripts/m1_readiness.py` execution result and the gate definition in `docs/M1_READINESS.md`.
- Decision state follows `references/decision_register.csv`.
- Source state follows `references/source_register.csv`.
- Validation evidence follows `ACCEPTANCE_TRACE.md`.
- Execution commands follow `docs/RUNBOOK.md`.
- If a summary document conflicts with a canonical source, prefer the canonical source.
- If drift is found, report it as drift instead of merging values by assumption.
- Do not copy current status or validation results into `README.md` or `docs/DEVELOPMENT_PLAN.md`.
- Do not create a new `docs/ROADMAP.md` unless the user explicitly requests it and defines its document role.
- Change `docs/DEVELOPMENT_PLAN.md` only when phase scope or sequence changes.
- Do not interpret the long-term roadmap as live project status during ordinary implementation work.

## Build-Stage Borrowed Practices

The repository may borrow governance practices from external harness templates only when they fit the current phase and this repository's safety boundary.

- Task contract: before edits, identify the requested goal, in-scope changes, likely touch files, likely no-touch files, expected verification, and side effects that will not be performed.
- Change class: classify non-trivial work as `documentation-only`, `validation-surface`, `source-register`, `storage-boundary`, `implementation`, or `side-effecting`.
- Verification hygiene: report any skipped check as `NOT RUN` with a reason; do not imply success for checks that were not executed.
- Closeout Receipt: final reports must distinguish commands run, commands not run, side effects not performed, blocker status, and required owner actions.
- Later borrowing of scanner, gate-module, CI, release, profile, render, RAG, or artifact-publishing ideas requires a separate scoped owner request and must still pass local safety, storage, and M1 readiness rules.

## Source and Artifact Boundary

- Do not add actual binaries, DBN files, PGM files, EXE files, DLL files, PDB files, ZIP files, PCAP files, actual configurations, or captures to Git.
- Do not record actual IP values, ports, credentials, secrets, or operational endpoint details in source files or fixtures.
- Keep actual source packages and reference artifacts outside this repository under an owner-approved `LOXFS_CMD_SIG_LOCAL_ROOT`.
- Git ignore rules are not sufficient storage-boundary enforcement; validator worktree scans must still fail on forbidden artifacts inside the repository.
- Source authority must stay separated as `common`, `K117 baseline`, `N3G target`, and `N3F target`.

## Decision Discipline

- Do not close Open decisions without source-backed owner review.
- Do not turn a TBD, candidate, or observed value into an authoritative value by assumption.
- Record unresolved assumptions in `STATUS.md` and `references/decision_register.csv`.

## File Scope

- Before creating a new file, check whether the change belongs in an existing file.
- Do not rename, move, or delete existing files unless the user explicitly asks for it.
- Keep shared utilities out of scope unless reuse is proven inside the current task.

## Script Policy

- Scripts must be dry-run first by default.
- Scripts may change files only when an explicit `--apply` option is used.
- Scripts must not install packages or depend on external services.
- Quality gate safety warnings must not be hidden or reported as clean completion.

## Implementation Separation

- Protocol implementation and Oracle implementation must stay separated.
- Do not use results extracted from the implementation itself as expected results.
- Expected results must come from independent source review, synthetic golden vectors, or an independent oracle.
- Do not change Validator security rules without negative tests.
- Do not start M1 Protocol Core implementation while M1 readiness is `BLOCKED`.
- Do not automatically change parent Git repository settings, Git remotes, or nested repository disposition.
- Treat the owner-designated GitHub `origin` as backup-only; do not use it as a runtime dependency, source authority, validation evidence source, or operational channel.

## Reporting

After changes, report:

- Changed files
- Commands run
- Verification results
- Unresolved risks and assumptions
- Safety confirmation
