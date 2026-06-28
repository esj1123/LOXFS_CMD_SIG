from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_repo  # noqa: E402


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def write_text(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(root: Path, rel: str, rows: list[dict[str, str]]) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=validate_repo.CSV_HEADERS[rel])
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(root: Path, rel: str) -> list[dict[str, str]]:
    with (root / rel).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def rewrite_csv(root: Path, rel: str, rows: list[dict[str, str]]) -> None:
    write_csv(root, rel, rows)


def valid_profile() -> dict[str, object]:
    return {
        "profile_id": "local-laptop",
        "environment": "isolated_local",
        "transport": "udp",
        "channels": [
            {"channel_id": 1, "bind_address": "127.0.0.1", "port": 17101},
            {"channel_id": 2, "bind_address": "127.0.0.1", "port": 17102},
            {"channel_id": 3, "bind_address": "127.0.0.1", "port": 17103},
        ],
        "allow_physical_controller": False,
        "allow_non_loopback": False,
        "allow_legacy_binary_execution": False,
        "allow_netarrays_force": False,
        "allow_actual_configuration": False,
    }


def source_scope(source_id: str) -> str:
    if source_id == "SRC-PROTO-001":
        return "common"
    return "K117 baseline"


def valid_readme() -> str:
    return """# Synthetic Harness

Synthetic repository for validator tests.

README.md is a navigation document, not the live status source.

## Project Path

M0 Repository and Source Baseline
-> M1 Protocol Core
-> M2 Local UDP Loopback
-> M3 Legacy RSID Characterization
-> M4 NetArrays Simulator Adapter PoC
-> M5 Closed-loop Representative Scenario
-> M6 Pattern-based Regression and Fault Injection

- Detailed phase definitions: [docs/DEVELOPMENT_PLAN.md](docs/DEVELOPMENT_PLAN.md)
- Current phase and blockers: [STATUS.md](STATUS.md)
- M1 entry conditions: [docs/M1_READINESS.md](docs/M1_READINESS.md)
- Validation evidence: [ACCEPTANCE_TRACE.md](ACCEPTANCE_TRACE.md)
- Commands: [docs/RUNBOOK.md](docs/RUNBOOK.md)

## Document Authority

| Information | Canonical source |
|---|---|
| Project purpose and scope | README.md, docs/SCOPE.md |
| M0-M6 phase definitions and delivery path | docs/DEVELOPMENT_PLAN.md |
| Current phase and blockers | STATUS.md |
| M1 entry conditions | docs/M1_READINESS.md, scripts/m1_readiness.py |
| Decision state | references/decision_register.csv |
| Source baseline state | references/source_register.csv |
| Validation evidence | ACCEPTANCE_TRACE.md |
| Commands | docs/RUNBOOK.md |
| Target architecture | docs/ARCHITECTURE.md |
"""


def valid_agents() -> str:
    return """# Synthetic Rules

## Required Startup Read

- README.md
- AGENTS.md
- STATUS.md
- docs/SAFETY_BOUNDARY.md
- references/decision_register.csv

For work that changes or interprets phase path, phase scope, or delivery sequence, also read docs/DEVELOPMENT_PLAN.md before changing files.

## Document Authority and Conflict Resolution

- Phase definitions and phase sequence follow docs/DEVELOPMENT_PLAN.md.
- Current phase and blockers follow STATUS.md only.
- M1 entry judgment follows scripts/m1_readiness.py and docs/M1_READINESS.md.
- Decision state follows references/decision_register.csv.
- Source state follows references/source_register.csv.
- Validation evidence follows ACCEPTANCE_TRACE.md.
- Execution commands follow docs/RUNBOOK.md.
- If a summary document conflicts with a canonical source, prefer the canonical source.
- If drift is found, report it as drift instead of merging values by assumption.
- Do not copy current status or validation results into README.md or docs/DEVELOPMENT_PLAN.md.
- Do not create docs/ROADMAP.md without explicit user request and document role.

## Build-Stage Borrowed Practices

- Task contract: identify goal, scope, likely touch files, likely no-touch files, expected verification, and side effects not performed.
- Change class: classify work as documentation-only, validation-surface, source-register, storage-boundary, implementation, or side-effecting.
- Verification hygiene: mark skipped checks as NOT RUN with a reason.
- Closeout Receipt: distinguish commands run, commands not run, side effects not performed, blocker status, and required owner actions.
- Later borrowing requires scoped owner approval.
"""


