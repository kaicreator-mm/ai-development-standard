# R3 — independent bounded logical challenge (experimental)

- Owner: ADS experimental formal verification branch only; **no normative ADS gate**.
- Baseline: R2 MODEL_ONLY_PASS, source equivalence and exact-SHA checkout still NOT_RUN.
- Script: [semantic_challenge.py](semantic_challenge.py) (Python stdlib only, no Node constraint).
- Run: `python formal/v4.19/r3/semantic_challenge.py`.
- Independent pre-commit local challenge used a semantically equivalent expanded implementation, not the exact committed script. The committed script's own execution receipt remains **NOT_RUN** until replayed; the counts below are locally exercised model observations, not a Git exact-artifact verified receipt.

## Observations from local equivalent model
1. R3-RELEASE-STALE: 256 combinations of 8 flags; 1 legal success; incorrect predicate accepts 3 illegal stale-CI/review combinations.
2. R3-DAG-STRUCTURE: 64 directed graphs of three tasks (no self-loops): 25 acyclic, 39 cyclic.
3. R3-FALSE-SERIAL: real edge A→B allows C independent; mutant adds B→C. Both graphs are acyclic but mutant needlessly serializes C. Cycle detection **cannot** establish dependency necessity.
4. R3-HISTORY-SCOPE: 8 combinations of frozen/revision-authorized/proposed; one mutant wrongly allows proposed policy to rewrite a frozen historical subject.

## Interpretation
- These are *bounded abstract counterexamples* to deliberately faulty policy translations, not a source-backed ADS proof.
- A positive witness and deliberate mutants reduce vacuous success but do not validate natural-language ADS → model mapping.
- Needed next: run committed R3 script at its pinned Git SHA, store exact script digest/tool/version/receipt under a new append-only record; independent source semantic mapping against actual effective v4.18 and candidate v4.19; factual dependency classification, then source-aligned proof.
- Do not count these 4 challenges as four newly proven ADS normative obligations or advance Freeze/Release based on them.
