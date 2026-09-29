# ai-development-standard v4.1.0 PRD — Agent Execution Foundation

Status: **DRAFT PRODUCT AUTHORITY — requires L1 Product Evidence review and explicit PRD Freeze before implementation**

## 1. Product intent

v4.1.0 establishes the execution-foundation layer required for reliable AI-native development. v4.0 already defines lifecycle, execution architecture, GitHub-native coordination, testing, validation and release authority, but real Agent execution still depends on under-specified repository/toolchain/configuration/workspace/external-system behavior.

The product goal is to make an authorized Human or Agent able to answer, from durable repository/GitHub facts rather than chat or local assumptions:

1. What source/workspace may I operate on?
2. What dependencies and toolchains are supported and actually certified?
3. What configuration and secrets may I consume, and from where?
4. What filesystem outputs are source, cache, runtime state, evidence, or release artifacts?
5. Which external systems may I access, at what environment class and with what side-effect authority?
6. What conditions are execution/environment BLOCKED rather than product FAIL?

## 2. Problem

Current v4 contains distributed guidance for lockfiles, clean checkouts, exact-SHA validation, external-boundary testing and project overrides, but does not define one coherent execution foundation. This allows Agents to make locally reasonable but globally inconsistent decisions, including:

- inventing or silently strengthening Node/Python/JDK/Git requirements;
- sharing writable Git workspaces across concurrent Agents;
- treating a local branch/worktree as workflow authority;
- using stale or mutable dependency graphs without explicit validation impact;
- creating `.env` or fake credentials merely to make execution succeed;
- deleting unknown caches/runtime data to obtain a clean workspace;
- treating mock/sandbox success as real external-system success;
- confusing build output/cache with durable Validation or Release artifacts.

## 3. Scope

### 3.1 Dependency & Toolchain Governance

Normative owner planned from Issue #187.

Required semantics include:

- canonical manifests and lockfiles;
- runtime/dev/build/test/optional/platform/transitive dependency classes;
- frozen/locked installation semantics where ecosystem supports them;
- vulnerability evidence, runtime exposure and risk-exception handling;
- dependency provenance and upgrade/change policy;
- compatibility floor, supported lines, preferred development version, certification tuple and deployment identity as distinct concepts;
- EOL/abandoned dependency and toolchain disposition;
- Agent MUST consume repository-owned requirements and MUST NOT invent or narrow toolchain constraints without authority;
- dependency/toolchain delta participates in Validation Impact.

### 3.2 Git Execution & Worktree Isolation

Normative owner planned from Issue #188.

Required semantics include:

- repository/branch/worktree/exact-SHA execution contract;
- concurrent writable executions MUST be isolated by worktree or equivalent workspace isolation;
- Builder writable branch-bound workspace vs Validator/Reviewer exact-SHA read-only/detached defaults;
- local workspace is NON-AUTHORITATIVE execution state;
- dirty-tree policy;
- local commit vs durable handoff;
- amend/rebase/reset/force-push effects on exact-SHA evidence;
- destructive Git operations require established workspace ownership;
- cherry-pick MUST NOT bypass Task DAG, sibling ownership or central integration authority;
- stacked PR remains code-baseline topology, not live Task DAG authority;
- cleanup/recovery rules for stale/interrupted workspaces.

### 3.3 Configuration & Secrets Governance

Add a normative standard that defines:

- canonical configuration schema/keys and deterministic precedence;
- defaults vs repository config vs deployment config vs explicit runtime override;
- secret references vs secret values;
- JIT secret injection and least-privilege access;
- prohibition on secrets in ordinary source, logs, Issues, evidence or fixtures;
- encrypted-in-Git secret material only when decryption authority is separate and project policy permits it;
- missing credential/configuration produces truthful BLOCKED/NOT_RUN-equivalent execution evidence rather than invented values;
- environment identity is part of materially environment-sensitive evidence.

### 3.4 Workspace & Artifact Governance

Add a normative standard classifying at least:

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

For each class define ownership, mutability, persistence, cleanup, Git eligibility, evidence eligibility and reconstruction expectations.

Core rules:

