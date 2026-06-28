#!/usr/bin/env python3
"""Owner review packet report for remaining M1 blockers.

This report is informational. It reads only local registers, does not close
decisions, and does not print source values that may contain sensitive paths.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import m1_readiness


DECISION_ACTIONS = {
    "DEC-DEV-001": "Owner review must approve the M1 implementation runtime and language.",
    "DEC-STORAGE-001": "Owner review must approve the external artifact root policy and storage location class.",
    "DEC-REPO-001": "Owner review must approve repository topology and nested parent Git disposition.",
}


@dataclass(frozen=True)
class OwnerAction:
    action_id: str
    file: str
    owner_action: str


def decision_actions(decision_by_id: dict[str, dict[str, str]]) -> list[OwnerAction]:
    actions: list[OwnerAction] = []
    for decision_id in m1_readiness.READY_DECISION_IDS:
        if not m1_readiness.is_resolved(decision_by_id.get(decision_id)):
            actions.append(
                OwnerAction(
                    decision_id,
                    "references/decision_register.csv",
                    DECISION_ACTIONS.get(decision_id, "Owner review must resolve this decision."),
                )
            )
    return actions


def source_actions(source_by_id: dict[str, dict[str, str]]) -> list[OwnerAction]:
    actions: list[OwnerAction] = []
    for source_id in m1_readiness.READY_SOURCE_IDS:
        missing = m1_readiness.source_metadata_errors(source_by_id.get(source_id))
        if missing:
            actions.append(
                OwnerAction(
                    source_id,
                    "references/source_register.csv",
                    "Provide reviewed source metadata: " + ", ".join(missing) + ".",
                )
            )
    return actions


def owner_actions(root: Path | str) -> list[OwnerAction]:
    source_by_id, decision_by_id = m1_readiness.load_registers(Path(root).resolve())
    return decision_actions(decision_by_id) + source_actions(source_by_id)


def print_report(actions: list[OwnerAction]) -> int:
    if actions:
        print("OWNER_REVIEW_REQUIRED")
        for action in actions:
            print(f"{action.action_id} | {action.file} | {action.owner_action}")
        print(f"summary: actions={len(actions)}")
        return 0
    print("OWNER_REVIEW_CLEAR")
    print("summary: actions=0")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report owner review actions for M1 readiness.")
    parser.add_argument("--root", default=".", help="Repository root. Default: current directory.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return print_report(owner_actions(args.root))


if __name__ == "__main__":
    raise SystemExit(main())
