# Golden Template and Conformance Example Standard

## 1. Purpose

Normative standards must be executable and teachable, not only descriptive. This standard requires maintained positive examples and explicit non-conformant examples for ai-development-standard.

## 2. Mandatory coverage

Every active normative standard in `standard-manifest.json` MUST have exactly one coverage record in:

```text
templates/golden/STANDARD_COVERAGE.json
```

Each coverage record MUST identify:

```text
standard
golden_ref
forbidden_ref
rationale_ref
```

The coverage registry is the repository-level reference on behalf of every normative standard. A standard MAY additionally embed direct links/sections, but it is not required to duplicate the registry locally.

Coverage MUST satisfy one of these forms:

1. **Artifact/protocol standard** — point to at least one maintained Golden Template or Golden Example that demonstrates the compliant shape; or
2. **Conceptual/policy standard** — point to a maintained Golden Conformance Example that demonstrates compliant application.

Every normative standard MUST also have:

- a Forbidden / Non-conformant example;
- rationale explaining why the forbidden form violates authority, correctness, evidence, recoverability, or maintainability;
- ownership/authority-boundary explanation when the standard could otherwise be mistaken for another authority.

CI MUST fail when the set of standards in `STANDARD_COVERAGE.json` differs from `standard-manifest.json.sections.normative_standards`, or when a referenced positive/negative/rationale asset is missing.

## 3. Golden examples are not authority copies

Golden examples demonstrate shape and semantics. They MUST NOT become a mutable copy of project/task truth.

A Golden Task Issue may contain placeholders such as `<baseline-sha>` or `<acceptance>`. It MUST NOT embed the current facts of an unrelated live project merely to stay realistic.

Authority remains with the actual project Issue, frozen artifact, schema, exact-SHA evidence, or release record.

## 4. Central indexes

Two complementary indexes are maintained:

- `templates/golden/STANDARD_COVERAGE.json` — machine-complete one-to-one coverage for every active normative standard;
- `templates/GOLDEN_INDEX.md` — human-oriented mapping for important execution surfaces and concrete reusable templates.

`templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md` provides concise positive/forbidden/rationale examples for standards whose primary Golden form is conceptual rather than a copyable artifact template.

The human index maps:

```text
owning standard
→ Golden Template / Example
→ Forbidden / Anti-pattern reference
→ verifier/regression coverage
```

## 5. Minimum v3.4 critical surfaces

In addition to complete standard-wide coverage, v3.4 MUST maintain concrete Golden coverage for at least:

- Version Task DAG;
- Version umbrella Issue;
- implementation Task Issue;
- planning/Task-DAG amendment Issue;
- research Issue;
- research-demo Issue;
- bug/fix Issue;
- validation request/handoff;
- blocker Issue;
- Independent Review dispatch/result shape;
- pointer-only task trigger;
- structured Agent event;
- implementation PR / exact-head evidence;
- Version DAG derived state card;
- release/version closeout.

## 6. Forbidden-example requirements

Forbidden examples SHOULD be minimal and diagnostic. They MUST identify the violated invariant rather than merely showing bad prose.

Good negative example:

```text
Labels: state:ready, state:implementing
Violation: active work item has more than one canonical workflow state.
```

Weak negative example:

```text
Bad Issue: “Do it better.”
```

The weak example may be true but does not teach the protocol invariant.

## 7. Standard authoring rule

When a standard is added, removed, or changes a durable artifact, workflow state, handoff, gate, event, or authority boundary, the same change MUST update:

1. `STANDARD_COVERAGE.json`;
2. its Golden Example/Template or conformance example;
3. its Forbidden/non-conformant example and rationale;
4. `templates/GOLDEN_INDEX.md` when a reusable critical surface changes;
5. focused verifier/regression coverage when machine checking is practical.

A normative change is incomplete if it changes required behavior but leaves Golden/Forbidden guidance teaching the old behavior.

## 8. Golden conformance example

A new `Validation Request` contract is introduced. The PR adds/updates:

```text
standards/...                                      normative semantics
templates/validation-request-issue.md              compliant shape
templates/golden/STANDARD_COVERAGE.json            standard-wide mapping
templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md  positive/negative rationale
templates/golden/ANTI_PATTERNS.md                   shared diagnostic anti-pattern
templates/GOLDEN_INDEX.md                           execution-surface index
scripts/...                                         regression
```

## 9. Forbidden examples and rationale

Forbidden: adding a new standard that defines required behavior but omitting it from `STANDARD_COVERAGE.json`.

Reason: some Agents receive no canonical positive/negative guidance and begin inventing project-local dialects.

Forbidden: copying a live project's current SHA/branch/task status into a Golden Template.

Reason: examples become stale parallel authority rather than reusable shape guidance.

Forbidden: a Golden example that contradicts its owning normative standard.

Reason: the repository teaches two incompatible contracts; the normative standard wins, but the example defect must block qualification until repaired.
