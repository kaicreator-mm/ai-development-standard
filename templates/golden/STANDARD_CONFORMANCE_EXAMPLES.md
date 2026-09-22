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

## development-workflow

**Golden:** Frozen PRD → L2 evidence/freeze → Task DAG → materialized Task Issues/dependencies → implementation/validation/review → version closure.

**Forbidden:** Skipping upstream authority by letting implementation tasks redefine product/architecture semantics or treating PR PASS as Release PASS.

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

**Golden:** Tests are selected by contract/risk, include negative cases where material, and report only what actually executed.

**Forbidden:** Claiming coverage from tests that were skipped/unavailable or using only happy-path tests for failure-sensitive behavior.

**Why:** Test evidence must be bounded and truthful.

## test-data-and-scenario-standard

**Golden:** Test data/scenarios declare provenance, represent normal/boundary/adversarial cases, avoid production secrets/PII and are reviewed when they influence product conclusions.

**Forbidden:** Using opaque fabricated fixtures as if they were production facts or leaking sensitive production data into tests.

**Why:** Scenario evidence strength and safety must be explicit.

## validation-standard

**Golden:** Validation binds artifact/code identity + environment/profile + procedure + result, and HEAD drift invalidates applicability to the successor identity.

**Forbidden:** Moving a PASS result to a new SHA by assertion or representing PASS only as a label.

**Why:** Validation truth is exact-identity evidence.
