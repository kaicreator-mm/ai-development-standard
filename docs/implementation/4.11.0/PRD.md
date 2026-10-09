<!--
v4.11 PRODUCT FREEZE CANDIDATE — NON-FROZEN until explicit Product authority.
Canonical preparation subject: #938@6067371136, independently reviewed PASS #941@6067535335.
This Git file recontextualizes the source document; it must be independently checked as an exact Git blob before any Freeze.
Historical drafting labels, including "SUBJECT=this_GitHub_comment" in source below, refer to the authoring record, NOT Git blob identity.
The actual Git blob + HEAD/tree and Product Freeze authority must be bound separately.
-->

# ADS v4.11 Unified Draft PRD v0.3 — R2 Bounded Successor / NON-FROZEN

**Entire self-contained successor Product candidate; supersedes v0.2 #938@6066695101 as proposal, NOT as history.** Inputs: Program L1 #938 body, source ledger #938@6066716255, Review R1 #939@6066443254 and Review R2 **#940@6066993773 CHANGES_REQUESTED (2×P1 + 2×P2)**. Source baseline `kaicreator-mm/ai-development-standard:version/v4.10.0@35a4016bb5421811a2ababbc3d0609c88304c6b5` (tree `d1c530f1f3ae40ea381d3fe24def3a0cd6f3ee2c`). Read-only v4.11 Product planning; v4.10 frozen Product/L2/DAG/closure not reopened.

```ini
VERSION=4.11.0
DRAFT_PRD_REVISION=v0.3
SUBJECT=this_GitHub_comment;new_content_digest_to_be_bound_by_independent_reviewer
STATUS=DRAFT_NOT_FROZEN
ONE_ADS_STANDARD_PIN=YES
A=INDIVIDUAL_AGENT_ENGINEERING_CONDUCT
B=MULTI_AGENT_INTERACTION
B_SCHEDULING=SUBFUNCTION
C=COMPOSITIONAL_CORRECTNESS
FRESH_PRODUCT_REVIEW_R3=REQUIRED
P1_A_RELEASE_PROOF=NOT_RUN
P2_B_RELEASE_PROOF=NOT_RUN
P3_C_RELEASE_PROOF=NOT_RUN
PRODUCT_FREEZE=NO
L2_TASK_DAG_IMPLEMENTATION=NO
NEW_RUNTIME_SCHEDULER_DATABASE=NO
```

## 1. Product thesis and users

ADS is a **single comprehensive, internally coherent, mature-practice-assimilating and evidence-verifiable AI-native software engineering STANDARD**, not a particular coding agent/runtime/scheduler. One repository/project pins ONE ADS immutable revision and every participating Agent or human executes only its role/task/stage/profile-applicable rules. Different coding agents, transports and build systems may implement ADS but cannot import competing development-method authority.

**A — Agent Engineering Conduct:** a single authorized Agent can correctly act as Product researcher/Architect/Planner/Builder/Reviewer/Validator/Controller under role-scoped professional process requirements including L1, PRD, architecture, tests, security, dependency, licensing, implemented-spec consistency, maintenance and release. It must NOT impersonate independent Review/real-host evidence it cannot produce.

**B — Multi-Agent Interaction:** role/capability/authority, delegation vs responsibility handoff, communication, task allocation, protected claims, **scheduling as a subset**, concurrent write isolation, evidence transfer, independence, conflicting verdict, human control, recovery and integration. No second scheduler/state database.

**C — Compositional Correctness:** A+B under shared pinned truth must preserve rule applicability, authority, exact identity, provenance, trusted/untrusted content boundaries, negative results, single-claim and safe side effects. Different agents may choose different lawful schedules/reviews but cannot change hard eligibility, gate or evidence meaning by transport/provider swap.

This v4.11 **Product chapter structure** does NOT mint new canonical owners; retain v4.10's seven conceptual planes and existing owner graph, GitHub durable source of truth and non-weakening floor. One version, many bounded concerns/PRs. No migration of v4.10 #865/#900/#916 operational closure.

## 2. Finite applicability scope and compound-job closure — R2 F01R2 P1 repair

### 2.1 Explicit supported vocabulary

