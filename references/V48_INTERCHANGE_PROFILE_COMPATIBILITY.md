# v4.8 Interchange Profile Compatibility — T-003

Disposition: **NO_CHANGE_REQUIRED** for the existing generic Interchange v1 schema and GitHub writer/admission protocol on the current v4.8 exact subject.

## Evidence basis

The active `schemas/interchange-envelope-v1.schema.json` already provides the transport-neutral correlation primitives required by Frozen v4.8:

- `operation_id`, `work_item_ref`, `dispatch_id` and `assurance_id` for durable work/execution correlation;
- `subject_ref`, `subject_identity_ref` and `identity_binding` for exact/candidate/validation-tuple subject binding;
- `actor` and `causation.correlation_refs` for logical operator and durable cross-owner references;
- `payload_ref` for a durable owning payload/evidence/result reference;
- `authority_effect = CORRELATION_ONLY_NON_AUTHORITATIVE`, preventing the envelope from becoming workflow/gate authority.

`docs/implementation/4.0.0/AGENT_INTERCHANGE.md` already owns stale/duplicate/superseded/conflict, replay/idempotency, durable materialization/reconstruction and transport-neutral mapping. `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` / `ai-dev:event:v2` remains the GitHub writer/admission owner.

## T-015 composition

Merged T-015 owns the logical Agent Capability Profile family in `schemas/agent-capability-profile-v1.schema.json`. Interchange does not need a receiver-capability object or another exchange family. A request/handoff can correlate to the durable Task/Dispatch/eligibility facts and to canonical profile/evidence refs using existing `work_item_ref`, `payload_ref` and `causation.correlation_refs` strings. The semantic meaning remains with those owning artifacts; the envelope only correlates them.

Therefore fields such as these are intentionally **not** Interchange properties:

```text
receiver_capability_profile
receiver_capability_score
eligibility_decision
availability_state
review_pass
validation_pass
agent_exchange_authority
```

The closed envelope schema rejects such ad-hoc ownership. If a future Product requirement needs a first-class interoperable field that cannot be represented by existing durable refs/correlation, that concrete gap must be demonstrated and the Task/Execution Pack rebound before a compatible same-family schema extension is attempted.

## Compatibility conclusion

For current v4.8 T-003:

```text
INTERCHANGE_SCHEMA_CHANGE=NO_CHANGE_REQUIRED
GITHUB_PROTOCOL_CHANGE=NO_CHANGE_REQUIRED
NEW_EXCHANGE_FAMILY=FORBIDDEN
EVENT_V3=NOT_REQUIRED
T015_PROFILE_OWNER=REFERENCED_NOT_COPIED
ACK_DELIVERY_PROGRESS_AUTHORITY=NONE
```

This is a positive compatibility result, not an absence of work. Focused conformance in `scripts/test_v48_interchange_profile.py` locks the owner and backward-compatibility boundaries while leaving later T-009 replay/restart conformance to its own Task.
