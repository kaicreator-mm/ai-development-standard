# v4.11 Product Proof Fixtures & Owner Evidence — Freeze-prep Annex (NON-FROZEN)

Prepared from exact source subjects:
- PRD Draft v0.3: #938@6067371136 (R3 Product Review PASS #941@6067535335)
- S01–S18 matrix from PRD Draft v0.2: #938@6066695101 (subject historical, but explicitly incorporated unchanged in v0.3 §2.4)
- owner/equivalence/source-only evidence: #938@6066716255

This annex **does not** assert any v4.11 execution/real-host/Hidden/Release PASS. It is a provenance-preserving planning snapshot at v4.10 source baseline `35a4016bb5421811a2ababbc3d0609c88304c6b5`. Unverified material profiles/compound jobs must remain `UNVERIFIED` pending owner disposition. Git blob and subject currentness need readback before an explicit Freeze.

---

### 2.2 Fixed mandatory cross-profile proof fixture set (no arbitrary ex post shrink)

Minimum **18** reference fixture subjects, each with effective-rule, task/role, required positive and adversarial coverage:

| ID | Shape; adoption; condition | Job / actors | Main semantic oracle |
| --- | --- | --- | --- |
| S01 | CLI A0 NEW | J02 one Builder | lightweight scoped task, valid required evidence, no extra ceremony |
| S02 | LIBRARY A1 BROWNFIELD | J03 one Builder → independent gate where policy selects | old interface intact, legal handoff or NOT_RUN |
| S03 | SERVICE A0 BROWNFIELD | J07 security-critical fix (Builder + required independent Reviewer) | A0 cannot waive higher-authority security review |
| S04 | SERVICE A1 BROWNFIELD | J06 migration with independent Validator | fresh-install ≠ upgrade ≠ interrupted recovery |
| S05 | LIBRARY A2 BROWNFIELD | J05 public API change | compatible contract decision and spec/currentness |
| S06 | CLI A2 NEW | J12 upstream reuse H1/H2/H3/BUILD_NEW | exact provenance and unknown license, old test not new PASS |
| S07 | SERVICE A3 NEW | J01→J04 Product/Planner/Builder/Reviewer | Product/Architecture authority/Task DAG → independent evidence |
| S08 | SERVICE A3 BROWNFIELD | J08 external deploy; Builder→successor | possible success, no ACK: reconcile before retry |
| S09 | LIBRARY A3 BROWNFIELD | J03 concurrent Builders + Reviewer | shared write-set collision, rebase/head drift |
| S10 | CLI A4 NEW | J04 two providers, review + CI | provider-neutral hard predicates and truthful source/host evidence |
| S11 | SERVICE A4 BROWNFIELD | J09 Release Controller + Hidden Validator | only exact candidate's frozen/Hidden/RQ gates yield release verdict |
| S12 | SERVICE A3 BROWNFIELD | J10 incident response + recovery | verified current source/target state, no fake rollback PASS |
| S13 | LIBRARY A0 BROWNFIELD | J11 public deprecation | declared consumer window, no silent destructive API retirement |
| S14 | CLI A4 BROWNFIELD | J12 upstream changed license/version | reuse decision invalidation and source authority |
| S15 | SERVICE A4 BROWNFIELD | mixed A0-like worker + A4 controller, same project pin | resolved mandatory floor, no override downgrades |
| S16 | LIBRARY A3 NEW | WEB/LOCAL Fresh Reviewer substitution | role/capability/currentness/independence over brand |
| S17 | SERVICE A4 BROWNFIELD | two accepted opposite same-head Reviews | fail-closed Merge before durable adjudication |
| S18 | CLI A3 NEW | external A2A/MCP/git comment input → Agent | untrusted instruction/secret remains data, not privileged command |

**Coverage proof obligation**: every J01–J12 appears in a fixture; every declared archetype, all A0–A4 adoption levels, both NEW/BROWNFIELD, one-agent/multi-agent, WEB/LOCAL, human decision points and required-gate negative cases are covered. For other supported combinations not instantiated, the *applicability/effective-rule resolver* must be proven by owner-based equivalent cases or explicitly listed as `UNVERIFIED`; they do **not** silently inherit an assertion of runtime coverage. Additional security-critical, public-contract, persistent-state, external-write and release cases are mandatory where those invariants can differ materially. No numeric coverage % can be claimed without a completed exact current matrix and numerator/denominator.

