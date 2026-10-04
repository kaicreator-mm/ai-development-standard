# Library Archetype Profile

```yaml
profile_id: archetype.library
profile_version: 1
profile_kind: archetype
applicability: public or reusable library/API concerns are material
core_owner_refs:
  - standards/IMPLEMENTATION_QUALITY_STANDARD.md
  - standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md
source_or_ecosystem_refs: project public API/IDL, package/source layout, supported consumer matrix and tests
project_check_mappings: project-selected public-contract, install/import and compatibility checks
high_risk_semantics: exported API changes, consumer compatibility, packaging identity, generated client/source boundaries
compatibility_notes: consumer population and baseline must be explicit when material; publication is optional
```

Status: v4.3 subordinate archetype mapping. This profile is not Product Architecture and does not require every library to be publicly published or installed via one package manager.

## Applicability

When material, map public/exported interface and consumer baseline, language-appropriate package/module manifests, generated clients, import/install paths and versioned compatibility/deprecation concerns into their existing normative owners. A green local unit test is not proof that a previously supported external consumer is compatible. Source-only or internal libraries may truthfully have Distribution NOT_APPLICABLE; packaging, publication and Deployment are separate conditional concerns.

## Composition and checks

Compose independently with an applicable language profile. Project-specific export, package identity and consumer checks come from durable repository/project authority; recommended defaults are not mandates. PROJECT_OVERRIDES may specialize mappings without weakening Frozen/Core or redefining compatibility, Testing, Validation or Release results. Language/archetype conflicts fail closed to the owning project/architecture decision; profile discovery order does not choose a winner.

## Failure handling

Unknown consumer baseline or public-contract applicability remains UNKNOWN and requires an owning decision or bounded Validation. Fast Path may omit non-material packaging/publication evidence; no library profile grants mutation, promotion, publication, Deployment or Release authority.
