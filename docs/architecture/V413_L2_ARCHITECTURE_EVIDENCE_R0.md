# ADS v4.13 — L2 Architecture Evidence R0 (Foundation for Tally v2)

> **STATUS: ARCHITECTURE_CANDIDATE / SOURCE-ONLY / NOT L2 FROZEN.**  
> Frozen Product: `docs/product/v4.13.0/ADS_V413_PRD_R0_TALLY_FOUNDATION.md`, Git blob `702bcf562b4292487fa8409cd17dee2d42aae9b3`, Freeze checkpoint `3123d7d4bd5ef7b8f9236119537ff9226d6bd3a9`; independent Product review R0 + P1-01 diff fix at [#1147](https://github.com/kaicreator-mm/ai-development-standard/issues/1147). This L2 is subordinate to that exact frozen Product, not a re-open of scope. Current inspected predecessor canonical source `main@4465e291df4e60e09af634a25ab7eed546b2915b` reports `VERSION=4.12.1`, but **actual released/qualified predecessor must be independently resolved before implementation baseline and version closure**; a source version string does not prove Release Qualification.

## 1. Drivers, scope and non-goals

**Drivers:** (D1) independent ADS use; (D2) Tally v2 consumer can interpret immutable standard/project policy; (D3) existing GitHub-native Issue/Claim/PR facts remain unique; (D4) organization-level development suggestions do not override compatibility or measured host evidence; (D5) source-proven ADS compatibility recommendation/PR/activation remain separate; (D6) validation/release truth/cost apply only to what ADS v4.13 itself ships.

**Out of scope:** ADS `dev` runtime CLI, import of devkit code, running mise/Worktrunk/native Git, agent fleet/scheduler, Tally Go/core/server rewrite, Tally Skills/MCP, actual project updater/rollback writer, platform/host certification and Tally v2 release. That implementation is entirely `kaicreator-mm/tally` under [#55](https://github.com/kaicreator-mm/tally/issues/55), Draft [#56](https://github.com/kaicreator-mm/tally/pull/56); do not put it in ADS's Task DAG.

## 2. Canonical source-owner map — avoid new semantics authorities

| Interface concern | Existing canonical source owner | v4.13 minimal delta |
|---|---|---|
| project immutable ADS pin | `standards/PROJECT_ADOPTION.md` and `.dev-standard/VERSION` template | clarify exact qualified source + future consumer prospective/adoption checkpoint projection; no mutable alias |
| toolchain compatibility, preferred, certification | `standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md` and `schemas/dependency-toolchain-profile-v1.schema.json` | **add separate organization-default declaration**, not a replacement for required project repository/manifest/certification profile |
| language/archetype profiles | existing `profiles/*`, existing profile governance | org configuration is separate axis, not a `language`/`archetype` type mutation |
| native Issue DAG / Git workflow | `standards/TASK_DAG_GOVERNANCE_STANDARD.md`, `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` | one concise read-only Tally consumer crosswalk, no independent ProjectFlow/state store |
| logical Agent/attribution | `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, existing role/authority owner | reuse actor-supplied `operator_kind/operator_id/session_ref/role`, not GitHub identity checker |
| source/behavior compatible versions | `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md`, `schemas/compatibility-record-v1.schema.json` | ensure semantic, behavior/authority and evidence refs, no second verifier or reduction of UNKNOWN |
| test/review/release truth | `standards/VALIDATION_STANDARD.md`, `standards/RELEASE_STANDARD.md`, existing Check/Review/CI owners | candidate evidence-applicability *reference table only if real uncovered gap* |
| local workspace/data safety | `WORKSPACE_ARTIFACT_STANDARD.md` | only illustrative Tally runtime boundary; no ADS workspace manager |
| devkit tools | `kaicreator-mm/devkit` source and Tally v2's own code | **no source copy into ADS**, use Tally runtime adapter |

## 3. Decision A1: additive Organization Development Environment Profile (FR01)

**Ownership:** new additive normative subsection of `DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md` as the authority for organization **defaults**; minimal new `schemas/organization-development-environment-profile-v1.schema.json` for the portable declaration and `examples/organization-development-environment-profile.json` for a positive grounded example. Add a small negative/precedence fixture reference, **not** a schema-per-toolchain.

**Why separate organization schema:** existing `dependency-toolchain-profile-v1` requires `repository`, `manifests`, per-project `compatibility` and `certification_tuples` and is an *optional project-level durable profile*. A shared organizational default has no single authoritative repository manifest, project compatibility range or already-executed certification; reusing it unmodified would force fabricated material values. The new schema describes defaults, not project-specific toolchain authority.

**Candidate minimal shape** (precise JSON Schema remains S02 concern):

```json
{
  "schema_version": 1,
  "profile_id": "org.kaicreator-mm.development",
  "organization": "kaicreator-mm",
  "preferred_toolchains": {
    "node": {"preferred_version": "ORG_APPROVED_VERSION"},
    "python": {"preferred_version": "ORG_APPROVED_VERSION"}
  },
  "environment_hints": {
    "cache_policy": "shared_reconstructible_only",
    "workspace_policy": "per_task_isolated",
    "offline": "allowed_only_when_exact_source_proven"
  }
}
```

No credentials, universal package-manager mandate, system path, explicit hardcoded language versions or source-specific host installer in global profile. No `certification_tuple` field in org profile; authoritative real certification remains project/runtime evidence elsewhere. `environment_hints` is advisory, not proof of installed software.

**Resolution function:** `resolve(project_contract_at_exact_SHA, org_profile_at_exact_SHA, host_observation)` SHALL return traceable **policy decision / conflict / unknown**, not real installed runtime or release certification. Correct precedence: exact project Frozen Product/Architecture + authoritative manifest/lock/runtime requirements > explicit compatible project override > compatible org preferred suggestion > host feasibility observations; host availability cannot legalize an incompatible project runtime. When multiple compatible values exist, project preference wins. When org preference falls outside a project required range, explicitly report ignored org suggestion and obey project choice if present, else `CONFLICT/UNKNOWN` rather than forced install. No secret persistence or automatic project mutation.

**Representative acceptance:**
- P: project Node compatible includes org suggestion; resolution returns `preferred_source=org`, no claim of installation.
- P: project has a compatible own exact preference; source attribution returns project choice.
- N: project Python range excludes org suggestion; org not applied; no rewritten lockfile.
- N: host reports a binary version but project requires another; host fact does not override the required version.
- N: certification absent; profile statement does not become a certified Release tuple.

## 4. Decision A2: ADS-to-Tally interop is a non-authoritative semantic projection (FR02)

**No new workflow schema or independent Task/Claim data store.** Document a compact mapping in a single consumer-neutral standard appendix or `references/v4.13/ADS_EXECUTION_INTEROP_CONTRACT.md`:

```text
Frozen ADS/Project Product+L2 + exact effective ADS revision
             ↓ (read-only contract resolution)
GitHub Task Issue/native blocked_by + accepted Claim + exact Git HEAD
             ↓ (Task eligibility checked, not inferred from title)
Tally Active DAG read-only projection → Tally Attempt/Host/Agent state
             ↓ (bounded runtime work owned by Tally only)
actual ChangeSet + test execution evidence + selected independent Review
             ↓ (exact source and applicable gate currentness)
GitHub PR/Review/Merge readback → eligible Task/Version fact projection
```

Authority split:
- Native GitHub Issue dependency edges, actual accepted Claim event, PR/Review/merge/current SHA are **external durable facts**, evaluated at current exact ref. No Tally snapshot write silently changes them.
- Tally owns local **operational** Task Attempt, queue, session, host capabilities, dispatch and retry/cancel/restart. Persisting a local Derived Ready projection is permitted, but it cannot be a second canonical GitHub Issue dependency authority.
- Read-only projection supports **stale/unknown/contradictory** status; material dispatch/merge must re-read required GitHub facts. Repository outage/permission missing => hold only the affected action; unrelated operations may continue where their required evidence remains available.
- `actual_validation_tuple` and source/change SHA are separate from provider/CI health, self-declared role and agent claim. `PASS` requires execution, not agent narration.
- Historical Tally 1.2.1 YAML project pin is a different project-era format; future Tally adapter may migrate prospectively, preserving frozen historical Task/Review/Release source identities. ADS v4.13 does not change `PROJECT_ADOPTION.md` canonical pin format to accept arbitrary legacy YAML.

**No state duplication:** reference existing `schemas/*` for Task, Claim, Dispatch, Validation report and compatibility records by path in the implementation concern; if a referenced schema is not found at the exact source, the consumer must explicitly mark UNKNOWN and escalate to a narrow new schema owner rather than inventing a normalized source of truth.

## 5. Decision A3: #1119 upgrade source proof + three independent checkpoints (FR03)

**Keep v4.12 read-only selector behavior unchanged.** Current `scripts/v412_ads_compatible_select.py` rejects any open Issue/PR at the live-project safety checkpoint. Its `NO_SAFE_RECOMMENDATION` is **not** proof of compatibility, cannot directly feed an update PR, and is not a prospective positive decision.

**Add normative minimal source-bound semantics to `PROJECT_ADOPTION.md` under existing interface compatibility owner; **no new module/service**:**

```text
P0: source-qualified candidate + project behavioral/actor/Claim/Review/Release
    compatibility positive ⇒ EVIDENCE_BACKED_COMPATIBLE_PROPOSAL (non-SAFE advisory)
    absent/stale/contradictory ⇒ PROSPECTIVE_UNVERIFIED/UNKNOWN (no PR)

P1: project opt-in + current target/head/permissions + source verified proposal
    ⇒ bounded update PR may open, effective .dev-standard/VERSION unchanged premerge

P2: immediately before PR merge, source/Claim/frozen candidates/permissions/
    affected Task isolation + real project required checks/review revalidated
    ⇒ lawful checkpoint activation/new eligible task pin
    unknown/conflicting state ⇒ no authorized merge, preserve old effective pin

P3: rollback ⇒ new project-authorized source-bound PR, never historical rewriting
```

**Important exactness:** merging a PR that modifies effective `.dev-standard/VERSION` changes project pin. Therefore a purported `ACTIVATE` *after* already merging without checks is a loophole. PRE-MERGE approval is necessary; frozen accepted old Tasks remain at their accepted old exact ADS revision. Do not add a Github account Owner credential Gate; actual permissions still must be observed. The upgrade writer, dedup, auth/portability and real E2E live entirely in Tally v2.

**Minimal standard change owner:** `PROJECT_ADOPTION.md` one addon + existing `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` reference, with a handful of positive/negative source-only cases. Existing v4.12 selector code remains unmodified; no separate parallel ADS compat runtime.

## 6. Decision A4: #1116 risk/capability applicability only for proven gap (FR04)

Existing `VALIDATION_STANDARD.md` §1/§4/§6 and `RELEASE_STANDARD.md` §2/§11 already cover exact subject/profile, NOT_APPLICABLE proof, change-impact reuse, final candidate composition, and standards-repo own non-runtime effects. **Do not create six new delivery-specific validators or an extra approval process.**

L2 disposition: **likely ALREADY_SATISFIED for ADS self and common code/CLI distinction**. If actual inspection of release applicability and mixed standard+executable cases yields a falsifiable uncovered case, S04 may add **one small capability→required-proof table** to the existing owner, with one positive/one negative example. Otherwise record `ALREADY_SATISFIED`, omit changes to Validation/Release Standards and mark FR04 acceptance by existing source pointers. This conditionality is authorized by PRD P1/FR04, not a silent weakening of a mandatory rule. Runtime evidence for Tally's real shipped CLI/server belongs to Tally v2.

## 7. Decision A5: minimal work organization / version release

- **No ADS-runner runtime:** neither `toolkit/ads-dev` nor `ads dev` host CLI, Agent Skills/MCP, env installer, Worktrunk adapter, bare mirror implementation, cross-repo updater writer, Project Steward or Task Learning storage.
- **No new stage authority:** reuse present ADS Product Freeze, L2 Freeze, Task DAG, issue Claims/Review/Validation/Release. Only Phase 2 source evidence and genuine material source fixes.
- **Release qualification:** standards-only source/evidence/fixtures, required existing version closure gates, one final exact candidate. `PR PASS != Release PASS`. Real Tally consumer deployment/testing is **post-release field learning**, not an ADS version release blocker.
- **Task-size discipline:** minimal separate concerns `S01` source-gap/admission (this L2 and PRD historical evidence can cover source analysis); `S02` Org Profile schema/normative+examples; `S03` Tally interop/Task/Claim mapping; `S04` conditional #1119/#1116 standard delta; `S05` one candidate integration/source-check and release handoff (may be existing release checkpoint, not artificial fifth implementation Issue). Merge or cancel steps already evidenced by unmodified predecessor.
- **Parallel execution:** S02 (toolchain owner) and S03 (interop reference) are disjoint; S04 (PROJECT_ADOPTION) may proceed separately from S02 and S03 until reference text depends on their names. No code baseline Stacked PR without true unmerged dependency. One concern/PR, smaller diff reviews, final version closure once.

## 8. Material architecture UNKNOWN register + dispositions

| ID | Question / risk | Evidence and decision | Disposition / Freeze impact |
|---|---|---|---|
| U01 | Will organization config accidentally override project manifest/lock or fabricate certification? | Existing toolchain standard separates five dimensions; existing project profile schema is repository-required; design introduces **separate org-declaration** + project wins | **STATIC_EVIDENCE_SUFFICIENT**, schema/fixture verification to S02 |
| U02 | Can Tally Active DAG and GitHub native deps both be canonical? | GitHub protocol/native Issue graph already canonical, status card a projection; derived runtime Attempt independent | **STATIC_EVIDENCE_SUFFICIENT**, one diagram+negative in S03 |
| U03 | Does source-only prospective upgrade need a second GitHub runtime selector? | PRD FR03 review P1-01 closed after showing separate proof obligations; no v4.12 selector edit; source bounded Tally future adapter | **STATIC_EVIDENCE_SUFFICIENT** for semantic protocol; real updater E2E deferred **to Tally**, not ADS L2 unknown |
| U04 | Can source-only standards certify executable CLI/physical effects? | Validation §1–4 and Release §2/§11 explicit capability/gate authority; requires actual tests when delivered | **STATIC_EVIDENCE_SUFFICIENT**; S04 changes only if source gap demonstrated |
| U05 | Does Tally v2 migration to new pin break its old frozen v1.5.x events? | migration not executed by ADS, old project pin remains current for those archived subjects, Tally v2 Product owns actual migration | **OUT_OF_ADS_SCOPE**, explicit consumer interoperability warning |
| U06 | Is main v4.12.1 actually published/qualified predecessor? | `main` source `VERSION=4.12.1` / README says static source identity is not Release proof; v4.12.0 public qualification historically documented; GitHub qualified Tag/Release is separate | **BLOCKED FOR IMPLEMENTATION ADMISSION**, **NOT BLOCKING SOURCE-ONLY L2 design**; source-owning controller must verify actual immutable qualified version before version integration/Release |
| U07 | Must schema be machine-executed now to prove architecture semantic possibility? | standard JSON Schema dialect and existing examples well established; implementation generates new JSON schema and bounded fixtures | **STATIC_EVIDENCE_SUFFICIENT** for L2; no mandatory Research Demo. Real schema conformance belongs S02 / closure |

No unresolved high-impact unknown changes the **architecture** decision if actual predecessor cannot yet be qualified: that is an execution/version admission prerequisite, explicitly separate and must not be misrepresented as PASS. Therefore **no standalone Architecture Research Demo is justified**. A future found conflict with immutable owner/published Release returns `BLOCKED` and revisits only the affected L2 decision.

## 9. L2 validation and freeze eligibility — NOT RUN

**Author/source E1 checks planned:** cross-read canonical owner links, ensure distinct org/project schema shape, impossible/unknown negative examples and unsafe merge prevention, Tally implementation exclusion; confirm frozen PRD blob unchanged, source SHA and actual main qualified predecessor separately. `GITHUB_READBACK/STATIC` is not a deployed/GitHub-live Task/CI/Release claim. An independent L2 review can be selected once for the exact candidate if required by current risk policy; only actual distinct review/judgment may claim independent PASS. No recurring research/verification spiral.

**L2 Freeze readiness** may be determined only on exact L2 blob after the above owner/unknown decisions and scope/authority assessment. L2 Freeze is separate from Product Freeze and does not authorize implementation Task Claims or tag/release.

## 10. Handoff to Task DAG (planned, not frozen)

Inputs: this exact L2 Architecture after its Freeze; immutable Product R0 blob `702bcf...`; real qualified predecessor/source readback; four minimal concerns above. After valid L2 Freeze create source-pinned Task DAG (Issue Dependencies only where genuinely material), L3 `Tests→Contract→Implementation→Failure Handling→Reference`, accepted Work Item/Claim, then write targeted standard/schema files. **All runtime Tally implementation Task DAG remains in the Tally repository.**
