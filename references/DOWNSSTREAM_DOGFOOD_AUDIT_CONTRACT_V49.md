# Downstream Dogfood / Independent Safety-Auditor Contract (v4.9 T-014)

Status: **evidence-contract reference — not an evidence owner, not a verdict authority, not an execution authorization.**

This reference defines the release-consumable **Proportional Dogfood Report / Checklist** and the
**independent safety-auditor eligibility contract** for v4.9, bound to the Frozen Product dogfood
and measurement contract (`docs/implementation/4.9.0/PRD.md` §16, blob
`a8ec7030a14337a4c2dca853dc474e965679d610`) and the Frozen L2 downstream dogfood evidence
architecture (`docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md` §14, blob
`bd41ea0175b459a6a490fd37ad579e429a58a1c3`), as consumed/handed off by the T-010 gate matrix row
M10 (`references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md`), under the immutable DAG v0.1
(blob `4f358ba2b32e01ae17ddcdf970151cf28e44bb3f`) section `### T-014` concern authority
composed with Frozen DAG v0.2 (`docs/implementation/4.9.0/TASK_DAG.md`, blob
`b9fe0cc7089f64929b4bcf45f7230d950e864db2`) admission rules.

- This contract edits **no Release surface**. The `T-005 → T-010 → T-014` Release-owner
  serialization is respected: Release applicability and any re-evaluation after candidate drift
  are consumed **by reference** to the T-005 owner
  (`standards/RELEASE_STANDARD.md#11-release-applicability-by-gate--subject`;
  `references/RELEASE_APPLICABILITY_REFERENCE.md`;
  `scripts/test_v49_release_applicability.py`). This lane cannot authorize execution, cannot
  issue Release Qualification, and cannot mint PASS/READY.
- Routing/currentness vocabulary is the T-010 owner map's: a report on the exact current ADS
  candidate is `BOUND_CURRENT`; on candidate thaw/drift it is `HISTORICAL_ONLY` until the
  Release owner re-evaluates. Currentness never mints a verdict
  (`registries/state-dimensions-v1.json`, forbidden inferences F13–F16).
- Deterministic negatives for this contract: `scripts/test_v49_dogfood_audit_contract.py` +
  `fixtures/dogfood-audit-contract/**` (oracles D01–D08).

## 0. Consumed authorities (exact refs; cited, not copied, not redefined)

```text
docs/implementation/4.9.0/PRD.md#16-downstream-dogfood-and-measurement-contract
docs/implementation/4.9.0/PRD.md#163-exact-candidate-binding
docs/implementation/4.9.0/PRD.md#164-baseline-and-selected-execution
docs/implementation/4.9.0/PRD.md#165-mechanism-exercise-matrix
docs/implementation/4.9.0/PRD.md#166-non-vacuity--positive-proportional-outcome
docs/implementation/4.9.0/PRD.md#167-independent-safety-audit
docs/implementation/4.9.0/PRD.md#168-manualgithub-native-viability
docs/implementation/4.9.0/PRD.md#169-claim-boundary
docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md#14-downstream-dogfood-evidence-architecture
docs/implementation/4.9.0/TASK_DAG.md
references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md#m10--proportional-dogfood-report-downstream-dogfood-candidate-binding
standards/RELEASE_STANDARD.md#11-release-applicability-by-gate--subject
references/RELEASE_APPLICABILITY_REFERENCE.md
scripts/test_v49_release_applicability.py
standards/VALIDATION_STANDARD.md#5-validation-layers
standards/VALIDATION_STANDARD.md#8-ci-execution-channel-vs-validation-gate
standards/VALIDATION_STANDARD.md#12-evidence-minimum
standards/CI_EVIDENCE_STANDARD.md
references/ROLE_EXECUTION_PROFILE_V1_REFERENCE.md#4-owner-reference-table-all-refs-point-into-existing-owners
references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md#identity-and-currentness
references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md#evidence-strength
scripts/test_v49_gate_currentness.py
registries/state-dimensions-v1.json
```

Every normative meaning below stays with its owner. This contract only shapes the
release-consumable record and rejects records that fail the owners' bindings.

## 1. Release-consumable Proportional Dogfood Report — required record shape

A report/checklist is release-consumable only when every required item is durably recorded with
an exact binding. Items may be truthfully `NOT_RUN | BLOCKED` with a reason ref; a missing item
without an explicit state is fail-closed (reject).

