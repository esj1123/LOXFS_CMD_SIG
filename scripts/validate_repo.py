#!/usr/bin/env python3
"""Fail-closed repository validation for Phase 0 hardening.

The validator intentionally checks both Git-tracked source and the full
worktree storage boundary. It never prints secret values or file contents.
"""

from __future__ import annotations

import argparse
import csv
import ipaddress
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


BOM = b"\xef\xbb\xbf"

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "STATUS.md",
    "CHANGELOG.md",
    "ACCEPTANCE_TRACE.md",
    ".gitignore",
    "docs/SCOPE.md",
    "docs/ARCHITECTURE.md",
    "docs/SAFETY_BOUNDARY.md",
    "docs/STORAGE_BOUNDARY.md",
    "docs/M1_READINESS.md",
    "docs/SOURCE_BASELINE_PLAN.md",
    "docs/DEVELOPMENT_PLAN.md",
    "docs/TEST_POLICY.md",
    "docs/LEGACY_ANALYSIS_PLAN.md",
    "docs/ENVIRONMENT_DISCOVERY.md",
    "docs/RUNBOOK.md",
    "references/source_register.csv",
    "references/artifact_manifest.csv",
    "references/decision_register.csv",
    "specs/common/protocol/header_fields.csv",
    "specs/common/protocol/data_block_fields.csv",
    "specs/common/protocol/packet_types.csv",
    "specs/common/protocol/session_controls.csv",
    "specs/common/protocol/ack_retry_rules.csv",
    "specs/common/protocol/README.md",
    "specs/baselines/k117-loxfs/command_signal_catalog.csv",
    "specs/baselines/k117-loxfs/loxfs_tag_mapping.csv",
    "specs/baselines/k117-loxfs/scan_timing.csv",
    "specs/baselines/k117-loxfs/legacy_behavior_matrix.csv",
    "specs/targets/n3g-preliminary/README.md",
    "specs/targets/n3f-interface/README.md",
    "profiles/local-laptop/profile.template.json",
    "profiles/local-laptop/README.md",
    "scenarios/README.md",
    "scenarios/templates/nominal.template.csv",
    "scenarios/templates/fault_injection.template.csv",
    "scenarios/expected/README.md",
    "src/README.md",
    "tests/README.md",
    "scripts/bootstrap_local_workspace.py",
    "scripts/inventory_local_artifacts.py",
    "scripts/migrate_local_workspace.py",
    "scripts/validate_repo.py",
    "scripts/quality_gate.py",
    "scripts/m1_readiness.py",
    "scripts/repo.ps1",
]

REQUIRED_DIRS = [
    "docs",
    "references",
    "specs/common/protocol",
    "specs/baselines/k117-loxfs",
    "specs/targets/n3g-preliminary",
    "specs/targets/n3f-interface",
    "profiles/local-laptop",
    "scenarios/templates",
    "scenarios/expected",
    "src",
    "tests/fixtures/synthetic",
    "tests/fixtures/golden",
    "tests/expected_headers",
    "scripts",
]

CSV_HEADERS = {
    "references/source_register.csv": [
        "source_id",
        "system",
        "title",
        "revision",
        "authority_scope",
        "source_role",
        "external_path",
        "sha256",
        "sensitivity",
        "owner",
        "review_state",
        "notes",
    ],
    "references/artifact_manifest.csv": [
        "artifact_id",
        "artifact_type",
        "title",
        "external_path",
        "sha256",
        "source_id",
        "git_policy",
        "review_state",
        "notes",
    ],
    "references/decision_register.csv": [
        "decision_id",
        "topic",
        "status",
        "priority",
        "owner_role",
        "source_basis",
        "decision_needed",
        "blocking_impact",
        "next_action",
        "notes",
    ],
    "specs/common/protocol/header_fields.csv": [
        "field_order",
        "field_name",
        "offset_bytes",
        "length_bytes",
        "endian",
        "source_status",
        "source_ref",
        "notes",
    ],
    "specs/common/protocol/data_block_fields.csv": [
        "field_order",
        "field_name",
        "offset_bytes",
        "length_bytes",
        "endian",
        "source_status",
        "source_ref",
        "notes",
    ],
    "specs/common/protocol/packet_types.csv": [
        "type_value",
        "type_name",
        "ack_type_value",
        "direction",
        "source_status",
        "notes",
    ],
    "specs/common/protocol/session_controls.csv": [
        "detail_value",
        "detail_name",
        "ack_detail_value",
        "source_status",
        "notes",
    ],
    "specs/common/protocol/ack_retry_rules.csv": [
        "rule_id",
        "trigger",
        "expected_behavior",
        "parameter_name",
        "parameter_value",
        "status",
        "source_ref",
        "notes",
    ],
    "specs/baselines/k117-loxfs/command_signal_catalog.csv": [
        "catalog_id",
        "legacy_id",
        "name",
        "direction",
        "data_type",
        "value_rule",
        "loxfs_tag",
        "applicability",
        "owner_review",
        "source_ref",
        "notes",
    ],
    "specs/baselines/k117-loxfs/loxfs_tag_mapping.csv": [
        "mapping_id",
        "command_signal_id",
        "netarrays_tag",
        "tag_type",
        "direction",
        "writer_form",
        "reader_form",
        "reset_owner",
        "ptdb_device",
        "review_state",
        "source_ref",
        "notes",
    ],
    "specs/baselines/k117-loxfs/scan_timing.csv": [
        "timing_id",
        "item",
        "value",
        "unit",
        "status",
        "source_ref",
        "notes",
    ],
    "specs/baselines/k117-loxfs/legacy_behavior_matrix.csv": [
        "case_id",
        "program",
        "input_condition",
        "observed_output",
        "ack_behavior",
        "retry_behavior",
        "session_behavior",
        "log_evidence",
        "review_state",
        "notes",
    ],
    "scenarios/templates/nominal.template.csv": [
        "case_id",
        "event_index",
        "scan_index",
        "relative_time_ms",
        "direction",
        "event_type",
        "message_id",
        "value",
        "expected_by_scan",
        "expected_state",
        "notes",
    ],
    "scenarios/templates/fault_injection.template.csv": [
        "case_id",
        "event_index",
        "scan_index",
        "direction",
        "event_type",
        "message_id",
        "value",
        "fault_type",
        "fault_parameter",
        "expected_effect",
        "notes",
    ],
}

