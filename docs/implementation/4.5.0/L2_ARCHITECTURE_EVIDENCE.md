# v4.5.0 L2 Architecture Evidence — Operations, Incident & Maintenance

Status: **FROZEN L2 ARCHITECTURE AUTHORITY — 2026-09-30**

Freeze inputs:

- Frozen Product Authority: `5581fb411647dfeca0aae1e9ef6e66a7dfd795f4`
- L1 Product Evidence: `docs/implementation/4.5.0/L1_PRODUCT_EVIDENCE.md`
- v4.4 Frozen Product Authority: `0acbc82b031bc5870589fc1a899b679b0290d40a`
- v4.4 Frozen L2: `5c19eb7f53c179b4e0068371fc546bbe8bc14784`
- v4.2 Frozen migration semantics
- existing Testing, Test Data, Validation and Release owners

## 1. Architecture recommendation

Use **three normative owners + three default machine-contract families + append-oriented incident facts**, while reusing v4.4 deployment/artifact identity and existing Validation/Release truth.

```text
Deployment Result / Artifact / Environment
                   │
                   ▼
      Observability & Runtime Evidence
                   │
          Runtime Observation Context
                   │
         healthy / degraded / unknown
                   │
              material incident
                   ▼
 Incident, Recovery & Engineering Feedback
                   │
             Incident Event Record
                   │
      ┌────────────┴─────────────┐
      ▼                          ▼
Regression / Follow-up      Runtime Recovery
      │                          │
      └────────────┬─────────────┘
                   ▼
       Maintenance / EOL / Hotfix
                   │
        Maintenance Policy Record
```

Architecture decisions:

1. **Three normative owners only.** Observability/Runtime Evidence, Incident/Recovery/Engineering Feedback, Maintenance/EOL/Hotfix remain separate semantic owners.
2. **Three default machine-contract families.** Runtime Observation Context, Incident Event Record, and Maintenance Policy Record are sufficient defaults. Backport/hotfix provenance is represented through refs/fields on maintenance/change/release evidence rather than a mandatory fourth schema.
3. **Incident history is append-oriented.** Do not encode the entire incident lifecycle as one mutable global enum whose later state erases earlier facts. Events carry semantic kind, time, actor/authority, evidence and refs.
4. **No runtime-health Gate state.** Runtime observations are domain evidence. They do not create Validation PASS/FAIL or Release READY/BLOCKED.
5. **Runtime identity reuses v4.4 exact artifact/deployment/environment identity.** Do not create a second deployment object.
6. **Incident recovery references, not replaces, v4.4 deployment recovery and v4.2 data/migration recovery.** Operational recovery may coordinate them but does not redefine them.
7. **Maintenance support state is a separate dimension.** Support-line truth cannot be inferred from branch/tag/package existence.
8. **Hotfix/backport provenance is exact-subject scoped.** Cherry-pick/backport never transfers source-branch Validation or Review PASS automatically.
9. **Telemetry payloads remain external.** ADS stores bounded identity/evidence refs and approved summaries, not raw log/metric/trace stores.
10. **SLO/severity/tool choices remain project authority.** No universal threshold, monitoring stack, paging system or incident severity scale is introduced.

## 2. Architecture drivers

### D1 — Runtime evidence is time-varying and dimensional
Logs, metrics, traces, profiles, health/readiness/liveness and business signals can describe different aspects of a running system. One healthy signal cannot safely become universal runtime health.

### D2 — Deployment completion is historical; health is ongoing
v4.4 Deployment Result records what occurred during rollout. v4.5 observations are later/time-scoped facts. Therefore `DEPLOYMENT_SUCCEEDED` can be an observation input but never a derived `RUNTIME_HEALTHY` proof.

### D3 — Incident facts must survive remediation
Detection, mitigation, recovery, verification and follow-up are distinct facts. An append-oriented record preserves what happened without rewriting history when service recovers.

### D4 — Incident learning must reconnect to normal engineering authority
Escaped defects need durable reproduction/regression/follow-up routes into existing Product/Architecture/Task/Test/Validation/Release systems rather than an operations-only parallel backlog.

