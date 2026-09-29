# ai-development-standard v4.3.0 PRD — Engineering Design & Implementation Profiles

Status: **FREEZE CANDIDATE — revised from L1 Product Evidence**

## 1. Product intent

v4.3.0 standardizes durable engineering-design quality, Task decomposition, live Task DAG evolution and implementation-profile resolution so high-capability planning can be safely consumed by lower-cost execution Agents without hidden redesign.

The version defines **what must be explicit and reconstructible**, not one architecture style, one Task taxonomy, one directory layout or one language style guide.

## 2. Product owners

v4.3 introduces four normative owners:

1. **Architecture Design Standard** — material decision/invariant quality after research.
2. **Task Decomposition Standard** — minimum coherent concern + maximum safe parallelism.
3. **Task DAG Governance Standard** — material live-DAG mutation after materialization.
4. **Implementation Quality Standard** — small language-neutral execution/quality baseline.

Language and archetype profiles are **mapping/default layers**, not competing normative owners.

The existing L2 prompt remains the architecture research workflow. Architecture Design Standard owns the durable quality requirements for architecture decisions/output; it does not replace L2 research.

## 3. Architecture Design Standard

Material architectures must make explicit, where applicable:

```text
Architecture Drivers
Invariants
System/component boundaries
Ownership/data ownership
Public/cross-component contracts
Sync/async boundaries
Failure semantics
Idempotency/ordering/concurrency
Durability
Security/trust boundaries
Observability requirements
Deployment topology assumptions
Compatibility/migration requirements
Known UNKNOWNs
Evidence basis
Escape hatch / rollback / recovery
```

Material decisions require a bounded durable record of:

```text
Decision
Alternatives
Rationale
Trade-offs
Failure modes
Evidence
Escape hatch / rollback
```

The standard must not mandate microservices, DDD, Clean Architecture, event-driven systems, monoliths or another universal paradigm.

v4.2 remains the normative owner of compatibility outcomes and persistent-state transition semantics; v4.3 only requires architecture to address them when material.

## 4. Task Decomposition Standard

Core principle:

> **minimum coherent concern + maximum safe parallelism**

A Task should normally carry:

```text
one primary concern
explicit frozen/current inputs
clear output
bounded write-set / ownership
forbidden scope
acceptance criteria
required gates
review policy
validation ownership
integration target
real dependencies
```

Common lane patterns such as contract/core/adapter/integration/UI/platform/migration/validation are advisory decomposition patterns, not required taxonomy.

Explicit anti-patterns:

- split only by file count;
- giant mixed-authority “implement feature” Task;
- splitting one atomic invariant/state transition into unsafe fragments;
- multiple concurrent Tasks owning the same mutable contract without one owner;
- fake lanes created only to increase apparent parallelism;
- dependency removal merely to make a Task appear READY;
- Task identity reused for materially different scope without an authorized mutation/supersession record.

Real stacked code-baseline dependencies remain allowed when genuine; safe parallelism does not mean every Task must be independently mergeable.

## 5. Task DAG Governance Standard

Canonical separation:

```text
Planning DAG = decomposition / rationale / frozen history
GitHub Issue Dependencies = canonical live execution dependency graph after materialization
```

v4.3 does not create another DAG engine.

Material post-materialization mutations include, at minimum:

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

Every material mutation records:

```text
reason
requesting/approving authority
affected work items
old topology
new topology
scope/release impact
Task Pack impact
Review/Validation impact
```

Agents MUST NOT silently edit dependencies, redefine scope or rewrite topology merely to unblock execution.

## 6. Implementation Quality Standard

Language-neutral durable baseline includes, where applicable:

- explicit repository-authoritative build/test/check entrypoints;
- deterministic formatting/tool invocation where the ecosystem/project supports it;
- static/type analysis expectations where applicable;
- dependency/toolchain integration with v4.1;
- source/test/generated-output ownership and discoverability;
- public error/contract discipline;
- generated-code ownership/regeneration authority;
- logging/configuration/secret safety;
- project-defined complexity/quality checks without universal arbitrary thresholds.

It does not copy ecosystem style guides or mandate one formatter/linter/build tool.

## 7. Language Profiles

Stable namespace:

```text
profiles/languages/typescript.md
profiles/languages/python.md
profiles/languages/go.md
profiles/languages/java.md
profiles/languages/rust.md
```

