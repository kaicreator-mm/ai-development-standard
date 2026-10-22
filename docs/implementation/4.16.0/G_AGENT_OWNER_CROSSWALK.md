# ADS v4.16 T06 — Agent selection and delegated Effect owner crosswalk

**Status:** SOURCE-ONLY IMPLEMENTATION CANDIDATE for [Task #1270](https://github.com/kaicreator-mm/ai-development-standard/issues/1270), not an independently accepted normative amendment. **Frozen scope:** Product #1261@6338348925; L2 #1261@6338359775; Task DAG #1261@6338768231 and exact blob `2bbfc230bf7a732957ea9b1d605cf434892b062c`. **Source baseline:** `version/v4.16@6d147eac6c86eff620d3695a46ccbb3be452debb`. T06 Builder source review remains required. Inherited P2-G03 is not closed by authoring this document.

## 1. Existing authority and precise gap decision

| Concern / identity | Exact existing normative owner at baseline | Disposition | Consequence |
| --- | --- | --- | --- |
| Parent responsibility, subwork versus transfer, one active owner and causal record | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §§28.1–28.2, blob `1f1601a20db08d263955241607dfd08d8b8f77e1` | **ALREADY_DEFINED** | Child result/evidence is not a responsibility transfer; parent Dispatch/Claim remains source |
| Child right attenuation and protected key through delegations | same source §§28.3, 28.5 | **ALREADY_DEFINED** | child authority is intersection of delegator, current Task, role, external authorization; no extra group/second claim |
| External effect authority refresh before irreversible mutation | `standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` §10 and §21.1, blob `3f7189301f7292200a98ebd027372513a801bc03` | **ALREADY_DEFINED** | current decision, subject/tenant, Claim and `effect_id/attempt_id` must be rechecked at sink boundary |
| Provider ACK loss, physical effect identity, retry, reconciliation | same source §§21.2–21.3 | **ALREADY_DEFINED** | lost ACK ⇒ `EFFECT_OUTCOME_UNKNOWN` / HOLD; no blind non-idempotent replay, late callback not parent success |
| Typed Dispatch/Claim and transport-vs-logical actor provenance | `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` §§5, 7, 8.4.1–8.5, blob `67516c36f4d202123224b1c2054419aa913b872d`; `schemas/dispatch.schema.json` blob `90bea62524beb0215d5f40cf0be9986786648fec` | **ALREADY_DEFINED** | Dispatch ACK/RUNNING/DONE is not a provider effect receipt or independent verifier Gate |
| Chosen effective per-Task Capability Profile revision and evidence witness, separately source-pinned from Role Profile, Tool/Host/Task/Claim | v1 Capability Profile/Evidence and Role Execution Profile plus `EXECUTION_ARCHITECTURE_STANDARD.md` §27 hard filters and `GITHUB_AGENT_INTERACTION_PROTOCOL.md` §8; exact Task/Pack currentness | **NEEDS_CLARIFICATION (audit-only optional projection)** | If an actual accepted selection cannot be reconstructed from existing refs, use one *optional* source-qualified Task/Pack/Dispatch reference and define old-reader behavior via compatibility owner. Absence in historical v1 is not malformed identity, but current selection-dependent facts remain UNKNOWN |
| Real Tally Agent scheduler, tool invocation, Host/provider effect receipt, DomainHarness Kernel and tenant authorization implementation | owning runtime/project, not ADS | **IMPLEMENTATION_ONLY** | no ADS Agent registry, Tool RPC, external Effect engine or new mandatory v1 machine field |

**P2-G03 decision:** The originally omitted §28 and External §§10/21 are acknowledged as existing normative owners. Only the optional *cross-owner source reference example* above may remain a bounded G1 clarification; G2 delegation/effect semantics are already defined. No new required field, second Event family or source standard edit is justified by these examples. This source crosswalk is evidence for a later independent owner disposition, not unilateral closure of the carried Reviewer finding.

## 2. Source-bound accepted path (G09)

1. Resolve an exact accepted Task/Pack and source-qualified candidate selection; retain immutable declared Capability Profile revision, Evidence v1 observation origin and Role execution constraints. Capability **claims** and historical observations do not grant live Host/Tool access.
2. Before Claim/Dispatch, recheck current Task, accepted serialized Claim/generation, actual Tool/Host ability and *independent* project/external permission; role and declared task writeset bound one protected key. A child receives only rights in the actual intersection, not a renamed grant.
3. Child Dispatch references causal parent, mode and exact work identity. Host or DomainHarness K independently owns real effect permission, `effect_id` and physical `attempt_id`; transport ACK or agent text is not successful business mutation.
4. Authoritative provider/sink receipt must bind the same real effect and tenant. Lost response, cancellation request without independently witnessed cancellation, conflicting owner/late ACK or provider outage is HOLD/UNKNOWN for effect truth; do not blindly retry.
5. Only independently source-qualified verifier and actual native GitHub readback support strict Task/Gate evidence. Later Task Learning may consume the result but cannot self-activate Package, reassign rights or amend a frozen standard.

## 3. Compatibility / refusal matrix (A03, G10–G12)

| Scenario | Required bounded interpretation |
| --- | --- |
| selected profile revision stale or live Tool permission UNKNOWN | reject current selection/Claim or HOLD; no ranking promotion from Capability Evidence |
| child requests permissions outside parent/Task/Role/external intersection | refuse Tool/effect; absence of actual denial witness is not a historical success |
| same protected Task key has incompatible accepted Claim | refuse second admission; do not derive parallel authority from child/operator/model name |
| dispatch reports DONE but sink receipt absent / ACK lost | effect outcome UNKNOWN, no strict completion or blind retry |
| cancellation **requested**, late success ACK arrives | reconcile actual provider state separately; do not retroactively transform cancellation or Gate |
| exact verifier is PASS but GitHub publication/readback absent | strict evidence publication **NOT PROVEN** |
| older v1 Profile/Dispatch without optional selection ref | historical object remains readable; no backfill, no new mandatory v1 field and no automatic grant |

The fixture oracle in `scripts/test_v416_t06_agent_governance.py` and `tests/fixtures/v416/t06/scenarios.json` implements **deterministic source-contract examples only**. It does not exercise the real Tally scheduler, DomainHarness K, provider, GitHub CAS admission or external irreversible sink. Positive and negative classifications are illustrative test oracles, not new ADS canonical workflow states.

## 4. Tests, limitations and independent handoff

Run `python scripts/test_v416_t06_agent_governance.py` on an actual checkout of this PR HEAD; required generic workflow CI, exact-source independent Review and issue-native completion checks remain separately applicable. A03 / G09–G12 are covered as example classes; real current Host/Tool, provider receipts, exact Task/Claim readbacks, and end-to-end interoperability #1210/#1231 remain `NOT_RUN`. Never turn source-only example PASS into provider/Kernel/Task Gate PASS. T06's inherited P2-G03 must be closed by the proper owner **after** source review/validation evidence, not by this Builder.
