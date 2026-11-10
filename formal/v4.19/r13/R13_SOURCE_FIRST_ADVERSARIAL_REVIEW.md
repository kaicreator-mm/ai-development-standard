# #1366 R13 — source-first adversarial review and exact-byte binding repair

**Source authority:** Candidate PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988`, `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` Git blob `935a905d593d7aec027cb54b5b137250ca14a4c1`, still OPEN/unmerged.

**Provenance / review scope:** Fresh adversarial source reading by the **same Web Builder**, not an independent reviewer. This is a bounded R13 source-to-model interpretation audit, not a full source/model refinement theorem.

## Reassessment and P2 repair

The R13 models' native 30/30 pair and 6/6 original mutation outcomes were real, but the `run_proofs.py` runner merely printed each model Git blob. It failed to *compare* that blob against the fixed exact model under review. A comment-only model change could yield the same SAT/UNSAT statuses and falsely receive PASS. This is `R13-RECEIPT-P2-01`, an **experimental evidence reliability** defect, not an ADS normative defect.

Repaired `run_proofs.py` now checks the two reviewed model Git blobs and the Z3/cvc5 executable SHA256 pins both **before any native subprocess** and **after** execution. An invalid model or tool produces BLOCK, never an inherited PASS. The mutation harness also pre/post-binds the original models/tools; its **temporary mutated copies** deliberately have different blobs and are accepted only as negative test subjects.

**Actually executed:** Python 3.13.5 preflight tests **6/6 PASS** (comment-only drift, missing model, absent/incorrect binary, postflight drift, positive identity), Z3 5.3.3/cvc5 1.4.2 **15/15 each / 30/30 pairs PASS**, 2/2 model+tool pre- and postflight PASS, and **6/6 native mutation tests detected**. Correctly bound native binary hashes: Z3 `fcd0ca765d1c0b4eac776f442ec0f10294b9a6416be91fad4e52fa19012c8d01`; cvc5 `6aecddf466552b83bb5883756c7955e0c9d5ddcc6d7f45b48c2f6e06a741b102`.

The new executed result files are `REBOUND_SOLVER_EXECUTION.json` and `REBOUND_MUTATION_EXECUTION.json`, with Git blobs `aece22437c9329f5ad11922cc1a3a318a7148905` and `ecb0bfce2d0530b3db2c2e5651cb2e37769b945f`. Original historical `SOLVER_PAIR_EXECUTION.json`, `MUTATION_EXECUTION.json`, and `R13_BOUND_EVIDENCE.json` are deliberately retained **unchanged** and remain tied to HEAD `ffe25023aa6652b9ac796b037ed5216bbfaa53c9`.

## Source/model interpretation and limitations

| Candidate atom | Bounded R13 abstraction | What is not established |
|---|---|---|
| `DP-01F` | `fullEnrichedPayloadChecked` boolean | Actual complete JSON Schema/required-field validation |
| `DP-01S` | `pinResolved`; `checkedSchema = pinnedSchema` | Effective project/Task revision lookup and cryptographically checked schema bytes |
| `DP-02` | `prePublicationCheckCompleted` boolean | A time-ordered trace proving the preflight precedes publication |
| `DP-05` | abstract payload/schema equality | Real byte-level identity and GitHub CAS/readback |
| `DP-06` | accepted Dispatch or Claim mutation implies the assumed guard | Actual durable zero-accepted-write outcome when the producer rejects |

Crucially, old R8 `reservedA` models a **reservation**, not an accepted canonical Dispatch. Its SAT witnesses only show an unconstrained reservation abstraction; they do not demonstrate a source policy violation. The new model **assumes** its safety guard and proves the selected forbidden states UNSAT under that assumption. It does not verify an implementation, historic invalid-record preservation, live claim serialization, or any effective v4.19 consumer.

**Qualification:** `R13_BYTE_BOUND_NATIVE_PASS`; `SOURCE_TO_SMT_REFINEMENT=NOT_PROVEN`; `ACTUAL_GITHUB_CAS=NOT_PROVEN`; `INDEPENDENT_SEMANTIC_REVIEW=NOT_RUN`; `FULL_ADS_NORMATIVE_DENOMINATOR=UNKNOWN`. Historical R11 35 native/61 Python remains exact-SHA qualified and **not** re-run for R13-only files.

The best next step is a separate source-first semantic review against these five exact candidate atoms and their exceptions, rather than another synthetic SMT state machine. No ADS normative edit, GitHub Actions, Gate, merger, Freeze, Release, or Local Agent dispatch.
