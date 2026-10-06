# Deployment Governance Reference

Non-normative guidance for `DEPLOYMENT_GOVERNANCE_STANDARD.md`.

## Deployment Plan worksheet

```text
plan_id:
immutable_artifact_ref:
target_environment_ref:
side_effect_authority_ref:
configuration/environment refs:
migration_transition_refs if material:
rollback_plan_ref if material:
executor/provider mechanism ref:
```

## Deployment Result worksheet

```text
result_id:
plan_ref:
immutable_artifact_ref:
environment_ref:
result_state: DEPLOYMENT_...
evidence_refs:
rollback_result_ref if executed:
```

The result should bind the exact plan, artifact and environment actually exercised.

## Example — staging vs production

A staging deployment can prove the staging tuple. It does not prove production success, even when the artifact bytes are identical, because environment, authority, dependencies and side effects can differ.

## Example — credentials

A cloud token that can update production demonstrates capability. It does not demonstrate that the current Task/operator is authorized to perform that update. Preserve an explicit authority reference.

## Example — rollback

A rollback plan is preparation, not evidence of rollback execution. Rolling back application bytes also does not prove a database/schema rollback or recovery occurred.

## Review prompts

1. Are plan and result separate subjects?
2. Is artifact identity immutable and exact?
3. Is target environment exact enough for the claim?
4. Is side-effect authority explicit rather than inferred from credentials?
5. Is a staging/mock result being promoted to production?
6. Are outcomes namespaced as deployment facts?
7. Is Release or Distribution evidence being misread as deployment truth?
8. Are migration/rollback boundaries preserved?
