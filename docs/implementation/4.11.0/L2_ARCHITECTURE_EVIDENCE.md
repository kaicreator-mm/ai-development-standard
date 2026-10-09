# ADS v4.11.0 — L2 Architecture Evidence v0.2 (R1 REPAIR CANDIDATE; NOT FROZEN)

> **Stage 2 architecture proposal / review subject.** No implementation, Task DAG, L2 Freeze, release branch or merge authority follows merely from this document. Its Product authority is [#943@6084264198](https://github.com/kaicreator-mm/ai-development-standard/issues/943#issuecomment-6084264198), not the historical NON-FROZEN headings inside the immutable PRD. A genuinely independent fresh Architecture Review and explicit L2 Freeze disposition remain required.

```ini
REPOSITORY=kaicreator-mm/ai-development-standard
VERSION=4.11.0
L2_REVISION=v0.2
L2_STATE=CANDIDATE_NOT_FROZEN
PRODUCT_AUTHORITY=#943@6084264198
FROZEN_PRD_COMMIT=34df09a2433aec5523ab80c90e885f6d9fc78803
FROZEN_PRD_TREE=f13bae159050063b32d53e527ec7fa1c157d7ad9
FROZEN_PRD_BLOB=d30f202e8ea662731ff8a4f2ad1ad88cfc5bb179
FROZEN_PROOF_ANNEX_BLOB=f59a6daf5430ece66103a830e392a04f71623ff0
PRODUCT_REVIEWS=#941@6067535335;#942@6068127988
PINNED_EXISTING_OWNER_BASE=version/v4.10.0@35a4016bb5421811a2ababbc3d0609c88304c6b5
PINNED_OWNER_TREE=d1c530f1f3ae40ea381d3fe24def3a0cd6f3ee2c
ARCHITECTURE_MODEL=EXISTING_OWNER_CONVERGENCE_PLUS_SUBORDINATE_PROJECTIONS
IMPLEMENTATION_BASE=NOT_AUTHORIZED_UNTIL_L2_FREEZE;FUTURE_BASE_REQUIRES_CURRENT_MAIN_REBIND
ACTUAL_PRODUCTION_A_B_C_PROOF=NOT_RUN
REAL_BUILD_HOST_VALIDATION=NOT_RUN
HIDDEN_VALIDATION=NOT_RUN
```

## 1. Architecture drivers and decision

Freeze Product means **one pinned ADS method** sufficient for *A* role-scoped individual Agent engineering, *B* provider-neutral Multi-Agent interaction (scheduling subordinate), and *C* authority/evidence-preserving composition. No part of v4.11 may create a rival software engineering framework, Task DAG, scheduler service, shared database, Review authority, or autonomous runtime.

**Decision D1 (candidate): owner-local semantics + additive verifiable projections.** Reuse the v4.10 seven conceptual planes (views only), GitHub exact-revision facts, existing normative owners, current schemas, `scripts/v40_rules.py` / `scripts/v40_semantics.py` and `scripts/verify_standard.py` extension points where actually applicable. Place new semantics inside owner documents and their subordinate schemas/templates/tests. A derived effective-rule trace or semantic verifier is **evidence/projection**, not a new canonical owner, Gate, or platform dependency.

The key architecture composition is:

```text
one immutable ADS pin + current Project Overrides
       + Frozen Product/L2 + current Task/Work/Execution facts
                         |
                applicability closure
           role × profile × multi-J × actual-risk
                         |
         owner/precedence/source-currentness trace
                         |
          all hard applicable obligations (AND)
                         |
     pre-admission legality; role/capability/independence
                         |
 existing GitHub Work/Dispatch/Claim/human decision facts
             /                     \
      A: role-scoped acts       B: cross-agent transport
             \                     /
               C: same hard gates and truth
                         |
      real Validation / Review / candidate / Hidden / RQ
```

Architecture must preserve *legal equivalence*, not guarantee identical schedules, model judgments or cost. Proportional A0/A1 manual and A3/A4 automated adoption both enforce one non-weakening mandatory floor.

## 2. Exact existing owner map and proposed minimal change boundary

This is an **L2 allocation**, not a statement that every missing production behavior is already implemented. Source identities are the exact blobs in the pinned v4.10 baseline, confirmed by live GitHub file readback.

| Concern / Frozen requirement | Existing unique normative owner (pinned blob abbreviation) | What v4.11 can add under that owner | Cannot transfer |
| --- | --- | --- | --- |
| Immutable ADS pin, A0–A4, local overrides, R01/R12 | `standards/PROJECT_ADOPTION.md@aac0d4bf`; `standards/DEVELOPMENT_WORKFLOW.md@a7fef842` | deterministic effective-rule applicability and trace: profile + actual material facts + multi-J closure, explicit contradictions and source precedence; existing manifest as inventory only | lower profile cannot waive hard gates; manifest cannot approve Product |
| Conduct/L1→L2→Task, R02/R11 | `DEVELOPMENT_WORKFLOW.md@a7fef842`; `TASK_DECOMPOSITION_STANDARD.md@f355c020`; existing Task Learning family | stage/role scoped obligations, bounded learning provenance, truthful evidence/hand-off, proportional Fast Path | no second full-SDLC owner or mandatory new agent |
| Accepted spec delta and current implemented contract J05/J04/J03, R04 | `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md@266aefe3` + Workflow and Validation (distinct owners) | accepted changed-spec baseline/delta/current revision, affected producer/consumer window, implementation linkage and invalidation on fresh material change | spec archive/merge is not compatibility, build, Product Freeze or Validation PASS |
| Upstream provenance/Reuse-First J12, R03/R04 | `DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md@5501ee46` + `ARCHITECTURE_DESIGN_STANDARD.md@66218c8a` + L1/Task evidence prompts | H1 pattern, H2 semantics reimplementation, H3 lawful direct reuse, BUILD_NEW decision with exact source/license/change invalidation and L1→L2→L3 trace | upstream/source license alone cannot become executable compatibility or release PASS |
| Agent identity, dispatch/event, review disagreement, R06/R09 | `GITHUB_AGENT_INTERACTION_PROTOCOL.md@ea007939` + existing event/review-finding schemas | exact-current accepted review disagreement projection; human denial event provenance and explicit verified supersession; hostile event data remains untrusted | event text or GitHub API login is not Product or human authority |
| Eligibility, Claim serialization, liveness, R07/R08/R09 | `EXECUTION_ARCHITECTURE_STANDARD.md@0bb9e304` (esp. §§11,27–28); Dispatch schema `f8532bfc` | classify hard eligibility independent of provider branding; protect current claim/key, version and resource atomicity; optional ranking only after legal admission; avoid advisory-gate deadlocks | no new scheduler, lease authority, durable Availability owner or role-specific queues |
| Uncertain external effect + migration/recovery, R05/R10 | `EXTERNAL_SYSTEM_EXECUTION_STANDARD.md@6da46996` + `DATA_MIGRATION_GOVERNANCE_STANDARD.md@df60d132` + execution handoff | causal effect key, attempt/outcome/ACK uncertainty, bounded reconciliation/retry/compensation evidence through successor identity | no exactly-once fiction; external credential/potential ability is not write authority |
| Secret/trust boundary R05/R10 | `CONFIGURATION_SECRETS_STANDARD.md@cda438ad`, `WORKSPACE_ARTIFACT_STANDARD.md@f54c37e9`, Interaction owner | promotion/attribution of GitHub and second external transport payload; reject instruction-like policy override, redact raw secrets | transport trust/authentication ≠ content authority |
| Exact executed proof and independent Review R05/R12 | `VALIDATION_STANDARD.md@1522b85f` + Interaction Review owner | selected new positive/negative conformance, exact tuple and required Review currentness | tests/CI/review source readback are not surrogate real-host PASS |
| Candidate/Hidden/Release/Integration R12 | `RELEASE_STANDARD.md@014f3996` + execution controllers | A/B/C proof matrix for exact candidate; honest S/X and material class coverage / qualification boundary | PR or Product Review PASS cannot create RQ PASS |

**Owner separation:** Compatibility decides *what a contract comparison means*, Dependency decides *what upstream source/license identity means*, Workflow decides *who can make Product/stage acts*, GitHub Interaction decides *what durable Agent facts mean*, Execution decides *what action is legal*, Validation decides *what executed checks prove*, Release decides *whether version is qualified*. Derived checks join these without changing any owner's authority. No duplicate state vocabulary: project Gate remains `PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE`; `UNKNOWN/CONFLICT/UNVERIFIED` are applicability/proof dispositions, not new gate statuses.

## 3. Effective obligation closure algorithm — C's common source

**Inputs (minimum architecture projection)**: project pin + exact revision; project archetype and NEW/BROWNFIELD; adoption level; declared *set* of J01–J12; observed risk/security/contract/migration/effect/release facts (including unlabelled material facts); roles and authorized actor; Frozen Product/L2/Task/overrides; exact relevant owner revisions; current evidence identities and validity windows.

**Candidate algorithm:**
1. Resolve immutable ADS pin and authoritative stage/work identities; reject moving-main, stale/missing material authority.
2. Read each canonical owner using existing precedence; enumerate *every* applicable hard requirement from declared jobs **and** observed facts, project type, affected role, profile and stage. Unsupported/ambiguous classification remains named UNKNOWN with source.
3. Resolve constraints for same concern by lawful priority and non-weakening strengthening. Distinct simultaneously applicable constraints are conjunctive. Never choose a dominant job or a weaker A0 floor.
4. Produce a derived `effective_rule_trace`: requirement id; canonical source path/revision; subject; reason/profile/risk; authority tier; gate/actor consequence; proof ref/currentness; `APPLICABLE | NOT_APPLICABLE_WITH_AUTHORITY | UNKNOWN | CONFLICT` **as trace-local classifications, not new Gate enums**.
5. Before an action, require **all** applicable hard authority, identity, currentness, capability, environment and evidence predicates. A missing material predicate is not true and cannot be rescued by ranking/provider preference.
6. After action/review/release, verify evidence belongs to exact subject and required tuple; material drift invalidates only affected current claims, preserves historical evidence.

### 3.1 R1/F02 — materiality intake is a required precondition, not a best-effort input

Before claiming a low-risk/Fast Path or `NO_MATERIAL_RISK` classification, the applicable existing Workflow/Project Adoption and Task/Review evidence owners MUST establish an **exact-subject affected-surface inventory**: diff or content scope + base/head; dependency or contract impacts; security/permission/secrets; persistent data/migration; external effect/tenant/deploy; release/retirement; upstream license/source; environment/host/role. The required source-of-observation is the actual affected files/contracts/dependencies and existing authoritative work facts, not only `jobs` labels or an optional caller-provided `observed` boolean. For each material dimension, emit one of: `PRESENT` with source/impact, `ABSENT_WITH_INSPECTED_SCOPE` with source and basis, or `UNKNOWN` with blocking consequence. This is a **derived owner-local projection**, not a new risk authority or mandatory heavy security scanner.

- Absence of a risk label or an omitted field **never** means inspected absence. `J02` docs-only shortcut requires a current bounded inspected-surface attestation, and must be invalidated when changed files, selected API/security/role/effect facts or baseline/current HEAD drift. If the actor cannot inspect a materially required affected surface, state UNKNOWN and prevent waiver/merge until lawful owner Review/Validation or risk disposition.
- Product/Task acceptance declares the permitted action and expected affected scope; Implementation compares actual diff and external operations against it before terminal; Reviewer/Validator independently check applicable material dimensions and negative classifications, not merely repeat Builder asserted risk; Merge Controller consumes their current signed/attributed evidence rather than a cached low-risk label. A0 is allowed manual minimal attestation, A3/A4 may automate it, **with identical non-weakening floor**.
- Negative mandatory oracles: `CLI/A0/J02` with a changed access-control, API signature, migration, secret or deploy effect but `observed_risk` missing must **not** admit docs-only PASS; `J03+J06+J07+J08` missing J07 label still inherits actual security/permission requirements. A changed actual contract/risk surface after earlier attestation invalidates its affected claims. No arbitrary full-universe risk certification is asserted.

**Conflict oracle:** A0 SERVICE `J03+J06+J07+J08` whose real work contains security fix, persistent migration, and external deployment must require the union of security Review, migration fresh/upgrade/interrupted recovery, effect authorization/reconciliation, and relevant human decision. Omitting the J07 label while leaving the security fact cannot erase security Review. A profile override contradicting a Frozen mandatory gate produces `CONFLICT` and an unsatisfied gate, not `NOT_APPLICABLE`.

**Additional unexpected-class oracle:** `J09+J10+J11+J12` release+incident+retirement+changed upstream license remains supported and must expose every owner/evidence intersection. It is currently **UNVERIFIED** unless a present, exact, equivalence-backed test proves the full predicate intersection. No exhaustive powerset certification is implied.

## 4. A — Agent conduct architecture

Role-scoped obligations live in existing Workflow, Task, architecture, quality, security, compatibility, dependency and assurance owners. For every applicable role and work item, define an auditable **Input → Allowed acts → Required evidence → Handoff/Exit** selection; automated steps are optional where the profile permits, not new authority. Shared mandatory floor persists even when one Agent sequentially assumes compatible roles. `INDEPENDENT_REVIEWER` may not certify its own builder context; WEB cannot claim real LOCAL platform/build evidence.

Selected material conduct: L1 discovers prior art where decision-material; L2 records H1/H2/H3/BUILD_NEW with provenance; L3 records Tests→Contract→Implementation→Failure→References; J05 reconciles accepted requirement delta with actually implemented current contract; J12 invalidates old reuse claims on material upstream license/revision drift. No compulsory external OpenSpec/Spec Kit install or research on genuinely low-risk Fast Path.

## 5. B — Multi-Agent Interaction architecture

Keep exactly one existing GitHub-native Work Item → Execution Pack → Dispatch → protected Claim → evidence/Review/Validation → merge/release lineage. A subagent is another auditable operator/capability profile in the **same** legal event and authority family; it is never a second supervisory SDLC. `actor_role`, `operator_id/session_ref`, and `transport_actor` remain distinct. Policy hard checks precede optional resource/time/cost ranking.

### 5.1 R1/F03 — canonical reviewer re-route and gate-liveness

An authorized Controller MUST re-route a genuinely unclaimed WEB Reviewer dispatch to a qualified fresh LOCAL Reviewer through the **existing protected-key generation protocol**, not by editing a planning note or silently changing `TARGET_ENVIRONMENT`. Required sequence: (1) read current dispatch/proposal, protected key, expected HEAD/tree, independent-review requirement and all claims; (2) confirm old WEB dispatch is `DISPATCHED_UNCLAIMED`, or if claimed stop for owner-authorized cancellation/recovery and do not manufacture an unclaim; (3) durably CANCEL/SUPERSEDE the old generation with reason and expected-source guard; (4) publish new role-correct proposal and canonical admission with new generation, exact-head/work/permission binding; (5) read back new admission as the latest current protected-key generation and require a fresh distinct LOCAL claim before Review; (6) retain old events as historical, deny any late old-generation claim, and wake legal merge-drain once the truly fresh terminal exists. Missing resource/availability is truthful BLOCKED; OPEN advisory Issues never create executable blockers. WEB/LOCAL independence constraints and real-host capability are rechecked, and cross-key overlap is rejected where mandatory shared resources cannot be admitted all-or-none. Same-key duplicate accepted claims are a negative test; no new scheduler/service is introduced.

**Admission:** work, exact head/base, Task Pack scope, resource/concurrency bindings and protected key must linearize all-or-none through an existing `SINGLE_WRITER_ADMISSION` or proven transactional/conditional-write mode. No per-key success chain may count as atomic composite admission. Publishing an event is not equivalent to an accepted Claim. Publication/ACK uncertainty requires readback of durable facts before replacement admission. Scheduler failure cannot erase independent legal work; an advisory audit issue cannot become a mandatory gate.

### 5.2 R1/F01 — all-surface durable Review and Validation admission before Merge

The existing Interaction protocol owns which GitHub review/issue/validation/repair events are **accepted, current and authoritative**; Merge Controller and Execution own the last pre-merge admission/expected-head action. A Merge Controller MUST re-fetch the *complete relevant durable state*, not merely its task's cached status: PR conversation comments, native PR reviews (including pending/changes-requested states as applicable), linked Task Issue, independent Review Issue/terminals, Validator/repair successor terminals, applicable protected-key claim/admission generations, and Product/L2/Task authority and release/CI prerequisites. Link discovery and relevance/filtering have to be source-bound (explicit referenced issues and native PR linkage), not broad, untrusted free-text string matches. Each included record is classified by actor role/authority, exact HEAD/base, terminal ownership, acceptance/currentness, supersession and observable GitHub creation/update identifiers.

Before merge, record a **bounded observed-state watermark/read-set** over all owning surfaces (per issue/PR latest event IDs/update times, native review IDs/state, fetched HEAD/base identities and validated gate input refs). Confirm all required independent Reviewer/Validator terminal generations have closed and no applicable current blocker remains. Re-read those surfaces **immediately before** a serialized expected-head merge; if a new relevant event, conflicting accepted same-head verdict, unexplained pagination/missing source, concurrent writer or changed ref appears, invalidate the admission, stop and re-sweep. GitHub's distinct Issue and PR APIs are **not a global atomic snapshot**: source-API race or unavailable readback must BLOCK, not be papered over as linearizable. Existing protected Merge Controller single-writer/merge-queue admission and eventual post-merge terminal readback are required, not a new distributed transaction system. A blocker that appears *after* irreversible merge is handled as a new corrective/closeout fact and cannot magically unmerge history; no impossible zero-race global guarantee is claimed.

Required negative evidence: accepted PASS(H) then linked Review Issue P1 CHANGES_REQUESTED(H) before final sweep → DENY; relevant blocker after initial cached PASS but before authorization/readback → re-sweep/BLOCK; contradictory same-H reviews no latest-wins; an old stale-H conflict cannot block unrelated current H2; status/pagination/readback failure → BLOCKED; post-merge surfaced negative recorded for bounded repair/release hold. The exact read-set/watermark and legal merge predicate are normative at the existing owner boundaries; optional scheduler state is never a gate authority.

**Review conflict:** classify accepted current Review records only at the target exact HEAD. Distinct stale-HEAD Reviews remain history. Same-head current PASS vs P1 CHANGES_REQUESTED remains blocking until authority-bound durable adjudication; never latest-wins, arbitrary severity deletion, or model vote.

### 5.3 R1/F04 — durable HUMAN decision provenance and supersession

The existing Product/Workflow authority owner determines who may grant/deny a human-controlled transition and its bounded delegation. GitHub Interaction owns canonical publication/admission of the durable decision record, while Execution/Release use the **exact authorized decision** to control side effects/merge/release. Required minimum evidence fields (as projections under existing owners, not a new event type): actual human authority actor vs shared transport writer; authority basis and delegation ref if any; `DENY/WITHHOLD/APPROVE` effect; exact repository/subject/operation/tenant/scope; decision time and immutable comment/event ref; applicable currentness; linked prior denial and explicit supersession scope; proof that the current approval grant can lawfully supersede the earlier denial. A Controller recording a human act must cite that act; models, tool data and Issue comments quoting `HUMAN_APPROVED` cannot impersonate it.

Acceptance requires owner/authority verification, current exact-subject mapping and fail-closed precedence: an unsuperseded current DENY dominates READY, alternate worker, provider switch or scheduling majority. If the authority holder, provenance/scope or supersession is unverified, hold the requested controlled action. Existing GitHub comments/event-v2 envelopes may carry the record **only when authority has been independently resolved by the owning contract**; transport login and schema validity do not themselves prove human consent. Required S08/S11 negative tests include quoted approval strings, worker-owned forged decision, stale/wrong-subject approval, accepted human denial + later agent READY replay, and valid owner-authorized successor explicitly superseding the exact denial. Do not add a mandatory line-by-line human diff gate.

**Human denial:** a durable authorized `DENY/WITHHOLD` of deployment/release outlives handoff/provider changes. READY, a majority or fresh transport ACK cannot supersede it. A successor approval must identify authority, exact scope and superseded decision, satisfy currentness and use the owning control path. Do not require universal human line-by-line code review.

## 6. C — Cross-Agent composition and trust/failure contracts

Compose **C as independent invariants verified over A and B**, not a third execution state machine.

- **C1 Actor substitution:** same pin/rules/effective hard obligations for WEB↔LOCAL/provider/subagent substitution; capability, permission, real host and independence re-evaluated; unsupported substitution blocked.
- **C2 Delegation:** no privilege amplification through Task Pack→Execution Pack→Dispatch, and no change to Product/L2/Task or gate ownership by subagent handoff.
- **C3 External effect uncertainty:** require source/target/tenant/environment/effect id, operation authority, attempt identity and observed outcome. If mutation may have succeeded without ACK, successor must reconcile from trustworthy external evidence, proven idempotency/dedup semantics, or explicitly authorized compensation. Absent proof, hold unsafe retry BLOCKED. No new database assumed.
- **C4 Untrusted transport:** GitHub issue/comment text, A2A/MCP/tool payload or generated artifacts are data; only authenticated authority acts with current subject and verified schema/owner can change authorization. Magic approval substrings, quoted examples, prompt injection, forged role metadata and secret-bearing instructions must not promote.
- **C5 Exact evidence:** current candidate HEAD and dependent base/head are checked before Review/Merge; changed contract, license, profile or risk may invalidate prior evidence; historical blobs remain immutable.
- **C6 Joint-gate composition:** an applicable required gate may not be converted to `NOT_APPLICABLE` for cost or because another actor has PASS. All required predicates must genuinely hold before releasing side effects or version Qualification.

**Counterexample families:** stale Review conflict accidentally blocks unrelated head; missing protected claim key; empty/unclassified trace returning allow; same-account different-operator independence confusion; post-DENY successor replay; lost ACK double external write; changed upstream MIT→unknown license reusing old H3 PASS; CI-only Release READY. The isolated #945/#946 Python toy uncovered analogous demo-only defects; it is *test inspiration*, not adopted code or a production ADS execution PASS.

## 7. Selected mature capability incorporation — concrete contract decisions

**Spec delta (mandatory J05):** extend *existing* interface/Workflow evidence with `spec_baseline_ref`, `proposed_delta_ref`, `acceptance_authority_ref`, `accepted_spec_current_ref`, `implementation_subject_ref`, `affected_producer_consumer_windows`, `revalidation_refs` when material. These are **candidate additive fields**, not a new canonical schema before L2 review. A change accepted for Product/contract purposes never implies implemented currentness until implemented target + material dimensions are checked on current version. Archive/move cannot silently mark PASS. Owner: Compatibility + Workflow; check results: Validation.

**Reuse-First (mandatory J12):** a source-attributed L1→L2→L3 chain declares exact upstream repository/ref/file/license/access/currentness, alternative H1/H2/H3/BUILD_NEW with security/maintenance/adoption trade-offs, chosen bounded action, tests and change invalidation triggers. Relevant source-license or upstream implementation drift makes earlier equivalence **stale** until re-evaluation. Do not scrape/copy protected source merely to satisfy pattern reuse; upstream historical pins are evidence, not runtime dependencies. Owners: Dependency/Toolchain, Architecture Design, L1 and Task prompts.

**Effective rule provenance (mandatory R01/R12):** derive current owner/source/profile precedence with non-weakening floor from existing Project Adoption/Workflow/manifest. A project-local profile override cannot silently remove a mandatory security or Release gate; any conflict is explicit. The schema/manifest/read-set verifier are projections, not a second rules authority.

**Existing-owner condition:** each future L3 implementation concern must first compare proposed change with existing exact owner plus a required positive/negative oracle. `ALREADY_SATISFIED` only with current source and executable proof. Mandatory selected incorporation cannot be parked as `EVIDENCE_ONLY`.

## 8. Adoption, compatibility, migration and cost envelope

Minimum ADS A0/A1: immutable pin, manual GitHub/repository evidence + small deterministic checks as needed. No mandatory controller process, network service, database, new agent or third-party tool. A2 opts into machine validation; A3/A4 may derive ready sets/claims/conformance from the **same** records. Only mechanisms vary by adoption; required safety floor does not.

Migration must preserve existing v3.4/v4 durable `ai-dev:event:v1/v2`, Task Pack/Execution Pack, `dispatch.schema.json`, `review-finding-v1`, `compatibility-record-v1`, manifest and existing state enums. Proposed fields are optional/additive for historical readers unless a new v4.11 work item explicitly declares a required material fact. Old absent fields become `UNKNOWN` only where a required new judgment truly needs them; old historical PASS remains history, not re-labeled as current. No mass history rewrite or retroactive v4.10/v4.9 release reinterpretation. Confirm template/prompts/schema/prose/manifest/verifier parity before final integration.

## 9. Architecture UNKNOWN register and evidence routing

The rows below are **L2 candidate decisions**, subject to independent challenge. Source evidence may settle owner *location* without proving executable conformance.

| ID | Material architecture question / consequence | Evidence & candidate disposition | Next decision |
| --- | --- | --- | --- |
| U01 | Can canonical existing owner data support multi-J risk+profile closure with deterministic fail-closed trace without creating new policy authority? | Existing Project Adoption, Workflow, Compatibility and manifest give owner/precedence; algorithm placement is source-supported. **STATIC_EVIDENCE_SUFFICIENT for owner partition; actual finite executable proof NOT_RUN.** | L2 Freeze may select owner-local projection; Task validation must falsify security/unknown/compound cases; if source constraints conflict, reopen Architecture |
| U02 | Can an uncertain external write be safely handed to a successor across publication/ACK loss without false retry or second state store? | **#949 E2 local-real PASS, limited:** separate hard-killed processes, persistent real local Git/event facts and append-only effect sink proved no duplicate on E1–E8; source/authority #949@6085049416 + closeout blob `8c58680c6dffc9d861011ffab2f2d40790e42b45`. **Real GitHub API transport, network partition and multi-host CAS are NOT_RUN**; result may not be generalized to them. | **KEEP conditional single-writer existing owner + external reconciliation**. L2 may freeze the fail-closed contract with scoped **local-Git E2** evidence, while remote GitHub/API/multi-host automated recovery remains BLOCKED/UNVERIFIED until actual integration proof. No false exactly-once claim. |
| U03 | Can multi-resource protected Claim be decided atomically across incompatible worker contexts? | Existing Execution §27.3 requires all-or-none single writer/linearizable conditional write; L2 chooses this explicit mode or fail-closed, **STATIC_EVIDENCE_SUFFICIENT for contractual architecture**, integration validation still NOT_RUN | No unproven per-key CAS substitute; implementation must test simultaneous claims and ambiguity |
| U04 | Can current contradictory Reviews and human veto remain binding through successor transport? | Existing Interaction §§9, execution §19 and source owner obligations identify event/authority boundaries; **STATIC_EVIDENCE_SUFFICIENT for placement**, verifier cases NOT_RUN | Exact-head conflict and DENY tests mandatory after implementation; security reviewer to challenge |
| U05 | Can J05 accepted spec and J12 source/license currentness attach to existing owners without competing revision authority? | Interface/Dependency owners have exact source/baseline and change identities; **STATIC_EVIDENCE_SUFFICIENT for placement**, new provenance/invalidation logic NOT_RUN | additive projection schema + currentness tests later; never infer from archival alone |
| U06 | Do S01–S18/X01–X08 plus material equivalents truly cover every selected mandatory owner and supported class? | Product explicitly allows bounded classes; actual owner/test equivalence is **UNVERIFIED**. This is a **release proof obligation**, not an architecture assertion of completeness | L2 matrix sets finite required tests; unexpected material intersections fail closed; no fake coverage percentage |
| U07 | Does live v4.10 predecessor closure authorize v4.11 integration mainline? | **#779@6084781854 RQ READY**, #779@6086103081 immutable baseline and #779@6086126555 Repository Integration COMPLETE on `main@b9461d48d902a2c7c00adff6746afc7a02a0ac3e` (tree `8ce0bbb09b537e4e0361f2b5aaf8aff3537127c7`, tag `v4.10.0`). This is a historical, exact predecessor integration fact, not automatic v4.11 branch admission. | Before v4.11 implementation branch creation, re-read current `main` and immutable predecessor baseline; stage/rebase only through legitimate owner after L2/DAG and preserve Product/L2 pins. |

### U02 R1 execution disposition — bounded exact research subject, not release proof

Author-side #949 terminal `#949@6085049416` reports E1–E8 PASS on an actual *local Git fact plane*, separately launched actors and a real append-only persistent effect sink; external write commits and an ACK is deliberately lost through a hard process kill. Readback #951 / `docs/experiments/v4.11-u02/CLOSEOUT.md@8c58680c6dffc9d861011ffab2f2d40790e42b45` records two fresh-run passes, real effect counts (E2 blocked successor stays 1; E3 initially 0 then one lawful mutation; E4 one accepted claim), negative human DENY/stale tenant/forged event/broken sink, tested toolchain Python 3.14.6 + git 2.52.0 Windows. **This is LOCAL E2 with an E3 process-death subclaim, not live GitHub API or remote cross-host E2; independent #950 R1 predates the terminal, and its CHANGES_REQUESTED remains binding history.**

Decided candidate architecture is **conditional**: the existing external-effect/Execution/Interaction owners must default to BLOCKED/HOLD on missing ACK; a successor may reconcile only by *actual external-effect boundary readback* to exact effect/operation/tenant, proven adapter idempotency/dedup with stable ID, or authorized exact compensation. Timeout, Git commit, event writer validation, `READY` and a local E2 PASS alone confer no new effect authority. Remote GitHub API durability, partial network partition, multi-host claim linearizability and arbitrary provider behavior remain `UNVERIFIED`; if a task depends on them for automatic recovery, block or require later real-boundary conformance before feature/release qualification. A manually authorized hold/reconciliation remains a supported safe behavior without importing the demo harness as a runtime.

### U02 research hypothesis (historical pre-execution question)

*If actor A initiates one authorized external effect and loses its ACK after possible success, then a successor actor B consuming the same existing durable Work/Dispatch/Claim/effect lineage must not issue a second non-idempotent effect until successful externally-grounded reconciliation, proven dedup/idempotency, or authorized compensation; the observable external mutation count remains ≤1 on blocked retry.* The experiment must use a **real** existing GitHub event/authority readback boundary and a real observable effect ledger/adapter under test; unrelated model/provider may be fake. Positive, negative, lost-ACK, duplicated successor, stale currentness, and human DENY cases; counters, exact SHAs, environment, E2 strength and explicit limits. Synthetic #945/#946 cannot be inherited as this E2 proof.

This required experiment must not touch v4.10/main or production providers; if no safe existing seam/environment is available, record `BLOCKED` and reassess only the dependency of a conditional L2 Freeze. Do not elevate unproven "exactly once" claims.

## 10. Conformance and executable acceptance architecture (P1/P2/P3)

For each required reference, store: `fixture_id`; archetype/condition/adoption/jobs/actual risks; owner and frozen requirement refs; actors/permissions/environment; exact start/input/currentness; allowed/denied action; required gates; negative counterexample; execution command/runner/tuple; evidence location; result; equivalence class coverage. The reference registry may be an additive test fixture/projection under existing scripts; it is **not** the canonical source of authority.

- **P1 / A:** S01–S07, S13–S14 plus other role/profile/applicable S cases; J05 accepted delta, J12 source/license changes and negative inadequate-evidence/classification; A0 minimal path remains lawful.
- **P2 / B:** S08–S12, S15–S18; provider-neutral WEB/LOCAL independent role admission, Claim concurrency, human DENY/S08+S11, same-head Review arbitration, critical gate liveness; real evidence vs toy.
- **P3 / C:** X01–X08 mandatory representative intersection negative cases and changed actual-risk no-label behavior, effect successor, Review subject, external trust, license/spec currentness, exact release candidate; unlisted materially distinct supported intersections require current equivalent owner/test proof or `UNVERIFIED/BLOCKED`.

Checks must include **positive + negative**, schema/prose/projection cross-consistency, clean-checkout deterministic suites, permitted real-host validation for material environment claims, full visible regression, Critical Journeys, Hidden, independent Fresh Closeout, Release Qualification, and eventual qualified main integration. Gate `PASS` only where executed; source review of this L2 is neither P1/P2/P3 nor product software proof.

Use existing verifier/test families rather than adding a separate standalone v4.11 engine if they can be safely extended. Each Task/PR receives risk-derived Review Policy; architecture and authority-sensitive changes require Fresh independent review. A common self-review cannot satisfy that role. No universal high-cost CI/platform matrix.

## 11. Decision matrix / alternatives / rollback

| Candidate | Benefits | Material defects | L2 posture |
| --- | --- | --- | --- |
| **Owner-local semantics + subordinate schemas/conformance** | Matches v4.10, one pin, A0/A4, minimal migration, testable | Cross-owner wiring and equivalence proof need strict audit | **PREFERRED** |
| New central rules/policy engine + database | Convenient universal API in large deployments | Competing truth owner, mandatory runtime, breaks Minimum ADS | **REJECTED** |
| Install/compose OpenSpec, Spec Kit, BMAD as standards | Existing tooling and templates | Competing precedence/SDLC authorities, agent lock-in | **REJECTED** |
| Add entirely new multi-agent scheduler | Easier isolated queue implementation | Duplicates existing Dispatch/Claim/controller, unsafe authority drift | **REJECTED** |
| Evidence-only research report, no owner/test changes | Low implementation cost | Violates frozen §5 J05/J12, A+B+C executable release proof | **REJECTED** |

Rollback for additive schema/projection defects: keep previous compatible historical readers, revert one concerned extension before merge while preserving non-weakenable Frozen Product; repair with exact successor review. If U02 fails, select a stricter architecture (manual safe hold/reconcile at owning boundary) or bounded re-design; never silently loosen the release gate.

## 12. Lane/write-set hints (NOT Task DAG)

Proposed post-L2 lanes, conditional on L2 Freeze, each `one concern, one PR` and current v4.11 integration base:
1. **Contract/owner precedence (serial foundation):** Project Adoption/Workflow effective-rule owner and a reviewed minimal trace interface. This may be a convergence prerequisite for downstream tests.
2. **J05 current-spec/compatibility:** Interface owner and supported contract evidence tests; avoid writing Project Adoption or Dispatch.
3. **J12 reuse provenance:** Dependency/Architecture evidence + L1/L2/L3 prompt/contract tests; avoid compatibility/Dispatch writes.
4. **Agent interaction:** Interaction/Execution capability/claim/review/human control, with protocol writers/central adapters **serialized where write sets overlap**; no naive split of atomic claim or review arbitration into competing writers.
5. **External-effect/trust:** External/Migration/Secrets/Workspace bounded adapters/negative paths; U02 Demo must resolve architecture assumption first; real side-effect tests must use safe isolated environment.
6. **Machine conformance and adoption:** S/X fixture map, schema projection, A0↔A4 dogfood, central `standard-manifest.json`/verifier/wiring is **single convergence owner** after contract lanes; cannot edit simultaneously with conflicting owners.
7. **Integrated validation / closure:** dependency-complete candidate, risk-based Independent Reviews/real-host, visible full regression, Hidden, Fresh Closeout, RQ; not an implementation PR shortcut.

Do not materialize these as official Task DAG/Task Issues before L2 Freeze. Use JIT branches only after legal integration baseline; no protected version/main mutation now. Distinct research issues may be opened exclusively to resolve *architecture* UNKNOWNs without implying Stage 3 authority.

## 13. Fresh review/freeze admission checklist

An independent L2 Reviewer must inspect exact L2 candidate HEAD/tree/blob, Frozen Product #943, source predecessor tree, all material owner references, #945/#946 synthetic limitations, and live #932/#926/#785 feedback where relevant. Challenge:
- R01–R12 and all six ship concerns ownership completeness and actual v4.11 standard assimilation;
- unsupported material J intersection and risk facts under A0–A4; no N/A loopholes;
- U02 real boundary/test method adequacy and whether lack of demo blocks L2 Freeze;
- no second semantic owner, runtime or mutable store; no schema/Gate enum drift;
- safe human veto, Review arbitration, protected Claim and lost ACK across successors;
- Product authority vs execution/Hidden/RQ, predecessor integration currentness;
- compatibility/history/Minimum ADS impact and actionable non-overlapping Task lanes.

**Review is not Freeze.** Final L2 Freeze requires exact reviewed successor subject, durable disposition of every architecture UNKNOWN (especially U02), a genuine Fresh independent architecture review, controller/authority decision, and no dependency on unproven runtime facts. Only then may Frozen Task DAG/Task Packs be authored and committed. PRD contradictions must be escalated to Product authority; technical failures normally repair L2.

```ini
L2_ARCHITECTURE_EVIDENCE=PREPARED_SOURCE_BASED_CANDIDATE
L2_FRESH_REVIEW=NOT_RUN
L2_FREEZE=NO
U02_REAL_EXPERIMENT=NOT_RUN
TASK_DAG=NOT_AUTHORIZED
STAGE3_IMPLEMENTATION=NOT_AUTHORIZED
FULL_A_B_C_VALIDATION=NOT_RUN
PREDECESSOR_RELEASE_INTEGRATION_CURRENTNESS=UNVERIFIED
```
