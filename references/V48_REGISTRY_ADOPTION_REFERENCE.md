# V4.8 Registry / Discoverability / Adoption Reference

Status: non-authoritative integration map for v4.8 T-006. It routes discovery; it owns nothing.

```text
authority_effect=NONE
gate_effect=NONE
mutation_authorized=false
```

This reference is discovery and adoption wiring only. Reading it, registering in it, or being discovered by it does not grant mutation, merge, Validation, Review, Candidate, Closure, Deployment or Release authority. The canonical owners named below keep their existing authority.

## 1. What v4.8 registers

v4.8 introduces exactly three new default machine-contract families and registers them into the preserved v4.7 discovery layer. No fourth family is created; availability is not a family.

| New family (schema, registered exactly once) | Semantic concern (`entry_id`) | Canonical owner (pre-existing, unchanged) | Applicability posture |
| --- | --- | --- | --- |
| `schemas/task-learning-v1.schema.json` | `execution.task_learning_evidence` (`task-learning-evidence`) | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | `MATERIALITY_DRIVEN` |
| `schemas/agent-capability-profile-v1.schema.json` | `execution.logical_agent_capability_claim` (`logical-agent-capability-profile`) | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | `MATERIALITY_DRIVEN` |
| `schemas/agent-capability-evidence-v1.schema.json` | `execution.agent_capability_evidence` (`agent-capability-evidence`) | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | `MATERIALITY_DRIVEN` |

`MACHINE_FAMILY_TARGET=EXACTLY_3`. The schemas are discoverable through `standard-manifest.json#sections.machine_contracts` and `standard-manifest.json#semantic_authorities`; the registry is a plain inventory plus discovery metadata and does not become a semantic owner. Semantic ownership of Task Learning, logical Agent capability claims and Agent Capability Evidence remains entirely with `standards/EXECUTION_ARCHITECTURE_STANDARD.md`. Runner/host capability remains owned by `standards/CI_RUNNER_CAPABILITY_STANDARD.md` (`ci.runner_capability_adoption`).

## 2. Interchange

`INTERCHANGE_POLICY=REUSE_EXISTING_V1_EXACTLY_ONCE`. Interchange remains the existing `schemas/interchange-envelope-v1.schema.json` / v4.0 `AGENT_INTERCHANGE.md` owner family, listed exactly once. No v2 envelope, second interchange owner or parallel exchange family is created. Interchange stays correlation/transport only and never owns lifecycle, Validation, Candidate or Release truth.

## 3. Availability and capability metadata are not authority

- Current Availability is a derived normalization over applicable owners. It has no durable family, no registry entry and no schema; it must not be materialized as a fourth machine family.
- `PROVIDER_IDENTITY=NOT_AUTHORITY`: provider/model identity or availability never grants correctness, authorization, routing admission, Validation, Review or Release truth.
- `CAPABILITY_EVIDENCE=NOT_CURRENT_VALIDATION_REVIEW_TRUTH`: an Agent Capability Profile or Capability Evidence record describes claimed/logical capability or historical evidence. It does not absorb runner/host resources, current capacity/Availability, or current Validation/Review truth, and it does not replace any existing owner's current facts.

## 4. Fast Path

Fast Path remains lightweight and orthogonal to adoption level. `TASK_LEARNING=NONE_MATERIAL` is a valid complete outcome: projects with no material task learning record nothing and instantiate nothing. Optional registries, profiles and machine families are loaded only when material to the active concern; their existence in v4.8 is never a project adoption requirement and never forces unrelated optional context into a Fast Path read.

## 5. v4.7 carry-forward provenance

The discovery layer is carried forward from the pinned canonical source `version/v4.7.0@d8f613127d0167453297a5a5e983de048607aa07` (tree `721dd393b7693d2ce82ebe0533a7fa51726d0a78`):

```text
COPY EXACT (pinned v4.7 T01–T06 portable stack; byte-for-byte, blob-identity pinned):
  schemas/authority-applicability-entry-v1.schema.json
  schemas/state-dimension-registry-v1.schema.json
  scripts/test_v47_convergence_metadata_contracts.py
  references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md
  scripts/test_v47_authority_registry.py
  registries/state-dimensions-v1.json
  references/STATE_DIMENSION_REGISTRY_REFERENCE.md
  scripts/test_v47_state_dimension_registry.py
  standards/REFERENCE_CONVENTION_STANDARD.md
  references/REFERENCE_CONVENTION_REFERENCE.md
  scripts/test_v47_reference_conventions.py
  references/PROGRESSIVE_DISCLOSURE_ROUTING.md
  scripts/resolve_standard_read_set.py
  scripts/test_v47_progressive_disclosure.py
  references/COMPATIBILITY_ALIAS_CONFORMANCE.md
  scripts/test_v47_compatibility_aliases.py

COMPOSE (current v4.8 text is the base; discovery wiring added):
  standard-manifest.json
  standards/PROJECT_ADOPTION.md
  templates/project/.dev-standard/PROJECT_OVERRIDES.md

ADD (v4.8-owned integration surfaces):
  references/V48_REGISTRY_ADOPTION_REFERENCE.md
  docs/implementation/4.8.0/MIGRATION_ADOPTION.md
  scripts/test_v48_registry_adoption.py
```

The carried files remain discovery/reference/conformance surfaces; none becomes a new semantic owner. Version-bound v4.7 conformance/closure/dogfood/release evidence (`docs/implementation/4.7.0/**`, `references/V47_SEMANTIC_CONFORMANCE_MATRIX.md`, `scripts/v47_conformance.py`, `scripts/test_v47_semantic_conformance.py` and related) stays source read-only at the pinned v4.7 revision; its semantic invariants are re-exercised against v4.8 by `scripts/test_v48_registry_adoption.py` and the carried focused tests, and historical exact-subject evidence is never rebound to v4.8 subjects.

## 6. Registry rules (unchanged, fail-closed)

- Unique `entry_id`; one canonical owner per `semantic_concern`; the same existing owner may serve distinct concerns; competing owners, broken owner/alias targets, alias chains/cycles and unknown materiality fail closed with no ordering or fallback winner.
- `standard-manifest.json` keeps its legacy `sections` inventory intact and additive; historical consumers reading only `sections` remain valid without knowing about `semantic_authorities`.
- The registry, the state-dimension registry and the read router produce read plans and discovery metadata only: `authority_effect=NONE`, `gate_effect=NONE`, `mutation_authorized=false` on every resolved read.
