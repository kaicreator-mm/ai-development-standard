# v4.9.0 Task Materialization Status

Frozen Task DAG: v0.2 / `b9fe0cc7089f64929b4bcf45f7230d950e864db2` / Freeze #719.

## Task Issue map

| Task | Issue | Initial posture |
|---|---:|---|
| T-001 | #720 | PLANNED / NOT_BUILDER_READY |
| T-002 | #721 | PLANNED / NOT_BUILDER_READY |
| T-003 | #722 | PLANNED / NOT_BUILDER_READY |
| T-004 | #723 | PLANNED / WAITING_LINEAGE |
| T-005 | #724 | PLANNED / NOT_BUILDER_READY |
| T-006 | #725 | PLANNED / WAITING_LINEAGE |
| T-007 | #726 | PLANNED / NOT_BUILDER_READY |
| T-008 | #727 | PLANNED / NOT_BUILDER_READY |
| T-009 | #728 | PLANNED / NOT_BUILDER_READY |
| T-010 | #729 | PLANNED / NOT_BUILDER_READY |
| T-011 | #730 | PLANNED / NOT_BUILDER_READY |
| T-012 | #731 | PLANNED / NOT_BUILDER_READY |
| T-013 | #732 | PLANNED / NOT_BUILDER_READY |
| T-014 | #733 | PLANNED / NOT_BUILDER_READY |
| T-015 | #734 | PLANNED / NOT_BUILDER_READY |

All 15 Task Packs are materialized under `docs/implementation/4.9.0/task-packs/` and bind the exact Frozen DAG plus Task Issue/dependencies/lineage refs.

## Native dependency hydration

The current ChatGPT GitHub connector exposes Issue creation/read/update but no mutation action for GitHub Native Issue Dependencies. Therefore the `deps[]` graph is **not yet claimed hydrated**.

```text
NATIVE_DEPENDENCY_HYDRATION=PENDING_LOCAL_AGENT
PROSE_DEPENDENCY_REFS=NON_AUTHORITATIVE_FOR_READY
IMPLEMENTATION_ADMISSION=NO
BRANCH_CREATION=NO
BUILDER_DISPATCH=NO
```

A local GitHub-capable agent must materialize exactly the Frozen DAG `deps[]` edges and verify no lineage predicate was converted into an Issue edge. After hydration, a Controller must re-check Task Pack currentness, lineage, L3/Assurance and integration baseline before transitioning any Task to READY.
