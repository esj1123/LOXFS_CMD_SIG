# M1 Owner Review Packet

Last updated: 2026-06-28

## Document Role

This packet is a review draft for owner decisions before M1 Protocol Core starts.

It does not close decisions, approve sources, update registers, authorize implementation, or replace the readiness gate. After owner review, approved values must be recorded in the canonical files:

- `references/decision_register.csv`
- `references/source_register.csv`
- `STATUS.md`
- `ACCEPTANCE_TRACE.md`

Current gate basis:

| Check | Current result |
| --- | --- |
| `repo.ps1 owner-review` | `OWNER_REVIEW_CLEAR` |
| `repo.ps1 m1-readiness` | `M1_READINESS_READY` |
| M1 Protocol Core status | Not started |

Safety boundary:

- Do not copy actual artifacts into Git.
- Do not record actual absolute paths, operational endpoints, ports, credentials, tag row values, catalog row values, configuration values, packet captures, DB rows, or raw screenshots in this packet.
- Do not execute NetArrays, iFIX, RSID binaries, controllers, simulators, databases, or network probes.
- Do not close Open decisions from this draft.
- Do not start M1 Protocol Core until `scripts/m1_readiness.py` reports `M1_READINESS_READY`.

## Current Review Position

The repository is in Phase 0 hardening closure. The next useful work is not more broad source discovery. The useful work is to separate source material into:

| Bucket | Use now | Use later |
| --- | --- | --- |
| M1 source baseline | Packet structure, catalog scope, timing/configuration source identity | Required before M1 starts |
| M1 protocol decisions | ACK correlation, CRC profile/vector authority, retry/timing treatment, runtime/language boundary | Required to avoid speculative implementation |
| M2+ context | LOXFS/NetArrays tag maps, iFIX screens, logs, alarm/event/historian context, scenario/oracle planning | Defer until Protocol Core and loopback boundary are stable |

The current evidence and owner approvals clear direct M1 readiness blockers. M1 implementation still requires an explicit owner request to start.

## Review Order

Recommended owner review sequence:

1. Confirm M1 boundary: protocol core only, no UDP, no NetArrays execution, no RSID execution, no actual controller or operational network.
2. Resolve repository/storage readiness decisions: `DEC-STORAGE-001` and `DEC-REPO-001`.
3. Select M1 runtime/language stance for `DEC-DEV-001`.
4. Approve or reject the direct M1 source baseline rows: `SRC-PROTO-001`, `SRC-K117-001`, and `SRC-TIME-001`.
5. Review protocol-specific P0 decisions: `DEC-PROTO-002`, `DEC-PROTO-003`, `DEC-RETRY-001`, and `DEC-TIME-001`.
6. Mark LOXFS/NetArrays/iFIX/tag/log material as M2+ supporting material unless the owner explicitly selects exact aliases as M1 supporting evidence.
7. Re-run `repo.ps1 validate`, `repo.ps1 test`, `repo.ps1 quality-gate`, `repo.ps1 owner-review`, and `repo.ps1 m1-readiness`.

## M1 Include / Exclude Boundary

M1 should include only:

- 48-byte header encode/decode.
- 10-byte data block encode/decode.
- Packet type and session-control table handling from owner-reviewed source material.
- Placeholder CRC interfaces only if the CRC profile remains unresolved.
- Synthetic golden vectors that do not contain actual catalog values or operational configuration.
- Unit and contract tests using synthetic fixtures.

M1 should exclude:

- UDP transport.
- NetArrays adapter work.
- iFIX integration.
- RSID binary execution.
- Actual source packages, actual DBN, actual PGM, actual configuration, actual captures, actual logs, and actual tag exports.
- Live endpoint/channel values.
- M2+ scenario/oracle/tag/log behavior.
- Any final acceptance judgment.

## Required Owner Actions

### DEC-DEV-001 - Implementation Runtime and Language

