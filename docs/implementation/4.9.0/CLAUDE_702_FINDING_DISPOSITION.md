# v4.9.0 — Claude #702 Product Finding Disposition

Source review: `#702@5966353271`
Source subject: PRD v0.3 / PR #698 HEAD `0c9b352c106f0068cec2f15baab96b4add724ff4` / tree `f5c20c25422f9f28284e2c59f583b7c98ead3c27` / PRD blob `fbd1b265491415451e8de382069a1b7df8f24321`
Source verdict: `FAIL`, `P0=0/P1=3/P2=6/P3=3`
Successor Product candidate: `PRD v0.4`
Disposition work item: `#706`

This artifact is Controller/Product-author disposition evidence. It is not independent Review authority and does not authorize Product Freeze.

## F1 — P1 — single-owner fail-closed predicate proof

Disposition: **CLOSED_IN_V04**.

PRD v0.4 §4.2 restores the requirement that every owner-scoped reduction predicate be established by current durable facts or an owner-accepted deterministic check. Model judgment alone is insufficient. Unknown/ambiguous/unproven predicates choose the stronger path or `BLOCKED`. §15 adds an explicit single-owner ambiguous-predicate acceptance scenario.

## F2 — P1 — downstream dogfood vacuity

Disposition: **CLOSED_IN_V04**.

PRD v0.4 §16 defines:

- a qualifying downstream project;
- exact candidate/revision binding;
- a legal baseline-vs-selected execution record;
- per-mechanism `EXERCISED|NOT_EXERCISED` evidence;
- at least one exercised unknown/ambiguous predicate;
- at least one nonzero authorized proportional delta;
- independent safety-negative audit;
- manual/GitHub-native viability;
- claim boundaries preventing unexercised mechanisms from being generalized.

Broken §16.13 references are removed.

## F3 — P1 — P4 overlaps v4.8 learning/evolution authority

Disposition: **CLOSED_IN_V04**.

PRD v0.4 §13 binds P4 to v4.8 `Task Learning Evidence v1`, `TASK_LEARNING=NONE_MATERIAL`, `ADS_EVOLUTION_CANDIDATE` and existing Evolution Intake. v4.9's delta is limited to execution-friction mappings and a bounded recurrence-audit escalation hook. Parallel learning/evolution families/intake, automated cross-project mining, universal fingerprinting and a dedicated learning database are explicitly non-goals. L1 is reconciled.

## F4 — P2 — weakened Product Freeze precondition / incomplete successor-review scope

Disposition: **CLOSED_IN_V04**.

PRD v0.4 §20 restores a fresh independent Product Review bound to the exact successor candidate as the Freeze precondition. Any material post-review revision requires full review or bounded review covering the complete predecessor→successor diff with diff-level no-regression/no-unreviewed-scope accounting. Controller disposition cannot satisfy the gate. #701 is retained as historical-only v0.3 evidence after #702 falsified its no-regression conclusion.

## F5 — P2 — specialized-role scope expansion

Disposition: **CLOSED_IN_V04**.

PRD v0.4 §8.5 restores `when standardized or used by the applicable project` and explicitly states Product does not require identical lifecycle depth for all roles.

## F6 — P2 — adverse verdict suppression / reviewer shopping

Disposition: **CLOSED_IN_V04**.

PRD v0.4 §6.3 explicitly forbids hiding, superseding, ignoring or dispatching around adverse independent terminals/findings merely to obtain PASS. Existing finding-union/blocker-dominance semantics remain binding. Re-review after FAIL requires successor subject or owning-authority disposition. §9.1 adds executor-selector conflict as an applicable independence dimension.

## F7 — P2 — retroactive migration

Disposition: **CLOSED_IN_V04**.

PRD v0.4 §17 makes migration owning-authority-governed and prospective-only. It cannot shorten gates already required for an in-flight Frozen/qualified/authority-bound candidate. The no-retroactive-shortening invariant is restored.

## F8 — P2 — release-applicability ownership

Disposition: **CLOSED_IN_V04_PRODUCT_DECISION**.

v4.9 chooses the prospective-policy option. PRD v0.4 §5.3 keeps Release applicability owned by `RELEASE_STANDARD.md` while placing prospective proportional Release-owned applicability predicates in v4.9 Product scope. L2 may encode those predicates only under positive permission, durable/deterministic proof, fail-closed ambiguity and prospective-only migration. Until such authority is Frozen/applicable, existing mandatory release gates remain unchanged.

## F9 — P2 — no binding to v4.8 predecessor / release lineage

Disposition: **CLOSED_IN_V04**.

PRD v0.4 and L1 bind reused predecessor authority to:

```text
V48_FROZEN_PRD_BLOB=f26439580e00de6ed8b2e27d732a3095eb566219
V48_FROZEN_L2_BLOB=f88c85454e80101a0fdf56050e21f11a05279841
```

Drift/thaw/supersession triggers v4.9 currentness re-evaluation. v4.9 Release Qualification requires the required v4.8 predecessor in the integrated lineage.

## F10 — P3 — broken cross-references

Disposition: **CLOSED_IN_V04**.

The downstream contract is consistently referenced as §16; no §16.13 reference remains.

## F11 — P3 — undispositioned v0.2 safety deletions

Disposition: **CLOSED_IN_V04_BY_RESTORE_OR_EXPLICIT_CARRY_FORWARD**.

Restored/carry-forward clauses include:

- Builder concern/write-set, insufficient-authority stop and exact handoff terminal;
- Reviewer actual-subject/evidence inspection, scope/currentness/forbidden-behavior verification and severity findings;
- explicit phase transition;
- independence-dimension distinction beyond `session_ref`;
- fresh-only/non-transferable evidence;
- recurrence-audit requester/prevention points;
- non-goal excluding full release ceremony where Release authority positively declares non-applicability;
- exact binding sets frozen in L2/implementation.

## F12 — P3 — #680 entry-criteria quantification

Disposition: **PARTIAL_EVIDENCE_GAP_EXPLICITLY_BOUND_TO_RELEASE_DOGFOOD**.

No metrics are invented. L1 now records amplification quantification as `PARTIAL`, economic benefit as `NOT_MEASURED`, and requires §16 downstream baseline measurement to collect execution objects, dispatches, gates, rebind/revalidation events and decision-value accounting. This is nonblocking for Product Freeze but remains a Release evidence obligation for generality claims.

## Environment / independence disclosure from #702

#702 executed in Claude Code Desktop rather than the Issue target Claude Web and disclosed that deviation. The review was READ-ONLY and currentness-bound. Its findings are retained as adversarial Product evidence. The same GitHub account cannot by itself prove principal independence; successor review must explicitly report the independence dimensions actually satisfied.

## Controller conclusion

```text
V49_CLAUDE_FINDING_DISPOSITION=COMPLETE
PREDECESSOR_PRD=v0.3
SUCCESSOR_PRD=v0.4
CLAUDE_REVIEW=#702@5966353271
F1=CLOSED_IN_V04
F2=CLOSED_IN_V04
F3=CLOSED_IN_V04
F4=CLOSED_IN_V04
F5=CLOSED_IN_V04
F6=CLOSED_IN_V04
F7=CLOSED_IN_V04
F8=CLOSED_IN_V04_PRODUCT_DECISION
F9=CLOSED_IN_V04
F10=CLOSED_IN_V04
F11=CLOSED_IN_V04
F12=PARTIAL_EVIDENCE_GAP_BOUND_TO_RELEASE_DOGFOOD
PRODUCT_FREEZE=NO
SUCCESSOR_REVIEW=REQUIRED
NEXT=FRESH_V04_PRODUCT_REVIEW
```
