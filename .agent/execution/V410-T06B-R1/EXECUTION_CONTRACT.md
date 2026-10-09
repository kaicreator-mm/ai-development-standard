# V410-T06B R1 execution contract — central projection & machine conformance wiring

Exact base: `ab8339f83a6a2308a5aa39009bd126698320ceee` (tree `4664b02ab36f3181a567c88fc0756079d2397343`), current `version/v4.10.0` tip = PR #925 merge (V410-T06A R2).
Task: #861. Execution environment: LOCAL. Branch: `task/v4.10.0-v410-t06b-machine-projection`.
Frozen authorities: Product #837, L2 #842, refined DAG #848, Task Pack R1 §V410-T06B, #861 WEB|LOCAL bounded refinement (canonical dimensions + semantics 1-8 + additive machine-contract direction). All predecessors durably DONE (see MANIFEST `dependency_completion`).

## Goal (Task Pack)

Project the settled owner semantics into machine/conformance surfaces **without creating authority**: shared projections match canonical owners; a stale passing verifier cannot override current authority; false prose enforcement claims are detected/dispositioned; positive and negative conformance coverage exists for material authority/currentness semantics; only materially affected shared surfaces change.

## Normative implementation order (from #861@6013678847 — binding, not advisory)

Stage 0 (this JIT, done): census + rebind + pack. Stages 1-6 execute under the Builder claim on the exact-current baseline:

- **Stage 1 — schemas (parallel-safe):**
  - W1 `schemas/dispatch.schema.json`: additive optional `execution_environment` enum `WEB|LOCAL`; `compatibility_group` string|null; `compatibility_authority_ref` string|null; `admission_generation` integer minimum 0|null; optional `scheduler_origin` enum `WEB|LOCAL` as request/writer provenance only (never key/authority input). allOf: non-default `compatibility_group` ⇒ `compatibility_authority_ref` required. Persisted `protected_claim_key` documented as audit-only provenance equal to the deterministic serialization (T1). `execution_profile` enum and profile↔role allOf couplings **byte-stable** (A11).
  - W2 `schemas/execution-state.schema.json`: additive `active_dispatches[]` row projection `{dispatch_id, role, execution_environment|null, compatibility_group(normalized), protected_claim_key(derived), claimed_by|null, exact subject refs}`; legacy singular fields retained; >1 active ⇒ singular MUST be null/omitted; stable sort by derived claim_key then dispatch_id; `NON_AUTHORITATIVE_DERIVED_STATE`.
  - W3 `schemas/agent-event-v2.schema.json`: **ZERO CHANGE required** (additiveProperties already admits lineage refs/scheduler_origin); OPTIONAL named properties `source_proposal_ref`/`canonical_admission_ref`/`scheduler_origin` — builder JIT decision, default to adding them explicitly for writer conformance (F3) since they are purely additive.
- **Stage 2 — prose (after Stage 1 field names settle):**
  - W4 `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §6/§11/§11.1/§11.2 additive paragraphs: derived 4-tuple protected key `(repository, task, role, normalize_group(compatibility_group))` replacing the coarse "(work item, role)"; non-default group requires durable higher-authority validation (authorize_non_default a-f); monotonic admission_generation CAS (reserve g→g+1, claim ==current, stale⇒STALE zero mutation, idempotent re-claim, terminal never decrements); multi-active visibility; scheduler checkpoint/proposal non-authority + terminal precedence (T5); stale-loser zero-canonical-mutation (T2).
  - W5 `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` §8.4/§8.5 writer guidance: explicit `__default__` serialization in `protected_claim_key` `repo#task:role:group` (revision/session ids never in slot 4, T1); durable `source_proposal_ref` (`#857@6010683815` form, never prose) + `canonical_admission_ref` on current admission+claim examples (T3); `execution_environment` canonical, `TARGET_ENVIRONMENT` marked proposal/history alias with fail-closed disagreement (T4; census: zero occurrences at base); losing-proposal `STALE|SUPERSEDED|REJECTED` disposition example (T2); disambiguation of event-v2 environment (validation-gate) and `operator_kind` (provider provenance) from dispatch `execution_environment` (A13; handoff schema hazard-1: its pre-existing `execution_environment` is the validation-gate environment, reconciled in prose).
  - W6 `templates/agent-event-comment.md`: writer examples mirroring W5 only.
