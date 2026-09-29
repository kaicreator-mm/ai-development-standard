# v4.7.0 Authority / State / Schema Convergence Inventory

Status: **RESEARCH INVENTORY — non-normative, pre-Freeze**

Inventory baseline: `main@e9eb39235e45e9ad90407b803ab1c8679d348dbf`

This inventory records the current v4 repository shape before v4.1–v4.6 are canonically converged. It MUST NOT be used to refactor paths, rename states or migrate schemas before v4.7 Product/L2 Freeze.

## 1. Current top-level discoverability model

`standard-manifest.json` already provides a useful canonical inventory split into:

```text
authority
normative_standards
compatibility_entries
templates
checklists
prompts
machine_contracts
references
verification
```

It explicitly states that compatibility entry files do not duplicate normative authority.

**Finding:** v4.7 should evolve this existing manifest/inventory into an authority/discovery registry rather than invent a parallel catalog. The current manifest is primarily an asset list; it does not yet answer all of:

```text
semantic concern -> normative owner
applicability / lifecycle dimension
machine contract -> prose owner
compatibility alias -> canonical target
profile / project override resolution
minimum progressive-disclosure read set
```

## 2. Current AGENTS progressive-disclosure behavior

Root `AGENTS.md` already defines role/operation-based read routing, for example:

- VERSION + AGENTS first;
- role-specific standards;
- Development Workflow for lifecycle work;
- L2 Research Demo material only when architecture evidence applies;
- GitHub/Task/Dispatch standards only for those operations;
- Validation/Release standards for assurance/release work;
- PROJECT_OVERRIDES when present.

It also freezes several core non-inference rules:

```text
chat != fact source
PR/Review PASS != Release PASS
workflow state != Gate result
Issue hierarchy != dependency
PR stack != Issue DAG
one Validation tuple != another tuple
Builder != Independent Reviewer
```

**Finding:** v4.7 progressive disclosure should preserve/normalize this read-routing behavior rather than require every Agent to load the entire repository.

## 3. Current normative-owner families

The current manifest lists mature owner families including:

### Lifecycle / assurance
- `DEVELOPMENT_WORKFLOW.md`
- `TESTING_STANDARD.md`
- `TEST_DATA_AND_SCENARIO_STANDARD.md`
- `VALIDATION_STANDARD.md`
- `RELEASE_STANDARD.md`

### Execution / Agent coordination
- `EXECUTION_ARCHITECTURE_STANDARD.md`
- `EXECUTION_PACK_STANDARD.md`
- `GITHUB_AGENT_INTERACTION_PROTOCOL.md`
- `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`
- `LOCAL_AGENT_HANDOFF_PROTOCOL.md`
- `ISSUE_FIRST_TASK_TRIGGER.md`
- `MODEL_USAGE_POLICY.md`
- role-specific ChatGPT/Codex documents

### Repository / adoption / CI
- Repository/Project/Documentation standards
- CI Execution/Evidence/Runner Capability standards
- Project Adoption

### Compatibility aliases
- `GITHUB_WORKFLOW.md`
- `VERSION_INTEGRATION_WORKFLOW.md`

**Finding:** the repository already follows “one owner + compatibility entry/reference” in some areas, but ownership is not yet machine-discoverable by semantic concern.

## 4. State dimensions currently present

### 4.1 Work-item workflow state

`execution-state.schema.json` currently projects:

```text
planned
ready
implementing
review-ready
reviewing
changes-requested
validation-needed
merge-ready
blocked
done
```

This is a work-item/router projection, not a Validation Gate.

### 4.2 Dispatch state

Canonical Dispatch uses:

```text
READY
CLAIMED
RUNNING
COMPLETED
BLOCKED
SUPERSEDED
```

with role/profile-specific authority.

### 4.3 Execution Pack state

```text
PACK_CURRENT
PACK_STALE_NONMATERIAL
PACK_STALE_MATERIAL
PACK_INVALID
```

### 4.4 Validation state

`validation-report.schema.json` owns:

```text
PASS
FAIL
BLOCKED
NOT_RUN
NOT_APPLICABLE
```

### 4.5 Review judgment

`review-aggregation-v1.schema.json` owns:

```text
PASS
CHANGES_REQUESTED
VALIDATION_REQUESTED
BLOCKED
```