- **Archetypes:** LIBRARY, SERVICE, CLI.
- **Condition:** NEW, BROWNFIELD.
- **Adoption:** A0_COMPATIBILITY, A1_MANUAL_PROTOCOL, A2_MACHINE_CONTRACTS, A3_DERIVED_AUTOMATION, A4_FULL_ORCHESTRATION. This changes implementation mechanism, **not** required authority/evidence gates.
- **Jobs (MULTI-LABEL IS ALLOWED):** J01_INTAKE_RESEARCH, J02_DOCS_LOW_RISK, J03_BUG_FIX, J04_FEATURE_CONTRACT, J05_PUBLIC_API_CHANGE, J06_PERSISTENT_DATA_MIGRATION, J07_SECURITY_VULNERABILITY, J08_EXTERNAL_WRITE_DEPLOY, J09_RELEASE_QUALIFICATION, J10_INCIDENT_RECOVERY, J11_DEPRECATION_RETIREMENT, J12_UPSTREAM_REUSE.
- **Roles:** PRODUCT_OWNER, ARCHITECT, PLANNER/CONTROLLER, BUILDER, VALIDATOR, INDEPENDENT_REVIEWER, RELEASE/INTEGRATION_CONTROLLER; HUMAN_AUTHORITY where required. An executor may hold compatible roles but independence is never inferred from identity/model coincidence.
- **Execution modes:** ONE_AGENT or MULTI_AGENT; WEB/LOCAL plus proved granular permissions, real host/device/platform/toolchain and evidence requirements. A single-agent scoped job may require independent handoff or return NOT_RUN/BLOCKED, never self-upgrade to required independent PASS.
- **Boundary:** AI software engineering including security fixes, contract changes, maintenance, incident-driven engineering changes and controlled software/API retirement; not a universal SRE platform or ISO certification service.

### 2.2 Effective obligation closure rule (Product behavior)

Any work item MAY be `jobs={J03,J06,J07,J08,...}` rather than one mutually exclusive job. Its **applicability/evidence obligation closure** MUST be derived from:
`ADS immutable pin + archetype + project condition + adoption profile + declared job-label SET + actual risk/contract/security/external-effect dimensions + actor roles + authoritative Frozen Product/L2 + project overrides + Task/Work/Execution facts`.

Compute **all materially applicable requirements** across the job set, not choose a single dominant J label or omit secondary dimensions. Distinct compatible requirements compose by **logical AND / obligation union** (for example a security Review **and** migration recovery validation **and** authorized deploy-effect reconciliation), NOT a collapsing single PASS. Within the same concern, authoritative precedence resolves permitted strengthening/narrowing while preserving the required floor; incompatibility, stale/missing material basis or irreconcilable owner conflict yields `UNKNOWN/CONFLICT` to owner adjudication, never silent N/A, auto-approval or lowest common denominator. Job labels are aids to identifying obligations, not permission to skip unlabelled material facts.

The **finite coverage denominator** is the declared archetypes/conditions/adoption/roles/jobs + authoritative applicability closure and material equivalence classes, NOT only the count of demonstration fixtures. For any combination not exercised, auditor must either:
(a) cite a tested owner+equivalence class that preserves every mandatory predicate, (b) list it as `UNVERIFIED` and assess Product/release impact, or (c) provide an authority-accepted explicit scope exclusion and its consumer impact. An Agent cannot call unsupported combinations `NOT_APPLICABLE` for convenience. Product Freeze needs a reviewable *bounded* applicability/negative oracle, not execution of the full combinatorial cross product; mandatory implementation/release gates later demand selected actual executable evidence, no fabricated completeness percentages.

### 2.3 Required material intersections / equivalence classes

