# ADS v4.11.0 — Version Task DAG v0.3 (R2-F07 REPAIR CANDIDATE, NOT FROZEN)

> This document is a **static planning checkpoint** only. It is neither the live GitHub execution DAG, a Task Pack, Task/Claim admission, actual implementation, Release Qualification, nor a second workflow-state authority. The immutable current live Task DAG, after authorized materialization, will be **GitHub Task Issues + native Issue Dependencies**. Changes to execution status belong there, never in this file.

```ini
REPOSITORY=kaicreator-mm/ai-development-standard
VERSION=4.11.0
PRODUCT_FREEZE=#943@6084264198
PRODUCT_COMMIT=34df09a2433aec5523ab80c90e885f6d9fc78803
PRODUCT_PRD_BLOB=d30f202e8ea662731ff8a4f2ad1ad88cfc5bb179
PRODUCT_MATRIX_BLOB=f59a6daf5430ece66103a830e392a04f71623ff0
L2_FREEZE=#954
L2_CONTROLLER_EVENT=#947@6093870964
L2_EXACT_COMMIT=f1fc21be366579cbeafa98217b52e106a55b41a5
L2_EXACT_TREE=54d9e20832fbfe47d1154212932c336c71e13a30
L2_BLOB=c0fa361474996a0626c63e93574a284ae3eb8d91
FRESH_L2_REVIEW=#953@6093710027 PASS
PREDECESSOR_V410_MAIN=b9461d48d902a2c7c00adff6746afc7a02a0ac3e
DAG_STATUS=v0.2_DRAFT_R1_CHANGES_REQUESTED_REPAIRED_NEW_INDEPENDENT_REVIEW_REQUIRED
R1_INDEPENDENT_DAG_REVIEW=#957@6094077245_CHANGES_REQUESTED_P1_3_P2_3
R1_REVIEWED_DAG_HEAD=dc563e3a29da92406f7a91d9226e1277fcae8035
R1_REVIEWED_DAG_BLOB=e3ef5caf7ed25e4a88c48a5a17d424c423b4a3fb
DAG_FREEZE=NO
NATIVE_ISSUES_AND_DEPENDENCIES=NOT_MATERIALIZED
TASK_PACKS=NOT_AUTHORIZED
STAGE3_IMPLEMENTATION=NOT_AUTHORIZED
V411_VERSION_BRANCH=NOT_CREATED
```

## 1. Planning rules and evidence model

