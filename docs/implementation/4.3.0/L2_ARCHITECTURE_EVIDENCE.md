# v4.3.0 L2 Architecture Evidence — Engineering Design & Implementation Profiles

Status: **FROZEN L2 ARCHITECTURE AUTHORITY — 2026-09-30**

Freeze basis:

- Frozen Product Authority: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
- L1: `docs/implementation/4.3.0/L1_PRODUCT_EVIDENCE.md`
- v4.2 Product boundary: `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9`
- explicit L2 Freeze: the commit introducing this frozen L2 file

## 1. Architecture recommendation

Use **four normative standards + one minimal DAG-mutation machine contract + a lightweight profile information architecture**.

```text
Frozen Product / Architecture
          │
          ├──────────────┬───────────────┬────────────────┐
          ▼              ▼               ▼                ▼
Architecture Design  Task Decomposition  Task DAG Gov.  Implementation Quality
          │              │               │                │
          │              │               ▼                ▼
          │              │      DAG Mutation Record   Language-neutral core
          │              │                                │
          └──────────────┴───────────────┬────────────────┘
                                         ▼
                              Profile mapping layer
                    Language profiles + small archetype set
                                         │
                                         ▼
                                  PROJECT_OVERRIDES
                                         │
                                         ▼
                                Task / Execution Pack
```

Architecture decisions:

1. **Four normative owners; profiles are not normative peers.** Profiles map/specialize implementation facts but cannot compete with core standards.
2. **No Architecture Decision schema by default.** A standard + reference/template is sufficient unless implementation proves cross-Agent machine exchange needs one.
3. **One new default machine contract: DAG Mutation Record.** Live topology mutation benefits from immutable old/new topology + authority/impact binding.
4. **Do not create a duplicate Task object/schema.** Task decomposition requirements extend Task Pack/Issue/Execution Pack content and validation.
5. **Do not create a full repository resolver in v4.3.** Profile resolution is deterministic through directory/index/manifest references + PROJECT_OVERRIDES; v4.7 owns repository-wide convergence/resolver.
6. **Language profiles are evidence-driven mappings.** Initial required set: TypeScript, Python, Go, Java, Rust.
7. **Archetype profiles start small.** L2 selects `library`, `service`, and `CLI` as representative initial mappings; other archetypes may be added later from evidence.
8. **Fast Path remains materiality-driven.** Small changes do not require an ADR/DAG mutation/profile manifest when those concerns are unchanged/non-material.

## 2. Architecture drivers

### D1 — Durable design rationale without architecture-style lock-in

ADR practice demonstrates value in recording significant decisions, rationale, alternatives and consequences. ADS should require equivalent semantics without mandating Markdown ADR format.

References:

- https://adr.github.io/
- https://adr.github.io/madr/

### D2 — Concern-sized work improves review/execution quality

Public engineering practice favors self-contained small changes and review scopes that a reviewer can understand completely. ADS must translate that into Task authority/write-set/gate semantics rather than arbitrary line/file-count limits.

Reference: https://google.github.io/eng-practices/review/

### D3 — Native GitHub dependencies remain the live topology mechanism

GitHub already supports explicit blocked-by/blocking Issue relationships. ADS should govern their semantic mutation, not build a second graph engine.

Reference: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies

### D4 — Agent instructions/profiles benefit from scoped composition

GitHub Copilot and AGENTS.md patterns demonstrate repository-wide and more-local instruction/profile composition. v4.3 can use analogous scoped mapping while preserving ADS authority precedence.

References:

- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions
- https://agents.md/

### D5 — Avoid v4.7 resolver preemption

v4.7 explicitly owns unified manifest/resolver/progressive disclosure and repository convergence. v4.3 must expose deterministic profile structure without claiming repository-wide authority resolution ownership.

## 3. Normative owner map

