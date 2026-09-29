# v4.4.0 Task DAG — Build, Packaging & Deployment

Status: **FROZEN TASK DAG — 2026-09-30**

Freeze inputs:

- Frozen Product Authority: `0acbc82b031bc5870589fc1a899b679b0290d40a`
- Frozen L2 Architecture: `docs/implementation/4.4.0/L2_ARCHITECTURE_EVIDENCE.md`
- v4.2 canonical planning merge: `7bef72d4c686bf206a163d421396af72aab2b247`

## 1. DAG

```text
T01 Shared Delivery Machine Contracts
        │
        ├──────────────┬──────────────┐
        ▼              ▼              ▼
T02 Build &         T03 Distribution  T04 Deployment
Artifact Governance Governance        Governance
        │              │              │
        ▼              │              │
T05 Build/Package      │              │
Conformance/Dogfood    └──────┬───────┘
                              ▼
                    T06 Distribution/Deployment
                    Conformance/Dogfood

T02 ────────────────┐
T03 ────────────────┼→ T07 Adoption & Cross-standard Wiring
T04 ────────────────┘

T05 ────────────────┐
T06 ────────────────┼→ T08 Cross-standard Conformance / Closure Inputs
T07 ────────────────┘
                              │
                              ▼
                       Version Closure
```

Dependency summary:

```text
T02 blocked by T01
T03 blocked by T01
T04 blocked by T01
T05 blocked by T02
T06 blocked by T03 + T04
T07 blocked by T02 + T03 + T04
T08 blocked by T05 + T06 + T07
```

## 2. Task definitions

### T01 — Shared Delivery Machine Contracts
Own only the minimum machine layer selected by Frozen L2:

- `schemas/build-manifest-v1.schema.json`
- `schemas/artifact-promotion-v1.schema.json`
- `schemas/deployment-plan-v1.schema.json`
- `schemas/deployment-result-v1.schema.json`
- narrowly justified optional refs in existing evidence/release schemas
- focused schema/backward-compatibility tests

Must not define normative delivery policy or provider-specific mechanisms.

### T02 — Build & Artifact Governance
Own:

- `standards/BUILD_ARTIFACT_GOVERNANCE_STANDARD.md`
- `references/BUILD_ARTIFACT_REFERENCE.md`
- focused semantic tests

Preserve exact source/profile/toolchain/output identity, build-output vs promoted-artifact separation, content-policy evidence, immutable artifact identity and rebuild non-transfer.

### T03 — Distribution Governance
Own:

- `standards/DISTRIBUTION_GOVERNANCE_STANDARD.md`
- `references/DISTRIBUTION_REFERENCE.md`
- focused semantic tests

Distribution remains optional. Mutable alias/tag/channel must never become canonical byte identity or Deployment truth.

### T04 — Deployment Governance
Own:

- `standards/DEPLOYMENT_GOVERNANCE_STANDARD.md`
- `references/DEPLOYMENT_REFERENCE.md`
- focused semantic tests

Preserve plan vs result separation, exact artifact/environment binding, namespaced deployment outcomes, side-effect authority, v4.2 migration boundary, and Release READY != Deployment SUCCESS.

### T05 — Build / Package Conformance & Dogfood
Own conformance fixtures/evidence for Build & Artifact semantics, including at least one non-container package/install path:

- source/profile/toolchain -> build output identity;
- package content-policy negatives for secret/cache/runtime/Agent-only leakage;
- promotion to immutable artifact identity;
- rebuilt bytes cannot inherit old artifact qualification;
- install/upgrade/package validation where material.

If required platform/package tooling cannot execute in Web/CI, create exact-subject local Validation handoff; do not simulate a PASS.

### T06 — Distribution / Deployment Conformance & Dogfood
Own conformance fixtures/evidence for publication/deployment semantics, including at least one container/service path when supported by the selected dogfood subject:

- immutable digest vs tag/channel alias;
- publication success != Deployment success;
- exact Deployment Plan -> actual Result binding;
- staging != production;
- credential capability != production authority;
- rollback plan != rollback execution;
- artifact rollback != data migration rollback.

Use sandbox/mock only for the dimensions they actually prove. Real external/environment execution requires explicit exact-scope Validation handoff when unavailable.

### T07 — Adoption & Cross-standard Wiring
Own central integration only:

- `standard-manifest.json` additions;
- selected `PROJECT_OVERRIDES` / project-adoption guidance;
- selected Validation/Release/checklist references where additive and justified;
- migration/adoption notes;
- focused wiring regression.

Must not rewrite T01–T06 semantics or introduce a new lifecycle/Gate state machine.

### T08 — Cross-standard Conformance / Closure Inputs
Own integrated negative inference tests, historical compatibility, Fast Path proportionality, v4.1/v4.2 composition and durable Version Closure inputs.

Must not issue the Version Closure/Release Qualification verdict itself.

## 3. Native Issue dependency graph

After materialization, GitHub Issue Dependencies are the canonical live execution DAG. This file remains frozen planning/history authority.

Expected native edges are exactly the dependency summary in §1. T01 is the single initial implementation root.

Task branches are JIT from current `version/v4.4.0` only after native blockers are satisfied.

## 4. Integration target

Planning authority integrates first. Create `version/v4.4.0` only after the planning PR is independently reviewed and canonically integrated to `main` (or equivalent current repository authority).

All implementation PRs target `version/v4.4.0` and follow one concern per PR.

## 5. Review / Validation posture

- T01–T04: required concern Validation + Fresh Independent Review.
- T05–T06: required Review; Validation binds the exact product/artifact/environment tuple actually exercised.
- T07: required Review/Validation because it mutates shared adoption/manifest surfaces.
- T08: required integration Review/Validation and durable closure inputs.

Exact-SHA evidence becomes stale on material subject drift. CI PASS is not a substitute for required real build/package/deployment evidence.

## 6. Risk / executor posture

| Task | Risk | Default executor suitability |
|---|---|---|
| T01 | high | bounded implementation agent after Frozen L2 |
| T02 | high | bounded implementation agent with normative reference pack |
| T03 | medium-high | bounded implementation agent; distribution optionality must remain explicit |
| T04 | high | high-capability builder/reviewer due production side-effect boundary |
| T05 | high | builder + exact environment validator when package/install proof is material |
| T06 | high | builder + external/local validator for real deployment dimensions |
| T07 | high | central integration builder + fresh reviewer |
| T08 | high | integration validator/reviewer |

## 7. Local environment posture

Planning and T01–T04 are repository/Web/CI executable by default.

T05 and T06 are the likely real-environment gates. A required real build, installer, registry, service or deployment proof that Web/CI cannot execute MUST become a dedicated exact-subject Validation Request; unavailable execution is `BLOCKED`/`NOT_RUN`, never inferred PASS.

`LOCAL_ENV=NOT_REQUIRED` at Task DAG Freeze.