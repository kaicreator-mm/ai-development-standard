# v4.1.0 L1 Product Evidence — Agent Execution Foundation

Status: **COMPLETE — supports Product Freeze after the PRD corrections recorded below**

Research date: 2026-09-29

Baseline / authority reviewed:

- `main@88aa35a6ac6ceec859c7c1d9114828873842c0c5`
- pinned standard version `4.0.0`
- Draft PR #189 / `planning/v4.1-v4.7-prds@88261ed1cff789f8d99b03159e84d75d075d31e1`
- Draft `docs/implementation/4.1.0/PRD.md`
- Issue #187 — Dependency & Toolchain Governance
- Issue #188 — Git Execution & Worktree Isolation
- current v4 `DEVELOPMENT_WORKFLOW`, `EXECUTION_ARCHITECTURE_STANDARD`, `CI_EXECUTION_STANDARD`, `TESTING_STANDARD`, `VALIDATION_STANDARD`, `RELEASE_STANDARD`, and `standard-manifest.json`

Research method follows `prompts/L1_PRODUCT_EVIDENCE.md`: real workflows and mechanisms, counter-evidence, product-boundary findings, and falsifiable assumptions were considered. This document is evidence for the Product decision; it is not itself a replacement for explicit PRD Freeze.

## 1. Recommendation

**PROCEED WITH NARROWING.**

The execution-foundation problem is real and increasingly material in Agent-driven development, but v4.1 must remain an **authority/interoperability contract**, not become a competing package manager, environment manager, secret manager, build system, artifact store, or external-service test framework.

L1 supports the five proposed concerns, with four required Product corrections before Freeze:

1. Treat the five concerns as one coherent **Execution Context** rather than five unrelated standards. Every material execution must be reconstructible across source/workspace, dependency/toolchain, configuration/secret references, filesystem/artifact state, and external-system environment/authority.
2. Keep mechanism choice project-owned. Existing tools already solve important slices; v4.1 owns cross-tool semantics, truth, authority, recovery, and evidence composition.
3. Do not freeze a universal external-environment enum more strongly than evidence supports. The Product requirement is fidelity/side-effect/environment identity and non-escalation of PASS; L2 may normalize labels while preserving provider/project mappings.
4. Prefer short-lived/JIT/least-privilege credentials where supported, but do not require a dynamic-secret mechanism universally. The mandatory Product rule is that secret values are not ordinary durable source/evidence and unavailable credentials produce truthful non-PASS execution state.

## 2. Problem Evidence

### 2.1 Dependency & Toolchain Governance

**Observed workflow/problem**

Modern ecosystems already distinguish a declared dependency graph, a resolved/locked graph, and the actual environment used to execute it. npm documents `npm ci` as a clean/frozen installation path: it requires an existing lockfile, errors when manifest and lock disagree, removes an existing `node_modules`, and does not rewrite the manifest/lockfile. This is direct evidence that reproducible execution depends on repository-owned dependency state rather than an Agent improvising installation.

Source: https://docs.npmjs.com/cli/commands/npm-ci/

GitHub/Dependabot and npm also preserve dependency scope such as runtime/development; npm supports `omit`/`include` classes and GitHub Dependabot alerts expose `development` vs `runtime` scope. This supports #187's requirement that vulnerability disposition must not flatten all dependency classes into one release rule.

Sources:

- https://docs.npmjs.com/cli/v11/commands/npm-audit/
- https://docs.github.com/en/rest/dependabot/alerts

Repository-configured environments already exist as an alternative mechanism. GitHub Codespaces recommends repository-owned `devcontainer.json` to provide a reproducible environment, while the Dev Container specification explicitly separates development-container concerns from production deployment. This supports a standard that records compatibility/certification truth without mandating containers.

Sources:

- https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces
- https://containers.dev/overview

