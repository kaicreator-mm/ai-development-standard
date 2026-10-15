# ADS v4.12 — #1119 Latest-Compatible Adoption Scope Decision Candidate R0

> **STATUS: NON-NORMATIVE FEASIBILITY/OPTION RECORD ONLY.** User asked on 2026-10-15 “#1119 能加入 v4.12 吗”. This is **not** an explicit migration, Product Freeze, L2 Freeze, DAG amendment, Task Claim or authorization to update any consuming project. This record permits the user to decide between a bounded v4.12 standards core and the full opt-in updater. Keep #1119 currently in v4.13 until the desired delivery depth is actually approved. No frozen Git blob changes.

```ini
EVENT=ADS_V412_I1119_SCOPE_FEASIBILITY_CANDIDATE
SOURCE_ISSUE=#1119
CURRENT_ISSUE_TARGET=v4.13.0
PROPOSED_TARGET=v4.12.0_WITH_EXPLICIT_USER_APPROVAL_ONLY
SOURCE_PREDECESSOR_PRODUCT_R3_BLOB=0bfbf782c8859e79df52c9b57904ad80bcd718e9
SOURCE_PREDECESSOR_L2_R5_BLOB=68608ef6456334d627db1797ba2e023233c84ce7
SOURCE_PREDECESSOR_DAG_R3_BLOB=adc9e522f3b734a59898091945b9c7545530565a
I1123_ALREADY_APPROVED_V412_PRODUCT_DELTA_BLOB=847e707b78359f6e9de2901b2ea049557b7eb104
I1123_L2_DELTA_CANDIDATE_BLOB=2e14870263f9b833628b06f1b5a27a48bc285e1e
I1123_DAG_DELTA_CANDIDATE_BLOB=faf3bffffcf2d4e6a74faad5535a15ac9e7725f4
V411_ADOPTION_SOURCE_BLOB=a8c2d7a01a3610d9444d17df614ec6cacf58b67e
V411_COMPAT_SOURCE_BLOB=15e355f6ec86370599f2dda7b61963d93fead66f
ACTUAL_V412_RELEASE_QUALIFIED=NO
I1119_SCOPE_MIGRATION_APPROVED=NO
PRODUCT_SUCCESSOR_FREEZE=NOT_RECORDED
L2_SUCCESSOR_FREEZE=NOT_RECORDED
DAG_SUCCESSOR_FREEZE=NOT_RECORDED
PROJECT_UPDATES_PERFORMED=0
```

## 1. Finding — yes, but two independent delivery classes

The #1119 issue requests:

**Class A: protocol compatibility and immutable version resolution (standards contract).**
- Distinguish ADS **qualified release identity** (version + immutable commit/tree) from the **normative/protocol semantic compatibility profile** (schemas, events, Claim CAS, Review/Release authority, actor/behavior, consumer).
- An adopter may **opt in** to `TRACK_LATEST_COMPATIBLE_STABLE` as a selection preference; *each actual Task/Claim/Review/Version Release still consumes an immutable qualified `.dev-standard/VERSION` exact SHA*. Never use mutable `main/latest` as an execution authority.
- Classify compatibility per current `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` (blob `15e355f6...`): compare baseline/candidate exact source and all *material* wire, source, behavioral, operator/admission, Review/Release/consumer dimensions. `UNKNOWN` or `PROTOCOL_BREAK` never means auto-eligible. The v4.11 #1122 and v4.12 proposed #1123 self-declared-actor behavior difference must be assessed even if event schema is unchanged.
- Current `PROJECT_ADOPTION.md` (blob `a8c2d7a...`) mandates a real immutable `.dev-standard/VERSION` source identity and explicitly prohibits raw `main/latest` resolution. Extend it **prospectively**, not by deleting this hard floor.
- Preserve existing project pins and old recorded Gate/Task evidence. An opt-in policy controls only *future admitted work or new version checkpoints*, not an in-flight Claim.

**Class B: proactive multi-repo updater (actually acting GitHub automation).**
- Discover genuinely **opted-in, accessible** consumer projects; check their actual `.dev-standard/VERSION`, `AGENTS.md`, `PROJECT_OVERRIDES`, relevant immutable adoption authority, current issue/claim states and GitHub API permissions.
- On a **RELEASE_QUALIFIED** compatible ADS release, prepare a minimal source-bound project PR for a new exact pin plus only ADS-owned generated guidance; no direct writes to frozen Product/L2/DAG, consumer source/overrides, active Claims or protected main. No account-as-Agent inference.
- Do not merge unreviewed PR, fabricate permission, assume default auto-merge or bypass project CI/branch rules. Activation is checkpoint-safe; retain rollback old/new pin and compatibility proof. There is no need for a registry/daemon or project-wide Release Gate.
- To claim this class **implemented**, it needs an actual updater/resolver executable or connected workflow with at least one real permitted opt-in project dry-run and (if authorized) actual project PR; a prose rule alone is **not** updater delivery.

## 2. Product options and recommendation

