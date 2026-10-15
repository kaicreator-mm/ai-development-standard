# ADS v4.12.0 — L2 Architecture Evidence R2 (Source-First, Not Frozen)

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

## 9. L2 R2 — N10 adversarial scope-exemption eligibility correction

**New material design falsifier found by self-dogfood adversarial readback:** R1's full Git path diff + frozen allowlist prevents **post-SF** writers from silently enlarging exemptions. But this alone cannot prove the *original accepted* scope was lawful: a planning author might pre-list an actual code path (e.g. `packages/new-adapter/index.ts`) as exempt and then modify it; an immutable-but-misclassified manifest would suppress the necessary material response. This is a **high-impact L2 checker admission gap**, not a new Product requirement or reason to reopen frozen PRD R3.

**Bounded repair to ADR-03:** Before *accepting* SF / its material-scope manifest, enforce **explicit exact-path semantic exemption eligibility under the Frozen L2/source owner**; proof must distinguish `DAG_ONLY_INPUT` (always still covered by DF/MI), `DERIVED_NONAUTHORITATIVE_OUTPUT` (always byte/recompute checked if claimed), `FREEZE_RECORD_OUTPUT` (must carry independent Owner act), and ordinary source/build/manifest/contract paths (ineligible). An unclassified path or an exemption that masks public contracts, runtime code, lockfiles, build inputs, CI, anchor inventory, or its own scope manifest is **rejected or MATERIAL** irrespective of writer assertions. No `docs/**` wildcard and no new policy database.

One L2 projection example (not a new mandatory schema):

```json
{
  "scope_version": 1,
  "material_selector": "ALL_TRACKED_MINUS_APPROVED_EXACT_NONMATERIAL_PATHS",
  "exact_exemptions": [
    {
      "path": "docs/planning/task-dag.json",
      "class": "DAG_ONLY_INPUT",
      "exempts": "SF_TREE_ONLY",
      "still_checked_by": ["DF_BLOB", "MI_DIGEST"]
    },
    {
      "path": "docs/planning/scaffold-task-map.generated.json",
      "class": "DERIVED_NONAUTHORITATIVE_OUTPUT",
      "exempts": "SF_TREE_ONLY",
      "still_checked_by": ["GENERATED_OUTPUT_RECOMPUTE"]
    }
  ],
  "classification_authority": "FROZEN_L2_SOURCE_OWNER_REF",
  "unknown_path_policy": "MATERIAL_OR_HOLD"
}
```

This is a **small semantic classification rule in the existing source/Freeze owner**, not another human Gate. Repo/project-specific filenames are allowed **only when backed by frozen owner classification**, not based on the example path literals. The existing L2 design's complete versioned source manifest and Git object identities remain authoritative, with no extra writable owner.

**Test evidence addition:** the in-session disposable Git/Python prototype was rerun with **N10: a source file listed as allegedly nonmaterial before SF acceptance → denied as an unapproved exemption**. Updated local prototype: **12/12 expected** (prior 11 + one new falsifier). The committed research fixture was amended at `references/v4.12/fixtures/v412_l2_git_pair_probe.py` (current Git blob `e360629cac23b481a0539b8c566f83f52e2b9e9b`). The fixture uses a **hardcoded synthetic role registry for its own sample files**; the *future actual checker* must use Frozen-L2/source-owner classifications and must not hardcode those example paths as universal legitimate exemptions. The GitHub-uploaded script's **exact bytes have not been separately executed**; its program text is a reproducible research asset, not formal CI PASS.

**Revised source-first closeout:**
- U02 structural feasibility: `E1_PROTOTYPE_SUPPORTED_12_CASES`, **not actual v4.12 production compliance**.
- U01 source Claim, U03 real Issue binding/SPLIT, U04 assertion proof composition retain existing owner and future exact implementation negatives.
- U05 unreleased predecessor remains a later Version Integration/Release constraint, **not** a reason to block source-only L2.
- **L2 Freeze remains `NOT_RECORDED`** until existing Architecture authority accepts the ADR and material classification/currentness conditions. No new v4.12 mandatory Gate/issue or Product R4.

```ini
L2_R2=BOUNDED_SELF_DOGFOOD_REPAIR
NEW_ARCHITECTURE_RISK=N10_PRE_FROZEN_ALLOWLIST_CLASSIFICATION
N10_STATUS=TEXT_DESIGN_REPAIRED_AND_MATCHING_E1_PROTOTYPE_EXPECTED
E1_LOCAL_SYNTHETIC_PROTOTYPE=12_OF_12_EXPECTED
GITHUB_COMMITTED_SCRIPT_EXECUTION=NOT_RUN
L2_FROZEN=NO
PRODUCT_FREEZE=R3_UNCHANGED
```