Supply-chain provenance standards such as SLSA separately model build inputs, resolved dependencies, builder identity, and output subjects. This supports v4.1 treating dependency/toolchain identity as evidence input while leaving release/build provenance ownership with later delivery/release semantics.

Source: https://slsa.dev/spec/v1.2/provenance

**Internal dogfood evidence**

Issue #187 records ADS Plane v0.0.1 evidence: lockfile hardening, `npm install` → `npm ci`, a High production vulnerability fixed before release, dev-tooling findings separated from production exposure, and a mismatch between a broad Node engine declaration and actual runtime feature requirements. The example directly demonstrates why compatibility floor, preferred development line, certification tuple, and production identity are different facts.

**Finding**

The problem is sufficiently evidenced. v4.1 should standardize truthful dependency/toolchain contracts and Validation Impact, but must remain ecosystem-neutral and must not universalize npm/Node commands.

### 2.2 Git Execution & Worktree Isolation

**Observed workflow/problem**

Git itself provides linked worktrees so one repository can have multiple working trees and multiple branches checked out concurrently. Git refuses several unsafe operations by default (for example, adding a worktree for a branch already checked out elsewhere or removing an unclean worktree without force). This is evidence that worktree identity and cleanup/ownership are real execution concerns, not merely Agent prompt style.

Source: https://git-scm.com/docs/git-worktree

Current Agent-development practice independently converges on per-worktree isolation. OpenAI's published harness-engineering experience describes making an application bootable per Git worktree so each change has an isolated app instance, logs, metrics, and ephemeral observability stack. OpenAI also describes Git worktrees as a technique to isolate long-horizon Codex runs and reduce thrash.

Sources:

- https://openai.com/index/harness-engineering/
- https://developers.openai.com/blog/run-long-horizon-tasks-with-codex

The current v4 standard already binds Validation to exact SHA and distinguishes HEAD/BASE/MERGE-RESULT/CANDIDATE drift. The missing product layer is how a real writable local repository/worktree safely realizes those facts without turning local state into workflow authority.

**Finding**

Issue #188 is well-founded. The Product boundary should be: Git execution safety, isolation, source materialization, rewrite/cleanup/recovery semantics, and durable handoff. Task/claim/dispatch state remains owned by existing GitHub/Execution Architecture standards; exact-SHA Gate truth remains owned by Validation/Review/Release.

### 2.3 Configuration & Secrets Governance

**Observed workflow/problem**

GitHub Actions OIDC exists specifically to avoid duplicating long-lived cloud credentials into repository-hosted secrets. GitHub documents short-lived provider tokens tied to workflow identity and recommends conditions that restrict who may obtain them.

Sources:

- https://docs.github.com/en/actions/concepts/security/openid-connect
- https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers

HashiCorp Vault similarly distinguishes static secrets from dynamic credentials generated just-in-time and revoked/expired through leases. This demonstrates the value of short-lived and least-privilege credentials, but also demonstrates that dynamic/JIT secrets are a provider capability, not a universally available mechanism.

Sources:

- https://developer.hashicorp.com/vault/tutorials/get-started/understand-static-dynamic-secrets
- https://developer.hashicorp.com/vault/docs/concepts/cloud-access-management

GitHub Codespaces documents multiple configuration locations and explicitly warns that values placed in `devcontainer.json` as ordinary environment values must be safe to commit as plaintext; sensitive values instead belong in development-environment secrets. This is concrete evidence that config values, secret references, and secret values require different persistence rules.

Source: https://docs.github.com/en/codespaces/developing-in-a-codespace/persisting-environment-variables-and-temporary-files

**Finding**

A configuration/secrets standard is justified, but it should define precedence, authority, reference/value separation, leak prevention, least privilege, and truthful unavailable-credential handling. It should not require Vault, OIDC, `.env`, Kubernetes Secrets, or any one provider.

### 2.4 Workspace & Artifact Governance

**Observed workflow/problem**

