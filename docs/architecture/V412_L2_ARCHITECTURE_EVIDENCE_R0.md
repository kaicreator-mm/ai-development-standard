# ADS v4.12.0 — L2 Architecture Evidence R1 (Source-First, Not Frozen)

> **L2-0 ADMITTED / SOURCE-BASED ARCHITECTURE CANDIDATE.** This is the first Stage-2 self-dogfood after the user-approved **Product Freeze** [`PRODUCT-FREEZE-v4.12.0-R3.md`](../product/PRODUCT-FREEZE-v4.12.0-R3.md) at checkpoint commit `5820542ad1c092e09fae268f7e77a6db3421297b`, tree `a4e5b372b9a970579240689437f385a0fcef7058`, for PRD R3 Git blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`. **Not an L2 Freeze, formal Task DAG, implementation Source Claim, executed Demo, release or v4.12 normative adoption.** Owner choices and scoped executable verification remain to be decided through the existing Stage-2 authority.

## 1. Source-first L2 evidence pins

| Authority / precedent | Exact Git blob or source | Use and limits |
|---|---|---|
| Frozen v4.12 PRD R3 | `0bfbf782c8859e79df52c9b57904ad80bcd718e9` / Product Freeze `5820542a` | Normative **Product scope for this version's planning**, not automatically implemented code |
| v4.11 Candidate Workflow | `standards/DEVELOPMENT_WORKFLOW.md@28c537e12c03f3f0cef501b8b5505e8ee28ca532` | Stage 2 UNKNOWN/Demo/freeze and Stage 2.6 Review Policy unchanged |
| Canonical Work Item | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md@196f7d9372bcffd6ff801a70e1c1fffb204f4336` | Existing `type:planning/type:task`, Issue Allowed/Forbidden changes, Claim CAS, native Issue identity |
| GitHub Agent Interaction | `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md@8c8fc74bd6deaf6987f6cf6d4e8e8e84c2692b75` | Actual source claim, Review, event admission and merge controller authority |
| Task DAG Governance | `standards/TASK_DAG_GOVERNANCE_STANDARD.md@e2ecfdbf0cd79f750aff40276e46a59159465f78` | `dag-mutation-record-v1`, SPLIT/SUPERSEDE and live Issue dependency governance |
| Validation and Release | `VALIDATION_STANDARD.md@1522b85f9e68cc4a1591ea5899b53c224998e5a8`; `RELEASE_STANDARD.md@c4d72506253ca7f3d95e305dbd84aae0e1fbe2cb` | Exact-SHA evidence/currentness and Release-by-subject; no second gate authority |
| Project Adoption | `standards/PROJECT_ADOPTION.md@a8c2d7a01a3610d9444d17df614ec6cacf58b67e` | A0/A1 manual evidence and A2+ machine modes with identical truth floor |
| L2 Research criteria | `prompts/L2_ARCHITECTURE_EVIDENCE.md@7bf41c3b125cfc2930296eb70faf8178761f4ee6` | Source-first, falsifiable high-impact UNKNOWN, max safe parallelism |
| Existing L1/architecture explorations | `references/v4.12/V412_CROSS_STAGE_CONTRACTS_CANDIDATE.md@f7b2622334b1f2c1f3fcf4de00151d0010f34662`; [#1111](https://github.com/kaicreator-mm/ai-development-standard/issues/1111); [multi-agent prior-art PR #1104](https://github.com/kaicreator-mm/ai-development-standard/pull/1104) @`6c571d2ee3b21feb3598fde6e075c1feaecc4773`, blob `3b4de3e63d7e32ac279f948ccd7f3d037b68f806` | Read-only/advisory prior research; **#1104 remains a Draft** and is not an adopted normative rule |

At the Product review the v4.11 candidate was `4924387815fa238382471e690fb169579767d9a1` vs historical PRD candidate `322e86845f78de8ea8cadb05ec624bfbb3a5de20` with owner norm blobs equivalent. **No v4.11 release assumed**. Recheck the actual predecessor version/tree JIT when eventually integrating v4.12.

## 2. Architecture drivers and immutable invariants

- **D1 Source and single owner:** GitHub native Issues/PRs/commits/Review/Claims remain execution and source authority. Phase-specific DAG-P/A are **advisory/document views**, never extra authoritative graph databases.
- **D2 Existing permission semantics:** A prospective `PLANNING_SCAFFOLD` Work Item (before formal full Implementation DAG Freeze) must first obtain a valid source-writing **accepted Claim**, own explicit new/write scope, resolve actual pre-dispatch Review Policy, satisfy merge-ready. Product Freeze alone never grants this implementation permission.
- **D3 Two independently current inputs:** accepted, actually merged Scaffold snapshot `SF` and full planning DAG checkpoint `DF` link through immutable material source-scope/tree + authoritative Product/L2/contract pins. A `DF` doc change is never exempt from **DF/map-semantic currentness**, even if exempt from Scaffold-tree rerun.
- **D4 One mapping fact / no double owners:** stable structural Anchor IDs (including Package/Capability IDs) + Task-side canonical typed bindings; all current effective ownership derived from actual Issue Allowed/Forbidden write scope + accepted Claim and effective Task/Issue current mapping; readonly forward/reverse indexes.
- **D5 Truth and min cost:** physical builder/runtime user journey ≠ structural Scaffold wiring; a single actual CI test execution may substantiate multiple release-owned assertions only if its **exact subject/exit/skip/environment** proves each one; no claims across changed source without owned impact.
- **D6 Adoption and version lineage:** A0/A1 may manually prove requisite predicates on exact Git objects; A2+ machine proof only when run. v4.11 owner standards remain pinned for existing projects until explicit legitimate adoption, Release/integration from actually qualified predecessor.
- **D7 Risk-bound execution:** No new compulsory daemon, graph backend, gate, fixed review rounds, 44 test commands for 44 evidence rows, blanket OS matrices or forced enterprise human Gold campaign.

## 3. Minimal architecture alternatives and tentative choices

| Concern | Option A | Option B | Tentative L2 selection & reason | Failure/escape |
|---|---|---|---|---|
| DAG-P/A/Execution | One always-on graph service | Phase-scoped conditional **views** + canonical native GitHub live Issues | **B**: source-first, A0-safe, no second mutable state | When dependent phase work needs ownable Work Items, project can materialize subset using existing issues; no synthetic `blocked_by` |
| Planning Scaffold authority | New Bootstrap Controller/human Gate | Existing `type:planning` or `type:task` scoped Work Item + accepted Claim + Review/merge | **B**: reuse canonical Issue/Claim/Review owners; label/profile is not a new `type:planning-scaffold` | Unknown legal Claim CAS before any source → HOLD; never auto-authorize through document |
| Bidirectional Scaffold↔Task | Writable Anchor owner/lifecycle + Task copy | Structural anchors + **one** effective Task binding facts and derived indexes | **B**: no drift-prone duplicate owner; current Task/Claim truth separate | Invalid/unknown Task↔Issue refs or split: fail closed & lawful `dag-mutation-record-v1` |
| Pair Freeze | Commit SHA equality or index self-hash | Cycle-free `(accepted SF commit, immutable scope/allowlist + tree, DF checkpoint, map input digest, frozen Product/L2)` | **B**: stable proof across docs-only successor, fail-closed material change | Drift → explicit source-owner repair/rebaseline; do not auto-move frozen tuple |
| Validation reuse | Per-Gate re-run full test suite | Existing Validation §6 + Release §11; optional derived assertion→obligation coverage | **B**, source-first `ALREADY_SATISFIED` for authority; evaluate only truly missing projection | Unknown/skip/currentness cannot be promoted; execute real affected tests |
| Orchestration/observability/learning | New Steward service + new Task state DB | Existing Controller/Issue/Task Learning records + read-only observations | **B** until source-backed material gap shown; no guaranteed separate P1 subsystem | Report stalls, never mutate protected Claim outside existing delegated authority |

**Note:** These are **recommended L2 alternatives**, not Product edits, executable/proven implementation, L2 authority acceptance, or frozen ADRs. Selected code location/format should be decided only after exact file-level reuse inspection.

## 4. Five independent reviewer P2 notes — L2 required disposition

| ID | Tentative architecture projection | Negative test/oracle | Disposition |
|---|---|---|---|
| **N1** Canonical Work Item | `PLANNING_SCAFFOLD` is a role/scope on canonical `type:planning` (or `type:task` if actual execution contract requires); no alias. Link Issue readiness/Claim §12.1 and Stage2.6 Review Policy | `type:planning-scaffold` or zero accepted Claim before public contract write → DENY | `STATIC_EVIDENCE_SUFFICIENT` for owner/type vocabulary; implementation admission checker later |
| **N2** predecessor pin | Historical `322e` and later `492438` are separate candidates; no assumed Release. Freeze version integration input only after predecessor RQ | Claim v4.11 Released solely from candidate ref → DENY | `STATIC_EVIDENCE_SUFFICIENT` for current Product; **Release predecessor remains runtime/external BLOCKED** |
| **N3** DAG-doc exemption | Explicit docs allowlist excludes only **Scaffold source-tree** recheck, not updated `DF/map digest`; `DF` semantic changes always tracked | Change only DAG bindings: unchanged `SF` tree reusable but new DF/map mandatory; an unknown CI file invalidates SF tuple | `STATIC_EVIDENCE_SUFFICIENT` for contract, checker proof later |
| **N4** A0 manual V01–V12 | Manual substantive source evidence may satisfy per-predicate existing owner evidence; evidence method is not Gate result; machine-only V10 N/A only if no generator claim | V01 manual exact Git anchors accepted under lawful owner, V10 fake generated PASS rejected | `STATIC_EVIDENCE_SUFFICIENT` for owner floor, manual vs machine fixture later |
| **N5** Writer bounds | Effective mapping binding's write path **subset** of canonical Task Issue Allowed paths, disjoint from Forbidden, consistent Claim/Review/merger; Task SPLIT triggers current binding refresh | Binding `T05 MODIFIES anchor:X` outside T05 Issue Allowed → HOLD | `STATIC_EVIDENCE_SUFFICIENT` for source ownership, implementation checker negative later |

**No need for five extra Product Issues, new Review round, 5 Demo branches, or a new authority.** Treat their acceptance negatives as one bounded contract/validation workstream later.

## 5. Material Architecture UNKNOWNs — evidence-first stop/defer

| UNKNOWN | What can change | Evidence at R0 | Provisional route / next owner |
|---|---|---|---|
| **U01** Is legal `PLANNING_SCAFFOLD` accepted Claim compatible with existing canonical Issue types/ready state without extra dispatch authority? | Protected source permission and write admission | Existing Work Item §4/§10/§12.1, protocol §8.5, Stage2.6 known; prospective stage ordering changed by Frozen Product | `STATIC_EVIDENCE_SUFFICIENT` for authoritative contract placement; **L2 owner must specify admission sequencing and a negative race/CAS fixture**, not assume already implemented |
| **U02** Can immutable scoped source tree + DAG/map digest support a docs-only DF update without accidental drift exemption or self-cycle? | Pair Freeze currentness correctness | Git object identities, Validation §6 and Product acceptance are known; not yet executed checker | **L2 detailed contract required**; if static derivation cannot settle material path comparison or self-reference, `EXECUTABLE_DEMO_REQUIRED` on a *minimal synthetic git fixture*, not a new service |
| **U03** Do effective Task binding projections survive SPLIT/SUPERSEDE and Issue write-scope authority? | Live write ownership and safety | TASK_DAG_GOVERNANCE `dag-mutation-record-v1` and Work Item Allowed changes exist | `STATIC_EVIDENCE_SUFFICIENT` for authority; checker/fixture during implementation. Conflicts HOLD |
| **U04** Can existing Validation/Release records express one executed log→multiple required predicates without double-counting? | Actual test cost and false PASS risk | #1111 confirmed owner coverage, source §6/§11 | `ALREADY_SATISFIED` for core currentness; **BOUNDED_DELTA only if missing assertion-to-obligation index proven**; do not automatically implement |
| **U05** Is final version branch allowed to start/merge against current `main` while v4.11 candidate Release unresolved? | Actual integration and authorized version lineage | v4.11 unreleased candidate and prior `main@b9461d...` | `BLOCKED_FOR_VERSION_INTEGRATION`, **not blocking source-only L2**; actual owner must rebind to qualified predecessor before implementation version merge |

**Architecture Contradiction:** none proven by R0 static inspection. `L2_FREEZE` **not claimed**. Owners must resolve any material unknown that still affects public ABI/security/multi-writer recovery before future Freeze; a minimal Research Demo is lawful **only** where static/existing evidence truly insufficient. An uncertain implementation detail is not by itself a reason to repeatedly reopen Frozen Product.

## 6. Lane-oriented draft DAG-A (only genuine independent planning work)

**Selected depth:** `BOUNDED_WORKLIST`, not universal EXPLICIT_DAG. Candidates can proceed in bounded parallel source-read lanes:

- **A1 — Control/authority:** Work Item / Claim / Review and Scoped Planning Scaffold. **Contract owner:** existing GitHub Work Item + Protocol, no new controller.
- **A2 — Source/mapping:** Anchor schema/bindings, material-scope tuple, DAG map checker, migration/SPLIT. **Contract owner:** Task DAG Governance + Validation currentness.
- **A3 — Evidence and self-dogfood:** actual one-new/one-mature source-pinned fixtures, proof equivalence/skip handling, release evidence reuse, research stop-loss. **Owner:** Validation/Release current standards.

**Safe interaction:** A1/A2/A3 can perform read-only owner gap analysis in parallel. **Serialize**: A1 freezes legal source-writing contract **before** Scaffold production authoring; A2 public schema/source write and A1 contracts require a single agreed interface owner; A2+Task DAG paired Freeze follows real accepted SF and L2 Freeze; final actual integration and Release require version predecessor qualification. Do not create duplicate mutable Issue/Task owners or Github-native dependency edges for these advisory L2 lanes.

## 7. Minimal next actions and adoption boundary

1. L2 owner first accepts/edits the **seven Architecture Drivers** and five reviewer P2 dispositions by comparing against exact current owner references above. Do not replay complete L1/PRD reviews.
2. Choose a minimal single-source mapping/evidence schema and material-source scope semantics; record a **small ADR/source write-set map** with 2 positive and 3 negative conceptual fixtures, no unbounded new test matrix.
3. Resolve U02 via static git-object sketch; if a high-impact assumption remains unresolved *and executable evidence is necessary*, issue one genuinely scoped Research Demo with E1 and positive/negative tests. No fake demo PASS in this R0.
4. When all material U01–U05 are lawfully classified, create a distinct exact-source **L2 Freeze** under existing Architecture Owner. **Only then** authorize scoped `PLANNING_SCAFFOLD` Work Item/Claim, DAG draft co-evolution, paired Freeze and actual implementation. Do not prematurely materialize the implementation Task DAG.

```ini
PRODUCT_FREEZE=PASS_R3_EXACT_BLOB
L2_ARCHITECTURE_R0=SOURCE_EVIDENCE_STARTED
L2_DEPTH=BOUNDED_WORKLIST
L2_FROZEN=NO
DEMO_RUN=NO
SCAFFOLD_CLAIM=NONE
IMPLEMENTATION_DAG=NOT_STARTED
RELEASE=NOT_QUALIFIED
SELF_DOGFOOD=REAL_L2_SOURCE_FIRST_PROCESS_USED;NO_IMPLEMENTATION_PASS_CLAIMED
```


## 8. L2 R1 — source authority, mapping and paired-freeze design

> **2026-10-15 Stage-2 source-first refinement.** This section is a prospective **L2 design candidate**, not a released normative ADS contract, not an L2 Freeze, and not implementation authority. It uses the current v4.11 canonical Work Item/Claim/Review/DAG/Validation owners exactly as already pinned in §1. The research fixture committed at `references/v4.12/fixtures/v412_l2_git_pair_probe.py` is a **self-contained isolated synthetic Git research artifact**, not a shipped library or required CI/Host suite.

### ADR-01 — Scoped Planning Scaffold authority (no new Issue type)

**Proposed decision:** `PLANNING_SCAFFOLD` is a *phase/concern scope* on a canonical GitHub Work Item. Select `type:planning` when its current owner permits the planned source-write role, or `type:task` when the actual adopted Issue Contract requires it. Never invent `type:planning-scaffold`; never infer current implementation rights from document text or a `type:planning` label. The normal `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §9/§10/§12.1 and `GITHUB_AGENT_INTERACTION_PROTOCOL.md` §8.5 are the execution admission owners.

**Proposed ordered source-write trace:**

```text
Frozen Product @0bfbf782... + future Frozen L2 exact authority
→ Canonical planning/Task Issue contract (identity, allowed/forbidden paths,
   source/L2 pins, true deps, scope, required tests, assigned role, risk)
→ Stage 2.6 Review Policy RESOLVED BEFORE dispatch
→ Canonical Work Item COMPLETE + dependencies/evidence CURRENT → READY
→ atomic/CAS accepted Claim + durable DISPATCH_CLAIMED (Start Record)
   ↳ rejected/raced/unknown Claim → STOP, zero source write
→ generate a RIGHT-SIZED scaffold on isolated bounded concern branch
   ↳ source file creation permission != execute install/postinstall/network
→ focus structural + contract + negative tests on claimed exact source
→ appropriate independent Review (required for public API/schema/trust when selected)
→ Validation + branch/target/head currentness + original merge-ready guards
→ authorized merge + exact integration SHA/tree readback → accepted Scaffold SF
→ DAG draft co-evolves and uniquely binds effective write owners
→ three-way Product/L2↔Scaffold↔DAG negative acceptance
→ paired planning Freeze and immutable DF (separate existing phase authority)
```

**Claim consistency:** Do not mint a second `ScaffoldClaim`/Bootstrap lock. Before DF materialization the existing Scaffold Work Item is the sole authorized mutable source writer. After materialization, a Task Issue's *current* Allowed/Forbidden scope and accepted Claim own actual execution. Source anchor relations cannot override Issue Contract or live Claim. Work Item Claim is a durable Start Record, not a Markdown issue status or API 200 response. Existing transient provider failure remains UNKNOWN until canonical readback.

**Fail-closed anti-examples:** two workers see READY, second loses CAS → second writes zero bytes; default permissive postinstall attempts network despite lawful `package.json` file creation → no execution without existing environment/effect authorization; public ABI claims `Review Policy=required` but PR has no independent Review → SF not accepted even with GREEN local compile; shared composition root with two effective writer Tasks → source conflict and HOLD, not arbitrary winner.

**Stage note:** This is a **prospective v4.12 change** to Stage-2/3 sequencing. Product Freeze alone did not update v4.11 operational source-write policy or dispatch an accepted Claim. The Architecture owner must pick the exact effective owner/protocol projection *before* any real production Scaffold authoring; a synthetic prototype is not that permission.

### ADR-02 — Structural anchors + single Task binding source of truth

Use only current Git objects/Task Issue contracts, without second writable graph. Suggested **semantic projection**, not a mandated separate JSON database:

```json
{
  "anchor": {
    "anchor_id": "contract.runtime.v1",
    "kind": "CONTRACT",
    "location": "packages/contracts/src/runtime.ts",
    "contract_ref": "Frozen-L2:runtime-abi",
    "presence": "PRESENT"
  },
  "task_binding": {
    "planned_task_id": "T-C01",
    "anchor_id": "contract.runtime.v1",
    "relation": "IMPLEMENTS",
    "scope": ["packages/contracts/src/runtime.ts"]
  }
}
```

Anchor never stores independently editable `owner`, implementation `PASS`, `lifecycle:IMPLEMENTED` or a live Claim. `PRESENT|PLANNED_FUTURE` is structural presence only; a present stub remains `NOT_IMPLEMENTED` as a product capability. The binding is the sole planning relation **fact**, not a second authorization: before source writing/after materialization respectively check accepted planning Work Item or bound canonical Task Issue+Claim. Every material mutable anchor has exactly one **effective writer at a time**, with any number of `CONSUMES`/`TESTS` readers. `INTEGRATES` involving composition-root writes requires an actual single integration owner. Import relationships do not create GitHub native `blocked_by` unless actual Task dependency exists.

**Post-materialization:** a single durable materialization record maps `planned_task_id → canonical GitHub Issue #`. For SPLIT/SUPERSEDE, the existing authorized `dag-mutation-record-v1` must capture the **effective binding projection delta** and affected Task/Issue/Review/Validation scope; after actual canonical live DAG mutation, derive new read-only forward/reverse mapping. Frozen DF remains history. A stale binding to superseded T02 is not a current writing license.

**Crucial reviewer P2 N5:** Require `binding_writer_path_set ⊆ canonical Issue Allowed changes` and `binding_writer_path_set ∩ Issue Forbidden changes = ∅`, plus current accepted Claim. If any dimension conflicts/UNKNOWN, deny writer admission; no mapping file may repair or broaden the Issue's approved scope.

### ADR-03 — Cycle-free paired identity and fail-closed drift algorithm

**Distinct identities rather than one overloaded SHA:**

```text
SF = accepted merged source commit + Git root tree id
SC = immutable material-scope manifest Git blob id + version
ALLOWLIST = exact file paths within SC, only exempt from SF *source-tree* recheck
MV = sha256(canonical sorted (path, filemode, git_kind, git_blob_or_tree_oid)
     for ALL tracked Git paths in accepted SF EXCEPT exact ALLOWLIST paths)
DF = final planned DAG exact checkpoint document blob / commit
MI = sha256(canonical committed semantic anchors + active planned bindings
     + mapping schema_version + pinned Product/L2 contract refs)
PAIR_INPUT = {ProductFreeze, L2Freeze, SF, SC, MV, DF, MI}
DERIVED = deterministic forward/reverse index(PAIR_INPUT) [output, NOT input]
RECORD = signed/authorized paired-checkpoint reference [output, NOT input]
```

`MV` is a **synthetic canonical material-view digest** and MUST NOT be falsely called a native Git subtree SHA. A0/A1 can independently inspect Git commit/root-tree + each relevant `path→Git object ID` using GitHub WEB/API for manual material proof, while a future ADS reference checker computes canonical MV. A semantic DAG checkpoint may be exempt from recomputing `MV` **only**; its `DF` blob and `MI` digest still require exact revalidation. A generated index may be excluded from `MV` but MUST be independently **recomputed and compared with checked-in output**. An untrusted Freeze record is not authoritative merely because its path is exempt from `MV`: it must be tied to accepted owner authority/source checkpoint.

**Change impact before initial paired Freeze:** obtain full **union of changed paths** between accepted SF and proposed pair candidate, including **adds, deletes, renames, CI/config, lockfiles, anchors and the manifest itself**; if any changed path is not an exact ALLOWLIST member of the **accepted source snapshot**, mark `MATERIAL` (not necessarily version defect; require lawful revalidation/repair/rebaseline). Unknown path diff, unknown scope/currentness, synthetic index mismatch or an unapproved new source owner → `HOLD`. Never use `docs/**` wildcard; no writer may silently amend the frozen ALLOWLIST. During **later lawful post-DF Implementation Tasks**, use existing Validation §6 scoped Task change-impact rules instead of recursively invalidating the *historical* accepted SF checkpoint for every feature commit.

**Recompute algorithm (candidate for L2 checker, no new Gate):**

```text
read frozen Product/L2 refs + accepted merged SF commit/tree
read immutable SC at accepted SF (not proposed writer's substitute)
collect current candidate Git tracked paths and object identities
for path in union(old_paths,new_paths):
    if old_object != new_object and path NOT IN SC.exact_sf_tree_exempt:
        mark MATERIAL, route revalidation/explicit authorized rebaseline
derive MV using sorted non-exempt committed Git entries; compare expected MV
recompute DF checkpoint and MI semantic digest even for an exempt DAG path
recompute derived map from committed canonical anchor+binding facts
compare generated bytes/semantics; forged/outdated output => HOLD
resolve one current effective writer from actual Issue Allowed/Forbidden + Claim
validate Product/L2 public ABI, trust/error/negative invariants with owner proofs
only after authorized PR merge/currentness + all required evidence:
    allow paired planning Freeze record with cycle-free input tuple
```

### Prototype negative evidence — Git-backed executable logic, NOT formal runtime Validation

**Research artifact:** [`references/v4.12/fixtures/v412_l2_git_pair_probe.py`](../../references/v4.12/fixtures/v412_l2_git_pair_probe.py). In this ChatGPT session's isolated disposable environment, a matching Python/std-lib/Git implementation of `material_view_digest`, distinct DF/MI checks, and **separate generated-output recomputation** was exercised in **11 scenarios; 11/11 matched expected assertions**. It creates and destroys only a scratch `git init` repository, makes no network requests, and does not write the real project source. The GitHub-committed file is a **reproducible source artifact**; its exact committed bytes have **not** been re-executed after GitHub upload because the container cannot access GitHub externally. Do not call that unperformed step PASS.

| Fixture | Expected oracle | Result in isolated local prototype |
|---|---|---|
| P01 accepted SF snapshot | Same input ⇒ same source/material/map digest, generated output compares current | EXPECTED |
| P02 DAG-only bindings changed | SF material view unchanged; DF/MI changed and generated index becomes stale | EXPECTED |
| N01 unknown added package | MATERIAL even outside old declared project module list | EXPECTED |
| N02 lockfile change | MATERIAL | EXPECTED |
| N03 `docs/planning/scaffold-anchors.json` change | MATERIAL; semantic map changes | EXPECTED |
| N04 accepted scope manifest change | MATERIAL and scope drift; cannot expand exemptions unilaterally | EXPECTED |
| N05 `.github/workflows/ci.yml` change | MATERIAL | EXPECTED |
| N06 contract file deletion | MATERIAL | EXPECTED |
| N07 nonallowlisted `docs/notes.md` | MATERIAL (no wildcard) | EXPECTED |
| N08 forged generated index | `MV` unchanged **but derived-output comparison rejects forgery** | EXPECTED |
| N09 derived Freeze output changed | `MV` unchanged, record **not self input**; real authority separately needed | EXPECTED |

**Evidence strength:** isolated **E1 synthetic algorithm-prototype** only. Does NOT exercise public API semantics, actual GitHub Issue CAS, concurrent real writers, accepted external Review, native Task SPLIT mutation, version Release, or production Build Host; all remain `NOT_RUN`. Positive conceptual invariant demonstrated: excluded derived outputs avoid self-hash cycles **without** turning forged derived output into an accepted view. Prototype `git ls-tree` parser assumes fixture-safe paths; eventual implementation MUST process NUL-separated names/rename cases and protect ambiguous byte/path ordering.

### L2 R1 Architecture-UNKNOWN disposition

| U | Disposition after bounded real work | Required before future L2 Freeze? |
|---|---|---|
| U01 canonical Work Item Claim ordering | **STATIC_EVIDENCE_SUFFICIENT** for contract/policy *design* via existing §4/§10/§12.1/§8.5; genuine Claim race and safe source admission tests are future implementation conformance | Need Architecture owner confirm precise phase-source permission and single canonical type; do **not** require new Claim service/Demo for proven existing CAS semantics |
| U02 SF↔DF↔MI pair currentness | **BOUNDED_E1_SYNTHETIC_PROBE_PERFORMED; DESIGN_SUPPORTED** by 11/11 prototype cases, not formal checker or integration; exact distinction of allowlist and mapping currentness resolved at algorithm level | Owner approve MV canonical byte/path/manifest schema and latest exact result; no expensive real Build Host research required for pure Git content |
| U03 SPLIT and writer scope | **STATIC_EVIDENCE_SUFFICIENT** for owner split governance; actual Issue Allowed/Forbidden projection/currentness must be covered by future checker negatives | Must record merge-safe Task-binding projection and stale-split rejection design; no premature live native Issue mutation |
| U04 evidence de-dup | **ALREADY_SATISFIED** for Validation/Release authority, `BOUNDED_DELTA_IF_PROVEN` for assertion→obligation index | No second test service or mandatory duplicate CI |
| U05 version predecessor | **BLOCKED_FOR_FUTURE_IMPLEMENTATION/RELEASE_INTEGRATION**, not an L2-source study blocker | Keep exact candidate vs released predecessor separate; no v4.11 release invented |

**Explicit L2 stopping rule:** if the source/owner checklist above resolves U01–U04 on the same current Product/owner pins and no genuinely new high-impact UNKNOWN appears, stop L2 exploration. One affected-scope architecture owner review/Freeze may occur; do not spin new Research Demo/independent Reviewer loops or create one Issue per fixture. The legitimate version-base blocker U05 is delegated to later actual version integration, not hidden by this research.

```ini
L2_R1=SOURCE_DESIGN_REFINED
L2_ADR_DRAFT=ADR01_CLAIM_AUTHORITY;ADR02_SINGLE_BINDING;ADR03_PAIR_HASH
SYNTHETIC_GIT_PROTOTYPE=11_OF_11_EXPECTED_IN_ISOLATED_CONTAINER
GITHUB_COMMITTED_FIXTURE_EXACT_EXECUTION=NOT_RUN
REAL_GITHUB_CLAIM_CAS_TEST=NOT_RUN
REAL_GITHUB_NATIVE_DAG_SPLIT=NOT_RUN
REAL_CANDIDATE_BUILD_HOST=NOT_RUN
PREDECESSOR_RELEASE=NOT_QUALIFIED
L2_ARCHITECTURE_OWNER_FREEZE=NOT_RECORDED
PRODUCT_FREEZE=UNCHANGED_EXACT_R3
```
