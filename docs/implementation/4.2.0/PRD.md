# ai-development-standard v4.2.0 PRD — Evolution Governance

Status: **DRAFT PRODUCT AUTHORITY — requires L1 Product Evidence review and explicit PRD Freeze before implementation**

## 1. Product intent

v4.2.0 standardizes how software contracts and persistent state evolve across versions. The goal is to prevent AI Agents from treating schema/API/data changes as ordinary local edits when those changes actually affect consumers, stored state, upgrade safety or rollback/recovery.

v4.2 must let a project answer, from durable facts:

1. What interface changed, and along which compatibility dimension?
2. Which producer/consumer combinations are supported and verified?
3. What schema/data migration is required between versions?
4. What recovery strategy exists if migration or rollout fails?
5. Which compatibility or migration evidence applies to this exact version/SHA/environment?

## 2. Problem

Current standards already require contract awareness, exact-SHA validation, migration testing where material and release qualification, but there is no unified authority for cross-version interface compatibility or persistent-state evolution.

Without such standards, Agents may:

- rename/remove fields without identifying a breaking contract change;
- infer compatibility from syntax/schema only while ignoring behavioral or consumer compatibility;
- treat fresh-database PASS as proof that upgrade from an existing version works;
- generate irreversible/destructive migrations without an explicit recovery strategy;
- confuse SQLite behavior with PostgreSQL behavior;
- silently redefine deprecation/removal policy;
- update consumer and provider together so tests pass while hiding an external compatibility break.

## 3. Scope

### 3.1 Interface & Compatibility Governance

Create a normative standard covering public and cross-component interfaces, including where applicable:

```text
REST / HTTP API
RPC / wire protocol
JSON / schema / serialization
Events / messages
CLI
SDK / library public API
Configuration contract
File format
Plugin / extension interface
```

Required change classes:

```text
ADDITIVE
COMPATIBLE
BREAKING
DEPRECATED
REMOVED
```

The standard must not collapse compatibility into one boolean. It should support relevant dimensions such as:

```text
source compatibility
wire compatibility
serialization compatibility
behavior compatibility
consumer compatibility
```

Required semantics:

- public/cross-system contract identity and version/baseline must be explicit;
- contract change must be classified against an identified baseline;
- producer/consumer evidence should bind concrete versions/SHAs when compatibility is release-significant;
- schema-level compatibility does not automatically prove runtime behavioral compatibility;
- deprecation and removal require an explicit policy/authority path;
- generated clients/SDKs and codegen outputs must remain subordinate to the canonical contract source;
- project-specific compatibility windows may strengthen defaults.

### 3.2 Data & Migration Governance

Create a normative standard for persistent schema/data evolution, including:

```text
schema migration
data migration / transform
backfill
seed/test data
index/storage-layout changes
migration package/artifact
```

Required semantics:

- release-significant schema/data change must be represented by a durable, reproducible transition mechanism or explicitly declared external migration procedure;
- migration identity/order/dependency must be reconstructable;
- fresh-install validation != upgrade validation;
- upgrade A→B != rollback/recovery B→A;
- one database/runtime tuple must not be presented as proof for another materially different tuple;
- destructive or high-risk migration requires explicit risk analysis and recovery strategy;
- every release-significant migration requires a recovery strategy, but not every migration is required to have an executable down migration;
- recovery may be rollback migration, backup/restore, forward repair, expand/contract, dual-write or another evidenced project-authorized method;
- production data operations require explicit authority and must not be inferred from development convenience.

## 4. Cross-standard integration

v4.2 should compose with rather than duplicate:

- `TESTING_STANDARD.md` — contract/integration/migration test-layer strategy;
- `VALIDATION_STANDARD.md` — exact-SHA/environment evidence;
- `RELEASE_STANDARD.md` — Candidate/Release authority;
- v4.1 External System Execution — real database/service environment classes;
- v4.1 Dependency/Toolchain — database/client/runtime compatibility;
- future Deployment Standard — migration ordering relative to rollout.

Expected conceptual flow:

```text
Current Version / Contract / Persistent State
        ↓
Proposed Change
        ↓
Compatibility + Migration Impact
        ↓
Implementation
        ↓
Contract / Upgrade / Failure / Recovery Tests
        ↓
Exact-SHA Validation
        ↓
Release / later Deployment
```

## 5. Non-goals

v4.2 does not:

- force semantic versioning onto every internal interface;
- require a specific schema language, migration framework or database;
- require down migrations where they are unsafe or impossible;
- make every internal refactor a public compatibility event;
- replace Task/PR Review or Release authority;
- prescribe one API style such as REST, gRPC or event-driven architecture.

## 6. Machine-readable expectations

L2 should determine whether the standard benefits from machine contracts such as:

- Interface Change Record;
- Compatibility Report;
- Consumer/Provider Compatibility Matrix;
- Migration Manifest;
- Migration Validation Report;
- Recovery Strategy Record.

Machine records must bind the relevant baseline/version/SHA/environment and preserve NOT_RUN/BLOCKED/NOT_APPLICABLE truth.

## 7. Compatibility posture

Target: additive/non-weakening minor release.

Existing projects without formal compatibility/migration artifacts should be able to adopt progressively. v4.2 must not retroactively claim that historical releases were incompatible or unvalidated; historical evidence remains scoped to what was actually executed and required at the time.

## 8. Product acceptance

v4.2.0 is complete when:

1. Interface & Compatibility and Data & Migration each have a single normative owner;
2. compatibility is explicitly multi-dimensional rather than a single boolean;
3. public contract changes can be classified and validated against an explicit baseline;
4. fresh install, upgrade, rollback/recovery and environment tuple semantics are distinguishable;
5. migration recovery is required without universally forcing unsafe down migrations;
6. negative conformance covers common Agent shortcuts such as silent field removal, consumer/provider co-change masking and fresh-DB-only proof;
7. at least one service/API case and one persistent-database case are dogfooded.

## 9. Next gate

Before Freeze:

1. run L1 Product Evidence against mature API/schema compatibility and migration systems;
2. validate boundaries with existing Testing/Validation/Release standards;
3. revise this PRD;
4. Freeze Product Authority;
5. run L2 Architecture Evidence and materialize Task DAG.
