# ADS #1366 R26 — reconcile actual R25 runs with v4.19 clause-level evidence

## Pre-execution status and correction

R25 is genuinely **closed**, not another task to dispatch: model code HEAD `6edd2bad98b455e1bcdd2895f50830412af25cff` (not the latest evidence HEAD), candidate source `dac263fa4c0ab155406d2f2117459b34322cc988`, WSL2 Python **77/77** zero skips, bounded **35/35** native, 16/16 solver differential and 3 TLC outcomes, all pin/readback checks PASS. The R24 void-source regression had a real CLI old FAIL→new PASS in the sense of evidence admission correctness (old wrongly accepted, repaired rejected).

The previous Issue top-level **“Latest completed full strict run model HEAD” still points at R11** even after R25's newer exact strict receipt. This is a stale progress index and will be corrected without changing original R11 receipts.

## Key scope finding—not a percentage of ADS proof

R25's `MODEL_AND_SOURCE_PASS` is a valid label for its **10 declared pilot properties at their exact model/head and seven specifically pinned source files**. It is **NOT** a full semantic equivalence theorem. The R8 Traceability source explicitly marks all ten properties awaiting independent equivalence review. Comparing the prospective v4.19 source changes against the pilot's declared normative sources:

- **46** manifest normative docs; **7** changed in PR #1365.
- Exactly **2** changed normative docs are directly named by any R25 pilot property: `standards/EXECUTION_PACK_STANDARD.md` and `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`.
- **5 changed normative docs have no direct source-index reference** among these 10 properties: `ARCHITECTURE_DESIGN_STANDARD`, `DEVELOPMENT_WORKFLOW`, `IMPLEMENTATION_QUALITY_STANDARD`, `TASK_DECOMPOSITION_STANDARD` and `TESTING_STANDARD`. This does *not* say they lack all other tests or qualitative review.
- The existing curated **21** candidate delta items span all 7 documents but are *review hypotheses*, not executable verification units. Exactly **one** of the 21, `TEST-01`, now has a clearer **bounded actual historical test inventory** evidence link from R20's genuine dual-environment 13 named R17 tests (and the later R25 77-test repo suite), never generalized to arbitrary Test/CI declarations.
- `TEST-02` has only synthetic missing-test negative demonstrations, not an actual newly observed omitted required production suite. `EXEC-01` and `GITHUB-01` have source/schema role-shape structural evidence, not actual legal Dispatcher Claim.

All 10 pilot model-property rows in the machine receipt preserve their exact existing trace statuses and state the external real facts assumed by their SMT/TLA abstractions. Actual proof value is bounded safety/counterexample inside these assumptions, **not conformance of physical GitHub workflow or all 21 normative candidates**.

## One-time sensible task prioritization

| Scope | Chosen next *evidence kind* | Why not create another synthetic proof |
|---|---|---|
| Testing §6.1 | Reuse actual R20 R17 test inventory receipt, no re-run | Already 13 named tests each host plus fail-closed fixture regressions |
| Architecture/Implementation §6.2 | Representative installed, actually selected public consumer result | Hook loaded or component tests cannot attest a consumer path |
| Task Decomposition | Native frozen DAG / real artifact prerequisites and ownership | A toy graph does not prove permission to edit native DAG |
| Development Workflow Stage 1 and repair | Real Git/Issue exact-source evidence and owner decision | Optional issue organization is practice, not a universal SMT invariant |
| Execution Pack + GitHub Protocol | Legally effective Project/Task policy + serialized producer Claim/CAS | Candidate Schema cannot retroactively authorize historical Tasks |

**Current finite stop**: R11/R17/R20/R25 are not to be rerun unchanged. Do not confuse 2/7 with a rule-level coverage rate. Do not rewrite older triage/index/receipt source files. This separate **evidence reconciliation overlay** makes stale evidence class upgrades visible without inventing a new normative registry.

**Output:** `formal/v4.19/r26/R26_EXACT_EVIDENCE_TO_RULE_CROSSWALK.json`; no code or policy changes, no native execution this round. A truly independent human/other source-review agent and lawful real producer remain future dependencies, explicitly NOT_PROVEN.
