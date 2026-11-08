# ADS v4.19 — Integrated Task DAG / Delivery Plan R0 (candidate; no native Task admission)

**State:** DRAFT / DAG_CANDIDATE / NOT_FROZEN / NO_CLAIM_GRANTED.  
**Source Product:** PR #1363 @ `9d2962e07a44e6b76f61e8ff5d1f3a02d1b57e47`, Blob `b776c09b341eb5fbdaeaf5aa98f4e2afbcd0ec9c`, Product Review candidate PASS_WITH_P2, **Product Owner Freeze NOT_RUN**.  
**Proposed L2:** `docs/architecture/v4.19/INTEGRATED_DELIVERY_L2_R0.md`, currently **NOT_FROZEN**.  
**Historical #1353:** frozen one-Task T01/7-path scope is unchanged; this plan is a prospective version-wide overlay, *not* an amendment to that frozen history or a second live DAG.

## 1. Smallest real outcomes and owners

Reuse four existing Draft workfronts and add at most one version-integrator after source qualification. Do not create per-Demo or per-review Task Issues merely to increase progress.

| Logical Outcome (not yet native Task) | Existing owner and exact candidate | Draft write ownership, qualification and disposition |
| --- | --- | --- |
| P0 — integrated Product/L1 decision | #1347 / PR #1363 | One Product candidate file. Independent Review PASS_WITH_P2 but **Owner exact Product Freeze missing**. Its future Freeze is a prerequisite for prospective policy amendments and normative activation. |
| A0 — prospective three-domain L2 + DAG | this stacked candidate | Two planning files; await real Product Freeze, actual L2 review/Freeze and Task DAG Freeze. |
| T01 — additive Dispatch profiles | Task #1357 / PR #1358 (frozen, 7 source/test files) | Preserve historical T01 Claim/write-set and five legacy profiles; actual Python focused/full suite, exact-SHA Woodpecker, required independent final source Review not proven. Prospective global Web-default correction requires lawful approved amendment; no Validator source write. |
| P1 — optional Demo Stage 1 evidence guidance | #1361 / PR #1362 (4 docs paths) | Product/L1 and Stage 1 owner review; no new schema, no per-Demo issue. `standards/DEVELOPMENT_WORKFLOW.md` is shared with P2. |
| P2 — source-based quality/issue prevention | #1347, #1341/#1343/#1344 / PR #1342 (17 source/docs/tests paths) | Qualify only actual v4.18 gaps; eight Python source regression tests and 18-case pilot remain *proposed*, not an accepted blind oracle. `standards/DEVELOPMENT_WORKFLOW.md` shared with P1. |
| I01 — version-owned composition and Outcome acceptance | Existing version integration authority, no Task yet | One authorized Writer composes final overlapping Workflow doc, checks exact SHA/pins, runs qualified tests/CI, handles version candidate and Release gates. Does not perform main merge/tag until independently authorized. |

## 2. Prospective dependencies

```text
P0 Product Owner exact Freeze
        |
        v
A0 L2 Review/Freeze + Prospective DAG/Task Owner Freeze
        |
        +---- T01 Dispatch profile finalization ----+
        |                                            |
        +---- P1 Stage 1 Demo optional evidence -----+--> I01 compose exact version tree
        |                                            |       --> source tests/current CI/review
        +---- P2 quality-source deltas --------------+       --> candidate qualification/closure
                                                               --> RQ --> authorized main/tag/release
```

The three implementation branches can perform **non-authoritative source preparation or already-authorized bounded validation** concurrently as allowed; an accepted Claim/Task Pack is still required before effects. Independent review/CI must use each actual SHA. I01 is a real dependency join, not a fabricated prerequisite that serializes three unrelated source concerns.

### 2.1 Single Writer for the only known overlapping file

`standards/DEVELOPMENT_WORKFLOW.md` is touched by both #1362 and #1342, with different original PR bases. A legitimate I01 version Writer must:

1. Re-read current `version/v4.19` HEAD and blob, current PR HEAD/TREE/BASE and each contributing patch.
2. Apply additive Stage 1 optional Demo paragraph from #1362 (keep Stage 2 Architecture Demo owner/gate) **and** separately the root-cause/minimum-sufficient-repair guidance from #1342 (keep existing risk-based review and scope authorization).
3. Confirm one coherent resulting file and one exact blob in the final version candidate; no conflicting concurrent edit or unreviewed later branch ref.
4. Run impacted source-only tests, applicable inherited Python/CI suites and independent review on the final composite SHA, not transfer old PASS from component SHA.
5. Record origin, owned changed-path inventory, failing/negative cases, expected HEAD guard, integrated commit and actual status. If a blocker is unrelated infrastructure rather than source, retain source PASS evidence and classify separately.

