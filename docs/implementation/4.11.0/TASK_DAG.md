# ADS v4.11.0 — Version Task DAG v0.1 (PLANNING CANDIDATE, NOT FROZEN)

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
DAG_STATUS=DRAFT_REQUIRES_INDEPENDENT_REVIEW
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

## 2. Proposed executable leaves

| ID | One primary invariant / outcome | Primary existing owner and bounded write-set | True predecessors | Required acceptance and independent proof | Risk / Review |
| --- | --- | --- | --- | --- | --- |
| **V411-T01** | One pinned ADS effective-rule profile and multi-J non-weakening AND with provenance/UNKNOWN | `PROJECT_ADOPTION.md`, effective-rule portions of `DEVELOPMENT_WORKFLOW.md`, subordinate owner-local trace schema/tests only | none | Same hard floor A0–A4; multi-label J03+J06+J07+J08; source/authority precedence and no unproved N/A; positive & negative | high / required |
| **V411-T02** | Real changed-source materiality intake distinguishing inspected ABSENT from missing/UNKNOWN risk | Task/change evidence and `DEVELOPMENT_WORKFLOW.md` risk-intake sections, narrow task/validation projection | T01 | CLI/A0/J02 actually changes security/API/deploy but omits label → BLOCK; verify actual file/contracts and review currentness | high / required |
| **V411-T03** | J05 accepted spec delta ↔ current implemented contract consistency and invalidation | `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md`, contract evidence schema, compatibility owner-local tests | none | Accepted spec archive alone never PASS; changed producer/consumer and stale implementation negative; L1→L2→L3 lineage | medium / required |
| **V411-T04** | J12 Reuse-First exact source/license currentness and H1/H2/H3/BUILD_NEW provenance | `DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md`, architecture/reuse evidence prompt and owner-local tests | none | Upstream source or license drift invalidates stale H3; exact trade-offs/ref and safe no-research Fast Path | medium / required |
| **V411-T05** | One existing canonical interaction/event evidence authority and current acceptance contract | `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, review/decision provenance evidence schema and focused tests | none | Role vs GitHub transport distinction, event currentness, accepted Reviews/denial context and untrusted quote not authority; no new event family | high / required |
| **V411-T06** | Protected Dispatch/Claim eligibility, atomic multi-resource admission and legal WEB→LOCAL reroute | `EXECUTION_ARCHITECTURE_STANDARD.md` Dispatch/Claim/admission sections and focused reducer/transition tests; Interaction owner changes **forbidden without serial new authorization** | T05 | Same-key double Claim, stale/cancelled generation, claimed-task cannot be stolen, qualified fresh reviewer, advisory Issues not blockers | high / required |
| **V411-T07** | Current all-surface accepted Review + Validation sweep at merge, with safer last-admission/readback | Existing Merge Controller/Review policy integration and focused merge-admission verification/procedures; must not concurrently rewrite Interaction/Execution Task T06 surfaces | T05, T06 | Same-head PASS vs late P1 CHANGES_REQUESTED blocks; stale unrelated HEAD not false block; pagination/watermark drift BLOCK; GitHub APIs not globally atomic | high / required |
| **V411-T08** | Authenticated HUMAN DENY/authorized supersession persists across Claim and irreversible effects | Owner-specific Workflow human authority binding and narrow irreversible-boundary decision checks; no competing Interaction/Execution owner | T02, T05, T06 | Real authority provenance and scoped DENY; A CLAIMED→DENY→A effect denied with actual sink count 0, B READY→DENY blocked; quote/wrong-scope replay denied | critical / required |
| **V411-T09** | Non-idempotent lost-ACK effect recovery strictly follows grounded readback, dedup or authorized compensation | `EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` + `DATA_MIGRATION_GOVERNANCE_STANDARD.md` and owner-local guarded effect tests (no runtime/database) | T08 | True effect identity/tenant; no blind retry, uncertain outcome remains BLOCKED, allowed bounded reconciliation & failure paths. U02 local Git E2 is limited reference only, real GitHub remote/multi-host not assumed | high / required |
| **V411-T10** | Untrusted GitHub/MCP/A2A/LLM/tool data cannot promote itself to authority or leak secret values | `CONFIGURATION_SECRETS_STANDARD.md`, `WORKSPACE_ARTIFACT_STANDARD.md` and focused trust/redaction negative tests | none | Fake approval, operator spoof, injected policy override and secret exfil attempts denied; transport identity ≠ authorization | high / required |
| **V411-T11** | One central schema/template/manifest/verifier wiring convergence for all new owner-local semantics | `standard-manifest.json`, `schemas/`, canonical templates, common `scripts/verify_standard.py` and registry/tests; **single writer only** | T01,T02,T03,T04,T05,T06,T07,T08,T09,T10 | No duplicate owner/Gate enum; v1/v2 reader compatibility; owner/schema/template/prose/test parity; failure on missing required current material facts | high / required |
| **V411-T12** | Canonical whole-version A+B+C positive and adversarial conformance fixtures (not just 42 toy tests) | One maintained golden fixture/validation test registration concern; isolate write set from T11 shared manifest by waiting on it | T11 | Real executable S01–S18 + X01–X08; Library/Service/CLI; NEW/BROWNFIELD; A0–A4; J09+J10+J11+J12 material unknown fail closed; independent actor/source/host proof | critical / required |
| **V411-V01** | Independent exact-candidate visible validation, real-host critical journeys and full regression | **Validation actor**; reports/evidence only, no Task implementation source writes | T12 | Local real Build Host and exact tuple; all mandatory S/X evidence, 0 silent N/A, full regression; failures preserve exact source and routing | high / required |
| **V411-V02** | Operational Candidate Freeze, formal Hidden and genuinely fresh Version Closeout under distinct owners | **Release/Hidden/Fresh actors**, each owns its separate gate and evidence; no private pack publication | V01 | Candidate stable; Hidden private results public-safe only; fresh context independence; negative human veto and uncertain external effect not substituted by synthetic PASS | critical / required |
| **V411-R01** | Release Qualification on qualified candidate then guarded repository integration/tag/base record | **Fresh RQ + Repository Integration** distinct owners; no package/standard implementation rewrite | V02 | RQ independently READY; exact-head recheck, bounded expected-main merge, post-merge validation, immutable baseline; tag alias not authority | critical / required |

**Issue materialization note:** V01, V02 and R01 are lifecycle/evidence gates, not claims that one agent may perform all Validation, Hidden, Fresh, RQ and integration roles. The future Task DAG Review may split V02/R01 into native separate validation/release nodes if actor ownership or audit protocol requires separate Issues. No independent reviewer is allowed to certify their own implementation or gate.

## 3. Dependencies and legal parallelism

```text
START ─┬── T01 ── T02 ─────────────────┬───────── T08 ── T09 ─┐
       ├── T03 ────────────────────────┤                     │
       ├── T04 ────────────────────────┤                     │
       ├── T05 ── T06 ── T07 ───────────┤                     │
       └── T10 ────────────────────────┤                     │
          T05 + T06 ────────────────> T08                     │
          T01..T10 COMPLETED ───────────────────────────────> T11
          T11 → T12 → V01 → V02 → R01
