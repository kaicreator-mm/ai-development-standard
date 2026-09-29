# ai-development-standard v4.3.0 PRD — Engineering Design & Implementation Profiles

Status: **DRAFT PRODUCT AUTHORITY — requires L1 Product Evidence review and explicit PRD Freeze before implementation**

## 1. Product intent

v4.3.0 standardizes the quality of architecture design, Task decomposition, live Task DAG evolution and language/ecosystem implementation profiles. The goal is not to prescribe one architecture or coding style; it is to make high-capability planning decisions explicit, reviewable and durable so lower-cost Agents can execute safely with bounded freedom.

The version should answer:

1. What must an architecture decision make explicit before it is considered sufficiently designed?
2. What makes a Task a coherent, reviewable, independently executable concern?
3. How may a live Task DAG evolve after planning freeze without silent scope/dependency drift?
4. Which language/ecosystem facts must be standardized so Agents do not reinvent build/test/layout conventions per Task?
5. How do global standards, language profiles, archetype profiles and project overrides compose?

## 2. Problem

v4 already contains strong L2 research prompts, lane-oriented Task DAG guidance and Execution Pack authority, but those concerns are distributed across prompts/templates rather than fully expressed as reusable normative engineering standards.

Current risks include:

- architecture decisions that select popular tools without drivers/trade-offs/failure semantics;
- Tasks that are too large, too small, split by file rather than concern, or fake-parallelized;
- Agents silently changing dependencies/lanes/scope after Task DAG materialization;
- language-specific execution rules being invented from the Agent host rather than repository facts;
- global standards duplicating ecosystem documentation instead of expressing only durable engineering requirements.

## 3. Scope

### 3.1 Architecture Design Standard

Create a normative standard that requires material architectures to make explicit, where applicable:

```text
Architecture Drivers
Invariants
System / component boundaries
Ownership and data ownership
Public / cross-component contracts
Sync / async boundaries
Failure semantics
Idempotency / ordering / concurrency
Durability
Security / trust boundaries
Observability requirements
Deployment topology assumptions
Compatibility and migration
Known UNKNOWNs
Evidence basis
Rollback / escape hatch
```

For material decisions require a bounded record of:

```text
Decision
Alternatives
Rationale
Trade-offs
Failure modes
Evidence
Escape hatch / rollback
```

Core principle:

> The standard defines what must be made explicit; it does not mandate microservices, DDD, Clean Architecture, event-driven systems, monoliths or any other universal architecture style.

The existing L2 Architecture Evidence prompt remains a research workflow; the new standard becomes the durable design-quality owner.

### 3.2 Task Decomposition Standard

Define a good Task as a minimum coherent concern with enough durable authority for independent execution.

A Task should normally have:

```text
one primary concern
explicit inputs / frozen authority
clear output
bounded write-set / ownership
forbidden scope
acceptance criteria
required gates
review policy
validation ownership
integration target
```

Task decomposition should actively seek maximum safe parallelism, but MUST NOT create artificial concurrency.

The standard should define when work commonly separates into contract/core/adapter/integration/UI/platform/migration/validation lanes, while making the taxonomy advisory rather than mandatory.

Explicit anti-patterns:

- split purely by file count;
- one giant “implement feature” Task with multiple unrelated authorities;
- splitting one atomic invariant/state transition into unsafe fragments;
- separate Tasks that must concurrently edit the same mutable contract without an owner;
- fake lanes created only to increase parallel Task count;
- dependency removal to make a Task appear READY.

Target principle:

> minimum coherent concern + maximum safe parallelism.

### 3.3 Task DAG Governance Standard

Existing planning DAG and GitHub Issue Dependencies remain distinct:

```text
Planning DAG = decomposition/history/rationale
Issue Dependencies = canonical live execution DAG
```

Add normative rules for live DAG evolution after materialization.

Supported mutation classes should include at least:

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

A material DAG change must record:

```text
reason
requesting/approving authority
affected work items
old topology
new topology
scope/release impact
required Task Pack / Review / Validation impact
```

Agents MUST NOT silently edit dependencies, redefine scope or reuse a Task identity for materially different work merely to unblock execution.

### 3.4 Implementation Quality Standard

Create a language-neutral implementation baseline covering durable concerns such as:

- deterministic formatting;
- static/type analysis expectations where ecosystem supports them;
- explicit build/test/check commands;
- dependency/toolchain integration with v4.1;
- predictable source/test/generated-output layout;
- public error/contract discipline;
- generated-code ownership;
- logging/secret safety;
- project-defined complexity/quality checks without universal arbitrary thresholds.

The core standard must not duplicate language style guides or prescribe subjective formatting choices already owned by ecosystem tooling.

### 3.5 Language Profiles

Introduce a profile mechanism under a stable namespace such as:

```text
profiles/languages/typescript.md
profiles/languages/python.md
profiles/languages/go.md
profiles/languages/java.md
profiles/languages/rust.md
```

Each profile maps the language-neutral requirements to ecosystem facts, including applicable items such as:

- canonical manifest and lockfile;
- runtime/compiler compatibility;
- package manager/build tool;
- formatter/linter/type/static checks;
- test conventions/commands;
- module/package boundaries;
- generated output;
- language-specific high-risk semantics (examples: ESM/CJS, Python packaging/imports, Go race/context, Java JDK/build tool, Rust MSRV/unsafe/features).

Profiles are defaults/reference mappings and may be strengthened by project authority. They MUST NOT copy large upstream style guides into ADS.

### 3.6 Project Archetype Profile Framework

Establish a composable profile axis for archetypes such as:

```text
library
CLI
web frontend
backend service
worker
SDK
desktop
plugin
monorepo
```

A repository may resolve its effective implementation policy as:

```text
Core Standards
+ Language Profile(s)
+ Archetype Profile(s)
+ PROJECT_OVERRIDES
```

Initial v4.3 may provide only the framework and a small evidence-driven archetype set if L1/L2 show value; profile explosion is explicitly out of scope.

## 4. Non-goals

v4.3 does not:

- replace official language documentation;
- define a universal coding style;
- force one architecture paradigm;
- force every project into the same directory structure;
- make all Tasks independently mergeable when real code-baseline dependencies exist;
- replace Issue Dependencies with a custom DAG engine;
- allow Task DAG governance to weaken Frozen Product/Architecture authority.

## 5. Cross-standard model

```text
Product Authority
      ↓
Architecture Design
      ↓
Task Decomposition
      ↓
Planning DAG
      ↓
Task Packs / live Issue DAG
      ↓
Implementation Quality
      + Language/Archetype Profiles
      ↓
Execution Pack / Agent implementation
      ↓
Testing / Review / Validation
```

The existing authority hierarchy in `EXECUTION_PACK_STANDARD.md` remains authoritative unless L2 identifies a justified additive clarification.

## 6. Machine-readable expectations

Architecture research should evaluate machine contracts for:

- Architecture Decision / invariant inventory;
- Task decomposition quality fields;
- DAG mutation record;
- Profile manifest / applicability declaration;
- effective profile resolution.

Do not introduce schemas when a deterministic reference/pointer is sufficient.

## 7. Compatibility posture

Target: additive/non-weakening minor release.

Existing Task DAGs and Task Packs remain valid history. New governance applies prospectively to material changes. Language profiles should be opt-in/project-declared until evidence supports stronger defaults.

## 8. Product acceptance

v4.3.0 is complete when:

1. Architecture Design, Task Decomposition and Task DAG Governance have clear normative ownership;
2. planning quality no longer depends only on prompts/templates;
3. DAG mutations are attributable and cannot silently rewrite execution truth;
4. Implementation Quality has a language-neutral core;
5. TypeScript, Python, Go, Java and Rust profiles exist with evidence-driven ecosystem mappings;
6. profile resolution with PROJECT_OVERRIDES is deterministic;
7. dogfood demonstrates a high-capability planner producing safe parallel lanes that lower-cost executors can consume without redesigning the system.

## 9. Next gate

Before Freeze:

1. run L1 Product Evidence against architecture/spec/task-planning and multi-language engineering practices;
2. review current L2/Task DAG/Execution Pack overlap to avoid duplicate authority;
3. revise this PRD;
4. Freeze Product Authority;
5. run L2 Architecture Evidence, including profile information architecture;
6. produce Task DAG with separate standards/profile/conformance lanes where safely parallel.
