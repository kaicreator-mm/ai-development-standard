# v4.3 Implementation Profile Adoption Reference

Status: **Reference guidance — subordinate to Frozen/Core authority, `standards/PROJECT_ADOPTION.md`, `profiles/README.md`, and project-specific authority**

Purpose: give projects a deterministic, lightweight way to record v4.3 language/archetype profile selection in `.dev-standard/PROJECT_OVERRIDES.md` without creating a new resolver, lifecycle state machine, or duplicate Task object.

## 1. PROJECT_OVERRIDES profile block

When implementation-profile selection is material, projects MAY add the following section to `.dev-standard/PROJECT_OVERRIDES.md`:

```text
## Implementation Profiles (v4.3)

- Language profile refs: <explicit pinned profiles/languages/*.md paths | [] — NOT_APPLICABLE: reason>
- Archetype profile refs: <explicit pinned profiles/archetypes/*.md paths | [] — NOT_APPLICABLE: reason>
- Applicability evidence refs: <Product / Architecture / repository manifest / build-runtime facts>
- Specialization / strengthening: <project-specific mapping changes | none>
```

Use explicit paths from `standard-manifest.json` section `profiles` at the exact pinned standard revision. Do not copy profile prose into PROJECT_OVERRIDES merely to make it project-local.

## 2. Selection and authority rules

1. Frozen/Core authority remains authoritative.
2. Profiles are mapping/default layers. `PROJECT_OVERRIDES` MAY select, specialize or strengthen them, but MUST NOT weaken Frozen/Core, Task, required Review, required Validation or release authority.
3. Applicability comes from durable project facts. File order, directory/glob order, IDE discovery, Agent-local compiler/runtime availability and Agent preference are not authority.
4. If applicable profile defaults conflict materially and project authority does not resolve the conflict, the work is `BLOCKED` and routes to the owning Product/Architecture/project authority. Discovery order MUST NOT choose a winner.
5. Task Pack / Execution Pack profile pointers consume the resolved project selection; those packs do not become an independent profile resolver.
6. No field in this reference authorizes a repository-wide v4.7 resolver or a new lifecycle state machine.

## 3. Progressive adoption / migration

Existing projects and historical Task/Validation/Review evidence retain their original subject, status and authority. v4.3 profile adoption is prospective: add profile selection when an implementation-profile decision becomes material; do not rewrite historical evidence or synthesize retroactive profile records.

Fast Path and genuinely non-material changes remain lightweight and MAY omit this block when no implementation-profile decision is material. Reduced ceremony does not weaken applicable authority.

Projects already using `.dev-standard/PROJECT_OVERRIDES.md` can adopt this block independently of their v4 A0–A4 automation level. Profile selection describes implementation mapping; the v4 adoption level continues to describe execution/assurance automation surface.
