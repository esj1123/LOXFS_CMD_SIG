# Scenarios

Scenario files are Phase 0 templates only. They do not claim implemented runner support.

Supported fault type candidates for future planning:

- `drop`
- `duplicate`
- `delay`
- `reorder`
- `corrupt`
- `channel_disagreement`
- `session_disconnect`
- `session_reconnect`
- `stop_during_pending`
- `reset_during_pending`

Expected outputs must be produced independently and stored under `scenarios/expected/` when future phases define the oracle contract.
