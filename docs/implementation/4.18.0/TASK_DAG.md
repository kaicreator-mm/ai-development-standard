# ADS v4.18.0 — Version Task DAG planning checkpoint R0

**State:** `PLANNING_CHECKPOINT / FIVE_ISSUES_CREATED / NATIVE_DEPENDENCY_EDGES_MISSING / NO_TASK_DAG_ADMISSION / NO_SOURCE_CLAIM`. This is **not** an authoritative executable DAG, Claim, Dispatch or release state ledger. Actual Issue state/relations remain GitHub-native.

## Frozen sources

- Product Freeze: [#1320@6388802387](https://github.com/kaicreator-mm/ai-development-standard/issues/1320#issuecomment-6388802387). PRD Git blob `98772b4594caa44b2611853ae482132f7aefa36b`.
- L2 Freeze: [#1321@6395575157](https://github.com/kaicreator-mm/ai-development-standard/issues/1321#issuecomment-6395575157). Frozen L2 Git blob `e3b5106c2fdaa8b2a0bbac5adb32b810fcbd51dd` from `version/v4.18@8f2737aba90719825bbc73a2f5cbe4f7e43fd6ef`.
- Integration branch: `version/v4.18` (distinct from main).
- Predecessor: `main@a45644d734fdf94da3e6f9c3f90ffe4ce3c25fda`, v4.17 source-only conditionally qualified.
- Version umbrella [#1322](https://github.com/kaicreator-mm/ai-development-standard/issues/1322).
- Native Issue edges are **mandatory**, and any Markdown `Depends On` below is advisory until native relations are successfully written and read back. The connected Chat-mode GitHub tool can read native edges but has no native edge mutation action.

## Capability → Concern trace

| Product outcome / FR | Existing owner or gap | Task(s) | Proof and notes |
| --- | --- | --- | --- |
| FR-01/02 capability-before-concern / atomic decomposition | TDS §3/§4/§9 and template existing; tiny prompt gap | A, B, C | no Step→Issue inflation |
| FR-03/04 bounded Patterns and alternative topology / dependency reasons | minimal new §13 SHOULD + reference/examples | A, B, C; I integrates | advisory only, no new native dependency kind |
| FR-05/06 SF↔DAG planning feedback + writer exclusivity | existing §10A SF/DF/MI; template prompt gap | B, C | this ADS version has no accepted own SF; hypothetical SF-only E1 test |
| FR-07 native Option A/JIT/source admission | existing Execution Architecture; negative oracle only | B, C, I | no merge-only bypass |
| FR-08/09/10 Agent/WEB/CI/LOCAL and minimal handoff | existing Model/GAIP/LAH + template fit gap | B, C | no new scheduler/schema or protected permission |
| FR-11/12 Human intervention | existing Human Decision Authority | C | fictitious positive/negative fixture only |
| FR-13/14 lightweight stage Pattern references | existing registered TDS Reference | C | no second Pattern catalog |
| FR-15 topology quality (non-gating) | planning quality prompt | A, B, C | no fabricated numerical duration or universal threshold |
| FR-16 evolution feedback | already covered/deferred | none | external projects decide own Product/L2 |

## Planned workfronts (5 native Issues created, not yet admissible)

| Task | Issue | Lane | Depends On (intended native) | Parallel after admission | Source writer (only) | Required evidence / review |
| --- | --- | --- | --- | --- | --- | --- |
| A | [#1323](https://github.com/kaicreator-mm/ai-development-standard/issues/1323) | minimal normative | none | YES with B,C | `standards/TASK_DECOMPOSITION_STANDARD.md` §13 | tiny SHOULD; TDS/T13/T05A; independent review required |
| B | [#1324](https://github.com/kaicreator-mm/ai-development-standard/issues/1324) | DAG template | none | YES with A,C | `templates/task-dag.md` | Lane CI/oracles; review recommended |
| C | [#1325](https://github.com/kaicreator-mm/ai-development-standard/issues/1325) | Golden E1 / reference | none | YES with A,B | `references/TASK_DECOMPOSITION_REFERENCE.md` + new standalone E1 test | frozen L2-only fixtures; Golden/G01–G14 regression |
| I | [#1326](https://github.com/kaicreator-mm/ai-development-standard/issues/1326) | integration & central wiring | #1323, #1324, #1325 | NO (starts after actual A/B/C completion) | `standard-manifest.json`, `.github/workflows/verify-standard.yml`, new I-owned integrated test; conditional index only if necessary | exact cross-source oracle, integrated CI, independent review |
| R | [#1327](https://github.com/kaicreator-mm/ai-development-standard/issues/1327) | release / metadata | #1326 | NO | `VERSION`, `README.md`, `CHANGELOG.md`, release evidence | whole candidate validation, RQ, main merge only after qualification |

### Native edge plan and durable authority

Expected native Issue Dependencies, **not yet present**:

- `#1326 blocked_by #1323` (blocking issue database ID `6022621376`).
- `#1326 blocked_by #1324` (blocking issue database ID `6022621812`).
- `#1326 blocked_by #1325` (blocking issue database ID `6022622085`).
- `#1327 blocked_by #1326` (blocking issue database ID `6022622322`).

Official GitHub REST: `POST /repos/kaicreator-mm/ai-development-standard/issues/{issue_number}/dependencies/blocked_by` with JSON body `{"issue_id": <blocking issue database ID>}`. A/B/C have no sibling edges and should remain independent; no edge from umbrella Product/L2 since those are **frozen authority prerequisites**, not material Task blocker Issues.

**Admission rule:** All five Issues currently `state:planned`. They cannot be called an **accepted materialized native DAG** until all four native edges are written and read back against this exact set and current Issue states. No Task Builder Claim or source write is authorized by an Issue body or this checkpoint.

## Alternative topology assessment — first source-only dogfood

| Candidate | Structural path in material Task edges | Source conflicts | Decision |
| --- | --- | --- | --- |
| A→B→C→I→R | 5 sequential Tasks | None requiring that sequence | REJECT unnecessary serialization; independent Frozen-L2 contracts suffice |
| A ∥ B ∥ C → I → R | 3 parallel front-line workfronts, then 2 convergences | none among A/B/C (disjoint file ownership); shared manifest/workflow only I | SELECT after native readback |
| A ∥ B ∥ C ∥ I ∥ R | I/R would consume unaccepted outcomes | Fake merge/Release readiness | REJECT |
| One giant Task for A+B+C+I+R | 1 PR, no workfront fan-out, large review surface | single owner plus higher blast radius | REJECT absent overriding atomic invariant |

This is a **topological** comparison only. Wall-clock time, token cost, queue delay and observed speedup = `UNKNOWN/NOT_MEASURED`. No source-scaffold accepted in this ADS self-change (`SF_Binding=NOT_APPLICABLE`); FR-05 examples are fictitious only.

## Dependency and role explanation (non-authoritative)

- A/B/C depend on **Frozen L2** and on their individually admitted Issue/Claim/currentness. No cross-sibling implementation code or source baseline assumed.
- I has real **merged source/contract + central wiring** prerequisites from each A/B/C, so it must have all three native blocked_by relationships.
- R has real **exact integrated source and version qualification** prerequisite I.
- A semantic standards author/reviewer owns A, template/UX engineering Agent owns B, fixture/research Agent owns C; CI validates actual declared profile and independent Reviewer when Review Policy selects it; Integration and Release Controller own their own authority.
- Local execution only when a required test/effect cannot be evidenced with connected source and qualified CI. Protected human decisions only by existing authority (none added by this version).
- Shared GitHub transport login is not identity-based independent-actor proof or legitimate protected human approval.

## Historical regression and release truth

The historical T13 suite has 62 methods, 61 fully passing and one method with exactly two old failing owner-equality subtests. The T05A suite has 39 methods, 38 fully passing and one method with a single old failing TDS owner pin subtest. These **three** exact-subject historic pin subtest identities are the only proposed current-version Release-owner `NOT_APPLICABLE` candidates. All remaining method assertions/subtests, including passing IQS/ICGS pin assertions inside T05A's partly failing method, remain applicable to v4.18.

Future validation runs complete unchanged suites and compares actual per-subtest FAIL/ERROR/SKIP sets, preserving EXIT 1 and actual raw logs; any new failure blocks, even if an existing historic pin already fails. Release owner must positively decide applicability at exact version candidate or RQ remains BLOCKED. Do not call old full v4.10 integration runner green.

## Acceptance/next steps

1. **Pending:** mutation of four native GitHub Issue Dependency relationships and readback; these are the only DAG edges.
2. Recheck five Task Issue canonical metadata and exact complete stable contracts; only then perform legal transition for dependency-free A/B/C from planned to ready where permitted, with genuine role-specific CAS Dispatch Claims.
3. A/B/C source concern PRs may proceed in parallel **only after** such admission and disjoint source ownership verified. I waits A/B/C, R waits I.
4. Source E1 tests and integrated CI truly executed and reused according to exact source impact; no fake Host/Agent runtime evidence.
5. Release owner qualifies whole-version exact candidate; main merge only after qualified version closure.

**Progress ledger:** 5/5 Task Issues created, 0/4 native dependency edges confirmed on initial GET readback, 0/5 source concerns completed, 0/5 legitimate Builder Claims, VERSION/Release/MAIN NOT_RUN.
