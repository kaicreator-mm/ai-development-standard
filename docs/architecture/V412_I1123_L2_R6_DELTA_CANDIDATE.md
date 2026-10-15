# ADS v4.12 — #1123 L2 R6 Scoped Identity/Authority Architecture Delta Candidate

> **STATE: AUTHOR-SIDE ARCHITECTURE DELTA, NOT FROZEN.** Bounded successor based on user-authorized #1123 intake [Product R4 Delta Candidate](../product/V412_I1123_PRODUCT_R4_DELTA_CANDIDATE.md) exact blob `847e707b78359f6e9de2901b2ea049557b7eb104`, and separately Frozen Product R3/L2 R5. Does not change old frozen Git objects, existing runtime/Claim/Gate authority or grant a normative implementation branch.

```ini
EVENT=ADS_V412_I1123_L2_R6_AUTHOR_SCOPED_DELTA
USER_SCOPE_AUTHORIZATION=CURRENT_CHAT_2026_10_15
CHANGE_SOURCE_BLOB=6d783ecb8b02a61d4e2d60174e1a12832f27b948
PRODUCT_DELTA_CANDIDATE_BLOB=847e707b78359f6e9de2901b2ea049557b7eb104
PRODUCT_R3_FROZEN_BLOB=0bfbf782c8859e79df52c9b57904ad80bcd718e9
L2_R5_FROZEN_BLOB=68608ef6456334d627db1797ba2e023233c84ce7
DAG_R3_FROZEN_BLOB=adc9e522f3b734a59898091945b9c7545530565a
V411_REUSE_INTERACTION_BLOB=b3f1191b2ee0c469e9b425d2336d4adbc47d6ede
V411_REUSE_RELEASE_BLOB=da82aa7d387d8f190c4ddff88b4c8782af804ac4
ARCHITECTURE_APPROVAL=NOT_RECORDED
INDEPENDENT_SOURCE_REVIEW=NOT_RUN
EXTRA_SERVICE=NONE
EXTRA_TASK=NONE
EXTRA_GATE=NONE
```

## 1. Architecture change boundary

Preserve **one GitHub durable facts plane** + versioned standard source, no second Agent identity service, Account registry, Owner-signature workflow, permission database, Release engine or event state machine. The adopted v4.11 #1122 rules in Interaction §5/§7/§8.1.1 and Release §11.7 already handle self-declared logical operators and ADS-only Release process. For the remaining #1123 predicates, amend *existing* rules by their proper source owners after actual source-first gap analysis.

### A. Identity attribution vs real authorization/evidence

| Distinction | Trusted source for ADS standard execution | Verifiable technical predicate | Forbidden inference |
|---|---|---|---|
| Logical executing identity | Executor-declared `actor_role`, `operator_kind`, `operator_id`, `session_ref`; optional delegation | Canonical event emitted/admitted for a current Task; fields present; no stale/contradictory actual state | GitHub `user.login` confirms/denies Agent role or independence |
| Builder/Reviewer independence | Distinct **declared** logical operator/session contexts, including same GitHub writer | Actual required Review result on current exact PR SHA and findings resolved | Separate real-world Session authentication or Owner credential proof |
| Task/Claim | Canonical live Work Item + accepted dispatch/Claim | Single writer/CAS generation, Allowed/Forbidden write set, native dependencies, current source; conflict rejects | Declaration grants unilateral concurrent write permission or auto-PASS |
| Assurance | Current semantic rule revision / required per-gate proof, not human Owner login | Eligibility of any reduced gate/assurance floor is based on actual proof and source-current rule | Deleting `CURRENT_OWNER_AUTHORITY` wholesale waives required proof |
| ADS standard Release | Existing standards-only §11.7 actor role declaration | Exact candidate, executed required test/gates, Hidden/Release proof when applicable, honest NOT_PROVEN | A named Owner signature required merely for identity; Agent says `PASS` so Release passes |
| Consumer real effects | Project-specific platform/consent/privilege evidence, per actually applicable policy | Real authorization/API permission, consent and observed effects/deny | Self-declared logical `human` automatically certifies real human consent |
| GitHub native PR approval | Actual GitHub branch-protection/ruleset state | GitHub-accepted approval if the repository mandates it | ADS text comment bypasses GitHub author self-approval limitation |

The term `owner` in `standard-manifest.json#semantic_authorities`, `ASSURANCE_PLAN_STANDARD` §§9–10 or contract binding can mean **the normative source controlling a predicate**. This is not an Agent credential test. Keep meaningful rule/precondition traceability; remove only authentication of the actor behind a *self-declared role* and unnecessary second Owner signatures. The successor cannot blindly downgrade `required` or replace a real-effect proof with simulated text.

## 2. Source owner mapping (existing S01–S05 concerns)

