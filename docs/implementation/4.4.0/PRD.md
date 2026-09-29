# ai-development-standard v4.4.0 PRD — Build, Packaging & Deployment

Status: **FREEZE CANDIDATE — revised from L1; explicit Product Freeze waits for canonical v4.2 planning integration/currentness**

## 1. Product intent

v4.4.0 standardizes the delivery path from exact validated source/candidate to identifiable build output, promoted artifact, optional distribution publication and actual environment deployment.

The version must let a project answer, from durable facts:

1. What exact inputs/profile/toolchain produced this build output?
2. What immutable artifact identity corresponds to the promoted/qualified bytes?
3. What content is permitted or forbidden in the shipped artifact?
4. Which distribution alias/channel points to which immutable artifact?
5. Which exact artifact was applied to which environment/config/migration plan?
6. What actually happened during rollout and recovery?

Core separation:

```text
Build
Artifact / Packaging Promotion
Distribution (optional)
Release Qualification
Deployment
```

These are related facts, not one overloaded delivery state.

## 2. Product owners

v4.4 introduces three normative owners:

1. **Build & Artifact Governance Standard** — build identity/provenance, package composition and promotion from build output to release/distribution artifact.
2. **Distribution Governance Standard** — publication/alias/channel semantics when distribution exists.
3. **Deployment Governance Standard** — authorized artifact-to-environment plan, rollout, result and deployment recovery/orchestration.

Existing `RELEASE_STANDARD.md` remains the Release Qualification owner.

v4.1 Workspace/Artifact remains the semantic class owner for `BUILD_OUTPUT`, `RELEASE_ARTIFACT`, `SECRET_MATERIAL`, cache/runtime/test artifact distinctions. v4.4 consumes those classes and defines delivery mechanics around them rather than redefining them.

v4.2 remains the migration transition/recovery semantic owner. v4.4 owns when/how deployment orchestrates the migration prerequisite relative to artifact/config rollout.

## 3. Build & Artifact Governance

A release-significant build must bind enough durable identity to reconstruct or explain the produced output, where applicable:

```text
source / candidate identity
source tree/digest where material
build profile / target
build command or deterministic entrypoint
builder identity/class when material
dependency/toolchain identity
safe build configuration inputs
generated-source inputs
platform/architecture/feature profile
output identity
logs/diagnostics refs
```

Required semantics:

- release-significant output is bound to immutable source/candidate identity;
- materially different build profiles produce distinct build identities;
- undeclared host-local state MUST NOT silently influence release-significant output;
- deterministic/reproducible builds are preferred/evidenced where practical, but universal byte-for-byte reproducibility is not required unless project authority requires it;
- stale build output MUST NOT be substituted for a failed/unexecuted requested build;
- build provenance may map to SLSA/in-toto/provider-specific formats, but ADS does not mandate one provenance technology.

## 4. Build Output vs Promoted Artifact

Frozen invariant:

> **Build output is not a release/distribution artifact merely because a file/image/package exists.**

Promotion requires applicable identity and authority such as:

```text
immutable content digest/identity
artifact type/platform applicability
source/build/candidate binding
package/content-policy checks
required Validation/Release prerequisites
promotion authority
candidate/release/distribution binding
```

Where content-addressable identity exists, digest/content identity is canonical. Filename, mutable tag, channel or bucket path is a locator/alias rather than proof of bytes.

A new/rebuilt byte sequence is a new artifact identity even if it reuses the same human version/tag.

## 5. Package Content Policy

Package composition is artifact/product specific, but v4.4 freezes these minimum rules:

- secret values/credentials MUST NOT become ordinary shipped content;
- caches and unrelated local runtime state MUST NOT be included merely because they exist under workspace/output paths;
- execution-only `.agent/` or equivalent local Agent state is excluded unless explicitly part of the product contract;
- unrelated test/debug fixtures/traces do not become package content by default;
- generated source/build output has explicit producer/regeneration ownership;
- install/uninstall/upgrade/package validation applies when material to that artifact/product type;
- signing/SBOM/provenance requirements are project/risk driven and compose with Dependency & Toolchain Governance.

## 6. Distribution Governance

Distribution is optional publication/availability between promoted artifact and Deployment, for example:

```text
GitHub Release
container/package registry
object/artifact storage
desktop installer/update channel
internal artifact repository
```

Required semantics:

- alias/tag/channel != canonical immutable artifact identity;
- publication binds the intended immutable artifact/digest where the system supports it;
- republishing/replacing an alias with different bytes MUST NOT silently inherit prior qualification;
- publication success != Deployment success;
- distribution access/retention/immutability policy remains project/provider specific;
- distribution may be `NOT_APPLICABLE` where delivery does not use a separate publication layer.

## 7. Deployment Governance

Deployment applies a specific authorized artifact identity to a specific target environment under an authorized plan.

Material plan facts may include:

```text
artifact identity/digest
source/candidate/release reference
target environment identity
configuration/secret profile references
migration transition/prerequisite references
preflight prerequisites
rollout strategy
health/readiness checks
post-deploy smoke/critical-journey checks
rollback/continue/forward-fix policy
operator/automation authority
deployment evidence/result
```

Core invariant:

> **Release READY != Deployment SUCCESS.**

Release Qualification proves the candidate under Release authority. Deployment SUCCESS requires actual applicable rollout evidence for the requested artifact/environment/plan.

