# Dependency & Toolchain Governance Standard

## 1. Purpose and authority

This standard is the normative owner for dependency and toolchain execution facts in ai-development-standard v4.1. It governs manifest/lock authority, dependency classification, toolchain compatibility/certification distinctions, dependency-risk disposition and change impact.

It does **not** own Validation, CI provider state, Review, Candidate Freeze or Release Qualification. Those remain with their existing standards. Dependency/toolchain facts feed those owners; they do not manufacture their states.

Machine payloads SHOULD use `schemas/dependency-toolchain-profile-v1.schema.json` and `schemas/dependency-risk-exception-v1.schema.json` when durable structured records are useful.

## 2. Repository authority and dependency sources

A repository or project MUST identify which manifests are authoritative for declared dependencies. Where an ecosystem has a lock/resolution artifact, the project MUST state whether it is authoritative, advisory or generated.

An Agent MUST NOT infer repository requirements from its own installed runtime, package cache, global tools or previous workspace. Local availability is execution evidence only.

When multiple manifests exist, authority and dependency-class scope MUST be explicit enough to avoid silently treating test/build/dev dependencies as runtime dependencies or vice versa.

## 3. Dependency identity, class, path and exposure

Security and change decisions MUST preserve, when material:

- package/component identity and resolved version;
- dependency class: `runtime`, `development`, `build`, `test`, `optional`, `platform`, `transitive` or project-defined `other`;
- dependency path/chain for transitive dependencies;
- exposure/applicability such as runtime-exposed, build-only, development-only, test-only, not-applicable or unknown;
- authoritative manifest and lock/resolution source.

A scanner severity alone MUST NOT erase dependency class/path/exposure or fabricate exploitability/applicability.

## 4. Toolchain dimensions are distinct

Projects MUST keep these facts distinct:

1. **compatibility requirement** — versions/ranges/floors that are supported by contract;
2. **supported line(s)** — maintained lines the project intends to support;
3. **preferred development version** — the normal developer/Builder choice;
4. **certification tuple** — an actually validated toolchain version × platform × validation profile;
5. **deployment identity** — the runtime/toolchain actually used by the deployed artifact/environment.

A preferred version does not narrow compatibility by itself. A certification tuple does not prove every compatible version. A deployment version does not rewrite repository requirements. An Agent-local version does not become any of these authorities by presence.

## 5. Install and resolution semantics

Projects SHOULD use reproducible/frozen resolution semantics when the ecosystem supports them and when the lock/resolution artifact is authoritative. The exact command is ecosystem-specific.

Examples include `npm ci`, Python installs from an authoritative lock, Rust `--locked`, or equivalent mechanisms. This standard does not prescribe one universal command.

If a project intentionally allows floating resolution, it MUST identify the authority and the resulting Validation Impact; the Agent MUST NOT silently convert a floating policy to frozen or vice versa.

## 6. Change policy

Dependency/toolchain changes MUST be classified by material effect, not merely file extension. At minimum consider:

- direct vs transitive change;
- runtime vs dev/build/test class;
- lock/resolution drift;
- toolchain compatibility or preferred-version change;
- build/runtime behavior impact;
- supply-chain/provenance source change;
- public contract or generated artifact impact.

Material dependency, lock, registry/source or toolchain deltas MUST participate in the existing `VALIDATION_IMPACT_DECISION` discipline from `VALIDATION_STANDARD.md`. Evidence reuse is forbidden when impact is affected or unknown.

## 7. Vulnerability applicability and disposition

A vulnerability finding MUST retain advisory identity, package/version, dependency class, path when relevant, exposure/applicability, severity, evidence references and disposition authority.

`severity` and `scanner result` are inputs, not release truth. A project MAY determine a finding is not applicable, accepted risk, deferred or remediated only with durable reasoning and authority appropriate to the project.

Unknown applicability MUST NOT be rewritten as not-applicable merely to clear a gate.

## 8. Dependency Risk Exception

A durable dependency-risk exception records accepted/deferred risk and review obligations. It is **not** Validation PASS, remediation evidence or Release Qualification.

The v1 machine contract intentionally permits statuses such as `accepted-risk`, `deferred`, `expired`, `closed-remediated` and `closed-not-applicable`; it MUST NOT encode `PASS`.

An exception SHOULD include owner/authority, reason, mitigation when any, review-by date, release scope and evidence references. Expiry/review dates MUST be re-evaluated rather than silently renewed by an Agent.

## 9. Provenance, registry, license and SBOM policy

Registry/source restrictions, provenance verification, license policy and SBOM requirements are project/risk-authoritative controls. They MAY be mandatory when frozen authority requires them, but this standard does not make every project adopt one registry, SLSA level, license allow-list or SBOM format.

Changing an authoritative source/registry or provenance policy is itself a material execution fact and may require Validation Impact review.

## 10. EOL, abandonment and support lifecycle

Projects SHOULD define how unsupported/EOL toolchains and abandoned dependencies are handled when material. EOL alone does not automatically define a Release verdict, but it MUST NOT be hidden when frozen authority makes support/security status relevant.

If the required compatible toolchain is unavailable on the executor, execution is truthfully `BLOCKED`; the Agent MUST NOT rewrite the project requirement to match its host.

## 11. Agent behavior

An Agent MUST:

- read repository/project authority before choosing versions;
- preserve dependency class/path/exposure in risk reasoning;
- distinguish compatibility, preferred, certification and deployment facts;
- avoid opportunistic unrelated upgrades unless Task authority permits them;
- report lock/resolution drift instead of silently accepting it;
- route material dependency/toolchain deltas through Validation Impact;
- record risk exceptions durably without calling them PASS/remediation.

An Agent MUST NOT:

- invent a supported version from its local environment;
- treat a scanner severity as exploitability proof;
- remove a dependency or regenerate a lock merely to obtain a green check when outside Task scope;
- convert an accepted-risk record into Validation/Release authority.

## 12. Fast Path and proportionality

Minimal/Fast-Path work need not materialize a full Dependency & Toolchain Profile when dependency/toolchain facts are immaterial and project authority does not require it. This does not permit ignoring a material manifest/lock/toolchain delta.

## 13. Failure handling

- Required compatible toolchain unavailable → execution `BLOCKED`, not project requirement mutation.
- Lock/manifest contradiction with unclear authority → `BLOCKED` pending authority resolution.
- Vulnerability applicability unknown → retain `unknown`; do not fabricate not-applicable.
- Required provenance/registry/license/SBOM evidence unavailable → preserve the owning gate as non-PASS according to its authority.

## 14. Boundary with other owners

- `VALIDATION_STANDARD.md` owns executed PASS/FAIL/BLOCKED truth and Validation Impact.
- CI standards own provider/executor/evidence-channel semantics.
- `RELEASE_STANDARD.md` owns release qualification.
- `CONFIGURATION_SECRETS_STANDARD.md`, `GIT_EXECUTION_STANDARD.md`, `WORKSPACE_ARTIFACT_STANDARD.md` and `EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` own their respective v4.1 concerns.
- T07 owns central manifest/adoption wiring; this standard does not edit those surfaces.
