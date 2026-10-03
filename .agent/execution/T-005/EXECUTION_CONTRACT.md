# T-005 Execution Contract

Exact base: `version/v4.9.0@67ad362a47d665c38dbb25f1667b064e6379923d` / tree `9d334c6290e6cf924dd58c909684c5d6451103fe`.
Authority: Frozen Product #709 > Frozen L2 #714 > Frozen DAG #719 > reviewed Task Pack blob `ecfc57282bc9f8cd6ba84913d180976cc2868f6c` > this Execution Pack.

## Source write set
- `standards/RELEASE_STANDARD.md`
- `references/RELEASE_APPLICABILITY_REFERENCE.md`
- `scripts/test_v49_release_applicability.py`

`.agent/execution/T-005/**` is Controller-authored execution authority and MUST NOT be rewritten by the Builder.

## Contract kernel
Add only prospective, Release-owned applicability semantics per `gate × subject`, using a vocabulary equivalent to `REQUIRED_NOW | DEFERRED_TO_VERSION_CLOSURE | NOT_APPLICABLE | UNKNOWN`. Preserve existing thaw/invalidate/Hidden/Closeout/Release Qualification authority. Concern-level decisions MUST NOT aggregate into a version-level release verdict. Unknown/ambiguous applicability fails closed. Migration is prospective-only and cannot shorten gates already bound to an in-flight Frozen/qualified candidate.

Do not implement cross-owner evidence currentness (T-010), dogfood contract (T-014), execution orchestration (T-007), or any parallel release lifecycle.

If implementation requires a new release schema/family or another normative owner surface outside this write set, stop with `TASK_PACK_DEFECT` or `ARCHITECTURE_CONTRADICTION`; do not widen locally.
