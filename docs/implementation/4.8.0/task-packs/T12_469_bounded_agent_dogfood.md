# T-012 Task Pack — #469 Task-Class / Bounded-Agent Dogfood

Status: **FINAL TASK PACK — JIT EXECUTION PACK REQUIRED**

Authority: Frozen Product blob `f26439580e00de6ed8b2e27d732a3095eb566219`; Frozen L2 blob `f88c85454e80101a0fdf56050e21f11a05279841`; Frozen Task DAG R2 blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc`; Issue #518; seed dogfood evidence #469, with current planning anchor `#469@5925124956`; native Issue Dependencies on #518 read back with `blocked_by=0,total_blocked_by=3` and T-004/#511, T-007/#513, T-008/#514 DONE.

```yaml
task_id: T-012
lane: 469-dogfood
dependencies: [T-004, T-007, T-008]
integration_target: version/v4.8.0
review_policy: required
validation_scope: exact-subject-evidence-integrity
validation_owner: independent-from-builder
l3_requirement: risk-scaled-required
evidence_matrix: required
agent_freedom_ceiling: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
execution_pack: JIT
```

## Scope

T-012 owns a bounded, evidence-only dogfood pass over #469 and its successor measured evidence. It tests whether a constrained Builder can consume a frozen Task Pack + risk-scaled L3 + JIT exact-base Execution Pack and produce a durable, inspectable evidence synthesis without widening authority.

T-012 may:

- bind exact source evidence identities from #469 and distinguish historical checkpoints from the latest consumed factual anchor;
- summarize actual bounded/local Builder runs only to the extent supported by pinned source evidence;
- record T-012's own execution observations: clarifications/escalations, edit/test loops, negative-oracle findings, contract/write-set drift findings, stale pack/base rebinds, elapsed/resource/cost fields only when actually observed;
- record independent Validation findings and later Fresh Review findings by reference after those gates occur;
- classify the outcome as `MORE_EVIDENCE`, `NO_CHANGE`, or an evidence-backed candidate for ordinary ADS evolution governance.

T-012 MUST NOT:

- treat #469 as pre-authorized standard truth;
- modify Frozen Product/L2/DAG, normative standards, schemas, execution/model-routing policy or completed upstream Task authority;
- introduce a blanket strong→low-cost routing rule, global Agent score, provider/model correctness ranking or economic optimizer;
- infer economic savings from planning-only evidence, incomparable samples, provider pricing assumptions or elapsed time alone;
- collapse Builder, Validator and Fresh Reviewer into one actor;
- turn a dogfood finding into an automatic ADS amendment.

A dogfood failure may falsify the current bounded-execution practice. It does not authorize the Builder to repair normative authority.

## Source-evidence boundary

The planning anchor is `#469@5925124956` (`L3_HYBRID_DOGFOOD_RESULT — MILESTONE 3`). It reports partially measured positive bounded execution across S00/C01/C02 and A01a, with A01b at validation/review-pending state at that checkpoint; it also keeps `ECONOMIC_SAVINGS=NOT_MEASURED`, rejects a blanket strong→low-cost rule and records continuing value from high-capability Fresh Review.

Earlier #469 comments remain historical evidence and may be cited when needed to explain candidate→validation→review→merge→stable-pointer progression, stale/currentness handling or dispatch gaps. A later successor comment discovered before Builder claim is material currentness input and requires explicit source-evidence rebind before execution; the Builder must not silently mix old and new source states.

Source-reported external executions are **referenced evidence**, not re-executed facts of T-012. T-012's own Builder/Validator/Reviewer facts must be recorded separately.

## Builder write set

Authorized Builder changes are exactly:

- `docs/implementation/4.8.0/dogfood/469/**`

Expected durable outputs:

- `docs/implementation/4.8.0/dogfood/469/EVIDENCE_MATRIX.md`
- `docs/implementation/4.8.0/dogfood/469/EXECUTION_OBSERVATIONS.md`
- `docs/implementation/4.8.0/dogfood/469/RESULT.md`

The Builder may add another file under the same directory only when it is strictly evidence-supporting and does not create new normative authority. No path outside this directory is in the Builder write set.

Read-only authority/reference inputs include Frozen Product/L2/DAG, this Task Pack, task-scoped L3, #469 exact source comments/PR/Issue references, T-004/T-007/T-008 evidence, `standards/EXECUTION_PACK_STANDARD.md`, `standards/MODEL_USAGE_POLICY.md`, `standards/EXECUTION_ARCHITECTURE_STANDARD.md` and current Review/Validation authority.

## Required evidence matrix

The Builder must materialize at least these bounded dimensions:

| ID | Dimension | Required oracle | Minimum posture |
|---|---|---|---|
| BDF-01 | source identity/currentness | every material #469 claim binds an exact Issue/comment/PR/commit ref; historical checkpoints are not presented as current | source-pinned |
| BDF-02 | actual bounded execution | source-reported S00/C01/C02/A01a/A01b status is represented without upgrading pending or limited gates | source-pinned |
| BDF-03 | Builder profile/provenance | provider/model identity is provenance only; execution profile/freedom is independently constrained by pack authority | T-012 observed + source-pinned |
| BDF-04 | clarification/escalation | counts are exact observed values or `NOT_MEASURED`; zero is not inferred from silence | source-pinned + T-012 observed |
| BDF-05 | edit/test loops | counts/ranges are retained with task/source attribution; no cross-task causal conclusion | source-pinned + T-012 observed |
| BDF-06 | negative oracle / drift | caught and uncaught findings are distinguished; green Builder/Validation does not imply no later Review findings | source-pinned |
| BDF-07 | stale pack/base/rebind | candidate/L3/JIT/base currentness events are recorded by exact ref; stale evidence never silently rebinds | source-pinned + T-012 currentness |
| BDF-08 | Validation/Review independence | Builder, Validator and Fresh Reviewer evidence remain distinct exact-subject gates | source-pinned + T-012 gate contract |
| BDF-09 | Review findings/rework | P0–P3 or equivalent findings/rework are recorded only where sourced; later Review value is not erased by earlier PASS | source-pinned |
| BDF-10 | time/resource/cost | only actually observed comparable fields are reported; missing token/cost/baseline fields remain `NOT_MEASURED` | fail-closed measurement |
| BDF-11 | T-012 bounded-agent behavior | own write-set adherence, freedom ceiling, clarification/escalation, loops, drift catches and stop/escalation behavior are recorded separately | T-012 observed |
| BDF-12 | disposition | `MORE_EVIDENCE`, `NO_CHANGE`, or evidence-backed evolution candidate follows the evidence and never mutates ADS automatically | evidence synthesis |

## Measurement rules

Required fields for each applicable source task and for T-012 itself:

```text
work_ref
builder_role_and_profile
provider_model_provenance_or_NOT_REPORTED
exact_base_or_subject_ref
pack_refs
clarifications
escalations
edit_test_loops
negative_oracle_failures_or_findings
contract_or_write_set_drift_findings
stale_pack_or_base_rebinds
validation_ref_and_result
fresh_review_ref_and_findings
rework_ref_or_NONE_REPORTED
elapsed_time_if_observed
resource_usage_if_observed
input/output_tokens_if_observed
cost_if_observed
measurement_limitations
```

`0`, `NONE`, `NOT_REPORTED`, `NOT_MEASURED`, `NOT_APPLICABLE` and `BLOCKED` are distinct. Missing evidence MUST NOT be normalized to zero.

Comparable economic claims require a declared comparison population/method, comparable task complexity and scope, comparable gate requirements, measured resource/time/cost fields and explicit limitations. Without that, the only permitted economic conclusion is:

```text
ECONOMIC_SAVINGS=NOT_MEASURED
```

## Required gates

Before Builder dispatch:

1. `version/v4.8.0` must still equal the exact JIT base bound by the Execution Pack;
2. native dependencies for #518 must remain `blocked_by=0` with T-004/#511, T-007/#513 and T-008/#514 DONE;
3. this Task Pack and `L3_T12_469_BOUNDED_AGENT_DOGFOOD.md` must be pinned by blob;
4. `.agent/execution/T-012/**` must bind base SHA/tree, source-evidence anchor, exact Builder write set, measurement/evidence matrices, failure handling, F1 freedom ceiling and independent Validation/Fresh Review posture;
5. #469 must be re-read at Builder claim: if a material successor to planning anchor `5925124956` exists, execution stops for explicit evidence-currentness rebind;
6. no `docs/implementation/4.8.0/dogfood/469/**` implementation/result path may be modified by Phase-1 Planning/JIT.

Builder closeout must bind exact base, Pack HEAD/tree, candidate HEAD/tree, exact diff, source anchors consumed and T-012's own measured fields. It must state `ECONOMIC_SAVINGS=NOT_MEASURED` unless a genuinely comparable measured methodology exists in the exact evidence set.

Required Validation is independent exact-subject evidence-integrity Validation. Fresh Independent Review occurs only after qualifying Validation and must independently re-read the exact current candidate and material source anchors. Builder, Validator and Reviewer identities remain distinct.

PR/Task PASS does not imply T-014, Version Closure, Release Qualification, Release PASS, or normative adoption of any dogfood observation.
