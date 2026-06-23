#!/usr/bin/env python3
"""M1 readiness gate.

This script reports readiness without closing decisions or inventing source
baseline values.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import quality_gate
import validate_repo


READY_SOURCE_IDS = ["SRC-PROTO-001", "SRC-K117-001", "SRC-NA-001", "SRC-TIME-001"]
READY_DECISION_IDS = ["DEC-DEV-001", "DEC-STORAGE-001", "DEC-REPO-001"]
APPROVED_STATUSES = {"approved", "accepted", "resolved", "closed"}


@dataclass(frozen=True)
class Blocker:
    blocker_id: str
    file: str
    owner_action: str


def is_resolved(row: dict[str, str] | None) -> bool:
    if row is None:
        return False
    return (row.get("status") or "").strip().lower() in APPROVED_STATUSES


def source_complete(row: dict[str, str] | None) -> bool:
    if row is None:
        return False
    for column in ("revision", "external_path", "sha256", "owner", "review_state"):
        value = (row.get(column) or "").strip()
        if not value or value.upper() == "TBD" or value.lower() in {"not_collected", "open"}:
            return False
    return True


def load_registers(root: Path) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    parsed: dict[str, list[dict[str, str]]] = {}
    issues: list[validate_repo.Issue] = []
    for rel in ("references/source_register.csv", "references/decision_register.csv"):
        path = root / rel
        if path.exists():
            try:
                _, rows = validate_repo.read_csv(path)
            except Exception as exc:
                issues.append(validate_repo.Issue("schema", "ERROR", f"{rel} parse failed: {exc}"))
                rows = []
        else:
            rows = []
        parsed[rel] = rows
    source_by_id = {row.get("source_id", ""): row for row in parsed["references/source_register.csv"] if row.get("source_id")}
    decision_by_id = {row.get("decision_id", ""): row for row in parsed["references/decision_register.csv"] if row.get("decision_id")}
    return source_by_id, decision_by_id


def acceptance_items_present(root: Path) -> bool:
    path = root / "ACCEPTANCE_TRACE.md"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    return all(item.lower() in text for item in validate_repo.ACCEPTANCE_HARDENING_ITEMS)


def evaluate_readiness(root: Path | str) -> tuple[list[Blocker], quality_gate.GateResult]:
    root = Path(root).resolve()
    gate = quality_gate.evaluate_quality_gate(root, run_tests=True)
    issues = gate.issues
    blockers: list[Blocker] = []

    if gate.failed:
        blockers.append(Blocker("M1-QG-001", "scripts/quality_gate.py", "Resolve quality gate errors and test failures."))

    if any(issue.level == "ERROR" and issue.category in {"safety", "secret", "network"} for issue in issues):
        blockers.append(Blocker("M1-SAFE-001", "docs/SAFETY_BOUNDARY.md", "Resolve all safety, secret, and network validation errors."))

    if any(issue.level == "ERROR" and issue.category in {"storage", "forbidden"} for issue in issues):
        blockers.append(Blocker("M1-STORE-001", "docs/STORAGE_BOUNDARY.md", "Move actual artifacts outside the repository through an approved migration."))

    if any(issue.level == "ERROR" and issue.category == "git" and "remote" in issue.message.lower() for issue in issues):
        blockers.append(Blocker("M1-GIT-001", "docs/SAFETY_BOUNDARY.md", "Remove unapproved Git remotes or restrict them to the approved backup-only repository."))

    if any(issue.level == "WARNING" and issue.category == "git" and "parent Git" in issue.message for issue in issues):
        blockers.append(Blocker("M1-REPO-001", "references/decision_register.csv", "Resolve DEC-REPO-001 for nested repository disposition."))

    source_by_id, decision_by_id = load_registers(root)
    for decision_id in READY_DECISION_IDS:
        if not is_resolved(decision_by_id.get(decision_id)):
            blockers.append(Blocker(decision_id, "references/decision_register.csv", "Owner review must resolve this decision before M1 Protocol Core."))

    for source_id in READY_SOURCE_IDS:
        if not source_complete(source_by_id.get(source_id)):
            blockers.append(Blocker(source_id, "references/source_register.csv", "Collect revision, path alias, SHA-256, owner, and review state."))

    if any(issue.level == "ERROR" and issue.category in {"reference", "protocol"} for issue in issues):
        blockers.append(Blocker("M1-PROTO-REF-001", "specs/common/protocol", "Resolve protocol table and source-reference validation errors."))

    if gate.test_result is None or not gate.test_result.passed:
        blockers.append(Blocker("M1-TEST-001", "tests", "Make validator regression tests pass."))

    if not acceptance_items_present(root):
        blockers.append(Blocker("M1-TRACE-001", "ACCEPTANCE_TRACE.md", "Record all hardening acceptance trace items."))

    deduped: dict[str, Blocker] = {}
    for blocker in blockers:
        deduped.setdefault(blocker.blocker_id, blocker)
    return list(deduped.values()), gate


def print_report(blockers: list[Blocker]) -> int:
    if blockers:
        print("M1_READINESS_BLOCKED")
        for blocker in blockers:
            print(f"{blocker.blocker_id} | {blocker.file} | {blocker.owner_action}")
        print(f"summary: blockers={len(blockers)}")
        return 1
    print("M1_READINESS_READY")
    print("summary: blockers=0")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run M1 readiness gate.")
    parser.add_argument("--root", default=".", help="Repository root. Default: current directory.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    blockers, _gate = evaluate_readiness(args.root)
    return print_report(blockers)


if __name__ == "__main__":
    raise SystemExit(main())
