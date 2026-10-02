# v4.7 T08 — Fresh-Agent Self-Dogfood

This directory is the durable T08 dogfood surface for Issue #352 / PR #624. It is subordinate to the Frozen T08 Task Pack and `.agent/execution/T-008/**`; it does not define new semantic owners, lifecycle state, Validation authority, Review authority, merge authority, Version Closure, or Release Qualification.

## Evidence classes

- `STATIC_OR_RECONSTRUCTION`: committed scenario data, deterministic reconstruction, unit tests, mocks, and replay/static examples. These may prove parsing, routing, currentness checks, and non-transfer behavior only.
- `REAL_FRESH_SESSION`: evidence from an actually executed fresh logical Agent/session that starts without hidden task-chat context and resolves current durable repository/GitHub facts through real interfaces.

A `STATIC_OR_RECONSTRUCTION` PASS is never evidence that a real fresh session ran. The Builder session for #352 already has task context and cannot honestly claim `REAL_FRESH_SESSION`; therefore the REAL scenario remains `NOT_RUN/BLOCKED` until the independent exact-subject Validation handoff is executed in a capable fresh logical session.

No artifact here requires or records private chain-of-thought. Observable durable pointers, recovered facts, structured outputs, operator/session identity, commands/results when applicable, and evidence classifications are sufficient.

## Durable starting pointers

A fresh logical session should need only these durable pointers:

1. repository `kaicreator-mm/ai-development-standard`;
2. task Issue #352;
3. PR #624;
4. branch `task/352-v47-fresh-agent-self-dogfood`;
5. Frozen T08 Task Pack `docs/implementation/4.7.0/task-packs/T08_fresh_agent_self_dogfood.md`;
6. Execution Pack `.agent/execution/T-008/MANIFEST.yaml` and its subordinate artifacts;
7. current integration target `version/v4.7.0`.

From those pointers, the session must recover current durable facts rather than inherit chat/history: pinned ADS/current authority, T05/T07 canonical composition inputs, applicable profiles/overrides, current Task/PR/exact HEAD/base, mutation and side-effect authority, Validation/Review requirements, and the next action or blocker.

## Currentness and authority rules

- Live repository/GitHub facts outrank stale chat/history.
- A stale Issue/PR/HEAD/base or mismatched Task/pack identity is `BLOCKED`; do not silently consume or rebase it.
- T05 `references/PROGRESSIVE_DISCLOSURE_ROUTING.md` + `scripts/resolve_standard_read_set.py` remain the read-routing owner inputs.
- T07 `references/V47_SEMANTIC_CONFORMANCE_MATRIX.md` + `scripts/v47_conformance.py` + `scripts/test_v47_semantic_conformance.py` remain the semantic-conformance inputs.
- Same/different user, account, provider, credential, or transport does not by itself prove logical freshness.
- The T08 Builder write set remains exactly `docs/implementation/4.7.0/dogfood/**` and `scripts/test_v47_fresh_agent_dogfood.py`.

## Gate order

1. Builder implementation/evidence.
2. Independent exact-subject T08 Validation on immutable final PR HEAD/tree and then-current expected target/base. REAL fresh-session evidence must actually be REAL.
3. Only after Validation PASS on the unchanged subject: genuinely new high-capability READ-ONLY Fresh Independent Review.
4. Separate Controller live-currentness / expected-head merge authorization.

CI/static test PASS is not independent Validation PASS; Validation PASS is not Fresh Review PASS; T08 PASS is not Version Closure or Release PASS.

`reconstruction.json` is deliberately `STATIC_OR_RECONSTRUCTION`. `VALIDATION_REQUEST.md` defines the external exact-subject binding that must be instantiated after the final Builder HEAD/tree exists.