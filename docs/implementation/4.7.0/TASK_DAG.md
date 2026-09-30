# v4.7.0 Task DAG — AI-native Development Convergence

Status: **FROZEN TASK DAG — 2026-09-30**

Freeze inputs:

- Frozen Product: `d4f90e1432b53fe0d30d4673674280f3c5e586ec`
- Frozen L2: `8a0687807e1c5ec7c415b0031862b0e367c44507`
- Product/currentness Review: #318 PASS / Freeze authorized
- integration target: `version/v4.7.0` after canonical planning integration

## 1. DAG

```text
T01 Convergence Metadata Contracts ───────┬───────────────┐
                                          ▼               ▼
                               T02 Authority /       T03 State-Dimension /
                               Applicability         Forbidden-Inference
                               Manifest Registry     Registry
                                          │               │
                                          │               │
T04 Reference Convention Standard ────────┼───────┐       │
                                          ▼       │       │
                               T05 Progressive     │       │
                               Disclosure Routing  │       │
                                          │       │       │
                               T06 Compatibility / │       │
                               Alias Conformance ◄─┘       │
                                          │               │
T02 ──────────────────────────────────────┼───────────────┤
T03 ──────────────────────────────────────┤               │
T04 ──────────────────────────────────────┤               │
T05 ──────────────────────────────────────┤               │
T06 ──────────────────────────────────────┘               │
                                                          ▼
                                         T07 Unified Semantic Conformance
                                          │
                                          ▼
                                  T08 Fresh-Agent Self-Dogfood

T02 ─────────────────────────────────────────────┐
T03 ─────────────────────────────────────────────┤
T04 ─────────────────────────────────────────────┤
T05 ─────────────────────────────────────────────┤→ T09 Adoption / Migration Wiring
T06 ─────────────────────────────────────────────┘

T07 ─────────────────────────────────────────────┐
T08 ─────────────────────────────────────────────┼→ T10 Cross-standard Closure Inputs
T09 ─────────────────────────────────────────────┘
                                                    │
                                                    ▼
                                             Version Closure
```

Exact dependency summary:

```text
T01: []
T02: [T01]
T03: [T01]
T04: []
T05: [T02, T04]
T06: [T02, T04]
T07: [T02, T03, T04, T05, T06]
T08: [T05, T07]
T09: [T02, T03, T04, T05, T06]
T10: [T07, T08, T09]
```

Initial roots are T01 and T04. T02/T03 become sibling metadata concerns after T01. T05/T06 are sibling derived-routing/compatibility concerns. T07 and T09 are sibling integration concerns with disjoint write-sets. T10 is the only pre-Closure join.

## 2. Task definitions

### T01 — Convergence Metadata Contracts

Own only the two Frozen-L2 default metadata families:

- Authority / Applicability Entry v1 schema/contract;
- State-Dimension / Forbidden-Inference Registry v1 schema/contract;
- focused schema/backward-compatibility tests.

No manifest population, owner policy, global state or reference-convention policy.

### T02 — Authority / Applicability Manifest Registry

Extend canonical `standard-manifest.json` additively with semantic registry metadata and implement owner/applicability consistency tests.

Preserve existing `sections` consumers. Registry points to normative owners and never grants mutation authority.

### T03 — State-Dimension / Forbidden-Inference Registry

Own canonical registry data for qualified state dimensions and forbidden cross-dimension inference rules plus focused conformance tests.

Must not own live state values, transitions or generic PASS/READY/BLOCKED semantics.

### T04 — Reference Convention Standard

Own a normative reference-convention standard/reference/tests covering compatible subject identity, exact SHA/base, authority refs, evidence refs and provenance pointers.

No mandatory universal Subject/Authority object and no historical schema rewrite.

### T05 — Progressive Disclosure Routing

Own derived read-routing rules/tests composing AGENTS, pinned ADS, manifest registry, PROJECT_OVERRIDES, profiles and exact Task/Execution authority.

No Context Snapshot database or new authority store.

### T06 — Compatibility / Alias Conformance

Own compatibility-path/alias integrity rules and tests: canonical target resolution, no duplicate normative owner, cycle/broken-target detection and evidence-driven path migration posture.

