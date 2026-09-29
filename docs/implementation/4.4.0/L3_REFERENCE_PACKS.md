# v4.4.0 L3 Reference Packs — Build, Packaging & Deployment

Status: **FROZEN IMPLEMENTATION REFERENCE — 2026-09-30**

Authority inputs:

- Frozen Product: `0acbc82b031bc5870589fc1a899b679b0290d40a`
- Frozen L2: `docs/implementation/4.4.0/L2_ARCHITECTURE_EVIDENCE.md`
- Frozen Task DAG: `docs/implementation/4.4.0/TASK_DAG.md`

L3 is implementation guidance subordinate to the Frozen Product/L2/Task Pack. Each Task follows **Tests → Contract → Implementation → Failure Handling → Reference** and may not broaden its allowed write-set or authority.

## T01 — Shared Delivery Machine Contracts

### Tests
- Draft 2020-12 / repository-supported schema subset.
- positive build, promotion, deployment-plan and deployment-result examples.
- historical payload compatibility when optional refs are absent.
- reject missing immutable artifact identity where promotion claims exist.
- reject Validation/Release PASS/READY vocabulary in domain records.
- reject secret values in obvious secret-value fields.

### Contract
Implement only four default families selected by L2. Build Manifest owns build identity facts; Artifact Promotion owns promoted immutable artifact facts; Deployment Plan owns requested/authorized plan facts; Deployment Result owns actual execution facts.

### Implementation
Prefer compact schemas compatible with current repository validators. Add optional evidence refs only where they do not make historical payloads invalid.

### Failure handling
Unsupported schema keywords, backward-compatibility regressions, or pressure to add provider-specific/global lifecycle state => fail closed and repair within T01; do not weaken schema verification.

### Reference
Frozen L2 §4–§5 and Task Pack T01.

## T02 — Build & Artifact Governance

### Tests
- source/candidate identity cannot be replaced by branch/latest.
- materially different build profile/toolchain => distinct build identity.
- file existence != promoted artifact.
- filename/tag != immutable artifact identity.
- rebuild/new bytes do not inherit old qualification.
- secret/cache/runtime/Agent-only content not shipped by default.

### Contract
Normative owner for release-significant build identity, package composition/content policy and promotion from build output to immutable artifact. It references v4.1 Dependency/Toolchain + Workspace/Artifact and existing Validation/Release authority.

### Implementation
Write one standard, one reference, focused semantic tests. Use provider-neutral language and examples spanning archive/package/container-style identities without requiring any one format.

### Failure handling
If package/product-specific requirements cannot be generalized, leave them project/profile owned and expose the authority hook; do not mandate OCI/SLSA/reproducible-build levels globally.

### Reference
Frozen Product §§3–5,10,12; L2 §§2–4.

## T03 — Distribution Governance

### Tests
- mutable alias/tag/channel cannot prove bytes.
- publication success cannot imply Deployment success.
- alias repointing cannot inherit old artifact qualification.
- distribution may truthfully be NOT_APPLICABLE.

### Contract
Optional normative owner for publication/availability semantics between promoted artifact and Deployment. Immutable artifact identity remains external input from Build & Artifact Governance.

### Implementation
Keep the standard small. Reference registries/releases/object stores as examples only. Do not create a mandatory distribution schema unless later evidence changes architecture authority.

### Failure handling
If publication system cannot expose immutable binding, record the limitation/required alternative evidence; never treat mutable locator alone as identity proof.

### Reference
Frozen Product §6; L2 decisions 3/6.

## T04 — Deployment Governance

### Tests
- plan existence != execution/result.
- Release READY != Deployment success.
- staging result != production result.
- credential/tool capability != production authority.
- rollback plan != rollback executed.
- artifact rollback != migration/data rollback.
- exact artifact + environment + plan binding required.

### Contract
Normative owner for authorized artifact-to-environment plan, rollout/result and deployment orchestration. v4.2 owns migration transition/recovery semantics; v4.1 owns external-system/config/secret facts; existing Release owns READY.

