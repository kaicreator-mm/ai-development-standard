# Test Data Pack Template

Use this template when a project needs a version-controlled simulation/test-data pack.

## Suggested Layout

```text
<pack>/
├── manifest.json|yaml
├── schema/ or contract references
├── scenario_matrix.json|yaml|md
├── cases/
│   ├── curated.jsonl
│   ├── generated.jsonl
│   └── schema_invalid.jsonl
├── generators/
├── coverage.json|yaml
└── VALIDATION_REPORT.md
```

## Manifest Fields

```json
{
  "pack_id": "<stable-id>",
  "format_version": "<version>",
  "purpose": "<what this pack proves>",
  "privacy_classification": "<classification>",
  "schema": "<path/ref>",
  "rules": "<path/ref>",
  "target": {
    "tested_sha": "<40-char-sha when formal evidence>",
    "validation_profile": "<profile when applicable>",
    "gate_authority": "<PRD|Architecture|PROJECT_OVERRIDES|Task|Standard|NOT_APPLICABLE>"
  },
  "generator": {
    "name": "<generator>",
    "version": "<revision>",
    "seed": 0,
    "deterministic": true
  },
  "provenance": [],
  "dimensions": {},
  "files": {}
}
```

## Curated / Golden Case Shape

```json
{
  "id": "GOLD-001",
  "class": "golden",
  "dimensions": {},
  "input": {},
  "expected": {
    "decision": "<semantic result>",
    "invariants": [],
    "forbidden_behavior": [],
    "allowed_variation": "<allowed variation>",
    "exact_text_match_required": false
  },
  "provenance": ["<source-id>"],
  "rationale": "<why this case matters>",
  "review": {
    "status": "approved",
    "reviewer_type": "rule|expert|human|approved-case|accepted-evaluator"
  }
}
```

## Schema-invalid Case Shape

```json
{
  "id": "SCHEMA-001",
  "class": "schema_invalid",
  "input": {},
  "expected_validation_error": {
    "kind": "<error-kind>"
  },
  "provenance": ["<contract-source>"],
  "rationale": "<targeted contract violation>"
}
```

## Validation Report Minimum

Record:

- pack identity and revision/hash;
- tested exact SHA / profile when formal evidence;
- Gate authority when required;
- case counts by class (informational only);
- required risk/dimension coverage;
- Golden/Regression authority status;
- generator replay/hash status;
- privacy/provenance status;
- Hidden-data separation status;
- errors/warnings;
- `PASS / FAIL / NOT_RUN / NOT_APPLICABLE / BLOCKED` decision;
- feedback that should change project rules or the global standard.

Do not copy this template mechanically when the project already has a stronger native format. Preserve the semantics, not the filenames.
