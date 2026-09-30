# Task Pack — T09 Adoption / Migration Wiring

```yaml
task_id: T09
repository: kaicreator-mm/ai-development-standard
version: 4.7.0
integration_target: version/v4.7.0
merge_target: version/v4.7.0
dependencies: [T02, T03, T04, T05, T06]
allowed_write_set:
  - templates/golden/STANDARD_COVERAGE.json
  - templates/project/.dev-standard/PROJECT_OVERRIDES.md
  - checklists/project-init.md
  - checklists/pr-review.md
  - checklists/version-closure.md
  - docs/implementation/4.7.0/MIGRATION_ADOPTION.md
  - docs/implementation/4.7.0/FUTURE_MAJOR_REGISTER.md
  - scripts/test_v47_adoption_wiring.py
forbidden_scope:
  - owner semantics duplication
  - physical standards/reference path migration
  - compatibility alias removal
  - mandatory adoption of optional capabilities
acceptance:
  - project bootstrap/adoption can discover v4.7 registry/routing without loading all optional capabilities
  - Golden coverage reflects new normative surface without becoming authority
  - checklists point to canonical owners rather than restating rules
  - future-major register captures incompatible convergence findings
  - stable aliases/paths remain supported
adversarial_minimum:
  - central wiring technical necessity cannot authorize paths outside this write-set
  - Golden coverage cannot grant normative or mutation authority
  - project overrides cannot silently weaken Frozen/Core rules
  - v4.7 adoption cannot force every project to instantiate optional registries/profiles when non-applicable
required_gates:
  - focused wiring tests
  - integration Validation
  - Fresh Independent Review
validation_owner: T09
review_policy: required
l3_requirement: docs/implementation/4.7.0/L3_REFERENCE_PACKS.md#t09--adoption--migration-wiring
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: any required central path not listed above requires an explicit Task Pack authority amendment before mutation. Incompatible path/contract migration goes to FUTURE_MAJOR_REGISTER unless separately authorized.