```text
record_id
downstream_repository                     # qualifying project per PRD §16.2 (distinct product/repo, own pinned authority artifacts, never ADS itself or a synthetic mirror)
bound_ads_candidate                       # exact candidate identity, PRD §16.3 (§2 below)
pinned_authority_refs                     # pinned Product/Architecture/Task/Review/Validation/Release refs of the downstream project + the frozen authority refs of the tested semantics (PRD §16.4)
legal_baseline_workflow                   # legal workflow under the project's bound authority WITHOUT the tested proportional decision; never an invented maximum-ceremony strawman (PRD §16.4)
selected_proportional_workflow            # the workflow actually executed under the tested v4.9 proportional decisions (PRD §16.4)
execution_containers                      # containers/issues
role_dispatch_claims                      # dispatches/claims
independent_gates_sessions                # independent gates/sessions
rebind_revalidation_events                # rebind/revalidation events
mechanism_matrix                          # per §4 below
ambiguous_predicate_exercise              # per §5 below (required exercise)
baseline_vs_selected_delta_nonzero        # per §3 below
delta_account                             # per-step decision-value account for omitted/coalesced/reused/avoided steps (PRD §16.4)
safety_negatives                          # per §6 below (five counters)
auditor                                   # per §7 below (identity + eligibility profile refs)
manual_github_native_viability            # per §9 below
claim_boundary                            # per §10 below
```

Execution counts (`execution_containers`, `role_dispatch_claims`, `independent_gates_sessions`,
`rebind_revalidation_events`) also supply the #680 quantification evidence set (PRD §16.10);
they are descriptive only and never alter Product authority.

## 2. Exact ADS candidate binding (D01)

Per `docs/implementation/4.9.0/PRD.md#163-exact-candidate-binding` and M10, the report MUST bind
to the exact v4.9 candidate/revision whose semantics it exercised:

```text
bound_ads_candidate format: candidate:<label>@sha:<40-hex>
```

- Missing, malformed, or non-exact binding => reject `MISSING_EXACT_ADS_CANDIDATE`.
- Exact match against the current ADS candidate => `BOUND_CURRENT`.
- Candidate thaw/drift => `HISTORICAL_ONLY`; the record stays historical truth and the Release
  owner must re-evaluate before any downstream use (`release_owner_reevaluation_required=true`).
  Re-evaluation is Release-owned (T-005 owner by reference); it is never performed by this
  contract, the reporter, or the auditor.
- `pinned_authority_refs` must be present and non-empty; each cited ref must resolve in the
  downstream project's durable authority or in this repository
  (`MISSING_PINNED_AUTHORITY_REFS` otherwise). A run whose authority baseline is not durably
  inspectable does not qualify (PRD §16.2).

## 3. Legal baseline vs selected workflow accounting (D02)

Per `docs/implementation/4.9.0/PRD.md#164-baseline-and-selected-execution`:

- The baseline MUST be recorded as legal under the project's bound authority and MUST declare
  `invented_maximum_ceremony=false`; an invented maximum-ceremony strawman rejects
  (`ILLEGAL_BASELINE_CONSTRUCTION`).
- Baseline and selected workflows MUST carry distinct workflow identities. Identical
  baseline/selected with a nonzero-delta claim is self-contradictory => reject
  `INCONSISTENT_BASELINE_SELECTED` (fail-closed).
- Every proportional step behind a claimed delta (omitted, coalesced, reused, or
  avoided-known-blocked dispatch) MUST carry a decision-value account
  (`delta_account[].decision_value_account` non-empty, per class
  `REDUCTION | COALESCING | REUSE | AVOIDED_KNOWN_BLOCKED_DISPATCH`). An unaccounted delta
  rejects (`UNACCOUNTED_PROPORTIONAL_DELTA`).
- A reduced-orchestration-cost claim MUST be `MEASURED` (with proof refs) or `NOT_MEASURED`;
  `MEASURED` without proof refs rejects (`UNMEASURED_COST_CLAIM`). Unmeasured observations stay
  descriptive evidence and never become Release authority or economic-savings claims.

## 4. Mechanism exercise matrix (D03)

