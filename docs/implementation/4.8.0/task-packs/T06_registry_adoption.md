# Task Pack — T-006 Registry / Discoverability / Adoption Wiring

Status: **JIT-FINALIZED FOR BUILDER HANDOFF — IMPLEMENTATION NOT YET PERFORMED**

```yaml
task_id: T-006
repository: kaicreator-mm/ai-development-standard
version: 4.8.0
parent_issue: "#512"
lane: registry-adoption
integration_target: version/v4.8.0
merge_target: version/v4.8.0
exact_planning_base: 257e95531551960cb163a3e20ab2b3d13f415d3c
exact_planning_base_tree: 1171de2c8afb08d6f793a258ffd0b586007e9dbf
dependencies:
  - T-001/#507
  - T-015/#522
  - T-016/#524
  - T-002/#510
  - T-003/#508
  - T-004/#511
  - T-005/#509
review_policy: required
validation_owner: independent-from-builder
validation_scope: exact-subject-integration
agent_freedom: F2_ENGINEERING_DISCRETION
jit_branch: task/v4.8.0-t06-registry-adoption
execution_pack: .agent/execution/T-006
risk: medium-high
```

## Purpose

T-006 is the **central discovery/adoption integration concern** after all seven semantic owners have merged. It does not create a new semantic owner, scheduler, authority store, capability truth source, or interchange family.

The Builder must make the already-merged v4.8 contracts discoverable from the current branch and expose bounded project-adoption / progressive-disclosure guidance without duplicating sibling semantics.

## Frozen authority

- Frozen Product: `docs/implementation/4.8.0/PRD.md` @ blob `f26439580e00de6ed8b2e27d732a3095eb566219`.
- Frozen L2: `docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md` @ blob `f88c85454e80101a0fdf56050e21f11a05279841`.
- Frozen Task DAG R2: `docs/implementation/4.8.0/TASK_DAG.md` @ blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc`.
- Issue authority: `#512`.
- JIT exact base: `version/v4.8.0@257e95531551960cb163a3e20ab2b3d13f415d3c`, tree `1171de2c8afb08d6f793a258ffd0b586007e9dbf`.

If any of these currentness conditions changes before authoritative Builder mutation, stop and request Execution Pack rebind.

## Dependency completion

Native GitHub Issue Dependencies are authoritative. At JIT planning time `#512` reports `blocked_by=0,total_blocked_by=7`; the seven canonical blockers are completed:

- T-001 / #507 — Task Learning Evidence v1.
- T-015 / #522 — Logical Agent Capability Profile v1.
- T-016 / #524 — Agent Capability Evidence v1.
- T-002 / #510 — Execution Architecture Core.
- T-003 / #508 — existing Interchange v1 profile/reuse.
- T-004 / #511 — Task Learning closeout/adoption wiring.
- T-005 / #509 — ADS Evolution Governance.

Their merged outputs are **read-only inputs** to T-006. T-006 must not repair or redefine them.

## Builder write set

Exactly:

```text
standard-manifest.json
standards/PROJECT_ADOPTION.md
references/V48_REGISTRY_ADOPTION_REFERENCE.md
docs/implementation/4.8.0/MIGRATION_ADOPTION.md
scripts/test_v48_registry_adoption.py
```

No other path is authorized by this pack. If implementation proves that another central path is technically necessary, stop and request a Task Pack / Execution Pack amendment rather than widening the diff.

## Required integration result

### 1. Manifest discoverability

`standard-manifest.json` must make exactly these three v4.8 machine-contract families discoverable as additions to the existing manifest inventory:

1. `schemas/task-learning-v1.schema.json`
2. `schemas/agent-capability-profile-v1.schema.json`
3. `schemas/agent-capability-evidence-v1.schema.json`

The existing `schemas/interchange-envelope-v1.schema.json` remains listed exactly once. Do not introduce an `Interchange v2` or another interchange owner.

The manifest may add the already-merged v4.8 reference/test paths needed to discover and verify these families, but registry presence remains metadata only.

### 2. Project adoption / progressive disclosure

`standards/PROJECT_ADOPTION.md` and `references/V48_REGISTRY_ADOPTION_REFERENCE.md` must describe a lightweight read path:

