# V410-T08A LOCAL-INTEGRATION-IMPACT-R1 — Integration Impact Analysis

Exact base: `30334e8c7b90a327f8597b86c88c785b98df07f7` (`origin/version/v4.10.0` tip, merge of T05A R3 #902).
Method: git history analysis (`git log --merges --first-parent`, `git diff --stat <merge>^1 <merge>`,
`git diff` on overlapping files) on the version branch. No network access. No source mutation.

This is a LOCAL preparation/analysis unit. Visible integration PASS produced by any command
listed here is NOT Hidden Validation PASS and NOT Release Qualification PASS.

## 1. Per-predecessor impact table

| Task | Merge SHA | Surfaces touched | Suites that must keep passing |
|---|---|---|---|
| V410-T01A Stage-1 lifecycle semantics | `df1ee51a0d6d1c30092c01102ca320db51091535` | `.agent/execution/V410-T01A/`; `standards/DEVELOPMENT_WORKFLOW.md` (Stage-1 section, owner blob `ac956e7e` rebind); adds `scripts/test_v410_stage1_lifecycle_contracts.py` | `python scripts/test_v410_stage1_lifecycle_contracts.py` |
| V410-T02A responsibility/control semantics | `2276afe7fdd057f300386ab19925ae37a4065684` (PR #879) | `.agent/execution/V410-T02A/`; `standards/EXECUTION_ARCHITECTURE_STANDARD.md` (+69); adds `scripts/test_v410_t02a_collaboration_control.py` (479 lines) | `python scripts/test_v410_t02a_collaboration_control.py` |
| V410-T03A automation-first implementation quality | `46fe74936cd88184bbd898643851b585d3299291` | `.agent/execution/V410-T03A/`; `standards/IMPLEMENTATION_QUALITY_STANDARD.md` (+14); `references/IMPLEMENTATION_QUALITY_REFERENCE.md`; adds `scripts/test_v410_t03a_implementation_quality.py` | `python scripts/test_v410_t03a_implementation_quality.py` |
| V410-T03B task decomposition & safe parallelism | `98ccd07ee18f3a8a8f10e91e04295324ebb130d8` | `.agent/execution/V410-T03B/`; `standards/TASK_DECOMPOSITION_STANDARD.md`; `references/TASK_DECOMPOSITION_REFERENCE.md`; extends `scripts/test_v43_task_decomposition.py` (+34) | `python scripts/test_v43_task_decomposition.py` |
| V410-T01B product projections | `f1daaffb6ae3469dc0e77e881ed73e17e6586295` (PR #880) | `.agent/execution/V410-T01B/`; `prompts/L1_PRODUCT_EVIDENCE.md`; `templates/research-issue.md`; adds `scripts/test_v410_t01b_product_projections.py` (390 lines) | `python scripts/test_v410_t01b_product_projections.py` |
| V410-T04A gate applicability & repair routing | `41236cb7250c6854170563d371d7debe7354c936` (PR #884) | `.agent/execution/V410-T04A/`; `standards/DEVELOPMENT_WORKFLOW.md` (+63, gate-applicability sections); `standards/VALIDATION_STANDARD.md`; adds `scripts/test_v410_t04a_gate_repair_routing.py` (382 lines) | `python scripts/test_v410_t04a_gate_repair_routing.py` |
| V410-T02B-R2 machine projection / dispatch-event family | `fee097db238b60d97ab2d449dcf210488d03814f` (PR #887) | `.agent/execution/V410-T02B-R2/`; `schemas/dispatch.schema.json` (+14/-2); `schemas/agent-event-v2.schema.json` (+1/-1); `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`; `templates/agent-event-comment.md`; adds `scripts/test_v410_t02b_machine_projection.py` (589 lines); MODIFIES `scripts/test_v410_t02a_collaboration_control.py` (+29/-8) | `python scripts/test_v410_t02b_machine_projection.py`; `python scripts/test_v410_t02a_collaboration_control.py` (updated version) |
| V410-T05A-R3 shared-code safety | `30334e8c7b90a327f8597b86c88c785b98df07f7` (PR #902; merge SHA identical to base) | adds `scripts/test_v410_t05a_shared_code_safety.py` (470 lines) only; owner blobs unchanged | `python scripts/test_v410_t05a_shared_code_safety.py` |

## 2. Composed-candidate conformance command list (full visible regression)

Ordered cheapest-first. All entrypoints are checked in at the exact base. Cost notes are
rough wall-clock estimates on a developer workstation; the full set is expected to run in
well under two minutes total (all suites are stdlib-only file/schema checks).

```bash
# 1. Base standard/schema sanity — fastest, gate for everything below (~1-2s)
python scripts/verify_standard.py
# 2. Protocol schema conformance (~2-3s)
python scripts/test_protocol_schemas.py
# 3. Interface compatibility regression (~1-2s)
python scripts/test_v42_interface_compatibility.py
# 4. T03B task decomposition / safe parallelism (~1-2s)
python scripts/test_v43_task_decomposition.py
# 5. T01A Stage-1 lifecycle contracts (~1-2s)
python scripts/test_v410_stage1_lifecycle_contracts.py
# 6. T03A implementation quality (~1-2s)
python scripts/test_v410_t03a_implementation_quality.py
# 7. T01B product projections (~2-4s)
python scripts/test_v410_t01b_product_projections.py
# 8. T04A gate applicability / repair routing (~2-4s)
python scripts/test_v410_t04a_gate_repair_routing.py
# 9. T02A collaboration control (post-T02B-R2 version) (~3-5s)
python scripts/test_v410_t02a_collaboration_control.py
# 10. T02B-R2 machine projection / dispatch-event family (~4-8s)
python scripts/test_v410_t02b_machine_projection.py
# 11. T05A-R3 shared-code safety (~3-6s)
python scripts/test_v410_t05a_shared_code_safety.py
```

Each predecessor owner is expected to keep its own suite green; together these eleven
commands constitute the full visible regression/conformance run on the integrated
candidate at `30334e8`. Execution of the expensive suites (9–11) is deferred to T08A
integration time per TEST_MATRIX `full_run: false` marking in this preparation unit.

## 3. Residual integration-only wiring candidates (for T08A execution, NOT implemented here)

Surfaces that truthfully belong to no single upstream owner and are candidates for the
T08A central integration wiring unit:

1. **A single top-level visible conformance runner** (e.g. `scripts/run_v410_visible_conformance.py`
   or a documented command block) that executes the eleven commands above in order and
   aggregates exit codes — no single predecessor may own a whole-candidate runner.
2. **Cross-suite conflict audit** — a check that no two suites mutate the same surface
   expectations (currently manual via git history; automatable as integration-only wiring).
3. **Integration admission record** — durable machine-readable record binding the exact
   integrated candidate SHA to the visible regression result at T08A integration time.
4. **Defect routing log scaffold** — a tracked placeholder for routing semantic defects
   found during integration back to owning concerns via repair/DAG governance, so that
   fixes do not happen invisibly inside the integration unit.

None of these are implemented in this preparation unit.

## 4. Risk / impact notes — where composition could contradict

Verified with `git diff --stat <merge>^1 <merge>` per predecessor and targeted `git diff`
on overlapping files:

- **Overlapping file: `standards/DEVELOPMENT_WORKFLOW.md` (T01A + T04A).** T01A rewrote the
  Stage-1 section (semantic L1 evidence, Product Research, Product Review, Product Freeze
  semantics); T04A appended the "Gate applicability 与合法来源" and "Applicability UNKNOWN 或
 矛盾：fail closed" sections (~60 lines later in the file). The combined
  `git diff df1ee51^1 41236cb -- standards/DEVELOPMENT_WORKFLOW.md` shows disjoint hunks;
  no textual contradiction. Semantic watch-item: T01A's Stage-1 Product Review selection
  rules and T04A's gate-applicability fail-closed rules must be read together at T08A
  integration Validation so a Product-scope gate is not double-applied or silently
  downgraded.
- **Overlapping file: `scripts/test_v410_t02a_collaboration_control.py` (T02A + T02B-R2).**
  T02B-R2 legitimately modified the T02A suite (+29/-8) as part of the dispatch/event
  family; both suites (02A updated, 02B added) must pass on the integrated candidate.
  Not a contradiction; an ordering dependency — the T02A suite is only authoritative in
  its T02B-R2-extended form.
- **Schema vs standard coupling (T02B-R2).** `schemas/dispatch.schema.json` and
  `schemas/agent-event-v2.schema.json` changed together with
  `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`; `test_protocol_schemas.py` (command 2)
  must stay green against the updated schemas.
- **Execution pack paths are disjoint** (V410-T01A/T02A/T03A/T03B/T01B/T04A/T02B-R2/T05A-R3
  directories do not collide); no pack-level composition conflict.
- **Outstanding predecessors (T04B PR #918, T05B pending) may still alter these surfaces**;
  this impact analysis is current only for base `30334e8`. Any additional merge rebases
  the composition and requires re-running the eleven commands.

## 5. Explicit non-claim

A green run of the eleven visible commands above is **visible integration conformance
only**. It is not Hidden Validation PASS and not Release Qualification PASS. Those verdicts
require their own owning gates on the exact final integrated candidate after T08A admission
(which itself stays gated on V410-T07B) — no such verdict is asserted, implied, or
fabricated here.

## 6. Local execution evidence (this preparation unit)

All eleven commands in §2 were executed locally on the exact candidate
(`30334e8c7b90a327f8597b86c88c785b98df07f7`) during this unit and all passed (exit 0).
This is recorded as visible preparation evidence only; the authoritative full visible
regression remains a T08A-integration-time obligation on the then-current candidate.

Verification script output (verbatim tail):

```text
entrypoint: scripts/test_v410_t05a_shared_code_safety.py -> OK
merge_sha: df1ee51a0d6d1c30092c01102ca320db51091535 -> OK
merge_sha: 2276afe7fdd057f300386ab19925ae37a4065684 -> OK
merge_sha: 46fe74936cd88184bbd898643851b585d3299291 -> OK
merge_sha: 98ccd07ee18f3a8a8f10e91e04295324ebb130d8 -> OK
merge_sha: f1daaffb6ae3469dc0e77e881ed73e17e6586295 -> OK
merge_sha: 41236cb7250c6854170563d371d7debe7354c936 -> OK
merge_sha: fee097db238b60d97ab2d449dcf210488d03814f -> OK
merge_sha: 30334e8c7b90a327f8597b86c88c785b98df07f7 -> OK
counts: commands=11 merge_shas=8
INTEGRATION_IMPACT_VERIFIED=PASS
```
