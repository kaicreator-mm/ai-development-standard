# v4.5.0 L3 Reference Packs — Operations, Incident & Maintenance

Status: **FROZEN IMPLEMENTATION REFERENCE — 2026-09-30**

Authority inputs:
- Frozen Product: `5581fb411647dfeca0aae1e9ef6e66a7dfd795f4`
- Frozen L2: `docs/implementation/4.5.0/L2_ARCHITECTURE_EVIDENCE.md`
- Frozen Task DAG: `docs/implementation/4.5.0/TASK_DAG.md`

Each Task uses **Tests → Contract → Implementation → Failure Handling → Reference**. L3 is subordinate to Product/L2/Task Pack and may not broaden authority.

## T01 — Shared Operations Machine Contracts
**Tests:** repository-supported Draft 2020-12; positive observation/incident/maintenance examples; historical payload compatibility; no Validation/Release PASS fields; incident append-history negatives; support branch/tag non-authority; secret/PII leakage field negatives.

**Contract:** exactly the three default families selected by L2: Runtime Observation Context, Incident Event, Maintenance Policy.

**Implementation:** compact schemas using current supported subset; optional refs only when backward-compatible.

**Failure Handling:** unsupported schema keyword or lifecycle-state pressure fails closed; repair schema, never weaken verifier.

## T02 — Observability & Runtime Evidence
**Tests:** Deployment SUCCESS cannot imply runtime health; health/readiness/liveness/business dimensions stay distinct; telemetry existence/absence cannot manufacture product truth; exact runtime subject/window required when material; secret/PII constraints.

**Contract:** technology-neutral runtime signal semantics and evidence identity/correlation only; no telemetry backend mandate or runtime-health Gate.

**Implementation:** one standard, one reference, focused tests; map OpenTelemetry/SRE concepts as examples, not requirements.

**Failure Handling:** project-specific SLO/severity/retention values remain project authority; unavailable signal source is not positive evidence.

## T03 — Incident, Recovery & Engineering Feedback
**Tests:** DETECTED != MITIGATED; RECOVERED != VERIFIED; VERIFIED != follow-up complete; incident events cannot rewrite prior Release/Deployment; recovery refs preserve v4.4/v4.2 ownership; follow-up routes to normal engineering work.

**Contract:** append-oriented incident facts + deterministic incident→reproduction/regression/scenario/product/architecture/standard feedback path.

**Implementation:** standard/reference/tests consuming T01 Incident Event.

**Failure Handling:** unknown authority/production side effect blocks mutation; recovery without required verification/follow-up remains explicit.

## T04 — Maintenance, EOL & Hotfix
**Tests:** branch/tag/package != support status; support line/baseline/change classes explicit; cherry-pick/backport != Validation transfer; urgency != truth waiver; maintenance Fast Path preserves required gates.

**Contract:** support-line policy and exact-subject hotfix/backport provenance semantics, consuming Git/Validation/Release authority rather than duplicating them.

**Implementation:** standard/reference/tests consuming Maintenance Policy.

**Failure Handling:** unclear support authority or baseline fails closed; backport result needs its own current evidence.

## T05 — Runtime Observation Conformance
**Tests:** observation subject/window binding; signal dimensionality; silence/availability negatives; privacy/secret-safe refs; historical compatibility.

**Contract:** conformance-only; no new owner.

**Implementation:** fixture/simulation may prove contract logic. Real runtime claims require exact environment/artifact/deployment tuple.

**Failure Handling:** required real telemetry/runtime unavailable => Validation Request/BLOCKED, not simulated PASS.

## T06 — Incident / Feedback Conformance & Dogfood
**Tests:** controlled detection→mitigation/recovery→verification→follow-up flow; failure paths for missing verification, unresolved follow-up, wrong recovery owner, secret evidence leakage.

**Contract:** conformance/dogfood only.

**Implementation:** simulated incident is acceptable if Product acceptance does not require real production side effects; any real system mutation needs explicit authority.

**Failure Handling:** unavailable required environment/authority => exact-scope handoff; no credential-presence inference.

## T07 — Maintenance / Hotfix Conformance & Dogfood
**Tests:** support policy applicability; source change → maintenance baseline → backported result exact SHA; new focused/Validation evidence; old source PASS non-transfer; Release/Deployment truth remains separate.

**Contract:** conformance/dogfood only.

**Implementation:** use a bounded repo fixture or controlled maintenance branch scenario; do not modify unrelated release history.

**Failure Handling:** missing suitable baseline/tooling => dedicated Validation handoff or fixture-only classification; never claim result-SHA PASS from source evidence.

## T08 — Adoption & Cross-standard Wiring
**Tests:** all owners/contracts/references discoverable; Golden coverage exact; project overrides/adoption support runtime/incident/maintenance applicability; historical evidence not retrofitted; non-runtime projects remain lightweight.

**Contract:** central integration only.

**Implementation:** manifest, selected project/adoption/checklist/migration wiring by reference; no T01–T07 redesign.

**Failure Handling:** owner conflict routes to owning Task/authority; manifest/Golden inconsistency repaired, not waived.

## T09 — Cross-standard Conformance / Closure Inputs
**Tests:** full forbidden inference matrix from Product §11/L2 §10; v4.4 deployment vs runtime separation; v4.2 recovery boundary; backport evidence non-transfer; Fast Path/historical compatibility.

**Contract:** integrated evidence/closure inputs only; no Release Qualification verdict.

**Implementation:** exact integrated candidate SHA/tree, actual tested environment tuples and all finding dispositions.

**Failure Handling:** unresolved P0/P1, required NOT_RUN/BLOCKED real tuple or subject drift prevents green closure input.