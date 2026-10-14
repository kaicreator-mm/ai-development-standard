# ADS v4.12.0 PRD — R1 Same-Author Adversarial Review

> **VERDICT: NEEDS_TARGETED_REVISION BEFORE PRODUCT FREEZE.** This is a deliberately adversarial **same-author static** review of the PRD, NOT a Fresh/Independent Product Review and not a machine implementation test. It is the **first** of the user's requested three review perspectives: (1) self-opposition, (2) separate adversarial ChatGPT conversation, (3) Claude. This report is the finding record, not a PRD amendment or a Product authority decision.

## 1. Locked reviewed subject / read-only method

```ini
REPO=kaicreator-mm/ai-development-standard
PR=1101
BRANCH=planning/v4.12-cross-stage-contracts-20261014
PRD=docs/product/PRD-v4.12.0-review-candidate.md
PRD_LAST_CONTENT_COMMIT=f7e6e234697fdba7eed5e43094e48af0d3e81be0
PRD_BLOB_SHA=f46ae82a6a77dbd2213298931a09300a7b83cbc4
SOURCE_OWNER_PIN=version/v4.11.0
REVIEW_OPERATOR_CLASS=SAME_AUTHOR_CHATGPT_WEB
REVIEW_INDEPENDENT=NO
PRODUCT_FREEZE=NO
L2=NO
MACHINE_CONFORMANCE=NOT_RUN
```

Inspected full PRD R1 168 lines and pinned v4.11 `DEVELOPMENT_WORKFLOW` Stage 1/2, `GITHUB_WORK_ITEM_CONTRACT_STANDARD` §§2–3/12.1, `GITHUB_AGENT_INTERACTION_PROTOCOL` independent reviewer/event roles, `ASSURANCE_PLAN_STANDARD`, `PROJECT_ADOPTION` A0–A4/immutable pin, and prior supporting v4.12 product v0.1/scope documents. Adjacent project precedents already pinned in intake: app8 #92/#97/#98, shun-assistant #10/#11, domain-harness #999/#1013/#1023, runx #318/#355, xDownload #101/#103. **The precedents were read as historic issue/evidence claims, not re-executed tests.**

**Testing strategy:** try to prove that the same English/Chinese requirements can authorize incompatible outcomes, self-certify a false PASS, change a frozen owner, accidentally demand all optional work, or make a new project impossible to bootstrap. Any such failure must have a specific PRD location, plausible counterexample, and bounded smallest remedy. Preserve this exact PRD blob for the next reviewers; do not silently revise it mid-chain.

## 2. Material findings (five P1)

### P1-F01 — Scaffold **file creation** vs executable **side effects** is not fully distinguished

**Subject:** PRD §5 FR-03 items 1–3, AC-03 (lines 67–78). `NEW_PROJECT_INIT` includes lockfile/build/test/CI manifests, generator output and minimal executable glue. The Product decision correctly says creating a new project does **not** need a special human Bootstrap gate, but the present prohibition on “irreversible external effects” leaves an operational hole: a scaffolding generator, package manager `postinstall`, CI workflow, schema `codegen` plugin or setup script can execute unbounded code/network/credentials even when the resulting file paths all satisfy scaffold scope.

**Attack:** A planner legitimately creates `package.json` with an `install` hook; another Agent runs install as presumed harmless planning preflight; it posts tokens/calls cloud API. A folder-only guard would have accepted both. Conversely a legitimate local `tsc` smoke is treated as forbidden Feature execution because “some code ran.”

**Required minimum Product repair:** explicitly separate `ARTIFACT_CREATION` (new files within planning scope) from `COMMAND_EXECUTION / EXTERNAL_EFFECT` (actual run, side effects, network, credential or irreversible operations). Allow deterministic harmless declared local build/contract smoke under eligible environment; apply existing tool/rights/side-effect authority to executed generators, installers and untrusted hooks, with explicit provenance, permission and fail-closed behavior for unknown effects. **No extra general human Gate**. L2 implements command classification/preflight using current owners.

**Freeze disposition:** `P1_REVISION_NEEDED`. No evidence of actual exploit in existing ADS; this is a missing PRD boundary.

### P1-F02 — Public architecture contract can drift silently during Scaffold↔DAG co-evolution

**Subject:** §5 FR-03 (lines 69–76) and §6 FR-04 line 85, §7 FR-05 line 96.

