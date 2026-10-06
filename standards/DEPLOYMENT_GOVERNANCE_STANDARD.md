# Deployment Governance Standard

Status: **Normative — v4.4**

## 1. Purpose

This standard governs planned and executed deployment side effects for an exact artifact and target environment. Deployment remains distinct from Release qualification, Distribution publication, v4.2 Data/Migration semantics, and v4.1 Configuration/Secrets/External-System authority.

## 2. Authority boundary

Owned here:

- Deployment Plan identity and intended target;
- exact artifact/environment binding;
- explicit side-effect authority required to execute a deployment;
- Deployment Result identity and namespaced deployment-domain facts;
- rollback plan/result references as deployment facts.

Not owned here:

- Release READY/PASS;
- artifact creation/immutable identity;
- publication success;
- database/schema migration transition semantics;
- secret values or credential storage;
- environment/configuration truth already owned by v4.1.

## 3. Plan is not result

A Deployment Plan expresses intended action. A Deployment Result records what happened for the executed plan. They MUST remain separate durable subjects.

Forbidden inference:

```text
Deployment Plan exists/approved -> Deployment succeeded
```

The default machine contracts are `deployment-plan-v1` and `deployment-result-v1`; neither is a Release verdict.

## 4. Exact artifact and environment identity

A deployment claim MUST preserve the exact artifact identity and exact material environment identity used by the execution. Mutable artifact tags, environment nicknames or provider defaults MUST NOT silently replace exact identities where those are material.

A result for staging, test, region A, account A, cluster A or another environment does not establish production/region B/account B/cluster B success.

Required negative:

```text
staging success != production success
```

## 5. Side-effect authority

Possessing credentials, network reachability, a deployment CLI, a provider token, or a functioning API is execution capability, not deployment authority.

Before a material side effect, the plan MUST carry or reference the applicable side-effect authority.

Required negative:

```text
credential/tool capability != production mutation authority
```

If authority is absent, ambiguous or stale, execution is BLOCKED/NOT_RUN in the owning execution flow.

## 6. Deployment outcomes are namespaced facts

Deployment Result outcomes MUST remain deployment-domain facts such as namespaced `DEPLOYMENT_*` values. They MUST NOT mint generic `PASS`, `READY`, Validation or Release states.

Examples may include provider/project-defined facts equivalent to:

```text
DEPLOYMENT_SUCCEEDED
DEPLOYMENT_FAILED
DEPLOYMENT_PARTIAL
DEPLOYMENT_ROLLED_BACK
```

The exact vocabulary may be extensible; namespacing prevents cross-owner inference.

## 7. Release and publication boundaries

`Release READY != Deployment SUCCESS`.

Likewise:

```text
publication success != deployment success
artifact promoted != deployment success
```

Release qualification may authorize a candidate for release without proving any deployment occurred. Distribution may publish bytes without proving target activation.

## 8. Migration boundary

Deployment may reference v4.2 Migration Transition evidence/plans when data/schema transition is material. Those references do not transfer migration authority into Deployment.

Required negatives:

```text
artifact rollback != data/schema rollback
rollback plan exists != rollback executed
```

A deployment rollback result records deployment-side execution facts only. Data recovery/reversion remains governed by Data & Migration authority.

## 9. Evidence fidelity

Sandbox/mock/staging evidence proves only the dimensions actually exercised. A simulated provider response MUST NOT become real production Deployment success.

If real environment execution is required for a claim and unavailable, create an exact-subject Validation handoff or leave the execution BLOCKED/NOT_RUN.

## 10. Required forbidden inferences

| Input fact | Forbidden conclusion |
|---|---|
| Release READY | Deployment succeeded |
| artifact published | Deployment succeeded |
| plan approved | plan executed successfully |
| staging succeeded | production succeeded |
| credentials/tool available | production mutation authorized |
| rollback plan exists | rollback executed |
| artifact rollback executed | data/schema rollback executed |
| mock/sandbox succeeded | real environment succeeded |

## 11. Failure handling

Environment identity, artifact identity, side-effect authority and execution-result uncertainty fail closed. Do not guess an environment, reuse another environment's PASS, or infer side-effect authority from credential possession.

Provider-specific rollout strategies remain project/profile authority unless separately standardized.
