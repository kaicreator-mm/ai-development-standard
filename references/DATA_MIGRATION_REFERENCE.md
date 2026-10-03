# Data & Migration Reference

This reference is non-normative guidance for `standards/DATA_MIGRATION_GOVERNANCE_STANDARD.md`.

## 1. Minimum transition worksheet

```text
source_state_ref:
target_state_ref:
datastore_kind:
runtime_or_engine_version:
environment_ref:
mechanism_refs:
ordered_steps/dependencies:
risk notes:
recovery strategy:
recovery prerequisites:
validation subject:
side_effect_authority_ref:
```

Do not replace source/target state with “latest migrations applied” unless that statement itself is durably and independently evidenced.

## 2. Fresh install vs upgrade

A fresh database created directly at schema B proves that B can initialize under the tested tuple. It does not prove that existing schema/data A can transition to B.

Useful upgrade fixtures should begin from a realistic A state, including representative existing rows/constraints where those affect transition behavior.

## 3. Interrupted transition

A useful recovery exercise can intentionally stop between steps or inject a controlled failure, then verify the selected recovery strategy. The evidence must say whether it proves rollback, restore, forward repair, retry/idempotency, or another strategy; do not generalize across strategy classes.

## 4. Engine/environment applicability

A transition can behave differently across database engines, versions, extensions, collations, transaction/DDL behavior, storage modes, or privilege models.

Record the dimensions actually exercised. When a different production tuple matters, either execute it or provide explicit compatibility evidence; do not silently substitute a convenient local fixture.

## 5. Expand/contract example

A common safe evolution may involve:

1. expand schema/state so old and new application versions can coexist;
2. backfill/dual-write or migrate data with observable progress;
3. verify consumers have moved;
4. contract/remove old representation only after the compatibility window permits it.

This is one strategy, not a universal mandate. The actual ordering and recovery plan remain project-specific evidence.

## 6. Destructive transition prompts

Before executing a destructive/high-risk transition, ask:

- Can data be reconstructed if the transform is lossy?
- Is the backup/snapshot itself validated and restorable?
- Can the operation be retried safely after partial execution?
- What is the lock/availability impact for the actual dataset size?
- Is application compatibility needed during transition?
- Which exact authority permits mutation of the selected environment?

## 7. Production authority example

Having `DATABASE_URL`, cloud credentials, or a migration tool installed proves capability only. A production execution still requires the applicable side-effect authority and exact environment subject.

## 8. Review prompts

1. Are source and target persistent-state identities explicit?
2. Is directionality preserved?
3. Is evidence from fresh install being reused as upgrade evidence?
4. Does the tested runtime/database/environment tuple match the claim?
5. Is migration presence confused with actual execution?
6. Is the recovery strategy explicit even when no down migration exists?
7. Are destructive risks treated proportionally?
8. Is production mutation authority explicit rather than inferred from credentials?
