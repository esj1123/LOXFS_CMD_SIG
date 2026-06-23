#!/usr/bin/env python3
"""Inventory external local artifacts without printing semantic contents."""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path

import bootstrap_local_workspace


CSV_HEADER = ["relative_path", "size_bytes", "sha256", "review_state", "notes"]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory files under the external local artifact root.")
    parser.add_argument("--root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--local-root", help="External local root. Defaults to LOXFS_CMD_SIG_LOCAL_ROOT.")
    parser.add_argument("--apply", action="store_true", help="Write CSV only with --output.")
    parser.add_argument("--output", help="Output CSV path. Required with --apply.")
    return parser.parse_args(argv)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(local_root: Path) -> list[dict[str, str]]:
    artifact_root = local_root / "artifacts"
    rows: list[dict[str, str]] = []
    if not artifact_root.exists():
        return rows
    for path in sorted(p for p in artifact_root.rglob("*") if p.is_file()):
        rel = path.relative_to(local_root).as_posix()
        rows.append(
            {
                "relative_path": rel,
                "size_bytes": str(path.stat().st_size),
                "sha256": sha256_file(path),
                "review_state": "candidate",
                "notes": "Content not printed or interpreted by inventory script.",
            }
        )
    return rows


def resolve_output(repo_root: Path, local_root: Path, output: str) -> Path:
    path = Path(output)
    if not path.is_absolute():
        path = local_root / path
    resolved = path.resolve()
    try:
        resolved.relative_to(repo_root)
    except ValueError:
        return resolved
    raise ValueError("output path resolves inside the source repository")


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

    rows = inventory(local_root)
    print(f"local_root={local_root}")
    print(f"files_found={len(rows)}")
    for row in rows:
        print(f"{row['relative_path']},{row['size_bytes']},{row['sha256']}")

    if args.apply:
        if not args.output:
            print("ERROR: --apply requires --output")
            return 2
        try:
            output = resolve_output(repo_root, local_root, args.output)
        except ValueError as exc:
            print(f"ERROR: {exc}")
            return 2
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_HEADER)
            writer.writeheader()
            writer.writerows(rows)
        print(f"wrote: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