**Freeze vs release distinction**: Before **Product Freeze**, require this declared coverage envelope, owner-gap/equivalence ledger, explicit Product UNKNOWN disposition, falsification oracles and reviewed PRD. It does **not** require S01–S18 actual software executions yet. Before **Version Release Qualification**, require selected real executable fixtures/independent assurance/visible full regression/Hidden according to frozen L2/DAG/gates, with unexecuted required subjects marked NOT_RUN/BLOCKED. Historical projects can be represented by safe isolated fixtures for destructive cases.

---

## v4.11 L1 owner-equivalence & proof-denominator ledger R0 — pinned-source audit

```ini
PARENT=#938
CONSUMED_PRD=#938@6066695101
SOURCE_STANDARD_REF=version/v4.10.0@35a4016bb5421811a2ababbc3d0609c88304c6b5
EVIDENCE_CLASS=PINNED_SOURCE_INSPECTION_ONLY
EXECUTABLE_CONFORMANCE=NOT_RUN
DRAFT_PRODUCT_STATUS=NON_FROZEN
L2_AUTHORITY=NO
```

This is **evidence for** PRD v0.2's 18 declared mandatory reference journeys, not claims that an unexecuted project pass/fail test passed. One actual ADS owner is stated for each relevant normative concern; a supporting second owner is an explicitly subordinate/composed obligation, not a second semantic authority. Historic tests may exist but no new v4.11 positive/negative tests have run. If source ref changes, re-evaluate only material owner differences.

### 1. Reference-journey owner / missing behavior matrix

