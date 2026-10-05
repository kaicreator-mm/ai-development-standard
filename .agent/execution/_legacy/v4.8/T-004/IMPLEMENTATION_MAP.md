# Implementation Map — T-004 Task Learning Closeout / Template Wiring

This map is deliberately limited to adoption/closeout surfaces. It does not grant semantic ownership over Task Learning or Execution Architecture.

| Path | Required bounded change | Must not do |
|---|---|---|
| `templates/task-pack.md` | Expose a durable Task Learning closeout requirement/pointer so a Task Pack can require either `TASK_LEARNING=NONE_MATERIAL` or material-learning refs. | Copy Task Learning schema/currentness semantics into the generic Task Pack template. |
| `templates/task-issue.md` | Add a completion/closeout slot for the task's Task Learning result, reference-first. | Turn learning into a workflow state/Gate/authority. |
| `templates/implementation-pr.md` | Add a reviewable Task Learning closeout section/result and durable evidence ref(s), with the NONE_MATERIAL Fast Path. | Claim material learning proves current Validation/Review or release readiness. |
| `templates/final-closeout.md` | Add a reference-only Task Learning evidence index/summary for completed work items, allowing NONE_MATERIAL. | Make the version closeout infer authority or behavioral truth from learning. |
| `checklists/pr-review.md` | Check that the declared Task Learning closeout path is present, reference-first, currentness-safe, authority-safe, and privacy-safe. | Require private reasoning or treat learning as a replacement for exact-HEAD review/validation. |
| `templates/execution-pack/EXECUTION_CONTRACT.md` | Allow a task-scoped closeout requirement/reference in the execution contract so Builder completion cannot omit learning disposition. | Redefine JIT admission/currentness/scheduling/resource semantics. |
| `templates/execution-pack/REVIEW_CHECKLIST.md` | Add reviewer checks for the closeout result/ref, stale-learning fail-closed behavior, and authority/privacy boundaries. | Add a new semantic owner or universal mandatory learning object. |

## Shared implementation rules

1. Preserve existing headings/fields unless the smallest compatible addition requires a new subsection.
2. Use `TASK_LEARNING=NONE_MATERIAL` literally for the no-material-learning path.
3. For material learning, prefer one-or-more durable refs/digests and point semantic interpretation to `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`; do not paste schema rules into every template.
4. Keep the existing Gate vocabularies and Review/Validation ownership unchanged.
5. Do not introduce an eighth implementation path without Controller rebind.
6. The implementation PR must target `version/v4.8.0` and remain one concern.
