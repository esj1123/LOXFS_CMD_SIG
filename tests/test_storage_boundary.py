from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import bootstrap_local_workspace  # noqa: E402
import validate_repo  # noqa: E402
from test_validate_repo import make_valid_repo, write_text  # noqa: E402


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def errors(root: Path) -> list[str]:
    return [issue.message for issue in validate_repo.run_checks(root) if issue.level == "ERROR"]


def issues(root: Path) -> list[validate_repo.Issue]:
    return validate_repo.run_checks(root)


class StorageBoundaryTests(unittest.TestCase):
    def test_untracked_pdf_in_repo_root_fails_storage_boundary(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "untracked.pdf", "synthetic text only")
            messages = errors(root)
            self.assertTrue(any("repo worktree forbidden artifact" in message for message in messages), messages)

    def test_untracked_office_file_in_repo_fails_storage_boundary(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "untracked.docx", "synthetic text only")
            messages = errors(root)
            self.assertTrue(any("repo worktree forbidden artifact" in message for message in messages), messages)

    def test_openable_zero_byte_office_file_still_fails_storage_boundary(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "zero-byte.docx", "")
            messages = errors(root)
            self.assertTrue(any("repo worktree forbidden artifact" in message for message in messages), messages)

    def test_environmental_decoy_candidate_is_not_storage_error(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "security-decoy.docx", "")
            decoy_path = root / "security-decoy.docx"

            def fake_decoy(path: Path, _root: Path, _tracked: set[str]) -> bool:
                return path == decoy_path

            with patch("validate_repo.is_environmental_decoy_candidate", side_effect=fake_decoy):
                observed = issues(root)

            messages = [issue.message for issue in observed]
            storage_errors = [
                issue
                for issue in observed
                if issue.level == "ERROR" and issue.category == "storage" and "security-decoy.docx" in issue.message
            ]
            self.assertEqual(storage_errors, [], messages)
            self.assertTrue(any("environmental decoy candidate: security-decoy.docx" in message for message in messages), messages)

    def test_tracked_environmental_decoy_name_still_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "security-decoy.docx", "")
            git(root, "add", "-f", "security-decoy.docx")

            with patch("validate_repo.is_environmental_decoy_candidate", return_value=True):
                messages = errors(root)

            self.assertTrue(any("forbidden tracked extension" in message for message in messages), messages)

    def test_external_local_root_inside_repo_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            repo_root.mkdir()
            local_root = repo_root / "local-root"
            messages = bootstrap_local_workspace.validate_local_root(repo_root, local_root)
            self.assertTrue(any("inside the source repository" in message for message in messages), messages)

    def test_valid_external_local_root_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            repo_root.mkdir()
            local_root = Path(tmp) / "external" / "LOXFS_CMD_SIG_LOCAL"
            self.assertEqual(bootstrap_local_workspace.validate_local_root(repo_root, local_root), [])

    def test_external_local_root_in_known_sync_root_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            repo_root.mkdir()
            local_root = Path(tmp) / "OneDrive" / "LOXFS_CMD_SIG_LOCAL"
            messages = bootstrap_local_workspace.validate_local_root(repo_root, local_root)
            self.assertTrue(any("known sync root" in message for message in messages), messages)


if __name__ == "__main__":
    unittest.main()