| Semantic concern | v4.3 owner | Must not duplicate |
|---|---|---|
| required material architecture decision quality | `ARCHITECTURE_DESIGN_STANDARD.md` | L2 research workflow, v4.2 compatibility outcomes |
| Task concern boundary / Task authority completeness | `TASK_DECOMPOSITION_STANDARD.md` | Issue state, Execution Pack state |
| live DAG material mutation | `TASK_DAG_GOVERNANCE_STANDARD.md` | GitHub dependency mechanism |
| language-neutral implementation baseline | `IMPLEMENTATION_QUALITY_STANDARD.md` | Testing/CI/Dependency/Secrets owners |
| language mapping/defaults | `profiles/languages/*.md` | official style guides / repository authority |
| archetype mapping/defaults | `profiles/archetypes/*.md` | Product architecture |
| effective project selection | `PROJECT_OVERRIDES` + profile framework | Frozen/Core authority weakening |
| repository-wide resolver/convergence | future v4.7 | no v4.3 ownership |

## 4. Machine contract architecture

### 4.1 New: `schemas/dag-mutation-record-v1.schema.json`

Purpose: attributable record of material live execution-DAG change.

Proposed shape:

```yaml
schema_version: 1
mutation_id:
mutation_class:
requested_by:
approved_by:
reason:
affected_task_refs: []
old_topology_ref:
new_topology_ref:
old_edges: []
new_edges: []
scope_impact:
release_impact:
task_pack_impact_refs: []
review_impact:
validation_impact_ref:
created_at:
```

Required properties:

- mutation record never creates Product/Architecture authority;
- removal of dependency requires explicit reason/authority and cannot fabricate readiness;
- old/new topology is reconstructible enough for audit;
- Task Pack/Review/Validation impact must be dispositioned when material;
- mutation class is extensible for future compatible additions.

### 4.2 No new Architecture Decision schema by default

Use a normative standard plus `references/ARCHITECTURE_DECISION_REFERENCE.md` with recommended durable fields. Repositories may use ADRs/design docs or equivalent.

If implementation proves automation needs machine exchange, a later additive schema may be proposed with separate evidence.

### 4.3 No new duplicate Task schema

Task decomposition requirements should be reflected in:

- Task Pack templates/guidance;
- execution Issue materialization requirements;
- conformance tests checking durable Task facts;
- Execution Pack references where execution-specific.

Do not create `task-v2` just to restate existing Task authority.

### 4.4 Profile information architecture

```text
profiles/
  README.md                     # non-normative resolver/reference contract
  languages/
    typescript.md
    python.md
    go.md
    java.md
    rust.md
  archetypes/
    library.md
    service.md
    cli.md
```

Profile documents contain structured sections/metadata sufficient to resolve:

```text
profile id/version
applicability
manifest/lock/toolchain mapping
recommended/required project-owned checks
source/test/generated conventions
high-risk semantics
references
```

They are mappings, not independent lifecycle standards.

### 4.5 Effective profile resolution

```text
Frozen Product/Architecture constraints
> mandatory Core ADS standard semantics
> applicable project-selected profile mappings
> PROJECT_OVERRIDES specialization/strengthening
> Task/Execution-specific instructions
```

`PROJECT_OVERRIDES` can select/specialize/strengthen profile defaults. It cannot silently weaken higher authority unless an existing owner permits an explicit waiver/exception.

## 5. Standard architecture

### 5.1 Architecture Design Standard

Must define materiality, required design dimensions, durable decision semantics, UNKNOWN handling, evidence references and escape-hatch expectations.

Must explicitly preserve:

- L2 as research/evidence workflow;
- v4.2 as compatibility/migration owner;
- project freedom over architecture paradigm.

### 5.2 Task Decomposition Standard

Must define:

- minimum coherent concern;
- bounded write-set/ownership;
- acceptance/gates/validation/review/integration facts;
- safe parallelism criteria;
- atomic-invariant non-splitting;
- real code-baseline dependency/stacking allowance;
- sibling/central wiring boundary.

### 5.3 Task DAG Governance Standard

Must define planning DAG vs live Issue dependency distinction and material mutation procedure.

