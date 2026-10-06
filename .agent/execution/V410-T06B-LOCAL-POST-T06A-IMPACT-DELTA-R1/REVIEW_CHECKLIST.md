# V410-T06B LOCAL-POST-T06A-IMPACT-DELTA-R1 review checklist

Unit type: LOCAL read-only impact/conflict analysis. Reviewers verify the *analysis*
(question, evidence, honesty), not an implementation — there is none.

1. **Write set.** Diff shape = exactly `.agent/execution/V410-T06B-LOCAL-POST-T06A-IMPACT-DELTA-R1/*`
   (six core artifacts + `POST_T06A_IMPACT_DELTA.md`). **Zero hunks** in `standard-manifest.json`,
   `schemas/*`, `templates/*`, `prompts/*`, `checklists/*`, `references/*`, `scripts/*`,
   `.github/*`, other execution packs, or any upstream owner standard. No new verification
   script was authored (authoring one would be implementation, which this unit forbids).

2. **Read-only honesty.** Confirm no source/fixture mutation by this unit, and that every probe
   was run against a disposable copy with the target restored. Reproduce: `git status --short`
   empty in `v410-t06a-owner-convergence` and `v410-t06b-local-backcompat-fixture-inventory-r1`.

3. **No verdict authority.** The pack emits no `READY`, no Concern Validation verdict, no
   Independent Review verdict, no Release Qualification, no gate waiver. Quoted
   `PASS`/`OK` strings are verbatim carried-suite output used as evidence, clearly labelled as
   non-verdict in `TEST_MATRIX.yaml#provenance.disclaimer`. Reject if any section reads as
   authorizing a change.

4. **Claim traceability.** Every verdict in sections 3, 5, and 6 of `POST_T06A_IMPACT_DELTA.md`
   traces to a reproduction in section 9 plus a row in `TEST_MATRIX.yaml`. Spot-check the two
   most load-bearing claims independently:
   - read `scripts/verify_standard.py` and confirm it never requires undeclared files to be
     registered (§3.3 — refutes the R1 note);
   - run `git diff --name-only <base>` after staging any new path and confirm
     `test_candidate_diff_shape_is_exact` fails (§5 C1 — the unconditional successor break).

5. **Subject binding accuracy.** Confirm the recorded subject is exact and that the pack states
   PR #925 is **OPEN / not merged**, that the Task Pack dependency `[V410-T06A]` is therefore
   **unsatisfied at the base**, and that this unit cannot satisfy it. Reject any wording that
   implies T06A is integrated.

6. **Baseline attribution.** Confirm §1.1 establishes the subject is green (77/77 + verifier PASS)
   so that D5/D6 failures are attributed to T06B's own future work and not to PR #925. Reject a
   reading of D5 as "PR #925 broke the build".

7. **Delta completeness.** Confirm D1–D7 each cite an exact source (route table in §2; measurement
   tables in §4–§7) and that D3's claim (the prior inventory omits the registry-growth guard's
   blocking role) is checked against the inventory's section D flag list, not just its tables.

8. **Contradictions left open.** Confirm X1–X4 are *recorded*, not resolved; and that no
   recommended shape is phrased as authorization. FAILURE_MATRIX S6 governs.

9. **Contradiction asymmetry check.** The analysis says the guard is *"mechanically"* amendable but
   *"governance-constrained"*. Confirm both halves are evidenced: no blob self-pin found (§3.2
   grep result), and the "must remain unmodified" wording is shown to live only in T06A-owned
   prose + its own TEST_MATRIX.

10. **Recency of the prior inventory.** Confirm D4's four drifted paths are reproduced from
    `git diff --name-status 30334e8 eea3e69`, and that the inventory's §E claim is characterised as
    *literally true but stale in pins-what prose* rather than as a false statement.

11. **Scope discipline.** Confirm no severity claim in §10 exceeds what the probes measured, and
    that `material_paths` enumerates every surface asserted as materially affected (S10).

12. **No downstream overreach.** Confirm the pack does not pre-approve, rank, or sequence T06B's
    dispositions beyond recording that C1's cheapest fix window is pre-merge; the choice belongs
    to T06B and its gates.

13. **Measurement validity (D8).** Confirm the `77/77 PASS` baseline was taken on a **committed**
    clean tree, and that D8 is stated as a pre-existing property of the base rather than as an
    effect of PR #925. Reject any reading that attributes the ODF-11 dirty-tree red to PR #925 or
    to T06A. Reproduce: run `python scripts/test_v48_orchestration_dogfood.py` clean (exit 0),
    add any untracked path under `.agent/execution/` (exit 1), remove it (exit 0).