## 10. L2 R3 — deterministic pre-DF Work Item choice and owner-classified scope (2026-10-15)

> **Bounded L2 design closure, NOT Architecture Freeze or source-write permission.** This addendum resolves a material author-choice ambiguity in R2 ADR-01 and makes R2 N10's pre-acceptance owner evidence explicit. Frozen Product R3 and its blob remain unchanged. Prior R2 blob `9dd12912550bbd0db30d1f391084ae058eae56db` remains the reviewed source checkpoint; this R3 has a new exact blob.

### ADR-01 R3 — one canonical planning path, prospective adoption only

1. **Before Implementation DAG Freeze**, a planned `PLANNING_SCAFFOLD` source-writing concern is **one canonical `type:planning` Work Item** under the current Work Item Contract; `PLANNING_SCAFFOLD` is its concern/profile label, **not** an Issue type or an independent Claim. One appointed owner owns the overlapping source write set. Do not let the scaffold author dynamically choose `type:task` as a second admission route for this same pre-DF concern. Planning-only read/research evidence can remain inline or in an existing planning Issue when no actual source write is needed.
2. A `type:task` implementation Work Item is used **after the legitimate Implementation DAG Freeze/materialization** for feature or repair execution. An already-materialized project-local Task cannot silently be reclassified as pre-DF planning. If a project's frozen higher-authority override genuinely requires a different role/type, classify it as an **authority conflict requiring existing owner disposition before dispatch**, not as writer discretion.
3. The prospective **v4.12 Workflow/Work Item/Agent Interaction projection must explicitly authorize this single planning-source case at its correct phase**; the v4.11 Stage-2→Task-DAG→Stage-3 ordering is not retroactively changed. Until that prospective owner projection is lawfully adopted, a canonical planning Issue and Product/L2 drafts **do not permit a real Scaffold source write**. A complete scoped Issue, resolved pre-dispatch Review Policy, owner-approved allowed/forbidden source set, actual `READY`, accepted CAS `DISPATCH_CLAIMED` Start Record and readback remain mandatory. New source files, PRs, merged SF and executed external effects remain distinct authorities.
4. Actual DAG-I Task Issues are materialized only through their own authoritative DF checkpoint and GitHub-native dependencies; planning Issue history is provenance, **not** a substitute Task or an extra native dependency. A single immutable `SF→DF` link later binds the accepted merged planning source to canonical Task bindings. No second controller, claim ledger, Bootstrap Gate or equivalent approval role is introduced.

**Admission falsifiers:** `type:task` masquerading as pre-DF `PLANNING_SCAFFOLD` without an adopted phase rule → HOLD; `type:planning` with no accepted Claim → DENY source write; accepted Claim but unresolved required Review Policy or unapproved public contract semantics → SF NOT_ACCEPTED; a valid planning Claim authorizing file creation alone → still DENY unknown package install, postinstall, network, secret or remote effects until separately admitted under existing effect/environment policy.

### ADR-03 R3 — L2-owned exemption eligibility and exact SF acceptance

The Frozen L2/source-owner rule must define **eligible semantic classes and independent checking obligations**; future project-specific actual exact paths are classified at **SF source-review/acceptance time** against that already-frozen rule. A planning author may propose paths but cannot self-certify their exemption. Keep the original full tracked Git path inventory, file mode/kind/OID, scope-manifest identity and accepted-SF immutable tuple. Use NUL-safe Git path handling in a production checker.

| Exact-path class proposed at SF | May omit from SF material-view digest? | Separate obligatory proof |
|---|---|---|
| `DAG_ONLY_INPUT` | Only if *exact* path is approved as DAG-only by existing source owner | Current DF blob, MI canonical semantic digest and Task-binding validity |
| `DERIVED_NONAUTHORITATIVE_OUTPUT` | Only if the path cannot act as a canonical source/config/contract | Regenerate independently from trusted committed inputs and compare output |
| `FREEZE_RECORD_OUTPUT` | Only if the path is exclusively the record output | Real owner act + accepted immutable pair-input reference, no self-attestation |
| Source, ABI/contract/schema, build/lock/CI, anchor/scope manifest, Git symlink/gitlink/external reference with executable/material impact, or UNKNOWN | **No** | MATERIAL or HOLD; applicable owner validation/rebaseline |

