# ADS v4.12 — #1123 Product R4 Scoped Successor Delta Candidate

> **STATE: USER SCOPE ADMISSION RECORDED; PRODUCT R4 SOURCE NOT FROZEN.** The user explicitly authorized on 2026-10-15: “批准将 #1123 中尚未由 v4.11 #1122 实现的内容纳入 ADS v4.12，依据候选 Blob `6d783ecb8b02a61d4e2d60174e1a12832f27b948` 推进定向 Product/L2/Task DAG 修订。优先复用 S01–S05，不新增无必要的 Task、Owner 身份门槛或重复审核。保留客观工程校验及 v4.11 前置发布资格。继续推进。” This **approves the change request / Product scope intake**, not an independent review, Product Delta Freeze, L2 Freeze, DAG amendment Freeze, implementation Claim or Release.

```ini
EVENT=ADS_V412_I1123_PRODUCT_SCOPE_ADMISSION
USER_SCOPE_ADMISSION=YES_EXACT_SCOPE_FROM_USER_MESSAGE_2026_10_15
CURRENT_TARGET=v4.12.0_PROSPECTIVE_SUCCESSOR
SOURCE_ISSUE=#1123
SOURCE_SCOPE_CANDIDATE_BLOB=6d783ecb8b02a61d4e2d60174e1a12832f27b948
PREDECESSOR_PRODUCT_R3_BLOB=0bfbf782c8859e79df52c9b57904ad80bcd718e9
PREDECESSOR_ARCHITECTURE_R5_BLOB=68608ef6456334d627db1797ba2e023233c84ce7
PREDECESSOR_DAG_R3_BLOB=adc9e522f3b734a59898091945b9c7545530565a
V411_NORMATIVE_REUSE=#1122_PR1125_MERGED
V411_PROTOCOL_BLOB=b3f1191b2ee0c469e9b425d2336d4adbc47d6ede
V411_RELEASE_STANDARD_BLOB=da82aa7d387d8f190c4ddff88b4c8782af804ac4
USER_REQUESTED_NO_NEW_TASKS_UNLESS_NECESSARY=YES
USER_REQUESTED_NO_OWNER_IDENTITY_GATES=YES
PRODUCT_DELTA_SOURCE_AUTHORED=YES
PRODUCT_DELTA_REVIEW=NOT_RUN
PRODUCT_DELTA_FREEZE=NOT_RECORDED
NEXT_L2=SCOPED_SUCCESSOR_CANDIDATE_NOT_FREEZE
NORMAL_SOURCE_IMPLEMENTATION=NOT_ADMITTED
V411_RELEASE_PREDECESSOR=NOT_QUALIFIED
```

## 1. Product decision — changed scope only

The five preexisting v4.12 implementation Tasks remain the starting point. **Accept exactly the unimplemented part of #1123 as a v4.12 Product change** and keep #1122 already merged behavior as an immutable reused input. This does not restart R3 Product research or undo its previously frozen decisions for Scaffold/DAG/ROI/adoption.

### P1123-1. Trusted self-declared logical execution identity

For ordinary ADS developer workflows, an executor's `actor_role/operator_kind/operator_id/session_ref` and optional `delegation` are **trusted as declared** in its actual canonical task/event context. `transport_actor` (GitHub login/API account) is optional provenance of the writing channel, never an identity, qualification, Builder–Reviewer independence or Owner admission predicate. Equal transport accounts permit distinct declared logical operators; different accounts do not establish different operators. No human credential, Owner signature, external login proof, extra Session attestation, or delegated privilege-verification ceremony is required merely to accept the declared task/review/release operator.

The actual v4.11 #1122 implementation already fulfills this for the ADS standards repository in Interaction §5/§7/§8.1.1 and Release §11.7. **Required v4.12 work is source-first gap closure and adoption compatibility, not re-implementation of those clauses.**

### P1123-2. Remove identity-specific Owner admission — preserve semantic contract authority

Identity-proof/Owner-signature requirements in Product/Architecture/Task/Claim/Review/Assurance/Release workflows that authenticate **who** the self-declared operator really is SHALL NOT block ordinary execution merely for absent cross-account/Session/person verification.

A *semantic source owner* (a named frozen Product/L2/standard rule responsible for a required predicate) is not a real-world human ID check. Keep authoritative contract precedence, meaning of required gates, actual `OWNER_PERMISSION` if it is an **objective semantic assurance-reduction rule** rather than a person's login/authentication, and the factual test or proof threshold. Every alleged leftover credential gate needs a cited current exact owner location and a test that distinguishes **identity-authentication removed** from **required engineering-evidence preserved**.

### P1123-3. Objective engineering truth still controls