Bazel's output-directory design explicitly aims to avoid collisions between users/workspaces/configurations, separate build state from source, and support selective cleanup. Bazel's remote cache stores action results and content-addressed build outputs specifically for reuse; those cache entries are not release authority.

Sources:

- https://bazel.build/versions/8.1.0/remote/output-directories
- https://bazel.build/versions/7.1.0/remote/caching

GitHub Actions workflow artifacts are separately uploaded, retained for a configured period, downloaded across jobs/runs, and deleted according to workflow/artifact retention. Their existence and lifecycle differ from local build caches and working-tree output.

Source: https://docs.github.com/en/actions/tutorials/store-and-share-data

SLSA provenance further distinguishes output subjects, build inputs/resolved dependencies, and byproducts useful for debugging or incident response. This supports an explicit distinction between generated/build/test byproducts and promoted release-significant artifacts.

Source: https://slsa.dev/spec/v1.2/provenance

**Finding**

The Product need is not to impose one directory layout. It is to prevent category mistakes (`cache == evidence`, `build output == release artifact`, `runtime state == disposable cache`) and to define ownership/cleanup/persistence/promotion semantics. Release artifact identity/provenance should compose with Release/Build ownership rather than be redefined here.

### 2.5 External System Execution

**Observed workflow/problem**

Testcontainers exists because shared or manually configured external test dependencies create nondeterministic results and configuration drift; it provisions real services in isolated containers instead of mocks/in-memory substitutes. This is evidence that “real dependency” and “mock” execution have different fidelity and failure properties.

Source: https://testcontainers.com/getting-started/

Provider-native sandboxes are another distinct execution class. Stripe's testing documentation allows simulated payments in sandboxes using provider-defined test values without moving real money and warns that test environments have different operational limits (for example, they should not be used for load testing). A provider sandbox therefore is neither a pure mock nor production.

Source: https://docs.stripe.com/testing

Current v4 Validation already requires an explicit platform/environment/toolchain/profile tuple and says a tuple proves only itself. v4.1 therefore does not need a second Gate model; it needs external-system authority/fidelity/side-effect semantics that feed the existing Validation tuple.

**Finding**

The external-system concern is justified, but L1 does not support treating the Draft PRD's six labels as an immutable universal taxonomy. Product Authority should require an ordered/declared fidelity model and minimum distinctions; exact labels/provider mappings belong to L2 and project overrides.

## 3. User / Agent Workflow Evidence

Across the five concerns, the repeated real workflow is:

```text
1. Resolve durable work authority (Issue / Task / Dispatch / Frozen inputs).
2. Materialize exact source identity into an owned/isolated workspace.
3. Resolve repository-owned dependency/toolchain contract.
4. Resolve non-secret configuration plus authorized secret references/credentials.
5. Classify local/generated/runtime/cache/evidence/artifact paths before mutation or cleanup.
6. Resolve external systems, environment fidelity and side-effect authority.
7. Execute.
8. Bind observed results to the actual execution context and exact subject.
9. Publish durable evidence/handoff; local workspace remains disposable/recoverable execution state.
```

Failure at steps 2–6 commonly means execution/environment `BLOCKED` or provider/channel unavailability, not an executed product assertion `FAIL`. This composes with the existing v4 Validation state model rather than replacing it.

## 4. Alternatives / Existing Solutions

| Concern | Existing mechanisms | What they solve | What remains for ai-development-standard |
|---|---|---|---|
| Dependency/toolchain | lockfiles, `npm ci`, Renovate/Dependabot, dev containers, language-specific version managers | graph resolution, updates, environment setup | authority, compatibility vs certification semantics, risk/waiver truth, Validation Impact, cross-ecosystem Agent behavior |
| Git/workspace | Git branches/worktrees/clones | source topology and local isolation primitives | role ownership, concurrent-Agent safety, rewrite/evidence semantics, recovery/handoff, destructive-operation authority |
| Config/secrets | env/config files, GitHub Secrets/OIDC, Vault, cloud IAM | value injection and credential issuance | precedence, secret-ref/value boundary, least privilege, durable-evidence redaction, unavailable-credential truth |
| Workspace/artifacts | build-system output trees/caches, CI artifacts, artifact stores, SLSA/OCI | build outputs, caching, storage, provenance mechanisms | cross-tool class semantics, cleanup/persistence/promotion rules, preventing category mistakes |
| External systems | mocks, fakes, Testcontainers, provider sandboxes/staging | test doubles and real/sandbox execution | fidelity/side-effect authority, PASS non-escalation, failure classification, environment binding |

