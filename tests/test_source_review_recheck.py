from __future__ import annotations

import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import source_review_recheck  # noqa: E402


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def write_notes(root: Path, alias: str, data: bytes) -> Path:
    notes = root / "docs" / "SOURCE_REVIEW_NOTES.md"
    notes.parent.mkdir(parents=True, exist_ok=True)
    notes.write_text(
        "\n".join(
            [
                "# Source Review Notes",
                "",
                "This file is a provisional, not approval, does not close decisions receipt.",
                "",
                "### 1. Synthetic Source",
                "",
                "| Field | Value |",
                "| --- | --- |",
                "| Candidate source ID | `SRC-SYN-001` |",
                f"| Alias | `{alias}` |",
                f"| Size | {len(data)} bytes |",
                f"| SHA-256 | `{digest(data)}` |",
                "| verification_status | `observed_in_session`; `owner_review_required` |",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return notes


class SourceReviewRecheckTests(unittest.TestCase):
    def test_parse_expected_artifacts_from_singular_table(self) -> None:
        with tempfile.TemporaryDirectory() as root_name:
            root = Path(root_name)
            data = b"synthetic source bytes"
            notes = write_notes(root, "ARTIFACTS/source.bin", data)

            artifacts = source_review_recheck.parse_expected_artifacts(notes)

            self.assertEqual(len(artifacts), 1)
            self.assertEqual(artifacts[0].alias, "ARTIFACTS/source.bin")
            self.assertEqual(artifacts[0].size, len(data))
            self.assertEqual(artifacts[0].sha256, digest(data))

    def test_matching_external_file_passes(self) -> None:
        with tempfile.TemporaryDirectory() as repo_name, tempfile.TemporaryDirectory() as local_name:
            repo = Path(repo_name)
            local = Path(local_name)
            data = b"synthetic source bytes"
            notes = write_notes(repo, "ARTIFACTS/source.bin", data)
            artifact = local / "ARTIFACTS" / "source.bin"
            artifact.parent.mkdir(parents=True)
            artifact.write_bytes(data)

            results = source_review_recheck.recheck(notes, local, repo)

            self.assertEqual([result.status for result in results], ["matched"])

    def test_missing_external_file_fails_without_root_path(self) -> None:
        with tempfile.TemporaryDirectory() as repo_name, tempfile.TemporaryDirectory() as local_name:
            repo = Path(repo_name)
            local = Path(local_name)
            data = b"synthetic source bytes"
            notes = write_notes(repo, "ARTIFACTS/source.bin", data)

            results = source_review_recheck.recheck(notes, local, repo)

            self.assertEqual([result.status for result in results], ["missing"])
            self.assertEqual(results[0].artifact.alias, "ARTIFACTS/source.bin")
            self.assertNotIn(str(local), results[0].artifact.alias)

    def test_hash_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as repo_name, tempfile.TemporaryDirectory() as local_name:
            repo = Path(repo_name)
            local = Path(local_name)
            data = b"synthetic source bytes"
            notes = write_notes(repo, "ARTIFACTS/source.bin", data)
            artifact = local / "ARTIFACTS" / "source.bin"
            artifact.parent.mkdir(parents=True)
            artifact.write_bytes(b"Synthetic source bytes")

            results = source_review_recheck.recheck(notes, local, repo)

            self.assertEqual([result.status for result in results], ["hash_mismatch"])

    def test_root_inside_repo_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as repo_name:
            repo = Path(repo_name)
            local = repo / "local"
            local.mkdir()
            notes = write_notes(repo, "ARTIFACTS/source.bin", b"synthetic source bytes")

            with self.assertRaisesRegex(ValueError, "outside the repository"):
                source_review_recheck.recheck(notes, local, repo)

    def test_missing_local_root_setting_blocks_main(self) -> None:
        with tempfile.TemporaryDirectory() as repo_name:
            repo = Path(repo_name)
            write_notes(repo, "ARTIFACTS/source.bin", b"synthetic source bytes")
            with patch.dict(os.environ, {"LOXFS_CMD_SIG_LOCAL_ROOT": ""}, clear=False):
                with patch.object(sys, "argv", ["source_review_recheck.py", "--root", str(repo)]):
                    self.assertEqual(source_review_recheck.main(), 1)


if __name__ == "__main__":
    unittest.main()
