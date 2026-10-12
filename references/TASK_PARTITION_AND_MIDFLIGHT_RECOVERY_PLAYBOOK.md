# Task Partition and Mid-flight Recovery — practice playbook

> **NON-NORMATIVE / NEXT-VERSION REVIEW INPUT.** Field practice for [ADS #1072](https://github.com/kaicreator-mm/ai-development-standard/issues/1072), subordinate to the current `TASK_DECOMPOSITION_STANDARD`, `TASK_DAG_GOVERNANCE_STANDARD`, `EXECUTION_ARCHITECTURE_STANDARD`, `VALIDATION_STANDARD`, and Claim/Review authority. This file creates **no new Task gate, schema, workflow state, reviewer role, actor permission, or frozen DAG node**. The frozen v4.11 DAG remains 20 nodes / 30 edges; no v4.11 release assurance is granted by this reference.

## 1. Scope, entry and decision

Use when (a) pre-dispatch planning reveals a parent combining multiple independently executable concerns or (b) an **ACTIVE** Builder/Claim unexpectedly spans overlapping mutable sources, duplicate PRs, independently owned Validation/Review, or private Hidden/Release tasks. Do not use a file-count, line-count, elapsed-time or token threshold as an automatic split policy.

Start with **live** GitHub Issue Dependencies, current Claim/Terminal and exact PR HEAD/base/tree, compared with the frozen Pack/DAG and current owner write sets. Do not redispatch from a stale issue body. Return one of:

- `SPLIT`: only if each new concern has an independent semantic contract, disjoint or serially owned mutable files, independently validatable accepted outcome, lawful DAG mutation when required, and a safe integration owner.
- `PRESERVE_ATOMIC`: unavoidable trust/runtime/ABI integration cannot be merged in valid partial states; keep one owner PR, reduce the remaining findings to bounded sub-results in that same Claim/branch.
- `PARALLEL_EVIDENCE_ONLY`: allow disjoint read-only test/Oracle/negative-case preparation, while exactly one writer owns the shared integration and no evidence lane claims a release verdict.

The decision should include `reason`, `owner`, `canonical_candidate`, `write_set`, `review_actor`, `validation_environment`, `merge_convergence` and any `BLOCKED` fact. Sibling dispatches are not automatically new DAG Tasks.

## 2. Pre-dispatch partition card

| Field | Evidence expected |
|---|---|
| Parent outcome | One version-level result; exact issue and Frozen DAG pin |
| Concern seams | Contract / core / authenticated host / UX / business / tests / closure, only where real |
| Native dependencies | Live blocked-by readback; remaining owner authority |
| Claim and PR identities | Protected key, current actor/session, HEAD/base/tree, accepted Terminal and Review |
| Shared mutable files | Exact paths, owner of each and current writer count |
| Validation boundaries | Focused tests, independent Reviewer, real Host/Hidden requirements |
| Candidate convergence | One nominated integration candidate and explicit final combined gate |
| Partition disposition | SPLIT / PRESERVE_ATOMIC / PARALLEL_EVIDENCE_ONLY with cost and safety rationale |
| Release ownership | Separate Visible, Hidden, Fresh Closeout and RQ actors; no Builder self-PASS |

For a small bounded Task with no overlap, this card may be embedded in its existing Task Pack/Claim. Do **not** create a new Issue merely to hold the card.

## 3. Mid-flight collision protocol

1. **Snapshot (read-only).** Read every currently claimed/accepted PR and Issue, the exact SHA/tree, changed paths, independent Review, CI, Owner and merge targets. Mark stale/unknown facts `UNKNOWN`, never `PASS`.
2. **Stop incompatible writers.** Overlapping write sets or duplicate protected Claim keys forbid new incompatible Builder admission. Do not force-push, blindly cherry-pick or merge a green sibling.
3. **Choose one canonical implementation candidate.** Explain why it covers the accepted semantics and real deficits. Treat other branches as frozen reference assets with exact file/blob inventory, not alternate authoritative PRs. No historical PASS is transferred.
4. **Recover tests first.** Extract disjoint negative cases, consumer oracles and review findings only if they can be incorporated under the canonical owner's write set and the existing authority. Precompiled evidence is not a new production implementation.
5. **Decide whether a *lawful* DAG mutation is necessary.** If source-ownership/dependency topology really changes, escalate `ADD/SPLIT/SUPERSEDE` through the existing explicit DAG governance; do not mutate a Frozen DAG through chat or Issue-body prose.
6. **Scope freeze; merge drain.** Stop repeated demos/advisory hardening unless a new material P0/P1 arises. Do not mutate source during genuinely Fresh Review. Use focused tests for defects, then one exact-HEAD combined gate and independent Review.
7. **Postmerge and closure.** Guarded merge to legal target, postmerge currentness and CI, Task Terminal; full visible/hidden/package/release checks remain separate. PR PASS is never Release PASS.

### Safety-negative: overlapping writers

**Setup:** Two proposed Builders independently request edits to the same `microkernel.ts` protected source on the same work item. One already holds the accepted incompatible Claim. **Expected:** second Claim/dispatch is blocked; its work may be preserved as read-only exact-blob evidence, but must not be merged as another live writer. A second accepted incompatible Claim, silent file overwrite, or promoted Review PASS is a **failure**. This is a *specified falsifier*, **not a claim that an executable implementation of the admission controller was run for this document**; an independent executable replay is needed for closure.

### Positive: parallel evidence without fake split

**Setup:** A D2 Approval test author, D3 Engineering test author and two source-only Oracle authors work in disjoint test/evidence files while the canonical integration Builder handles shared H/K/S/B and authenticated UX. **Expected:** independent tests can complete as evidence; one integration PR combines current source, passes full E2E and receives its own required Review. No evidence lane obtains the right to merge the canonical Runtime or declare release.

## 4. DomainHarness v0.8 recorded practice

| Work item | Actual issue evidence | Partition / convergence decision | What was **not** proven |
|---|---|---|---|
| [#1013](https://github.com/kaicreator-mm/domain-harness/issues/1013) / [PR #1016](https://github.com/kaicreator-mm/domain-harness/pull/1016) | One candidate touched 46 files, +3511/-117 at cited HEAD; #1014 and #1015 overlapped. Canonical selection recorded at #1013@6117177222; scope freeze at @6118857314 | **PRESERVE_ATOMIC** existing integration owner; overlapping PRs read-only assets; bounded R1/R2 repairs; no blind new writer | File count alone does not establish defect or authorize split; later review/CI/host truth must be re-read |
| [#1005](https://github.com/kaicreator-mm/domain-harness/issues/1005) / [PR #1012](https://github.com/kaicreator-mm/domain-harness/pull/1012) | D2/D3 dual-domain acceptance plus source-only FR02/FR07 and FR05/FR08 oracles; 29 reused D2/D3/F01 tests at cited PR state | **PARALLEL_EVIDENCE_ONLY**, one dual-app convergence parent and exact H-authenticated E2E before terminal | Independent oracle preparation is not proof of an integrated, packaged, real-host domain app |
| [#1006](https://github.com/kaicreator-mm/domain-harness/issues/1006) | 44 retained-functionality rows, Node22/24 SQLite/CAS/UNKNOWN, clean consumers, private Hidden and RQ | **Separate execution/evidence actors**, **single Release Qualification**; private pack creation can precede Candidate Freeze, private Hidden execution cannot | The 44 rows remain `NOT_RUN` until real exact-candidate execution; no public Hidden vectors or speculative release PASS |

This classification was applied as a no-DAG-expansion decision in ADS #1072@6119122889. No claim is made that #1013's failures, all #1005 consumers, or #1006's 44 rows have passed since that recorded subject; re-read live GitHub before future use.

## 5. Evidence and learning

Record only observed measurements: `scope_expansion_count`, `overlap_pr_count`, `repeated_review_rounds`, `actual_changed_files`, `evidence_reuse_count`, `critical_path_wait_reason`. Use `UNKNOWN` rather than inventing costs, approvals or percentages. A proposed `SPLIT` must record expected critical-path relief **and** risk of writer collision, shared files and extra review gates.

Recommended owner route: ADS #775 for Task decomposition/granularity; #680 for proportional gate cost and stop rules; #803 for estimate-vs-actual telemetry; #926 for gate proliferation; #1072 for active-Claim field practice. This practice reference must not replace their normative standards.

## 6. Exit decision

```ini
PARTITION_DISPOSITION=<SPLIT|PRESERVE_ATOMIC|PARALLEL_EVIDENCE_ONLY>
AUTHORITATIVE_CLAIM=<exact ref or UNKNOWN>
CANONICAL_CANDIDATE=<PR@SHA/tree or NONE>
OVERLAP_WRITESET=<paths with active owners>
EVIDENCE_LANES=<IDs, nonblocking unless separately mandated>
NEW_NATIVE_DAG_MUTATION=<NONE|explicit owner-approved ref>
FOCUSED_VALIDATION=<exact refs or NOT_RUN>
COMBINED_VALIDATION=<exact refs or NOT_RUN>
FRESH_REVIEW=<exact ref or NOT_RUN>
RELEASE_QUALIFICATION=NOT_INFERRED
NEXT_OWNER=<existing Issue / operator>
```

**Stop** after one lawful disposition unless a material new P0/P1, accepted source drift, or genuine new dependency is observed. No universal task-size threshold, self-Review, unauthorized Frozen DAG modification, or fake full/Hidden/Release gate.
