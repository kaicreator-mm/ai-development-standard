# v4.4.0 L2 Architecture Evidence — Build, Packaging & Deployment

Status: **FROZEN L2 ARCHITECTURE AUTHORITY — 2026-09-30**

Freeze inputs:

- Frozen Product Authority: `0acbc82b031bc5870589fc1a899b679b0290d40a`
- L1 Product Evidence: `docs/implementation/4.4.0/L1_PRODUCT_EVIDENCE.md`
- v4.1 execution-foundation owners already integrated on their version line
- v4.2 Frozen Product/L2 and canonical planning merge `7bef72d4c686bf206a163d421396af72aab2b247`
- existing `RELEASE_STANDARD.md`, `VALIDATION_STANDARD.md`, `CI_EVIDENCE_STANDARD.md`

## 1. Architecture recommendation

Use **three normative owners + four compact default machine-contract families + existing Validation/Release authority**.

```text
Exact Source / Candidate
        │
        ▼
Build & Artifact Governance
   │            │
   │            ├─ Build Manifest
   │            └─ Artifact Promotion Record
   │                     │
   ▼                     ▼
Distribution          Release Qualification
(optional owner)          │
   │                       │
   └──────────────┬────────┘
                  ▼
          Deployment Governance
          │                  │
          ├─ Deployment Plan │
          └─ Deployment Result
```

Architecture decisions:

1. **Three normative owners only.** Build & Artifact, Distribution, Deployment are separate semantic owners; existing Release remains unchanged.
2. **Four default machine-contract families.** Separate build output from promoted artifact, and deployment plan from deployment result. These separations are semantically material and must not be compressed into one overloaded record.
3. **No default standalone Distribution schema.** Distribution is optional. Core artifact records carry immutable identity plus optional publication refs; a project/provider may define a dedicated publication record when distribution is material.
4. **No new global Gate/workflow state machine.** Delivery records expose domain facts; Validation and Release retain their own PASS/FAIL/BLOCKED/READY truth.
5. **Deployment result values are dimension-qualified.** Machine vocabulary should use namespaced values such as `DEPLOYMENT_SUCCEEDED`, `DEPLOYMENT_FAILED`, `DEPLOYMENT_PARTIAL`, `DEPLOYMENT_ROLLED_BACK`, `DEPLOYMENT_BLOCKED`, `DEPLOYMENT_NOT_RUN`, `DEPLOYMENT_NOT_APPLICABLE` to prevent cross-state inference.
6. **Artifact identity is content-bound.** Digest/content identity is canonical where available; filename/tag/channel is locator/alias metadata.
7. **Promote, do not silently rebuild.** A release-significant artifact is promoted by identity. Environment-specific rebuilds are allowed only as new artifact identities with their own required evidence.
8. **v4.2 migration remains authoritative.** Deployment Plan references migration transition/prerequisite identities but cannot redefine source/target/recovery semantics.
9. **v4.1 execution foundation composes by reference.** Toolchain/config/secret/environment/workspace facts are referenced, not duplicated into provider-specific delivery schemas.
10. **Production side effects remain separately authorized.** A Deployment Plan does not grant production authority merely by existing or by having credentials available.

## 2. Architecture drivers

### D1 — Provenance must bind an output to actual inputs
SLSA-style provenance demonstrates the value of recording how a build platform produced a specific artifact from identified inputs. ADS consumes the identity/provenance principle without mandating SLSA levels or one builder implementation.

### D2 — Content identity must survive mutable names
OCI/content-addressable practice demonstrates why digest/content identity and mutable tags/channels are different facts. ADS generalizes this to containers, packages, installers, archives and project-defined artifacts.

### D3 — Build output and release artifact have different authority
v4.1 already distinguishes `BUILD_OUTPUT` and `RELEASE_ARTIFACT`. v4.4 therefore needs separate machine objects for build production and artifact promotion rather than one file-exists shortcut.

### D4 — Plan and result cannot share one truth value
A deployment plan may exist while execution is not run, blocked, partial, failed or rolled back. The result must therefore be independently recorded and bound to plan/artifact/environment identity.

### D5 — Distribution is optional
Many internal/local products do not publish through a registry/channel. A mandatory publication object would create ceremony without truth. Publication refs are therefore optional by default.

## 3. Normative owner map

| Concern | Owner | Must not duplicate |
|---|---|---|
| build source/profile/toolchain/output identity | Build & Artifact Governance | Dependency/Toolchain policy, Validation result |
| package composition/content leakage policy | Build & Artifact Governance | v4.1 artifact class definitions |
| promotion from build output to immutable artifact | Build & Artifact Governance | Release verdict |
| publication/tag/channel/alias semantics | Distribution Governance | artifact digest identity, Deployment result |
| Release qualification | existing `RELEASE_STANDARD.md` | Deployment success |
| deployment plan/artifact/environment binding | Deployment Governance | migration semantics, config/secret ownership |
| rollout/result/partial/rollback facts | Deployment Governance | Validation/Release state |
| migration transition/recovery semantics | v4.2 Data & Migration | deployment orchestration |
| external environment/account/side-effect execution | v4.1 External System Execution | Deployment domain result |

## 4. Machine contracts

### 4.1 `schemas/build-manifest-v1.schema.json`
Purpose: identify one release-significant build output and the inputs/profile/toolchain/builder facts that materially produced it.

Required semantic fields:

```text
schema_version
build_id
source_identity {sha, tree/digest?}
build_profile
entrypoint_or_command_ref
builder_ref
toolchain_refs[]
dependency_profile_ref?
non_secret_config_fingerprint?
generated_input_refs[]
platform / architecture / feature refs when material
outputs[] {name/type/digest/size?}
evidence_refs[]
```

