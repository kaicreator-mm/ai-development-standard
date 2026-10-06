# Observability & Runtime Evidence Standard

Status: **Normative — v4.5**

## 1. Purpose

This standard governs runtime observation evidence after deployment/activation. It does not create a universal runtime-health Gate and does not redefine Deployment, Validation or Release results.

## 2. Runtime evidence is a distinct dimension

Deployment success proves only the deployment result it owns. It MUST NOT be interpreted as runtime health.

```text
DEPLOYMENT_SUCCEEDED != RUNTIME_HEALTHY
```

Likewise, runtime evidence cannot rewrite the historical Deployment or Release result that preceded it.

## 3. Signal dimensions

Where material, health/readiness, liveness, performance/resource, error/failure and business/domain signals MUST remain distinguishable. A project may map or extend signal classes according to its Product/Architecture needs.

This standard does not mandate one telemetry vendor, backend, signal transport, dashboard, SLI/SLO, severity ladder or threshold.

## 4. Observation identity

A material runtime observation MUST identify enough of the observed subject to prevent evidence substitution. As applicable, bind:

- exact artifact/content identity;
- deployment/result reference;
- environment/tenant/account identity;
- observation window/time reference;
- signal source/backend reference;
- configuration/runtime profile when it materially affects meaning.

v4.5 reuses v4.4 artifact/deployment/environment identity. It does not mint a second Deployment object.

## 5. Availability and silence

Signal/backend availability is capability, not product truth. Missing, quiet or unavailable telemetry MUST NOT be upgraded into healthy behavior.

```text
no alert observed != healthy
backend reachable != runtime healthy
signal source unavailable != NOT_APPLICABLE
```

A required but unavailable observation remains truthful `NOT_RUN`/`BLOCKED` under the owning workflow.

## 6. Privacy and sensitive data

Ordinary durable telemetry evidence MUST NOT require raw credentials, tokens, secrets or unapproved PII. Prefer stable refs, classifications, redaction and bounded aggregates. A diagnostic exception requires explicit applicable authority and still does not make secret values ordinary evidence.

## 7. Evidence boundaries

Runtime evidence may support later incident, engineering-feedback or release decisions, but those owners issue their own conclusions. Runtime observations do not create Validation PASS/FAIL, Release READY, Deployment result or Task state.

## 8. Failure handling

Unknown subject identity, material environment mismatch, unavailable required signals or ambiguous observation provenance fails closed. Project-specific thresholds/retention/severity stay with Product/project authority rather than being invented here.