- cache != evidence;
- build output != release artifact until promoted by authorized build/release process;
- Agents MUST NOT delete unknown state merely to make a workspace clean;
- generated source/artifacts must record generator/revision when materially required;
- release-significant artifacts should have immutable identity such as digest/size plus source/candidate binding.

### 3.5 External System Execution

Add a normative standard for APIs, databases, cloud services, LLM providers, OAuth, queues, browsers, remote Build Hosts and similar boundaries.

Required environment classes:

```text
MOCK
SIMULATED
EPHEMERAL_REAL
SANDBOX
STAGING
PRODUCTION
```

Required rules include:

- lower-fidelity PASS MUST NOT imply higher-fidelity PASS;
- external writes/side effects require explicit authority;
- timeout/retry/rate-limit behavior must be bounded and must not hide deterministic failure;
- distinguish NETWORK_UNAVAILABLE, SERVICE_UNAVAILABLE, CREDENTIAL_UNAVAILABLE, RATE_LIMITED and equivalent infrastructure/execution facts from product failures;
- real external-service release requirements remain authority-driven through PRD/Architecture/PROJECT_OVERRIDES/Task acceptance.

## 4. Non-goals

v4.1.0 does not:

- replace Testing, Validation, CI, Review or Release standards;
- mandate one package manager, secret manager, workspace technology or external-service test framework;
- require all projects to use containers;
- require exact patch pinning for every toolchain;
- make all security scanner findings automatic release blockers regardless of exposure;
- convert local execution observations into Task/workflow authority.

## 5. Cross-standard model

v4.1 should establish the following execution chain:

```text
Task / Claim / Dispatch
        ↓
Dependency & Toolchain Contract
        ↓
Git Source / Workspace Contract
        ↓
Configuration / Secret Contract
        ↓
Workspace / Artifact Contract
        ↓
External System Contract
        ↓
Agent Execution
        ↓
Testing / Review / Validation
```

One semantic concern MUST have one normative owner; existing standards should reference rather than duplicate new rules.

## 6. Machine-readable expectations

v4.1 architecture research should determine which of the following merit schemas/manifests versus prose-only rules:

- Toolchain/Dependency Profile;
- Dependency Risk Exception;
- Git Workspace Record;
- Configuration Profile / secret-reference contract;
- Artifact Manifest;
- External System Execution Profile.

Machine contracts must be proportional to value and must not create mandatory bureaucracy for trivial projects.

## 7. Compatibility posture

Target: additive/non-weakening minor release over v4.0.

- Existing v4 evidence remains historical for its original subject.
- New standards MUST NOT retroactively fabricate PASS/FAIL for capabilities that were not previously required.
- Existing projects may adopt progressively through project overrides/capability declarations.
- If a proposed rule requires incompatible lifecycle or authority semantics, defer the breaking change rather than smuggle it into v4.1.

## 8. Product acceptance

v4.1.0 is product-complete when:

1. the five execution-foundation concerns have one clear normative owner each;
2. an Agent can determine applicable toolchain, source/workspace, config/secrets, filesystem classes and external-system authority without chat-only facts;
3. exact-SHA and Gate truth from v4.0 are preserved;
4. common unsafe shortcuts have explicit negative conformance cases;
5. Node/npm plus at least one non-Node ecosystem demonstrate language-neutral applicability;
6. at least one multi-Agent dogfood path demonstrates isolated execution and recoverability;
7. project adoption remains lightweight for Fast Path/low-risk repositories.

## 9. Planned references

- Issue #187 — Dependency & Toolchain Governance Standard
- Issue #188 — Git Execution & Worktree Isolation Standard
- Existing `EXECUTION_ARCHITECTURE_STANDARD.md`
- Existing `CI_EXECUTION_STANDARD.md`
- Existing `VALIDATION_STANDARD.md`
- Existing `TESTING_STANDARD.md`
- Existing `RELEASE_STANDARD.md`

## 10. Next gate

Before Freeze:

1. run L1 Product Evidence for the five proposed concerns;
2. validate scope boundaries against current v4 normative owners;
3. revise this PRD from evidence;
4. explicitly Freeze Product Authority;
5. proceed to L2 Architecture Evidence and Task DAG.
