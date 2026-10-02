# T-008 Execution Contract — Fresh-Agent Self-Dogfood

## Exact authority binding

This pack is subordinate to Frozen T08 and is valid only for the exact integration base `version/v4.7.0@3e9c24b671c5619b6024ec79a90b20f6eb1b9346` (tree `17163c9cfb78f3d2a11b8c713cc27abf627beb07`) on branch `task/352-v47-fresh-agent-self-dogfood`.

Authority inputs:

- Frozen Product: `d4f90e1432b53fe0d30d4673674280f3c5e586ec`
- Frozen L2: `8a0687807e1c5ec7c415b0031862b0e367c44507`
- Frozen Task DAG: `754f76ecd452abb654f9b35fdbb52acd12e9954b`
- T08 Task Pack: `docs/implementation/4.7.0/task-packs/T08_fresh_agent_self_dogfood.md@168acd4acf3e23fbb3ca3f6197e4192cb05a9f50`
- T08 L3: `docs/implementation/4.7.0/L3_REFERENCE_PACKS.md#t08--fresh-agent-self-dogfood@6a2000cf9b8bf8024450eb5f0f0704960140095f`
- dependency completion: `T05@1ab7d5fa6bfc528d2c7ab3dc5dbd905f26fcc4e3`, `T07@3e9c24b671c5619b6024ec79a90b20f6eb1b9346`

At Builder claim time, reread current Issue #352, branch, target, dependency facts, Task Pack/L3 and this pack. If the integration target no longer equals the bound base, an authority identity changed, or the pack/branch does not match, do not silently rebase or rewrite `base_sha`; stop and route to the Controller for explicit currentness classification/rebind.

## Frozen implementation write set

Builder source mutation is limited exactly to:

- `docs/implementation/4.7.0/dogfood/**`
- `scripts/test_v47_fresh_agent_dogfood.py`

`.agent/execution/T-008/**` is Planning-owned pack material and is not part of T08's implementation write set. T08 must not alter Product/L2 authority, T05/T07 owners, registries, global Gate/lifecycle semantics, release/closure authority, or any other source path. GitHub PR/Validation-request workflow side effects are permitted only as the durable gate handoff required by the Task Pack/Issue; they do not widen the repository write set.

## Semantic boundary

T08 owns reproducible fresh logical Agent/session dogfood only. It consumes, and must not redefine:

- T05 fail-closed progressive-disclosure/read-routing semantics, including current durable repository/GitHub authority over stale chat/history;
- T07 unified semantic-conformance rules, including exact-identity non-transfer and the prohibition on promoting mock/static evidence to a higher-fidelity claim.

The dogfood subject must recover from durable repository/GitHub facts: pinned ADS/current authority, canonical owners, applicable profiles/overrides, current Task/PR/exact SHA/base, allowed mutation/side effects, required Validation/Review gates, and next action/blocker. Hidden prior chat/session facts must not be required.

No artifact may require, request, store, or score private chain-of-thought. Observable inputs, structured outputs, durable traces, commands/results when applicable, and explicit evidence classifications are sufficient.

## REAL versus static/reconstruction evidence

`STATIC_OR_RECONSTRUCTION` includes committed fixtures, synthetic transcripts, unit tests, reconstructed payloads, mocks, and replayed/static examples. It may prove deterministic parsing/routing/test logic only. It must never be labeled as proof that a genuinely fresh Agent/session or external runtime actually executed.

`REAL_FRESH_SESSION` requires a genuinely fresh logical Agent/session that starts without hidden task-chat context, receives only durable repository/GitHub pointers needed by the standard, resolves the current live subject through real accessible repository/GitHub/runtime interfaces, and records observable session/operator identity plus recovered exact facts and outcome. Reuse of the same user, account, transport, provider, or credential neither proves nor disproves logical freshness by itself.

If material Frozen acceptance requires `REAL_FRESH_SESSION` and the Builder environment cannot execute it, the Builder may still implement in-scope deterministic support, but the real-session claim remains `NOT_RUN`/`BLOCKED`. The Builder must create a durable exact-subject Validation handoff for a capable independent environment; static/reconstruction PASS cannot clear that blocker.

Any Builder-run REAL scenario is Builder evidence only and does not satisfy independent Validation.

## Exact-subject gates

After implementation is committed, define the immutable subject as the exact Builder HEAD/tree plus the then-current expected integration target/base and T08 Task/pack identities.

Required sequence:

1. Builder implementation/evidence on the Frozen write set; no self-Validation and no self-review.
2. Independent exact-subject T08 Validation on that immutable subject. Required REAL fresh-session evidence must be REAL or remain `NOT_RUN`/`BLOCKED`; CI/static evidence cannot substitute.
3. Only after Validation PASS on the unchanged exact subject, create a genuinely new high-capability READ-ONLY Fresh Independent Review bound to the same exact subject and Validation evidence.
4. Only a separate Controller may perform live currentness/expected-head merge authorization.

Any implementation HEAD/tree change, material target/base change, or relevant authority/currentness drift invalidates transfer of prior Validation/Review evidence and requires a successor exact-subject gate as prescribed by current authority.

T08 grants no Version Closure, Release Qualification, Release PASS, merge, or downstream-task authority.
