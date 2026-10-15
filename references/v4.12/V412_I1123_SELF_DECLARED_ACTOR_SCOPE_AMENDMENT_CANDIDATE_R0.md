# ADS v4.12 — #1123 Self-Declared Actor / Owner-Credential Scope Amendment Candidate R0

> **NON-NORMATIVE, NOT FROZEN, NOT DISPATCHABLE.** Decision packet for moving the genuinely missing parts of [Issue #1123](https://github.com/kaicreator-mm/ai-development-standard/issues/1123) from the v4.13 intake to a **bounded prospective v4.12 successor scope**. This document neither changes nor secretly overrides the already Frozen v4.12 Product R3, L2 R5, Task DAG R3, nor approves any Actor/Release Gate. No new Task Issue, independent Owner service or unverified validation is created.

## 1. Source-first facts — avoid repeating v4.11 work

1. **#1122 already landed on the v4.11 version branch** through PR #1125, implementing self-declared actor/role/session attribution for the ADS **standards repository**. Current `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` blob `b3f1191b2ee0c469e9b425d2336d4adbc47d6ede` §5/§7/§8.1.1 uses **declared** `actor_role/operator_kind/operator_id/session_ref`, not GitHub author identity or separately credential-verified sessions. §8.1.1 still rejects raw/quoted event text that was never admitted as a canonical event. `standards/RELEASE_STANDARD.md` blob `da82aa7d387d8f190c4ddff88b4c8782af804ac4` §11.7 accepts the declared Release process executor for the **ADS standards-only release**, with real production-human effect proof explicitly **NOT_PROVEN**. Do not do #1122 again.
2. Current v4.11 `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §11 (blob `846158b95e4173182a258f49847e1fde6600baec`) still correctly demands objective **single writer / CAS generation / actual current Task/Claim** for concurrent execution. This does not prove a human's identity and should not be removed by #1123.
3. `standards/ASSURANCE_PLAN_STANDARD.md` §§9–10 (blob `ddc39f2843e7af4b41b1cf2e6b34675c23bcb614`) uses `CURRENT_OWNER_AUTHORITY` and `OWNER_PERMISSION` to distinguish **semantic rule ownership and authorized proof of lowering a required assurance floor**. Merely renaming/removing the word Owner can make existing material gates disappear; this must be classified by predicate, not deleted en masse. Any *credential check that merely authenticates the person/agent* is separately removable under #1123.
4. PR #1124 is an **OPEN DRAFT based on historical `main`**, touching just `AGENTS.md`, Interaction and independent-review prompt. Its proposed self-declared identity language overlaps code already merged by #1122. It **does not** implement the complete #1123 release/assurance/work-item migration and must not be merged/cherry-picked blindly into the v4.12 implementation lineage.
5. Frozen v4.12 inputs are Product R3 blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`, L2 R5 blob `68608ef6456334d627db1797ba2e023233c84ce7`, Task DAG blob `adc9e522f3b734a59898091945b9c7545530565a` (User-approved Freeze at `7949caf630edbe83d1dff1ffb7cee8906b77c56f`). Their original product policy still preserves real security/protected human/result proof. **Full #1123 protocol re-scope is not presently authorized** by these exact Frozen subjects.
6. Five *unfrozen* Task Pack candidates already exist; only their **self-declared operator oracles** in S01/S05 have been corrected to cite v4.11 actual #1122 semantics, without touching Frozen Product/L2/DAG. The Pack/index static contract work is **not** normative implementation or a Review PASS.

## 2. Proposed v4.12 Product successor delta (requires explicit owning disposition)

**Delta P-1123 — Honest execution attribution without operator credential suspicion, with objective engineering truth.**

- **Logical actor attribution:** `actor_role/operator_kind/operator_id/session_ref` supplied by each execution context is trusted *as declared* on admitted canonical work events. `transport_actor` is merely GitHub/API transport metadata. No user-login comparison, org-membership lookup, real-person/signature check, cross-session proof, Owner-permission-to-act identity review or additional delegated Owner credential gate is imposed by ADS's **normal development workflow**. Do not demand a fresh physical Session just to establish declaration authenticity.
- **Reviewer/Validator/Release:** when relevant Review is selected, its own canonical result and exact subject still matter. Self-declared different logical contexts can satisfy identity attribution and declared-context independence, including through one shared GitHub account; do not let mere self-declaration also assert `PASS`, an executed test, or a native GitHub approval. The ADS standards-only Release process reuses v4.11 §11.7 instead of demanding an Owner signature.
- **Semantic authorities are not human Owners:** `owner` in standard-manifest semantic authorities, Product/Architecture contract precedence, assurance floor, release gate applicability and policy source refs can name **which normative contract owns the decision**. A source-current objective proof or required assurance predicate is **not** an operator-identity credential gate. Keep source-based precedence and technical proof; remove only actor-authentication/Owner-identity admission checks. Classify every removal with an exact current owner clause and observed intended effect.
- **Objective safeguards unchanged:** actual canonical event origin vs raw embedded quotation, Task/Claim currentness and CAS serialization, Allowed/Forbidden file scope, immutable source refs, Review Policy, real executed test/negative oracle, secrets/privacy, approval/effect results, and mandatory Release gates. A declared human Role is not evidence that a real external API granted authorization or that a genuine participant consent/irreversible-action DENY was performed. Preserve explicit `NOT_PROVEN/NOT_RUN` for downstream deployments.
- **Compatibility:** publish an explicit prospective protocol/behavior compatibility decision for consumers; keep their existing immutable ADS pins and past Gate facts. A changed actor-admission semantics can be **protocol breaking** even if event-v2 schema validates unchanged. Neither v4.11 nor earlier v4.12 Frozen objects are overwritten; no retroactive PASS.

**Product negative oracles:** (P1) same GitHub account, two distinctly **declared** logical actors ⇒ accepted context attribution without extra identity challenges; (P2) different GitHub accounts but same declared operator/session ⇒ not inferred to be different; (P3) required Review with no admitted canonical result / wrong SHA ⇒ still NOT_RUN/BLOCKED; (P4) fabricated PASS, missing actual CAS, competing writer or secret leakage ⇒ reject for objective cause; (P5) Source Owner semantic `OWNER_PERMISSION` cannot be dropped to make an unproven material gate disappear; (P6) historical REQUIRED_NOW on an already frozen subject cannot be reclassified by a newer rule; (P7) external native GitHub protection cannot be satisfied by a fictional second GitHub approver.

## 3. Prospective bounded owner / Task mapping — do not create a new sixth Builder Task unless shown necessary

| Concern | Proposed existing owner | Prospective source boundary | Actual admission |
|---|---|---|---|
| Self-declared actor, Review and Claim | **S01** | Existing Workflow / Work Item / Interaction; **only proven remaining** EXECUTION_ARCHITECTURE credential checks, AGENTS or review prompt (requires explicit amended S01 write-set) | S01 Task Pack + frozen DAG write-scope amendment first |
| Adoption/migration and human/transport distinction | **S04** | Existing `PROJECT_ADOPTION` and bounded examples, exact pin/protocol compatibility without false automatic upgrades | Product/L2 contract and Task Pack amendment |
| Assurance/Release identity vs semantic owner | **S01** contract author with **S06** existing Release authority accepting applicability; S05 deterministic integration owner | `ASSURANCE_PLAN_STANDARD` / `RELEASE_STANDARD` only the exact actor-credential clause if actually present (currently **not** in frozen S01/S05 write sets); existing semantic proof floor remains. S06 does not become a Builder Task | Explicit source-owner write-set / L2 currentness / Release acceptance, no silent owner transfer |
| Schema, scripts, currentness/negative regression, Golden/manifest/CI | **S05** | Existing shared `schemas/**`, `scripts/verify_standard.py` / manifest/Golden/CI under actually amended exact allowed paths; per-concern focused tests placed with the proper owner | Actual native Task/Claim after predecessor qualified; no invented execution PASS |

**Frozen DAG impact:** same five implementation Tasks and four genuine Task dependencies can **probably** carry the requested minimal subject, but new files `EXECUTION_ARCHITECTURE_STANDARD.md`, `ASSURANCE_PLAN_STANDARD.md`, `RELEASE_STANDARD.md`, `AGENTS.md` and review prompt are currently **outside the S01/S05 frozen write sets**. An owner must approve **a bounded DAG successor/amendment and changed Pack scopes** before dispatch. If source audit reveals distinct high-risk independent work with unsafe overlapping writer ownership, a narrowly split concern may be necessary—do not claim a new Issue is automatically needed just because a file exists.

## 4. Minimum lawful path and stop rules

1. **Owner-selected target**: explicitly accept moving the **not-yet-covered substantive #1123 scope** into v4.12. #1123 can remain the provenance/issue number; **do not simultaneously run conflicting v4.13 and v4.12 implementations**. Leave #1119 rolling compatible adoption future design separate; annotate any new protocol-compatibility requirement.
2. **Single Product Delta + affected L2 Delta + affected DAG/Task Pack amendment**, each with explicit exact subject/approval under original version policy. Reuse the already verified v4.11 #1122 Product/Review/source evidence; only substantively changed higher-authority assertions get selected focused Review. No repeated full v4.12 PRD/L2 audits without a novel failure class.
3. **One existing-integration targeted test battery**: check current v4.11 source and scripts first, retain all existing passing/required technical oracles, add only gaps, no new login/Owner-credential engine. Reuse actual exact evidence; execute a version-candidate regression once on the qualified candidate when eligible.
4. **No implementation until actual predecessor Release Qualification and Task/Claim**: as of the inspected state, v4.11 V01/V02 closed but V03 Hidden / V04 Fresh / R01 Release Qualification / R02 main integration are still pending. Historic `main` or PR #1124 draft is not a lawful v4.12 implementation base.
5. **Hard stop:** if supporting Owner changes would weaken genuine mandatory evidence or runtime security, return `SCOPE_CONFLICT` to Product/L2 for an explicit compatibility/assurance disposition; never transform missing real proof to PASS and never turn operator trust into implicit authorization for effects.

## 5. Status

```ini
SOURCE_ISSUE=#1123_V413_CURRENTLY_OPEN
PROPOSED_TARGET=v4.12_SCOPED_SUCCESSOR_NOT_YET_APPROVED
USER_INTEREST=ASKED_IF_V412_POSSIBLE_2026_10_15
V411_I1122=MERGED_NORMATIVE_SOURCE_REUSED
PR1124=OPEN_DRAFT_NONQUALIFIED_HISTORIC_MAIN
FROZEN_PRODUCT_R3=UNCHANGED
FROZEN_L2_R5=UNCHANGED
FROZEN_TASK_DAG_R3=UNCHANGED
TASK_PACK_S01_S05=REBASED_AUTHOR_DRAFT_ONLY
FORMAL_V412_PRODUCT_DELTA_FREEZE=NOT_RECORDED
FORMAL_V412_L2_DELTA_FREEZE=NOT_RECORDED
FORMAL_V412_DAG_AMENDMENT=NOT_RECORDED
NATIVE_TASK_ADMISSION=NOT_RUN
NORMATIVE_V412_IDENTITY_SOURCE_IMPLEMENTATION=NOT_RUN
V412_RELEASE=NOT_QUALIFIED
```
