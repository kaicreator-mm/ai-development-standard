# ADS v4.12 — ADS-first Standard Delivery Pack R0

> **Status: architecture / implementation planning candidate; not a Frozen Task DAG, not an executable Work Item or normative standard.** This pack applies the frozen Product R3 scope (Git blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`) and L2 source study §11 (L2 R4 Git blob `794f8e6374c2cda88cfc54cb284a1838ea67cddc`). It records the user-selected delivery sequencing: **ship ADS's own standards / templates / small checker first; other projects then validate ADS**. No consumer application's release or Scaffold is an ADS version release prerequisite by itself.

## 1. Separate three acceptance subjects

1. **ADS standard product:** authoritative owner standards, developer workflow, reusable task/review/validation templates, minimal deterministic checker and versioned adoption instructions. These are the v4.12 product to ship.
2. **ADS-internal verification:** test the standard's own machine-checkable contracts, semantic owner consistency and a **source-pinned new + mature snapshot fixture** already required by frozen PRD AC03/AC04. Fixture outputs are evidence; they are *not* an ADS business application, an ADS internal Scaffold, or a new mandatory GitHub-native DAG.
3. **External project adoption:** only after a legally qualified ADS baseline exists, real domain-harness/runx/xDownload/etc projects may exercise v4.12 under their own explicit adoption/authority; report observations back via normal ADS evolution feedback, without retroactive changes to their frozen history.

The frozen PRD requires **one new-project and one mature-project fixture** for the reference checker. Keep these minimal, synthetic/source-pinned, and inside the ADS conformance work; **do not block standards delivery on building/deploying full demonstration apps** unless a material requirement remains unproven. Do not replace required conformance predicates with a promise of later external dogfood. Exact actual GitHub CAS/Review/Host actions remain `NOT_RUN` until executed; shadow fixture results cannot satisfy those authorities.

## 2. Source/owner reuse before any implementation work

| Existing normative owner / facility | Adopt by reference | Bounded v4.12 change ONLY when source-proven |
|---|---|---|
| `standards/DEVELOPMENT_WORKFLOW.md` | Stage 1/2 Freeze, Stage 2.6 Review Policy, Stage 3/4 Task and version checkpoints | Conditional DAG-P/A selection, prospective post-L2 / pre-DAG Scaffold planning stage, paired planning freeze; no new universal gate |
| `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` and `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` | Canonical `type:planning`, ready, per-(work,role) serialized CAS accepted Claim, `NO_CLAIM_NO_EXECUTION`, native Task issues and role attribution | One permitted pre-DF `PLANNING_SCAFFOLD` planning-write concern *after* v4.12 adoption, using existing complete Work Item and accepted Claim |
| `standards/TASK_DAG_GOVERNANCE_STANDARD.md`, Task decomposition owners | Frozen intended planning DAG, actual GitHub native dependencies, SPLIT/SUPERSEDE, atomic owner/write sets | Single source structural anchors + canonical Task-side binding + derived forward/reverse projections; split-safe refresh, no owner duplication |
| `VALIDATION_STANDARD.md`, `RELEASE_STANDARD.md` and Adoption | Exact-subject currentness, risk floor, same log satisfying actual proved assertions, A0/A1 manual / A2+ machine truth | Deterministic pair material scope + hash checker; assertion-to-obligation projection if demonstrably missing, not a second validation DB |
| Existing controller, environment, learning and role standards | Read-only progress/review/claim visibility, preflight/cleanup, task learning and source-evidence stop rules | Source-local gap-only clarification (P1); no standalone W2/W3/W4 service |

**Predecessor constraint:** v4.11 is not established as Release-qualified. The current #1101 branch originates from historic `main`; v4.12 implementation version branch/merge/adoption must be rebound to the exact eventual qualified predecessor, not silently based on #1101. The inherited CI shallow-checkout problem is already repaired on v4.11 by #1038/#1040; consume that fix via lawful integration, do not duplicate it.

## 3. Minimal implementation concerns (draft DAG-I, not Frozen)

The **first work item is the actual L2 Architecture Owner decision on exact revised L2**, not a new implementation Gate. Before lawful L2 Freeze, all below are planning-only; no implementation source/standards normative edits, Task Issue materialization, or accepted Claim is implied.

| ID | Concern / one source owner | Intended output/write set | Dependencies | Minimum acceptance and negative oracle |
|---|---|---|---|---|
| **S01** | Workflow + Scaffold phase authority | `standards/DEVELOPMENT_WORKFLOW.md` and narrowly required associated text | Exact L2 Freeze + eligible version predecessor | Old stages preserved for old pins; selected `type:planning` cannot write without accepted Claim; side-effect install/network not authorized from file creation; no extra Bootstrap human gate |
| **S02** | Task/Scaffold binding contract | Canonical Task DAG governance and related owner contract docs, limited schema projection only if missing | Exact L2 Freeze; coordinate public interface with S01 before both source edits | Single effective writer, bind scope subset Issue Allowed/disjoint Forbidden, rename/split/stale bindings HOLD, structural stub cannot become functional PASS |
| **S03** | Tiny pure reference mapping + freeze checker | `scripts/` reusable deterministic generator/checker plus scoped tests/fixtures; exact write set after L2 owner choice | S02 effective binding/manifest contract | One new + one mature source-pinned fixture; stable forward/reverse output; old/new Git objects, scope, lock/config/CI, DAG-only change, forged derived output, pre-allowlisted malicious source fail closed; no GitHub side effects |
| **S04** | Adoption/template and owner reconciliation | existing `templates/`, `checklists/`, `standards/PROJECT_ADOPTION.md` where needed; non-normative examples if no gap | Exact L2 Freeze; may run parallel with S01/S02 | New/existing + A0/A1/A2+ instructions; DAG-P/A inline vs bounded vs explicit; S02 source not duplicated; W2/W3/W4 already-satisfied gaps marked as reused/deferred |
| **S05** | Integrated ADS conformance / ADS-version closure input | ADS-focused conformance tests and exact assertion→obligation evidence; no generated app shipping | S01+S02+S03+S04 integrated and source-current | Applicable focused negative tests and **one final candidate regression** (not many gate-named duplicate suites); mandatory owner evidence actual or NOT_RUN; ADS release and fixture outcome separate |
| **S06** | Version integration/qualification | Actual qualified v4.12 version target, Release-owner evidence and adoption baseline | S05 + real v4.11 predecessor qualification and legitimate integration authority | Current exact merged SHA/tree, required independent Review and validation, release owner record; an unqualified predecessor or unresolved material gates yields HOLD, not synthetic PASS |

**Actual parallelism:** after L2 Freeze and authorized exact base, run S01/S02 on non-overlapping source-owner scopes, S04 in parallel where write sets are disjoint; S03 starts after S02 contract; S05 follows implemented outputs; S06 requires both qualification and predecessor. Reconcile any overlapping owner-standard file *before dispatch*, not by late conflict resolution. These **six are candidates**, not six already-created native Issues. If source-level reuse makes S04 or another task trivial, fold/remove it at legitimate Task DAG Freeze with rationale; no ceremonial Issue count target.

## 4. ADS-first minimum usable handoff

A qualified version is **usable in external projects** when:
- [ ] Product R3 and exact L2 owner Freeze, correct qualified predecessor and adopted effective v4.12 owner rules exist.
- [ ] A developer can read the single entrypoint: phase mode selection, source-writing claim/Review boundaries, pre-DF scaffold, paired freeze, GitHub-native Task DAG, proof currentness and version release.
- [ ] The reference mapper/checker is deterministic on one new and one mature snapshot fixture, with targeted negatives and actual logs; A0/A1 projects have a legal manual equivalent when no generator is claimed.
- [ ] `not implemented`, `not run`, `unknown` and `not applicable` are distinguished from PASS; no independent/release claim is derived from demo output.
- [ ] Review/validation/closure is passed on the **ADS** exact version subject. If any required proof is unperformed, ship only a **preview / candidate**, not a qualified release.

No requirement to generate a deployable example app, build an always-on Steward, host a central service or execute every adopting project's future Task DAG before ADS standard publication.

## 5. Early external validation without falsely adopting v4.12

Before the standards release, participating external projects may read this planning pack and prospective v4.12 documents as **SHADOW / non-normative** only while following their **pinned currently approved ADS authority**. They can report source-pinned discrepancies; they cannot use the unapproved Scaffold phase exception or waive original source Claim/Review/Release rules. Upon eventual v4.12 qualification, each project independently decides lawful adoption and version migration.

## 6. Progress, truth and stop-loss

```ini
DELIVERY_MODE=ADS_CORE_FIRST_EXTERNAL_DOGFOOD_SECOND
PACK_STATUS=PLANNING_CANDIDATE_NOT_TASK_DAG_FREEZE
PRODUCT_FREEZE=PASS_R3_BLOB_0bfbf782c8859e79df52c9b57904ad80bcd718e9
L2_FREEZE=PENDING_ARCHITECTURE_OWNER
ADS_IMPLEMENTATION_TASKS_MATERIALIZED=NO
ADS_NORMATIVE_V412_ADOPTED=NO
NEW_FIXTURE_EXECUTION=NOT_RUN
MATURE_FIXTURE_EXECUTION=NOT_RUN
REAL_CONSUMER_APPLICATION_BUILD=NOT_REQUIRED_AS_SEPARATE_BLOCKING_DELIVERABLE
V411_RELEASE_PREDECESSOR=UNQUALIFIED_AT_PLANNING
V412_RELEASE=NOT_QUALIFIED
```

After each concern, report **real merged implementation Tasks / total frozen Tasks**, exact current HEAD, reused vs new owner rules, actual checks and next blocker. Do not present this plan as completed implementation or invent a completion percentage before the DAG is frozen.
