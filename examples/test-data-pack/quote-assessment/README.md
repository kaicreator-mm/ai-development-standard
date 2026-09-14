# Reference Test Data Pack — Quote Assessment

This small, framework-neutral pack exercises `standards/TEST_DATA_AND_SCENARIO_STANDARD.md` end to end. It is **not** a business-domain standard and contains no real customer/production data.

## Demonstrates

- schema/contract-derived structure and explicit domain rules;
- provenance catalog;
- scenario dimensions with behavioral/risk rationale;
- risk-based Scenario Matrix rather than a Cartesian product;
- curated Golden/Boundary/Domain-invalid/Incomplete/Adversarial/Regression cases;
- intentionally schema-invalid data stored separately;
- deterministic generated supplements with fixed seed + generator version;
- coverage and frozen hashes;
- `NOT_APPLICABLE + rationale` for runtime failure injection because this pack has no runtime dependency boundary;
- validation feedback that changed the standard itself.

## Files

```text
manifest.json
schema.json
RULES.md
scenario_matrix.json
cases/
  curated.jsonl
  generated.jsonl
  schema_invalid.jsonl
generate_supplement.py
coverage.json
VALIDATION_REPORT.md
```

## Validation

`python scripts/verify_test_data_pack.py examples/test-data-pack/quote-assessment`

Repository `verify-standard` also validates this pack and replays the deterministic generator in a temporary directory, comparing the generated SHA-256 with `coverage.json`.