| Ref | Primary current owner(s) inspected | Existing source-level guarantee | Residual requirement to falsify | State |
| --- | --- | --- | --- | --- |
| S01 A0/CLI/new/docs | `DEVELOPMENT_WORKFLOW.md` + `PROJECT_ADOPTION.md` | Fast Path, minimum adoption, no mandatory research ceremony | A0 actor's exact gates resolved; no accidental extra Research Issue | COVERED_SOURCE / PROOF_NOT_RUN |
| S02 A1/library/brownfield/bug | `IMPLEMENTATION_QUALITY_STANDARD.md`, `VALIDATION_STANDARD.md`, `GITHUB_AGENT_INTERACTION_PROTOCOL.md` | typed checks, exact evidence, risk-based Review | role-specific single-agent handoff vs self-independent PASS | COVERED_SOURCE / PROOF_NOT_RUN |
| S03 A0/service/brownfield/security | `PROJECT_ADOPTION.md` §2, `VALIDATION_STANDARD.md` §2, `GITHUB_AGENT_INTERACTION_PROTOCOL.md` §6 | non-weakening mandatory floor and review policy | cross-profile effective-rule conflict and gate resolution trace | PARTIAL_CURRENT_RULE / NEW_NEGATIVE_REQUIRED |
| S04 A1/service/brownfield/migration | `DATA_MIGRATION_GOVERNANCE_STANDARD.md` + `VALIDATION_STANDARD.md` | directional source→target and distinct fresh/upgrade/interrupted recovery | agent/handoff side-effect uncertain retry across source states | PARTIAL_COMPOSITION_GAP |
| S05 A2/library/brownfield/public API | `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` (blob `266aefe3…`) | baseline/candidate, change operations separate from compatibility outcome, deprecation | true accepted-spec/current implemented-state reconciliation after change | PARTIAL_SPEC_SYNC |
| S06 A2/CLI/new/upstream | `DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md`, `ARCHITECTURE_DESIGN_STANDARD.md` | chosen dependency/architecture evidence, alternative/tradeoff | H1/H2/H3/BUILD_NEW with exact source version/license/upgrade, #929/#930/#931 | GAP_BOUNDED_REUSE_SPINE |
| S07 A3/service/new/L1→release | `DEVELOPMENT_WORKFLOW.md`, `TASK_DECOMPOSITION_STANDARD.md` (blob `f355c020…`), `RELEASE_STANDARD.md` | Product→L2→Task→Validation→Release, no PR PASS as Release | real complete authority/evidence cross-agent trace | COVERED_SOURCE / PROOF_NOT_RUN |
| S08 A3/service/brownfield/deploy | `EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` (blob `6da46996…`) + `EXECUTION_ARCHITECTURE_STANDARD.md` (blob `0bb9e304…`) | explicit side-effect authority, bounded no-duplicate non-idempotent retries, delegated responsibility | ACK-unknown first effect then successor handoff/reconciliation oracle | PARTIAL_COMPOSITION_GAP |
| S09 A3/library/brownfield/concurrent | `TASK_DECOMPOSITION_STANDARD.md`, `TASK_DAG_GOVERNANCE_STANDARD.md`, `GIT_EXECUTION_STANDARD.md` | Task write-set, minimum coherent concern, native dependency truth | concurrent/shared-owner race and successor exact subject | COVERED_SOURCE / PROOF_NOT_RUN |
| S10 A4/CLI/new/actor substitution | `EXECUTION_ARCHITECTURE_STANDARD.md` §27, `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `schemas/dispatch.schema.json` (blob `f8532bfc…`) | composite eligibility, hard filters before ranking, WEB/LOCAL execution_environment | brand-closed event schema/current brand-based bootstrap compatibility #890 | PARTIAL_PROVIDER_NEUTRAL |
| S11 A4/service/brownfield/release | `RELEASE_STANDARD.md` (blob `014f3996…`) + `VALIDATION_STANDARD.md` (blob `1522b85f…`) | required full visible/Hidden/fresh closeout/RQ and candidate immutable identity | two-agent stale transfer/changed gate and exact evidence closure | COVERED_SOURCE / PROOF_NOT_RUN |
| S12 A3/service/brownfield/incident | `DATA_MIGRATION_GOVERNANCE_STANDARD.md`, `EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` | source/target/recovery intent, external environment identity | human-visible incident response and uncertain recovery between Agents | PARTIAL_COMPOSITION_GAP |
| S13 A0/library/brownfield/deprecate | `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` | contract baseline/current candidate and deprecation/consumer-window obligations | lifecycle retirement boundary vs ISO 12207, prevent silent removal | COVERED_SOURCE / LIFECYCLE_BOUNDARY_UNKNOWN |
| S14 A4/CLI/brownfield/license change | `DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md` plus #930/#931 | selected dependency identity/source scope should be tracked | changed upstream license/revision invalidates frozen reuse claims | PARTIAL_PROVENANCE / NO_REUSE_PASS |
| S15 mixed A0/A4/service/brownfield | `PROJECT_ADOPTION.md` (blob `aac0d4bf…`) + `VALIDATION_STANDARD.md` | truth floor across A0–A4 independent of runtime adoption | complete rule-resolution conflict oracle across pinned/Project/Frozen/Pack | PARTIAL_EFFECTIVE_RULE_ORACLE |
| S16 A3/library/new/Fresh WEB↔LOCAL | `EXECUTION_ARCHITECTURE_STANDARD.md` §27; `GITHUB_AGENT_INTERACTION_PROTOCOL.md`; #932 | independent context and atomic protected Claim exist | eligible LOCAL subagent auto-route/admission/currentness and wake liveness | PARTIAL_ROUTING_LIVENESS |
| S17 A4/service/brownfield/conflicting review | `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `VALIDATION_STANDARD.md`, #785 | exact Review and high-severity blocker model | accepted same-HEAD PASS vs P1 CHANGES_REQUESTED premerge sweep | MATERIAL_MERGE_CONFLICT_GAP |
| S18 A3/CLI/new/tool input | `CONFIGURATION_SECRETS_STANDARD.md` (blob `cda438ad…`) + `WORKSPACE_ARTIFACT_STANDARD.md` (blob `f54c37e9…`) + `GITHUB_AGENT_INTERACTION_PROTOCOL.md` | no durable raw secrets, transport isn't authority, artifacts aren't PASS | hostile instructions embedded in externally obtained artifact crossing Agent boundary | PARTIAL_UNTRUSTED_INPUT_GAP |

