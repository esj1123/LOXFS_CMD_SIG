#!/usr/bin/env python3
"""Create the external local-only workspace directory skeleton.

Default mode is dry-run. Use --apply to create directories.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


ENV_LOCAL_ROOT = "LOXFS_CMD_SIG_LOCAL_ROOT"
LOCAL_DIRS = [
    "artifacts/documents",
    "artifacts/legacy_rsid",
    "artifacts/netarrays",
    "artifacts/configurations",
    "artifacts/reference_logs",
    "runtime/harness",
    "runtime/legacy_rsid",
    "runtime/netarrays",
    "runs",
    "config",
]
SYNC_ROOT_MARKERS = {
    "onedrive",
    "google drive",
    "googledrive",
    "dropbox",
    "icloud drive",
    "iclouddrive",
    "내 드라이브",
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap external local-only workspace directories.")
    parser.add_argument("--root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--local-root", help=f"External local root. Defaults to {ENV_LOCAL_ROOT}.")
    parser.add_argument("--apply", action="store_true", help="Create directories. Default is dry-run.")
    return parser.parse_args(argv)


def resolve_local_root(value: str | None) -> Path | None:
    selected = value or os.environ.get(ENV_LOCAL_ROOT)
    if not selected:
        return None
    return Path(selected).expanduser().resolve()


def is_known_sync_root(path: Path) -> bool:
    parts = {part.lower() for part in path.resolve().parts}
    return any(marker in parts for marker in SYNC_ROOT_MARKERS)


def validate_local_root(repo_root: Path, local_root: Path) -> list[str]:
    errors: list[str] = []
    if local_root == repo_root or repo_root in local_root.parents:
        errors.append("local root resolves inside the source repository")
    if is_known_sync_root(local_root):
        errors.append("local root resolves inside a known sync root")
    return errors


def planned_directories(local_root: Path) -> list[Path]:
    return [local_root / rel for rel in LOCAL_DIRS]


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.root).resolve()
    local_root = resolve_local_root(args.local_root)
    print(f"repo_root={repo_root}")
    print(f"mode={'apply' if args.apply else 'dry-run'}")

    if local_root is None:
        print(f"ERROR: provide --local-root or set {ENV_LOCAL_ROOT}")
        return 2

    print(f"local_root={local_root}")
    errors = validate_local_root(repo_root, local_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 2

    created = 0
    existing = 0
    for path in planned_directories(local_root):
        rel = path.relative_to(local_root).as_posix()
        if path.exists():
            existing += 1
            print(f"exists: {rel}")
            continue
        if args.apply:
            path.mkdir(parents=True, exist_ok=True)
            created += 1
            print(f"created: {rel}")
        else:
            print(f"would create: {rel}")

    print(f"summary: created={created} existing={existing} planned={len(LOCAL_DIRS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
