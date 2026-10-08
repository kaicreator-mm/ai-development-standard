# V410-T08A R1 execution contract — visible whole-project integration conformance wiring

Exact base: `402bf2899a7e1cd43eea3e7d78a37c947fe28c46` (tree `2af7450ff8312bd8652742996071252c42abe65e`), the merged PR #934 integration tip (V410-T07B INTEGRATED; full predecessor chain #861@0518202c → #862@cea2e0cc → #863@402bf289 live-verified). Task: #864 V410-T08A. Execution environment: LOCAL. Branch: `task/v4.10.0-v410-t08a-integration-execution`. Validation scope: integration. Agent freedom: F1_BOUNDED_IMPLEMENTATION.

Frozen authorities: Product #837 (PRD v0.4), L2 #842, refined DAG #848, Task Pack R1 §V410-T08A. Predecessor integrated surfaces: T06B (#861), T07A (#862), T07B (#863) — T08A composes them and routes semantic defects back, never repairing them.

## Visibility boundary (binding, verbatim)

**VISIBLE INTEGRATION PASS IS NOT HIDDEN VALIDATION OR RELEASE QUALIFICATION PASS.**

Every record emitted by `scripts/run_v410_integration.py` carries this disclaimer verbatim; `hidden_validation_verdict`, `release_qualification_verdict` and `candidate_freeze_verdict` are structurally `NOT_CLAIMED`; `v01_dispatch_gate` is `NOT_DISPATCHABLE_BY_THIS_RUNNER`. Integration verdicts are `VISIBLE_INTEGRATION_PASS | VISIBLE_INTEGRATION_FAIL` only, merge-scoped evidence on one exact candidate SHA/tree. No gate verdict, freeze verdict, Hidden verdict or RQ verdict may be inferred from any visible result.

## Integration boundary (binding)

This task owns ONLY integration-only residual wiring that cannot truthfully belong to one upstream semantic owner (Task Pack §V410-T08A): the whole-project visible runner, its focused conformance suite, this pack, and the disclosed successor-aware positional-registry rebinds with their mechanically forced blob-pin cascade. It **may not hide semantic repairs**: a semantic defect discovered during visible assembly routes to its owning concern (claim_key/compatibility/admission_generation semantics → #861 owner chain; event/writer attribution → GITHUB_AGENT_INTERACTION_PROTOCOL owner; Pack inventory/currentness → EXECUTION_PACK_STANDARD owner; gate/tuple/impact-decision semantics → VALIDATION_STANDARD owner; DAG/dependency → TASK_DAG_GOVERNANCE_STANDARD owner; decision-support surfaces → #863/#862 owner chain; Product/L2/DAG contradiction → #837/#842/#848 through governance amendment). T08A never repairs a semantic defect, even a small one; ambiguity is not a repair license (RC1–RC5 residual oracle, #864@6020074080).

## L3 seed (from #864@6011933890 + #864@6020074080, bound at this JIT)

### Tests

Positive (whole-candidate assembly, TS1–TS3 of the residual oracle):
1. All owner-local changes compose: the full visible command inventory (20 commands, 4 tiers) executes green on ONE exact committed candidate; the standard verifier + repository regression/conformance suites are green; manifest/schema/template/golden/protocol surfaces mutually agree.
2. Cross-owner composition: the three positional candidate registries agree on the single active T08A successor entry; the predecessor merge chain (#861/#862/#863) is intact as ancestors of the tested head; the predecessor packs' mandatory commands are all carried by the runner inventory.
3. False-green negatives (F1–F12, #864@6043181240) fail closed as record-model mutants: stale/mixed subject, missing/duplicate/unregistered suite rows, zero-collected or NOT_RUN rows, dirty tree or tree-mutating commands, open defect routes, Hidden/RQ/freeze verdict claims, evidence reuse — every mutant is rejected by the fail-closed record validator.
4. Clean-tree proof: pre-run, per-command and post-run `git status --porcelain` all zero; no suite writes artifacts into the tree.
5. After the bounded commit: the full battery re-executes on the COMMITTED HEAD/tree (not only the dirty worktree) and stays green.

Negative (never green):
1. Semantic defect inside T08A scope: REJECTED — routed to the owning concern via the defect-routing rows; T08A performs no semantic repair (forbidden_scope).
2. Stale upstream PASS binding a changed candidate: REJECTED — every run re-executes the complete inventory; `evidence_reuse=NONE` by construction (F11).
3. Visible PASS implying Hidden/RQ: REJECTED — structurally not representable in the record model (F8).
4. #900 historical nonconformance erased by integration PASS: REJECTED — the runner makes no historical claims at all.
5. #865 V01 dispatched on a pre-integration candidate: REJECTED — `v01_dispatch_gate=NOT_DISPATCHABLE_BY_THIS_RUNNER`.

### Contract / invariants

- Exact-subject binding: record binds `base_sha/base_tree` (= 402bf289/2af7450f), `tested_head_sha/tested_head_tree`, `head_at_emission_sha` separately (F10); any drift between suite execution and emission is a P0 CANDIDATE_DRIFT defect.
- Predecessor chain: #861@0518202c, #862@cea2e0cc, #863@402bf289 must all be ancestors of the tested head; drift fails closed (F7).
- Owner routing: every failure carries a defect route naming a known owning concern or CONTROLLER_ARBITRATION; `repair_dispatch_ref` is `TO_BE_ISSUED_BY_CONTROLLER` — the runner never self-repairs.
- Determinism: the command inventory and tier order are fixed in source; required_count = 20; the inventory is complete or the record is FAIL.

### Implementation seam

`scripts/run_v410_integration.py` (the runner: 4-tier order from the dryrun #864@6040893503, rebound at this JIT) + `scripts/test_v410_t08a_integration_runner.py` (the focused oracle suite: inventory binding, record-model mutants, registry agreement, pack surface) + this pack + the disclosed three-registry successor rebind with in-commit pin convergence.

### Failure handling

- Suite failure → owner-routed defect row, tier policy honored (TIER-0 fail-fast; TIER-1/2 continue-within-tier; halt before TIER-3 on any defect).
- Dirty tree / ancestry loss / chain drift → PRE_RUN_REFUSAL, nothing executes.
- Runner/provider infrastructure inability → BLOCKED/NOT_RUN record, never PASS fabrication.
- Semantic defect → owner routing (see boundary above); successor candidate rebind invalidates affected exact-subject evidence.

### References

#864@6011933890 (preplan), #864@6016404606 (integration delta INT-P/N), #864@6018269654 (currentness matrix), #864@6020074080 (residual oracle RC1-RC5/TS1-TS5/MR1-MR8), #864@6037701635 (impact inventory), #864@6040893503 (runner dryrun), #864@6043181240 (false-green oracle), #864@6046066388 (fast-path), #864@6055469111/#864@6055469682 (proposal/admission+claim), #864@6056973981 (safe-resume handoff), #916@6055817004 (positional-guard precheck), #916@6056834207 (native DAG reconciliation), merge terminals #861@0518202c/#862@cea2e0cc/#863@402bf289.
