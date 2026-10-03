# T-006 JIT Execution Contract

## Exact subject

- Task: `T-006` / Issue `#512`
- Target: `version/v4.8.0`
- JIT branch: `task/v4.8.0-t06-registry-adoption`
- Exact execution base: `257e95531551960cb163a3e20ab2b3d13f415d3c`
- Exact base tree: `1171de2c8afb08d6f793a258ffd0b586007e9dbf`
- Task Pack: `docs/implementation/4.8.0/task-packs/T06_registry_adoption.md` @ blob `6d6ea5b8ad69e1536495ee59228b0037818ac9a7`
- L3: `docs/implementation/4.8.0/L3_T06_REGISTRY_ADOPTION.md` @ blob `a4b7087c2fa53abc655ce22a417eb3e04a7bc8bb`

This pack was prepared on the exact base above. The Builder must re-read live target/dependencies before authoritative implementation. A moved target is not a reason to silently reuse the pack; it requires explicit rebind/currentness handling.

## Objective

Perform only registry/discoverability/adoption integration for already-merged v4.8 owners. The result is metadata/guidance/verifier wiring, never a new semantic or lifecycle authority.

## Exact Builder write set

```text
standard-manifest.json
standards/PROJECT_ADOPTION.md
references/V48_REGISTRY_ADOPTION_REFERENCE.md
docs/implementation/4.8.0/MIGRATION_ADOPTION.md
scripts/test_v48_registry_adoption.py
```

The Builder may create the three currently absent paths in that list. No other repository path may be changed.

## Required semantic kernel

1. Exactly three v4.8 machine families are added to manifest discoverability:
   - Task Learning Evidence v1;
   - Logical Agent Capability Profile v1;
   - Agent Capability Evidence v1.
2. Existing Interchange v1 is reused and remains one manifest entry.
3. Registry/discovery/adoption has no authority/gate/mutation effect.
4. Already-merged sibling schema/reference/semantic owners remain read-only.
5. Historical consumers remain valid; migration is additive.
6. Optional/materiality-driven context stays optional unless current Task/project authority makes it applicable.
7. Fast Path stays lightweight and can use `TASK_LEARNING=NONE_MATERIAL`.
8. v4.7 branch-only registry/progressive-disclosure implementation is lineage input, not current v4.8 authority.

## Authority-effect invariants

The integration reference must state:

```text
authority_effect=NONE
gate_effect=NONE
mutation_authorized=false
```

Manifest membership, project-adoption text, provider/model identity, capability claim/evidence, or verifier success cannot grant merge, Validation PASS, Review PASS, Release READY, scheduler admission, or mutation permission.

## Currentness / phase gates

Before the first authoritative Builder write:

- `version/v4.8.0` must still be bound to the current execution base or the Controller must explicitly rebind this pack;
- #512 native dependency summary must still be `blocked_by=0,total_blocked_by=7`;
- Task Pack/L3 blob identities must match the manifest;
- the five-path write set must remain sufficient.

Builder completion is not Validation. Validation PASS is not Fresh Independent Review PASS. No merge is authorized by this pack.

## Required evidence

Builder terminal must record:

- exact start base SHA/tree;
- exact candidate SHA/tree;
- exact changed paths;
- result of every command listed in the Task Pack;
- whether all five write-set paths were the only mutations;
- `INTERCHANGE_REUSED=YES`;
- `V48_MACHINE_FAMILY_COUNT=3`;
- `REGISTRY_AUTHORITY_EFFECT=NONE`;
- `HISTORICAL_COMPATIBILITY=PRESERVED|BLOCKED`;
- any `NOT_RUN/BLOCKED` limitation;
- Task Learning outcome (`TASK_LEARNING=NONE_MATERIAL` or durable ref).

## Stop / escalation

Stop with a precise reason if the implementation requires a sibling owner edit, v4.7 resolver/schema port, fourth machine family, new Interchange family, destructive migration, workflow/CI/release mutation, or any sixth Builder path. Use `TASK_PACK_DEFECT`, `ARCHITECTURE_AMENDMENT_REQUIRED`, or Controller rebind as appropriate.

Do not self-repair outside the pack.
