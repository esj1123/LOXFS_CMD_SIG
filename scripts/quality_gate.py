#!/usr/bin/env python3
"""Phase 0 hardening quality gate."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import validate_repo


GATES = [
    (("structure",), "repository structure"),
    (("document",), "document authority"),
    (("schema",), "CSV/JSON schema"),
    (("reference",), "reference integrity"),
    (("protocol",), "protocol structure"),
    (("storage", "forbidden"), "storage boundary"),
    (("secret", "network", "safety"), "credential/network safety"),
    (("git",), "Git safety"),
]
SAFETY_WARNING_CATEGORIES = {"safety", "storage", "secret", "network"}


@dataclass(frozen=True)
class TestResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def passed(self) -> bool:
        return self.returncode == 0


@dataclass(frozen=True)
class GateResult:
    issues: list[validate_repo.Issue]
    test_result: TestResult | None

    @property
    def errors(self) -> list[validate_repo.Issue]:
        return [issue for issue in self.issues if issue.level == "ERROR"]

    @property
    def warnings(self) -> list[validate_repo.Issue]:
        return [issue for issue in self.issues if issue.level == "WARNING"]

    @property
    def failed(self) -> bool:
        if self.errors:
            return True
        if self.test_result is not None and not self.test_result.passed:
            return True
        return False


def run_unittests(root: Path) -> TestResult:
    result = subprocess.run(
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return TestResult(returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)


def evaluate_quality_gate(root: Path | str, run_tests: bool = True) -> GateResult:
    root = Path(root).resolve()
    issues = list(validate_repo.run_checks(root))
    for issue in list(issues):
        if issue.level == "WARNING" and issue.category in SAFETY_WARNING_CATEGORIES:
            issues.append(validate_repo.Issue(issue.category, "ERROR", f"safety warning escalated: {issue.message}"))
    test_result = run_unittests(root) if run_tests else None
    return GateResult(issues=issues, test_result=test_result)


def print_gate(result: GateResult) -> int:
    errors = result.errors
    warnings = result.warnings
    for categories, label in GATES:
        category_errors = [issue for issue in errors if issue.category in categories]
        status = "FAIL" if category_errors else "PASS"
        print(f"{label}: {status}")
        for issue in category_errors:
            print(f"  - {issue.message}")

    if result.test_result is None:
        print("validator unit tests: SKIPPED")
    elif result.test_result.passed:
        print("validator unit tests: PASS")
    else:
        print("validator unit tests: FAIL")
        for line in (result.test_result.stdout + result.test_result.stderr).splitlines()[-20:]:
            print(f"  {line}")

    acceptance_errors = [issue for issue in errors if issue.category == "acceptance"]
    print(f"acceptance trace consistency: {'FAIL' if acceptance_errors else 'PASS'}")
    for issue in acceptance_errors:
        print(f"  - {issue.message}")

    print("M1 readiness summary: see scripts/m1_readiness.py")
    for issue in warnings:
        print(f"WARNING [{issue.category}] {issue.message}")

    if result.failed:
        print("QUALITY_GATE_FAIL")
        print(f"summary: errors={len(errors)} warnings={len(warnings)}")
        return 1

    print("QUALITY_GATE_PASS")
    print(f"warning count: {len(warnings)}")
    print("summary: errors=0 warnings={}".format(len(warnings)))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 0 quality gate.")
    parser.add_argument("--root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--skip-tests", action="store_true", help="Skip unittest discovery.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = evaluate_quality_gate(args.root, run_tests=not args.skip_tests)
    return print_gate(result)


if __name__ == "__main__":
    raise SystemExit(main())
