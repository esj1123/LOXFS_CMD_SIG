#!/usr/bin/env python3
"""Plan or apply migration from repo/local to the external local root."""

from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
import sys
from datetime import datetime
from pathlib import Path

import bootstrap_local_workspace


CSV_HEADER = ["relative_path", "source_size_bytes", "source_sha256", "destination_size_bytes", "destination_sha256", "status", "action"]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan migration of repo/local files to the external local root.")
    parser.add_argument("--root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--local-root", help="External local root. Defaults to LOXFS_CMD_SIG_LOCAL_ROOT.")
    parser.add_argument("--apply", action="store_true", help="Copy verified files and remove only matching sources.")
    return parser.parse_args(argv)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*") if not path.is_dir())


def inventory_source(repo_root: Path) -> list[Path]:
    return inventory_files(repo_root / "local")


def inventory_destination(local_root: Path) -> list[Path]:
    return [path for path in inventory_files(local_root) if "runs" not in path.relative_to(local_root).parts[:1]]


def destination_for(repo_root: Path, local_root: Path, source_file: Path) -> Path:
    rel_under_local = source_file.relative_to(repo_root / "local")
    return local_root / rel_under_local


def source_for(repo_root: Path, local_root: Path, destination_file: Path) -> Path:
    rel_under_destination = destination_file.relative_to(local_root)
    return repo_root / "local" / rel_under_destination


def file_metadata(path: Path) -> tuple[str, str] | None:
    try:
        return str(path.stat().st_size), sha256_file(path)
    except OSError:
        return None


def build_plan(repo_root: Path, local_root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    source_files = inventory_source(repo_root)
    destination_files = inventory_destination(local_root)
    planned_sources = set(source_files)

    for source in source_files:
        rel = source.relative_to(repo_root).as_posix()
        source_meta = file_metadata(source)
        if source_meta is None:
            rows.append(
                {
                    "relative_path": rel,
                    "source_size_bytes": "unavailable",
                    "source_sha256": "unavailable",
                    "destination_size_bytes": "",
                    "destination_sha256": "",
                    "status": "source_only",
                    "action": "keep_source",
                }
            )
            continue
        source_size, source_hash = source_meta
        destination = destination_for(repo_root, local_root, source)
        if not destination.exists():
            destination_size = ""
            destination_hash = ""
            status = "planned_copy"
            action = "copy"
        elif destination.is_file():
            destination_meta = file_metadata(destination)
            if destination_meta is None:
                destination_size = "unavailable"
                destination_hash = "unavailable"
                status = "conflict"
                action = "keep_source"
            else:
                destination_size, destination_hash = destination_meta
            if destination_hash == source_hash:
                status = "same_hash"
                action = "remove_source_after_verify"
            elif destination_hash != "unavailable":
                status = "different_hash"
                action = "keep_source"
        else:
            destination_size = ""
            destination_hash = ""
            status = "conflict"
            action = "keep_source"
        rows.append(
            {
                "relative_path": rel,
                "source_size_bytes": source_size,
                "source_sha256": source_hash,
                "destination_size_bytes": destination_size,
                "destination_sha256": destination_hash,
                "status": status,
                "action": action,
            }
        )

    for destination in destination_files:
        source = source_for(repo_root, local_root, destination)
        if source in planned_sources:
            continue
        rel = destination.relative_to(local_root).as_posix()
        destination_meta = file_metadata(destination)
        destination_size, destination_hash = destination_meta or ("unavailable", "unavailable")
        rows.append(
            {
                "relative_path": rel,
                "source_size_bytes": "",
                "source_sha256": "",
                "destination_size_bytes": destination_size,
                "destination_sha256": destination_hash,
                "status": "destination_only",
                "action": "keep_destination",
            }
        )
    return rows


def clean_empty_dirs(source_root: Path) -> None:
    if not source_root.exists():
        return
    for path in sorted((p for p in source_root.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        try:
            path.rmdir()
        except OSError:
            pass


def apply_plan(repo_root: Path, local_root: Path, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    applied: list[dict[str, str]] = []
    for row in rows:
        source = repo_root / row["relative_path"]
        destination = destination_for(repo_root, local_root, source)
        result = dict(row)
        if row["status"] == "planned_copy":
            if destination.exists():
                result["action"] = "destination_appeared_source_kept"
                applied.append(result)
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            if sha256_file(destination) == row["source_sha256"]:
                source.unlink()
                result["action"] = "copied_verified_removed_source"
            else:
                result["action"] = "copy_hash_mismatch_source_kept"
        elif row["status"] == "same_hash":
            source.unlink()
            result["action"] = "verified_removed_source"
        applied.append(result)
    clean_empty_dirs(repo_root / "local")
    return applied


def write_receipt(local_root: Path, rows: list[dict[str, str]]) -> Path:
    runs_dir = local_root / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    receipt = runs_dir / f"migration_receipt_{timestamp}.csv"
    with receipt.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_HEADER)
        writer.writeheader()
        writer.writerows(rows)
    return receipt


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.root).resolve()
    local_root = bootstrap_local_workspace.resolve_local_root(args.local_root)
    print(f"repo_root={repo_root}")
    print(f"mode={'apply' if args.apply else 'dry-run'}")

    if local_root is None:
        print(f"ERROR: provide --local-root or set {bootstrap_local_workspace.ENV_LOCAL_ROOT}")
        return 2
    errors = bootstrap_local_workspace.validate_local_root(repo_root, local_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 2

    rows = build_plan(repo_root, local_root)
    print(f"local_root={local_root}")
    print(f"files_found={len(rows)}")
    for row in rows:
        print(
            ",".join(
                [
                    row["relative_path"],
                    row["source_size_bytes"],
                    row["source_sha256"],
                    row["destination_size_bytes"],
                    row["destination_sha256"],
                    row["status"],
                    row["action"],
                ]
            )
        )

    if not args.apply:
        print("dry_run_only: no files copied or removed")
        return 0

    applied = apply_plan(repo_root, local_root, rows)
    receipt = write_receipt(local_root, applied)
    print(f"receipt={receipt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
