# v4.1.0 L2 Architecture Evidence — Agent Execution Foundation

Status: **L2 FREEZE CANDIDATE — Architecture UNKNOWNs dispositioned**

Research date: 2026-09-29

## 1. Frozen inputs

- Frozen PRD: `docs/implementation/4.1.0/PRD.md`
- Product Freeze commit before integration: `b43dcae197976322a78659ce464c5c73152f46b8`
- Product planning merge / version baseline: `e9eb39235e45e9ad90407b803ab1c8679d348dbf`
- L1: `docs/implementation/4.1.0/L1_PRODUCT_EVIDENCE.md`
- pinned standard at baseline: `4.0.0`
- Issue #187 — Dependency & Toolchain Governance
- Issue #188 — Git Execution & Worktree Isolation
- Issue #190 — non-blocking standards-self L1 process gap

Architecture research follows `prompts/L2_ARCHITECTURE_EVIDENCE.md` and the v4 `DEVELOPMENT_WORKFLOW`: identify drivers/invariants/UNKNOWNs, prefer static/source evidence when sufficient, require Research Demo only for material architecture assumptions whose behavior cannot be established without executable evidence.

## 2. Architecture recommendation

Use a **composed execution-foundation architecture**:

```text
Frozen Task / Dispatch / existing v4 authority
                │
                ▼
      Stable execution requirements
                │
      ┌─────────┼─────────┐
      ▼         ▼         ▼
 Dependency   Git      Config / Secret
 Toolchain   Workspace      Contract
      │         │         │
      └──────┬──┴──────┬──┘
             ▼         ▼
       Workspace /   External
       Artifact       System
       semantics      Contract
             │         │
             └────┬────┘
                  ▼
       Execution Context projection
        (NON-AUTHORITATIVE context)
                  │
                  ▼
 Existing Test / Review / Validation / CI / Release authority
```

Architecture decisions:

1. **Five normative owners, one composed context.** Each concern gets one standard; cross-concern composition uses an optional `Execution Context` projection/reference model.
2. **Execution Context does not own lifecycle or Gate state.** It records/requests facts needed to reconstruct execution; canonical claim/dispatch/workflow/Validation/Release truth remains in existing v4 owners.
3. **Additive machine contracts only.** v4.1 introduces a minimal set of optional schemas and optional references/fields. Existing v4 machine contracts remain valid.
4. **No durable canonical Git workspace state machine.** Worktree/clone/sandbox state is an execution observation. Durable recording is required only when needed for handoff/recovery/evidence; Task/dispatch authority remains on GitHub/v4 records.
5. **No full build/package Artifact Manifest in v4.1.** v4.1 owns classification, identity/promotion boundaries and cleanup safety. v4.4 remains the natural owner for complete build/package/distribution artifact contracts.
6. **External-system fidelity is dimensional, not one closed universal enum.** The standard freezes distinctions and non-escalation rules; provider/project mappings remain extensible.
7. **Secrets are references in durable contracts.** Values are injected/resolved only through authorized execution mechanisms and are never part of ordinary Execution Context evidence.
8. **Fast Path is capability/risk driven.** Optional machine contracts are used when the concern is material; prose/project-owned facts remain conformant for simple projects.

## 3. Architecture drivers

### D1 — Preserve v4 authority ownership

The strongest constraint is non-duplication. v4.0 already owns:

- Task/claim/dispatch/workflow state;
- GitHub durable coordination;
- test type/ownership semantics;
- Validation Gate states and exact-SHA tuple truth;
- CI execution/evidence;
- Candidate/Release/Repository Integration.

v4.1 must make real execution safer without creating parallel sources of truth.

### D2 — Reconstruct actual execution, not idealized configuration

A declared requirement and an observed execution are different facts. The architecture must permit:

```text
required compatibility/toolchain/profile
!=
actual executor/toolchain/dependency/config/external environment
```

Evidence must bind to what actually executed.

### D3 — Progressive adoption / Fast Path

A docs-only or low-risk repository cannot be forced to materialize six manifests for no semantic benefit. Machine contracts must be optional based on materiality while truth/authority rules remain mandatory.

### D4 — Multi-Agent concurrency and recovery

Concurrent writable execution needs isolation and ownership. OpenAI's published agent-first harness experience describes booting an isolated application/observability instance per Git worktree, while Git itself supports multiple linked working trees. These are strong pattern evidence for isolated execution surfaces without making the surface itself workflow authority.

References:

- https://openai.com/index/harness-engineering/
- https://git-scm.com/docs/git-worktree

### D5 — Supply-chain and dependency identity can affect evidence validity

SLSA provenance models build definition, run details, subjects and resolved dependencies as distinct provenance facts. v4.1 needs enough dependency/toolchain identity to drive Validation Impact, without taking over build provenance/release authority.

Reference: https://slsa.dev/spec/v1.1/provenance

### D6 — Credential mechanisms vary

GitHub Actions OIDC proves short-lived federated credentials are practical and useful, but it is explicitly provider/integration dependent. Architecture must allow OIDC/Vault/JIT/static authorized mechanisms while keeping durable secret values out of source/evidence.

Reference: https://docs.github.com/en/actions/concepts/security/openid-connect

### D7 — Real service fidelity differs from mocks/simulations

Testcontainers deliberately runs real service implementations instead of mocks/in-memory substitutes; provider sandboxes have still different fidelity/side-effect semantics. External-system architecture must preserve those distinctions without claiming a provider-neutral closed lifecycle.

Reference: https://testcontainers.com/guides/introducing-testcontainers/

## 4. Current-state findings

### 4.1 Existing schemas are intentionally extension-tolerant

At the version baseline:

- `schemas/validation-report.schema.json` has `additionalProperties: true`;
- `schemas/dispatch.schema.json` has `additionalProperties: true`;
- `schemas/execution-pack-manifest.schema.json` has `additionalProperties: true`.

Therefore new optional references/objects can be introduced without making historical valid v4 payloads invalid under the schema. v4.1 verifiers may begin checking the new fields when present/applicable.

### 4.2 Validation already owns environment/toolchain tuple truth

`VALIDATION_STANDARD.md` already defines:

```text
<exact tested SHA>
× <real platform/environment>
× <runtime/toolchain>
× <validation profile>
```

and Gate states `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`.

v4.1 must not create another result state model. It supplies richer execution facts used to interpret/compose that existing tuple.

### 4.3 Project overrides already provide a progressive-adoption surface

`templates/project/.dev-standard/PROJECT_OVERRIDES.md` already holds repository profile, CI execution model, validation environments, runtime/platform requirements, required services and command truth. v4.1 should extend this surface with optional execution-foundation declarations rather than require a new mandatory project manifest for every repository.

### 4.4 Execution Pack is the correct JIT execution-requirement handoff surface

The existing Execution Pack is subordinate to the stable Task Pack and binds exact baseline, branch and pinned standard. It is the appropriate place to carry a reference to material execution-context requirements at dispatch time; it must not become Product/Architecture authority.

## 5. Architecture UNKNOWNs and disposition

| ID | UNKNOWN | Impact | Disposition | Evidence / decision |
|---|---|---|---|---|
| U1 | Do we need a new authoritative Execution Context state machine? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Existing v4 owns state/Gates; Product requires context reconstruction, not new authority. Use non-authoritative projection/reference. |
| U2 | Can existing v4 schemas be extended compatibly? | High | `STATIC_EVIDENCE_SUFFICIENT` | Core target schemas use `additionalProperties: true`; new fields remain optional. Historical payloads stay valid. |
| U3 | Should Git workspace state be a canonical durable record? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Local workspace is explicitly non-authoritative. Record binding/observations only when material to execution/recovery/evidence. |
| U4 | Must v4.1 define a complete Artifact Manifest? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. v4.1 needs classes + identity/promotion rules; v4.4 owns build/package/deployment convergence. |
| U5 | Can external environments use one closed six-value enum? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Provider semantics differ. Freeze dimensions + recommended mappings; allow extension. |
| U6 | Must all secret access use JIT/dynamic credentials? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Prefer short-lived/federated where supported; mandatory rules are ref/value separation, authority, least privilege, non-leakage, truthful BLOCKED. |
| U7 | Which new machine contracts have enough value for v4.1? | High | `STATIC_EVIDENCE_SUFFICIENT` | Three: optional execution-context projection, dependency/toolchain profile, dependency-risk exception. Other concerns use standards + optional context sections/project overrides. |
| U8 | Do we need executable Research Demos before L2 Freeze? | High | `STATIC_EVIDENCE_SUFFICIENT` | No material runtime algorithm/protocol behavior is unresolved; changes are standards/schemas with deterministic verifier coverage. Executable conformance belongs to implementation Tasks, not architecture spike. |
| U9 | How do we prevent optional context metadata from becoming a mandatory bureaucracy? | High | `STATIC_EVIDENCE_SUFFICIENT` | applicability/materiality rules + minimal example + verifier negatives that forbid requiring absent non-applicable profiles. |
| U10 | How do v4.1 context fields interact with historical evidence? | High | `STATIC_EVIDENCE_SUFFICIENT` | additive successor metadata only; never retrofit historical PASS as if context was captured. |

