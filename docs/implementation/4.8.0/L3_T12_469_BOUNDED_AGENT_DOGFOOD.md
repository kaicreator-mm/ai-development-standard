# v4.8.0 T-012 L3 — #469 Task-Class / Bounded-Agent Dogfood

Status: **FINAL TASK-SCOPED L3 — JIT EXACT-BASE EXECUTION PACK REQUIRED**

Authority: Frozen Product blob `f26439580e00de6ed8b2e27d732a3095eb566219` + Frozen L2 blob `f88c85454e80101a0fdf56050e21f11a05279841` + Frozen Task DAG R2 blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc` + T-012 Task Pack blob `10168f6ea2a1cb3b0ffff9c1a493b0904d82942f` + Issue #518 + source dogfood evidence #469.

This L3 is bounded evidence-synthesis guidance. It does not authorize normative ADS edits, a new model-routing policy, a global Agent score, a savings claim, or Builder self-certification.

## Tests

The T-012 Builder produces evidence artifacts only under `docs/implementation/4.8.0/dogfood/469/**`. The exact candidate must satisfy all of the following checks before Builder closeout.

### T12-01 — exact source binding

Every material factual claim imported from #469 must carry a durable exact source identity: Issue comment, PR, commit/tree, Validation/Review comment or other exact reference where the source provides one. The planning anchor is #469 comment `5925124956`.

The Builder must distinguish:

```text
historical checkpoint
current consumed source anchor
source-reported external execution
T-012 Builder observation
future T-012 independent Validation
future T-012 Fresh Review
```

No source-reported execution is relabeled as an execution performed by T-012.

### T12-02 — source-currentness preflight

At Builder claim, re-read #469. If a material successor comment exists after `5925124956`, stop before authoring result content and request explicit evidence-currentness rebind. Do not silently combine planning-anchor facts with a newer source state.

This check is independent from Git integration-base currentness. Both must pass.

### T12-03 — actual bounded task outcomes

The evidence matrix must represent the actual statuses present in the consumed source. At planning time, #469@5925124956 reports:

- S00 — bounded Builder completed/merged, with independent Validation and Fresh Review;
- C01 — bounded Builder completed/merged, with independent Validation and Fresh Review;
- C02 — source reports completed/merged bounded work in its aggregate disposition;
- A01a — source reports completed bounded implementation path with later review findings;
- A01b — source anchor reports independent real-browser Validation complete while Fresh Review remained pending at that checkpoint.

The Builder must not upgrade any source status. If claim-time source reread changes these facts, stop for rebind rather than editing the planning contract ad hoc.

### T12-04 — measurement null semantics

The matrix must keep these states distinct:

```text
0
NONE_REPORTED
NOT_REPORTED
NOT_MEASURED
NOT_APPLICABLE
BLOCKED
```

A missing number is never normalized to zero. A source statement such as `CLARIFICATIONS=0` may be recorded as zero; silence may not.

### T12-05 — provider/model provenance boundary

Where #469 identifies a Builder model (for example, source-reported GLM-5.3-Flash runs), record it only as provenance. The candidate must contain no rule equivalent to:

```text
provider/model name -> correctness
provider/model name -> authority
provider/model name -> universal eligibility
bounded success -> all tasks should use lower-cost executor
```

T-012's own Builder identity/provider/model is recorded separately and receives no authority from its name.

### T12-06 — clarification/escalation and loop accounting

For every source task where the values are available, preserve exact clarification/escalation and edit/test-loop observations with work attribution. At planning time, the source includes repeated `CLARIFICATIONS=0` observations and reported edit/test-loop counts/ranges, but those are descriptive per-task observations only.

T-012 must also record its own:

```text
T012_CLARIFICATIONS
T012_ESCALATIONS
T012_EDIT_TEST_LOOPS
```

from the actual Builder session. Do not pre-fill these during Phase 1.

### T12-07 — negative-oracle and drift accounting

The matrix must distinguish:

- negative-oracle failures observed by Builder;
- contract/write-set drift caught before merge;
- stale pack/base/L3 rebinding events;
- later Validation findings;
- later Fresh Review P0/P1/P2/P3 findings and resulting rework.

A green Builder or Validation result must not erase later Review findings. Conversely, a later Review finding must not be rewritten as something the Builder had already caught unless the source explicitly says so.

### T12-08 — independence

For each consumed source task, Builder, Validator and Fresh Reviewer identities/results remain distinct when evidence exists. T-012 follows the same rule:

```text
Phase-2 Builder != independent Validator != Fresh Reviewer
```

No Builder-authored `RESULT.md` may claim T-012 Validation PASS or Fresh Review PASS.

### T12-09 — exact-base / pack currentness

Before material work, the Builder must verify:

```text
current version/v4.8.0 SHA == Execution Pack base_sha
Task Pack blob == bound Task Pack blob
L3 blob == bound L3 blob
branch == bound JIT branch
native #518 blockers == 0
```

Any mismatch stops execution for rebind. No silent base rewrite.

### T12-10 — write-set oracle

The eventual candidate diff after the Pack HEAD must contain only:

```text
docs/implementation/4.8.0/dogfood/469/**
```

Any need to touch `standards/**`, `schemas/**`, Frozen Product/L2/DAG, another Task Pack/L3, CI/workflows or release authority is out of scope and must stop.

### T12-11 — economics/comparability oracle

A savings/economic conclusion requires all of:

```text
declared comparison population
comparable task class / complexity / scope
comparable gate requirements
measured elapsed/resource fields
measured token/cost fields where cost is asserted
method that separates observed fact from provider-price assumption
limitations / confounders
```

If these are not all present in the consumed exact evidence, `RESULT.md` must state:

```text
ECONOMIC_SAVINGS=NOT_MEASURED
```

Elapsed time alone does not prove cost savings. A bounded model completing a task does not prove it was economically superior to a strong-model control.

### T12-12 — disposition oracle

`RESULT.md` must end in exactly one evidence-governance posture:

```text
MORE_EVIDENCE
NO_CHANGE
ADS_EVOLUTION_CANDIDATE
```

`ADS_EVOLUTION_CANDIDATE` means only a candidate entering ordinary ADS Intake/L1/PRD/L2 governance. It is not authorization to edit normative authority in T-012.

### Required repository checks

The Builder must record exact command results for:

```text
git diff --check <PACK_HEAD>...HEAD
git diff --name-only <PACK_HEAD>...HEAD
python -B scripts/verify_standard.py
```

The first two prove bounded candidate hygiene/write-set. `verify_standard.py` is repository conformance only; it does not independently validate the factual accuracy of #469 synthesis.

Independent Validation must additionally re-read the exact #469 source anchor/current successor state and challenge material factual bindings against the exact candidate.

## Contract

### 1. T-012 is evidence synthesis, not authority promotion

The Builder consumes evidence and produces a bounded evidence record. It does not change Product/L2/DAG, model routing, Execution Pack semantics, Agent capability semantics or Review/Validation ownership.

The governing hierarchy remains:

```text
Frozen Product
> Frozen L2
> Frozen Task DAG
> T-012 Task Pack
> T-012 Execution Contract
> bounded Builder evidence synthesis
```

A contradictory need routes upward; it is not resolved by widening the Builder's interpretation.

### 2. F1 freedom ceiling

The Builder freedom ceiling is `F1_BOUNDED_IMPLEMENTATION`:

- evidence table organization and concise wording may vary;
- exact source identities, measurement semantics, authority boundaries, output directory, required fields and negative oracles are fixed;
- the Builder may not invent missing measurements, redesign the experiment, reinterpret policy, or widen scope;
- material ambiguity about a source claim, source-currentness, comparability, authority or write-set requires escalation.

This Task should be dispatched to a bounded/lower-cost Builder only if current eligibility evidence supports the required role/profile. Provider/model identity by itself is insufficient eligibility proof. If no eligible bounded Builder exists, use an eligible stronger Builder without changing the Task's F1 authority ceiling.

### 3. Source evidence is pinned, but may become stale

The Phase-1 planning anchor is `ai-development-standard#469@5925124956`. It is an exact historical fact, not an immutable declaration that no successor evidence will appear.

At Builder claim:

- no material successor -> anchor remains current consumed source for this run;
- material successor exists -> stop and request source-evidence rebind;
- source cannot be read/verified -> `BLOCKED_SOURCE_CURRENTNESS`, not guessed continuation.

This is separate from repository `PACK_CURRENT` classification.

### 4. Evidence layers remain separate

For T-012 purposes, use these non-normative evidence labels only inside the dogfood result:

```text
SOURCE_PINNED_FACT
SOURCE_REPORTED_VALIDATED_REVIEWED
T012_BUILDER_OBSERVED
T012_INDEPENDENT_VALIDATION
T012_FRESH_REVIEW
NOT_REPORTED
NOT_MEASURED
BLOCKED
```

These labels are local presentation aids, not a new ADS machine-contract family.

### 5. Required source facts from the planning anchor

The Builder may use the following only with exact source refs and claim-time currentness PASS:

- #469 records real bounded lower-cost implementation work beyond the earlier planning-only stage;
- S00 and C01 include source-reported GLM-5.3-Flash Builder provenance, zero clarifications, bounded edit/test loops, independent Validation PASS and Fresh Review PASS before separate Controller merge;
- aggregate #469 disposition reports completed merged lower-cost S00/C01/C02 plus A01a bounded implementation path, while A01b had reached Validation with Review pending at that checkpoint;
- #469 states `ACTUAL_LOW_COST_IMPLEMENTATION_OUTCOME=PARTIALLY_MEASURED_POSITIVE_EXECUTION`;
- #469 states `ECONOMIC_SAVINGS=NOT_MEASURED`;
- #469 states `BLANKET_STRONG_TO_LOW_COST_RULE=NOT_SUPPORTED`;
- #469 records `HIGH_CAPABILITY_REVIEW_VALUE=OBSERVED`, based on nonblocking but material findings after green Builder/Validation work;
- input-pack token size and comparable end-to-end cost baselines remain largely not measured.

These are dogfood observations, not normative rules.

### 6. T-012 self-dogfood

T-012 itself is part of the evidence:

- Builder profile and provider/model provenance, if available;
- whether an eligible bounded execution profile was used;
- exact Task Pack/L3/JIT Pack identities;
- exact base and Pack HEAD;
- clarification/escalation count;
- edit/test-loop count;
- write-set or source-currentness drift caught;
- negative-oracle failures/findings;
- elapsed/resource/tokens/cost only when observed;
- independent Validation findings;
- Fresh Review findings/rework.

The Phase-2 Builder records only its own execution facts and leaves Validation/Review fields pending.

### 7. No economic or universal routing inference

The Builder may describe observed task outcomes. It may not infer:

```text
lower-cost model success -> lower total cost
lower-cost model success -> same quality as strong model in general
zero clarifications -> no strong-model value
Validation PASS -> Fresh Review unnecessary
one project/task class -> universal routing rule
provider name -> capability truth
```

Cross-task/cross-project economic or causal claims require comparable methodology beyond the current source evidence.

## Implementation

The Builder creates only evidence artifacts under `docs/implementation/4.8.0/dogfood/469/**`.

### `EVIDENCE_MATRIX.md`

Must contain one row for every BDF-01..BDF-12 dimension and, where source evidence supports it, per-work rows for S00, C01, C02, A01a and A01b.

Minimum columns/fields:

```text
row_id
work_or_dimension_ref
source_ref
source_subject_sha_tree_or_NOT_REPORTED
builder_profile_provenance_or_NOT_REPORTED
exact_pack_base_ref_or_NOT_REPORTED
clarifications
escalations
edit_test_loops
negative_oracle_findings
contract_write_set_drift
stale_rebinds
validation_ref_result
fresh_review_ref_findings
rework_ref_or_NONE_REPORTED
elapsed_time
resource_usage
tokens
cost
evidence_label
limitations
```

### `EXECUTION_OBSERVATIONS.md`

Must record T-012's own bounded execution separately from source tasks:

```text
T012_BASE_SHA/TREE
T012_PACK_HEAD/TREE
T012_BUILDER_PROFILE
T012_PROVIDER_MODEL_PROVENANCE_OR_NOT_REPORTED
T012_AGENT_FREEDOM=F1_BOUNDED_IMPLEMENTATION
T012_CLARIFICATIONS
T012_ESCALATIONS
T012_EDIT_TEST_LOOPS
T012_NEGATIVE_ORACLE_FINDINGS
T012_WRITE_SET_DRIFT_FINDINGS
T012_SOURCE_CURRENTNESS_REBINDS
T012_BASE_REBINDS
T012_ELAPSED_TIME_IF_OBSERVED
T012_RESOURCE_USAGE_IF_OBSERVED
T012_TOKENS_IF_OBSERVED
T012_COST_IF_OBSERVED
T012_VALIDATION=PENDING
T012_FRESH_REVIEW=PENDING
```

Do not manufacture measurements solely to fill the template.

### `RESULT.md`

Must synthesize:

1. exact evidence scope and source anchors;
2. what the evidence supports;
3. what it does not support;
4. counterevidence and Fresh Review value;
5. measurement/comparability gaps;
6. T-012's own bounded-execution observation status;
7. one allowed disposition (`MORE_EVIDENCE`, `NO_CHANGE`, `ADS_EVOLUTION_CANDIDATE`);
8. explicit non-adoption boundary.

If economic comparability remains absent, include `ECONOMIC_SAVINGS=NOT_MEASURED` verbatim.

## Failure Handling

- `version/v4.8.0` differs from Execution Pack base at claim -> `PACK_STALE_MATERIAL`; stop for JIT rebind.
- Task Pack or L3 blob differs from bound identity -> `PACK_INVALID`/rebind; stop.
- #518 gains an active blocker -> stop; do not execute from prose readiness.
- #469 has a material successor after planning anchor -> `BLOCKED_SOURCE_CURRENTNESS` until explicit evidence-currentness rebind.
- #469 source cannot be inspected when required -> `BLOCKED_SOURCE_CURRENTNESS`; never guess.
- material source claim lacks exact support -> record `NOT_REPORTED`/limitation or omit the claim; do not infer.
- missing measurement -> `NOT_MEASURED`/`NOT_REPORTED`; never zero-fill.
- Builder needs to edit outside `docs/implementation/4.8.0/dogfood/469/**` -> stop for pack/task-owner decision.
- Builder proposes normative standard/schema/model-policy changes -> stop; only evidence disposition may point to ordinary ADS evolution governance.
- provider/model identity used as correctness/authority/universal eligibility -> blocking evidence-integrity failure.
- source task success converted into blanket strong→low-cost rule -> blocking scope failure.
- incomparable data converted into savings claim -> blocking measurement-integrity failure.
- Builder collapses Validation or Fresh Review into self-attestation -> blocking independence failure.
- later Review findings omitted to preserve a positive narrative -> blocking evidence-integrity failure.
- historical pending state upgraded without successor evidence -> blocking currentness failure.
- T-012 result merges source observations and its own execution measurements without attribution -> blocking provenance failure.
- any material candidate drift after Validation/Review -> affected evidence becomes stale and must requalify.

## Evidence matrix / review handoff

The independent Validator must verify the exact candidate and at least:

- base/Pack currentness and ancestry;
- diff is entirely inside the Builder write set;
- BDF-01..BDF-12 completeness;
- exact #469 source refs for material claims;
- no status upgrades relative to the consumed source anchor;
- null/zero measurement semantics;
- no unsupported economic, causal or universal routing conclusion;
- T-012 own Builder observations are separated from source evidence;
- `python -B scripts/verify_standard.py` and diff hygiene results;
- Builder did not self-claim Validation/Review.

After qualifying Validation, a genuinely Fresh Independent Reviewer must re-read the exact current candidate and source anchors, challenge the evidence interpretation, examine counterevidence/review findings, and decide only the PR/Task review verdict. That Reviewer does not automatically authorize a normative ADS change.

## Reference

- Frozen Product: `docs/implementation/4.8.0/PRD.md` blob `f26439580e00de6ed8b2e27d732a3095eb566219`
- Frozen L2: `docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md` blob `f88c85454e80101a0fdf56050e21f11a05279841`
- Frozen DAG R2: `docs/implementation/4.8.0/TASK_DAG.md` blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc`
- T-012 Task Pack: `docs/implementation/4.8.0/task-packs/T12_469_bounded_agent_dogfood.md` blob `10168f6ea2a1cb3b0ffff9c1a493b0904d82942f`
- Task: #518 / T-012
- Upstream tasks: T-004/#511, T-007/#513, T-008/#514
- Dogfood seed: #469, planning anchor comment `5925124956`
- Execution Pack authority: `standards/EXECUTION_PACK_STANDARD.md`
- Model routing authority: `standards/MODEL_USAGE_POLICY.md`