No mutation record is needed for non-material metadata edits that do not alter execution topology/scope/owner.

### 5.4 Implementation Quality Standard

Must remain language neutral and compose with:

- v4.1 Dependency/Toolchain;
- Config/Secrets;
- Git execution;
- Testing/CI/Validation;
- Documentation.

It owns implementation-quality expectations only, not the result states of those systems.

## 6. Language profile selection rationale

The five Frozen Product languages cover distinct ecosystems and risk families:

- TypeScript: Node/package managers, ESM/CJS/typecheck/build split;
- Python: packaging/import/runtime/tooling variability;
- Go: module/toolchain/race/context conventions;
- Java: JDK + Maven/Gradle/toolchain/runtime split;
- Rust: Cargo/MSRV/features/unsafe/build targets.

L2 does not freeze exact tool brands (e.g. one Python formatter) as mandatory. Each profile should map common alternatives and defer final authority to the repository/project.

## 7. Initial archetype selection

Use only:

- `library` — emphasizes public API/compatibility, packaging and broad consumer concerns;
- `service` — emphasizes runtime/external/deployment/observability boundaries;
- `cli` — emphasizes executable packaging, command interface and environment interaction.

Web frontend/worker/SDK/desktop/plugin/monorepo remain valid future mappings but are not required to prove the initial framework.

## 8. Architecture UNKNOWNs and disposition

| ID | UNKNOWN | Impact | Disposition | Decision |
|---|---|---|---|---|
| U1 | Need Architecture Decision machine schema? | Medium | `STATIC_EVIDENCE_SUFFICIENT` | No default schema; standard/reference sufficient. |
| U2 | Need duplicate Task schema? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No; extend existing Task Pack/Issue/Execution Pack semantics. |
| U3 | Need machine record for live DAG mutation? | High | `STATIC_EVIDENCE_SUFFICIENT` | Yes, one `dag-mutation-record-v1`. |
| U4 | Need a full profile resolver service/schema now? | High | `STATIC_EVIDENCE_SUFFICIENT` | No; deterministic doc/index/project override resolution. v4.7 owns convergence resolver. |
| U5 | How many archetypes initially? | Medium | `STATIC_EVIDENCE_SUFFICIENT` | Three representative mappings: library/service/CLI. |
| U6 | Can PROJECT_OVERRIDES weaken profile defaults? | High | `STATIC_EVIDENCE_SUFFICIENT` | Can specialize/strengthen; cannot weaken mandatory higher authority without explicit owner mechanism. |
| U7 | Does v4.3 duplicate v4.2 compatibility/migration? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No; architecture requires consideration, v4.2 owns semantic outcomes/transitions. |
| U8 | Need executable multi-language Research Demo before L2 Freeze? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Profile mappings rely on official ecosystem facts; executable conformance belongs implementation tasks. |

**Research Demo decision: NOT REQUIRED before L2 Freeze.**

## 9. Conformance architecture

Required negative families:

```text
architecture popularity -> justified decision                  MUST fail
high-impact UNKNOWN -> ordinary implementation freedom         MUST fail
file split -> coherent Task boundary                           MUST fail
atomic invariant split -> safe parallelism                     MUST fail
remove dependency -> READY                                     MUST fail
PR stack -> canonical Task DAG                                 MUST fail
DAG edit without mutation authority/impact                     MUST fail
Agent-local tool version -> repository profile authority       MUST fail
profile mapping -> universal tool/style requirement            MUST fail
PROJECT_OVERRIDES -> weaken Frozen/Core semantics              MUST fail
```

Positive dogfood should demonstrate one high-capability planning pass producing parallel Task Issues/Task Packs that a lower-cost executor can implement without architecture redesign.

## 10. L2 verdict

**Architecture is sufficiently resolved to materialize the v4.3 Task DAG.**

No local environment is required for Task planning. Later language-profile conformance may use normal CI/local tooling, but any unavailable required ecosystem proof must use an explicit exact-subject Validation handoff rather than assumption.