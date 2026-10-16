# ADS v4.13.0 — Product Requirements R0: Foundation for Tally v2

> **STATUS: PRODUCT_FREEZE_CANDIDATE / DRAFT / NOT FROZEN**  
> Product intake: [#1147](https://github.com/kaicreator-mm/ai-development-standard/issues/1147). Architecture scope successor: [Draft PR #1150](https://github.com/kaicreator-mm/ai-development-standard/pull/1150). Tally's independent implementation: [tally #55](https://github.com/kaicreator-mm/tally/issues/55) and [Tally Draft #56](https://github.com/kaicreator-mm/tally/pull/56).  
> Scope direction explicitly confirmed by user on 2026-10-16: **v4.13 is solely ADS normative/configuration/interface preparation for Tally v2; Tally owns all executable implementation**. No new intermediate ADS version; no dependency on Tally v2 release. Exact qualified predecessor to be verified from remote source prior to L2/implementation admission. Historical frozen v4.12 source is not rewritten.

## 1. Product problem, intended users, value

**Problem.** ADS now has substantial process/authority/validation standards and v4.12's exact-source stable-compatible selection. Tally has a working, separately modeled Engineering Control Plane, multi-Agent lifecycle and runtime; its historical project ADS adoption uses a 1.2.1 YAML pin. Moving Tally toward the latest ADS-native normative semantics without an explicit, minimal interoperability contract would create competing Task/DAG/Claim authority, version drift, redundant validation, and two incompatible Toolkit implementations.

**Consumers:**

- **Tally v2** is primary *execution-platform consumer*, not an ADS build dependency.
- **Independent Agents and other adopter platforms** must continue to use ADS alone via immutable project pin, without any Tally installation.
- **Organizations/projects/Build Hosts** use an ADS-declared Organization Development Environment Profile to choose compatible defaults; an installed host tool is an observed fact, not project Product authority.
- **ADS maintainers** need a self-contained source-only release proving coherence and applicability of the standards and reference contracts.

**Benefit test:** Tally v2 can implement one semantics-aligned provider and reuse mature internal infrastructure without duplicating ADS policy engines. ADS itself becomes easier to adopt and still independently releasable.

## 2. Fixed authority and data boundaries

| Subject | Canonical owner for this ADS release | Consumer behavior |
|---|---|---|
| Product/Architecture/Task/Claim/Review/Validation/Release semantics | Existing effective frozen ADS standards from **exact qualified source revision** | Tally reads and implements; not a competing normative definition |
| Org defaults / runtime preferred versions and config precedence | New additive v4.13 org environment Profile schema/contract consistent with existing toolchain owners | Host/Tally resolves values; no policy authority from mise or local installation |
| GitHub native Issue dependencies, accepted Claims, PR/Review/Merge, Git SHA/currentness | Actual GitHub facts; ADS supplies interpretation semantics | Tally's Active TaskDAG for ADS-native project is a **readable operational projection**, not an independently writable alternative Issue/dependency fact source |
| Agent/Host/Execution Attempt/Scheduler snapshots | Tally runtime, not an ADS Gate or native GitHub fact | Tally may independently store/retry these local states |
| DevKit/CLI/Agent Skills/MCP and cross-project PR executor | **Tally repository only** | ADS defines minimal portable behavior/interface requirements, no hosted implementation |
| Compatibility-qualified ADS release, version migration semantics | ADS pinned source + actual Release and source/behavior/authority proof | Tally may create opt-in PRs only on qualified compatible proposals; effective pin changes at legal project checkpoint |

**Actor contract:** logical roles/identity are self-declared by an execution actor; GitHub account is transport and real platform permissions. No Owner credential-based identity validation. Claims, execution evidence, actual tests, immutable sources and actual legal/external effects are **not** replaced by role self-declaration.

## 3. Functional requirements (FR)

### FR01 — Organization Development Environment Profile (P0)

ADS SHALL document a **versioned, machine-readable, independently usable** organization environment profile with only required minimum fields and one realistic organization example. It SHALL separate:

1. project compatibility requirements (runtime ranges, project-selected tool/manager/lockfile and frozen Product/Architecture constraints),
2. organization preferred toolchain/defaults, caches/mirrors and host capability expectations,
3. project-local exceptions/overrides and reproducible override precedence,
4. observed host environment/tool availability, and
5. *real* certification evidence (platform × toolchain × validation profile), which no preferred version can invent.

The effective resolution is source-attributed and fails with **CONFLICT/UNKNOWN** instead of silently overriding incompatible project requirements. Profile defaults are declarative, not installation or global forced runtime selection. Existing `DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md`, `profiles/*`, `PROJECT_ADOPTION.md` and frozen project manifests remain the authority; new schema SHALL not redefine existing language/archetype Profiles. Do not require all projects to install mise/Worktrunk, adopt pnpm, share mutable venv/node_modules, or use Windows/Ubuntu specifically. Machine-local tokens, proxy secrets and credentials are references/config injected locally, never committed into organization policy.

**AC01:** Two compatible projects resolve the same organizational suggestion and two conflicting projects yield explainable project-overrides/conflict outcomes from deterministic source-pinned fixtures; no host binaries need be installed for this ADS acceptance.

### FR02 — ADS-native execution/interop mapping contract (P0)

ADS SHALL publish a **compact semantic crosswalk and source-bound examples**, not a second Tally domain model, mapping:

- pinned ADS `.dev-standard/VERSION` `repository/version/revision` and project `PROJECT_OVERRIDES` against exact source currentness;
- L1/PRD, L2, Implementation Task DAG/Task/accepted Claim, runtime Attempt, native GitHub Issue Dependency, PR, Review, Validation and Release evidence;
- external GitHub native **Task facts** versus Tally **runtime scheduler/Host/Attempt local state**, including stale/unknown reconciliation requirements;
- self-declared Agent role/ID and exact source/candidate/actual execution tuple;
- truthful `PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE` versus separate scheduler/provider state.

ADS SHALL prefer referencing existing schemas/protocol owners and provide at most the genuinely missing minimal interoperable additions. It SHALL NOT define a competing Task DAG scheduler, project database, Claim CAS service, Review/Release controller or new Gate status. A local projection may optimize scheduling but cannot certify contradictory native task dependencies or latest effective source without current GitHub readback before materially consequential actions.

**AC02:** One fixture with a real native blocked_by relationship, Tally local READY projection, immutable Task pin and staleness shows dispatch must HOLD when GitHub still blocks; separate happy-path fixture advances only after authoritative currentness/Claim/Review/actual evidence requirements are satisfied.

**AC03:** Two logical Actors using the same GitHub transport login are represented as separately self-declared contexts; no Owner-signature gate. A forged PASS, stale SHA, missing actual test or unauthorized GitHub write is still refused.

### FR03 — Qualified compatible ADS adoption and activation rules (P0)

ADS v4.13 SHALL **reuse** qualified-release proof, effective exact SHA pin and read-only compatibility selector shipped in v4.12. It SHALL clarify a portable **three-action contract**:

```text
READ_ONLY_COMPATIBLE_PLAN  (no project write, can examine prospective updates)
→ OPTED_IN_PROJECT_UPDATE_PR  (source-scoped proposal only, effective pin unchanged)
→ PROJECT_CHECKPOINT_ACTIVATION (re-check exact source/permissions/compatibility/Claim/freeze facts)
→ optional bounded ROLLBACK as a fresh project-authorized operation
```

This distinction avoids equating any unrelated open GitHub Issue/PR with a conflicting active Task, **without** weakening the existing v4.12 fail-closed source validation or silently mutating its published selector. Unknown relevant Task/Claim/currentness blocks **activation**, though an accurately labeled *prospective plan* may exist. Projects have default `PINNED/MANUAL`, cross-repository PR creation is opted-in, and an in-flight Task retains its old effective ADS revision. Human-authored project overrides, historical evidence and frozen PRD/L2/DAG/candidates are unchanged.

**AC04:** A qualified compatible ADS revision can be *proposed* for an active project with unrelated open Issues while an accepted running Task still pins its original revision and activation is disallowed if relevant source evidence is unknown.

**AC05:** Unqualified tag, semver-only assertion, compatibility UNKNOWN, unpublished Release, missing opt-in, stale base, failed GitHub permission or irreversible frozen-Task mutation cannot become activation or fabricated read-only `SAFE`. This ADS release shall **not** actually create downstream PRs; Tally v2 is the writer/Host runtime.

### FR04 — Minimal capability-aware validation / release interop (P1 where genuinely missing)

Where current `VALIDATION_STANDARD.md` and `RELEASE_STANDARD.md` leave a material normative gap, ADS SHALL define an **additive capability→required-proof applicability crosswalk**, not six software-delivery engine implementations:

| Capability actually delivered | Potential required evidence (only when Product/L2/project policy demands it) |
|---|---|
| Normative documentation/schema/templates | Cross-document owner consistency, exact source/manifest, deterministic positive/negative schema examples |
| Executable SDK/CLI | Actual executed API/entrypoint and relevant runtime/profile correctness |
| Git/filesystem/Host mutations | Real workspace/paths/concurrency/cleanup/error behavior |
| Services, external effects, physical hardware | Required actual endpoint/authority/physical negative scenarios, when genuinely shipped |
| Packaging/distribution | Applicable real install/launch/download evidence |

The same exact current executed predicate may be reused only if all relevant subject/tuple/impact conditions remain identical. `NOT_RUN` never becomes `PASS`; source-only ADS does not inherit Tally CLI Host gates. `SELF_COHERENCE` + relevant ADS standards source self-dogfood before ADS release; independent Tally runtime and multi-project `FIELD_VALIDATION` occurs under Tally's own version process **after** qualified ADS v4.13, unless a future legitimately frozen Product requires otherwise.

**AC06:** Mixed standards+CLI consumer class cannot mark shipped CLI checks N/A, while standards-only ADS need not demonstrate Tally/real runtime delivery. Small changes use existing bounded impact/reuse rules; no generic full OS matrix or repetitive root suite required.

### FR05 — Selective reuse of v4.12 residual W1–W5 and existing normative behavior (P1 only if source gap proven)

ADS SHALL make a source-grounded `ALREADY_SATISFIED | MATERIAL_GAP | DEFER | EXCLUDE` disposition against #1096/#1100/#1116, explicitly retaining v4.12 delivered #1099 risk-bounded value, #1123 logical Actor/Owner credential cleanup, project adoption/selector and limited impacted-validation rules. W1's conceptual phase-scoped views do not imply separate mandatory DAG stores; W2/W3/W4/W5 **execution functions** belong to Tally, not ADS. Only a material interface/authority gap justifies extra v4.13 normative writing. No task-per-historical-idea expansion.

**AC07:** Every proposed v4.13 normative write maps to a current canonical source owner and one falsifiable consumer need; fulfilled or unrelated W1–W5 ideas create no extra Task.

## 4. Explicit exclusion & repo boundary

**ABSOLUTELY NOT ADS v4.13 implementation:** copying devkit into ADS, Bootstrap installer, `ads dev` executable CLI, mise/Worktrunk/native Git Worktree provider, bare mirror orchestration, cleanup/scheduler server, Agent Skills/MCP implementations, Tally rewrite, SQLite/Postgres migrations, actual multi-Agent dispatch, Project Portfolio, Tally cross-project updater PR writer, Tally UI, Host deployment on Windows/Linux, real Tally user journeys, Tally runtime release qualification.

All executable work belongs exclusively to Tally [#55](https://github.com/kaicreator-mm/tally/issues/55) / [Draft PR #56](https://github.com/kaicreator-mm/tally/pull/56). **This PRD does not freeze, approve, merge, build or release Tally v2.** Keep Tally v1.5.x old YAML adoption pin and frozen facts untouched; Tally prospective migration is its own Task.

## 5. Acceptance, gates, release blockers, closure

**Release blockers only for ADS's shipped subject:**

- **P0/B1:** normative config/interop/adoption clauses contradict one another, existing project source authority, or native GitHub Issue/Claim/PR fact boundary;
- **P0/B2:** organization default can override incompatible frozen project requirement, or secrets embedded in normative example;
- **P0/B3:** an unqualified/mutable latest ADS version can be inferred safe, active Task gets re-pinned, or required Claim/Review/actual test facts are bypassed;
- **P0/B4:** manual `NOT_RUN`/simulated output described as actual Validation PASS or Release PASS; source-vs-executable applicability cannot be decided for mixed consumers;
- **P0/B5:** source-only ADS v4.13 closure lacks applicable current exact-source coherence/Release qualification proof, or the successor silently rewrites frozen predecessor standards.

**No blockers:** Tally v2 implementation/tests/release, unrelated projects' actual upgrades, standalone mise/Worktrunk real execution, every hardware/OS variant for a standard document, cosmetic updates, or an R1→R8 review campaign without novel material contradictions.

**Required Product-level gates (current ADS Stage1):**
- one semantic L1/source-gap report within this PRD and #1147,
- **one selected independent Product Review** for this new compatibility/authority-sensitive Product subject at exact source blob/SHA (mandatory under `DEVELOPMENT_WORKFLOW.md` Stage1),
- explicit Product authority Freeze on reviewed exact PRD blob + remote checkpoint;
- after Product Freeze, separate L2 architecture evidence/disposition/Freeze and Task DAG freeze under existing rules;
- implementation source truth, bounded changed-source tests, exact candidate and applicable existing release gates. No new Gate states, Owner credential gate or cross-product release dependency.

**Product Freeze subject and precedence:** The eventual Freeze record MUST bind the exact authored PRD Git blob and actual review decision. An issue title, PR creation or this author's self-review is **not** the freeze. Any change to FR/AC after Freeze requires lawful amendment, not stealth PRD revision.

## 6. Source-gap and risk/ROI record (L1 evidence)

| Area | Current source evidence | Observed gap or route | Decision |
|---|---|---|---|
| Org profile | `DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md` already distinguishes compatible/preferred/certified/deployed; current `profiles/` project language model | no single org-scoped portable precedence/profile sample identified in inspected current owners | **MATERIAL_GAP → FR01** |
| Task/GitHub | `TASK_DAG_GOVERNANCE_STANDARD.md` native Issue Dependencies, `DEVELOPMENT_WORKFLOW.md`, `PROJECT_ADOPTION.md` | external Tally internal DAG semantic conflict / no concise interoperability crosswalk | **MATERIAL_GAP → FR02**, not new authority |
| Compatible ADS update | `PROJECT_ADOPTION.md` + `scripts/v412_ads_compatible_select.py` genuine source-bound read-only advisory; #1119 remains open | prospective PR vs checkpoint activation not compactly separated for Tally future writer | **MATERIAL_GAP → FR03** |
| Delivery type | `VALIDATION_STANDARD.md` Task vs candidate scope, `RELEASE_STANDARD.md` source-only v4.12 applicability | mixed standards + real Tally executables and conditional capability proof mapping needs small clarification if current source truly insufficient | **CONDITIONAL GAP → FR04** |
| W1 conditional graphs / W2 Steward | `DEVELOPMENT_WORKFLOW.md` and `TASK_DAG_GOVERNANCE_STANDARD.md` task/phase graph rules | implementation monitoring/scheduler better in Tally | **REUSE/DEFER** |
| W3 environment lifecycle | devkit patterns + Tally v1.5.2 runtime & host | declarative interface FR01 needed; all runtime in Tally | **SPLIT: FR01 + Tally** |
| W4 learning / W5 research & ROI | #1099, existing ADS learning and source reuse standards | no new general standard or service justified yet | **ALREADY SATISFIED / EXCLUDE** |
| #1123 actor identity & #1099 value | already delivered v4.12 | duplicate credential gates or extra process would regress | **REUSE AS IS** |

Inspected source facts are as of `main@4465e291df4e60e09af634a25ab7eed546b2915b` where applicable; future currentness MUST re-check any changed canonical owner prior to L2/implementation; don't presume a GitHub Release from source files alone. Planning lineage: PR #1150 head may change; attach current exact source on Review submission.

## 7. Stage2 handoff questions (not Product blockers)

1. Schema owner placement and representation: new `schemas/organization-development-environment-profile-v1.schema.json` plus non-normative organization example vs additive existing toolchain profile; choose smallest owner without redefining established v4.3 language/archetype.
2. How to represent ADS-native GitHub source facts versus Tally operational Attempt state without an all-consuming new task machine schema or requiring a Tally-specific import from independent adopters.
3. Whether `PROJECT_ADOPTION.md` FR03 wording alone suffices with a few counterexamples, versus one small proof projection for future releases; do not rewrite the whole v4.12 selector.
4. Whether FR04 requires actual normative text once current release applicability source is inspected; if not, mark `ALREADY_SATISFIED` and skip.
5. Integration baseline/version branch from actual qualified v4.12.1 successor and exact issue/PR/adoption source at admission.

**One source only:** Product authority is this single reviewed and exact-frozen PRD, not independent Comment/Product scope variants. Follow with bounded L2 and minimal DAG after lawful freeze; no automatic Tally dependency.
