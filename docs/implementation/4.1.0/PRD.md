# ai-development-standard v4.1.0 PRD — Agent Execution Foundation

Status: **DRAFT PRODUCT AUTHORITY — L1 COMPLETE / FREEZE CANDIDATE**

Product Evidence:

- `docs/implementation/4.1.0/L1_PRODUCT_EVIDENCE.md`
- Issue #187 — Dependency & Toolchain Governance
- Issue #188 — Git Execution & Worktree Isolation
- Issue #190 — tracked non-blocking L1 standard-self process gap

Baseline: `main@88aa35a6ac6ceec859c7c1d9114828873842c0c5` / pinned standard `4.0.0`

## 1. Product intent

v4.1.0 establishes the **Agent Execution Foundation** required for reliable AI-native development.

v4.0 already defines lifecycle, execution architecture, GitHub-native coordination, testing, validation and release authority. Real Human/Agent execution still depends on under-specified source/workspace, dependency/toolchain, configuration/secrets, filesystem/artifact and external-system behavior.

v4.1.0 does **not** replace the tools that implement those concerns. It defines the repository-owned authority, truth, failure, recovery and evidence-composition semantics that allow different tools/executors to interoperate safely.

The product goal is to make an authorized Human or Agent able to answer, from durable repository/GitHub facts rather than chat or local assumptions:

1. What exact source/workspace may I operate on, and who owns it?
2. What dependencies/toolchains are compatible, preferred, and actually certified?
3. What configuration may I consume, which secret references am I authorized to resolve, and what must never become ordinary durable evidence?
4. What filesystem outputs are source, generated source, cache, runtime state, test/validation evidence, or release artifacts?
5. Which external systems may I access, with what fidelity/environment identity and side-effect authority?
6. What material execution context must be bound to results/evidence so another executor can reconstruct what actually ran?
7. Which failures are execution/environment `BLOCKED` or provider/channel unavailability rather than an executed product `FAIL`?

## 2. Product model — one Execution Foundation, five normative owners

The five concerns remain separate normative owners to avoid duplicate rules, but MUST compose as one execution foundation.

For materially environment-sensitive work, the execution context must be reconstructible across the applicable dimensions:

```text
Execution Context
├── subject / source identity
├── Git repository + workspace/materialization identity
├── dependency graph + toolchain identity
├── configuration identity + secret references
├── workspace/artifact class state
├── external-system environment / fidelity / side-effect authority
└── executor / host identity when material
```

L2 determines whether this is represented as one shared machine contract, a derived view, references among smaller contracts, or prose plus existing evidence fields. Product Authority requires reconstructibility and non-contradictory composition; it does not require bureaucracy for dimensions that are immaterial to a task/project.

## 3. Problem

Current v4 contains distributed guidance for lockfiles, clean checkouts, exact-SHA validation, external-boundary testing and project overrides, but does not define one coherent execution foundation. This allows Agents to make locally reasonable but globally inconsistent decisions, including:

- inventing or silently strengthening Node/Python/JDK/Git requirements;
- sharing writable Git workspaces across concurrent Agents;
- treating a local branch/worktree as workflow authority;
- using stale or mutable dependency graphs without explicit validation impact;
- creating `.env` or fake credentials merely to make execution succeed;
- persisting secret values into source, logs, Issues or evidence;
- deleting unknown caches/runtime data to obtain a clean workspace;
- treating cache/build output as durable Validation or Release artifact merely because it exists;
- treating mock/simulated/provider-sandbox success as higher-fidelity staging/production success;
- collapsing credential/network/provider unavailability into misleading product PASS/FAIL.

## 4. Scope

### 4.1 Dependency & Toolchain Governance

Normative owner planned from Issue #187.

Required semantics include:

- canonical manifests and ecosystem-appropriate lock/resolution authority;
- runtime/dev/build/test/optional/platform/transitive dependency classes where the ecosystem exposes them;
- frozen/locked installation semantics where the ecosystem supports and project authority requires them;
- vulnerability evidence, runtime exposure/applicability and risk-exception handling;
- dependency provenance, registry/source and upgrade/change policy;
- compatibility floor/range, supported lines, preferred development version, certification tuple and deployment identity as distinct concepts;
- EOL/abandoned dependency and toolchain disposition;
- supply-chain provenance, license and SBOM capabilities as authority/risk-driven concerns rather than universal release blockers;
- Agent MUST consume repository-owned requirements and MUST NOT invent or narrow toolchain constraints without authority;
- dependency/lockfile/toolchain delta participates in Validation Impact.

