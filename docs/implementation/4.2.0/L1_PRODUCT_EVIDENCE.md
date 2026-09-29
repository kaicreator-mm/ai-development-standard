# v4.2.0 L1 Product Evidence — Evolution Governance

Status: **COMPLETE — supports Product Freeze after the PRD corrections recorded below**

Research date: 2026-09-30

Baseline / authority reviewed:

- `main@e9eb39235e45e9ad90407b803ab1c8679d348dbf`
- Draft `docs/implementation/4.2.0/PRD.md`
- v4.1 Frozen Product/L2 decisions for Dependency & Toolchain, External System Execution and Validation Impact composition
- current `TESTING_STANDARD.md`, `VALIDATION_STANDARD.md`, `RELEASE_STANDARD.md`
- roadmap `docs/implementation/V4_1_TO_V4_7_ROADMAP.md`

This evidence follows `prompts/L1_PRODUCT_EVIDENCE.md`. It is Product evidence, not itself Product Freeze.

## 1. Recommendation

**PROCEED WITH NARROWING.**

The Product problem is well evidenced: interface evolution and persistent-state evolution are materially different from ordinary source edits, and both need durable baseline/transition/evidence semantics. The Draft PRD is directionally correct, but L1 requires five corrections before Freeze:

1. Do not place `ADDITIVE`, `COMPATIBLE`, `BREAKING`, `DEPRECATED`, `REMOVED` on one overloaded axis. Separate **change operation/class** from **compatibility outcome by dimension**.
2. Compatibility is explicitly multi-dimensional. Wire-safe does not imply source/application compatibility, and schema-valid does not imply behavioral/consumer compatibility.
3. Model migration as a **state transition** with source state/baseline, target state, mechanism/order/dependencies, evidence and recovery strategy. Fresh-install evidence is never upgrade evidence.
4. Require a recovery strategy for release-significant migration, but do not universally require executable down migrations. Rollback, restore, forward repair, expand/contract or another evidenced method may be valid.
5. Keep deployment sequencing/orchestration with v4.4. v4.2 owns compatibility and migration semantics; v4.4 later owns rollout ordering and deployment result.

## 2. Interface & Compatibility Evidence

### 2.1 Compatibility cannot be one boolean

Protocol Buffers explicitly distinguishes binary wire-safe, wire-compatible/conditionally-safe and wire-unsafe changes. Its documentation also warns that a wire-safe schema change can still break generated/application code, for example exhaustive enum handling.

Sources:

- https://protobuf.dev/programming-guides/proto3/#updating
- https://protobuf.dev/best-practices/dos-donts/

This directly supports the Draft PRD's multi-dimensional compatibility requirement. The Product should preserve dimensions such as wire/serialization, source/API, behavioral and consumer compatibility rather than creating one `compatible=true` field.

### 2.2 A baseline/public contract must be explicit

Semantic Versioning requires a declared public API before version numbers can communicate backward-compatible versus incompatible change. ADS does not need to mandate SemVer, but this is strong evidence that compatibility classification is meaningless without an identified contract/baseline.

Source: https://semver.org/

**Finding:** v4.2 should require an explicit baseline identity for release-significant compatibility claims. Version labels alone are insufficient when exact SHA/schema/consumer identity matters.

### 2.3 Producer and consumer co-change can hide breaks

If a provider and its only in-repo consumer are changed together, integration tests may pass while older or external consumers break. Compatibility evidence therefore needs, where release-significant, explicit producer/consumer identities or a project-authoritative compatibility window.

**Product negative case:** `new producer + new consumer PASS` MUST NOT automatically prove `old consumer + new producer` compatibility.

## 3. Data & Migration Evidence

### 3.1 Existing state changes migration risk

PostgreSQL documents that schema operations have materially different effects depending on operation and existing data. Adding a constant-default column can be fast without rewriting every row, while volatile defaults may update every row; changing types may require conversions and can fail against existing values/constraints.

Source: https://www.postgresql.org/docs/18/ddl-alter.html

This is direct evidence that a fresh empty database does not prove upgrade behavior over existing state.

### 3.2 Fresh install, upgrade and recovery are distinct claims

Required evidence dimensions should remain separate:

```text
fresh install / bootstrap
upgrade A -> B
mixed-version / compatibility window when applicable
failed/interrupted migration recovery
rollback B -> A when supported
forward repair / restore when rollback is not supported
```

A project may not need every dimension, but an Agent must not substitute one for another.

### 3.3 Recovery strategy != mandatory down migration