Current state: Approved on 2026-06-28.

Current evidence:

- `docs/ENVIRONMENT_DISCOVERY.md` records local runtime availability.
- Design Description and SAT observations can inform module boundaries but do not choose a language.
- RSID static inspection observations are useful for boundary analysis but do not require M1 to use the same implementation language as legacy tooling.

Approved review stance:

- M1 Protocol Core may use Python standard library for deterministic packet codec, table validation, and synthetic regression tests.
- C#/.NET/C++ remain available for later RSID, NetArrays, iFIX, Windows integration, adapter, or packaging work if separately approved.
- This approval does not authorize UDP transport, NetArrays execution, iFIX integration, RSID execution, or M1 implementation while readiness is still blocked.

Register state:

- `references/decision_register.csv` records `DEC-DEV-001` as `Approved`.

Record after review: `references/decision_register.csv`.

### DEC-STORAGE-001 - External Local Artifact Root

Current state: Approved on 2026-06-28.

Current evidence:

- Storage boundary policy exists.
- Actual artifacts must remain outside the repository.
- Desktop worktree retention is the current working direction, and external artifact storage policy is owner-approved.

Recommended review stance:

- Approve a storage policy/location class, not a sensitive absolute path in Git.
- Keep actual source documents, packages, screenshots, logs, configs, exports, and run outputs outside the repository.
- Keep source-register references as aliases and SHA-256 only.

Register state:

- `references/decision_register.csv` records `DEC-STORAGE-001` as `Approved`.
- The approval covers policy and location class only; actual root paths remain outside Git.

Record after review: `references/decision_register.csv`.

### DEC-REPO-001 - Nested Git Repository Disposition

Current state: Approved on 2026-06-28.

Current evidence:

- Desktop worktree retention is the current working direction.
- Parent Git risk remains recorded.
- The owner-designated GitHub remote is backup/publication only.

Recommended review stance:

- If Desktop retention is intentional, record that nested layout is owner-approved for now.
- Keep remote usage limited to backup/publication; do not treat GitHub as runtime, source authority, artifact store, or validation evidence.
- Do not change parent Git settings automatically.

Register state:

- `references/decision_register.csv` records `DEC-REPO-001` as `Approved`.
- The current Desktop/nested repository topology is accepted for M1.
- GitHub remains backup/publication only.

Record after review: `references/decision_register.csv`.

## Required Source Baseline Review

Each required source must have reviewed metadata before M1:

- revision
- non-absolute path alias
- 64-hex SHA-256
- owner
- `reviewed` or `approved` review state

### SRC-PROTO-001 - Protocol Authority

Current state: approved on 2026-06-28.

Current candidate evidence:

| Candidate alias | Size | SHA-256 | Current interpretation |
| --- | ---: | --- | --- |
| `RSID_DOC/230131_Command Signal Protocol Design VerI.docx` | 70735 | `FBE90FE971B9D208AD353AE0EB6E03FC0DE4020DEB95F760B92F7E31B9AE680D` | Strongest current packet/header/data block/packet type/session candidate. |

Observed M1-relevant evidence:

- Header length candidate: 48 bytes.
- Data block length candidate: 10 bytes.
- Big-endian interpretation candidate.
- Request/ACK packet type pair candidates.
- Session open/close pair candidates.
- ACK and retransmission behavior concepts.
- Header and data block CRC fields.

Still not resolved by this source approval:

- CRC profile.
- Independent CRC test vectors.
- Exact ACK correlation field or field set.
- Retry parameter values.
- Timing authority.

Register state:

- `references/source_register.csv` records `SRC-PROTO-001` with reviewed alias and SHA-256 metadata.
- This approval does not close CRC profile, ACK correlation, retry, or timing decisions.

Record after review: `references/source_register.csv`.

### SRC-K117-001 - K117 Command and Signal Catalog Baseline

Current state: approved on 2026-06-28.

