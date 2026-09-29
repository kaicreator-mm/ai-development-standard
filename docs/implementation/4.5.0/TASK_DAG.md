# v4.5.0 Task DAG — Operations, Incident & Maintenance

Status: **FROZEN TASK DAG — 2026-09-30**

Freeze inputs:

- Frozen Product Authority: `5581fb411647dfeca0aae1e9ef6e66a7dfd795f4`
- Frozen L2 Architecture: `docs/implementation/4.5.0/L2_ARCHITECTURE_EVIDENCE.md`
- v4.4 Frozen Product/L2 deployment boundary

## 1. DAG

```text
T01 Shared Operations Machine Contracts
        │
        ├──────────────┬────────────────┐
        ▼              ▼                ▼
T02 Observability   T03 Incident,     T04 Maintenance,
& Runtime Evidence  Recovery &        EOL & Hotfix
                    Feedback
        │              │                │
        ▼              │                ▼
T05 Runtime           │          T07 Maintenance/Hotfix
Observation           │          Conformance/Dogfood
Conformance           │
        └──────┬───────┘
               ▼
       T06 Incident/Feedback
       Conformance/Dogfood

T02 ────────────────┐
T03 ────────────────┼→ T08 Adoption & Cross-standard Wiring
T04 ────────────────┘

T05 ────────────────┐
T06 ────────────────┼→ T09 Cross-standard Conformance / Closure Inputs
T07 ────────────────┤
T08 ────────────────┘
                             │
                             ▼
                      Version Closure
```

Expected dependency edges:

```text
T02 blocked by T01
T03 blocked by T01
T04 blocked by T01
T05 blocked by T02
T06 blocked by T02 + T03
T07 blocked by T04
T08 blocked by T02 + T03 + T04
T09 blocked by T05 + T06 + T07 + T08
```

## 2. Task definitions

### T01 — Shared Operations Machine Contracts
Own only:
- `schemas/runtime-observation-context-v1.schema.json`
- `schemas/incident-event-v1.schema.json`
- `schemas/maintenance-policy-v1.schema.json`
- narrowly justified optional refs in existing evidence contracts
- focused schema/backward-compatibility tests

No normative operations policy or lifecycle/Gate state.

### T02 — Observability & Runtime Evidence
Own one normative standard + reference + focused tests for signal semantics, exact runtime observation identity/correlation and privacy/secret boundary. No universal telemetry stack/SLO/severity constants and no runtime-health Gate state.

### T03 — Incident, Recovery & Engineering Feedback
Own incident event semantics, mitigation/recovery/verification/follow-up distinctions and deterministic incident→engineering feedback routing. It references v4.4 Deployment and v4.2 Migration recovery, never redefines them.

### T04 — Maintenance, EOL & Hotfix
Own support-line policy, deprecation/EOL truth, maintenance Fast Path and backport/hotfix exact-subject provenance semantics. Branch/tag existence is not support authority; source PASS never transfers to backported SHA.

### T05 — Runtime Observation Conformance
Own conformance fixtures for runtime identity/signal dimensionality/privacy boundaries. Static/simulated evidence may cover contract logic; any claim requiring a real runtime/telemetry environment requires exact-environment Validation.

### T06 — Incident / Feedback Conformance & Dogfood
Own at least one controlled incident exercise covering detection → mitigation/recovery → verification → regression/follow-up. No new normative owner. Real side effects require explicit authority/handoff.

### T07 — Maintenance / Hotfix Conformance & Dogfood
Own at least one maintenance/backport case proving support policy authority and new exact-SHA testing/Validation for the backported result. Do not reuse source-branch PASS.

### T08 — Adoption & Cross-standard Wiring
Own manifest/project override/adoption/checklist/migration wiring only. Preserve v4.1/v4.2/v4.4 and existing Testing/Validation/Release owners.

### T09 — Cross-standard Conformance / Closure Inputs
Own integrated negative-inference regressions, historical compatibility, Fast Path proportionality and durable closure inputs. No Version Closure verdict itself.

## 3. Native Issue dependency graph

After materialization, GitHub Issue Dependencies become the canonical live execution DAG; this file remains frozen planning/history authority. T01 is the single initial implementation root.

Task branches are JIT from current `version/v4.5.0` only after native blockers are satisfied.

## 4. Integration target

Planning authority integrates first. Create `version/v4.5.0` only after planning PR Fresh Independent Review PASS and canonical integration.

All implementation PRs target `version/v4.5.0`; one concern per PR. Stacked PR is allowed only for real unmerged code-baseline dependency, never as the Task DAG authority.

## 5. Review / Validation posture

- T01–T04: required concern Validation + Fresh Independent Review.
- T05: required Review; Validation binds only the runtime/signal dimensions actually executed.
- T06: required Review and exact-environment Validation for any real incident/recovery side effects.
- T07: required Review and result-SHA Validation for backport/hotfix dogfood.
- T08: required integration Validation + Fresh Independent Review.
- T09: required integration/closure-input Validation + Fresh Independent Review.

CI/model agreement does not substitute for required real runtime/hotfix evidence.

## 6. Risk / executor posture

| Task | Risk | Default executor suitability |
|---|---|---|
| T01 | high | bounded implementation agent after Frozen L2 |
| T02 | high | bounded normative implementation + fresh reviewer |
| T03 | high | high-capability review due multi-owner recovery/feedback boundary |
| T04 | high | bounded implementation + exact identity/release-aware reviewer |
| T05 | medium-high | repository/CI executor; local/external validator only when real runtime proof required |
| T06 | high | controlled simulator/validator; real side effects require explicit authority |
| T07 | high | Git/maintenance-aware builder + exact-SHA validator |
| T08 | high | central integration builder + reviewer |
| T09 | high | integration validator/reviewer |

## 7. Local environment posture

Planning and T01–T04 are repository/Web/CI executable by default. T05 may remain fixture-driven if no real runtime claim is made. T06/T07 are the likely real-environment gates when incident recovery or backport tooling must actually execute.

Unavailable required environment/access is `BLOCKED`/`NOT_RUN` with an exact-scope Validation Request; never inferred PASS.

`LOCAL_ENV=NOT_REQUIRED` at Task DAG Freeze.