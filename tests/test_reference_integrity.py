from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_repo  # noqa: E402
from test_validate_repo import make_valid_repo, read_csv_rows, rewrite_csv  # noqa: E402


def errors(root: Path) -> list[str]:
    return [issue.message for issue in validate_repo.run_checks(root) if issue.level == "ERROR"]


class ReferenceIntegrityTests(unittest.TestCase):
    def assert_has_error(self, root: Path, fragment: str) -> None:
        messages = errors(root)
        self.assertTrue(any(fragment in message for message in messages), messages)

    def test_duplicate_source_id_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            rows = read_csv_rows(root, "references/source_register.csv")
            rows.append(dict(rows[0]))
            rewrite_csv(root, "references/source_register.csv", rows)
            self.assert_has_error(root, "duplicate ID")

    def test_duplicate_decision_id_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            rows = read_csv_rows(root, "references/decision_register.csv")
            rows.append(dict(rows[0]))
            rewrite_csv(root, "references/decision_register.csv", rows)
            self.assert_has_error(root, "duplicate ID")

    def test_artifact_source_orphan_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            rows = read_csv_rows(root, "references/artifact_manifest.csv")
            rows[0]["source_id"] = "SRC-MISSING-001"
            rewrite_csv(root, "references/artifact_manifest.csv", rows)
            self.assert_has_error(root, "artifact_manifest orphan source_id")

    def test_protocol_source_ref_orphan_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            rows = read_csv_rows(root, "specs/common/protocol/header_fields.csv")
            rows[0]["source_ref"] = "SRC-MISSING-001"
            rewrite_csv(root, "specs/common/protocol/header_fields.csv", rows)
            self.assert_has_error(root, "orphan source_ref")

    def test_common_protocol_authority_scope_conflict_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            rows = read_csv_rows(root, "specs/common/protocol/header_fields.csv")
            rows[0]["source_ref"] = "SRC-K117-001"
            rewrite_csv(root, "specs/common/protocol/header_fields.csv", rows)
            self.assert_has_error(root, "authority_scope conflict")


if __name__ == "__main__":
    unittest.main()
