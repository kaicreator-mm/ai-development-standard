## Related Work

- Task / Issue: #
- Milestone / Version:
- Baseline Commit:
- Integration target:
- Development Standard: `kaicreator-mm/ai-development-standard@v3.1.0` + immutable revision
- Author role / logical operator: `<actor_role> / <operator_id>`
- Session ref / transport actor: `<session_ref> / <github:account>`

## Dependency / Branch Topology

- Execution dependencies: Issue Dependencies / none
- Branch strategy: `independent / stacked`
- Stack parent PR / branch: `NOT_APPLICABLE / ...`

Issue Dependency is the canonical Task DAG. Stacked PR is only for real unmerged code-baseline dependency.

## Why


## Scope

- In:
- Out:

## Changes


## Validation

- Tested SHA:
- Execution environment:
- CI profile: `minimal / custom / disabled`
- Validator operator / session: `<operator_id / session_ref / NOT_APPLICABLE>`

| Gate / Tuple | State | Evidence |
|---|---|---|
| Fast Gate | | |
| Integration | | |
| Critical Journeys | | |
| Hidden Validation | | |
| Platform / Production Build | | |
| Minimal CI | | |

Use only `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`.

## Independent Review

- Review policy: `required / recommended / not-required`
- Policy authority / rationale:
- Decision for `recommended`: `PERFORM / SKIP / NOT_APPLICABLE`
- Reviewed SHA:
- Review status: `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`
- Reviewer operator / session: `<operator_id / session_ref / NOT_APPLICABLE>`
- Review evidence/event:

Review is risk-based, not universally mandatory. `required` needs PASS on current SHA; `recommended` may be explicitly skipped; `not-required` uses `NOT_APPLICABLE`. Any performed Review PASS applies only to the exact reviewed SHA.

When required Independent Review is performed through the same GitHub account as implementation, reviewer `operator_id/session_ref` must identify an independent context from the Builder context.

## Remaining Gates / Blockers

- gate → state → reason → downstream impact

## Merge Readiness

- [ ] Required task/local Validation satisfied.
- [ ] Review condition satisfied for the declared Review Policy.
- [ ] Required Review independence/operator attribution is auditable when applicable.
- [ ] Configured required CI satisfied when applicable.
- [ ] Required Issue Dependencies satisfied for merge.
- [ ] Correct integration target / stack parent.
- [ ] No unresolved release-significant blocker/finding.

## Remaining Issues / Limitations

None / describe explicitly.

## Release Impact

PR PASS / Review PASS / Minimal CI PASS does not imply Release PASS.