Per `docs/implementation/4.9.0/PRD.md#165-mechanism-exercise-matrix`, for every mechanism for
which downstream generality is claimed, the matrix records `EXERCISED | NOT_EXERCISED` (or
truthful `NOT_RUN | BLOCKED` with reason ref) plus proof references:

```text
OWNER_PERMITTED_REDUCTION                     (owner-permitted reduction)
CROSS_OWNER_FLOOR_COMPOSITION                 (cross-owner floor composition)
SAME_CONTAINER_PHASE_COALESCING               (same-container phase coalescing)
GATE_OWNED_EVIDENCE_TRANSFER                  (gate-owned evidence transfer)
FAIL_CLOSED_UNKNOWN_AMBIGUOUS_PREDICATE       (fail-closed unknown/ambiguous predicate)
NON_DISPATCH_WAIT                             (non-dispatch wait)
PROSPECTIVE_RELEASE_APPLICABILITY_SELECTION   (prospective release-applicability selection, if claimed)
```

- A claimed mechanism absent from the matrix rejects (`INCOMPLETE_MECHANISM_MATRIX`).
- `EXERCISED` requires at least one proof ref (`EXERCISED_WITHOUT_PROOF` otherwise).
- `NOT_EXERCISED` requires an explicit per-mechanism claim boundary; a missing claim boundary
  rejects (`UNEXERCISED_CLAIM_BOUNDARY_MISSING`). Being truthful about non-exercise is
  evidence; it can never support a generality claim for that mechanism.
- Unknown mechanism ids are ambiguous predicates => fail-closed
  (`AMBIGUOUS_PREDICATE_FAIL_CLOSED`).

## 5. Ambiguous predicate fail-closed exercise (D05)

Per PRD §16.5 and the architecture UNKNOWN dispositions (Frozen L2 §16, U3: model output never
proves reduction), at least one observed or deliberately induced unknown/ambiguous
reduction-predicate case MUST be exercised and shown to take the stronger existing path or
`BLOCKED`:

```text
ambiguous_predicate_exercise.state   in { EXERCISED, NOT_RUN, BLOCKED }
ambiguous_predicate_exercise.outcome in { STRONGER_PATH, BLOCKED, MODEL_JUDGMENT }
```

- `outcome=MODEL_JUDGMENT` rejects (`AMBIGUOUS_PREDICATE_MODEL_RESOLVED`): an ambiguous
  predicate resolved by model judgment is never durable owner-accepted proof.
- An unknown outcome/state value rejects (`AMBIGUOUS_PREDICATE_FAIL_CLOSED`).
- The exercise honestly `NOT_RUN`/`BLOCKED` keeps the record consumable as evidence but
  downstream generality is `NOT_SATISFIED` (`REQUIRED_AMBIGUOUS_EXERCISE_NOT_RUN`).
- Any other ambiguous predicate anywhere in the record (unknown enum, missing required field,
  contradictory states) fails closed: reject `AMBIGUOUS_PREDICATE_FAIL_CLOSED` or
  `MISSING_REQUIRED_FIELD`, never guess.

## 6. Safety-negative account

Per `docs/implementation/4.9.0/PRD.md#167-independent-safety-audit` and Frozen L2 §14, the
independent audit MUST establish, from durable baseline/terminal evidence:

```text
UNAUTHORIZED_GATE_OMISSION=0
STALE_PASS_TRANSFER=0
INDEPENDENCE_LOSS=0
CROSS_OWNER_REQUIREMENT_CANCELLATION=0
ADVERSE_TERMINAL_SUPPRESSION=0
```

- All five counters are required; any missing counter rejects
  (`MISSING_SAFETY_NEGATIVE_ACCOUNT`).
- Any nonzero counter is honest evidence of failure: the record stays consumable, downstream
  generality is `NOT_SATISFIED` (`SAFETY_NEGATIVE_VIOLATION`) and the concern routes to its
  owning authority. Suppression or omission of a violated counter is itself a
  `SAFETY_NEGATIVE_VIOLATION` finding.

## 7. Independent safety-auditor eligibility and profile (D06)

Per `docs/implementation/4.9.0/PRD.md#167-independent-safety-audit` and Frozen L2 §14, the
safety-negative account MUST be checked by an executor who satisfies the applicable independent
evidence-source policy and is not the orchestrating or Builder principal for the tested
decisions. Eligibility is bound **by reference into the owners**; auditor identity alone grants
no authority:

```text
auditor.auditor_id                        # durable identity (never sufficient by itself)
auditor.eligibility_profile_refs          # one or more owner-surface refs (see below)
auditor.is_orchestrator_principal         # MUST be false
auditor.tested_decision_principal_ids     # dispatch/claim principals of the tested decisions
```

Eligibility profile owner surfaces (each ref must resolve in-repository; the auditor profile
projection follows the owner-reference discipline of
`references/ROLE_EXECUTION_PROFILE_V1_REFERENCE.md#4-owner-reference-table-all-refs-point-into-existing-owners`):

```text
docs/implementation/4.9.0/PRD.md#167-independent-safety-audit
docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md#14-downstream-dogfood-evidence-architecture
standards/VALIDATION_STANDARD.md#5-validation-layers
standards/VALIDATION_STANDARD.md#8-ci-execution-channel-vs-validation-gate
standards/VALIDATION_STANDARD.md#12-evidence-minimum
references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md#identity-and-currentness
references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md#evidence-strength
```

- Missing/empty profile refs, or refs that resolve to no owner surface, reject
  (`AUDITOR_PROFILE_REF_NOT_OWNER_SURFACE`); no profile at all rejects (`INELIGIBLE_AUDITOR`).
- The auditor being the orchestrator/Builder principal of the tested decisions, or appearing in
  `tested_decision_principal_ids`, rejects (`AUDITOR_IS_TESTED_PRINCIPAL`). Self-attestation by
  the orchestrator/Builder is insufficient for Release generality evidence.
- The auditor produces the safety-negative check only; the auditor identity can never mint a
  verdict, authorize execution, or issue Release Qualification (§8).

## 8. Evidence-only posture (D07)

The report/checklist is **Release evidence only** (Frozen L2 §14; M10 owner rule):

- For every evaluation outcome the contract's outputs are fixed:
  `authorizes_execution=false` and `authorizes_release_qualification=false`. No report content,
  auditor identity, or counter value can flip them.
- A record carrying self-authorizing fields (any of `authorization`, a self-set
  `authorizes_execution` / `authorizes_release_qualification` flag,
  `release_qualification_verdict`, `gate_pass`) rejects (`SELF_AUTHORIZING_FIELD`).
- `downstream_generality=SATISFIED` is an evidence-accounting result, not a gate verdict: it is
  never PASS, never READY, and cannot be inferred from currentness alone (registry F13–F16).
  Release Qualification remains a Release-owner verdict on a current candidate.

## 9. Manual/GitHub-native viability

Per `docs/implementation/4.9.0/PRD.md#168-manualgithub-native-viability`, at least one
qualifying run MUST remain executable through manual/GitHub-native interaction without a
scheduler daemon or proprietary transport:

```text
manual_github_native_viability.state       in { EXERCISED, NOT_EXERCISED, NOT_RUN, BLOCKED }
manual_github_native_viability.proof_refs  # required when EXERCISED
```

Honest `NOT_EXERCISED/NOT_RUN/BLOCKED` keeps the record consumable; downstream generality is
`NOT_SATISFIED` (`MANUAL_VIABILITY_NOT_SATISFIED`).

## 10. Claim boundary for unexercised mechanisms (D07-adjacent)

Per `docs/implementation/4.9.0/PRD.md#169-claim-boundary`, Release claims of downstream
generality MUST enumerate exactly which mechanisms were exercised and supported. A run
exercising only one mechanism implies nothing for unexercised mechanisms; every `NOT_EXERCISED`
matrix row carries its own explicit claim boundary (§4).

## 11. Owner surfaces cited, not copied (D08)

- Every authority in §0/§7 is cited by exact repository ref; each ref must resolve at the
  candidate (path + heading anchor). Owner text is never copied into this contract and owner
  semantics are never redefined here.
- The kernel test asserts: all cited refs resolve; the owner surfaces (including every Release
  surface, the Frozen Product/L2/DAG blobs, and the T-010 artifacts) are unmutated since this
  lane's base; the committed diff stays inside the Builder write set; and the rejection/
  mechanism vocabularies of this document agree with `fixtures/dogfood-audit-contract/**` and
  `scripts/test_v49_dogfood_audit_contract.py`.

## 12. Observational evidence bindings (late, audit-input-only)

