# Service Archetype Profile

```yaml
profile_id: archetype.service
profile_version: 1
profile_kind: archetype
applicability: long-running or request/event service boundaries are material
core_owner_refs:
  - standards/IMPLEMENTATION_QUALITY_STANDARD.md
  - standards/CONFIGURATION_SECRETS_STANDARD.md
source_or_ecosystem_refs: project service contract/runtime/configuration/deployment and external-system facts
project_check_mappings: project-selected interface, runtime, integration, deployment and observability checks
high_risk_semantics: public error contracts, external side effects, configuration/secret refs, deployment vs runtime observation
compatibility_notes: production rollout and runtime health evidence are separately applicable concerns, not universal service requirements
```

Status: v4.3 subordinate archetype mapping. A service profile does not prescribe HTTP, containers, cloud deployment, a telemetry vendor or a universal SLO.

## Applicability

Map the project's actual request/event contracts, API error behavior, runtime/worker lifecycle and relevant external-system boundaries to existing owners. Where material, map configuration and secret references without ordinary raw-secret persistence. A service may be development-only, embedded, local or simulated: production Deployment is not mandatory merely because the service archetype applies. A sandbox service test cannot substitute for a real external environment tuple when one is required.

## Runtime, deployment and evidence separation

A successful build/test is not a successful rollout; Deployment success is not automatically runtime healthy. Applicable deployment identity, external-system fidelity, runtime observation and incident/recovery evidence stay with their owners. Profile-selected default checks can reference live readiness/liveness/business signals only when project facts make them material; never synthesize Validation PASS, Release READY or Deployment SUCCESS from profile availability.

## Composition and failure handling

Compose with the applicable language profile and non-weakening PROJECT_OVERRIDES. Product/Architecture/project authority decides service topology and required environments; profile file order cannot resolve conflicting assumptions. Unknown production access, side-effect authority or required runtime fidelity remains UNKNOWN/BLOCKED pending an explicit owner decision or exact-tuple Validation. Fast Path may omit genuinely non-applicable rollout/telemetry work.
