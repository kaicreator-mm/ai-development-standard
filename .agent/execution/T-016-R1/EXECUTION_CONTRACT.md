# T-016 R1 Execution Contract

## Authority

This pack is subordinate to Frozen v4.8 Product/L2/DAG, T-016 Task Pack blob `a77cc3d9c562a438b94386752e89a89ca4520fb2`, L3 blob `03c2b47111b0922641d5f87a6519b88c8231e0e7`, and bounded repair Issue #599 derived from #593 P1.

Exact base: `version/v4.8.0@ee75ffe759461b1cec8e43676c2d6a0ddf54b7b4` / tree `452c9d184a7545adc2e4136b02ec111a1bf1cccb`.

## Repair concern

Close exactly the T-016 owner defect where arbitrary non-empty `exact_subject_ref` can be treated as exact-subject evidence and therefore allow mutable aliases to remain textually equal across content drift.

## Required semantics

- Code/artifact exact subjects use immutable `git:<owner>/<repository>@<40-lowercase-hex-commit-sha>` identity.
- Branch/symbolic refs, tags/ref aliases, repository-only tokens, short/malformed/non-hex SHAs fail closed for exact-subject applicability.
- Equality of mutable text is not evidence of current applicability.
- Stale/drifted evidence remains historical only.
- Historical evidence never grants current Availability, eligibility/routing, Review/Validation PASS, authorization, or side-effect authority.
- Preserve POSITIVE/NEGATIVE/MIXED observations, reference-only external owner facts, bounded evidence strength, provider/model provenance-only semantics, and economic non-inference.

## Write set

Only these implementation paths may change:

1. `schemas/agent-capability-evidence-v1.schema.json`
2. `references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md`
3. `scripts/test_v48_agent_capability_evidence.py`

The six `.agent/execution/T-016-R1/**` files are Controller-authored JIT guidance and must not be rewritten by the repair Builder unless Controller rebinds the pack.

## Forbidden scope

No T-007 test workaround, T-002 scheduler semantics, Interchange/Event changes, Availability owner, Review/Validation authority, global Agent score, economic policy, Product/L2/DAG/Task Pack/L3 mutation, or new machine-contract family.

## Completion

Builder completion requires exact successor HEAD/tree, effective write-set proof, focused tests and applicable CI stated truthfully. It does not authorize self-Validation, self-Review, merge, downstream T-007 admission, Version Closure, or Release Qualification.
