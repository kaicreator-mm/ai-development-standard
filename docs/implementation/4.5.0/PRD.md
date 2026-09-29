# ai-development-standard v4.5.0 PRD — Operations, Incident & Maintenance

Status: **FREEZE CANDIDATE — revised from L1; explicit Product Freeze waits for stable v4.4 Deployment Product boundary**

## 1. Product intent

v4.5.0 extends ADS from deployment into runtime truth, incident learning and version-line maintenance without turning ADS into an observability/on-call platform.

The version must let a project answer, from durable facts:

1. What runtime/artifact/environment is actually being observed?
2. Which signals support a health/readiness/liveness/business claim?
3. What happened during a material incident, what mitigation/recovery occurred, and what remains open?
4. How does escaped production failure create regression/scenario/product/architecture/standard follow-up?
5. Which product/version lines are supported and under what maintenance policy?
6. How can hotfix/backport work move quickly without transferring stale exact-SHA truth?

## 2. Product owners

v4.5 introduces three normative owners:

1. **Observability & Runtime Evidence Standard** — technology-neutral runtime signal semantics, runtime identity/correlation and privacy/secret boundaries.
2. **Incident, Recovery & Engineering Feedback Standard** — incident facts, mitigation/recovery/verification and deterministic engineering feedback.
3. **Maintenance, EOL & Hotfix Standard** — support-line state, backport/hotfix provenance and maintenance Fast Path boundaries.

These are separate lifecycle dimensions. v4.5 MUST NOT create one overloaded global Operations state machine.

v4.4 remains the Deployment result/rollback-orchestration owner. v4.2 remains persistent-state migration/recovery semantic owner. Existing Testing/Test Data/Validation/Release owners remain authoritative for their results.

## 3. Observability & Runtime Evidence

Runtime evidence may include, where material:

```text
logs / events
metrics
traces / spans
profiles
health / readiness / liveness
business / critical-journey signals
alerts
runtime resource/version/artifact identity
```

Required semantics:

- projects use only signals material to risk/product behavior;
- health, readiness and liveness remain distinct where the platform uses them;
- infrastructure/process health does not automatically prove business/critical-journey success;
- telemetry availability/existence does not itself prove product correctness;
- runtime evidence binds artifact/version/environment and observation time/window when material;
- user-visible failures should be diagnosable through bounded non-secret identifiers/context rather than unrestricted raw dumps;
- secret values, credentials and unapproved sensitive/PII content MUST NOT enter ordinary durable telemetry/incident evidence;
- SLO/SLI targets and severity thresholds remain project/product authority, not universal ADS constants.

## 4. Runtime identity

Material runtime evidence should be able to reference:

```text
release / immutable artifact identity
deployment/environment identity
service/component/fleet scope when material
configuration/profile reference when material
observation timestamp/window
```

Friendly environment/service labels are insufficient when materially different runtime identities could make evidence substitution unsafe.

Runtime identity consumes v4.4 Deployment/artifact facts; it does not create a second deployment record.

## 5. Deployment result vs runtime health

Frozen invariant:

> **Deployment SUCCESS != Runtime Healthy.**

Deployment result is a historical fact about rollout execution. Runtime health is time-varying evidence after/during operation.

Forbidden shortcuts include:

```text
Deployment SUCCESS -> Runtime Healthy
/health 200 -> critical journey PASS
metrics exist -> product healthy
no alert fired -> no user-visible failure
```

## 6. Incident & Recovery semantics

A material incident should preserve append-oriented facts sufficient to reconstruct, where applicable:

```text
incident identity
observed/affected runtime identity
impact/scope/severity under project authority
detection evidence/timeline
classification
containment/mitigation
recovery action
recovery verification
root/contributing cause evidence when known
follow-up/action ownership
closure state/reason
```

Semantic phases include:

```text
DETECTED
CLASSIFIED
CONTAINED / MITIGATED
RECOVERED
VERIFIED
FOLLOW_UP / CLOSED
```

L2 may choose event/append-oriented representation instead of one mutable enum. Product invariants:

- detection != mitigation;
- mitigation != permanent fix;
- recovered service != verified fix;
- verified recovery != all follow-up completed;
- incident facts add runtime history and MUST NOT rewrite prior Release/Deployment evidence;
- severity/impact is evidence-based/project-defined, not universal ADS scoring.

## 7. Operational recovery boundary

Operational recovery may reference:

```text
artifact rollback / redeploy
configuration correction
traffic reroute / failover
feature disablement
capacity response
data restore/repair
forward fix
```

v4.5 owns incident runtime handling/verification. It references rather than redefines:

- v4.4 Deployment rollback/result semantics;
- v4.2 persistent-state migration/recovery semantics;
- v4.1 external-system/config/secret authority.

Credential/access capability never implies production mutation authority.

## 8. Incident → Engineering Feedback

Frozen feedback path:

```text
Incident / Escaped Defect
        ↓
minimal reproduction / observed evidence
        ↓
regression test / scenario / critical journey
        ↓
classification:
product | architecture | implementation | test | validation | standard/process gap
        ↓
fix / follow-up Task(s)
        ↓
normal Review / Validation / Release
        ↓
systemic standard/project feedback where warranted
```

