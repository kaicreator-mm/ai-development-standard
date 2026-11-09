# ADS formal R2 coverage and qualification — 2026-11-09

## Actual execution

- Experiment branch: `experiment/v4.19-formal-proof-r0`, prospective PR #1365 exact candidate `dac263fa4c0ab155406d2f2117459b34322cc988`; **not merged/frozen**.
- Native Z3 5.3.3, cvc5 1.4.2 and TLC 2.19 were used in the current Linux x86_64 container.
- **19 executed cases:** 13 normal `PASS_MODEL`; 6 expected mutant/invariant `COUNTEREXAMPLE`; **0 failed checks**.
- **6 independent SMT solver comparisons:** Z3/cvc5 agree, including finite-four-node cycle check and legal witnesses.
- TLC normal 27 distinct states, two deliberate invariant violations reproduced with 7/3 distinct states respectively.
- Seven distinct, declared pilot properties have at least one executed case: **7/7 pilot obligations**. This is **NOT** full ADS coverage.
- Six pinned GitHub candidate source files match exact Git blob and anchor strings **6/6**; canonical execution DAG standard additional anchor checked. Separate Python exact checkout verification remains `NOT_RUN`.

## Honest denominators

| Metric | Verified | Denominator | Qualification |
|---|---:|---:|---|
| Declared pilot property exercised | 7 | 7 | MODEL_ONLY, bounded |
| Normal checks expected | 13 | 13 | Native tools executed |
| Deliberate mutant detections | 6 | 6 | Native tools executed |
| Z3/cvc5 parity | 6 | 6 | Native tools executed |
| Candidate GitHub source blob/anchor readback | 6 | 6 | GitHub readback only |
| Source-bound Python strict-checkout properties | 0 | 7 | NOT_RUN: exact checkout absent |
| Full ADS normative rules | UNKNOWN | UNKNOWN | Inventory and rule denominator not built |
| Independently reviewed source→model semantic mappings | 0 | 7 | Independent reviewer NOT_RUN |
| General/unbounded DAG safety | NOT_PROVEN | n/a | Four-node finite model only |
| Liveness under explicit fairness | NOT_PROVEN | n/a | TLC verified safety, not temporal progress |

## T00–T08 execution outcome

| Task | Result | What is still missing |
|---|---|---|
| T00 tools | PARTIAL: manifest, checksums for selected artifacts, actual Z3/cvc5/TLC smoke and runs | other tools deliberately NOT_RUN; only used tools required |
| T01 source crosswalk | PARTIAL: 7 pilot properties, GitHub blob/anchor readback, forward/reverse indices | all v4.18 rules denominator, effective scope adjudication, exact local checkout |
| T02 Python suite | FUNCTIONAL PILOT: original runner extended; bounded subprocess, native SMT/TLC, mutation, selection, fail-closed unknown and stale | broader tool adapters as justified, separate independent audit |
| T03 lifecycle/authority | BOUNDED_PASS: actual TLC and Z3/cvc5 | Claim expiry/CAS, multiple Tasks, liveness fairness |
| T04 DAG and Writer | BOUNDED_PASS: rank-four DAG repair and mutant | arbitrary graph algorithm, native Task DAG ingestion, false serial edges |
| T05 evidence/evolution | BOUNDED_PASS: exact-subject logical equality and historic/prospective scope | real cryptographic verification, historical revisions and actual evidence chain |
| T06 cross-model | BOUNDED_PASS: integrated SMT safety | richer state/interface alignment, failure and recovery |
| T07 adversarial semantic review | PARTIAL: deliberate mutations and same-builder challenge | independent semantics evaluator NOT_RUN |
| T08 incremental/report | FUNCTIONAL PILOT: changed-source selection invalidates prior proof and strict mode blocks without checkout | automatic Git diff change impact, denominator inventory, source-bound qualification |

## Model findings and action

- **MODEL_COVERAGE_DEFECT (R1; improved in R2)**: triangle-only cycle check insufficient. Four-node all-directed-edge rank model now detects 2/3/4 cycles, with legal paths and an injected D→A guard omission witness; still bounded.
- **SUITE_DEFECT (fixed)**: cvc5 must run with `--incremental`; solver `unknown` now results in `INCONCLUSIVE`. Both validated.
- **ADS_NORMATIVE_DESIGN_DEFECT**: none demonstrated by this pilot. Do not infer full correctness from absence of counterexamples.
- No new FIR, runtime status engine, Claim authority, mandatory CI gate or ADS normative change was introduced.

### Reproduction

```bash
python formal/suite/run.py --suite formal/v4.19/r2/suite.json \
  --z3 /path/to/z3 --cvc5 /path/to/cvc5 --java java \
  --tlc-jar /path/to/tla2tools.jar \
  --out /tmp/ads-formal-r2-receipt.json

ADS_FORMAL_Z3=/path/to/z3 ADS_FORMAL_CVC5=/path/to/cvc5 \
  python -m unittest discover -s formal/tests -v
```

For source-bound output, use a second Git worktree with HEAD `dac263fa4c0ab155406d2f2117459b34322cc988`, and pass `--source-checkout /path/to/candidate-worktree --strict-source`. **Do not point --source-checkout at the experiment branch.** Leave originals and receipts immutable; source changes require a new round.
