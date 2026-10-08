# V410-T07A R1 execution contract — product acceptance / release-blocker evidence wiring

Exact base: `0518202c715dcf91784a694bdf4a8eeeaeb16ab6` (tree `75566c464505386fedffde803e05e3e726922434`), the merged #861 integration tip. Task: #862. Execution environment: LOCAL. Branch: `task/v4.10.0-v410-t07a-product-acceptance-evidence`.
Frozen authorities: Product #837 (PRD v0.4 blob `b0b9906035eee253aad4bff0274d3d4c8f90b9db`), L2 #842, refined DAG #848, Task Pack R1 §V410-T07A (`TASK_PACKS_R1.md` blob `3300f8494ecb2120d96fff520cd09270b538344b`). Direct dependency V410-T06B INTEGRATED at this exact base.

## Goal (Task Pack)

Make PRD §19 evidence obligations / release blockers reconstructible through existing owners: R1/R2/R3/R4/R6/R7/R11/R12 map to durable evidence producers; blockers are visible without redefining Release authority; exact candidate/currentness identity is preserved; historical qualification cannot silently bind to successor; Minimum and Advanced ADS evidence paths remain possible.

risk=high; agent_freedom=F1_BOUNDED_IMPLEMENTATION; validation_scope=concern.

## L3 seed (from #862@6003300393, bound at this JIT)

This pack embeds the repo L3 convention (`Tests → Contract/Invariant → Implementation seam → Failure Handling → References`) rather than emitting a separate L3 file — the same convention the integrated V410-T06B six-core pack uses (`l3_inputs` + distributed sections).

### Tests

Positive:
1. Every active Product requirement row (R1/R2/R3/R4/R6/R7/R11/R12) resolves to at least one durable current evidence producer with an explicit exact-subject binding class (acceptance-map completeness).
2. Exact candidate/SHA currentness is explicit: every producer names its binding class, and CANDIDATE_BOUND/DURABLE_STATIC producers carry blob identities verifiable at the checkout (P2).
3. The §19.3 blocker list is reconstructible by a fresh observer from the projection alone (blocker_projection + missing-evidence description + route-to-owner per row; closure blocker inputs visibly distinct from Product requirement rows).
4. Minimum-ADS and Advanced-ADS evidence paths both remain legal: authority-required evidence is mandatory on both; Advanced-only orchestration producers never become Minimum requirements.
5. Release owner remains external to the index: the projection emits no Release verdict vocabulary and no second release state machine.