Profiles map neutral requirements to ecosystem facts such as:

- manifest/lock authority;
- compiler/runtime compatibility;
- package/build tools;
- formatter/linter/type/static checks;
- test conventions/commands;
- module/package boundaries;
- generated output;
- selected high-risk language semantics.

Profiles are defaults/reference mappings. They MUST NOT copy large upstream style guides or convert Agent-local tool availability into repository authority.

## 8. Archetype Profile Framework

Provide composable archetype mappings for evidence-driven cases such as:

```text
library
CLI
web frontend
backend service
worker
SDK
desktop/plugin
monorepo
```

Initial v4.3 need not exhaustively implement every archetype. L2 may select a small representative set plus the framework.

## 9. Effective policy resolution

Conceptual resolution:

```text
Frozen Product / Architecture constraints
        ↓
Core ADS normative standards
        ↓
Applicable Language Profile(s)
+ Applicable Archetype Profile(s)
        ↓
PROJECT_OVERRIDES selections/strengthening
        ↓
Task / Execution Pack authority
```

`PROJECT_OVERRIDES` may choose, specialize or strengthen profile defaults within allowed authority. It MUST NOT silently weaken Frozen Product/Architecture or mandatory Core Standard semantics unless an owning waiver/exception mechanism explicitly permits it.

More-specific task instructions also cannot rewrite higher authority.

## 10. Machine-readable expectations

L2 should evaluate, without schema proliferation:

- Architecture Decision / invariant inventory — schema only if machine exchange needs justify it;
- DAG Mutation Record — strong candidate for a machine contract because live topology changes need attributable old/new truth;
- Profile applicability/effective-resolution record — use deterministic references when sufficient; schema only if cross-Agent resolution otherwise becomes ambiguous;
- Task decomposition quality fields — extend Task Pack/Execution Pack where possible rather than create a duplicate Task object.

## 11. Product-level forbidden inferences

v4.3 conformance must reject at least:

```text
popular tool/style -> architecture decision without drivers/trade-offs
high-impact UNKNOWN -> ordinary implementation detail
file count -> safe Task boundary
shared atomic invariant -> arbitrary parallel Tasks
dependency removal -> fabricated READY
branch/stack topology -> replacement for Issue Dependencies
live DAG mutation -> allowed without reason/authority/impact
local runtime/tool version -> repository compatibility authority
language profile -> universal style guide
profile/project override -> permission to weaken Frozen/Core authority
```

## 12. Non-goals

v4.3 does not:

- replace official language documentation;
- define universal coding style or directory structure;
- force one architecture paradigm;
- make all Tasks independently mergeable;
- replace Issue Dependencies with a custom DAG engine;
- allow DAG mutation to weaken Frozen Product/Architecture;
- duplicate v4.2 compatibility/migration ownership;
- require heavyweight architecture records for Fast-Path/non-material changes.

## 13. Compatibility posture

Target: additive/non-weakening v4 minor release.

Existing Task DAGs/Task Packs remain valid history. New DAG-governance rules apply prospectively to material mutations. Profiles are project/applicability driven and cannot retroactively rewrite historical evidence.

## 14. Product acceptance

v4.3.0 is complete when:

1. four normative owners in §2 have clear non-overlapping authority;
2. architecture quality is durable beyond prompts/templates;
3. Task decomposition encodes minimum coherent concern + maximum safe parallelism;
4. material live DAG mutations are attributable and cannot silently rewrite execution truth;
5. Implementation Quality has a small language-neutral core;
6. TypeScript, Python, Go, Java and Rust profiles provide evidence-driven mappings;
7. archetype profile composition is deterministic without profile explosion;
8. effective policy resolution with PROJECT_OVERRIDES is deterministic and non-weakening;
9. dogfood demonstrates a high-capability planner producing safe parallel lanes that lower-cost executors can consume without redesign.

## 15. Freeze basis / next gate

Freeze basis:

- `docs/implementation/4.3.0/L1_PRODUCT_EVIDENCE.md`
- v4.2 Product Freeze confirms compatibility/migration ownership remains outside v4.3.

After explicit Product Freeze:

1. run L2 Architecture Evidence;
2. decide machine-contract/profile information architecture;
3. materialize Task DAG only after L2;
4. create separate standards/profile/conformance lanes with JIT branches after dependency completion.

`LOCAL_ENV=NOT_REQUIRED` for Product Freeze/L2 research by default.