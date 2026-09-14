# Reference Test Data Pack — Quote Assessment

This is a deliberately small, framework-neutral example used to exercise `standards/TEST_DATA_AND_SCENARIO_STANDARD.md` end to end.

It is **not** a business-domain standard and does not contain real customer or production data.

## What it demonstrates

- contract/schema-derived structure;
- explicit domain rules;
- provenance catalog;
- scenario dimensions with behavioral/risk rationale;
- risk-based Scenario Matrix rather than a full Cartesian product;
- curated Golden Cases;
- separate schema-invalid and domain-invalid data;
- boundary, failure-injection, adversarial and regression cases;
- deterministic generated supplements with a fixed seed;
- coverage and reproducibility hashes;
- validation feedback used to improve the standard itself.

## Files

```text
manifest.json
schema.json
RULES.md
scenario_matrix.json
cases/
  cases.jsonl
  schema_invalid.jsonl
coverage.json
VALIDATION_REPORT.md
```

## Validation

Repository CI validates pack structure through `scripts/verify_test_data_pack.py` and checks this reference domain's expected decisions/invariants through the standard repository verification flow.

The frozen reference result is recorded in `coverage.json` and `VALIDATION_REPORT.md`.