Material follow-up ownership must be durable even when the incident is operationally recovered before engineering work completes.

Incident closure MUST NOT erase skipped/blocked evidence or open required follow-up.

## 9. Maintenance & support-line truth

Projects may use their own vocabulary, but the product must represent equivalent states such as:

```text
CURRENT
MAINTENANCE
SECURITY_ONLY
DEPRECATED
EOL
```

Required semantics:

- supported line(s)/baseline(s) explicitly identified;
- allowed change classes per support state explicit;
- maintenance branch/source baseline identity reconstructible;
- hotfix/backport authority explicit;
- security-fix policy where applicable;
- deprecation/EOL effective timing/communication where external consumers matter;
- upgrade/migration path to supported line referenced;
- branch/tag/package existence MUST NOT be interpreted as supported status.

L2 may use extensible project-mapped vocabulary rather than one closed global enum.

## 10. Hotfix / backport governance

Urgency can reduce ceremony, not truth.

Required semantics:

- exact urgent scope/baseline explicit;
- backport/cherry-pick provenance recorded;
- the resulting maintenance-branch exact SHA receives its own applicable testing/Validation evidence;
- PASS from source/original branch MUST NOT transfer automatically after backport;
- risk-adjusted Fast Path may omit non-required gates only under applicable project authority;
- emergency mitigation/deployment may proceed under explicit emergency authority, but skipped/not-run evidence remains truthful and creates required follow-up where policy requires;
- hotfix Release/Deployment results remain separate dimensions.

## 11. Product-level forbidden inferences

v4.5 conformance MUST reject at least:

```text
Deployment SUCCESS -> Runtime Healthy
health endpoint PASS -> business journey PASS
monitoring backend available -> product healthy
no alert -> no incident
incident recovered -> permanent defect fixed
incident record -> rewrite earlier Release/Deployment evidence
telemetry usefulness -> permission to persist secrets/PII
branch/tag exists -> version supported
backport/cherry-pick -> old exact-SHA Validation transfers
hotfix urgency -> release/validation truth waived
mitigation -> follow-up complete
```

## 12. Machine-readable expectations

L2 should minimize contract count and first evaluate reuse/extensions of existing/future v4.4 records.

Conceptual durable records:

1. **Runtime Observation Context** — preferably refs/reuse of Deployment/artifact/environment identity rather than duplicate deployment schema.
2. **Incident Record / Event History** — incident identity, affected runtime, impact/timeline/evidence, mitigation/recovery/verification/follow-up refs.
3. **Maintenance Policy / Support Matrix** — version-line/baseline state, allowed changes, dates/policy refs.
4. **Backport/Hotfix Provenance** — preferably an extension/reference to existing change/release records if deterministic.

A separate Recovery Verification schema is not automatically required; L2 should prefer incident events/refs if sufficient.

ADS does not store raw telemetry. Durable references to approved external telemetry/incident systems may satisfy evidence linkage.

## 13. Non-goals

v4.5 does not:

- prescribe OpenTelemetry, Prometheus, Grafana, Sentry, PagerDuty or another stack;
- establish universal SLO/SLI/severity values;
- require production deployment for projects where operations is not applicable;
- replace organization-specific incident/compliance policy;
- authorize production data/system access by default;
- make every warning/error an incident;
- redefine Deployment result/rollback (v4.4), migration recovery (v4.2), Validation or Release states;
- exempt hotfixes from exact identity/testing/release truth.

## 14. Compatibility posture

Target: additive/non-weakening v4 minor release.

Operational capabilities can be `NOT_APPLICABLE` with rationale for projects without persistent deployed runtime. Historical releases MUST NOT receive retroactive runtime/incident/maintenance evidence that did not exist.

If convergence requires incompatible incident/execution/release wire changes, route them to v4.7/future-major planning rather than hiding them in v4.5.

## 15. Product acceptance

v4.5.0 is complete when:

1. three owners in §2 have clear non-overlapping authority;
2. deployment result cannot be interpreted as runtime health;
3. runtime evidence is version/artifact/environment/time attributable where material;
4. privacy/secret constraints cover telemetry and incident evidence;
5. incident handling preserves mitigation/recovery/verification/follow-up distinctions;
6. escaped incidents have deterministic engineering-feedback paths;
7. maintenance/support state is explicit and branch existence is not support authority;
8. hotfix/backport cannot transfer old exact-SHA evidence or silently weaken release truth;
9. at least one real or simulated incident dogfood demonstrates detection → mitigation/recovery → verification → regression/follow-up closure.

## 16. Freeze basis / next gate

Freeze candidate basis:

- `docs/implementation/4.5.0/L1_PRODUCT_EVIDENCE.md`
- existing Testing/Test Data/Validation/Release ownership
- v4.4 delivery/deployment Product evidence on the parallel lane

Before explicit Product Freeze:

1. v4.4 must explicitly Freeze a stable Deployment Product boundary;
2. re-read v4.4 exact Product authority for drift in Deployment result/rollback semantics;
3. then record v4.5 Product Freeze and proceed to L2.

`LOCAL_ENV=NOT_REQUIRED` for Product Freeze/L2 research. Real incident/telemetry exercises belong later exact-environment dogfood/Validation Tasks.