ID_COLUMNS = {
    "references/source_register.csv": "source_id",
    "references/artifact_manifest.csv": "artifact_id",
    "references/decision_register.csv": "decision_id",
    "specs/common/protocol/ack_retry_rules.csv": "rule_id",
    "specs/baselines/k117-loxfs/command_signal_catalog.csv": "catalog_id",
    "specs/baselines/k117-loxfs/loxfs_tag_mapping.csv": "mapping_id",
    "specs/baselines/k117-loxfs/scan_timing.csv": "timing_id",
    "specs/baselines/k117-loxfs/legacy_behavior_matrix.csv": "case_id",
}

REQUIRED_GITIGNORE_PATTERNS = [
    "local/",
    "runs/",
    "runtime/",
    "artifacts/",
    "config/local/",
    "profile.local.json",
    "__pycache__/",
    "*.pyc",
    "bin/",
    "obj/",
    "TestResults/",
    "*.dbn",
    "*.pgm",
    "*.exe",
    "*.dll",
    "*.pdb",
    "*.zip",
    "*.7z",
    "*.pcap",
    "*.pcapng",
    "*.db",
    "*.bak",
]

FORBIDDEN_EXTENSIONS = {
    ".dbn",
    ".pgm",
    ".exe",
    ".dll",
    ".pdb",
    ".zip",
    ".7z",
    ".rar",
    ".pcap",
    ".pcapng",
    ".db",
    ".bak",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
}
FORBIDDEN_EXACT_NAMES = {"gatewaysetting.xml", "network.cfg", "profile.local.json"}
FORBIDDEN_PATH_PREFIXES = [
    "local/",
    "runs/",
    "runtime/",
    "artifacts/",
    "config/local/",
    "__pycache__/",
    "testresults/",
    "bin/",
    "obj/",
]
WORKTREE_EXCLUDED_DIRS = {".git", "build"}

TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".csv",
    ".env",
    ".gitignore",
    ".ini",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
ACTIVE_CONFIG_SUFFIXES = {".cfg", ".env", ".ini", ".json", ".ps1", ".toml", ".xml", ".yaml", ".yml"}
ACTIVE_CONFIG_NAMES = {"profile.template.json", "profile.local.json", "network.cfg", "gatewaysetting.xml"}

SECRET_KEYS = (
    "password",
    "passwd",
    "pwd",
    "secret",
    "token",
    "api_key",
    "apikey",
    "access_key",
    "private_key",
    "credential",
    "credentials",
    "connection_string",
    "connectionstring",
)
SECRET_KEY_RE = "|".join(re.escape(key) for key in SECRET_KEYS)
SECRET_ASSIGNMENT_RE = re.compile(
    rf"""(?ix)
    (?:^|[\s,{{;])
    ["']?\$?(?P<key>{SECRET_KEY_RE})["']?
    \s*[:=]\s*
    (?P<value>[^,#;\r\n]+)
    """
)
XML_ELEMENT_SECRET_RE = re.compile(
    rf"(?is)<(?P<key>{SECRET_KEY_RE})\b[^>]*>(?P<value>.*?)</(?P=key)>"
)
XML_ATTR_SECRET_RE = re.compile(
    rf"""(?ix)\b(?P<key>{SECRET_KEY_RE})\b\s*=\s*["'](?P<value>[^"']*)["']"""
)
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
URL_RE = re.compile(r"\bhttps?://(?P<host>[A-Za-z0-9_.-]+)(?::\d+)?(?:/[^\s'\"<>]*)?", re.IGNORECASE)
UNC_RE = re.compile(r"\\\\[A-Za-z0-9_.-]+\\")
ENDPOINT_ASSIGNMENT_RE = re.compile(
    r"""(?ix)
    (?:^|[\s,{;])
    ["']?(host|hostname|endpoint|server|url|address)["']?
    \s*[:=]\s*
    (?P<value>[^,#;\r\n]+)
    """
)
SRC_TOKEN_RE = re.compile(r"\bSRC-[A-Z0-9-]+\b")
NUMERIC_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
ALLOWED_ENDIAN = {"big", "little", "n/a", "none", "not_applicable", ""}
OPEN_VALUES = {"open"}
APPROVED_VALUES = {"approved", "accepted", "resolved", "closed"}
PLACEHOLDER_VALUES = {
    "",
    "null",
    "none",
    "tbd",
    "redacted",
    "changeme",
    "placeholder",
    "<set-by-environment>",
}

ACCEPTANCE_HARDENING_ITEMS = [
    "external artifact root",
    "worktree forbidden artifact scan",
    "tracked artifact scan",
    "credential detection",
    "non-loopback endpoint detection",
    "Git backup remote restriction",
    "protocol offset validation",
    "ACK pair validation",
    "source-reference integrity",
    "validator regression tests",
    "PowerShell entrypoint",
    "M1 readiness gate",
    "nested repo disposition",
    "source baseline completeness",
]

