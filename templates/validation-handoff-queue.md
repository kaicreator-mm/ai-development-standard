# Validation Handoff Queue — <project> <version>

> `[Validation Handoff] <version> Build Host exact-SHA validation queue`
>
> This Issue is a **version-scoped projection/index of Validator dispatches**. It is a stable entrypoint for READY/HOLD discovery, exact-SHA identity, historical provenance and restart/recovery. It is NOT validation authority, NOT Task authority and NOT an independent workflow state machine — canonical truth remains the parent Task/PR + canonical events/evidence (`EXECUTION_ARCHITECTURE_STANDARD.md` §24, `VALIDATION_STANDARD.md` §9).

## Queue items (derived; one row per dispatch)

| dispatch_id | task | issue | pr | validation_scope | expected_base_sha | requested_head_sha | validation_profile | focused_gates | review_state | status |
|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  | READY/HOLD/RUNNING/PASS/FAIL/BLOCKED/SUPERSEDED |

Derived statuses are projections of canonical dispatch/gate facts. Multiple READY/HOLD/SUPERSEDED items coexist deterministically; superseded rows keep historical provenance and are never deleted to "clean up" — append or mark, do not rewrite history.

## Local Validator invocation (pointer-only)

```text
Continue <project> <version> current READY validation work in Issue #NN.
```

The worker reads this queue, selects the READY item, claims its dispatch (`DISPATCH_CLAIMED`), then follows `prompts/local-validator-bootstrap.md`:

```text
clean checkout at exact SHA
→ verify requested_head_sha == current PR HEAD   (else HEAD_DRIFT → superseded, do not execute)
→ execute declared validation profile
→ publish exact-SHA Validation Report + event (PASS/FAIL/BLOCKED)
```

## Exact-identity completion rule

A Validator dispatch MUST NOT project to terminal `PASS` merely because a loose validation event says PASS. The returned Validation Report must be bound back to the dispatch identity:

```text
dispatch_id            == dispatched id
requested_sha          == dispatch.requested_head_sha
tested_sha             == dispatch.requested_head_sha
actual_checked_out_sha == dispatch.requested_head_sha
current_pr_head        == dispatch.requested_head_sha
expected_base_sha      == dispatch.expected_base_sha
validation_profile     == dispatch.validation_profile
```

`schemas/validation-report.schema.json` requires the exact identity fields whenever `dispatch_id` is present. Consumers/reducers use the deterministic `validator_result_matches_dispatch(...)` rule from `scripts/v34_rules.py`; an unbound/legacy PASS remains historical evidence but cannot complete a v3.4 Validator dispatch.

## Rules

- A queue item becomes READY only from its dispatch facts; HOLD marks unmet prerequisites.
- Exact-SHA rule is strict: HEAD drift supersedes the dispatch; a new candidate requires a new dispatch identity; PASS never moves to a successor SHA.
- Validators never repair source here; defects route to a Builder dispatch on the parent Task.
- Closing this queue Issue never closes validation gates; gates live on the parent Task/PR.