- **One concern, one PR**; Task boundary is a genuine indivisible authority/validation contract, not file count, category labels or developer time estimate.
- Follow `standards/TASK_DECOMPOSITION_STANDARD.md`, `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `TASK_DAG_GOVERNANCE_STANDARD.md`, `VALIDATION_STANDARD.md`, `RELEASE_STANDARD.md` and `ISSUE_FIRST_TASK_TRIGGER.md` from the qualified exact v4.10 owner baseline. Use later qualified `main` only after fresh currentness rebind; no accidental introduction of frozen Product/L2 prep ancestry as implementation code baseline.
- **All six mandatory v4.11 Product ship concerns remain actual owner/test delivery**, not assessment-only. A = individual Agent engineer conduct; B = full multi-Agent interaction with scheduler as only one part; C = non-weakening cross-agent composition. Keep accepted J05 spec vs current implementation, J12 Reuse-First exact source/license evolution, effective-rule/profile trace, unsafe effect handling, human DENY, review conflict, and executable whole-version A/B/C proof.
- Every Implementation Task later needs a complete Task Issue/Task Pack (goal, exact frozen inputs, output, allowed write set and forbidden scope, tests, acceptance, risk/review policy, current base and dependencies, failure handling and merge rules). No Builder work before canonical GitHub Issue dependencies + current Task Pack and protected accepted claim.
- Role actor validation and Review are **separate**. PR-local CI or self-review does not constitute formal real Build Host, Hidden, Release or Fresh independent proof. Conformance fixtures S01–S18 and X01–X08 must bind to canonical owners and include negative and untested material compound cases, without fabricated universal completeness.

## 2. Proposed executable leaves — source-owned, 20 separately dispatchable nodes

**Write-set contract (R1-F04/F05):** Before a Task Pack becomes executable, resolve exact paths and glob matches on the then-current qualified implementation baseline. Owner-local Tasks T01–T10/T13/T14 may edit only the **named normative owner path(s)** and dedicated `scripts/test_v411_<concern>.py` or equivalent *unique* new focused test path within their Task Pack. Shared `schemas/**`, `templates/**`, `standard-manifest.json`, generic verifier, shared `templates/GOLDEN_INDEX.md` and `checklists/version-closure.md` are **READ ONLY** to every owner-local Task, exclusively writable by **T11** after all contracts have landed. Existing owner Schema v1/v2 compatibility MUST remain enforceable pending T11; if a Task cannot establish its owner-local behavior without modifying a centrally owned schema, it records a proposed additive schema change for T11 and returns a current failing-focused verification/blocked integration note rather than secretly mutating a shared contract or claiming integrated PASS. A Task may not create an ambiguous schema shadow file.

| ID | One coherent primary invariant / outcome | Allowed normative / artifact write ownership (plus UNIQUE focused test) | True predecessors | Focused acceptance + negative evidence | Risk / Review |
| --- | --- | --- | --- | --- | --- |
| **V411-T01** | Pinned effective-rule/profile/multi-J AND provenance, UNKNOWN and non-weakening floor | `standards/PROJECT_ADOPTION.md`; `standards/DEVELOPMENT_WORKFLOW.md` **effective-rule section only**; no shared schema/template/manifest | none | A0–A4 same hard floor, J03+J06+J07+J08 compound, unknown material risk and conflicting source priority fail closed | high / required |
| **V411-T02** | Affected-source materiality inventory and inspected-ABSENT vs uninspected UNKNOWN | `standards/DEVELOPMENT_WORKFLOW.md` **risk-intake section only**; owner-local change-provenance tests; central Task template read-only | T01 | Real diff permission/API/deployment changed with J02/no label → BLOCKED; actual source/HEAD/currentness test | high / required |
| **V411-T03** | J05 accepted-spec delta vs actually shipped contract and changed consumer currentness | `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` only; local compatibility tests; additive schema proposal handed to T11 | none | Archive or approved spec alone never certifies implementation, producer/consumer drift invalidates old compatibility claim | medium / required |
| **V411-T04** | J12 Reuse-First H1/H2/H3/BUILD_NEW, exact upstream source/license/provenance | `standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md`, `standards/ARCHITECTURE_DESIGN_STANDARD.md`; distinct owner-local tests; task template proposals → T11 | none | Changed upstream license/source invalidates old H3; cited alternatives/tradeoffs and bounded lawful reuse or new build | medium / required |
| **V411-T05** | One canonical accepted GitHub Agent event, human/Review provenance and current event authority | `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` **accepted-event/Review authority section** only, distinct local tests; `schemas/**` read-only | none | Real logical operator vs shared transport, quote/injected approval cannot acquire rights, current accepted Review/decision boundaries | high / required |
| **V411-T06** | Atomic protected Claim / Dispatch and lawful unclaimed WEB→fresh LOCAL reroute | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` **Claim/Dispatch §§27–28** only, source-specific tests; T05 Interaction owner read-only | T05 | Duplicate protected keys, stale generations, no stolen claim, multi-resource all-or-none, legal wake/drain | high / required |
| **V411-T07** | Merge Controller last-admission exact-state sweep and guarded merge readiness | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` **§14 Merge Controller** and subordinate merge-admission procedures, existing shared `scripts/test_execution_architecture.py` **READ ONLY** (all proposed common-suite edits are handed to exclusive T11), and uniquely owned `scripts/test_v411_merge_admission.py`; `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` and native review/event Schemas **READ ONLY** | T05,T06 | PR/native Reviews, linked Task/Review/Validation, stale-head vs same-head current P1, post-sweep late blocker/watermark/pagination failures and exact-head merge recheck; no fictitious atomic GitHub snapshot | high / required |
| **V411-T08** | Human authority decision provenance and lawful DENY/WITHHOLD/supersession contract, **without side-effect execution** | `standards/DEVELOPMENT_WORKFLOW.md` **human authority section only** + dedicated human-provenance contract tests; Interaction/Execution/External owners read-only | T02,T05,T06,T13 | Independently source-bound actual human/delegation authorization, exact subject/scope, stale/quoted/forged approvals blocked, successor B READY cannot supplant DENY; **no sink-counter or effect-phase PASS claimed** | critical / required |
| **V411-T09** | Irreversible effect guard and lost-ACK reconciliation under existing external-system owner | `standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md`, `standards/DATA_MIGRATION_GOVERNANCE_STANDARD.md` **effect/recovery clauses only** + focused real-boundary safe sink tests; Workflow/Interaction and Execution §§14/27–28 read-only | T08 | **At the actual effect boundary** re-fetch authoritative current human DENY on an *already-CLAIMED A* before sink mutation; `A CLAIMED→valid DENY→A effect` must BLOCK with observable mutation count 0; B READY→DENY blocked. Also ACK unknown HOLD and externally grounded dedup/reconciliation and authorized compensation. Local #949 E2 not human-auth, remote/multi-host NOT_RUN unless actual integration test | critical / required |
| **V411-T10** | Untrusted tool/GitHub/MCP/A2A data cannot grant authority or leak credentials | `standards/CONFIGURATION_SECRETS_STANDARD.md`, `standards/WORKSPACE_ARTIFACT_STANDARD.md`; isolated trust/redaction tests | none | Fake owner/subagent, policy-override text, secret-bearing tool messages rejected, transport authentication ≠ content authority | high / required |
| **V411-T13** | **R02** role-scoped individual engineering conduct `Input→Allowed acts→Required evidence→Handoff/Exit` | `standards/DEVELOPMENT_WORKFLOW.md` **role-conduct section**, `standards/TASK_DECOMPOSITION_STANDARD.md` **role/Task entry requirements** and uniquely scoped positive/negative owner-local tests; T01/T02 owner sections frozen/read-only | T02 | Agent role/job/profile/archetype choices require legal input/mutation/evidence/exit, WEB cannot assert real host, builder cannot self-award Fresh review; low-risk A0 stays proportional, unsupported role/class fail closed | high / required |
| **V411-T14** | **R11** bounded factual Task Learning, source/currentness/epistemic strength and later-work consumption | Canonical `standards/EXECUTION_ARCHITECTURE_STANDARD.md` **Task Learning evidence owner section** plus `references/TASK_LEARNING_V2_REFERENCE.md` and uniquely scoped `scripts/test_v411_task_learning.py`; existing v1/v2 Schemas, `scripts/test_v49_task_learning_v2.py` and manifest read-only | T07 | Real cited source/current subject, factual confidence vs unsupported inferred lesson, stale/forged private deliberation rejected, use later only as subordinate evidence not Product/L2/Task mutation authority; positive AND negative. `ALREADY_SATISFIED` only if exact production source+current executable tests prove full R11 equivalence, else implement missing owner-local semantics | medium / required |
| **V411-T11** | Single converge/wiring owner: schemas, templates, manifest, verifier and current gate projections | **EXCLUSIVE** `schemas/**`, `templates/**`, `standard-manifest.json`, `scripts/verify_standard.py`, `templates/GOLDEN_INDEX.md`, shared gate wiring tests; no rewriting siblings' normative content | T01,T02,T03,T04,T05,T06,T07,T08,T09,T10,T13,T14 | All declared owner-local schema requests reconciled exactly once, v1/v2 reader compatibility, manifest/owner/schema/template/prose parity, missing mandatory fact fail closed | high / required |
| **V411-T12** | Integrated A+B+C executable conformance rather than a synthetic rule model | Dedicated version golden fixture and conformance test registration, **after** T11; no concurrent central schema/manifest writes | T11 | S01–S18 + X01–X08, Library/Service/CLI, NEW/BROWNFIELD, A0–A4 and J09+J10+J11+J12 fail-closed; true A CLAIMED→verified DENY→A irreversible effect prevented in admissible environment; bounded actual source/authority/actor/host evidence | critical / required |
| **V411-V01** | **Independent** dependency-complete visible Validation/Closure of exact candidate, not Task PR CI | Validator owns exact tuple, visible full regression, Critical Journeys, real host and platform/build/package/install/external/CI/profile gates **per Release owner gate×exact-subject applicability** plus architecture/docs reconciliation and closure inventory evidence; implementation source read-only | T12 | Exact SHA/tree; positive REQUIRED_NOW/DEFERRED/NOT_APPLICABLE proof and UNKNOWN/BLOCKED when missing; applicable production build, artifact packaging/install, external tenant/effect evidence or grounded not-applicable; permitted CI waiver *only by owning policy*; no fake Release PASS | critical / required |
| **V411-V02** | **Candidate Freeze only**: release owner admits immutable exact candidate | Release/Candidate Controller owns freeze identity and visible gate snapshot, not validation source or private pack | V01 | Eligible exact candidate SHA/tree/ref+standard revision+visibility tuple current, docs reconciliation and no unresolved required closure gate; new content invalidates freeze | critical / required |
| **V411-V03** | **Formal Hidden Validation only** on frozen candidate | Independent Hidden Validator owns private immutable pack identity/checksum, isolated run and public-safe verdict; pack bytes never placed in public GitHub | V02 | Exact frozen SHA/ref/tree and true private fixture execution, blind spot/pack defect classification, zero leaked Hidden vectors; blocked/unavailable declared NOT_RUN | critical / required |
| **V411-V04** | **Genuinely Fresh Final Closeout** of frozen/Hidden-evidenced candidate | Separate Fresh Closeout Reviewer owns current full-version gate inventory and independent findings, not source/Hidden builder | V03 | Full visible+Hidden/critical journeys/gate×subject applicable truth and escaped-defect/blind-spot disposition, no inherited Task PASS→version PASS | critical / required |
| **V411-R01** | **Independent Release Qualification** on same exact candidate and authoritative closure | Fresh RQ actor owns release verdict and disposition, no repo integration/write | V04 | Release §6 READY/CONDITIONAL/BLOCKED/FAIL; exact candidate & freeze+Hidden+Fresh evidence, authorized limitations and material UNKNOWN cannot be hidden | critical / required |
| **V411-R02** | **Guarded Repository Integration** on qualified release | Distinct repository-integrator actor owns re-read main/candidate, expected-head legal merge, final-main exact validation/baseline and optional tag alias | R01 | RQ READY or owner-admitted qualifying verdict, exact main drift/recheck, qualified source only, final merged tree sanity, immutable baseline/ref/tag identity; no tag as substitute for Git SHA | critical / required |

**Owned completion boundary:** A Task is not `done` until its focused owner-local semantics are supported by actual validation on its exact PR and required independent Review; tests that need later T11 Schema or T12 integrated runtime are labelled `DEFERRED_TO_T11/T12` **with explicit owner and gate**, never promoted to whole-version PASS. T09's irreversible-boundary evidence is implementation-owner local; T12/V01 verify composition and actual host/authority at integrated scale. V01/V02/V03/V04/R01/R02 are **six distinct native work items with different actors and own terminal states** and are not bundled in one Issue.

## 3. Exact dependency topology, write collision proof and safe parallelism

```text
Initial independent owner concerns: T01 | T03 | T04 | T05 | T10
T01 → T02 → T13
T05 → T06 → T07 → T14
T02 + T05 + T06 + T13 → T08 → T09
T05 + T06 → T07 (T07 follows T06's Execution §27 edit before §14 edit)
T01..T10 + T13 + T14 → T11 (exclusive schema/template/manifest)
T11 → T12 → V01 → V02(Candidate Freeze) → V03(Hidden)
    → V04(Fresh Final Closeout) → R01(Independent RQ) → R02(Repository Integration)
```

**Exact predecessors** are the ones in §2. `T13` follows T02 because both own distinct *sequential* sections of `DEVELOPMENT_WORKFLOW.md`; `T08` also follows T13 for legal scope/human delegation owner cross-section. `T14` follows T07 because T06/T07/T14 touch different sections of `EXECUTION_ARCHITECTURE_STANDARD.md` and require ordered baselines. T07's Interaction reference is read-only. T09 owns External effect and observes the already accepted T08 human authority contract. Central T11 follows ALL owner-local concerns and is exclusive writer of every shared schema/template/manifest/verifier. It consumes schema proposals and cannot manufacture missing owner semantics. T12 consumes settled schema and owner integration. Stage actors get individual gate subjects and terminals; candidate/Hidden/Fresh/RQ/integration are distinct.

**R2-F07 shared test guard:** T07's `scripts/test_execution_architecture.py` is a pre-existing shared manifest-registered test and may ONLY be used as an observation/reference; any change to that shared test is an explicit T11 integration proposal after the owner-local T07 contract. T07 may write its unique `scripts/test_v411_merge_admission.py` only. A pending T11 common-suite edit cannot be used as evidence that T07 already passed full integrated verification; label that gate pending T11 and T12. This rule removes the contradictory "when serially owned" shared-script exception without a new node or fabricated dependency.

**Constrained parallelism:** The five first concerns T01/T03/T04/T05/T10 have **disjoint named normative paths** and **no `schemas/**`, `templates/**`, `standard-manifest.json`, shared verifier or shared test file write rights**. Concurrent work is legal only if JIT Task Packs confirm disjoint *actual* unique focused test paths and stable contract provenance on the current implementation baseline; overlaps are serialized, not “solved” by retrospective cherry-pick. Unknown current owner overlap leads to Task BLOCKED/clarification, not unsafe dispatch. No arbitrary T03↔T04 dependencies or stacks.

**Canonical materialization**: on DAG Freeze and separately authorized Task Pack preparation, each leaf maps to ONE native GitHub Issue with type/state/review/risk and native blocked-by edges. Markdown is immutable planning history; it cannot represent mutable readiness or claim identity. If connected actor lacks native dependency capability, local authorized API/CLI executor must create AND read back canonical edges; don't call written prose an admissible execution DAG.

## 4. Acceptance matrix: Frozen Product six ship concerns → accountable leaves

| Frozen requirement | Main implementation leaves | Mandatory negative proof location |
| --- | --- | --- |
| #1 Applicability + multi-label requirements | T01, T02, T11 | T12 X01/X08 plus S-cases; omitted labels, uninspected material risk, weaker A0 overrides |
| #2 Multi-Agent role/eligibility/interaction | T05, T06, T08, T13, T14 | T12 S08–S12/S15–S18; role-scoped conduct, source-backed Task Learning, duplicate Claim, wrongful delegation, reviewer reroute, DENY replay |
| #3 Dispatch/Review/Merge admission safety | T05, T06, T07 | T12 same-HEAD opposite accepted Reviews, late blocker/watermark update, incomplete GitHub readback |
| #4 Unsafe effect, cross-actor recovery, trust | T08 authority → T09 irreversible effect guard, T10 transport/secret boundary | T09 owner-local actual pre-effect DENY sink count 0; T12/V01 integrated A CLAIMED→verified DENY→A effect negative and U02 ACK/lost replay, no remote proof borrowed from research |
| #5 Selected OpenSpec/Spec Kit/Reuse-First assimilation | T01, T03, T04, T13, T14, T11 | T12 J05 accepted-vs-implemented and J12 changed upstream/license; R02 role practice and R11 Task Learning must have real positive/negative owner proof, not evidence-only |
| #6 P1/P2/P3 whole-version executable assurance | T11, T12, V01, V02, V03, V04, R01, R02 | S01–S18 + X01–X08, unexpected material intersections UNVERIFIED/BLOCKED; exact gate×subject visible closure, Candidate Freeze, real Hidden, independent Fresh, RQ and guarded main baseline |

The full Frozen PRD `§5` remains controlling if a summary row misses any sub-obligation. **Never call a new fixture suite universal proof**: the unknown intersection denominator must be stated, owners/equivalence currentness shown, and unverified material classes held.

## 5. Cross-cutting contract / Task Pack rules

1. Implementation task owner writes only its concern paths and directly owned focused tests; explicit read-set covers frozen Product, L2, required predecessor work, exact target branch baseline, existing owner source and accepted schema. No broad `main` overwrite.
2. A concern that needs another owner's public contract first must identify that concrete dependency and re-evaluate on live GitHub before dispatch. Stable frozen contract can permit non-overlapping parallel code, but two writers to `DEVELOPMENT_WORKFLOW.md`, `EXECUTION_ARCHITECTURE_STANDARD.md`, central schema or manifest must be serialized.
3. Every task includes Tests → Contract → Implementation → Failure Handling → References in its L3/Task Pack where required; locally validated PR-level success plus risk-derived Fresh review cannot turn into v4.11 Release PASS.
4. Non-normative research PR #946 (synthetic trace model) and #951 (local Git U02 demo) **never merge automatically** into implementation; reuse their negative scenario ideas only through legitimate owner/task contract and independent testing. #951's Draft main comparison is an unrelated large diff, not a 178-file intended implementation.
5. v4.10 main `b9461d48...` is qualified predecessor, but v4.11 planning branch descends from earlier frozen v4.10 candidate for Product/L2 exact proof. Before stage3 code branch, the controller must reconstruct a clean **v4.11 implementation baseline from current qualified main**, reintroducing only authorized frozen Product/L2/DAG artifacts as exact reviewed inputs with a safe integration plan. Do not merge the whole earlier planning ancestry into main or treat a tag name as a version evidence substitute.
6. No implementation branch/Task Pack/Task Issue is `ready` before official DAG Freeze and separate Task Pack/Issue/native-dependency admission. If GitHub native Issue dependency mutation is unavailable, record a capability BLOCKED/fallback according to `GITHUB_CAPABILITY_FALLBACK.md` rather than calling prose lists canonical.
7. v4.11 Product Freeze and L2 Freeze do not inherit v4.10 Hidden/RQ evidence or release verdict. Candidate and exact source proof must be re-executed for v4.11 with appropriate real environments.

## 6. Pre-freeze DAG review criteria

A genuinely fresh independent reviewer should challenge all 20 leaves for minimum coherent concern, dispatchability, risks and independent gate actors, exact owner/write-set overlap, J05/J12 non-assessment assimilation, dual-agent authority and human DENY post-Claim negative path, real GitHub-bound effect proof non-substitution, coverage of Frozen six ship concerns and S/X fixtures, safe initial concurrency, architecture placement, absence of unearned Task READY, no unauthorized version branch, and qualified predecessor main rebind.

Specifically check whether T05 is an overly broad "Interaction" authority concern and whether T06/T07/T08 simultaneous source changes would collide; split concerns or add source-derived legal dependency only if concretely necessary. V02 Candidate Freeze, V03 Hidden, V04 Fresh Final Closeout, R01 Independent RQ and R02 Repository Integration must remain separately owned native issues; an L3 executor must never collapse them into one actor/terminal. Ensure R02 conduct T13 and R11 source-bounded Task Learning T14 are delivered under existing owners and no local simulated human test counts as production authorization. Any material DAG revision requires a new exact doc commit and genuinely fresh review.

```ini
DAG_CANDIDATE_ONLY=YES
DAG_INDEPENDENT_REVIEW_R1=#957@6094077245_CHANGES_REQUESTED
DAG_R2_INDEPENDENT_REVIEW=#958@6094240273_CHANGES_REQUESTED_P2_1
DAG_R3_FRESH_REVIEW=NOT_RUN
DAG_FREEZE=NO
EXECUTION_ISSUES=NOT_MATERIALIZED
NATIVE_DEPENDENCIES=NOT_MATERIALIZED
TASK_PACKS=NOT_MATERIALIZED
STAGE3_SOURCE_MUTATION=NO
V411_RELEASE_INTEGRATION=NO
```
