# Source Review Notes

Last updated: 2026-06-26

This file is a provisional, not approval, does not close decisions receipt for read-only source review observations gathered during Phase 0 hardening.

It is not a canonical source register, approval record, acceptance trace, or decision closure. The authoritative records remain:

- `references/source_register.csv`
- `references/decision_register.csv`
- `ACCEPTANCE_TRACE.md`
- `STATUS.md`

## Scope

- Preserve source review observations that were discussed in-session before M1 Protocol Core begins.
- Use aliases, hashes, sizes, roles, M1 impact, decision impact, and owner actions only.
- Keep all entries provisional until source owner review updates the canonical registers.
- Do not record actual absolute paths, endpoints, IP values, port values, credentials, actual configuration values, or catalog row values.
- Do not copy source artifacts into this repository.
- Do not close Open decisions from these notes.

## Verification Status Values

Allowed values used in this file:

- `observed_in_session`
- `metadata_recheck_needed`
- `content_recheck_needed`
- `owner_review_required`

## Review Backlog and Priority

This backlog orders remaining read-only reviews by M1 blocker impact. It does not approve source rows, close decisions, or authorize implementation.

| Priority | Source candidate | Main purpose | Related decisions or sources | Current action |
| --- | --- | --- | --- | --- |
| P0 | Protocol DOCX | Packet, header, data block, ACK/session, CRC question source review | `SRC-PROTO-001`, `DEC-PROTO-002`, `DEC-PROTO-003`, `DEC-RETRY-001`, `DEC-TIME-001` | Owner confirmation remains required. |
| P0 | K117 AT pages 14-34 | Catalog scope and M1 source baseline candidate | `SRC-K117-001`, `DEC-PROTO-001` | Owner confirmation remains required. |
| P0 | GatewaySetting XML family | Timing, retry, endpoint/channel, runtime configuration source family review without values | `SRC-RSIDCFG-001`, `SRC-TIME-001`, `SRC-NETMAP-001`, `DEC-NET-001`, `DEC-TIME-001`, `DEC-RETRY-001` | Owner must select variant or approved family. |
| P0 | SAT PDF | Session, ACK procedure, and command/signal test workflow cross-check | `DEC-PROTO-002`, `DEC-DEV-001` | Targeted review complete; owner action remains. |
| P0 | Runtime config files | Runtime setting category review without actual values | `SRC-TIME-001`, `DEC-NET-001`, `DEC-TIME-001`, `DEC-DEV-001`, `DEC-LOG-001` | Targeted review complete; owner action remains. |
| P1 | Design Description PDF | Legacy architecture boundary and module separation context | `DEC-DEV-001`, `DEC-LOG-001` | Owner decision needed for supporting-source role. |
| P1 | RSIDGW schema candidates | Trace/log schema shape context | `DEC-LOG-001` | Owner decision needed for supporting-source role. |
| P1 | Operator Instruction PDF | Operator workflow, registry, trace, log, and DB procedure context | `DEC-LOG-001`, `DEC-TAG-001`, `DEC-NET-001` | Defer unless owner requests supporting evidence. |
| P2 | TEACS CSV and FBK family | NetArrays or TEACS baseline identity for later tag mapping | `SRC-NA-001`, `DEC-TAG-001` | Owner must select baseline artifact; no NetArrays execution. |
| P2 | Historian and alarm XLSX files | Reference-only historian, alarm, or validation context | `DEC-LOG-001`, `DEC-TAG-001` | Defer unless owner requests supporting evidence. |
| P2 | WBS PDF | Reference-only system breakdown context | `DEC-TAG-001`, `DEC-NET-001` | Defer unless owner requests supporting evidence. |

## M1 Owner Action Matrix

| Blocker | Evidence currently available | Remaining owner action |
| --- | --- | --- |
| `DEC-DEV-001` | DD and SAT review candidates can inform runtime/module boundary; owner selected Python standard library for M1. | Owner-approved 2026-06-28. |
| `DEC-STORAGE-001` | External storage policy and candidate-root observation exist outside this note. | Owner-approved 2026-06-28. |
| `DEC-REPO-001` | Desktop worktree retention is the working direction, but nested parent Git remains a recorded risk. | Owner-approved 2026-06-28. |
| `SRC-PROTO-001` | Protocol DOCX metadata and packet-structure observations exist. | Owner-approved 2026-06-28. |
| `SRC-K117-001` | K117 AT scoped catalog extraction metadata exists. | Owner-approved 2026-06-28. |
| `SRC-NA-001` | TEACS/NetArrays metadata candidates exist. | Deferred to M2+ on 2026-06-28. |
| `SRC-TIME-001` | GatewaySetting and runtime config candidates exist. | Owner-approved `RSID_PROGRAM/RSIDGW/GatewaySetting.xml` as source identity on 2026-06-28. |

## Reviewed Source Candidates

### 1. Protocol DOCX

| Field | Value |
| --- | --- |
| Candidate source ID | `SRC-PROTO-001` |
| Alias | `RSID_DOC/230131_Command Signal Protocol Design VerI.docx` |
| Size | 70735 bytes |
| SHA-256 | `FBE90FE971B9D208AD353AE0EB6E03FC0DE4020DEB95F760B92F7E31B9AE680D` |
| Role | Protocol definition candidate |
| verification_status | `observed_in_session`; `owner_review_required` |

Observed evidence:

- Header length candidate: 48 bytes.
- Data block length candidate: 10 bytes.
- Big-endian field interpretation candidate.
- Packet type, ACK pair, session control, sequence number, repeated transmission, ACK wait, retransmission, and link-loss concepts were observed.

M1 impact:

- Strongest current candidate for packet, header, data block, ACK pair, and session structure.
- Protocol Core should not start until owner review confirms this source metadata in the canonical register.

Decision impact:

- Supports review for `DEC-PROTO-002`, `DEC-PROTO-003`, `DEC-RETRY-001`, and `DEC-TIME-001`.
- Does not close those decisions.

Owner action:

- Confirm revision, alias, SHA-256, owner, and review state for `SRC-PROTO-001`.
- Provide independent CRC profile and test vector authority before implementation.

#### Targeted Review Update - 2026-06-25

Reviewed scope:

- DOCX duplicate metadata check in the owner-provided external document collection.
- Packet structure section.
- Header structure table.
- Data block structure table.
- Data packet type table.
- Session control table.
- ACK/retry behavior paragraphs.
- CRC-related paragraphs.

Observed evidence:

- Four external DOCX candidates with the same size and SHA-256 were observed; canonical alias assignment remains an owner action.
- The reviewed DOCX contains 261 non-empty paragraphs and 6 tables.
- Packet structure states that a data packet is composed of a header and data block combination.
- Header size candidate remains 48 bytes.
- Data block size candidate remains 10 bytes; data block multiplicity remains provisional because 0, 1, n, and TBD wording were observed.
- Byte order candidate remains big-endian.
- Header field layout candidate totals 48 bytes:
  - Type of Data: 4 bytes.
  - Sequence Number of Packet: 4 bytes.
  - Number of Repeated Transmission: 4 bytes.
  - Size of Data Block(s): 4 bytes.
  - Time: 8 bytes.
  - Reserve: 16 bytes, with TBD wording.
  - CRC32 of Data Block / Detail Type: 4 bytes.
  - CRC32 of Header: 4 bytes.
- Data block field layout candidate totals 10 bytes:
  - Data Block Header: 1 byte.
  - Data Dimension: 1 byte.
  - Command/Signal ID: 4 bytes.
  - Data: 4 bytes.
- Data packet type candidates were observed as request/ACK pairs:
  - `USR_CONTROL` / `USR_CONTROL_ACK`.
  - `PERIODIC_USR_DATA` / `PERIODIC_USR_DATA_ACK`.
  - `USR_TESTING` / `USR_TESTING_ACK`.
  - `APERIODIC_USR_DATA` / `APERIODIC_USR_DATA_ACK`.
- Session control candidates were observed:
  - `SESSION_CLOSE` / `SESSION_CLOSE_ACK`.
  - `SESSION_OPEN` / `SESSION_OPEN_ACK`.
- ACK behavior was observed at protocol level:
  - non-ACK packet receipt triggers the corresponding ACK packet.
  - ACK packets are described as header-only.
  - sender treats ACK receipt as normal transmission.
  - missing ACK leads to same-packet retransmission and updates `Number of Repeated Transmission`.
  - extended ACK absence is treated as link-loss behavior.
- Session open/close sequencing includes a minimum interval statement, but the numeric timing value is not promoted here because timing remains owner-reviewed source material.
- CRC fields are described for both data block and header:
  - data block CRC applies when data blocks exist.
  - detail type usage applies when data blocks do not exist.
  - header CRC excludes the header CRC field itself.
  - a standard CRC function is mentioned.
- No polynomial, initial value, final xor, reflection setting, or independent CRC test vector was confirmed in this targeted review.
- ACK pair names and immediate ACK behavior were observed, but the exact ACK correlation field or field set was not confirmed.
- Table 1 network/configuration default values were deliberately not recorded as source note values because retry/timing/config decisions remain Open.

M1 impact:

- This review strengthens the provisional basis for protocol table structure, field lengths, packet type pairings, and session control pairings.
- It does not make the Protocol Core ready to implement because CRC profile/test vectors and ACK correlation rules remain unresolved.
- Header/data block field candidates may guide later synthetic fixtures only after owner review confirms the source baseline.

Decision impact:

- `DEC-PROTO-002` remains Open because ACK correlation fields were not confirmed.
- `DEC-PROTO-003` remains Open because CRC profile and test vectors were not confirmed.
- `DEC-RETRY-001` remains Open because retransmission behavior was observed but retry parameters are not owner-approved.
- `DEC-TIME-001` remains Open because timing statements were observed but not promoted to actual operating timing.

Owner action:

- Protocol owner must confirm whether this DOCX is the reviewed source for `SRC-PROTO-001`.
- Protocol owner must provide or identify CRC profile details and independent test vectors.
- Protocol owner must confirm the ACK correlation rule.
- Protocol owner must confirm which observed packet/session values may be promoted from provisional source review into protocol specification tables.

verification_status:

- `observed_in_session`
- `owner_review_required`

### 2. K117 AT Composite PDF

| Field | Value |
| --- | --- |
| Candidate source ID | `SRC-K117-001` |
| Alias | `K117_BASELINE/K117.00_RSID_AT_submission_composite.pdf` |
| Size | 7681957 bytes |
| SHA-256 | `6B06EB397D2737C66FFD6EF897CE737D60F4CE71F45CCCA3680B2C4481F33FEC` |
| Role | K117 Command and Signal catalog authority candidate |
| verification_status | `observed_in_session`; `owner_review_required` |

Observed evidence:

- Extraction scope was limited to pages 14-34.
- Aperiodic, periodic, and internal or signal table sections were observed.
- Catalog scope summary observed: 21 tables, 890 rows, 840 non-empty rows.
- No catalog row values are recorded in this repository.

M1 impact:

- Candidate baseline source for Command and Signal catalog coverage.
- Not enough by itself to approve source completeness until owner review updates the canonical source register.

Decision impact:

- Supports review for `DEC-PROTO-001`, `DEC-TAG-001`, `DEC-NET-001`, `DEC-LOG-001`, and `DEC-STORAGE-001`.
- Does not close those decisions.

Owner action:

- Confirm catalog revision, alias, SHA-256, owner, and review state for `SRC-K117-001`.
- Decide whether the scoped pages should become the owner-reviewed M1 catalog baseline.

#### Targeted Review Update - 2026-06-25

Reviewed scope:

- Metadata recheck for the K117 AT composite PDF candidate.
- Pages 14-34 only.
- Table count, row count, non-empty row count, and section-category keyword signals only.
- Catalog row values were not printed or recorded.

Observed evidence:

- A K117 AT PDF candidate with matching size and SHA-256 was observed; the filename variant still requires owner alias confirmation.
- The reviewed PDF has 88 pages.
- Pages 14-34 contain 21 extracted tables.
- The scoped extraction counted 890 table rows and 840 non-empty rows.
- Aperiodic, periodic, internal/signal, command, LOXFS, and network/channel label categories were observed in the scoped text.
- No IPv4-like or credential-label candidates were detected in the scoped pages by this text extraction.

M1 impact:

- This remains the strongest current catalog-scope candidate for `SRC-K117-001`.
- The extraction confirms coverage shape only; it does not authorize importing catalog row values into Git or fixtures.
- Protocol Core may later need synthetic catalog fixtures, but expected values must come from owner-reviewed source material or a sanitized independent oracle.

Decision impact:

- `DEC-PROTO-001` remains Open because authoritative catalog revision and owner-reviewed scope are not recorded in the source register.
- `DEC-TAG-001` remains Open because NetArrays tag mapping authority is separate from this catalog extraction.
- `DEC-NET-001` remains Open because network/channel labels were observed but approved endpoint/channel mapping is not selected.

Owner action:

- Confirm whether pages 14-34 of this PDF are the reviewed M1 catalog baseline.
- Provide owner-reviewed revision, alias, SHA-256, owner, and review state for `SRC-K117-001`.
- Keep all catalog row values and endpoint details outside Git unless a separate sanitized fixture is explicitly approved.

verification_status:

- `observed_in_session`
- `owner_review_required`

### 3. SAT PDF