### D5 — Maintenance branches are source topology, not support authority
A branch/tag/package may exist after EOL or before support is declared. Support-line truth therefore needs explicit project authority and baseline identity.

## 3. Normative owner map

| Concern | Owner | Must not duplicate |
|---|---|---|
| runtime observation semantics / bounded identity | Observability & Runtime Evidence | Deployment result, Validation result, raw telemetry backend |
| incident detection/impact/mitigation/recovery/verification/follow-up | Incident, Recovery & Engineering Feedback | deployment/data recovery owners, Product/Architecture decision authority |
| regression/follow-up routing | Incident, Recovery & Engineering Feedback | Task DAG/Testing/Validation execution authority |
| support line / EOL / allowed maintenance change classes | Maintenance, EOL & Hotfix | dependency EOL, Release verdict |
| backport/hotfix exact-subject provenance | Maintenance, EOL & Hotfix | Git execution, Review/Validation results |
| deployment rollout/result/rollback orchestration | v4.4 Deployment Governance | runtime health |
| persistent-state migration/recovery | v4.2 Data & Migration | incident timeline |
| exact Validation truth | existing Validation owner | runtime observation |
| Release Qualification | existing Release owner | support state / runtime health |

## 4. Machine contracts

### 4.1 `schemas/runtime-observation-context-v1.schema.json`

Purpose: bind a runtime observation/evidence reference to the exact runtime subject and observation window without storing raw telemetry.

Required semantic fields:

```text
schema_version
observation_id
artifact_ref
deployment_ref
environment_ref
component_or_scope_ref?
observed_at or observation_window
signal_refs[]
configuration_profile_ref?
```

Optional semantic classification may describe observed signal class such as log/metric/trace/health/readiness/liveness/business/custom, but the set must remain extensible.

Rules:

- no `PASS`, `READY` or universal `healthy=true` field that would manufacture another owner’s result;
- missing/quiet telemetry is not positive health evidence;
- secret values/credentials/sensitive raw payloads are excluded;
- friendly service/environment names do not replace immutable/material identity when evidence substitution would be unsafe.

### 4.2 `schemas/incident-event-v1.schema.json`

Purpose: append one durable incident fact/event to an incident history.

Required semantic fields:

```text
schema_version
incident_id
event_id
event_kind
occurred_at
runtime_subject_refs[]
evidence_refs[]
actor_or_authority_ref
```

Recommended extensible `event_kind` semantics include:

```text
DETECTED
CLASSIFIED
IMPACT_UPDATED
CONTAINED
MITIGATED
RECOVERY_STARTED
RECOVERED
VERIFIED
FOLLOW_UP_CREATED
CAUSE_UPDATED
CLOSED
project-defined extension
```

Optional fields may carry project-defined impact/severity refs, mitigation/recovery action refs, deployment/migration recovery refs and engineering-follow-up refs.

Rules:

- append facts rather than overwriting history;
- `RECOVERED` does not imply `VERIFIED`;
- `VERIFIED` does not imply all `FOLLOW_UP` complete;
- incident events cannot rewrite historical Release/Deployment evidence;
- closure cannot erase unresolved required follow-up.

### 4.3 `schemas/maintenance-policy-v1.schema.json`

Purpose: represent explicit support-line authority for one product/version family/baseline.

Required semantic fields:

```text
schema_version
policy_id
product_or_component_ref
support_lines[] {
  line_id
  baseline_ref
  support_state
  allowed_change_classes[]
  authority_ref
  effective_from?
  effective_until?
  upgrade_or_migration_ref?
}
```

`support_state` should remain project-mappable/extensible. Recommended semantics include CURRENT, MAINTENANCE, SECURITY_ONLY, DEPRECATED and EOL without forcing every project to use those exact labels.

Optional backport/hotfix provenance fields/refs may bind source SHA/PR, target maintenance baseline, resulting exact SHA and relevant Validation/Review/Release refs.

Rules:

- branch/tag/package existence is not support authority;
- source-branch PASS does not transfer to the backported exact SHA;
- emergency authority may reduce ceremony only where project policy permits; skipped/not-run evidence remains truthful.

