# v4.5.0 L1 Product Evidence — Operations, Incident & Maintenance

Status: **COMPLETE RESEARCH — supports PRD revision; Product Freeze waits for stable v4.4 Deployment Product boundary**

Research date: 2026-09-30

Baseline reviewed:

- `main@e9eb39235e45e9ad90407b803ab1c8679d348dbf`
- Draft `docs/implementation/4.5.0/PRD.md`
- current Testing/Test Data/Validation/Release standards
- v4.4 Draft + v4.4 L1 delivery evidence on parallel planning lane

This is Product evidence, not Product Freeze.

## 1. Recommendation

**PROCEED WITH NARROWING.**

Operations/Incident/Maintenance is a real missing lifecycle domain, but v4.5 should freeze only technology-neutral runtime truth and learning/maintenance semantics. It must not become an observability platform, incident-management product or universal SLO policy.

Required Product corrections before Freeze:

1. Separate **telemetry/evidence signals**, **runtime health interpretation**, **incident lifecycle**, and **maintenance/support state** rather than one global Operations state.
2. `Deployment SUCCESS != Runtime Healthy`; deployment result is a historical rollout fact, runtime health is time-varying evidence.
3. Health/readiness/liveness/business/critical-journey signals are distinct when material; no single endpoint/metric universally proves system correctness.
4. Incident records add new runtime facts and must never rewrite prior Release/Deployment PASS/READY evidence.
5. Material incidents require a deterministic engineering-feedback path into reproduction/regression/scenario/architecture/product/standard follow-up.
6. Maintenance/hotfix/backport can reduce ceremony through risk-bounded Fast Path, but exact identity/testing/Validation/Release truth remains truthful.
7. Telemetry/incident evidence must preserve secret/privacy constraints and should bind artifact/version/environment identity where material.

## 2. Observability Evidence

OpenTelemetry defines semantic conventions across traces, metrics, logs, profiles and resources. Its conventions provide common names/attributes so heterogeneous telemetry can be correlated, while the signals remain semantically distinct.

Sources:

- https://opentelemetry.io/docs/concepts/semantic-conventions/
- https://opentelemetry.io/docs/specs/semconv/
- https://opentelemetry.io/docs/specs/otel/logs/data-model/

**Finding:** ADS should standardize durable observability semantics and identity/correlation requirements, not mandate OpenTelemetry or a particular backend.

Product signal classes may include:

```text
logs / events
metrics
traces / spans
profiles
deployment/runtime resource identity
health / readiness / liveness
business or critical-journey signals
alerts
```

Not every project needs every signal.

## 3. Monitoring / Health Evidence

Google SRE monitoring guidance distinguishes monitoring data, alerting and externally/user-visible behavior; it emphasizes signals such as request/error/latency/system behavior rather than one universal health indicator.

Source: https://sre.google/sre-book/monitoring-distributed-systems/

Product requirements:

- risk-proportional critical behavior should be diagnosable/observable;
- health, readiness and liveness remain distinct where the platform uses them;
- infrastructure health does not automatically prove business journey success;
- telemetry existence is evidence input, not automatic product PASS;
- SLO/SLI thresholds remain project/product authority, not ADS universal constants.

Required non-inference:

```text
Deployment SUCCESS -> Runtime Healthy        forbidden
/health 200 -> Critical Journey PASS         forbidden
metrics present -> incident detectable       forbidden
no alert fired -> no user-visible failure    forbidden
```

## 4. Runtime Identity

Material runtime evidence should bind enough identity to distinguish what is actually running:

```text
release/artifact digest or immutable ref
deployment/environment identity
service/component/runtime instance or fleet scope when material
configuration/profile ref where material
observed time/window
```

This composes with future v4.4 Deployment Result and v4.1 External System/Config semantics. Friendly service/environment labels alone are insufficient where identity substitution could change the claim.

## 5. Privacy / Secret Boundary

OpenTelemetry's logging/semantic models permit rich attributes, but ADS must explicitly constrain project-sensitive data.

Required Product rule:

> Ordinary telemetry and incident evidence MUST NOT become a backdoor for durable secret values, credentials or unapproved sensitive/PII content.

Correlation/debug usefulness does not waive v4.1 Config/Secrets boundaries. Redacted/non-secret identifiers should be preferred when sufficient.

## 6. Incident & Recovery Evidence

Google SRE incident management treats incidents as managed events requiring preparation/detection, coordinated mitigation/recovery and learning. Its postmortem practice records incident impact, mitigation/resolution, contributing causes and concrete follow-up actions.

Sources:

- https://sre.google/resources/practices-and-processes/incident-management-guide/
- https://sre.google/sre-book/postmortem-culture/
- https://sre.google/workbook/postmortem-culture/

**Finding:** v4.5 should own a minimal incident semantic lifecycle without prescribing one ticketing/on-call platform.

Product-level semantic phases:

```text
DETECTED
CLASSIFIED
CONTAINED / MITIGATED
RECOVERED
VERIFIED
FOLLOW_UP / CLOSED
```

