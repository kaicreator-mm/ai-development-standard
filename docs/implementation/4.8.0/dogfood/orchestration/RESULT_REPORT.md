# T-011 Orchestration Dogfood — Result Report

Task: T-011 / Issue #517 · Builder phase 2 + Phase-5 bounded P1 repair · branch `task/v4.8.0-t11-orchestration-dogfood` · PR target `version/v4.8.0`

## Identity

- Exact base: `94955c6f93fd7316406ea96bce8f7c32a62509ef` / tree `bb7f25f1e05ff2423fc79029465bcf7be458a82c`
- JIT Execution Pack HEAD: `26fdae3dd2b4a686820637665ee6f30811543b1f` / tree `dc2fafc5c1433db23423a49c22c0250a0adc88b6`
- Candidate: bound by the harness at run time (`candidate_head_sha` / `candidate_head_tree` in the emitted evidence JSON) and durably in the repair terminal + PR head
- Write set actually touched: `scripts/test_v48_orchestration_dogfood.py`; `docs/implementation/4.8.0/dogfood/orchestration/README.md`; `docs/implementation/4.8.0/dogfood/orchestration/EVIDENCE_MATRIX.md`; `docs/implementation/4.8.0/dogfood/orchestration/RESULT_REPORT.md`; `docs/implementation/4.8.0/dogfood/orchestration/fixtures/scenario_manifest.json`; `docs/implementation/4.8.0/dogfood/orchestration/fixtures/t011_builder_claim_event.json`

## Phase-5 bounded P1 repair (this revision)

