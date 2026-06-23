# Architecture

This document records intended future components at concept level only. No component listed here is implemented in Phase 0.

## Conceptual Components

- Scenario Runner
- Protocol Encoder/Decoder
- UDP Transport
- Channel Manager
- Session State Machine
- ACK/Retry Manager
- Fault Injector
- Trace Recorder
- Independent Oracle
- Legacy RSID Adapter
- NetArrays Simulator Adapter
- CLI

## Separation Principles

- Protocol encoding and decoding should not depend on transport state.
- Oracle logic should remain independent from the implementation under test.
- Legacy and simulator adapters should be boundary components, not core protocol authority.