| Class | Supported compound jobs | REQUIRED combined obligations | Negative oracle | Disposition in v4.11 |
| --- | --- | --- | --- | --- |
| X01 high-risk compound | SERVICE/BROWNFIELD/A0 `J03+J06+J07+J08` | security Review + baseline/target migration state and interrupted recovery + deployment side-effect authorization/idempotency + applicable human decision | A0 chooses J07 alone and drops J06/J08 → DENY | **REQUIRED_IN_V411** cross-cutting conformance |
| X02 contract+reuse | LIBRARY/A2 `J05+J12` | exact upstream/license/currentness + Contract delta + producer/consumer impact + spec reconciliation | upstream version/license changed but old accepted spec/reuse PASS retained → DENY | **REQUIRED_IN_V411** |
| X03 incident + data restoration | SERVICE/BROWNFIELD/A3 `J06+J08+J10` | incident target/permission + operation outcome uncertainty + recovery/compensation evidence | successor replays timed-out destructive migration → DENY | **REQUIRED_IN_V411** |
| X04 release + security | SERVICE/A4 `J07+J09` | security risk/gate review AND exact candidate/visible/Hidden/RQ evidence when required | security fix concern PASS promotes release PASS → DENY | **REQUIRED_IN_V411** |
| X05 parallel/public API | LIBRARY/A3 `J04+J05` | frozen public contract + writer separation + conflicting change impact + exact version/review | each child PASS but merged public contract breaks consumers → DENY | **REQUIRED_IN_V411** |
| X06 retirement + reuse | LIBRARY/BROWNFIELD/A1 `J11+J12` | compatibility/deprecation windows + source license/provenance + consumer impact | remove upstream-backed API without declared migration window → DENY | **REQUIRED_IN_V411** |
| X07 release + external deploy | SERVICE/A4 `J08+J09` | exact release candidate + explicit deploy permission + environment/source/target identity + truthful real-host result | green CI interpreted as production deploy/Hidden PASS → DENY | **REQUIRED_IN_V411** |
| X08 low-risk mixed | CLI/A0 `J02+J03` | only genuinely applicable affected checks and role duties; no mandatory speculative research ceremony | documentation-only change silently hides a security/API delta → DENY | **REQUIRED_IN_V411** |

These eight classes are **representative mandatory intersections**, not a claim of universal pairwise completeness. Any unlisted combination that materially changes owner, permissions, gate or evidence must be classified by the same deterministic closure rules and a reviewable `MATERIAL_INTERSECTION_UNKNOWN` disposition if not yet proven. No new task Issue per class or 12-job powerset explosion.

### 2.4 Standard acceptance fixtures

Preserve 18 **mandatory** S01–S18 from v0.2, as exact reference matrix in #938@6066695101 §2.2 / companion owner-evidence ledger #938@6066716255; adoption and subjects are unchanged. v0.3 makes that inherited bounded fixture list explicit, not optional. Supplement S01–S18 with **X01–X08** derived compound obligation classes above; each has at least one negative oracle, and X01 must actually test all four jobs simultaneously in one work/transition subject. S18 tests hostile instructions + secrets across at least GitHub + second permitted transport. `OWNER_DISCOVERED` is not `BEHAVIOR_PROVED`; 18/18 source owner mapping, zero executed v4.11 proofs at this stage.

**Human denial modification (B11R2 P2):** S08 must include an explicit durable, authorized human **DENY/WITHHOLD** deployment, followed by an otherwise READY successor Agent attempting the same side effect. It must remain blocked; an unchanged denial cannot be erased by a new worker, expired chat or claimed `CONTROLLER_PASS`. S11 must also check that refusal to authorize release does not become `READY` by schedule/majority. Valid superseding human authorization needs exact current decision identity, owning authority, explicit scope and replay-currentness proof; no mandatory human line-by-line diff inspection.

## 3. Twelve v4.11 Product requirements (all one ADS owner graph)

