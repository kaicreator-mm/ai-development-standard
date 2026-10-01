# T-009 Review Checklist

- Exact base/candidate currentness verified.
- Only replay/restart focused test/fixture paths plus Execution Pack changed.
- No Interchange schema/protocol/standard mutation.
- Same identity+payload is idempotent; conflicting payload/digest fails closed.
- Lost/replayed/stale cases are deterministic and authority-safe.
- ACK/progress remain correlation-only and non-authoritative.
- Restart reconstructs from durable facts without transient queue/chat history.
- `ai-dev:event:v2` remains writer/admission authority.
- No new Exchange lifecycle/family or delivery chronology authority.
- Independent Validation and genuinely Fresh Review required before merge.
