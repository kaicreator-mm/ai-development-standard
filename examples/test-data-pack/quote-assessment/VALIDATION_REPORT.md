# Reference Test Data Pack — Validation Report

Date: 2026-09-14

## Decision

`PASS`

The reference pack satisfies the structural, provenance, scenario, Golden, reproducibility and risk-coverage checks defined for this repository example.

## Final Pack Summary

- Total cases: 27
- Curated schema-valid cases: 16
- Deterministically generated schema-valid cases: 8
- Intentionally schema-invalid cases: 3
- Golden Cases: 4
- Boundary Cases: 4
- Domain-invalid Cases: 2
- Incomplete / Uncertain Cases: 3
- Adversarial Cases: 2
- Regression Cases: 1
- Runtime Failure Injection: `NOT_APPLICABLE` for this pure decision pack; runtime dependency failure belongs in integration packs
- Risk-matrix entries: 10
- Required scenario dimensions: 5
- Validation errors: 0
- Validation warnings: 0

## Reproducibility

- Generator: `reference_quote_generator`
- Generator version: `2.0.0`
- Seed: `20260914`
- Generated data runtime: Python stdlib
- Curated cases SHA-256: `3ba19b4141e65e1f0ee302e803fbe6b9b350136ad37b543a3c9cf8b525442194`
- Generated cases SHA-256: `9495174dda12aaa413a583bc59ee7ce9af6205373633cdd3dae37fa414a70df0`
- Schema-invalid cases SHA-256: `fc1e648b13d95a8fa64ed668969936d8ccd9e787c6b21caa41237a750667cd74`

Running `generate_supplement.py` with the frozen seed reproduces the committed generated-case hash.

## Coverage Evidence

Every declared required dimension has all declared values represented:

- completeness: complete / partial / invalid
- quantity_band: negative / zero / one / normal / large / huge
- supplier_status: verified / unknown / blocked
- evidence_state: consistent / conflicting / insufficient
- text_risk: none / prompt_injection

The pack does not claim full Cartesian coverage. It uses an explicit risk matrix and records why the full product is excluded.

## Validation Feedback That Changed the Standard

### 1. Inert dimensions can fake coverage

The first pass included a dimension/value without a rule that changed expected behavior. That made the dimension look covered while adding no semantic evidence.

**Standard change:** every required dimension must state why it matters and map to a rule/risk; inert/exploratory dimensions cannot count as required coverage.

### 2. Invalid, incomplete and runtime failure are different things

The first pass used one broad failure category for structurally invalid input, business-invalid input, missing information and uncertainty. A later review also found that `missing lead time`, `unknown supplier` and `insufficient evidence` had been mislabeled as failure injection even though no runtime system failed.

**Standard change:** the final taxonomy separates:

- `schema_invalid` — contract/schema violation;
- `domain_invalid` — structurally valid but business-invalid;
- `incomplete / uncertain` — valid state where facts/evidence are missing or unknown and the correct result is request/defer;
- `failure_injection` — actual runtime/dependency/I-O/DB failure.

A pack must mark a risk class `NOT_APPLICABLE` when it genuinely has no relevant boundary rather than fabricating a case to satisfy a checklist.

### 3. Golden set was too weak

The first pass had only happy-path and missing-product Goldens and did not lock high-value risk semantics.

**Standard change:** Golden selection is risk-driven, not count-driven. The final pack adds blocked-supplier and conflicting-evidence Goldens and requires explicit invariants and allowed variation.

### 4. Reproducibility needed more than a seed

A seed alone does not identify generator behavior because generator/library upgrades can change output.

**Standard change:** record generator version/revision, relevant runtime/dependency identity and frozen hashes where appropriate.

### 5. Record count is a weak metric

The pack could be inflated with many similar normal records without increasing meaningful evidence.

**Standard change:** coverage is reported by risk class, contract/domain rule, boundary and dimension values. Duplicate/near-duplicate records cannot increase risk coverage by themselves.

### 6. LLM-generated expected answers need independent authority

An LLM can create plausible cases and rationales, but that does not make its answer authoritative.

**Standard change:** Golden expected behavior must map to deterministic rules, approved evidence, an independent reviewer/domain expert or an accepted evaluator/rubric. One LLM cannot be generator + oracle + approver.

## Remaining Deliberate Limitations

This reference domain is intentionally small. It does not attempt to demonstrate every technique, including:

- runtime dependency failure injection (explicitly N/A here);
- large-scale performance distributions;
- time-series/event ordering;
- database referential graph generation;
- image/audio/video fixtures;
- real de-identification pipelines;
- multilingual locale packs;
- hidden-data access controls.

Projects should add only applicable dimensions/risk classes and preserve the same provenance, reproducibility and validation principles.