The standard MUST remain ecosystem-neutral. npm/Node may be one conformance example, not universal implementation authority.

### 4.2 Git Execution & Worktree Isolation

Normative owner planned from Issue #188.

Required semantics include:

- repository/clone/branch/workspace/exact-SHA execution contract;
- concurrent writable executions MUST use isolated workspaces (Git worktree or equivalent isolated clone/sandbox/workspace);
- Builder writable branch-bound workspace vs Validator/Reviewer exact-subject read-only/detached defaults where local execution is used;
- local repository/workspace is NON-AUTHORITATIVE execution state;
- dirty-tree and intended write-set discipline;
- local commit vs durable handoff;
- amend/rebase/reset/force-push effects on exact-SHA Review/Validation evidence;
- destructive Git operations require established workspace ownership;
- cherry-pick MUST NOT bypass Task DAG, sibling ownership or central integration authority;
- stacked PR remains code-baseline topology, not canonical live Task DAG authority;
- cleanup/recovery rules for stale/interrupted workspaces;
- submodule/LFS/sparse/partial materialization where project-owned source semantics require them.

Task/claim/dispatch/workflow state remains owned by existing GitHub/Execution Architecture authority. Git execution MUST NOT create a second workflow state machine.

### 4.3 Configuration & Secrets Governance

Add one normative owner for configuration and secret-consumption semantics.

Required semantics include:

- canonical configuration schema/keys when a project has configurable behavior;
- deterministic precedence across defaults, repository configuration, deployment/environment configuration and explicit runtime override as applicable;
- secret references/identities vs secret values;
- least-privilege secret access and environment/role-scoped authorization;
- short-lived/JIT credentials are preferred where the provider supports them, but are not universally mandatory;
- prohibition on secret values in ordinary source, logs, Issues, screenshots, evidence, fixtures or other unauthorized durable surfaces;
- encrypted-in-Git secret material only when decryption authority is separate and explicit project policy permits it;
- missing/unresolvable credential or required configuration produces truthful `BLOCKED`/`NOT_RUN`-equivalent execution evidence rather than invented values;
- material configuration/environment identity participates in evidence where behavior depends on it.

The standard MUST NOT mandate Vault, OIDC, `.env`, Kubernetes Secrets, a cloud provider, or any one secret manager.

### 4.4 Workspace & Artifact Governance

Add one normative owner that can classify at least the following semantic roles when they are present:

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

L2 may refine names/relationships but MUST preserve the distinctions required by Product behavior.

For each applicable class define ownership, mutability, persistence, cleanup, Git eligibility, evidence eligibility and reconstruction/promotion expectations.

Core rules:

- cache != evidence;
- build output != release artifact until promoted/bound by authorized build/release semantics;
- runtime state != disposable cache by default;
- Agents MUST NOT delete unknown/unowned state merely to make a workspace clean;
- generated source/artifacts record generator/revision/input identity when materially required;
- release-significant artifacts should have immutable identity such as digest/size plus source/candidate binding according to Release/Build authority;
- local/CI artifact existence alone does not establish Gate or Release state.

This concern defines class/ownership semantics and composes with, rather than replaces, Release/CI evidence/provenance authority.

### 4.5 External System Execution

Add one normative owner for APIs, databases, cloud services, LLM providers, OAuth, queues, browsers, remote Build Hosts and similar external boundaries.

Product Authority requires the execution contract to distinguish the semantic dimensions needed to prevent fidelity and authority escalation, including where applicable:

```text
real dependency vs deterministic fake/mock/simulation
provider-owned test/sandbox vs project staging vs production
ephemeral/isolated vs shared/persistent state
read-only vs permitted write/side-effect class
external environment/account/tenant identity
credential/authorization scope
```

A normalized vocabulary MAY include concepts such as `MOCK`, `SIMULATED`, `EPHEMERAL_REAL`, `SANDBOX`, `STAGING`, and `PRODUCTION`, but v4.1 Product Authority does **not** require every provider/project to implement an identical six-value enum. L2 owns the minimal normalized model and extensible mapping.

Required rules include:

- lower-fidelity PASS MUST NOT imply higher-fidelity PASS;
- external writes/side effects require explicit authority;
- timeout/retry/rate-limit behavior must be bounded and must not hide deterministic failure;
- distinguish material infrastructure/execution facts such as network unavailable, service unavailable, credential unavailable and rate limited from executed product defects;
- real external-service release requirements remain authority-driven through PRD/Architecture/PROJECT_OVERRIDES/Task acceptance;
- the external environment/fidelity identity feeds the existing Validation tuple/evidence model rather than creating a second Gate system.

## 5. Existing authority boundaries

v4.1.0 MUST feed existing v4 authority rather than duplicate it:

- `EXECUTION_ARCHITECTURE_STANDARD.md` owns claim/dispatch/workflow/controller state;
- `GITHUB_AGENT_INTERACTION_PROTOCOL.md` owns durable Issue/PR/event/operator coordination;
- `CI_EXECUTION_STANDARD.md` / `CI_EVIDENCE_STANDARD.md` own CI execution channel and CI evidence semantics;
- `TESTING_STANDARD.md` owns test type/ownership semantics;
- `VALIDATION_STANDARD.md` owns Gate states, exact-SHA evidence and Validation tuples/impact;
- `RELEASE_STANDARD.md` owns Candidate/Release/Repository Integration authority.

Normative rule:

> One semantic concern MUST have one normative owner. v4.1 standards reference existing owners for downstream Gate/workflow/release truth and own only the missing execution-foundation semantics.

## 6. Non-goals

v4.1.0 does not:

- replace Testing, Validation, CI, Review, Execution Architecture or Release standards;
- mandate one package manager, dependency bot, development environment, secret manager, build system, artifact store, workspace technology or external-service test framework;
- require all projects to use containers or Git worktrees specifically when an equivalent isolated workspace satisfies the contract;
- require exact patch pinning for every toolchain;
- make all security scanner findings automatic release blockers regardless of exposure/applicability;
- require SBOM/signing/provenance gates for every low-risk project by default;
- require dynamic/JIT secret issuance when the provider/project cannot support it;
- hard-code one provider-independent external-environment taxonomy beyond the semantic distinctions needed for truthful evidence;
- convert local execution observations into Task/workflow authority;
- create a second PASS/FAIL/BLOCKED state model.

## 7. Cross-standard execution flow

v4.1 should establish the following composition:

```text
Task / Claim / Dispatch authority
        ↓
Source + Git Workspace Contract
        ↓
Dependency & Toolchain Contract
        ↓
Configuration + Secret Reference Contract
        ↓
Workspace / Artifact Class Contract
        ↓
External System / Side-effect Contract
        ↓
Agent / Human Execution
        ↓
Existing Testing / Review / Validation / CI Evidence / Release authority
```

The ordering is conceptual, not a requirement that every task materialize every contract as a separate file.

## 8. Machine-readable expectations

L2 Architecture Evidence must determine which concepts merit schemas/manifests versus prose/derived views:

- Execution Context composition/reference model;
- Toolchain/Dependency Profile;
- Dependency Risk Exception;
- Git Workspace/Materialization Record;
- Configuration Profile / secret-reference contract;
- Artifact Manifest/classification view;
- External System Execution Profile.

Rules:

- machine contracts MUST be proportional to value/risk;
- trivial/Fast-Path projects MUST have a lightweight conformant path;
- existing `dispatch`, `validation-report`, event and release contracts SHOULD be extended/referenced compatibly when sufficient rather than replaced;
- any design requiring incompatible lifecycle/authority/wire semantics is future-major input, not hidden inside v4.1.

## 9. Compatibility posture

Target: additive/non-weakening minor release over v4.0.

- Existing v4 evidence remains historical for its original subject.
- New standards MUST NOT retroactively fabricate PASS/FAIL for capabilities that were not previously required.
- Existing projects may adopt progressively through project overrides/capability declarations and truthful non-applicable/not-run states.
- New execution metadata may refine successor evidence but MUST NOT relabel historical execution as if the metadata had existed then.
- If a proposed rule requires incompatible lifecycle, authority hierarchy or machine/wire semantics, defer the breaking change to future-major input under the v4.1→v4.7 roadmap guard.

## 10. Product-level unsafe shortcuts / negative conformance

