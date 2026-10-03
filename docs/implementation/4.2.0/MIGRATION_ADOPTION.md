# v4.2 Evolution Governance — Migration & Adoption

Status: **adoption guidance; non-authoritative summary of Frozen v4.2 owners**

v4.2 adds two independently owned evolution concerns:

- **Interface & Compatibility Governance** — contract baseline/candidate identity, change operations, compatibility dimensions, consumer/window evidence, deprecation/removal obligations.
- **Data & Migration Governance** — directional source→target persistent-state transition identity, fresh-install vs upgrade/recovery distinction, environment applicability and recovery evidence.

The canonical normative rules remain in their standards. This document is discovery/adoption guidance and MUST NOT be treated as a second semantic owner or mutation authority.

## Adoption by materiality

Create compatibility or migration evidence only when the project change materially invokes the concern.

Examples:

- documentation-only/internal edits with no relied-upon interface or state transition need not create empty v4.2 records;
- a public schema/API/CLI contract change should identify the exact baseline/candidate and material compatibility dimensions;
- a persistent-state version transition should distinguish source→target upgrade from fresh installation and bind recovery/runtime evidence when material.

Fast Path reduces non-material ceremony. It does not turn a material compatibility or migration concern into `NOT_APPLICABLE` merely to avoid evidence.

## Existing projects and historical evidence

v4.2 is prospective and additive inside v4:

- historical v4 payloads and evidence retain their original subject identity and meaning;
- optional v4.2 references do not become retroactively required on old records;
- old evidence MUST NOT be relabeled as compatibility/migration PASS merely because v4.2 now exists;
- a new exact SHA, new consumer population, new source/target state, or materially different runtime requires evidence applicable to that new subject.

## Owner boundaries

Do not infer across owners:

```text
schema/checker PASS != behavioral/source/consumer compatibility
fresh install PASS != upgrade PASS
migration file exists != migration executed
compatibility/migration PASS != Validation PASS
Validation PASS != Release READY
Release READY != Deployment success
credential/tool available != side-effect authority
```

Deployment rollout/result semantics remain outside v4.2 and belong to the v4.4 Deployment owner when applicable. v4.2 migration recovery may describe persistent-state recovery requirements/evidence, but it does not own deployment orchestration.

Testing, Validation and Release remain their existing authorities. Machine contracts and Golden examples are evidence/discovery surfaces; they do not grant mutation authority.

## Project override profile

Projects MAY record a lightweight Evolution Governance profile in `.dev-standard/PROJECT_OVERRIDES.md`:

```text
evolution.compatibility = <materiality-driven | always-evaluate | project-specific stronger rule>
evolution.compatibility_window = <project policy/ref | determined per material change>
evolution.migration = <materiality-driven | always-evaluate | project-specific stronger rule>
evolution.runtime_evidence = <required when material | stricter project rule>
```

These are project applicability/defaults only. They MUST NOT weaken Frozen Product/Architecture/Task authority or replace the two v4.2 normative owners.

## Failure handling

If the canonical contract, consumer population, source/target state, runtime applicability, or required evidence is unknown, preserve the uncertainty and route to the owning concern. Do not normalize missing evidence into compatibility, successful migration, Validation PASS, Release READY or Deployment success.
