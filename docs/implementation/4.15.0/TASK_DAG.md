# ADS v4.15.0 — Source-frozen Architecture → Executable Task DAG (R0 planning candidate)

**State:** `TASK_DAG_CANDIDATE / NOT_FROZEN / NATIVE_DEPENDENCIES_NOT_YET_MATERIALIZED`. This file is a **planning checkpoint**, never live Task/Gate/Claim status authority.
**Frozen upstream exact subjects:**
- [Product Freeze #1207@6284631551](https://github.com/kaicreator-mm/ai-development-standard/issues/1207#issuecomment-6284631551): PRD `fbeacd479f5a9a0d3dc1a3f853abe623cc211031`, L1 `34a8833056e8a3e31ba2238777fde21e816ce6ac`.
- [L2 Freeze #1207@6285932823](https://github.com/kaicreator-mm/ai-development-standard/issues/1207#issuecomment-6285932823): Architecture `cf4721a90122a9c9bad486209d478f2adf81e0dc`, Evidence `4c280d690f087efe39a0d3d6b07860d4806b18b4`, reviewed source `1a472af3d5742c1948f9530f0cdbd1c24a03052a`.
- Baseline ADS v4.14.0 main `584512e8566408bed479192753c12a036309d277`, version integration `version/v4.15`; no mid-version main merges.
- [R1 independent L2 review #1213@6285181392](https://github.com/kaicreator-mm/ai-development-standard/issues/1213#issuecomment-6285181392): `L2_FREEZE_READY=YES`, P0=P1=P2=0.

## Scope, DAG shape, genuine dependencies

```text
S01 Capture/publisher projection crosswalk ──→ S02 New v4 report Schema/validator ──→ S03 Tally GitHub consumer/feedback contract ─┐
                                             │                                                         │
S04 Qualified SHA/manual adoption clarification ───────────────────────────────────────────────────────┤
task-meta actual producer + Tally actual TS reader (separate repo issue work) ────────────────────────┤
                                                                                                         ▼
                                                S05 Real 2-way GitHub E2E conformance + negatives
                                                                                                         │
                                                                                                         ▼
                                                S06 Version closure/RQ/only-final-main integration
```

The preceding **external** task-meta/Tally producers/readers are **actual upstream prerequisites to S05** but live in their own repositories and must not be falsely represented by intra-ADS GitHub dependency edges. Mark them explicitly `EXTERNAL_BLOCKER` until code and real test receipts exist.

| ID | Proposed executable concern | Prerequisites | Source allowed / required evidence | Review policy / risk |
| --- | --- | --- | --- | --- |
| **S01** | ADS §10 existing passive telemetry sole owner → task-meta GitHub-safe source/coverage/actor/Attempt/metric/verifier projection crosswalk (#1208) | Frozen Product/L2 | `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` §10 minimal normative delta only if proven; supporting `references/AGENT_EXECUTION_METADATA_COLLECTION_REFERENCE.md` and bounded fixtures | recommended; medium; source/tables/negative cases, no collector code |
| **S02** | **Report-only** `ads/github/v4` strict Draft2020-12 schema, safe validator/per-kind dispatch, JCS data digest and v3/v4 fixtures (existing #1205) | S01 for exact consumer fields/coverage | `schemas/github/v4.15/report.schema.json`, original `scripts/verify_github_structured_interaction.py` safe parser extension, focused schema tests, §16.4 / reference normative contract. Preserve v3 root bytes | **required**; high wire/compatibility; negative mixed pin/unsafe YAML |
| **S03** | Tally GitHub-only read/reconciliation/manifest-free feedback / permission-grant evidence normative contract (#1209) | S02 accepted schema/field authority | `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` & `references/GITHUB_STRUCTURED_INTERACTION_REFERENCE.md`, bounded conformance fixtures; no Tally TS code in ADS | **required**; high authority/privacy; Tally v2 Reader feedback integration contract |
| **S04** | Qualified exact SHA without Tag manual adoption vs legacy advisory selector, test-only candidate pin / post-RQ effective adoption | Frozen Product/L2; **independent of S01–S03 source** | `standards/PROJECT_ADOPTION.md` narrow clause and focused docs/fixture. Do not modify v4.12 selector unless separately evidenced + authorized. | recommended; medium semantic compatibility; negative float `main`, still `NO_SAFE_RECOMMENDATION` for auto selector |
| **S05** | **Real** task-meta→GitHub→Tally→GitHub E2E with immutable receipts and source/external evidence, strict verifier & cost UNKNOWN, denial, retry/correction/edit/429 (existing #1210) | S02+S03+S04; **actual task-meta Publisher** [#3](https://github.com/kaicreator-mm/task-meta/issues/3)/[#5](https://github.com/kaicreator-mm/task-meta/issues/5)/[#12](https://github.com/kaicreator-mm/task-meta/issues/12), **real Tally TS GitHub reader/feedback publisher** [#62](https://github.com/kaicreator-mm/tally/issues/62)/[#65](https://github.com/kaicreator-mm/tally/issues/65) | `docs/implementation/4.15.0/` source test plan / actual GitHub pilot Issue, task-meta+Tally commit SHA/build; credential grant/egress witness; no fake adapter substitution | **required**; high external/authority/privacy; `BLOCKED/NOT_RUN` until external runtime available |
| **S06** | Independent full-version closure, source/version currentness, actual required regression & RQ, only final main integration | S01–S05 accepted; **S05 real E2E PASS** | exact frozen candidate SHA + tree, CI, independent review, real critical journeys/Hidden applicability, release authority; final merge `version/v4.15 → main`, Tag optional | **required**; critical; PR PASS ≠ Release PASS |

## Canonical native dependency edges after Issue materialization

```text
S02 blocked_by S01
S03 blocked_by S02
S05 blocked_by S03
S05 blocked_by S04
S06 blocked_by S05
```

No edges are implied merely by this Markdown. **GitHub native Issue Dependencies must actually exist**, with GitHub readback proving exact edges and no cycle; merely Issue body references or labels never qualify. S01 and S04 have no intra-ADS blockers and may proceed in parallel only **after proper Task Contract, metadata and accepted current Claim admission**. S02 after S01; S03 after S02. S05 after the complete S01→S02→S03 chain **and** S04 and external implementations; S06 after S05. Native edges deliberately use **transitive reduction** (5 edges), not redundant direct blocked_by edges.

## Reuse/not-yet-executable distinction

Pre-existing umbrella/Product issues [#1208](https://github.com/kaicreator-mm/ai-development-standard/issues/1208), [#1205](https://github.com/kaicreator-mm/ai-development-standard/issues/1205), [#1209](https://github.com/kaicreator-mm/ai-development-standard/issues/1209), [#1210](https://github.com/kaicreator-mm/ai-development-standard/issues/1210) are **Product Intake** and normative owners, **not substitutes for admitted executable `type:task` Issues**. This R0 candidate has no new Issue IDs assigned yet. Assign after selected DAG review/Freeze; canonical GitHub metadata and native dependencies become the live status authority, not this file.

## Validation and authority safeguards

- Every executable Issue is `<!-- ads:github -->` + v3 `kind: work_item / type:task` and **actual** native `type:task`, `state:planned|ready|blocked`, `review:...`, `risk:...`; YAML shape alone never admits a Claim or native Issue dependency.
- Each work item has frozen PRD/L2 refs, exact baseline/task branch target, allowed/forbidden paths, tests and failure-handling. One concern per PR to **`version/v4.15`**; do not modify frozen L1/PRD/L2 blobs; do not ship a new service in ADS.
- Schema/reader smoke uses **one real GitHub issue**, supported Agent/Host, actual task-meta publisher and actual Tally TS reader; Tally has **GitHub-only** permissions verified on same build, feedback manifest-free v4 and external real GitHub receipt.
- Keep missing provider metrics `UNKNOWN`, observed CI/Host provenance separately source-qualified; no self-attested `PASS`, no imported private manifest or raw tool args, no second Gate/Task State/Effect authority.
- Source-only CI/fixtures and existing v4.14 conformance **cannot substitute** the required v4.15 external E2E Release Qualification; unresolved S05 ⇒ S06 BLOCKED.
- Do not change effective adopter pins under a pre-RQ candidate; v4.15 schema validation uses an isolated frozen exact test SHA, manual qualified/merged adoption only after release.
- Freeze Task DAG after proportionate review and checkpoint; materialize with native GitHub dependency edges and readback. If the active GitHub connector cannot create native edges, produce a minimal verified local agent dispatch task; **do not claim dependency materialization success**.

**Current state:** `TASK_DAG_NOT_FROZEN`, `TASK_ISSUES_NOT_CREATED`, `NATIVE_DEPENDENCIES_NOT_MATERIALIZED`, `S05_E2E_BLOCKED/NOT_RUN`, `RQ_NOT_READY`. Subsequent source commit for this planning file is not a Product/L2 thaw.
