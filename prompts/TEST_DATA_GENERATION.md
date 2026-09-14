# Test Data Generation Prompt Baseline

Use this prompt when an LLM designs or generates simulation/test data. You are designing **test evidence**, not decorative fake data.

## Inputs

Read when available: frozen PRD/scope, schema/contracts, domain rules/invariants, existing tests, real bugs/incidents, Critical Journeys, approved public/real datasets, privacy/security constraints, Hidden Validation policy.

Missing material facts must be `UNKNOWN`; do not invent business rules.

## Workflow

1. **Source Catalog** — record source identity/type, trust/authority, version/frozen date, license/usage restriction, privacy class and what it supports. Mark LLM content synthetic.
2. **Rules / Contracts** — extract required fields/types/enums, domain constraints, state transitions, permissions, failure behavior, invariants and critical decisions.
3. **Scenario Dimensions** — for each dimension provide values/range, why it matters, linked rule/risk and whether coverage is required. Do not count inert dimensions.
4. **Scenario Matrix** — design only applicable classes: normal, boundary, schema-invalid, domain-invalid, incomplete/uncertain, runtime failure injection, adversarial, regression, Critical Journey, load/scale. If a class is irrelevant, mark `NOT_APPLICABLE + rationale`; do not fabricate it.
5. **Golden Cases** — choose risk-driving semantic anchors, not a fixed count. Define input, expected decision, invariants, forbidden behavior, allowed variation, rationale, provenance and review authority.
6. **Generators** — use LLM for semantic design/natural-language content; use deterministic/property/fuzz code for bulk generation where practical. Record generator revision, seed and relevant runtime/dependencies.
7. **Generate** — curated high-value cases first; supplemental generated cases second. Keep schema-invalid separate from intended-valid data.
8. **Validate** — check integrity, intended-valid schema compliance, intended-invalid violations, rule/oracle consistency, provenance, Golden/Regression authority, risk/dimension coverage, dedup, reproducibility/hash, privacy/secrets and Hidden-data separation.
9. **Feedback** — identify inert dimensions, taxonomy mistakes, missing risks, weak Goldens, ambiguous rules, non-reproducibility, coverage gaming and project/standard gaps.

## Taxonomy Guardrails

- `schema_invalid`: contract structure/type/required/enum violation.
- `domain_invalid`: structurally valid but business-invalid.
- `incomplete/uncertain`: valid but missing/unknown/insufficient facts; expected behavior is often request/defer/low-confidence.
- `failure_injection`: actual runtime/dependency/I-O/DB failure, not missing business information.

## Golden Authority

An LLM may propose expected behavior but may not mark an LLM-only expectation `approved`. Approval requires deterministic contract/rule, approved real case, independent reviewer/domain expert, or accepted evaluator/rubric.

For LLM output, prefer schema/decision/facts/forbidden claims/invariants/evidence correctness over exact natural-language matching.

## Reproducibility

Seed alone is insufficient. Record generator name/revision and any dependency/runtime/locale/timezone/clock that changes bytes; for frozen packs record hashes.

## Required Output

Prefer a version-controlled pack:

```text
manifest.json|yaml
schema / contract / rule refs
scenario_matrix.*
cases/
  curated.*
  generated.*
  schema_invalid.*
generators/
coverage.*
VALIDATION_REPORT.md
```

## Hard Rules

- Never label an invented distribution “realistic” without evidence.
- Never use record count as the primary coverage claim.
- Never let one LLM be generator + oracle + sole approver.
- Never expose Hidden expected mapping to implementation agents.
- Never include real credentials or unapproved PII/customer data.
- Never turn an unexecuted check into PASS.
- Never invent an irrelevant scenario to satisfy a checklist; use `NOT_APPLICABLE + rationale`.
