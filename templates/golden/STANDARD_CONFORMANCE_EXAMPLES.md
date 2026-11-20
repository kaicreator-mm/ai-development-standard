# Standard-wide Golden Conformance Examples

Status: `ACTIVE`

This companion registry gives every active normative standard a concise positive example, forbidden example, and rationale. It supplements concrete templates indexed by `templates/GOLDEN_INDEX.md`.

## architecture-research-demo-standard

**Golden:** A material architecture UNKNOWN becomes a falsifiable hypothesis, isolated Research Demo Issue, exact evidence, bounded PASS/FAIL/BLOCKED conclusion, and explicit statement of what was not proven.

**Forbidden:** Treating a demo PASS as production/release readiness or silently merging exploratory code as production implementation.

**Why:** Research Demo owns bounded architecture evidence, not product implementation or release authority.

## chatgpt-web-role

**Golden:** ChatGPT Web materializes task-specific requirements in GitHub, then emits only `完成 owner/repo Issue #N。` for execution handoff.

**Forbidden:** Sending branch/SHA/scope/test/gate/closeout instructions only through chat.

**Why:** Chat is a workspace/invocation transport, not durable project state.

## ci-evidence-standard

**Golden:** CI evidence records provider/run/job, exact code identity, environment/capability, checks and bounded conclusion.

**Forbidden:** Calling a green CI badge complete Validation or Release PASS without the required evidence tuple.

**Why:** CI is execution evidence, not the whole validation/release authority.

## ci-execution-standard

**Golden:** Cheap deterministic checks run in the configured local/CI stage; expensive/platform truth runs only in the required environment and is routed as validation evidence.

**Forbidden:** Repeatedly using remote CI as the ordinary debugging loop when local execution is available, or fabricating unavailable platform PASS.

**Why:** Execution location and validation truth are separate concerns.

## ci-runner-capability-standard

**Golden:** A runner capability record names the actual runner/backend, supported tools/platforms and known limitations; validation is scheduled only where the profile is satisfiable.

**Forbidden:** Assuming a runner has a capability because another runner/provider has it.

**Why:** Environment capability must be explicit and reproducible.

## codex-handoff-protocol

**Golden:** Codex receives a durable Issue/handoff contract, reconstructs repository facts, executes only authorized scope and writes durable results back to GitHub.

**Forbidden:** A bespoke chat-only Codex prompt contains required task facts absent from GitHub.

**Why:** Handoff must survive a new executor/session.

## codex-role

**Golden:** Codex performs bounded implementation/real-host execution according to the assigned Issue and pinned standard, escalating architecture changes rather than silently deciding them.

**Forbidden:** Codex changes Frozen PRD/Architecture semantics because an implementation shortcut appears easier.

**Why:** Executor authority is bounded by frozen upstream authority.

## data-migration-governance-standard

**Golden:** A material persistent-state change binds exact source state A, target state B, transition identity, runtime/environment applicability and the evidence for upgrade/recovery. Fresh-B installation remains a distinct subject.

**Forbidden:** Treating `fresh install PASS` as upgrade PASS, treating `migration file exists` as migration execution, or reusing source/original evidence for a new result SHA/runtime without applicable evidence.

**Why:** Migration truth is directional and evidence-bearing. Presence, freshness, recovery and runtime applicability are separate dimensions; v4.2 does not own Deployment rollout/result semantics.

## development-workflow

**Golden:** Frozen PRD → L2 evidence/freeze → Task DAG → materialized Task Issues/dependencies → implementation/validation/review → version closure. On a material recurring or cross-component finding, route to the root-class owner and choose minimum sufficient correction by comparing a bounded local fix against the right contract/adapter/architecture repair level, and retain Review rounds under the same concern when lawful.

**Forbidden:** Skipping upstream authority by letting implementation tasks redefine product/architecture semantics or treating PR PASS as Release PASS. Choosing another tiny patch solely to preserve a stale DAG while the same cross-component root class keeps failing, or creating a new Task for every review checkpoint.

**Why:** Stage ownership and checkpoints prevent semantic drift.

## documentation-standard

**Golden:** One authoritative document owns a fact; secondary docs link/ summarize it and generated material is regenerated rather than manually forked.