- **R01 ONE_STANDARD_AND_EFFECTIVE_RULES (REQUIRED):** Single pinned ADS development-method authority; each applicable rule resolves to source, version, owner, profile and why it applies. Conflict/UNKNOWN fail closed; lower-authority overrides cannot weaken Frozen Product, required gate or evidence.
- **R02 INDIVIDUAL_AGENT_ENGINEERING_CONDUCT (REQUIRED):** An Agent in every declared supported role/job/profile resolves input, engineering practice, allowed mutation, evidence and exit/handoff; material omissions become GAP/UNVERIFIED.
- **R03 MATURE_PRACTICE_ASSIMILATION (REQUIRED):** Material best practices are **absorbed into ADS's normative owner and executable conformance**, not simply catalogued or delegated to separate SDLC installations. Specific mandatory selected outcomes defined in §6.
- **R04 CHANGE_SPEC_AND_UPSTREAM_CURRENTNESS (REQUIRED):** A change declares baseline, proposed delta, authority, affected implementation/spec/contract, revalidation and reconciled accepted state; immutable historical spec/change and upstream evidence never self-promote to current PASS.
- **R05 IMPLEMENTATION_ASSURANCE_AND_TRUST (REQUIRED):** Implement/check/test/security/license/real-build evidence stays exact, scoped, truthful. External content is untrusted until authority/evidence promotion is verified; no unauthorized secret transfer or side effect.
- **R06 MULTI_AGENT_INTERACTION (REQUIRED):** Actor roles/capabilities, delegation, communication, handoff, Dispatch/Claim, concurrency, scheduling, independent Review, arbitration, recovery and human decision contracts are valid end-to-end.
- **R07 PROVIDER_NEUTRAL_ELIGIBILITY (REQUIRED):** Role, actual capability, environment, authorization, independence and currentness determine legal eligibility. Provider/model is provenance absent justified exception. WEB cannot fabricate LOCAL evidence; old frozen actor-bound history stays intact.
- **R08 SCHEDULING_AS_INTERACTION (REQUIRED):** Hard predicates precede priority/cost ranking; critical legal gate liveness and advisory-issue nonblocking behavior avoid self-inflicted stalls. No second scheduler/authority.
- **R09 DISPATCH_REVIEW_MERGE_SAFETY (REQUIRED):** Pinned schema prepublish, atomic/serialized legal Claim, contradictory same-subject current Review arbitration before Merge, root-cause Repair and successor exact-head evidence.
- **R10 COMPOSITIONAL_CORRECTNESS (REQUIRED):** Actor/transport path cannot change hard required obligations, evidence truth or legal state transitions. Compound J closure + X classes and safety/liveness uncertainty are explicit.
- **R11 FACTUAL_ENGINEERING_LEARNING (REQUIRED BOUNDED EXISTING-OWNER):** Evidence-backed lessons/decisions and failures with source/currentness/epistemic strength feed later work, no raw private deliberation or auto normative authority.
- **R12 STANDARD_CONFORMANCE_ADOPTION_AND_RELEASE (REQUIRED):** Prose/owners/manifest/schema/templates/prompts/fixture verifier mutually consistent; Minimum ADS remains legal, Advanced supports heterogeneous workers; Product Freeze and executable release proof separate.

## 4. Mandatory effective-rule and trust/side-effect invariants (R1 passed in R2)

- `EFFECTIVE_RULE_TRACE`: pinned ADS revision + authoritative Product/L2/Task refs + adopted profile/overrides + applicable combined job dimensions + owner/precedence/strengthening + reason, exact requirement and required gate. An A0 or A4 worker MUST share the same non-weakening mandatory floor. `CONFLICT/UNKNOWN` are **resolution dispositions**, not new Validation Gate states.
- `EFFECT_OUTCOME_UNKNOWN`: after a possibly applied external mutation with lost ACK, no second Agent blindly retries. Need actual idempotency/dedup proof on effect ID, state reconciliation, or authorized compensation with proof; otherwise BLOCKED for a certainty-required effect. No exactly-once blanket promise.
- `UNTRUSTED_CONTENT`: GitHub comment, retrieved doc, tool response, A2A/MCP artifact and generated handoff may contain instruction-like hostile data. Source/transport identity does not upgrade text to policy, approval, Review PASS, merge authority or credential access. Enforce attribution/currentness, scoped redaction, secret refs and authorized admission.
- `CONFLICTING_REVIEW`: same exact HEAD, two accepted current contradictory Reviewer judgments, including P1 CHANGES_REQUESTED, cannot be resolved by “latest PASS” or averaging models; an authorized durable reconciliation is required before Merge.
- `TRANSPORT_EQUIVALENCE`: only equivalent **hard predicates, evidence validity and legal transition constraints**, NOT identical schedule/model judgment/result order.
- `HUMAN_CONTROL`: authorized human DENY/WITHHOLD of destructive/scope/release action remains durable, and any successor must re-evaluate; only owning authority can supersede on exact current subject.
- `PROPORTIONALITY`: low-risk docs/Fast Path need no artificial full Product research; missing mandatory evidence cannot be called N/A because costly.
- `IMMUTABLE_AUTHORITY`: GitHub/repository+exact evidence owners determine truth, not chat, CI latest pointer, raw tool output, capability or optional scheduler cache.