The final v4.1 implementation must make at least these shortcuts explicitly non-conformant:

1. Agent invents/narrows a toolchain requirement because of its own host.
2. Agent concurrently mutates or destructively cleans an unowned/shared writable workspace.
3. Agent treats local branch/worktree existence or an unpushed commit as durable Task/dispatch/handoff authority.
4. Agent writes a secret value into ordinary source/Issue/log/evidence/fixture to unblock execution.
5. Agent converts unavailable credentials/network/provider into product PASS or an executed product FAIL without the required execution evidence.
6. Agent treats cache/build output as Validation/Release evidence merely because a file exists.
7. Agent infers fake/mock/simulated/sandbox PASS as higher-fidelity staging/production PASS.
8. Agent rewrites source/dependency/toolchain identity and silently reuses old exact-subject PASS without authorized impact/reuse semantics.
9. Agent uses an execution-foundation contract to override the existing canonical workflow/Gate/Release owner.

## 11. Product acceptance

v4.1.0 is product-complete when:

1. the five execution-foundation concerns have one clear normative owner each and compose as one Execution Foundation;
2. an Agent can determine applicable source/workspace, dependency/toolchain, config/secret references, filesystem classes and external-system authority without chat-only facts;
3. materially environment-sensitive evidence can reconstruct the applicable Execution Context without requiring every optional field for every task;
4. exact-SHA and Gate truth from v4.0 are preserved;
5. common unsafe shortcuts in §10 have explicit negative conformance coverage;
6. Node/npm plus at least one non-Node ecosystem demonstrate language-neutral Dependency/Toolchain applicability;
7. at least one multi-Agent dogfood path demonstrates isolated execution, durable handoff and recovery;
8. at least one provider sandbox/real-dependency case demonstrates fidelity non-escalation;
9. at least one minimal/Fast-Path conformance example demonstrates that optional machine contracts do not become universal bureaucracy;
10. no new standard duplicates or weakens the authority owned by Execution Architecture, GitHub interaction, Testing, Validation, CI or Release;
11. verifier/regression coverage catches material cross-standard weakening/duplication and the Product-level negative cases.

## 12. L2 questions / assumptions not frozen as Architecture Facts

Product Freeze does not answer these Architecture questions:

- one shared `execution-context` schema vs composed references/derived view;
- which existing schemas can be compatibly extended and which should remain unchanged;
- minimal normalized external-environment/fidelity vocabulary and extension mechanism;
- whether workspace records are durable machine facts, ephemeral observations, or optional evidence fields;
- exact dependency-risk exception schema and scanner-adapter boundaries;
- exact artifact-manifest relationship to future v4.4 build/package/deployment work;
- exact configuration precedence representation and secret-reference schema;
- how to verify minimal/Fast-Path conformance without forcing unused capabilities.

These are L2 Architecture Evidence subjects. High-impact UNKNOWNs must receive explicit disposition before L2 Freeze.

## 13. Planned references

- `docs/implementation/4.1.0/L1_PRODUCT_EVIDENCE.md`
- Issue #187 — Dependency & Toolchain Governance Standard
- Issue #188 — Git Execution & Worktree Isolation Standard
- Issue #190 — non-blocking L1 standards-evolution process gap
- `EXECUTION_ARCHITECTURE_STANDARD.md`
- `GITHUB_AGENT_INTERACTION_PROTOCOL.md`
- `CI_EXECUTION_STANDARD.md`
- `CI_EVIDENCE_STANDARD.md`
- `VALIDATION_STANDARD.md`
- `TESTING_STANDARD.md`
- `RELEASE_STANDARD.md`

## 14. Freeze gate

L1 Product Evidence is complete and supports Freeze after this revision because:

- each of the five concerns has real workflow/problem evidence;
- existing tools/alternatives and counter-evidence were considered;
- Product scope was narrowed away from replacing mechanisms;
- existing v4 normative owners are explicitly preserved;
- Fast-Path proportionality is an acceptance requirement;
- external-environment and secret-mechanism over-specification was removed from Product Authority;
- architecture/schema questions remain explicitly open for L2 rather than being disguised as Product facts;
- no L1 evidence currently requires a breaking v4 lifecycle/authority/wire change.

The next Product action is an **explicit PRD Freeze checkpoint**. Only after that checkpoint may L2 Architecture Evidence become authoritative input.
