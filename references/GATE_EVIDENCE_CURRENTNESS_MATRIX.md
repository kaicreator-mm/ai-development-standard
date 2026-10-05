# Gate-Owned Evidence Currentness Matrix (v4.9 T-010)

Status: **cross-owner wiring reference — not an evidence owner, not a verdict authority.**

This reference makes the Frozen L2 gate-owned evidence binding/currentness matrix
(`docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md` §10, frozen blob
`bd41ea0175b459a6a490fd37ad579e429a58a1c3`) executable through the existing owners at
v4.9 base `version/v4.9.0@f4fe88542de9d3f5376498e62778e2353391bc57`. It performs
wiring only: every row cites its owning standard/contract by exact repository ref,
and no row redefines, replaces, or re-derives owner-specific evidence meaning.

- This map can **never** mint, transfer, or infer PASS/READY. Routing outcomes are
  `NON_AUTHORITATIVE_DERIVED_STATE` (see §2); verdict authority stays with the owners.
- Release-owner serialization (`T-005 → T-010 → T-014`) is respected: this lane edits
  no Release surface. Release applicability binding is consumed **by reference** to the
  T-005 owner (`standards/RELEASE_STANDARD.md` §11; illustrative reference
  `references/RELEASE_APPLICABILITY_REFERENCE.md`; owner test
  `scripts/test_v49_release_applicability.py`).
- Executable binding: `scripts/test_v49_gate_currentness.py` +
  `fixtures/gate-currentness/**` (TEST_MATRIX T01–T07).

## 1. Consumed authorities (exact refs)

```text
Frozen Product #709        docs/implementation/4.9.0/PRD.md (blob a8ec7030a14337a4c2dca853dc474e965679d610), §16 downstream dogfood
Frozen L2 #714             docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md (blob bd41ea0175b459a6a490fd37ad579e429a58a1c3), §5.2/§9/§10/§11/§14
Frozen Task DAG v0.2       docs/implementation/4.9.0/TASK_DAG.md (blob b9fe0cc7089f64929b4bcf45f7230d950e864db2)
T-002 contract             standards/ASSURANCE_PLAN_STANDARD.md §12/§13 + schemas/assurance-plan-v2.schema.json
T-005 owner                standards/RELEASE_STANDARD.md §11 + references/RELEASE_APPLICABILITY_REFERENCE.md + scripts/test_v49_release_applicability.py
T-007 consumer contract    standards/EXECUTION_ARCHITECTURE_STANDARD.md §28 (28.1/28.5/28.6) + scripts/test_v49_execution_core.py
```

## 2. Executable wiring vocabulary (routing only)

A **gate evidence record** is an owner-issued durable fact with this minimum shape
(fixture wire format; owners may require stronger bindings — the stronger binding
controls):

```json
{
  "record_id": "<durable result pointer>",
  "row_id": "M01..M10 (this matrix)",
  "owner_ref": "<exact owner ref from the row>",
  "verdict": "<owner vocabulary, e.g. PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE; Review adds CHANGES_REQUESTED|VALIDATION_REQUESTED>",
  "subject_identity": "<exact subject, e.g. sha:<40-hex> or candidate:<id>@tree:<40-hex>>",
  "binding": { "<row binding-minimum fields>" : "..." }
}
```

A **current subject fact** carries the exact identity a gate would execute against now
(SHA/tree/candidate), the governing Assurance Plan state, and the carried unresolved
finding set.

The wiring engine (implemented only in `scripts/test_v49_gate_currentness.py`) maps an
evidence record plus the current subject fact onto **routing dispositions — never
verdicts**:

```text
BOUND_CURRENT             record subject/binding exactly matches the current subject under the row's owner rule
HISTORICAL_ONLY           no owner transfer rule applies (L2 §10); evidence stays historical
FRESH_EXECUTION_REQUIRED  owner rule is fresh-only and the subject drifted (L2 §10 OWNER_FRESH_ONLY)
SUCCESSOR_ASSURANCE_REQUIRED  material binding change => successor assurance per the owning rule
CARRY_FORWARD_UNTIL_DISPOSITION   unresolved adverse finding persists across subject succession
RECOMPUTE_REQUIRED        plan/binding STALE => recompute/rebind before authority-bearing use
BLOCKED                   unknown/ambiguous binding => stronger legal path or BLOCKED (fail-closed)
```

