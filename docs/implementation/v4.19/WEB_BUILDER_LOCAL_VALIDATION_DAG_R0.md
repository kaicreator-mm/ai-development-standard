# WEB_BUILDER / LOCAL_VALIDATION — Task DAG R0

**Target:** ADS v4.19.0  
**Frozen Product:** `44562165d715a347a4ee00c010b8fb6e302530c7`  
**Frozen L2:** `b82f201d02ae9013eb42c3597a8a1768aa63ce4f`  
**Owner bootstrap authority:** ADS #1353 comment 6585163422

## 1. DAG decision

One cross-layer Task is the smallest safe unit. Schema, semantic projection, normative profile inventories and conformance tests are one contract; splitting them would create temporary incompatible writers and intermediate invalid Dispatch contracts.

```text
ADS419-T01-DISPATCH-PROFILES
  depends_on: []
  writes: exact seven-path allowlist
  review: required
  validation: concern + integration
```

| Metric | Frozen value |
|---|---:|
| Task count | 1 |
| Dependency edges | 0 |
| Parallel implementation lanes | 1 |
| Shared central writers | 1 |
| Independent source Review | Required |
| Merge/release authorization | Not granted |

## 2. T01 Task Pack

**Task ID:** `ADS419-T01-DISPATCH-PROFILES`  
**Purpose:** Add `WEB_BUILDER` and `LOCAL_VALIDATION` as additive, role-bound, environment-projected profiles without changing existing authority or dispatch lifecycle.

### Exact allowed_write_set

1. `schemas/dispatch.schema.json`
2. `scripts/v34_rules.py`
3. `standards/EXECUTION_PACK_STANDARD.md`
4. `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`
5. `scripts/test_protocol_schemas.py`
6. `scripts/test_v410_t06b_multi_dispatch_conformance.py`
7. `scripts/test_execution_architecture.py`

No other path may be changed by T01.

### Acceptance

- JSON Schema admits WEB_BUILDER only with builder and LOCAL_VALIDATION only with validator.
- Validator role continues to require requested_head_sha and validation_profile; Builder role continues to require task_pack_ref.
- Semantic projection maps WEB_BUILDER→WEB and LOCAL_VALIDATION→LOCAL.
- Contradictory explicit environment fails closed for both profiles.
- Legacy LOCAL_BUILDER, LOCAL_VALIDATOR, WEB_REVIEWER, PLATFORM_VALIDATOR and CLOSURE_VALIDATOR remain unchanged.
- Unknown profile remains UNKNOWN / rejected at canonical admission.
- Protected claim key is invariant to execution profile/environment for a fixed repository/task/role/compatibility group.
- Builder and Validator remain distinct roles; profile labels add no authority.
- New ordinary implementation work defaults to WEB_BUILDER; LOCAL_BUILDER is retained only for v4.18-pinned history and explicitly grandfathered workflows.
- Local Validation is exact-SHA, validation-only, CI-first and no-source-write.
- No second scheduler, lifecycle, Claim key, queue, event family or automatic handoff is added.

### Required tests

- Extend schema profile enum and role-coupling assertions in `test_protocol_schemas.py`.
- Add positive and negative environment projection tests in `test_v410_t06b_multi_dispatch_conformance.py`.
- Add protected-claim-key invariance tests for profile/environment metadata in `test_execution_architecture.py`.
- Retain all legacy positives and the existing LOCAL_BUILDER+WEB contradiction negative.
- Add negative cases for wrong role, wrong explicit environment, unknown profile and any attempt to infer authority from environment/profile.

### Validation order

1. Read exact branch/base/Task Pack and verify the one-writer allowlist.
2. Exact-tree source syntax preflight: parse the JSON schema and compile all changed Python files before any CI run.
3. Focused schema/projection/claim-key tests.
4. Full ADS test suite and conformance runner.
5. Self-hosted Woodpecker CI on the exact PR HEAD.
6. Required independent source Review on the exact HEAD; repair only in the same bounded Task scope and rerun affected checks on the new SHA.

### Review / risk

- Risk: normative Dispatch/schema and authority-boundary change.
- Review Policy: REQUIRED, independent.
- Validation: concern + integration.
- No release qualification or main merge under this DAG Freeze.

## 3. Execution admission note

The only implementation bootstrap is the explicit one-time Owner authorization in #1353 comment 6585163422. v4.18.0 is immutable; do not emit a false v4.18 WEB_BUILDER Dispatch/Claim. This exception applies only to T01 and its exact write set. After the new profile is implemented and adopted in a published v4.19 revision, ordinary implementation Tasks use the canonical WEB_BUILDER Dispatch and the existing serialized Claim/CAS protocol.
