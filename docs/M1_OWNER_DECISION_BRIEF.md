# M1 Owner Decision Brief

Last updated: 2026-06-28

## Purpose

This brief compresses `docs/M1_OWNER_REVIEW_PACKET.md` into owner-facing choices.

It is a draft. It does not close decisions, approve sources, update registers, or authorize M1 implementation. After owner review, accepted choices must be recorded separately in:

- `references/decision_register.csv`
- `references/source_register.csv`
- `STATUS.md`
- `ACCEPTANCE_TRACE.md`

Current state after the 2026-06-28 owner approvals:

| Gate | Result |
| --- | --- |
| Owner review | `OWNER_REVIEW_CLEAR` |
| M1 readiness | `M1_READINESS_READY` |
| M1 Protocol Core | Not started |

Resolved or deferred by owner review on 2026-06-28:

- `DEC-STORAGE-001`: approved external artifact storage policy.
- `DEC-REPO-001`: approved current Desktop/nested topology for M1 with risk acceptance.
- `SRC-PROTO-001`: approved protocol DOCX alias and SHA-256 metadata.
- `SRC-K117-001`: approved K117 catalog PDF alias and SHA-256 metadata.
- `SRC-NA-001`: deferred from direct M1 readiness to M2+.

Runtime decision:

- `DEC-DEV-001`: approved Python standard-library M1 Protocol Core on 2026-06-28.
- C#/.NET/C++ remain later adapter or Windows/iFIX/OPC/NetArrays integration options.

Source identity decision:

- `SRC-TIME-001`: approved `RSID_PROGRAM/RSIDGW/GatewaySetting.xml` as timing/config source identity on 2026-06-28.
- Actual timing, retry, endpoint, channel, and configuration values remain external and deferred to M2 behavior review.

## Recommended Direction

Recommended owner-level direction:

| Area | Recommendation | Reason |
| --- | --- | --- |
| M1 boundary | Approve narrow M1: protocol core and synthetic tests only. | Prevents transport, NetArrays, iFIX, and legacy runtime scope from leaking into M1. |
| Runtime | Approve Python standard library for M1 Protocol Core only. | Best fit for deterministic codec, table validation, and fast regression tests. |
| Later integration | Keep C#/.NET open for later adapter or Windows integration work. | Later stages may need Windows/runtime interoperability that M1 does not need. |
| Protocol authority | Use protocol DOCX candidate only after owner metadata confirmation. | Strongest current packet/header/data block/ACK/session source candidate. |
| Catalog authority | Use K117 AT catalog candidate only after owner metadata and scope confirmation. | Strongest current catalog-scope candidate. |
| NetArrays/LOXFS/iFIX | Keep as M2+ supporting material unless exact aliases are owner-promoted later. | Valuable for tag/log/scenario/oracle work, not direct packet authority. |
| ACK/CRC/retry/timing values | Do not hard-code unresolved values. | Prevents speculative implementation. |

## Immediate Owner Choices

### 1. M1 Boundary

Recommended choice: **Approve narrow M1**.

Owner answer needed:

| Choice | Meaning |
| --- | --- |
| Approve | M1 may include only protocol encode/decode, table-backed structure, placeholder CRC interfaces if needed, and synthetic tests. |
| Reject | M1 scope must be redefined before any implementation. |
| Defer | M1 remains blocked. |

Register impact after approval:

- No direct register row required unless owner wants a new decision row.
- Keep `docs/DEVELOPMENT_PLAN.md` unchanged because the current M1 definition already matches this boundary.

### 2. DEC-DEV-001 - Runtime and Language

Recommended choice: **Approve Python standard library for M1 only; reserve C#/.NET for later if needed**.

Decision wording to consider after owner approval:

```text
M1 Protocol Core may use Python standard library for protocol encode/decode, table validation, and synthetic tests. C#/.NET remains available for later transport, adapter, or Windows integration work if separately approved.
```

Owner answer needed:

| Choice | Meaning |
| --- | --- |
| Approve recommendation | Use Python for M1. Keep C#/.NET open for later phases. |
| Reject recommendation | Provide the required runtime/language constraint before M1. |
| Defer | M1 remains blocked by `DEC-DEV-001`. |

Do not infer this from local tool availability alone.

### 3. DEC-STORAGE-001 - External Artifact Root

Recommended choice: **Approve external artifact storage policy/location class, not a sensitive absolute path in Git**.

Decision wording to consider after owner approval:

```text
Actual artifacts, packages, documents, configs, logs, screenshots, and run outputs remain outside the repository. Git stores only source files, specifications, synthetic fixtures, path aliases, SHA-256 values, and non-sensitive notes.
```

Owner answer needed:

| Choice | Meaning |
| --- | --- |
| Approve recommendation | External artifact root policy is accepted; actual files remain outside Git. |
| Reject recommendation | Provide a different storage policy before M1. |
| Defer | M1 remains blocked by `DEC-STORAGE-001`. |

Do not record the real artifact root path in source files.

### 4. DEC-REPO-001 - Repository Topology

Recommended choice: **Approve current Desktop/nested topology for now with explicit risk acceptance; keep GitHub backup-only**.

Decision wording to consider after owner approval:

```text
The current Desktop worktree may be retained for M1 with nested repository risk accepted by the owner. The owner-designated GitHub remote remains backup/publication only and is not source authority, runtime dependency, artifact storage, or validation evidence.
```

Owner answer needed:

| Choice | Meaning |
| --- | --- |
| Approve recommendation | Current topology is acceptable for M1. |
| Reject recommendation | Move or restructure must happen before M1. |
| Defer | M1 remains blocked by `DEC-REPO-001`. |

Do not change parent Git settings automatically.

## Required Source Choices

M1 readiness currently requires direct M1 source rows to have reviewed metadata:

- revision
- non-absolute path alias
- 64-hex SHA-256
- owner
- `reviewed` or `approved` review state

### 5. SRC-PROTO-001 - Protocol Source

Recommended choice: **Approve the protocol DOCX candidate if owner confirms the exact artifact and metadata**.

Candidate currently recorded in source notes:

| Candidate alias | Current use |
| --- | --- |
| `RSID_DOC/230131_Command Signal Protocol Design VerI.docx` | Packet/header/data block/packet type/session source candidate. |

Owner answer needed:

| Choice | Meaning |
| --- | --- |
| Approve candidate | Record reviewed metadata in `source_register.csv`. |
| Replace candidate | Provide another protocol authority alias and metadata. |
| Defer | M1 remains blocked by `SRC-PROTO-001`. |

Do not use this approval to close CRC or ACK correlation decisions automatically.

### 6. SRC-K117-001 - K117 Catalog Source

Recommended choice: **Approve the K117 AT catalog candidate and reviewed scope only if owner confirms it is the M1 catalog baseline**.

Candidate currently recorded in source notes:

| Candidate alias | Current use |
| --- | --- |
| `K117_BASELINE/K117.00_RSID_AT_submission_composite.pdf` | K117 command/signal catalog-scope candidate. |

Owner answer needed:

| Choice | Meaning |
| --- | --- |
| Approve candidate and scope | Record reviewed catalog metadata in `source_register.csv`. |
| Replace candidate or scope | Provide the approved catalog source and reviewed scope. |
| Defer | M1 remains blocked by `SRC-K117-001`. |

Do not import catalog row values into Git.

### 7. SRC-NA-001 - NetArrays Baseline

Owner decision on 2026-06-28: **Defer `SRC-NA-001` to M2+ and do not use LOXFS/NetArrays review rows as M1 packet authority**.

Current evidence classes:

| Evidence class | Recommended classification |
| --- | --- |
| `MAINTENANCE_LOXFS_NETARRAYS` review workspace | M2+ derivative/supporting evidence by default. |
| TEACS/NetArrays metadata candidates | Possible `SRC-NA-001` identity source after owner selection. |
| iFIX materials | M4+ SCADA/tag/log context by default. |