L2 may refine representation. The Product invariant is that:

- detection is not recovery;
- mitigation is not permanent fix;
- service recovery is not verification/follow-up completion;
- incident severity/impact is project-defined and evidence-based;
- incident facts append to history; they do not rewrite earlier Release/Deployment truth.

## 7. Recovery Boundary

Operational recovery may include:

```text
artifact rollback
configuration correction
traffic reroute/failover
feature disablement
capacity response
data repair/restore
forward fix
```

v4.5 owns incident/recovery **runtime handling and verification**. v4.2 remains owner of persistent-state migration transition/recovery semantics; v4.4 remains owner of Deployment rollback/result semantics. Incident response references those owners rather than redefining them.

## 8. Incident → Engineering Feedback Loop

Google SRE postmortem practice emphasizes action items that prevent recurrence and feed back into engineering priorities. This strongly supports a first-class ADS learning loop.

Frozen Product target:

```text
Incident / Escaped Defect
        ↓
minimal reproduction / observed evidence
        ↓
regression case / scenario / critical journey
        ↓
classify product | architecture | implementation | test | validation | standard/process gap
        ↓
fix/follow-up Task(s)
        ↓
normal Review / Validation / Release
        ↓
closure + systemic feedback where warranted
```

Material incident closure must not consist only of “service recovered” when required follow-up remains open; follow-up ownership may be separate/longer-lived, but must be durable and attributable.

## 9. Maintenance / Support Evidence

Projects need explicit support-line truth so Agents do not infer maintenance policy from branch existence or package availability.

Product concepts should represent, with project-defined vocabulary allowed:

```text
CURRENT
MAINTENANCE
SECURITY_ONLY
DEPRECATED
EOL
```

Required semantics:

- supported lines/baselines explicit;
- allowed change classes per support state explicit;
- deprecation/EOL timing/communication when consumers matter;
- maintenance source branch/baseline identity reconstructible;
- upgrade/migration guidance points to supported path;
- branch/tag existence != supported state.

The exact enum need not be globally closed; projects can map their support vocabulary while preserving equivalent semantics.

## 10. Hotfix / Backport Governance

Urgency may reduce ceremony but not truth.

Required Product invariants:

- exact hotfix scope/baseline explicit;
- cherry-pick/backport provenance recorded;
- exact-SHA testing/Validation remains scoped to the backported result;
- prior source-branch PASS does not automatically transfer to maintenance branch;
- risk-bounded Fast Path may skip non-required ceremony when project authority permits;
- emergency deployment/mitigation may happen under explicit emergency authority but skipped evidence remains skipped/NOT_RUN and creates required follow-up where policy says so;
- hotfix Release/Deployment results remain separate.

## 11. Machine-contract Product Findings

L2 should evaluate a compact record set rather than one schema per signal:

1. **Runtime Identity / Observation Context** — may reuse/reference Deployment/Execution Context rather than a new schema if sufficient.
2. **Incident Record** — incident identity, impact/scope, affected runtime identity, timeline/state facts, evidence refs, mitigation/recovery/follow-up refs.
3. **Recovery Verification Result** — may be embedded/linked in Incident Record if append-only/event history preserves truth.
4. **Maintenance Policy / Support Matrix** — project version-line state and allowed support/change policy.
5. **Backport/Hotfix Provenance** — may extend existing change/release records rather than default to a standalone schema.

Avoid centralizing raw telemetry in ADS; durable refs to approved external telemetry systems are sufficient where policy permits.

## 12. Product-level Negative Conformance

Reject at minimum:

- Deployment SUCCESS -> Runtime Healthy;
- health endpoint PASS -> business journey PASS;
- alert absent -> no incident;
- monitoring system available -> product healthy;
- incident recovered -> permanent defect fixed;
- incident record -> rewrite prior Release/Deployment evidence;
- production log usefulness -> permission to retain secret/PII values;
- branch exists -> version supported;
- cherry-pick/backport -> prior exact-SHA Validation transferred;
- hotfix urgency -> release/validation truth waived;
- mitigation -> postmortem/follow-up automatically complete.

## 13. Counter-evidence / Scope Risks

- Many projects have no production runtime; operations can be NOT_APPLICABLE with rationale.
- Small products may use simple logs and manual incident handling; ADS should not require a full telemetry platform.
- Universal incident severity/SLO thresholds are organization-specific and out of scope.
- A full incident state machine can become bureaucratic; L2 should prefer append-oriented facts/events where possible.
- Not every warning/error deserves an incident record.

## 14. L1 Verdict

**Evidence is sufficient for PRD revision.**

Product Freeze remains intentionally blocked until v4.4's Deployment Product boundary is Frozen/stable enough to prevent v4.5 from stealing Deployment result/rollback ownership.

`LOCAL_ENV=NOT_REQUIRED` at L1. Real telemetry/incident exercises belong later dogfood/Validation with explicit environment and side-effect authority.