The accepted SF's immutable exemption **path + class + checking obligation** must be verifiable from the source owner and fixed before the initial pair checkpoint. The eventual checker must not treat this document's example paths or the research fixture's hardcoded synthetic role registry as universal permissions. Subsequent additions/removals/renames must be evaluated using the accepted SF manifest, not a proposed successor's expanded list. The DAG/derived/record paths remain excluded from **SF-tree hashing only**, never from their distinct currentness/authority checks.

**Targeted negative oracles for implementation:** (a) preaccepted but unauthorized source file included in exemption registry → `SF_ACCEPTANCE=DENY`; (b) legitimate DAG-only successor with unchanged material Git objects → `SF_MV_REUSE=YES` while `DF_MI_RECHECK=REQUIRED` and stale derived output → `HOLD`. These are **design-level requirements, not newly executed tests**; historic E1 research evidence remains `12/12 EXPECTED`, with committed fixture exact execution and real native CAS `NOT_RUN`.

### L2 stop and owner decision packet

- **Design resolved for owner's acceptance:** U01 = unique `type:planning` pre-DF source concern, no source write until explicit prospective Workflow adoption and accepted Claim; U02 = scoped Git-object identity + preaccepted owner-classified exemptions; U03 = one current binding from canonical Issue scope, lawfully updated after SPLIT; U04 = reuse existing Validation/Release exact assertion evidence.
- **Known and not disguised:** U05 = v4.11 unreleased predecessor blocks eventual version integration/release, **not** current Architecture source study. The planning PR inherits historic `main` CI with a shallow checkout, while `version/v4.11.0` already carries the owner-reviewed `fetch-depth: 0` fix (Issue #1038 / PR #1040); its missing-history v4.9 kernel failure is a baseline lineage issue, not proof of v4.12 behavior. Reuse the qualified predecessor's CI fix at legal integration; do not open a duplicate v4.12 CI concern solely for this inherited failure.
- **Architecture Owner decision requested:** review and accept/adjust ADR-01/02/03 against frozen Product R3, the exact R3 blob and existing v4.11 owner standards; then record a *separate legitimate exact L2 Freeze* if no material contradiction remains. Do not silently mint approval from this author's analysis. No other all-workstream R4 audit, extra gate, real Build Host run or artificial Task materialization is warranted for these source-first facts.

```ini
L2_R3=SOURCE_DESIGN_DECISION_PACKET
PRODUCT_FREEZE=UNCHANGED_R3_EXACT_BLOB
U01_PRE_DF_CANONICAL_TYPE=type:planning_PROSPECTIVE
N10_EXEMPTION_POLICY=FROZEN_OWNER_CLASSIFICATION_AND_EXACT_SF_ACCEPTANCE
ARCHITECTURE_OWNER_DECISION=NOT_RECORDED
L2_FREEZE=NOT_RECORDED
IMPLEMENTATION_SOURCE_CLAIM=NONE
COMMITTED_PROTOTYPE_EXACT_RUN=NOT_RUN
CI_PREDECESSOR_MISSING_HISTORY=KNOWN_REUSE_PR1040_AFTER_LEGAL_REBASE
RELEASE=NOT_QUALIFIED
```


## 11. L2 R4 — ADS standard producer vs external conformance project (2026-10-15)

> **Owner-scope correction from user Product clarification.** ADS itself is a **development standard and workflow product**. Its primary deliverables are adopted documentation/owner rules, procedures, templates, schema/contract checks, lightweight reference tooling and evidence; it is **not** the generated application. This L2 interpretation is consistent with frozen PRD R3's acceptance on **one new-project and one mature-project case**. Frozen Product R3 blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9` remains unchanged. This author-produced addendum is NOT L2 Owner Freeze.

### Separate the subjects; never conflate their Task DAGs or release truth

| Subject | Real deliverable and execution authority | What its PASS demonstrates |
|---|---|---|
| **ADS v4.12 standard development (producer)** | Changes to ADS normative owner documents, workflow, contracts, templates, optional reusable checkers and ADS's own conformance harness; its **own** ADS-version Task DAG / GitHub Issues / Claims / Review / Validation / Release | Whether **the ADS standards release** was lawfully authored and qualifies under ADS's own applicable version procedure; documentation-only changes do not require an invented application Scaffold |
| **Fresh conformance project (consumer, NEW_PROJECT_INIT)** | An isolated small, actually buildable multi-module reference app/repo, its **own** planning Scaffold SF, Implementation DAG DF, Task Issues, native dependencies, accepted Claims, contract/integration tests, real packaging/user journey and release exercise | Whether the **ADS procedure being tested** produces an executable, source-current, verifiable consumer project; this consumer's PASS is not ADS release PASS |
| **Existing-project conformance case (consumer, EXISTING_PROJECT_ADAPT)** | Pinned existing-project source/repo or isolated faithful copy, minimal adaptation and bounded DAG/contract/claim/validation flow; do not regenerate its whole structure | Whether ADS handles incremental adoption/reuse without extra mandatory scaffold or DAG ceremony |
| **Algorithmic / static research fixture (supporting only)** | Disposable synthetic Git/Python cases like `v412_l2_git_pair_probe.py`, checked against exact source | Only the specific E1 predicate executed; **not** real GitHub CAS, independent Review, Build Host, or final user/release behavior |

**Correction to §7/§10 wording:** 'ADS v4.12 self-dogfood' means **ADS standard development exercises existing governance**, while prospective *Scaffold↔DAG co-evolution is tested on a separate conformance consumer*, not by treating the `ai-development-standard` repository itself as the greenfield generated application. ADR-01 R3's proposed pre-DF `type:planning` route applies to a consumer **only after that project's applicable adopted ADS owner rule** admits it. It must NOT be used to bypass ADS's own Task/Claim authority or to force creation of an ADS internal application skeleton. A conformance fixture committed to the ADS repository is an ADS testing asset governed by ADS implementation work; its embedded sample DAG/claims do not become ADS's actual execution DAG.

### Minimal test architecture (one concern, risk-bounded)

- **Static conformance layer:** run ADS schema/document/owner-cross-reference checks and deterministic negative fixtures under ADS's existing test commands; reproduce only exact invariants, avoid a new always-on graph server or universal full OS/CI matrix.
- **Consumer reference layer:** maintain the smallest **two** representative project cases already required by FR-04/AC-04: one clean-slate multi-module project and one pinned mature project. They may be isolated temporary repositories or fixture directories, provided actual file identities are preserved and output never writes into ADS normative directories. Avoid making sample application functionality part of ADS's public API/product promises.
- **Real workflow layer (when necessary for claimed behavior):** perform bounded GitHub Issue/Claim/PR/Review/merge/currentness flow in a separately authorized **test repository** (or an eligible isolated test target) to prove predicates that scratch fixtures cannot. Source-writing admission, policy adoption, real execution side effects and any Build Host/CI claims are subject to that consumer project's **own** lawful authority, not permission borrowed from an ADS planning document.
- **Release truth:** keep `ADS_STANDARD_RELEASE`, `CONSUMER_PROJECT_CONFORMANCE` and `SYNTHETIC_FIXTURE_E1` as three independent evidence subjects. Never project a test app's released status as the ADS standards release; never use ADS documentation CI PASS as proof of a functioning consumer.

### Acceptance and stop rule

**Needed v4.12 P0 proof:** adopted standard clauses + lightweight structural checker + one fresh and one mature project trace demonstrating source/Task bindings and required negative admission/currentness oracles. Exercise at least one actual consumer build/integration journey where required; reserve expensive GitHub/Host/Release repetitions only for unproven higher-risk behaviors. Record source exact SHA, actual execution/log and skipped or UNKNOWN assertions separately. No requirement to build a general-purpose app generator, application hosting service, or new product runtime in ADS.

**No new stage Gate, mandatory third project, or Product PRD amendment** is proposed. Existing Architecture Owner must decide this exact distinction before L2 Freeze; if any prior R0–R3 passage implies `ADS standard repository == generated Scaffold consumer`, **this §11 interpretation supersedes only that target conflation**, not the source/Claim/Review/three-way-pair requirements for real consumer projects. Product Freeze remains scoped to the already accepted R3 requirements.

```ini
L2_R4=ADS_STANDARD_VS_CONFORMANCE_CONSUMER_SUBJECT_CORRECTION
ADS_DELIVERABLE=NORMATIVE_DOCUMENTS_WORKFLOW_TEMPLATES_CHECKERS
ADS_OWN_TASK_DAG=STANDARD_DEVELOPMENT_GOVERNANCE_ONLY
SCAFFOLD_DF_TEST_SUBJECT=ISOLATED_CONFORMANCE_CONSUMER
CONSUMER_CASES=NEW_PROJECT_INIT;EXISTING_PROJECT_ADAPT
REAL_GITHUB_WORKFLOW_PROOF=NOT_RUN
ARCHITECTURE_OWNER_FREEZE=NOT_RECORDED
PRODUCT_R3_FROZEN_BLOB=0bfbf782c8859e79df52c9b57904ad80bcd718e9
NO_NEW_GATE=YES
```