Every disposition is derived state. `BOUND_CURRENT` means only "the owner-issued verdict
may be *consulted* for this subject" — it is never itself a verdict, and verdict
inferences from currentness (`CURRENT -> PASS`, `CURRENT -> READY`, `BOUND_CURRENT ->
gate satisfied` without an owner verdict on the current subject) are forbidden per
`registries/state-dimensions-v1.json` F13–F16 and L2 §10 ("Path disjointness, unchanged
HEAD/tree or ancestry are only possible proof inputs under an owner rule; never transfer
authority themselves").

## 3. Owner map (executable rows)

Each row: `row_id` | evidence/decision family | canonical owner (exact ref) | minimum
binding | owner-defined currentness/transfer rule | wiring function of this map. The
machine-readable row table lives in `fixtures/gate-currentness/owner_map.json`; the test
kernel asserts every `owner_ref` below resolves in-repository and that no owner text is
redefined.

### M01 — Assurance Plan successor (Assurance currentness; T-002 contract)

Exact refs (resolvable at the candidate; machine-checked by the kernel):

```text
standards/ASSURANCE_PLAN_STANDARD.md#12-currentness-binding
standards/ASSURANCE_PLAN_STANDARD.md#13-adverse-finding-carry-forward
schemas/assurance-plan-v2.schema.json#currentness_binding
schemas/assurance-plan-v2.schema.json#finding_carry_forward_policy
standards/EXECUTION_ARCHITECTURE_STANDARD.md#281-assurance-plan-currentness-consumption-at-architecture-owned-transitions
```

- Owner meaning: currentness binding (`standards/ASSURANCE_PLAN_STANDARD.md`
  §12, §13) + schema
  `schemas/assurance-plan-v2.schema.json` (`currentness_binding.rule` =
  `all-components-exact-current`; `finding_carry_forward_policy` =
  `unresolved-valid-findings-carry-forward`).
- Minimum binding (§12, schema-required): `subject_identity_ref`,
  `owner_authority_refs`+digest, `proof_input_refs`+digest, `task_pack_ref`+digest,
  `release_decision_refs`+digest, `unresolved_finding_refs`+digest, `binding_digest`,
  `state ∈ {CURRENT, STALE, UNKNOWN}`. An empty set is still bound by its digest;
  omission is not an empty set.
- Owner rule: any material identity/digest drift => `STALE`; missing/ambiguous =>
  `UNKNOWN`; `STALE`/`UNKNOWN` never authorize a lower assurance path.
- Wiring: authority-bearing consumers recheck `currentness_binding.state` immediately
  before Dispatch materialization, Claim admission, merge/merge-ready, Candidate Freeze,
  Release Qualification (`standards/EXECUTION_ARCHITECTURE_STANDARD.md` §28.1) —
  transition proceeds only on `CURRENT`; otherwise `RECOMPUTE_REQUIRED`/`BLOCKED`. A new
  adverse finding between Dispatch and Claim fails Claim admission (§28.1/§28.6). The
  plan proves derivation only; it creates no Gate PASS, scope, Release applicability, or
  finding disposition.

### M02 — Concern Validation

Exact refs (resolvable at the candidate; machine-checked by the kernel):

```text
standards/VALIDATION_STANDARD.md#6-exact-sha-evidence-and-drift
standards/VALIDATION_STANDARD.md#12-evidence-minimum
```

- Owner meaning: `standards/VALIDATION_STANDARD.md` §6 (exact-SHA evidence and drift) + §12
  (evidence minimum).
- Minimum binding: tested SHA + profile/scope + environment/toolchain + authority refs.
- Owner rule: evidence remains attributed to the SHA where it actually ran; a PASS is
  never rewritten onto a successor SHA.
- Wiring: `tested_sha == current subject sha` else `HISTORICAL_ONLY` (T01). No transfer
  rule exists for a different subject.

### M03 — Integration Validation (impact decisions)

Exact refs (resolvable at the candidate; machine-checked by the kernel):

```text
standards/VALIDATION_STANDARD.md#6-exact-sha-evidence-and-drift
standards/VALIDATION_STANDARD.md#7-tested-checkpoint-vs-evidence-only-head
```

- Owner meaning: `standards/VALIDATION_STANDARD.md` §6 (`BASE / merge-result drift`,
  `VALIDATION_IMPACT_DECISION`, `Evidence-preserving successor`) + §7 (tested checkpoint
  vs evidence-only head).
- Minimum binding: `validated_head_sha`, `base_sha_at_validation`, `current_target_sha`,
  base delta / write-set comparison, `validation_impact`, `evidence_reuse_basis`,
  attribution.
- Owner rule: an expensive tuple stays usable across BASE drift **only** through an
  explicit `VALIDATION_IMPACT_DECISION` proving `validation_impact=none` whose delta
  proof excludes source/runtime behavior, tests/fixtures, dependency/lockfile/toolchain/
  build inputs, public contract/architecture semantics, shared integration wiring,
  artifact identity, or overlapping write sets. `affected|unknown` => rerun affected
  gates. HEAD drift is never repaired by an impact decision (new dispatch identity).
- Wiring: evaluates the decision's presence and proof classes only; reuse is asserted
  per the owner's rule, and reuse never mints a new PASS — it binds the existing
  owner-issued tuple to the current merge subject (T03).

### M04 — Review (successor / full / complete-delta; carried findings)

Exact refs (resolvable at the candidate; machine-checked by the kernel):

```text
standards/DEVELOPMENT_WORKFLOW.md#stage-26--review-policy-selection
standards/DEVELOPMENT_WORKFLOW.md#44-independent-review按需
standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md#6-review-policy-and-risk
schemas/review-aggregation-v1.schema.json#aggregation_policy
schemas/review-finding-v1.schema.json
docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md#9-adverse-findings-and-successor-subjects
standards/EXECUTION_ARCHITECTURE_STANDARD.md#285-adverse-finding-carry-forward-and-no-review-shopping-routing
```

- Owner meanings: `standards/DEVELOPMENT_WORKFLOW.md` Stage 2.6 (Review Policy Selection) + §4.4
  (Independent Review); `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §6 (Review
  Policy and risk); aggregation contract `schemas/review-aggregation-v1.schema.json`
  (`aggregation_policy = finding-union-blocker-dominance`, `unresolved_blocker_refs`);
  finding contract `schemas/review-finding-v1.schema.json`.
- Minimum binding: exact subject/diff + current authority + required independence +
  carried unresolved findings.
- Owner rules: material successor => new **full** or **complete-delta** Review; PASS is
  not transferred (L2 §10; §9 carry-forward). Every unresolved predecessor finding
  relevant to the repair lineage is carried into the successor review contract and leaves
  the unresolved set only through per-finding verification — `RESOLVED` /
  `STILL_PRESENT` / `NOT_APPLICABLE_TO_SUCCESSOR`, each with evidence refs and, for
  not-applicable, an owning-rule basis — or an explicit owning-authority finding
  disposition (L2 §9.1; `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §28.5). Re-review
  only via authorized mutable repair path; same-subject re-dispatch to obtain PASS is
  rejected; a new reviewer PASS over an unresolved blocker does not remove the blocker.