- existing projects remain valid under their pinned standard and historical contracts;
- v4.8 consumers discover the three new families only when relevant to the Task/project;
- optional/materiality-driven context is not loaded merely because a file/provider/capability exists;
- a Fast Path may remain one directly eligible executor + ordinary Dispatch/Claim + `TASK_LEARNING=NONE_MATERIAL`;
- registry/reference presence never grants mutation, merge, Validation PASS, Review PASS, Release READY, or provider/model trust.

### 3. Migration/adoption note

`docs/implementation/4.8.0/MIGRATION_ADOPTION.md` must provide additive migration guidance and an explicit non-rewrite posture for historical Task Packs, Execution Packs, Dispatch/Claim, Interchange v1, event-v2, Validation and Review evidence.

### 4. Focused verifier

`scripts/test_v48_registry_adoption.py` must deterministically verify at minimum:

- the exact three v4.8 machine families are discoverable;
- existing Interchange v1 is present exactly once;
- the three owner references and v4.8 Interchange compatibility reference are discoverable;
- the T-006 adoption reference and focused verifier are themselves discoverable where appropriate;
- no fourth v4.8 machine family is introduced by T-006;
- adoption/reference text preserves metadata-only, Fast Path, and no-authority boundaries;
- the base-to-candidate manifest diff adds only the intended v4.8 discovery surface and does not remove historical inventory.

## v4.7 lineage boundary

The predecessor `version/v4.7.0` contains `references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md` and `references/PROGRESSIVE_DISCLOSURE_ROUTING.md`; those files are not physically present on the current `version/v4.8.0` base.

They are lineage/read-only design inputs only. T-006 must **not** silently copy them into v4.8, manufacture their absent schema/resolver machinery, or claim that their branch-local implementation is already integrated. The v4.8 task-owned reference may preserve compatible discovery principles without becoming a competing semantic owner.

If acceptance truly requires porting the v4.7 registry resolver/schema/semantic-authority implementation, stop with `ARCHITECTURE_AMENDMENT_REQUIRED` / Controller rebind.

## Forbidden scope

- Frozen Product, Frozen L2, or Frozen Task DAG mutation.
- Any sibling schema, reference, normative semantic owner, or conformance implementation rewrite.
- A fourth v4.8 machine-contract family.
- A new Interchange owner/family/version.
- `semantic_authorities` or another registry authority model invented by T-006.
- provider/model identity becoming correctness, authorization, or ranking authority.
- capability claims/evidence becoming current Validation/Review truth.
- project adoption becoming mandatory for non-applicable optional capabilities.
- `.github/workflows/**`, CI policy, Release/Closure authority, T-013, or T-014.

## Acceptance

- [ ] Exactly three new v4.8 machine families are discoverable from the current manifest.
- [ ] Existing Interchange v1 is reused and appears once.
- [ ] Registry/discovery/adoption artifacts have `authority_effect=NONE`, `gate_effect=NONE`, and no mutation authorization semantics.
- [ ] Existing/historical consumers remain valid; no destructive migration is required.
- [ ] Fast Path remains lightweight and does not require loading every optional family/reference.
- [ ] No sibling semantic owner is rewritten.
- [ ] Focused verifier + required regressions pass on the exact candidate.
- [ ] Independent exact-subject Validation passes before Fresh Independent Review.

## Required commands

```text
python -B scripts/test_v48_registry_adoption.py
python -B scripts/test_v48_task_learning.py
python -B scripts/test_v48_agent_capability_profile.py
python -B scripts/test_v48_agent_capability_evidence.py
python -B scripts/test_v48_interchange_profile.py
python -B scripts/test_v48_contract_compatibility.py
python -B scripts/test_work_item_contract_and_golden_templates.py
python -B scripts/verify_standard.py
```

Builder command results are implementation evidence only. They do not substitute for independent Validation.

## Failure handling

Stop and escalate rather than widen scope when:

- exact base, frozen blobs, Task Pack, L3, or Execution Pack currentness drifts;
- native blockers are no longer zero;
- a required path is outside the five-path Builder write set;
- integration requires changing sibling semantics/schema ownership;
- a duplicate/new Interchange owner or fourth machine family is needed;
- v4.7 branch-only artifacts are required as current v4.8 authority;
- historical compatibility cannot be preserved additively;
- focused/regression tests expose a semantic defect owned by another Task.

The correct outcome can be `BLOCKED`, `TASK_PACK_DEFECT`, `ARCHITECTURE_AMENDMENT_REQUIRED`, or a bounded owner repair; never silently broaden T-006.