**Research Demo decision: NOT REQUIRED before L2 Freeze.**

No UNKNOWN requires proving a new runtime component, distributed algorithm, durability behavior or external integration implementation. The architectural claims are about authority ownership, schema compatibility and standard composition; repository source plus official mechanism evidence is sufficient. Implementation Tasks must still provide executable schema/verifier/conformance regression evidence.

## 6. Machine contract architecture

### 6.1 New: `schemas/execution-context-v1.schema.json`

Purpose: optional non-authoritative context projection for requested/observed execution facts.

Proposed top-level shape:

```yaml
schema_version: 1
subject:
  repository:
  sha:
source_workspace:
  kind:                 # worktree | clone | sandbox | ci-checkout | other
  workspace_id:         # non-secret opaque/local identity when useful
  branch_ref:
  materialization:      # full | sparse | partial | submodule/lfs facts when material
dependency_toolchain:
  profile_ref:
  manifest_refs: []
  lock_refs: []
  observed_runtime_toolchain:
configuration:
  profile_ref:
  non_secret_fingerprint:
  secret_refs: []       # identity/ref only; never values
artifacts:
  relevant: []          # class + identity/ref; not full v4.4 manifest
external_systems:
  - system_id:
    dependency_fidelity:
    environment_class:
    environment_ref:
    side_effect_authority:
    credential_ref:
executor:
  host_role:
  environment_ref:
```

Normative properties:

- no Gate/workflow/result state fields;
- no secret value field;
- optional sections, populated only when material;
- observed context can differ from requested profile and evidence must preserve that truth;
- identifiers/fingerprints are evidence aids, not authority by themselves.

Integration:

- `validation-report.schema.json`: add optional `execution_context` or `execution_context_ref`;
- `dispatch.schema.json`: add optional `execution_context_requirements_ref` only, not observed facts;
- `execution-pack-manifest.schema.json`: add optional `execution_context_requirements_ref` / material profile refs.

### 6.2 New: `schemas/dependency-toolchain-profile-v1.schema.json`

Purpose: optional durable repository/project contract for material dependency/toolchain facts.

Must distinguish:

```text
manifest / lock authority
package/dependency classes
compatibility floor/range
supported release lines
preferred development line/version
certification tuple(s)
deployment/runtime identity when applicable
package source/registry/provenance policy when applicable
```

It MUST NOT assert that certification of one version proves the whole compatibility range.

### 6.3 New: `schemas/dependency-risk-exception-v1.schema.json`

Purpose: durable exception record that makes deferred dependency risk visible without rewriting Gate truth.

Required semantics:

```text
advisory identity
affected package/version + dependency class/path
exposure/applicability
severity
reason deferred
mitigation when applicable
authority/owner
created_at
expiry/review date
release scope/version
status/disposition
```

An exception is evidence of accepted/deferred risk, **not PASS** and not proof of remediation.

### 6.4 No v4.1 standalone schemas for these concerns

**Git Workspace Record:** no canonical durable record. Use Execution Context source/workspace section plus existing dispatch/handoff/evidence when material.

**Configuration Profile:** project overrides + normative standard own precedence/secret-ref behavior; Execution Context may carry a profile ref/fingerprint. A separate schema can be added later only if real cross-project machine exchange justifies it.

**Artifact Manifest:** deferred to v4.4. v4.1 uses class + identity/ref semantics only.

**External System Profile:** project/Task/Execution Pack requirements + Execution Context array are sufficient for v4.1. Avoid premature provider taxonomy lock-in.

This is intentionally a **minimum viable machine-contract set**.

## 7. Normative owner map

| Semantic concern | v4.1 owner | Must reference / must not duplicate |
|---|---|---|
| dependency/toolchain contract, dependency risk exception | `DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md` | Validation Impact, CI execution, Release gates |
| Git repository/workspace execution safety | `GIT_EXECUTION_STANDARD.md` | GitHub claim/dispatch, Validation exact-SHA/drift, Release integration |
| configuration + secret consumption | `CONFIGURATION_SECRETS_STANDARD.md` | project override authority, CI secret mechanism, external system authorization |
| filesystem/workspace/artifact classes | `WORKSPACE_ARTIFACT_STANDARD.md` | CI evidence, Validation evidence, Release artifact authority, future v4.4 packaging |
| external system fidelity/side effects | `EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` | Testing, Validation tuple/state, Release requirements |
| cross-concern context composition | lightweight sections in the five standards + `execution-context-v1` | no lifecycle/Gate authority |

