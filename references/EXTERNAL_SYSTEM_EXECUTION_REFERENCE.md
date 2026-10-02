# External System Execution Reference

This document is non-normative guidance for `EXTERNAL_SYSTEM_EXECUTION_STANDARD.md`.

## 1. Fidelity examples

A project may describe a dependency with dimensions such as:

```text
system_id=payments-api
dependency_fidelity=provider-sandbox
environment_ref=payments/project-A/sandbox
state_scope=isolated-test-account
side_effect_authority=create-test-charge-only
credential_ref=ci:payments-sandbox-token
```

Another provider may use entirely different labels. The requirement is semantic clarity, not a fixed global enum.

## 2. Mock versus real service

Valid statement:

```text
mocked HTTP client contract tests PASS
```

Invalid escalation:

```text
therefore real provider authentication/rate-limit/network journey PASS
```

The mock result may satisfy a concern-level unit/contract requirement while a real-service gate remains NOT_RUN/BLOCKED.

## 3. Sandbox versus production

If acceptance requires production/live environment behavior, sandbox PASS cannot be relabeled production PASS. If frozen authority explicitly says provider sandbox is the required fidelity, then production execution is not automatically required.

## 4. Read versus write

A read-only database connection can prove query behavior but cannot prove create/update/delete side effects. A write-capable token does not authorize mutation by itself.

Before write execution, bind:

```text
target account/tenant/environment
allowed operation class
scope/record namespace when relevant
cleanup/rollback expectation
credential reference
```

## 5. Tenant mismatch

Required:

```text
tenant=customer-sandbox-A
```

Observed credential authenticates to:

```text
tenant=customer-sandbox-B
```

Correct action: do not substitute the evidence. Resolve authority/credential/environment or report BLOCKED.

## 6. Infrastructure blocker examples

Typical external blockers:

```text
DNS resolution unavailable
TLS handshake blocked by network policy
provider 503 outage
credential expired
account not provisioned
HTTP 429 quota exhausted
remote Build Host offline
```

These describe execution availability. They are not automatically product defects.

## 7. Product failure example

If the required service is reachable with valid credentials and the product sends an invalid request that violates the documented contract, an observed 400/contract failure may be a real product FAIL. Classify from the evidence; do not hide it as infrastructure.

## 8. Bounded retry example

Safe policy:

```text
GET-like idempotent request
max_attempts=3
backoff=1s,2s
per-attempt timeout=10s
overall deadline=30s
retry only network reset / 429 / provider 5xx
```

Unsafe policy:

```text
retry forever until green
```

For non-idempotent write requests, require an idempotency key/deduplication guarantee or explicit human/controller authorization before automatic retry.

## 9. LLM example

A local fake can validate prompt assembly and response parsing. A real provider sandbox/test key can validate authentication, transport and provider behavior. Neither proves production quota/account behavior unless that fidelity is actually required and executed.

Record provider/model/environment/account identity when those facts are material to the result.

## 10. Browser example

A static HTML fixture can prove parser/selector behavior. A real browser against a local test server can prove browser integration. A logged-in remote browser journey against a provider can prove a higher-fidelity flow only for the actual account/environment exercised.

## 11. Build-host example

A Windows local compile does not prove a required Ubuntu Build Host/package tuple. Conversely, a remote Build Host outage is an infrastructure blocker when the host-specific gate cannot execute; it is not evidence that the product fails to build.

## 12. Cleanup example

A test creates external sandbox objects with prefix `t197-<run-id>`. The Task has authority to delete objects with that owned prefix after execution. It does not have authority to bulk-delete unknown shared sandbox records.
