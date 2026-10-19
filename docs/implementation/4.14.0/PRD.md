# ADS v4.14.0 — Product Requirements (R0)

Status: **PRODUCT_CANDIDATE — NOT INDEPENDENTLY REVIEWED OR FROZEN**
Parent: [#1187](https://github.com/kaicreator-mm/ai-development-standard/issues/1187).
Product evidence: `docs/implementation/4.14.0/L1_PRODUCT_EVIDENCE.md`.
Version branch: `version/v4.14`; current main baseline `b1126df404b09b4d3ab9deedaaf26d9b9d5e1a5e`.

## Problem
ADS v2 unified the visible YAML carrier but does not place shape rules fully in JSON Schema, creating Python-only domain knowledge and partially redundant format/version fields. It was merged into main without sufficiently proving a real GitHub Issue consumer journey.

## Requirements
- **FR01 / P0: True declarative schema.** A single published Draft 2020-12 root uses a discriminated `oneOf` over `work_item, intent, event, report`, with `$defs` for ten Issue profiles and each of six native Issue mutation requests, and local/pinned `$ref` to canonical Task Contract and Agent Event v2 payload. Strict missing/unknown/extra-field rejects. No Python branch copies type/field definitions.
- **FR02 / P0: Data vs authority.** Safe YAML parse + real JSON Schema format checker returns only `SHAPE_VALID_ONLY`. Admission of native status/Claim/Dependency/Review/Validation/Release depends on fresh GitHub fact readback, expected source and existing workflow predicates. GitHub transport account is not logical actor identity. Never render `PASS` from shape alone.
- **FR03 / P0: Minimal latest-only envelope.** One first-line marker `<!-- ads:github -->` (no redundant version), a single YAML map with `schema: ads/github/v3`, `kind`, `data`; normal Markdown follows. Each Event and Report publishes its own direct comment; only six native Issue mutation operations use an Intent. Keep no v1/v2 parser path, no double `publication_key`.
- **FR04 / P0: Real bounded dogfood.** One small real GitHub smoke project test work item, machine-valid body and actual GitHub operations with Issue IDs/URLs: create → readback → contract amendment → native metadata and dependency (only if available) → event and report publication → close/readback/reopen (or honest scoped limitation). Negative: invalid schema, stale request, no fabricated authorization or stored report object.
- **FR05 / P0: Version governance.** Source/Task decomposition in `version/v4.14`; concern PRs integrate into version branch only. Product review/freeze, L2 review/freeze, executable DAG, required independent protocol Review, version regression/closure and release eligibility must have explicit evidence before **one final main integration**.
- **FR06 / P1: Current writer consistency.** Maintained Issue/comment templates and reference examples use v3, not old header. Source maps and manifest identify one canonical schema. No redundant YAML writable GitHub state.

## Non-goals
Backward compatibility, migration of thousands of Issues/comments, databases, new GitHub controller/runtime, new Agent identity credentials, new Review/Release stage, real OSS credentials or cross-project Tally/task-meta implementation.

## Acceptance and test matrix
- A third-party JSON Schema Draft2020-12 implementation validates every positive case and rejects each missing/extra-field/type/cross-kind mutation test.
- A safe YAML loader rejects duplicate keys/aliases/tags/unsupported scalar coercions without data loss.
- An independent shape validator and actual GitHub state checker are visibly separate. Source-only validator must not call GitHub write API.
- At least one live Issue/Comment trace with immutable repo-ref and actual GitHub readback, not a fixture-only PASS.
- Exact version SHA+CI+independent protocol review and documented decision on non-material historical gates. No main merge until version-level closure.

## Open Product decisions
None on envelope and ownership after user latest-only instruction; **actual** GitHub permission/capability and object-store availability may still block a full E2E. Freeze eligibility depends on review.
