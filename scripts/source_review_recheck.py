#!/usr/bin/env python3
"""Read-only recheck for provisional source review notes.

This tool compares aliases, sizes, and SHA-256 values recorded in
docs/SOURCE_REVIEW_NOTES.md against files under an external local root.
It does not update registers, close decisions, copy files, or print the
external root path.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path


SHA256_RE = re.compile(r"^[0-9A-F]{64}$")
SINGULAR_ALIAS_RE = re.compile(r"^\|\s*Alias\s*\|\s*`([^`]+)`\s*\|")
SINGULAR_SIZE_RE = re.compile(r"^\|\s*Size\s*\|\s*([0-9]+)\s+bytes\s*\|")
SINGULAR_SHA_RE = re.compile(r"^\|\s*SHA-256\s*\|\s*`([0-9A-F]{64})`\s*\|")
METADATA_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([0-9]+)\s*\|\s*`([0-9A-F]{64})`\s*\|")
SECTION_RE = re.compile(r"^###\s+(.+)$")


@dataclass(frozen=True)
class ExpectedArtifact:
    section: str
    alias: str
    size: int
    sha256: str


@dataclass(frozen=True)
class RecheckResult:
    artifact: ExpectedArtifact
    status: str


def is_relative_alias(alias: str) -> bool:
    if not alias or alias.startswith(("/", "\\")):
        return False
    if "\\" in alias:
        return False
    if re.match(r"^[A-Za-z]:", alias):
        return False
    if "://" in alias:
        return False
    return ".." not in alias.split("/")


def parse_expected_artifacts(notes_path: Path) -> list[ExpectedArtifact]:
    text = notes_path.read_text(encoding="utf-8", errors="ignore")
    section = ""
    artifacts: list[ExpectedArtifact] = []
    singular_alias: str | None = None
    singular_size: int | None = None
    singular_sha: str | None = None

    def flush_singular() -> None:
        nonlocal singular_alias, singular_size, singular_sha
        if singular_alias and singular_size is not None and singular_sha:
            artifacts.append(ExpectedArtifact(section, singular_alias, singular_size, singular_sha))
        singular_alias = None
        singular_size = None
        singular_sha = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        section_match = SECTION_RE.match(line)
        if section_match:
            flush_singular()
            section = section_match.group(1).strip()
            continue

        metadata_match = METADATA_ROW_RE.match(line)
        if metadata_match:
            flush_singular()
            alias, size, sha256 = metadata_match.groups()
            artifacts.append(ExpectedArtifact(section, alias, int(size), sha256))
            continue

        alias_match = SINGULAR_ALIAS_RE.match(line)
        if alias_match:
            singular_alias = alias_match.group(1).strip()
            continue

        size_match = SINGULAR_SIZE_RE.match(line)
        if size_match:
            singular_size = int(size_match.group(1))
            continue

        sha_match = SINGULAR_SHA_RE.match(line)
        if sha_match:
            singular_sha = sha_match.group(1).strip()
            continue

    flush_singular()
    return artifacts


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def root_inside_repo(local_root: Path, repo_root: Path) -> bool:
    try:
        local_root.relative_to(repo_root)
        return True
    except ValueError:
        return False


def recheck(notes_path: Path, local_root: Path, repo_root: Path) -> list[RecheckResult]:
    local_root = local_root.resolve()
    repo_root = repo_root.resolve()
    if root_inside_repo(local_root, repo_root):
        raise ValueError("local root must be outside the repository")

    results: list[RecheckResult] = []
    for artifact in parse_expected_artifacts(notes_path):
        if not is_relative_alias(artifact.alias):
            results.append(RecheckResult(artifact, "invalid_alias"))
            continue
        if not SHA256_RE.match(artifact.sha256):
            results.append(RecheckResult(artifact, "invalid_sha256"))
            continue

        path = local_root / artifact.alias
        if not path.exists():
            results.append(RecheckResult(artifact, "missing"))
            continue
        if not path.is_file():
            results.append(RecheckResult(artifact, "not_file"))
            continue

        actual_size = path.stat().st_size
        if actual_size != artifact.size:
            results.append(RecheckResult(artifact, "size_mismatch"))
            continue

        actual_sha = sha256_file(path)
        if actual_sha != artifact.sha256:
            results.append(RecheckResult(artifact, "hash_mismatch"))
            continue

        results.append(RecheckResult(artifact, "matched"))
    return results


def print_blocked(message: str) -> int:
    print("SOURCE_REVIEW_RECHECK_BLOCKED")
    print(f"owner_action: {message}")
    return 1


def print_results(results: list[RecheckResult]) -> int:
    counts: dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1

    failed = [result for result in results if result.status != "matched"]
    print("SOURCE_REVIEW_RECHECK_FAIL" if failed else "SOURCE_REVIEW_RECHECK_PASS")
    for result in results:
        print(f"{result.artifact.alias} | {result.status}")
    print(
        "summary: "
        + " ".join(f"{status}={count}" for status, count in sorted(counts.items()))
        + f" total={len(results)}"
    )
    return 1 if failed else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recheck SOURCE_REVIEW_NOTES.md metadata against external artifacts.")
    parser.add_argument("--root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--notes", default="docs/SOURCE_REVIEW_NOTES.md", help="Review notes path relative to root.")
    parser.add_argument("--local-root", default=None, help="External artifact root. Defaults to LOXFS_CMD_SIG_LOCAL_ROOT.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.root).resolve()
    notes_path = (repo_root / args.notes).resolve()

    local_root_value = args.local_root or os.environ.get("LOXFS_CMD_SIG_LOCAL_ROOT")
    if not local_root_value:
        return print_blocked("Set LOXFS_CMD_SIG_LOCAL_ROOT or pass --local-root for a read-only recheck.")

    local_root = Path(local_root_value)
    if not notes_path.exists():
        return print_blocked("Create docs/SOURCE_REVIEW_NOTES.md before recheck.")
    if not local_root.exists():
        return print_blocked("External local root is not available for read-only recheck.")

    try:
        results = recheck(notes_path, local_root, repo_root)
    except ValueError as exc:
        return print_blocked(str(exc))

    if not results:
        return print_blocked("No source metadata rows were found in review notes.")
    return print_results(results)


if __name__ == "__main__":
    raise SystemExit(main())