| Field | Value |
| --- | --- |
| Candidate source ID | `SRC-RSIDSAT-001` |
| Alias | `RSID_SAT/K117.00-I-213-011-PC_Rev1.pdf` |
| Size | 1308942 bytes |
| SHA-256 | `5B42F5A824CEF69E7FA666F3EF3AF606A484A7ADF5B92431A45504B1601B9A78` |
| Role | SAT procedure reference |
| verification_status | `observed_in_session`; `owner_review_required` |

Observed evidence:

- Session open and close procedure evidence was observed.
- Session ACK and Command and Signal test procedure evidence was observed.
- Procedure checklist evidence was observed.

M1 impact:

- Useful procedure evidence for expected workflow and session behavior.
- Not the primary packet authority.

Decision impact:

- Supports review for `DEC-PROTO-002` and `DEC-DEV-001`.
- Does not close those decisions.

Owner action:

- Decide whether SAT evidence should be added as a supporting source row.
- Keep procedure evidence separate from protocol field authority.

#### Targeted Review Update - 2026-06-26

Reviewed scope:

- Metadata recheck for the SAT PDF candidate.
- Full-document text extraction for procedure and workflow keywords only.
- Session open/close, ACK, command/signal test workflow, expected-result wording, retry, timing, CRC, and network-label category search.
- Sensitive value candidate counting only; actual values were not printed or recorded.

Observed evidence:

- A SAT PDF candidate with matching size and SHA-256 was observed; the filename variant contains spacing/date details that still require owner alias confirmation.
- The reviewed SAT PDF has 31 text-extractable pages.
- Session open and session close keyword evidence was observed.
- ACK keyword evidence was observed in the same procedure area as session workflow evidence.
- Command/signal and procedure/checklist language was observed across the document.
- Expected-result or pass/fail style language was observed, but no expected values are recorded here.
- Timing-label language was observed, but actual timing values were not promoted.
- Retry terms were not found by this text extraction.
- CRC terms were not found by this text extraction.
- Network-label language and credential-label candidates exist in the source text, but no actual values are recorded in this repository.

M1 impact:

- SAT evidence can support workflow understanding for session open/close, ACK procedure, and command/signal test flow.
- SAT evidence does not resolve ACK correlation fields, retry parameters, CRC profile, or CRC test vectors.
- SAT evidence is procedure context only and must remain separate from packet field authority and independent expected-result authority.

Decision impact:

- `DEC-PROTO-002` remains Open because ACK correlation fields were not confirmed.
- `DEC-PROTO-003` remains Open because CRC profile and test vectors were not observed.
- `DEC-RETRY-001` remains Open because retry terms were not confirmed in this SAT extraction.
- This historical procedure review did not close `DEC-DEV-001`; owner approval was later recorded on 2026-06-28.

Owner action:

- Decide whether SAT should be registered as a supporting source row.
- Confirm whether SAT workflow evidence may be used as procedural context for M1 tests.
- Keep SAT expected-result wording separate from synthetic golden vectors and independent oracle material.

verification_status:

- `observed_in_session`
- `owner_review_required`

### 4. Design Description PDF

| Field | Value |
| --- | --- |
| Candidate source ID | `SRC-RSIDDD-001` |
| Alias | `RSID_DESIGN/K117.00-I-209-004-DD_Rev0.pdf` |
| Size | 3295569 bytes |
| SHA-256 | `92B473CDF3E58E519EA065F706FF2BF5ED6C44C09CC246506C366B18D9B9F8D9` |
| Role | Legacy design description reference |
| verification_status | `observed_in_session`; `owner_review_required` |

Observed evidence:

- MVVM, database manager, LPNet manager, packet container, packet data block, protocol define, Modbus container, voting, Command and Signal configuration, map, signal history, and DB/log field candidates were observed.

M1 impact:

- Helps keep Protocol Core independent from UI, DB, Modbus, voting, and legacy runtime concerns.
- Does not provide final CRC profile authority.

Decision impact:

- Supports review for `DEC-DEV-001`, `DEC-PROTO-002`, `DEC-PROTO-003`, and `DEC-LOG-001`.
- Does not close those decisions.

Owner action:

- Decide which architecture observations are allowed to influence M1 structure.
- Keep legacy implementation observations separate from expected-result authority.

#### Targeted Review Update - 2026-06-25

Reviewed scope:

- Metadata recheck for the DD PDF candidate in the owner-provided external document collection.
- Full-document text extraction for architecture and boundary keywords only.
- Legacy component boundary signals relevant to M1 runtime and module separation.
- Protocol-related keyword search for ACK, retry, session, and CRC authority signals.

Observed evidence:

- A DD PDF candidate with matching size and SHA-256 was observed; the filename variant contains a revision/date label that still requires owner alias confirmation.
- The reviewed PDF has 128 text-extractable pages.
- Architecture and legacy implementation terms were observed across the document, including MVVM, database manager, LPNet manager, packet container, packet data block, protocol define, Modbus, voting, Command and Signal configuration, map, signal history, UI, thread, DB, and log concepts.
- ACK, session, retry, and timing terms were observed, but this review did not confirm an ACK correlation field set, retry parameter authority, or operating timing authority.
- CRC terms were not found by text extraction in this DD review, so the DD PDF does not currently reduce the `DEC-PROTO-003` blocker.
- The extracted source text contains endpoint/configuration/credential label candidates, but no actual values are recorded in this repository.

M1 impact:

- The DD PDF supports a separation rule for M1: Protocol Core should remain independent from UI, DB, Modbus, voting, signal history, runtime configuration, and legacy process execution concerns.
- The DD PDF may inform module boundary review, but it is not sufficient to choose Python or C# by itself and must not be treated as expected-result authority.
- Packet container and data block references can support later owner review against the Protocol DOCX, but Protocol DOCX remains the stronger packet-structure candidate.

Decision impact:

- This historical design review did not close `DEC-DEV-001`; owner approval was later recorded on 2026-06-28.
- `DEC-PROTO-002` remains Open because ACK correlation was not confirmed.
- `DEC-PROTO-003` remains Open because CRC profile and test vectors were not confirmed.
- `DEC-LOG-001` remains Open because DB/log/schema details are legacy context only at this stage.

Owner action:

- Confirm whether the DD PDF should be registered as a supporting source row.
- Decide which architecture observations may constrain M1 module boundaries.
- Keep DD-derived observations separate from independent oracle and expected-result sources.

verification_status:

- `observed_in_session`
- `owner_review_required`

### 5. GatewaySetting XML Family

| Field | Value |
| --- | --- |
| Candidate source IDs | `SRC-RSIDCFG-001`, `SRC-TIME-001`, `SRC-NETMAP-001` |
| Alias family | `RSIDCFG/RSIDGW/.../GatewaySetting.xml`, `RSIDLOG/.../GatewaySetting.xml`, `RSIDSIM/.../GatewaySetting.xml` |
| Role | Restricted configuration source family |
| verification_status | `observed_in_session`; `owner_review_required` |

Observed metadata:

| Alias | Size | SHA-256 |
| --- | ---: | --- |
| `RSIDCFG/RSIDGW/ConfigFiles/GatewaySetting.xml` | 499844 | `AD5AA03DF51F8BFAAB671061AB9F58B5D863E1273FEAEB90870EA2C36E9BFF72` |
| `RSIDCFG/RSIDGW/GatewaySetting.xml` | 490488 | `7E51C78E5B9751A3EBF001FA74716B033FA9FE37C5694D4E094779AFB85A6700` |
| `RSIDCFG/RSIDGW/ConfigFiles/GW2_Config/GatewaySetting.xml` | 499844 | `6982E1650EDEF57C00F4E8ECACE8B8EAB9BF1E2A3764AF0B08D7E2B2FE556D34` |
| `RSIDCFG/RSIDGW/ConfigFiles/GW3_Config/GatewaySetting.xml` | 499844 | `9AA236D878EAC84DAACD90B8DDE8C22E2BC84BFE5AC96FB602B5EF5514842589` |
| `RSIDCFG/RSIDGW/ConfigFiles/SIM/GatewaySetting.xml` | 499815 | `22CDB70ABF4CE53A151DAFAD8F530AD24F42930A95E6F9453848A2CE2C5F9007` |
| `RSIDCFG/RSIDGW/ConfigFiles/TEACS/GatewaySetting.xml` | 499844 | `AD5AA03DF51F8BFAAB671061AB9F58B5D863E1273FEAEB90870EA2C36E9BFF72` |
| `RSIDLOG/ConfigFiles/GatewaySetting.xml` | 499815 | `3E4C64EDBC10A9B5E923A95C681708BD3F60156773E84FF1ACBE1DF601893559` |
| `RSIDSIM/ConfigFiles/GatewaySetting.xml` | 499815 | `3E4C64EDBC10A9B5E923A95C681708BD3F60156773E84FF1ACBE1DF601893559` |

Observed evidence:

- Multiple GatewaySetting variants exist.
- Some variants share identical hashes.
- Timing, retry, sequence, heartbeat, information period, and Modbus-related key names were observed.
- Network-related key names were observed, but no values are recorded here.

M1 impact:

- Candidate family for timing, retry, endpoint/channel, and runtime configuration review.
- Variant ownership must be selected before any authoritative value is recorded.

Decision impact:

- Supports review for `DEC-NET-001`, `DEC-RETRY-001`, `DEC-TIME-001`, and `DEC-STORAGE-001`.
- Does not close those decisions.

Owner action:

- Select the owner-reviewed variant or variant family for M1 source baseline.
- Confirm alias, hash, owner, and review state without recording actual configuration values.

#### Targeted Review Update - 2026-06-25

Reviewed scope:

- Read-only metadata and XML parse check for GatewaySetting candidates under the external RSID configuration family.
- Element and attribute name category review only.
- Sensitive value candidate counting only; actual values were not printed or recorded.

Observed evidence:

- Fifteen GatewaySetting XML candidates were observed in the restricted configuration family review.
- The observed candidates form multiple duplicate-hash groups; owner alias mapping is still required before any source row can be reviewed.
- All reviewed candidates parsed as XML.
- Element and attribute names contain timing, retry, sequence, heartbeat, Modbus, database/log, and network/channel categories.
- Value-level candidates for endpoint-like and URL-like material exist in the source content, but no actual values are recorded in this repository.
- No credential-label key names were observed in the XML element or attribute names during this targeted review.

M1 impact:

- GatewaySetting is a plausible source family for timing, retry, endpoint/channel, and runtime configuration context.
- It is not safe to derive active profile values from these files; M1 and M2 profiles must stay loopback-only and sanitized.
- Variant selection is now the main blocker for treating any configuration metadata as source-reviewed.

Decision impact:

- `DEC-NET-001` remains Open because approved endpoint/channel mapping is not selected or recorded.
- `DEC-TIME-001` remains Open because actual timing values were not promoted.
- `DEC-RETRY-001` remains Open because retry parameter values were not promoted.
- `DEC-STORAGE-001` remains Open because configuration artifacts must remain external under an owner-approved root.

Owner action:

- Select the exact owner-reviewed GatewaySetting variant or explicitly approve a variant family.
- Provide reviewed alias, hash, owner, and review state for any source row update.
- Keep all actual endpoint, URL, timing, retry, and configuration values outside Git.

verification_status:

- `observed_in_session`
- `owner_review_required`

### 6. Runtime Config Files

| Field | Value |
| --- | --- |
| Candidate source IDs | `SRC-RSIDGWCFG-001`, `SRC-TIME-001` |
| Role | Restricted runtime configuration source candidates |
| verification_status | `observed_in_session`; `owner_review_required` |

Observed metadata:

| Alias | Size | SHA-256 |
| --- | ---: | --- |
| `RSIDGW/RSIDGW.exe.config` | 2823 | `CB676E9ACB35BA67A91D5CCE4803D87FA400D6FCBF30AD69FBE72CB5AED1C661` |
| `RSIDSIM/RSIDSIM.exe.config` | 2238 | `74B18B1A5CBAF9DAEE93A099F7073C3497F32C40A75E09CF0C24C19C6CC47B64` |
| `RSIDLOG/RSIDLOG.exe.config` | 1702 | `AE152F3CF6361335F99ECCD6D2BB73C9F00EA29669D3C665AE2360493FB8A68D` |

Observed evidence:

- Runtime setting names were observed in these config files.
- Time synchronization, simulator, network, and restricted access related setting groups were observed.
- No setting values are recorded here.

M1 impact:

- Useful for deciding what must remain out of Git and what may become sanitized profile defaults.
- Not sufficient to authorize actual runtime configuration.

Decision impact:

- Supports review for `DEC-NET-001`, `DEC-TIME-001`, `DEC-DEV-001`, `DEC-STORAGE-001`, and `DEC-LOG-001`.
- Does not close those decisions.

Owner action:

- Decide whether any sanitized metadata belongs in `source_register.csv`.
- Keep actual runtime config files external only.

#### Targeted Review Update - 2026-06-26

Reviewed scope:

- Metadata recheck for runtime config candidates.
- XML parse check and key/name token category review only.
- Timing, network, simulator, database/log, legacy runtime, and security/access categories.
- Sensitive value candidate counting only; actual values were not printed or recorded.

Observed evidence:

- Three runtime config candidates were observed with matching size and SHA-256 values.
- All reviewed runtime config candidates parsed as XML.
- `RSIDGW/RSIDGW.exe.config` contains timing, network, legacy runtime, and security/access key-name categories.
- `RSIDLOG/RSIDLOG.exe.config` contains timing, network, database/log, legacy runtime, and security/access key-name categories.
- `RSIDSIM/RSIDSIM.exe.config` contains timing, network, simulator, legacy runtime, and security/access key-name categories.
- IPv4-like and security/access value candidates exist in source content, but no actual values are recorded in this repository.
- No URL-like or UNC-like values were recorded by this review.

M1 impact:

- Runtime config files can support identifying which setting categories must remain external and sanitized.
- Runtime config files may help owner review for `SRC-TIME-001`, but they do not authorize importing actual timing, endpoint, access, or runtime values.
- M1 and M2 profiles must remain loopback-only and must not be derived directly from actual runtime config values.

Decision impact:

- `DEC-TIME-001` remains Open because actual timing values were not promoted.
- `DEC-NET-001` remains Open because endpoint/channel values were not recorded or approved.
- This historical config review did not close `DEC-DEV-001`; owner approval was later recorded on 2026-06-28.
- `DEC-LOG-001` remains Open because logging/schema behavior remains supporting context only.

Owner action:

- Decide whether runtime config metadata should support `SRC-TIME-001` or remain supporting evidence only.
- Confirm which source should be treated as timing authority without recording actual values.
- Keep all runtime config values and files external only.

verification_status:

- `observed_in_session`
- `owner_review_required`

### 7. RSID Operator Instruction PDF

| Field | Value |
| --- | --- |
| Candidate source ID | `SRC-RSIDEOI-001` |
| Alias | `RSID_OI/K117.00-I-211-001-OI_RevA_RSID_SERVER.pdf` |
| Size | 9494100 bytes |
| SHA-256 | `CFA222996ACBEF5FDA1D404752E06736F14363979B3475547080631AC6E2507D` |
| Role | Operator instruction and DB/log operation reference |
| verification_status | `observed_in_session`; `owner_review_required` |

Observed evidence:

- RDB operation, DB connection setting screen and fields, Command and Signal registry operation, log, tracer, monitoring, SCADA DB backup, import, and save procedure evidence were observed.

M1 impact:

- Useful as restricted operational context.
- Not schema authority and not protocol authority.

Decision impact:

- Supports review for `DEC-LOG-001`, `DEC-NET-001`, `DEC-STORAGE-001`, and `DEC-TAG-001`.
- Does not close those decisions.

Owner action:

- Decide whether any non-sensitive operational metadata should be registered.
- Keep restricted operational procedure details outside Git.

### 8. TEACS CSV and FBK Family

| Field | Value |
| --- | --- |
| Candidate source ID | `SRC-NA-001` |
| Role | NetArrays and TEACS export or raw package family |
| verification_status | `observed_in_session`; `owner_review_required` |

Observed metadata:

| Alias | Size | SHA-256 |
| --- | ---: | --- |
| `NETARRAYS/LOXFS/O_2/TEACS2_240116.csv` | 6068716 | `C8B470ED00F0D2810C4848E31234FBB98FC482440594D7C750613569D77C13B2` |
| `NETARRAYS/LOXFS/O/TEACS2_240116.csv` | 6068716 | `C8B470ED00F0D2810C4848E31234FBB98FC482440594D7C750613569D77C13B2` |
| `NETARRAYS/LOXFS/O_2/TEACS2_210116_O.csv` | 2854875 | `1E26530618FF0B1CDD44C1BDA7B85DA576AB2BF7735797F6FC7573C25D6D1BCF` |
| `NETARRAYS/LOXFS/O/TEACS2_210116_O.csv` | 2854875 | `1E26530618FF0B1CDD44C1BDA7B85DA576AB2BF7735797F6FC7573C25D6D1BCF` |
| `NETARRAYS/LOXFS/O/TEACS2.fbk` | 186277925 | `A59502354EC50F7BC9E2F8A211C991816A2EFCD9FA31F9352395389B242BE504` |

Observed evidence:

- CSV files appeared to be encoded as a Korean Windows code page and were not normal header CSV tables.
- Two CSV alias pairs shared duplicate hashes.
- The FBK package was treated as a raw binary backup package.
- NetArrays was not executed.

M1 impact:

- Candidate NetArrays or TEACS source family for later tag mapping and simulator adapter work.
- Not a packet protocol authority for M1 Protocol Core.

Decision impact:

- Supports review for `DEC-TAG-001` and `DEC-STORAGE-001`.
- Does not close those decisions.

Owner action:

- Confirm which export or package should become the owner-reviewed `SRC-NA-001` baseline.
- Keep raw packages external only.

### 9. Historian and Alarm XLSX Files

| Field | Value |
| --- | --- |
| Candidate source IDs | `SRC-HIST-*`, `SRC-ALARM-*` |
| Role | Reference-only historian or alarm source candidates |
| verification_status | `observed_in_session`; `owner_review_required` |

Observed metadata:

| Alias | Size | SHA-256 |
| --- | ---: | --- |
| `HISTORIAN/LOXFS_FT_CMD_SIG_20211021.xlsx` | 68572 | `F65726D3D33B3241094DFA6C3AE36D0A994951FD0C62E0F818CF417A9B29B31A` |
| `HISTORIAN/LOXFS_WDR_CMD_SIG_20210901.xlsx` | 68579 | `9625066953A81E67E342D841126EA202A010FADFE758CF8B442F3EFC33B71066` |

Observed evidence:

- Sheet names indicating dry-run and D-day contexts were observed.
- Network-like candidates were detected during review but values are not recorded here.

M1 impact:

- Reference-only support for alarm, historian, or validation context.
- Not source authority for protocol fields or catalog rows.

Decision impact:

- Supports review for `DEC-TAG-001`, `DEC-LOG-001`, `DEC-NET-001`, and `DEC-STORAGE-001`.
- Does not close those decisions.

Owner action:

- Decide whether these should become supporting source rows.
- Keep spreadsheet files external only.

### 10. WBS PDF

| Field | Value |
| --- | --- |
| Candidate source ID | `SRC-K117WBS-001` |
| Alias | `REFERENCE/K.00-I-WB-201-001_Rev0.pdf` |
| Size | 728735 bytes |
| SHA-256 | `F57B2CD78B63CD706709E4FD7608238E49BA15A8147C6BB63087BC58CE51A818` |
| Role | WBS and system breakdown reference |
| verification_status | `observed_in_session`; `owner_review_required` |

Observed evidence:

- WBS and system breakdown identifiers were observed.

M1 impact:

- Reference-only context.
- Not a protocol, catalog, endpoint, timing, or tag mapping authority.

Decision impact:

- Supports review for `DEC-TAG-001`, `DEC-NET-001`, and `DEC-STORAGE-001`.
- Does not close those decisions.

Owner action:

- Decide whether WBS context should be registered as a supporting reference source.

### 11. MariaDB MSI and DB Tool Folder

| Field | Value |
| --- | --- |
| Candidate source IDs | `SRC-DBRUNTIME-001`, `SRC-RSIDDBTOOL-001` |
| Alias | `RSID_DB_TOOL/mariadb-10.3.12-winx64.msi` |
| Size | 54886400 bytes |
| SHA-256 | `52A04DADB2E013BFE6F42CDF5DDE23B5D8DD4F524F26D055BFB4985AABF6ADCD` |
| Role | Runtime installer reference only |
| verification_status | `observed_in_session`; `owner_review_required` |

Observed evidence:

- The folder inventory contained the MSI package only.
- No schema source file was observed in this package inventory.
- The installer was not installed or executed.

M1 impact:

- No direct M1 Protocol Core impact.
- Confirms runtime installer material must remain external only.

Decision impact:

- Supports review for `DEC-LOG-001` and `DEC-STORAGE-001`.
- Does not close those decisions.

Owner action:

- Keep runtime installers external.
- Locate schema authority separately if DB/log behavior becomes part of M2 or later evidence.

## Newly Discovered / Provisional Schema Review

### RSIDGW Schema Candidates

| Field | Value |
| --- | --- |
| Candidate aliases | `RSIDGW/Schema/rsiddb.sql`, `RSIDGW/Schema/rsiddb.mwb` |
| Candidate role | DB schema source candidates |
| verification_status | `observed_in_session`; `owner_review_required` |

Observed evidence:

- `RSIDGW/Schema/rsiddb.sql` metadata was rechecked: size 10730 bytes, SHA-256 `2CB209ED4C87EBFF34580CD302C8577516D48082AC6492FC183D38FED31D3830`.
- `RSIDGW/Schema/rsiddb.mwb` metadata was rechecked: size 30068 bytes, SHA-256 `760491F32219476AD0E7789C6300735A9E9F26693DD378387B953D143F6EBF26`.
- The SQL candidate has 186 lines, 10 `CREATE TABLE` statements, no `INSERT` statements, no view or trigger statements, 19 index/key/constraint tokens, and no foreign-key tokens by text scan.
- The MWB candidate is a ZIP-style model container with 3 internal files and 388272 bytes of uncompressed internal content.
- No IPv4-like or credential-label candidates were detected in the SQL text by this review.
- Schema table and column names were not recorded in this repository.

M1 impact:

- No M1 Protocol Core packet authority.
- Potential future evidence for trace, DB, or log schema review.
- SQL schema shape may inform later trace/log boundary discussions, but it must not be used as protocol expected-result authority.

Decision impact:

- Relevant to `DEC-LOG-001`.
- Does not close the decision.

Owner action:

- Decide whether either schema file should become an owner-reviewed supporting source row.
- Do not import schema content into Git unless a separate owner review approves a sanitized source change.
- Keep database tools and MariaDB unexecuted during Phase 0.

## Register Update Candidates

These are candidates only. They do not modify the canonical registers.

| Candidate | Possible action |
| --- | --- |
| `SRC-PROTO-001` | Confirm protocol DOCX metadata and owner review. |
| `SRC-K117-001` | Confirm scoped K117 catalog baseline metadata and owner review. |
| `SRC-NA-001` | Confirm owner-reviewed TEACS or NetArrays baseline artifact. |
| `SRC-TIME-001` | Confirm owner-reviewed timing/config source without recording actual values. |
| `SRC-RSIDCFG-001` | Confirm owner-reviewed GatewaySetting variant or family. |
| Additional supporting sources | Decide whether SAT, DD, OI, WBS, historian, and DB schema candidates should be registered. |

## Final Document Keyword Sweep - 2026-06-26

This sweep checked whether the current document set can resolve CRC profile, CRC test vector, ACK correlation, retry, or timing blockers before moving to RSID static inspection. It used read-only metadata-matched documents and recorded only aggregate counts.

Reviewed documents:

| Alias | Match state | Scope |
| --- | --- | --- |
| `RSID_DOC/230131_Command Signal Protocol Design VerI.docx` | matched; 4 duplicate candidates observed | DOCX text units only |
| `K117_BASELINE/K117.00_RSID_AT_submission_composite.pdf` | matched | PDF text extraction |
| `RSID_SAT/K117.00-I-213-011-PC_Rev1.pdf` | matched | PDF text extraction |
| `RSID_DESIGN/K117.00-I-209-004-DD_Rev0.pdf` | matched | PDF text extraction |
| `RSID_OI/K117.00-I-211-001-OI_RevA_RSID_SERVER.pdf` | matched | PDF text extraction |

Aggregate keyword result:

| Alias | CRC general | CRC profile-specific | CRC vector | ACK general | ACK/correlation-related | Retry/timing | Packet structure |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `RSID_DOC/230131_Command Signal Protocol Design VerI.docx` | 13 | 0 | 0 | 13 | 43 | 33 | 31 |
| `K117_BASELINE/K117.00_RSID_AT_submission_composite.pdf` | 0 | 15 | 0 | 3 | 15 | 41 | 8 |
| `RSID_SAT/K117.00-I-213-011-PC_Rev1.pdf` | 0 | 0 | 0 | 2 | 15 | 0 | 0 |
| `RSID_DESIGN/K117.00-I-209-004-DD_Rev0.pdf` | 0 | 0 | 0 | 6 | 2 | 27 | 11 |
| `RSID_OI/K117.00-I-211-001-OI_RevA_RSID_SERVER.pdf` | 0 | 0 | 0 | 3 | 40 | 23 | 8 |

Interpretation:

- The Protocol DOCX remains the only reviewed document with CRC field-level evidence, but it still does not expose CRC profile-specific terms or independent test vectors.
- K117 AT had profile-specific keyword hits without CRC-general hits, so those hits are treated as generic text matches, not CRC profile evidence.
- SAT, DD, and OI provide workflow or legacy-context ACK and packet hints, but they do not confirm the ACK correlation field set.
- OI adds operational context but remains supporting evidence only; it is not protocol authority and not expected-result authority.
- Retry/timing terms exist across multiple documents, but actual values are not promoted and remain owner-reviewed configuration/source material.
- Sensitive candidate labels or endpoint-like patterns may exist in extracted source text; no actual values are recorded here.

Decision impact:

- `DEC-PROTO-002` remains Open because document evidence still does not identify a confirmed ACK correlation field set.
- `DEC-PROTO-003` remains Open because document evidence still does not identify CRC polynomial, initial value, final xor, reflection settings, or independent test vectors.
- `DEC-RETRY-001` remains Open because retry/timing documents do not provide owner-approved parameter authority in this repository.
- `DEC-TIME-001` remains Open because actual timing values remain external configuration/source material.

Next boundary:

- If the owner cannot provide CRC/ACK authority directly, the next useful step is RSID static inspection for implementation hints only.
- RSID static inspection must be recorded as legacy implementation observation, not source authority, not owner approval, and not expected-result oracle material.

## RSID Static Inspection Dry-run - 2026-06-26

This owner-requested pass inspected RSID package candidates as read-only legacy implementation observation after the document keyword sweep. It did not execute, load, decompile, debug, compile, install, copy, move, or delete any external artifact.

Inspection boundary:

- Scope was limited to file inventory, SHA-256, size, and aggregate keyword-category counts.
- Output used aliases only; no absolute external paths are recorded.
- Config, endpoint, network, credential, catalog, DB row, and runtime values were not printed or recorded.
- Category counts are raw string-category hits, not validated semantic matches.
- Results are implementation hints only and do not update `references/source_register.csv`, `references/decision_register.csv`, or `ACCEPTANCE_TRACE.md`.

Inventory summary:

| Component | Extension | Count |
| --- | --- | ---: |
| `RSIDCFG` | `.xml` | 15 |
| `RSIDGW` | `.config` | 1 |
| `RSIDGW` | `.dll` | 15 |
| `RSIDGW` | `.exe` | 7 |
| `RSIDGW` | `.mwb` | 1 |
| `RSIDGW` | `.pdb` | 2 |
| `RSIDGW` | `.sql` | 1 |
| `RSIDGW` | `.txt` | 1 |
| `RSIDLOG` | `.config` | 1 |
| `RSIDLOG` | `.dll` | 6 |
| `RSIDLOG` | `.exe` | 1 |
| `RSIDLOG` | `.pdb` | 2 |
| `RSIDSIM` | `.config` | 1 |
| `RSIDSIM` | `.dll` | 6 |
| `RSIDSIM` | `.exe` | 1 |
| `RSIDSIM` | `.pdb` | 2 |

Inventory result:

- Total candidates: 63 files.
- Unique file groups by component, extension, name, size, and SHA-256: 56.
- GatewaySetting family: 15 XML files across 8 unique file groups.
- No files were copied into this repository.

Core static candidates:

| Alias | Size | SHA-256 | Role |
| --- | ---: | --- | --- |
| `RSID_STATIC/RSIDGW/RSIDGW.exe` | 982016 | `685E0F2F9064B1D840002EDE269F68EFD96608DBA00CFD9493C55724D8CDC962` | legacy binary, not executed |
| `RSID_STATIC/RSIDGW/RSIDGW.pdb` | 652800 | `6079A5DE9280FCC1593CDADC623FE66DD7555CB8855950C903F3AC01860DAABD` | symbol/debug metadata |
| `RSID_STATIC/RSIDGW/CommLib.dll` | 8704 | `EF56B60ACA2B9A27B588AC9A3ED823B21A1C6F0EA646159FEC49521DFA079BB8` | legacy library, not loaded |
| `RSID_STATIC/RSIDSIM/RSIDSIM.exe` | 225280 | `18449F05A5C4D63C069762A7835237228F882538238CC78D9EFF1409B8315493` | legacy binary, not executed |
| `RSID_STATIC/RSIDSIM/RSIDSIM.pdb` | 368128 | `6EBEB32485DCC5D2DD4D7035D8706E602516F4D680576E11952B0302EAA23FF6` | symbol/debug metadata |
| `RSID_STATIC/RSIDSIM/CommLib.dll` | 7680 | `8ABFDA487B58A11181C430CCA307299746E60A17854602EDA9C8A6BF365E12A4` | legacy library, not loaded |
| `RSID_STATIC/RSIDLOG/RSIDLOG.exe` | 4151296 | `04EE571A3EA50C12925166E8D6AC6DB77B88FEC0FCDC417E5105E9338F0EA4F8` | legacy binary, not executed |
| `RSID_STATIC/RSIDLOG/RSIDLOG.pdb` | 484864 | `74A945E602243F64BF324D926A02F973B850252230B0E1DBEF57B7094C292B9A` | symbol/debug metadata |
| `RSID_STATIC/RSIDLOG/CommLib.dll` | 8704 | `EF56B60ACA2B9A27B588AC9A3ED823B21A1C6F0EA646159FEC49521DFA079BB8` | legacy library, not loaded |
| `RSID_STATIC/RSIDGW/rsiddb.sql` | 10730 | `2CB209ED4C87EBFF34580CD302C8577516D48082AC6492FC183D38FED31D3830` | database schema candidate |
| `RSID_STATIC/RSIDGW/rsiddb.mwb` | 30068 | `760491F32219476AD0E7789C6300735A9E9F26693DD378387B953D143F6EBF26` | database model container |

Runtime configuration candidates rechecked:

| Alias | Size | SHA-256 |
| --- | ---: | --- |
| `RSID_STATIC/RSIDGW/RSIDGW.exe.config` | 2823 | `CB676E9ACB35BA67A91D5CCE4803D87FA400D6FCBF30AD69FBE72CB5AED1C661` |
| `RSID_STATIC/RSIDSIM/RSIDSIM.exe.config` | 2238 | `74B18B1A5CBAF9DAEE93A099F7073C3497F32C40A75E09CF0C24C19C6CC47B64` |
| `RSID_STATIC/RSIDLOG/RSIDLOG.exe.config` | 1702 | `AE152F3CF6361335F99ECCD6D2BB73C9F00EA29669D3C665AE2360493FB8A68D` |

Keyword category result:

| Alias or family | CRC | ACK | ACK/correlation | Retry/timing | Session | Packet structure | Network label | Credential label |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `RSID_STATIC/RSIDCFG/GatewaySetting*.xml` | 0 | 44 each | 12 each | 8 each | 0 | 0 | 5966-6182 each | 0 |
| `RSID_STATIC/RSIDGW/RSIDGW.exe.config` | 0 | 0 | 0 | 0 | 0 | 0 | 12 | 4 |
| `RSID_STATIC/RSIDSIM/RSIDSIM.exe.config` | 0 | 0 | 0 | 0 | 0 | 0 | 20 | 4 |
| `RSID_STATIC/RSIDLOG/RSIDLOG.exe.config` | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 6 |
| `RSID_STATIC/RSIDGW/CommLib.dll` | 6 | 36 | 34 | 0 | 0 | 26 | 3 | 0 |
| `RSID_STATIC/RSIDSIM/CommLib.dll` | 6 | 36 | 26 | 0 | 0 | 26 | 3 | 0 |
| `RSID_STATIC/RSIDLOG/CommLib.dll` | 6 | 36 | 34 | 0 | 0 | 26 | 3 | 0 |
| `RSID_STATIC/RSIDGW/RSIDGW.exe` | 50 | 567 | 270 | 89 | 21 | 292 | 646 | 318 |
| `RSID_STATIC/RSIDGW/RSIDGW.pdb` | 76 | 298 | 172 | 66 | 0 | 280 | 538 | 8 |
| `RSID_STATIC/RSIDSIM/RSIDSIM.exe` | 56 | 448 | 184 | 53 | 20 | 271 | 366 | 210 |
| `RSID_STATIC/RSIDSIM/RSIDSIM.pdb` | 64 | 232 | 128 | 34 | 0 | 246 | 436 | 0 |
| `RSID_STATIC/RSIDLOG/RSIDLOG.exe` | 44 | 444 | 258 | 22 | 12 | 287 | 799 | 360 |
| `RSID_STATIC/RSIDLOG/RSIDLOG.pdb` | 0 | 134 | 120 | 16 | 0 | 20 | 394 | 8 |
| `RSID_STATIC/RSIDGW/rsiddb.sql` | 0 | 6 | 6 | 0 | 0 | 12 | 4 | 0 |
| `RSID_STATIC/RSIDGW/rsiddb.mwb` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Additional container metadata:

- `RSID_STATIC/RSIDGW/rsiddb.mwb` was treated as a ZIP-style model container only: 3 internal files, 388272 uncompressed bytes.
- Internal model content, table names, and column names were not recorded.

Interpretation:

- RSIDGW, RSIDSIM, and RSIDLOG binaries contain CRC, ACK, ACK/correlation, retry/timing, session, and packet-structure labels by static string-category scan.
- PDB files expose additional category labels and may be useful for later non-executing static review, but they are still legacy implementation observation, not source authority.
- `CommLib.dll` has repeated ACK/correlation and packet-structure labels across components, suggesting a possible shared protocol helper candidate for later static inspection.
- GatewaySetting XML files contain ACK, correlation, retry/timing, and network-label categories, but no actual values are recorded and no variant is selected.
- Runtime config files contain network and credential labels, reinforcing that actual config values must remain external and owner-reviewed.
- The schema files remain log/DB support candidates only and do not provide protocol authority.

Decision impact:

- `DEC-PROTO-002` remains Open because the static scan does not confirm the authoritative ACK correlation rule.
- `DEC-PROTO-003` remains Open because string hits do not confirm CRC polynomial, initial value, final xor, reflection settings, or independent test vectors.
- `DEC-RETRY-001` remains Open because retry/timing labels do not approve parameter values.
- `DEC-TIME-001` remains Open because timing values remain external configuration/source material.
- This historical static RSID observation did not close `DEC-DEV-001`; owner approval was later recorded on 2026-06-28.

Owner action:

- Decide whether to permit a deeper read-only static inspection focused on non-sensitive symbols, type names, and method/category names.
- Provide CRC profile and independent test vector authority separately from legacy implementation observation.
- Confirm ACK correlation, retry, and timing authority through owner-reviewed sources before Protocol Core starts.
- Keep actual binaries, PDBs, configs, schema files, endpoints, credentials, and runtime values outside Git.

## RSID Program Package Static Review - 2026-06-26

This owner-requested pass inspected the `RSID_PROGRAM` external package root as read-only legacy implementation observation. It did not execute, load, decompile, debug, compile, install, copy, move, or delete any external file.

Review boundary:

- Scope was limited to inventory, extension distribution, SHA-256, binary/PDB printable-string categories, and sanitized symbol-like tokens.
- Output used aliases only; no absolute external paths are recorded.
- Actual configuration values, endpoint values, credentials, DB rows, source paths, and package-local absolute paths were not recorded.
- PDB path-like string counts were observed but path values were deliberately not recorded.
- Results are implementation hints only and do not update `references/source_register.csv`, `references/decision_register.csv`, or `ACCEPTANCE_TRACE.md`.

Package inventory summary:

| Item | Observation |
| --- | --- |
| Root alias | `RSID_PROGRAM` |
| Directory count | 33 |
| File count | 144 |
| Total bytes | 120366862 |
| Source-like project files | None observed for `.cs`, `.sln`, `.csproj`, `.vb`, `.c`, `.cpp`, `.h`, `.hpp`, or XAML source files. |
| Hidden/system Office decoy pattern | `.docx` entries were observed in the package tree and treated as environmental/documentation inventory only, not source authority. |

Component summary:

| Component alias | File count | Total bytes | Main observed extensions |
| --- | ---: | ---: | --- |
| `RSID_PROGRAM/RSID_DB_TOOL` | 2 | 54886400 | `.msi`, `.docx` |
| `RSID_PROGRAM/RSIDGW` | 95 | 47943567 | `.dll`, `.exe`, `.pdb`, `.config`, `.xml`, `.sql`, `.mwb`, `.db`, manuals/support files |
| `RSID_PROGRAM/RSIDSIM` | 15 | 3356965 | `.exe`, `.dll`, `.pdb`, `.config`, `.xml` |
| `RSID_PROGRAM/RSIDLOG` | 31 | 14179930 | `.exe`, `.dll`, `.pdb`, `.config`, `.xml`, UI assets |

Core package artifacts:

| Alias | Size | SHA-256 | Role |
| --- | ---: | --- | --- |
| `RSID_PROGRAM/RSIDGW/RSIDGW.exe` | 982016 | `685E0F2F9064B1D840002EDE269F68EFD96608DBA00CFD9493C55724D8CDC962` | legacy binary, not executed |
| `RSID_PROGRAM/RSIDGW/RSIDGW.pdb` | 652800 | `6079A5DE9280FCC1593CDADC623FE66DD7555CB8855950C903F3AC01860DAABD` | symbol/debug metadata |
| `RSID_PROGRAM/RSIDGW/CommLib.dll` | 8704 | `EF56B60ACA2B9A27B588AC9A3ED823B21A1C6F0EA646159FEC49521DFA079BB8` | shared communication library candidate, not loaded |
| `RSID_PROGRAM/RSIDSIM/RSIDSIM.exe` | 225280 | `18449F05A5C4D63C069762A7835237228F882538238CC78D9EFF1409B8315493` | legacy simulator binary, not executed |
| `RSID_PROGRAM/RSIDSIM/RSIDSIM.pdb` | 368128 | `6EBEB32485DCC5D2DD4D7035D8706E602516F4D680576E11952B0302EAA23FF6` | simulator symbol/debug metadata |
| `RSID_PROGRAM/RSIDSIM/CommLib.dll` | 7680 | `8ABFDA487B58A11181C430CCA307299746E60A17854602EDA9C8A6BF365E12A4` | simulator communication library candidate, not loaded |
| `RSID_PROGRAM/RSIDLOG/RSIDLOG.exe` | 4151296 | `04EE571A3EA50C12925166E8D6AC6DB77B88FEC0FCDC417E5105E9338F0EA4F8` | legacy log binary, not executed |
| `RSID_PROGRAM/RSIDLOG/RSIDLOG.pdb` | 484864 | `74A945E602243F64BF324D926A02F973B850252230B0E1DBEF57B7094C292B9A` | log symbol/debug metadata |
| `RSID_PROGRAM/RSIDLOG/CommLib.dll` | 8704 | `EF56B60ACA2B9A27B588AC9A3ED823B21A1C6F0EA646159FEC49521DFA079BB8` | shared communication library candidate, not loaded |
| `RSID_PROGRAM/RSIDGW/rsiddb.sql` | 10730 | `2CB209ED4C87EBFF34580CD302C8577516D48082AC6492FC183D38FED31D3830` | database schema candidate |
| `RSID_PROGRAM/RSIDGW/rsiddb.mwb` | 30068 | `760491F32219476AD0E7789C6300735A9E9F26693DD378387B953D143F6EBF26` | database model container |
| `RSID_PROGRAM/RSID_DB_TOOL/mariadb-10.3.12-winx64.msi` | 54886400 | `52A04DADB2E013BFE6F42CDF5DDE23B5D8DD4F524F26D055BFB4985AABF6ADCD` | runtime installer reference only, not installed |

