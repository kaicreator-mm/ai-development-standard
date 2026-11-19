# Validation Standard

## 1. Purpose and states

Validation proves behavior on an explicit subject and execution tuple. Every Gate uses exactly one state:

```text
PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE
```

`PASS` requires actual execution. `FAIL` means an executed required check did not meet acceptance. `BLOCKED` means a prerequisite/environment/tool prevents execution. `NOT_RUN` means it has not executed. `NOT_APPLICABLE` means the gate genuinely does not apply.

`NOT_APPLICABLE` is an authority-derived determination about applicability, not an executor convenience. It MUST NOT be produced from cost, effort/turnaround, change size/file count, a docs-only or mechanical appearance, Agent/model confidence, historical habit, or the absence of an objection. When applicability is `UNKNOWN` or contradictory, a required gate does not become `NOT_APPLICABLE`: it remains not satisfied (`NOT_RUN`/`BLOCKED`) and routes to the owning authority under the gate authority rules of `DEVELOPMENT_WORKFLOW.md`.

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

Before Validator execution the exact-SHA dispatch rule MUST hold:

```text
requested_head_sha == current PR HEAD
```

Otherwise the outcome is `HEAD_DRIFT`: the dispatch is stale/superseded, the validator MUST NOT execute it as PASS evidence and MUST NOT silently switch to the new HEAD. A new candidate requires a new dispatch identity.

A changed PR HEAD invalidates current-SHA evidence for affected required gates. Old evidence remains historical; PASS is never rewritten onto a successor SHA.

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

### Local-equivalent-first: prove the profile once (v4.19 successor)

**Default execution choice:** When the current authorized Builder/Validator/Agent environment can actually execute the complete required validation profile for the current subject, it SHOULD execute that profile there and publish its real evidence. Once the same exact-SHA, scope, target/toolchain and required independence have been proved, a second CI run **MUST NOT** be requested merely for ceremony, redundant verification or to obtain a provider-branded green badge. CI is an execution channel, **not an additional Gate by default**. This is independent of whether CI is healthy or pending; it is not only a CI-outage exception.

Before requesting a CI run, the executor/controller MUST check the applicable frozen/project Task/Release authority for: the actual required check set; the exact subject/SHA and environment tuple; and whether an independent executor, provider-specific attestation, branch-protection status context, or real Host/device/platform is separately required. The minimal decision is:

```text
profile complete + valid same-subject evidence + no independent/provider CI requirement
  → reuse PASS evidence; no duplicate CI invocation
profile complete + equivalent current executor + no independent/provider CI requirement
  → execute once here, record actual PASS/FAIL; no duplicate CI invocation
profile incomplete, wrong SHA/tuple, or necessary independence absent
  → run the missing required checks in a capable environment
explicitly required provider/status/independent CI
  → perform or truthfully report that distinct requirement; local PASS cannot satisfy it
```

For final Task/PR/Release evidence, local execution MUST preserve the actual tested commit SHA (and current PR HEAD/base where relevant), a clean/reproducible source and dependency input, required commands/checks with exit codes, OS/runtime/toolchain/Target, and artifact/result references; independent execution MUST remain independent when so required. Development checks against an uncommitted worktree are useful feedback but are not automatically an exact-SHA final Gate PASS. The report belongs in the **source GitHub Task Issue** for other Agents to retrieve; the version Master indexes the verified Task result. Prior matching immutable evidence SHOULD be reused instead of rerunning the same commands.

**Truthful states:** local profile PASS remains local profile PASS; an unexecuted CI provider stays `NOT_RUN` or its actual `pending` state. `CI_NOT_REQUESTED_EQUIVALENT_LOCAL_PASS` MAY appear as a **descriptive execution decision**, never as a new validation Gate state or provider SUCCESS. No required check is changed to `NOT_APPLICABLE` merely to avoid CI. A failing local required check stays FAIL, not replaced by an unexecuted CI green claim.

**Non-substitutable exceptions:** if current frozen/project authority truly requires a named provider/check, independent clean runner, branch-protection required status, Release-owned attestation, Hidden Validation or another real platform/Host tuple, those distinct requirements remain enforceable. A GitHub required context cannot be made green by a local receipt, and a pending provider is not a PASS. Change the project profile/branch rules only through prospective authorized governance, never as an ad hoc waiver for an in-flight candidate. Existing ADS pins and previously frozen gates are not retroactively changed.


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