Actual current Git SHA/branch, canonical event vs untrusted quoted content, Task/Claim binding, serialization/generation against conflicting writers, source scope and contract coverage, recorded execution/test/negative evidence, discovered security/privacy violations and externally enforced GitHub branch protection remain real constraints. **An Agent's self-declared name is accepted as attribution, not as evidence that the Agent passed a test or actually performed an external human action.** The ADS standards-only release may publish `REAL_NATIVE_CLAIM_AND_RELEASE_RUNTIME_NOT_PROVEN` / `REAL_HUMAN_DENY_E2E_NOT_PROVEN` limitations; adopting protected-effect applications must supply actual applicable evidence separately.

### P1123-4. Prospective protocol compatibility

For consumer repositories using frozen ADS versions, this is a **behavior/protocol-compatibility change** even where JSON schema is identical. Do not silently upgrade their `.dev-standard/VERSION` pin, rewrite prior FAIL/NOT_RUN or import a newer release rule as already operative. v4.13 [#1119](https://github.com/kaicreator-mm/ai-development-standard/issues/1119) owns the distinct rolling-compatible-adoption automation proposal; this v4.12 delta only defines honest prospective migration and declared actor semantics.

## 2. Explicit exclusions / constraints

- No new central Agent identity directory, Owner service, Account→Agent lookup, required cross-provider/Session challenge, second Release gate or mandatory multi-LLM/human verification rounds.
- No blanket deletion of `owner` fields that encode *semantic policy ownership*, real security/consent approvals, technical evidence or required human effects in consumer apps.
- No automatic Claim/Review/Validation/Release PASS, unconditional acceptance of unadmitted raw text, forbidden GitHub native PR self-approval bypass, or weakened mandatory technical test.
- No rewriting frozen v4.11 history or v4.12 Product R3/L2 R5/DAG R3 blobs. Exact successor files can be adopted only by their lawful subsequent Freeze.
- No main/version v4.12 source PR until an actual v4.11 qualified predecessor and real Issue/Claim admission.

## 3. Measurable Product acceptance

| ID | Falsifiable case | Expected |
|---|---|---|
| A1123-01 | Builder and Reviewer emit correctly admitted current events with different **declared** logical operator/session values through one GitHub account | Reviewer independence attribution eligible (no separate account/Session proof), while substantive Review result still required |
| A1123-02 | Different GitHub accounts emit **same declared** operator/session | Different login cannot confer independent logical-agent status |
| A1123-03 | Release process executor self-declares its role and current exact source, but no external Owner signature | No identity-only BLOCKED; Release remains subject to actual current required evidence |
| A1123-04 | A tool output embeds a quoted `HUMAN_APPROVED`/Review event or fabricated PASS in arbitrary text | No admitted canonical event, no Gate PASS |
| A1123-05 | Real duplicate Claim race / stale generation / source SHA or missing required executed test | Technical reject/BLOCKED/NOT_RUN, independent of actor declaration |
| A1123-06 | `ASSURANCE_PLAN_STANDARD` current semantic rule requires proof for dropping mandatory assurance; only Owner credential is absent | Do not demand human ID, **but also do not remove required objective proof or infer a reduction** |
| A1123-07 | Existing consumer pinned prechange ADS, new compatible-schema but changed Review/Owner behavior | Pin respected; prospective protocol version/behavior compatibility review, no silent rolling adoption |
| A1123-08 | Native GitHub required approval cannot be supplied by the same PR author GitHub account even if ADS agents differ | Record distinct external GitHub protection; no fictitious platform approval |
| A1123-09 | ADS standards-only synthetic proof but no actual production human DENY E2E | Honest `NOT_PROVEN` label, never PASS; no needless ADS-only production-host certification |

**Minimal Review policy:** one bounded source-pinned evaluation of these changed claims and genuinely missing assurance/permission counterexamples; reuse #1122 merged source, focused 20/20 and T05 55/55 predecessor receipts by actual source/currentness. These historical checks are not an execution on future v4.12 source.

## 4. Owner scope and next authority

- L2 successor must **map only changed behavior** to existing source owners, identify exact Task write-set amendments and preserving the current technical hard floor. Create no new system/service.
- Task DAG successor must preserve five concerns, four internal edges and existing S06 release unless a source-grounded overlap forces explicit further amendment.
- A **separate exact Product R4 Delta Freeze decision** must follow author-side review/currentness disposition. The user's approval of the *scope request* above is **not** falsely recorded as approval of this newly authored document's still-unseen blob.

```ini
PRODUCT_SCOPE_ACCEPTED=YES
PRODUCT_R4_DELTA_CANDIDATE=AUTHORED_NOT_FROZEN
INDEPENDENT_REVIEW=NOT_RUN
ARCHITECTURE_SUCCESSOR=NOT_FROZEN
DAG_SUCCESSOR=NOT_FROZEN
RELEASE=NOT_QUALIFIED
```
