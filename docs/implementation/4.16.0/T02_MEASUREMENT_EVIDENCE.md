# T02 — Physical accounting and clock reconciliation (ADS v4.16)

**Source-only concern:** [Issue #1266](https://github.com/kaicreator-mm/ai-development-standard/issues/1266). Integration source `version/v4.16@3041a1be3f130e5cc5e676c2e56a99882adfd97c` after upstream T01 source merge; frozen R4 P1-03 blob `fcde65f728a87d6ecd073a37b145fdb5548367b1`. **No provider API/runtime/ledger/invoice observation or production billing proof** follows from the Python oracle.

## Existing normative decisions reused, not redesigned

- v5 `ads/github/v5:report` is a strict *shape* contract, not evidence that declared `source_receipt_ref`, `window_current`, provider alias, clock, invoice or publisher namespace is genuine. External owner and native readback must qualify each witness separately before passing rows to this reducer.
- A GitHub public report revision/digest is **not** a physical Attempt ID, metric event ID or accounting receipt. Deduplicate the *same* source observation with identical `source_digest`; same identity and revision but different source digest/value is `CONFLICT`. Distinct Task/Attempt/provider/adapter/physical retry keys must not collide because their local indices match.
- Group measurement by publisher + Task + Attempt + adapter + provider run + physical attempt, versioned metric/registry/unit, qualified window and original observation ID. Do not add transport duplicates, late revisions, included cache/reasoning subsets, parent/child scopes or mixed delta/cumulative events. Source-only `COUNTER_DELTA` adds nonoverlapping named observations; `CUMULATIVE_SNAPSHOT` chooses the latest witnessed monotone watermark and rejects changed/wrongly ordered source. `UNKNOWN` is not zero.
- Billing identity excludes GitHub Report revision: publisher/economic scope/provider receipt/currency/category/window plus its **source** revision/lineage. A verified **settled** bill may displace a quote/estimate in the *same* scoped population; multiple overlapping bills without reconciliation, missing settlement, disjoint coverage, cross-currency conversion or incomplete invoices remain `UNKNOWN/NOT_COMPARABLE`. Only an actual owner can certify disjoint scopes/settlement.
- Time union requires one provably common clock domain and witness; source `window_id` is an opaque lookup key, not endpoints. Never total wall time from different clocks or add overlapping parent spans.
- Positive cases in `tests/fixtures/v416/t02/scenarios.json` are **synthetic** source-contract examples. `scripts/v416_measurement_reconciler.py` has no native GitHub reader and no provider network. It must not be imported as a production accounting control without external source qualification and replay/pagination/privacy proofs. T03 owns the full GitHub public verifier and v3/v4/v5 dispatch.

## Executable concern tests

Run `python scripts/test_v416_t02_measurement.py` using Python 3.14 or another supported modern Python with `decimal`; its result is based on verified source bytes and expected reducer behavior, not interpreter version. This is bounded C02 (identity/revisions), C03 (physical scope), C04 (counter/watermark), C05 (cost), C12 (interval union) coverage. Actual native provider receipt, clock synchronization, settlement completeness and task-meta/Tally real E2E remain **NOT_RUN**.

**Source-only status** remains implementation candidate until actual test readback, independent exact-HEAD Review and version-only merge. Preserve v5 Schema and all old v4 Schema/Protocol bytes, no new Agent/Claim/Gate state.
