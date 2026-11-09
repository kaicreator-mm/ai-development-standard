# ADS v4.19 — Integrated L2 Architecture R0 (proposed; not frozen)

**Status:** ARCHITECTURE_CANDIDATE / PRODUCT_FREEZE=NOT_RUN / L2_FREEZE=NOT_RUN / NO_TASK_ADMISSION  
**Input:** [Product/L1 independent-review candidate PR #1363](https://github.com/kaicreator-mm/ai-development-standard/pull/1363), HEAD `9d2962e07a44e6b76f61e8ff5d1f3a02d1b57e47`, Product blob `b776c09b341eb5fbdaeaf5aa98f4e2afbcd0ec9c`. The Product is review-qualified as a *candidate*, not Owner-frozen. This L2 is anticipatory architecture for review and must be rebound to an explicit lawful Product Freeze before any L2/DAG adoption or Task Claim.
**Existing exact frozen subjects:** #1353 Product `44562165...`, L2 `b82f201d...`, DAG `fbf1a7d...`; historically unchanged.

## 1. Architectural decision: additive three-domain responsibility model

ADS v4.19 is a compatible evolution of v4.18 rather than a new task scheduler. The three domains are **responsibility classifications for existing normative owners**:

| Domain | Decisions, evidence and existing owner | No new mechanism |
| --- | --- | --- |
| Task Execution Optimization & Management | `EXECUTION_ARCHITECTURE_STANDARD` (derived state/coordination), `EXECUTION_PACK_STANDARD` (Task/Execution Packs), Dispatch Schema + `v34_rules.py`, `VALIDATION_STANDARD`, `CI_EXECUTION_STANDARD`, `LOCAL_AGENT_HANDOFF_PROTOCOL`, `DEVELOPMENT_WORKFLOW` | No second Task status/Claim key/Writer queue; existing role-based authority and accepted write set still gate effects |
| Project Optimization & Management | `DEVELOPMENT_WORKFLOW` Stage 1/2, `TASK_DECOMPOSITION_STANDARD`, `ARCHITECTURE_DESIGN_STANDARD`, native GitHub DAG, `RELEASE_STANDARD` and integration owners | No new Project runtime or duplicate DAG; source/CI PASS does not close an Outcome |
| Experience & Feedback | Existing Task Learning v1/v2, Golden/Forbidden reference, execution evidence and source-qualified reviews; #1359/#1361 feedback | No second learning store, automatic normative promotion or per-Demo mandatory Issue |

For a normative change, the current standard owner remains exclusive; Product classification is not an alternative authority.

## 2. Execution Strategy: policy, mode and permission are different

### 2.1 General Delivery-First policy (reuses #1359, not new schema)

For any eligible Task, select the execution plan by **Task outcome + actual capability + justified total cost + required evidence/risks**. Local/remote/Web/CI are alternatives or compatible assignments, not sequential mandatory stops. Prefer continuous Writer/repair, minimal handoff, proportional verification and earliest legitimate DAG progress. Do not invent cost/time metrics; where measured values are absent use an explicitly provisional qualitative choice and record UNKNOWN.

`TotalCost = Web + Local + CI/Runner + Handoff + Rework + CriticalPathDelay + Risk` is a planning comparison, not a mandatory numerical score or JSON field. Real source-independent environmental requirements may dominate cheapest compute tokens.

### 2.2 Specific low-cost Web-primary mode (optional)

The mode `WEB_BUILDER` (role=builder, environment=WEB) may perform authorized source analysis, implementation, tests, repair and PR authorship. If actual required testing needs a local physical/browser/Host environment that Web or existing CI cannot truthfully satisfy, `LOCAL_VALIDATION` (role=validator, environment=LOCAL, exact requested HEAD) may provide **no-source-write validation**. Use CI before expensive Local if equivalent evidence is available; avoid redundant validation or repeated Web/Local ping-pong.

This is a **selectable mode** chosen where lower Web compute/agent cost genuinely offsets any handoff and repair cycle. It does not make Web-first a universal executor restriction for all Tasks.

### 2.3 Native Local Builder or hybrid mode

An existing `LOCAL_BUILDER` (role=builder, environment=LOCAL), or another lawful capable Builder, can be assigned a *new* Task when needed for physical OS/desktop/device/Host-dependent implementation and in-place repair, **only after its effective prospective frozen Product/Task Pack authorizes that selection and an accepted Builder Claim/Writer exists**. It is not the `LOCAL_VALIDATION` profile in disguise.

Hybrid/parallel work uses disjoint authorized write sets or serialized conflicting resources. A Validator never becomes a Builder by editing source after detecting failure. A Web or Local role label does not create protected Claim authority.

### 2.4 Proposed precise compatibility amendment (superseding only prospective global default)

The additive Dispatch mappings in #1358 are correct for both modes:
- New: `WEB_BUILDER → builder/WEB`, `LOCAL_VALIDATION → validator/LOCAL`.
- Retain unchanged: `LOCAL_BUILDER → builder/LOCAL`, `LOCAL_VALIDATOR → validator/LOCAL`, `WEB_REVIEWER → reviewer/WEB`, `PLATFORM_VALIDATOR` and `CLOSURE_VALIDATOR` environment-orthogonal.
- `execution_profile` / `execution_environment` remain provenance/routing; protected key remains repository + Task + role + compatibility group. No schema change to claim identity, role enum, new event family or lifecycle.

#1353's historical frozen global new-work Web default remains valid **for its historical subject**. A future v4.19 Task may select Local Builder based on cost/capability only after a **prospective Product Freeze and derived amended L2/DAG** legally supersede the default. No retroactive rewrite, automatic opt-in or source permission relaxation.

**Specific source delta, pending admission:** compare the *actual* T01 seven-path source against the current integrated preview before deciding precise prospective normative edits. The original `standards/EXECUTION_PACK_STANDARD.md` contains the historical global Web-default clause; the historical `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` contains role/profile inventory and admission prose, **not that same default clause**. PR #1365 already holds **proposed and unqualified** capability/cost selection prose in both files. A legally frozen **new** Product/L2/DAG authorizes only the necessary source-specific changes: the Pack's default, plus any Protocol inventory/admission wording proven to need alignment. Do not blanket-rewrite both texts, silently amend the frozen #1353 Task, change Claim identity or grant `LOCAL_VALIDATION` source-write. Both paths remain under T01's original seven-path source boundary; modified final SHA requires affected tests and independent review. This draft does not confer admission or approve the preview.

## 3. Project-level planning, demos, and progress

- Stage 1 Product Research may optionally use one **existing** master Issue + Git versioned Demo/evidence/revisions for multiple falsifiable questions, per #1361/#1362. Small adequate studies remain inline; r0/r1 does not create Product SemVer or automatically adopt Product. Stage 2 Architecture Research Demo retains its separate required Issue/branch/E1–E3 requirements and Product Freeze boundary.
- Native GitHub Issue dependencies remain the live DAG. Plan real prerequisite edges and shared Writer/Build artifacts, not false "integration must come first" source dependencies.
- A project progress numerator counts accepted/closed **Outcome Tasks**, not PR/Dispatch/Review activity; track issue/CI/integration/Host evidence separately. Only the owning transition can close a Task.
- A stall response identifies the earliest actual open native dependency or legitimate CI/Claim/Review/Host blocker, isolates unrelated lanes and advances eligible closure first.
- ADS owns common task-meta↔GitHub↔Tally contract semantics; task-meta produces execution facts, Tally consumes/coordin​ates workflow; providers and Host implement concrete adapters. Do not claim a genuine end-to-end run from a proposed contract.

## 4. Feedback and evidence

Reuse `Task Learning` / `Golden` / `VALIDATION` owners. Producer record may describe `OBSERVED`, `INFERRED`, `UNKNOWN` and `NOT_RUN` accurately; a new DKE semantic scripted PASS does not prove independent SAP authority, Host effect or v4.19 CI. Reusable insight requires source-bound original problem, counterfactual, cost if measured, applicable standard owner, qualification and actual adoption. Time saved without measured active time remains UNKNOWN.

## 5. Integration topology and single Writer

Existing candidates (no automatic adoption):
- Product R0: #1363 — standalone reviewed candidate, pending explicit Product Owner Freeze.
- T01: #1357 / PR #1358 — seven source+tests paths, immutable one-Task historical scope.
- Demo: #1361 / PR #1362 — four paths, Stage 1 optional evidence pattern.
- Issue Prevention: #1347 / PR #1342 — 17 paths, some normative changes still pending owner-qualified scope.

**One original concern-to-concern collision:** `standards/DEVELOPMENT_WORKFLOW.md` is shared by #1362 and #1342; a *single legitimate version integration Writer* must reconstruct latest `version/v4.19`, compose both Stage 1 and root-cause repair hunks, prove per-hunk provenance and test/review the final composed blob. Historical #1342 base=main is not authority to merge into main.

**Separate actual preview synchronization:** PR #1365 at HEAD `dac263fa4c0ab155406d2f2117459b34322cc988` also carries copies of **both this PR #1364 L2/DAG planning files** and the composed Workflow file. During the two-file review/repair, #1364 is the **only modifying owner for those L2/DAG source paths**; #1365's copies are derived/read-only preview evidence, not an independent competing Writer. A #1364 repair makes the preview copies **STALE**. Once exact Product/L2/DAG approval establishes legal integration ownership, one I01 version Writer must re-read the final #1364 HEAD/TREE and refresh only accepted final planning blobs into the integrated version; record old/new blob lineage, run affected final-SHA verification and required independent source review. This review does not modify #1365, create a new Task or grant a Claim.

**Independent frozen-vs-prospective execution:** the new capability/cost policy still requires prospective Product→L2→DAG approval. It does **not** suspend #1353's already frozen T01 seven-path implementation, its focused/full Python validation, explicitly required self-hosted Woodpecker or independent Review under its *existing* legal Task/Claim authority. Other lawfully authorized work may advance independently; only actual shared Writer resources and final integration join need serialization. Do not add an automatic Writer/Claim or broaden a frozen write set from this L2 draft.

## 6. Acceptance matrix (proposed)

| Scenario | Required observable judgment |
| --- | --- |
| Web-only Task; Local would bring no missing evidence | Select Web path; avoid redundant Local handoff |
| Windows/native capability required for both implementation + repair; legal new local-builder pack | Local Builder may complete continuously *after new prospective policy admission* |
| Current frozen #1353 default still governs Task | Respect historical Web-default restriction; no automatic Local qualification |
| `LOCAL_VALIDATION` writes source or adopts Builder Claim | REJECT, no permission promotion |
| Profile changed, role/group/task same | Protected Claim key unchanged |
| Wrong profile/role or explicit incompatible environment | Fail closed, retain legacy compatibility |
| Required nested tests omitted by aggregate command | Missing suite NOT_RUN; green command not proof |
| Public plugin imported but selected call not executed | Selected-path behavior NOT_PROVEN |
| Product Demo positive scripted result but independent semantic authority absent | Preserve narrow outcome and UNKNOWN/BLOCKED qualification |
| Stage 2 Architecture Demo with no required Issue/E1-E3 evidence | REJECT, Stage 1 index is not substitute |
| CI/Review PASS without native Outcome Closure | Task remains OPEN |
| Same `DEVELOPMENT_WORKFLOW.md` on both PR branches | No parallel conflicting writes; single version integrator, final exact blob review |
| One source reviewer identifies P1 in another PR | Reviewer may repair only in valid original write set, tests must rerun on new SHA |

## 7. Qualification / unresolved owners

**CI applicability is not universally equivalent to a Woodpecker status.** `RELEASE_STANDARD.md` §2 explicitly requires project Minimal CI only when the frozen/project policy selects it; `VALIDATION_STANDARD.md` §8 distinguishes the required profile from its normal provider and permits a trusted equivalent clean executor only when no provider-specific attestation is itself required. **T01 #1357 currently names Woodpecker in its frozen Task Pack**, so its required provider run cannot be casually waived. For the integrated version, re-evaluate each exact-subject/profile obligation under its actual authority; do not add a blanket new Woodpecker gate for unrelated docs-only changes, and do not pretend a two-test Web container result is equivalent to clean-checkout CI.

**No L2 Freeze here.** Sequence: (1) Product Owner explicitly freezes or revises PR #1363 exact source after independent Product Review; (2) bind L2 to resulting immutable Product subject, review architecture; (3) explicit L2 Freeze + approved Task DAG/Task writes; (4) qualify exact source and CI/review for #1358/#1362/#1342 and integration composition; (5) Version Candidate/Release Qualification under inherited release owner. Required real Host or E2E checks stay BLOCKED/NOT_RUN where evidence is unavailable; avoid treating practice-only #1360/#1352 etc. as universal v4.19 blockers unless actual Product Freeze admits them.

No main merge, tag, release, production side effect, cross-project source write, or historic v4.18/1353 rewrite is authorized by this proposal.
