# v4.4.0 L1 Product Evidence — Build, Packaging & Deployment

Status: **COMPLETE — supports PRD revision; Product Freeze waits for v4.2 planning integration/currentness confirmation**

Research date: 2026-09-30

Baseline reviewed:

- `main@e9eb39235e45e9ad90407b803ab1c8679d348dbf`
- Draft `docs/implementation/4.4.0/PRD.md`
- v4.1 Frozen execution-foundation Product/L2, including Workspace/Artifact and Config/Secrets
- v4.2 Frozen Product `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9` and Frozen L2 `ea4532cacf87c03689351e43363580e2a14acd95` on planning PR #219
- current Testing/Validation/Release ownership

This evidence is Product evidence, not Product Freeze.

## 1. Recommendation

**PROCEED WITH NARROWING.**

The missing Product domain is strongly evidenced: ADS currently qualifies source/candidates but lacks a single durable path from exact source/build inputs to immutable distributable artifact identity and from an authorized artifact to environment-specific rollout evidence.

Required Product corrections before Freeze:

1. Separate **Build**, **Artifact/Packaging**, **Distribution**, and **Deployment** facts rather than one overloaded delivery state.
2. Freeze the invariant `build output != release artifact`; promotion/binding creates release/distribution identity.
3. Canonical artifact identity is immutable content identity/digest where the artifact format supports it; filename/tag/channel remains an alias/reference, not proof of bytes.
4. `Release READY != Deployment SUCCESS`; Release and Deployment are separate dimensions/owners.
5. Deployment must apply a specific authorized artifact identity to a specific environment/config/migration plan. Rebuilding per environment is not equivalent to promoting the same qualified artifact unless project authority explicitly allows a different model with new evidence.
6. v4.2 owns migration transition/recovery semantics; v4.4 owns deployment sequencing/orchestration and result around those prerequisites.
7. Production/live deployment authority is not inferred from credentials or a Release READY verdict.

## 2. Build Identity / Provenance Evidence

SLSA Build Provenance defines provenance as verifiable information describing where, when and how software artifacts were produced. Its build model binds build definition, builder identity, resolved dependencies/materials and produced artifacts.

Sources:

- https://slsa.dev/spec/v1.2/build-provenance
- https://slsa.dev/spec/v1.2/provenance

**Finding:** v4.4 should require release-significant builds to bind enough input/source/toolchain/profile/builder identity to explain the produced output. ADS should not require SLSA or in-toto for every project, but the evidence model supports durable build provenance as a first-class concern.

Product boundary:

```text
source/candidate identity
+ build profile/parameters
+ dependency/toolchain identity
+ builder identity when material
        ↓
build execution
        ↓
build output identity
```

Host-local undeclared state must not silently become a release build input.

## 3. Artifact Identity Evidence

OCI Image Specification uses content-addressable descriptors/manifests; descriptor digests identify content via collision-resistant hashes and allow independent verification that content has not changed.

Sources:

- https://specs.opencontainers.org/image-spec/manifest/
- https://github.com/opencontainers/image-spec/blob/main/descriptor.md

This is strong evidence for separating immutable artifact content identity from mutable human/distribution aliases.

Required Product distinction:

```text
artifact digest/content identity        # canonical where supported
artifact filename/tag/channel/alias     # locator/reference
artifact type/platform/architecture     # applicability
source/build provenance                 # origin
promotion/candidate/release binding     # authority
```

A mutable `latest`, version tag, filename or bucket path MUST NOT by itself prove that deployed bytes equal qualified bytes.

## 4. Build Output vs Release Artifact

v4.1 Workspace/Artifact Product semantics already freeze `BUILD_OUTPUT` and `RELEASE_ARTIFACT` as different semantic classes and require authorized promotion/binding rather than file existence.

v4.4 should consume and deepen this boundary:

```text
build output
→ package/content policy checks
→ immutable identity/digest
→ source/build/candidate binding
→ required Validation/Release prerequisites
→ authorized promotion
→ release/distribution artifact
```

v4.4 must not redefine v4.1 artifact-class ownership; it owns build/package/distribution/deployment mechanics built on that semantic foundation.

## 5. Package Content / Leakage Evidence

Release-significant package composition must be explicit enough to exclude execution-only and secret/runtime material. Relevant negative classes already exist in v4.1:

```text
SECRET_MATERIAL
CACHE
unowned/unknown RUNTIME_STATE
.agent / local execution-only state unless intentionally product content
unrelated TEST_ARTIFACT
```

Product requirements:

- package content policy is project/artifact-type specific;
- secrets MUST NOT become ordinary shipped content;
- caches/local runtime state are not shipped merely because they exist under workspace/output paths;
- generated source/build output ownership remains reconstructible;
- install/uninstall/upgrade validation applies where the artifact type/product requires it.

## 6. Distribution Boundary

Distribution is the publication/availability layer, when present, between promoted artifact and Deployment.

Examples:

```text
GitHub Release asset
container/package registry
object/artifact storage
installer/update channel
internal artifact repository
```

Required invariants:

- distribution alias/tag/channel is not canonical bytes identity;
- publication success != Deployment success;
- republishing an existing alias with different bytes cannot silently inherit prior qualification;
- retention/access/immutability policy remains project/provider-specific;
- distribution may be NOT_APPLICABLE for projects that deploy directly from a controlled artifact store.

## 7. Deployment Product Model

Deployment is modeled as application of a specific authorized artifact to a specific environment under a plan.

Material facts may include:

```text
artifact identity/digest
source/candidate/release ref
target environment identity
configuration/secret profile refs
migration transition/prerequisite refs
preflight
rollout strategy
health/readiness verification
post-deploy smoke/critical journey checks
operator/automation authority
result/evidence
```

Product invariant:

> `Release READY != Deployment SUCCESS`.

A Release verdict proves release qualification under `RELEASE_STANDARD.md`. Deployment success requires actual applicable rollout/execution evidence.

## 8. Deployment State / Result Separation

L2 should define Deployment result semantics without reusing Validation/Release states. Candidate Product outcomes may include:

```text
SUCCESS
FAILED
PARTIAL
ROLLED_BACK
BLOCKED
```

The exact machine vocabulary belongs to L2. `NOT_RUN` / applicability truth may remain projected through existing Validation/execution owners rather than overloading Deployment result if that composes better.

Required non-inferences:

- Release READY -> Deployment SUCCESS;
- registry upload success -> Deployment SUCCESS;
- health endpoint 200 -> complete business/critical-journey success;
- deployment credential exists -> deployment authorized;
- staging success -> production success;
- mutable tag points to image -> qualified digest identity;
- rebuilt-for-production bytes -> same qualified artifact by assertion.

## 9. Migration / Rollback Boundary With v4.2

v4.2 Frozen Product owns:

- migration source/target transition identity;
- ordering/dependencies internal to migration transition;
- upgrade vs fresh/recovery distinction;
- recovery strategy semantics.

v4.4 owns:

- when the migration prerequisite executes relative to artifact/config rollout;
- environment/application orchestration;
- partial rollout state;
- artifact/config rollback/continue decision evidence;
- references to v4.2 recovery strategy when data state constrains rollback.

v4.4 MUST NOT fabricate a reversible data rollback merely because artifact rollback is available.

## 10. Rebuild vs Promote

Default release-significant posture:

> Build once / identify immutable bytes / promote the same authorized artifact across applicable environments where the product/deployment model permits.

This is not an absolute universal rule. Some platform-native delivery models legitimately rebuild environment-specific outputs. In that case the new output has a new artifact/build identity and must satisfy the evidence required for that model; it cannot inherit another artifact's digest/qualification by assertion.

## 11. Machine-contract Product Findings

L1 supports evaluating four conceptual records, but L2 should minimize schema count:

1. **Build Manifest** — source/build profile/toolchain/builder/output identity.
2. **Artifact Manifest / Promotion Record** — immutable artifact identity, composition/provenance, candidate/release binding.
3. **Distribution Publication Record** — optional when publication is material.
4. **Deployment Plan + Result** — may be two records or one plan/result family depending currentness/append-only requirements.

Do not make SLSA/OCI fields mandatory for non-SLSA/non-OCI products; ADS should preserve semantic equivalents.

## 12. Product-level Negative Conformance

At minimum reject:

- source Validation PASS -> shipped artifact PASS;
- file exists in `dist/` -> release artifact;
- filename/tag/channel -> immutable content identity;
- qualified source -> independently rebuilt unbound bytes qualified;
- registry publication -> deployment success;
- Release READY -> Deployment SUCCESS;
- staging deployment -> production deployment PASS;
- write-capable credential -> deployment authority;
- artifact rollback -> data migration rollback;
- package useful debug trace -> permission to ship secret material.

## 13. Counter-evidence / Scope Risks

- Byte-for-byte reproducible builds are not universally practical; ADS should require sufficient identity/provenance, not universal determinism.
- Not every product has packaging or distribution; NOT_APPLICABLE must remain honest.
- Mutable tags/channels are operationally useful locators; the standard should prohibit treating them as canonical identity, not prohibit them.
- Some deployment platforms rebuild or synthesize environment-specific artifacts; new identity/evidence can be valid.
- Production deployment is often organization-controlled outside repository automation; durable references to external deployment systems may be sufficient.

## 14. L1 Verdict

**Evidence is sufficient for PRD revision.**

Product Freeze should occur after controller currentness confirms the v4.2 Frozen Product/L2 planning authority has been independently reviewed/integrated (or an explicit equivalent stable authority is accepted), because v4.4 consumes the migration/deployment boundary as a frozen upstream contract.

`LOCAL_ENV=NOT_REQUIRED` for L1/Product revision. Real build/package/install/deployment execution belongs later conformance/Validation Tasks with exact platform/artifact/environment subjects.