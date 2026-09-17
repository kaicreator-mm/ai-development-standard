# Test Data & Scenario Standard

## 1. Purpose

This standard defines the source, construction, validation, provenance, storage, and evolution of simulation data, test scenarios, Golden cases, regression data, synthetic generators, and Hidden Validation data.

It complements:

- `TESTING_STANDARD.md` for test-layer strategy;
- `VALIDATION_STANDARD.md` for Gate state/evidence semantics;
- `RELEASE_STANDARD.md` for Candidate/Release authority.

A Test Data / Scenario Gate is **not automatically mandatory for every project**. It becomes required only when the normal Gate Authority chain requires it:

```text
Frozen PRD / Contract
→ Frozen Architecture
→ PROJECT_OVERRIDES
→ Task acceptance
→ Standard defaults
```

## 2. Hard principles

1. Test data MUST derive from contracts, schema, domain rules, approved examples, incidents, public/approved datasets, or explicit evidence; an LLM must not invent domain truth.
2. **Scenario before records**: define sources, rules, risk dimensions, and the Scenario Matrix before bulk generation.
3. Golden cases MUST state expected behavior, invariants, forbidden behavior, allowed variation, rationale, provenance, and approval authority.
4. An LLM may design scenarios and generate semantic inputs but is not the default Golden oracle.
5. LLM-generated data used as formal evidence MUST pass independent schema/rule/invariant validation.
6. Synthetic generators SHOULD be replayable and record generator revision, seed, and relevant runtime/dependency identity.
7. Bugs/incidents SHOULD become minimal reproduction + Regression Case.
8. Hidden Validation input/expected mappings that could cause overfitting MUST remain unavailable to implementation agents.
9. Record count is not coverage; coverage maps to contract, rule, risk, boundary, Critical Journey, or regression.
10. One LLM MUST NOT be generator + expected-answer oracle + sole approver for the same formal evidence.
11. Test-data evidence still obeys exact-SHA and Validation Tuple rules when used by a required Validation Gate.
12. Test-data quality evidence cannot substitute for an unexecuted Critical Journey, Hidden Validation, platform build, or other required Gate.

## 3. Scenario taxonomy

Use only classes that apply:

- **Fixture** — small stable input used by tests.
- **Scenario** — user/system state, risk, or failure condition.
- **Golden Case** — high-value semantic baseline with independent authority.
- **Boundary Case** — min/max/empty/null/precision/time/size/state boundary.
- **Schema-invalid Case** — structure/type/required/enum violation.
- **Domain-invalid Case** — structurally valid but violates a domain rule.
- **Incomplete / Uncertain Case** — structurally/domain valid but missing facts/evidence; correct behavior is often request/defer/low-confidence.
- **Failure Injection Case** — runtime/dependency/I-O/DB/permission failure.
- **Adversarial Case** — malicious, conflicting, untrusted, ambiguous, prompt-injection, or evidence-confusion input.
- **Regression Case** — derived from a known bug/incident.
- **Critical Journey Dataset** — supports end-to-end critical business outcomes.
- **Hidden Validation Dataset** — independent data unavailable to implementation agents when required by Hidden Validation policy.
- **Load / Scale Dataset** — performance/capacity/stability data.

`schema_invalid`, `domain_invalid`, `incomplete/uncertain`, and `failure_injection` MUST NOT be collapsed into one generic `failure` class.

If a risk class is irrelevant, record `NOT_APPLICABLE + rationale`; do not fabricate cases merely to complete a checklist.

## 4. Sources and provenance

Preferred source order:

1. approved real/de-identified test data or production-derived aggregate statistics;
2. real examples, tickets, incidents, reviewed cases;
3. authoritative public datasets/standards;
4. frozen PRD/contract/schema/domain rule/Decision Model/accepted ADR;
5. expert/product/tester-defined cases;
6. synthetic data derived from the above by deterministic code or LLM.