Rules:
- no secret values;
- no Release/Validation PASS field;
- stale output cannot satisfy a new requested build identity;
- multiple materially different profiles produce different build identities.

### 4.2 `schemas/artifact-promotion-v1.schema.json`
Purpose: record promotion of an identified build output into a release/distribution artifact identity.

Required semantic fields:

```text
schema_version
promotion_id
build_ref
artifact {type, immutable_identity/digest, size?, platform?}
content_policy_evidence_refs[]
promotion_authority_ref
candidate_ref?
release_ref?
provenance_refs[]
sbom_refs[]
publication_refs[]
```

Rules:
- filename/tag/channel cannot be the only immutable identity;
- record cannot manufacture Release READY;
- secret/cache/runtime/Agent-only content checks are referenced as applicable evidence;
- new bytes require new immutable identity.

### 4.3 `schemas/deployment-plan-v1.schema.json`
Purpose: durable authorized plan binding one exact artifact identity to one target environment and applicable config/migration prerequisites.

Required semantic fields:

```text
schema_version
plan_id
artifact_ref
target_environment_ref
configuration_profile_ref?
secret_refs[]          # references only, never values
migration_transition_refs[]
preflight_refs[]
rollout_strategy
verification_profile_refs[]
rollback_or_forward_policy_ref
side_effect_authority_ref
operator_or_automation_ref?
```

Rules:
- plan existence != execution;
- credentials/tool capability != side-effect authority;
- migration refs consume v4.2 semantics without redefining them.

### 4.4 `schemas/deployment-result-v1.schema.json`
Purpose: append/current execution fact for one plan/artifact/environment tuple.

Required semantic fields:

```text
schema_version
result_id
plan_ref
artifact_ref
target_environment_ref
result_state
started_at?
ended_at?
rolled_out_scope_ref?
rollback_result_ref?
evidence_refs[]
```

`result_state` domain vocabulary:

```text
DEPLOYMENT_SUCCEEDED
DEPLOYMENT_FAILED
DEPLOYMENT_PARTIAL
DEPLOYMENT_ROLLED_BACK
DEPLOYMENT_BLOCKED
DEPLOYMENT_NOT_RUN
DEPLOYMENT_NOT_APPLICABLE
```

Rules:
- namespaced values are deployment-domain facts, not Validation Gate status;
- rollback plan/ref does not prove rollback occurred;
- staging result does not imply production result;
- result is exact artifact + environment + plan scoped.

## 5. Existing schema integration

Prefer optional refs from applicable evidence/release objects rather than embedding delivery semantics into dispatch/workflow state.

Allowed examples:

- Validation Report MAY reference build/artifact/deployment record refs when a tuple validates those subjects.
- Release evidence MAY reference promoted artifact identities without changing Release verdict semantics.
- v4.2 migration transition refs MAY be consumed by Deployment Plan.

Do not make all four records mandatory for Fast Path/internal products where the underlying delivery stages are genuinely not material.

## 6. Architecture UNKNOWNs and disposition

| ID | UNKNOWN | Impact | Disposition | Decision |
|---|---|---|---|---|
| U1 | Combine build output and artifact promotion? | Critical | static/source evidence sufficient | No; v4.1 class separation makes them distinct. |
| U2 | Require standalone Distribution record? | Medium | static evidence sufficient | No default schema; publication refs by default. |
| U3 | Combine deployment plan/result? | Critical | static evidence sufficient | No; plan existence must not imply execution. |
| U4 | Require byte-for-byte reproducibility universally? | High | L1 sufficient | No; project/risk driven. |
| U5 | Require OCI/SLSA fields? | High | L1 sufficient | No; semantic mapping only. |
| U6 | Does Release READY authorize deployment? | Critical | authority evidence sufficient | No. |
| U7 | Does artifact rollback imply data rollback? | Critical | v4.2 boundary sufficient | No. |
| U8 | Need executable build/deploy Research Demo before L2 Freeze? | High | static authority evidence sufficient | No; real delivery proof belongs implementation dogfood/Validation. |

**Research Demo decision: NOT REQUIRED before L2 Freeze.**

## 7. Conformance architecture

Required semantic negative families include:

```text
source validation PASS -> artifact qualified       FAIL inference
build output exists -> promoted artifact           FAIL inference
filename/tag/channel -> immutable bytes             FAIL inference
old artifact qualification -> rebuilt bytes         FAIL inference
publication success -> deployment success            FAIL inference
Release READY -> deployment success                  FAIL inference
staging success -> production success                FAIL inference
credential exists -> production authority            FAIL inference
artifact rollback -> migration/data rollback         FAIL inference
rollback plan -> rollback executed                    FAIL inference
```

Positive dogfood later must cover at least:

1. a container/service path with immutable digest promotion and deployment-plan/result reconstruction;
2. a non-container package/install path with content-policy checks and immutable artifact identity.

## 8. Security / secret boundary

- Build/deployment records contain secret refs only, never secret values.
- Signed URLs/bearer publication URLs are secret material when possession grants access and must not become ordinary evidence.
- Package-content checks explicitly treat `.agent/`, caches, local runtime state and credentials as non-product unless Product authority says otherwise.

## 9. Fast Path / materiality

Small/internal projects MAY mark distribution/package/deployment contracts `NOT_APPLICABLE` with rationale when those stages genuinely do not exist. This does not weaken any actual required build/Validation/Release fact.

Machine records are instantiated when durable machine exchange adds value for material delivery truth; prose/pointers remain valid for trivial/non-material cases when identities and authority are still deterministic.

## 10. L2 verdict

Architecture is sufficiently resolved to create the v4.4 Task DAG.

No local/Build Host execution is required for planning. Real build/package/install/deployment validation will require exact-subject execution environments later and must use explicit handoff when the Web environment cannot execute them.
