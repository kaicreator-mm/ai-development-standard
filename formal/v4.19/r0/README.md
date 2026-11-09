# ADS v4.19 formal verification experiment — R0 (non-normative)

This is a **bounded model-checking experiment**, not a proof of all ADS natural-language rules. No change is made to the ADS standards, schema, frozen #1353 subjects, Task DAG, Claim, CI, or release eligibility.

## Authority and immutable source

- Repository: `kaicreator-mm/ai-development-standard`
- Branch baseline: `version/v4.19` at `fbf1a7d49596c549e955ef36949f4110a0da2d33`
- Experimental source: PR #1365 HEAD `dac263fa4c0ab155406d2f2117459b34322cc988`, unmerged/non-frozen candidate.
- `source-map.json` gives exact per-file Git blob hashes and the text anchors used to form each hypothesis. **Prospective rules do not govern historical #1353-frozen Tasks.**

## What was checked, and what wasn't

| Group | Exact experiment | Result |
|---|---|---|
| Z3 / role profiles | 12 SAT/UNSAT queries: Validator/Reviewer cannot source-write, Profile/Role/Environment consistency, accepted Claim and write-set permission, historical vs prospective Local Builder admission, positive legal builder executions | 12/12 match expectations |
| Z3 / abstract gate prerequisites | 5 queries: no release without prerequisite freezes/CI/Review; no Claim ahead of DAG; a fully qualified path remains satisfiable | 5/5 match expectations |
| Z3 / injected bug | Deliberately remove the source-write Builder guard; Z3 finds an unauthorized Validator write | expected SAT counterexample |
| TLC / lifecycle | Exhaustive finite-state search of one Task, 2 potential Writers, monotone freeze/claim/test/review/closure/release flags | 27 distinct states, no modeled invariant violation |
| TLC / two injected bugs | Remove Release gate; allow multiple active Writers for one Task | both produce expected invariant counterexamples |
| Checkout-byte alignment | `--source-checkout` verifies candidate exact HEAD, each Git blob SHA1, and cited anchors | NOT_RUN here; only GitHub connector readback performed |
| Semantics / actual delivery | Full source→model semantic equivalence, temporal liveness with real failure/timeout, all ADS v4.18/v4.19 rules, live GitHub history and genuine release acceptance | NOT_PROVEN |

### Reproduce

Requirements: Python 3 stdlib, Z3 executable, Java and `tla2tools.jar` (TLC 2.19 in the tested environment). No Node requirement; this is formal-only evidence, not ADS's existing source/CI gate.

```bash
python formal/v4.19/r0/verify.py \
  --z3 /path/to/z3 \
  --tlc-jar /path/to/tla2tools.jar
```

To verify exact input blobs, supply a Git checkout **at PR #1365's pinned candidate HEAD**:

```bash
python formal/v4.19/r0/verify.py \
  --z3 /path/to/z3 --tlc-jar /path/to/tla2tools.jar \
  --source-checkout /path/to/pinned-candidate-checkout
```

`verify.py` regenerates `receipt.json`, and fails on a model mismatch. Mutation tests are intentionally expected to fail invariants; they count as successful detection, *not as flaws in ADS*. The normal model's invariants are consequences of its encoded guards; the result does not independently validate that the guard was translated faithfully from normative source.

## Next iteration (R1)

1. Automatically extract citations/constraints from exact Git blobs with source-to-model crosswalk and independent semantic review.
2. Model Claim/CAS generation, expiry/staleness, multi-Task parallel DAG and real role/profile orthogonality; check safety **and**, under explicit fairness assumptions, liveness.
3. Compare against historical v4.18/#1353 source and prospectively scoped v4.19 constraints without silently inheriting Drafts.
4. Reuse Z3 and TLC first; Alloy/Soufflé can improve relational coverage, Lean is only required if a stronger fully kernel-checked theorem is worth its cost.

**Status:** R0 model check PASS; all-ADS formal correctness `NOT_PROVEN`; no Freeze or release authority.
