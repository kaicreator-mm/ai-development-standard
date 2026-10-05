# Role Execution Profile v1 Reference

`role-execution-profile-v1` is the only new default machine family of v4.9. It is a provider-neutral **normalized projection** of role requirements and source-authority facts. It does not create a second lifecycle, scheduler, claim authority, workflow state, independence authority, or capability owner.

Canonical machine contract: `schemas/role-execution-profile-v1.schema.json`.
Deterministic oracles: `scripts/test_v49_role_execution_profile.py`.
Normative L2 source: `docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md` section 6 (Frozen L2, blob `bd41ea0175b459a6a490fd37ad579e429a58a1c3`).

## 1. What this family is and is not

```text
Role Execution Profile = normalized projection of role requirements + source-authority readout
Agent Capability Profile/Evidence (v4.8) = executor capability claims/evidence — stays external
Claim / Dispatch / eligibility (v4.8)    = admission + lifecycle authority — stays external
Assurance Plan / Task / Gate owners      = independence authority — stays external
MODEL_USAGE_POLICY                       = model-strength routing owner — stays external
provider/model identity                  = provenance/routing context — never authority
```

The profile **summarizes and references**; it never decides. Every normative field is either a bounded vocabulary value or a reference INTO an existing owner surface. There are no role-action grants, no terminal-authority grants, no capability proofs, and no free claim-policy switch in this family.

## 2. Normalized fields

```text
schema_version           const ai-dev/role-execution-profile-v1
role_profile_id          identity of the profile document
role                     kebab-case role label (provider-neutral; no closed authority roster)
profile_version          version of the profile document
source_authority_refs[]  >=1 reference into durable source authorities
source_authority_projection  normalized source-authority readout (see section 3)
allowed_actions[]        free-text role requirements projected FROM source authorities
forbidden_actions[]      free-text role prohibitions projected FROM source authorities
required_evidence_refs[] refs to evidence owners (exact-subject truth stays with owners)
terminal_authority_ref   single ref into the terminal/dispatch owner (never a capability family)
eligibility_predicate_refs[] >=1 ref INTO the v4.8 hard-eligibility owner
independence_requirement_refs[] refs to Assurance Plan/Task/Gate owners
selector_conflict_policy_ref?  ref to the applicable selector/conflict owner
environment_requirement_refs[] refs to environment/toolchain/runner capability owners
mutation_class           READ_ONLY | MUTABLE | AUTHORITY_TRANSITION
claim_policy_ref         single ref deriving from existing v4.8 Claim rules
required_input_refs[]    refs to required input owners
handoff_requirement_refs[] refs to exact-identity/handoff owners
```

An instance with `additionalProperties: false` rejects every injected field, including authority-shaped ones (`granted_role_actions`, `terminal_authority_grant`, `capability_proof`, `provider_authority`, `model_routing_authority`, `claim_switch`, `lifecycle_state`).

## 3. Source-authority projection semantics

`source_authority_projection` is the normalized readout over `source_authority_refs`:

```text
projection_state:
  PROJECTED                          every source resolved, current, and agreeing
  BLOCKED_SOURCE_AUTHORITY_CONFLICT  two or more current sources disagree
  BLOCKED_SOURCE_REF_UNRESOLVED      one or more refs missing or stale
resolution_policy:                   const source-authorities-prevail-never-last-writer-wins
conflict_refs[]                      refs that disagree (must be empty unless the state is the conflict state)
unresolved_refs[]                    refs that are missing/stale (must be empty unless the state is the unresolved state)
```

Fail-closed rules:

1. Source authorities prevail; the profile never overrides them.
2. Two disagreeing authoritative sources produce `BLOCKED_SOURCE_AUTHORITY_CONFLICT` until the owning authority resolves the conflict. The projection outcome MUST be independent of reference order: **no last-writer-wins**.
3. A stale or missing source ref fails closed as `BLOCKED_SOURCE_REF_UNRESOLVED` / `WAITING_LINEAGE` posture. There is no permissive default; a retired or unreadable snapshot never contributes requirements.
4. A document that declares `PROJECTED` while `conflict_refs`/`unresolved_refs` are non-empty is a lying projection: it is schema-invalid and rejected by the resolver.
5. All authority refs use one grammar: `<family>:<path>#<anchor>`. Unknown families, unknown paths, and stale anchors fail closed.

