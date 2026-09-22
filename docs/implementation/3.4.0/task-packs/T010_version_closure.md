# Task Pack T-010 — Version Closure

- Goal: full Version Closure per RELEASE_STANDARD: full standard verifier, schema/protocol tests, coherence review, reference project validation, Fresh Independent Review, Release Qualification, main integration, immutable v3.4 baseline.
- Write set: `*` (closure repairs only, each traceable to a closure finding).
- Forbidden: claiming READY without required gates; reusing PASS across SHA changes.
- Closure gates:
  - full standard verifier green on final exact candidate;
  - Fresh Independent Review PASS on the final exact candidate (independent context, attributable operator, REVIEW_RESULT published to GitHub);
  - Release Qualification per RELEASE_STANDARD;
  - #45 closed as absorbed by v3.4 with material criteria mapped to files/tests; #46 closed as absorbed by Validator Dispatch / version-scoped Validation Handoff profile with explicit record that no independent queue lifecycle was introduced;
  - `version/v3.4.0` → `main` integration + immutable baseline commit recorded.
- Issue disposition rule: close #45/#46 only after material acceptance criteria are implemented and verified, not merely because they are referenced.
- Agent freedom: F3_ARCHITECTURE_REQUIRED (release judgement returns to Strong Model / architecture authority).
- Dependencies: T-009.
- Validation ownership: closure.