Canonical owner placement remains `PROJECT_ADOPTION`, `DEVELOPMENT_WORKFLOW`, `INTERFACE_COMPATIBILITY_GOVERNANCE`, `DEPENDENCY_TOOLCHAIN_GOVERNANCE`, `CONFIGURATION_SECRETS`, `EXTERNAL_SYSTEM_EXECUTION`, `DATA_MIGRATION_GOVERNANCE`, `GITHUB_AGENT_INTERACTION`, `EXECUTION_ARCHITECTURE`, `VALIDATION`, `RELEASE`, `Task Learning`, `standard-manifest` projection. L2 selects minimal compatible schema/template/tests and need for executable Demo only after Freeze.

## 5. Six mandatory release concerns (closed bounded v4.11 ship set)

1. **Applicability + Effective Rule + Compound Job Closure**: Machine-checkable or deterministic validated rules under existing owners, one ADS pin, negative security override/role/evidence matrix, no invalid N/A; implement X01–X08 with appropriate representative executable conformance.
2. **Multi-Agent Interaction & Eligibility**: Provider-neutral role/capabilities and Fresh WEB/LOCAL admission/review, genuine independence, protected claim, human denial, legal gate liveness; no general agent runtime.
3. **Dispatch/Assurance Integrity**: Pinned-schema prepublish, same-head review disagreement fail-closed, bounded repair/re-review and exact candidate identity.
4. **Cross-Agent Recovery and Trust**: Uncertain external mutations, idempotency/reconcile/compensation and malicious/untrusted payload/secret protection across at least two permitted transports.
5. **MATURE CAPABILITY INCORPORATION, NOT JUST EVALUATION**: Both selected material, supported Product outcomes in §6 **MUST BE NORMATIVELY INCORPORATED INTO EXISTING ADS OWNERS, VERIFIED BY NEGATIVE AND POSITIVE CONFORMANCE**, namely (a) accepted-spec/requirement delta/currentness reconciliation on material J05 and (b) source-attributed upstream-reuse decision/evidence-spine and invalidation on material J12. Existing proven equivalent requirements may be marked ALREADY_SATISFIED only with exact current owner + falsification evidence; an assessment-only `EVIDENCE_ONLY` or unimplemented “future candidate” cannot satisfy either required outcome.
6. **A+B+C Release Proof and Minimum/Advanced Adoption**: Multiple bounded PRs in ONE v4.11; selected S/X realistic positive/adversarial trials, deterministic verification, true real-host/build where applicable, Candidate Freeze, Hidden, Fresh Closeout, Release Qualification and main/tag. Cross-project dogfood for A0/A1 and A3/A4 without runtime mandate.

The one-release scope is **not** “implement every discovered standard practice”. It is the six finite cross-owner outcomes above, plus honest disposition of all candidate practices and existing Issues. If a supported, materially required behavior in this ship set lacks an owner/conformance, only `REQUIRED_IN_V411`, proven `ALREADY_SATISFIED_WITH_EXACT_OWNER`, or a **formal Product authority scope change with impact** can resolve it. `EVIDENCE_ONLY` is valid solely for preliminary/optional/inapplicable/rejected research, **never as loophole for J05/J12/R01–R12 mandatory outcome**.

## 6. Selected mandatory-practice version/license/ADS-owner equivalence ledger — R2 F05R2+F08R2 repairs

Pinned **as-observed upstream source identities for Product selection**, not installed runtime dependencies and not copied source. Each selected MIT repository's exact `LICENSE` blob inspected; incorporation here means original ADS normative rules and tests, not literal redistribution, so license copying obligations arise only if substantive protected source/text is reused. A future upstream update is NOT self-applicable and must trigger evidence review; do not use moving main as a normative pin.

