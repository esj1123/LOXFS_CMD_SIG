# Common Protocol Seed

These CSV files record a Phase 0 protocol skeleton only.

- `header_fields.csv` validates to a 48-byte candidate header layout.
- `data_block_fields.csv` validates to a 10-byte candidate data block layout.
- `packet_types.csv` records packet type and ACK type candidates.
- `session_controls.csv` records session detail candidates.
- `ack_retry_rules.csv` records behavior candidates and Open timing parameters.

Open CRC, reserve, ACK correlation, timeout, retry, and link-off values must not be closed without source-backed review.
