# Task DAG — ai-development-standard v4.1.0

Status: **FROZEN PLANNING DAG — 2026-09-29**

## Frozen Inputs

- PRD: `docs/implementation/4.1.0/PRD.md`
- Frozen L2: `docs/implementation/4.1.0/L2_ARCHITECTURE_EVIDENCE.md`
- L2 Freeze SHA: `043d4da7efcdd8564a2ddb6eb84860d0e1bf76fb`
- Version baseline: `e9eb39235e45e9ad90407b803ab1c8679d348dbf`
- Integration branch: `version/v4.1.0`
- Pinned standard at planning baseline: `4.0.0`

## Decomposition rationale

The Frozen L2 establishes one shared Execution Foundation with five separate normative owners. The safest high-throughput decomposition is therefore:

```text
T01 shared machine contracts
        ↓
 ┌──────┼────────┬────────┬────────┐
 ▼      ▼        ▼        ▼        ▼
T02    T03      T04      T05      T06
Deps   Git      Config   Workspace External
Tool   Exec     Secrets  Artifact  Systems
 └──────┴────────┴────────┴────────┘
                 ↓
               T07
       central adoption / wiring
                 ↓
               T08
      conformance + dogfood hardening
                 ↓
      Version Closure / Release Qualification
```

This provides maximum safe parallelism after T01 while preventing parallel Tasks from racing on shared convergence surfaces.

## Planning DAG

| Task | Execution Issue | Lane | Depends On | Parallel | Risk | Input / Reference | Primary Output | Acceptance summary | Model / executor suitability | Required Validation | Review Policy | Code Baseline | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T01 | `PENDING_MATERIALIZATION` | shared-contract | — | NO | HIGH | Frozen PRD/L2 | 3 new schemas + additive optional refs in existing schemas + focused schema tests | v4 payloads remain valid; no Gate/workflow authority in context; no secret values | high-capability for contract implementation; low-cost allowed only with L3 + review | schema tests + backward-compat fixtures | required | independent | TODO |
| T02 | `PENDING_MATERIALIZATION` | dependency-toolchain | T01 | YES | HIGH | #187 + Frozen PRD/L2 + T01 schemas | `DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md` + focused examples/tests | compatibility != certification; class/exposure/risk exception semantics; ecosystem-neutral | bounded implementation with L3 | focused verifier/schema/example checks | required | independent | TODO |
| T03 | `PENDING_MATERIALIZATION` | git-execution | T01 | YES | HIGH | #188 + Frozen PRD/L2 + T01 context | `GIT_EXECUTION_STANDARD.md` + focused examples/tests | isolated writable workspaces; non-authoritative local state; safe rewrite/destructive/recovery semantics | bounded implementation with L3 | focused semantic/regression checks | required | independent | TODO |
| T04 | `PENDING_MATERIALIZATION` | config-secrets | T01 | YES | HIGH | Frozen PRD/L2 + T01 context | `CONFIGURATION_SECRETS_STANDARD.md` + focused examples/tests | deterministic precedence; ref/value split; least privilege; no durable secret values; truthful BLOCKED | security-sensitive; high capability preferred | secret-leak negative + precedence examples | required | independent | TODO |
| T05 | `PENDING_MATERIALIZATION` | workspace-artifact | T01 | YES | HIGH | Frozen PRD/L2 + T01 context | `WORKSPACE_ARTIFACT_STANDARD.md` + focused examples/tests | class/ownership/lifecycle/promotion truth; cache/output cannot imply evidence/release | bounded implementation with L3 | class/promotion/cleanup negatives | required | independent | TODO |
| T06 | `PENDING_MATERIALIZATION` | external-systems | T01 | YES | HIGH | Frozen PRD/L2 + T01 context | `EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` + focused examples/tests | fidelity dimensions; side-effect authority; lower-fidelity PASS non-escalation; infrastructure truth | security/side-effect sensitive; high capability preferred | fidelity/authority negative cases | required | independent | TODO |
| T07 | `PENDING_MATERIALIZATION` | convergence-adoption | T02,T03,T04,T05,T06 | NO | HIGH | five normative standards | shared references, `PROJECT_OVERRIDES`, workflow/checklist/manifest/schema registry/adoption wiring | one owner per semantic concern; no duplicated authority; Fast Path remains lightweight | high capability integration owner | cross-standard verifier + template checks | required | independent | TODO |
| T08 | `PENDING_MATERIALIZATION` | assurance-dogfood | T07 | NO | HIGH | dependency-complete v4.1 integration | central regression/golden examples/self-dogfood evidence and closure inputs | all Product negative cases + minimal project + Node/non-Node + multi-Agent + external fidelity scenarios pass | high capability verifier/reviewer; low-cost fixture generation allowed | full repository verifier/regression + exact-SHA evidence | required | independent | TODO |