- Wiring: carries the finding set, evaluates per-finding successor outcomes, and holds a
  successor Review judgment non-admissible while the unresolved set is non-empty
  (blocker dominance per the aggregation contract). It does not grade findings —
  equivalence/severity/aggregation stay with the Review/Adversarial owners (M04 never
  redefines them).

### M05 — Hidden Validation

Exact refs (resolvable at the candidate; machine-checked by the kernel):

```text
standards/RELEASE_STANDARD.md#4-operational-immutability
standards/RELEASE_STANDARD.md#5-hidden-validation-and-escaped-defects
standards/TEST_DATA_AND_SCENARIO_STANDARD.md
```

- Owner meaning: `standards/RELEASE_STANDARD.md` §4–§5 + applicable Hidden authority; scenario
  quality `standards/TEST_DATA_AND_SCENARIO_STANDARD.md`.
- Minimum binding: frozen candidate + private pack/revision + holder policy.
- Owner rule: fresh-only on candidate/pack/holder drift unless the owner positively
  states otherwise; escaped-defect classes and strengthened-pack re-identification per
  §5; post-freeze change requires the §4 chain `FROZEN → THAWED/INVALIDATED → fix →
  affected visible validation → new freeze → required Hidden Validation → new Release
  Qualification`.
- Wiring: compares the record's frozen-candidate identity to the current candidate
  identity (and thaw state) => `BOUND_CURRENT` or `FRESH_EXECUTION_REQUIRED` (T04).

### M06 — Closeout / Release Qualification

Exact refs (resolvable at the candidate; machine-checked by the kernel):

```text
standards/RELEASE_STANDARD.md#3-candidate-prepared-vs-candidate-frozen
standards/RELEASE_STANDARD.md#4-operational-immutability
standards/RELEASE_STANDARD.md#6-release-verdict
standards/RELEASE_STANDARD.md#7-release-sequence
```

