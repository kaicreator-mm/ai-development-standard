# Incident, Recovery & Engineering Feedback Reference

Non-normative guidance for `INCIDENT_RECOVERY_FEEDBACK_STANDARD.md`. The existing `schemas/incident-event-v1.schema.json` is the T01 machine event shape; examples below are not a second lifecycle or Task authority.

## Append-oriented event example

```text
DETECTED -> MITIGATED -> RECOVERED -> VERIFIED -> FOLLOW_UP
```

This is not a mandatory global lifecycle state machine. It illustrates distinct durable facts. A project may record additional facts without collapsing their meanings. Do not overwrite earlier events or infer `FOLLOW_UP_COMPLETE` from service recovery.

## Existing T01 Incident Event contract mapping

Illustrative append-only record shaped by `schemas/incident-event-v1.schema.json`:

```json
{
  "schema_version": 1,
  "incident_id": "incident-042",
  "event_id": "incident-042-detected-001",
  "event_kind": "DETECTED",
  "occurred_at": "2026-09-30T08:00:00Z",
  "runtime_subject_refs": ["artifact:sha256:example/environment:staging"],
  "evidence_refs": ["evidence:redacted/incident-042-summary"],
  "actor_or_authority_ref": "incident-response-owner:team-ops",
  "engineering_follow_up_refs": ["github-issue:#example-defect"]
}
```

`incident_id` joins later append-only facts; `event_id`/`event_kind`/`occurred_at` distinguish them. `runtime_subject_refs` and `evidence_refs` keep observed subject and approved non-secret evidence identities, while `actor_or_authority_ref` identifies the owner of this event. The optional `engineering_follow_up_refs` binds project-owned engineering work/obligations when applicable. An illustrative schema-valid payload does not establish real incident execution, confidentiality of a referenced destination, or an authorized Task state.

## Recovery references

An incident may reference a Deployment rollback result, migration recovery evidence, configuration change, credential rotation or external-system action. Each mutation remains governed by its owning authority; the incident does not grant that authority.

## Verification example

After a rollback restores service, verify the affected exact subject/environment and record whether the triggering condition is absent. If a permanent corrective change is later produced, it receives its own Testing/Validation/Review evidence.

## Feedback routing worksheet

```text
incident_ref: incident-042
reproduction_ref: evidence:redacted/reproduction-042
classification_disposition: REQUIRED_ENGINEERING_WORK | INVESTIGATION_PENDING | NO_ENGINEERING_WORK_WITH_RATIONALE
classification_decision_ref: incident-classification:042
classification_owner_ref: project-owner:quality
accountable_assignment_authority_ref: project-owner:quality
engineering_work_item_ref: github-issue:#example-defect
unresolved_owner_assignment_obligation_ref:
unresolved_work_item_creation_obligation_ref:
next_routing_owner_ref:
no_engineering_work_rationale_ref:
regression_scenario_ref: test-scenario:042
product_or_architecture_ref:
runbook_or_config_ref:
standard_gap_ref:
unresolved_follow_up_refs:
```

These worksheet keys are application-level routing guidance; they are not newly required fields in T01's Incident Event schema. Use only applicable routes, but a required engineering follow-up must never consist solely of `reproduction_ref` without a responsible owner/work-item link or explicit durable pending obligations. Example of **blocked premature follow-up completion**: classification REQUIRED_ENGINEERING_WORK, reproduction evidence exists, `classification_owner_ref` empty, `engineering_work_item_ref` empty and no unresolved owner/work-item obligations recorded. Service may be operationally RECOVERED, but `FOLLOW_UP_COMPLETE` cannot be claimed.

When classification is pending, record its accountable investigation owner and next decision obligation; only an owner-backed decision with rationale may say no further engineering work is required. Closure does not mean every optional field is populated; it means required unresolved follow-up remains durable, visible and accountable.

## Incident evidence confidentiality

Reference approved redacted evidence, not an embedded bearer token, signed URL or raw credential. `evidence:redacted/incident-042-summary` is illustrative and **does not prove the target is safe** without the applicable v4.1 Configuration/Secrets and Workspace/Artifact handling. A raw `Authorization: Bearer ...` line or URL containing live `token=`/`X-Amz-Signature=` cannot be pasted into an ordinary incident event `evidence_refs` merely because the schema accepts strings. Use non-secret stable artifact identifiers, approved redaction, and the owning diagnostic exception process when unavoidable.