README_REQUIRED_LINKS = [
    "docs/DEVELOPMENT_PLAN.md",
    "STATUS.md",
    "docs/M1_READINESS.md",
    "ACCEPTANCE_TRACE.md",
    "docs/RUNBOOK.md",
]
DOCUMENT_AUTHORITY_SOURCES = [
    "README.md",
    "docs/SCOPE.md",
    "docs/DEVELOPMENT_PLAN.md",
    "STATUS.md",
    "docs/M1_READINESS.md",
    "scripts/m1_readiness.py",
    "references/decision_register.csv",
    "references/source_register.csv",
    "ACCEPTANCE_TRACE.md",
    "docs/RUNBOOK.md",
    "docs/ARCHITECTURE.md",
]
PHASE_IDS = ["M0", "M1", "M2", "M3", "M4", "M5", "M6"]
FORBIDDEN_LIVE_RESULT_PATTERNS = [
    "QUALITY_GATE_PASS",
    "QUALITY_GATE_FAIL",
    "M1_READINESS_READY",
    "M1_READINESS_BLOCKED",
    "Current blockers:",
    "Blocker count:",
    "Quality Gate: PASS",
    "Quality Gate: FAIL",
]
AGENTS_BUILD_STAGE_MARKERS = [
    "Build-Stage Borrowed Practices",
    "Task contract",
    "Change class",
    "NOT RUN",
    "Closeout Receipt",
    "Later borrowing",
]
TEST_POLICY_VERIFICATION_MARKERS = [
    "Verification Hygiene",
    "NOT RUN",
    "Do not imply success",
    "Negative tests",
]
RUNBOOK_CLOSEOUT_MARKERS = [
    "Closeout Receipt",
    "commands run",
    "commands not run",
    "required owner actions",
]
DEVELOPMENT_PLAN_BUILD_STAGE_MARKERS = [
    "Build-Stage Governance Imports",
    "task contract discipline",
    "change class discipline",
    "verification hygiene",
    "closeout receipt discipline",
]
APPROVED_BACKUP_REMOTES = {
    "origin": {"https://github.com/esj1123/LOXFS_CMD_SIG.git"},
}


@dataclass(frozen=True)
class Issue:
    category: str
    level: str
    message: str


def add_issue(issues: list[Issue], category: str, level: str, message: str) -> None:
    issues.append(Issue(category=category, level=level, message=message))


