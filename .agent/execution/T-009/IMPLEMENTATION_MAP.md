# T-009 Implementation Map

1. Re-read merged T-003 compatibility conclusion plus existing Interchange v1 schema/protocol/reference.
2. Build deterministic durable-fact fixtures for duplicate, conflict, stale, loss/replay and restart cases.
3. Prove duplicate same identity+payload is idempotent; conflicting payload/digest fails closed.
4. Prove ACK/progress never changes Task/Review/Validation authority.
5. Prove restart reconstruction uses durable facts only and does not depend on transient queue/chat history.
6. Preserve `ai-dev:event:v2` writer/admission semantics and existing owner boundaries.
7. Run focused replay/restart suite plus required repository/protocol regressions.