Static category result for binaries and PDB files:

| Alias | CRC | ACK | ACK/correlation | Retry/timing | Session | Packet structure | Path-like strings | Credential labels |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `RSID_PROGRAM/RSIDGW/CommLib.dll` | 3 | 18 | 17 | 0 | 16 | 13 | 1 | 0 |
| `RSID_PROGRAM/RSIDGW/CommLib.pdb` | 0 | 0 | 12 | 0 | 12 | 6 | 16 | 0 |
| `RSID_PROGRAM/RSIDGW/RSIDGW.exe` | 27 | 282 | 137 | 45 | 142 | 152 | 2 | 159 |
| `RSID_PROGRAM/RSIDGW/RSIDGW.pdb` | 36 | 149 | 86 | 33 | 163 | 144 | 412 | 4 |
| `RSID_PROGRAM/RSIDSIM/CommLib.dll` | 3 | 18 | 13 | 0 | 16 | 13 | 1 | 0 |
| `RSID_PROGRAM/RSIDSIM/CommLib.pdb` | 0 | 0 | 8 | 0 | 12 | 6 | 16 | 0 |
| `RSID_PROGRAM/RSIDSIM/RSIDSIM.exe` | 31 | 230 | 99 | 27 | 71 | 145 | 1 | 105 |
| `RSID_PROGRAM/RSIDSIM/RSIDSIM.pdb` | 32 | 116 | 64 | 17 | 68 | 127 | 228 | 0 |
| `RSID_PROGRAM/RSIDLOG/CommLib.dll` | 3 | 18 | 17 | 0 | 16 | 13 | 1 | 0 |
| `RSID_PROGRAM/RSIDLOG/CommLib.pdb` | 0 | 0 | 12 | 0 | 12 | 6 | 16 | 0 |
| `RSID_PROGRAM/RSIDLOG/RSIDLOG.exe` | 23 | 227 | 128 | 11 | 64 | 144 | 100 | 181 |
| `RSID_PROGRAM/RSIDLOG/RSIDLOG.pdb` | 0 | 67 | 60 | 8 | 61 | 10 | 320 | 4 |

Sanitized protocol-symbol observations:

- `CommLib.dll` exposes protocol error and session labels such as `DataBlockCRCError`, `HeaderCRCError`, `SequenceNumberError`, `SessionOpenCommand`, `SessionCloseCommand`, `GetSessionStatus`, and synchronous packet send labels.
- `RSIDGW.pdb` exposes strong packet construction/parsing labels such as `CRC32Calc`, `get_CrcOfDataBlock`, `get_CrcOfHeader`, `get_DataBlock`, `get_Header`, `get_RawPacket`, `get_ReceiveAck`, `get_SizeOfDataBlock`, `get_TypeOfData`, and packet queue labels.
- `RSIDSIM.pdb` exposes strong simulator-side packet labels such as `MakeAckPacket`, `MakeErrorPacket`, `MakePacket`, `SetContainerFromPacket`, `PacketContainer`, `PacketDataBlock`, `ReceiveAck`, `SessionOpen`, and `SessionClose`.
- `RSIDLOG.pdb` exposes trace/log-side ACK and packet-time labels such as `get_Ack`, `ackType`, ACK checkbox labels, `packettime`, and communication-log container labels.
- `.NET` runtime and WPF-related labels were observed in the binaries, which supports that the legacy programs are .NET/WPF applications; this does not by itself decide the M1 implementation language.

Interpretation:

- The package is a deployed binary/runtime package, not a source-code package.
- The strongest read-only implementation hints for Protocol Core are `RSIDGW.pdb`, `RSIDSIM.pdb`, and the `CommLib.dll` family.
- `RSIDSIM.pdb` is particularly useful for ACK packet construction and packet container naming hints.
- `RSIDGW.pdb` is particularly useful for CRC, raw packet, ACK receipt, and gateway packet queue naming hints.
- PDBs contain path-like strings, so raw PDB strings must not be copied into repository notes or fixtures.
- Credential-label counts in EXE/config contexts reinforce that actual runtime configuration and DB/log values must remain external and owner-reviewed.

Decision impact:

- `DEC-PROTO-002` remains Open because symbol labels indicate ACK handling but do not prove the authoritative ACK correlation rule.
- `DEC-PROTO-003` remains Open because `CRC32Calc` and CRC field labels do not identify polynomial, init, final xor, reflection settings, or independent vectors.
- `DEC-RETRY-001` remains Open because retry/timing labels do not authorize parameter values.
- This historical legacy .NET/WPF observation did not close `DEC-DEV-001`; owner approval was later recorded on 2026-06-28.

Owner action:

- Decide whether a deeper non-executing PDB/symbol review is permitted for method-level names only.
- Provide or identify actual legacy source code if source-level review is intended; this package does not contain source-like project files.
- Provide CRC profile and independent test vectors from owner-reviewed authority.
- Confirm ACK correlation rule separately from legacy symbol observations.
- Keep binaries, PDBs, configs, installers, schema files, endpoint/config values, and PDB raw paths outside Git.

## RSID Method-Focus Static Review - 2026-06-26

This owner-requested pass narrowed the prior `RSID_PROGRAM` static review to method-level symbol groups from selected PDB, EXE, and DLL files. It remains a read-only legacy implementation observation and does not execute, load, decompile, debug, compile, install, copy, move, or delete any external file.

Review boundary:

- Scope was limited to selected PDB/EXE/DLL printable strings and sanitized symbol grouping.
- Raw PDB strings, local build paths, endpoint/config values, credential labels, and source paths were not recorded.
- No source code was available in the package and no decompilation was performed.
- The result is a question-shaping aid for owner review, not an authoritative protocol source.

Focused artifacts:

| Alias | Size | SHA-256 | Primary value of this pass |
| --- | ---: | --- | --- |
| `RSID_METHOD_FOCUS/RSIDGW/RSIDGW.pdb` | 652800 | `6079A5DE9280FCC1593CDADC623FE66DD7555CB8855950C903F3AC01860DAABD` | Gateway packet container, CRC, ACK receipt, retry queue, and trace/log boundary names. |
| `RSID_METHOD_FOCUS/RSIDSIM/RSIDSIM.pdb` | 368128 | `6EBEB32485DCC5D2DD4D7035D8706E602516F4D680576E11952B0302EAA23FF6` | Simulator ACK construction, packet assembly, CRC field, session, and parse-from-packet names. |
| `RSID_METHOD_FOCUS/RSIDGW/RSIDGW.exe` | 982016 | `685E0F2F9064B1D840002EDE269F68EFD96608DBA00CFD9493C55724D8CDC962` | Runtime string confirmation for gateway queues and ACK-wait packet categories. |
| `RSID_METHOD_FOCUS/RSIDSIM/RSIDSIM.exe` | 225280 | `18449F05A5C4D63C069762A7835237228F882538238CC78D9EFF1409B8315493` | Runtime string confirmation for simulator ACK-wait queues and packet categories. |
| `RSID_METHOD_FOCUS/*/CommLib.dll` | varies by component | shared or component-specific hashes recorded in prior section | Common session, data block, CRC-error, sequence-error, and synchronous packet send labels. |

Method-group observations:

| Group | RSIDGW signal | RSIDSIM signal | Interpretation |
| --- | --- | --- | --- |
| ACK construction | `MakeAckPacket`, `get_ReceiveAck`, `set_ReceiveAck`, `ackPacket`, `APERIODIC_USR_DATA_ACK`, `USR_CONTROL_ACK` | `MakeAckPacket`, `get_ReceiveAck`, `set_ReceiveAck`, `ackPacket`, `APERIODIC_USR_DATA_ACK`, `PERIODIC_USR_DATA_ACK`, `USR_CONTROL_ACK` | ACK handling is present in both gateway and simulator artifacts, but matching fields are not proven. |
| Packet container | `PacketContainer`, `PacketDataBlock`, `SetContainerFromPacket`, `SetDataBlockFromPacket`, `MakePacket`, `get_RawPacket`, `get_Header`, `get_DataBlock` | `PacketContainer`, `PacketDataBlock`, `SetContainerFromPacket`, `SetDataBlockFromPacket`, `MakePacket`, `MakeErrorPacket`, `get_RawPacket`, `get_Header`, `get_DataBlock` | Packet assembly and parse-from-packet names align with the Protocol DOCX structure. |
| CRC fields | `CRC32Calc`, `get_CrcOfHeader`, `get_CrcOfDataBlock`, `headerCrc32`, `dataCrc32`, `HEADER_CRC32_HEADER`, `HEADER_CRC32_OF_DATABLOCK` | `CRC32Calc`, `get_CrcOfHeader`, `get_CrcOfDataBlock`, `headerCrc32`, `dataCrc32`, `CRC32_OF_DATABLOCK_DUMMY` | CRC calculation and field names exist, but profile parameters and vectors are still absent. |
| Correlation candidates | `get_TypeOfData`, `set_TypeOfData`, `get_SizeOfDataBlock`, `set_SizeOfDataBlock`, `get_LPNET_LastSequenceNumber`, `get_PacketTime` | `get_TypeOfData`, `set_TypeOfData`, `get_SizeOfDataBlock`, `set_SizeOfDataBlock`, `get_LPNET_LastSequenceNumber`, `packetTimeOffset` | Candidate correlation fields are visible, but the exact ACK match rule is not confirmed. |
| Session flow | `SessionOpen`, `SessionClose`, `SessionOpenCommand`, `SessionCloseCommand`, `get_IsSessionOpen`, `GetSessionStatus` | `SessionOpen`, `SessionClose`, `SessionCloseGw1Init`, `SessionCloseGw2Init`, `SessionCloseGw3Init`, per-channel session status names | Session behavior is clearly modeled, but the source authority for state transitions remains owner-reviewed. |
| Retry/ACK-wait queue | `ForAckWait`, `get_SendLPN*PacketQueueCount`, `get_ReceiveLPNPacketQueueCount`, `LPNET_DefWaitAnswer`, `LPNET_LoseLinkResponseTime` | `ForAckWait`, per-gateway send/receive packet queues, `LPNET_DefWaitAnswer`, `LPNET_LoseLinkResponseTime` | ACK-wait and link-loss setting labels exist, but actual timing/retry values remain external and unapproved. |
| Trace/log boundary | `InsertPacketDBLogQueue`, `CommLogContainer`, `packetTime`, `CommTime` | minimal signal | Gateway/log artifacts can inform later trace schema review, not M1 protocol authority. |

Owner question set for `DEC-PROTO-002`:

| Question ID | Question | Evidence basis | Needed owner answer |
| --- | --- | --- | --- |
| `Q-ACK-001` | Does ACK matching use `TypeOfData`, `SequenceNumber`, both, or additional fields? | Symbol groups expose `MakeAckPacket`, `ReceiveAck`, `TypeOfData`, `LPNET_LastSequenceNumber`, and packet time labels. | Confirm exact ACK correlation field set. |
| `Q-ACK-002` | Does an ACK packet copy the request sequence field or generate a new one? | ACK construction and sequence labels appear together, but string review cannot prove assignment behavior. | Confirm sequence handling for ACK packets. |
| `Q-ACK-003` | Are ACK packets always header-only, and if so how are data block size and CRC fields populated? | Protocol DOCX says ACK is header-oriented; symbols show `SizeOfDataBlock`, `CrcOfDataBlock`, and ACK construction names. | Confirm ACK packet layout and CRC field handling. |
| `Q-ACK-004` | Are ACK categories one-to-one for all command/signal packet types, including session and periodic/aperiodic packets? | Symbols show `APERIODIC_USR_DATA_ACK`, `PERIODIC_USR_DATA_ACK`, and `USR_CONTROL_ACK`; protocol tables also list ACK pairs. | Confirm complete ACK mapping and exceptions. |

Owner question set for `DEC-PROTO-003`:

| Question ID | Question | Evidence basis | Needed owner answer |
| --- | --- | --- | --- |
| `Q-CRC-001` | What exact CRC32 profile is used: polynomial, initial value, final xor, reflect input, and reflect output? | Symbols show `CRC32Calc` and CRC field names only. | Provide source-backed CRC profile. |
| `Q-CRC-002` | What byte range is used for header CRC? | Protocol DOCX says header CRC excludes itself; symbols show `HEADER_CRC32_HEADER` and `get_CrcOfHeader`. | Confirm exact covered bytes and byte order. |
| `Q-CRC-003` | What byte range is used for data block CRC, especially when zero or multiple data blocks exist? | Symbols show `CrcOfDataBlock`, `CRC32_OF_DATABLOCK_DUMMY`, `SizeOfDataBlock`, and `PacketDataBlock`. | Confirm data block CRC coverage and dummy/empty behavior. |
| `Q-CRC-004` | Can owner provide at least one request packet and expected header/data CRC pair as an independent test vector? | No reviewed document or static symbol pass produced a test vector. | Provide independent CRC vector before implementation is treated as verified. |

Owner question set for `DEC-RETRY-001` and `DEC-TIME-001`:

| Question ID | Question | Evidence basis | Needed owner answer |
| --- | --- | --- | --- |
| `Q-RETRY-001` | What timeout starts ACK retry handling? | Symbols show ACK-wait queues and `LPNET_DefWaitAnswer`. | Confirm approved timeout source and value outside Git. |
| `Q-RETRY-002` | What condition transitions from retry to link-loss/offline handling? | Symbols show `LPNET_LoseLinkResponseTime` and last received packet time labels. | Confirm approved link-loss rule and source. |
| `Q-RETRY-003` | Does retry reuse the same raw packet and sequence number, or rebuild a packet with updated fields? | Symbols show raw packet, queue, sequence, and retry labels, but no behavior proof. | Confirm retry packet mutation rule. |

Implementation planning impact:

- The observed names support modeling M1 around independent packet container, packet data block, CRC interface, ACK matcher, session state, and retry queue concepts.
- They do not authorize implementation values, CRC settings, ACK matching rules, retry timing, or expected outputs.
- If M1 proceeds before `DEC-PROTO-003` closes, CRC must stay behind a placeholder or injectable interface and tests must not claim CRC correctness.
- If M1 proceeds before `DEC-PROTO-002` closes, ACK matching must stay configurable or explicitly blocked by tests rather than inferred from symbols.
- The legacy artifacts suggest C#/.NET heritage, but M1 language selection remains `DEC-DEV-001` and is not closed by this review.

Next useful owner-provided evidence:

| Priority | Evidence needed | Why it matters |
| --- | --- | --- |
| P0 | CRC profile and at least one independent packet/CRC vector | Only path to close `DEC-PROTO-003` without guessing. |
| P0 | ACK correlation rule and ACK packet field population rule | Only path to close `DEC-PROTO-002` without guessing. |
| P0 | Owner decision on whether PDB observations may guide architecture only or also implementation behavior | Prevents treating legacy symbols as authority. |
| P1 | Legacy source code package, if available | Would allow source-level review instead of symbol inference, still requiring owner authority. |
| P1 | Sanitized packet/ACK hex examples | Would cross-check packet layout, CRC, and ACK behavior without actual endpoints or logs. |

## RSID CRC/ACK Focus Static Recheck - 2026-06-28

This pass rechecked the owner-supplied `RSID_PROGRAM` package for CRC, ACK, retry, and timing confirmation candidates. It remains read-only static inspection. No executable, DLL, PDB, simulator, database tool, controller, network path, or external service was executed, loaded, debugged, decompiled, or modified.

Review boundary:

- Scope was limited to file identity metadata, SHA-256, printable strings, and symbol-like tokens.
- The search deliberately excluded raw PDB paths, local absolute paths, endpoint/config values, credential-like strings, DB rows, catalog rows, and tag rows.
- The result is implementation observation only. It does not close `DEC-PROTO-002`, `DEC-PROTO-003`, `DEC-RETRY-001`, `DEC-TIME-001`, or any source row.

Located target files:

| Alias | Size | SHA-256 | Static review role |
| --- | ---: | --- | --- |
| `RSID_PROGRAM/35_K117-00-LCC-IFD-CD-001(RSID GATEWAY)/RSIDGW/RSIDGW.pdb` | 652800 | `6079a5de9280fcc1593cdadc623fe66dd7555cb8855950c903f3ac01860daabd` | Gateway-side symbol metadata for CRC, ACK, packet container, retry, and timing names. |
| `RSID_PROGRAM/36_K117-00-LCC-IFD-CD-002(RSID SIMULATOR)/RSIDSIM/RSIDSIM.pdb` | 368128 | `6ebeb32485dcc5d2dd4d7035d8706e602516f4d680576e11952b0302eaa23ff6` | Simulator-side symbol metadata for packet assembly, ACK construction, CRC fields, and timing names. |
| `RSID_PROGRAM/35_K117-00-LCC-IFD-CD-001(RSID GATEWAY)/RSIDGW/CommLib.dll` | 8704 | `ef56b60aca2b9a27b588ac9a3ed823b21a1c6f0ea646159fec49521dfa079bb8` | Shared communication library candidate; not loaded. |
| `RSID_PROGRAM/36_K117-00-LCC-IFD-CD-002(RSID SIMULATOR)/RSIDSIM/CommLib.dll` | 7680 | `8abfda487b58a11181c430cca307299746e60a17854602eda9c8a6bf365e12a4` | Simulator communication library candidate; not loaded. |
| `RSID_PROGRAM/35_K117-00-LCC-IFD-CD-001(RSID GATEWAY)/RSIDGW/RSIDGW.exe` | 982016 | `685e0f2f9064b1d840002ede269f68efd96608dba00cfd9493c55724d8cdc962` | Gateway runtime string confirmation; not executed. |
| `RSID_PROGRAM/36_K117-00-LCC-IFD-CD-002(RSID SIMULATOR)/RSIDSIM/RSIDSIM.exe` | 225280 | `18449f05a5c4d63c069762a7835237228f882538238cc78d9eff1409b8315493` | Simulator runtime string confirmation; not executed. |

Focused CRC findings:

| Evidence class | Observed tokens | Interpretation |
| --- | --- | --- |
| CRC helper class names | `RSIDGW.HelperClasses.Crc32`, `RSIDSIM.HelperClasses.Crc32` | Gateway and simulator artifacts both expose a CRC helper class name. This supports a shared implementation concept but not its numeric profile. |
| CRC calculation labels | `CRC32Calc`, `Crc32`, `_crc32`, `m_checksumTable`, `checksumRegister`, `crcByte`, `packetCrc` | Executable and PDB strings expose calculation/table/register-style names. They do not reveal polynomial/init/xor/reflection settings by themselves. |
| Header/data CRC fields | `get_CrcOfHeader`, `set_CrcOfHeader`, `get_CrcOfDataBlock`, `set_CrcOfDataBlock`, `headerCrc32`, `dataCrc32` | Field and property names align with the Protocol DOCX header/data CRC fields. |
| Header/data CRC constants | `HEADER_CRC32_HEADER`, `HEADER_CRC32_OF_DATABLOCK`, `CRC32_OF_DATABLOCK_DUMMY` | Runtime strings reinforce header CRC, data block CRC, and dummy/no-data-block handling concepts. Exact byte ranges are still not proven. |
| CRC profile-specific terms | none found among focused printable terms for polynomial, reflect/refin/refout, xorout, named CRC variants, or common polynomial literals | `DEC-PROTO-003` remains Open. The static string pass did not expose a source-backed CRC profile or independent test vector. |

Focused ACK findings:

| Evidence class | Observed tokens | Interpretation |
| --- | --- | --- |
| ACK construction | `MakeAckPacket`, `ackPacket`, `get_ReceiveAck`, `set_ReceiveAck` | ACK packet construction and ACK receipt state are visible in gateway and simulator artifacts. |
| Packet assembly/parsing | `MakePacket`, `MakeErrorPacket`, `SetContainerFromPacket`, `SetDataBlockFromPacket`, `PacketContainer`, `PacketDataBlock`, `get_RawPacket` | Packet container construction and parse-from-packet concepts align with the Protocol DOCX structure. |
| Correlation candidate fields | `get_TypeOfData`, `set_TypeOfData`, `get_SizeOfDataBlock`, `set_SizeOfDataBlock`, `get_LPNET_LastSequenceNumber`, `set_LPNET_LastSequenceNumber`, `get_PacketTime`, `packetTimeOffset` | Candidate fields for ACK matching are visible, but exact matching rule and assignment behavior are not proven. |
| ACK-wait/retry timing labels | `get_LPNET_DefWaitAnswer`, `set_LPNET_DefWaitAnswer`, `get_LPNET_LoseLinkResponseTime`, `set_LPNET_LoseLinkResponseTime`, `ForAckWait`, `WaitAnswerTime` | Retry and link-loss timing concepts are visible, but approved values and M1 inclusion remain owner decisions. |

Timing/config source identity candidates:

| Candidate family | Observed count | Interpretation |
| --- | ---: | --- |
| `RSID_PROGRAM/.../GatewaySetting.xml` variants | 15 | Multiple gateway, simulator, log, and variant configuration identities exist. Exact timing/config authority remains an owner selection. |
| `RSID_PROGRAM/.../RSIDGW.exe.config` | 1 | Runtime config identity candidate; values were not inspected or recorded. |
| `RSID_PROGRAM/.../RSIDSIM.exe.config` | 1 | Simulator runtime config identity candidate; values were not inspected or recorded. |

Updated interpretation:

- The RSID program package confirms that CRC, ACK construction, packet container, retry, and timing concepts exist in deployed legacy artifacts.
- The package does not contain source-like project files in the reviewed tree, so the pass cannot verify implementation statements at source level.
- Printable symbol metadata did not expose CRC polynomial, initial value, final xor, reflect input/output, named variant, or independent test vector.
- `m_checksumTable` and `checksumRegister` indicate a table/register-style CRC implementation exists, but they are not enough to identify a standard CRC profile without source code or vectors.
- ACK construction is visible, but static strings do not prove whether ACK matching uses packet type, sequence number, packet time, size, or a combination.
- Header/data CRC field names and `CRC32_OF_DATABLOCK_DUMMY` strengthen the need for owner answers on header-only and zero-data-block behavior.

Decision impact:

- `DEC-PROTO-002` remains Open. ACK matching and ACK packet field population must be confirmed by owner-reviewed source, source code, or sanitized packet examples.
- `DEC-PROTO-003` remains Open. CRC must stay placeholder/injectable until a source-backed profile and independent vector exist.
- `DEC-RETRY-001` remains Open. Retry/link-loss labels exist, but timing values and retry mutation behavior remain unapproved.
- `DEC-TIME-001` remains Open. Config identity candidates exist, but actual timing values remain external and not recorded.
- `SRC-TIME-001` still requires owner-selected exact alias, revision, SHA-256, owner, and review state.

Owner action:

- Provide legacy source code if source-level CRC implementation review is intended.
- Provide at least one sanitized packet example with expected header CRC and data CRC if source code is unavailable.
- Confirm whether `CRC32_OF_DATABLOCK_DUMMY` represents a zero-data-block placeholder, detail type behavior, or another source-backed rule.
- Confirm ACK correlation fields and whether ACK packets copy request sequence fields.
- Select the exact `GatewaySetting.xml` or runtime config alias for timing/config authority without recording actual values.

## Targeted External Document Candidate Review - 2026-06-26

This owner-requested pass narrowed review to two external document roots supplied by the owner. The roots are recorded only by aliases:

- `RSID_DOC_SET`
- `IFF_PRELIM_PDF`

Review boundary:

- File inventory used filename, extension, size, SHA-256, page count, and aggregate keyword-category counts only.
- PDF text extraction was used for keyword categories; extracted text, snippets, endpoint values, credentials, configuration values, catalog rows, and DB rows were not recorded.
- No actual absolute external path is recorded.
- No source file was copied into this repository.
- These observations do not update source registers, decision registers, acceptance traces, or M1 readiness state.

Inventory summary:

| Root alias | Observed document set |
| --- | --- |
| `RSID_DOC_SET` | 1 DOCX, 10 PDF files, and 1 TXT file were observed. |
| `IFF_PRELIM_PDF` | 239 PDF files were observed. |

Focused PDF review summary:

| Root alias | Reviewed scope | Result |
| --- | --- | --- |
| `RSID_DOC_SET` | 10 PDF files matching RSID, DD, PC, PCI, TestView, and WBS names | Reinforces previously recorded SAT/DD/AT/manual context. No reviewed PDF produced CRC vector evidence. ACK/procedure/context evidence remains supporting only. |
| `IFF_PRELIM_PDF` | 17 PDFs matching protocol, N3F interface equipment, N3F/N3G SDS, N3G simulator, N3B network, and related REQ/CFG/HDS/LAY candidates | Contains interface/protocol context and several raw CRC/ACK/packet keyword signals. No reviewed PDF produced CRC vector evidence. |

High-signal IFF candidates:

| Candidate alias | Size | SHA-256 | Pages | CRC general | CRC profile-like | CRC vector | ACK | ACK/correlation | Retry/timing | Packet structure | Interpretation |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `IFF_PRELIM_PDF/protocol_improvement_RevA_IFI.pdf` | 782245 | `F63548F386D818E73C8511576910B4687DA62753A56F875AA5794E60CD6E8BBA` | 21 | 4 | 2 | 0 | 11 | 19 | 22 | 37 | Best current IFF protocol-context candidate, but not K117 RSID authority by itself. |
| `IFF_PRELIM_PDF/N3FP.03.00-EG-REQ_Rev1_interface_equipment_requirements.pdf` | 1194538 | `1C4953D4BDB500E13C9DE0D11C0DF7CAFBA02B154012D4BEDFE92BC97082B14F` | 46 | 1 | 6 | 0 | 7 | 4 | 26 | 45 | Strong N3F interface-equipment requirements context. Requires owner relevance decision before use. |
| `IFF_PRELIM_PDF/N3FP.03.00-EG-REQ_Rev0_interface_equipment_requirements.pdf` | 1188643 | `90012D62DCD47D6CE6308DB32918DF93281CE2E15160ACB92561BCDC979F7009` | 46 | 1 | 6 | 0 | 7 | 4 | 21 | 45 | Same document family as Rev1; owner must choose revision if relevant. |
| `IFF_PRELIM_PDF/N3GP.03.00-EG-SDS_Rev0_scenario_simulator_SDS.pdf` | 732681 | `6541856CB5288A4FFAC4B0377BF71597302E351333807B380DB411E109536275` | 18 | 1 | 2 | 0 | 1 | 0 | 4 | 2 | Simulator software design context only. |
| `IFF_PRELIM_PDF/N3FP.05.00-EG-SDS_Rev0_data_processing_acceleration_SDS.pdf` | 761452 | `E6DD48652BC6FA67A8356BEEB0A6AFEB9010359B34821EB871A26C67960DADF0` | 23 | 0 | 4 | 0 | 0 | 0 | 15 | 7 | Data-processing software design context only. |
| `IFF_PRELIM_PDF/N30P.00.00-EG-SDS_Rev1_common_control_logic_SDS.pdf` | 598012 | `97EAF4D5B59BDA3E85F91DC49818C65BB5A3512404CC85BC15D6BDBDDFFE0366` | 18 | 0 | 4 | 0 | 3 | 0 | 0 | 0 | Common software design context only. |

RSID PDF recheck observations:

- `RSID_DOC_SET` PDFs were consistent with prior notes: SAT, DD, and AT strengthen ACK/procedure/interface context but do not close CRC or ACK decisions.
- `RSID_DOC_SET` PCI and TestView manuals are hardware/software tool context; they are not packet protocol authority.
- No reviewed RSID PDF had CRC vector category hits.
- Protocol DOCX remains the strongest current packet-structure authority candidate; this pass did not replace it.

IFF interpretation:

- IFF candidates may be useful for `SRC-N3F-001`, `SRC-N3G-001`, or later target-interface context if the owner confirms relevance.
- IFF documents do not automatically supersede the K117 RSID protocol source baseline.
- Raw `CRC profile-like` hits may include generic words such as initialization or profile-related text; they are not proof of a CRC profile.
- Because `CRC vector` count was 0 in the targeted IFF review, `DEC-PROTO-003` remains Open.
- Because ACK/correlation hits are aggregate keyword signals and do not identify a confirmed matching field set, `DEC-PROTO-002` remains Open.

Owner action:

- Decide whether IFF preliminary PDFs are in scope for M1 source baseline, N3F/N3G target context, or later-phase reference only.
- If in scope, select exact reviewed aliases and revisions before any source register update.
- Provide independent CRC profile and test vector authority separately; do not infer CRC settings from IFF keyword counts.
- Confirm ACK correlation rule separately; do not infer it from aggregate ACK keyword counts.

## Review Closure - 2026-06-26

This closes the current Codex-led targeted source review pass for M1 pre-entry. It does not close decisions, approve sources, or permit M1 Protocol Core implementation.

Closure basis:

- The owner supplied two external document folders after the RSID static dry-run; targeted document candidate review is recorded above as provisional source-review context only.
- The owner explicitly requested RSID static inspection after the document review closure; the dry-run is recorded above as legacy implementation observation only.
- P0 source candidates have been reviewed to the point where further progress requires owner selection or owner-supplied authority rather than additional Codex inference.
- P1 and P2 materials are documented as supporting or deferred evidence and are not required for Codex to continue autonomous M1 pre-entry source review.
- Actual source files remain external and were not copied into this repository.
- Actual endpoint, IP, port, credential, configuration, catalog row, DB row, and runtime value material is not recorded in this repository.
- `references/source_register.csv` and `references/decision_register.csv` remain unchanged by this note.

Ready for owner review:

| Handoff item | Current evidence state | Owner decision needed |
| --- | --- | --- |
| `SRC-PROTO-001` | Protocol DOCX candidate metadata and packet-structure observations are recorded. | Owner-approved 2026-06-28. |
| `SRC-K117-001` | K117 AT scoped catalog-shape evidence is recorded without catalog row values. | Owner-approved 2026-06-28. |
| `SRC-TIME-001` | GatewaySetting and runtime config categories are recorded without actual values. | Owner-approved `RSID_PROGRAM/RSIDGW/GatewaySetting.xml` as source identity on 2026-06-28; actual values remain external and deferred. |
| `SRC-NA-001` | TEACS/NetArrays metadata candidates are recorded without executing NetArrays. | Deferred to M2+ and no longer a direct M1 readiness blocker. |
| `DEC-DEV-001` | DD and SAT evidence can inform boundaries but do not choose runtime. | Approve implementation runtime and language before M1 starts. |
| `DEC-STORAGE-001` | Storage boundary policy exists; external root approval remains outside this note. | Approve the non-repository storage location class. |
| `DEC-REPO-001` | Desktop worktree retention is the working direction; parent Git risk remains recorded. | Approve nested repository disposition. |
| `DEC-PROTO-002` | ACK pair/procedure evidence exists, but correlation fields are not confirmed. | Confirm ACK correlation rule or keep M1 blocked. |
| `DEC-PROTO-003` | CRC fields are observed, but profile and vectors are not confirmed. | Provide CRC profile and independent test vectors or keep CRC implementation deferred. |
| `DEC-RETRY-001` | Retransmission behavior exists as provisional evidence; parameter values are not promoted. | Confirm retry and link-off parameters from owner-reviewed authority. |
| `DEC-TIME-001` | Timing category evidence exists; actual timing values are not promoted. | Confirm timing authority and approved operating values outside this repository. |

No further Codex-led source review is planned before owner review unless the owner explicitly asks for one of these scoped follow-ups:

| Follow-up | Trigger |
| --- | --- |
| Operator Instruction PDF targeted review | Needed only if owner wants additional operational workflow context for `DEC-LOG-001` or `DEC-TAG-001`. |
| TEACS/NetArrays deep metadata review | Needed only if owner cannot select `SRC-NA-001` from the current metadata candidates. |
| Historian/alarm XLSX review | Needed only if owner wants supporting validation or log context. |
| WBS/system breakdown review | Needed only if owner wants additional system-scope context. |
| External-root source-review recheck | Needed when `LOXFS_CMD_SIG_LOCAL_ROOT` points to an owner-approved external artifact root. |

Review closure status:

- `observed_in_session`
- `owner_review_required`

## IFIX and Maintenance Folder Recon - 2026-06-26

This is an owner-requested follow-up after the targeted source review closure. It records only alias-based inventory and relevance assessment. It does not copy, execute, launch, or approve any source.

Safety boundary:

- Root aliases used: `IFIX` and `MAINTENANCE_NOTES`.
- Read-only metadata and keyword-count scans were performed.
- No iFIX runtime, NetArrays runtime, RSID runtime, controller connection, network probe, or package installation was performed.
- No actual absolute path, endpoint value, credential, configuration value, tag row value, catalog row value, or DB row value is recorded.
- File names, sizes, SHA-256 hashes, extension counts, and aggregate keyword counts are treated as provisional inventory metadata only.

Inventory summary:

| Root alias | Directory count | File count | Total bytes | Dominant file classes | Initial relevance |
| --- | ---: | ---: | ---: | --- | --- |
| `IFIX` | 49 | 1764 | 471733505 | iFIX picture/event/log/tag/config-like files plus office/archive/binary artifacts | Strong later-phase iFIX/SCADA/tag/log context candidate. |
| `MAINTENANCE_NOTES` | 184 | 1500 | 252682538 | Markdown notes, CSV evidence registers, images, DOCX/PDF references | Strong LOXFS/NetArrays/CMD_SIG review-context candidate. |

IFIX aggregate observations:

| Category | Count |
| --- | ---: |
| RSID/Gateway filename signals | 1 |
| command/signal/protocol filename signals | 168 |
| iFIX/SCADA/tag/alarm/historian filename signals | 1764 |
| log/event/trend filename signals | 274 |
| config-like extension candidates | 57 |
| Office/PDF candidates | 44 |

High-signal IFIX aliases:

| Candidate alias | Size | SHA-256 | Interpretation |
| --- | ---: | --- | --- |
| `IFIX/iFIX_recommended_set_2026-03-13/PIC/Backup/K117_G_CP40_LeaderCommandAck.grf` | 557568 | `5b4e8f0874f63dfdbb7957ea4385acc888e7f183c8f0fdca763b56246e75988a` | iFIX screen-level command/ACK context candidate. |
| `IFIX/iFIX_recommended_set_2026-03-13/PIC/K117_O_CP40_LeaderCommandAck.grf` | 403968 | `bbaf1acde8718d91f520ec03f8a4ee8c227e61a79b328b693d1fad8843f09b8d` | iFIX screen-level command/ACK context candidate. |
| `IFIX/iFIX_recommended_set_2026-03-13/PIC/Backup/K117_O_CP41_ReportLeaderAck.grf` | 443392 | `63be33afd387c7c6cd7c83f38a3d250120a60117277d8dbd3133a2033284a5c7` | iFIX report/ACK context candidate. |
| `IFIX/iFIX_recommended_set_2026-03-13/PIC/K117_O_CP41_ReportLeaderAck.grf` | 438272 | `d5c1401970d66a95d0811699dfb6a471ca573fc15dee64bdf02897015a46e937` | iFIX report/ACK context candidate. |
| `IFIX/iFIX_recommended_set_2026-03-13/PIC/Backup/K117_O_XP47_ONSlog.grf` | 31744 | `be8d60c448b9a936f8a6dac27da95052efa7b94fb8472500bc9e4f5e9781b41f` | iFIX log-view context candidate. |
| `IFIX/iFIX_recommended_set_2026-03-13/PIC/K117_O_XP47_MSGlog.grf` | 29184 | `0ff59b8e7de7f992f27eb8e6674c667f41640768bdef3107da949e13b5851a7d` | iFIX message-log context candidate. |
| `IFIX/raw/iFIX_recommended_set_2026-03-13.zip` | 158324631 | `49cf8b9df04cd2a19fba8ae1de338840f2b48e18b0a8ff54e33490941574e338` | Raw packaged source candidate that must remain outside Git. |

MAINTENANCE_NOTES aggregate observations:

| Category | Count |
| --- | ---: |
| Text files with keyword hits | 804 |
| Filename/path keyword hits | 1500 |
| Markdown files | 675 |
| CSV files | 121 |
| PDF files | 70 |
| DOCX files | 187 |

High-signal MAINTENANCE_NOTES aliases:

| Candidate alias | Size | SHA-256 | Interpretation |
| --- | ---: | --- | --- |
| `MAINTENANCE_NOTES/60_ProgramReview/LOXFS/NetArrays/K1173_LOXFS_AFC5X_NETARRAY875/40_PB_Review/100_CMD_SIG_Tag_Raw_Evidence.csv` | 1832553 | `b783690aee896f67c3ca31c14ab336159812c97aa69866fdd5e2ebbd7c22b075` | Strong tag evidence candidate for later CMD/SIG tag mapping review. |
| `MAINTENANCE_NOTES/60_ProgramReview/LOXFS/NetArrays/K1173_LOXFS_AFC5X_NETARRAY875/40_PB_Review/108_Stop_Reset_Initial_Tag_Evidence.csv` | 1757596 | `8e01f2e5c92b66a98d4022bbc7d2276f7ecab0a03a1899bef7b4eed706c63e8b` | Strong stop/reset/initial tag evidence candidate. |
| `MAINTENANCE_NOTES/60_ProgramReview/LOXFS/NetArrays/K1173_LOXFS_AFC5X_NETARRAY875/10_Global_Extraction/26_Valve_Tag_Object_Raw.csv` | 1369716 | `333cab8ffaba3a78943afe87da4c84c5c23d76e7c242ec9e465cebe979b4f962` | Raw valve/tag object context candidate; not suitable for Git copy. |
| `MAINTENANCE_NOTES/60_ProgramReview/LOXFS/NetArrays/K1173_LOXFS_AFC5X_NETARRAY875/40_PB_Review/127_P0_Execution_Comparison_Review_Register.csv` | 4116881 | `dd410ea73aeffd42ea7c2b03244b86a5b31edd899364c2d0ebd474008859a95c` | Existing review register candidate for execution-comparison context. |
| `MAINTENANCE_NOTES/60_ProgramReview/LOXFS/NetArrays/K1173_LOXFS_AFC5X_NETARRAY875/40_PB_Review/139_P0_Shared_Variable_Dependency_Register.csv` | 1695589 | `ec5ff777d6451a62e99119065a4239d35fe24541369209e5573fa514c656dd84` | Shared-variable dependency context candidate. |
| `MAINTENANCE_NOTES/60_ProgramReview/LOXFS/NetArrays/K1173_LOXFS_AFC5X_NETARRAY875/40_PB_Review/138_P0_Logic_Coverage_Matrix.csv` | 1314087 | `8090eace759830aabbe07df0f8219ceee175d59197113b0c2c0b07f07af52765` | Logic coverage context candidate. |
| `MAINTENANCE_NOTES/60_ProgramReview/LOXFS/NetArrays/K1173_LOXFS_AFC5X_NETARRAY875/40_PB_Review/105_CMD_SIG_Void_Interface_Evidence_Register.csv` | 155471 | `0806391800deb6c2298717141680a724a1aa35bdfa9bfe8f8534f6866231ca0d` | CMD/SIG interface evidence candidate. |
| `MAINTENANCE_NOTES/60_ProgramReview/LOXFS/NetArrays/K1173_LOXFS_AFC5X_NETARRAY875/99_Review_Log.md` | 352480 | `6c935b13f7a085b5f91628dc7d27b8101e3a235250e5d281c255605618eb3832` | Existing review log candidate for source-review trace context. |