- Owner meaning: `standards/RELEASE_STANDARD.md` (§3 prepared-vs-frozen, §4 operational
  immutability, §6 release verdict, §7 release sequence).
- Minimum binding: frozen candidate + predecessor gate bindings + release authority.
- Owner rule: fresh-only on candidate drift; verdict vocabulary READY/CONDITIONAL/
  BLOCKED/FAIL is Release-owned; never convert `NOT_RUN`/`BLOCKED` to PASS or
  old-candidate evidence to successor PASS (§6).
- Wiring: candidate-identity currentness check only => `BOUND_CURRENT` or
  `FRESH_EXECUTION_REQUIRED` (T04).

### M07 — Release applicability decision (T-005 owner; bind by reference)

Exact refs (resolvable at the candidate; machine-checked by the kernel):

```text
standards/RELEASE_STANDARD.md#11-release-applicability-by-gate--subject
references/RELEASE_APPLICABILITY_REFERENCE.md
scripts/test_v49_release_applicability.py
```

- Owner meaning: `standards/RELEASE_STANDARD.md` §11 (Release applicability by gate × subject;
  §11.1 meanings; §11.2 decision identity; §11.3 no concern-to-version aggregation;
  §11.4 currentness/re-evaluation). Illustrative non-authority reference:
  `references/RELEASE_APPLICABILITY_REFERENCE.md`. Owner test:
  `scripts/test_v49_release_applicability.py`.
- Minimum binding (§11.2): `gate_id`, `subject_ref`, `subject_identity`, `applicability`
  ∈ {`REQUIRED_NOW`, `DEFERRED_TO_VERSION_CLOSURE`, `NOT_APPLICABLE`, `UNKNOWN`},
  `release_authority_ref`, `decision_ref`, `basis_or_proof_refs`,
  `candidate_or_currentness_identity`, `decided_at`, `actor_or_operator`.
- Owner rules: decision is Release-owned per gate × exact subject; concern decisions
  never aggregate to version-level truth (`CONCERN_NOT_APPLICABLE != 
  VERSION_NOT_APPLICABLE`, `CONCERN_DEFERRED != VERSION_GATE_SATISFIED`); `UNKNOWN` is
  fail-closed; applicability is re-evaluated when any binding dimension materially
  changes; version-level applicability is evaluated fresh on the composed candidate.
- Wiring: this map **binds, never decides** — it references the T-005-owned decision
  record, checks its binding currency against the current candidate, and enforces that
  no version-level gate omission is derived from concern-level decisions (T05). It does
  not mint applicability and does not redefine the vocabulary.

### M08 — CI evidence

Exact refs (resolvable at the candidate; machine-checked by the kernel):

```text
standards/CI_EVIDENCE_STANDARD.md#3-identity-model
standards/VALIDATION_STANDARD.md#8-ci-execution-channel-vs-validation-gate
```

- Owner meaning: `standards/CI_EVIDENCE_STANDARD.md` (identity model §3; validation summary §6)
  with the Validation owner (`standards/VALIDATION_STANDARD.md` §8/§10) deciding
  channel-vs-gate.
- Minimum binding: exact SHA/run/profile/provider where material.
- Owner rule: never generic PASS transfer (L2 §10).
- Wiring: subject-identity match only, same predicate family as M02.

### M09 — Task Learning evidence

Exact refs (resolvable at the candidate; machine-checked by the kernel):

```text
schemas/task-learning-v2.schema.json
references/TASK_LEARNING_EVIDENCE_REFERENCE.md#exact-subject-currentness
```

- Owner meaning: v4.8 Task Learning family (`schemas/task-learning-v2.schema.json`; reference
  `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`).
- Minimum binding: work/subject/evidence refs.
- Owner rule: historical learning evidence only; never Gate PASS (L2 §10).
- Wiring: fixed rule — Task Learning records are always `HISTORICAL_ONLY` for gate
  purposes; no wiring function may promote them.

### M10 — Proportional Dogfood Report (downstream dogfood candidate binding)

Exact refs (resolvable at the candidate; machine-checked by the kernel):

```text
docs/implementation/4.9.0/PRD.md#163-exact-candidate-binding
docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md#14-downstream-dogfood-evidence-architecture
```

