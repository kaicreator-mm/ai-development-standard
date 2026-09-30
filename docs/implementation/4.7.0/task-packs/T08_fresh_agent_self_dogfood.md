# Task Pack — T08 Fresh-Agent Self-Dogfood

```yaml
task_id: T08
repository: kaicreator-mm/ai-development-standard
version: 4.7.0
integration_target: version/v4.7.0
merge_target: version/v4.7.0
dependencies: [T05, T07]
allowed_write_set:
  - docs/implementation/4.7.0/dogfood/**
  - scripts/test_v47_fresh_agent_dogfood.py
forbidden_scope:
  - hidden use of prior chat/session context
  - transport-account identity as independence proof
  - static fixture promoted to real external/runtime PASS
  - Product/L2 authority repair inside dogfood task
acceptance:
  - fresh logical Agent/session reconstructs pinned ADS and applicable canonical owners from durable facts
  - current Task/PR/exact SHA/base and allowed mutation/side effects are recovered
  - required Validation/Review gates and next action/blocker are recovered
  - stale issue/PR/currentness is detected rather than silently consumed
  - dogfood evidence states fidelity and logical independence truthfully
adversarial_minimum:
  - prior chat-only fact cannot be required for successful reconstruction
  - stale lower-authority memory cannot override current Git/GitHub facts
  - same user/account cannot by itself prove fresh logical context
  - unavailable real runtime cannot be replaced by fixture PASS
required_gates:
  - dogfood scenario execution
  - exact-subject Validation
  - Fresh Independent Review
validation_owner: T08
review_policy: required
l3_requirement: docs/implementation/4.7.0/L3_REFERENCE_PACKS.md#t08--fresh-agent-self-dogfood
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: if genuinely fresh Agent/session or external tool/runtime capability is material and unavailable, create a durable exact-subject Validation Request and return BLOCKED/NOT_RUN for that claim. Fixture/static evidence remains explicitly labeled.
