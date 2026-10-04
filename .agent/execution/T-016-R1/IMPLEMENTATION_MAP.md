# T-016 R1 Implementation Map

## `schemas/agent-capability-evidence-v1.schema.json`

Narrow the existing `exact_subject_ref` contract so code/artifact exact-subject evidence cannot use mutable/non-exact identifiers. Prefer repository-supported JSON Schema constructs and preserve existing closed-object/non-authority behavior.

Canonical immutable form for this repair: `git:<owner>/<repository>@<40-lowercase-hex-commit-sha>`.

Do not add current-state, routing, availability, review, validation, authorization, score, or infrastructure-owner fields.

## `references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md`

Document that exact subject identity is immutable; branch/tag/repository-only refs are locators/aliases, not behavioral-currentness proof. Explain stale/drifted evidence as historical-only and retain all existing owner/economic boundaries.

## `scripts/test_v48_agent_capability_evidence.py`

Extend focused executable coverage with at least:

- canonical 40-lowercase-hex exact Git subject positive;
- `@main` / named branch negative;
- tag or symbolic ref negative;
- repository-only token negative;
- short SHA negative;
- malformed/non-hex/uppercase-as-noncanonical negative where applicable;
- same textual mutable alias across simulated subject drift does not establish applicability;
- stale immutable SHA remains historical only;
- all predecessor false-authority/owner-fact/global-score/economic negatives remain green.

No other path is an implementation target.