**Forbidden:** Maintaining several divergent copies of the same contract/status across README, chat, agent files and docs.

**Why:** Documentation must reduce, not create, competing sources of truth.

## execution-architecture-standard

**Golden:** Durable GitHub facts are reduced into ready sets/dispatches; workers claim a role and controllers recompute after accepted events/merges.

**Forbidden:** Treating a queue/dashboard as an independent workflow authority or introducing separate state machines per role.

**Why:** Derived projections must remain reconstructible from one durable execution model.

## execution-pack-standard

**Golden:** A JIT Execution Pack is generated/bound to the exact executable base after dependencies are satisfied and remains subordinate to the frozen Task Pack.

**Forbidden:** Long-lived Execution Packs drift from the current base or redefine Task acceptance.

**Why:** Execution Packs are exact-base execution authority, not planning authority.

## github-agent-interaction-protocol

**Golden:** Issue body carries stable contract, metadata carries canonical current routing state, comments carry append-oriented events, and exact-SHA review/validation evidence is preserved.

**Forbidden:** Rewriting Issue body as an event log, using Agent identity labels, or treating stale labels as gate truth.

**Why:** GitHub objects have distinct responsibilities required for multi-Agent recovery.

## github-capability-fallback

**Golden:** When a connector cannot mutate a canonical GitHub object, the limitation is recorded explicitly and a defined fallback preserves semantics without claiming the native object exists.

**Forbidden:** Writing prose that pretends a native Issue Dependency/review/state mutation was created when capability was unavailable.

**Why:** Capability limitations must not corrupt durable truth.

## github-work-item-contract-standard

**Golden:** A substantial version has a frozen planning DAG, materialized Task Issues/native dependencies, exactly one canonical type/state/review policy where applicable, and derived state cards marked non-authoritative.

**Forbidden:** Agents invent workflow synonyms, carry two `state:*` values, or coordinate through a shared live Markdown status file.

**Why:** Shared canonical vocabulary and authority boundaries make multi-Agent routing deterministic.

## golden-template-standard

**Golden:** Every active normative standard has an entry in `STANDARD_COVERAGE.json` pointing to positive, forbidden and rationale guidance; artifact standards also provide concrete reusable templates where applicable.

**Forbidden:** Adding/changing a normative standard while leaving no maintained positive/negative conformance guidance.

**Why:** Agents otherwise infer incompatible local dialects.

## interface-compatibility-governance-standard

**Golden:** A material contract change binds exact contract/baseline/candidate identities, records the actual change operation and separately evaluates every material compatibility dimension for the supported consumer/window population.

**Forbidden:** Promoting `wire-safe` or schema/checker PASS into source/behavior/consumer compatibility, using new/new success to hide old/new breakage, or normalizing UNKNOWN/unexecuted dimensions to compatible.

**Why:** Compatibility is multi-dimensional and evidence-scoped. Generated artifacts and checkers are evidence, not the canonical contract or universal compatibility authority.

## issue-first-task-trigger

**Golden:** `完成 owner/repo Issue #N。`

**Forbidden:** A user-visible trigger repeats baseline SHA, branch rules, scope, commands, gates, review and closeout details.

**Why:** The Issue/referenced repository authority is the complete task contract; the trigger is only a pointer.

## local-agent-handoff-protocol

**Golden:** The handoff Issue is contract-complete before `HANDOFF_READY`; the local agent receives a pointer and loads pinned repository bootstrap/standard.

**Forbidden:** Marking handoff ready because a long external prompt fills fields missing from the Issue.

**Why:** Handoff completeness is a durable precondition, not a chat convention.

## model-usage-policy

**Golden:** Model capability/effort is matched to task risk and evidence needs while all models obey the same frozen authority and validation rules.

**Forbidden:** Using a stronger model as justification to skip evidence, review or authority boundaries.

**Why:** Model strength changes execution capability, not project truth.

## project-adoption

**Golden:** A project pins the standard revision, records explicit overrides, installs only the required adapters/templates and verifies conformance.

**Forbidden:** Copying the standard into a project and editing it locally without an explicit pin/override boundary.

**Why:** Adoption must preserve upstream standard authority and project-specific exceptions.

## project-structure

