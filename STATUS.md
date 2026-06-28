# Status

## Current Phase

Phase 0 Hardening is active.

M1 Protocol Core remains future work until the owner explicitly starts implementation work. `scripts/m1_readiness.py` reports `M1_READINESS_READY`.

## Preflight Snapshot

Last checked: 2026-06-25.

| Check | Result |
| --- | --- |
| Current path | `<RepoWorktree>` |
| Git top-level | `<RepoWorktree>` |
| Parent Git repository | Detected by ancestor `.git`; owner-approved for current M1 worktree retention in `DEC-REPO-001`. |
| Git ownership | Plain `git status --short` succeeded in this session; scripts still use per-invocation `safe.directory` and do not change global Git config. |
| Git status | Initial source baseline is committed on `main`; `.tmp.driveupload/` is ignored by Git and not added to source control. |
| Additional local directory | `.tmp.driveupload/` is present as a temporary upload/cache directory; contents were inspected by metadata only and not deleted or added to Git. |
| Git tracked files | Initial baseline tracks 56 source, document, specification, profile, scenario, script, and test files. |
| Git remote | `origin` is configured for the owner-designated GitHub backup/publication repository `https://github.com/esj1123/LOXFS_CMD_SIG.git`; it is not used for harness runtime behavior. |
| `py --version` | Failed: no installed Python found on PATH. |
| `python --version` | Failed in the current session. |
| Bundled Python used for verification | `LOXFS_HARNESS_PYTHON` was supplied at command time; source does not hard-code the path. |
| `.NET` | SDK 10.0.201 and 10.0.109 present. |
| PowerShell | 5.1.26100.8655. |
| `local/` projected entries | 13 hidden/system zero-byte Office entries are visible by directory enumeration in `<RepoLocal>`, but Python stat/open reports them as missing projected entries; validator classifies them as environmental decoy INFO, not actual artifacts. |
| Candidate external root skeleton | Root alias `<CandidateExternalRoot>` was created with 10 planned directories; no artifact files were copied by the migration tooling. |
| Candidate root file check | 0 files are visible under `<CandidateExternalRoot>` after skeleton creation and sentinel probe. |
| Sentinel probe | Write/read/SHA-256/delete probe under `<CandidateExternalRoot>` passed. |
| Migration dry-run | Reports 13 `source_only` `local/` entries and keeps source files; source hash metadata was unavailable for the preserved hidden Office placeholders. |
| Known sync root in repository path | None detected from the path string. |

## Hardening Outcome

- Validator fail-closed checks were added for Git safety, source/register schema, reference integrity, protocol table structure, storage boundary, credential detection, network endpoint detection, and acceptance trace completeness.
- Validator safety checks now reject local absolute path candidates in Markdown and CSV while allowing the documented external-root template path.
- Validator worktree storage checks now distinguish non-openable hidden/system zero-byte Office/PDF environmental decoy entries from actual forbidden artifacts. Openable, hashable, tracked, or non-zero forbidden artifacts remain ERROR.
- Reference integrity now checks source authority scope for protocol/baseline tables and warns on registered sources not yet referenced by current manifests or tables.
- Quality gate now fails on any validator ERROR or unittest failure.
- M1 readiness gate now reports blockers without closing Open decisions or inventing source values; source completeness requires non-absolute path aliases, 64-hex SHA-256 values, owners, and reviewed/approved states.
- M1 owner review packet guidance is documented in `docs/M1_READINESS.md`, `docs/SOURCE_BASELINE_PLAN.md`, and `docs/RUNBOOK.md`.
- `repo.ps1 owner-review` reports current owner actions from local Decision and Source registers without changing values.
- `docs/SOURCE_REVIEW_NOTES.md` preserves provisional source review observations without approving sources or closing decisions.
- `repo.ps1 source-review` performs read-only alias, size, and SHA-256 rechecks against an external local root without printing that root path or modifying registers.
- `.tmp.driveupload/` is listed in `.gitignore` and required by the validator; worktree storage scanning still applies to files under that directory.
- `docs/ENVIRONMENT_DISCOVERY.md` uses path aliases such as `<RepoWorktree>`, `<ParentGitRoot>`, and `<BundledPython>` instead of local absolute paths.
- Generated `.pyc` files from syntax checking were removed. `scripts/__pycache__` remains visible because the workstation projects an environmental Office decoy entry there; it is not treated as a Python build artifact.

## Current Gate Status

- GitHub `origin` is allowed only as a backup/publication remote; any additional remote or URL change remains a validation error.
- The owner selected Desktop worktree retention for now. `repo.ps1 validate` passes storage boundary checks by classifying the 37 visible hidden/system zero-byte Office entries as environmental decoy INFO; actual forbidden artifacts still fail.
- `<CandidateExternalRoot>` is currently clean after initial skeleton creation and sentinel probe; `DEC-STORAGE-001` records owner approval for the external artifact storage policy.
- `repo.ps1 migrate-plan` against `<CandidateExternalRoot>` remains dry-run only and reports the 13 `<RepoLocal>` placeholders as `source_only`/`keep_source`; no copy or removal was performed.
- `repo.ps1 m1-readiness` reports `M1_READINESS_READY`.
- `repo.ps1 source-review` currently reports `SOURCE_REVIEW_RECHECK_BLOCKED` because `LOXFS_CMD_SIG_LOCAL_ROOT` is unset in this session.
- Owner review actions are clear for direct M1 readiness.
- `repo.ps1 owner-review` reports `OWNER_REVIEW_CLEAR`.
- `DEC-DEV-001` is owner-approved for Python standard-library M1 Protocol Core only; C#/.NET/C++ remain later adapter or integration options.
- Parent Git repository disposition is owner-approved in `DEC-REPO-001` for current Desktop worktree retention; parent Git settings were not changed.
- External artifact storage policy is owner-approved in `DEC-STORAGE-001`; actual root paths remain outside Git.
- `SRC-PROTO-001` and `SRC-K117-001` are owner-approved with alias and SHA-256 metadata.
- `SRC-NA-001` is explicitly deferred to M2+ and is not a direct M1 readiness blocker.
- `SRC-TIME-001` is owner-approved as a timing/config source identity alias. Actual timing, retry, endpoint, and channel values remain external and deferred to M2.
- `py` and `python` are unavailable on PATH; set `LOXFS_HARNESS_PYTHON` before using `scripts\repo.ps1` in this environment.

## Safety Status

- Actual controller access: not performed.
- Actual controller or operational network access: not performed.
- NetArrays execution: not performed.
- Legacy RSID binary execution: not performed.
- External package installation: not performed.
- External local root directory creation: performed for owner-selected candidate roots only.
- User file copy, move, or delete: not performed.
- Remote creation and GitHub pushes: performed for the owner-designated backup/publication repository only.
- Automatic commit without owner approval: not performed.
- M1 Protocol implementation: not performed.
