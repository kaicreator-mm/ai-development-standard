# T-009 Execution Contract

Exact base: `version/v4.8.0@22e8e1701661689fb39a5c363eed424cf827c403`.

This is a test-only conformance concern for the existing Interchange v1 family. Verify duplicate same identity+payload idempotency, conflicting payload/digest fail-closed, lost/replayed/stale delivery handling, ACK/progress non-authority, durable canonical effect materialization, and crash/restart reconstruction from durable facts without queue/chat history.

Allowed paths: `scripts/test_v48_interchange_replay_restart.py` and `fixtures/v48_interchange_replay/**`. No existing schema/protocol/standard mutation. Any additional path requires Controller rebind. Do not introduce a new Exchange lifecycle/family, use delivery chronology as workflow truth, or replace `ai-dev:event:v2`. Builder cannot self-certify Validation or Fresh Review.
