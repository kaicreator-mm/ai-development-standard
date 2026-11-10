# #1366 R15 — Real candidate dispatch Schema: shape vs admission

**Reassessment:** R11 and R13 have fixed-SHA historical strict passes. R14 isolated a concrete source→model refinement gap: `schemaPass` and `schemaBytesVerified` were asserted, not verified against the actual Schema bytes. Instead of building another synthetic Controller or repeating SMT, R15 reads the **actual** PR #1365 `schemas/dispatch.schema.json` and creates a fail-closed, reusable Python syntax boundary backed by the repository's existing `scripts/test_protocol_schemas.py` checker.

**Source identity:** prospective PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` OPEN/UNMERGED; Schema blob `5d9233b6b881d9d92f66fc6cd5307a05a0fdbe2f`, protocol `935a905d593d7aec027cb54b5b137250ca14a4c1`. The new fixture `fixtures/dispatch.schema.json` references the **same Git blob** as the PR source, rather than hand-copying the schema or inventing a new one.

## Concrete findings

1. `LOCAL_VALIDATION` must use validator role and a real exact-SHA subject by protocol; however the candidate Schema's `requested_head_sha` and `validation_profile` are **required but may be null**. The actual source Schema accepts both nulls. This is **not automatically a schema bug**: source syntax is only one layer, runtime may have more predicates. It is an observable reason to refuse promotion of `SHAPE_VALID_ONLY` to authorized validation/Claim.
2. `pinned_standard_revision` requires a 40-hex shape, not a real lookup of the active project/Task revision. An unrelated 40-hex string remains syntactically valid; a valid syntax is not an effective source pin.
3. `dispatch_state=READY` can be shape-valid regardless of measured check-before-write order. The actual schema and this script cannot prove a serialized publish, no-accepted-mutation rejection, GitHub CAS, or readback.

## Implementation

- `schema_boundary.py`: Git blob identity check **before** importing Schema semantics; reuses `assert_supported_schema` / `validate_subset` from `scripts/test_protocol_schemas.py`; emits structured `EXACT_BLOB_PASS/SHAPE_VALID_ONLY/INVALID_SCHEMA/BLOCK` with `canonical_admission=NOT_PROVEN` and `publication_authorized=false` regardless of shape success. The CLI never performs a GitHub write.
- `test_schema_boundary.py`: 12 reproducible unittest cases against exact fixture, including nullable validator fields, profile/role mismatch, malformed SHA, wrong-but-well-formed source revision and mutated schema bytes. Run in a checkout with `python -m unittest discover -s formal/v4.19/r15 -p 'test_schema_boundary.py' -v`.
- `fixtures/dispatch.schema.json`: candidate Schema Git blob reused exactly, not normalized/reformatted.

## Execution evidence and qualification

- **14/14** real candidate Schema behavior scenarios matched expectations in a fresh in-session source-backed JavaScript JSON-Schema-subset structural evaluator. This is **not** execution of the checked-in Python code and not an independent reference JSON Schema implementation.
- **12/12** Python unit tests ran and passed in an isolated container using a **synthetic subset fixture + local stand-in checker**, confirming the Python boundary/test logic only. These are not 12/12 tests against the full candidate source.
- **Exact candidate fixture + real repository Python checker together: NOT_RUN** here. Their full Git blobs and test suite are now committed so a normal repository checkout can run the above command without inventing another local orchestration. No native Z3/cvc5 or TLC test was rerun; R11/R13 historical receipts continue to bind their prior SHA only.
- **Real v4.19 producer / project pin / Claim/CAS/readback: NOT_PROVEN.** External independent source-model reviewer: NOT_RUN. Full ADS rule denominator: UNKNOWN. Normative defect P0/P1/P2 = 0/0/0 (none confirmed in this bounded audit).

**Decision:** Reuse the original Schema checker, never treat a syntactically valid Schema/READY as an accepted Dispatch. Next highest-value work is source-bound Python full-suite readback or a genuinely authorized v4.19 real publisher, whichever is available first. No formal standard edits, new Gate, GitHub Actions, merge, Freeze, Release or unnecessary Local dispatch.


## R15 post-publication source audit correction

**Evidence-hardening defect (R15-P2-01, experiment-only):** the first Python `assess(..., expected_blob=...)` signature let a library caller override the exact expected Git blob, potentially presenting an arbitrary Schema as `EXACT_BLOB_PASS`. The CLI did not expose this parameter and all results still returned `publication_authorized=false`, but the evidence label itself could be misleading.

**Fix:** remove the caller-controlled override; `assess` now reads the fixed constant internally. A new negative unittest rejects an `expected_blob` argument. This changes the checked-in test declaration from 12 to **13**, but the new full exact-blob Python integration test is **NOT_RUN** in this environment; the prior 12/12 synthetic fixture result is a historic, narrower verification of the pre-fix logic and is **not transferred** to this exact revision.

**Dependency reuse check:** experimental `scripts/test_protocol_schemas.py` blob `248d652a890dd069322308bce90da2528ba0ad82` differs from candidate PR source blob `96edf2413e35a90d8049e529c11e832637dbaabd`, but direct fresh source comparison of the full `assert_supported_schema` + `validate_subset` function bodies (5,706 characters) was **byte-for-byte identical**. This is source-level alignment of the reused checker core, not a run against actual full source. No replacement checker or new JSON Schema framework was introduced.
