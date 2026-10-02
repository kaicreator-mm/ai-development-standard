# Task Pack — T08 Conformance, Dogfood & Closure Inputs

```yaml
task_id: T08
repository: kaicreator-mm/ai-development-standard
version: 4.1.0
integration_target: version/v4.1.0
merge_target: version/v4.1.0
task_pack_ref: docs/implementation/4.1.0/task-packs/T08_conformance_dogfood.md
dependencies: [T07]
allowed_write_set:
  - templates/golden/V41_EXECUTION_FOUNDATION_EXAMPLES.json
  - docs/implementation/4.1.0/SELF_DOGFOOD_EVIDENCE.md
  - docs/implementation/4.1.0/CONFORMANCE_STATUS.md
  - scripts/test_v41_execution_foundation_conformance.py
  - scripts/test_verify_standard.py
forbidden_scope:
  - substantive production contract changes to T01-T07
  - release verdict or repository integration
  - weakening fixtures to obtain PASS
acceptance:
  - Frozen PRD unsafe-shortcut negatives are machine-covered
  - representative historical v4 payloads remain compatible
  - minimal/Fast-Path positive path passes
  - Node/npm plus non-Node dependency/toolchain example passes
  - multi-Agent isolation/handoff/recovery scenario passes
  - provider sandbox/real-dependency fidelity scenario passes
  - evidence index distinguishes Task/integration proof from Release Qualification
required_gates:
  - full repository verifier/regression on exact candidate SHA
  - v4.1 focused conformance matrix
validation_scope: integration
validation_owner: T08
review_policy: required
l3_requirement: docs/implementation/4.1.0/L3_REFERENCE_PACKS.md#t08--conformance-dogfood--closure-inputs
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
execution_pack: JIT
```

## Why

T08 validates the dependency-complete execution foundation rather than proving each concern in isolation. It is the final implementation Task before version-level Closure / Release Qualification.

## Acceptance detail

Exercise authority non-escalation, dependency/toolchain semantics, secret-ref-only handling, workspace ownership/recovery, artifact promotion, external fidelity, progressive adoption and language neutrality. Produce durable dogfood/conformance evidence without declaring Release READY.

## Out of scope

No production contract redesign, no new feature implementation, no hidden fixture leakage, no final Release Qualification or merge to main.