Credential capability does not itself authorize production/live deployment.

## 8. Deployment Result Dimension

L2 must design deployment result semantics as a separate dimension from Validation and Release. Product-level semantic outcomes include, where applicable:

```text
SUCCESS
FAILED
PARTIAL
ROLLED_BACK
BLOCKED
```

L2 may refine exact machine vocabulary and decide how `NOT_RUN` / `NOT_APPLICABLE` compose with existing execution/Validation truth.

Required distinctions:

- requested deployment never executed;
- infrastructure/access blocked deployment;
- deployment started and failed;
- partial rollout;
- completed rollout;
- rollback actually executed and verified.

A rollback plan existing is not proof that rollback occurred.

## 9. Migration / Data Recovery Boundary

v4.2 owns:

```text
source-state -> transition -> target-state
migration ordering/dependencies internal to that transition
fresh vs upgrade vs failed/interrupted recovery semantics
recovery strategy for persistent state
```

v4.4 owns:

```text
deployment sequencing around migration prerequisites
artifact/config rollout order
partial deployment/fleet state
artifact/config rollback or continue/forward-fix decision
reference to v4.2 migration recovery constraints
actual deployment result/evidence
```

Artifact rollback MUST NOT be interpreted as data/schema rollback.

## 10. Promote vs Rebuild Across Environments

Default release-significant posture:

```text
build once
→ bind immutable artifact identity
→ qualify/promote
→ apply that same authorized artifact across compatible environments
```

This is not a universal prohibition on environment-specific build systems. If a product legitimately rebuilds/synthesizes environment-specific output, that output has a distinct build/artifact identity and must satisfy the evidence required for that model. It cannot inherit another artifact's qualification by assertion.

## 11. Product-level forbidden inferences

v4.4 conformance MUST reject at least:

```text
source Validation PASS -> shipped artifact PASS
file exists in dist/ -> RELEASE_ARTIFACT
filename/tag/channel -> immutable bytes identity
qualified source -> independently rebuilt bytes qualified
registry/publication success -> Deployment SUCCESS
Release READY -> Deployment SUCCESS
staging deployment -> production deployment PASS
write-capable credential -> deployment authority
artifact rollback -> data migration rollback
rollback plan exists -> rollback executed
package/debug usefulness -> permission to ship SECRET_MATERIAL
```

## 12. Machine-readable expectations

L2 should minimize machine-contract count while evaluating these conceptual durable records:

1. **Build Manifest** — exact source/profile/toolchain/builder/output identity.
2. **Artifact Manifest / Promotion Record** — immutable artifact identity, composition/provenance and candidate/release binding.
3. **Distribution Publication Record** — only when distribution is a material separate stage.
4. **Deployment Plan / Result family** — exact artifact/environment/config/migration references plus append/current result truth.

ADS MUST NOT require SLSA/OCI-specific fields for non-SLSA/non-OCI products; equivalent semantics are sufficient.

## 13. Non-goals

v4.4 does not:

- replace `RELEASE_STANDARD.md`;
- redefine v4.1 workspace/artifact classes;
- redefine v4.2 migration transition/recovery semantics;
- require Kubernetes, containers, GitHub Releases or another deployment platform;
- require byte-identical reproducible builds universally;
- require every project to publish SBOM/signatures;
- define runtime SLO/alerting/incident ownership (v4.5);
- authorize production deployment because tools/credentials exist;
- require packaging/distribution for products where those stages are genuinely not applicable.

## 14. Compatibility posture

Target: additive/non-weakening v4 minor release.

Historical Release evidence remains scoped to what it proved. v4.4 MUST NOT retroactively invent artifact provenance, distribution publication or Deployment results for historical releases.

If delivery architecture requires incompatible core lifecycle/wire changes, record future-major input rather than hide it inside v4.4.

## 15. Product acceptance

v4.4.0 is complete when:

1. three Product owners in §2 have clear boundaries with v4.1/v4.2/Release;
2. release-significant build outputs bind source/profile/toolchain identity sufficiently for evidence;
3. build output cannot self-promote into a release/distribution artifact;
4. immutable artifact identity is distinct from mutable aliases/channels;
5. package leakage of secrets/cache/runtime/Agent-only material is explicitly prohibited/testable;
6. Release READY and Deployment SUCCESS cannot be conflated in docs/schemas/tests;
7. migration/config/artifact ordering is explicit without stealing v4.2 migration semantics;
8. partial/failure/rollback deployment truth is reconstructible;
9. at least one container/service path and one non-container packaging/install path are dogfooded or evidenced.

## 16. Freeze basis / next gate

Freeze candidate basis:

- `docs/implementation/4.4.0/L1_PRODUCT_EVIDENCE.md`
- v4.1 Frozen Workspace/Artifact + Config/Secrets Product semantics
- v4.2 Frozen Product/L2 migration boundary on planning PR #219

Before explicit Product Freeze:

1. v4.2 planning authority must pass independent review and be canonically integrated/current, or an explicit equivalent stable-authority decision must be recorded;
2. re-read upstream boundaries for drift;
3. then record Product Freeze and proceed to L2 Architecture Evidence.

`LOCAL_ENV=NOT_REQUIRED` for Product Freeze/L2 research. Real build/package/install/deployment proof belongs later exact-subject Validation/dogfood Tasks.