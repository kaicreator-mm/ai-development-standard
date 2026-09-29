# v4.2.0 L2 Architecture Evidence — Evolution Governance

Status: **FROZEN L2 ARCHITECTURE AUTHORITY — 2026-09-30**

Freeze basis:

- Frozen Product Authority: `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9`
- L1: `docs/implementation/4.2.0/L1_PRODUCT_EVIDENCE.md`
- explicit L2 Freeze: the commit introducing this frozen L2 file

## 1. Frozen inputs

- Frozen PRD: `docs/implementation/4.2.0/PRD.md`
- v4.1 Frozen execution-foundation Product/L2 semantics, especially External System Execution, Dependency/Toolchain and Validation Impact composition
- current `TESTING_STANDARD.md`, `VALIDATION_STANDARD.md`, `RELEASE_STANDARD.md`
- roadmap `docs/implementation/V4_1_TO_V4_7_ROADMAP.md`

Architecture research follows `prompts/L2_ARCHITECTURE_EVIDENCE.md`: define drivers/invariants/owners/contracts/UNKNOWN disposition, prefer static/source evidence where sufficient, and require executable Research Demo only for architecture behavior that cannot be established otherwise.

## 2. Architecture recommendation

Use **two normative domain owners + two compact machine-contract families + existing Validation/Release authority**.

```text
Contract / Persistent-State Baseline
              │
              ├───────────────┐
              ▼               ▼
 Interface & Compatibility   Data & Migration
 Governance Standard         Governance Standard
              │               │
              ▼               ▼
 Compatibility Record     Migration Transition Record
              │               │
              └──────┬────────┘
                     ▼
          Existing Testing / Validation
                     │
                     ▼
                 Release
                     │
                     ▼
          later v4.4 Deployment orchestration
```

Architecture decisions:

1. **Two normative owners only.** Interface/Compatibility and Data/Migration are separate concerns with explicit cross-references.
2. **No new global Gate state machine.** Compatibility outcomes are domain facts; Validation retains PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE.
3. **Two default machine-contract families.** Use a Compatibility Record and a Migration Transition Record. Recovery strategy is embedded/referenced from the migration record rather than becoming a mandatory third schema.
4. **Change operation and compatibility outcome remain orthogonal fields.** Do not encode them as one enum.
5. **Compatibility dimensions are an extensible map/list, not a closed universal enum.** Provide recommended canonical dimension names while allowing project/protocol extension.
6. **Migration transition identity is directional.** `A -> B` is not interchangeable with fresh install, `B -> A`, or recovery from interrupted `A -> B`.
7. **Environment/runtime evidence composes with v4.1 Execution Context/External System facts when material.** Do not duplicate provider/environment schema ownership.
8. **Deployment ordering remains future v4.4 authority.** v4.2 may expose prerequisites/order/dependencies that deployment consumes but does not own rollout result.

## 3. Architecture drivers

### D1 — Preserve evidence dimensionality

Protocol Buffers demonstrates that wire-safe schema changes may still break source/application behavior. Architecture must permit different compatibility outcomes for different dimensions under one change subject.

Reference: https://protobuf.dev/programming-guides/proto3/#updating

### D2 — Baseline identity is mandatory for meaningful comparison

Compatibility is a relation between an identified old and new contract plus, where material, consumer/provider identities. A label such as `v2` without immutable/pinned contract identity is insufficient for exact evidence.

### D3 — Persistent state makes transition behavior first-class

PostgreSQL schema operations can have materially different effects on existing rows and constraints. Fresh/bootstrap behavior cannot stand in for upgrade behavior.

Reference: https://www.postgresql.org/docs/18/ddl-alter.html

### D4 — Recovery method varies by project

Architecture must record recovery semantics and prerequisites without forcing down migrations. A recovery reference can name backup/restore, forward repair, expand-contract, rollback migration or another authorized strategy.

### D5 — Existing ADS already owns validation truth

v4.2 must avoid introducing compatibility/migration “PASS” states that collide with `VALIDATION_STANDARD.md`. A Compatibility Record can say a dimension is `COMPATIBLE` or `INCOMPATIBLE`; whether the required validation gate passed remains separate.

### D6 — Progressive adoption / Fast Path

An internal additive config field with no external consumer should not require a full consumer matrix. Machine records are required only when the compatibility/migration concern is material and durable machine exchange adds value.

## 4. Normative owner map

| Semantic concern | v4.2 owner | Must not duplicate |
|---|---|---|
| contract baseline/change operation | `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` | Product/Architecture authority, Git diff ownership |
| compatibility dimensions/outcomes | `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` | Validation result states |
| producer/consumer compatibility evidence semantics | `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` | Testing layer strategy |
| persistent-state transition identity/order/dependency | `DATA_MIGRATION_GOVERNANCE_STANDARD.md` | Deployment rollout state |
| recovery strategy requirement/semantics | `DATA_MIGRATION_GOVERNANCE_STANDARD.md` | incident/runtime recovery in v4.5 |
| exact subject/environment validation | existing `VALIDATION_STANDARD.md` | no new PASS state |
| release qualification | existing `RELEASE_STANDARD.md` | no release verdict in v4.2 |
| rollout/deployment ordering/result | future v4.4 Deployment | v4.2 only exports prerequisites |

## 5. Machine contracts

### 5.1 `schemas/compatibility-record-v1.schema.json`