| Concern | Files eligible **only after explicit DAG/write-set successor** | Scope | Non-overlap |
|---|---|---|---|
| **S01** — stage + logical Claim/operator contract | Currently owned `standards/DEVELOPMENT_WORKFLOW.md`, `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` **plus proposed** `standards/EXECUTION_ARCHITECTURE_STANDARD.md`, `AGENTS.md`, `prompts/independent-review-bootstrap.md` | Only proven remaining identity/credential/admission contradictions, not a new Claim or Review machine; trust declarations exactly per #1122 | S05 does not write these normative files |
| **S02** — single Scaffold/DAG binding | Existing Task DAG governance/template unchanged | No #1123 diff unless new material structural contract proves otherwise | S01/S03 unchanged semantics |
| **S03** — reference deterministic checker | Existing reference checker only | Real Git object material identity and scope testing remains source truth; no Agent credential verification | Never edits identity/Release standards |
| **S04** — adoption + compatibility | Existing `standards/PROJECT_ADOPTION.md` and scoped templates, prospective guidance referencing existing compatibility standard | Explain declared Agent identity on shared GitHub transport, older immutable consumer pins, **protocol behavior** negotiation when evolving; no automatic rolling adoption | Do not modify `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` without distinct exact source owner amendment |
| **S05** — shared conformance integration | Existing manifest, `scripts/verify_standard.py`, Golden index, CI; **proposed** `standards/ASSURANCE_PLAN_STANDARD.md`, `standards/RELEASE_STANDARD.md`, affected `schemas/**`, existing focused `scripts/test_*` where explicitly allocated | Credential/Owner identity vs semantic assurance-release separation; reusing #1122 source; test positive/negative cases and conformance; release policy changes require existing release authority consistency | S06 performs actual `type:release` qualification, not Builder source implementation |

**Write-set amendment required:** Frozen R3 Task DAG does **not** presently grant the proposed S01/S05 additional source paths, and S05's release-standard source semantics are release-critical. New DAG successor must name exact file/section ownership and no concurrent effective writers. These are proposed planning allocations; **not implementation-source write permission now**.

## 3. Technical assurance preservation / failure mapping

Do NOT reinterpret `CURRENT_OWNER_AUTHORITY` as 'authenticated GitHub person' if its source means actual current normative Gate policy. The safe classification algorithm for each cited suspected Owner or actor predicate is:

1. Locate exact current normative source clause + schema/checker consumer + protected subject/pin.
2. Classify `ACTOR_IDENTITY_OR_CREDENTIAL` vs `SEMANTIC_AUTHORITY_APPLICABILITY` vs `OBJECTIVE_EXECUTION_OR_EFFECT` vs `UNKNOWN`. No new public schema enum required; these are analysis categories.
3. Identity credentials for normal ADS process are removed or made irrelevant when already covered by v4.11 #1122. Semantic/technical predicates remain current and evidence-backed; `UNKNOWN` cannot be assumed identity-only.
4. Bind any actual change to one of S01/S04/S05 owners, write focused positive/negative examples, reuse existing impacted checks and the version-candidate single regression. A no-change `ALREADY_SATISFIED` disposition is valid.
5. Do not move a mandatory `REQUIRED_NOW` or past `BLOCKED` verdict to PASS by editing a field: apply the current prospective source rule to its own subject and preserve history.

### Failure vectors / expected decisions

- **L2-ID01:** one shared GitHub login, different admitted **declared** Builder/Reviewer contexts, exact current Review result → logical independence eligible, not authentication blocked.
- **L2-ID02:** two GitHub logins, same declared operator/session → still one logical context; login difference irrelevant.
- **L2-ID03:** correct declared Review role but embedded unadmitted comment, stale SHA or no actual result → technical NOT_RUN/BLOCKED.
- **L2-ID04:** simultaneous claims on one protected key without valid serialization → losing claim DENIED atomically, no duplicate source write.
- **L2-ID05:** absence of real Owner credential with valid current standard source/prior rule and all executed evidence → no identity-only BLOCKED.
- **L2-ID06:** assurance floor needs a real proof and only an operator declaration exists → no assurance reduction; preserve semantically required evidence.
- **L2-ID07:** standards-only synthetic Human DENY truth has not executed real-world action → `NOT_PROVEN`, no pretend production certification.
- **L2-ID08:** no eligible native GitHub approver while ruleset demands one → external GitHub rule still BLOCKED; user/Agent statement not native approval.
- **L2-ID09:** legacy consumer pin with current schema but changed behavior → explicit protocol compatibility decision before prospective adoption.
- **L2-ID10:** prechange frozen historical source FAIL/NOT_RUN survives identity successor; no retroactive sanitization.

## 4. Relative DAG / validation impact

No new concern node, DAG edge, phase, Owner signature or universal human audit is justified merely by this change. Reuse **S01, S04, S05**, with S02/S03 source input and S06 actual Release role unchanged. S01/S04 are parallel after lawful admission; S05 remains after S03 and S04. The already frozen Stage2.4 graph remains historical, and a separate successor must describe material **write-set extension only**, preserving original four internal dependency edges.

Technical implementation should be a few focused changes on actual eligible source, rather than a blind v4.13 draft PR cherry-pick. The actual v4.11 #1122 amendment and test evidence is reusable for identical predicates and source pins, but not a claim that v4.12 conformance ran. A0/A1 static manual currentness and A2+ real-run evidence still follow established validation owners.

## 5. Authority and freeze path

The user approved **adding this concern to v4.12** from #1123 and deriving targeted successor artifacts. That does not freeze the new Product R4 text or this newly created L2 R6 text, and is not permission to mutate the old frozen R3/R5/DAG blobs. A properly sourced Product delta review/Freeze → scoped L2 disposition/Freeze → exact Task DAG write-set amendment/Freeze is required **before accepting an expanded Task Pack for native source work**. Do not demand re-review of unchanged R3/R5 sections merely for ceremony. The implementation lineage must still use actual v4.11 Release-qualified predecessor and real Task/Claim; as checked 2026-10-15 V01/V02 closed, V03/V04/R01/R02 open.

```ini
L2_DELTA_AUTHOR_PREPARED=YES
L2_DELTA_FREEZE=NOT_RECORDED
PRODUCT_DELTA_FREEZE=NOT_RECORDED
DAG_WRITESET_AMENDMENT_FREEZE=NOT_RECORDED
IMPLEMENTATION=NOT_ADMITTED
```
