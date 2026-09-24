# v4.0 T-010 Self-Dogfood Evidence

Status: R4 DOGFOOD PASS — FINAL EVIDENCE CLOSURE CANDIDATE
Task: T-010 / Issue #82
Evidence-closeout coordination: #159
Dogfood coordinator: #153
Carry-forward backlog: #158

## 1. Exact dogfood subject

The current successful self-dogfood result is bound to exactly:

```text
repository: kaicreator-mm/ai-development-standard
ref at dispatch: version/v4.0.0
subject_sha: fdc6a0f6e694284d8e6cdb38ef3ee2e9e499fe15
subject_tree: 194adffc605fbce5d3b5477537ecd99087745993
subject_identity_ref: sha:fdc6a0f6e694284d8e6cdb38ef3ee2e9e499fe15
identity_binding: exact-sha
```

This subject is the integration baseline produced by PR #151 after the R3 successor hardening and Fresh Independent Review #152.

The evidence-closeout commit that adds this file is evidence-only. It does not migrate the R4 dogfood PASS to a semantically changed machine-contract subject. Final PR Review remains exact-HEAD-bound and separate from dogfood evidence.

## 2. Historical rounds remain historical

The following dogfood rounds remain immutable historical `CHANGES_REQUESTED` evidence and are not rewritten as PASS:

- R1: #127;
- R2: #135;
- R3: #145.

R4 is a successor execution against a different exact subject. It does not retroactively change prior outcomes.

## 3. R4 assurance contract

R4 used:

```text
mode: model-diverse-adversarial
model_diversity_basis: provider-diverse
required blind lanes: 2
context independence: required
model independence: required
executor independence: required
majority_vote_for_correctness: false
```

Both first passes were durable before sibling/historical detailed findings were exposed. Cross-challenge occurred only after both blind first-pass records existed.

## 4. Blind first-pass provenance

### Lane A

Durable record: #156
Finding prefix: `R4A-*`

```text
provider: zhipu-bigmodel
model_family: GLM
model_id: GLM-5.3
executor_id: zcode-agent-tool-general-purpose-subagent
context_ref: fresh-isolated-subagent:t010-r4-laneA
blind_first_pass_ref: #156 comment 5809757421
FIRST_PASS_BLIND: true
coverage: 14/14
```

### Lane B

Durable record: #157
Finding prefix: `R4B-*`

```text
provider: deepseek
model_family: DeepSeek-V4
model_id: deepseek-v4-pro
executor_id: deepseek-chat-completions-api
context_ref: fresh stateless API conversation recorded by the coordinator
blind_first_pass_ref: #157 comment 5809876240
FIRST_PASS_BLIND: true
coverage: 14/14
```

The two lanes used distinct providers, model IDs, executors and isolated contexts. The coordinator transported Lane B's durable result but did not author its finding content.

## 5. Coverage

Each blind lane independently covered all required dimensions:

1. authority;
2. lifecycle;
3. Operation;
4. Assurance;
5. model diversity;
6. findings;
7. aggregation;
8. exchange;
9. routing;
10. Validation;
11. Candidate / Release;
12. Fast Path;
13. machine contract / schema-facade non-weakening;
14. compatibility / historical truth.

The coordinator also executed read-only probes to settle factual/runtime claims and re-ran the frozen-subject verifier as corroborating evidence. Model agreement was never treated as Validation truth.

## 6. Aggregate result

Authoritative durable aggregate record for this exercise: #153 comment `5809992547`.

```text
record: T010_R4_DOGFOOD_AGGREGATE_RESULT
outcome: PASS
subject_identity_ref: sha:fdc6a0f6e694284d8e6cdb38ef3ee2e9e499fe15
subject_tree: 194adffc605fbce5d3b5477537ecd99087745993
aggregation_policy: finding-union-blocker-dominance
majority_vote_for_correctness: false
unresolved_blocker_refs: []
requested_route: review-ready
requested_route_authority: NON_AUTHORITATIVE_DERIVED_STATE
```

Finding union summary:

```text
P0: 0
P1: 0
P2: 7 source finding IDs / 6 logical groups
P3: 9 source finding IDs / 6 logical groups
```

Every P2/P3 has an explicit durable disposition. One first-pass P1 was reduced to P2 only after the originating lane conceded severity and executable probes bounded the defect; reviewer count did not determine correctness.

## 7. Carry-forward disposition

All open non-blocking R4 findings are preserved in Issue #158.

P2 groups:

- AG-1 — non-enum aggregation judgment fail-closed behavior;
- MD-2 — single-composite MDA enforcement for every declared diversity basis;
- ID-1 — exact-sha Assurance plan/aggregate identity-format binding;
- OP-1 — `identity_binding:none` prose/machine reconciliation;
- AS-1 — Assurance `depends_on` existence/acyclicity verification;
- RI-1 — Repository Integration precondition evidence binding.

P3 groups include plural provenance facade completeness, legacy Fast Path compatibility debt, wrapped circular self-authority, durable Validation evidence refs, namespaced operation-kind facade checks, single-kind wording reconciliation and the accepted live-DAG boundary for next-operation correlation.

These findings are not erased by the R4 PASS. #158 remains the durable backlog, and T-012/T-013 may reclassify any item if closure/release evidence requires it.

## 8. Non-substitution invariants preserved

R4 evidence does not change these invariants:

```text
Review != Validation
model diversity != executable truth
Operation completion != Gate PASS
PR PASS != Release PASS
Candidate PREPARED != FROZEN
Release READY != Repository Integration complete
routing projection != owning truth dimension
```

The R4 aggregate is assurance evidence about its exact frozen subject. It is not executable Validation, Candidate Freeze, Release Qualification or Repository Integration authority.

## 9. Final T-010 closure gates

After this evidence-only commit:

1. run the full repository `verify-standard` chain on the exact closeout PR HEAD;
2. perform a Fresh Independent Review on that exact HEAD;
3. if both PASS with no blocking finding or identity drift, merge the evidence-closeout PR to `version/v4.0.0`;
4. close #82 completed;
5. only then may T-011 begin.

The Fresh Independent Review must verify that this evidence file accurately points to durable records and does not overstate the scope of R4 PASS or silently discard #158 carry-forwards.
