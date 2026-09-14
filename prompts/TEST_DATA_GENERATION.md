# Test Data Generation Prompt Baseline

Use this prompt when an LLM is asked to design or generate simulation/test data for a project.

## Role

You are designing **test evidence**, not decorative fake data. Your output must be derived from the project's frozen contracts, rules, risks and evidence.

## Required Inputs

Read, when available:

1. PRD / frozen scope;
2. API/schema/file/data contracts;
3. domain rules / Decision Models / invariants;
4. existing tests and fixtures;
5. real bug / incident / support examples;
6. Critical Journeys;
7. external standards or public datasets approved for the project;
8. privacy/security constraints;
9. Hidden Validation policy.

If a necessary fact is missing, mark it `UNKNOWN` rather than inventing a business rule.

## Workflow

### Step 1 — Build Source Catalog

For every source record:

- identity/path/URL;
- source type;
- authority/trust level;
- version or frozen date;
- license/usage restriction if external;
- privacy classification;
- what fields/rules/distributions it supports.

Do not present LLM-created content as a real-world source.

### Step 2 — Extract Contracts and Rules

Produce a compact list of:

- required fields/types/enums;
- business/domain constraints;
- state transitions;
- permissions;
- failure behavior;
- invariants;
- critical decisions;
- AI-specific evidence/trust rules.

Each expected result later generated must map back to one or more of these rules or an approved Golden source.

### Step 3 — Design Scenario Dimensions

Create only dimensions that matter to behavior or risk. For each dimension include:

- name;
- candidate values/ranges;
- why the dimension matters;
- rule/risk it exercises;
- whether every value must be covered.

Typical dimensions include completeness, numeric boundary, role/permission, lifecycle state, dependency state, evidence quality, locale/timezone, concurrency, AI ambiguity and adversarial text.

Do not create dimensions merely to inflate coverage counts.

### Step 4 — Create Scenario Matrix Before Records

Design a risk-based matrix containing at least the applicable classes:

- normal;
- boundary;
- schema-invalid;
- domain-invalid;
- failure injection;
- adversarial;
- regression;
- Critical Journey;
- scale/load.

Do not blindly generate the full Cartesian product. Prefer high-risk combinations, pairwise combinations, historical failures, contract boundaries and property-based generation.

### Step 5 — Select Golden Cases

For each Golden Case define:

- id;
- intent/scenario;
- input;
- expected decision/structured result;
- required invariants;
- forbidden behavior;
- allowed output variation;
- rationale;
- provenance;
- review state.

For natural-language/LLM outputs, avoid exact-string goldens unless exact text is itself the contract.

You may propose a Golden Case, but you may not mark an LLM-only expectation as approved without independent rule/evidence/reviewer support.

### Step 6 — Build Generators

Use the LLM primarily for semantic scenario design and natural-language content. Use deterministic code for bulk generation when practical.

A generator must record:

- name/version;
- seed;
- runtime/dependency versions that affect output;
- locale/timezone/clock assumptions;
- generated file hashes when the pack is frozen.

### Step 7 — Generate Data

Generate small curated high-value examples first, then supplemental deterministic/property-based data.

Keep schema-invalid fixtures separate from schema-valid/domain-invalid fixtures so validators can distinguish an intentionally invalid case from a broken pack.

### Step 8 — Validate

Validate at least:

- file/pack integrity;
- intended-valid schema compliance;
- intended-invalid constraint violation;
- rule/oracle consistency;
- invariants;
- provenance references;
- Golden/Regression review state;
- dimension/risk coverage;
- duplicate/near-duplicate inflation;
- deterministic reproducibility/hash;
- privacy/secret scanning policy;
- Hidden Validation separation.

### Step 9 — Produce Feedback

Do not stop at PASS. Review whether the generation exercise exposed weaknesses in the standard, source material or test model.

Report:

- inert dimensions that do not affect behavior;
- missing risk classes;
- rules that are ambiguous or untestable;
- Golden Cases with weak evidence;
- invalid/failure categories that were conflated;
- non-reproducible generation;
- coverage metrics that can be gamed;
- missing privacy/provenance metadata.

Propose concrete changes to the standard or project rules.

## Required Output

Prefer a version-controlled pack containing:

```text
manifest.json|yaml
schema / contract refs
scenario_matrix.*
cases/
golden/
regression/
generators/
coverage.*
validation-report.md
```

Use the repository's own format conventions when they already exist.

## Hard Rules

- Never invent a real-world distribution and label it realistic without evidence.
- Never use record count as the main coverage claim.
- Never let one LLM be the sole source of input, expected answer and approval.
- Never expose Hidden Validation expected answers to implementation agents.
- Never include real credentials or unapproved personal/customer data.
- Never convert an unexecuted check to PASS.
