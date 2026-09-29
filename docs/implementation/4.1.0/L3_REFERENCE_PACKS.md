# v4.1.0 L3 Implementation Reference Packs

Status: **IMPLEMENTATION REFERENCE — bound to Frozen PRD/L2/Task DAG**

Frozen inputs:

- Product: `docs/implementation/4.1.0/PRD.md`
- L2 Freeze SHA: `043d4da7efcdd8564a2ddb6eb84860d0e1bf76fb`
- Task DAG Freeze SHA: `f930af8babaa9790b6cae8d0215fc63d2d66d4d6`
- Integration branch: `version/v4.1.0`

These references narrow implementation freedom. They do not replace the Task Pack or permit changes outside a Task's allowed write-set.

---

## T01 — Shared Execution Context & Machine Contracts

### Tests first

- Add positive/negative JSON Schema fixtures for all three new contracts.
- Prove representative historical v4 `dispatch`, `validation-report`, and Execution Pack payloads still validate.
- Reject any Execution Context fixture that carries a secret value or claims Gate/workflow authority.
- Prove optional v4.1 fields may be absent for historical/minimal payloads.

### Contract / interface

Create:

- `schemas/execution-context-v1.schema.json`;
- `schemas/dependency-toolchain-profile-v1.schema.json`;
- `schemas/dependency-risk-exception-v1.schema.json`.

Add only optional integration fields/refs to:

- `schemas/validation-report.schema.json`;
- `schemas/dispatch.schema.json`;
- `schemas/execution-pack-manifest.schema.json`.

`execution-context-v1` is a non-authoritative evidence/request projection. It MUST NOT own Task state, dispatch state, Gate state, candidate state, review result or release verdict.

`configuration.secret_refs[]` may contain reference identity/source/scope metadata only. Do not add `value`, token, password, key material, signed URL or equivalent secret-value fields.

### Core implementation

Prefer JSON Schema Draft 2020-12 consistent with current repository schemas. Keep new fields additive/optional. Use explicit `additionalProperties` boundaries inside sensitive subobjects to prevent secret-value escape hatches while allowing top-level evolution where appropriate.

### Failure handling

- If a desired field would become a new source of workflow/Gate authority: stop and report `ARCHITECTURE_CONTRADICTION` / Task Pack defect.
- If backward compatibility requires making a historical required field newly mandatory: stop; do not smuggle breaking change into v4.1.
- If secret value persistence is needed to make tests pass: implementation is wrong; keep refs only.

### References

Frozen L2 §6; existing `schemas/validation-report.schema.json`, `dispatch.schema.json`, `execution-pack-manifest.schema.json`; `scripts/test_protocol_schemas.py` and current schema verification patterns.

---

## T02 — Dependency & Toolchain Governance

### Tests first

Cover at least:

- compatibility range/floor is distinct from certification tuple;
- Agent-local runtime version cannot invent/narrow repository requirements;
- runtime vs dev/build/test dependency class survives into risk disposition;
- dependency/lock/toolchain delta triggers Validation Impact semantics;
- risk exception cannot produce `PASS` or `remediated` by itself;
- Node/npm example plus at least one non-Node ecosystem example.

### Contract / interface

Create `standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md` consuming T01 profile/exception schemas.

### Core implementation

Own manifest/lock authority, dependency classes, compatibility/supported/preferred/certification/deployment distinctions, change policy, vulnerability applicability, risk exception, provenance/registry/license/SBOM policy, EOL/abandonment and Agent behavior.

Do not prescribe one package manager command globally. Examples may show `npm ci`, Python/Rust/Java equivalents, etc., as non-normative mappings.

### Failure handling

- Scanner severity alone is insufficient to fabricate exploitability/applicability.
- Missing supported toolchain must become truthful execution `BLOCKED`, not a project requirement rewrite.
- Do not change Validation/Release state semantics; reference their owners.

### References

Issue #187; Frozen PRD §4.1; Frozen L2 §8.1; SLSA provenance as external reference pattern.

---

## T03 — Git Execution & Worktree Isolation

### Tests first

Cover at least:

- worktree/local branch existence is non-authoritative;
- two concurrent writers cannot share one writable workspace;
- exact-subject reviewer/validator checkout identity is verified;
- rewrite/rebase/force-push does not transfer old exact-SHA evidence by assertion;
- destructive clean/reset/remove requires established workspace ownership;
- cherry-pick cannot bypass Task DAG/sibling/central wiring;
- stacked PR remains code-baseline topology only;
- recovery protects unpublished work.

### Contract / interface

Create `standards/GIT_EXECUTION_STANDARD.md`; consume T01 Execution Context workspace projection without creating a workspace state machine.

### Core implementation

Define repository materialization, branch traceability, worktree/equivalent isolation, role defaults, dirty-tree policy, commit/handoff, rewrite, merge integration references, cleanup/recovery, submodule/LFS/sparse/partial clone, hooks, Git capability constraints and provenance/signing as authority-driven.

### Failure handling

Ambiguous workspace ownership must fail closed for destructive operations. Prefer a new clean/detached workspace over mutating an uncertain Builder workspace.

### References

Issue #188; Git `git-worktree` official docs; Frozen L2 §8.2; existing Validation exact-SHA/drift and GitHub execution authority.

---

## T04 — Configuration & Secrets Governance

### Tests first

Cover at least:

- deterministic precedence example and conflict resolution;
- secret ref accepted while secret value field/content is rejected from durable contract/example;
- unavailable required credential produces `BLOCKED`/not executed truth;
- short-lived/JIT example is supported but static authorized secret mechanism is not falsely prohibited;
- no `.env`/Vault/OIDC provider becomes universal authority.

