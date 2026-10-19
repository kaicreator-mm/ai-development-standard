# ADS v4.14 — L2 Architecture Evidence R0

Status: **ARCHITECTURE_CANDIDATE / NOT YET FROZEN**. Product: `docs/implementation/4.14.0/PRD.md` (candidate, review pending); source pin `main@b1126df404b09b4d3ab9deedaaf26d9b9d5e1a5e`.

## A1. Source and authority
- Existing `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` is **carrier semantics** owner; existing `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` owns Issue Type/State/DAG/Claim; Review/Validation/Release standards own evidence. This version does not duplicate them.
- New `schemas/github/v4.14/structured-interaction.schema.json` is the **single** latest `ads/github/v3` envelope and structural family. Reuse existing Task Contract and Agent Event v2 through exact-schema `$ref`, registered locally by a Draft2020-12 validator. Remove active v2 sibling schemas only after successor checks are green.
- Parser `scripts/verify_github_structured_interaction.py` handles only tagged Markdown and safe YAML syntax, delegates all structural dispatch and conditional validation to real `jsonschema.Draft202012Validator`; `test_protocol_schemas.py` remains frozen subset test for existing older schema families and scans only root file glob. Do not implement a second JSON Schema engine.
- Dedicated workflow installs pinned `jsonschema` and `PyYAML`. Runtime checks must not make network requests for schema resolution: exact known IDs map to repository-local bytes. All other remote refs fail closed.

## A2. Bounded envelope
```markdown
<!-- ads:github -->
```yaml
schema: ads/github/v3
kind: intent
data:
  id: intent:example:1
  operation: ISSUE_CLOSE
  target:
    repository: example-org/project
    issue: "#10"
  actor:
    role: builder
    operator_kind: codex
    operator_id: codex:worker-01
  expected_ref: github:example-org/project#10@current
  change:
    reason: "All authorized work closed"
    evidence_refs:
      - "github:pr#15@exact-sha"
```
```
Envelope marker is a *discovery delimiter*, schema value alone is wire version. Exactly one YAML block is normative. Plain markdown is non-operational.

## A3. Source vs dynamic facts
Parser -> SafeLoader (no duplicate keys/aliases/tags/unsupported coercions) -> root schema validator + registered references -> `SHAPE_VALID_ONLY`.
A separate caller operation coordinator performs actual GitHub API readback, Claim/State/Dependency/CI/Review/Release predicates, GitHub write and readback; only **real** GitHub object evidence can project accepted state. No automatic admission in parser or Schema; expected_ref is checked against actual current source (not accepted merely because it is a nonempty string).

## A4. Schema decisions
- `oneOf` requires exactly one matching kind; nested `oneOf` requires exactly one Work Item profile or native intent operation.
- `$defs` contains required field vocab; `unevaluatedProperties: false`/strict nested `additionalProperties: false` except existing canonical Task/Event payload owners. Use explicit `x_*` extensions only where documented, not undifferentiated unknown fields.
- `ISSUE_CREATE`: null target Issue and expected_ref; `ISSUE_CONTRACT_UPDATE`: exact old contract ref, reason, new Work Item; `ISSUE_METADATA_CHANGE`: native field and typed old/new; `ISSUE_DEPENDENCY_CHANGE`: add/remove, exact distinct target; `ISSUE_CLOSE/REOPEN`: required reason/evidence refs. No Event/Report Intent operations.
- `report`: correction requires `corrects_ref`; durable manifest ref/hash/coverage; report key is derived at publication time rather than serialized.
- Existing Agent Event v2 data is not redefined; its canonical source/write owner remains authoritative.

## A5. Real dogfood location and safeguards
Use existing bounded `kaicreator-mm/ai-dev-pilot` repo as real GitHub smoke project only if a safe isolated Issue can be created and closed; no code or deployment mutation there. If not permitted, use an explicitly marked isolated smoke Issue in ADS and document the limitation. Do not mutate real business Issues for simulation. Publication without real object-store evidence is `NOT_RUN`; a static fixture digest is not a verified external upload.

## A6. Review and release risks
Risks: YAML loader denial-of-service or alias bypass, schema ref network fetching, strict-oneOf ambiguity, nested source binding, mismatch between machine shape and GitHub facts, overbroad historical freeze expectation. Mitigations: bounded input bytes/depth, local resolver, source-specific true E2E, negative tests, independent protocol review, version-level closure.

**L2_FREEZE_READY: NO**, until Product Freeze, schema/test review and this source's exact SHA recorded. No implicit implementation permit by this candidate.
