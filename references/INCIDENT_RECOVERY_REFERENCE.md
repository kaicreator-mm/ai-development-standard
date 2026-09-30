# Incident, Recovery & Engineering Feedback Reference

Non-normative guidance for `INCIDENT_RECOVERY_FEEDBACK_STANDARD.md`.

## Append-oriented event example

```text
DETECTED -> MITIGATED -> RECOVERED -> VERIFIED -> FOLLOW_UP
```

This is not a mandatory global lifecycle state machine. It illustrates distinct durable facts. A project may record additional facts without collapsing their meanings.

## Recovery references

An incident may reference a Deployment rollback result, migration recovery evidence, configuration change, credential rotation or external-system action. Each mutation remains governed by its owning authority; the incident does not grant that authority.

## Verification example

After a rollback restores service, verify the affected exact subject/environment and record whether the triggering condition is absent. If a permanent corrective change is later produced, it receives its own Testing/Validation/Review evidence.

## Feedback routing worksheet

```text
incident_ref:
reproduction_ref:
regression_scenario_ref:
product_or_architecture_ref:
runbook_or_config_ref:
standard_gap_ref:
unresolved_follow_up_refs:
```

Use only applicable routes. Closure does not mean every optional field is populated; it means required unresolved follow-up remains durable and visible.