Interpretation:

- `IFIX` is meaningful, but it is not a clean M1 Protocol Core authority by itself. It is stronger for later iFIX/SCADA/HMI screen behavior, tag mapping, event/log view, and operator-facing ACK context.
- `MAINTENANCE_NOTES` is meaningful and likely more immediately useful as a review index for LOXFS/NetArrays/CMD_SIG tag and logic evidence. It still should be treated as derivative review evidence unless the owner designates exact source aliases as authority.
- Both roots contain actual artifacts that must stay outside Git. They should be linked, if needed, through source-register aliases and SHA-256 only after owner review.
- These observations do not close `DEC-PROTO-002`, `DEC-PROTO-003`, `DEC-TAG-001`, `DEC-LOG-001`, `DEC-STORAGE-001`, or `DEC-REPO-001`.

Recommended use:

| Stage | Recommended use |
| --- | --- |
| M1 pre-entry | Use only as owner-review context. Do not use these roots to start Protocol Core implementation. |
| M1 source baseline | Use only if the owner selects exact aliases as supporting evidence and confirms they are not replacing packet protocol authority. |
| Later tag/log/SCADA work | Strong candidates for `DEC-TAG-001`, `DEC-LOG-001`, and possible `SRC-NA-001` support after sanitization and owner review. |

Owner action:

- Decide whether `IFIX` should be registered as later-phase iFIX/SCADA/tag/log evidence only, or whether any exact alias should support an M1 source baseline decision.
- Decide whether `MAINTENANCE_NOTES` review registers can be used as derivative evidence, and identify which exact aliases are owner-approved.
- Keep raw iFIX packages, pictures, logs, binaries, office files, exports, and screenshots outside Git.
- If any exact file is promoted to a source-register item, provide owner-approved revision, path alias, SHA-256, owner, and review state without recording actual values.

## Maintenance LOXFS Internal Recon - 2026-06-26

This follow-up narrows the `MAINTENANCE_NOTES` review to LOXFS-specific internal content. It is a read-only structural review and does not promote any observed file into an authoritative source.

Scope and safety:

- Root aliases used: `MAINTENANCE_LOXFS`, `MAINTENANCE_LOXFS_NETARRAYS`, `MAINTENANCE_LOXFS_KNOWLEDGE`, and `MAINTENANCE_LOXFS_PROCEDURES`.
- Reviewed metadata: directory structure, extension counts, selected file aliases, sizes, SHA-256 hashes, CSV column names, and Markdown headings.
- Not reviewed or recorded: CSV data rows, tag values, initial values, raw line values, endpoint values, configuration values, screenshots, binary payloads, credentials, or actual absolute paths.
- No NetArrays, iFIX, RSID, controller, simulator, database, or network component was executed.

LOXFS inventory:

| Root alias | Directory count | File count | Total bytes | Interpretation |
| --- | ---: | ---: | ---: | --- |
| `MAINTENANCE_LOXFS` | 32 | 730 | 137455663 | Main LOXFS review tree; almost all content is under NetArrays review. |
| `MAINTENANCE_LOXFS_NETARRAYS` | 30 | 728 | 137455663 | Primary static review package for LOXFS NetArrays materials. |
| `MAINTENANCE_LOXFS_KNOWLEDGE` | 7 | 10 | 1059 | Lightweight index placeholders for future LOXFS knowledge organization. |
| `MAINTENANCE_LOXFS_PROCEDURES` | 0 | 1 | 0 | No substantive procedure content observed in this pass. |

Primary internal structure:

| Alias | Direct files | Recursive files | Recursive bytes | Role |
| --- | ---: | ---: | ---: | --- |
| `MAINTENANCE_LOXFS_NETARRAYS/00_File_Retention_Harness` | 17 | 17 | 106513 | Review retention and reproducibility support. |
| `MAINTENANCE_LOXFS_NETARRAYS/10_Global_Extraction` | 33 | 293 | 79663202 | Global extraction outputs, tag/object maps, signal-chain evidence, and image evidence packs. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review` | 172 | 379 | 56506543 | PB-focused review registers, worksheets, coverage matrices, comparison registers, and image evidence packs. |
| `MAINTENANCE_LOXFS_NETARRAYS/10_Global_Extraction/50_Image_Packs` | 1 | 260 | 77789261 | Screenshot/image evidence pack; actual artifacts must remain outside Git. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/150_Image_Packs` | 1 | 203 | 41224665 | PB visual relation evidence pack; actual artifacts must remain outside Git. |

Extension summary for `MAINTENANCE_LOXFS`:

| Extension | Count | Interpretation |
| --- | ---: | --- |
| `.png` | 422 | Visual evidence packs and screenshots; not suitable for Git. |
| `.md` | 143 | Human-readable review logs, summaries, worksheets, and register companions. |
| `.csv` | 121 | Structured review registers and evidence matrices. |
| `.docx` | 41 | Includes environmental placeholder/office candidates; do not copy into Git. |
| `.py` | 2 | Review support scripts; not executed in this pass. |
| `.json` | 1 | Review metadata/config-like candidate; not interpreted as authority. |

High-signal structured review files:

| Candidate alias | Size | SHA-256 | Observed schema role |
| --- | ---: | --- | --- |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/100_CMD_SIG_Tag_Raw_Evidence.csv` | 1832553 | `b783690aee896f67c3ca31c14ab336159812c97aa69866fdd5e2ebbd7c22b075` | Tag evidence register with source/form/page/tag-role/human-review columns. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/104_CMD_SIG_Tag_Coverage_Audit.csv` | 3191 | `af21ac419c8f70b7729f4adf47a5242b3adc2527501910398899eec16ca21c72` | CMD/SIG tag coverage audit metrics. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/105_CMD_SIG_Void_Interface_Evidence_Register.csv` | 155471 | `0806391800deb6c2298717141680a724a1aa35bdfa9bfe8f8534f6866231ca0d` | Interface evidence register with form, source reference, linked tag, and review-state columns. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/108_Stop_Reset_Initial_Tag_Evidence.csv` | 1757596 | `8e01f2e5c92b66a98d4022bbc7d2276f7ecab0a03a1899bef7b4eed706c63e8b` | Stop/reset/initial tag evidence register. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/111_Interface_Signal_Classification_Audit.csv` | 26053 | `50f7697194f24d67709ca87d4fdf53d498636dfa675ec05c2ad6a0f6b2a1378e` | Interface signal classification audit. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/118_Stop_FlowChart_CMD_SIG_Compare_Worksheet.csv` | 6283 | `6e3a7dc6ec8db9bd3dbc4117bced0445d9112ac609bc2dfd4911f986a6a2c5b5` | Stop flowchart versus CMD/SIG comparison worksheet. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/127_P0_Execution_Comparison_Review_Register.csv` | 4116881 | `dd410ea73aeffd42ea7c2b03244b86a5b31edd899364c2d0ebd474008859a95c` | Execution comparison review register with ordering, match, and follow-up columns. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/138_P0_Logic_Coverage_Matrix.csv` | 1314087 | `8090eace759830aabbe07df0f8219ceee175d59197113b0c2c0b07f07af52765` | Logic coverage matrix with case, trigger, boundary, trace, confidence, and next-action columns. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/139_P0_Shared_Variable_Dependency_Register.csv` | 1695589 | `ec5ff777d6451a62e99119065a4239d35fe24541369209e5573fa514c656dd84` | Shared-variable dependency register with writer/reader/reset/downstream-impact columns. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/142_Current_Logic_Review_Spine_Register.csv` | 1201578 | `a8ad1f55163f8cbf47005f5131d4e7810c565882b50258b5e3ca09008adfbab7` | Current logic review spine and artifact coordination register. |

High-signal Markdown companions:

| Candidate alias | Size | SHA-256 | Heading-level interpretation |
| --- | ---: | --- | --- |
| `MAINTENANCE_LOXFS_NETARRAYS/99_Review_Log.md` | 352480 | `6c935b13f7a085b5f91628dc7d27b8101e3a235250e5d281c255605618eb3832` | Review log with workspace creation and live-target heading markers; content not copied. |
| `MAINTENANCE_LOXFS_NETARRAYS/10_Global_Extraction/27_Valve_Common_Logic_Map.md` | 6514 | `8bbce73fca73af66b32a0188d0eb285153b3840cbea0081035beb9bb590b6239` | Valve common logic map summary and CSV companion. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/139_P0_Shared_Variable_Dependency_Register.md` | 177886 | `96d0a925e48cd4691664ef8cebfaff988f0cb1e606c6ba941c7f40fa8eb645c9` | Shared-variable dependency summary, cluster review, reset-owner linkage, and PB additions. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/118_Stop_FlowChart_CMD_SIG_Compare_Worksheet.md` | 4734 | `1b4f5e6d53656f254480d78899eba866d98961df8f548e41eb500eb74104811b` | STOP flowchart/CMD-SIG comparison worksheet summary and reviewer options. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/104_CMD_SIG_Tag_Coverage_Audit.md` | 1691 | `51154e4a5b232c4cd7d423fffa254d2c22fa8298ded082e6d60fc57a5a6034bb` | CMD/SIG tag coverage audit companion. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/105_CMD_SIG_Void_Interface_Evidence_Register.md` | 1989 | `0451081efa3d5ff85160ee6f0b2713d8d72b5afc71643616e3de4544095a3293` | Void/interface evidence register companion. |
| `MAINTENANCE_LOXFS_NETARRAYS/40_PB_Review/111_Interface_Signal_Classification_Audit.md` | 1386 | `e71afd0fb75bc2ee56b0dc954ffe88bfc99e0fd67929622bbe74ea668c374884` | Interface signal classification rule/audit companion. |

Interpretation:

- This LOXFS folder is a strong pre-existing static-review workspace for NetArrays-derived LOXFS behavior, tag mapping, interface classification, flowchart comparison, logic coverage, and shared-variable dependency review.
- The material is likely more useful for M2+ local scenario/oracle planning, later NetArrays adapter work, `DEC-TAG-001`, and `DEC-LOG-001` than for M1 packet-level protocol implementation.
- The reviewed aliases may help define future synthetic fixtures, review packets, and owner questions, but they should not be used to infer authoritative packet CRC, ACK correlation, timing, retry, or endpoint values.
- `MAINTENANCE_LOXFS_KNOWLEDGE` and `MAINTENANCE_LOXFS_PROCEDURES` did not add substantive source evidence in this pass.

Recommended next use:

| Need | Best LOXFS source-review starting point |
| --- | --- |
| Tag role taxonomy | `100_CMD_SIG_Tag_Raw_Evidence.csv`, `104_CMD_SIG_Tag_Coverage_Audit.csv`, `108_Stop_Reset_Initial_Tag_Evidence.csv` |
| Interface boundary review | `105_CMD_SIG_Void_Interface_Evidence_Register.csv`, `111_Interface_Signal_Classification_Audit.csv` |
| Flowchart versus observed logic comparison | `118_Stop_FlowChart_CMD_SIG_Compare_Worksheet.csv`, `127_P0_Execution_Comparison_Review_Register.csv` |
| Logic coverage and shared state | `138_P0_Logic_Coverage_Matrix.csv`, `139_P0_Shared_Variable_Dependency_Register.csv` |
| Review trace and coordination | `99_Review_Log.md`, `142_Current_Logic_Review_Spine_Register.csv` |

Owner action:

- Decide whether `MAINTENANCE_LOXFS_NETARRAYS` should be treated as derivative review evidence for later phases or as supporting evidence for `SRC-NA-001`.
- Select exact aliases for any future owner review packet instead of importing the entire folder.
- Keep CSV rows, images, DOCX artifacts, and any raw extracted values outside Git.
- Do not use this material to start M1 Protocol Core while M1 readiness remains blocked.

## Open Owner Actions

- No direct M1 readiness owner action remains after `SRC-TIME-001` verification. Protocol-specific behavior decisions remain Open as separate scope controls.
- Review CRC profile and test vector authority separately from observed protocol structure.
- Review ACK correlation, retry, timing, and endpoint/channel decisions without recording actual endpoint or configuration values.

## Safety Receipt

- Actual controller access: not performed.
- Actual network access: not performed.
- NetArrays execution: not performed.
- Legacy RSID binary execution: not performed.
- MariaDB installation or execution: not performed.
- External package installation: not performed.
- User file copy, move, or delete: not performed.
- Actual artifacts copied into Git: not performed.
- Remote creation or push: not performed.
- Automatic commit: not performed.
- M1 Protocol implementation: not performed.
