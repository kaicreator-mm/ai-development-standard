# ADS v4.14.0 — L1 Product Evidence

STATUS: `CANDIDATE / independent-review-pending`
Intake: [#1187](https://github.com/kaicreator-mm/ai-development-standard/issues/1187). Origin: user explicitly requested targeted optimization of (1) declarative JSON Schema, (2) data/operation truth separation, (3) optimized envelope and (4) real simulated GitHub project; plus **one version branch** and withheld main merge until closure.
Pinned predecessor `main@b1126df404b09b4d3ab9deedaaf26d9b9d5e1a5e`; target `version/v4.14`.

## Actual evidence
- Existing `schemas/github-document-v2.schema.json` checks `kind` enum but `data` only `type: object`; malformed work-item/intent/report can pass it. Reproduced by static inspection of source blob.
- `scripts/verify_github_structured_interaction.py` implements kind-specific required fields, 10 Work Item profiles, six Issue operation shapes and report corrections in Python instead of portable full Draft 2020-12 JSON Schema.
- Existing dependency-free schema subset verifier `scripts/test_protocol_schemas.py` does not implement `$defs/$ref/oneOf/unevaluatedProperties` and cannot certify a full JSON Schema 2020-12 contract.
- A GitHub Operation Intent is not a GitHub mutation: schema/identity and currentness/Claim state are different authorities; current v2 source checker says `SHAPE_VALID_ONLY` but does not actually exercise live native GitHub writes.
- ADS v4.13 direct-to-main change at #1185 created a cross-project protocol without the requested Product/L2/Task DAG/release decision.

## Rejected shortcuts
- No new DIY reimplementation of full JSON Schema.
- No schema-per-GitHub REST endpoint; no double Event/Report comment and intent envelopes.
- No generic `{data:{}}` accepted as complete contract.
- No human/GitHub-login proof for logical Agent identity.
- No acceptance of simulated HTTP results as actual GitHub create/mutate/readback.
- No historical v1/v2 parser/migration as requirement.

## Product questions requiring falsifiable answer
1. Is one `<!-- ads:github -->` marker + YAML `schema: ads/github/v3` + `kind` + `data` minimal, with *only* schema value authoritative for version? Yes proposed: removing duplicate version from marker preserves one readable detection token.
2. Can a normal third-party Draft2020-12 validator validate **each kind and each operation** directly from a self-contained root with local pinned Task/Event refs? Acceptance: invalid mixed kind/payload and all six operation-specific missing fields fail.
3. Are state transitions and GitHub Claim authorization outside JSON Schema? Yes: real GitHub readback/conditional writer uses current facts and its own existing normative owner, not the data-only parser.
4. Will a real task-like test Issue demonstrate create/read/update, Event/Report comment and terminal lifecycle? Must report real URLs and results, including explicitly NOT_RUN external provider boundaries.

## Product risk/ROI
This is a **breaking public interface** with high interface risk, low runtime complexity, little external infrastructure. Select `review:required` for schema/authority change and focused negative tests. Do not invent a full Host/platform build matrix. Product Freeze and L2 Freeze remain separately provable preconditions, not automatic from passing CI.
