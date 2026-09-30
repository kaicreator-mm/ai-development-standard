# Context Engineering Reference

Non-normative guidance for `CONTEXT_ENGINEERING_STANDARD.md`.

## Fresh-task read sequence

A practical sequence is:

```text
1. repository AGENTS / pinned standard
2. current Product/L2 if material
3. Frozen Task DAG + exact Task Pack
4. live Issue dependencies and current branch/base
5. current PR/HEAD when one exists
6. only the source/tests/evidence referenced by the concern
7. expand outward when a conflict or missing dependency requires it
```

This is a read sequence, not a universal authority ranking. Resolve each fact by its semantic owner, allowed override surface and required live currentness. In particular, valid `PROJECT_OVERRIDES.md` specialization may refine standard defaults without weakening hard constraints, and native Issue Dependencies are the canonical live blocked-by topology after materialization even though the Frozen DAG remains planning/history authority.

Do not start by loading the whole repository or a historical chat transcript.

## Currentness-sensitive actions

Re-read live facts immediately before actions such as:

- expected-head merge;
- exact-SHA Review/Validation;
- JIT branch creation;
- dependency-unlocked dispatch;
- mutation outside a previously observed write-set;
- external side effects.

## Context quality questions

1. What authority owns this fact?
2. Is this a hard constraint, default, allowed override, frozen semantic, or live execution fact?
3. Is it current enough for the next action?
4. Is the source durable/recoverable?
5. Is this fact required or merely useful?
6. Does another same-level source disagree?
7. Am I confusing availability/provenance with authority?

## Lost-session test

Imagine the current Agent disappears. A replacement should be able to recover required Product/Task/currentness/blocker/next-action facts from durable repository/GitHub references. If not, persist the missing development truth in its owning surface rather than relying on transcript recovery.
