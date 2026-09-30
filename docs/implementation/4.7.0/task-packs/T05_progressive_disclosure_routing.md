# Task Pack — T05 Progressive Disclosure Routing

```yaml
task_id: T05
repository: kaicreator-mm/ai-development-standard
version: 4.7.0
integration_target: version/v4.7.0
merge_target: version/v4.7.0
dependencies: [T02, T04]
allowed_write_set:
  - references/PROGRESSIVE_DISCLOSURE_ROUTING.md
  - scripts/resolve_standard_read_set.py
  - scripts/test_v47_progressive_disclosure.py
forbidden_scope:
  - Context Snapshot schema/database
  - new durable authority store
  - v4.6 Context Engineering semantic redefinition
  - model/provider-specific routing mandate
acceptance:
  - read routing composes AGENTS + pinned ADS + semantic registry + PROJECT_OVERRIDES + profiles + exact task/execution authority
  - higher-currentness durable authority defeats stale lower history/chat
  - optional/non-applicable capability does not force extra context
  - material applicability or owner ambiguity fails closed
  - derived read plan remains non-authoritative/debuggable
adversarial_minimum:
  - stale chat/memory cannot override current repository/GitHub authority
  - larger context volume cannot imply higher authority
  - file order cannot resolve owner conflict
  - tool/resource availability cannot create requirement or side-effect authority
required_gates:
  - focused routing tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T05
review_policy: required
l3_requirement: docs/implementation/4.7.0/L3_REFERENCE_PACKS.md#t05--progressive-disclosure-routing
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: unresolved material applicability/currentness produces an explicit fail-closed route to the owning planning/human authority. No guessed context winner.