and emits only a `NON_AUTHORITATIVE_DERIVED_STATE` requested route.

### 4.6 Candidate state

Projected in `execution-state.schema.json`:

```text
PREPARED
FROZEN
THAWED
INVALIDATED
```

### 4.7 Release state

Projected in `execution-state.schema.json`:

```text
NOT_READY
READY
CONDITIONAL
BLOCKED
FAIL
```

### 4.8 Provider/execution availability

```text
AVAILABLE
INFRA_BLOCKED
TIMED_OUT
CANCELLED
```

### 4.9 Future dimensions from planned v4.4/v4.5

Expected but not yet canonical at this baseline:

- Deployment result dimension;
- Runtime/Incident dimension;
- Maintenance/Support dimension.

**Inventory conclusion:** v4.7 must normalize vocabulary **by dimension**, not collapse these into one master enum.

## 5. Required cross-state non-inference registry

The following should become explicit cross-standard conformance families:

```text
work item done != Validation PASS
PR merged != Release READY
Review PASS != Validation PASS
Validation PASS != Release READY
Release READY != Deployment SUCCESS
Deployment SUCCESS != Runtime Healthy
worktree/branch exists != Task RUNNING/claimed
Dispatch COMPLETED != product/release PASS unless result/gate owner says so
PACK_CURRENT != implementation correct
old exact-SHA PASS != successor exact-SHA PASS
provider AVAILABLE != side-effect authority
waiver/exception != PASS
fresh install PASS != upgrade PASS
mock/sandbox PASS != higher-fidelity PASS
artifact tag/filename != immutable artifact identity
incident recovered != permanent defect/follow-up closed
branch exists != maintenance-supported
```

## 6. Machine-contract inventory and convergence pressure

Current machine contracts include:

```text
agent-event-v2
assurance-plan-v1
dispatch
execution-pack-manifest
execution-state
interchange-envelope-v1
local-agent-handoff
operation-binding-v1
operation-v1
repository-integration-v4-precondition
review-aggregation-v1
review-finding-v1
task-contract
validation-report
```

### 6.1 Identity fields repeat across contracts

Observed recurring concepts:

```text
repository
version/task/issue/pr
subject_ref / subject_identity_ref
exact SHA / requested SHA / tested SHA / current PR head
expected base SHA
operator/executor/session/context refs
provider/model provenance
validation tuple/profile/environment/toolchain
state/result/judgment
```

Repeated fields are not automatically defects: each object has a different owner/claim. v4.7 should identify where a **shared identity reference convention** can replace subtly different encodings without changing evidence meaning.

### 6.2 Subject identity is already converging

`operation-v1` and `assurance-plan-v1` both use identity-binding concepts such as:

```text
exact-sha
validation-tuple
candidate
project-defined
```

Review aggregation also uses `subject_identity_ref`.

**Candidate convergence:** document a canonical Subject Identity reference vocabulary/contract or reusable schema definition, while preserving each object owner's meaning.

### 6.3 Result vocabularies must not be unified mechanically

The same string `BLOCKED` appears in workflow/provider/dispatch/Validation/Review/Release contexts with different semantics.

**Finding:** v4.7 MUST NOT deduplicate states merely because strings match. Convergence should use qualified dimensions/owner maps, e.g. `validation.state`, `review.judgment`, `dispatch.state`.

### 6.4 Review provenance already overlaps v4.6 Product research

`review-aggregation-v1` can carry provider/model family/model/executor/context/blind-first-pass provenance. `assurance-plan-v1` can require model/context/executor/evidence independence and model-diverse-adversarial modes.

**Finding:** v4.6 should extend/reference these instead of introducing duplicate AI-review/provenance schemas; v4.7 should later normalize discoverability/field naming if necessary.

### 6.5 Dispatch and Local Handoff overlap intentionally

`dispatch.schema.json` is canonical executable handoff/lifecycle identity, while `local-agent-handoff.schema.json` is an environment-specific durable handoff package/contract.

Potential convergence question for v4.7: which local-handoff fields should become references to Dispatch/Execution Pack instead of duplicated values? Do not remove redundancy until compatibility/currentness needs are understood.

## 7. Operation model inventory

`operation-v1.schema.json` already supplies a cross-lifecycle operation concept with categories such as:

```text
product-evidence
product-definition
architecture-research
architecture-definition
task-decomposition
task-materialization
implementation
integration
review
validation
coherence-review
candidate-freeze
hidden-validation
release-qualification
repository-integration
```

and kinds:

```text
PRODUCE
RESEARCH
ASSURE
DECIDE
CONTROL
```

Its `operation_binding_authority` is explicitly `CORRELATION_ONLY_NON_AUTHORITATIVE`.

**Finding:** v4.7 should assess whether later v4.1–v4.6 lifecycle domains extend this operation taxonomy additively. It MUST NOT reinterpret Operation as a universal state/authority object.

## 8. Compatibility-entry inventory

Current manifest separates compatibility entries from normative owners:

```text
standards/GITHUB_WORKFLOW.md
standards/VERSION_INTEGRATION_WORKFLOW.md
```

This is the correct migration pattern for future repository/path refactor:

```text
old stable path -> compatibility entry/alias -> canonical normative owner
```

v4.7 should inventory every path/name that downstream pinned adopters may consume before moving/renaming files. Directory aesthetics alone are not sufficient justification for breaking paths.

## 9. Repository information-architecture pressures

Current `standards/` is flat and contains lifecycle, execution, CI, roles, adoption and compatibility documents together. Flat structure has one major benefit: stable simple paths. Its pressure points are:

- growing document count;
- less obvious domain grouping;
- role/protocol/standard/compatibility entries visually mixed;
- later profile domains will add another axis;
- Agents currently depend on AGENTS/manual routing rather than a concern-to-owner registry.

**Candidate v4.7 direction:** improve discoverability first through manifest/authority map and progressive disclosure. Physical directory refactor should be evidence-driven and compatibility-preserving, not assumed mandatory.

## 10. Authority-owner inventory gaps

Current manifest identifies files as normative but does not machine-state which file owns specific concerns such as:

```text
Validation state
Review judgment
Task Pack authority
Dispatch lifecycle
Issue Dependency truth
model routing
local handoff
CI evidence publication
candidate/release truth
```

v4.7 should produce a canonical registry such as:

```text
semantic_concern
canonical_owner
machine_contract_refs
compatibility_aliases
applicability/read-routing tags
supersession/migration metadata
```

The exact format belongs to Product/L2; this inventory only establishes the need.

## 11. Future v4.1–v4.6 merge points

The convergence inventory must later incorporate, after those owners stabilize:

- v4.1 execution foundation: Git/Dependency/Config/Workspace/External System + Execution Context;
- v4.2 Interface Compatibility + Data Migration + records;
- v4.3 Architecture/Task/DAG/Implementation Quality + profiles;
- v4.4 Build/Artifact/Distribution/Deployment;
- v4.5 Observability/Incident/Maintenance;
- v4.6 Intent/Context/Skills + assurance/provenance extensions.

Do not freeze a final authority map using draft owner names that may still change.

## 12. Future-major candidate register

Potentially incompatible changes that MUST NOT be smuggled into v4.7:

- collapsing distinct state dimensions into one enum/state machine;
- replacing current dispatch/event protocol without compatibility migration;
- changing core Product/Architecture/Task authority precedence;
- deleting/moving stable normative paths without aliases/migration;
- changing exact-SHA evidence meaning;
- changing Review/Validation/Release result semantics incompatibly;
- redefining historical event/payload meanings;
- removing project ability to mark optional/non-applicable capabilities truthfully.

If evidence shows these are required, v4.7 should prepare a v5 migration plan rather than claim additive v4 compatibility.

## 13. Inventory verdict

The repository already contains the seeds of v4.7 convergence:

- `standard-manifest.json` inventory;
- root `AGENTS.md` progressive-disclosure routing;
- explicit compatibility entries;
- operation/assurance/dispatch schemas with non-authoritative correlation boundaries;
- strong state-dimension separation rules.

The primary v4.7 problem is therefore **not lack of mechanisms**. It is making semantic ownership, applicability, state dimension, machine-contract relationships and compatibility aliases deterministically discoverable and self-conformant as v4.1–v4.6 grow.

`LOCAL_ENV=NOT_REQUIRED` for this inventory. Repository-wide executable conformance/migration experiments remain blocked until v4.7 Product/L2 and stable upstream owners exist.