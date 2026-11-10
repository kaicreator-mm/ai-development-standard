# ADS #1366 — Exact-source consumer-chain audit (R12)

**Subject:** prospective PR #1365 source HEAD `dac263fa4c0ab155406d2f2117459b34322cc988`; experiment evidence HEAD `1346ba0b82b8fa5442770fe83970d5ea5e4d5c2f`. Program index: [#1366](https://github.com/kaicreator-mm/ai-development-standard/issues/1366).

## Delivery-First reassessment

R11 strictly qualified **61/61 Python and 35/35 SMT/TLC** at the previously fixed pair of exact SHAs; the newer evidence-only commits have not altered pinned runner/model inputs. Do not repeat integration or add gratuitous test models. The highest-value remaining question is **where the canonical dispatch constraints are actually consumed by a real authorized producer**.

## What the observed source actually supports

- PR #1365 base `fbf1a7d49596c549e955ef36949f4110a0da2d33` has **five** `execution_profile` values, whereas candidate `dac263fa4c0ab155406d2f2117459b34322cc988` has **seven**: the additive prospective profiles are `WEB_BUILDER` and `LOCAL_VALIDATION`. `schemas/dispatch.schema.json` candidate blob `5d9233b6b881d9d92f66fc6cd5307a05a0fdbe2f` couples all seven to the intended builder/validator/reviewer role (7/7 checked). **Do not retroactively apply candidate rules to frozen historic subjects.**
- `scripts/v34_rules.py` blob `0829be09f46dde75710bc54607a14edd7a2c4cea` is a **pure helper**: five profile→environment projections, plus two environment-orthogonal validator profiles; `derive_claim_key` uses repository/task/role/compatibility group, not profile/environment. It labels `active_dispatches` as **NON_AUTHORITATIVE**. None of these functions is a native producer Claim authorization grant.
- `scripts/test_protocol_schemas.py` blob `96edf2413e35a90d8049e529c11e832637dbaabd` already includes four relevant positive/negative tests for invalid profiles, role mismatch, canonical v4.19 positives and environment contradiction; the test comments explicitly say a real producer must separately bind pinned schema revision, serialized admission and immutable history. The source test definitions are **present**; they were **not executed in this current audit**.
- `scripts/test_v411_t06_claim_admission.py` blob `4c36998f9e86a8a7d6e05486d9740fb0910cea69` identifies its adapter as a **Test oracle**. The stored claim/CAS model is bounded mock evidence, **not** an observed GitHub transaction.
- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` blob `935a905d593d7aec027cb54b5b137250ca14a4c1` §“Dispatch pre-publication schema admission” expressly requires exact **effective project-pinned ADS revision**, full enriched payload validation, previous/current Claim and serialization semantics, and checking the same object again at publication. Bad schema/pin/drift cannot yield accepted canonical mutation; historical invalid records are append-only. These are **distinct from schema syntax PASS**.

### Cross-project applicability boundary

Examined `kaicreator-mm/tally` main HEAD `e988321439f65b55936a691c02250b6d62a29409`: `internal/controlplane/dispatch.go` blob `3c9cc4f757dcaaba602900b458ce8d79720e3757` has a real `Service.Dispatch` invoking its own Task execution; `internal/taskexecution/contracts.go` blob `0c4d02fee5e4bae3e5374a1f565b189983aeb638` describes a `TaskExecutionRequest` contract, not the candidate ADS `schemas/dispatch.schema.json` tuple. **No verified exact v4.19 adoption pin / adapter lineage was established.** The name “Dispatch” or this foreign service is not proof of canonical ADS producer conformance, and lack of a field in one file is not proof that no adapter exists elsewhere. No Tally source is modified.

## Disposition and most valuable next experiment

- `PROFILE_TO_ROLE_SCHEMA=PASS(7/7)`, `PROFILE_TO_ENVIRONMENT_HELPER=SOURCE_CONSISTENT`.
- `TEST_FIXTURES=SOURCE_PRESENT_NOT_EXECUTED_IN_THIS_AUDIT`.
- `CANONICAL_REAL_PRODUCER_PREPUBLISH_AT_EXACT_ADS_PIN=NOT_PROVEN`.
- `REAL_GITHUB_ACCEPTED_CLAIM_CAS_AND_PUBLICATION=NOT_PROVEN`.
- `ADS_SPEC_SOURCE_DEFECT=NOT_ESTABLISHED`.

Before adding a solver property, identify **one consumer with a verified prospective v4.19 project pin** and inspect its end-to-end `enrich → validate effective schema SHA → check Task/Claim/authority → serialize publication → readback` chain. If no eligible consumer exists, record `UNKNOWN` rather than fabricating a mock. Keep #1366 as one main Issue and re-use R11 at its historical exact SHA; no new Gate, merge, Freeze, Release or local Agent dispatch.

Machine exact Git source and structured cross-check: `CANONICAL_DISPATCH_CONSUMER_READBACK.json`. Four deliberately broken consistency-matrix mutations were rejected in this Web source-readback audit. This is **not** a fresh Python/SMT run or semantic-equivalence theorem.