Do not silently merge old #1342 (main-based) into main. Do not invent a second GitHub-native dependency topology or standalone Claim from this doc.

## 3. Proposed execution/verification order

**Before any CI:** source syntax/JSON schema parse and Python compile on the exact new source candidate; no unnecessary Node-major rule for semantic Demo content.

**T01 focus:** `scripts/test_protocol_schemas.py`, `scripts/test_v410_t06b_multi_dispatch_conformance.py`, `scripts/test_execution_architecture.py`, and existing relevant ADS full conformance; profile/role/environment contradiction, legacy profile semantics and protected-claim-key invariance.

**P1 focus:** old no-exploration fast path; multi-study master Issue/Git-source exact pin; negative/unknown; Stage 1 vs mandatory Stage 2; no automatic Product Freeze. Doc-only tests as applicable; version-level tests still required on integrated candidate.

**P2 focus:** `python -m unittest discover -s tests -p test_v419_issue_prevention.py -v`; owner coverage, 18 cases/3 positive controls, nested discovery synthetic negative, public hook loaded-not-invoked negative, Golden/Forbidden and old normative owner consistency; physical selected-consumer proof remains separate if material.

**I01 focus:** final combined file content, all affected Python/schema tests and inherited suite with known historical fixed-SHA failures classified (do not call EXIT 1 PASS), self-hosted Woodpecker exact candidate, source-bound independent normative Review, current Release Standard qualification. Do not substitute GitHub Actions. Do not rerun unchanged-tree PASS without a change/required new environment.

## 4. Minimal critical-path acceptance contract

A row can be called closed only after its own native owner legally closes the Outcome. A Draft PR, frozen Product scope, static review, schema parse or READY Dispatch is not Task CLOSED, CI SUCCESS or release qualified.

For each candidate use separate flags: `PRODUCT_FREEZE`, `L2_FREEZE`, `DAG_FREEZE`, `SOURCE_SYNTAX`, `FOCUSED_TEST`, `FULL_REGRESSION`, `CI_EXACT_SHA`, `INDEPENDENT_REVIEW`, `VERSION_INTEGRATION`, `OUTCOME_CLOSURE`, `RELEASE_QUALIFICATION`; retain `NOT_RUN` or `BLOCKED` unless actual receipts exist. These are human-readable progress ledger labels, **not new ADS machine Gate states**.

| Event | Legal outcome |
| --- | --- |
| Product Owner issues exact prospective Product Freeze | P0 can become frozen; qualify derived L2 before new source scope |
| Source fails focused regression after a repair | Same authorized Writer repairs within original write-set, reruns affected checks on changed SHA |
| Web cheaper but Local-only environment is required for implementation | Choose existing authorized Local Builder under effective contract, not `LOCAL_VALIDATION` source mutation |
| Native DAG has true blocked predecessor | Progress upstream only; do not fake readiness from stale `state:ready` |
| Two PRs touch Workflow Standard | Compose via one I01 Writer and complete final exact-source tests/review |
| PR and CI pass, but Outcome Issue remains open | Do not increase Outcome closure numerator |
| RQ, independent gate, or high-impact authorization absent | No main/tag/release; report exact missing evidence, not automatic PASS |

## 5. Current observed delivery ledger

At authoring: PR #1363 HEAD `9d2962e...` independently reviewed as Product *candidate* with P0=0, P1=0, P2=1; Owner Freeze not run. PR #1358 HEAD `f495c374...`, #1362 HEAD `5cfbdb8...`, #1342 HEAD `84fd57d...` are separate open Drafts with reviewer source repairs, but no actual native Python/CI final qualification/merge. `version/v4.19` contains three historical #1353 planning documents only, `VERSION=4.18.0`. Current native work remains **not CLOSED** simply because review comments or this prospective plan exist.

**Version risk:** release qualification depends on the real baseline and inherited failures/required gates; no automatic version number, changelog, main merge, tag, GitHub Release or downstream adoption.