Purpose: durable exact compatibility claim for one identified contract evolution subject.

Proposed shape:

```yaml
schema_version: 1
record_id:
contract:
  kind:
  identity:
baseline:
  version_ref:
  sha_or_digest:
candidate:
  version_ref:
  sha_or_digest:
change_operations: []
dimensions:
  - name: wire
    outcome: COMPATIBLE | CONDITIONALLY_COMPATIBLE | INCOMPATIBLE | UNKNOWN | NOT_APPLICABLE
    evidence_refs: []
producer_refs: []
consumer_refs: []
compatibility_window_ref:
notes_ref:
```

Requirements:

- baseline and candidate are distinct identities;
- dimensions are extensible;
- operation does not imply outcome;
- absent dimension is not implicit PASS;
- schema checker evidence may support a dimension but cannot manufacture behavior/consumer proof;
- producer/consumer refs are optional when not material.

### 5.2 `schemas/migration-transition-v1.schema.json`

Purpose: durable description of a release-significant persistent-state transition.

Proposed shape:

```yaml
schema_version: 1
transition_id:
source_state_ref:
target_state_ref:
mechanism_refs: []
ordered_steps: []
dependency_refs: []
applicability:
  datastore_kind:
  runtime_or_version:
  environment_ref:
risk_class:
recovery:
  strategy_class:
  strategy_ref:
  prerequisites: []
validation_refs: []
```

Requirements:

- no embedded `PASS` field;
- directional source/target identity;
- fresh-install is represented separately rather than pretending source state is empty unless that is the actual subject;
- recovery strategy may be non-reversible/forward-only;
- production execution authority is never inferred from the record itself.

### 5.3 Existing schema integration

Prefer optional references from existing evidence objects where useful, rather than making v4.2 schemas mandatory everywhere. `validation-report` may reference compatibility/migration record IDs/refs when the gate actually validates them.

Do not modify dispatch/workflow state merely to carry these domain records.

## 6. Architecture UNKNOWNs and disposition

| ID | UNKNOWN | Impact | Disposition | Decision |
|---|---|---|---|---|
| U1 | One compatibility enum or multi-dimensional outcomes? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | Multi-dimensional, extensible dimensions. |
| U2 | Separate change-operation enum from compatibility? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | Yes, orthogonal fields. |
| U3 | Need a full mandatory compatibility matrix? | High | `STATIC_EVIDENCE_SUFFICIENT` | No; records may reference producer/consumer/window only when material. |
| U4 | Need a separate Recovery schema? | Medium | `STATIC_EVIDENCE_SUFFICIENT` | No default third family; embed/reference recovery in migration transition. |
| U5 | Need mandatory down migrations? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No; recovery strategy required, implementation method project-owned. |
| U6 | Does v4.2 own deployment ordering/result? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No; export transition prerequisites to future v4.4. |
| U7 | Is executable database Research Demo required before L2 Freeze? | High | `STATIC_EVIDENCE_SUFFICIENT` | No; architecture concerns are authority/schema composition. Real upgrade/failure proof belongs implementation conformance/dogfood. |
| U8 | How to avoid dimension vocabulary explosion? | Medium | `STATIC_EVIDENCE_SUFFICIENT` | canonical recommended names + project/protocol extension; no closed enum. |

**Research Demo decision: NOT REQUIRED before L2 Freeze.**

Executable service/database cases are required later for conformance/dogfood, but no runtime algorithm or external integration choice blocks the architecture decision.

## 7. Standard responsibilities

### 7.1 Interface & Compatibility Governance

Must define:

- applicability/materiality;
- contract/baseline identity;
- change-operation semantics;
- compatibility dimensions/outcomes;
- producer/consumer/window evidence;
- deprecation/removal authority;
- generated-client/codegen subordination;
- non-inference/adversarial cases;
- Fast Path behavior.

### 7.2 Data & Migration Governance

Must define:

- persistent-state subject identity;
- transition ordering/dependencies;
- fresh vs upgrade vs interrupted recovery distinctions;
- environment/runtime applicability;
- destructive/high-risk change handling;
- recovery strategy requirement;
- production authority boundary;
- migration evidence binding;
- Fast Path behavior.

## 8. Conformance architecture

Implementation must include executable semantic negatives for at least:

```text
wire-safe => source-compatible                 FAIL inference
schema-compatible => behavior-compatible       FAIL inference
new/new pair => old-consumer compatibility     FAIL inference
fresh install => upgrade                        FAIL inference
A->B PASS => B->A PASS                          FAIL inference
migration exists => migration executed          FAIL inference
credential available => production authority    FAIL inference
no down migration => no recovery possible       FAIL inference
old SHA/environment evidence => successor PASS   FAIL inference
```

Positive cases should include an additive backward-compatible interface change and a stateful migration with a non-down-migration recovery strategy.

## 9. Adoption / compatibility posture

- additive/non-weakening v4 minor;
- historical evidence is never retrofitted;
- projects may adopt records prospectively;
- simple/internal changes may remain prose/pointer-driven when material truth is still deterministic;
- future v4.4 consumes migration prerequisites without rewriting v4.2 ownership.

## 10. L2 verdict

**Architecture is sufficiently resolved to materialize the v4.2 Task DAG.**

No local/Build Host execution is required for Task planning. Later service/database dogfood may require a local or external-system Validation handoff with an exact subject and environment tuple.