## 4. Owner-reference table (all refs point INTO existing owners)

| Profile field | Owner it references (read-only) | Owner surface |
| --- | --- | --- |
| `eligibility_predicate_refs[]` | v4.8 hard-eligibility owner ("Hard filters before ranking") | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §27.2 |
| `claim_policy_ref` | v4.8 atomic Claim admission rules | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §11; `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §12.1 |
| `terminal_authority_ref` | dispatch-lifecycle/validation terminal owners | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §11 / §7 / §12 |
| `independence_requirement_refs[]` | Assurance Plan / Gate Authority owners | `standards/ASSURANCE_PLAN_STANDARD.md` §9 / §10; `schemas/assurance-plan-v2.schema.json` |
| `selector_conflict_policy_ref?` | selector conflict / Gate Authority owner | `standards/ASSURANCE_PLAN_STANDARD.md` §9 |
| `environment_requirement_refs[]` | runner/toolchain capability owners | `schemas/dependency-toolchain-profile-v1.schema.json`; runner capability owners |
| `required_evidence_refs[]` | exact-subject evidence owners | `schemas/agent-capability-evidence-v1.schema.json` |
| `required_input_refs[]` | Execution Pack / Task requirement owners | `schemas/execution-pack-manifest.schema.json` |
| `handoff_requirement_refs[]` | exact identity / evidence composition owner | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §12 |
| `source_authority_refs[]` | any durable authority that owns a projected requirement | standards/schemas via `ads:` refs; test-only snapshots via `fixture:` refs |

The profile never copies owner inventories. Eligibility predicates **feed** the frozen v4.8 hard-eligibility resolver as additional hard predicates; they are not a second eligibility engine. Claim policy **derives** from the existing Claim rules; there is no `REQUIRED|NOT_REQUIRED|INHERIT` switch in this family.

## 5. Family-boundary oracles

Rejected by contract (schema or deterministic resolver):

```text
Role Profile presence                  -> proves executor capability        (capability stays in v4.8 evidence owner)
Agent Capability Profile instance      -> usable as a Role Profile          (different family, schema rejects)
Agent Capability Profile/Evidence      -> grants role actions/terminal authority
provider/model identity                -> becomes normative role authority  (provenance only; provider swap is authority-inert)
profile-injected authority fields      -> granted role actions / terminal authority / capability proof
free claim switch (NOT_REQUIRED, ...)  -> bypass existing Claim rules       (claim_policy_ref resolves or rejects)
independence refs at MODEL_USAGE_POLICY-> new independence authority        (routing owner, not independence owner)
conflicting source authorities         -> accept the last writer            (BLOCKED, order-independent)
stale/missing source refs              -> permissive defaults               (BLOCKED / WAITING_LINEAGE)
```

## 6. Non-goals

T-004 does not own and this family does not implement:

```text
Authority/Applicability or State registry integration (T-003)
execution reducer, JIT, Dispatch/Claim/merge-time recheck (T-007)
gate-owned evidence transfer/currentness integration (T-010)
central manifest/adoption wiring (T-011)
model-strength routing decisions (MODEL_USAGE_POLICY owner)
executor capability claims/evidence (v4.8 capability family)
```

No second lifecycle: the profile introduces no workflow state, no dispatch/claim state, no lease/lock, no scheduler ownership, and no durable state database. Presence of a profile does not satisfy any Claim predicate by itself; the existing v4.8/v4.9 admission predicates remain the only admission path.

## 7. Compatibility posture (v4.2 governance)

`role-execution-profile-v1` is a new machine family with no closed predecessor; there is no baseline to break. Any future change is evaluated under `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md`: baseline/candidate identity, per-dimension evidence, and explicit compatibility records. "Optional field" or "versioned successor" is never compatible by assertion, and a v1 identity must not silently gain fields.