Register impact:

- `SRC-NA-001` remains `not_collected` and `M2+ deferred`.
- `scripts/m1_readiness.py` no longer treats `SRC-NA-001` as a direct M1 blocker.
- NetArrays, LOXFS, iFIX, DBN, tag-map, and driver material remain excluded from M1 packet authority unless a later owner review promotes exact aliases.

Do not register an entire folder. Select exact aliases only.

### 8. SRC-TIME-001 - Timing / Configuration Source

Owner decision on 2026-06-28: **Approve `RSID_PROGRAM/RSIDGW/GatewaySetting.xml` as timing/config source identity for M1 readiness, while deferring actual timing values to M2**.

Current evidence classes:

| Evidence class | Recommended classification |
| --- | --- |
| GatewaySetting family | Timing/configuration source candidate, values not recorded. |
| Runtime config candidates | Category-level source context only. |

Register state:

- `references/source_register.csv` records `SRC-TIME-001` with alias and SHA-256 metadata.
- M1 may use synthetic timing only.
- Actual timing, retry, endpoint, channel, and configuration values remain outside Git.

Do not record actual timing, endpoint, channel, or configuration values in Git.

## Protocol Decisions To Review After Source Selection

These are not all direct readiness-script blockers, but they affect whether M1 implementation would be speculative.

| Decision | Recommended current choice | Register action after owner review |
| --- | --- | --- |
| `DEC-PROTO-002` ACK correlation | Defer exact ACK matching until field rule is source-backed; allow structural ACK parsing only if owner approves. | Keep Open or record explicit limited M1 scope. |
| `DEC-PROTO-003` CRC profile/vector | Keep CRC implementation behind placeholder interface until profile and independent vectors are approved. | Keep Open or record explicit placeholder-only M1 scope. |
| `DEC-RETRY-001` retry/link-off | Defer parameter values; allow state labels only if needed. | Keep Open or record M1 defer. |
| `DEC-TIME-001` actual scan cycle | Defer actual timing behavior to M2 unless owner says M1 needs it. | Keep Open or record M1 defer. |
| `DEC-TAG-001` tag read/write | Keep M2+ by default. | Keep Open. |
| `DEC-LOG-001` packet/tag trace schema | Keep M2+ by default. | Keep Open. |

## Static Inspection Update - 2026-06-28

Read-only RSID Program static recheck found stronger implementation hints, but no decision-closing evidence.

| Area | Recheck result | Decision impact |
| --- | --- | --- |
| CRC helper | `RSIDGW` and `RSIDSIM` artifacts expose `Crc32` helper names, `CRC32Calc`, `m_checksumTable`, `checksumRegister`, header CRC, data CRC, and dummy data-block CRC labels. | Confirms CRC implementation exists in legacy artifacts, but does not identify profile or vector. Keep `DEC-PROTO-003` Open. |
| CRC profile | No focused printable terms were found for polynomial, reflect/refin/refout, xorout, named CRC variant, or common polynomial literal. | Do not implement authoritative CRC yet. Use placeholder/injectable CRC interface if M1 proceeds later. |
| ACK construction | Gateway and simulator artifacts expose `MakeAckPacket`, `ReceiveAck`, `ackPacket`, packet container, raw packet, and data block parse/build names. | ACK structure is strongly suggested, but exact match rule remains unproven. Keep `DEC-PROTO-002` Open. |
| ACK correlation candidates | `TypeOfData`, `SizeOfDataBlock`, `LPNET_LastSequenceNumber`, and packet-time labels are visible. | Treat as candidate fields only; owner must confirm actual ACK correlation. |
| Retry/timing | ACK-wait and link-loss timing labels are visible. | Do not hard-code values. Keep `DEC-RETRY-001` and `DEC-TIME-001` Open or explicitly defer to M2. |
| Timing/config source identity | `SRC-TIME-001` source identity is selected. | Actual values remain outside Git and deferred to M2. |

