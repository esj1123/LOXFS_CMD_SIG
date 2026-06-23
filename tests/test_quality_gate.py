from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import quality_gate  # noqa: E402
from test_validate_repo import make_valid_repo, write_text  # noqa: E402


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


class QualityGateTests(unittest.TestCase):
    def test_quality_gate_passes_minimal_valid_repository_without_running_nested_tests(self) -> None:
        with make_valid_repo() as root_name:
            result = quality_gate.evaluate_quality_gate(Path(root_name), run_tests=False)
            self.assertFalse(result.failed)

    def test_quality_gate_fails_on_validator_error(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "payload.exe", "synthetic text only")
            git(root, "add", "-f", "payload.exe")
            result = quality_gate.evaluate_quality_gate(root, run_tests=False)
            self.assertTrue(result.failed)


if __name__ == "__main__":
    unittest.main()