def valid_test_policy() -> str:
    return """# Test Policy

## Verification Hygiene

- Report skipped checks as NOT RUN with a reason.
- Do not imply success for a check that was not executed.
- Focused verification is acceptable only when scope is named.
- Negative tests must prove unsafe examples fail.
"""


def valid_runbook() -> str:
    return """# Runbook

## Closeout Receipt

- changed files
- commands run
- commands not run
- validation and readiness results
- required owner actions
"""


def valid_development_plan() -> str:
    return """# Development Plan

## Document Role

This document is the canonical delivery roadmap for M0 through M6.

It owns:

- phase objectives
- phase sequence
- entry conditions
- work scope
- exit conditions

It does not own:

- current phase
- current blockers
- readiness result
- decision status
- source collection status
- validation result
- execution commands

Canonical references:

- Current state: ../STATUS.md
- M1 entry definition: M1_READINESS.md
- Decision state: ../references/decision_register.csv
- Source state: ../references/source_register.csv
- Validation evidence: ../ACCEPTANCE_TRACE.md
- Commands: RUNBOOK.md
- Architecture: ARCHITECTURE.md

## Build-Stage Governance Imports

The approved imports are task contract discipline, change class discipline, verification hygiene, and closeout receipt discipline.

## M0: Repository and Source Baseline Hardening

Entry: Synthetic entry.

Work: Synthetic work.

Exit criteria: Synthetic exit.

## M1: Protocol Core

Entry: Synthetic entry.

Work: Synthetic work.

Exit criteria: Synthetic exit.

## M2: Local UDP Loopback

Entry: Synthetic entry.

Work: Synthetic work.

Exit criteria: Synthetic exit.

## M3: Legacy RSID Black-Box Characterization

Entry: Synthetic entry.

Work: Synthetic work.

Exit criteria: Synthetic exit.

## M4: NetArrays Simulator Tag Mapping PoC

Entry: Synthetic entry.

Work: Synthetic work.

Exit criteria: Synthetic exit.

## M5: Closed-Loop Representative Scenario

Entry: Synthetic entry.

Work: Synthetic work.

Exit criteria: Synthetic exit.

## M6: Pattern-Based Regression and Fault Injection

Entry: Synthetic entry.

Work: Synthetic work.

Exit criteria: Synthetic exit.
"""


