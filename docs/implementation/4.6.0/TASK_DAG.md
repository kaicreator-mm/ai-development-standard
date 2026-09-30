# v4.6.0 Task DAG — AI-native / Agentic Development Governance

Status: **FROZEN TASK DAG — 2026-09-30**

Freeze inputs:

- Frozen Product: `e6aa04981110376e623d19b7dd4d0c6d0e139bdf`
- Frozen L2: `f47ea81e8f8df32ac6c8b7cc922c405a17b704d9`
- owner-currentness review: #280 PASS
- integration target: `version/v4.6.0` after canonical planning integration

## 1. DAG

```text
T01 Shared AI-native Machine Contracts ─────┬───────────────┐
                                             ▼               ▼
                                  T02 Intent &         T04 Skill / Procedure
                                  Assumption           Governance
                                  Governance

T03 Context Engineering ─────────────────────────────────────┐
                                                            │
T05 Existing-owner Assurance / Dispatch / Handoff Integration│
                                                            │
T02 ─────────────────────────────────────────────────────────┤
T04 ─────────────────────────────────────────────────────────┤
                                                            ├→ T06 Session / Operator Handoff Dogfood
                                                            │
                                                            └→ T07 Adoption & Cross-standard Wiring
                                                                    │
T06 ────────────────────────────────────────────────────────────────┤
T07 ────────────────────────────────────────────────────────────────┘
                                                                    ▼
                                                     T08 Cross-standard Conformance /
                                                         Closure Inputs
                                                                    │
                                                                    ▼
                                                             Version Closure
```

Exact dependency summary:

```text
T01: []
T02: [T01]
T03: []
T04: [T01]
T05: []
T06: [T02, T03, T04, T05]
T07: [T02, T03, T04, T05]
T08: [T06, T07]
```

T01, T03 and T05 are initial parallel roots. T02/T04 become parallel after T01. T06/T07 are sibling integration concerns with disjoint write-sets. T08 is the only pre-Closure join.

## 2. Task definitions

### T01 — Shared AI-native Machine Contracts

Own only the minimum machine layer selected by Frozen L2:

- `schemas/intent-assumption-record-v1.schema.json`
- `schemas/skill-metadata-v1.schema.json`
- narrowly justified optional reference fields in existing `dispatch.schema.json` / `execution-pack-manifest.schema.json`
- focused schema/historical-compatibility tests

No normative Intent/Context/Skill policy, no new lifecycle state, no Context Snapshot schema, no new Assurance result family.

### T02 — Intent & Assumption Governance

Depends on T01. Own:

- `standards/INTENT_ASSUMPTION_GOVERNANCE_STANDARD.md`
- `references/INTENT_ASSUMPTION_REFERENCE.md`
- focused semantic tests

Preserve intent/interpretation/assumption/unknown distinctions. Promotion into durable requirements remains owned by existing Product/Architecture/Task authority.

### T03 — Context Engineering

Independent initial root because Frozen L2 creates no Context machine family. Own:

- `standards/CONTEXT_ENGINEERING_STANDARD.md`
- `references/CONTEXT_ENGINEERING_REFERENCE.md`
- focused precedence/currentness/progressive-disclosure tests

No repository-wide context database/snapshot, no lifecycle state and no v4.7 unified resolver.

### T04 — Skill / Reusable Agent Procedure Governance

Depends on T01. Own:

- `standards/SKILL_PROCEDURE_GOVERNANCE_STANDARD.md`
- `references/SKILL_PROCEDURE_REFERENCE.md`
- focused Skill metadata/authority/security tests

Skill installation/capability MUST NOT become side-effect or Task authority.

### T05 — Existing-owner Assurance / Dispatch / Handoff Integration

Initial root. Own only non-normative integration/reference material plus conformance tests proving that AI-native coverage/provenance/handoff reuses existing owners:

- `references/AI_NATIVE_EXISTING_OWNER_INTEGRATION.md`
- `scripts/test_v46_existing_owner_integration.py`

No new normative standard, Assurance plan/result, autonomy scale, Dispatch state or Validation/Release vocabulary.