| Selected mature-practice source/version | License/access & evidence | Mandatory ADS outcome and pinned existing owner(s) | Equivalence/gap and negative case | Adoption overhead / Product decision |
| --- | --- | --- | --- | --- |
| **OpenSpec** `Fission-AI/OpenSpec@9111a7654d7800391459431fff4eaf66e33a3d2e`; `docs/concepts.md` blob `824795b6590c3f65fa23b05f98eff913075e5aac` | Public source; `LICENSE` blob `84c125ae7b8ee08dc5b6e06358ebb6134f45a4c4`, **MIT**. Docs describe separate current specs vs proposed changes, ADDED/MODIFIED/REMOVED and merge/archive | **REQUIRED_IN_V411** accepted requirement/spec-delta and implementation-currentness reconciliation for J05/J04/J03; existing `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md@266aefe32e0990c24fc8c1d6d731c4a3456fc3fc` + `DEVELOPMENT_WORKFLOW.md@a7fef842927e58a93b671fe9869b9395559845ac` + Product Freeze/Validation owners | Existing owner covers baseline/candidate/change operation/compatibility but does NOT by itself prove accepted current-spec matches implemented behavior. **Must strengthen** accepted delta+changed contract+required verification+current-source truth; negative: archive/sync alone **never** makes Product Freeze, implementation PASS or stale baseline current | **No OpenSpec CLI/install mandatory**. One bounded change-spec evidence extension using existing Product/Compatibility/Task refs; no duplicate spec authority. Status GAP_REQUIRED; actionable even if OpenSpec upstream changes |
| **Spec Kit composition** `github/spec-kit@93989802b1401c99cc7de6e4ed76572f9cb662e8`; `docs/guides/customization.md` blob `2edf6971bbc2dc1044fc56e6d0be6ce256bf9c81`, `docs/reference/bundles.md` blob `81bceaacb8a5d4d39223ce45815b12566098d7b1` | Public source; `LICENSE` blob `28a50fa22639e32febe14e4ffc7a732b0ba8c90a`, **MIT**. Docs show preset/project overlay precedence, pinned bundle components, provenance and idempotent apply | **REQUIRED_IN_V411** effective ADS rule/profile applicability and provenance (R01/R12), existing `PROJECT_ADOPTION.md@aac0d4bff0ed67e6e23d89903e58732524cab024`, `standard-manifest.json@c4fc9ecf9bfdedf10cfe5da5f05818d27e45757a`, Workflow owner `a7fef842...` | ADS already has immutable pin/override/gate floor. **Must prove** effective rule provenance/priority and refusal to weaken mandatory gates, under compound jobs. Negative: project-local profile claims security review unnecessary against Frozen required Review → CONFLICT/DENY | **No Spec Kit extensions/bundle/runtime installed**. Improve own manifest/profile resolution and golden negative cases rather than importing Spec Kit’s priority chain blindly (ADS authority ordering differs). Status EXISTING_PARTIAL+REQUIRED_CONFORMANCE |
| **Reuse-First prior art workflow / upstream provenance** anchored by **ADS native dogfood #929/#930/#931** (live historical Issue sources) and pinned ADS `prompts/L1_PRODUCT_EVIDENCE.md@a0c7eb74d7bcc46bf7321dc6daa11a3b4f09eed6`, `ARCHITECTURE_DESIGN_STANDARD.md@66218c8a2779a9f84c67433426b9c5512f9f831a`, `DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md@5501ee46708c612071647be85bf7a368c6473cbe` | ADS-native evidence and external source identity discovered during actual J12 reuse decision; **not** attributed to one competitor's license or unlicensed third-party text | **REQUIRED_IN_V411** L1 competitor/neighbor discovery→L2 H1 pattern/H2 reconstructed semantics/H3 direct reuse/BUILD_NEW decision with explicit upstream source ref, license/access/compatibility/security and L3 exact reference/test/error+currentness. Existing owner partially covers local stage facts, not continuous evidence/invalidation | Negative: H3 external source changes license/revision or test behavior, earlier H3 reuse equivalence automatically promoted → DENY until authorized re-evaluation | **No mandatory upstream catalog or runtime**. Proportional per material reuse; no forced external research for already-scoped fast path. Status MATERIAL_GAP_V411 |
| **BMAD** `bmad-code-org/BMAD-METHOD@bda3c5929f672019b90f39a3ea27259d35d00974` | Public MIT `LICENSE` blob `557212d307dbed13aa72e8f158c9e4a626a3243a`; docs not independently proof-mapped for mandatory particular practice | `EVIDENCE_ONLY/OPTIONAL_PROFILE`: adaptive role and planning-depth ideas, use existing Task Decomposition/Workflow without mandatory roleplay | No gap adjudicated material to declared required S/X outcome solely from BMAD documentation | No BMAD installation requirement; adoption non-goal, further L2 research optional |

For the **selected required** OpenSpec and Spec Kit semantics, version/source/license/access, chosen applicable J, ADS owner exact blobs, source-document evidence, gap, expected positive/negative outcomes, and adopter cost are pinned ABOVE before Product Freeze. L2 retains freedom to select semantic projection, choose examples, schema fields and actual runtime/code implementation. The upstream `main` branches may move later; this historical L1 selection stays exact.

