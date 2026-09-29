# Task Pack — T07 Maintenance / Hotfix Conformance & Dogfood

```yaml
task_id: T07
repository: kaicreator-mm/ai-development-standard
version: 4.5.0
integration_target: version/v4.5.0
merge_target: version/v4.5.0
dependencies: [T04]
allowed_write_set:
  - v4.5 maintenance/hotfix conformance fixtures and evidence
  - scripts/test_v45_maintenance_hotfix_conformance.py
  - docs/implementation/4.5.0/dogfood/maintenance-hotfix/**
forbidden_scope:
  - rewriting historical release/validation evidence
  - branch existence as support authority
  - unrelated release-line mutation
acceptance:
  - support policy identifies line/baseline/change-class authority
  - source change and maintenance baseline are exact-identity bound
  - backport/cherry-pick resulting exact SHA is recorded
  - result SHA obtains its own applicable testing/Validation evidence
  - old source PASS is rejected as result-SHA PASS
  - hotfix Release/Deployment truth remains separate
required_gates:
  - focused conformance/dogfood tests
  - exact-result-SHA Validation
  - Fresh Independent Review
validation_owner: T07
review_policy: required
l3_requirement: docs/implementation/4.5.0/L3_REFERENCE_PACKS.md#t07--maintenance--hotfix-conformance--dogfood
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: if no suitable maintenance baseline/tooling is available, use a bounded fixture and label its fidelity or create a dedicated handoff. Never transfer source-branch Review/Validation PASS to the backported subject.
