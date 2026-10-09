# Execution Contract Reference Wiring v4.9 (T-008) Reference

v4.9 T-008 wires the references required to carry **Assurance Plan currentness, Role Profile identity and JIT phase / selector-independence-currentness identity** through the existing work-item / execution-pack / dispatch contract surfaces. The one Dispatch/Claim lifecycle of `EXECUTION_ARCHITECTURE_STANDARD.md` section 11 remains the only admission path; this wiring adds no second admission mechanism.

The wiring is additive and backward-compatible: three OPTIONAL reference fields on `schemas/dispatch.schema.json`. No required field, enum, vocabulary, lifecycle or gate semantics changed.

## Field semantics

| Field | Meaning |
|---|---|
| `assurance_currentness_ref` | Identity of the governing Assurance Plan currentness binding (`ASSURANCE_PLAN_STANDARD.md` §12 `currentness_binding`) consumed at the §29.1 architecture-owned transitions of this dispatch (Dispatch reservation, Claim admission, and any other owner-declared transition). |
| `role_profile_ref` | Identity of the Role Execution Profile v1 instance (`schemas/role-execution-profile-v1.schema.json`) feeding the §27.2/§29.4 hard-eligibility predicates for this dispatch. |
| `jit_phase_ref` | Identity of the JIT phase inside the current Task envelope (§29.2 P1–P3 with E1/E2) that this dispatch materializes, including its selector-independence/currentness identity. |

All three fields are typed `["string", "null"]` with `minLength: 1` — the schema's established optional-reference style (`task_pack_ref`, `execution_pack_ref`, `execution_context_requirements_ref`, `dependency_toolchain_profile_ref`). The supported JSON-Schema subset of this repository forbids `$ref`/`definitions`; the fields are plain reference-identity strings and their targets are resolved by consumers against the owning surfaces, never inlined or copied.

The fields are references, not state: a dispatch instance that omits them stays a complete, valid v1 dispatch. Populating a field declares which currentness/identity artifact governs THIS dispatch, so that claim-time recompute (§29.6) has an exact pointer to re-read.

## Claim-time and currentness consistency

- A declared reference is bound at the §29.1 recompute points: Dispatch reservation, Claim admission (section 11 re-read), merge/merge-ready, Candidate Freeze, Release Qualification. The ref is a pointer, not a cache — every transition re-reads the binding from facts; there is no hidden mutable latch.
- All three fields are **resolve-or-fail-closed**: a consumer must resolve each declared reference against its owning surface at claim time or fail that admission closed. A stale or missing reference never becomes a default, never silently narrows an obligation, and never passes currentness.
- A dispatch whose `assurance_currentness_ref` resolves to a binding whose `currentness_binding.state` is `STALE` or `UNKNOWN` MUST NOT authorize Dispatch, Claim, merge or Freeze (§29.1): it routes to deterministic recomputation/rebinding, a stronger legal path, or `BLOCKED`. A transition that proceeded on a plan later shown `STALE`/`UNKNOWN` is re-evaluated at the next recompute point and never ratified retroactively.
- Currentness drift between Dispatch reservation and Claim admission resolves fail-closed under sections 11/11.1/27.3 (§29.6): at most one claim linearizes against still-current predicates; a drifted admission publishes no canonical claim and recomputes or blocks.

## Authority and gate boundaries

The three fields carry identity only. They never duplicate Task scope, Claim authority or gate truth, and they never create, replace or re-define an owner verdict:

- `assurance_currentness_ref` — the currentness verdict stays owned by `ASSURANCE_PLAN_STANDARD.md` §12 (`CURRENT`/`STALE`/`UNKNOWN`). A resolvable ref is not a verdict: `CURRENT -> PASS/READY/state:ready` remains a forbidden inference (registry F13–F16), and the ref creates no Gate PASS, Task scope, Release applicability or finding disposition.
- `role_profile_ref` — the profile instance stays owned by `schemas/role-execution-profile-v1.schema.json` and §29.4: a ref never grants role actions, terminal authority, executor capability or a claim-policy switch, and a profile-blocked candidate is never promoted by priority, cost, latency or provider strength.
- `jit_phase_ref` — phase identity stays owned by the §29.2 predicate: the ref never widens the Task envelope, never changes Task ownership or dependency semantics, and a material topology change is never carried as a phase ref — it routes to v4.3 Task DAG mutation governance.

No dispatch field gained decision authority: `dispatch_state`, `result`, `role`, `execution_profile`, `agent_freedom` keep their exact base vocabulary.

## Backward compatibility

v1 dispatch instances remain valid unchanged, and a v1-only dispatch consumer is not required to change: the candidate schema only adds optional properties to a root whose `additionalProperties` is `true`. Both directions are compatible:

- the candidate parser accepts every v1 instance (nothing new is required);
- the base parser accepts instances that populate the new fields (no unknown-field rejection).

There is no migration, no re-interpretation and no dual vocabulary. See `references/EXECUTION_CONTRACT_REFS_V49_COMPATIBILITY.json` for the v4.2 Compatibility Record.

## Material change declaration

The material change is exactly the additive optional property set `{assurance_currentness_ref, role_profile_ref, jit_phase_ref}` on `schemas/dispatch.schema.json`, declared in `references/EXECUTION_CONTRACT_REFS_V49_COMPATIBILITY.json` `change_operations`. Baseline identity is the dispatch schema blob at `version/v4.9.0@f4fe88542de9d3f5376498e62778e2353391bc57` (`git-blob:4607f6cb4b690bf68137294a9acf5d6ccc49e6bd`); the candidate identity is the dispatch schema blob at this Task's candidate commit. No required list, `allOf` clause, enum or vocabulary changed; executable probes live in `scripts/test_v49_execution_contract_refs.py`.

## Non-goals

This wiring authorizes neither a second lifecycle, a new scheduler, workflow state, a runtime authority store, a second eligibility engine, a generic PASS-equivalence engine, Task-scope duplication, nor registry/manifest adoption wiring. Assurance Plan, Role Profile, phase-predicate and DAG-mutation semantics stay with their existing owners; the dispatch fields only point at them.

## Ownership boundaries

T-008 does not own:

- execution reducer / JIT phase predicate / Dispatch-Claim admission semantics — T-007 and sections 11/28 owners;
- JIT materialization vs Task DAG mutation governance — T-009;
- gate-owned evidence binding / currentness transfer — T-010;
- registry / manifest / adoption wiring for the new fields — T-011;
- the integrated proportional-orchestration conformance suite — T-012.

If any of those surfaces were required to make this wiring appear functional, the Task stops and routes to the owning Task instead of extending T-008 scope.

## Minimal material example

```json
{
  "dispatch_id": "d-v4.9.0-T-012-builder-00000000",
  "repository": "kaicreator-mm/ai-development-standard",
  "version": "4.9.0",
  "task": "T-012",
  "issue": "#731",
  "role": "builder",
  "execution_profile": "LOCAL_BUILDER",
  "branch": "task/v4.9.0-t12-conformance-suite",
  "expected_base_sha": "f4fe88542de9d3f5376498e62778e2353391bc57",
  "pinned_standard_revision": "f4fe88542de9d3f5376498e62778e2353391bc57",
  "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
  "dispatch_state": "READY",
  "task_pack_ref": "docs/implementation/4.9.0/task-packs/T12_conformance_suite.md",
  "assurance_currentness_ref": "assurance-plan:v4.9.0/T-012#/currentness_binding",
  "role_profile_ref": "role-profile:v4.9.0/local-builder-primary",
  "jit_phase_ref": "jit-phase:v4.9.0/T-012#implementation"
}
```
