# v4.5 T05 — Runtime Observation Conformance Dogfood

Evidence class: **COMMITTED FIXTURE / SOURCE-BOUND CONFORMANCE ONLY**. This is not live production telemetry, a real runtime-health verdict, Validation PASS, Release READY, or Task Done.

## Authority and execution

- Issue: #274; Task Pack: `docs/implementation/4.5.0/task-packs/T05_runtime_observation_conformance.md`.
- Frozen L3: `docs/implementation/4.5.0/L3_REFERENCE_PACKS.md#t05--runtime-observation-conformance`.
- Normative owner: `standards/OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md` (T02 merged).
- Existing machine contract consumed, **not modified**: `schemas/runtime-observation-context-v1.schema.json`.
- Run from repository root: `python3 scripts/test_v45_runtime_observation_conformance.py` (Python 3 stdlib only).
- `cases.json` uses a fully specified positive baseline plus copied negative deltas. The script expands those deltas, checks source-owner anchors and evaluates 23 named cases. These are fictitious refs, times and signals. They establish fixture-oracle behavior only; no actual signal source was contacted.

## Coverage and non-substitution

The fixture suite binds exact artifact, deployment, environment, configuration-profile, source and ordered time window. It differentiates health/readiness, liveness, resource/performance, error/failure, business/domain and project-defined signal labels. It exercises wrong identity/source/config/window and missing identity, required source unavailable, reachable-but-unobserved backend, quiet/no-alert without health evidence, deployment vs runtime, health vs business, telemetry vs Validation/Release/Task authority, privacy-safe opaque references, qualified historical evidence and prohibited retroactive PASS. The machine contract only stores bounded identity/refs; the script's `FIXTURE_CONFORMANT`, `REJECT_INFERENCE`, `NOT_RUN` and `BLOCKED` values are **test-oracle categories, not new normative ADS result states**.

Important limitation: this stdlib test is a focused semantic fixture harness, **not** a substitute for a complete Draft 2020-12 schema validation suite or host telemetry validation. Its fake timestamps and refs never establish product runtime behavior. Real signal availability and project-specific health thresholds are deliberately not inferred. Historical adopted data may be cited with explicit qualification but cannot be retroactively upgraded.

## VALIDATION_REQUEST — distinct independent LOCAL_VALIDATOR

Status: **NOT_RUN / BLOCKED pending real runtime selection and exact-subject evidence**. Do not interpret fixture completion, CI availability, Deployment SUCCESS, telemetry silence, or a backend reachable response as runtime health.

Controller must choose whether the frozen product acceptance actually requires a real runtime tuple. If required, appoint an **independent** Local Validator (not this Builder or the Fresh Reviewer) and bind before execution:

- `candidate_pr_head` and `candidate_tree`: actual final T05 PR SHA/tree at validation start;
- `actual_target`: then-current `version/v4.5.0` commit SHA (rebind if T03 or any sibling merges);
- `exact_artifact`: digest/content identity of the actually deployed/runtime-tested artifact;
- `deployment_result_ref`: actual v4.4 deployment result identity (not an inferred success);
- `environment_ref`: actual account/tenant/environment identity and approved runtime configuration/profile ref;
- `observation_window`: absolute start/end timestamps, timezone and clock/provenance;
- `signal_source_ref`: actual backend/collector identity and coverage/availability for each material dimension;
- `scope`: project-specific required health/readiness, liveness, resource/performance, error/failure and business/domain dimensions with product-owned thresholds/applicability;
- `privacy`: approved redacted, secret-ref/PII-safe durable evidence refs and access authority;
- `procedure`: obtain actual per-dimension raw-source-bound evidence, induce/observe permitted negatives for quiet/unavailable required signals, check source/window conflicts, capture command, exit, environment, logs/digests and regressions.

If a project has no persistent deployed runtime, its Product authority may justify `NOT_APPLICABLE`; absence of a selected runtime is **not itself** such authority. On an unavailable required signal, remain `NOT_RUN/BLOCKED`. Only a different, genuinely NEW READ-ONLY Reviewer may conduct the required Fresh Independent Review after current exact-HEAD and actual-target evidence exists. Only Controller may authorize expected-head merge. No norm/source, manifest, Golden, CI, frozen authority or sibling scope is altered here.