## 5. Why no default Backport/Hotfix schema

Existing Git commit/PR/change provenance plus maintenance policy and Validation/Review/Release refs can deterministically represent the required truth. A separate mandatory schema would duplicate identity that Git/GitHub already owns.

A project MAY introduce a structured backport record if machine exchange needs it, but v4.5 does not make it a default ADS object.

## 6. Incident projection / derived state

A UI/controller MAY derive a current incident projection from append events, for example:

```text
DETECTED / ACTIVE / MITIGATED / RECOVERED_UNVERIFIED / VERIFIED_WITH_FOLLOWUP / CLOSED
```

Such projection is explicitly derived/non-authoritative. The durable event history remains evidence. The projection MUST NOT erase unresolved follow-up or convert missing events into positive facts.

## 7. Privacy / secret architecture

Runtime/incident evidence follows v4.1 Configuration & Secrets boundaries:

- store refs/identity, not secret values;
- raw request/response dumps are not default evidence;
- signed URLs/bearer material are secrets when possession grants access;
- approved sensitive/PII handling remains project/compliance authority;
- bounded correlation identifiers are preferred to unrestricted payload capture.

## 8. Engineering feedback architecture

Incident follow-up routes through existing authority:

```text
incident event / escaped defect
→ reproduction/scenario/evidence
→ classification owner
→ GitHub work item / Product or Architecture issue when applicable
→ normal Task Pack / DAG / implementation
→ exact-head Review / Validation
→ Release / Deployment
```

No incident event itself mutates the live Task DAG or grants a code-change scope.

Systemic findings may create a standard-gap Issue but do not silently rewrite the pinned Standard.

## 9. Architecture UNKNOWNs and disposition

| ID | UNKNOWN | Impact | Disposition | Decision |
|---|---|---|---|---|
| U1 | One mutable incident schema vs append events? | Critical | Product/history evidence sufficient | Append event record + derived projection. |
| U2 | Separate runtime-health result schema? | High | dimensional evidence sufficient | No default health verdict object; observation context only. |
| U3 | Separate recovery verification schema? | Medium | incident events + evidence refs sufficient | No default separate schema. |
| U4 | Mandatory backport/hotfix provenance schema? | Medium | Git/GitHub + refs sufficient | No default schema. |
| U5 | Universal incident severity/SLO vocabulary? | High | Product non-goal sufficient | No. Project/product authority. |
| U6 | Store telemetry inside ADS records? | High | privacy/scale evidence sufficient | No; refs/approved summaries only. |
| U7 | Need executable incident demo before L2 Freeze? | High | static authority/evidence sufficient | No; dogfood later. |

**Research Demo decision: NOT REQUIRED before L2 Freeze.**

## 10. Conformance architecture

Required negative families:

```text
Deployment SUCCESS -> Runtime Healthy                 reject
health endpoint success -> business journey PASS      reject
metrics/monitor available -> product healthy          reject
no alert -> no incident                               reject
RECOVERED -> VERIFIED                                 reject
VERIFIED -> all follow-up complete                    reject
incident closure -> erase prior events/follow-up      reject
telemetry utility -> secret/PII persistence authority reject
branch/tag exists -> supported line                   reject
cherry-pick/backport -> source PASS transfer          reject
hotfix urgency -> required truth waived               reject
```

Positive dogfood later should include a simulated/controlled incident demonstrating:

```text
runtime identity
→ detection
→ mitigation/recovery
→ verification
→ regression/follow-up creation
→ maintenance/hotfix provenance when applicable
```

## 11. Fast Path / materiality

Projects without persistent deployed runtime MAY mark runtime/incident capabilities `NOT_APPLICABLE` with rationale. A library may still use Maintenance/EOL semantics even when Observability/Incident are not applicable.

Small operational/documentation changes need not instantiate empty incident/observation records. Material production facts, once they exist, must remain truthful and attributable.

## 12. L2 verdict

Architecture is sufficiently resolved to create the v4.5 Task DAG.

No local environment is required for planning. Real telemetry/incident recovery dogfood, if selected later, must use an explicit exact-environment handoff when the Web/CI environment cannot execute the required scenario.
