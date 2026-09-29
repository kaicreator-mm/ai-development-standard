# v4.3.0 L1 Product Evidence — Engineering Design & Implementation Profiles

Status: **COMPLETE — supports PRD revision; Product Freeze should wait only for the explicitly identified v4.2 boundary check**

Research date: 2026-09-30

Baseline / authority reviewed:

- `main@e9eb39235e45e9ad90407b803ab1c8679d348dbf`
- Draft `docs/implementation/4.3.0/PRD.md`
- current L2/Task DAG/Task Pack/Execution Pack/GitHub interaction standards
- v4.2 Evolution Governance Draft + L1 findings

This document is Product evidence, not itself Product Freeze.

## 1. Recommendation

**PROCEED WITH NARROWING.**

The product problem is real: architecture quality, Task decomposition, live DAG mutation and ecosystem implementation facts currently depend too much on prompts/templates/tacit planner quality. However v4.3 must standardize **decision quality and durable execution boundaries**, not prescribe one architecture style, one task taxonomy, or duplicate language style guides.

Required Product corrections before Freeze:

1. Architecture Design owns durable **decision/invariant quality**, while L2 remains the research workflow that discovers evidence.
2. Task Decomposition freezes `minimum coherent concern + maximum safe parallelism`; lane names remain advisory patterns, not mandatory taxonomy.
3. Task DAG Governance owns post-materialization topology mutation records; GitHub Issue Dependencies remain canonical live dependency relationships.
4. Implementation Quality should be a small language-neutral contract, with language/archetype profiles acting as mappings/defaults rather than independent competing normative standards.
5. Profile resolution must be deterministic and authority-aware; a local Agent runtime/tool cannot silently redefine repository compatibility or commands.

## 2. Architecture Design Evidence

Architectural Decision Records are an established mechanism for preserving a significant design choice together with its rationale, alternatives/trade-offs and consequences. ADR practice explicitly treats the decision log as durable architectural knowledge rather than only an implementation note.

Sources:

- https://adr.github.io/
- https://adr.github.io/madr/

**Finding:** the Draft PRD is justified in requiring material design decisions to expose drivers/invariants/boundaries/failure semantics and a bounded Decision/Alternatives/Rationale/Trade-offs/Evidence/Escape-hatch record.

The Product must not mandate ADR Markdown specifically. ADS owns the semantic content needed for reconstructible engineering decisions; repositories may use ADRs, design docs, schemas or equivalent durable forms.

## 3. Task Decomposition Evidence

Google's public engineering practices define a changelist as one self-contained change and explicitly recommend small changes because they are easier to review and maintain. Review guidance also emphasizes design, correctness, complexity, tests and understanding the entire requested review scope.

Sources:

- https://google.github.io/eng-practices/review/
- https://google.github.io/eng-practices/review/developer/
- https://google.github.io/eng-practices/review/reviewer/looking-for.html

This supports concern-oriented Tasks and reviewable write sets, but does **not** support arbitrary file-count limits or universal maximum Task size.

Product principle:

> A Task is the minimum coherent concern that can carry a truthful independent authority/evidence boundary while preserving maximum safe parallelism.

A Task should normally identify:

```text
primary concern
frozen/current inputs
bounded output/write-set
forbidden scope
acceptance
required gates
review policy
validation owner
integration target
real dependencies
```

Anti-patterns supported by current ADS dogfood include giant mixed-authority tasks, file-based fake splits, sibling write-set leakage and removing dependency edges merely to make work appear READY.

## 4. Live Task DAG Governance Evidence

GitHub Issue Dependencies provide native `blocked by` / `blocking` relationships. They are execution relationships, while a planning DAG can preserve decomposition rationale/history.

Source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies

**Finding:** current ADS separation is sound:

```text
Planning DAG = frozen decomposition/rationale/history
Issue Dependencies = canonical live execution dependency graph
```

v4.3 should govern **material mutation after materialization**, not introduce another DAG engine.

Mutation records should cover classes such as:

```text
ADD_TASK
SPLIT_TASK
MERGE_TASK
SUPERSEDE_TASK
ADD_DEPENDENCY
REMOVE_DEPENDENCY
CHANGE_LANE
CHANGE_INTEGRATION_OWNER
DEFER_TASK
```