- Owner meaning: `docs/implementation/4.9.0/PRD.md` §16 (downstream dogfood and measurement
  contract; §16.3 exact-candidate binding) + Frozen L2 §14 (downstream dogfood evidence
  architecture). Consumption/handoff: T-014 (release-consumable evidence only).
- Minimum binding (L2 §14 / PRD §16.3–16.8): exact ADS candidate/version, qualifying
  downstream repository, pinned authority refs, baseline vs selected workflows, mechanism
  matrix (`EXERCISED | NOT_EXERCISED` + proof refs), nonzero proportional delta,
  ambiguous-predicate fail-closed exercise, independent auditor identity, safety-negative
  evidence, `UNAUTHORIZED_GATE_OMISSION=0`, `STALE_PASS_TRANSFER=0`, `INDEPENDENCE_LOSS=0`,
  `CROSS_OWNER_REQUIREMENT_CANCELLATION=0`, `ADVERSE_TERMINAL_SUPPRESSION=0`, claim
  boundary for unexercised mechanisms.
- Owner rule: the report is Release evidence; it cannot authorize execution or Release
  Qualification; ADS candidate thaw/drift makes the report historical-only until the
  Release owner re-evaluates; baseline=selected with zero proportional delta is
  compatibility evidence only and cannot satisfy downstream generality.
- Wiring: exact-candidate match check => `BOUND_CURRENT` or `HISTORICAL_ONLY` (T06).

## 4. Generic routing rules (Frozen L2 §10, fixed)

```text
NO_OWNER_TRANSFER_RULE          => HISTORICAL_ONLY
UNKNOWN_BINDING                 => HISTORICAL_ONLY_OR_BLOCKED (fail-closed)
OWNER_FRESH_ONLY                => FRESH_EXECUTION_REQUIRED
MATERIAL_BINDING_CHANGE         => SUCCESSOR_ASSURANCE_REQUIRED
UNRESOLVED_ADVERSE_FINDING      => CARRY_FORWARD_UNTIL_DISPOSITION
```

These are routing dispositions of the wiring engine. They carry no verdict semantics;
the only way any gate is satisfied is an owner-issued verdict bound to the current
subject under the owner's own rule above.

## 5. Negative invariants bound by this map

```text
stale PASS onto current subject                     forbidden (M02/M03/M04/M05/M06/M08/M10; T01)
PASS transferred across material successor          forbidden — new/full or complete-delta Review (M04; T02)
unresolved finding erased by chronology/new SHA/PASS forbidden — carry-forward until disposition (M01/M04; T02)
impact decision minting a new PASS                  forbidden — reuse binds existing tuple only (M03; T03)
frozen-candidate mutation keeping old evidence current forbidden — thaw/invalidate chain (M05/M06; T04)
concern NOT_APPLICABLE/DEFERRED => version omission forbidden — no aggregation (M07; T05; registry F12)
dogfood report on drifted ADS candidate             historical-only (M10; T06)
currentness (BOUND_CURRENT/CURRENT) => PASS/READY   forbidden — registry F13–F16 (§2)
Task Learning evidence => Gate PASS                 forbidden (M09)
```

Violation of any invariant is a finding against the wiring, never repaired by weakening
an owner rule.

## 6. Fixture inventory (`fixtures/gate-currentness/`)

```text
owner_map.json             machine-readable M01–M10 rows (owner_ref, binding keys, rules); kernel asserts doc/fixture/repo agreement
stale_pass.json            T01 scenarios: stale PASS vs current subject (per owner row) + same-subject positive control
successor_chain.json       T02 scenarios: authorized repair, carried findings, per-finding outcomes, review-shopping negatives
impact_decisions.json      T03 scenarios: VALIDATION_IMPACT_DECISION reuse/deny classes (none-proven / affected / unknown / HEAD drift)
frozen_candidates.json     T04 scenarios: Hidden/Closeout/RQ fresh-only, §4 thaw chain, strengthened pack
release_applicability.json T05 scenarios: concern-vs-version non-aggregation, stale applicability fail-closed, fresh Release-owned decision
dogfood_binding.json       T06 scenarios: exact ADS candidate binding, thaw/drift historical-only, zero-delta boundary
assurance_binding.json     M01 consumption: §28.1 transition admissions on CURRENT/STALE/UNKNOWN + adverse finding between Dispatch and Claim
```

Test kernel: `scripts/test_v49_gate_currentness.py` (TEST_MATRIX T01–T07). The kernel is
Builder evidence only — it is not independent Validation and never a source of gate
verdicts.
