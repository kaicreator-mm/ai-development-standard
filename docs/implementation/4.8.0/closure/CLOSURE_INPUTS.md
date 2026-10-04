# v4.8.0 Integrated Convergence / Version Closure Inputs — T-014

Status: **CLOSURE INPUTS ONLY — this document issues no Version Closure, Release Qualification, Hidden Validation, tag/release or main-integration verdict.**

```text
CLOSURE_VERDICT_ISSUED=NO
RELEASE_QUALIFICATION_VERDICT_ISSUED=NO
HIDDEN_VALIDATION_VERDICT_ISSUED=NO
BUILDER_SELF_VALIDATION=NO
BUILDER_SELF_REVIEW=NO
MERGE_AUTHORIZED=NO
```

These are closure INPUTS only. Version Closure verdict authority remains with the later closure gates (independent integrated-closure Validation, then genuinely Fresh Independent Review, then the Controller). Every claim below binds an exact durable ref; the machine-readable counterpart of this document is `docs/implementation/4.8.0/closure/INTEGRATED_REGRESSION_EVIDENCE.json` and the focused oracle `scripts/test_v48_integration_closure.py` (C01–C10 of `.agent/execution/T-014/TEST_MATRIX.yaml`).

## 1. Exact subject and evidence scope

- Base: `version/v4.8.0@6bfb8aecd4c7e533ae4f392dc4e58de1da71d5b4` (tree `593dd5d12890f68e3830419b07b909ccf587dc2b`); live currentness re-checked at Builder claim (claim `#520@5974957328`, CURRENTNESS=PASS).
- Execution Pack head admitted: `a7fc5f56b78ca1af4f2d4cfa6313a057a830e510` (tree `2bd3f2719151a373e4365ce6641c0e25ea207dd0`); Dispatch `#520@5974939373`, Handoff `#520@5974940298`.
- Candidate: this document, `INTEGRATED_REGRESSION_EVIDENCE.json` and `scripts/test_v48_integration_closure.py` at their own commit on `task/v4.8.0-t14-integration-closure-inputs` (exact head/tree recorded in the T-014 Builder terminal on #520 and the PR body). Write set = exactly those three paths; the six `.agent/execution/T-014/**` planning files and all Frozen authorities are untouched.
- Frozen authorities consumed read-only: Frozen Product blob `f26439580e00de6ed8b2e27d732a3095eb566219` (`docs/implementation/4.8.0/PRD.md`), Frozen L2 blob `f88c85454e80101a0fdf56050e21f11a05279841` (`docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md`), Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34` (`docs/implementation/4.8.0/TASK_DAG.md`), Task Pack blob `1373438d17ca540c69d14f835d0f7252b7221b82`, L3 blob `8af06fd5bd7237b260fe478c23cb410c0e15898f`.

## 2. Integrated v4.8 semantics inventory

### 2.1 Exactly three new default machine-contract families (L2 §4; C01)

Frozen L2 §4: "v4.8 introduces exactly **three new default machine-contract families**". Count and identities below are asserted mechanically by `test_c01_exactly_three_new_v48_machine_families` against the live `standard-manifest.json`; a fourth family, a dropped family or a rename fails the test.

| # | Family (schema) | `schema_version` | Semantic concern (`entry_id`) | Canonical owner (unchanged) | Frozen refs |
|---|---|---|---|---|---|
| 1 | `schemas/task-learning-v1.schema.json` | `ai-dev/task-learning-v1` | `execution.task_learning_evidence` (`task-learning-evidence`) | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | L2 `@f88c85454e80101a0fdf56050e21f11a05279841` §4.1; PRD `@f26439580e00de6ed8b2e27d732a3095eb566219` §3 item 1, §4; `references/TASK_LEARNING_EVIDENCE_REFERENCE.md` |
| 2 | `schemas/agent-capability-profile-v1.schema.json` | `ai-dev/agent-capability-profile-v1` | `execution.logical_agent_capability_claim` (`logical-agent-capability-profile`) | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | L2 §4.2; PRD §3 item 2, §5; `references/AGENT_CAPABILITY_PROFILE_REFERENCE.md` |
| 3 | `schemas/agent-capability-evidence-v1.schema.json` | `ai-dev/agent-capability-evidence-v1` | `execution.agent_capability_evidence` (`agent-capability-evidence`) | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | L2 §4.3; PRD §3 item 2, §5; `references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md` |

Registry discovery: `references/V48_REGISTRY_ADOPTION_REFERENCE.md` (`MACHINE_FAMILY_TARGET=EXACTLY_3`, `INTERCHANGE_POLICY=REUSE_EXISTING_V1_EXACTLY_ONCE`). No Availability family exists (L2 §6, UNKNOWN U2): no `*availability*` schema, no manifest machine contract, no state-dimension entry. ADS evolution feedback (PRD §3 item 5) deliberately creates no machine family — promotion is ordinary governance (L2 §12, U8).

### 2.2 Interchange — single-surface reuse, not duplication (L2 §5; C02)

- The transport-neutral correlation owner remains `docs/implementation/4.0.0/AGENT_INTERCHANGE.md` + `schemas/interchange-envelope-v1.schema.json` (`ai-dev/interchange-v1`, `authority_effect=CORRELATION_ONLY_NON_AUTHORITATIVE`), registered exactly once in `standard-manifest.json`; GitHub writer/admission remains `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` / `ai-dev:event:v2`.
- T-003 disposition (`references/V48_INTERCHANGE_PROFILE_COMPATIBILITY.md`): `INTERCHANGE_SCHEMA_CHANGE=NO_CHANGE_REQUIRED`, `GITHUB_PROTOCOL_CHANGE=NO_CHANGE_REQUIRED`, `NEW_EXCHANGE_FAMILY=FORBIDDEN`, `EVENT_V3=NOT_REQUIRED`. No `AGENT_EXCHANGE_BINDING_STANDARD.md`, no v2 envelope exists anywhere in the tree.

### 2.3 Owner-uniqueness map v4.1–v4.8 (C03)

`standard-manifest.json#semantic_authorities` (11 entries) and `registries/state-dimensions-v1.json` (9 dimensions) hold one canonical owner per concern/dimension; `test_c03_owner_uniqueness_across_v4_1_to_v4_8` asserts uniqueness and that every inherited v4.1–v4.7 concern keeps its exact inherited owner.

| Concern (`entry_id`) | Canonical owner | Inherited from | Posture |
|---|---|---|---|
| `development.lifecycle_and_task_stage` (`development-lifecycle`) | `standards/DEVELOPMENT_WORKFLOW.md` | pre-v4.8 (inherited) | `ALWAYS` |
| `github.issue_pr_event_coordination` (`github-agent-coordination`) | `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` | pre-v4.8 (inherited) | `MATERIALITY_DRIVEN` |
| `execution.controller_and_dispatch_state` (`execution-state`) | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | pre-v4.8 (inherited) | `MATERIALITY_DRIVEN` |
| `github.work_item_contract` (`work-item-contract`) | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` | pre-v4.8 (inherited) | `MATERIALITY_DRIVEN` |
| `validation.concern_evidence_and_exact_subject` (`validation-evidence`) | `standards/VALIDATION_STANDARD.md` | pre-v4.8 (inherited) | `MATERIALITY_DRIVEN` |
| `release.qualification_and_candidate_gate` (`release-qualification`) | `standards/RELEASE_STANDARD.md` | pre-v4.8 (inherited) | `MATERIALITY_DRIVEN` |
| `ci.runner_capability_adoption` (`runner-capability`) | `standards/CI_RUNNER_CAPABILITY_STANDARD.md` | pre-v4.8 (inherited) | `PROJECT_DEFINED` |
| `architecture.research_demo` (`research-demo`) | `standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md` | pre-v4.8 (inherited) | `OPTIONAL` |
| `execution.task_learning_evidence` (`task-learning-evidence`) | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | **new in v4.8** | `MATERIALITY_DRIVEN` |
| `execution.logical_agent_capability_claim` (`logical-agent-capability-profile`) | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | **new in v4.8** | `MATERIALITY_DRIVEN` |
| `execution.agent_capability_evidence` (`agent-capability-evidence`) | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | **new in v4.8** | `MATERIALITY_DRIVEN` |

One owner may serve distinct concerns (Execution Architecture owns four); no concern is owned twice. The registry itself remains discovery metadata with `authority_effect=NONE` (v4.7 carry-forward, `references/V48_REGISTRY_ADOPTION_REFERENCE.md` §5–6); no fourth semantic owner was created by registering the new families.

### 2.4 Hard eligibility before optional ranking (L2 §8; EAS §27.2; C04)

`standards/EXECUTION_ARCHITECTURE_STANDARD.md` §27.2: "`**All hard predicates are evaluated before ranking.**` Only `ELIGIBLE` choices may enter optional ranking" and rank inputs "MUST NOT promote `INELIGIBLE` or `UNKNOWN` to `ELIGIBLE`". Eligibility stays a derived tri-state (`ELIGIBLE | INELIGIBLE | UNKNOWN`, UNKNOWN fails closed); no universal Agent score or economic optimizer exists (L2 U4/U10).

### 2.5 Composite work + resource admission atomicity (L2 §9; EAS §27.3–27.4; C05)

The protected set `A = {work_claim_key} ∪ every required resource/capacity binding` linearizes all-or-none at one admission point (`SINGLE_WRITER_ADMISSION` or `LINEARIZABLE_CONDITIONAL_WRITE`); per-key CAS sequences are explicitly not composite proof; `sum(active accepted units bound to G) <= N` (exclusive `N=1`) holds at every canonical transition; the four partial canonical states (EAS §27.3 block) are forbidden; crash/publication ambiguity fails closed until durable reconciliation (§27.4). No second reservation authority exists (U3).

### 2.6 Historical compatibility and Fast Path (L2 §14; PRD §16; C06)

Historical Task Packs, Execution Packs, Dispatches, `interchange-envelope-v1`, `ai-dev:event:v2` and Validation/Review payloads remain valid; the pinned historical event-v2 claim and interchange handoff still validate, the dispatch schema keeps its exact pre-v4.8 required set (L2 §10 candidate optional refs were conservatively not added), and `TASK_LEARNING=NONE_MATERIAL` stays a valid complete Fast Path outcome (`standards/PROJECT_ADOPTION.md`, `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`, `references/V48_REGISTRY_ADOPTION_REFERENCE.md` §4, `standards/DEVELOPMENT_WORKFLOW.md` §7).

### 2.7 Dogfood claims bounded to evidence strength (C07)

The merged dogfood evidence preserves the `NOT_MEASURED` economics posture end-to-end: `dogfood/469/RESULT.md` (`ECONOMIC_SAVINGS=NOT_MEASURED`, `BLANKET_STRONG_TO_LOW_COST_RULE=NOT_SUPPORTED`, `DISPOSITION=MORE_EVIDENCE`, `STANDARD_CHANGE=NOT_AUTHORIZED`), `dogfood/evolution/EVIDENCE_MATRIX.json` (`claim_boundaries`, all three streams `external_claim_eligible=false`), `dogfood/orchestration/RESULT_REPORT.md` (descriptive-only measurements; no universal ranking / blanket routing / savings claim). No economic-savings or universal-routing inference exists without comparable measured evidence (OVERCALL guard: OVERCLAIM disposition of the T-014 FAILURE_MATRIX).

## 3. Evidence index (acceptance oracles → proof)

Focused oracle: `scripts/test_v48_integration_closure.py` (run `python -B scripts/test_v48_integration_closure.py`; exit 0; counts in the execution evidence). Regression evidence: `docs/implementation/4.8.0/closure/INTEGRATED_REGRESSION_EVIDENCE.json` (base `6bfb8aecd4c7e533ae4f392dc4e58de1da71d5b4`, host-identified, one row per executed command with exit code and summary).

| Oracle | Assertion (TEST_MATRIX) | Proof surface(s) | Execution evidence |
|---|---|---|---|
| C01 | exactly three new v4.8 machine families from Frozen L2/Product; count fails on any other count | `standard-manifest.json` machine_contracts ∩ semantic_authorities vs pinned pre-v4.8 inventory; L2 §4 anchors; `references/V48_REGISTRY_ADOPTION_REFERENCE.md` `MACHINE_FAMILY_TARGET=EXACTLY_3` | `test_c01_exactly_three_new_v48_machine_families`; `INTEGRATED_REGRESSION_EVIDENCE.json` `commands[]` (focused-test row) |
| C02 | Interchange owner reused, single canonical surface | manifest single registration; no v2 envelope / no `AGENT_EXCHANGE_BINDING_STANDARD.md`; `references/V48_INTERCHANGE_PROFILE_COMPATIBILITY.md` dispositions; L2 §5 anchor | `test_c02_interchange_owner_reused_exactly_once` |
| C03 | owner uniqueness v4.1–v4.8; duplicates fail | `standard-manifest.json#semantic_authorities` (11 entries, unique ids/concerns, inherited owners unchanged); `registries/state-dimensions-v1.json` (9 dimensions, no availability) | `test_c03_owner_uniqueness_across_v4_1_to_v4_8` |
| C04 | eligibility-before-ranking enforced | EAS §27.2 anchors; L2 §8 anchors; PRD §6.2 anchor; tri-state + rank-exclusion behavioral model | `test_c04_hard_eligibility_precedes_ranking` |
| C05 | composite resource atomicity retained | EAS §27.3/§27.4 anchors incl. forbidden partial states and capacity invariant; L2 §9 anchors; all-or-none admission behavioral model (capacity N=1 race, subset rejection) | `test_c05_composite_resource_admission_is_atomic` |
| C06 | historical compatibility + Fast Path present and valid | historical event-v2/interchange payloads validate; dispatch required set unchanged; Fast Path anchors in `PROJECT_ADOPTION.md` / `TASK_LEARNING_EVIDENCE_REFERENCE.md` / `DEVELOPMENT_WORKFLOW.md` §7 / PRD §16 | `test_c06_historical_compatibility_and_fast_path` |
| C07 | dogfood claims bounded; NOT_MEASURED preserved | `dogfood/469/RESULT.md` + `EVIDENCE_MATRIX.md`; `dogfood/evolution/EVIDENCE_MATRIX.json` `claim_boundaries`; `dogfood/orchestration/RESULT_REPORT.md`; unsupported-claim negative scan | `test_c07_dogfood_claims_bounded_not_measured_preserved` |
| C08 | regression evidence covers verify_standard + every pinned `run:` command with exits | `.github/workflows/verify-standard.yml` parsed live (25 pinned commands) + `python -B scripts/verify_standard.py` + focused test; all rows exit=0 | `test_c08_regression_evidence_covers_pinned_commands` |
| C09 | closure inputs contain no closure/release verdict | forbidden verdict-assignment scan over both closure files; boundary sentinels present | `test_c09_closure_inputs_issue_no_verdict` |
| C10 | every carry-forward / NOT_RUN\|BLOCKED item has exact ref + routing | §5 carry-forward table rows (ref + routing cells); §6 sentinels; `not_run` rows require reasons | `test_c10_carry_forwards_and_not_run_items_have_refs_and_routing` |

## 4. Full pinned visible regression (execution evidence)

Executed on the LOCAL build host at the exact base, each command individually, from the repository root: `python -B scripts/verify_standard.py` plus every pinned `run:` command of `.github/workflows/verify-standard.yml` (25 commands, verbatim) plus the focused T-014 oracle (`python -B scripts/test_v48_integration_closure.py`). Exact commands, exit codes, test/suite counts, host identity (OS / git / python) and generation time are recorded in `INTEGRATED_REGRESSION_EVIDENCE.json`. Result: **27/27 commands exit=0, no substitution, no NOT_RUN.** This is Builder-executed evidence, not independent Validation.

## 5. Carry-forwards and routed findings

Unresolved adverse findings and routed items carried forward from the integrated v4.8 lane. Each row binds an exact ref and a routing; none is repaired in this lane (no silent semantic repair).

| ID | Finding | Exact ref | Routing |
|---|---|---|---|
| CF-01 | T-013 P3-01 (cosmetic, non-blocking): JIT TEST_MATRIX `required_builder_checks` (`python -B scripts/verify_standard.py`) lacked a durable in-repo Builder evidence line under `docs/implementation/4.8.0/dogfood/evolution/` at the T-013 head; non-blocking per Fresh Review because CI run 37155721886 executed the pinned commands. T-014 answers the evidence-line concern for the closure lane: the durable per-command evidence now exists at `docs/implementation/4.8.0/closure/INTEGRATED_REGRESSION_EVIDENCE.json`. | `#763@5974751546` (T-013 Fresh Review result, P0=0/P1=0/P2=0/P3=1); consumed note `#763@5974764506` | informational carry-forward; T-013 evidence-line practice satisfied for T-014 by this repository's evidence file; no code change authorized here |
| CF-02 | #469 bounded-agent evidence stream remains `MORE_EVIDENCE`: economic savings `NOT_MEASURED`, blanket strong-to-low-cost routing `NOT_SUPPORTED`; heterogeneous task classes and comparable token/cost/latency/rework measurement remain missing | `dogfood/469/RESULT.md` at base `6bfb8aecd4c7e533ae4f392dc4e58de1da71d5b4`; anchor `#469@5925124956` | ordinary ADS evolution governance only (`DISPOSITION=MORE_EVIDENCE`); no v4.8 standard change authorized |
| CF-03 | Cross-project evolution dogfood (T-013) streams S1–S3: all `external_claim_eligible=false`, dispositions `MORE_EVIDENCE`/`NO_CHANGE`; private-project evidence stays non-publishable | `#519` / `docs/implementation/4.8.0/dogfood/evolution/EVIDENCE_MATRIX.json` at base `6bfb8aecd4c7e533ae4f392dc4e58de1da71d5b4` | routed to future evidence collection; no closure implication |
| CF-04 | v4.9 work items (e.g. `#764`, v4.9 T-002 Fresh Independent Review for PR #757) are out of scope for v4.8 closure inputs and are deliberately not imported into this carry-forward set | `#764` (live state: open, v4.9 lane) | v4.9 lane; excluded from v4.8 closure scope |

No owner Task defect was discovered by this integrated pass that would require routing to an owning Task: C01–C07 passed against the integrated baseline without repair (see §3 evidence index).

## 6. NOT_RUN / BLOCKED items

```text
NOT_RUN_ITEMS=NONE
BLOCKED_ITEMS=NONE
```

Every pinned visible regression command and the focused oracle ran successfully on the LOCAL build host; `INTEGRATED_REGRESSION_EVIDENCE.json#not_run` is empty. No evidence required for C01–C10 was unavailable; no Hidden/private payload was consumed.

## 7. Authority boundary

This document and `INTEGRATED_REGRESSION_EVIDENCE.json` are closure INPUTS only: integrated semantics inventory, bounded execution evidence, and carry-forward routing. They issue no Version Closure, Release Qualification, Hidden Validation, tag/release or main-integration verdict, and they do not substitute for independent Validation or genuinely Fresh Independent Review. Version Closure verdict authority remains with the later closure gates on the exact candidate HEAD. The Builder performed no source mutation outside the three authorized write-set paths and performed no semantic repair of any owner Task.
