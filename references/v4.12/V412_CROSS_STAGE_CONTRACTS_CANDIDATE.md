# v4.12 Cross-Stage Execution Contracts — Product/L1 Candidate (R1)

> STATUS: **PROPOSED R1 after author-led adversarial R0, NON-NORMATIVE, NOT FROZEN.** This is a reviewed-issues synthesis plus an author-led draft for L1 Product adoption, **not** operative ADS rules. No version/v4.11.0 source/Task Pack/Release applicability changes. Parent: [#1096](https://github.com/kaicreator-mm/ai-development-standard/issues/1096). Three-DAG intake: [#1100](https://github.com/kaicreator-mm/ai-development-standard/issues/1100). Risk-bounded value: [#1099](https://github.com/kaicreator-mm/ai-development-standard/issues/1099). 

## 0. Authority and construction rules

The contracts below define **candidate cross-owner expectations**, not a new sixth normative owner. Every final MUST/SHOULD needs a reviewed v4.12 PRD acceptance binding and an L2 placement decision into existing normative owners. This R0 cannot dispatch work, authorize gate omission, change Issue Dependencies, thaw Product/L2, mark Validation PASS or merge a PR.

Existing owners to preserve (v4.11 reference branch):
- `DEVELOPMENT_WORKFLOW.md` Stage 1/2 and `L1_PRODUCT_EVIDENCE.md`, `L2_ARCHITECTURE_EVIDENCE.md`: semantic phases, research applicability and Product/L2 freezes;
- `ARCHITECTURE_DESIGN_STANDARD.md`, `ARCHITECTURE_RESEARCH_DEMO_STANDARD.md`: Architecture UNKNOWN, Demo hypothesis/proof/evidence-only promotion;
- `TASK_DECOMPOSITION_STANDARD.md`, `TASK_DAG_GOVERNANCE_STANDARD.md`: implementation DAG authority, Task splits/mutations and native GitHub `blocked_by` once materialized;
- `EXECUTION_ARCHITECTURE_STANDARD.md` §§6,11,14,27–30, `GITHUB_AGENT_INTERACTION_PROTOCOL.md`: canonical dispatch/claim, currentness, merge, human responsibility, learning;
- `ASSURANCE_PLAN_STANDARD.md`, `VALIDATION_STANDARD.md`, `RELEASE_STANDARD.md` §11: assurance currentness, exact-subject execution and release gate × subject applicability;
- `PROJECT_ADOPTION.md`: immutable ADS pin, Fast Path independent of A0–A4 and prospective adoption;
- #931 evidence spine, #775/#1072 Task split, #926 merge-drain, #932 reroute, #803 budget, #1081 L1 convergence, #1092 anti-loop dogfood.

Common prohibitions: `OBSERVATION != AUTHORITY`; `INFORMS != BLOCKED_BY`; `PRODUCT_EVIDENCE_PASS != PRODUCT_FREEZE`; `DEMO_PASS != IMPLEMENTATION_PASS`; `TASK_PASS != RELEASE_PASS`; `OPEN_ADVISORY_ISSUE != GATE_BLOCKER`; `CI_GREEN != UNEXECUTED_TEST_PASS`; `STALE != CURRENT`; `UNKNOWN != NOT_APPLICABLE`. Model/provider identity, agent prose, labels, Issue existence, apparent speed or approximate ROI cannot grant authority.

## C01 — Phase graph identity, applicability and boundaries (W1; P0)

Three **logical phase views** on common provenance; no default requirement for three persisted DAGs:

| View | Phase / one decision question | Legal exit and handoff | Authority that DOES NOT transfer |
|---|---|---|---|
| P: Product Evidence/PRD research | L1, before Product Freeze; **what problem and promise to make?** | Product evidence disposition → Draft PRD (may evolve during studies) → policy-selected Product Review → explicit **Product Authority Freeze** | A study/tooling/reviewer PASS is not Product Freeze, L2 or code authority |
| A: Architecture Evidence/Design | L2, after Frozen Product; **how to fulfill this exact Product?** | source/architecture decisions + material UNKNOWN resolution → explicit **L2 Architecture Freeze** | Demo PASS is hypothesis-only; cannot self-thaw Product or count as production test |
| I: Implementation | after Frozen Product/L2 for substantial implementation; **what code/contract/evidence to deliver?** | frozen planning Task DAG → native GitHub live DAG if Issue based → Task/PR/concern gates → distinct version Closure/Release | task/composition/CI PASS cannot certify Hidden/RQ/Release |

`P` and `A` graphs are optional *execution coordination views*; they never replace their semantic L1/L2 owner. Only actual implementation `I` nodes use the established Task DAG Governance semantics by default. Whether/how a material P/A work item can use native GitHub dependency admission is **L2-RESERVED**, not assumed by this document.

## C02 — Per-phase execution depth and decision classification (W1, W4; P0)

Choose work organization **independently per phase** after inspecting canonical hard obligations, affected real behavior, current evidence and constraints:

- `INLINE`: existing current evidence, single bounded owner, no material schedulable dependencies → concise referenced decision, no empty DAG/Issue.
- `BOUNDED_WORKLIST`: a few checks or a single research unknown, no contested blocking topology → one owner-bounded list/checkpoint.
- `EXPLICIT_DAG`: *actual* dependent independently ownable studies, architecture unknowns/probes or implementation Tasks requiring sequencing/coordination; human/real-host constraints or critical-path visibility may justify one. Model real edges only.
- `FAST` or `STANDARD` denotes execution ceremony/profile as authorized by existing Fast Path/assurance rules. `EXPLORATORY` (uncertainty/evidence intensity) and `HIGH_ASSURANCE` (consequence/mandatory proofs) are **orthogonal flags**, not steps in a single ordered ladder; both may hold.
- Inputs: affected Product promises/core/material risk, unresolved product/architecture unknowns, provenance/confidence and source-currentness, available reuse, role/independence, write collision, dependency topology, environment fidelity, expected wall-clock/Review/Host/queue/rework cost and **distinct incremental decision value**.
- If scope/risk/currentness unknown, apply the existing hard floor; commission a *bounded* relevant probe or owning decision rather than self-classify LOW/FAST or waive. No arbitrary universal file/LOC/time, ROI percentage, or per-DAG node-count threshold.
- The chooser records a short `CHOICE + REASON + SOURCE_AUTHORITY + UNCERTAINTY + REVISIT_TRIGGER` only when decision is material or contested, not a new form for every small Task.

## C03 — Nodes, relations and conditional materialization (W1, W2; P0)

A material scheduling entry resolves `phase, concern/question, source/owner, exact subject/evidence source, independent output/acceptance, predecessor and proof consumer, environment/capability, write-scope (if any), authority-backed blocker, terminal/stop condition, escalation owner`. Existing Work Item/Task Pack semantics outrank this **conceptual minimum**.

Relations cannot be collapsed:
1. `BLOCKED_BY`: a *real*, current, independently necessary execution prerequisite, whose blocking effect is grounded in the native DAG or higher authority as applicable. For materialized **I**, GitHub Issue Dependencies are the canonical live blocked-by. For P/A, the L2 choice of whether/how canonical dependency mechanics apply remains OPEN.
2. `INFORMS / EVIDENCE_LINEAGE`: an observation suggests context or risk; no independent blocking effect.
3. `CONSUMES`: later phase explicitly adopted a cited result into its own decision; it is a **new decision** by the receiving owner, not transitive PASS.
4. `SUPERSEDES`: prior version/decision remains durable historical truth, newer decision has explicitly scoped prospective effect; never rewrites prior PASS/FAIL or currentness.
5. `RELATED_TO`: navigation only, not an execution dependency or gate.

Materialize independent Issues **only** for real ownable execution, responsible Review/Validation/human/E3 tasks, valid lifecycle owners or long-lived independent scheduling; deterministic controller calculations, simple reviewer notes, status snapshots and read-only precompute normally live in existing Issue/comments/checkpoints. An advisory Issue never mints new blocker authority.

## C04 — Stage terminal, sufficiency, transfer and negative evidence (W1, W5; P0)

- **P terminal:** bounded study/claim result, population/selection and limitations, counterevidence, decision relevance, exact provenance and material unknowns. Product owner chooses `ADOPT_SCOPE / REVISE_SCOPE / DEFER / REJECT / BLOCKED` *as a product decision*; only explicit Product Freeze is authoritative for implementation. Material unanswered product question cannot be hidden as `NO_RESEARCH_REQUIRED`.
- **A terminal:** each material UNKNOWN has sufficient existing/static evidence, falsifiable executed Demo with `What was NOT proven`, owner-bounded supported assumption/defer (where lawful), or `BLOCKED/CONTRADICTION`. Architect's L2 adopted decisions freeze explicitly and only after material contradiction is handled; Demo code is not silently promoted into production.
- **I terminal:** Task outcomes must satisfy actual required owner concern gates and review/validation truth. Version candidate separately executes relevant full regression, required Critical Journeys/Hidden/RQ and qualified integration. P/A early evidence never covers new production/real-host predicates unless current explicit consuming owners authorize equivalent coverage.
- Reuse is legal only with **exact claim/subject, tested predicates including negatives, identity/host fidelity, scope, original owner, freshness and counterevidence**. If any material predicate changes or proof unknown, reuse stays bounded/historical and owner decides targeted re-evaluation.

## C05 — Change/invalidation impact propagation (W1, W5, W2; P0)

Trigger on: Product scope/acceptance amendment, L2 invariant/contract/trust or dependency change, current source/HEAD/base/tree revision, external upstream/license/toolchain facts, real environment change, negative test/reviewer finding, Release applicability/assurance owner change, evidence provenance becoming unreliable.

For each **material change**, the owning authority supplies a bounded `CHANGE_REF + CHANGED_FACTS + ORIGINAL_SUBJECT + CONSUMER_EDGES + AFFECTED_P/A/I_NODES + AFFECTED_ASSURANCE/GATE_SUBJECTS + DECISION_OWNER + REVALIDATE/REUSE/HISTORICAL_ONLY/BLOCKED` impact rationale. Re-evaluate **dependent claims**, not all graph nodes by blanket invalidation. Preserve unaffected current proof only if the currentness/equivalence authority demonstrates the required predicate survives, never because a task author said unrelated.

- Product changed → explicit Product authority amendment/thaw/Freeze; impacted A decisions and I Task Pack/currentness are recomputed before next irreversible step.
- Architecture changed → L2 owner checks consumer contract and Task split/integration impact; true Product contradiction returns to Product authority instead of changing scope in L2.
- Code/candidate changed → actual exact-subject Validation/Review and release applicability readback by their original owners; no candidate-scoped PASS copied to successor.
- In-flight accepted Claim is not stolen or silently cancelled; apply existing admission-generation, cancellation/terminal/recovery protocol, with source/currentness hold.
- Keep old decisions append-only and mark `HISTORICAL_ONLY` where appropriate; no transitive promotion from task learning or Chat narrative.

## C06 — Decision owner, escalation and veto boundaries (W1, W2; P0)

**Decision ownership matrix:**

| Action | Decision authority (existing owner only) | Adviser cannot do |
|---|---|---|
| Product scope, acceptance, Freeze, material waiver by prospective amendment | Product Authority / authorized Product policy | Research worker/Reviewer cannot freeze |
| Architecture invariant/decision/Freeze, Product contradiction routing | L2/Architecture owner | Demo or Builder cannot choose silently |
| Material Implementation DAG mutation / Task split, scope, write set | Task DAG Governance + Task/Pack/currentness owners | Steward/chat status cannot supersede |
| Dispatch, reroute, protected Claim, resource admission | existing serialized Controller/Claim admission | scheduler suggestion or expired lease cannot steal |
| Human DENY/explicit approval for protected effects | authorized Human Decision Queue / source-bound authority | model or Controller cannot auto-approve |
| Validation/Review/gate verdict | role-/subject-/source-correct existing Validation/Review owners | Builder or quality score cannot PASS |
| Release applicability/Freeze/RQ/Main merge | current Release/Integration authority | cost/learning cannot waive REQUIRED_NOW |

A claimed decision with missing authority, stale binding, contradictory genuine P0/P1 or unresolved human decision must not advance to irreversible execution. Route to a named existing owner, mark the *specific required affected work* blocked/unknown per owner and allow unrelated legal work to proceed. No global deadlock by an incidental advisory Issue.

## C07 — Steward detection → lawful action → readback (W2; P1)

Steward is read-only analysis/recommendation on canonical GitHub/repository facts and available real observability, **not** a second always-on scheduler/Claim writer. A bounded intervention record proposes:
`OBSERVATION_REF | EXACT_CURRENTNESS | SYMPTOM | MATERIAL_BLOCKER_AUTHORITY_REF_OR_NON_BLOCKING | AFFECTED_CRITICAL_PATH | OWNER | RECOMMENDED_EXISTING_ACTION | RECHECK_CONDITION`.

Eligible symptoms: product/L2 drift, READY not claimed, dual WEB/LOCAL dispatch conflict, stale active Claim, resource contention, candidate merge queue aging, same-HEAD contradictory Review, excessive optional Issues, recurring test/harness failures, stalled convergence, missing required evidence.

Routing:
`OBSERVE → VERIFY → CLASSIFY → ROUTE_TO_EXISTING_AUTHORITY → AUTHORIZED_CONTROLLER/OWNER_ACTION → DURABLE_READBACK → RESOLVED_OR_REMAINING_BLOCKED`.
May **recommend** JIT dispatch/reroute, merge-drain, root-cause check, lawful DAG split, bounded stop, environmental preflight, Product/L2 reopen or Human decision. Cannot itself create PASS, cancel/steal Claim, infer liveness from missing branch, mint blocker from an advisory status, or independently rewrite source. For claimed stale work, §11/§27.5 normal recovery/reroute restrictions apply.

## C08 — Budget, stop-loss and loop suppression (W1–W5; P1)

Per phase/concern, name the **novel falsifiable decision predicate and consuming owner** before adding a costly research/demo/real-host/Review/extra Issue. Prefer existing source evidence and one integrated necessary proof where exact subject/equivalence/independence permit; maintain safety/rights/contract/real effect mandatory negatives.

- **P** sufficient when representative material user/problem/alternative evidence supports an authorized scope decision; classify `EVIDENCE_VALIDITY_BLOCKER | EXECUTION_BLOCKER | OPTIONAL_HARDENING | IMPLEMENTATION_CONCERN`. Optional experiment tooling does not become recursive Product gate.
- **A** sufficient when high-impact unknowns are decided or lawfully bounded/blocked; a Demo closes on evidence completeness, **not** fully built production software. Unanswered high-impact hypothesis stays open.
- **I** run focused task smoke before expensive Host/full version sequence; batch same-root repairs; if repeated iterations yield no new evidence, request owner adjudication of root cause/subject/fidelity instead of repeat dispatch. A **safety-required** rerun is never cancelled by a numerical round cap.
- Estimate `builder_active / review / validation / wait / rework / environment / downstream maintenance` at rough ranges with confidence or UNKNOWN; use W4 actual outcomes to adjust future planning, not fabricated score or quota.
- Stop/deferral `DO_MINIMAL | REUSE | BATCH | TIMEBOX | DEFER_WITH_TRIGGER | EXCLUDE_WITH_REASON` applies only where source-owner Product/risk applicability permits. No retrospective dropped frozen REQUIRED_NOW via ROI.

## C09 — Environment, capability, privacy and resource truth (W3, W2; P1)

A material dispatched action declares only relevant `execution_environment, required_capabilities, eligible role, subject/tenant identity, isolation, safe write/resource scope, E1/E2/E3 fidelity, human/local/real-host constraints, preflight and cleanup/rollback`. Actual provider/model is provenance, not gate authority.

For high-cost or real-world stages: `DECLARE → PREPARE → PREFLIGHT → (canonical) ALLOCATE/CLAIM → EXECUTE/OBSERVE → RECONCILE → CLEANUP`. Preparation is not resource/Claim admission. Ensure executable toolchain/version/exit code and test skip awareness, environment/network/registry path, timeout/log observability, external side-effects and resource release. Allocation obeys §27.3 all-or-none admission; failures/unknown ACK never justify a duplicate irreversible action.

Do not place secrets, private human/participant records, hidden test fixtures or proprietary credentials in GitHub graph metadata or Task Learning. Durable evidence may use a permitted redacted hash/provenance reference, with explicit access limitation and nonclaim of inaccessible proof.

## C10 — Task outputs, uncertainty and learning promotion (W4; P1)

Task Result (delivered work/accepted terminal/verification under existing authority) and Task Metadata (bounded cost, failure/root cause, environment, decisions, reuse/defer reasons and references) are **logical outputs**, not a demand for two files. No material learning: `TASK_LEARNING=NONE_MATERIAL`.

Learning confidence `PROVEN / SUPPORTED / HYPOTHESIS` must resolve to existing Task Learning v1/v2 source binding and evidence strength; current exact subject and usage-time verification are required. Failed hypothesis/negative results are retained with equal provenance integrity. `learning observation → proposed reusable recipe/test/skill → owner-proven project adoption → ADS evolution candidate` is never automatic normative promotion. Private agent thoughts and unsupported factual anecdotes are forbidden.

## C11 — Project adoption/version-lineage and stage crash recovery (W1–W3; P1)

Projects remain pinned to their immutable ADS version/profile until adopted through existing `PROJECT_ADOPTION` mechanisms. A0–A4 are **automation capability levels** independent of safety/assurance and FAST applicability. Applying v4.12 graph views is prospective, can be manual/inline, and does not rewrite old Frozen PRD, L2, Issue histories or past gate outputs.

After interruption or changing controlling Agent, reconstruct from **GitHub canonical issue/dependency + exact repository refs + accepted dispatch/claim/review/validation/human/Release records**, not chat memory. Distinguish local worktree changes (not yet durable delivery), stale/unknown readbacks and genuinely claimed active work. Reconcile before mutation; missing readback on an authority edge blocks that edge rather than granting replacement work. Cross-project plans must not conflate project-specific DAG authority or disjoint release candidates.

## C12 — Version convergence and delivery assurance (W1, W2, W4; P1)

Version readiness is a separate composed candidate decision:
- all **required** implementation concern gates complete; integration wiring/conformance owns cross-cutting composition;
- current gate × exact candidate applicability evaluated by Release authority (not inferred from leaf green);
- selected required full regression/Critical Journeys/real platform evidence, Hidden, Final Closeout, RQ and integration follow existing scoped obligations;
- material unresolved risk and non-run obligations stay `BLOCKED/NOT_RUN/UNKNOWN`, never `PASS` from equivalence assertion alone;
- optional advisory work is removed from release critical path unless a new real owner-material fact justifies blocking;
- Release is performed on a stable exact candidate and new candidate evidence is properly re-evaluated after material drift.

**Metrics describe**: acceptance value, distinct material predicates proven, true host executions vs dispatched, critical-path unlocks, ready/merge idle, revalidation churn, review loops, genuine escaped defects. They neither set automatic pass thresholds nor replace gate proof.

## 13. Minimal handoff sketch (conceptual, NOT new event/schema)

```text
P_STUDY {question, evidence_refs, source_exact_refs, limitations, negative_evidence,
  decision_consumer, exit, owner, currentness}
  → PRODUCT_DECISION {adopted_evidence, excluded scope, acceptance, authority_ref}
  → Product Freeze (existing owner)
A_RESEARCH {Product_Freeze_ref, unknown, alternatives, evidence/optional_demo,
  facts_not_proven, invariant/contract, reuse_licensing, consumer}
  → L2_DECISION {adopted invariants, frozen architecture_ref, unsupported claims}
  → L2 Freeze (existing owner)
I_PLANNING {Product_Freeze_ref, L2_Freeze_ref, Task DAG, scope, dependencies,
  write_ownership, review/validation floor, L3 pointers}
  → GitHub native Issue Dependencies & canonical dispatch/claim for implementation
  → PR currentness / concern gates → version Release-qualified candidate
```

Every evidence transfer is a **new receiving-authority adoption or a cited subordinate input**, never an automatic state transition. Phase view/provenance fields are a candidate compact projection that may already be representable in existing GitHub/Task Packs; machine serialization is deferred to L2 after gap proof.

## 14. Adversarial tests required by this proposed contract

| ID | Counterexample | Required reaction / evidence |
|---|---|---|
| AT01 | Product Freeze changed but stale A/I task appears READY | Affected A/I hold/re-evaluate; unaffected evidence unaffected only with owner proof |
| AT02 | L2 Demo fails on choice A but Product promise remains feasible via B | Change architecture candidate; no Product thaw without contradiction |
| AT03 | Demo PASS after mock-heavy E1 claimed production real-host PASS | Reject promotion; fidelity/scope bounded |
| AT04 | Advisory Issue references active PR and is OPEN after real gates pass | Cannot block merge without higher blocking authority |
| AT05 | Human DENY contradicted by model PASS/vote | DENY governs relevant effect; no attempted release approval |
| AT06 | Agent says Claim lease elapsed, remote branch absent | Cannot steal accepted Claim; reconcile owned cancellation/recovery |
| AT07 | Two WEB/LOCAL schedulers propose same Task | One atomic protected claim generation wins; rest rejected without effects |
| AT08 | FAST optional UI under high-risk auth change | Scope is materially security-sensitive: legal hard floor, no ROI waiver |
| AT09 | L1 experiment tooling keeps getting robustness suggestions | Stop optional tool hardening once study validity suffices |
| AT10 | PR CI green but task-specific test omitted or skip-heavy | Focused actual test/skip/evidence remains BLOCKED; no fake PASS |
| AT11 | Many overlapping independent large Tasks share central registry | Separate contract/central wiring or preserve atomic; no fake parallel writers |
| AT12 | Implementation Task PASS, Hidden/RQ not run | Version remains unqualified |
| AT13 | Older adoption pin upgraded; historical gate incorrectly relabelled | Preserve old exact identities; prospective policy only |
| AT14 | Missing access to private E3 proof, dashboard says green | Evidence unverified in current consumer, never assert full PASS |
| AT15 | Upstream license/contract drift while Product scope unchanged | Reconsider affected L2/code reuse rights and consumer contracts only |
| AT16 | Contradictory independent same-HEAD P1 and PASS | Do not merge until authorized adverse-finding adjudication |
| AT17 | Worklist turns into 40 dependent issues without new proof consumers | Materialization economy; advisory nonblocking; controller merge-drain |
| AT18 | One atomic security invariant is unusually large | Preserve atomicity, narrow internal steps, don't force arbitrary split |

## 15. Explicit UNRESOLVED design choices (PRD/L2 boundary)

These MUST be labelled OPEN and owner-assigned before freeze; they are not silently decided by this draft.

1. **P/A graph serialization:** only Markdown checklist/Issue dependencies vs additive existing Work Item/projection; which P/A edges may use GitHub native dependencies and under what admission/scope.
2. **Cross-phase impact calculation:** pure manual evidence register vs derived graph index; exact definition of dependency/currentness traversal; matching predicate proving safe retained evidence.
3. **Stage sufficiency evidence:** precisely who signs an adopted Product/L2 sufficiency decision for each adoption profile and whether selected review is required on that subject; conflict/appeal routing via existing Human Decision/Owner.
4. **Adaptive profile placement:** whether FAST/STANDARD plus EXPLORATORY/HIGH_ASSURANCE are semantic fields, existing assurance-plan projections or just planning prose; exact compatibility/override precedence.
5. **Steward operational delivery:** read-only manual checklist vs automated reducer alert; polling cadence/capability availability, owner actor and proof of follow-up actions; no new scheduler.
6. **Resource/environment record:** minimal toolchain/human/E3 fidelity metadata and cleanup proof binding; conflicts and runner evidence owner.
7. **Version convergence metric scope:** best reconstructible metrics, denominator, required vs optional, non-gaming; no unsupported SLA.
8. **Adoption compatibility:** which v4.12 changes are semantically additive vs migration-requiring and what is versioned; specific frozen in-flight projects as regression examples.
9. **Privacy/public evidence references:** redacted proof envelope and access control when sensitive human or hidden evidence cannot reside in public GitHub.
10. **Evidence equivalence and Review independence:** exact predicate/negative/fidelity matching and autonomous vs independently authorized reviewer semantics; reused prior evidence is not automatically acceptable.

## 16. Planned L1 closeout (not done)

One bounded owner-gap matrix marks each C01–C12 as `ALREADY_IMPLEMENTED_WITH_TEST | BOUNDED_DELTA | NEEDS_PRODUCT_DECISION | L2_ONLY | DEFER`; pairs with actual app8/domain-harness/runx/ADS T12 dogfood; runs fresh external Product review as policy requires before Product Freeze. **No claim of independent review, Product Freeze, L2 Freeze or executable implementation DAG in this R0.**


## 17. Counterexample-driven R1 repairs to C01–C12 (after author-led R0 review)

These are **candidate contract clarifications**, not machine implementation or normative PASS. The R0 reviewer findings are preserved at `V412_ADVERSARIAL_REVIEW_R0.md`.

### R1-F01 — Stable scope, identity and phase graph membership

Every *material* graph entity and evidence-consumption decision must resolve an identity tuple adequate for its real subject: `repository/project + Product/version stream + stage P|A|I + stable concern/work identity + governing frozen/current authority revision + evidence subject identity/currentness basis`. A source doc path, local session ID, provider label, array index or issue number without repository/version scope alone is insufficient when ambiguous. Historical P/A evidence without exact commit SHA (e.g. external user interviews) MUST instead carry attributable collection/scope/time/source permissions, limits and a reproducible owning decision; never fabricate a SHA. Cross-repo consumption must explicitly cite which receiving Product/L2 authority adopted the finding. Stable task ID may remain while *current decision revision* changes, with older revisions historical.

**Counterexample:** P-01 from two different repositories with the same title are not one node, and a 2024 market study cannot automatically satisfy a current 2026 product claim.

### R1-F02 — Product feasibility probes without premature L2 authority

The **question/consumer determines the stage**, not whether a probe runs real software. Stage P MAY use a timeboxed reproducible technical feasibility probe, demo or human study **only to decide Product viability/acceptance scope** when existing/static evidence is insufficient. It must state `PRODUCT_QUESTION, FALSIFIABLE_PREDICATE, WHAT_NOT_PROVEN, STOP_RULE, DATA/TOOLING_LIMIT`. It is **not** an L2 architecture selection, production implementation, or v4.11 Architecture Research Demo. Architecture-level choices, public contract, durability and trust design remain post-Product-Freeze L2-owned unless a current explicit higher authority provides another lawful route. Existing Product/Architecture contradiction/amendment handling governs return flow.

**Counterexample:** testing whether users can legally export required data can justify excluding a Product feature, but cannot pre-freeze a runtime library or certify a production adapter.

### R1-F03 — Minimum bounded impact algorithm (behavior, not new graph engine)

At every *material* change, the existing authorized owner/controller performs:
1. **Resolve** exact old/current product/architecture/task/assurance subject and accepted durable changed fact; untrusted commentary is not a changed authority fact.
2. **Find consumers** from explicit adopted evidence/contract/Task Pack/source dependencies and currently accepted native implementation blocked-by edges. Unknown/unresolvable consumer mapping triggers manual owning disposition on affected execution; no guessing all remain current.
3. **Compare** each consumer's actual required predicate/binding: (a) identity/authority, (b) semantic contract/negative/safety proof, (c) exact source/base/HEAD where relevant, (d) independence/evidence fidelity, (e) Release gate × subject and external/rights/toolchain binding.
4. **Classify** each affected consumer only as `RETAIN_CURRENT_WITH_OWNER_PROOF | REVALIDATE_OR_REBIND | HISTORICAL_ONLY | BLOCKED_UNKNOWN` (a **decision record**, not workflow or gate status). A positive retain needs owner-accepted provenance/currentness/equivalence proof, not "unrelated diff" narrative alone.
5. **Apply** existing Product/L2/DAG/Assurance/Validation/Release control for lawful successor decisions; never change an accepted Claim via Work Graph edge editing.
6. **Re-read** accepted current artifacts/claims/real native dependencies before JIT/merge/Freeze/Release; preserve old failure history and impact rationale.

Only **material reachable consumers** are reviewed; no automatic project-wide CI/host storm. An unrelated version-history issue cannot self-create dependencies. Explicit uncertainty fails closed on affected authority-bearing transition, not all unrelated work.

### R1-F04 — Supersession, terminal and stage authority

The conceptual graph `SUPERSEDES` edge conveys history/currentness **only**. It is not a new terminal record, cancellation event, Release waiver, Product/L2 Freeze or claim authority. For P/A decisions, new adopted revision requires exact owning Product/L2 amendment/Frozen handoff, with previous evidence retained as historical. For I, native Task DAG mutations require existing Task DAG Governance; dispatch and Claim cancellation/terminal require existing serialized protocol. There is no universal cross-stage `COMPLETE/PASS` object. A parent "research complete" list can be true while one required Product finding remains insufficient; only the actual owner resolves phase exit.

### R1-F05 — Conflict resolution and affected-scope blocking

Before an authority-changing action, collect currently binding **hard floors** from actual Product, Architecture, Security/Trust, Human Decision, Assurance, Validation and Release owners. `LOW_ROI`, FAST eligibility, "non-core", model confidence, evidence quantity or lighter adoption is never a superior authority. If two valid current owner decisions conflict:
- do not choose latest comment/stronger model/more reviews by majority;
- identify exact subject, predicate and owning authority precedence; send to legitimate owner(s) for bounded adjudication/amendment;
- preserve adverse factual finding and human DENY according to existing source authority;
- block only the implicated irreversible action/gate; let genuinely independent, legal tasks proceed;
- never retroactively weaken `REQUIRED_NOW` or old Frozen safety rules.

Where Product scope inclusion and Release gate applicability are different decisions, Product may narrow **future Product scope** via lawful amendment, but only Release authority can change its gate×subject applicability for the then-current candidate.

### R1-F06 — Canonical evidence source, event admission and untrusted text

A source-like line (`FREEZE=YES`, `REVIEW_PASS`, `SCHEMA_VALID`), pasted JSON, issue label, LLM summary or provider transcript is **untrusted content until canonical authentication and writer/role/subject admission** under existing `GITHUB_AGENT_INTERACTION_PROTOCOL` §8 and `EXECUTION_ARCHITECTURE_STANDARD`. A proposed v4.12 reducer can ingest P/A evidence only with `ORIGINAL_SOURCE + ADMISSIBLE_ISSUER + SOURCE_IDENTITY + SUBJECT + CLAIMED_STATUS_VS_ACTUAL_ADMISSION + EVIDENCE_VERSION`. Where machine event v2 publication is applicable, construct → strict pinned schema/semantic validation → role/currentness check → canonical publish → readback. Unknown publication outcome must reconcile before retry; never print an event-shaped status into chat and count it as admitted fact. Exact schema/evidence envelope remains **L2-reserved** with existing writer owner, not a new W1 event family.

### R1-F07 — Strict full-predicate equivalence and restricted-data handling

Reuse a prior test/proof only if accepting **gate/evidence owner**, at consumption time and on the exact applicable subject, confirms:
`material predicate AND negative/failure or denial branches AND actor/independence AND fidelity (simulated vs real) AND environment/tenant/rights AND current exact evidence identity AND applicable time/source limitations`.
One real observation can satisfy several **logically equivalent** coverage rows only when this complete bar is met; same names, helper code, or source-only assertions cannot prove equivalence. A material difference in human approval, irreversibility, tenant data, upstream license or external effect defeats equivalence. Redacted/hidden proof must be verifiable by an eligible actual reviewer/authority through a legal protected channel; merely citing an inaccessible private location yields `NOT_VERIFIED/UNKNOWN`, not PASS.

### R1 review-repair coverage table

| R0 | Candidate patch | Residual authority |
|---|---|---|
| F01 | R1-F01 identity, version & multi-repo scoping | L2 chooses actual metadata shape |
| F02 | R1-F02 Product-purpose feasibility probes | Product/L2 owners approve phase routing |
| F03 | R1-F03 6-step material impact/readback procedure | Assurance/Validation/Release owner acceptance; no engine implemented |
| F04 | R1-F04 supersession never replaces canonical state | P/A and I existing canonical owners |
| F05 | R1-F05 priority and specific affected-scope blocking | Specific Product/Security/Human/Release adjudication |
| F06 | R1-F06 admissible source and before-publish schema checks | Existing event writer conformance; #783 remains to audit |
| F07 | R1-F07 strict evidence equivalence and eligibility | Existing gate owner must actually accept each equivalence |

**After these repairs:** the draft can enter Product/L1 review as a **complete candidate model**, but it still cannot be called Product-Frozen or production-conformant. The R0 author-led adversarial review remains historical, not an independent PASS. P/A native materialization, mutation proof algorithm schema, Steward delivery, human/private evidence permissions, resource preflight, compatibility and ROI calibration remain explicit L2/product policy questions rather than fabricated settled implementation.


## C13 — Human necessity classification and minimum necessary human evidence (W1/W2/W4/W5; Product/L1 candidate)

**Product intent:** use the cheapest *lawful and epistemically adequate* combination of bounded multi-LLM adversarial analysis, deterministic tools and minimally necessary real-human involvement. This is a **default routing principle, not a forced three-stage gate**. Existing Human Decision Queue, Product/L2/Review/Validation/Release authority and applicable pre-registered empirical protocols remain owners. "Human as expensive" is never a reason to fabricate human observations.

### H.1 First ask what specifically requires a person

Before assigning any expensive human work, classify the **actual predicate**, evidence consumer and existing authority:

| Class | What must be established | Lower-cost treatment | Genuine human obligation |
|---|---|---|---|
| `H0_MACHINE_PROVABLE` | Well-specified logic, schema, SHA/currentness, code/tests, reproducibility, access constraints | Deterministic scripts first; focused reproducible negative tests; optional AI analysis for gaps | **NONE** unless existing authority explicitly requires reviewer/human |
| `H1_JUDGMENT_ADVICE` | Product alternatives, document quality, plausibility, competing design, test ideas | Distinct-role LLM author/critic/red-team, source-backed analysis and disagreement logging, bounded iterations | **NONE** if policy permits; owner still owns Product/L2/Review disposition, not the LLM consensus |
| `H2_RESERVED_HUMAN_DECISION` | Product Freeze/thaw, explicit business acceptance, irreversible effects, privacy/consent, legal/regulatory/contract-authorized approval, any existing policy requiring a human | Prepare one short evidence-complete decision card, automate prerequisites and evidence verification | **REQUIRED authorized human**, not replaced by model votes or tools |
| `H3_HUMAN_OBSERVATION` | Actual target-user behavior/preferences, representative study, independent-human review if specifically required, blind human Gold/oracle creation when method demands it | AI prepares protocol/materials and candidate labels; deterministic checks sampling/format/leakage; limit cohort to **credible minimum** justified by study validity | **REQUIRED real participant/qualified independent human** to produce the predicate; merely rubber-stamping AI labels is not equivalent to independently authored blind labels |
| `H4_HUMAN_REAL_WORLD_ACTION` | Genuine participant consent, physical/device action, authorized manual recovery, human-in-the-loop approval/deny at effect boundary | Minimize interaction by prepared plan, dry-run, bound exact subject & consequences, one-tap accept/deny only when policy permits | **REQUIRED** for actual human action/effect; LLM cannot counterfeit it |
| `H_UNKNOWN` | Owner/consent/independence/representativeness applicability unclear or private evidence inaccessible | Small preflight to clarify current source obligation; route to existing authority | **NO automatic downgrade** to H0/H1 or synthetic PASS |

The classes are **routing labels only**, not a new canonical lifecycle state or mandatory schema. One concern can include several classes (e.g. H0 fixture checks + H3 empirical observations + H2 Product Freeze). A Project override cannot erase a binding H2/H3/H4 requirement.

### H.2 Optional three-layer evidence pipeline; stop when lawful sufficiency is achieved

1. **Bounded multi-LLM adversarial analysis (only when material semantic uncertainty exists):** separate author/critic/falsifier roles; different eligible models/prompts where cost-effective; blind candidate/protocol where experimental independence matters; cite source and exact subject; seek specific disconfirming examples, not score-based consensus. Record unresolved claims/alternatives. *Multiple models are correlated and cannot claim a genuine human observation, source truth, truly independent operator or actual Review PASS merely by agreeing.* 
2. **Deterministic verification (where predicates are executable):** strict schema/parser, SHA/provenance, coverage denominator, test entrypoint, negative fixtures, reproducible comparisons, data/label leakage & train/test partition checks, numerical consistency, and observed real execution exit/status. A script proves **its asserted properties only**. It cannot determine subjective human preference, consent, legal authority, truth of unobserved empirical labels or population representativeness by itself.
3. **Human minimum necessary involvement (only for remaining lawful predicate):** produce a short `DECISION_CARD` with exact subject, evidence, main alternatives, material unresolved disagreements, explicit risk/limitations, requested human role/qualification, the one decision/action/observation required, and audit receipt; batch genuinely compatible human requests while preserving blinding and independence; accept real disagreement rather than solicit another human until desired verdict. Only owning human/qualified reviewer/participant action is admissible where required. When no real human is available, return **BLOCKED / NOT_RUN / RESEARCH_LIMITATION** by owning policy, or prospectively amend Product/experiment design via authority. Never mark PASS/NOT_APPLICABLE from "AI consensus."
4. **Stop-rule:** omit a layer with no expected unique evidence contribution. A low-risk fully deterministic task can go directly to correct machine owner terminal; a mandated physical/Human DENY test cannot be bypassed even if 20 LLMs agree. Revalidate when exact subject or binding conditions materially change; do not repeatedly convene agents/humans to restate unchanged facts.

### H.3 Human cost minimization without empirical invalidation

- Use one **human minute spent on decision-relevant uncertainty**, not "number of human sessions" as quality; prepare consent, instructions, gold candidate and deterministic sample summaries in advance, but preserve pre-registration, blindness, subject independence and representative cohort when required.
- For empirical Gold: `AI_DRAFT_LABEL` plus human spot check is a **hybrid annotation scheme**, not a `HUMAN_AUTHORED_BLIND_GOLD` dataset. Change the experiment methodology with study/Product authority if necessary, disclose limitations and rerun validity analysis. Human-independent Reviewer also cannot be replaced by the Builder's own LLM personas if the current policy requires a fresh independent actor.
- **Before adversarial multi-LLM dispatch:** verify each model/provider/processor is authorized for the exact source data and destination; redact or restrict sensitive participant, customer, legal, credential or hidden-test facts. A model may not access protected raw evidence merely because it is playing a Reviewer role. If no authorized model can read it, use approved deterministic or human-only verification and record the limitation.
- **Meaningful human consent and control:** a compact decision card or one-action approval may reduce friction only when the real person can see the actual subject, material consequences, permissions, alternatives and a genuine `DENY/REFUSE` path without default assent. Required consent/withdrawal/independence rules are those of the current empirical/human/external-effect owner, not this draft's UI convenience.
- Human participant data, private or hidden truth must stay in lawful protected systems; GitHub contains only permitted evidence reference/redaction. An eligible source-bearing validator must actually verify protected truth before declaring current accepted evidence.
- Avoid mandatory "two/three LLM reviewers" for each Task. Optimize over source-relevant independent perspectives, deterministic proof and targeted human decision, while observing existing assurance/Review policy.
- Measure `HUMAN_REQUESTS_PLANNED, ACTUAL_HUMAN_ACTIONS, HUMAN_DECISION_LATENCY, MATERIAL_DISAGREEMENTS_ESCALATED, TOOL_PROVEN_PREDICATES, UNVERIFIABLE_HUMAN_PREDICATES, REAL_STUDY_COVERAGE, HUMAN_TIME_UNKNOWN_OR_OBSERVED`. Never invent cost savings, assign generic numerical minimum cohort, or turn metrics into mandatory extra Issues.

### H.4 Falsifiable acceptance examples (not tested yet)

| ID | Case | Required outcome |
|---|---|---|
| HT01 | Pure schema/contract/source proof + no human owner requirement | H0 deterministic verification; zero arbitrary human approvals |
| HT02 | Three agreeing LLMs on user happiness with no real users | H3 remains unobserved; Product may choose a lawful bounded real study or declare uncertainty |
| HT03 | Blinded independently authored human Gold required, LLM produces 48 candidate labels and one person rubber-stamps | Cannot claim 48 independent human-authored blind Gold; pre-registered study protocol must be preserved or formally amended |
| HT04 | Human authorized DENY after a genuine external-effect proposal while models vote ALLOW | Human DENY retains authority; effected operation blocked |
| HT05 | Reviewer identity must be fresh/independent, same Builder invokes several critique personas | Does not satisfy genuinely fresh independent Reviewer; route to qualified independent actor |
| HT06 | Model proposes edge failures; deterministic checker reproduces one but others are not executable | Reproduced fact proven within test scope; untested ideas remain hypotheses, not PASS |
| HT07 | A human study is expensive but real-user representativeness is a material Product unknown | Cannot automatically drop H3 on ROI; redesign scope/protocol by Product owner or honestly block |
| HT08 | A low-risk issue's machine tests and existing authorized review gates are satisfied | Stop after current owner terminal, no redundant three-model contest or human meeting |
| HT09 | Real-user samples include sensitive participation data not accessible to public agent | No public raw-data leak; authorized human/validator checks protected evidence, inaccessible observer cannot assert PASS |
| HT10 | Two LLM reviewers disagree on normative obligation, tool checks cannot arbitrate | Escalate the exact unresolved owner decision once, with bounded competing evidence and a decision card |

**Remaining policy decision for v4.12 PRD:** exact owner/qualification/independence triggers for H2/H3/H4 and minimum-permitted hybrid annotation changes must be mapped against current Product/Review/Human/Research authorities; decision-card schema/automation is optional L2 design, not mandated by this candidate. No new human review system, model voting authority or human substitution protocol is created.


## C14 — Publicly observed human evidence before commissioned human studies (W1/W5/W4; Product/L1 candidate)

**Product direction:** source-first L1: investigate existing **authentic human expressions and behavior traces** before commissioning expensive custom interviews, surveys, blinded gold or real-user tests, **but only when the precise Product predicate can be answered by that evidence type**. This is a default **evidence selection strategy**, not a universal scrape requirement, collection permission or authority to replace reserved H2/H3/H4 human predicates from C13.

### O.1 Evidence kinds and what they can actually prove

| Evidence class | Examples | Bounded positive claim | Cannot infer |
|---|---|---|---|
| `O1_PUBLIC_SELF_REPORT` | opt-in public forum/blog/product review: “I attempted X; Y failed” | a person publicly **reported** that experience, at an attributable time and scope | that it happened as stated, actual frequency among all users, actual UI completion, independent human-blind truth |
| `O2_PUBLIC_BEHAVIOR_TRACE` | public issues/PR actions, timestamped community support interactions, bug reproduction with observable artifacts | that a **publicly observable action/artifact** occurred under source provenance | hidden user intent, full real-world population representativeness, legal identity or consent |
| `O3_AUTHORIZED_PRODUCT_TELEMETRY` | first-party consented anonymized event log, permitted aggregate usage/support metrics | bounded observed behavior/frequency *within the known instrumented population* | unmeasured offline/non-instrumented users, causal effect absent controlled design, equivalent consent outside original purpose |
| `O4_CURATED_RESEARCH_DATASET` | appropriately licensed survey/study/interview corpus with stated sampling frame, study report | the exact claims covered by the original valid method and use rights | new identity/current population truth automatically, reconstructed unpublished raw behavior |
| `O5_PURPOSE_BUILT_REAL_HUMAN_STUDY` | prospective target-user session, representative sample, randomized usability comparison, truly human-authored blind labels | independently observed specific experimental predicate (if protocol, blinding, representativeness and privacy valid) | any effect or generalization beyond that protocol |
| `O_UNKNOWN_OR_SYNTHETIC` | AI-generated persona/replies, suspected bot/marketing manipulation, inaccessible source, unknown license, unattributable dump | hypothesis-generation only; provenance cannot be claimed real | any true human observation/empirical or human Gold PASS |

**No promotion by wording:** a forum post is usually an instance of **self-reported experience**, not direct verified action or a representative study. Even genuinely human posts need not correspond to the intended end-user population. Negative reports may be overrepresented, visible material may be curated, deleted, dated, translated, promotional, copied or AI-generated. Never substitute raw post count for an unbiased denominator, and do not assert human identity from a platform handle alone.

### O.2 Source selection and rights gate BEFORE data collection or LLM upload

Choose in order: currently held lawfully usable project/first-party research → licensed/public datasets and published study results → **platform-authorized** official research/API/search/exports → permitted bounded observation of public pages. Always check **current platform policy + robots/rate rules + copyright/license & permitted purpose + privacy/personal-data restrictions + region/jurisdiction + retention/deletion**. Public visibility != permission to scrape in bulk, train a model or republish content. No login bypass, CAPTCHA avoidance, forbidden scraping, collection from restricted/private communities without proper access and rights, or unauthorized content retention.

Concrete contemporary counterexample: Reddit's 2026 Developer Platform guidance distinguishes permitted developer access from its **Reddit for Researchers** pathway and its Data API Terms impose specific restrictions including commercial uses; don't treat indexed Reddit pages or ordinary developer API as blanket research bulk-access rights. An independent public privacy regulator joint statement likewise warns that openly visible personal data can remain protected. Source policy references (verify at actual use):
- https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data
- https://redditinc.com/policies/data-api-terms
- https://ico.org.uk/media2/migrated/4026232/joint-statement-data-scraping-202308.pdf

Prefer minimized analytical features and aggregated patterns over storing/republishing identifiable quoted content. Never pass restricted content, personal profiles, protected study data or hidden Gold to an unapproved LLM/model provider. Respect deletion/withdrawal, secure storage and research ethics where applicable. If permissions cannot be established, skip that source; look for lawfully available alternatives or acquire authorization, not a workaround.

### O.3 Minimum evidence register (bounded; not a new mandatory DB)

For each material externally sourced claim, enough information for an authorized consumer to check:
```text
PRODUCT_QUESTION / EXPECTED_DECISION
CLAIM_SCOPE = observed self-report | public trace | instrumented behavior | existing research | prospective human study
SOURCE_SITE_AND_SPECIFIC_REF / SOURCE_TYPE / COLLECTION_DATE_AND_TIME_WINDOW
LEGAL_ACCESS_AND_USE_BASIS / DATA_PERMISSION / REDACTION_OR_AGGREGATION
SEARCH_QUERY_OR_SAMPLING_FRAME / INCLUSION_EXCLUSION / LANGUAGE_REGION_PRODUCT_COHORT
N_RAW_ITEMS / N_DISTINCT_CONTRIBUTORS_ESTIMATE_IF_VERIFIABLE / DEDUP_BOT_SPAM_CHECKS
POSITIVE_AND_NEGATIVE_CASES / KNOWN_SELECTION_COVERAGE_VOICE_BIAS
QUOTE_OR_EXTRACTION_METHOD / LLM_CLASSIFIER_LIMITATIONS / RECHECK_SAMPLE_AND_FINDINGS
ACTUAL_CLAIM_AND_WHAT_NOT_PROVEN
PRODUCT_DECISION_CONSUMER / REAL_HUMAN_STUDY_TRIGGER_OR_STOP_RATIONALE
```
Do not require this register for a trivial search; detailed entries are proportional to material Product decisions. If denominator, user identity, representativeness or collection legality is unknown, write `UNKNOWN` and narrow the claim.

### O.4 Source-first escalation and study-method authority

1. Define the *specific decision predicate* (e.g. "does this pain point exist?" vs "what fraction of Myanmar home users hit this obstacle?" vs "can a user complete this new UX in 3 minutes?" vs "is blinded independently authored Gold correct?").
2. Search **lawfully accessible** existing evidence and diversify platforms, languages, participant communities, time periods and opposing observations when material. Do not scrape "everything" or let collection tools become an L1 infrastructure project.
3. Deterministic provenance, rights, dedupe, sampling/coverage and data consistency checks; then **bounded multi-LLM adversarial extraction** (distinct source-backed accounts of patterns and disagreement), and reproduce spot checks without revealing protected personal content.
4. Product evidence owner classifies `SUFFICIENT_FOR_THIS_PRODUCT_DECISION | PARTIAL_DECISION_SUPPORT | OBSERVATION_BIAS_MATERIAL | NOT_APPLICABLE_TO_PREDICATE | ACCESS_PROHIBITED | UNKNOWN` as **advisory sufficiency/limitations**, not new Product/Validation gate PASS.
5. If evidence suffices to decide **L1 Product scope** at its required standard, cite it and stop; no prospective humans required by default. If objective requires observed task completion, causal comparison, quantified representative prevalence, experimental blindness, reserved human consent/denial or actual human independent review, **conduct only the necessary bounded real study/human action** unless existing Product/Research authority prospectively approves a different method. If too expensive, narrow/defer the Product claim honestly; do not manufacture approval.
6. Explicitly distinguish *source method amended before Freeze* from *retroactively weakening a frozen experiment/Release gate*. Source data can answer L1 Product questions but never self-freeze PRD, create L2 PASS or establish software production E3.

### O.5 Acceptance / negative tests (conceptual, not executed)

| ID | Scenario | Expected bounded result |
|---|---|---|
| OT01 | 300 permitted support posts independently describe the same core pain with dated links | Substantial existence/problem-pattern evidence; no universal 300-person population denominator |
| OT02 | 300 posts are copied from three marketing accounts/AI bots | Deduplicate/identify source limitation; no 300-user claim |
| OT03 | Forum self-reports of a button confusing users, but no video/log of task | Product pain hypothesis supported; timed usability success **not proven** |
| OT04 | 200 negative Reddit posts vs unknown whole-market sample | No "X% of all users" estimate; opt-in/coverage bias declared |
| OT05 | Restricted login-only patient or child group, web crawler technically can access | Access is not lawful permission; privacy/source gate blocks unapproved collection |
| OT06 | Official research/API channel restricts bulk export or commercial use | Respect current platform program/terms; no generic public-scrape workaround |
| OT07 | New target-region UX not used yet; existing unrelated forum discussion | Need a lawful target-user study or limit Product claim; don't infer completion/causality |
| OT08 | Existing approved blinded human Gold requires independently human-authored labels | Public discussions/LLM votes can't substitute; execute or formally amend method |
| OT09 | Existing consented first-party telemetry shows cohort-specific task abandonment | Report instrumented cohort with known denominator; don't extrapolate untracked population |
| OT10 | Forum dataset is pushed to external LLM despite restriction | Reject transfer; use permitted aggregate/redacted analysis or owner-approved tool |
| OT11 | Published qualitative sample contains a genuine rare catastrophic security event | Low post prevalence doesn't downgrade mandatory risk assurance |
| OT12 | Product/L1 evidence complete but L2 high-impact UNKNOWN remains | Product may freeze if authorized; Architecture still needs L2 evidence/decision |

### O.6 Open decisions reserved to Product/Research/L2

- Product **evidence sufficiency** depends on exact claim and intended user population; no fixed number of posts/users, global confidence cutoff, or universal permission to scrape.
- When a sample is sufficient for L1 scope versus when original empirical study mandates purpose-built human observations is decided by the existing Product/Study owner with source methods and counterevidence, not the LLM majority.
- Access/rights catalog, safe ingestion connector, sampling/dedupe algorithms and redacted proof storage are **L2 implementation choices** and may be satisfied by existing CrawlKit or other permitted research tooling. No new crawler, mandatory scraping job, P/A DAG node, independent human panel or universal data lake is requested.
- No use of observed public forum behavior as normative PASS, independent-human-authored blind oracle or evidence of legally reserved human decisions without genuine source-method proof.


## C15 — Co-evolving scaffold and Implementation Task DAG before paired freeze (W1/W3/W5; v4.12 Product direction, candidate)

> **USER PRODUCT DIRECTION CONFIRMED AND CLARIFIED 2026-10-14:** Generate an appropriately sized actual project scaffold **before full Implementation Task DAG Freeze**. While drafting/refining the Implementation Task DAG, **progressively enrich the same scaffold**. At completion of DAG planning, the scaffold is formally baselined **together with** the Implementation Task DAG; downstream execution Tasks consume that baseline. This **supersedes the former C15 choice of T00-as-default vs optional B** for prospective v4.12 Product design. It is **not yet Frozen PRD/normative permission** to bypass the currently pinned v4.11 Task-DAG-before-source rules.

### S.1 Exact stage sequence and semantic boundaries

```text
Product Freeze
  → L2 Architecture Evidence / Research and explicit L2 Freeze
  → Scaffold Planning scope under prospective v4.12 policy (no extra gate)
  → Initial Scaffold S0 (right-sized working project / contract shells / reuse)
  ↔ Implementation DAG DRAFT D0
      → Plan one feature/invariant concern
      → Allocate module contract/owner/write scope
      → Enrich SAME scaffold S1, S2, ... only as needed for that concern
      → Add Task input/output, acceptance, dependency, L3 need, gates
      → Check consistency/real build-smoke, clarify responsibility and repeat boundedly
  → PAIRWISE CONVERGENCE: Scaffold SF + Task DAG DF agree on contracts,
    module paths, write ownership, test entrypoints, blockers and references
  → Scaffold Baseline acceptance + Implementation Task DAG Freeze
      bind {FROZEN_PRODUCT_REF, FROZEN_L2_REF, SCAFFOLD_PROJECT_REF,
            SCAFFOLD_EXACT_SHA/TREE, DAG_EXACT_CHECKPOINT, CONTRACT_SET,
            UNIMPLEMENTED_BOUNDARIES, REQUIRED_PROOFS, ENVIRONMENT_LIMITS}
  → Materialize implementation Tasks/native GitHub Issue Dependencies
  → JIT Task Packs, accepted dispatch/Claim and implementation PRs
  → Integration + version-gate evaluation + Release
```

**L2** fixes Architecture obligations/invariants and component ownership; its Freeze is **not** automatically a functioning project skeleton. **Scaffold** is real source/build/tests with a bounded **structure/contract** claim, **not** a Product/L2 decision or implemented feature. **Draft DAG** is planning and does not authorize a downstream worker. **Frozen DAG** is an implementation plan bound to the final accepted scaffold source; GitHub native Issue Dependencies are the live DAG only after authorized materialization. L3 remains task-local implementation evidence, often generated JIT after Freeze.

### S.2 Planning Scaffold Creation (NEW_PROJECT_INIT) — positive permission, not an extra gate

**Product decision clarified 2026-10-14:** generating a **brand-new** project Scaffold after Product/L2 Freeze is a legitimate **planning artifact creation**, not modifying an existing Frozen implementation, and must not be mislabeled as an illegal Feature-Task source mutation. `NEW_PROJECT_INIT` and `EXISTING_PROJECT_ADAPT` are distinct. Under the **prospective v4.12 workflow**, the Scaffold Planning stage has **express scope-limited permission to create and enrich files before the complete Implementation Task DAG Freeze**. It needs no new mandatory human approval, independent Bootstrap Freeze, or extra task per generated file. This is the user's intended design correction and **replaces S.2's earlier supposed unresolved P0 Product permission question**.

Permission and bounded accountability use only the current-source project and existing GitHub/work governance:
- The **Frozen Product and L2** determine project goal, architecture, public boundary, compatibility and whether a new scaffold is appropriate. The responsible Scaffold planning owner/Agent has normal GitHub repository write permissions and a source/branch/PR identity.
- Scope **PLANNING_SCAFFOLD** includes project/package directories, contracts/types/schemas, structural placeholder modules, build/test/CI entry points, dependency/lock/config, and bounded integration seams needed to represent the planned Task DAG. For mature existing source, make only necessary scoped additions without destructively overwriting existing code.
- An explicit **stage role/scope reference** (can be in the existing L2→Scaffold/DAG planning checkpoint and Project/Work Item authority) records owner, allowed new/write paths, inputs/version pin, source branch and known out-of-scope behavior. This is **not a new formal Gate, separate control-plane authority or a claim of full implementation execution**.
- Genuine Git writes remain attributable GitHub commits/PRs with ownership and conflict discipline. If several agents share mutable contracts/manifests, use existing serialized writer/Claim/controller mechanisms **where applicable**; a Draft DAG Task must not start unrelated business Feature implementation work. No automatic HIGH_ASSURANCE for ordinary clean-slate file creation.
- Creation of real Product business behavior, data migration, privileged/external irreversible action and changed Frozen public API/Trust invariants require the same **real implementation/owner authority** that would apply outside Scaffold Planning; calling it "bootstrap" cannot bypass those obligations.
- **Planning closeout** is an accepted, integrated exact Scaffold source/tree and a logically matching Frozen DAG checkpoint; actual scaffold structural/compile checks are required *as applicable*, not full product Feature/E3/Release PASS. A normal project's working branch/PR can be the delivery surface without artificially generating a `T00` merely to unlock ordinary planning.
- **Version boundary:** this new planning-stage permission must still be integrated into the actual v4.12 `DEVELOPMENT_WORKFLOW` and its current Work Item/source-writer rules in L2, approved under v4.12 Product/architecture authority before normative adoption. **Current pinned v4.11 remains unchanged** and uses its lawful T00-in-DAG path.

**Specific open L2 implementation matter, not a Product blocker:** define the minimum actor/scope/currentness/PR proof necessary to enforce `PLANNING_SCAFFOLD`, including rejection of **out-of-scope Feature execution**, while reusing existing GitHub/Claim roles without a second scheduler or mandatory manual gate. See [Initial Policy v0.1](V412_INITIAL_POLICY_DECISIONS_V01.md) §D01–D02.

### S.3 Adaptive scaffold detail and progressive enrichment

Scaffold detail is chosen from the **actual Frozen L2 and coordination need**, not from project labels, number of Agents, percentage complete or template size:

| Scope | Suitable baseline | Guidance |
|---|---|---|
| Existing mature project | **REUSE** verified current source, add only absent seams | No regeneration/destructive reset of working layouts |
| Small concern / low-risk change | **MINIMAL / CONTRACT-ONLY** project/reference; optional omission only if authorized Product applicability | Do not add empty generator steps, redundant code or obligatory Host |
| Several independent modules / multi-Agent | **STRUCTURAL / BUILDABLE** packages, schemas, stable contract boundaries, composition root, test runner, isolated write surfaces | Prefer reproducible compile/import/build smoke where relevant |
| High-risk runtime / external integration | **RISK-BOUNDED** trust/error/failure contracts, fake-vs-real labels, environment preflight, relevant negative proof requirements | No fake/E1 proof promoted to E3, no automatic entire release matrix |

During **each** DAG design iteration, ask:
1. Is the intended Task a meaningful independently reviewable **feature/invariant/contract/validation/integration concern** with clear authority and acceptance, rather than one method/interface/file?
2. Which **actual concrete scaffold seam** (path, interface, schema, test harness, config, ownership boundary) must exist for an unfamiliar Agent to execute the Task without ad hoc architecture invention?
3. Does enriching the scaffold now **reduce** foreseeable interface disagreement, shared-writer collision or downstream rework enough to justify its added cost? If not, leave the detail to L3/Task implementation.
4. Is the new seam already supported by Frozen L2? If not, refer to Architecture owner; material Product/L2 changes cannot be silently imported as a bootstrap convenience.
5. Do scaffold/source and draft Task acceptance now agree? Record mismatches and fix boundedly, avoiding circular "Task cannot be planned until fully implemented" claims.

**Allow gradual detail, not gradual fake implementation:** type/interface/API contract, minimal package tree, import/export, named module owner, dummy/no-op adapter that explicitly reports `NOT_IMPLEMENTED`, minimal test runner, generator provenance, dependency/lockfile, clean build instructions and known external Host prerequisites. Feature behavior should remain for post-freeze Tasks unless absolutely necessary to prove **scaffold structure**, and any required real executable pre-freeze behavior must be explicitly within Bootstrap authorized concern rather than silently hidden.

### S.4 Paired Freeze — acceptance contract and identities

At **one coordinated planning checkpoint**, the pair must be proven mutually consistent; conceptual "same-time freeze" does **not** require unsafe simultaneous GitHub writes or pretending two different SHAs are identical. The accepted source snapshot is **integrated on the authorized version branch**, with immutable commit/tree identity; the frozen DAG has its own exact revision pointing to that source. If both can be checkpointed in one safe commit under legitimate merge governance, fine; otherwise pin the explicit ordered pair.

Minimal acceptance:
- **Exact pins**: Product Freeze, L2 Freeze, repository/branch/source commit/tree, dependency & lock versions where material, scaffold validation evidence exact subject, planning DAG checkpoint/hash and current owner.
- **Inventory match**: every planned independently dispatchable Task identifies the owned module/contracts/write-set and known interfaces/test commands in the scaffold, or an explicit lawful Task-owned future seam not yet created; no orphan scaffold promises that silently count as implemented.
- **Dependency correctness**: true blocked-by relationships, cross-owner shared contracts, central wiring Task, atomic safety invariants and legitimate independent parallelism; no circular dependency caused by provisional scaffold notes.
- **Implementation absence truth**: interface stub that throws or intentionally fails cannot satisfy Task/feature PASS. Track intentionally missing implementations and the Task(s) that will own them, distinguishing schema/compile smoke from behavior, real host and Release.
- **Reproducibility**: applicable build/import/contract/negative-smoke executed on declared eligible environment with source/evidence identity, truthful `NOT_RUN` where required Host unavailable. High-risk mandatory proof may remain a legitimate downstream Task/Version responsibility **only if** its owner allows deferral and no bootstrap claim asserts it passed.
- **Independent authority**: acceptance is a bounded bootstrap/current-source check + regular Task DAG planning Freeze under existing applicable policy, **not** a newly minted "scaffold Product Freeze". Frozen DAG/Task Packs consume the integrated scaffold and preserve Product/L2 authority hierarchy.
- **Readback**: before materializing Issues, re-read accepted paired identities and validate source/contract/DAG concordance. If drift or ambiguity, rebind or hold impacted dependent tasks rather than issuing READY from stale draft.

DAG-planning closeout **and** scaffold baseline completion are one program-level convergence objective; until both are satisfied, `IMPLEMENTATION_DAG_FREEZE=NO`. Do not block forever on optional scaffold polish that has no material Task/contract consumer; unknown mandatory architecture constraint remains blocking under the actual existing owner.

### S.5 Post-Freeze implementation and change response

Downstream tasks must consume **actual accepted scaffold source**, rather than re-specifying the build/run/contract conventions:
`PRODUCT_REF + L2_REF + SCAFFOLD_SHA/TREE + DAG_CHECKPOINT + TASK_ID + OWNED_CONTRACTS + ALLOWED_WRITESET + DEPENDENCIES + REQUIRED_L3/TEST/GATES + INTEGRATION_OWNER`.

Task size remains **one coherent independently valid concern**, not mechanically one API endpoint/TypeScript interface; Tasks for tests, migration, adaptation and central wiring can legitimately consume or evolve interfaces within authorized scope.

Post-Freeze edit classification:
- `PRIVATE_IMPLEMENTATION`: same contract and scoped behavior → current normal Task/concern test; **no blanket HIGH_ASSURANCE**.
- `OWNED_INTERNAL_SEAM`: internal change with bounded consumers → scoped rebind/tests, Task Pack/DAG mutation when material; Architect only if L2 invariant changes.
- `SHARED_CONTRACT_CHANGE`: changed public schema/API/error semantics/shared invariant → actual L2/compatibility amendment, affected consumer Task DAG and evidence impacts, risk-required review/tests; no unapproved Builder schema drift.
- `HIGH_CONSEQUENCE`: security/permission/data integrity/irreversible effects/human DENY/major migration → **HIGH_ASSURANCE** for applicable mandatory evidence **plus** owning Product/L2 change authority as appropriate.
- `PRODUCT_SCOPE_CHANGE`: Product amendment/thaw and affected L2/scaffold/Task reprojection before continued work.

**HIGH_ASSURANCE remains assurance depth, not permission to edit Frozen contract.** Any scaffolding baseline changes after freeze are ordinary governed source/contract changes with currentness propagation; do not invalidate all unaffected code/evidence by default.

### S.6 Adversarial examples for co-evolution (candidate negative tests)

| ID | Attempted failure | Required outcome |
|---|---|---|
| SC15 | Implementation DAG draft appears first, then scaffold code changes while planning agent declares full DAG frozen | No freeze until source accepted and paired identities read back |
| SC16 | Scaffold grows to include full feature logic because planners want "100% runnable" Task templates | Bound to structural/contract concern, postpone behavior to feature Tasks; no hidden pre-DAG feature implementation |
| SC17 | Two planning/Bootstrap Agents simultaneously edit a shared manifest and public contracts | One source writer under valid Claim; route conflicts through current owner |
| SC18 | Scaffold compiles after inserting false-returning stubs; controller marks all corresponding Tasks DONE | Structure-only smoke, feature tasks remain unimplemented |
| SC19 | Planning draft references interface schema V2, but merged scaffold contains V1 | Hold DAG Freeze; bind matching exact sources and truthfully migrate/repair |
| SC20 | Repeated draft iterations make 30 empty PRs/issues with no new decision predicate | Budget/stop-loss; batch coherent bootstrap edits and minimize ceremony |
| SC21 | Project pinned to v4.11 uses "new v4.12 Product direction" to write pre-DAG code | Prohibit, use old legal T00 DAG path or adopt future frozen rule prospectively |
| SC22 | After Freeze, Worker silently edits cross-agent public API as a "quick fix" | Shared contract owner and affected consumers re-evaluation; cannot rely on stronger testing alone |
| SC23 | Scaffold branch remains unmerged, but Task DAG bound to local unverified HEAD | Freeze not authorized until accepted integrated exact SHA/current source |
| SC24 | Mature project with stable build receives complete rewrite under "generate once" | Reuse and minimally enrich existing project; no destructive recreation |
| SC25 | A newly added adapter stub requires absent real E3 platform proof, but baseline CI is green | No E3 promotion; required applicable real proof remains NOT_RUN/blocked/deferred only by owner |
| SC26 | During paired Freeze, late mandatory auth invariant reveals current architecture incomplete | Reopen/resolve actual L2 authority; no scaffold-only policy override or fake freeze |

### S.7 Product decisions and remaining engineering placement

**Chosen prospective v4.12 Product behavior:**
```ini
NEW_PROJECT_SCAFFOLD_CREATION_IN_PLANNING=ALLOWED_IN_BOUNDED_SCOPE
BOOTSTRAP_EXTRA_HUMAN_APPROVAL_GATE=NO
SCAFFOLD_BEFORE_FULL_DAG_FREEZE=YES
SCAFFOLD_AND_DAG_DRAFT_COEVOLVE=YES
PAIRED_BASELINE_AT_DAG_FREEZE=YES
SCAFFOLD_TASK_MAPPING=GITHUB_SOURCED_TYPED_MANY_TO_MANY
SCAFFOLD_MAPPING_REVERSE_VIEW=DETERMINISTICALLY_DERIVED
SCAFFOLD_DETAIL=PROJECT_SPECIFIC
AFTER_FREEZE_TASKS_CONSUME_SCAFFOLD=YES
EXISTING_V411_PIN_MUTATION=NO
```

**Decided baseline representation / generation / validation (Product v0.1):** Store actual Scaffold source, anchor IDs and Task DAG `scaffold_bindings` under GitHub Git objects and repository planning paths; generate both read views from **one** relation set; deterministic V01–V12 consistency checks and stable paired `(scaffold source scope/tree, DAG checkpoint, mapping ref)` identity. Existing GitHub native Issue Dependencies remain the *post-freeze live execution graph*; mapping relationships never grant their own execution authority. See [Initial Policy Decisions v0.1](V412_INITIAL_POLICY_DECISIONS_V01.md) §D02.

**Only L2 technical placement remains:** exact minimal reuse of existing Task DAG/Task Pack/manifest metadata rather than a forced new JSON schema; scaffold source writer/branch evidence under current Work Item/GitHub owner; accepted subtree/tree currentness across docs-only DAG commits; deterministic generator/checker implementation and fixtures; verified policy reconciliation for projects already pinned to v4.11. These are **implementation details**, not reopened Product decisions.

**No additional fourth DAG, no new independent scaffold authority, no mandatory HIGH_ASSURANCE for all edits or one-interface-per-Task decomposition.** Authentic contract changes, real-risk behavior, native dependencies and current required Release/Validation floors retain their existing original owners.

### S.8 Bidirectional scaffold ↔ Implementation Task DAG traceability (Product direction candidate, not a new authority)

**Decision:** The paired Scaffold Baseline and Implementation Task DAG SHOULD be **mutually traceable through a typed, source-bound many-to-many relation** while they co-evolve, and pairwise consistency SHOULD be a material freeze acceptance fact. **Mutual mapping != equivalence or one-to-one file/interface/Task assignment**. Scaffold is *project structure and contracts*; DAG is *authorized execution concerns/dependencies and acceptance*. Only L2 owns architecture facts; only frozen implementation planning/Task owners own Task boundaries and native live dependency semantics. Reverse lookup cannot rewrite either owner automatically.

#### S.8.1 Mapping cardinality and semantic relation types

Define the smallest useful conceptual index, not a second manually maintained truth DB:

```text
S = ScaffoldAnchor {
  anchor_id, repo_ref, artifact_path_or_contract_id, kind,
  scaffold_source_ref, lifecycle(existing|structural_stub|planned_future),
  bound_architecture_contract_ref, surface_owner_ref
}
T = ImplementationConcern {
  task_id, frozen_dag_ref, product_ref, l2_ref,
  primary_goal_and_acceptance, task_owner, required_tests,
  allowed_write_scope, required_consumer_contracts
}
M = Relation {
  scaffold_anchor_id, task_id,
  type(IMPLEMENTS|CREATES|MODIFIES|CONSUMES|TESTS|INTEGRATES),
  authority_ref, scope, currentness_ref
}
```

Names are **illustrative L2 projections**, not a new required schema or event vocabulary. Source project/actual code identities and GitHub current Task DAG dependency data remain native canonical authorities. A small versioned Markdown mapping, references in existing Task Packs/contracts, or generated source-index **all qualify** when grounded, cheap and reproducible. Avoid two writable copies of a mapping.

Valid cardinalities:
- **One Task → several anchors:** a coherent Runtime concern implements a type, runtime function, contract tests and packaging seam.
- **One anchor → several Task links:** a shared API is **consumed** by Runtime/UI/Adapter and **tested** by Validation, while exactly one authorized change/integration owner handles incompatible mutations for the given current scope.
- **Zero code anchors:** a Task may plan audit/validation/human evidence that creates no new code path; it still references the applicable contract/test subject.
- **Future anchor:** a Task may own a declared future module that does not exist in scaffold source yet, explicitly `planned_future` and `NOT_IMPLEMENTED`, without fabricating a path/compiled proof.
- **Scaffold-owned anchor:** existing dependency/CI/generated/bootstrap-only files may be governed by L2/integration/bootstrap ownership with **no feature implementation Task**, provided the provenance/owner is explicit.
- **Structural relation ≠ task dependency:** a module import or API consumer link is not automatically a canonical GitHub `blocked_by` edge. Genuine blocked-by arises only from required integrated predecessor results/architecture/Task governance.

#### S.8.2 Practical two-way lookup, not automatic scope authority

```text
Task → anchors
  implemented/created/modified paths + concrete contracts
  read-only dependency anchors + focused test/negative-proof anchors
  allowed/forbidden writes + integration owner

Anchor → Tasks
  authorized write/change owner(s) by scope/time and status
  implementation Task(s), consumers, test/validation owner
  feature currently unimplemented vs structurally present
```

The mapper MAY signal: `TASK_HAS_NO_CONCRETE_BOUNDARY`, `CONTRACT_WITH_NO_CLEAR_CONSUMER`, `UNOWNED_MUTABLE_SURFACE`, `SHARED_WRITE_COLLISION`, `SCHEMA_OR_DAG_REF_STALE`, `ORPHAN_UNIMPLEMENTED_STUB`. These are **diagnostic findings**; they are not a new workflow status, authoritative Gate FAIL, forced Task split, automatic blocker or source-edit authorization. A graph checker never creates/removes GitHub native Issue Dependencies or changes Frozen L2 by inferring ownership from file paths.

#### S.8.3 Co-evolution procedure and paired freeze consistency

1. L2 Freeze → initial bounded scaffold authority and S0 structure, then Draft DAG D0.
2. For each *material* planned Task, link the Task to an existing actual scaffold anchor, a contract-/module-level owner, or one explicitly declared **future seam**. Identify what is changed vs merely consumed, and validation acceptance.
3. When a genuine new boundary appears, update the Draft DAG *and* lawful bounded scaffold source as applicable. Each real scaffold code change has an accepted Bootstrap Claim/write set and exact current source; a draft Task is never permission to write.
4. Reverse scan only **material** scaffold anchors—public contracts, shared mutable wiring, critical test/build entrypoints, intentional stubs, exposed adapters—to ensure each has a declared responsible Task or baseline owner and all critical consumers. Do not require mapping every symbol or generated line.
5. Detect and address: interface signature/type mismatch; incompatible Task write ownership; unimplemented placeholder without future Task/proof; Task acceptance missing required negative/integration proof; unjustified dependency and deadlock; unauthorized scope change.
6. Freeze one accepted **pair** `{SCAFFOLD_SOURCE_SHA/TREE, DAG_CHECKPOINT, MAPPING_CHECKPOINT_OR_DERIVATION, PRODUCT_FREEZE_REF, L2_FREEZE_REF}`. Mapping snapshot is a *consistency/provenance projection*, not a separate third freeze/gate authority. Two source commits need not have identical SHA; exact ordered identities must resolve.
7. After freeze, implementation Task Packs consume this snapshot. Changes to source/contracts or Task topology use their **existing** authorized amendment/currentness rules; recompute only affected map links and legally impacted Tasks/Validation. A post-freeze Task may legitimately create new private source files within its write set; requiring every future file in the original scaffold is an anti-pattern.

**Minimal pairwise validation predicates (risk-weighted, not automatic per-file bureaucracy):**

```text
P1  every material planned Task has a resolvable concern/contract/future-seam ref
P2  every material public/shared scaffold seam has accountable ownership and consumer/test routing
P3  incompatible shared-mutating Task write sets are serialized or assigned explicit integration ownership
P4  frozen L2 public contract meaning and mapped scaffold types/fixtures do not contradict
P5  each material unimplemented placeholder stays NOT_IMPLEMENTED and maps to intended owner/required verification
P6  mapping points at the accepted exact scaffold source and frozen DAG checkpoint, not a stray local head
P7  reverse consumer/test links never imply GitHub blocked-by or Gate PASS without own accepted authority
```

Unknown or contradictory **material** P1–P7 prevents claim of paired planning consistency under its existing owning source; unrelated trivial/generated files may be unmapped. For a low-risk Fast Path, a compact Task→existing-code-and-test reference can be the entire mapping. No new universal mapping microservice, mandatory per-interface Issue or eager full-codebase analyzer.

#### S.8.4 Concrete illustration

```text
Scaffold:
  contracts/runtime-api.ts   [PUBLIC_CONTRACT; owner=L2/Contract]
  runtime/engine.ts          [STRUCTURAL_STUB; owner=Runtime]
  adapters/host.ts           [STRUCTURAL_STUB; owner=Adapter]
  app/composition.ts         [SHARED_WIRING; owner=Integration]
  tests/runtime.test.ts      [TEST_ENTRY; owner=Runtime/Validation]

DAG:
  T01 Runtime Core      IMPLEMENTS engine.ts; CONSUMES runtime-api.ts;
                        TESTS runtime.test.ts
  T02 Host Adapter      IMPLEMENTS host.ts; CONSUMES runtime-api.ts
  T03 Integration       INTEGRATES composition.ts; CONSUMES T01/T02
  T04 Validation        TESTS critical behavior via tests/; no mandatory interface creation

Reverse: runtime-api.ts → T01,T02 (consumers), T03 (integration), T04 (validation)
but it has one bounded public-contract change owner; `T01,T02` are not automatically a `blocked_by` relation merely because both import it.
```

#### S.8.5 Adversarial negative tests (candidate only)

| ID | Challenge | Correct result |
|---|---|---|
| BM01 | Planner infers one Task per interface/file and 80 artificial tasks | Reject cardinality rule, preserve coherent concern and real dependencies |
| BM02 | T01/T02 both write `app/composition.ts` claiming independent adapter implementation | Shared write collision, explicit integration owner or serialization |
| BM03 | One public contract is consumed by six Tasks; mapper assigns six equal contract-edit owners | Distinguish CONSUMES from MODIFIES and current legitimate write/contract owner |
| BM04 | Future extension does not yet have a source file so planning claims it complete | Explicit future seam/NOT_IMPLEMENTED, actual implementation later |
| BM05 | Bootstrap-only lockfile/readme lacks a feature Task | Owner/provenance known, no synthetic feature Task needed |
| BM06 | Path import automatically converted into GitHub blocked-by | Reject structural-link-to-Task-dependency promotion without owning proof |
| BM07 | Frozen DAG pins source `abc`, mapping pins unmerged scaffold `def` | Pair invalid/stale; current source readback required |
| BM08 | CI compiles 20 empty public stubs so mapper records 20 finished Tasks | Structure smoke only, feature acceptance unproven |
| BM09 | Task concerns are valid but public contract mismatches actual scaffold schema | Paired freeze held for material mismatch, no hidden contract drift |
| BM10 | After Freeze legitimate Runtime Task creates two internal files not in S0 | Allow under Task write-set; update affected projection, do not demand new Product/L2 freeze |
| BM11 | Reviewer claims mapped test path ensures test was executed on exact SHA | Mapping is routing only; actual Validation owner evidence still needed |
| BM12 | Auto-mapper sees a new module and self-creates a Task/changes Task DAG edge | Advisory only, authority-owned DAG mutation required |

### S.8.6 Unresolved implementation specifics

L2 must choose the lightest durable linkage (existing Task Pack/manifest/README or generated index), granularity (contract/module/test first), anchor identities on files renames/moves, acceptable manual A0/A1 projection, checker ownership/negative fixtures, currentness composition and handling of generated dependencies. These are **implementation/projection choices** not additional Product feature families. Pairwise mapping remains subordinate to already Frozen Product/L2 and current Task DAG/Claim/Validation authorities.