The following late bindings strengthen existing evidence dimensions. They create **no new
normative owner, no new telemetry lifecycle/schema, and no Release authority**. Every dimension
is recorded where evidence exists; absent evidence is recorded `UNKNOWN`, never fabricated
(#733 late bindings: #775/#696, #803@5987255662, #807):

```text
observational.task_granularity_coherence        # semantically coherent, agent-dispatchable tasks; no mechanical LOC/time splitting
observational.parallelism_correctness           # task-level vs dispatch-level parallelism used correctly
observational.learning_signals                  # repeated LONG/repair/rebind patterns recorded as learning signals, never converted into unsupported hard thresholds
observational.routing_evidence_basis            # executor/environment/transport routing evidence-based (incl. Web whole-file-replacement limitation); capability mismatch failed closed or rerouted
observational.cost_claim                        # MEASURED (proof refs) | NOT_MEASURED (§3; never economic-savings authority)
observational.review_owner_proposals_isolation  # unresolved Review-owner proposals (e.g. #696) kept outside v4.9 normative mutation
observational.estimate_vs_actual                # bounded estimate-vs-actual / gate-decision-value set; ACTIVE vs ELAPSED distinguished; UNKNOWN over fabricated active effort; durable GitHub timestamps may support elapsed/queue measurement
observational.execution_learning_samples        # existing T006 fields referenced where possible; task-local vs cross-task reusability; anti-noise incl. valid NO_MATERIAL_EXECUTION_LEARNING; privacy/secrets/chain-of-thought excluded; promotion candidate only, never automatic authority
```

These dimensions may make an audit finding more precise; they can never relax §2–§11.

## 13. Deterministic evaluation vocabulary (kernel agreement)

Rejection reasons (record is not release-consumable as-is; fix the record):

```text
MISSING_REQUIRED_FIELD
MISSING_EXACT_ADS_CANDIDATE
MISSING_PINNED_AUTHORITY_REFS
ILLEGAL_BASELINE_CONSTRUCTION
INCONSISTENT_BASELINE_SELECTED
UNACCOUNTED_PROPORTIONAL_DELTA
UNMEASURED_COST_CLAIM
INCOMPLETE_MECHANISM_MATRIX
EXERCISED_WITHOUT_PROOF
UNEXERCISED_CLAIM_BOUNDARY_MISSING
AMBIGUOUS_PREDICATE_MODEL_RESOLVED
AMBIGUOUS_PREDICATE_FAIL_CLOSED
MISSING_SAFETY_NEGATIVE_ACCOUNT
INELIGIBLE_AUDITOR
AUDITOR_IS_TESTED_PRINCIPAL
AUDITOR_PROFILE_REF_NOT_OWNER_SURFACE
SELF_AUTHORIZING_FIELD
```

Non-rejection dispositions and outcomes:

```text
BOUND_CURRENT
HISTORICAL_ONLY
REJECTED
SATISFIED
NOT_SATISFIED
NOT_EVALUATED
ADS_CANDIDATE_DRIFT
SAFETY_NEGATIVE_VIOLATION
REQUIRED_AMBIGUOUS_EXERCISE_NOT_RUN
MANUAL_VIABILITY_NOT_SATISFIED
UNEXERCISED_MECHANISM_CLAIM_LIMITED
COMPATIBILITY_EVIDENCE_ONLY
release_owner_reevaluation_required=true
authorizes_execution=false
authorizes_release_qualification=false
```

## 14. Downstream generality decision table

```text
REJECTED                                    => not release-consumable; repair the record; no evidence posture asserted
HISTORICAL_ONLY                             => historical truth only; Release-owner re-evaluation required before any downstream use
BOUND_CURRENT + all §2-§9 requirements met  => downstream_generality=SATISFIED (evidence only)
BOUND_CURRENT + zero baseline-vs-selected delta => compatibility evidence only; downstream_generality=NOT_SATISFIED
any safety-negative counter nonzero          => downstream_generality=NOT_SATISFIED; route to owning concern
any required exercise honestly NOT_RUN/BLOCKED => downstream_generality=NOT_SATISFIED with explicit reason
any outcome, always                          => authorizes_execution=false; authorizes_release_qualification=false
```

Synthetic, compatibility-only, or no-op runs cannot substitute for a qualifying run. Missing
required real evidence is recorded `NOT_RUN | BLOCKED` and blocks any downstream-generality
claim.
