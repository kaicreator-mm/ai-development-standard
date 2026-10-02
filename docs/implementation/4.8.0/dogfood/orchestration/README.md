# v4.8 T-011 — Heterogeneous Multi-Agent / Resource / Transport Dogfood

Bounded dogfood of the already-merged v4.8 orchestration semantics (T-007 contract compatibility, T-008 scheduling/resources, T-009 interchange replay/restart, T-017 execution ownership) over one deterministic scenario corpus. Issue #517.

## Contents

- `EVIDENCE_MATRIX.md` — ODF-01..ODF-18 scenario/evidence matrix (inputs, oracles, observed results, evidence classes, limitations)
- `RESULT_REPORT.md` — run/report, evidence-class accounting, falsification observations, explicit NOT_RUN/BLOCKED external dimensions
- `fixtures/scenario_manifest.json` — deterministic corpus (profiles, work items, availability, resources, subject identities, T-011 ownership facts)
- `fixtures/t011_builder_claim_event.json` — verbatim durable copy of the accepted Builder Claim event (durable original: Issue #517 comment)

## Run

```bash
python -B scripts/test_v48_orchestration_dogfood.py
```

The harness imports the merged upstream conformance oracle modules (no normative semantics are redefined), executes the ODF-01..ODF-18 corpus, and emits a machine-readable evidence registry (including the exact candidate SHA/tree it executed against) between the `T011_ORCHESTRATION_DOGFOOD_EVIDENCE_JSON_BEGIN` / `_END` markers.

## Evidence boundary

`SYNTHETIC_DETERMINISTIC` rows prove bounded reference-model semantics only; `REPOSITORY_REAL_EXECUTION` rows executed against real repository artifacts at the candidate checkout; no `REAL_HOST_OR_RUNTIME_VALIDATION` dimension was executed or claimed — external host/device/provider/runtime claims require independent exact-subject Validation and remain `NOT_RUN`/`BLOCKED` until then. Measurements are descriptive only: no universal Agent ranking, no blanket strong-to-low-cost routing, no savings claim.

This directory and `scripts/test_v48_orchestration_dogfood.py` are the entire T-011 Builder write set; authority files (PRD/L2/DAG, standards, schemas, upstream task packs) are read-only inputs.