def make_valid_repo() -> tempfile.TemporaryDirectory[str]:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    for rel in validate_repo.REQUIRED_DIRS:
        (root / rel).mkdir(parents=True, exist_ok=True)

    write_text(root, ".gitignore", "\n".join(validate_repo.REQUIRED_GITIGNORE_PATTERNS) + "\n")
    write_text(root, "ACCEPTANCE_TRACE.md", "\n".join(validate_repo.ACCEPTANCE_HARDENING_ITEMS) + "\n")
    for rel in validate_repo.REQUIRED_FILES:
        if rel in validate_repo.CSV_HEADERS or rel in {".gitignore", "ACCEPTANCE_TRACE.md", "profiles/local-laptop/profile.template.json"}:
            continue
        write_text(root, rel, f"# {Path(rel).name}\n")
    write_text(root, "README.md", valid_readme())
    write_text(root, "AGENTS.md", valid_agents())
    write_text(root, "docs/TEST_POLICY.md", valid_test_policy())
    write_text(root, "docs/RUNBOOK.md", valid_runbook())
    write_text(root, "docs/DEVELOPMENT_PLAN.md", valid_development_plan())

    sources = [
        {
            "source_id": source_id,
            "system": "common",
            "title": source_id,
            "revision": "TBD",
            "authority_scope": source_scope(source_id),
            "source_role": "test",
            "external_path": "TBD",
            "sha256": "TBD",
            "sensitivity": "external_reference",
            "owner": "TBD",
            "review_state": "not_collected",
            "notes": "synthetic test row",
        }
        for source_id in ["SRC-PROTO-001", "SRC-K117-001", "SRC-NA-001", "SRC-TIME-001", "SRC-RSIDCFG-001", "SRC-NETMAP-001"]
    ]
    write_csv(root, "references/source_register.csv", sources)
    write_csv(
        root,
        "references/artifact_manifest.csv",
        [
            {
                "artifact_id": "ART-CFG-001",
                "artifact_type": "configuration",
                "title": "synthetic",
                "external_path": "TBD",
                "sha256": "TBD",
                "source_id": "SRC-RSIDCFG-001",
                "git_policy": "external_only",
                "review_state": "not_collected",
                "notes": "synthetic",
            }
        ],
    )
    write_csv(
        root,
        "references/decision_register.csv",
        [
            {
                "decision_id": "DEC-DEV-001",
                "topic": "runtime",
                "status": "Open",
                "priority": "P0",
                "owner_role": "owner",
                "source_basis": "",
                "decision_needed": "runtime",
                "blocking_impact": "M1",
                "next_action": "review",
                "notes": "",
            },
            {
                "decision_id": "DEC-RETRY-001",
                "topic": "retry",
                "status": "Open",
                "priority": "P0",
                "owner_role": "owner",
                "source_basis": "SRC-PROTO-001",
                "decision_needed": "retry",
                "blocking_impact": "M1",
                "next_action": "review",
                "notes": "",
            },
            {
                "decision_id": "DEC-STORAGE-001",
                "topic": "storage",
                "status": "Open",
                "priority": "P0",
                "owner_role": "owner",
                "source_basis": "",
                "decision_needed": "storage",
                "blocking_impact": "M1",
                "next_action": "review",
                "notes": "",
            },
            {
                "decision_id": "DEC-REPO-001",
                "topic": "repo",
                "status": "Open",
                "priority": "P0",
                "owner_role": "owner",
                "source_basis": "",
                "decision_needed": "repo",
                "blocking_impact": "M1",
                "next_action": "review",
                "notes": "",
            },
        ],
    )
    write_csv(
        root,
        "specs/common/protocol/header_fields.csv",
        [
            {"field_order": "1", "field_name": "a", "offset_bytes": "0", "length_bytes": "4", "endian": "big", "source_status": "candidate", "source_ref": "SRC-PROTO-001", "notes": ""},
            {"field_order": "2", "field_name": "b", "offset_bytes": "4", "length_bytes": "4", "endian": "big", "source_status": "candidate", "source_ref": "SRC-PROTO-001", "notes": ""},
            {"field_order": "3", "field_name": "c", "offset_bytes": "8", "length_bytes": "4", "endian": "big", "source_status": "candidate", "source_ref": "SRC-PROTO-001", "notes": ""},
            {"field_order": "4", "field_name": "d", "offset_bytes": "12", "length_bytes": "4", "endian": "big", "source_status": "candidate", "source_ref": "SRC-PROTO-001", "notes": ""},
            {"field_order": "5", "field_name": "e", "offset_bytes": "16", "length_bytes": "8", "endian": "big", "source_status": "candidate", "source_ref": "SRC-PROTO-001", "notes": ""},
            {"field_order": "6", "field_name": "f", "offset_bytes": "24", "length_bytes": "16", "endian": "n/a", "source_status": "Open", "source_ref": "SRC-PROTO-001", "notes": ""},
            {"field_order": "7", "field_name": "g", "offset_bytes": "40", "length_bytes": "4", "endian": "big", "source_status": "Open", "source_ref": "SRC-PROTO-001", "notes": ""},
            {"field_order": "8", "field_name": "h", "offset_bytes": "44", "length_bytes": "4", "endian": "big", "source_status": "Open", "source_ref": "SRC-PROTO-001", "notes": ""},
        ],
    )
    write_csv(
        root,
        "specs/common/protocol/data_block_fields.csv",
        [
            {"field_order": "1", "field_name": "a", "offset_bytes": "0", "length_bytes": "1", "endian": "big", "source_status": "candidate", "source_ref": "SRC-PROTO-001", "notes": ""},
            {"field_order": "2", "field_name": "b", "offset_bytes": "1", "length_bytes": "1", "endian": "big", "source_status": "candidate", "source_ref": "SRC-PROTO-001", "notes": ""},
            {"field_order": "3", "field_name": "c", "offset_bytes": "2", "length_bytes": "4", "endian": "big", "source_status": "candidate", "source_ref": "SRC-PROTO-001", "notes": ""},
            {"field_order": "4", "field_name": "d", "offset_bytes": "6", "length_bytes": "4", "endian": "big", "source_status": "candidate", "source_ref": "SRC-PROTO-001", "notes": ""},
        ],
    )
    write_csv(
        root,
        "specs/common/protocol/packet_types.csv",
        [
            {"type_value": "34", "type_name": "USR_CONTROL", "ack_type_value": "35", "direction": "command_to_peer", "source_status": "candidate", "notes": ""},
            {"type_value": "35", "type_name": "USR_CONTROL_ACK", "ack_type_value": "", "direction": "ack_to_sender", "source_status": "candidate", "notes": ""},
        ],
    )
    write_csv(
        root,
        "specs/common/protocol/session_controls.csv",
        [
            {"detail_value": "50", "detail_name": "SESSION_CLOSE", "ack_detail_value": "51", "source_status": "candidate", "notes": ""},
            {"detail_value": "51", "detail_name": "SESSION_CLOSE_ACK", "ack_detail_value": "", "source_status": "candidate", "notes": ""},
        ],
    )
    write_csv(
        root,
        "specs/common/protocol/ack_retry_rules.csv",
        [
            {"rule_id": "ACK-001", "trigger": "packet", "expected_behavior": "ack", "parameter_name": "ack_latency", "parameter_value": "TBD", "status": "Open", "source_ref": "SRC-PROTO-001", "notes": ""},
            {"rule_id": "ACK-002", "trigger": "ack", "expected_behavior": "header only", "parameter_name": "ack_payload_size", "parameter_value": "0", "status": "candidate", "source_ref": "SRC-PROTO-001", "notes": ""},
        ],
    )
    write_csv(
        root,
        "specs/baselines/k117-loxfs/command_signal_catalog.csv",
        [{"catalog_id": "CAT-001", "legacy_id": "TBD", "name": "TBD", "direction": "TBD", "data_type": "TBD", "value_rule": "TBD", "loxfs_tag": "TBD", "applicability": "TBD", "owner_review": "required", "source_ref": "SRC-K117-001", "notes": ""}],
    )
    write_csv(root, "specs/baselines/k117-loxfs/loxfs_tag_mapping.csv", [])
    write_csv(root, "specs/baselines/k117-loxfs/scan_timing.csv", [{"timing_id": "TIME-001", "item": "actual", "value": "TBD", "unit": "ms", "status": "Open", "source_ref": "SRC-TIME-001", "notes": ""}])
    write_csv(root, "specs/baselines/k117-loxfs/legacy_behavior_matrix.csv", [])
    write_csv(root, "scenarios/templates/nominal.template.csv", [])
    write_csv(root, "scenarios/templates/fault_injection.template.csv", [])
    write_text(root, "profiles/local-laptop/profile.template.json", json.dumps(valid_profile(), indent=2))
    git(root, "init")
    git(root, "add", ".")
    return tmp


