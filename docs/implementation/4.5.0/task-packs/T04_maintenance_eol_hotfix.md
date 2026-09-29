# Task Pack — T04 Maintenance, EOL & Hotfix

```yaml
task_id: T04
repository: kaicreator-mm/ai-development-standard
version: 4.5.0
integration_target: version/v4.5.0
merge_target: version/v4.5.0
dependencies: [T01]
allowed_write_set:
  - standards/MAINTENANCE_EOL_HOTFIX_STANDARD.md
  - references/MAINTENANCE_EOL_HOTFIX_REFERENCE.md
  - scripts/test_v45_maintenance_hotfix.py
forbidden_scope:
  - branch/tag/package existence as support authority
  - Git provenance redefinition
  - Validation/Review/Release result ownership
acceptance:
  - supported line/baseline and allowed change classes are explicit
  - support vocabulary is project-mappable/extensible
  - deprecation/EOL authority and upgrade/migration refs are representable
  - backport/cherry-pick provenance binds source, maintenance baseline and resulting exact SHA
  - source-branch PASS never transfers automatically to the result SHA
  - hotfix urgency may reduce non-required ceremony only under explicit authority
required_gates: [focused semantic tests, concern Validation, Fresh Independent Review]
validation_owner: T04
review_policy: required
l3_requirement: docs/implementation/4.5.0/L3_REFERENCE_PACKS.md#t04--maintenance-eol--hotfix
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: unclear support policy, baseline or hotfix authority fails closed. The resulting maintenance-branch SHA must obtain its own applicable current testing/Validation/Release evidence.
