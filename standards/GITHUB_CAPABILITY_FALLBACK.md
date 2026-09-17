# GitHub Capability Fallback Standard

## 1. Purpose

This standard defines what an Agent must do when the current GitHub connector, token, API surface, repository plan, or permission set cannot mutate a GitHub object that the active workflow treats as canonical.

The objective is to preserve semantics and audit truth. Tool limitations MUST NOT silently redefine the workflow model.

## 2. Canonical semantics do not downgrade with tool capability

Examples of canonical facts include:

```text
Issue Dependency = blocked-by / blocking execution edge
Milestone        = version/release aggregation when the project uses Milestones
PR base          = code integration target / temporary stack parent
Commit SHA       = immutable code/evidence identity
Review Result    = exact-SHA review evidence when review is performed
Validation       = exact-SHA execution evidence
```

If the current operator cannot perform the canonical mutation, it MUST NOT replace the canonical fact with a weaker representation and then claim the canonical mutation happened.

Examples:

```text
NOT ALLOWED:
Issue body says "blocked by #12" → claim native Issue Dependency exists

NOT ALLOWED:
Comment says "milestone v3.2" → claim GitHub Milestone was assigned

NOT ALLOWED:
Branch name contains T02 → claim execution dependency is materialized
```

## 3. Capability discovery

Before a workflow depends on a GitHub mutation that may not be available, the acting operator SHOULD determine whether the current tool surface can perform it.

Relevant capability classes include:

```text
issue.create / issue.update
issue_dependency.read / issue_dependency.write
sub_issue.read / sub_issue.write
milestone.read / milestone.write
label.read / label.write
branch.create / branch.update
pull_request.create / pull_request.update / pull_request.merge
review.read / review.write
workflow.read
release.write
```

Capability discovery is an execution fact, not a product decision.

## 4. Fallback rule

When a required canonical mutation cannot be performed:

1. preserve the intended canonical semantic;
2. record the missing capability and affected object;
3. record any temporary mirror explicitly as `NON_AUTHORITATIVE_MIRROR`;
4. use `NOT_RUN` when the mutation has not been attempted/executed;
5. use `BLOCKED` when permission/tool/API constraints currently prevent completion;
6. route the canonical mutation to an operator that has the required capability, typically a Local Agent, repository administrator, or supported automation;
7. once the canonical mutation is performed, publish a corrective/completion event and stop relying on the mirror.

A mirror is for recovery and routing only. It MUST NOT become Release Authority, dependency authority, or merge authority.

## 5. Issue Dependency fallback

Issue Dependency remains the canonical live execution DAG when Issue-based execution is enabled.

If the current connector cannot create native Issue Dependency edges, the Task contract MAY temporarily record:

```text
NON_AUTHORITATIVE_MIRROR
planned_blocked_by: [#14, #15]
reason: current connector lacks issue_dependency.write
canonical_state: NOT_RUN | BLOCKED
handoff: <issue/operator that will materialize the edge>
```

Rules:

- do not infer canonical dependency satisfaction from the mirror;
- do not mark a dependency-sensitive Task `merge-ready` solely from mirrored text;
- implementation MAY continue early only when the frozen Task contract allows it and doing so does not violate an actual dependency invariant;
- once native edges exist, the mirror may remain as historical explanation but is no longer used for routing authority.

## 6. Milestone / label fallback

Milestones and labels are routing metadata, not substitutes for Task contracts or Gate evidence.

If mutation is unavailable:

- keep version/review/state semantics in the stable Task contract and structured events;
- mark metadata mutation `NOT_RUN/BLOCKED` truthfully;
- do not create ad-hoc alternative semantics that another Agent could mistake for canonical metadata;
- materialize the canonical metadata later when an authorized operator is available if project policy requires it.

## 7. Branch / PR fallback

If branch or PR mutation is unavailable, implementation MUST NOT be described as integrated.

Allowed states include:

```text
implementation artifact prepared
branch mutation BLOCKED
PR creation NOT_RUN
merge NOT_RUN
```

A patch, archive, chat message, or local working tree is not a merged GitHub fact.

## 8. Validation and Review are not capability fallbacks for each other

A missing GitHub metadata mutation does not invalidate real Validation evidence, but it also does not allow Validation to replace required Review, or Review to replace required Validation.

Likewise, a CI success cannot prove a canonical GitHub dependency edge exists.

Each fact keeps its own authority.

## 9. Capability handoff contract

A capability handoff SHOULD identify:

```text
repository
exact target object(s)
required canonical mutation
current operator and missing capability
current mirrored state (if any)
expected postcondition
forbidden substitutions
completion evidence
```

For Issue Dependency materialization, completion evidence should identify the affected Issues and confirm the native blocked-by/blocking relation is observable through GitHub.

## 10. Self-dogfood requirement for this standard repository

When `ai-development-standard` develops itself, it SHOULD use the same rules it publishes:

```text
Task Issue contract
→ explicit Review Policy
→ logical operator attribution
→ task branch / PR
→ exact-head Validation
→ Review when required/selected
→ merge to version branch
→ version closeout
```

Any connector limitation discovered during self-development MUST be recorded as a capability limitation rather than hidden by documentation-only substitutes.

Self-dogfood evidence is implementation feedback for the standard. If the workflow cannot be executed with available tools, the result should improve the capability fallback/handoff rules rather than weaken the canonical model.
