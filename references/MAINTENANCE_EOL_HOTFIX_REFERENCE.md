# Maintenance, EOL & Hotfix Reference

Non-normative guidance for `MAINTENANCE_EOL_HOTFIX_STANDARD.md`.

## Support-line example

```text
support_line_ref: release/2.x
target_baseline_ref: <exact SHA>
support_status: project-defined
allowed_change_classes: [security-fix, critical-bug]
maintenance_policy_ref: <durable owner>
```

The branch name is a locator, not the support decision itself.

## Backport evidence tuple

```text
source_ref: <source change/PR/SHA>
target_support_line_ref: <line>
target_baseline_ref: <exact pre-change SHA>
result_sha_ref: <exact result SHA>
validation_refs: [<result-SHA evidence>]
review_refs: [<when applicable>]
release_refs: [<when applicable>]
```

Every result binds its own evidence. Do not keep ambiguous parallel top-level arrays that make source/result association unclear.

## Hotfix proportionality

Urgency can shorten coordination, batching or optional review only when authority permits. It does not convert required exact-SHA gates into optional gates.

## EOL example

An EOL line may remain clonable, tagged or downloadable. Those availability facts do not restore support status. Upgrade/migration guidance should point to the current owning destination when material.