**Attack:** L2 has frozen one public capability ABI/error semantic. Planning Agent progressively enriches the same file using a different but type-correct signature that simplifies Task decomposition. Source and DAG agree with **each other**, so the paired Freeze passes, but both disagree with the **Frozen L2** or Product promise. L2 Freeze becomes de facto edit-authorized by planning owner.

**Required minimum Product repair:** pair validity is a **3-way** semantic acceptance: `Frozen Product/L2 invariant ↔ accepted Scaffold public contract ↔ Draft Task DAG acceptance/consumer map`. Structural or private-seam elaboration may evolve without L2 amendment; **any material public API/Trust/Error/ABI or product behavior departure** must be routed to its existing Product/L2 owner *before* it can appear in an accepted SF/DF Freeze. Semantic compatibility is not proven merely by compilation or same-name anchors.

**Freeze disposition:** `P1_REVISION_NEEDED` (close with one invariant and one negative counterexample; no new Architecture gate).

### P1-F03 — The paired SHA/checkpoint and generated index can be self-referential or spuriously stale

**Subject:** §5 FR-03 item 5 (line 75), §6 FR-04 items 2–4 & AC-04 (lines 82–88), §12 point 3 (line 136). `byte-identical output`, `committed inputs`, `scaffold subtree/tree`, and `DAG checkpoint` are individually sensible but lack a freeze-time self-reference exclusion.

**Attack A:** generated index embeds the “final Git HEAD” including itself; updating generated output shifts SHA forever. **Attack B:** accepted scaffold source ref at HEAD X, then DAG-doc-only Freeze commit Y moves HEAD; validator either rejects valid unchanged scaffold, or ignores a changed root manifest/CI file outside a narrow `src/` subtree. **Attack C:** index copied from another branch happens to match Task names but was generated from wrong L2.

**Required minimum Product repair:** require a **cycle-free immutable freeze tuple** with accepted input object IDs/hash scopes and an explicitly excluded **generated output/checkpoint record from its own digest**. Normalize a versioned *material scaffold scope* (incl. build/test/manifests/dependency lock/critical config where applicable), not a naive fixed source-only directory. A docs-only commit does not invalidate unchanged material scaffold tree, but actual covered source/manifest drift must. L2 chooses representation; Product must require non-self-authorizing freeze and tests.

**Freeze disposition:** `P1_REVISION_NEEDED`; algorithm design L2-owned, negative test required.

### P1-F04 — Structural integration smoke is conflated with post-implementation user-path proof

**Subject:** §6 FR-04 V09/AC-04 (lines 85–88), §7 FR-05 item 2, AC-05 (lines 93,99), §10 cases (line 123).

**Attack:** Before implementation, a structural composition entrypoint exists with `NOT_IMPLEMENTED` adapters; paired mapping/contract smoke sees all declared modules and a test entrance. Acceptance language “real integration entrance” or “shared integration entrance verified” is interpreted as “installed feature truly reaches the user.” Alternatively an L2 planner tries to fully implement user interaction solely to satisfy pre-DAG Scaffold Freeze, violating the prohibition on feature implementation.

**Required minimum Product repair:** mark **two distinct predicates**:
- `SCAFFOLD_STRUCTURE_WIRED`: build/import/contract registration and declared entrypoint with truthful unimplemented behavior; sufficient for paired planning Freeze if underlying L2 contract consistent.
- `FEATURE_USER_PATH_REACHABLE`: real installed Core/CLI/UI/external feature behavior and negative proof; **only post-implementation integration/release** can claim it, on exact subject.
An intentionally unimplemented stub must be visibly failing/flagged (not a success-returning fake), never promote `SCAFFOLD_STRUCTURE_WIRED` to product behavior PASS.

**Freeze disposition:** `P1_REVISION_NEEDED`. This preserves the useful runx/xDownload integration lessons without forcing premature Feature construction.

### P1-F05 — A0/A1 manual adoption versus mandatory deterministic mapping execution needs a precise floor

**Subject:** §2.1 P0, §6 FR-04/AC-04, §10 first two bullets (lines 38–46, 80–88, 117–121). Existing `PROJECT_ADOPTION` A0/A1 intentionally does not require adoption of machine contracts/reducers. Yet PRD calls a deterministic mapping generator/checker a **P0 minimum** for v4.12 and says A0/A1 manual path “must be legal.”