### Implementation
Use namespaced deployment-domain result vocabulary. Keep plan/result distinct and reference external authority rather than embedding credentials or migration semantics.

### Failure handling
Unavailable target access/environment is BLOCKED/NOT_RUN for the relevant execution; it cannot be converted into simulated success. Authority ambiguity routes upward before side effects.

### Reference
Frozen Product §§7–10; L2 §§3–4.

## T05 — Build / Package Conformance & Dogfood

### Tests
Use a bounded fixture/dogfood matrix containing:
- one non-container package/install path;
- package content-policy positives and leakage negatives;
- exact source/profile/toolchain/output binding;
- immutable promotion identity;
- rebuilt-bytes negative;
- install/upgrade/package checks when applicable.

### Contract
Conformance-only Task. It proves T02 semantics and may create evidence/fixtures/tests, not new normative rules.

### Implementation
Prefer repository-executable fixtures first. If real packaging/install tooling is materially required, hand off an exact SHA/platform/toolchain/profile tuple.

### Failure handling
Missing real tooling => explicit Validation Request. A simulated/static fixture may prove contract logic but not the absent real tuple.

### Reference
Frozen Product acceptance 2–5,9; L2 §7.

## T06 — Distribution / Deployment Conformance & Dogfood

### Tests
Use a bounded container/service or equivalent deployed-service scenario covering:
- digest vs alias;
- publication vs deployment result;
- plan/result identity;
- partial/failed/rolled-back states;
- staging/production non-substitution;
- side-effect authority;
- migration reference boundary.

### Contract
Conformance-only Task for T03/T04; no new normative owner.

### Implementation
Use sandbox/mock only for dimensions actually proven. For real external effects, bind exact environment/account/artifact identity and authorized mutation scope.

### Failure handling
No production access, missing registry/runtime, or unavailable target => Validation Request/BLOCKED. Never use credential presence as authority.

### Reference
Frozen Product acceptance 6–9; L2 §§7–8.

## T07 — Adoption & Cross-standard Wiring

### Tests
- all v4.4 standards/schemas/references discoverable.
- project overrides can declare applicable delivery stages without weakening truth.
- existing Release/Validation/checklists reference owners rather than duplicate them.
- Fast Path/non-deployed projects are not forced into fake publication/deployment records.
- historical releases are not retrofitted with provenance/results never produced.

### Contract
Single convergence owner for manifest/project-adoption/checklist/migration surfaces. No semantic redesign of T01–T06.

### Implementation
Wire by reference. Preserve current Golden coverage invariants when adding normative owners to the manifest.

### Failure handling
Manifest/Golden/adoption inconsistency is a T07 defect and must be repaired rather than waived. Owner conflicts route to their normative Task/authority.

### Reference
Frozen Product §§13–16; L2 §§5,9.

## T08 — Cross-standard Conformance / Closure Inputs

### Tests
Integrated negative inference matrix at minimum:
- source Validation PASS -> artifact qualified;
- build output exists -> promoted artifact;
- alias -> immutable bytes;
- old artifact qualification -> rebuilt bytes;
- publication success -> Deployment success;
- Release READY -> Deployment success;
- staging -> production;
- credential -> authority;
- artifact rollback -> data rollback;
- rollback plan -> rollback executed.

Also run historical/adoption compatibility and v4.1/v4.2 composition regressions.

### Contract
Produce integration evidence and closure inputs only. Version Closure still owns candidate freeze/full visible regression/Hidden Validation/Release Qualification.

### Implementation
Bind all evidence to exact integrated candidate SHA/tree and actual tested tuple. Carry unresolved P2/P3 or environment gaps explicitly into closure.

### Failure handling
Any unresolved P0/P1, required NOT_RUN/BLOCKED tuple or subject drift prevents a green closure input; do not manufacture Release readiness.

### Reference
Frozen Product §11/§15; L2 §7; current Version Closure/Release standards.