Negative (from #862@6012768804 N1-N15 + #862@6043147928 A1-A12, bound into TEST_MATRIX.yaml):
1. An old-candidate PASS (preview heads `a7dc127`/`41df8e5`, predecessor base `ab8339f`) never binds a successor exact subject; historical evidence stays reachable-but-non-current (N1/N2/A1/A5/A10).
2. CI/Task/PR PASS, machine-conformance PASS, scheduler dispatch/admission/claim events, and multi-lane duplicate evidence never manufacture Product acceptance or clear a §19.3 blocker (N3/N4/N5/N6/N7/N8/N10/A2/A3).
3. Missing/ambiguous evidence never becomes NOT_APPLICABLE from cost, docs-only label, file count, speed or model confidence — unknown reduction predicates fail closed (N11).
4. The index never redefines a Product requirement, mints a Release verdict, turns Advanced-path evidence into Minimum ceremony, or reaches `ADS_CORE_FEATURE_FREEZE_ELIGIBLE` (N13/N15/A4/A6/A11/A12); WEB-origin evidence never substitutes for LOCAL exact-subject validation (N9); multi-dispatch verdicts never merge (N12/N14).

### Contract / invariants

- `PROJECTION_ONLY=true; authorizes_execution=false; authorizes_release_qualification=false; verdict_authority=LATER_GATES_AND_OWNING_STANDARDS_ONLY` (v4.9 handoff record discipline).
- `Evidence != Verdict != Authority` stays true; RELEASE_STANDARD keeps Candidate/Freeze/Hidden/Release Qualification authority and §11 gate applicability; VALIDATION_STANDARD keeps exact-subject evidence meaning (the only legal NOT_APPLICABLE); DEVELOPMENT_WORKFLOW keeps lifecycle/gate routing; Frozen Product §18/§19 keeps requirement meaning; EXECUTION_ARCHITECTURE_STANDARD is a provenance producer only (claim_key/admission_generation/compatibility_group/environment).
- Exact-subject binding: every CANDIDATE_BOUND producer names blob identity; candidate drift/thaw renders the row historical and reopens `UNRESOLVED` — no verdict or evidence transfer to a successor (§16).
- Fail-closed: missing/ambiguous owner or evidence yields an explicit `UNRESOLVED` row with `route_to_owner` — never a guess, never NOT_APPLICABLE by convenience (§13/§19.2).
- The projection issues no Version Closure, no Release Qualification and no `ADS_CORE_FEATURE_FREEZE_ELIGIBLE` assertion (§19.4/§1.1 — T07B decision-support path).

### Implementation seam

Allowed write set (bounded, verbatim from Task Pack §V410-T07A): existing version-closure/release/reference/checklist surfaces; acceptance-evidence index/projection; focused tests. Concretely:
- NEW `docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md` (the index/projection; ROW_SCHEMA + BLOCKER_RULES from #862@6013713353).
- NEW `scripts/test_v410_t07a_acceptance_projection.py` (focused deterministic suite; stdlib unittest).
- Six-core pack artifacts (this directory).
- Optional minimal pointer edit to `checklists/version-closure.md` ONLY if closure-time consumption materially needs it — JIT decision: NOT taken (default NO checklist mutation per #862@6013713353; the projection is discoverable through `docs/implementation/4.10.0/` and the pack).

Do NOT touch: `schemas/`, `templates/agent-event-comment.md`, `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md` (T06B-owned), `standards/RELEASE_STANDARD.md`, `standards/VALIDATION_STANDARD.md`, `standards/DEVELOPMENT_WORKFLOW.md`, `standards/EXECUTION_ARCHITECTURE_STANDARD.md`, `docs/implementation/4.10.0/PRD.md`, `standard-manifest.json` (registration not required by `scripts/verify_standard.py`; RA-guards in `scripts/test_v48_registry_adoption.py` forbid unlisted section additions — manifest untouched is the only green path for this task).

### Failure handling

- Missing/ambiguous owner or evidence ⇒ explicit `UNRESOLVED` blocker row with `route_to_owner`; never a guess.
- Producer blob drift at any later checkout ⇒ the focused suite fails closed (stale producer can no longer silently bind — A1/A10).
- Parse drift of the embedded machine record ⇒ suite fails closed (N13-class).
- Owner/semantic conflict with integrated T06B surfaces or a need for new authority ⇒ STOP and return to Controller for rebind; never widen scope.

### References

- Frozen Product #837 / `docs/implementation/4.10.0/PRD.md` (§1.1/§2/§9/§13/§16/§18/§19/§20)
- Frozen L2 #842 / refined DAG #848 / `docs/implementation/4.10.0/TASK_PACKS_R1.md#V410-T07A`
- #861 integrated at `0518202c` (V410-T06B machine/projection surfaces)
- `standards/RELEASE_STANDARD.md` (§2/§6/§10/§11), `standards/VALIDATION_STANDARD.md`, `standards/DEVELOPMENT_WORKFLOW.md`
- #900 (provenance remediation campaign — distinct closure blocker input), #865 (V410-V01 — later closure-input Validation)
- Precompute set: #862@6003300393 / @6012768804 / @6013713353 / @6034650781 / @6040863477 / @6043147928 / @6046061801

## Forbidden scope (verbatim from Task Pack §V410-T07A)

`second Release verdict/state machine; Product requirement redefinition; historical evidence transfer`

Additionally forbidden by the fast-path handoff (#862@6046061801): manufacturing Product acceptance/Release verdicts; treating scheduler/CI/Review PASS as Product acceptance; turning Advanced-only evidence into a Minimum requirement; reusing stale preview exact-subject facts.

## Gate obligations

Focused acceptance-map completeness + negative automatic-transfer suite green; all carried producer/currentness suites green (see TEST_MATRIX.yaml); `python scripts/verify_standard.py`; `python scripts/verify_event_writer_surfaces.py`; `tools/task-check.sh`; fresh LOCAL Concern Validation; genuinely Fresh Independent Review on one unchanged HEAD/tree. Review PASS is not Release PASS; the Builder does not merge.