**Golden:** Project layout exposes clear entry points for code, docs, tests, standard pin/overrides and Agent instructions without duplicating global standard text.

**Forbidden:** Hiding authoritative contracts in tool-specific folders inaccessible to other Agents.

**Why:** Project structure must support cross-tool recovery.

## release-standard

**Golden:** Release Qualification evaluates the final exact candidate after required closure validation/review, then records immutable release identity and known limitations.

**Forbidden:** Promoting an earlier validated SHA after candidate drift or equating PR merge with Release PASS.

**Why:** Release authority applies to one exact qualified candidate.

## repository-standard

**Golden:** Repository branches/commits/PRs reflect isolated concerns and durable checkpoints, with main/version integration following the configured mode.

**Forbidden:** Long-lived ad-hoc branches or unrecorded baseline changes that make provenance unrecoverable.

**Why:** Repository topology is part of execution identity and auditability.

## testing-standard

**Golden:** Tests are selected by contract/risk, include negative cases where material, and report only what actually executed. For a material claimed suite, check actual discovered/executed test inventory; for material public features, exercise the selected runtime/consumer call path rather than merely loading its package.

**Forbidden:** Claiming coverage from tests that were skipped/unavailable or using only happy-path tests for failure-sensitive behavior. A green `npm test` excluding nested critical suites (DomainHarness #162), or declaring a selected extension functional because it was imported but never invoked (#1264).

**Why:** Test evidence must be bounded and truthful.

## test-data-and-scenario-standard

**Golden:** Test data/scenarios declare provenance, represent normal/boundary/adversarial cases, avoid production secrets/PII and are reviewed when they influence product conclusions.

**Forbidden:** Using opaque fabricated fixtures as if they were production facts or leaking sensitive production data into tests.

**Why:** Scenario evidence strength and safety must be explicit.

## validation-standard

**Golden:** Validation binds artifact/code identity + environment/profile + procedure + result, and HEAD drift invalidates applicability to the successor identity.

**Forbidden:** Moving a PASS result to a new SHA by assertion or representing PASS only as a label.

**Why:** Validation truth is exact-identity evidence.

## v417-shared-bounded-golden-pairs

Bounded v4.17 P03 shared pair pack (Task #1310): one language-neutral, source-only deterministic Golden/reference corpus of 14 positive/forbidden paired scenarios. This section is conformance guidance, not a new Gate, wire, registry row or runtime authority; the pair budget ≤14 is a planning target, not a universal numeric Gate. The executable finite oracle is `tests/test_v417_golden_consistency.py` (reused unchanged owners: `tests/v415_consumer_oracle.py`, `scripts/verify_github_structured_interaction.py` frozen v4/v5 schemas, v4.16 T03 reader bridge, T02 measurement reducer). All verdict labels below are analysis values, never wire enums or authority grants.

| Pair | Controlling source | Golden (positive) | Forbidden |
| --- | --- | --- | --- |
| G01 | GAIP §10 C08 metric-eligibility table | Source-owner approved causal A→B→A′ with both strategy-changing edges and owner-certified A′≡A yields `N_obs_pivot/D_obs_pivot=2/2`, `N_obs_revisit/D_obs_revisit=1/1`; proven non-return is a legitimate Revisit-negative | Mere code rollback, missing owner equivalence, missing middle state or an undecidable material comparison (absent/non-boolean `changed` on an accepted covered decision) ≠ observed outcome; they are UNKNOWN, excluded from N and D |
| G02 | GAIP §10 C08 epistemic lanes | One fixed labeler revision + feature/cohort yields distinctly `INFERRED` diagnostics (`D_inf/N_inf`) | Same features or a self-report cannot promote to OBSERVED; lanes/revisions/coverage are never pooled (`NOT_COMPARABLE`) |
| G03 | GAIP §10 C08 occurrence identity | A unique causal selection opportunity counts once; a distinct genuinely selected retry keeps its own occurrence | Duplicate delivery/re-read/late corrected copies double-count; unordered concurrent branches or missing intermediates are UNKNOWN, never negative or positive |
| G04 | GAIP §10 C08 publication/privacy + §16.7 reader pins | Cleared, owner-supported, profile-compatible public projection publishes bounded | Private/ungraded/unaccepted sources never become public OBSERVED/PASS/zero; a v4-only reader of v5 is UNSUPPORTED, not absence |
| G05 | GAIP §16.6–16.7 (C10) | Verified aligned `REVOKE`/`REDACT` withholds only NEW materially reliant decisions until requalified | A same-owner or foreign `DISPUTE` never revokes and withholds nothing by itself; unrelated qualified decisions proceed |
| G06 | GAIP §16.6 (C10) native identity contract | Native PR/Issue/Review/CI with canonical repo, immutable native object id + url, owner witness, witnessed sha-256 content snapshot (currentness), complete scoped readback and a consumer-local material-use edge qualifies a new dependent inference WITHOUT Report ID | Citation/existence alone ≠ consumption; missing native identity or a non-digest/stale snapshot never qualifies (no invented Report ID); fabricated Report fields on native objects are invalid; same-comment identity collisions stay CONFLICT |
| G07 | GAIP §16.5–16.7 + frozen v4.15/v4.16 Report schemas | Schema-exact v4 8-key correction target and v5 14-key target are each profile-correct; complete terminal readback qualifies CURRENT | v5-only keys in a v4 target (and missing v5 keys) are schema-invalid; wrong digest/owner ⇒ DISPUTED/UNKNOWN, never clean absence |
| G08 | GAIP §16.6–16.7 (C10) prospective boundary | A verified invalidating notice gates only future *reliant* choices; non-reliant new decisions and unrelated work proceed; historical BUILD/Host receipts stay byte-immutable | Retroactive undo of BUILD/Effect, globally blocking non-reliant or unrelated work, or rewriting accepted history is forbidden |
| G09 | EXECUTION_ARCHITECTURE_STANDARD §11 (claim/generation/lost-ACK fencing) + EXTERNAL_SYSTEM_EXECUTION_STANDARD | Fully authorized current Claim (scope, capability, valid credential) with a confirmed-safe effect may ACT once | Missing scope/capability, revoked credential or unconfirmed safety ⇒ ABSTAIN before any effect; lost ACK/503 ⇒ reconcile without replay; refusal after an unauthorized effect is UNAUTHORIZED_EFFECT, not abstention |
| G10 | DEVELOPMENT_WORKFLOW Stage 5–6 + VALIDATION_STANDARD §4/§6 + RELEASE_STANDARD | Two source targets passing locally AND previously-active obligations holding at the final current SHA give a cumulative PASS | Cross-target integration failure, SHA drift after validation (stale PASS), or a verdict sourced from hidden-oracle bytes — provenance-observed (`FAIL_ORACLE_LEAK`) — is never a PASS; hidden pack contents stay undisclosed even when a pack is supplied |
| G11 | EXECUTION_ARCHITECTURE_STANDARD §11.1 + TASK_DAG_GOVERNANCE_STANDARD §8 | Disjoint protected keys with no contract collision admit genuine parallel work | Shared-ABI version conflict, stale generation or overlapping generated index never silently merges |
| G12 | SKILL_PROCEDURE_GOVERNANCE_STANDARD §7 + VALIDATION_STANDARD | Matched pinned baseline/policy/model/environment/verifier with an independently witnessed clean holdout is comparable with declared coverage | Training-only gain, holdout contamination, an explicitly witnessed holdout/hidden-oracle leak (even with disjoint item IDs), hidden-oracle reuse or unmeasured regressions never promote |
| G13 | GAIP §16.6 feedback + §10 Level-3 phases (C09) | PRESENTED→APPLIED→INDEPENDENTLY_CHECKED advances only with each phase's own owner-witnessed source-qualified receipt and a genuinely independent nonempty verifier operator | Presented ≠ applied; applied ≠ independently checked; a missing/absent verifier operator is not independence; a transport login is neither an Agent identity nor an effect authority |
| G14 | GAIP §16.7 + v4.16 T02/T03 (C11+C12) | A supported reader path, deduplicated physical attempts, one comparable window and publishable clearance give a bounded comparable summary | v4-only reading v5 ⇒ UNSUPPORTED; estimated+billed double-count, guessed private provider routes, unknown attempts or wrong clearance never become comparable rates |
