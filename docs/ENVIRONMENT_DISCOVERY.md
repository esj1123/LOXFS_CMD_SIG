# Environment Discovery

Discovery date: 2026-06-18.

## Requested Root

`<RepoWorktree>`

## Preflight Results

| Check | Result |
| --- | --- |
| Current path | `<RepoWorktree>` |
| Initial tree | No subfolders were present before bootstrap. |
| Existing files | A hidden zero-byte Office artifact existed and was preserved. |
| `.git` in requested root before bootstrap | Absent |
| Parent Git repository | `<ParentGitRoot>` was detected by `git rev-parse --show-toplevel` before local init. |
| Existing README.md | Not present before bootstrap. |
| Existing AGENTS.md | Not present before bootstrap. |
| Existing STATUS.md | Not present before bootstrap. |
| Existing .gitignore | Not present before bootstrap. |
| Git status before bootstrap | Parent repository contained unrelated changes outside this workspace; they were not touched. |
| Git action | Local Git repository initialized in the requested root; owner-designated GitHub backup remote configured after approval. |
| git --version | `git version 2.53.0.windows.1` |
| py --version | Failed: no installed Python found on PATH. |
| python --version | Failed: `python.exe` could not be launched from PATH. |
| Bundled local Python | Available as `<BundledPython>` in the Codex runtime; used for verification through `LOXFS_HARNESS_PYTHON`. |
| dotnet --info | .NET SDK `10.0.201`; additional SDK `10.0.109`; host `10.0.9`. |
| PowerShell version | `5.1.26100.8655` |

## Tool Installation

No tools or packages were installed.

## Hardening Preflight Update

Discovery date: 2026-06-19.

| Check | Result |
| --- | --- |
| Current path | `<RepoWorktree>` |
| Git top-level | `<RepoWorktree>` |
| Parent Git repository | Detected by ancestor `.git`; tracked as `DEC-REPO-001`. |
| Plain Git status | Blocked by dubious ownership unless per-command `safe.directory` is supplied. |
| Git remote | `origin` is configured as backup/publication only and is not part of harness runtime behavior. |
| Git tracked files | None. |
| Git untracked candidates | Repository source files and hardening files. |
| Forbidden worktree artifacts | 37 hidden Office artifact candidates detected by validator; user files were preserved. |
| `local/` file count and size | 13 files, 0 bytes total in the sandbox view. |
| Migration dry-run | 13 `local/` entries reported as `source_only`; no files copied or removed. |
| Known sync root | None detected in the repository path string. |
| `py --version` | Failed: no installed Python found on PATH. |
| `python --version` | Failed in the current session. |
| Verification Python | Supplied through `LOXFS_HARNESS_PYTHON` at command time. |
| External package install | Not performed. |
