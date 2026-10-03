# T-010 Implementation Map

Read first, in order:

1. `docs/implementation/4.8.0/task-packs/T10_governance_conformance.md`
2. `docs/implementation/4.8.0/L3_T10_GOVERNANCE_CONFORMANCE.md`
3. Frozen DAG R2 T-010 definition and Issue #516 native blocker readback
4. `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`
5. `schemas/task-learning-v1.schema.json`
6. `scripts/test_v48_task_learning.py`
7. T-004 closeout/wiring surfaces and `scripts/test_work_item_contract_and_golden_templates.py`
8. `standards/DEVELOPMENT_WORKFLOW.md` §8
9. `scripts/test_v48_ads_evolution_governance.py`

Implement exactly one path:

- `scripts/test_v48_governance_conformance.py`

## Focused conformance design

Create deterministic scenario records and small pure evaluation helpers that model only the already-owned boundaries needed for the oracle. The focused test must independently assert outcomes; do not implement a second production governance engine or merely search for strings.

### Learning scenarios

Represent at least:

- literal `TASK_LEARNING=NONE_MATERIAL`;
- one valid material Task Learning record with exact immutable subject/currentness and durable evidence/authority refs;
- stale successor subject;
- missing/mutable/malformed/ambiguous subject identities;
- bounded confidence layers;
- friction classification/disposition as non-authoritative metadata.

Reuse repository schema validation helpers where useful. Keep the schema/reference read-only.

### Governance scenarios

Represent all six canonical observation classes. Assert that the first four route to their existing owners, `STANDARD_FRICTION_CANDIDATE` only reaches `NO_CHANGE`/`MORE_EVIDENCE`, and `ADS_EVOLUTION_CANDIDATE` only reaches `OPEN_ADS_INTAKE` followed by ordinary governance.

Include counterexamples where count/score/rate/cost/latency/provider/model/scheduler/heuristic signals attempt promotion; all must fail.

### Privacy/publication scenarios

Represent `PROJECT_PRIVATE`, `RESTRICTED`, `PUBLISHABLE` and missing classification. Publication must fail closed without explicit `PUBLISHABLE`. Even a publishable observation must reject secret/credential/private-CoT/hidden-evaluator payload material. Prefer refs/digests/minimized summaries in the accepted path.

### Owner boundary scenarios

Explicitly reject any derived outcome that tries to turn Task Learning/governance evidence into Product/L2/Task/ADR/Incident/Intent/Skill/Review/Validation/merge/release authority.

## Implementation constraints

The focused test MAY read current normative owner files to prevent documentation/oracle divergence, but it MUST NOT mutate them. It SHOULD use inline deterministic fixtures. If a separate fixture/reference path becomes necessary, STOP with `CONTROLLER_REBIND_REQUIRED` before adding it.

Do not create new classification names, publication classes, confidence layers, promotion states or lifecycle owners. Use the canonical vocabulary from T-004/T-005/T-001.

Required commands:

```text
python -B scripts/test_v48_governance_conformance.py
python -B scripts/test_v48_task_learning.py
python -B scripts/test_v48_ads_evolution_governance.py
python -B scripts/test_work_item_contract_and_golden_templates.py
python -B scripts/verify_standard.py
```

If any requirement cannot be proven inside this one-path write set without changing upstream owner semantics, STOP with `ARCHITECTURE_AMENDMENT_REQUIRED` or an explicit upstream-owner repair request rather than weakening the oracle.