### Contract / interface

Create `standards/CONFIGURATION_SECRETS_STANDARD.md`; use T01 Execution Context configuration refs.

### Core implementation

Define configuration schema/key authority, precedence, source identity/fingerprint, secret refs vs values, least privilege, redaction, authorized encrypted-in-Git exception boundary, credential availability and environment-sensitive evidence identity.

### Failure handling

Never create fake credentials, plaintext secret files, Issue comments or fixtures merely to clear a gate. Credential/config unavailability must preserve truthful non-PASS execution state.

### References

Frozen PRD §4.3; Frozen L2 §8.3; GitHub Actions OIDC and Vault-like short-lived credential mechanisms as examples, not mandatory technologies.

---

## T05 — Workspace & Artifact Governance

### Tests first

Cover at least:

- cache cannot satisfy evidence requirement;
- build output cannot become release artifact by file presence;
- runtime state is not disposable cache by default;
- unknown/unowned state cannot be destructively cleaned to get a green workspace;
- authorized promotion binds identity/provenance and owner;
- secret material classification prevents ordinary evidence/release handling.

### Contract / interface

Create `standards/WORKSPACE_ARTIFACT_STANDARD.md`; use T01 Execution Context artifact references only for material items.

### Core implementation

Define class, ownership, mutability, persistence, cleanup, Git eligibility, evidence eligibility, reconstruction and promotion authority for SOURCE, GENERATED_SOURCE, BUILD_OUTPUT, CACHE, RUNTIME_STATE, TEST_ARTIFACT, VALIDATION_EVIDENCE, RELEASE_ARTIFACT and SECRET_MATERIAL.

Do not define the future full build/package Artifact Manifest; preserve v4.4 ownership.

### Failure handling

If class/ownership is unknown, destructive cleanup is not authorized. Artifact existence never manufactures Gate/Release truth.

### References

Frozen PRD §4.4; Frozen L2 §8.4; existing CI Evidence/Validation/Release standards.

---

## T06 — External System Execution

### Tests first

Cover at least:

- mock/simulated PASS does not satisfy real-service requirement;
- sandbox PASS does not satisfy staging/production requirement;
- read-only evidence does not prove write-side-effect journey;
- tenant/account/environment identity mismatch prevents evidence substitution;
- credential/network/service/rate-limit unavailability is distinguished from product defect;
- retries/timeouts are bounded and cannot hide deterministic failure.

### Contract / interface

Create `standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md`; use T01 Execution Context external-system array with extensible dimensions.

### Core implementation

Define dependency fidelity, provider/project environment, state scope, side-effect authority, environment/account/tenant identity, credential reference and truthful infrastructure/execution failure semantics. Keep actual Gate states in `VALIDATION_STANDARD.md`.

### Failure handling

Never escalate lower-fidelity evidence, invent production authority, or execute unapproved writes. Required unavailable environment remains `BLOCKED` until authority changes or an allowed equivalent executor/environment is proven.

### References

Frozen PRD §4.5; Frozen L2 §8.5; Testcontainers real-service pattern and provider sandbox patterns.

---

## T07 — Adoption & Cross-standard Wiring

### Tests first

Add/adjust central verifier tests to prove:

- all five new standards and three schemas are discoverable from `standard-manifest.json`;
- existing standards reference the new owner rather than duplicate normative semantics;
- PROJECT_OVERRIDES has a lightweight Execution Foundation Profile;
- optional profiles remain optional for minimal/Fast-Path fixtures;
- project-init/review/closure checklists surface only applicable facts;
- old v4 adoption examples remain non-weakened.

### Contract / interface

Central convergence surfaces owned only here:

- `standard-manifest.json`;
- `templates/project/.dev-standard/PROJECT_OVERRIDES.md`;
- selected `DEVELOPMENT_WORKFLOW`, CI/Testing/Validation/Release references;
- relevant checklists;
- migration/adoption/index documentation.

### Core implementation

Wire by reference. Do not paste the full Dependency/Git/Config/Artifact/External standards into existing documents. Preserve one normative owner per semantic concern.

### Failure handling

If two standards end up making contradictory MUST-level claims about the same semantic, stop and resolve owner precedence before merge. Do not “solve” it with duplicated wording.

### References

Frozen L2 §§7,9,11; `standard-manifest.json`; `PROJECT_OVERRIDES.md`; current workflow/adoption standards.

---

## T08 — Conformance, Dogfood & Closure Inputs

### Tests first

Build the dependency-complete matrix from Frozen PRD §10–§11 and Frozen L2 §10. Include positive + adversarial negative fixtures.

### Contract / interface

Own central v4.1 regression/golden/dogfood evidence; do not redefine T01–T07 production contracts.

### Core implementation

At minimum prove:

- backward compatibility of representative v4 payloads;
- no Execution Context authority escalation;
- dependency/toolchain truth + risk exception behavior;
- secret refs only;
- workspace isolation/recovery semantics;
- artifact class/promotion semantics;
- external fidelity/side-effect non-escalation;
- minimal/Fast-Path positive path;
- Node/npm + non-Node example;
- multi-Agent isolated workspace/durable handoff/recovery scenario;
- provider sandbox/real dependency scenario.

Produce closure inputs/evidence index without declaring Release READY.

### Failure handling

A failing Product acceptance scenario is a real v4.1 defect. Do not weaken fixtures or mark required behavior `NOT_APPLICABLE` to obtain green state.

### References

Frozen PRD §§10–11; Frozen L2 §10; existing golden/conformance and self-dogfood patterns under `templates/golden/**` and `docs/implementation/4.0.0/**`.