## 9. Validator dispatch and the version-scoped Validation Handoff Queue

A Validator executes under a dispatch with role `validator` and an execution profile (`LOCAL_VALIDATOR / PLATFORM_VALIDATOR / CLOSURE_VALIDATOR`), defined by `schemas/dispatch.schema.json` and `EXECUTION_ARCHITECTURE_STANDARD.md`.

A Validator is allowed to: clean checkout/worktree, verify the exact SHA, verify the current PR HEAD/base, read required authority, execute the declared validation profile, capture OS/runtime/toolchain, capture exact commands + exit codes, and publish exact-SHA validation evidence.

A Validator MUST NOT implicitly: modify product source, repair discovered defects, redesign architecture, weaken tests, change Frozen Authority, merge a PR, close an implementation Issue, or validate an undispatched replacement SHA. A real defect produces `FAIL`. Environment/access/toolchain inability produces `BLOCKED`. Repair requires a separate Builder dispatch.

Projects MAY expose a version-scoped Validation Handoff Queue — a projection/index of Validator dispatches providing a stable entrypoint, READY/HOLD discovery, exact-SHA identity, provenance and restart/recovery (`EXECUTION_ARCHITECTURE_STANDARD.md` §24). The queue is not validation authority, not Task authority and not an independent workflow state machine; its derived item statuses (`READY / HOLD / RUNNING / PASS / FAIL / BLOCKED / SUPERSEDED`) are projections of canonical dispatch/gate facts.

## 10. CI execution and evidence

When CI is enabled, follow:

- `CI_EXECUTION_STANDARD.md` for provider/backend/checkout/runtime semantics;
- `CI_RUNNER_CAPABILITY_STANDARD.md` for routing inventory;
- `CI_EVIDENCE_STANDARD.md` for immutable evidence publication.

A Runner Capability Profile routes work only; actual run preflight and exact-SHA evidence win.

## 11. Blocker propagation

`BLOCKED` propagates only through real dependency edges. Continue all independent work.

A blocked macOS/device tuple may block Candidate Freeze while unrelated docs, another platform tuple, Hidden-pack preparation, or release-note preparation continues.

## 12. Evidence minimum

A useful Validation Report records:

```text
repository
tested_sha
candidate_sha when relevant
branch/ref as auxiliary metadata
dispatch identity when executed under a dispatch (dispatch_id)
expected_base_sha / requested_sha / actual_checked_out_sha / current_pr_head when exact-SHA dispatched
execution host role/channel/provider state
platform/architecture
runtime/toolchain
validation profile + scope
exact command/entrypoint
exit code
key logs/evidence
state
working_tree_clean and source_modifications_after_validation for dispatch validation
validation impact/reuse basis when evidence composition is used
```

External CI evidence remains governed by immutable evidence identity/completion rules in `CI_EVIDENCE_STANDARD.md`.

## 13. Prohibited practices

- claiming PASS without execution;
- moving PASS from one SHA/platform/toolchain to another by assertion;
- using CI PASS as unexecuted platform/CJ/Hidden/packaging PASS;
- deleting/weaking required tests to clear a gate;
- changing a required gate to optional to obtain READY;
- recording a required gate as `NOT_APPLICABLE` from cost, effort/turnaround, change size/file count, docs-only or mechanical appearance, Agent/model confidence, historical habit or silence instead of authority;
- re-running an unchanged subject without new evidence (changed environment/toolchain/inputs or a demonstrated non-deterministic cause) in order to obtain a different verdict for a deterministic `FAIL`; a later incidental `PASS` does not erase the recorded `FAIL`;
- treating an arbitrary retry/timeout bound as a gate verdict, or as a substitute for escalating a non-converging repair to its owning authority;
- unlimited retries/timeouts that mask deterministic defects;
- treating `latest.json`, evidence publication completion, artifact presence, or runner capability inventory as Validation PASS;
- treating infrastructure unavailability as product FAIL or PASS;
- a Validator opportunistically repairing product source under a validation dispatch;
- rewriting PASS evidence onto a successor SHA or an undispatched replacement candidate;
- treating a validation queue's derived item status as Gate state or as a second validation authority.
