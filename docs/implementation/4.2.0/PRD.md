# ai-development-standard v4.2.0 PRD — Evolution Governance

Status: **FROZEN PRODUCT AUTHORITY**

Product Freeze basis:

- L1 evidence: `docs/implementation/4.2.0/L1_PRODUCT_EVIDENCE.md`
- revised Freeze Candidate: `6a59ad3b194a93ad9aa1bdafc6064b52ed3ee515`
- Freeze date: 2026-09-30

## 1. Product intent

v4.2.0 standardizes how software contracts and persistent state evolve across versions. The goal is to prevent AI Agents from treating interface/schema/data changes as ordinary local edits when they affect consumers, stored state, upgrade safety or recovery.

The version must let a project answer, from durable facts:

1. What contract/state baseline changed?
2. What operation occurred and what compatibility outcome applies on each material dimension?
3. Which producer/consumer/version combinations were actually evidenced?
4. What persistent-state transition is required between versions?
5. What evidence exists for fresh install, upgrade and failure/recovery paths?
6. Which recovery strategy applies if the transition fails?

## 2. Product model

v4.2 has two normative owners that compose through existing Validation/Release authority:

```text
Interface & Compatibility Governance
Data & Migration Governance
```

They are related but not collapsed into one state machine.

### 2.1 Change operation is not compatibility outcome

The Product MUST keep these concepts separate.

Change operation/kind may include, where applicable:

```text
ADD
ALTER
DEPRECATE
REMOVE
RENAME
project-defined operation
```

Compatibility outcome is evaluated per relevant dimension, for example:

```text
COMPATIBLE
CONDITIONALLY_COMPATIBLE
INCOMPATIBLE
UNKNOWN
NOT_APPLICABLE
```

L2 may refine exact machine vocabulary. The Product invariant is that operation and compatibility result are not one overloaded enum.

### 2.2 Compatibility is multi-dimensional

Material dimensions may include:

```text
source / compile compatibility
wire / protocol compatibility
serialization compatibility
schema compatibility
behavior compatibility
consumer compatibility
configuration/file-format compatibility
```

A PASS on one dimension MUST NOT manufacture PASS on another.

## 3. Interface & Compatibility Governance

Create a single normative owner for public and cross-component interfaces, including where applicable:

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

Required semantics:

- contract identity and comparison baseline are explicit when compatibility is material;
- each material change records operation/kind separately from compatibility outcome;
- producer/consumer evidence binds concrete versions/SHAs or an explicitly authorized compatibility window when release-significant;
- schema/wire compatibility does not automatically prove source/application/behavior compatibility;
- generated clients/SDKs remain subordinate to the canonical contract source;
- deprecation/removal follows explicit project/product authority;
- project-specific compatibility windows may strengthen defaults;
- co-changing a producer and consumer MUST NOT hide an external/older-consumer break.

Compatibility evidence proves only the tuple/dimensions actually evaluated.

## 4. Data & Migration Governance

Create a single normative owner for persistent-state evolution, including:

```text
schema migration
data migration / transform
backfill
seed/test-data transition
index/storage-layout changes
migration package/artifact
external migration procedure
```

A release-significant migration is modeled as a reconstructible transition:

```text
source state / baseline
        ↓
ordered transition mechanism
+ dependencies / prerequisites
+ target execution environment
        ↓
target state
        ↓
evidence
+ recovery strategy
```

Required semantics:

- transition identity/order/dependency is reconstructable;
- fresh-install/bootstrap evidence is distinct from upgrade evidence;
- upgrade `A -> B` is distinct from rollback/recovery `B -> A`;
- interrupted/failed migration recovery is distinct from successful upgrade;
- one database/runtime/environment tuple MUST NOT be substituted for another materially different tuple;
- destructive/high-risk transitions require explicit risk/recovery treatment;
- every release-significant migration has an applicable recovery strategy;
- recovery strategy does **not** universally require an executable down migration;
- permitted recovery strategies may include rollback migration, backup/restore, forward repair, expand/contract, dual-read/write transition or another project-authorized evidenced method;
- production data mutation requires explicit applicable authority and cannot be inferred from credentials/tool availability.

## 5. Evidence dimensions

Projects apply only the dimensions material to their product, but Agents MUST distinguish:

```text
fresh install / bootstrap
upgrade from supported baseline(s)
mixed-version / compatibility window when applicable
failed/interrupted transition recovery
rollback when supported
forward repair / restore when rollback is not supported
```

