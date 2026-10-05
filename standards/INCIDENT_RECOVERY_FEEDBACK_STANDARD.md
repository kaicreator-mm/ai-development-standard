# Incident, Recovery & Engineering Feedback Standard

Status: **Normative — v4.5**

## 1. Purpose

This standard governs append-oriented incident facts, recovery verification and engineering-feedback routing. It does not redefine Deployment rollback/result, persistent-state migration recovery, Task state, Validation or Release authority.

## 2. Append-oriented incident history

Material incident history MUST preserve prior facts rather than rewriting earlier observations to match the latest outcome. Detection, mitigation, recovery, verification and follow-up are distinct facts that may occur at different times.

```text
DETECTED != MITIGATED
RECOVERED != VERIFIED
VERIFIED != FOLLOW_UP_COMPLETE
```

A later recovery event does not erase earlier failure evidence.

## 3. Incident identity and correlation

Where material, incident events SHOULD correlate the affected artifact/deployment/environment/runtime observation and relevant configuration/external-system facts using their owning references. Correlation does not transfer ownership of those concerns.

Consume the existing T01 `schemas/incident-event-v1.schema.json`, not a competing incident family: `incident_id` correlates append-only events; `event_id`, `event_kind` and `occurred_at` distinguish immutable recorded facts; `runtime_subject_refs` and `evidence_refs` bind the affected subject and non-secret evidence; `actor_or_authority_ref` identifies the event's responsible actor or applicable authority. Existing optional `engineering_follow_up_refs`, deployment/migration recovery refs and impact/severity refs link to separate durable owners; their presence does not authorize those owners' actions. The machine contract's optional fields do not waive this standard's conditional material-follow-up obligations.

Incident `evidence_refs` and reproduction material inherit v4.1 Configuration/Secrets and Workspace/Artifact boundaries. Ordinary incident evidence MUST NOT embed raw credentials, bearer tokens, live signed URLs, secret values or unapproved sensitive/PII data; use bounded non-secret stable references, approved redacted summaries and explicit applicable diagnostic-exception authority where genuinely necessary. A structurally valid reference string is not proof of confidentiality or permission to publish its target.

## 4. Recovery authority boundaries

Recovery actions MUST use the owning authority for the mutated concern:

- deployment rollback/roll-forward remains v4.4 Deployment Governance;
- persistent-state migration/data recovery remains v4.2 Data/Migration Governance;
- configuration/credential change remains its configuration/secret owner;
- external-system mutation requires its applicable side-effect authority.

Ambiguous production mutation authority blocks the action rather than being inferred from incident urgency.

## 5. Verification after recovery

Operational mitigation or apparent recovery MUST NOT be treated as permanent-fix truth without the required verification. Verification must bind the subject/environment/procedure appropriate to the claim.

```text
service responds again != root cause fixed
rollback completed != corrective change verified
```

## 6. Engineering feedback

A material incident MUST route durable follow-up as applicable to one or more of:

- reproducible defect/bug evidence;
- regression or test scenario;
- test-data/fixture improvement;
- product/architecture decision;
- operational/runbook/configuration improvement;
- standard/process gap.

For every material incident the owning project/incident authority MUST record a durable follow-up classification/disposition: **required engineering work**, **investigation pending**, or **no engineering work required with a durable accountable rationale**. These are project-owned decision facts, not a new global incident state machine; severity alone cannot infer the disposition.

Where engineering work is required, the route MUST preserve an incident/reproduction reference, the durable classification decision, a responsible classification/follow-up owner reference, and a link to the existing-authority engineering work item (GitHub Issue/Task or the project's approved work owner). If an owner or work item cannot yet be designated, record an **explicit unresolved owner-assignment obligation** and/or **unresolved work-item-creation obligation**, with durable accountable assignment authority and next routing owner; do not silently replace missing ownership with an evidence-only link. `engineering_follow_up_refs` may reference the existing work item or durable unresolved routing obligation; it does not manufacture a Task or grant a workflow mutation.

When classification remains **investigation pending**, preserve a durable investigation owner (or unresolved owner-assignment obligation), reproduction/evidence refs and the next classification decision obligation. It MUST NOT be silently treated as `no engineering work required`. A `no engineering work required` disposition requires its owner-backed rationale; a recovered service alone is not such a rationale.

The route MUST preserve a durable reference from the incident/follow-up fact to the created work/evidence. Incident closure MUST NOT erase required unresolved follow-up. Operational incident recovery/closure may be recorded distinctly, but `FOLLOW_UP_COMPLETE` MUST NOT be asserted while required work lacks a responsible owner/work-item link or its pending obligations remain unresolved. Completion of a linked engineering Task still requires its own applicable Review/Validation authority; incident text does not issue a Task PASS.

## 7. Prior evidence is immutable history

Incident facts may invalidate confidence or trigger new evidence requirements, but MUST NOT rewrite a prior exact Release/Deployment/Validation result as though the original execution had produced a different outcome.

## 8. Failure handling

If recovery authority, environment identity, incident subject or required verification is unknown, fail closed and record the unresolved fact. Missing follow-up classification, owner/work-item routing or safe evidence handling requires explicit pending obligations, not premature follow-up completion. Recovery without required verification/follow-up remains explicit and cannot be collapsed to permanent-fix truth.
