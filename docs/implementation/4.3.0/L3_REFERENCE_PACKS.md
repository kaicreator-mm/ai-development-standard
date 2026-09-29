# v4.3.0 L3 Reference Packs — Engineering Design & Implementation Profiles

Status: **IMPLEMENTATION REFERENCE — subordinate to Frozen PRD/L2/Task DAG**

## T01 — DAG Mutation Machine Contract

### Tests
- Draft 2020-12 meta-valid schema;
- material mutation has identity/class/reason/authority/affected tasks;
- old/new topology reconstructible;
- dependency removal cannot omit reason/authority;
- Review/Validation/Task Pack impact can be recorded explicitly;
- schema has no Product/Architecture/Task READY authority;
- historical payloads remain valid when optional refs absent.

### Contract
`dag-mutation-record-v1` records mutation evidence; it never performs/makes authoritative the GitHub dependency change itself.

### Failure handling
Unknown topology/authority for a material mutation => BLOCKED, not fabricated new DAG truth.

## T02 — Profile Framework

### Tests
- deterministic profile IDs/applicability/reference sections;
- language/archetype profiles remain mapping/default layers;
- project selections cannot silently weaken mandatory higher authority;
- local Agent tools never become profile authority;
- no repository-wide resolver/state machine introduced.

### Contract
`profiles/README.md` defines stable profile document semantics and composition references only.

### Implementation
Prefer human-readable structured Markdown with predictable metadata/sections. Do not introduce a profile schema unless implementation proves deterministic doc pointers insufficient.

## T03 — Architecture Design Standard

### Tests
- material decisions require drivers/invariants/boundaries/failure semantics/evidence/UNKNOWN handling;
- popularity/tool familiarity alone is not sufficient rationale;
- bounded Decision/Alternatives/Rationale/Trade-offs/Failure modes/Evidence/Escape hatch record;
- small/Fast-Path changes do not require heavyweight architecture ceremony;
- v4.2 remains compatibility/migration semantic owner;
- L2 remains research workflow owner.

### Failure handling
High-impact unresolved UNKNOWN cannot be silently delegated to implementation; route through explicit architecture/product decision or BLOCKED.

## T04 — Task Decomposition Standard

### Tests
- one primary concern + bounded write-set/forbidden scope/acceptance/gates/integration/dependencies;
- file-count split alone rejected;
- giant mixed-authority Task rejected;
- atomic invariant cannot be fake-parallelized;
- real stacked dependency allowed;
- sibling central wiring stays with integration owner;
- dependency removal cannot fabricate readiness.

### Contract
Minimum coherent concern + maximum safe parallelism.

### Failure handling
If a Task cannot be isolated without shared-authority race, merge concerns or introduce a clear contract/integration owner rather than pretending independence.

## T05 — Task DAG Governance Standard

### Tests
- Planning DAG != live Issue Dependencies;
- material ADD/SPLIT/MERGE/SUPERSEDE/ADD_DEPENDENCY/REMOVE_DEPENDENCY/etc requires mutation record;
- old/new topology and affected Task refs durable;
- dependency removal without authority/impact rejected;
- Task identity cannot be silently reused after material scope change;
- PR stack/cherry-pick cannot replace live DAG.

### Contract
GitHub Issue Dependencies remain canonical live execution graph; this standard governs semantic mutation and evidence.

### Failure handling
Missing native dependency capability => explicit controller/local GitHub handoff, not body-text substitution.

## T06 — Implementation Quality Standard

### Tests
- repository-authoritative commands/tooling > Agent-local defaults;
- deterministic format/static/type/build/test checks where applicable;
- dependency/toolchain/config/secret/testing owners referenced, not duplicated;
- generated code ownership explicit;
- arbitrary universal thresholds rejected;
- profile mapping layer subordinate to core/project authority.

### Contract
Small language-neutral implementation-quality baseline.

### Failure handling
Required project check unavailable => truthful BLOCKED/waiver path from owning standard, not requirement rewrite.

## T07 — TypeScript + Python Profiles

### Tests
For each profile verify:
- manifest/lock/toolchain mapping is ecosystem-aware but project-authoritative;
- common formatter/linter/type/test/build choices are references/mappings, not universal mandates;
- risky semantics highlighted without turning into a style guide;
- local installed Node/Python version cannot rewrite compatibility;
- profile composes with archetype + PROJECT_OVERRIDES.

TypeScript focus: package manager/lock, ESM/CJS/module resolution, typecheck vs runtime/build, generated declarations/output.

Python focus: `pyproject.toml`/requirements/lock variability, packaging/import environment, interpreter compatibility vs preferred dev, type/static/tool selection, test layout.

## T08 — Go + Java + Rust Profiles

### Tests
Go: module/toolchain authority, `go test`, race/context/concurrency caveats, generated code.

Java: JDK compatibility vs selected runtime, Maven/Gradle project authority, test/build/check split, generated sources.

Rust: Cargo manifest/lock, MSRV vs preferred toolchain, features/targets/unsafe semantics, test/clippy/fmt as project-selected checks.

All: no local tool availability -> repo authority; no universal exact tool-version mandate beyond project/frozen authority.

## T09 — Archetype Profiles

### Tests
- library mapping emphasizes public contract/package/consumer compatibility but does not mandate publication;
- service mapping emphasizes runtime/external/config/deployment/observability applicability but does not require production deployment;
- CLI mapping emphasizes command interface/build/package/environment semantics without universal installer format;
- archetypes are composable mappings, not Product Architecture;
- language + archetype conflict resolves through higher authority/project rules rather than discovery order.

## T10 — Adoption & Wiring

### Tests
- manifest discovers four normative owners + DAG mutation schema + profile framework;
- Task Pack/Execution Pack docs consume decomposition/profile semantics without duplicate Task object;
- PROJECT_OVERRIDES profile selection/strengthening deterministic;
- no v4.7 unified resolver implemented;
- historical projects remain valid/progressive adoption;
- Fast Path remains lightweight.

## T11 — Conformance & Dogfood

### Negative families
- popular architecture -> justified decision;
- UNKNOWN -> implementation freedom;
- file count -> Task boundary;
- atomic shared invariant -> parallel-safe;
- dependency removal -> READY;
- PR stack -> live DAG;
- DAG edit without record/authority -> valid topology;
- local tool version -> repository profile authority;
- profile mapping -> universal style/tool mandate;
- PROJECT_OVERRIDES -> weakening Frozen/Core authority.

### Positive dogfood
Use v4.3 itself or another non-trivial ADS planning subject: high-capability planner creates concern-sized Task DAG/Task Packs; lower-cost executor prompt can act without redesigning Product/Architecture. Record where durable authority is sufficient/insufficient.

### Closure input
Produce evidence summary and unresolved P0/P1/P2/P3 disposition for Version Closure; do not issue release verdict.