No physical repository refactor is required or authorized by this task.

### T07 — Unified Semantic Conformance

Own executable cross-standard semantic conformance for owner uniqueness, mutation authority, state non-inference, exact identity/currentness, profile resolution, machine/prose consistency and compatibility history.

No new Convergence PASS state family.

### T08 — Fresh-Agent Self-Dogfood

Own reproducible dogfood proving a genuinely fresh logical Agent/session can reconstruct applicable authority, current task identity, allowed mutations/side effects, evidence requirements and next action using durable facts only.

If a real Agent/session/runtime claim cannot be executed in the current environment, create exact-subject Validation handoff; static fixture proof remains labeled static.

### T09 — Adoption / Migration Wiring

Own central adoption/migration wiring only:

- selected PROJECT_OVERRIDES / project-init / review / closure guidance;
- v4.7 migration/adoption notes;
- future-major register integration;
- selected manifest/reference/checklist wiring after owner-specific concerns are stable.

No owner semantics duplication and no physical path migration without separate evidence/authority.

### T10 — Cross-standard Closure Inputs

Own integrated v4.1–v4.7 forbidden-inference regression, historical compatibility, Fast Path proportionality, fresh-Agent reconstruction evidence summary and durable Version Closure inputs.

No Version Closure/Release Qualification verdict itself.

## 3. Native Issue dependency graph

After planning integration and Task Issue materialization, GitHub Issue Dependencies are the canonical live execution DAG. This file remains Frozen planning/history authority.

Expected native edges are exactly the dependency summary in §1. Roots T01/T04 have no blockers.

Task branches are JIT from current `version/v4.7.0` only after native blockers are satisfied. Body-text dependency lists do not substitute for native edges.

## 4. Integration / branch posture

Planning Product/L2/DAG/L3/Task Packs integrate first after required Fresh Independent Planning Review. `version/v4.7.0` is created from that canonical planning merge.

All implementation PRs target `version/v4.7.0`, one concern per PR. Stacked PRs are allowed only for a real unmerged code-baseline dependency and never replace the Task DAG.

## 5. Risk / executor suitability

| Task | Risk | Default executor | Review / Validation posture |
|---|---|---|---|
| T01 | high | bounded builder after Frozen L2 | concern Validation + Fresh Independent Review |
| T02 | high | strong/bounded integration builder | concern Validation + Fresh Independent Review |
| T03 | high | strong semantic builder | concern Validation + Fresh Independent Review |
| T04 | high | strong/Web for cross-owner reference semantics | concern Validation + Fresh Independent Review |
| T05 | high | strong integration builder | concern Validation + Fresh Independent Review |
| T06 | high | bounded compatibility builder + fresh reviewer | concern Validation + Fresh Independent Review |
| T07 | high | independent integration validator/reviewer | integration Validation + Fresh Independent Review |
| T08 | high | genuinely fresh logical Agent/session + independent validator | exact-subject Validation + Fresh Independent Review |
| T09 | high | central wiring builder | integration Validation + Fresh Independent Review |
| T10 | high | independent integration validator/reviewer | integration Validation + Fresh Independent Review |

## 6. Required Task Pack contract

Every Task Pack MUST state:

- task identity and dependencies;
- integration/merge target;
- allowed write-set and forbidden scope;
- acceptance criteria including adversarial negatives;
- required gates and validation owner;
- review policy;
- L3/reference pointer;
- agent freedom;
- failure/currentness handling.

No execution agent may self-broaden these fields. Technical necessity, registry presence, CI or Validation cannot create mutation authority.

## 7. Local environment posture

T01–T07/T09 are repository/Web/CI executable by default.

T08 may require a genuinely fresh logical Agent/session. If the chosen claim requires unavailable external runtime/tool/provider capability, use an exact-scope Validation Request and preserve `BLOCKED/NOT_RUN`; do not simulate real-runtime PASS.

T10 can remain repository/CI-based unless it consumes a real-runtime claim from T08.

`LOCAL_ENV=NOT_REQUIRED` at Task DAG Freeze.
