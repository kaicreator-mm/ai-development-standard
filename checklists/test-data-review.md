# Test Data Review Checklist

Use before a simulation/test-data pack becomes required validation evidence.

## Scope / Sources

- [ ] Pack purpose and target tests are explicit.
- [ ] Contract/schema/domain-rule references are identified.
- [ ] External/real sources have provenance, version/frozen date and usage restrictions.
- [ ] LLM-derived/synthetic content is labeled.
- [ ] No real secret/token/private key is present.
- [ ] PII/customer/production-derived data is absent or explicitly approved.

## Scenario Model

- [ ] Every required dimension maps to behavior, contract or risk.
- [ ] Normal path is covered where applicable.
- [ ] Relevant boundaries are covered.
- [ ] Schema-invalid and domain-invalid are distinguished.
- [ ] Missing/unknown/insufficient facts are modeled as incomplete/uncertain rather than runtime failure.
- [ ] Runtime failure injection covers actual dependency/I-O/DB failures where applicable.
- [ ] AI systems cover ambiguity/conflicting evidence/adversarial input where applicable.
- [ ] Critical Journeys and historical regressions are covered where required.
- [ ] Non-applicable categories are explicitly `NOT_APPLICABLE + rationale`, not fabricated.
- [ ] Full Cartesian explosion is avoided unless justified.

## Golden / Regression

- [ ] Golden expected behavior is tied to independent rule/evidence/reviewer authority.
- [ ] Required invariants and forbidden behavior are explicit.
- [ ] Allowed variation is documented.
- [ ] Natural-language output is not exact-match unless contractually required.
- [ ] LLM-only self-approval is not used.
- [ ] Regression cases have bug/incident/reproduction provenance when available.

## Generator / Reproducibility

- [ ] Generator name/revision is recorded.
- [ ] Seed is recorded when randomness is used.
- [ ] Dependency/runtime/locale/timezone/clock influences are controlled or recorded.
- [ ] Frozen pack hashes are recorded where useful.
- [ ] Failures can be replayed from case id, seed or minimal reproduction.

## Validation

- [ ] Pack files parse successfully.
- [ ] Intended-valid inputs pass target schema/type validation.
- [ ] Intended-invalid inputs violate the intended constraint.
- [ ] Expected behavior matches rule/contract/oracle.
- [ ] Provenance references resolve.
- [ ] Required risk/dimension coverage has no unexplained gap.
- [ ] Duplicate/near-duplicate records do not inflate coverage.
- [ ] Privacy/secret policy has been checked.
- [ ] Hidden expected mapping is separated from implementation assets.
- [ ] Status uses PASS / FAIL / NOT_RUN / NOT_APPLICABLE / BLOCKED.

## Feedback Loop

- [ ] Inert dimensions were removed or labeled exploratory.
- [ ] Taxonomy mistakes were corrected (schema/domain/incomplete/runtime/adversarial).
- [ ] Ambiguous expected behavior was escalated instead of guessed.
- [ ] Weak Golden authority was identified.
- [ ] New reusable findings were fed back to project rules or the global standard.
