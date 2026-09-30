# v4.4 T06 — Distribution / Deployment Conformance & Dogfood

Status: **BUILDER FIXTURES PREPARED, EXECUTION EVIDENCE NOT YET ATTESTED**. This file is not a real external registry/production Deployment Result, required Validation PASS, Review PASS or Version Closure.

## Owner and test subject

Canonical Task #265, Frozen v4.4 T06 Task Pack. `scripts/test_v44_distribution_deployment_conformance.py` owns a deterministic local conformance experiment: build two different bytes under a mutable channel, publish one to an isolated temporary filesystem, then execute `sandbox_service.py` as a separate **real local subprocess** and probe a real `127.0.0.1` HTTP health endpoint for the exact digest and `sandbox:local-1` identity. Its Deployment Plan/Result examples are tested only against the existing T01 `deployment-plan-v1` / `deployment-result-v1` schema and are namespaced `DEPLOYMENT_*` domain facts for a **sandbox**, not real infrastructure deployment claims. `cases.json` identifies 9 positive/negative scenarios; its examples are fixture declarations, not prior PASS records.

## What the focused test is intended to prove after actual execution

- A repointed mutable channel/alias does not preserve immutable bytes or old qualification.
- Temporary publication is distinct from launching a service and probing the deployed exact artifact.
- A Plan alone does not issue a Result; actual separately observed loopback process + artifact digest + target + explicitly test-scoped sandbox authority are all required even for the **sandbox-only** illustrative success.
- Result enum preserves failed, partial, rolled-back, blocked and not-run distinctions; no generic PASS/READY/Release claim.
- Sandbox/staging observations cannot be reused for production target; tool and credential capability alone does not confer side-effect authorization.
- Rollback plan is not rollback execution; artifact rollback never proves separate v4.2 migration/data rollback.

## Explicit unexecuted dimensions

An isolated temporary directory is **not** an external registry. A Python loopback subprocess is **not** a cloud/containerized production rollout. The repository standard does not mandate one external provider, cloud account, real customer environment or deployment for projects where deployment/distribution is non-material. Therefore external-publication and real production tuples are `NOT_RUN/NOT_APPLICABLE` **only under owning project/Frozen applicability decisions**; an absent provider must never be assigned `NOT_APPLICABLE` solely to obtain a green result. Real external-boundary tuples become a dedicated exact-subject Validation Request if required by an adopting project's authority.

## Required independent gates

1. Wait for the final PR exact HEAD and verify-standard generic CI; that CI may omit the new T06 focused script.
2. Separate clean LOCAL_VALIDATOR must record exact PR HEAD/base/live version target, worktree clean before/after, host/Python/loopback capability, full command outputs/exit/test counts for `python scripts/test_v44_distribution_deployment_conformance.py`, owner suites and `python scripts/verify_standard.py`. If real loopback environment is unavailable, record `BLOCKED` for the requested profile; never assert test success from code inspection.
3. Distinct NEW high-capability READ-ONLY Fresh Independent Review must assess T06 scope/actual run fidelity and outstanding real external tuples, P0–P3 and exact-currentness; only thereafter expected-head merge. T07/T08 and Version Closure are separate owners.
