# Task Pack — T01 Shared Operations Machine Contracts

```yaml
task_id: T01
repository: kaicreator-mm/ai-development-standard
version: 4.5.0
integration_target: version/v4.5.0
merge_target: version/v4.5.0
dependencies: []
allowed_write_set:
  - schemas/runtime-observation-context-v1.schema.json
  - schemas/incident-event-v1.schema.json
  - schemas/maintenance-policy-v1.schema.json
  - narrowly justified optional references in existing evidence schemas
  - scripts/test_v45_operations_contracts.py
forbidden_scope:
  - normative operations policy
  - raw telemetry storage
  - new workflow/Validation/Release state authority
acceptance:
  - repository-supported Draft 2020-12 schemas
  - runtime observation binds material subject/window without universal PASS/healthy field
  - incident facts are append-oriented and do not erase history
  - maintenance support state is explicit and not inferred from branch/tag/package
  - historical payloads remain valid when optional refs are absent
  - no ordinary secret/credential/PII value fields
required_gates: [focused contract tests, concern Validation, Fresh Independent Review]
validation_owner: T01
review_policy: required
l3_requirement: docs/implementation/4.5.0/L3_REFERENCE_PACKS.md#t01--shared-operations-machine-contracts
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: unsupported schema keywords, backward-compatibility regression, or pressure to introduce lifecycle/Gate authority fails closed inside T01; do not weaken the verifier.