**Attack:** A mature A0 project upgrades its pinned ADS standard but runs only manual GitHub Tasks. It records exact anchored links and source hashes correctly without installing a generator script. It is incorrectly classified nonconformant and forced to upgrade to A2. Or a team manually edits a “generated” map and claims equivalent deterministic V01–V12 proof without executing any tool.

**Required minimum Product repair:** distinguish **standard implementation deliverable** (a deterministic reference generator/checker and fixtures MUST exist and be tested in ADS's v4.12 implementation) from **downstream project adoption** (A0/A1 may use canonical GitHub links and manually checked source/Task mapping, with honest evidence limitations and no invented machine PASS; A2+ machine-claims need actual script/schema verification when those records are adopted). The material owner/currentness/public-contract truth floor is equal across profiles, **evidence collection mechanism** may differ, and an A0 cannot assert a machine test succeeded.

**Freeze disposition:** `P1_REVISION_NEEDED`. No new adoption level.

## 3. Secondary findings / improvement guidance (four P2)

### P2-F06 — FR-06/07 have broad outputs but thin minimum measurable release acceptance
**Subject:** PRD §8–9 (lines 101–115), §2.1 P1. “Steward reports stall / actor unblocks” presumes eligible actor and actual ready event; Environment cleanup outcomes and Task Learning provenance acceptance are less explicit. **Bounded resolution**: define a minimal observable reference case per existing owner (e.g. fabricated READY is rejected; eligible controller action + readback; real env cleanup success/failure logged; Task Learning `UNKNOWN` not projected to PROVEN), while keeping richer automation deferred. Do not require new agents/services.

### P2-F07 — Product metrics and improvement economics lack an honest comparison basis
**Subject:** §1 (lines 16–24), §9 (line 113). Claims “reduce conflict/rework” and “minimum cost” are aspirations; no actual baseline or counterfactual. **Bounded resolution**: require actual `baseline = observed|UNKNOWN`, compare only per eligible case with matched subject/constraints, report true cost/rework/uncertainty; **no fixed numeric ROI threshold** or new benchmark campaign. Launch conformance focuses on *working mechanism and no-regressions*; efficiency improvements may be post-release learning.

### P2-F08 — Source reuse / helper extraction Builder and Reviewer behavior not fully operational
**Subject:** §7 FR-05 (line 92). Favoring reuse is a preference rather than an actionable quality contract; Agent may endlessly create abstractions or fail to reuse tested helpers. **Bounded resolution**: Task Builder checks existing helpers/contracts/functions before writing; extracts only if semantic duplication/maintainability is demonstrable, respecting atomic owner and tests; Reviewer flags true duplicated logic, harmful abstraction, failed reuse, or write-scope creep **without automatically creating refactor Issues**. This can be a lightweight existing role guideline, not a new gate.

### P2-F09 — Normative owner placement and source precedence among five large reference files remain hard to audit
**Subject:** §1 provenance (lines 5–8), §12 (lines 131–142). PRD points to evolving C01–C15 drafts (which include historical superseded C15 R0 records). An implementer may quote an older review's `BOOTSTRAP_PRE_DAG_AUTHORITY=P0_OPEN` against the later owner-approved Product direction. **Bounded resolution**: provide **one explicit precedence sentence**: current reviewed/frozen PRD > specific adopted v0.1 decisions > active non-normative C01–C15 draft *within its current clause* > historical red-team record for provenance only, always subordinate to applicable pinned normative source until prospective release. Use “superseded” index, not rewriting old audit history.

## 4. Counterexamples that **passed** bounded semantic inspection

- **NF01:** `DAG-P / DAG-A / DAG-I` are not L1/L2/L3 themselves and optional planning views do not automatically create native Issue Dependencies (FR-01).
- **NF02:** `HIGH_ASSURANCE` is evidence depth, not a contract-mutating authority; Product/Architecture amendments remain separate (FR-02/05).
- **NF03:** Source/module import != GitHub `blocked_by` and free-standing advisory Issue != canonical Merge blocker.
- **NF04:** AI majority neither manufactures independently human-authored blind Gold nor overrides genuine human DENY; public complaints cannot prove actual cohort prevalence.
- **NF05:** `PR PASS != VERSION RELEASE PASS`, skipped/unknown real E3/Hidden is not green.
- **NF06:** User's prospective new-project Scaffold creation scope is acknowledged without adding a universal extra human gate; current v4.11 pinned projects are not retroactively altered.
- **NF07:** Existing project source/layout/usable evidence can be reused instead of an all-project scaffold regeneration.
- **NF08:** One coherent Task concern is not forced into one method/interface/file; shared integration owner and actual native DAG mutation preserved.
- **NF09:** No compulsory always-on Steward/independent graph database or all-three-DAG research program was added.
- **NF10:** Past user/project issue cases are acknowledged as **reference evidence**, not pretended v4.12 real conformance.

These bounded passes are **author-led thought probes**, NOT machine test PASS, external independent reviewer agreement or release evidence.

## 5. Minimal proposed R2 repair package — **do not edit R1 before other reviews**

If the next reviews corroborate, make **one bounded PRD R2 textual repair** on the **same PR #1101**, addressing F01–F05 with AC-negative additions (no separate Issue per finding) and F06–F09 if materially valuable. Preserve this R1 PRD blob and the independent reviewers' exact-subject results for comparison. Add no new required human Reviewer beyond current normative Stage1 independent Product Review.

**Suggested actual PRD changes (minimal):**
1. §5 FR-03 add scoped `ARTIFACT_CREATION != EXECUTED_EFFECT`; stage-sensitive generator/install hooks.
2. §5/§6 add **3-way** L2/Product ↔ SF ↔ DF public semantic alignment and **cycle-free** material source/DF/map tuple.
3. §6–7 explicitly split `STRUCTURAL_WIRING_READY` from later `REAL_FEATURE_ENTRYPOINT_WORKING`.
4. §10 separate **ADS-standard generator conformance** from **A0/A1 human/manual use**, keep same truth floor.
5. §12 exact owner and precedence, optional concise Builder/reviewer reuse & Steward minimum negative.

## 6. Independent review sequence / stable exact-subject handoff

**External review instructions** (give to fresh adversarial ChatGPT session before disclosing this self-review, to reduce anchoring):

```text
执行 kaicreator-mm/ai-development-standard 的 v4.12 PRD R1 盲式独立对抗审核。
审核 EXACT SUBJECT：
docs/product/PRD-v4.12.0-review-candidate.md
Git blob SHA f46ae82a6a77dbd2213298931a09300a7b83cbc4
PR #1101（规划分支 planning/v4.12-cross-stage-contracts-20261014）。
首先独立读取此 PRD、version/v4.11.0 的权威工作流、Task/Claim/Review/Project Adoption/Release owner，并用 domain-harness/runx/app8/xDownload/shun-assistant 的真实 GitHub 证据找可证伪反例。
不要先读 V412_PRD_ADVERSARIAL_R1_SELF_REVIEW.md，也不要继承之前作者的 PASS。
优先质疑：Scaffold 规划写入与真实执行副作用；L2 公共契约是否被无声改写；paired Freeze exact SHA/树/索引循环；Stub 与真正入口；A0/A1 与 P0 自动映射；Task/Owner/Review/Release 权威；实际 ROI 与无止境验证。
输出每项 {severity, 位置, 严格反例, 可复现或精确 source ref, 最小修复, 是否 Product Freeze blocker}，并输出最终 FREEZE_READY YES/NO。
仅只读审核；不改 PRD、不合并、不直接 Product Freeze。
```

**Claude** should run against **the same exact PRD R1 blob** initially, with no self-/independent-review findings in context (ideally). Then compare its new findings with ChatGPT independent reviewer and this report, deduplicate by underlying failure predicate, settle one R2 and only then request one final source-bound independent Product review/authorization according to actual Stage1 policy. No fictional extra review gate and no endless R-round process.

## 7. Status

```ini
R1_SELF_ADVERSARIAL=COMPLETE_STATIC
MATERIAL_FINDINGS_P1=5
IMPROVEMENT_FINDINGS_P2=4
P0_CONFIRMED=0
PRODUCT_SCOPE_DIRECTION=RETAIN
RECOMMENDATION=NEEDS_TARGETED_REVISION
PRD_R1_EDITED_BY_THIS_REVIEW=NO
EXTERNAL_ADVERSARIAL_CHATGPT=NOT_RUN
CLAUDE_REVIEW=NOT_RUN
FRESH_INDEPENDENT_PRODUCT_REVIEW=NOT_RUN
PRODUCT_FREEZE=NO
IMPLEMENTATION_CONFORMANCE=NOT_RUN
```
