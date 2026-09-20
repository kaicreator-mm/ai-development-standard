# Validation Standard

## 1. Purpose and states

Validation proves behavior on an explicit subject and execution tuple. Every Gate uses exactly one state:

```text
PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE
```

`PASS` requires actual execution. `FAIL` means an executed required check did not meet acceptance. `BLOCKED` means a prerequisite/environment/tool prevents execution. `NOT_RUN` means it has not executed. `NOT_APPLICABLE` means the gate genuinely does not apply.

Workflow state, CI/provider health, dispatch state, candidate state, and release verdict are separate dimensions defined by `EXECUTION_ARCHITECTURE_STANDARD.md`.

## 2. Gate Authority

Mandatory gates must trace to, in priority order:

```text
Frozen PRD / Contract
→ Frozen Architecture
→ PROJECT_OVERRIDES
→ Task acceptance
→ Standard defaults
```

Historical workflows, old scripts/artifacts, or Agent preference do not create a mandatory gate.

## 3. Validation Tuple

The smallest platform-sensitive evidence unit is:

```text
<exact tested SHA>
× <real platform/environment>
× <runtime/toolchain>
× <validation profile>
```

A tuple proves only itself. Cross-build, another platform/toolchain, CI provider success, or an older SHA cannot be inferred as PASS for an unexecuted tuple.

Validation Reports use `schemas/validation-report.schema.json` when a machine payload is produced.

## 4. Validation ownership

Every Task/validation request SHOULD resolve a validation scope:

```text
concern | integration | closure
```

### concern

Use the smallest strict affected evidence: format/lint/typecheck/unit/contract/build subsets, affected integration checks, and any real platform/runtime gate intrinsic to the concern.

A normal leaf Task SHOULD NOT automatically run full repository regression, the complete OS/device matrix, all Critical Journeys, Hidden Validation, packaging, or unrelated sibling integration.

### integration

An explicit integration owner validates cross-component assembly, shared runtime/public wiring, package/dependency composition, and representative integration journeys.

### closure

The dependency-complete candidate owns full regression and the release-level matrix authorized by frozen scope: Critical Journeys, required real platforms, production build/package/install, external boundaries, Hidden Validation, and Release Qualification inputs.

Cost never weakens a required gate. If a platform gate is intrinsic to a host adapter Task, it remains concern-owned even when expensive.

## 5. Validation layers

Useful profiles include:

- Fast — deterministic format/lint/typecheck/unit/contract/basic build;
- Integration — real component composition and boundary behavior;
- Critical Journey — critical user/system outcomes;
- Hidden — independent scenarios unavailable to implementation context;
- Platform / Production Build — real OS/device/SDK/runtime/package;
- Minimal CI — low-cost clean-checkout independent sanity.

CI is an executor, not Release Authority. High-cost device/CJ/Hidden/packaging work normally belongs outside Minimal CI unless project authority explicitly says otherwise.

## 6. Exact-SHA evidence and drift

Evidence remains attributed to the SHA where it actually ran.

Distinguish:

```text
HEAD drift
BASE drift
MERGE-RESULT drift
CANDIDATE drift
```

### HEAD drift

A changed PR HEAD invalidates current-SHA evidence for affected required gates. Old evidence remains historical.

### BASE / merge-result drift

If the PR HEAD is unchanged but its target advances, do not automatically rewrite old evidence as PASS for the merge result.

A concern-specific expensive tuple MAY remain usable only through an explicit `VALIDATION_IMPACT_DECISION` proving `validation_impact=none`. The decision should identify, when relevant:

```text
validated_head_sha
base_sha_at_validation
current_target_sha
base delta / write-set comparison
merge_result_sha/tree or deterministic preview
validation_impact
evidence_reuse_basis
reviewer/controller attribution
```

Reuse is allowed only when the target delta does not affect relevant source/runtime behavior, tests/fixtures, dependency/lockfile/toolchain/build inputs, public contract/architecture semantics, shared integration wiring, artifact identity, or overlapping write sets, and the target delta has its own required disposition.

If impact is `affected` or `unknown`, rerun affected gates.

### Evidence-preserving successor

A successor commit may use the same explicit impact discipline. CI/workflow/config-only changes are not automatically evidence-preserving because they can alter execution semantics.

No event/report may claim a tuple executed on a SHA where it did not execute.

## 7. Tested checkpoint vs evidence-only head

When a report or evidence index is committed after execution, distinguish:

```text
tested_sha = actual executed commit
evidence_only_head = later evidence-recording commit
```

Evidence-only recording should preferably live in Issue/events/external evidence storage rather than mutate a frozen candidate.

## 8. CI execution channel vs Validation gate

The required Validation profile and its normal provider are different facts.

Provider/channel health may use:

```text
AVAILABLE / INFRA_BLOCKED / TIMED_OUT / CANCELLED
```

A stuck/pending CI provider is not candidate FAIL.

### Alternate executor substitution

If authority requires the profile and CI is merely its normal executor, an equivalent or stronger trusted clean executor MAY satisfy the profile when it records:

- exact SHA;
- clean checkout;
- equivalent required check set/entrypoints;
- material environment/toolchain identity;
- actual commands/results;
- independent execution context when required;
- the fact that the normal provider remained unavailable.

If authority explicitly requires a provider-specific attestation/environment, alternate execution cannot substitute; that requirement remains BLOCKED until resolved or authority changes.

Use `CI_INFRA_EXCEPTION` for the infrastructure fact. Do not change the provider UI/history to pretend it passed.

Known broken channels should not be retried indefinitely without new evidence that infrastructure changed.

## 9. CI execution and evidence

When CI is enabled, follow:

- `CI_EXECUTION_STANDARD.md` for provider/backend/checkout/runtime semantics;
- `CI_RUNNER_CAPABILITY_STANDARD.md` for routing inventory;
- `CI_EVIDENCE_STANDARD.md` for immutable evidence publication.

A Runner Capability Profile routes work only; actual run preflight and exact-SHA evidence win.

## 10. Blocker propagation

`BLOCKED` propagates only through real dependency edges. Continue all independent work.

A blocked macOS/device tuple may block Candidate Freeze while unrelated docs, another platform tuple, Hidden-pack preparation, or release-note preparation continues.

## 11. Evidence minimum

A useful Validation Report records:

```text
repository
tested_sha
candidate_sha when relevant
branch/ref as auxiliary metadata
execution host role/channel/provider state
platform/architecture
runtime/toolchain
validation profile + scope
exact command/entrypoint
exit code
key logs/evidence
state
validation impact/reuse basis when evidence composition is used
```

External CI evidence remains governed by immutable evidence identity/completion rules in `CI_EVIDENCE_STANDARD.md`.

## 12. Prohibited practices

- claiming PASS without execution;
- moving PASS from one SHA/platform/toolchain to another by assertion;
- using CI PASS as unexecuted platform/CJ/Hidden/packaging PASS;
- deleting/weaking required tests to clear a gate;
- changing a required gate to optional to obtain READY;
- unlimited retries/timeouts that mask deterministic defects;
- treating `latest.json`, evidence publication completion, artifact presence, or runner capability inventory as Validation PASS;
- treating infrastructure unavailability as product FAIL or PASS.
