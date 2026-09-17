# Test Data Engineering Reference Notes

## Purpose

This reference preserves the engineering conclusions validated during the legacy Test Data & Scenario pilot (PR #4) while the normative rules are re-integrated onto the v3.x workflow model.

## Validated findings carried forward

The legacy reference pack contained curated, deterministic generated, intentionally schema-invalid, Golden, Boundary, Domain-invalid, Incomplete/Uncertain, Adversarial, and Regression cases. The exact historical counts are evidence about that pilot only; they are not universal minimums.

The pilot produced several reusable findings:

1. **Required dimensions must affect behavior or risk.** Inert dimensions cannot be used to inflate coverage.
2. **Schema-invalid, domain-invalid, incomplete/uncertain, and runtime failure injection are different classes.** They require different expected behavior and different validators.
3. **Non-applicable risk classes should be explicit N/A.** Fabricating irrelevant scenarios reduces signal.
4. **Golden selection is risk-driven, not count-driven.** There is no useful cross-project minimum Golden count.
5. **Seed alone is not reproducibility.** Generator/dependency/runtime identity or frozen artifact hashes are also needed when they affect bytes/behavior.
6. **Duplicate synthetic records do not increase risk coverage.** Coverage must map back to rules, contracts, boundaries, incidents, or other explicit risk dimensions.
7. **An LLM cannot be generator + expected-answer oracle + sole approver.** Formal expected behavior needs an independent authority path.
8. **Hidden data needs the same provenance/privacy/reproducibility discipline as visible data.** Hidden means unavailable to the implementation context, not exempt from engineering controls.

## v3.x integration constraints

The legacy v1.x branch is not itself a valid v3.x integration baseline. Therefore its useful content is migrated conceptually rather than merged wholesale.

In v3.x:

- a Test Data / Scenario Gate is required only through the normal Gate Authority chain;
- formal pack evidence binds to exact SHA / validation profile where applicable;
- Hidden Validation execution still follows Candidate Freeze rules;
- CI publication follows `CI_EVIDENCE_STANDARD.md` when evidence is externalized;
- a pack PASS cannot substitute for unexecuted Critical Journey, platform, packaging, or other required gates;
- the standard five-state Gate model remains `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`.

## Legacy source

Historical source: PR #4, branch `docs/test-data-scenario-standard`.

That PR should not be merged directly after v3.x because it also modifies old VERSION/README/AGENTS/Validation semantics. It is retained only as historical source evidence until the v3.2 migration is integrated, then should be closed as superseded.
