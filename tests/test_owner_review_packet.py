from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import m1_readiness  # noqa: E402
import owner_review_packet  # noqa: E402
from test_validate_repo import make_valid_repo, read_csv_rows, rewrite_csv  # noqa: E402


def complete_ready_sources(root: Path) -> None:
    rows = read_csv_rows(root, "references/source_register.csv")
    for row in rows:
        if row.get("source_id") in m1_readiness.READY_SOURCE_IDS:
            row["revision"] = f"rev-{row['source_id']}"
            row["external_path"] = f"artifacts/reviewed/{row['source_id']}"
            row["sha256"] = "b" * 64
            row["owner"] = "source_owner"
            row["review_state"] = "reviewed"
    rewrite_csv(root, "references/source_register.csv", rows)


def resolve_ready_decisions(root: Path) -> None:
    rows = read_csv_rows(root, "references/decision_register.csv")
    for row in rows:
        if row.get("decision_id") in m1_readiness.READY_DECISION_IDS:
            row["status"] = "Resolved"
    rewrite_csv(root, "references/decision_register.csv", rows)


class OwnerReviewPacketTests(unittest.TestCase):
    def test_current_minimal_repo_reports_six_owner_actions(self) -> None:
        with make_valid_repo() as root_name:
            actions = owner_review_packet.owner_actions(Path(root_name))
            self.assertEqual([action.action_id for action in actions], [
                "DEC-DEV-001",
                "DEC-STORAGE-001",
                "DEC-REPO-001",
                "SRC-PROTO-001",
                "SRC-K117-001",
                "SRC-TIME-001",
            ])

    def test_completed_owner_inputs_clear_review_packet(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            resolve_ready_decisions(root)
            complete_ready_sources(root)
            self.assertEqual(owner_review_packet.owner_actions(root), [])

    def test_source_action_reports_field_names_not_values(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            resolve_ready_decisions(root)
            complete_ready_sources(root)
            rows = read_csv_rows(root, "references/source_register.csv")
            sensitive_path = "C:/actual/source/path/protocol.pdf"
            for row in rows:
                if row.get("source_id") == "SRC-PROTO-001":
                    row["external_path"] = sensitive_path
            rewrite_csv(root, "references/source_register.csv", rows)

            actions = owner_review_packet.owner_actions(root)
            messages = [action.owner_action for action in actions]
            self.assertTrue(any("path alias" in message for message in messages), messages)
            self.assertFalse(any(sensitive_path in message for message in messages), messages)


if __name__ == "__main__":
    unittest.main()
