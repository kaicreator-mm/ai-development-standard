# ADS v4.13 — Task DAG R0 Freeze (source-only exact graph)

> **STATUS: TASK_DAG_FROZEN (PLAN ONLY)**. This freezes only the intended implementation topology of **S02/S03/S04 and one existing Release Closure concern**. GitHub Issue materialization, exact Task Claims, source writes and release remain separate.

```ini
EVENT=ADS_V413_TASK_DAG_R0_FREEZE
DAG_FROZEN_PATH=docs/tasks/v4.13.0/TASK_DAG_R0.md
DAG_FROZEN_BLOB=da877ec97be61c86c391f022b6e789be727b5d7b
DAG_PREFREEZE_HEAD=69172742765d5c25901a4bcb26fee1ff949d8fb2
PRODUCT_FROZEN_BLOB=702bcf562b4292487fa8409cd17dee2d42aae9b3
PRODUCT_FREEZE_CHECKPOINT=3123d7d4bd5ef7b8f9236119537ff9226d6bd3a9
L2_FROZEN_BLOB=86b9243c065ab909f82d52d1d7b7f945791d3696
L2_FREEZE_CHECKPOINT=91bb0378b0516367177c1570bd8f09cf1878ec4b
IMPLEMENTATION_CONCERNS=3
PARALLEL_CONCERNS=V413-S02,V413-S03,V413-S04
INTRA_IMPLEMENTATION_DEPENDENCY_EDGES=0
VERSION_CLOSURE=AFTER_ALL_3_ACTUAL_COMPLETION
TASK_ISSUES=MATERIALIZE_AFTER_THIS_FREEZE
TASK_CLAIMS=NONE
NORMATIVE_SOURCE_WRITES=NOT_AUTHORIZED_BY_DAG_FREEZE_ALONE
LAST_QUALIFIED_PUBLISHED_ADS=v4.12.0@ee8258106547abd2c2d7b9f5e87af9965e430bd2
CURRENT_MAIN_HOTFIX_LINEAGE=4465e291df4e60e09af634a25ab7eed546b2915b
SOURCE_INTEGRATION_IMPACT_PROOF=BEFORE_FIRST_NORMATIVE_TASK_WRITE
RUNTIME_TALLY_TASKS=OUT_OF_SCOPE
RELEASE_PASS=NO
```

The User's request to continue all v4.13 Issues is scoped to lawful planning Task DAG Freeze and issue preparation; not authorization to bypass the accepted Work Item/Claim/CAS rules or to treat a title/Comment as a native dependency. One source-only architecture proposal with explicit source-owner boundaries is sufficient for Task planning. No independent DAG review is claimed; first real normative schema, Task/Claim authority and adoption PRs carry applicable risk-based independent Review.

**Version baseline observation:** GitHub compare of released Tag commit `ee825810...` to current `main@4465e291...` reports `ahead=13`, `behind=0`, merge base is exactly `ee825810...`; five changed files (VERSION, README, CHANGELOG, selector and its tests). Thus the current main hotfix delta is **ancestrally derived from qualified 4.12.0**, not a published/qualified 4.12.1 Release. The v4.13 integration branch may carry it only while recording the full source diff and running affected/candidate checks; no “inherited v4.12.1 Release PASS.”

**Planning topology:** exactly 3 independent implementation Issues, S02 org defaults/schema; S03 GitHub/Task/Attempt consumer interop; S04 #1119 prospective/PR/activation contract and any *proven* #1116 delta. They do not require native `blocked_by` edges against each other. The version Closure stage waits for genuine completion and Release proof, not a new manufactured implementation dependency edge.

**Downstream requirements:** Materialize each `type:task` Issue with complete source pins, allowed/disallowed write sets, Review Policy and validation, `state:planned` pending integration-source/currentness and accepted CAS Claim. No source writing from this record. Reconcile source baseline; resolve predecessor + current-main patch impact for implementation. Only after legitimate task Claims may Builder create targeted normative PRs.

Freeze document owns no self-hash: source blob and prefreeze HEAD named above, and actual remote checkpoint is read back and posted to #1147.