Additional ISO/IEC/IEEE 12207:2026, ISO/IEC 25010:2023, NIST SSDF, SLSA 1.2, SPDX, MCP specification 2026-07-28, A2A and DORA remain **DOCUMENTED_REFERENCE / OPTIONAL_APPLICABILITY_RESEARCH**, not automatically `REQUIRED_IN_V411` complete certification. If existing ADS required security/source/Build Host/release practice is applicable, it remains required **because ADS owns it**, not because entire external standard is inherited. Do NOT infer full ISO clauses from public summary, SPDX latest without pinned revision, or MCP/A2A remote task state as ADS release authority.

## 7. Prior issues and bounded disposition authority

- Mandatory owner hardening candidates: `#929 #930 #931 #890 #932 #783 #785 #926`, plus material residuals from `#696 #680 #775 #803 #807 #811 #186`. Issue OPEN does not prove missing behavior; each needs exact current owner and test residual after predecessor release.
- `#893@6065865144` WEB research, `#894@6002850863` LOCAL audited earlier exact revision, `#896@6065878473` Product scope synthesis: bounded evidence consumed, not whole-version PRD freeze.
- `#469` low-cost evidence remains unproven economic efficacy; no mandatory low-cost routing. `#810/#821` old mandatory line-by-line human review was superseded by v4.10 human controllability; do not resurrect. `#779/#865/#900/#916` are v4.10-owned release/operational duties, do not migrate or turn into v4.11 blocker.
- Before Freeze, each material Issue/practice gets `REQUIRED_IN_V411|ALREADY_SATISFIED_WITH_EXACT_OWNER|OPTIONAL_PROFILE|EVIDENCE_ONLY|EXCLUDED_WITH_REASON`, with Product authority justifying any scope narrowing and impact. No Issue creation per fixture/claim; only real bounded concerns are Task DAG materialized after Freeze/L2.

## 8. Acceptance and separation of truth gates

**Product Freeze preconditions**: independently reviewed exact immutable Draft v0.3 content, finite scope above (including multi-label closure), mandatory compound negative Product oracles, effective rule/side-effect/trust/human veto semantics, selected upstream exact sources and owner dispositions, bounded six-ship-concern set, material Product UNKNOWNs with actual Product authority decision; independent reviewer verdict is evidence only. Prefer durable Git-tracked PRD as Frozen authority; Issue comment is currently DRAFT, not a magic SHA-pinned Frozen blob.

**After Product Freeze**: L2 unique normative owner placement and risk-driven demos; Task DAG small concerns with real native dependencies; per-concern real tests/Validation/Review and expected-head merge; full version conformance P1/P2/P3 on actual executable selection including S/X fixtures; Candidate/Hidden/Fresh Closeout/Release Qualification and immutable main integration. A Product Review PASS does NOT prove a delivered executable standard, real-host PASS, Hidden PASS or a release.

Defect/adversarial cases: R2 F01R2 **compound J union** X01; F05R2 **genuine incorporation not evaluation** J05/J12 under §5/§6; F08R2 **exact version/license/owner/gap** ledger §6; B11R2 **human denied deployment/release** S08/S11. R1 F02/F03/F04 and R2 PASS findings remain preserved without claim that any unexecuted tests passed.

## 9. Current terminal

```ini
V411_DRAFT_PRODUCT_v0_3=PREPARED_NON_FROZEN
REVIEW_R1=#939@6066443254_CHANGES_REQUESTED
REVIEW_R2=#940@6066993773_CHANGES_REQUESTED
REVIEW_R2_REPAIRS=F01R2,F05R2,F08R2,B11R2
SELECTED_REQUIRED_INCORPORATIONS=OPEN_SPEC_DELTA_RECONCILIATION;SPEC_KIT_INFORMED_ADS_RULE_COMPOSITION;ADS_REUSE_FIRST_EVIDENCE_SPINE
ONE_RELEASE_MANDATORY_CONCERNS=6
MATERIAL_COMPOUND_CLASSES=8
CURRENT_PROOF_EXECUTIONS=NOT_RUN
NEXT=GENUINELY_FRESH_INDEPENDENT_PRODUCT_REVIEW_R3_OF_NEW_EXACT_COMMENT
PRODUCT_FREEZE=NO
L2_TASK_DAG_IMPLEMENTATION=NO
```

