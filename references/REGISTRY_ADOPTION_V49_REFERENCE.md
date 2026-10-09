# V4.9 Registry / Manifest / Adoption Reference

Status: non-authoritative integration map for v4.9 T-011 (central registry / manifest / adoption wiring). It routes discovery; it owns nothing.

```text
authority_effect=NONE
gate_effect=NONE
mutation_authorized=false
MACHINE_FAMILY_TARGET_V49=EXACTLY_1_NEW_DEFAULT_FAMILY
```

This reference is discovery and adoption wiring only. Reading it, being registered through it, or being discovered by it does not grant mutation, merge, Validation, Review, Candidate, Closure, Deployment or Release authority. The canonical owners named below keep their existing authority; registry metadata never becomes a semantic owner and never gates anything.

## 1. What v4.9 registers

v4.9 introduces exactly one new default machine-contract family and registers it into the preserved v4.7/v4.8 discovery layer. Two versioned successors are registered as same-family successors of already-registered families, not as new families. No fourth unrelated family is created; availability stays derived and non-durable.

| Registered machine contract (exactly once) | Family accounting | Predecessor retained | Compatibility record | Canonical owner (pre-existing, unchanged) |
| --- | --- | --- | --- | --- |
| `schemas/role-execution-profile-v1.schema.json` | the only new default machine family of v4.9 | none (first versioned member) | n/a (new family, no successor record) | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` |
| `schemas/assurance-plan-v2.schema.json` | same-family successor of `schemas/assurance-plan-v1.schema.json` | registered, unchanged | `references/ASSURANCE_PLAN_V2_COMPATIBILITY.json` | `standards/ASSURANCE_PLAN_STANDARD.md` |
| `schemas/task-learning-v2.schema.json` | same-family successor of `schemas/task-learning-v1.schema.json` | registered, unchanged | `references/TASK_LEARNING_V2_COMPATIBILITY.json` | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` (Task Learning family owner) |

The schemas are discoverable through `standard-manifest.json#sections.machine_contracts`; the semantic concerns they serve resolve through `standard-manifest.json#semantic_authorities` (post-T003 inventory: carried v4.7 entries + three v4.8 discovery entries + three v4.9 entries — `assurance-proof-currentness`, `role-execution-profile`, `release-applicability`). The registry stays a plain inventory plus discovery metadata and does not become a semantic owner. The dispatch surface gains only optional reference fields (`assurance_currentness_ref`, `role_profile_ref`, `jit_phase_ref`) under the same v1 identity; the material-change declaration and backward-compatibility evidence live in `references/EXECUTION_CONTRACT_REFS_V49_COMPATIBILITY.json` and `references/EXECUTION_CONTRACT_REFS_V49_REFERENCE.md`.

## 2. Successor discovery (compatibility aliases / same-family chains)

Successor discovery is descriptive and fail-closed; it never relabels evidence and never converts a v1 record into a v2 record:

- Assurance Plan: `ai-dev-assurance/v1` -> `ai-dev-assurance/v2` is a versioned same-family successor chain. `references/ASSURANCE_PLAN_V2_COMPATIBILITY.json` is the machine-checkable compatibility record (owner-family semantics COMPATIBLE; historical v1 record validity COMPATIBLE; `v1-parser-accepts-v2-instance` INCOMPATIBLE is honestly recorded); the adoption window is `references/ASSURANCE_PLAN_V2_REFERENCE.md#8-v1v2-compatibility`.
- Task Learning: `ai-dev/task-learning-v1` -> `ai-dev/task-learning-v2` is a versioned same-family successor chain. `references/TASK_LEARNING_V2_COMPATIBILITY.json` records the dimensions, including the honest INCOMPATIBLE parser directions; the adoption window is `references/TASK_LEARNING_V2_REFERENCE.md#v1v2-compatibility`.
- Dispatch contract refs: `ai-dev/dispatch-v1` remains the family identity before and after the T-008 additive extension; `references/EXECUTION_CONTRACT_REFS_V49_COMPATIBILITY.json` records both blob identities (baseline `4607f6cb`, candidate re-bound `123a6622` after the #805 post-recovery recompose composed the recovered v4.6 dispatch wiring's two optional array fields into the same additive extension; re-bound to the v4.10-integrated dispatch schema blob `90bea625` by the v4.10 integration — claim #779@6084794791 / pre-merge #779@6084805500, merge commit e0315b2a — whose additive optional fields are declared by `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §11.1.1/§28).
- Consumers discover successors by reading the compatibility records through the manifest `references` section; a v1-only consumer that never reads them keeps working unchanged against v1 owners and v1 schemas, which stay registered exactly once.

## 3. Progressive adoption

Adoption remains optional and materiality-driven, unchanged from `references/PROGRESSIVE_DISCLOSURE_ROUTING.md` and `standards/PROJECT_ADOPTION.md`:

- the v4.9 machine contracts and references are loaded only when their owning standard makes them material to the active concern;
- a project with no role profiles, no assurance plans and no task-learning records is not incomplete, and `TASK_LEARNING=NONE_MATERIAL` remains a valid complete outcome;
- `templates/project/.dev-standard/PROJECT_OVERRIDES.md` stays the Fast Path/adoption-level surface; nothing in v4.9 forces unrelated optional context into a Fast Path read;
- upgrading an existing pin is additive-only (see `docs/implementation/4.9.0/MIGRATION_ADOPTION.md`).

## 4. Registry rules (unchanged, fail-closed)

- Unique `entry_id`; one canonical owner per `semantic_concern`; competing owners, broken owner/alias targets, alias chains/cycles and unknown materiality fail closed with no ordering or fallback winner.
- `standard-manifest.json` keeps its legacy `sections` inventory intact and additive; historical consumers reading only `sections` remain valid without knowing about `semantic_authorities`.
- The registry, the state-dimension registry and the read router produce read plans and discovery metadata only: `authority_effect=NONE`, `gate_effect=NONE`, `mutation_authorized=false` on every resolved read.
- Older projects pinned to earlier revisions remain valid; a pin upgrade resolves through the project-standard re-pin route and only adds discovery surfaces.

## 5. Provenance

Wired by v4.9 T-011 (issue #730, dispatch #730@5995609862) at base `version/v4.9.0@a351a6ef9d2c9733d01df46e9dbd4888e392cc97`, consuming the completed owner outputs of v4.9 T-001..T-010 and the T-003 authority/state registration, with the carry-forward registers #745@5992918366 (CF-V49-02), #722@5985991276 (CF-V49-01), #831@5994177360 (stale-pin classification) and #841@5995114854 (T-010 CI registration note) consumed. The focused guards live in `scripts/test_v48_registry_adoption.py` (post-T003 registry inventory re-bind plus the v4.9 family-accounting guard) and the per-lane kernels under `scripts/test_v49_*.py`.
