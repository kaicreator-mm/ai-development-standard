# T-010 Task Pack — Reference Flows and Self-Dogfood Multi-Model Review

Task: T-010 / Issue #82
Primary coordination: #143
Final evidence-closeout coordination: #159
Parent version: #72
Dependency: T-009 / #81 plus successor hardening through #150 / PR #151 / Review #152
Current integration baseline for final closure: `version/v4.0.0@fdc6a0f6e694284d8e6cdb38ef3ee2e9e499fe15`
Final closure branch: `task/v4.0.0-t010-r4-evidence-closeout`
Review Policy: required
Risk: critical
Validation scope: integration
Agent freedom: F1_BOUNDED_IMPLEMENTATION

## Goal

Prove the v4 architecture with end-to-end reference flows and durable blind provider-diverse self-dogfood, then close the Task through evidence-only Stage D, exact-head repository validation and Fresh Independent Review.

Historical dogfood #127, #135 and #145 remain `CHANGES_REQUESTED` evidence. They are regression inputs, never current PASS evidence. R4 #153 is the current successful dogfood result and is exact-subject-bound.

## Frozen / durable inputs for final closure

- #72 / #82 / #143 / #159;
- merged T-001..T-009 v4 architecture and machine contracts;
- historical dogfood #127/#135/#145 and their durable records;
- R3 successor hardening #150 / PR #151 / Fresh Review #152;
- R4 coordinator #153 and blind lanes #156/#157;
- R4 carry-forward backlog #158;
- current dogfood subject / integration baseline `fdc6a0f6e694284d8e6cdb38ef3ee2e9e499fe15`, tree `194adffc605fbce5d3b5477537ecd99087745993`;
- `ADVERSARIAL_REVIEW.md`, `ASSURANCE_PLAN.md`, `OPERATION_CONTRACT.md`, current v4 machine rules/facade and the eight reference flows.

## Allowed write set

The implementation/hardening stages used the broader T-010 write set. The final Stage D/E closeout is deliberately narrower:

- `docs/implementation/4.0.0/SELF_DOGFOOD_EVIDENCE.md`;
- this Task Pack for current-baseline / closure reconciliation;
- `standard-manifest.json` only if repository inventory rules require explicit registration;
- `docs/implementation/4.0.0/TASK_PACKS.json` only if its T-010 pointer needs non-semantic reconciliation.

No schema, semantic-rule, reducer, event, release or migration changes belong in the evidence-closeout PR.

## Required reference scenarios

T-010 keeps eight reference scenarios:

1. major Product/PRD definition;
2. major Architecture/L2 freeze;
3. ordinary bounded implementation Task;
4. high-risk public-contract/security Task;
5. cross-Task/cross-contract coherence review;
6. version closure/release qualification;
7. Fast Path;
8. stale identity/conflict/blocker recovery.

Each scenario exposes authority, Operation sequence/kinds, exact identity boundary, Assurance dimensions, durable evidence, recovery route and a non-substitution invariant.

## Dogfood execution history

### R1

Coordinator #127. Outcome: `CHANGES_REQUESTED`.

### R2

Coordinator #135. Outcome: `CHANGES_REQUESTED`.

### R3

Coordinator #145. Outcome: `CHANGES_REQUESTED`. Its blocker findings drove successor hardening #150 / PR #151.

### R4 — current successful dogfood

Coordinator #153. Outcome: `PASS`.

Exact subject:

```text
sha: fdc6a0f6e694284d8e6cdb38ef3ee2e9e499fe15
tree: 194adffc605fbce5d3b5477537ecd99087745993
identity_binding: exact-sha
```

Blind lanes:

- #156 — provider `zhipu-bigmodel`, model `GLM-5.3`;
- #157 — provider `deepseek`, model `deepseek-v4-pro`.

Both first passes were durable before sibling/historical detailed conclusions were exposed, both attested 14/14 coverage, and cross-challenge occurred only after both blind records existed.

Aggregate: #153 comment `5809992547`.

```text
outcome: PASS
model_diversity_basis: provider-diverse
P0: 0
P1: 0
unresolved_blocker_refs: []
requested_route: review-ready
requested_route_authority: NON_AUTHORITATIVE_DERIVED_STATE
```

All P2/P3 findings have explicit durable dispositions and remain preserved in #158. They are not silently erased by Task closure and may be reclassified later by authorized Closure/Release review.

## Required dogfood assurance invariants

- two independently durable blind first-pass reviews;
- required `model-diverse-adversarial` execution with declared provider-diverse basis;
- actual provider/model/executor/context provenance recorded durably;
- fresh contexts reconstructing from durable authority;
- no sibling/detailed historical conclusions consumed before each first pass is published;
- same 14-dimension coverage matrix for both passes;
- finding union, no majority vote;
- P0/P1 blocker dominance preserved;
- required activity coverage and result identity attested at aggregation;
- cross-challenge only after both first-pass records are durable;
- factual/runtime conflicts routed to executable evidence;
- aggregate exact-subject-bound and never treated as executable Validation truth.

## Staged completion

### Stage A — reference/protocol + hardening candidate

Completed through the T-010 implementation/successor chain. The reference flows and focused regressions are present in the integration baseline.

### Stage B — repository-real validation

Completed for implementation/hardening candidate heads through GitHub Actions. Historical CI remains historical and does not satisfy Stage D final-head validation.

### Stage C — local model-diverse dogfood execution

Completed by R4 #153 with provider-diverse blind lanes #156/#157. Earlier R1/R2/R3 non-PASS outcomes remain historical.

### Stage D — evidence closure

Add `SELF_DOGFOOD_EVIDENCE.md` containing only durable refs, exact identity/provenance/coverage/aggregation metadata and dispositions. Do not copy private model scratchpad/transcripts or hidden evaluator payload.

The evidence-closeout commit is evidence-only. It does not migrate R4 PASS to a semantically changed machine-contract subject. It does invalidate any earlier PR-head CI/Review claim for the closeout PR itself, so exact-head repository validation must rerun.

### Stage E — Fresh Independent PR Review

Review the final evidence-closeout PR exact HEAD after Stage D. Dogfood evidence does not replace this Review. Review must confirm evidence accuracy, historical-truth preservation, #158 carry-forward preservation, and the absence of semantic code/schema changes.

## Validation commands

The authoritative CI chain remains the repository `verify-standard` workflow, including the v4 focused suites such as:

```text
python scripts/test_v40_r3_carryforward.py
python scripts/test_v40_reference_flows.py
python scripts/test_v40_t010_successor_hardening.py
python scripts/test_v40_t010_canonical_surface.py
```

Static inspection is not Validation PASS.

## Forbidden scope

- no migration/adoption policy (T-011);
- no T-012 Closure review;
- no T-013 Release Qualification/main integration;
- no event-v3;
- no second lifecycle/reducer/DAG;
- no majority-vote dogfood aggregation;
- no claiming two prompts from one continuing model/session as model diversity;
- no changing diversity basis after seeing results merely to obtain PASS;
- no inventing Validation truth from review consensus;
- no relabeling #127/#135/#145 from `CHANGES_REQUESTED` to PASS;
- no erasing or silently closing #158 carry-forwards as part of T-010 closeout.

## Completion

Eight reference scenarios + focused machine regressions present → R4 durable provider-diverse dogfood PASS on exact subject → `SELF_DOGFOOD_EVIDENCE.md` committed → final exact-head full verifier PASS → required Fresh Independent Review PASS → merge evidence-closeout PR to `version/v4.0.0` → close #82 completed → T-011 may begin.