Current candidate evidence:

| Candidate alias | Size | SHA-256 | Current interpretation |
| --- | ---: | --- | --- |
| `K117_BASELINE/K117.00_RSID_AT_submission_composite.pdf` | 7681957 | `6B06EB397D2737C66FFD6EF897CE737D60F4CE71F45CCCA3680B2C4481F33FEC` | Strongest current catalog-scope candidate for pages 14-34 review. |

Observed M1-relevant evidence:

- Scoped review observed 21 tables.
- Scoped review counted 890 table rows and 840 non-empty rows.
- Aperiodic, periodic, internal/signal, command, LOXFS, and network/channel label categories were observed.
- No catalog row values are recorded in Git.

Still not resolved by this source approval:

- Owner-approved catalog revision.
- Whether the scoped pages are sufficient for M1.
- Whether sanitized synthetic catalog fixtures are allowed later.

Register state:

- `references/source_register.csv` records `SRC-K117-001` with reviewed alias and SHA-256 metadata.
- Catalog row values remain external and are not imported into Git.

Record after review: `references/source_register.csv`.

### SRC-NA-001 - NetArrays Baseline Source

Current state: `M2+ deferred` / `not_collected`.

Current candidate evidence:

| Candidate family | Current interpretation |
| --- | --- |
| TEACS/NetArrays metadata candidates from earlier source review | Possible baseline identity source for later tag mapping. |
| `MAINTENANCE_LOXFS_NETARRAYS` review workspace | Strong derivative review evidence for LOXFS/NetArrays behavior, tag mapping, interface classification, flowchart comparison, logic coverage, and shared-variable dependency review. |
| `IFIX` reviewed aliases | Strong later iFIX/SCADA/HMI/tag/log context, not a clean M1 packet authority. |

Recommended review stance:

- Treat `MAINTENANCE_LOXFS_NETARRAYS` as derivative review evidence unless the owner selects exact aliases as supporting source evidence.
- Do not register an entire folder as a source. Select exact aliases only.
- Keep image packs, DBN-like artifacts, binaries, packages, screenshots, and raw extracted values outside Git.
- Do not use this source to infer packet CRC, ACK correlation, retry, timing, or endpoint/channel values.

High-value later-phase aliases already observed:

| Alias | Use |
| --- | --- |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/100_CMD_SIG_Tag_Raw_Evidence.csv` | Tag evidence review. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/104_CMD_SIG_Tag_Coverage_Audit.csv` | CMD/SIG tag coverage audit. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/105_CMD_SIG_Void_Interface_Evidence_Register.csv` | Interface evidence review. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/127_P0_Execution_Comparison_Review_Register.csv` | Execution comparison review. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/138_P0_Logic_Coverage_Matrix.csv` | Logic coverage review. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/139_P0_Shared_Variable_Dependency_Register.csv` | Shared-variable dependency review. |

Owner decision on 2026-06-28:

- Defer `SRC-NA-001` from direct M1 readiness.
- Keep NetArrays, LOXFS, iFIX, DBN, tag-map, and driver evidence as M2+ material unless exact aliases are promoted later.
- Do not register an entire folder.

Record after review: `references/source_register.csv`.

### SRC-TIME-001 - Timing / Configuration Source

Current state: approved on 2026-06-28.

Current candidate evidence:

- GatewaySetting XML family was identified as a timing, retry, endpoint/channel, and runtime configuration source family.
- Runtime configuration files were reviewed only at category level.
- Actual values were not recorded.

Recommended review stance:

- Select the exact timing/configuration source identity without recording actual values in Git.
- Keep actual configuration files outside Git.
- Do not promote observed timing words or default-like values into protocol tables without owner review.

Register state:

- `references/source_register.csv` records `SRC-TIME-001` with alias and SHA-256 metadata.
- The source identity supports M1 readiness only.
- Actual timing, retry, endpoint, channel, and configuration values remain outside Git and defer to M2 behavior review.