The alternatives are therefore **mechanisms to consume**, not evidence that the governance problem does not exist.

## 5. Counter-evidence / Risks to the Product Shape

### 5.1 Existing tools already cover much of the mechanism

A repository with a dev container, lockfile, hosted secret manager, hermetic build system, and provider sandbox may already have good execution hygiene. A standard that duplicates those tools would add bureaucracy without value.

**Product response:** v4.1 specifies durable authority and cross-tool truth; it MUST accept equivalent project-owned mechanisms.

### 5.2 Small/Fast-Path repositories do not need every machine contract

For a tiny docs-only or low-risk project, requiring ToolchainProfile + WorkspaceRecord + ArtifactManifest + ExternalSystemProfile for every task would be disproportionate.

**Product response:** machine-readable contracts are capability/risk-driven. Absence of a non-applicable optional contract is not failure. Lightweight repository-owned facts remain valid.

### 5.3 Ecosystems disagree about pinning and lockfiles

Applications, reusable libraries, native toolchains, container images, and deployment runtimes have different compatibility/pinning goals. “Exact pin everything” can make a compatibility claim false or impractical.

**Product response:** separate compatibility range/floor, certification tuple, preferred development environment, and immutable deployment identity; never infer one from another.

### 5.4 Environment taxonomies are provider-specific

“Sandbox”, “test”, “staging”, “ephemeral real”, and “simulated” overlap differently across providers. A universal hard-coded enum risks false precision.

**Product response:** freeze required semantic dimensions (real-vs-double fidelity, persistence/isolation, side-effect class, environment identity, authority) and let L2 define a minimal normalized vocabulary plus extensible provider mapping.

### 5.5 Secret mechanisms vary

OIDC/Vault-style dynamic credentials are desirable but not universally available; requiring them would block valid legacy/on-prem/local workflows.

**Product response:** short-lived/JIT credentials are SHOULD/preferred where supported. Mandatory rules concern authority, least privilege, non-persistence/leakage, reference/value separation, and truthful BLOCKED state.

## 6. Product Shape Findings

### 6.1 One Execution Foundation, five normative owners

The five concerns should remain separate normative owners to avoid semantic duplication, but they must compose through one Product concept:

```text
Execution Context
├── subject/source identity
├── Git workspace/materialization identity
├── dependency + toolchain identity
├── configuration identity + secret references (never ordinary secret values)
├── workspace/artifact class state
├── external-system environment/fidelity/side-effect authority
└── executor/host identity when material
```

L2 must decide whether this becomes a shared machine contract, derived view, or composition of smaller contracts. L1 only freezes the requirement that the context be reconstructible when material to evidence or recovery.

### 6.2 Existing Gate authority stays authoritative

v4.1 must feed, not replace:

- `EXECUTION_ARCHITECTURE_STANDARD` for claim/dispatch/workflow state;
- `VALIDATION_STANDARD` for PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE and exact-SHA tuples;
- `CI_EXECUTION_STANDARD` / `CI_EVIDENCE_STANDARD` for CI execution/evidence;
- `RELEASE_STANDARD` for Candidate/Release/Repository Integration authority;
- `TESTING_STANDARD` for testing ownership and test type semantics.

### 6.3 Product-level negative cases

At minimum, the final version must make these shortcuts non-conformant:

- Agent invents/narrows a toolchain version because of its own host.
- Agent mutates or cleans an unowned/shared writable worktree.
- Agent treats a local commit/worktree as durable Task/dispatch authority.
- Agent writes a secret value into source/Issue/log/evidence to unblock execution.
- Agent converts unavailable credentials/network/service into product PASS or executed FAIL without evidence.
- Agent promotes cache/build output to release/evidence identity merely because the file exists.
- Agent infers sandbox/mock/simulated PASS as staging/production PASS.
- Agent reuses old exact-SHA evidence after material dependency/toolchain/source rewrite without an authorized impact decision.

## 7. Key Assumptions and Validation Plan

| Assumption | Risk if false | Validation / design requirement |
|---|---|---|
| A1. One composable execution context can span all five concerns without creating a second workflow state machine. | semantic duplication/conflict with v4 | L2 normative-owner map + schema composition review |
| A2. Existing `validation-report` / dispatch contracts can reference material execution context rather than being replaced. | breaking wire change | L2 schema-delta analysis; future-major if incompatible |
| A3. Environment fidelity can use a small normalized core plus provider/project extension. | false taxonomy or impossible adoption | L2 compare Testcontainers/provider sandbox/staging/production mappings |
| A4. Optional machine contracts can remain lightweight for Fast Path. | bureaucracy / low adoption | Task acceptance + conformance examples for minimal and rich projects |
| A5. Git worktree isolation can be normative without requiring Git worktrees specifically. | excludes remote sandbox/clone implementations | specify “worktree or equivalent isolated workspace”; conformance by semantics |
| A6. Secret governance can be secure without universal dynamic secrets. | either insecure or impractical | L2 define mandatory vs preferred controls; static-secret exception examples |

No L1 evidence currently shows a Product contradiction requiring Stop or future-major. Any L2 design that requires incompatible core lifecycle/wire semantics must be deferred or routed to future-major input under the roadmap SemVer guard.

## 8. PRD Corrections Required Before Freeze

The Draft PRD should be revised to:

1. add a unified Execution Context / reconstructibility requirement;
2. explicitly state v4.1 governs semantics and authority, not implementation mechanisms;
3. change external environment classes from a prematurely frozen universal enum to minimum fidelity distinctions + L2 normalization/provider mapping;
4. change JIT/dynamic secrets from universal implication to preferred mechanism where supported, while preserving mandatory secret-reference/value and least-privilege rules;
5. include supply-chain provenance/SBOM/license concerns as authority-driven Dependency Governance scope without making every scanner/SBOM a universal release blocker;
6. explicitly preserve current Validation Gate states and existing normative owners;
7. add lightweight/minimal conformance acceptance so Fast Path does not require all optional machine contracts;
8. add the cross-concern negative cases above to acceptance/conformance planning.

## 9. Standard-self Gap Found During L1

The current generic `prompts/L1_PRODUCT_EVIDENCE.md` is strong for product discovery but does not explicitly require **existing normative-owner/authority overlap analysis, internal dogfood/incident evidence, or compatibility/SemVer impact** when the “product” being evolved is itself a governance/development standard.

For this v4.1 L1 those checks were performed manually because they are material to avoiding duplicated authority. A separate standard-gap Issue should track a narrow enhancement to the L1 prompt/process; it should not silently expand the v4.1 Agent Execution Foundation Product scope.

## 10. Freeze Readiness

After applying §8 to the Draft PRD, L1 supports explicit Product Freeze because:

- real workflows/problems exist for all five concerns;
- credible existing mechanisms and counter-evidence were considered;
- the Product boundary is narrowed to governance/interoperability rather than tool replacement;
- existing v4 authority ownership is preserved;
- Fast Path/adoption proportionality is explicit;
- major assumptions are identified for L2 rather than disguised as Frozen Product facts;
- no evidence currently requires an incompatible v4 lifecycle/wire change.

**L1 verdict: PROCEED WITH NARROWING → revise PRD → explicit Freeze.**
