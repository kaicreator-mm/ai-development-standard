# ai-development-standard Profile Framework

Status: **Profile framework / mapping contract — v4.3**

Profiles translate language- and archetype-specific ecosystem facts into the language-neutral requirements owned by normative standards. Profiles are not independent lifecycle or Product/Architecture authorities.

## 1. Profile identity

Every material profile SHOULD expose a stable header equivalent to:

```text
profile_id
profile_version
profile_kind = language | archetype
applicability
core_owner_refs
source_or_ecosystem_refs
project_check_mappings
high_risk_semantics
compatibility_notes
```

Profile identity/version describes the mapping document. It does not replace the pinned ADS revision, project version, toolchain profile, lockfile, or Product authority.

## 2. Profile kinds

v4.3 initial framework supports two mapping layers:

```text
language profile
archetype profile
```

Language profiles map neutral implementation-quality requirements to ecosystem facts such as manifests, lockfiles, compilers/runtimes, package/build/test conventions and generated-source boundaries.

Archetype profiles map neutral requirements to project-shape concerns such as library, service and CLI boundaries.

A profile MUST NOT claim that its examples are universally required by every repository in that language/archetype.

## 3. Deterministic composition

The effective project guidance is composed conceptually as:

```text
Frozen/Core normative authority
        + applicable language profile mapping
        + applicable archetype profile mapping
        + PROJECT_OVERRIDES specialization/strengthening
```

Composition rules:

1. Frozen/Core normative authority always remains authoritative.
2. Profiles map/default; they do not weaken or replace Core requirements.
3. Language and archetype profiles are independent axes. A repository may have one, both, or neither when genuinely non-applicable.
4. `PROJECT_OVERRIDES` may select, specialize or strengthen applicable mappings, but MUST NOT silently weaken Frozen/Core authority.
5. If two applicable profile defaults conflict materially and project authority does not resolve the conflict, composition fails closed to an explicit planning/architecture decision. File/discovery order MUST NOT choose a winner.
6. A project may document an explicit non-applicable profile axis with rationale rather than generating empty profile artifacts.

## 4. Applicability

Applicability is determined from durable project facts such as Product/Architecture choice, repository manifests, build/runtime boundaries and explicit project overrides.

The following are not sufficient authority by themselves:

- whatever compiler/runtime happens to be installed on one Agent host;
- IDE detection;
- an Agent's preferred ecosystem tool;
- a generated file appearing in a working tree;
- a popular community convention not adopted by the project.

Agent-local tooling is execution capability/evidence, never profile authority.

## 5. Required vs recommended mappings

Profiles may distinguish:

```text
required mapping
recommended default
conditional mapping
reference/example
```

A `required mapping` is valid only when it maps an already-applicable Core requirement or an explicit project requirement. Profiles cannot manufacture a new global requirement merely by labeling a tool/convention required.

Recommended defaults are overrideable by applicable project authority when doing so does not weaken Core obligations.

## 6. Toolchain / manifest mapping

A language profile may identify canonical ecosystem facts such as:

```text
manifest / module descriptor
lock / dependency resolution artifact
toolchain/runtime identity
build/test/lint/type-check entrypoints
generated-source conventions
package/public API boundaries
```

The profile points to the owning Dependency/Toolchain, Testing, CI, Secrets or other standards rather than duplicating their semantics.

## 7. Project-owned checks

Profiles may suggest or map project-owned checks, but the executable project/CI configuration remains the source of truth for what actually runs.

`profile says check X -> CI X passed` is a forbidden inference.

Likewise, `tool installed -> project selected that tool` is forbidden.

## 8. Fast Path / non-applicability

Small or non-code changes MUST NOT be forced to instantiate language/archetype profile records when no implementation-profile decision is material.

Fast Path reduces ceremony, not authority: if a change materially depends on a language/runtime/public API/archetype boundary, the applicable profile mapping may still be needed.

## 9. Profile discovery

v4.3 establishes the stable directory convention:

```text
profiles/
  README.md
  languages/
  archetypes/
```

This file defines profile composition only. It is **not** the repository-wide owner/applicability resolver. Canonical concern-to-owner resolution and broader progressive disclosure belong to v4.7.

## 10. Conflict / failure handling

Fail closed when:

- profile applicability is ambiguous and material;
- profile mappings conflict with Frozen/Core authority;
- two profiles prescribe incompatible defaults without project resolution;
- a requested mapping would require changing Product/Architecture authority;
- a repository-wide resolver feature is required.

Route the issue to the owning Product/Architecture/project authority or v4.7 where applicable; do not resolve by file order or Agent preference.