def errors(root: Path) -> list[str]:
    return [issue.message for issue in validate_repo.run_checks(root) if issue.level == "ERROR"]


class ValidateRepoTests(unittest.TestCase):
    def assert_has_error(self, root: Path, fragment: str) -> None:
        messages = errors(root)
        self.assertTrue(any(fragment in message for message in messages), messages)

    def test_minimal_valid_repository_passes(self) -> None:
        with make_valid_repo() as root_name:
            self.assertEqual(errors(Path(root_name)), [])

    def test_tracked_pdf_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "evidence.pdf", "synthetic text only")
            git(root, "add", "-f", "evidence.pdf")
            self.assert_has_error(root, "forbidden tracked extension")

    def test_tracked_docx_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "evidence.docx", "synthetic text only")
            git(root, "add", "-f", "evidence.docx")
            self.assert_has_error(root, "forbidden tracked extension")

    def test_tracked_exe_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "tool.exe", "synthetic text only")
            git(root, "add", "-f", "tool.exe")
            self.assert_has_error(root, "forbidden tracked extension")

    def test_tracked_local_actual_config_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "local/actual_config.json", "{}")
            git(root, "add", "-f", "local/actual_config.json")
            self.assert_has_error(root, "forbidden tracked path")

    def test_json_password_actual_value_fails_without_printing_value(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            key = "pass" + "word"
            value = "synthetic" + "-secret"
            write_text(root, "settings.json", json.dumps({key: value}) + "\n")
            git(root, "add", "settings.json")
            messages = errors(root)
            self.assertTrue(any("settings.json:1:password" in message for message in messages), messages)
            self.assertFalse(any(value in message for message in messages), messages)

    def test_yaml_secret_actual_value_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            key = "sec" + "ret"
            value = "synthetic" + "-secret"
            write_text(root, "settings.yaml", f"{key}: {value}\n")
            git(root, "add", "settings.yaml")
            self.assert_has_error(root, "settings.yaml:1:secret")

    def test_placeholder_credential_allowed(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            first_key = "pass" + "word"
            second_key = "tok" + "en"
            write_text(root, "settings.json", json.dumps({first_key: "REDACTED", second_key: "${ENV_VAR}"}) + "\n")
            git(root, "add", "settings.json")
            self.assertFalse(any("credential candidate" in message for message in errors(root)))

    def test_markdown_local_absolute_path_fails_without_printing_value(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            path_value = "C:\\Users\\Owner\\Documents\\source.pdf"
            write_text(root, "docs/local_note.md", f"source path: {path_value}\n")
            messages = errors(root)
            self.assertTrue(any("local absolute path candidate: docs/local_note.md:1" in message for message in messages), messages)
            self.assertFalse(any(path_value in message for message in messages), messages)

    def test_documented_template_local_root_path_allowed(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            write_text(root, "docs/local_root_example.md", "template only: C:\\LOXFS_CMD_SIG_LOCAL\\artifacts\n")
            self.assertFalse(any("local absolute path candidate" in message for message in errors(root)))

    def test_non_loopback_ipv4_in_profile_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            profile = valid_profile()
            profile["channels"][0]["bind_address"] = "10.1.2.3"  # type: ignore[index]
            write_text(root, "profiles/local-laptop/profile.template.json", json.dumps(profile))
            self.assert_has_error(root, "non-loopback bind address")

    def test_zero_bind_address_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            profile = valid_profile()
            profile["channels"][0]["bind_address"] = "0.0.0.0"  # type: ignore[index]
            write_text(root, "profiles/local-laptop/profile.template.json", json.dumps(profile))
            self.assert_has_error(root, "non-loopback bind address")

    def test_loopback_only_profile_allowed(self) -> None:
        with make_valid_repo() as root_name:
            self.assertFalse(any("non-loopback" in message for message in errors(Path(root_name))))

    def test_unapproved_git_remote_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            git(root, "remote", "add", "origin", "https://example.invalid/repo.git")
            self.assert_has_error(root, "unapproved Git remote configured")

    def test_approved_backup_git_remote_passes(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            git(root, "remote", "add", "origin", "https://github.com/esj1123/LOXFS_CMD_SIG.git")
            self.assertFalse(any("remote" in message.lower() for message in errors(root)))

    def test_additional_git_remote_fails_even_with_backup_origin(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            git(root, "remote", "add", "origin", "https://github.com/esj1123/LOXFS_CMD_SIG.git")
            git(root, "remote", "add", "mirror", "https://example.invalid/repo.git")
            self.assert_has_error(root, "unapproved Git remote configured: mirror")

    def test_missing_gitignore_pattern_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            patterns = [pattern for pattern in validate_repo.REQUIRED_GITIGNORE_PATTERNS if pattern != "local/"]
            write_text(root, ".gitignore", "\n".join(patterns) + "\n")
            self.assert_has_error(root, "required .gitignore pattern missing: local/")

    def test_missing_temporary_upload_gitignore_pattern_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            patterns = [pattern for pattern in validate_repo.REQUIRED_GITIGNORE_PATTERNS if pattern != ".tmp.driveupload/"]
            write_text(root, ".gitignore", "\n".join(patterns) + "\n")
            self.assert_has_error(root, "required .gitignore pattern missing: .tmp.driveupload/")


if __name__ == "__main__":
    unittest.main()
