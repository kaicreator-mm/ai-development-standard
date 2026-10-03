# v4.8 T-006 L3 — Registry / Discoverability / Adoption Wiring

Status: **TASK-SCOPED L3 — JIT BUILDER INPUT**

Authority is bounded by Frozen Product, Frozen L2, Frozen Task DAG R2, Task Pack T-006, Issue #512, and the exact-base Execution Pack. This L3 is implementation guidance only and cannot expand the Builder write set or create semantic authority.

## 1. Implementation objective

Integrate already-merged v4.8 semantic owners into **discovery and adoption surfaces only**.

The implementation must answer four questions without creating a new authority layer:

1. Which three new v4.8 machine-contract families can a consumer discover?
2. Which existing reference explains each family?
3. How does a project adopt/read the material context without loading every optional surface?
4. How is backward compatibility verified while reusing existing Interchange v1?

The answer belongs in the current manifest, project-adoption guidance, one v4.8 integration reference, one migration/adoption note, and one focused verifier.

## 2. Read-only semantic inputs

The Builder should inspect but must not edit:

- `schemas/task-learning-v1.schema.json`
- `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`
- `schemas/agent-capability-profile-v1.schema.json`
- `references/AGENT_CAPABILITY_PROFILE_REFERENCE.md`
- `schemas/agent-capability-evidence-v1.schema.json`
- `references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md`
- `schemas/interchange-envelope-v1.schema.json`
- `references/V48_INTERCHANGE_PROFILE_COMPATIBILITY.md`
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md`
- Task Learning closeout surfaces merged by T-004
- ADS evolution governance surfaces merged by T-005
- Frozen Product/L2/DAG and the seven completed upstream Task Packs

The v4.7 predecessor references are historical lineage inputs only:
`version/v4.7.0:references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md` and
`version/v4.7.0:references/PROGRESSIVE_DISCLOSURE_ROUTING.md`.

Their absence from the current v4.8 tree is material: do not claim or reconstruct them as current v4.8 authority.

## 3. File-by-file implementation map

### `standard-manifest.json`

Preserve `schema_version: 1` and the complete historical `sections` inventory. Make additive changes only.

Required discovery additions:

```text
machine_contracts:
  schemas/task-learning-v1.schema.json
  schemas/agent-capability-profile-v1.schema.json
  schemas/agent-capability-evidence-v1.schema.json

references:
  references/TASK_LEARNING_EVIDENCE_REFERENCE.md
  references/AGENT_CAPABILITY_PROFILE_REFERENCE.md
  references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md
  references/V48_INTERCHANGE_PROFILE_COMPATIBILITY.md
  references/V48_REGISTRY_ADOPTION_REFERENCE.md

verification:
  scripts/test_v48_task_learning.py
  scripts/test_v48_agent_capability_profile.py
  scripts/test_v48_agent_capability_evidence.py
  scripts/test_v48_interchange_profile.py
  scripts/test_v48_registry_adoption.py