Updated recommendation: static inspection supports the planned M1 architecture shape, but it does not remove the need for source-backed CRC profile, independent CRC vector, ACK correlation rule, and timing/config source selection.

## M2+ Material Classification

Recommended classification:

| Material | Default classification | Promote to M1 only if |
| --- | --- | --- |
| `MAINTENANCE_LOXFS_NETARRAYS` | M2+ scenario/oracle/tag/logic review evidence. | Owner selects exact aliases as supporting evidence, not packet authority. |
| `IFIX` | M4+ iFIX/SCADA/HMI/tag/log context. | Owner selects exact aliases as supporting evidence, not packet authority. |
| SAT PDF | Supporting workflow/procedure context. | Owner explicitly approves procedural context for M1 tests. |
| Design Description PDF | Architecture and separation context. | Owner approves module-boundary influence only. |
| IFF preliminary PDFs | N3F/N3G target context. | Owner decides target context is in scope. |

Default recommendation: do not promote these to M1 packet authority.

## Review Checklist For Owner

Use this table as the actual review worksheet.

| Item | Recommended answer | Owner decision |
| --- | --- | --- |
| M1 boundary | Approve narrow protocol-core-only M1. | TBD |
| `DEC-DEV-001` | Approve Python standard library for M1; keep C#/.NET/C++ open for later. | Approved 2026-06-28 |
| `DEC-STORAGE-001` | Approve external artifact storage policy/location class only. | Approved 2026-06-28 |
| `DEC-REPO-001` | Approve Desktop/nested topology for M1 with risk acceptance. | Approved 2026-06-28 |
| `SRC-PROTO-001` | Approve protocol DOCX candidate if exact metadata is confirmed. | Approved 2026-06-28 |
| `SRC-K117-001` | Approve K117 AT catalog candidate/scope if exact metadata is confirmed. | Approved 2026-06-28 |
| `SRC-NA-001` | Defer from direct M1 readiness and keep as M2+ source identity. | Approved 2026-06-28 |
| `SRC-TIME-001` | Select exact timing/config source identity or keep M1 blocked. | Approved 2026-06-28 |
| `DEC-PROTO-002` | Defer ACK correlation rule unless source-backed. | TBD |
| `DEC-PROTO-003` | Use placeholder CRC interface until source-backed profile/vectors exist. | TBD |
| `DEC-RETRY-001` | Defer retry/link-off values. | TBD |
| `DEC-TIME-001` | Defer actual timing values unless required for M1. | TBD |
| `DEC-TAG-001` | Keep M2+. | TBD |
| `DEC-LOG-001` | Keep M2+. | TBD |

## If Owner Approves The Recommended Path

Expected register changes after explicit owner approval:

| File | Likely update |
| --- | --- |
| `references/decision_register.csv` | Close or record approved/deferred scope for `DEC-DEV-001`, `DEC-STORAGE-001`, and `DEC-REPO-001`; possibly record limited M1 scope for protocol-specific decisions. |
| `references/source_register.csv` | Fill reviewed metadata for direct M1 sources only with aliases and SHA-256 values; keep `SRC-NA-001` deferred unless promoted later. |
| `STATUS.md` | Summarize owner-approved decisions and remaining blockers. |
| `ACCEPTANCE_TRACE.md` | Add evidence references after validation and readiness reruns. |

Do not update these files until the owner has reviewed and approved the chosen rows.

## Commands After Register Updates

Run after owner-approved register changes:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 validate
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 test
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 quality-gate
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 owner-review
powershell -ExecutionPolicy Bypass -File scripts\repo.ps1 m1-readiness
```

Expected target before M1 starts:

```text
QUALITY_GATE_PASS
OWNER_REVIEW_CLEAR
M1_READINESS_READY
```

## Short Recommendation

Approve a narrow M1, use Python standard library for the M1 protocol core, keep C#/.NET open for later integration, confirm exact protocol and catalog sources, select exact NetArrays and timing source identities, and keep LOXFS/NetArrays/iFIX review materials as M2+ support unless exact aliases are owner-promoted.
