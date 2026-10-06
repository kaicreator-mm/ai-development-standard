# v4.7 Adoption / Migration Wiring

Status: **T09 NON-AUTHORITATIVE ADOPTION WIRING**

This document is a v4.7 convergence/adoption delta. It does not replace `standards/PROJECT_ADOPTION.md`, `docs/implementation/4.0.0/MIGRATION_ADOPTION_GUIDE.md`, any canonical semantic owner, Task Pack mutation authority, Validation, Review, Version Closure, or Release Qualification.

```text
AUTHORITY_EFFECT=NONE
MUTATION_AUTHORITY=NONE
GATE_EFFECT=NONE
```

## 1. Canonical bootstrap / discovery route

For a project pinned to v4.7, resolve only the surfaces needed for the current concern:

1. Read `.dev-standard/VERSION` and resolve the exact pinned ADS commit as required by `standards/PROJECT_ADOPTION.md`.
2. Use `standard-manifest.json#semantic_authorities` to discover the canonical owner for the concern. The manifest is discovery metadata; it is not mutation authority.
3. Read project specialization from `.dev-standard/PROJECT_OVERRIDES.md`. Overrides remain subordinate to higher authority and cannot weaken Frozen/Core requirements.
4. Read the discovered canonical owner before acting. Compatibility aliases remain read/compatibility routes and do not become owners.
5. Load optional supporting surfaces only when applicable to the concern. Examples include `registries/state-dimensions-v1.json` for qualified state/non-inference discovery and `scripts/resolve_standard_read_set.py` for derived read routing. Their presence does not make them mandatory project capabilities.
6. For implementation work, resolve the current Task/Issue and Task Pack; an Execution Pack, when present, remains subordinate to the Task Pack.

This route is intentionally progressive. A project is not required to instantiate every registry, profile, reducer, controller, or optional v4 capability merely because the pinned standard contains it.

## 2. Existing v4 project adoption

v4.7 is compatible wiring over the existing v4 adoption model. Existing projects SHOULD keep their current truthful adoption level and only add the v4.7 discovery route when useful.

- Keep the A0–A4 semantics and non-weakening rules owned by `standards/PROJECT_ADOPTION.md`.
- Keep the v3.4→v4 migration matrix and historical-evidence rules owned by `docs/implementation/4.0.0/MIGRATION_ADOPTION_GUIDE.md`.
- Do not relabel historical evidence, transfer PASS across exact subjects, or reinterpret old payloads merely to make them look v4.7-native.
- Preserve stable compatibility entry paths such as `standards/GITHUB_WORKFLOW.md` and `standards/VERSION_INTEGRATION_WORKFLOW.md`; the canonical owner relationship is discoverable through `standard-manifest.json`.
- Do not perform physical standard/reference path migration as part of T09.

## 3. PROJECT_OVERRIDES and Fast Path proportionality

`PROJECT_OVERRIDES.md` is a project specialization surface, not a second standards owner. For v4.7 adoption it SHOULD record only project facts and selections, while owner discovery remains in the pinned standard.

Optional/non-applicable capability stays optional/non-applicable. Fast Path proportionality remains intact across A0–A4: a small eligible change does not have to load or instantiate unrelated registries, profiles, Execution Packs, reducers, controllers, or orchestration capabilities. If higher authority requires a capability or gate for the concern, the project cannot use Fast Path or an override to remove it.

## 4. Compatible change vs future-major input

Use v4.7 compatible wiring when the change is additive, preserves canonical owners, keeps exact-subject/evidence meaning, preserves stable compatibility routes, and does not turn optional capability into a universal requirement.

When a requested change requires an incompatible authority hierarchy change, object/state collapse, destructive schema/wire replacement, historical evidence reinterpretation, exact-SHA meaning change, stable-path removal without compatibility, or mandatory adoption of a currently optional capability, do not smuggle it into v4.7. Record the evidence-backed concern in `docs/implementation/4.7.0/FUTURE_MAJOR_REGISTER.md` and route it to future-major planning.

The future-major register is planning input only; recording an item does not approve, reject, schedule, or implement it.

## 5. Validation / Review boundary

T09 focused tests may prove that the wiring is internally consistent, but test/CI success is not Validation, Review, Closure, or Release authority. The T09 candidate still requires independent exact-head/current-target integration Validation followed by a genuinely new Fresh Independent Review before merge, as required by the T09 Task Pack.

T07 remains the owner of unified semantic conformance for v4.7. T09 may keep that suite passing and point to its results, but it does not create a `CONVERGENCE_PASS` state or reinterpret T07 evidence.

## 6. Adoption checklist

For a v4.7 adoption/migration change, verify only the applicable items:

- exact standard pin resolves;
- canonical concern owner is discoverable through `standard-manifest.json#semantic_authorities`;
- project specialization is read from `PROJECT_OVERRIDES.md` without weakening higher authority;
- optional surfaces are loaded only when applicable;
- stable compatibility aliases continue to resolve;
- implementation mutation stays within current Task Pack authority;
- incompatible needs are routed to the future-major register rather than implemented silently;
- required Validation/Review gates remain separate from test/CI evidence.
