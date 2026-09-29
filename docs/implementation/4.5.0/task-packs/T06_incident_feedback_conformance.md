# Task Pack — T06 Incident / Feedback Conformance & Dogfood

```yaml
task_id: T06
repository: kaicreator-mm/ai-development-standard
version: 4.5.0
integration_target: version/v4.5.0
merge_target: version/v4.5.0
dependencies: [T02, T03]
allowed_write_set:
  - v4.5 incident/feedback conformance fixtures and evidence
  - scripts/test_v45_incident_feedback_conformance.py
  - docs/implementation/4.5.0/dogfood/incident-feedback/**
forbidden_scope:
  - new incident normative policy
  - unauthorized production side effects
  - Deployment/Migration recovery semantic redefinition
acceptance:
  - controlled incident flow demonstrates detection -> mitigation/recovery -> verification -> follow-up
  - missing verification and unresolved follow-up negatives are covered
  - recovery actions preserve v4.4/v4.2/v4.1 owner boundaries
  - incident facts cannot rewrite prior Release/Deployment evidence
  - escaped defect creates durable regression/scenario/follow-up path
  - secret/PII leakage negatives are covered
required_gates:
  - focused conformance/dogfood tests
  - exact-environment Validation for any real side-effect scenario
  - Fresh Independent Review
validation_owner: T06
review_policy: required
l3_requirement: docs/implementation/4.5.0/L3_REFERENCE_PACKS.md#t06--incident--feedback-conformance--dogfood
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: simulated/controlled incident evidence is acceptable only for the dimensions it proves. Any required real mutation without environment/access/authority becomes an exact-scope Validation handoff; credential presence never grants authority.
