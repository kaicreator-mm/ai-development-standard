# Observability & Runtime Evidence Reference

Non-normative guidance for `OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md`.

## Observation tuple

A material observation can be represented as:

```text
artifact_ref
deployment_result_ref
environment_ref
observation_window_ref
signal_class
signal_source_ref
observation_ref
```

Use the existing v4.4 artifact/deployment/environment identities where applicable rather than creating parallel identities.

## Distinct signal examples

- readiness: can this instance receive intended traffic/work?
- liveness: is the process/service alive enough for its owner-defined meaning?
- performance/resource: latency, saturation, utilization or equivalent;
- failure/error: exceptions, failed requests, error budget inputs, crashes;
- business/domain: owner-defined functional outcome evidence.

One dimension does not automatically prove another.

## Negative examples

```text
Deployment succeeded -> runtime healthy
no alert fired -> runtime healthy
metrics backend connected -> product works
staging observation -> production observation
raw credential in log -> acceptable durable evidence
```

## Project specialization

Projects may choose OpenTelemetry, vendor agents, logs, traces, metrics, probes or domain-specific evidence. These are mechanisms, not universal normative owners. Thresholds, SLOs, severity and retention should be recorded in Product/project authority when material.