Record after review: `references/source_register.csv`.

## Protocol-Specific Decisions For Review After Source Selection

These decisions may not be required by the minimal readiness script, but they are practical blockers for a non-speculative Protocol Core design.

### DEC-PROTO-002 - ACK Correlation Rule

Current state: Open.

Known evidence:

- Packet type ACK pairs were observed.
- Immediate ACK behavior was observed.
- ACK packets are described as header-only.

Unresolved:

- Exact field or fields used to match ACK to the original packet.
- Whether packet type alone is insufficient or acceptable for any synthetic tests.

Recommended review stance:

- Do not implement an ACK manager that assumes correlation by packet type only.
- M1 may define packet type pairs and parse ACK headers, but ACK matching behavior should remain behind an explicit interface until owner review confirms the rule.

Owner question:

| Question | Owner answer needed |
| --- | --- |
| Which field or field set correlates ACK to request? | Source-backed rule |
| Can M1 include only structural ACK parsing until this is confirmed? | Approve/Reject |

Record after review: `references/decision_register.csv`.

### DEC-PROTO-003 - CRC Profile and Test Vectors

Current state: Open.

Known evidence:

- CRC fields exist for data block and header.
- Header CRC excludes the header CRC field itself.
- Data block CRC behavior depends on whether data blocks exist.

Unresolved:

- Polynomial.
- Initial value.
- Final xor.
- Reflection settings.
- Byte range and zeroing rules beyond the observed structural statement.
- Independent CRC test vectors.

Recommended review stance:

- Use placeholder CRC interfaces only until owner-reviewed profile and independent vectors exist.
- Do not choose a common CRC32 variant by assumption.

Owner question:

| Question | Owner answer needed |
| --- | --- |
| What is the exact CRC32 profile? | Source-backed profile |
| What independent test vectors are approved? | Vector alias/hash or source reference |
| Should M1 implement only interfaces until profile review is complete? | Approve/Reject |

Record after review: `references/decision_register.csv`.

### DEC-RETRY-001 - ACK Timeout / Retry / Link-Off

Current state: Open.

Known evidence:

- Missing ACK leads to same-packet retransmission.
- Repeated transmission count behavior was observed.
- Extended ACK absence is treated as link-loss behavior.

Unresolved:

- Timeout value.
- Maximum retry count.
- Link-off threshold.
- Whether parameter values belong in M1 or should defer to M2 timing behavior.

Recommended review stance:

- Do not hard-code timeout or retry values in M1.
- M1 may define data structures and state labels only if values remain placeholders.

Owner question:

| Question | Owner answer needed |
| --- | --- |
| Are retry/link-off parameters required for M1, or deferred? | M1/defer |
| What source supplies approved parameters? | Source alias |
| Can M1 include placeholder/state-only retry structures? | Approve/Reject |

Record after review: `references/decision_register.csv`.

### DEC-TIME-001 - Actual LOXFS Scan Cycle

Current state: Open.

Known evidence:

- Timing category evidence exists.
- Runtime/configuration source families exist.

Unresolved:

- Actual scan cycle authority.
- Whether scan-cycle behavior belongs in M1 or M2.

Recommended review stance:

- Keep actual timing values outside Git.
- Defer runtime timing behavior to M2 unless owner confirms it is required for M1 tests.

Owner question:

| Question | Owner answer needed |
| --- | --- |
| Is actual scan-cycle timing needed for M1 Protocol Core? | Yes/No |
| Which source alias supplies timing authority? | Source alias |
| Can M1 use synthetic time values only? | Approve/Reject |

Record after review: `references/decision_register.csv`.

## M2+ Supporting Material

The following material is valuable but should not drive M1 packet implementation unless the owner explicitly promotes exact aliases as supporting evidence.