Source-limited verdict: 18/18 have **identified existing owner candidates**; **0/18 newly executed v4.11 proof fixtures**. Therefore `OWNER_DISCOVERED` does not equal `REQUIREMENT_IMPLEMENTED` or `P1/P2/P3 PASS`. Domain completeness beyond these fixtures also depends on supported-envelope applicability, not arbitrary mapping count.

### 2. Critical composition dimensions and ownership

| Boundary | Canonical resolution surface | Material negative class |
| --- | --- | --- |
| Effective-rule precedence | `PROJECT_ADOPTION` + `DEVELOPMENT_WORKFLOW` Gate Authority / pinned Product/Architecture/Task | two agents applying inconsistent subset of required gate (F02) |
| External side effects | `EXTERNAL_SYSTEM_EXECUTION` + `DATA_MIGRATION`; `EXECUTION_ARCHITECTURE` owns actor handoff | possible-success ACK failure, duplicate attempt on reassignment (F03) |
| Instruction/data/promoted authority | `GITHUB_AGENT_INTERACTION` + `CONFIGURATION_SECRETS` + `WORKSPACE_ARTIFACT` | trusted actor transports untrusted injection/secret (F04) |
| Reviewer arbitration | Existing Review/Validation aggregation / Work Item & Merge ownership | conflicting accepted same-head verdict (F06/#785) |
| Actor eligibility + scheduling | `EXECUTION_ARCHITECTURE` §27; Dispatch/Agent Event schema under Interaction owner | provider-only rejection; critical gate starvation; unauthorized resource ranking |
| Source/contract currentness | Interface Compatibility, Dependency/Toolchain, Validation, Release | future source change/archival evidence wrongly promoted to Product/Validation |
| Machine projection | `standard-manifest.json` semantic_authorities and verification suite | prose/schema/template mismatches; stale registry pin acceptance |

### 3. Owner notes and materiality

- `EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` **already explicitly prohibits unsafe non-idempotent side-effect retry** (§10). v4.11 must not write a duplicate generalized retry standard; only settle *cross-Agent outcome-uncertainty/reconciliation proof*.
- `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` already covers change operations, deprecation and explicit compatibility dimensions. OpenSpec-inspired spec reconciliation must preserve this owner and avoid a rival Product Freeze.
- `PROJECT_ADOPTION.md` already defines A0–A4 immutable pin and non-weakening floor. New need is a *testable effective-rule trace/oracle*, not a second precedence owner.
- `EXECUTION_ARCHITECTURE_STANDARD.md` already has composite eligibility and hard predicates before optimization ranking. No new scheduler service; #932 is liveness/routing hardening.
- `VALIDATION_STANDARD.md` already keeps real tuple PASS, `RELEASE_STANDARD.md` owns closure. Do not equate source-only L1 owner coverage with actual conformance test execution.

### 4. Outstanding evidence that Product authority must disposition

```ini
OWNER_COVERAGE_LEDGER=PREPARED_SOURCE_ONLY
CROSS_PROFILE_TESTS=NOT_RUN
EFFECTIVE_RULE_COMPOSITION=PARTIAL
EXTERNAL_SIDE_EFFECT_CROSS_ACTOR_RECONCILIATION=PARTIAL
UNTRUSTED_AGENT_MESSAGE_BOUNDARY=PARTIAL
SPEC_DELTA_CURRENT_BASELINE_RECONCILIATION=PARTIAL
SOURCE_LICENSE_REUSE_SPINE=PARTIAL
REVIEW_CONFLICT_BEFORE_MERGE=GAP
RELEASE_CANDIDATE_HIDDEN=NOT_RUN
FULL_ISO_CLAUSE_EQUIVALENCE=UNKNOWN
NEW_NORMATIVE_OWNER_FAMILY_REQUIRED=NOT_PROVEN
NEXT=FRESH_PRODUCT_REVIEW_ON_DRAFT_V0_2;THEN_PRODUCT_AUTHORITY_PRODUCT_FREEZE_DISPOSITION
```

No native Task DAG expansion, v4.10 blocker, new scheduler, new mandatory gate or source mutation. These proposed Product-level requirements need genuinely fresh independent review and later L2/implementation/real-host falsification.