- **Stage 3 — verifier helpers:**
  - W7 `scripts/v34_rules.py`: `normalize_group`; `derive_claim_key` + serialize/reparse roundtrip (fail-closed on reorder/mismatch/extra segment); `authorize_non_default` input check; generation/CAS conformance helper; multi-active projection helper; lineage-ref presence check for current writers; TARGET_ENVIRONMENT-vs-execution_environment agreement check; terminal-precedence reducer rule. `core_artifacts_complete()` **REUSED UNCHANGED**.
- **Stage 4 — tests:**
  - W8 NEW `scripts/test_v410_t06b_multi_dispatch_conformance.py`: oracle sections B,C,D,E,F,G,H + J frozen guards + dogfood T1-T5 worked negatives (FC-T1a..FC-T5). MUST register (W13).
  - W9 `scripts/test_protocol_schemas.py`: section A conformance A1-A13 (incl. A8 ENVIRONMENT_PROFILE_CONTRADICTION, A11 byte-stable couplings, A12 handoff-schema guard, A13 disambiguation).
  - W10 `scripts/test_execution_architecture.py`: extend the existing ClaimCell race oracle to keyed compatibility groups + scheduler-origin/environment/provider invariance (D1,D2,E3,G8); §11/§11.1 prose anchors only where W4 changed text.
  - W11 `scripts/test_v34_lifecycle_contracts.py`: I1-I6 core-inventory exact-set regressions (exact six PASS; missing/duplicate/legacy-core/superset ⇒ PACK_INVALID; historical packs readable).
  - W12 `test_v410_t02b_machine_projection.py` NOT edited (import/mirror only).
- **Stage 5 — registration/drift:**
  - W13 `scripts/verify_standard.py` + `standard-manifest.json`: register W8; drift-check tokens for new dispatch fields, event lineage provenance, active_dispatches, Pack exact-set in writer/template examples. **This stage also resolves the T06A-routed registry growth under one authorized mechanism**: add to `sections.verification` the new test file AND update `test_v48_registry_adoption`'s `AUTHORIZED_SECTION_ADDITIONS`/registry-count guard + manifest rows **together** (case-H evidence: guard+manifest moved together stays green; BASELINE_SECTIONS rewrite is RA-01-impossible), registering `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md` and updating the seven routed GAP rows + the T06A focused suite's zero-delta/coupled assertions **in the same authorized change**. NO_GREEN_BY_DELETION forbidden: v4.8 historical invariants/negative protection preserved.
- **Stage 6 — conditional writer examples:** W14 local-builder/local-validator/web-reviewer bootstrap + validation-handoff queue examples, only where current wording re-couples role/environment/profile (post-rebind inspection decides).

## Allowed write set (bounded)

`schemas/dispatch.schema.json`, `schemas/execution-state.schema.json`, `schemas/agent-event-v2.schema.json` (W3 optional), `standards/EXECUTION_ARCHITECTURE_STANDARD.md`, `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `templates/agent-event-comment.md`, `scripts/v34_rules.py`, NEW `scripts/test_v410_t06b_multi_dispatch_conformance.py`, `scripts/test_protocol_schemas.py`, `scripts/test_execution_architecture.py`, `scripts/test_v34_lifecycle_contracts.py`, `scripts/verify_standard.py`, `standard-manifest.json` (Stage 5 authorized growth incl. `test_v48_registry_adoption.py` guard evolution + T06A focused-suite conscious updates + GAP-row closure), W14 conditional template examples, plus this pack's artifacts. Anything else requires a new dispatch.

## Forbidden

No central semantic rewrite; no second registry/lifecycle/scheduler/gate family/claim family; no blanket touch-every-file migration; no silent weakening of `execution_profile` enum/couplings; no migration of historical durable events; no brand/model authority; no NO_GREEN_BY_DELETION; no merge by the Builder; no source mutation before the accepted `V410-T06B-BUILDER-R1` claim.

## Gate obligations

Repository verifier/schema/conformance suites (all carried suites green incl. `test_v48_registry_adoption` under its authorized evolution, `test_v410_t04b_review_currentness`, `test_v410_owner_convergence` under its conscious update), fresh exact-candidate LOCAL Concern Validation, genuinely Fresh WEB Independent Review on one unchanged HEAD/tree; then merge admission by the LOCAL merge controller. Review PASS is not Release PASS.