| Option | v4.12 deliverable | What stays v4.13 | DAG consequence | Tradeoff |
|---|---|---|---|---|
| **A — Recommended fast v4.12** | **Class A fully**, plus bounded read-only/manual/shadow candidate lookup, compatibility record, next-checkpoint adoption rule, precise positive/negative conformance. Preserve immutable pin. | **Class B automatic GitHub updater** and continuous adopter fleet management | Fit with existing S04 `PROJECT_ADOPTION` + S05 conformance; S01 actor/Claim source already handled by #1123. No new Builder Task *if* source-audited write sets suffice; otherwise explicit bounded amendment. | Fast release, no fake automation, unlocks later safer per-project updates. |
| **B — Full #1119 in v4.12** | Class A **and** real opt-in discovery/resolver and bounded GitHub PR updater, activation/rollback plus observed real reference implementation | Generalized fleet UI/daemon/auto-merge remain optional, not core | Existing S04 documentation and S05 common verifier alone **cannot implement cross-repo updater**. At least one **separate substantive implementation concern** (e.g. S07 with exact code/CLI/workflow own files) and an actual L2/DAG amendment may be justified. | Larger v4.12 change / more critical-path work; no legitimate release before upstream v4.11, and project side effects demand actual permission/readback. |

**Recommendation:** For ADS's standards/specification v4.12 core, take **Option A** and keep #1119's updater Class B assigned to a single future implementable v4.13 concern. #1123 already introduces a behavior-level protocol migration and v4.12 frozen material needs its scoped successor review. Adding cross-repository mutating execution to the same release increases blast radius and makes v4.12 engineering schedule less predictable. A project consumer may opt into safe shadow/manual resolution with exact pins in v4.12 but it is **not automatically updated by ADS**.

If the user prefers complete automation immediately, Option B is technically feasible. Be explicit that a genuine updater/CLI/workflow and non-overlapping Task concern is needed; do not merely add `auto_update=true` to S04 prose and call #1119 DONE.

## 3. Minimal v4.12 Option A scope if accepted

- Product: a **delta to pending #1123 Product R4 candidate** (or bounded R5 successor if R4 is already reviewed/frozen at admission time) for “release version vs protocol/behavior compatibility profile” and opt-in resolution; no original R3 freeze rewrite.
- L2: add only Class A immutable `RELEASE_QUALIFIED` resolution, material compatibility dimensions and old/new pin currentness to the existing unfrozen #1123 L2 R6 delta before its Freeze when legally allowed; no second compatibility service. Producer/consumer subset and human scope may be declared in versioned adoption config without reinterpreting an event schema as policy truth.
- Task DAG: **S04** owns `standards/PROJECT_ADOPTION.md` + candidate adoption template/protocol selection; **S05** owns exact constrained compatibility-record verifier/test/manifest registration *if genuinely needed*. `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` is a distinct existing semantic source owner: make it **read-only if already sufficient**, otherwise record exact bounded write-set amendment, never silently write it via S04. `S01` (actor/Claim owner), S02/S03 and Release S06 remain unchanged.
- Negative tests: (1) same semver/different SHA not treated identical; (2) schema-compatible but policy/actor/Review change material→NOT_AUTO; (3) nonqualified release and mutable `main/latest` rejected; (4) live Task remains bound to old pin; (5) default `PINNED/MANUAL` no automatic update; (6) opt-in and exact fully evidenced compatible new release yields **candidate proposal** rather than in-flight source mutation; (7) unknown project permissions or source scope means `BLOCKED/UNKNOWN`, not PASS; (8) old frozen candidates unaffected; (9) **no v4.12 release gate requiring actual adopter update**.
- Validation: source-first reuse current v4.11 PROJECT_ADOPTION/compatibility-record rules; one bounded pair of new/mature project *source-pinned* fixture inputs (reuse S03 where actually applicable); actual resolver outputs if implemented, no credential/account-as-Agent inference, no false “already updated” statement.

## 4. Stop and authorization conditions

- **No automatic project GitHub writes now.** #1119 is still v4.13 intake, and its Issue target should not be changed by asking whether moving it is possible.
- Scope migration needs explicit user selection of Option A (partial scoped migration) or B (full move), because they deliver materially different end states. For A, #1119 stays **OPEN** for proactive update Class B; use a linked v4.12 scoped acceptance record rather than falsely closing all of #1119.
- Actual Product/L2/DAG successor edits/freeze are separate from this feasibility document. For the already user-approved #1123 successor: Product R4 blob `847e707b...`, L2 R6 blob `2e148702...`, DAG R4 blob `faf3bfff...` are still **not frozen**. Any #1119 inclusion must update their exact candidate sources and downstream Pack source pins accordingly, or create their own later lawful successor if already frozen.
- v4.11 V01/V02 candidate is not a qualified predecessor until V03/V04/R01/R02 are actually complete. v4.12 S01–S05 cannot write normative version source from old-main Draft PR #1101 or counterfeit native Issue Dependencies/CAS Claims.
- Preserve legitimate project branch protections/privileges, actual evidence, and logical self-declared actors. Don't impose extra Owner credential audits merely to verify an ADS pin, and don't replace project user authorization with blind automation.

```ini
RECOMMENDED_CHOICE=OPTION_A_CLASS_A_STANDARDS_SCOPE_IN_V412_CLASS_B_REAL_UPDATER_V413
FULL_I1119_IN_V412=TECHNICALLY_FEASIBLE_REQUIRES_GENUINE_UPDATER_CONCERN
IMPLEMENTATION_ADMISSION=NO
FREEZE=NOT_RECORDED
```