Planning status values: `TODO / DOING / BLOCKED / DONE / DEFERRED / NOT_APPLICABLE`.

## Task details

### T01 — Shared Execution Context & Machine Contracts

Owns shared contract surfaces only.

Outputs:

- `schemas/execution-context-v1.schema.json`;
- `schemas/dependency-toolchain-profile-v1.schema.json`;
- `schemas/dependency-risk-exception-v1.schema.json`;
- additive optional integration in `validation-report.schema.json`, `dispatch.schema.json`, and `execution-pack-manifest.schema.json`;
- focused schema/backward-compatibility tests.

Hard boundary:

- MUST NOT define workflow/Gate/Release state;
- MUST NOT include secret-value fields;
- MUST NOT implement any of T02–T06 normative standards beyond contract semantics required by Frozen L2.

### T02 — Dependency & Toolchain Governance

Consumes Issue #187 as detailed Product/research input. Owns the new dependency/toolchain normative standard and concern-local examples/tests. Shared project templates/manifest/checklists are reserved for T07.

### T03 — Git Execution & Worktree Isolation

Consumes Issue #188 as detailed Product/research input. Owns the new Git execution standard and concern-local examples/tests. It MUST preserve GitHub Issue/dispatch authority and Validation exact-SHA/drift ownership.

### T04 — Configuration & Secrets Governance

Owns configuration precedence, secret references/value boundaries, least privilege, credential availability and durable redaction semantics. It MUST NOT mandate one secret manager or dynamic-secret mechanism.

### T05 — Workspace & Artifact Governance

Owns SOURCE/GENERATED_SOURCE/BUILD_OUTPUT/CACHE/RUNTIME_STATE/TEST_ARTIFACT/VALIDATION_EVIDENCE/RELEASE_ARTIFACT/SECRET_MATERIAL classification semantics, ownership, cleanup and promotion boundaries. Full build/package Artifact Manifest remains out of scope for v4.1/v4.4-owned.

### T06 — External System Execution

Owns external dependency fidelity, provider/project environment identity, state scope, side-effect authority and infrastructure failure truth. It MUST use existing Testing/Validation Gate semantics rather than create new PASS/FAIL states.

### T07 — Adoption & Cross-standard Wiring

Central convergence owner. Only T07 should make the broad shared edits needed to connect T01–T06 into:

- `standard-manifest.json`;
- `templates/project/.dev-standard/PROJECT_OVERRIDES.md`;
- relevant workflow/CI/testing/validation/release reference points;
- project-init / PR review / version closure checklists where applicable;
- migration/adoption documentation and central index/README references.

T07 MUST reference new owners instead of copying normative content into existing standards.

### T08 — Conformance, Dogfood & Closure Inputs

Owns dependency-complete regression/negative scenarios and v4.1 Product acceptance proof. Must cover at least:

- historical v4 payload backward compatibility;
- Execution Context does not become authority;
- invented/narrowed toolchain requirement rejection;
- compatibility vs certification distinction;
- risk exception != PASS/remediation;
- durable secret-value rejection;
- shared writable workspace/destructive unknown ownership rejection;
- cache/build output != evidence/release artifact;
- lower-fidelity external PASS non-escalation;
- minimal/Fast-Path positive adoption;
- Node/npm + at least one non-Node dependency/toolchain example;
- multi-Agent isolated workspace + durable handoff/recovery example;
- provider sandbox/real-dependency fidelity example.

