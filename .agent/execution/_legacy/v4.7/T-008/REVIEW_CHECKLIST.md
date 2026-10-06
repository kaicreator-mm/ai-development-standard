# T-008 Fresh Independent Review Checklist

This is criteria for the separate Fresh Independent Reviewer. It is **not** a Builder self-review artifact and the Builder must not mark a Fresh Review verdict.

## Review admission

- Exact T08 implementation HEAD and tree are immutable and stated.
- The expected integration target/base and Task Pack/Execution Pack identities are stated and current.
- Independent exact-subject T08 Validation has already posted PASS for that unchanged subject.
- Any Frozen-required `REAL_FRESH_SESSION` claim is backed by actual real fresh logical-session evidence; if REAL is `NOT_RUN`/`BLOCKED`, review cannot convert static evidence into PASS.
- Reviewer is a genuinely new high-capability READ-ONLY logical review context, distinct from Builder and Validator; transport/account identity alone is neither sufficient nor required evidence of independence.

## Scope and authority

- Source diff stays inside exactly `docs/implementation/4.7.0/dogfood/**` and `scripts/test_v47_fresh_agent_dogfood.py`.
- T08 does not rewrite Product/L2, T05 read-routing, T07 semantic conformance, registries, Gate/lifecycle, release/closure semantics, or other canonical owners.
- T05/T07 are consumed as current composition inputs and stale lower-authority chat/history cannot override current durable facts.
- No private chain-of-thought is required; review relies on observable durable evidence.

## Evidence fidelity

- Static fixtures, mocks, reconstructions and unit tests are labeled `STATIC_OR_RECONSTRUCTION` and are not used as REAL-session proof.
- REAL evidence identifies an actually executed fresh logical Agent/session, its observable session/operator reference, durable starting pointers, recovered live exact subject, and outcome/blocker without relying on hidden prior task context.
- Same/different user/account/provider/transport is not treated by itself as proof of freshness.
- Stale Issue/PR/SHA/base is detected rather than silently accepted.

## Gate integrity

- CI/test PASS is not substituted for independent Validation.
- Validation evidence has not been transferred across exact-subject drift.
- Fresh Review occurs only after Validation PASS and is not inherited from another HEAD/session.
- Review verdict does not authorize Version Closure, Release Qualification, Release PASS, or merge by itself.

On any failed item, report the smallest bounded finding against the exact subject; do not repair, merge, or widen T08 from the reviewer role.