## 8. Detailed concern architecture

### 8.1 Dependency & Toolchain

Contract layers:

```text
Declared compatibility
      !=
Preferred development environment
      !=
Certification environment(s)
      !=
Deployment/runtime immutable identity
```

Dependency graph identity should be derived from repository-owned manifests/lockfiles/resolution sources; v4.1 does not invent a universal hash algorithm. Projects MAY record content digests where useful.

Risk flow:

```text
scanner/advisory evidence
→ dependency class/path + runtime exposure/applicability
→ remediation OR explicit risk exception
→ existing Validation/Release authority consumes the disposition
```

### 8.2 Git execution

Execution binding:

```text
Durable Task/Dispatch
→ authorized repository + expected base/subject
→ isolated writable workspace OR detached/read-only exact-subject workspace
→ actual HEAD/materialization verification
→ execution
→ durable handoff/evidence
```

Workspace observations such as `ACTIVE`, `DIRTY`, `HEAD_DRIFT`, `ORPHANED`, `SAFE_TO_PRUNE` are local/derived observations, not workflow states.

Destructive operations fail closed when ownership is ambiguous.

### 8.3 Configuration & Secrets

Separate:

```text
configuration key/schema
configuration source/precedence
non-secret value/fingerprint
secret reference/identity
secret value (execution-only; prohibited from ordinary durable evidence)
```

Precedence is project-owned and deterministic. The standard provides ordering rules/requirements but does not assume `.env` is canonical.

Credential unavailability maps to truthful execution/Validation `BLOCKED` when a required gate cannot run; Agents do not manufacture credentials or substitute a lower-fidelity environment without authority.

### 8.4 Workspace & Artifact

Class model:

```text
SOURCE
GENERATED_SOURCE
BUILD_OUTPUT
CACHE
RUNTIME_STATE
TEST_ARTIFACT
VALIDATION_EVIDENCE
RELEASE_ARTIFACT
SECRET_MATERIAL
```

Key architecture distinction:

```text
class
+ ownership
+ lifecycle/cleanup
+ identity
+ promotion authority
```

A path alone does not define authority. The same physical storage mechanism may hold different classes.

Promotion examples:

```text
BUILD_OUTPUT --authorized build/release binding--> RELEASE_ARTIFACT
TEST_ARTIFACT --evidence publication rules--> VALIDATION_EVIDENCE (when applicable)
```

Promotion never occurs by file existence alone.

### 8.5 External systems

Use orthogonal dimensions rather than one overloaded enum:

```text
dependency fidelity: test-double | simulated | real
provider/project environment: sandbox | staging | production | project/provider-specific
state scope: ephemeral/isolated | shared/persistent | project-specific
side-effect authority: none | read-only | bounded-write | production-write | project-specific
environment/account/tenant identity: explicit when material
credential scope/reference: explicit when material
```

Canonical labels are guidance/mapping values; projects/providers MAY extend them if semantics remain explicit.

PASS non-escalation is mandatory:

```text
mock PASS          !=> real-service PASS
sandbox PASS       !=> staging PASS
staging PASS       !=> production PASS
read-only PASS     !=> write-side-effect PASS
one account/tenant !=> another account/tenant
```

## 9. Compatibility / migration architecture

v4.1 is additive:

- historical v4 payloads remain valid;
- new schemas are optional capability contracts;
- new fields added to existing tolerant schemas are optional;
- no new required state/result values are added to existing v4 lifecycle/Gate enums;
- projects adopt profiles when material and can remain on prose/project-override facts for non-applicable capabilities;
- new v4.1 evidence may carry richer context, but old evidence is not retroactively enriched;
- any future need to require incompatible fields/authority transitions is a future-major input.

## 10. Verification architecture

Implementation should use deterministic repository verifier/regression coverage rather than an architecture demo.

Required test families:

1. schema positive/negative tests for the three new machine contracts;
2. backward compatibility: historical representative v4 dispatch/validation payloads still validate;
3. authority negatives: Execution Context cannot become Gate/workflow authority;
4. dependency/toolchain negatives: Agent-invented constraint and certification!=compatibility cases;
5. secret leakage negatives: durable context/profile has refs only, no value field;
6. workspace negatives: shared writable workspace/destructive unknown ownership is non-conformant;
7. artifact negatives: cache/build output cannot imply evidence/release artifact state;
8. external fidelity negatives: lower-fidelity PASS cannot satisfy higher-fidelity requirement;
9. Fast Path/minimal project positive: optional profiles absent when immaterial remains conformant;
10. language neutrality: Node/npm + at least one Python/Rust/Java-style example.

## 11. Adoption architecture

Extend `PROJECT_OVERRIDES.md` with an **Execution Foundation Profile** containing only applicable facts/references, for example:

```text
Dependency/toolchain profile: <ref | repository-owned prose fields | NOT_APPLICABLE reason>
Git workspace isolation: <worktree | isolated clone | sandbox | CI checkout | project-specific>
Configuration precedence: <project rule/ref>
Secret mechanism: <OIDC/Vault/provider/static authorized/local ref | project-specific | NOT_APPLICABLE>
Workspace/artifact classification: <canonical | project extension/ref>
External systems: <systems + fidelity/environment/side-effect authority refs>
Execution Context machine record: <enabled | disabled/NOT_APPLICABLE reason>
```

This is not a declaration that every Task must populate every item.

## 12. Task DAG lane hints

After L2 Freeze, safe parallel lanes are available because the five standards have distinct owner files.

Suggested decomposition:

```text
T01 shared machine contracts / cross-standard semantics
        ↓
 ┌──────┼────────┬────────┬────────┐
 ▼      ▼        ▼        ▼        ▼
T02    T03      T04      T05      T06
Deps   Git      Config   Workspace External
Tool   Exec     Secrets  Artifact  Systems
 └──────┴────────┴────────┴────────┘
                 ↓
               T07
      adoption + cross-standard wiring
                 ↓
               T08
     conformance + dogfood hardening
                 ↓
               T09
       version closure preparation
```

Parallelism constraints:

- T02–T06 must not concurrently edit shared `standard-manifest.json`, shared project template, common verification registry or central cross-standard docs; T07 owns those convergence surfaces.
- T01 owns shared/new schemas and the execution-context semantic contract; later lanes consume but do not redefine them.
- T08 owns central regression/conformance examples; concern lanes may add focused tests only in their explicitly allocated files.
- Full release qualification/closure remains a later version gate, not leaf Task acceptance.

## 13. Architecture risks / escape hatches

### R1 — Execution Context grows into a second state machine

Mitigation: schema forbids lifecycle/Gate ownership; standards explicitly point to existing owners; regression negatives.

### R2 — Optional profiles become mandatory bureaucracy

Mitigation: materiality/applicability language; Fast Path positive fixture; no universal requirement to instantiate all schemas.

### R3 — Artifact semantics collide with v4.4

Mitigation: v4.1 owns class/identity/promotion boundary only; full packaging/build artifact manifest deferred.

### R4 — Provider environment labels become misleading

Mitigation: orthogonal dimensions + extensible mappings; never infer higher fidelity.

### R5 — Security policy becomes scanner-driven rather than exposure-driven

Mitigation: advisory evidence must include dependency class/path and applicability; exception does not rewrite PASS.

### R6 — Workspace isolation is implemented as Git-specific lock-in

Mitigation: normative contract says isolated worktree **or equivalent isolated clone/sandbox/workspace**; Git worktree is the default/reference mechanism, not mandatory technology.

## 14. Architecture contradictions

**None found.**

No Frozen Product requirement is technically contradictory with the existing v4 architecture. The recommended design remains additive and non-weakening.

## 15. L2 Freeze readiness

All identified high-impact Architecture UNKNOWNs have an explicit disposition. No Research Demo is required before Freeze because static repository/schema/official mechanism evidence is sufficient for the architecture decisions.

Freeze candidate decisions to preserve:

- five normative owners + one non-authoritative Execution Context projection;
- exactly three new v4.1 machine-contract families by default: Execution Context, Dependency/Toolchain Profile, Dependency Risk Exception;
- additive optional integration with existing dispatch/Execution Pack/Validation schemas;
- no canonical Git workspace workflow state;
- no full artifact manifest before v4.4;
- dimensional/extensible external-system fidelity model;
- secrets durable by reference only;
- optional/materiality-driven Fast Path adoption;
- deterministic verifier/conformance implementation instead of an architecture Research Demo.

**Candidate verdict: READY FOR EXPLICIT L2 FREEZE.**
