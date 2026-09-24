# T-011 Task Pack — Migration, Adoption Levels and PROJECT_OVERRIDES

Task: T-011 / Issue #83
Parent version: #72
Dependency: T-010 / #82 completed at `version/v4.0.0@f85793d3c05b848ba91ce1c771cbffdb15efbd49`
JIT baseline: `version/v4.0.0@f85793d3c05b848ba91ce1c771cbffdb15efbd49`
Branch: `task/v4.0.0-t011-migration-adoption-overrides`
Review Policy: required
Risk: medium
Validation scope: concern
Agent freedom: F1_BOUNDED_IMPLEMENTATION

## Goal

Define a v3.4→v4 migration path that lets projects adopt v4 progressively without creating a second standard, weakening mandatory truth semantics, or forcing every repository to deploy reducer/controller/runtime automation.

## Frozen inputs

- #72 / #83;
- T-010 completion #82 and merge baseline `f85793d3c05b848ba91ce1c771cbffdb15efbd49`;
- released v3.4 adoption, Validation, Review, Task/Execution Pack and GitHub execution semantics;
- v4 Operation, Assurance, Interchange, routing, Fast Path, Validation/Candidate/Release contracts;
- R4 carry-forward #158 remains separate hardening backlog and MUST NOT be silently closed by migration guidance.

## Allowed write set

- `standards/PROJECT_ADOPTION.md`
- `templates/project/.dev-standard/PROJECT_OVERRIDES.md`
- `checklists/project-init.md`
- `docs/implementation/4.0.0/MIGRATION_ADOPTION_GUIDE.md`
- `templates/golden/V4_ADOPTION_MIGRATION_EXAMPLES.json`
- `scripts/test_v40_adoption_migration.py`
- `standard-manifest.json`
- `.github/workflows/verify-standard.yml`
- `docs/implementation/4.0.0/TASK_PACKS.json` (T-011 pointer only)
- this Task Pack.

No v4 runtime/schema/semantic-facade changes belong to T-011.

## Required decisions

### Adoption levels

Define exactly five monotonic implementation levels:

- `A0_COMPATIBILITY` — v4 pin with v3.4-compatible/manual execution; no requirement to materialize v4 Operation/Assurance machine records.
- `A1_MANUAL_PROTOCOL` — canonical v4 Operation/Assurance concepts recorded durably by humans/agents; routing remains manual.
- `A2_MACHINE_CONTRACTS` — A1 plus v4 schema/semantic verification for adopted records.
- `A3_DERIVED_AUTOMATION` — A2 plus reducer/queue/routing/controller-derived state; derived state remains non-authoritative.
- `A4_FULL_ORCHESTRATION` — A3 plus the project-selected full Operation/Assurance/Interchange/controller automation surface.

Levels describe implementation surface only. They MUST NOT weaken mandatory authority, exact identity, actual Validation execution, required Review, blocker dominance, Candidate Freeze, Release Qualification, Repository Integration separation, or `PR PASS != Release PASS`.

### Migration compatibility

The v3.4→v4 matrix MUST state which existing concepts remain compatible, which gain v4 representation, and which require explicit migration. Existing durable historical evidence retains its original identity/status; migration never rewrites historical `PASS`/`FAIL`/`CHANGES_REQUESTED`.

### Override boundaries

`PROJECT_OVERRIDES.md` MAY select adoption level, stronger assurance defaults, model-diversity defaults, exchange transport, automation enablement and stricter Fast Path policy. It MUST NOT:

- downgrade a higher-authority required gate/review/Validation tuple;
- turn model agreement into Validation truth;
- remove standard Fast Path disqualifiers;
- make Interchange authoritative;
- collapse Candidate/Release/Repository Integration state;
- replace exact-SHA evidence with branch/latest/current-chat claims;
- reinterpret `NOT_RUN/BLOCKED` as `NOT_APPLICABLE` to obtain green state.

## Reference project profiles

The guidance MUST include at least:

1. a small project that pins v4 at A0/A1, uses manual GitHub facts and minimal CI, and does not run reducer/controllers;
2. a substantial project at A2/A3 or A4 using machine contracts and derived automation while preserving GitHub/owning-controller authority.

## Fast Path

Fast Path is available independently of adoption level. Projects MAY disable it or strengthen eligibility, but MUST NOT remove canonical disqualifiers or use a low adoption level as proof of Fast Path eligibility.

## Validation

Focused regression:

```text
python scripts/test_v40_adoption_migration.py
```

The test MUST verify:

- exactly A0–A4 with monotonic capabilities;
- common non-weakening invariants at every level;
- migration compatibility entries for v3.4 core facts;
- forbidden override examples remain forbidden;
- small/substantial reference profiles exist;
- normative standard, project template and checklist expose the same adoption vocabulary;
- T-011 does not claim migration executes T-012/T-013 release/closure authority.

Then run the full repository `verify-standard` workflow on the exact PR HEAD.

## Completion

Migration/adoption guide + PROJECT_ADOPTION + PROJECT_OVERRIDES + project-init guidance + Golden/Forbidden examples + focused regression → exact-head full verifier PASS → required Fresh Independent Review PASS → merge to `version/v4.0.0` → close #83 and unlock T-012.