def normalize_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def git_run(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-c", f"safe.directory={root.as_posix()}", *args],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_lines(root: Path, args: list[str], issues: list[Issue], label: str) -> list[str]:
    try:
        result = git_run(root, args)
    except FileNotFoundError:
        add_issue(issues, "git", "ERROR", f"git unavailable for {label}")
        return []
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()[0] if result.stderr.strip() else "unknown git error"
        add_issue(issues, "git", "ERROR", f"git {label} failed: {detail}")
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def get_tracked_files(root: Path, issues: list[Issue]) -> list[Path]:
    return [root / line for line in git_lines(root, ["ls-files"], issues, "ls-files")]


def get_untracked_source_candidates(root: Path, issues: list[Issue]) -> list[Path]:
    return [
        root / line
        for line in git_lines(root, ["ls-files", "--others", "--exclude-standard"], issues, "ls-files --others")
    ]


def iter_worktree_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        rel_parts = path.relative_to(root).parts
        lowered = {part.lower() for part in rel_parts}
        if lowered & WORKTREE_EXCLUDED_DIRS:
            continue
        files.append(path)
    return files


def path_has_prefix(rel: str, prefixes: list[str]) -> bool:
    rel_lower = rel.lower()
    return any(rel_lower == prefix.rstrip("/") or rel_lower.startswith(prefix) for prefix in prefixes)


def is_forbidden_artifact(path: Path, root: Path) -> bool:
    rel = normalize_rel(path, root)
    rel_lower = rel.lower()
    name_lower = path.name.lower()
    if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
        return True
    if name_lower in FORBIDDEN_EXACT_NAMES:
        return True
    if name_lower.endswith(".pyc") or "__pycache__/" in rel_lower:
        return True
    if path_has_prefix(rel, ["local/", "runs/", "runtime/", "artifacts/", "config/local/", "testresults/", "bin/", "obj/"]):
        return True
    return False


def is_text_file(path: Path) -> bool:
    suffix = ".gitignore" if path.name == ".gitignore" else path.suffix.lower()
    return suffix in TEXT_SUFFIXES


def is_active_config(path: Path) -> bool:
    name = path.name.lower()
    suffix = path.suffix.lower()
    rel = path.as_posix().lower()
    if name in ACTIVE_CONFIG_NAMES:
        return True
    if suffix not in ACTIVE_CONFIG_SUFFIXES:
        return False
    if rel.startswith("docs/") or rel.startswith("references/") or rel.startswith("specs/"):
        return False
    if ".template." in name and name != "profile.template.json":
        return False
    return True


def clean_scalar(value: str) -> str:
    cleaned = value.strip().strip(",").strip()
    if cleaned.lower() in {"true", "false"}:
        return cleaned.lower()
    if (cleaned.startswith('"') and '"' in cleaned[1:]) or (cleaned.startswith("'") and "'" in cleaned[1:]):
        quote = cleaned[0]
        cleaned = cleaned[1:].split(quote, 1)[0]
    return cleaned.strip()


def is_placeholder(value: str) -> bool:
    cleaned = clean_scalar(value)
    lowered = cleaned.lower()
    if lowered in PLACEHOLDER_VALUES:
        return True
    if cleaned.startswith("${") and cleaned.endswith("}"):
        return True
    return False


def is_allowed_endpoint_host(host: str) -> bool:
    host = host.strip().strip('"').strip("'").lower()
    if host in {"localhost", "loopback", "::1"}:
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def check_required_paths(root: Path, issues: list[Issue]) -> None:
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            add_issue(issues, "structure", "ERROR", f"missing file: {rel}")
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            add_issue(issues, "structure", "ERROR", f"missing directory: {rel}")


def check_gitignore(root: Path, issues: list[Issue]) -> None:
    path = root / ".gitignore"
    if not path.exists():
        return
    lines = {line.strip() for line in path.read_text(encoding="utf-8", errors="ignore").splitlines()}
    for pattern in REQUIRED_GITIGNORE_PATTERNS:
        if pattern not in lines:
            add_issue(issues, "git", "ERROR", f"required .gitignore pattern missing: {pattern}")


def remote_line_parts(line: str) -> tuple[str, str, str] | None:
    parts = line.split()
    if len(parts) < 3:
        return None
    return parts[0], parts[1], parts[2].strip("()")


def check_git_remotes(root: Path, issues: list[Issue]) -> None:
    remote_lines = git_lines(root, ["remote", "-v"], issues, "remote -v")
    if not remote_lines:
        return

    approved_seen: set[str] = set()
    for line in remote_lines:
        parsed = remote_line_parts(line)
        if parsed is None:
            add_issue(issues, "git", "ERROR", "unparseable Git remote entry")
            continue
        name, url, action = parsed
        approved_urls = APPROVED_BACKUP_REMOTES.get(name)
        if approved_urls is None or url not in approved_urls:
            add_issue(issues, "git", "ERROR", f"unapproved Git remote configured: {name} ({action})")
            continue
        approved_seen.add(name)

    if approved_seen:
        add_issue(issues, "git", "INFO", "approved backup-only Git remote configured")


def check_git_safety(root: Path, issues: list[Issue]) -> None:
    check_git_remotes(root, issues)

    status = git_lines(root, ["status", "--short"], issues, "status --short")
    if status:
        add_issue(issues, "git", "INFO", f"working tree has {len(status)} staged or unstaged entries")

    try:
        detached = git_run(root, ["symbolic-ref", "--quiet", "--short", "HEAD"])
        if detached.returncode != 0:
            add_issue(issues, "git", "WARNING", "detached HEAD or unnamed branch")
    except FileNotFoundError:
        add_issue(issues, "git", "ERROR", "git unavailable for symbolic-ref")

    for parent in root.resolve().parents:
        if (parent / ".git").exists():
            add_issue(issues, "git", "WARNING", "parent Git repository detected")
            break


def check_forbidden_tracked_files(root: Path, tracked_files: list[Path], issues: list[Issue]) -> None:
    for path in tracked_files:
        rel = normalize_rel(path, root)
        rel_lower = rel.lower()
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            add_issue(issues, "forbidden", "ERROR", f"forbidden tracked extension: {rel}")
        if path.name.lower() in FORBIDDEN_EXACT_NAMES:
            add_issue(issues, "forbidden", "ERROR", f"forbidden tracked name: {rel}")
        if path_has_prefix(rel_lower, FORBIDDEN_PATH_PREFIXES):
            add_issue(issues, "forbidden", "ERROR", f"forbidden tracked path: {rel}")


def check_worktree_storage(root: Path, issues: list[Issue]) -> None:
    for path in iter_worktree_files(root):
        if is_forbidden_artifact(path, root):
            add_issue(issues, "storage", "ERROR", f"repo worktree forbidden artifact: {normalize_rel(path, root)}")


def check_csv_files(root: Path, issues: list[Issue]) -> dict[str, list[dict[str, str]]]:
    parsed: dict[str, list[dict[str, str]]] = {}
    for rel, expected in CSV_HEADERS.items():
        path = root / rel
        if not path.exists():
            continue
        if not path.read_bytes().startswith(BOM):
            add_issue(issues, "schema", "WARNING", f"CSV has no UTF-8 BOM marker: {rel}")
        try:
            headers, rows = read_csv(path)
        except Exception as exc:  # pragma: no cover - exact parser text is platform-specific.
            add_issue(issues, "schema", "ERROR", f"CSV parse failed: {rel}: {exc}")
            continue
        parsed[rel] = rows
        if headers != expected:
            add_issue(issues, "schema", "ERROR", f"CSV header mismatch: {rel}")
        id_column = ID_COLUMNS.get(rel)
        if id_column:
            seen: set[str] = set()
            for line_no, row in enumerate(rows, start=2):
                value = (row.get(id_column) or "").strip()
                if not value:
                    add_issue(issues, "schema", "ERROR", f"blank required ID at {rel}:{line_no}:{id_column}")
                    continue
                if value in seen:
                    add_issue(issues, "schema", "ERROR", f"duplicate ID at {rel}:{line_no}:{id_column}:{value}")
                seen.add(value)
    return parsed


def source_ids(parsed_csv: dict[str, list[dict[str, str]]]) -> set[str]:
    return {row.get("source_id", "").strip() for row in parsed_csv.get("references/source_register.csv", []) if row.get("source_id")}


def source_scope_by_id(parsed_csv: dict[str, list[dict[str, str]]]) -> dict[str, str]:
    return {
        row.get("source_id", "").strip(): (row.get("authority_scope") or "").strip()
        for row in parsed_csv.get("references/source_register.csv", [])
        if row.get("source_id")
    }


def decision_map(parsed_csv: dict[str, list[dict[str, str]]]) -> dict[str, dict[str, str]]:
    return {
        row.get("decision_id", "").strip(): row
        for row in parsed_csv.get("references/decision_register.csv", [])
        if row.get("decision_id")
    }


def check_source_reference_integrity(parsed_csv: dict[str, list[dict[str, str]]], issues: list[Issue]) -> None:
    sources = source_ids(parsed_csv)
    scopes = source_scope_by_id(parsed_csv)
    referenced_sources: set[str] = set()
    if not sources:
        add_issue(issues, "reference", "ERROR", "source_register has no source IDs")
        return

    for line_no, row in enumerate(parsed_csv.get("references/artifact_manifest.csv", []), start=2):
        source_id = (row.get("source_id") or "").strip()
        if source_id:
            referenced_sources.add(source_id)
        if source_id and source_id not in sources:
            add_issue(issues, "reference", "ERROR", f"artifact_manifest orphan source_id at line {line_no}: {source_id}")

    for line_no, row in enumerate(parsed_csv.get("references/decision_register.csv", []), start=2):
        for token in SRC_TOKEN_RE.findall(row.get("source_basis", "")):
            referenced_sources.add(token)
            if token not in sources:
                add_issue(issues, "reference", "ERROR", f"decision_register orphan source_basis at line {line_no}: {token}")

    for rel, rows in parsed_csv.items():
        if rel in {"references/source_register.csv", "references/artifact_manifest.csv", "references/decision_register.csv"}:
            continue
        if "source_ref" not in CSV_HEADERS.get(rel, []):
            continue
        for line_no, row in enumerate(rows, start=2):
            for token in SRC_TOKEN_RE.findall(row.get("source_ref", "")):
                referenced_sources.add(token)
                if token not in sources:
                    add_issue(issues, "reference", "ERROR", f"{rel} orphan source_ref at line {line_no}: {token}")
                else:
                    check_authority_scope(rel, line_no, token, scopes.get(token, ""), issues)

    for source_id in sorted(sources - referenced_sources):
        add_issue(issues, "reference", "WARNING", f"source_register source not referenced by current manifests or tables: {source_id}")


def allowed_scopes_for_rel(rel: str) -> set[str] | None:
    if rel.startswith("specs/common/protocol/"):
        return {"common"}
    if rel.startswith("specs/baselines/k117-loxfs/"):
        return {"K117 baseline", "common"}
    if rel.startswith("specs/targets/n3g-preliminary/"):
        return {"N3G target", "common"}
    if rel.startswith("specs/targets/n3f-interface/"):
        return {"N3F target", "common"}
    return None


def check_authority_scope(rel: str, line_no: int, source_id: str, authority_scope: str, issues: list[Issue]) -> None:
    allowed = allowed_scopes_for_rel(rel)
    if allowed is None:
        return
    if authority_scope not in allowed:
        add_issue(
            issues,
            "reference",
            "ERROR",
            f"{rel}:{line_no}:authority_scope conflict for {source_id}: {authority_scope or 'blank'}",
        )


def check_review_literals(parsed_csv: dict[str, list[dict[str, str]]], issues: list[Issue]) -> None:
    allowed_review = {"not_collected", "candidate", "required", "reviewed", "approved", "rejected", "open", "tbd", ""}
    allowed_status = {"open", "candidate", "approved", "accepted", "resolved", "closed", "tbd", ""}
    for rel, rows in parsed_csv.items():
        for line_no, row in enumerate(rows, start=2):
            for column in ("review_state", "owner_review", "source_status"):
                if column in row and (row.get(column) or "").strip().lower() not in allowed_review:
                    add_issue(issues, "schema", "ERROR", f"invalid {column} literal at {rel}:{line_no}")
            if "status" in row and (row.get("status") or "").strip().lower() not in allowed_status:
                add_issue(issues, "schema", "ERROR", f"invalid status literal at {rel}:{line_no}")


def parse_non_negative_int(value: str, rel: str, line_no: int, column: str, issues: list[Issue]) -> int | None:
    try:
        parsed = int(value)
    except ValueError:
        add_issue(issues, "protocol", "ERROR", f"{rel}:{line_no}:{column} is not an integer")
        return None
    if parsed < 0:
        add_issue(issues, "protocol", "ERROR", f"{rel}:{line_no}:{column} is negative")
        return None
    return parsed


def check_field_layout(
    rel: str,
    rows: list[dict[str, str]],
    expected_total: int,
    issues: list[Issue],
) -> None:
    if not rows:
        add_issue(issues, "protocol", "ERROR", f"{rel} has no field rows")
        return

    orders: set[int] = set()
    spans: list[tuple[int, int, int]] = []
    for line_no, row in enumerate(rows, start=2):
        order = parse_non_negative_int(row.get("field_order", ""), rel, line_no, "field_order", issues)
        offset = parse_non_negative_int(row.get("offset_bytes", ""), rel, line_no, "offset_bytes", issues)
        length = parse_non_negative_int(row.get("length_bytes", ""), rel, line_no, "length_bytes", issues)
        endian = (row.get("endian") or "").strip().lower()
        if endian not in ALLOWED_ENDIAN:
            add_issue(issues, "protocol", "ERROR", f"{rel}:{line_no}:endian invalid")
        if order is not None:
            if order in orders:
                add_issue(issues, "protocol", "ERROR", f"{rel}:{line_no}:field_order duplicate")
            orders.add(order)
        if offset is not None and length is not None:
            if length <= 0:
                add_issue(issues, "protocol", "ERROR", f"{rel}:{line_no}:length_bytes must be positive")
            spans.append((offset, offset + length, line_no))

    expected_offset = 0
    for start, end, line_no in sorted(spans):
        if start < expected_offset:
            add_issue(issues, "protocol", "ERROR", f"{rel}:{line_no}:field overlap")
        elif start > expected_offset:
            add_issue(issues, "protocol", "ERROR", f"{rel}:{line_no}:field gap")
        expected_offset = max(expected_offset, end)
    if expected_offset != expected_total:
        add_issue(issues, "protocol", "ERROR", f"{rel} total length {expected_offset} != {expected_total}")


def check_ack_pairs(
    rel: str,
    rows: list[dict[str, str]],
    key_column: str,
    name_column: str,
    ack_column: str,
    issues: list[Issue],
) -> None:
    by_value = {(row.get(key_column) or "").strip(): row for row in rows if (row.get(key_column) or "").strip()}
    if len(by_value) != len([row for row in rows if (row.get(key_column) or "").strip()]):
        add_issue(issues, "protocol", "ERROR", f"{rel}:{key_column} duplicate")

    referenced_ack: dict[str, str] = {}
    for line_no, row in enumerate(rows, start=2):
        value = (row.get(key_column) or "").strip()
        name = (row.get(name_column) or "").strip().upper()
        direction = (row.get("direction") or "").strip().lower()
        ack_value = (row.get(ack_column) or "").strip()
        is_ack = name.endswith("_ACK") or direction.startswith("ack")

        if is_ack and ack_value:
            add_issue(issues, "protocol", "ERROR", f"{rel}:{line_no}:ACK row must not define {ack_column}")
        if not is_ack:
            if not ack_value:
                add_issue(issues, "protocol", "ERROR", f"{rel}:{line_no}:missing ACK pair")
                continue
            if ack_value == value:
                add_issue(issues, "protocol", "ERROR", f"{rel}:{line_no}:self ACK reference")
            ack_row = by_value.get(ack_value)
            if not ack_row:
                add_issue(issues, "protocol", "ERROR", f"{rel}:{line_no}:ACK target missing")
                continue
            ack_name = (ack_row.get(name_column) or "").strip().upper()
            ack_direction = (ack_row.get("direction") or "").strip().lower()
            if not (ack_name.endswith("_ACK") or ack_direction.startswith("ack")):
                add_issue(issues, "protocol", "ERROR", f"{rel}:{line_no}:ACK target is not ACK row")
            if ack_value in referenced_ack:
                add_issue(issues, "protocol", "ERROR", f"{rel}:{line_no}:ACK target referenced more than once")
            referenced_ack[ack_value] = value

    for value, row in by_value.items():
        name = (row.get(name_column) or "").strip().upper()
        direction = (row.get("direction") or "").strip().lower()
        if name.endswith("_ACK") or direction.startswith("ack"):
            if value not in referenced_ack:
                add_issue(issues, "protocol", "ERROR", f"{rel}:ACK row not paired: {value}")


def check_ack_retry_rules(parsed_csv: dict[str, list[dict[str, str]]], issues: list[Issue]) -> None:
    rows = parsed_csv.get("specs/common/protocol/ack_retry_rules.csv", [])
    seen: set[str] = set()
    for line_no, row in enumerate(rows, start=2):
        rule_id = (row.get("rule_id") or "").strip()
        if rule_id in seen:
            add_issue(issues, "protocol", "ERROR", f"ack_retry_rules duplicate rule_id at line {line_no}: {rule_id}")
        seen.add(rule_id)
        if (row.get("status") or "").strip().lower() in OPEN_VALUES:
            value = (row.get("parameter_value") or "").strip()
            if value and NUMERIC_RE.match(value):
                add_issue(issues, "protocol", "ERROR", f"Open retry parameter has authoritative numeric value at line {line_no}")

    decisions = decision_map(parsed_csv)
    retry_decision = decisions.get("DEC-RETRY-001")
    if not retry_decision:
        add_issue(issues, "reference", "ERROR", "DEC-RETRY-001 missing")
    elif (retry_decision.get("status") or "").strip().lower() not in OPEN_VALUES | APPROVED_VALUES:
        add_issue(issues, "reference", "ERROR", "DEC-RETRY-001 has invalid status")


def check_protocol_tables(parsed_csv: dict[str, list[dict[str, str]]], issues: list[Issue]) -> None:
    check_field_layout("specs/common/protocol/header_fields.csv", parsed_csv.get("specs/common/protocol/header_fields.csv", []), 48, issues)
    check_field_layout("specs/common/protocol/data_block_fields.csv", parsed_csv.get("specs/common/protocol/data_block_fields.csv", []), 10, issues)
    check_ack_pairs(
        "specs/common/protocol/packet_types.csv",
        parsed_csv.get("specs/common/protocol/packet_types.csv", []),
        "type_value",
        "type_name",
        "ack_type_value",
        issues,
    )
    check_ack_pairs(
        "specs/common/protocol/session_controls.csv",
        parsed_csv.get("specs/common/protocol/session_controls.csv", []),
        "detail_value",
        "detail_name",
        "ack_detail_value",
        issues,
    )
    check_ack_retry_rules(parsed_csv, issues)


def check_profile(root: Path, issues: list[Issue]) -> None:
    rel = "profiles/local-laptop/profile.template.json"
    path = root / rel
    if not path.exists():
        return
    try:
        profile = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        add_issue(issues, "schema", "ERROR", f"JSON parse failed: {rel}: {exc}")
        return
    if not isinstance(profile, dict):
        add_issue(issues, "safety", "ERROR", f"{rel} is not a JSON object")
        return

    seen_channels: set[str] = set()
    seen_ports: set[int] = set()
    for index, channel in enumerate(profile.get("channels", []), start=1):
        if not isinstance(channel, dict):
            add_issue(issues, "safety", "ERROR", f"{rel}:channel {index} is not an object")
            continue
        channel_id = str(channel.get("channel_id", ""))
        if channel_id in seen_channels:
            add_issue(issues, "safety", "ERROR", f"{rel}:channel_id duplicate")
        seen_channels.add(channel_id)
        bind_address = str(channel.get("bind_address", ""))
        if bind_address != "127.0.0.1":
            add_issue(issues, "network", "ERROR", f"{rel}:non-loopback bind address")
        port = channel.get("port")
        if not isinstance(port, int):
            add_issue(issues, "network", "ERROR", f"{rel}:port is not integer")
        else:
            if port in seen_ports:
                add_issue(issues, "network", "ERROR", f"{rel}:port duplicate")
            seen_ports.add(port)

    for key in [
        "allow_physical_controller",
        "allow_non_loopback",
        "allow_legacy_binary_execution",
        "allow_netarrays_force",
        "allow_actual_configuration",
    ]:
        if profile.get(key) is not False:
            add_issue(issues, "safety", "ERROR", f"{rel}:{key} is not false")


def check_secret_patterns(root: Path, source_files: list[Path], issues: list[Issue]) -> None:
    for path in source_files:
        if not path.exists() or not is_text_file(path):
            continue
        rel = normalize_rel(path, root)
        try:
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
        except OSError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for match in SECRET_ASSIGNMENT_RE.finditer(line):
                key = match.group("key")
                value = match.group("value")
                if not is_placeholder(value):
                    add_issue(issues, "secret", "ERROR", f"credential candidate: {rel}:{line_no}:{key}")
            for match in XML_ATTR_SECRET_RE.finditer(line):
                key = match.group("key")
                value = match.group("value")
                if not is_placeholder(value):
                    add_issue(issues, "secret", "ERROR", f"credential candidate: {rel}:{line_no}:{key}")
            for match in XML_ELEMENT_SECRET_RE.finditer(line):
                key = match.group("key")
                value = match.group("value")
                if not is_placeholder(value):
                    add_issue(issues, "secret", "ERROR", f"credential candidate: {rel}:{line_no}:{key}")


def check_network_patterns(root: Path, source_files: list[Path], issues: list[Issue]) -> None:
    for path in source_files:
        if not path.exists() or not is_text_file(path) or not is_active_config(Path(normalize_rel(path, root))):
            continue
        rel = normalize_rel(path, root)
        try:
            lines = path.read_text(encoding="utf-8-sig", errors="ignore").splitlines()
        except OSError:
            continue
        for line_no, line in enumerate(lines, start=1):
            for match in IPV4_RE.finditer(line):
                value = match.group(0)
                try:
                    ip = ipaddress.ip_address(value)
                except ValueError:
                    continue
                if not ip.is_loopback:
                    add_issue(issues, "network", "ERROR", f"non-loopback IPv4 endpoint: {rel}:{line_no}")
            if "::1" not in line and re.search(r"\b[0-9a-fA-F:]{3,}:[0-9a-fA-F:]{2,}\b", line):
                add_issue(issues, "network", "ERROR", f"IPv6 literal endpoint: {rel}:{line_no}")
            if UNC_RE.search(line):
                add_issue(issues, "network", "ERROR", f"UNC network path: {rel}:{line_no}")
            for match in URL_RE.finditer(line):
                if not is_allowed_endpoint_host(match.group("host")):
                    add_issue(issues, "network", "ERROR", f"http endpoint in active config: {rel}:{line_no}")
            endpoint_match = ENDPOINT_ASSIGNMENT_RE.search(line)
            if endpoint_match:
                value = clean_scalar(endpoint_match.group("value"))
                if value and not is_placeholder(value) and not is_allowed_endpoint_host(value):
                    add_issue(issues, "network", "ERROR", f"hostname endpoint in active config: {rel}:{line_no}")


def check_acceptance_trace(root: Path, issues: list[Issue]) -> None:
    path = root / "ACCEPTANCE_TRACE.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    for item in ACCEPTANCE_HARDENING_ITEMS:
        if item.lower() not in text:
            add_issue(issues, "acceptance", "ERROR", f"acceptance item missing: {item}")


def read_text_if_exists(root: Path, rel: str) -> str:
    path = root / rel
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def check_no_roadmap_doc(root: Path, issues: list[Issue]) -> None:
    if (root / "docs" / "ROADMAP.md").exists():
        add_issue(issues, "document", "ERROR", "docs/ROADMAP.md must not be created for this repository")


def check_readme_authority(root: Path, issues: list[Issue]) -> None:
    rel = "README.md"
    text = read_text_if_exists(root, rel)
    if not text:
        return
    for link in README_REQUIRED_LINKS:
        if link not in text:
            add_issue(issues, "document", "ERROR", f"README missing required canonical link: {link}")
    if "## Project Path" not in text:
        add_issue(issues, "document", "ERROR", "README missing Project Path section")
    if "## Document Authority" not in text:
        add_issue(issues, "document", "ERROR", "README missing Document Authority section")
    for source in DOCUMENT_AUTHORITY_SOURCES:
        if source not in text:
            add_issue(issues, "document", "ERROR", f"README Document Authority missing canonical source: {source}")
    for phase_id in PHASE_IDS:
        if phase_id not in text:
            add_issue(issues, "document", "ERROR", f"README Project Path missing phase ID: {phase_id}")
    check_no_live_result_patterns(rel, text, issues)


def phase_heading_matches(text: str) -> list[re.Match[str]]:
    return list(re.finditer(r"(?m)^## (M[0-6]): .+$", text))


def check_development_plan_authority(root: Path, issues: list[Issue]) -> None:
    rel = "docs/DEVELOPMENT_PLAN.md"
    text = read_text_if_exists(root, rel)
    if not text:
        return
    if "canonical delivery roadmap" not in text:
        add_issue(issues, "document", "ERROR", "DEVELOPMENT_PLAN missing canonical roadmap role")
    for marker in ["It owns:", "It does not own:", "Canonical references:"]:
        if marker not in text:
            add_issue(issues, "document", "ERROR", f"DEVELOPMENT_PLAN missing Document Role marker: {marker}")
    for source in ["../STATUS.md", "M1_READINESS.md", "../references/decision_register.csv", "../references/source_register.csv", "../ACCEPTANCE_TRACE.md", "RUNBOOK.md", "ARCHITECTURE.md"]:
        if source not in text:
            add_issue(issues, "document", "ERROR", f"DEVELOPMENT_PLAN missing canonical reference: {source}")

    matches = phase_heading_matches(text)
    found = [match.group(1) for match in matches]
    for phase_id in PHASE_IDS:
        count = found.count(phase_id)
        if count == 0:
            add_issue(issues, "document", "ERROR", f"DEVELOPMENT_PLAN missing phase heading: {phase_id}")
        elif count > 1:
            add_issue(issues, "document", "ERROR", f"DEVELOPMENT_PLAN duplicate phase heading: {phase_id}")
    unexpected = [phase_id for phase_id in found if phase_id not in PHASE_IDS]
    for phase_id in unexpected:
        add_issue(issues, "document", "ERROR", f"DEVELOPMENT_PLAN unexpected phase heading: {phase_id}")

    for index, match in enumerate(matches):
        phase_text_start = match.end()
        phase_text_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[phase_text_start:phase_text_end]
        for marker in ["Entry:", "Work:", "Exit criteria:"]:
            if marker not in section:
                add_issue(issues, "document", "ERROR", f"DEVELOPMENT_PLAN {match.group(1)} missing {marker}")
    check_no_live_result_patterns(rel, text, issues)


def check_agents_authority(root: Path, issues: list[Issue]) -> None:
    rel = "AGENTS.md"
    text = read_text_if_exists(root, rel)
    if not text:
        return
    required = [
        "Document Authority and Conflict Resolution",
        "docs/DEVELOPMENT_PLAN.md",
        "Current phase and blockers follow",
        "scripts/m1_readiness.py",
        "references/decision_register.csv",
        "references/source_register.csv",
        "ACCEPTANCE_TRACE.md",
        "docs/RUNBOOK.md",
        "canonical source",
        "drift",
        "docs/ROADMAP.md",
    ]
    for marker in required:
        if marker not in text:
            add_issue(issues, "document", "ERROR", f"AGENTS missing conflict resolution marker: {marker}")
    for marker in AGENTS_BUILD_STAGE_MARKERS:
        if marker not in text:
            add_issue(issues, "document", "ERROR", f"AGENTS missing build-stage governance marker: {marker}")


def check_test_policy_governance(root: Path, issues: list[Issue]) -> None:
    rel = "docs/TEST_POLICY.md"
    text = read_text_if_exists(root, rel)
    if not text:
        return
    for marker in TEST_POLICY_VERIFICATION_MARKERS:
        if marker not in text:
            add_issue(issues, "document", "ERROR", f"TEST_POLICY missing verification hygiene marker: {marker}")


def check_runbook_closeout(root: Path, issues: list[Issue]) -> None:
    rel = "docs/RUNBOOK.md"
    text = read_text_if_exists(root, rel)
    if not text:
        return
    for marker in RUNBOOK_CLOSEOUT_MARKERS:
        if marker not in text:
            add_issue(issues, "document", "ERROR", f"RUNBOOK missing closeout receipt marker: {marker}")


def check_development_plan_build_stage_governance(root: Path, issues: list[Issue]) -> None:
    rel = "docs/DEVELOPMENT_PLAN.md"
    text = read_text_if_exists(root, rel)
    if not text:
        return
    for marker in DEVELOPMENT_PLAN_BUILD_STAGE_MARKERS:
        if marker not in text:
            add_issue(issues, "document", "ERROR", f"DEVELOPMENT_PLAN missing build-stage governance marker: {marker}")


def check_no_live_result_patterns(rel: str, text: str, issues: list[Issue]) -> None:
    for pattern in FORBIDDEN_LIVE_RESULT_PATTERNS:
        if pattern in text:
            add_issue(issues, "document", "ERROR", f"{rel} contains fixed live-result pattern: {pattern}")


def check_document_authority(root: Path, issues: list[Issue]) -> None:
    check_no_roadmap_doc(root, issues)
    check_readme_authority(root, issues)
    check_development_plan_authority(root, issues)
    check_agents_authority(root, issues)
    check_test_policy_governance(root, issues)
    check_runbook_closeout(root, issues)
    check_development_plan_build_stage_governance(root, issues)


def run_checks(root: Path | str) -> list[Issue]:
    root = Path(root).resolve()
    issues: list[Issue] = []
    check_required_paths(root, issues)
    tracked_files = get_tracked_files(root, issues)
    untracked_source_files = get_untracked_source_candidates(root, issues)
    source_candidate_files = sorted({*tracked_files, *untracked_source_files})
    check_git_safety(root, issues)
    check_gitignore(root, issues)
    check_forbidden_tracked_files(root, tracked_files, issues)
    check_worktree_storage(root, issues)
    parsed_csv = check_csv_files(root, issues)
    check_review_literals(parsed_csv, issues)
    check_source_reference_integrity(parsed_csv, issues)
    check_protocol_tables(parsed_csv, issues)
    check_profile(root, issues)
    check_secret_patterns(root, source_candidate_files, issues)
    check_network_patterns(root, source_candidate_files, issues)
    check_acceptance_trace(root, issues)
    check_document_authority(root, issues)
    return issues


def grouped_counts(issues: list[Issue]) -> dict[str, int]:
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    for issue in issues:
        counts[issue.level] = counts.get(issue.level, 0) + 1
    return counts


def print_report(issues: list[Issue]) -> int:
    counts = grouped_counts(issues)
    if counts["ERROR"]:
        print("VALIDATION_FAIL")
    else:
        print("VALIDATION_PASS")
    for level in ("ERROR", "WARNING", "INFO"):
        for issue in issues:
            if issue.level == level:
                print(f"{level} [{issue.category}] {issue.message}")
    print(f"summary: errors={counts['ERROR']} warnings={counts['WARNING']} info={counts['INFO']}")
    return 1 if counts["ERROR"] else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Phase 0 repository.")
    parser.add_argument("--root", default=".", help="Repository root. Default: current directory.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return print_report(run_checks(args.root))


if __name__ == "__main__":
    raise SystemExit(main())
