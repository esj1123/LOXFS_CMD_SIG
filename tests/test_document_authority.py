from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

import validate_repo  # noqa: E402
from test_validate_repo import (  # noqa: E402
    make_valid_repo,
    valid_agents,
    valid_development_plan,
    valid_readme,
    valid_runbook,
    valid_test_policy,
    write_text,
)


def document_errors(root: Path) -> list[str]:
    return [issue.message for issue in validate_repo.run_checks(root) if issue.level == "ERROR" and issue.category == "document"]


class DocumentAuthorityTests(unittest.TestCase):
    def assert_document_error(self, root: Path, fragment: str) -> None:
        messages = document_errors(root)
        self.assertTrue(any(fragment in message for message in messages), messages)

    def test_valid_canonical_document_structure_passes(self) -> None:
        with make_valid_repo() as root_name:
            self.assertEqual(document_errors(Path(root_name)), [])

    def test_readme_missing_development_plan_link_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "README.md", valid_readme().replace("docs/DEVELOPMENT_PLAN.md", "docs/PLAN.md"))
            self.assert_document_error(root, "README missing required canonical link: docs/DEVELOPMENT_PLAN.md")

    def test_readme_missing_status_link_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "README.md", valid_readme().replace("STATUS.md", "STATE.md"))
            self.assert_document_error(root, "README missing required canonical link: STATUS.md")

    def test_development_plan_missing_m3_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            text = valid_development_plan()
            start = text.index("## M3:")
            end = text.index("## M4:")
            write_text(root, "docs/DEVELOPMENT_PLAN.md", text[:start] + text[end:])
            self.assert_document_error(root, "DEVELOPMENT_PLAN missing phase heading: M3")

    def test_development_plan_duplicate_m2_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            text = valid_development_plan()
            start = text.index("## M2:")
            end = text.index("## M3:")
            m2_section = text[start:end]
            write_text(root, "docs/DEVELOPMENT_PLAN.md", text[:end] + m2_section + text[end:])
            self.assert_document_error(root, "DEVELOPMENT_PLAN duplicate phase heading: M2")

    def test_readme_fixed_quality_gate_result_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "README.md", valid_readme() + "\nQuality Gate: FAIL\n")
            self.assert_document_error(root, "README.md contains fixed live-result pattern: Quality Gate: FAIL")

    def test_development_plan_fixed_m1_readiness_result_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "docs/DEVELOPMENT_PLAN.md", valid_development_plan() + "\nM1_READINESS_BLOCKED\n")
            self.assert_document_error(root, "docs/DEVELOPMENT_PLAN.md contains fixed live-result pattern: M1_READINESS_BLOCKED")

    def test_agents_missing_conflict_resolution_rules_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "AGENTS.md", "# Synthetic Rules\n")
            self.assert_document_error(root, "AGENTS missing conflict resolution marker")

    def test_readme_project_path_phase_names_passes(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            text = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn("## Project Path", text)
            self.assertIn("M0 Repository and Source Baseline", text)
            self.assertIn("M6 Pattern-based Regression and Fault Injection", text)
            self.assertNotIn("Entry:", text)
            self.assertEqual(document_errors(root), [])

    def test_development_plan_entry_work_exit_preserved_passes(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            text = (root / "docs/DEVELOPMENT_PLAN.md").read_text(encoding="utf-8")
            for marker in ("Entry:", "Work:", "Exit criteria:"):
                self.assertIn(marker, text)
            self.assertEqual(document_errors(root), [])

    def test_agents_missing_build_stage_borrowed_practices_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "AGENTS.md", valid_agents().replace("## Build-Stage Borrowed Practices", "## Local Rules"))
            self.assert_document_error(root, "AGENTS missing build-stage governance marker")

    def test_test_policy_missing_not_run_reporting_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "docs/TEST_POLICY.md", valid_test_policy().replace("NOT RUN", "SKIPPED"))
            self.assert_document_error(root, "TEST_POLICY missing verification hygiene marker: NOT RUN")

    def test_runbook_missing_closeout_receipt_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "docs/RUNBOOK.md", valid_runbook().replace("## Closeout Receipt", "## Report"))
            self.assert_document_error(root, "RUNBOOK missing closeout receipt marker: Closeout Receipt")

    def test_development_plan_missing_build_stage_governance_imports_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "docs/DEVELOPMENT_PLAN.md", valid_development_plan().replace("## Build-Stage Governance Imports", "## Local Governance"))
            self.assert_document_error(root, "DEVELOPMENT_PLAN missing build-stage governance marker")


if __name__ == "__main__":
    unittest.main()
