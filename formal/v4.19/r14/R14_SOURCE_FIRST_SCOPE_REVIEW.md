# ADS #1366 R14 — Fresh source-first review of R13 Dispatch proof scope

**Execution class:** Delivery-First / Web-First; **static GitHub-source review only**, not a rerun of Python/Z3/cvc5/TLC or an external independent Reviewer verdict.

**Exact source under review:** PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` (OPEN, unmerged). Candidate protocol Git blob `935a905d593d7aec027cb54b5b137250ca14a4c1`. R13 experiment `5822bb85fc6ffcba2da10581db14d52ff680c3a9`, TREE `52bf0780797643cf544c049f1a8afe3e178126a5`; published R13 SMT blob `515454a82171c668739708ef50c46a254dcd9cc8`. Evidence is pinned in [SOURCE_MODEL_READBACK.json](./SOURCE_MODEL_READBACK.json).

## Execution reassessment

R11 already has historical 61/61 Python, 35/35 native, 16/16 paired strict evidence at its exact tested model/source; R13 has executed 32/32 Z3+cvc5 and 7/7 mutants at the frozen prior HEAD. The latest R13 repair fixed the previously missed `schemaBytesVerified` negative. Repeating those tests without changing the underlying model would add no independent normative semantic evidence. Focus on the actual source/logic relation and what is missing.

**Performed this round:** re-read candidate protocol §§8.1, 10 (lines 577–583), the current R13 SMT, pinned runner and guard regression directly from GitHub. **16/16 exact-source/structural checks passed**. This is a source-readback result, not a native proof run or runtime observation.

## Clause-to-model audit

| Curated atom | Source requirement | R13 representation | Review qualification |
|---|---|---|---|
| DP-01F | Fully enriched object, complete schema validation | `fullEnrichedPayloadChecked` and `schemaPass` | Boolean assumption; no actual JSON Schema invocation |
| DP-01S | Active project-pinned ADS revision and checked schema bytes | `pinResolved`, `schemaBytesVerified`, `checkedSchema=pinnedSchema` | No active pin lookup/hash derivation |
| DP-02 | Validation **before READY/QUEUED OR accepted publication** | `prePublicationCheckCompleted`, `acceptedDispatch` | **R14-GAP-01/02:** no READY/QUEUED visibility or ordered execution trace |
| DP-05 | Checked object/schema same at the write boundary | Uninterpreted `SchemaIdentity` and `PayloadIdentity` equality | Abstract identity, not an actual serialized byte comparison/CAS |
| DP-06 | Failure yields no accepted dispatch/Claim mutation | `(acceptedDispatch OR acceptedClaimMutation) => publishAdmissible` | The safety implication is **asserted**, not inferred from real writer behavior |

## Material observations

**R14-GAP-01 — READY/QUEUED publication is out of R13's guarded state.** Protocol line 577 requires admission before publishing a new durable dispatch as READY/QUEUED *or* accepted. R13 only guards `acceptedDispatch` / `acceptedClaimMutation`. It cannot establish safety of an early but not-yet-accepted READY/QUEUED publication. This is a **bounded-model coverage limitation**, not evidence such a publication occurred. Do not silently promote R13 to a complete DP-02 proof.

**R14-GAP-02 — time ordering is assumed.** `prePublicationCheckCompleted: Bool` is not a temporal relation: a hypothesis where the variable is true but a real check happens *after* the GitHub write is not excluded through a measured event order. R13 has no clock/order or step transition; the solver's UNSAT cannot certify before/after semantics. No claim that temporal counterexample was executed against a real producer.

**R14-GAP-03 — real source bytes, schema execution, atomicity and historical readback are not modeled.** Protocol lines 579–581 demand these real behaviors; R13's booleans and uninterpreted equalities deliberately have no authenticated runtime derivation. Historical invalid dispatch preservation and corrected emission are outside the model. The old R8 `reservedA` is still a reservation proxy, not a canonical accepted event.

## Findings and disposition

- **Confirmed ADS normative defects:** P0=0, P1=0, P2=0 in reviewed material; no new production-defect report.
- **Open verification gaps:** R14-GAP-01/02/03. These are scope/refinement gaps, not new numbered normative defects or retroactive test failures.
- **Validated qualification:** `SOURCE_MAPPING_PASS / SEMANTIC_EQUIVALENCE_NOT_PROVEN / INDEPENDENT_EXTERNAL_REVIEW_NOT_RUN`. The 10 negative SMT queries and historical 32/32 paired result are not changed or relabeled.
- **Next cost-effective check:** obtain a legally effective ADS v4.19 producer/Task/Claim pin; read its actual schema validation, READY/QUEUED publication and durable accepted event/Claim readback in one bounded trace. If unavailable, commission a separate independent source-to-model reviewer. Do **not** invent another Controller, retest R11 without impact, or claim complete ADS coverage.

**No writes to ADS standards, v4.19 candidate, R11/R13 model/runner, historic receipts, CI gates, release, or merge.** The full ADS atomic-obligation denominator remains UNKNOWN.