Lower-authority synthetic data MUST NOT override higher-authority confirmed facts.

A formal pack SHOULD maintain a Source Catalog containing source id/type, version/frozen date, license/usage restriction, privacy classification, and the rules/fields/Golden cases it supports.

LLM-derived content must be marked synthetic/LLM-derived.

Secrets, credentials, unapproved PII/customer data, and raw production dumps MUST NOT enter the repository as ordinary fixtures.

## 5. Standard construction workflow

```text
PRD / Contract / Schema / Rules / Incidents / Approved Examples
        ↓
Source Catalog + Privacy Constraints
        ↓
Rules / Invariants / Critical Decisions
        ↓
Scenario Dimensions + Risk Rationale
        ↓
Scenario Matrix
        ↓
Curated Golden / Boundary / Invalid / Incomplete / Adversarial Cases
        ↓
Deterministic / Property-based / Fuzz / LLM-assisted generation
        ↓
Schema + Rule + Invariant Validation
        ↓
Coverage + Dedup + Reproducibility + Privacy Review
        ↓
Test / Regression / Critical Journey / Hidden assets
        ↓
Feedback to project rules or global standard
```

If material contract/expected behavior is `UNKNOWN`, preserve `UNKNOWN`, `NOT_RUN`, or `BLOCKED` as appropriate; do not let the data generator invent a business rule.

## 6. Scenario dimensions and risk matrix

Each dimension counted toward required coverage MUST record:

- values/range;
- why it matters;
- linked contract/rule/risk;
- whether it is required.

An inert dimension that does not change behavior/risk/contract coverage cannot inflate the coverage conclusion.

Typical dimensions include role/permission, completeness, numeric precision/size, lifecycle state, locale/timezone, evidence quality, dependency state, concurrency/order, AI ambiguity/injection, and historical regression.

Do not default to the full Cartesian product. Prioritize release blockers, contract boundaries, known fragile paths, high-impact risks, pairwise/property-based combinations, and Critical Journeys.

## 7. Golden and oracle authority

A Golden case SHOULD include:

```text
id
intent/scenario
input
expected decision/behavior
required invariants
forbidden behavior
allowed variation
rationale
provenance
review status / authority
```

Golden selection is risk-driven; there is no cross-project minimum count.

Expected behavior MUST trace to at least one authority such as deterministic rule/contract, approved real case, independent reviewer/domain expert, or accepted evaluator/rubric. LLM-only expected output is not automatically approved Golden truth.

For AI/LLM outputs, prefer structured schema, decisions, required facts, forbidden claims, invariants, evidence correctness, and rubric results over exact natural-language string matching unless exact text itself is the contract.

## 8. LLM generation protocol

An LLM SHOULD:

- read frozen sources;
- identify risk dimensions and gaps;
- propose a Scenario Matrix;
- generate semantic/natural-language/multilingual inputs;
- propose properties/invariants;
- analyze coverage gaps after deterministic validation.

An LLM SHOULD NOT:

- invent a real-world distribution without evidence;
- be the sole Golden oracle;
- replace deterministic bulk/property/fuzz generation when code is more appropriate;
- generate, judge, and approve the same formal evidence alone.

When LLM generation materially affects a formal pack, record provider/model class, prompt/instruction revision, relevant generation parameters, and the later deterministic/independent validation path.

Reusable prompt: `prompts/TEST_DATA_GENERATION.md`.

## 9. Reproducibility

Randomized generators SHOULD record:

```text
generator name + revision
seed
dependency/runtime identity
locale/timezone/clock controls
frozen output hash when the pack is release evidence
```

Seed alone is insufficient because dependency or algorithm changes may alter output.

Property/fuzz tests require explicit properties/invariants. A discovered failure SHOULD evolve as:

```text
Generated Failure
→ Minimal Reproduction
→ Regression Case
→ Required Test
```

## 10. Test Data Pack

Recommended shape:

```text
pack/
├── manifest.json|yaml
├── schema/contract/rule refs
├── scenario_matrix.*
├── cases/
│   ├── curated.*
│   ├── generated.*
│   └── schema_invalid.*
├── generators/
├── coverage.*
└── VALIDATION_REPORT.md
```

A pack manifest SHOULD include pack identity/version, purpose/scope, privacy class, schema/rule refs, provenance, taxonomy, required dimensions+rationale, generator identity/seed, file mapping, and coverage/validation references.

Template: `templates/test-data-pack.md`.

## 11. Coverage and anti-gaming

Coverage SHOULD be traceable from rule/risk → case IDs.

Review applicable dimensions such as Scenario/Risk, Contract/Schema, Boundary, Domain Rule, Incomplete/Uncertain, Failure Injection, Critical Journey, Regression, and AI adversarial/semantic coverage.

Duplicate/near-duplicate records MUST NOT increase risk coverage by themselves. Large synthetic volume cannot replace Golden/Regression authority.

## 12. Pack Validation Gate

Before a pack becomes required Validation evidence, check at least:

1. integrity/parsability;
2. intended-valid data satisfies schema/type;
3. intended-invalid cases violate the targeted constraint;
4. expected results align with rule/contract/oracle authority;
5. provenance resolves;
6. Golden/Regression authority is acceptable;
7. required dimensions are covered or exceptions are recorded;
8. required risk matrix has no unexplained gap;
9. duplicates do not inflate coverage;
10. generators replay or frozen hashes match;
11. privacy/secret policy passes;
12. Hidden expected mappings are not leaked.

Gate state uses only:

```text
PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE
```

A Test Data / Scenario Gate is aggregated into Task/Release decisions only when its authority source makes it required. A pack PASS is evidence for that pack/profile; it is not a blanket project PASS.

Checklist: `checklists/test-data-review.md`.

## 13. Hidden Validation integration

Hidden Validation pack design may happen before Candidate Freeze. Hidden Validation **execution** still follows `VALIDATION_STANDARD.md` and normally occurs only on `CANDIDATE_FROZEN_SHA`.

Public harness/schema/taxonomy may live in the repository while hidden input/expected mappings remain in the independent validation store/process.

Hidden data must still satisfy provenance, privacy, reproducibility, and oracle/review authority.

## 14. CI Evidence integration

When a test-data generator/validator runs in CI and publishes evidence externally, use `CI_EVIDENCE_STANDARD.md`.

The immutable run must identify the exact tested SHA/profile. `completion.json` proves publication completion, not Validation PASS. `latest.json` remains discovery-only.

Large generated packs should be treated as artifacts when appropriate rather than causing unbounded Git repository growth.

## 15. Feedback loop

After generating/validating a pack, review whether:

- declared dimensions truly affect rule/risk;
- taxonomy is correct;
- Goldens miss critical semantic risks;
- only a seed was recorded without generator/dependency identity;
- duplicate synthetic data inflates coverage;
- expected behavior lacks independent authority;
- provenance/privacy is weak;
- project contracts are ambiguous, conflicting, or untestable;
- a risk class is actually `NOT_APPLICABLE` rather than needing fabricated examples.

Cross-project findings should update this standard. Domain-specific findings should update the project contract/rules; they must not silently become new domain truth inside the test pack.

## 16. Prohibited practices

- LLM hallucination used as Golden truth.
- Record volume presented as sufficient coverage without risk mapping.
- Real secrets or unapproved PII/customer data in fixtures.
- One LLM acting as generator + oracle + sole approver.
- Non-reproducible randomized failures without replay/minimal case.
- Default copying of production dumps.
- Hidden expected mappings exposed to implementation agents.
- Schema-only validation when domain invariants matter.
- Deleting Golden/Regression/invariants merely to make implementation pass.
- Fabricating non-applicable scenario classes to satisfy a checklist.