### T06 — Session / Operator Handoff Dogfood

Depends on T02/T03/T04/T05. Own a reproducible dogfood packet proving a fresh logical Agent/session can reconstruct authority and next action from durable facts without the lost chat transcript.

Allowed dogfood surfaces:

- `docs/implementation/4.6.0/dogfood/**`
- `scripts/test_v46_session_handoff_dogfood.py`

The dogfood MUST distinguish same transport account from logical operator/context independence. If a real external Agent/runtime capability is required and unavailable, create an exact-subject Validation handoff; fixture/static proof must remain labeled as such.

### T07 — Adoption & Cross-standard Wiring

Depends on T02/T03/T04/T05. Central wiring only:

- `standard-manifest.json`
- `templates/golden/STANDARD_COVERAGE.json`
- `templates/project/.dev-standard/PROJECT_OVERRIDES.md`
- selected checklists/adoption references
- `docs/implementation/4.6.0/MIGRATION_ADOPTION.md`
- focused wiring regression

Must reference rather than duplicate existing Assurance/Dispatch/Handoff/Validation/Release owners. No v4.7 repository-wide resolver.

### T08 — Cross-standard Conformance / Closure Inputs

Depends on T06/T07. Own integrated forbidden-inference tests, historical compatibility, Fast Path proportionality, v4.1–v4.5 owner composition and durable Version Closure inputs.

No Version Closure/Release Qualification verdict itself.

## 3. Native Issue dependency graph

After planning integration and Issue materialization, GitHub Issue Dependencies become the canonical live execution DAG. This file remains frozen planning/history authority.

Expected native edges are exactly the dependency summary in §1. Roots are T01/T03/T05.

Task branches are JIT from current `version/v4.6.0` only after native blockers are satisfied. Body-text dependency descriptions never substitute for native edges.

## 4. Integration / branch posture

The planning PR integrates Frozen Product/L2/DAG/L3/Task Packs first. `version/v4.6.0` is created only after Fresh Independent Planning Review PASS and canonical merge.

Implementation PRs target `version/v4.6.0`; one concern per PR. Stacked PR is allowed only for a real unmerged code-baseline dependency and never substitutes for the Task DAG.

## 5. Risk / executor suitability

| Task | Risk | Default executor suitability | Review posture |
|---|---|---|---|
| T01 | high | bounded builder after Frozen L2; Strong model for contract conflict | Fresh Independent Review + concern Validation |
| T02 | high | Strong/Web for intent/promotion authority; bounded implementation inside Task Pack | Fresh Independent Review + concern Validation |
| T03 | high | Strong/Web because precedence/currentness mistakes can steal authority | Fresh Independent Review + concern Validation |
| T04 | high | Strong/Web for trust/authority semantics; bounded schema/reference work | Fresh Independent Review + concern Validation |
| T05 | high | Strong/Web integration owner; must not create parallel Assurance/Handoff semantics | Fresh Independent Review + concern Validation |
| T06 | high | independent dogfood executor/validator; external Agent capability only when explicitly required | Fresh Independent Review + exact-subject Validation |
| T07 | high | central integration builder + fresh reviewer | Fresh Independent Review + integration Validation |
| T08 | high | independent integration validator/reviewer | Fresh Independent Review + integration Validation |

## 6. Required L3 / Task Pack contract

Every Task Pack MUST state:

- task identity and dependencies;
- integration/merge target;
- allowed write-set and forbidden scope;
- acceptance criteria and adversarial negatives;
- required gates and validation owner;
- review policy;
- L3/reference pointer;
- agent freedom;
- failure/currentness handling.

No execution agent may self-broaden these fields.

## 7. Local environment posture

Planning and T01–T05/T07 are repository/Web/CI executable by default.

T06 may require a real fresh-Agent/session/tool runtime only if the chosen dogfood claim depends on that capability. In that case unavailable execution becomes an exact-scope Validation Request and `BLOCKED/NOT_RUN`, never simulated PASS.

T08 can remain repository/CI-based unless it consumes a real-runtime claim from T06.

`LOCAL_ENV=NOT_REQUIRED` at Task DAG Freeze.