Absence of a non-applicable dimension is not failure. Substituting a cheaper dimension for a required one is non-conformant.

## 6. Cross-standard integration

v4.2 feeds rather than duplicates:

- `TESTING_STANDARD.md` — contract/integration/migration test strategy;
- `VALIDATION_STANDARD.md` — exact subject/environment result and evidence reuse/currentness;
- `RELEASE_STANDARD.md` — Candidate/Release authority;
- v4.1 External System Execution — database/service fidelity/environment identity;
- v4.1 Dependency & Toolchain — client/database/runtime/toolchain compatibility inputs;
- v4.4 Deployment — rollout sequencing, migration ordering relative to deployment and Deployment result.

Expected conceptual flow:

```text
Current Contract / Persistent State
        ↓
Proposed Change
        ↓
Operation + Compatibility / Migration Impact
        ↓
Implementation
        ↓
Contract / Upgrade / Failure / Recovery Tests
        ↓
Exact-subject Validation
        ↓
Release
        ↓
later Deployment orchestration
```

v4.2 owns transition semantics; it does not create Deployment SUCCESS/FAILED states.

## 7. Product-level forbidden inferences

The final standard/conformance MUST reject at least:

```text
wire-safe -> source/application compatible
schema diff PASS -> behavioral compatibility PASS
new producer + new consumer PASS -> old consumer compatible
fresh DB PASS -> upgrade PASS
migration file exists -> migration executed PASS
SQLite PASS -> PostgreSQL PASS when behavior is materially different
credential/tool access -> production migration authority
no down migration -> no valid recovery strategy
old SHA/environment evidence -> successor PASS without currentness/impact authority
```

## 8. Machine-readable expectations

L2 should evaluate a compact composition rather than assume one schema per concept. Candidate families:

1. **Interface Change / Compatibility Record**
   - contract/baseline identity;
   - change operation;
   - compatibility outcomes by dimension;
   - producer/consumer/evidence references.
2. **Migration Transition Record/Manifest**
   - source/target state;
   - ordered mechanism/dependencies;
   - applicable environment/runtime;
   - execution/evidence references.
3. **Recovery Strategy linkage**
   - may be embedded or referenced if deterministic pointer semantics are sufficient.

A full Cartesian consumer/provider matrix is not mandatory for small/internal interfaces. Machine records preserve `UNKNOWN`, `NOT_RUN`, `BLOCKED` and `NOT_APPLICABLE` truth through existing owners rather than converting them to PASS.

## 9. Non-goals

v4.2 does not:

- mandate Semantic Versioning for every interface;
- require a specific API/schema/migration framework or database;
- require reversible/down migrations universally;
- make every internal refactor a compatibility event;
- replace Task/Review/Validation/Release authority;
- prescribe REST, gRPC, events or another API style;
- own rollout/deployment sequencing or Deployment result;
- require compatibility matrices when no material multi-version consumer relationship exists.

## 10. Compatibility posture

Target: additive/non-weakening v4 minor release.

Existing projects may adopt prospectively. Historical evidence remains scoped to what was actually executed and required at the time. v4.2 MUST NOT retroactively claim historical compatibility, upgrade coverage or recovery evidence that did not exist.

If implementation requires an incompatible core lifecycle/authority/wire change, record it as future-major input rather than hiding it in v4.2.

## 11. Product acceptance

v4.2.0 is complete when:

1. Interface & Compatibility and Data & Migration each have one normative owner;
2. change operation and compatibility outcome are distinct concepts;
3. compatibility is multi-dimensional rather than one boolean;
4. public/cross-component contract changes can be evaluated against an explicit baseline;
5. producer/consumer co-change cannot mask required compatibility truth;
6. migration is represented as source-state -> transition -> target-state with evidence and recovery strategy;
7. fresh install, upgrade, interrupted recovery and rollback/forward-repair semantics are distinguishable;
8. recovery is required without universally forcing unsafe down migrations;
9. negative conformance covers the forbidden inferences in §7;
10. at least one service/API case and one persistent-database case are dogfooded during implementation/closure.

## 12. Next gate

Product Authority is Frozen. Before implementation:

1. run L2 Architecture Evidence;
2. decide machine-contract composition and owner map;
3. materialize Task DAG only after L2;
4. create Task Packs/Issues and native dependencies;
5. execute concern Validation/Review followed by Version Closure.

`LOCAL_ENV=NOT_REQUIRED` for L2 research by default. Executable database/service proof must use an explicit later handoff/validation subject.