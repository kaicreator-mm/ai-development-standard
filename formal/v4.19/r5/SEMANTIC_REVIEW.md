# R5 round 2 — Independent Source→Model semantic review (executed)

**Reviewer stance.** This review was produced by a separate verification session, not by the
session that authored the R5 hardening commits. It reads the seven candidate source files at
the independent exact-SHA checkout of PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988`
and the native models at experiment HEAD `e64702c9a9c18c70767cdacc74f086605b38fb39`
(strict fix commit; parent `3d5fd1c6d11eddec313cb25a5a1ea75ac5496b77` is the R5 docs close).
All 27 r4 suite cases were then actually executed with Z3 5.3.3 and cvc5 1.4.2 plus TLC 2.19
under `--model-head`, `--source-checkout`, `--strict-source` (receipt:
`R5_SOURCE_BOUND_RUN.json`, digest in `R5_SOURCE_BOUND_RECEIPT.json`).
Historical #1353 freezes (Product `44562165…`, L2 `b82f201d…`, DAG `fbf1a7d…`) remain frozen
and are not reinterpreted here. This file records semantic correspondence and gaps only; it is
not a normative ADS proof, not a Freeze, and not full rule-denominator coverage.

## Property-by-property Source→Model correspondence

| Property | Source rule (file §) | Model encoding | Verdict |
| --- | --- | --- | --- |
| ADS-P-AUT | `NO_CLAIM_NO_EXECUTION`, accepted Claim as durable Start Record, "rejected, stale or duplicate claim means STOP" (GITHUB_AGENT_INTERACTION_PROTOCOL §8.5, blob 935a905d…); Validator never repairs source — repair needs a separate Builder dispatch (`scripts/v34_rules.py:287-290`, blob 0829be09…); execution profiles/roles (EXECUTION_PACK_STANDARD §4-5, dispatch.schema role enum) | `sourceMutation ⇒ builder ∧ acceptedClaim ∧ writeSetAuthorized ∧ claimCurrent`; 4 UNSAT negatives + nonvacuous witness; mutant drops Claim/currentness/write-set conjuncts and flips SAT | ALIGNED (bounded) |
| ADS-P-CAS | `SINGLE_WRITER_ADMISSION` + `LINEARIZABLE_CONDITIONAL_WRITE`, "A stale expected revision MUST fail the write rather than allow two accepted dispatches/claims"; monotonic `admission_generation` CAS, terminal never decrements generation (EXECUTION_ARCHITECTURE §11.1/§11.1.1) | two-admission QF_LIA model: second acceptance requires own authority + `expectedSecond == secondCurrentGeneration` where a same-key accepted first advances `g→g+1` unless closed; C01 unauthorized UNSAT, C02 two active same-key UNSAT, C03 stale-after-close UNSAT, C04 sequential handoff SAT, C05 distinct keys parallel SAT, C06 own-authority UNSAT; mutant admits both at same generation (SAT) | ALIGNED (bounded; findings S1-S3 below) |
| ADS-P-WRITER-KEYS | Protected claim key is at least `(repository, work item, role)` (§11.1); fail-closed doctrine of §11.1.1; R4 material gap: distinct Claim keys alone do not authorize overlapping writes | concurrent writes require `writeSetsKnown ∧ ¬writeSetsOverlap` even across distinct keys; W01 overlap UNSAT, W02 unknown-relation fail-closed UNSAT, W03 inactive-writer UNSAT, W04 known-disjoint SAT, W05 coexist-without-concurrent-write SAT, W06 authority independence UNSAT; mutant omits the exclusion conjunct (SAT) | ALIGNED as conservative derived discipline (finding S4) |
| ADS-P-DEP / ADS-P-DEP-4 | v4.19 integrated delivery DAG must progress upstream on true blocked predecessors, never fake readiness (INTEGRATED_DELIVERY_DAG_R0 decision table, blob dd72a092…) | 3-node and full 12-edge 4-node rank models: every edge demands strictly increasing topological rank ⇒ any cycle UNSAT in the bounded universe; acyclic witnesses SAT; ranked-4 mutant omits the `eDA` constraint so the injected A→B→C→D→A cycle is SAT | ALIGNED (bounded only, not an unbounded DAG theorem) |
| ADS-P-EVI | CI/review evidence must match exact subject; `expected_base_sha`/`requested_head_sha` are 40-hex exact pins (dispatch.schema.json, GITHUB_AGENT §8.5 provenance list) | `qualified ⇒ acceptedClaim ∧ ciPass ∧ reviewPass ∧ currentHead=ciHead ∧ currentHead=reviewHead` over an abstract `Sha` sort; stale CI/review and NOT_PASS UNSAT; witness SAT | ALIGNED as abstract identity (explicitly not cryptographic) |
| ADS-P-EVO | "Existing v4.18 and #1353-frozen historical subjects"; candidate cannot retroactively amend frozen scopes (EXECUTION_PACK; RULE_CROSSWALK historical_scope, retroactive_amendment=false) | historical denial survives prospective approval (UNSAT), prospective approval cannot self-authorize a new Task (UNSAT), grandfathered and approved-prospective paths SAT | ALIGNED (bounded) |
| ADS-P-CROSS | Composition: release and source mutation consume consistent Claim, DAG state and current evidence (L2_R0 three-domain model, DAG_R0, GITHUB_AGENT, EXECUTION_PACK) | freeze chain `dagFrozen⇒productFrozen`, `claimAccepted⇒dagFrozen`, mutation gate, closure evidence+SHA match, release gate; negatives + legal release witness SAT | ALIGNED composition (bounded) |
| ADS-P-LC | Product→L2→DAG freeze order, Claim gates on DAG freeze, single writer, release needs the full chain (L2_R0 Product Freeze sections, DAG_R0 `NO_CLAIM_GRANTED`, GITHUB_AGENT claim lifecycle) | TLC 2.19 replay of ADSWorkflow.tla: 27 distinct states exit 0, `SingleWriter`+`LifecycleSafe` hold; `UnsafeClaim`/`UnsafeRelease` mutant configs produce 7/3-state counterexamples exit 12 | ALIGNED (bounded; liveness/fairness unmodeled as declared) |

## Semantic findings (non-blocking, recorded for scope honesty)

- **S1 — reservation step unmodeled.** EXECUTION_ARCHITECTURE §11.1 requires the *same*
  serialization mode to protect the earlier dispatch-reservation step ("Two schedulers that
  both observed no active dispatch MUST NOT be able to publish two incompatible
  READY/QUEUED dispatch identities"). The CAS model starts at claim admission and does not
  represent the reservation transition. Bounded-scope limitation; add to the property's
  limitation list rather than treat as satisfied.
- **S2 — idempotent re-claim unmodeled.** §11.1.1 "an identical operator re-claiming the
  same dispatch at the current generation is idempotent" is neither proved nor contradicted
  by the two-admission model.
- **S3 — compatibility-group authorization assumed.** C05's SAT witness for two parallel
  distinct-key claims assumes an authorized parallelism that §11.1.1 ties to a durable
  `compatibility_authority_ref`; the model does not check that authorization.
- **S4 — write-set discipline is model-side.** `ADS-P-WRITER-KEYS` enforces a stricter
  fail-closed discipline (known disjoint sets) than any single source sentence states; it is
  a conservative derived safety property, not a transcription of a source rule.
- **S5 — regression restored.** R5 hardening commit `8a17425` reintroduced the defect that
  R3 had already fixed at `1d21fb9` ("source strictness must not hide solver FAIL"): with
  `--strict-source` and no model pin, the runner blocked before executing and downgraded a
  definite solver failure to BLOCKED. Restored by experiment commit `e64702c`; the R3-era
  regression test now actually executes (formal/tests 18/18 green on exact repo bytes).
- **S6 — anchor honesty.** All 22 source-map/traceability anchors were located in live
  candidate bytes during this review; none is a dangling or decoy string. Anchor presence
  alone does not prove rule equivalence — the per-property table above is the actual
  correspondence claim, bounded to the anchored sections.

## What this review does NOT establish

No natural-language-to-model equivalence theorem, no full ADS rule denominator, no claim
that the bounded models cover all §8/§11 behaviors, no executed GitHub Claim/CAS, CI, Host or
Release, no v4.19 Freeze or merge. Findings S1-S4 are scope limitations, not demonstrated
ADS source defects. Mutation detections certify the *checker*, not the product.
