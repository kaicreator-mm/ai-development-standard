# ai-development-standard v4.4.0 PRD — Build, Packaging & Deployment

Status: **DRAFT PRODUCT AUTHORITY — requires L1 Product Evidence review and explicit PRD Freeze before implementation**

## 1. Product intent

v4.4.0 standardizes the path from validated source to deployable, immutable software artifacts and from release-qualified artifacts to real environment rollout. Existing v4 Release authority decides whether a candidate is qualified; v4.4 adds the missing delivery mechanics without collapsing Release and Deployment into one state.

The product goal is to make a project answer, from durable facts:

1. What exact inputs produced this build/package?
2. What artifact identity/digest corresponds to the qualified source/candidate?
3. What content is allowed or forbidden inside a shipped artifact?
4. How was install/package/runtime behavior validated?
5. What environment received the artifact, with what config/migration plan?
6. Did deployment succeed, fail, partially roll out, or roll back?

## 2. Problem

Current Testing and Release standards reference build/package/platform evidence, but there is no single normative owner for build reproducibility, package composition, artifact provenance or deployment rollout. This creates ambiguity around generated artifacts, mutable tags, debug/release profiles, package leakage, environment promotion and rollback.

Common risks include:

- validating source but shipping an artifact that was built differently;
- treating a filename or mutable tag as artifact identity;
- including `.agent/`, local caches, credentials, debug-only content or unrelated test fixtures in packages;
- rebuilding separately for each environment so the deployed bytes differ from the qualified candidate;
- treating `Release READY` as proof of successful deployment;
- performing migration/config changes without binding them to the deployment plan;
- rolling forward after partial deployment without evidence of environment state.

## 3. Scope

### 3.1 Build Standard

Create a normative build standard covering, where applicable:

```text
source identity
build profile
build command / builder identity
toolchain/dependency identity
configuration inputs safe for build
generated-source inputs
reproducibility expectations
build outputs
build logs / diagnostics
```

Required principles:

- release-significant build must bind an immutable source/candidate identity;
- build profile must distinguish materially different outputs such as debug/release, platform/architecture or feature profile;
- builder/toolchain/dependency identity must be sufficiently recorded to explain or reproduce release-significant output;
- host-local undeclared state must not silently influence a release build;
- deterministic/reproducible builds are encouraged where practical, but universal byte-for-byte reproducibility is not required unless project authority demands it;
- a build failure is not converted to product PASS by reusing stale artifacts.

### 3.2 Packaging & Artifact Governance

Define promotion from ordinary build output to release/distribution artifact.

A release-significant artifact should be identifiable by durable metadata such as:

```text
artifact name/type
content digest
size
source/candidate SHA + tree
build profile
producer/build identity
created_at
platform/architecture when applicable
SBOM/provenance refs when required
```

Required rules:

- build output != release artifact until authorized packaging/promotion occurs;
- immutable digest/identity is preferred over mutable filename/tag as canonical artifact identity;
- package content rules must exclude secrets, local caches, unrelated runtime state and execution-only `.agent/` material unless explicitly part of the product;
- committed/generated artifacts must have clear source and regeneration ownership;
- install/uninstall/upgrade/package validation should be supported where relevant;
- signing/SBOM/provenance requirements remain project/risk driven and compose with Dependency & Toolchain Governance.

### 3.3 Distribution Boundary

Define distribution as the publication/availability layer between package and deployment when applicable.

Examples:

```text
GitHub Release
container registry
package registry
object storage
desktop installer channel
internal artifact store
```

Required semantics:

- distribution alias/tag/channel != canonical artifact digest;
- publication must not silently replace an already-qualified immutable artifact with different bytes;
- access, retention and immutability policy may be project-specific;
- distribution success is distinct from Deployment success.

### 3.4 Deployment Standard

Create a normative standard for applying an authorized artifact to an environment.

Environment classes should be explicit, for example:

```text
development
test/sandbox
staging
production
```

The standard should define:

```text
artifact identity
target environment identity
configuration/secret profile
preflight
migration dependency/order
rollout strategy
health/readiness verification
post-deploy smoke/critical checks
rollback/continue decision
operator/automation identity
deployment result/evidence
```

Core invariant:

```text
Release READY != Deployment SUCCESS
```

Deployment strategies may include rolling, canary, blue/green, replace-in-place, installer/manual or others. ADS defines required semantics and evidence, not one universal deployment technology.

### 3.5 Rollback / Failed Deployment

A deployment plan must define applicable recovery behavior before release-significant rollout where failure could leave persistent/partial state.

Required distinctions:

```text
artifact rollback
configuration rollback
migration/data recovery
partial fleet rollback
forward-fix / continue rollout
```

v4.2 Migration Governance remains the owner of data/schema migration semantics; v4.4 owns orchestration/order and deployment evidence.

## 4. Non-goals

v4.4 does not:

- replace `RELEASE_STANDARD.md`;
- require Kubernetes, containers, GitHub Releases or any specific deployment platform;
- require byte-identical reproducible builds for all projects;
- require every project to publish SBOM/signatures;
- define production SLO/alerting/incident response; those belong to Operations standards;
- authorize an Agent to deploy to production merely because a release is READY.

## 5. Cross-standard model

```text
Validated Source / Candidate
        ↓
Build
        ↓
Package / Artifact Identity
        ↓
Release Qualification
        ↓
Distribution (when applicable)
        ↓
Deployment Plan + Environment
        ↓
Rollout
        ↓
Deployment Verification
        ↓
SUCCESS / FAILED / PARTIAL / ROLLED_BACK / BLOCKED
```

Release and Deployment states must remain separate dimensions.

## 6. Machine-readable expectations

L2 should evaluate schemas for:

- Build Manifest;
- Artifact Manifest;
- Distribution Publication Record;
- Deployment Plan;
- Deployment Result.

Any artifact/deployment record used as formal evidence must bind exact source/artifact/environment identities and preserve truthful failure states.

## 7. Compatibility posture

Target: additive/non-weakening minor release. Existing Release evidence remains valid for what it proved; v4.4 must not retroactively claim historical deployments or package provenance that was never recorded.

## 8. Product acceptance

v4.4.0 is complete when:

1. Build/Packaging/Deployment have clear normative ownership and boundaries with Release;
2. release-significant artifacts have immutable identity and source binding;
3. package leakage of execution-only/secret/cache material is explicitly prohibited and testable;
4. Release READY and Deployment SUCCESS cannot be conflated by schemas, docs or conformance tests;
5. migration/config/artifact ordering is explicit for deployment;
6. at least one container/service path and one non-container packaging/install path are dogfooded or evidenced;
7. deployment failure/partial/rollback truth can be reconstructed without chat history.

## 9. Next gate

Before Freeze:

1. run L1 Product Evidence against mature build/package/provenance/deployment practices;
2. verify boundaries with Release, v4.1 Artifact/Config and v4.2 Migration standards;
3. revise and Freeze this PRD;
4. run L2 Architecture Evidence;
5. generate Task DAG with build/artifact/deployment/conformance lanes where safe.