Fresh Independent Review of candidate `fdd6b30d6736586e15f2396ab9fafeb0a690c08f` returned `CHANGES_REQUESTED` with P1=1 (#517@5966240519): ODF-01 eligibility was derived from the fixture-only `scheduling_oracle_capabilities` shadow field while `required_role_claim` did not participate, so wrong-role and unclaimed-capability candidates were not falsified. Per the Phase-5 repair dispatch (#517@5966292564), this revision:

1. derives hard-eligibility inputs only from canonical `agent-capability-profile-v1` documents — `eligible_role_claims` (`role:*` tokens), `reasoning_or_semantic_capability_claims` (claimed capabilities) and `max_agent_freedom_claim` (`freedom_le:*` tokens composed against the work item's `required_max_agent_freedom`, bound to the real MANIFEST `task_pack_agent_freedom_ceiling`);
2. removed the `scheduling_oracle_capabilities` shadow field from the corpus (corpus version 2) so no non-canonical capability authority exists;
3. added negative scenarios **ODF-19** (wrong-role candidate cannot reach ranking/admission, with a role-conforming control) and **ODF-20** (unclaimed-capability candidate cannot reach ranking/admission, falsifying the exact drift the review identified);
4. composed everything through the merged T-008 oracle's existing opaque capability-token subset predicate — no new scheduler/admission rule, T-007/T-008/T-009/T-017 owners preserved unchanged.

The pre-existing non-blocking P3 (Execution Pack L3 citation) is **not** repaired here: `.agent/execution/T-011/**` is outside the Phase-5 repair write set.

## Scenario summary (ODF-01..ODF-20)

All 20 scenarios PASS on the repaired candidate (ODF-01..ODF-18 Task Pack/L3 corpus + ODF-19/ODF-20 repair negatives). Per-row detail, inputs, oracles, observed results, evidence classes and limitations: see `EVIDENCE_MATRIX.md`. The harness re-emits the machine-readable registry (`scenario_id`, `name`, `oracle`, `observed_result`, `evidence_class`, `environment`, `limitations`) between the `T011_ORCHESTRATION_DOGFOOD_EVIDENCE_JSON_BEGIN/END` markers on every run, together with the exact candidate SHA/tree it executed against.

Layer composition: eligibility/ranking and resource admission reuse the merged T-008 oracle module; replay/restart/reconstruction reuse the merged T-009 oracle module; claim/start-record/ownership reuse the merged T-017 oracle module; subject currentness reuses the merged T-007 oracle module. No normative semantics were redefined, no new scheduler/admission lifecycle, no new Exchange family, no new Availability authority, no mandatory runtime database.

## Commands and results

Filled with the actual observed results of the Builder run on the candidate; re-run to reproduce.

```text
python -B scripts/test_v48_orchestration_dogfood.py
python -B scripts/test_v48_contract_compatibility.py
python -B scripts/test_v48_scheduling_conformance.py
python -B scripts/test_v48_interchange_replay_restart.py
python -B scripts/test_v48_execution_ownership.py
python -B scripts/verify_standard.py
```

Exact exit codes / test counts are recorded in the Builder terminal comment for the candidate commit.

## Evidence-class accounting

- `SYNTHETIC_DETERMINISTIC`: ODF-02, ODF-05, ODF-06, ODF-07, ODF-08, ODF-13 (+ composite component of ODF-01/03/04/14/15/16/19/20)
- `REPOSITORY_REAL_EXECUTION`: ODF-09, ODF-10, ODF-11, ODF-12, ODF-17, ODF-18 (+ repository component of ODF-01/03/04/14/15/16/19/20)
- `REAL_HOST_OR_RUNTIME_VALIDATION`: **not executed, not claimed**
- `NOT_RUN`: real host/runtime restart; real GitHub transport delivery of escalation events; real provider-backed bounded-executor generation step; real webhook/queue transport — all require independent exact-subject environment Validation before any such claim
- `BLOCKED`: none at repair time

## Falsification observations

- The Phase-4 Fresh Review P1 was confirmed and is now falsified-as-repaired: before the Phase-5 repair, a wrong-role or unclaimed-capability candidate could reach eligibility through the fixture-only shadow field; after the repair (ODF-19/ODF-20) both stay hard-INELIGIBLE before ranking/admission, and the corpus contains no shadow capability authority.
- No scenario falsified the already-merged v4.8 semantics on this candidate: hard eligibility stayed before ranking; stale/missing Availability stayed fail-closed; capacity-N/N=1 and composite all-or-none invariants held; independence stayed a hard filter; replay stayed idempotent and conflicting replay failed closed; transport facts never became workflow truth; reconstruction never needed transient history; the accepted Claim remained the only Start Record and ambiguous replacement stayed blocked; the bounded executor succeeded only inside its write set and escalated on all three ambiguity probes.
- Non-blocking Phase-1 observation (P3, unchanged, outside this repair write set): `.agent/execution/T-011/EXECUTION_CONTRACT.md` cites L3 blob `9d40ed242b146a54b9ccbf39fe0a85fc2efcfac6`, the pre-correction draft; the canonical L3 blob per the Phase-1 dispatch terminal, `MANIFEST.yaml` and the live git object is `fe7e1c46bcaef45cb7c8ce57615dcf0f1e0feb1a`. No semantic impact (the bound L3 content is the corrected one).

## Boundary of this report

- Measurements in this dogfood are **descriptive only** of this deterministic run. They support **no universal Agent ranking**, **no blanket strong-to-low-cost routing** and **no savings claim**; ranking inputs in the corpus are explicit rank tuples only, and provider/model provenance is identity provenance, never authority.
- The Phase-3 Validation (PASS) and Phase-4 Fresh Review (`CHANGES_REQUESTED` → this repair) are historical to the pre-repair candidate `fdd6b30d6736586e15f2396ab9fafeb0a690c08f`. Independent exact-subject scenario/integration Validation of **this repaired candidate** has **not** been performed and is not claimed (`NOT_RUN` until a successor independent Validator qualifies the exact repaired SHA/tree); a genuinely new Fresh Independent Review is **PENDING** and permitted only after that qualifying Validation.
- A PR/Task PASS would authorize T-011 concern completion/integration only; it implies nothing about T-014, Version Closure, Release Qualification or Release PASS.
