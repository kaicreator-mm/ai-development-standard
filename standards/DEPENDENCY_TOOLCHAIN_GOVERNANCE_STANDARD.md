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

Reuse-sourced deltas follow the same materiality rule. Vendored or copied upstream source, a changed upstream revision or source path behind material already relied on, and an upstream license/NOTICE change are material deltas whenever the reused material remains in the tree or dependency chain. A docs-only/chore label or a Fast Path claim does not change this classification.

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

Reuse of outside work is additionally bound to exact provenance facts observed at a named upstream revision. The full identity floor below binds reuse-right-bearing material: directly reused or physically copied upstream source or artifacts — the H3 mode of `ARCHITECTURE_DESIGN_STANDARD.md` §15 — and any reliance on a changed upstream revision or drifted source path behind material already relied on. A cited upstream pattern (H1) and a disclosed re-specification (H2) carry the mode-matched provenance floors defined there: the cited upstream reference with a locally owned design for H1, and disclosed origin/derivation with a local contract plus differential tests for H2. This scoping never lowers the direct-copy rule: the moment upstream source or artifacts are physically taken into the tree in any claimed mode, the full floor below applies.

- the upstream repository, the full commit SHA relied on, and the material paths taken from it;
- the license file and NOTICE content as observed at that revision, not as remembered or as currently advertised;
- the project license-policy disposition authorizing the specific reuse mode.

These observations are revision-bound. Reliance on a different revision or a drifted source path is a new fact: it does not inherit the earlier license/NOTICE observation, and the earlier observation stays valid only as history. Re-observation and, where material, Validation Impact review are required before continued reliance.

Public availability of an upstream repository is not by itself evidence of a reuse right. Unknown rights, a conflicting license or a missing NOTICE keep the reuse disposition fail-closed with the project license/security authority; an Agent MUST NOT assume a lawful reuse basis from visibility, popularity or a README claim.

Wiring these reuse facts into shared L1/L2/L3 prompts, schemas or the manifest is central-surface work owned by the central wiring task (T11); this section records only owner-local duties and does not edit those surfaces.

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
- Missing full upstream identity, license/NOTICE observation or license-policy disposition for reused material → keep the reuse disposition non-authoritative (`BLOCKED`/unknown) with the project license/security authority; upstream visibility does not resolve it.
- Upstream source, path or behavior drift behind already-relied-on reuse → the prior permission is stale; fresh source/equivalence tests plus Validation Impact precede further reliance.
- A reuse record is provenance/currentness input only; it MUST NOT be promoted to Validation PASS, license legality or release permission.

## 14. Boundary with other owners

- `VALIDATION_STANDARD.md` owns executed PASS/FAIL/BLOCKED truth and Validation Impact.
- CI standards own provider/executor/evidence-channel semantics.
- `RELEASE_STANDARD.md` owns release qualification.
- `CONFIGURATION_SECRETS_STANDARD.md`, `GIT_EXECUTION_STANDARD.md`, `WORKSPACE_ARTIFACT_STANDARD.md` and `EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` own their respective v4.1 concerns.
- T07 owns central manifest/adoption wiring; this standard does not edit those surfaces.


## 15. v4.13 organization development environment defaults (prospective)

For an ADS adopter using the qualified v4.13+ contract, an organization MAY publish a versioned **Organization Development Environment Profile** as a machine-readable **defaults/hints** declaration. Its optional canonical JSON Schema is `schemas/organization-development-environment-profile-v1.schema.json`, with a **non-normative** sample at `examples/organization-development-environment-profile.json`. This profile is **not** the repository/project `dependency-toolchain-profile-v1` contract: it does not own authoritative project manifests, compatibility requirements, lock/resolution sources, certification evidence, deployment identity, or actual Host runtime inventory.

### 15.1 Effective precedence and source attribution

A standards consumer (including Tally) MUST resolve under the **project's effective immutable ADS revision**, and keep each winning/ignored value attributable to a current source reference:

1. Frozen project Product/Architecture and authoritative runtime ranges, package-manager constraints, manifests and lockfiles establish the **actual compatibility requirement**; an organization's preference cannot narrow, replace, or waive them.
2. A documented project-specific preference or exception MAY select its own compatible development toolchain. An exception MUST NOT waive mandatory source, security or actually required certification/test constraints.
3. Compatible organization `preferred_toolchains` apply only **when the project has not already selected a higher-authority compatible choice**. An out-of-range organization suggestion is **ignored/CONFLICT** with explicit reason, not auto-installed or silently used.
4. Host/runtime availability is an **observed fact**, not permission to rewrite source or assume project compatibility; if an eligible version is unavailable, the required execution remains `BLOCKED/NOT_RUN` under its existing owning Validation rules.
5. Certification and deployment are independent evidence dimensions from §4. An organization preferred version, example file, cache hint, successful syntax check or Agent-installed binary MUST NOT be reported as an actually certified tuple or Release/Validation PASS.

The consumer SHOULD produce a read-only trace naming `project_requirement_ref`, `project_preference_ref` if present, `org_profile_revision`, `observed_host_ref`, `effective_preferred_version` (when proved compatible) and `resolution=SELECTED|IGNORED_INCOMPATIBLE|UNKNOWN|BLOCKED` with human-readable reason. These are **illustrative projection fields**, not a new mandatory global Event/Gate status enum and not a new standard claim/activation authority. Where compatibility or precedence is materially unknown, do not guess from lexicographic version strings or mutable latest aliases. Project manifest/lock truth always remains unchanged unless separately authorized through the existing workflow.

### 15.2 Resource hints, secrets and execution boundary

`preferred_provider` (such as mise), `environment_hints` (cache, workspace, offline, mirrors and Host capability hints) are **advisory**, not mandatory tool choices, executable instructions, runtime certification or platform test evidence. Sharing should be limited to source-verified immutable Git objects and safely reconstructible downloads/caches; mutable virtual environments and dependency installations remain project/task-isolated unless independently proven safe.

Org policy and sample material MUST NOT embed tokens, credentials, private proxy authentication, bearer URLs or broader Host security exclusions. Store machine-local secrets only through existing secret owners and local references. Profile source/currentness MUST be immutable or otherwise bound to an auditable exact version at every consequential execution; a mutable configuration ref is not an accepted pin merely because a parser reads it. Actual Host Bootstrap, installer, Git mirror/Worktree/cleanup, Agent Skills/MCP, runtime selection and multi-project execution are **Tally (or another consumer implementation)**, not ADS standard repository features.

### 15.3 Bounded positive and negative interpretations

- **Positive:** project requirement `Node 22–24`, no higher-authority project preference, org preferred `24` → effective compatible *preference*, not proof that Node 24 is installed.
- **Positive:** project requirement `Python 3.11–3.13`, project preferred `3.11`, org preferred `3.12` → project preferred remains effective.
- **Negative:** project requirement `Node 18–20`, org preferred `24` → organization preference is ignored as incompatible; do not mutate the project lock or claim test PASS.
- **Negative:** Host happens to have Node 24 while project requires Node 20 → Host observation does not override project requirement; actual execution is held until compatible toolchain exists.
- **Negative:** no actual certification record → organization Profile cannot fabricate a `certification_tuple` or release-readiness claim.
- **Negative:** parser accepts an organization Profile with example cache/mirror hints → no automatic download, network access, system security exclusion, Git mutation, Task Claim or external authorization.

This section is additive and prospective. Existing §4 compatibility/preferred/certification/deployment distinctions, project-specific adoption rules, actual Claim/Review/Validation/Release gates and frozen consumer revisions remain in force.
