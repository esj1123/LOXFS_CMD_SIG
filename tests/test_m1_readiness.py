from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import m1_readiness  # noqa: E402


def complete_source_row() -> dict[str, str]:
    return {
        "source_id": "SRC-PROTO-001",
        "revision": "rev-1",
        "external_path": "artifacts/documents/SRC-PROTO-001",
        "sha256": "a" * 64,
        "owner": "source_owner",
        "review_state": "reviewed",
    }


class M1ReadinessSourceMetadataTests(unittest.TestCase):
    def test_reviewed_source_metadata_is_complete(self) -> None:
        self.assertTrue(m1_readiness.source_complete(complete_source_row()))

    def test_tbd_source_metadata_is_incomplete(self) -> None:
        row = complete_source_row()
        row["revision"] = "TBD"
        self.assertIn("revision", m1_readiness.source_metadata_errors(row))
        self.assertFalse(m1_readiness.source_complete(row))

    def test_invalid_sha256_is_incomplete(self) -> None:
        row = complete_source_row()
        row["sha256"] = "abc123"
        self.assertIn("64-hex SHA-256", m1_readiness.source_metadata_errors(row))
        self.assertFalse(m1_readiness.source_complete(row))

    def test_absolute_windows_path_is_not_alias(self) -> None:
        row = complete_source_row()
        row["external_path"] = "C:/actual/path/source.pdf"
        self.assertIn("path alias", m1_readiness.source_metadata_errors(row))
        self.assertFalse(m1_readiness.source_complete(row))

    def test_url_is_not_path_alias(self) -> None:
        row = complete_source_row()
        row["external_path"] = "https://example.invalid/source.pdf"
        self.assertIn("path alias", m1_readiness.source_metadata_errors(row))
        self.assertFalse(m1_readiness.source_complete(row))

    def test_candidate_review_state_is_incomplete(self) -> None:
        row = complete_source_row()
        row["review_state"] = "candidate"
        self.assertIn("review_state", m1_readiness.source_metadata_errors(row))
        self.assertFalse(m1_readiness.source_complete(row))


if __name__ == "__main__":
    unittest.main()
