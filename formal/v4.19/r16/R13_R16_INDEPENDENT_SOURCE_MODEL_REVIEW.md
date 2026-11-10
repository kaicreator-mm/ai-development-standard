# ADS #1366 — R13–R16 Fresh source/model semantic review (scoped)

**Reviewed exact experiment HEAD:** `ceeed4ae5a58b396338217323215497d7325570b` · **TREE:** `76a4440b49d3ff8bad105e3c785fccd50ba46870`. The only write in this review is the new R16 review/receipt pair; earlier R0–R16 evidence, models, execution scripts and official ADS standards are unchanged.

**Prospective normative subject:** [PR #1365](https://github.com/kaicreator-mm/ai-development-standard/pull/1365) `dac263fa4c0ab155406d2f2117459b34322cc988` (**OPEN, UNMERGED**). Actual reviewed protocol blob `935a905d593d7aec027cb54b5b137250ca14a4c1`; dispatch schema blob `5d9233b6b881d9d92f66fc6cd5307a05a0fdbe2f`. These are not current released ADS authority for an arbitrary project.

## Independent method and evidence layers

This review is a *fresh source-first examination* of the named GitHub blobs and model/runner/test code, not acceptance of a Builder summary. **32/32** direct source/receipt assertions matched (exact refs, guards, query count, schema/reused checker, explicit limitations). A separate small propositional evaluation produced **10/10 countermodels to the acceptance safety predicate when its asserted implication is removed**; this is a reviewer logic witness, **not a Z3/cvc5 rerun and not a real Controller trace**. R16's **9/9** previously reported positive file blobs matched the recorded exact source commits. The five original R16 missing-file rows had no immutable commit; each missing path was **freshly reread as GitHub 404 at a newly pinned main commit** (details in companion machine receipt), avoiding inference that ADS is unused.

Historical genuinely executed receipts retain their own SHA qualifications, *without rerun*: R13 Z3/cvc5 **16/16 each** and 7/7 native mutants at the recorded R13 model hashes; R15 exact-source Python **13/13** in both WSL2 and Windows at repaired HEAD `4de398a02f4c96d20ad763ea11d81a9a40ff0266` after the real pre-fix zero-test import failure. R11 **35/35 native and 61/61 Python** are older, independently scoped. No native Z3/cvc5/TLC or full Python test was executed on *this* reviewed HEAD; do not sum historic test counts into current PASS.

## Four-round semantic disposition

| Round | Actual source and model finding | Scoped result |
| --- | --- | --- |
| R13 | The safety relation `(acceptedDispatch OR acceptedClaimMutation) => publishAdmissible` is **asserted**, not derived from real Controller/Claim code. 10 negative UNSAT results and 7/7 mutations check this assumed guard; the P01 SAT witness only shows non-vacuity *within the model*. The old `reservedA` is a **reservation proxy**, not accepted publication. | **PASS** model/solver receipt integrity within hypothesis; **BLOCK** production invariant/semantic equivalence |
| R14 | The protocol explicitly requires preflight **before READY/QUEUED or accepted**; the R13 model lacks early READY/QUEUED publication, event ordering and actual bytes/CAS/readback. R14-GAP-01/02/03 remain real **coverage gaps**, not proved normative defects. | **PASS** source→model gap identification; **NOT_PROVEN** complete DP-02/05/06 |
| R15 | Exact prospective schema fixture matches `5d9233b...`, the experiment/candidate `assert_supported_schema` and `validate_subset` source bodies are equal at pinned refs; 13/13 exact-source Python results after repaired import are supported by stored dual-host receipt. However validator `requested_head_sha` and `validation_profile` can be null; a well-formed but unrelated 40-hex `pinned_standard_revision` and READY record can be syntactically valid. Every checker result retains `publication_authorized=false` and `canonical_admission=NOT_PROVEN`. | **PASS** syntax-only boundary and historic repaired-source evidence; **BLOCK** real publication admission |
| R16 | Original 14 named ref observations: 8 old-version exact ADS pins, 1 version-only, 5 path-only 404, **zero confirmed exact v4.19 candidate producer in the sample**. All nine positive source blobs independently reread. Five missing refs now pinned to exact commit in this review. No lawful current v4.19 Task/Claim producer has been proven. | **PASS** scoped survey/source readback; **UNKNOWN** organization-wide adoption; **NOT_PROVEN** real E2E |

## Review findings (strictly separate from ADS normative defects)

**R13-R16-REV-P2-01 — experiment proof/source-identity gap; OPEN, P2.** `run_proofs.py` checks exact *model blobs* and both native tool binaries before and after execution; it does **not** check candidate `GITHUB_AGENT_INTERACTION_PROTOCOL.md` or PR #1365 HEAD before launching. The source→model relation is a prose/source-review assumption. If any future report upgrades these native results to “source equivalence PASS,” require a separate exact candidate-source preflight and **independent semantic conformance check**. No existing receipt is inaccurately upgraded in this review. Not a demonstrated ADS normative or production security bug.

**R13-R16-REV-P2-02 — original R16 404 reproducibility gap; MITIGATED IN NEW RECEIPT, P2.** The five prior `PIN_FILE_NOT_FOUND_AT_CHECKED_REF` records carried `ref=main` but no immutable HEAD. This review re-read five newly pinned SHA subjects and observed 404 for that specific path. The new evidence **does not** retroactively prove the earlier 404 occurred at exactly those SHAs; the old receipt remains unchanged, and 404 remains UNKNOWN for broader ADS usage. No repair to product or policy source is warranted.

**Existing coverage restrictions, not additional P0/P1/P2 normative findings:** R14-GAP-01/02/03, R15-OBS-01/02/03, real authorized v4.19 producer/source pin, GitHub accepted Claim/CAS and durable readback, effective Release authority, complete ADS atomic rule denominator. The R13 Bool model is at most a collection of *necessary conditions* and no source-derived preservation theorem.

## Decision and handoff

```ini
R13_R16_SCOPED_REVIEW=PASS_SCOPED_SOURCE_MODEL_REVIEW_WITH_P2
ADS_NORMATIVE_P0_P1_P2=0/0/0
EXPERIMENT_P0_P1_P2_OPEN=0/0/1
R16_PROVENANCE_P2=MITIGATED_BY_NEW_EXACT_SHA_READBACK
REAL_SOURCE_MODEL_EQUIVALENCE=NOT_PROVEN
R13_NEW_NATIVE=NOT_RUN
R15_NEW_PYTHON=NOT_RUN
REAL_V419_DISPATCH_CLAIM_CAS=NOT_PROVEN
FULL_ADS_RULE_DENOMINATOR=UNKNOWN
NORMS_OR_PRODUCT_WRITES=NONE
PR1365_MERGE_FREEZE_RELEASE=NOT_RUN
```

This is an independently **reasoned source review**, not a cryptographically distinct human reviewer identity: the GitHub transport identity does not establish independent personhood. Do not promote it to a separate external signed Review gate if that is required. With no eligible real producer, further synthetic Bool rounds have diminishing value; first obtain legally effective project/Task/version adoption and real checked object → serialized READY/QUEUED/accepted GitHub mutation → durable readback if the product later chooses to validate true runtime semantics.

**Machine-readable companion:** [R13_R16_INDEPENDENT_REVIEW_RECEIPT.json](./R13_R16_INDEPENDENT_REVIEW_RECEIPT.json).