```

**Potential initial independent work:** T01 / T03 / T04 / T05 / T10; they own distinct primary normative paths. T02 follows T01 because both may touch Workflow. T06 follows T05 because Interaction/Execution's accepted event contract is foundational. T07 follows T06 to avoid shared merge-admission/Execution state collision. T08 depends on T02/T05/T06 due to Workflow/human/claim authority; T09 follows T08 for irreversible effect-boundary precedence. Central T11 follows all owner-local concerns; T12 checks integrated behavior, V01/V02/R01 require genuine role-separated actual gate evidence.

**No fabricated dependency:** DAG edges express actual contract, owner file conflicts or executable-baseline needs. When native GitHub Issues later replace this planning checkpoint, use native blocked-by edges only; a body text list, PR stack or a shared Markdown status file is NOT live dependency truth.

## 4. Acceptance matrix: Frozen Product six ship concerns → accountable leaves

| Frozen requirement | Main implementation leaves | Mandatory negative proof location |
| --- | --- | --- |
| #1 Applicability + multi-label requirements | T01, T02, T11 | T12 X01/X08 plus S-cases; omitted labels, uninspected material risk, weaker A0 overrides |
| #2 Multi-Agent role/eligibility/interaction | T05, T06, T08 | T12 S08–S12/S15–S18; duplicate Claim, wrongful delegation, reviewer reroute, DENY replay |
| #3 Dispatch/Review/Merge admission safety | T05, T06, T07 | T12 same-HEAD opposite accepted Reviews, late blocker/watermark update, incomplete GitHub readback |
| #4 Unsafe effect, cross-actor recovery, trust | T08, T09, T10 | T12 X03/X04/X07 and genuine V01 real-effect/HUMAN gate proof; local U02 research only as bounded seed |
| #5 Selected OpenSpec/Spec Kit/Reuse-First assimilation | T01, T03, T04, T11 | T12 J05 accepted-vs-implemented and J12 changed upstream/license; actual normative owner change required |
| #6 P1/P2/P3 whole-version executable assurance | T11, T12, V01, V02, R01 | S01–S18 + X01–X08, unexpected material intersections UNVERIFIED/BLOCKED, Hidden/Fresh/RQ independent |

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

A genuinely fresh independent reviewer should challenge all 15 leaves for minimum coherent concern, dispatchability, risks and independent gate actors, exact owner/write-set overlap, J05/J12 non-assessment assimilation, dual-agent authority and human DENY post-Claim negative path, real GitHub-bound effect proof non-substitution, coverage of Frozen six ship concerns and S/X fixtures, safe initial concurrency, architecture placement, absence of unearned Task READY, no unauthorized version branch, and qualified predecessor main rebind.

Specifically check whether T05 is an overly broad "Interaction" authority concern and whether T06/T07/T08 simultaneous source changes would collide; split concerns or add source-derived legal dependency only if concretely necessary. Check whether V02 and R01 must be split for role separation rather than pretending one Task can self-certify release. Any material DAG revision requires a new exact doc commit and genuinely fresh review.

```ini
DAG_CANDIDATE_ONLY=YES
DAG_INDEPENDENT_REVIEW=NOT_RUN
DAG_FREEZE=NO
EXECUTION_ISSUES=NOT_MATERIALIZED
NATIVE_DEPENDENCIES=NOT_MATERIALIZED
TASK_PACKS=NOT_MATERIALIZED
STAGE3_SOURCE_MUTATION=NO
V411_RELEASE_INTEGRATION=NO
```