```

Do not remove or reorder historical inventory gratuitously. `schemas/interchange-envelope-v1.schema.json` must remain exactly once.

Do not add a new top-level authority model just to imitate v4.7. The current branch's manifest inventory is sufficient for T-006's bounded discoverability requirement unless an authoritative amendment says otherwise.

### `standards/PROJECT_ADOPTION.md`

Add a small v4.8 adoption/discovery subsection that:

- points to `standard-manifest.json` as the discoverability inventory, not a permission engine;
- names the three new v4.8 families;
- points to `references/V48_REGISTRY_ADOPTION_REFERENCE.md`;
- states materiality-driven / explicit adoption and the lightweight Fast Path;
- preserves project pinning/currentness precedence and existing override semantics;
- does not duplicate schema field definitions or sibling owner rules.

### `references/V48_REGISTRY_ADOPTION_REFERENCE.md`

Create a **non-authoritative integration reference**. It should contain explicit result semantics:

```text
authority_effect=NONE
gate_effect=NONE
mutation_authorized=false
```

It should map each new family to its schema/reference owner, map Interchange to the existing v1 family, explain progressive-disclosure read behavior, and record the v4.7 lineage boundary.

It must not become a second owner for Task Learning, capabilities, scheduling/resources, Interchange, Validation, Review, or Release.

### `docs/implementation/4.8.0/MIGRATION_ADOPTION.md`

Create a task-scoped migration note with:

- additive adoption steps;
- compatibility posture for old v4 payloads and existing durable evidence;
- Fast Path example in descriptive form;
- explicit “no destructive rewrite / no new Interchange family” rule;
- how to handle an old project that does not use one or more new optional families;
- a stop/escalation section for owner gaps.

This document is guidance/evidence, not normative authority.

### `scripts/test_v48_registry_adoption.py`

Create a deterministic repository-local focused verifier. It must not need network/provider/real-host access.

Recommended structure:

1. load `standard-manifest.json`;
2. assert the three expected v4.8 schema paths occur exactly once in `sections.machine_contracts`;
3. assert `schemas/interchange-envelope-v1.schema.json` occurs exactly once;
4. assert required owner/reference paths are present exactly once;
5. assert required focused verification paths are present exactly once;
6. assert all discovered paths exist in the checkout;
7. inspect the T-006 reference/adoption/migration text for explicit metadata-only/no-authority/Fast-Path boundaries;
8. compare the candidate manifest inventory against the frozen pre-T006 baseline contract encoded as the expected v4.8 additions, rejecting a fourth T-006 machine family or removals of legacy entries;
9. exit nonzero with a precise failure message for each invariant.

Do not import or recreate a v4.7 resolver as part of this verifier.

## 4. Positive test matrix

- **RA-01 — Three-family discoverability:** exactly the three named v4.8 schemas are present once.
- **RA-02 — Interchange reuse:** Interchange v1 is present once; no T-006-created Interchange family/version exists.
- **RA-03 — Owner-reference routing:** each family points by discovery to its already-merged reference owner; discovery does not restate semantics.
- **RA-04 — Project adoption:** PROJECT_ADOPTION exposes v4.8 discovery without making every family mandatory.
- **RA-05 — Fast Path:** lightweight execution remains possible without loading every optional family/reference and with `TASK_LEARNING=NONE_MATERIAL`.
- **RA-06 — Historical compatibility:** legacy manifest inventory is retained and historical consumers need no destructive migration.
- **RA-07 — Metadata-only result:** integration reference explicitly has no authority/gate/mutation effect.
- **RA-08 — Lineage honesty:** v4.7 branch-only registry/routing artifacts are not claimed as current v4.8 files.
- **RA-09 — Path integrity:** every newly registered path exists on the exact candidate checkout.
- **RA-10 — Regression compatibility:** all required sibling focused tests plus repository verifier pass.

## 5. Adversarial / negative matrix

- **RA-N01 — Fourth machine family:** any extra T-006 machine-contract family fails.
- **RA-N02 — Duplicate Interchange:** duplicate v1 or new v2-like ownership fails.
- **RA-N03 — Registry grants authority:** any wording/data that authorizes mutation/merge/PASS/release fails.
- **RA-N04 — Provider/model authority:** provider availability or identity cannot imply eligibility/correctness/permission.
- **RA-N05 — Capability proof inflation:** capability profile/evidence cannot become current Validation/Review truth.
- **RA-N06 — Mandatory optional adoption:** optional/materiality-driven context cannot be globally forced by registry presence.
- **RA-N07 — Historical deletion:** removal of legacy manifest inventory or destructive migration fails.
- **RA-N08 — v4.7 false-currentness:** copying/claiming branch-only v4.7 owner machinery without authority fails.
- **RA-N09 — Sibling repair:** implementation that changes sibling schema/reference/semantic owner fails write-set validation.
- **RA-N10 — Currentness drift:** base/dependency/pack drift before authoritative mutation requires rebind.

## 6. Builder sequence

1. Re-read `version/v4.8.0`; require exact base `257e95531551960cb163a3e20ab2b3d13f415d3c` before starting authoritative implementation. If target moved because this planning commit was merged elsewhere or another Task advanced the target, rebind rather than treating this pack as current.
2. Re-read #512 native dependency summary; require `blocked_by=0,total_blocked_by=7`.
3. Verify Task Pack/L3 blobs match `.agent/execution/T-006/MANIFEST.yaml`.
4. Confirm the five-path Builder write set and all read-only owner inputs.
5. Implement the smallest additive manifest/adoption/reference/migration changes.
6. Build `scripts/test_v48_registry_adoption.py` and run all commands in the Task Pack.
7. Inspect `git diff --name-only` and fail if any path falls outside the five-path write set.
8. Publish Builder terminal with exact base, candidate SHA/tree, exact diff, tests and limitations.
9. Hand the exact candidate to an independent Validator.
10. Only after qualifying Validation PASS may a genuinely Fresh Independent Review begin.

## 7. Evidence classification

Expected Builder evidence is repository-real execution against the exact candidate plus deterministic static/conformance assertions. No external host/device/provider/runtime claim is needed for T-006.

If a future claim depends on external environment behavior, record it as `NOT_RUN/BLOCKED` and request appropriate exact-subject Validation; do not promote synthetic/static evidence.

## 8. Stop conditions

Stop rather than widen scope if implementation needs:

- Frozen Product/L2/DAG edits;
- schema or semantic owner changes;
- a fourth machine family;
- a new Interchange family;
- v4.7 branch-only registry resolver/schema copied into v4.8;
- `.github/workflows/**` or Release/Closure changes;
- T-013/T-014 work;
- any path outside the five-path write set.

That condition is a Controller/owner handoff, not engineering discretion.
