# Test Data Review Checklist

Use this checklist before a simulation/test-data pack becomes required validation evidence.

## Scope / Sources

- [ ] Pack purpose and target tests are explicit.
- [ ] Contract/schema/domain-rule references are identified.
- [ ] Real/public/external sources have provenance and usage restrictions recorded.
- [ ] LLM-derived/synthetic content is labeled as such.
- [ ] No real secret/token/private key is present.
- [ ] PII/customer/production-derived data has an explicit approved handling basis or is absent.

## Scenario Model

- [ ] Scenario dimensions map to behavior, contract or risk.
- [ ] Normal path is covered.
- [ ] Relevant numeric/string/collection/time/state boundaries are covered.
- [ ] Schema-invalid cases are represented separately when relevant.
- [ ] Domain-invalid cases are represented separately when relevant.
- [ ] Failure injection covers important dependency/runtime failures.
- [ ] AI/LLM systems include ambiguity, insufficient/conflicting evidence and adversarial cases where relevant.
- [ ] Critical Journeys are represented where the pack is used for release validation.
- [ ] Historical P0/P1 regressions are represented or explicitly not applicable.
- [ ] Excluded combinations have a reason; full Cartesian explosion is not used without need.

## Golden / Regression

- [ ] Golden expected behavior is tied to rules/evidence.
- [ ] Required invariants and forbidden behavior are explicit.
- [ ] Allowed variation is documented.
- [ ] Natural-language output is not exact-string matched unless contractually required.
- [ ] Golden cases are independently approved; LLM-only self-approval is not used.
- [ ] Regression cases have a bug/incident/reproduction source where available.

## Generator / Reproducibility

- [ ] Generator name/version is recorded.
- [ ] Seed is recorded when randomness is used.
- [ ] Dependency/runtime/locale/timezone/clock influences are controlled or recorded.
- [ ] Frozen pack hash is recorded when useful.
- [ ] A failure can be replayed from case id, seed or minimal reproduction.

## Validation

- [ ] Pack files parse successfully.
- [ ] Intended-valid inputs pass schema/type validation.
- [ ] Intended-invalid inputs actually violate the targeted constraint.
- [ ] Expected behavior matches rules/contract/oracle.
- [ ] Provenance references resolve.
- [ ] Required scenario/risk coverage has no unexplained gap.
- [ ] Duplicate/near-duplicate records do not inflate coverage claims.
- [ ] Privacy/secret policy has been checked.
- [ ] Hidden expected answers are separated from implementation-side assets.
- [ ] Validation status uses PASS / FAIL / NOT_RUN / NOT_APPLICABLE / BLOCKED.

## Feedback Loop

- [ ] The pack-generation exercise recorded weaknesses discovered in rules or standards.
- [ ] Inert dimensions were removed or justified.
- [ ] Ambiguous expected behavior was escalated instead of guessed.
- [ ] New reusable rules were fed back to the project or global standard.
