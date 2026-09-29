# Task Pack — T04 Configuration & Secrets Governance

```yaml
task_id: T04
repository: kaicreator-mm/ai-development-standard
version: 4.1.0
integration_target: version/v4.1.0
merge_target: version/v4.1.0
task_pack_ref: docs/implementation/4.1.0/task-packs/T04_configuration_secrets.md
dependencies: [T01]
allowed_write_set:
  - standards/CONFIGURATION_SECRETS_STANDARD.md
  - references/CONFIGURATION_SECRETS_REFERENCE.md
  - scripts/test_v41_configuration_secrets.py
forbidden_scope:
  - T01 shared schemas except consumption/reference
  - standard-manifest.json
  - PROJECT_OVERRIDES and shared workflow/checklist wiring
  - mandate of one secret manager/provider
acceptance:
  - configuration precedence is deterministic and project-authoritative
  - durable contracts distinguish secret refs from secret values
  - least privilege and redaction/non-persistence rules are explicit
  - unavailable required credentials produce truthful non-PASS execution state
  - short-lived/JIT credentials are preferred where supported but not universally mandatory
required_gates:
  - secret-value leakage negatives
  - precedence/conflict examples
validation_scope: concern
validation_owner: T04
review_policy: required
l3_requirement: docs/implementation/4.1.0/L3_REFERENCE_PACKS.md#t04--configuration--secrets-governance
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
execution_pack: JIT
```

## Why

Configuration and secrets are security-sensitive execution inputs. T04 gives them one owner while keeping actual credential issuance/provider mechanisms project-specific.

## Acceptance detail

Define key/schema authority, deterministic source precedence, non-secret fingerprinting, secret refs/identity, least privilege, redaction, encrypted-in-Git exception boundary, environment identity and truthful credential/config unavailability semantics.

## Out of scope

No universal `.env`, Vault, OIDC, Kubernetes Secret or cloud requirement; no external-system side-effect model; no central adoption wiring.
