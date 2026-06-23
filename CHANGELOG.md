# Changelog

## Unreleased

- Adopt build-stage governance practices from `codex-dev-harness`: task contract, change class, `NOT RUN` reporting, and closeout receipt.
- Add document validation and regression tests for the build-stage governance markers.
- Defer scanner, gate-module, CI, release, profile, render, RAG, and artifact-publishing ideas to separate owner-scoped future work.
- Mark `docs/DEVELOPMENT_PLAN.md` as the canonical M0-M6 delivery roadmap without creating `docs/ROADMAP.md`.
- Add README project-path navigation and document-authority mapping.
- Add AGENTS document authority and conflict-resolution rules.
- Add document authority validation and regression tests.
- Harden repository validation with fail-closed storage, secret, network, Git, reference, and protocol table checks.
- Add source authority-scope validation and orphan source warnings to reference integrity checks.
- Add external local root boundary docs and dry-run-first bootstrap/migration planning.
- Align migration planning statuses with `planned_copy`, `same_hash`, `conflict`, `different_hash`, `source_only`, and `destination_only`.
- Keep local artifact inventory outputs under the external local root and reject source-repository output paths.
- Add PowerShell entrypoint for status, bootstrap, inventory, migration planning, validation, tests, quality gate, and M1 readiness.
- Add M1 readiness gate that reports blockers without closing Open decisions.
- Add unittest regression coverage for validator, quality gate, storage boundary, reference integrity, and protocol tables.
- Correct RSID configuration and network mapping source references.
- Remove generated `validate_repo` bytecode from `scripts/__pycache__`.
- Bootstrap local-only Phase 0 repository structure.
- Add safety boundary, scope, development plan, test policy, and legacy analysis plan.
- Seed source, artifact, decision, protocol, baseline, profile, and scenario files.
- Add dry-run-first local workspace and inventory scripts.
- Add repository validation and quality gate scripts.