Some destructive or externally coordinated migrations cannot safely reverse through a generated `down` script. The durable requirement should be a project-authorized recovery strategy with prerequisites and evidence, not a universal implementation mechanism.

Valid strategy classes include backup/restore, forward repair, expand/contract, dual-read/write transition, rollback migration where safe, or another explicitly evidenced method.

## 4. Product Boundary With Existing/Future Owners

v4.2 should own:

- interface/contract baseline identity;
- change operation/classification;
- compatibility outcome by relevant dimension;
- producer/consumer/version evidence binding;
- persistent-state transition identity/order/dependency;
- upgrade/migration/recovery semantics and evidence requirements.

It should feed, not replace:

- `TESTING_STANDARD.md` — test layer/type strategy;
- `VALIDATION_STANDARD.md` — exact subject/environment PASS/FAIL/BLOCKED truth and evidence reuse;
- `RELEASE_STANDARD.md` — Candidate/Release authority;
- v4.1 External System Execution — database/service fidelity and environment identity;
- v4.1 Dependency & Toolchain — client/database/runtime compatibility inputs;
- v4.4 Deployment — rollout sequencing, environment application and deployment result.

## 5. Required PRD Corrections Before Freeze

### 5.1 Replace overloaded change-class list

Instead of treating these as one enum:

```text
ADDITIVE / COMPATIBLE / BREAKING / DEPRECATED / REMOVED
```

freeze two concepts:

```text
change operation/kind: ADD | ALTER | DEPRECATE | REMOVE | RENAME | project-defined
compatibility outcome per dimension: COMPATIBLE | CONDITIONALLY_COMPATIBLE | INCOMPATIBLE | UNKNOWN | NOT_APPLICABLE
```

L2 may choose exact machine vocabulary. Product Authority should freeze the separation, not necessarily these exact enum strings.

### 5.2 Compatibility evidence is scoped

A compatibility report proves only the baseline/producer/consumer/protocol/environment tuple it actually evaluates. Do not infer universal compatibility from one matrix cell or one schema checker.

### 5.3 Migration transition is first-class

A release-significant migration should be reconstructible as:

```text
source state/baseline
-> ordered transition mechanism
-> target state
+ prerequisites/dependencies
+ execution environment
+ evidence
+ recovery strategy
```

### 5.4 Destructive migration authority

Production data mutation requires explicit applicable authority. Local development convenience or migration-file presence never authorizes production execution.

## 6. Machine-contract Product Findings

L1 supports machine-readable records where they carry durable cross-Agent truth, but does not justify six independent schemas by default.

L2 should evaluate a compact set around:

1. **Interface Change / Compatibility Record** — baseline, change operation, dimensions, producer/consumer evidence.
2. **Migration Transition Record/Manifest** — source/target state, mechanism/order/dependencies, environment applicability.
3. **Recovery Strategy / Migration Validation linkage** — may be embedded/referenced rather than a standalone schema when deterministic references are sufficient.

Avoid a mandatory full Cartesian compatibility matrix for small/internal interfaces.

## 7. Product-level Negative Conformance

At minimum v4.2 must reject these shortcuts:

- wire-safe -> source/application compatible by assertion;
- schema diff PASS -> behavioral compatibility PASS;
- new producer + new consumer PASS -> old consumer compatibility PASS;
- fresh DB PASS -> upgrade A->B PASS;
- migration file exists -> migration executed PASS;
- SQLite PASS -> PostgreSQL PASS when behavior is materially different;
- rollback script absent -> release automatically impossible, even when an evidenced alternate recovery strategy exists;
- destructive migration -> production authority inferred from credentials/tool access;
- old migration evidence -> successor SHA/environment PASS without Validation Impact/currentness rules.

## 8. Counter-evidence / Scope Risks

- Many internal refactors have no cross-version consumer or persistent-state consequence. v4.2 must remain materiality-driven.
- Compatibility frameworks differ by protocol and language. ADS must define dimensions/truth, not duplicate every ecosystem checker.
- Small SQLite/local-only applications may not need producer/consumer matrices or complex rollout windows.
- A universal requirement for reversible migrations would be unsafe and unrealistic.

These findings support progressive adoption and Fast Path rather than weakening the core truth model.

## 9. L1 Verdict

**Evidence is sufficient to revise and Freeze v4.2 Product Authority.**

Product Freeze is justified once the Draft PRD incorporates the separation of change operation vs compatibility outcome, transition/recovery semantics, evidence scoping, and v4.4 deployment boundary above.

`LOCAL_ENV=NOT_REQUIRED` for Product Freeze. Executable database/service proofs belong to later architecture/conformance Tasks, not this L1 decision.