# ADS v4.13 — Minimal Implementation Task DAG R0 (source-only candidate)

> **STATUS: PLANNING_DAG_CANDIDATE / NOT YET FROZEN / NOT MATERIALIZED.** GitHub Task Issues and actual native Issue Dependencies become the live execution DAG only after lawful materialization. This file is not a live state card or a Task Claim.  
> **Frozen Product:** `docs/product/v4.13.0/ADS_V413_PRD_R0_TALLY_FOUNDATION.md` blob `702bcf562b4292487fa8409cd17dee2d42aae9b3`, Product Freeze checkpoint `3123d7d4bd5ef7b8f9236119537ff9226d6bd3a9`.  
> **Frozen L2:** `docs/architecture/V413_L2_ARCHITECTURE_EVIDENCE_R0.md` blob `86b9243c065ab909f82d52d1d7b7f945791d3696`, L2 Freeze checkpoint `91bb0378b0516367177c1570bd8f09cf1878ec4b`.  
> **Version base safety (updated exact evidence):** latest confirmed qualified **public stable** predecessor is **v4.12.0 Tag/Release** at commit `ee8258106547abd2c2d7b9f5e87af9965e430bd2` (Release RQ #1143@6210278828, publication readback #1143@6210620486). Current `main@4465e291df4e60e09af634a25ab7eed546b2915b` has `VERSION=4.12.1` source hotfix PR #1146 merged, but **tag `v4.12.1` absent**; it is not asserted as an independently published qualified predecessor. A v4.13 integration branch may carry these current-main hotfix changes only with explicit source/change-impact account and affected candidate validation; exact source-currentness and version-lineage admission remain required before normative source writing.

## 1. Scope and minimal topology

```text
Product R0 FROZEN + L2 R0 FROZEN
             |
   v4.12.0 qualified tag + explicit main hotfix-lineage admission
             |
             +------------------+------------------+
             |                  |                  |
        V413-S02             V413-S03           V413-S04
       Org Profile       Tally interop        #1119 adoption
      schema/standard    source mapping        policy delta
             |                  |                  |
             +------------------+------------------+
                                |
                         V413-CLOSURE
               one standards-source candidate
               validated + review + RQ + Release
```

**S02, S03 and S04 have no inherent unmerged-code or execution dependencies on each other** and SHOULD be independently mergeable after each legitimate task PR completes. The final Closure's wait for all three is the version Release dependency-completeness requirement and does not create a fourth hidden implementation concern or fabricated native `blocked_by`. Source owner S04 may refer to S03's stable contract without modifying S03's file. S01 L1/L2 source gap mapping already exists and is **not** a separate executable Task.

## 2. Concern / ownership / readiness table

| Task | Scope and exact write-set target | Frozen inputs | Dependencies | Review | Parallelism |
|---|---|---|---|---|---|
| **V413-S02** | `standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md` **only additive org defaults section**; new `schemas/organization-development-environment-profile-v1.schema.json`; one `examples/organization-development-environment-profile.json`; focused deterministic positive/negative fixture if needed | FR01, L2 A1; existing `schemas/dependency-toolchain-profile-v1.schema.json` | v4.12.0 published predecessor + current-main hotfix-impact disposition/accepted Claim; **none on S03/S04** | **required** if new normative schema/compat contract is material, otherwise actual policy | Can parallel S03/S04 |
| **V413-S03** | New `references/v4.13/ADS_EXECUTION_INTEROP_CONTRACT.md`; at most one targeted existing owner-reference update if necessary **after checking current source**, no new workflow state/schema | FR02/FR05, L2 A2; `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `TASK_DAG_GOVERNANCE_STANDARD.md` | Predecessor qualification/accepted Claim; **none on S02/S04** | **required** for changed Task/Claim/actor/GitHub authority semantics, source review focused on delta | Can parallel S02/S04 |
| **V413-S04** | `standards/PROJECT_ADOPTION.md` additive #1119 FR03 three-checkpoint contract; selected `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` cross-ref **only if true owner gap**. #1116 capability table only after proving missing material case, do not automatically edit VALIDATION/RELEASE | FR03/FR04, L2 A3/A4, #1119/#1116; existing `scripts/v412_ads_compatible_select.py` read-only | Predecessor qualification/accepted Claim; **none on S02/S03** | **required** for update/Claim/merge/authority-semantic delta, independent exact-head review | Can parallel S02/S03 |
| **V413-CLOSURE** | Existing version candidate evidence source, `VERSION`/README/CHANGELOG minimal actual release metadata only when qualified, actual Release qualification/handoff records | S02/S03/S04 accepted merged source; Product/L2 freezes; exact current candidate SHA/tree | All material concerns closed and no materially required proof unknown | Existing Release/Reviewer/Controller applicable policy | After S02–S04, no premature Release PASS |

**Write-set guard:** no S02/S03/S04 may edit old v4.12 selector, historical Tally sources, Tally runtime/CLI, unrelated W1–W5 standards, frozen Product or L2. Source owner conflict discovered later ⇒ local Scope Amendment before actual write, not silent Task expansion.

## 3. Per-concern Task Pack essentials

### S02 — Organization Profile (risk: MEDIUM/HIGH, model: medium/high Web)

**Tests first**
- schema structural validation via repo's existing JSON-schema checks and source-specific explicit positive/negative fixtures; organization default does not carry project manifest/certification.
- two deterministic example project compatibility/override cases; conflicting constraints and host-installed version never override Frozen project requirement.
- reject credentials/secrets and unsupported/mutable external version fields; actual tool installation checks **N/A for ADS standard**, not fabricated runtime PASS.

**Contract** — one separately versioned organization **defaults** schema, applied under existing toolchain canonical owner and subordinate to immutable project contract. Exact source provenance/precedence.

**Implementation** — additive standard text, JSON schema, one example and smallest actually needed targeted test. Use existing `dependency-toolchain-profile`, avoid duplicate requirement model.

**Failure handling** — incompatible/UNKNOWN => source-attributed conflict; no project lock rewrite, no install side effect.

**References** — Frozen FR01/AC01, L2 A1, `DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md`.

### S03 — Tally/other consumer execution interop (risk: HIGH semantics, model: high Web)

**Tests first**
- one frozen GitHub-native Issue dependency vs Tally stale ready-state negative;
- running accepted Task retains source ADS SHA and verified Claim after a newer qualified version is proposed;
- same GitHub login but two distinct **self-declared logical actors**, without fabricated independent execution proof;
- PASS depends on actual test/Review evidence; offline/unknown GitHub facts never promoted to Task DONE.

**Contract** — **read-only semantic mapping**, not a new Task state schema, between existing ADS pin/Task/Claim/PR/Review/Validation/Release facts and Tally's Agent/Host/Attempt projection. Applicable to independent adopters; no forced Tally dependency.

**Implementation** — new `references/v4.13/ADS_EXECUTION_INTEROP_CONTRACT.md` and only narrowly necessary canonical cross-ref; no Go or local SQLite code.

**Failure handling** — GitHub fact source mismatch ⇒ STALE/HOLD for consequential action, source provenance included. Unexecuted Host validation remains NOT_RUN/BLOCKED.

**References** — Frozen FR02/AC02/AC03/FR05, L2 A2, GitHub Work Item/Agent Interaction and Validation Standards.

### S04 — qualified adoption rules (risk: HIGH authority, model: high Web)

**Tests first**
- v4.12 read-only selector given unrelated open Issues still returns `NO_SAFE_RECOMMENDATION` (historical behavior retained);
- separate source-qualified non-SAFE prospective positive only when verified released candidate and consumer behavioral/authority compatibility evidence actually present;
- unknown evidence cannot produce `EVIDENCE_BACKED_COMPATIBLE_PROPOSAL` or update PR; stale GitHub head/failed permission/no opt-in reject PR plan;
- if effective `.dev-standard/VERSION` changes on PR merge, activation prerequisites must have been satisfied before merge; accepted prior Task retains old pin.
- FR04: inspect mixed standards+CLI gate policy and record `ALREADY_SATISFIED` or exact absent case; if absent add minimal capability table with negative.

**Contract** — `READ_ONLY_PROSPECTIVE_PLAN ≠ SAFE_RECOMMENDATION ≠ OPTED_IN_PR ≠ AUTHORIZED_ACTIVATION`; no new Gate state, no actual writer. Released v4.12 selector remains unmodified.

**Implementation** — additive `PROJECT_ADOPTION.md` section + bounded fixture/document examples; only touch additional owner standard after a proven hole.

**Failure handling** — fail closed on qualification/compatibility/Task isolation/Claim/Review/permission UNKNOWN; no autonomous merge, no historical evidence rewrite.

**References** — Frozen FR03/AC04/AC05, L2 A3/A4, `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md`.

## 4. Admission, claims and issue materialization

1. **Before source writing:** qualified predecessor is positively established as **v4.12.0**: published tag `v4.12.0` resolves to version 4.12.0, RQ #1143@6210278828 and publication #1143@6210620486 bind published commit `ee8258106547abd2c2d7b9f5e87af9965e430bd2`. The current main SHA `4465e291df4e60e09af634a25ab7eed546b2915b` contains *unreleased/unqualified as a separate version* v4.12.1 source delta via merged PR #1146. Before constructing v4.13 version integration branch, explicitly verify ancestry/current Git objects plus the exact patch write set and required affected-source checks; carry-forward is subject to v4.13 candidate validation and cannot inherit a fictional v4.12.1 Release PASS. If that evidence is missing, keep source-writing Tasks PLANNED/BLOCKED; never build on guessed branch/tag.
2. Freeze this **exact DAG blob** under own Task DAG authority only after source-owner/write-set and predecessor admission disposition, then materialize Task Issues via canonical `type:task`, `state:planned`, scope and exact current Task Pack, selected review policy, acceptance, validation and executor identity.
3. No implementation dependencies among S02/S03/S04: do **not invent** native `blocked_by` edges just for serial process staging. Version Closure is a separate release prerequisite, recorded in Version/Release authority; it may use GitHub Issue dependencies if actually materialized and supported by connector, but text alone never claims native edges.
4. Actual source modification needs own valid `state:ready` dispatch and accepted CAS Builder Claim on qualified version baseline. `PRD_FREEZE/L2_FREEZE/DAG_FREEZE` alone never permits source byte.
5. One concern one PR; disjoint owners can merge main after true local Review/Validation and accepted GitHub facts. Expensive whole suite only at final candidate when required; affected-diff test on small changes; CI/Review source currentness preserved.
6. New Tally v2 runtime tasks only in [Tally #55](https://github.com/kaicreator-mm/tally/issues/55) / Draft PR #56. ADS version qualified Release **does not depend on Tally code/E2E**.

## 5. Release closure (one version candidate, not every Task)

```text
source owner mapping / current Task issues
→ actual merged source S02/S03/S04
→ canonical schemas & source examples and bounded negative fixtures
→ source cross-ref / self-coherence and qualified version identity
→ selected independent exact-source review where policy demands
→ existing applicable candidate / CI / Release Qualification
→ Tag + published Release + immutable version base
```

Real Tally host/Agent/Portfolio tests occur only under Tally v2. No extra spec-only Owner verification/denial E2E, no fake runtime proof, no duplicate general QA campaigns.

## 6. Task DAG status truth

```ini
PRODUCT_FREEZE=R0_BLOB_702bcf562b4292487fa8409cd17dee2d42aae9b3
L2_FREEZE=R0_BLOB_86b9243c065ab909f82d52d1d7b7f945791d3696
TASK_DAG_SOURCE_STATE=CANDIDATE_NOT_FROZEN
NATIVE_IMPLEMENTATION_ISSUES=NOT_MATERIALIZED
IMPLEMENTATION_DEPENDENCY_EDGES=ZERO_PROPOSED
VERSION_CLOSURE=NOT_RUN
QUALIFIED_RELEASED_PREDECESSOR=v4.12.0@ee8258106547abd2c2d7b9f5e87af9965e430bd2
CURRENT_MAIN_SOURCE_DELTA=v4.12.1_UNPUBLISHED_HOTFIX_PR1146
SOURCE_INTEGRATION_HOTFIX_CURRENTNESS=REQUIRES_ADMISSION_AND_AFFECTED_CHECK
CLAIM_STATUS=NONE
IMPLEMENTATION=NOT_STARTED
TALLY_V2_IMPL=OWNED_BY_TALLY_ONLY
```

Do not update this frozen/planning document later as a mutable status board; route future progress to native Issues/PRs.
