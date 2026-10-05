# V4.9 Registry / Manifest / Adoption — Migration & Adoption Note

Status: additive migration note for v4.9 T-011 (central registry / manifest / adoption wiring). This note moves nothing and retitles nothing; it records what becomes discoverable in v4.9 and what stays valid.

## 1. Additive-only posture

The v4.9 registry/manifest/adoption wiring is a pure addition on top of the current v4.9 standard revision:

- every pre-v4.9 manifest section, entry and inherited inventory is preserved verbatim; no historical entry is removed, renamed or rewritten, and no destructive migration exists in this change;
- `standard-manifest.json` gains the completed v4.9 outputs for discoverability: three machine contracts (`schemas/role-execution-profile-v1.schema.json` — the only new default machine family — plus the same-family successors `schemas/assurance-plan-v2.schema.json` and `schemas/task-learning-v2.schema.json`), the v4.9 references (Assurance Plan owner/v2 surfaces, Role Execution Profile v1, Task Learning v2, Execution Contract refs v4.9, gate-owned evidence currentness matrix, JIT DAG mutation governance, release applicability, proportional orchestration, and `references/REGISTRY_ADOPTION_V49_REFERENCE.md`), and the ten `scripts/test_v49_*.py` focused kernels in the `verification` section. This closes the T-002 output-registration gap noted at #793/#794;
- the pinned CI battery `.github/workflows/verify-standard.yml` gains the ten v4.9 focused kernels appended in the established style; existing commands are unremoved and unreordered;
- consumers that read only the legacy `sections` inventory keep working unchanged.

## 2. Older pinned projects remain valid

Projects pinned to any earlier revision keep their pinned behavior:

- registry and manifest adoption metadata grants no semantic authority (`authority_effect=NONE`, `gate_effect=NONE`, `mutation_authorized=false`); registration changes nothing an owner decides;
- every v1 machine contract stays registered exactly once next to its successor: `schemas/assurance-plan-v1.schema.json` and `schemas/task-learning-v1.schema.json` remain valid, resolvable targets, and v1 records are never relabeled as v2 records;
- the dispatch contract keeps its v1 family identity; the T-008 additions are optional reference fields, and a v1 producer/consumer pair continues to interoperate (see `references/EXECUTION_CONTRACT_REFS_V49_REFERENCE.md#backward-compatibility`);
- the state registry's forbidden inferences stay in force: an old exact-SHA Validation PASS must not be inferred to be a successor PASS.

## 3. Re-pin route (project-standard, resolving)

To adopt v4.9, a consumer project follows the unchanged immutable pin procedure:

1. Re-pin `.dev-standard/VERSION` to the current v4.9 revision (immutable resolution procedure per `standards/PROJECT_ADOPTION.md` §2.1).
2. Run the project-standard verification route (`python scripts/verify_project_standard.py`, guarded by `scripts/test_verify_project_standard.py`); it resolves the re-pinned revision through the wired manifest and passes unchanged — no project-side manifest edits are required.
3. Optionally declare the v4.9 convergence surfaces in `.dev-standard/PROJECT_OVERRIDES.md` and use `references/REGISTRY_ADOPTION_V49_REFERENCE.md` as the non-authoritative map of what is discoverable.

The route is verified against the wired manifest: every newly registered path exists at the candidate, sections stay globally unique, and the exact-set guards in `scripts/test_v48_registry_adoption.py` still fail closed on unlisted additions, removals or duplicates.

## 4. What changed for consumers in v4.9

- Role Execution Profile v1 is available as a projection contract owned by `standards/EXECUTION_ARCHITECTURE_STANDARD.md`; it is the only new default machine family of v4.9 and adopts only when material.
- Assurance Plan authors may version plans to `ai-dev-assurance/v2` under the same owner (`standards/ASSURANCE_PLAN_STANDARD.md`); the v1/v2 window and parser directions are recorded in `references/ASSURANCE_PLAN_V2_COMPATIBILITY.json` / `references/ASSURANCE_PLAN_V2_REFERENCE.md`.
- Task Learning recorders may emit `ai-dev/task-learning-v2` records under the same family owner; `references/TASK_LEARNING_V2_COMPATIBILITY.json` / `references/TASK_LEARNING_V2_REFERENCE.md` record the same-family chain.
- Dispatch envelopes may carry the new optional reference fields; nothing requires them.
- Gate evidence carries an owner-scoped currentness matrix (`references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md`); release qualification gains per-gate applicability resolution (`references/RELEASE_APPLICABILITY_REFERENCE.md`).

## 5. What does not change

- Canonical owner boundaries are unchanged: role profile projection, execution state, task learning and capability surfaces remain owned by `standards/EXECUTION_ARCHITECTURE_STANDARD.md`; assurance composition and currentness by `standards/ASSURANCE_PLAN_STANDARD.md`; release qualification and per-gate applicability by `standards/RELEASE_STANDARD.md`; Interchange stays the existing v4.0 owner with `schemas/interchange-envelope-v1.schema.json` reused exactly once.
- No second lifecycle, no availability/provider-capability durable family, and no Interchange v2 exists; availability stays derived and provider/capability metadata stays non-authority.
- Fast Path stays lightweight and orthogonal to adoption level; `TASK_LEARNING=NONE_MATERIAL` remains a valid complete outcome, and adopting v4.9 does not require loading unrelated optional registries, profiles, packs or automation.