| Material | Current role | Recommended phase |
| --- | --- | --- |
| `MAINTENANCE_LOXFS_NETARRAYS` | LOXFS/NetArrays static review workspace for tag, interface, flowchart, logic, shared-variable, and execution-comparison evidence | M2+ scenario/oracle/tag mapping |
| `IFIX` | iFIX/SCADA/HMI screen, event, log, tag, and package context | M4+ SCADA/tag/log context |
| SAT PDF | Procedure and workflow context | Supporting context, not packet authority |
| Design Description PDF | Architecture and module-boundary context | Supporting context for separation decisions |
| IFF preliminary PDFs | N3F/N3G target context | Later target context unless owner promotes |

M2+ material should be used to draft future review packets for:

- `DEC-TAG-001`
- `DEC-LOG-001`
- scenario/oracle boundaries
- NetArrays simulator-only adapter planning
- trace schema planning
- tag/log validation context

## Proposed Owner Review Checklist

Use this checklist during owner review. Do not update registers until the owner has reviewed the row.

| Item | Review question | Proposed outcome type |
| --- | --- | --- |
| M1 boundary | Is M1 limited to protocol core and synthetic tests? | Approve/Reject |
| `DEC-DEV-001` | Is Python standard library acceptable for M1, with C#/.NET reserved for later integration if needed? | Approve/Reject/Defer |
| `DEC-STORAGE-001` | Is the external artifact storage policy/location class accepted? | Approve/Reject/Defer |
| `DEC-REPO-001` | Is Desktop/nested repository topology accepted for M1? | Approve/Reject/Defer |
| `SRC-PROTO-001` | Is the protocol DOCX candidate the reviewed protocol authority? | Approve/Reject/Replace |
| `SRC-K117-001` | Is the K117 AT candidate and reviewed scope the catalog baseline? | Approve/Reject/Replace |
| `SRC-NA-001` | Should NetArrays baseline remain M2+ deferred? | Deferred for M1 |
| `SRC-TIME-001` | What exact timing/config source is acceptable? | Approved 2026-06-28 |
| `DEC-PROTO-002` | What is the ACK correlation rule? | Confirm/Defer |
| `DEC-PROTO-003` | What is the CRC profile and vector authority? | Confirm/Defer |
| `DEC-RETRY-001` | Are retry/link-off parameters needed in M1? | M1/Defer |
| `DEC-TIME-001` | Is actual scan-cycle timing needed in M1? | M1/Defer |
| `DEC-TAG-001` | Should LOXFS/NetArrays tag review remain M2+? | Confirm/Promote exact aliases |
| `DEC-LOG-001` | Should iFIX/log/historian context remain M2+? | Confirm/Promote exact aliases |

## Register Update Rules After Review

Only after owner review:

- Update `references/decision_register.csv` for approved or deferred decisions.
- Update `references/source_register.csv` only with reviewed metadata.
- Keep actual source files external.
- Use aliases and SHA-256 only.
- Do not insert actual absolute paths, endpoint values, credentials, packet capture content, tag row values, catalog row values, DB rows, or actual configuration values.
- Re-run validation and readiness gates after register updates.

## Expected Next Commands After Owner Review

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 validate
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 test
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 quality-gate
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 owner-review
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 m1-readiness
```

`QUALITY_GATE_PASS` alone does not mean Protocol Core is validated. M1 starts only when the readiness gate reports `M1_READINESS_READY`.

## Draft Conclusion

The current recommended direction is:

- Keep M1 narrow: protocol core, source-backed structure, synthetic tests.
- Use RSID protocol source and K117 catalog source as the primary M1 evidence path.
- Use RSID inspection to shape questions and separation boundaries, not to invent expected values.
- Treat LOXFS/NetArrays/iFIX materials as high-value M2+ context unless exact aliases are owner-promoted.
- Decide the M1 runtime after reviewing the implementation boundary, not from later integration needs.
- Do not update Decision or Source registers until this packet is reviewed by the owner.