T08 produces closure inputs; Version Closure / Release Qualification remains version-level authority and is not redefined as a leaf Task.

## Lane Summary

| Lane | Tasks | Entry prerequisites | Shared write-set / authority constraints | Converges at |
|---|---|---|---|---|
| shared-contract | T01 | Frozen L2 | sole owner of new shared schemas and optional existing-schema integration | T02–T06 |
| dependency-toolchain | T02 | T01 DONE | no central manifest/template/checklist edits | T07 |
| git-execution | T03 | T01 DONE | no central manifest/template/checklist edits | T07 |
| config-secrets | T04 | T01 DONE | no central manifest/template/checklist edits | T07 |
| workspace-artifact | T05 | T01 DONE | no central manifest/template/checklist edits | T07 |
| external-systems | T06 | T01 DONE | no central manifest/template/checklist edits | T07 |
| convergence-adoption | T07 | T02–T06 DONE | owns shared convergence surfaces | T08 |
| assurance-dogfood | T08 | T07 DONE | owns central regression/golden/dogfood proof | Closure |

## Review Policy Planning

All eight implementation Tasks are `review:required` because this release changes public normative standards and/or shared machine contracts, or owns security/destructive/side-effect/high-blast-radius semantics.

This is a risk-based result for v4.1.0, not a change to the global rule that every project/task always requires Independent Review.

## Validation ownership

- T01–T06: `concern` validation only.
- T07: `integration` validation for cross-standard wiring.
- T08: dependency-complete integration/conformance evidence and closure preparation; it does not declare Release READY.
- Version Closure owns full regression/Release Qualification/repository integration under existing authority.

## L3 requirement

T01–T08 each require a bounded L3 Reference Pack because:

- all are high-risk normative/shared-contract changes;
- several are suitable for lower-cost bounded execution only when implementation references are explicit;
- L3 prevents concern lanes from guessing central wiring or authority semantics.

Each L3 must follow the priority:

```text
Tests → Contract/Interface → Core Implementation → Failure Handling → References
```

## Code baseline strategy

All Tasks are `independent` JIT branches relative to the current `version/v4.1.0` integration branch after dependencies merge. No stacked PR is planned.

T02–T06 become simultaneously ready only after T01 has merged into `version/v4.1.0`. Their branches MUST be created JIT from that then-current integration SHA.

## Execution DAG materialization

This file is the Frozen planning/history DAG. After this checkpoint:

1. create bounded Task Packs + required L3 References;
2. create one Task Issue per T01–T08;
3. assign canonical metadata / Review Policy;
4. materialize GitHub Issue Dependencies matching this DAG;
5. use Issue Dependencies as the canonical live execution DAG;
6. create implementation branches only JIT when a Task enters the ready set.

The Issue column intentionally says `PENDING_MATERIALIZATION` at Freeze time because execution Issues do not become canonical until after the planning DAG is Frozen. The materialization map must be recorded separately without rewriting the frozen decomposition.

## Companion standard-gap disposition — Issue #190

Issue #190 is a real standards-self process gap discovered by L1, but it is **not part of the Frozen v4.1 Agent Execution Foundation Product scope** and is not an execution dependency of T01–T08.

Disposition:

- remain a separately tracked maintenance/process-hardening Issue;
- may proceed independently when it cannot destabilize the v4.1 integration baseline;
- MUST NOT be silently folded into a T01–T08 PR;
- if implemented during the v4.1 timeline and merged to main, its impact on the version branch must be handled explicitly rather than cherry-picked ad hoc.

## Freeze decision

The decomposition is Frozen because:

- all implementation concerns trace to Frozen Product/L2 authority;
- shared mutable surfaces have explicit owners;
- safe parallelism is maximized without overlapping central wiring;
- Task-level vs integration vs closure validation ownership is explicit;
- Review Policy is explicit;
- no Task requires an unresolved Architecture UNKNOWN or research spike;
- the standard-self gap #190 is tracked without scope smuggling.

**Freeze decision: FROZEN — proceed to Task Pack/L3/Issue materialization.**
