# Golden Template and Conformance Example Standard

## 1. Purpose

Normative standards must be executable and teachable, not only descriptive. This standard requires maintained positive examples and explicit non-conformant examples for ai-development-standard.

## 2. Mandatory coverage

Every active normative standard in `standard-manifest.json` MUST satisfy one of these forms:

1. **Artifact/protocol standard** — reference at least one maintained Golden Template or Golden Example that demonstrates the compliant shape; or
2. **Conceptual/policy standard** — contain or reference at least one Golden Conformance Example that demonstrates compliant application.

Every normative standard MUST also contain or reference:

- a Forbidden / Non-conformant example;
- rationale explaining why the forbidden form violates authority, correctness, evidence, recoverability, or maintainability;
- ownership/authority-boundary explanation when the standard could otherwise be mistaken for another authority.

## 3. Golden examples are not authority copies

Golden examples demonstrate shape and semantics. They MUST NOT become a mutable copy of project/task truth.

A Golden Task Issue may contain placeholders such as `<baseline-sha>` or `<acceptance>`. It MUST NOT embed the current facts of an unrelated live project merely to stay realistic.

Authority remains with the actual project Issue, frozen artifact, schema, exact-SHA evidence, or release record.

## 4. Central index

`templates/GOLDEN_INDEX.md` is the canonical mapping from normative execution surfaces to:

```text
owning standard
→ Golden Template / Example
→ Forbidden / Anti-pattern reference
→ verifier/regression coverage
```

The index MUST explain whether the referenced file is:

- a copyable template;
- a worked conformance example;
- a checklist/reference surface;
- a negative example library.

## 5. Minimum v3.4 critical surfaces

v3.4 MUST maintain Golden coverage for at least:

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

When a standard introduces a new durable artifact, workflow state, handoff, gate, event, or authority boundary, the same change MUST update:

1. its Golden Example/Template;
2. its Forbidden/non-conformant example or shared anti-pattern reference;
3. the central Golden Index;
4. focused verifier/regression coverage when machine checking is practical.

A normative change is incomplete if it changes required behavior but leaves its Golden example teaching the old behavior.

## 8. Golden conformance example

A new `Validation Request` contract is introduced. The PR adds:

```text
standards/...                     normative semantics
templates/validation-request-issue.md  compliant shape
templates/golden/ANTI_PATTERNS.md      forbidden stale-label example
templates/GOLDEN_INDEX.md              ownership/index row
scripts/...                             regression
```

## 9. Forbidden examples and rationale

Forbidden: adding a new standard that defines a required artifact but provides no positive example.

Reason: Agents must infer shape independently, creating inconsistent project-local dialects.

Forbidden: copying a live project's current SHA/branch/task status into a Golden Template.

Reason: examples become stale parallel authority rather than reusable shape guidance.

Forbidden: a Golden example that contradicts its owning normative standard.

Reason: the repository teaches two incompatible contracts; the normative standard wins, but the example defect must block qualification until repaired.