Each material mutation must preserve reason, authority, old/new topology, affected Tasks and Product/Architecture/Review/Validation impact. Exact machine vocabulary belongs to L2.

## 5. Implementation Quality Evidence

Language-neutral engineering practices commonly require explicit build/test/check commands, deterministic tooling, code review, tests and manageable complexity, but exact tools vary by ecosystem.

The core Product contract should therefore own durable requirements such as:

- repository-authoritative build/test/check entrypoints;
- deterministic formatter/static/type checks where the project/ecosystem supports them;
- source/generated/test ownership and layout discoverability;
- dependency/toolchain composition with v4.1;
- public error/contract discipline where material;
- generated-code ownership;
- secret-safe logging and configuration use;
- no arbitrary universal complexity/coverage thresholds.

It should **not** reproduce TypeScript/Python/Go/Java/Rust style guides.

## 6. Language / Archetype Profile Evidence

Modern Agent tools already distinguish global repository instructions from more specific path/agent instructions. GitHub Copilot supports repository-wide, path-specific and `AGENTS.md` agent instructions, with more-local instruction scopes available for relevant work.

Sources:

- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions
- https://agents.md/

This supports a layered profile resolver rather than one global giant standard.

Recommended Product model:

```text
Core normative requirements
+ applicable Language Profile(s)
+ applicable Archetype Profile(s)
+ PROJECT_OVERRIDES
= effective implementation policy
```

Profiles should primarily map neutral requirements to ecosystem facts such as manifest/lock authority, compiler/runtime compatibility, formatter/linter/type checks, test/build conventions and high-risk language semantics.

They are defaults/mappings and may be strengthened or replaced by project authority. Local Agent availability never becomes profile authority.

## 7. Authority Boundary With v4.2

v4.3 Architecture Design should require architects to address compatibility/migration when material, but **v4.2 remains the normative owner of interface compatibility outcomes and persistent-state transition semantics**.

v4.3 may Freeze after confirming this boundary in the revised v4.2 Product Authority. It does not need to wait for all v4.2 implementation to complete.

## 8. Product-level Negative Conformance

v4.3 should reject at least:

- architecture selected only by popularity with no material drivers/trade-offs/failure semantics;
- unresolved high-impact architectural UNKNOWN silently converted to implementation detail;
- one Task containing multiple unrelated authority/write-set concerns merely for convenience;
- Tasks split by file count while sharing one atomic invariant/state transition;
- dependency edge removed only to fabricate readiness;
- live Issue DAG mutation without durable reason/authority/impact;
- stacked PR topology substituted for canonical Issue Dependencies;
- local Python/Node/JDK/Rust version treated as repository compatibility authority;
- language profile copied as a mandatory universal style guide;
- archetype/profile selection silently overriding Product/Architecture or PROJECT_OVERRIDES.

## 9. Machine-contract Findings

L2 should evaluate, without assuming every concept needs a schema:

1. **Architecture Decision / Invariant inventory** — durable material decisions and known UNKNOWNs.
2. **DAG Mutation Record** — old/new topology and impact for material live-DAG changes.
3. **Profile Applicability/Resolution record** — only if deterministic pointers cannot resolve effective policy reliably.

Task decomposition quality fields should preferably extend Task Pack/Execution Pack authority rather than create a parallel Task object.

## 10. Scope Risks / Counter-evidence

- Small/Fast-Path work should not require heavyweight architecture records.
- Mature repositories often already encode language conventions in manifests/config/tooling; ADS should reference them rather than duplicate them.
- Some real Tasks require stacked code dependencies and are not independently mergeable; “maximum parallelism” cannot erase actual ancestry.
- Profiles can explode combinatorially. Initial archetype set must be evidence-driven and small.

## 11. L1 Verdict

**Evidence is sufficient for PRD revision.**

Product Freeze should proceed once the v4.2 revised Product Authority confirms the compatibility/migration ownership boundary. No local environment proof is required for this gate.

`LOCAL_ENV=NOT_REQUIRED` at L1. Executable cross-language/profile probes belong to L2/conformance Tasks if architecture evidence later shows they are necessary.