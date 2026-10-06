# Project Overrides

## Project Identity

- Repository: `<owner/repo>`
- Product / Service: `<name>`
- Standard revision: read `.dev-standard/VERSION`

## Structure Profile

- Repository profile: `<single-service | monorepo | library | cli | desktop | mobile | other>`
- Main modules: `<paths>`
- Intentional deviations from `PROJECT_STRUCTURE.md`:
  - `<deviation + reason>`

## Integration / GitHub Execution Profile

- Integration mode: `<version-branch | trunk-fast-path>`
- Version integration branch pattern: `<version/vX.Y.Z | NOT_APPLICABLE>`
- Issue-based execution DAG: `<enabled | disabled + reason>`
- Task Issue template/profile: `<canonical | project-specific path>`
- Stacked PR policy: `<allowed only for real code-baseline dependency | disabled | stricter project rule>`

When Issue-based execution is enabled:

- Frozen Task DAG remains the planning checkpoint.
- GitHub Issue Dependencies are the canonical live execution DAG.
- Sub-issues express hierarchy, not implicit blocking.
- Stacked PR MUST NOT replace Issue Dependency.
- JIT branch rule: task branches are created after dependencies merge, from the current integration exact SHA (exceptions only for real stacked code dependency).

## v4.1 Execution Foundation Profile

This profile declares project-level applicability/defaults for v4.1 execution concerns. It configures discovery and expected evidence; it does **not** create a second workflow or weaken Frozen Product/Architecture/Task/Validation/Release authority.

Recommended fields:

- `execution_foundation.profile`: `<materiality-driven | strict | project-specific>`
- `execution_foundation.dependency_toolchain`: `<applicable | NOT_APPLICABLE — reason>`
- `execution_foundation.git_execution`: `<applicable | NOT_APPLICABLE — reason>`
- `execution_foundation.configuration_secrets`: `<applicable | NOT_APPLICABLE — reason>`
- `execution_foundation.workspace_artifact`: `<applicable | NOT_APPLICABLE — reason>`
- `execution_foundation.external_systems`: `<applicable | NOT_APPLICABLE — reason>`
- `execution_foundation.execution_context`: `<when-material | always | NOT_APPLICABLE — reason>`

Rules:

- Material concerns resolve to their pinned normative owners; these fields do not redefine semantics.
- `Execution Context` is non-authoritative and SHOULD be instantiated only when material durable cross-Agent evidence/context exchange adds value.
- Minimal/Fast Path changes MUST NOT be forced to generate empty/non-applicable machine records merely because the project pins v4.1.
- Project authority MAY strengthen requirements, but MUST NOT turn a material concern into `NOT_APPLICABLE` merely to bypass evidence.
- Dependency/toolchain local availability is not repository requirement authority.
- Secret values MUST NOT be stored in ordinary durable context/evidence; use authorized secret refs/identity.
- Workspace file existence does not promote build/cache/runtime state into Validation or Release artifacts.
- External mock/sandbox/read-only evidence MUST NOT be escalated to unexecuted higher-fidelity/side-effect PASS.
- Credential/tool availability does not grant external side-effect authority.
- See `docs/implementation/4.1.0/MIGRATION_ADOPTION.md` in the pinned standard for adoption examples and owner mapping.

## v4 Adoption / Compatibility Profile

Adoption level controls how much v4 implementation machinery this project uses. It does **not** reduce the mandatory truth/authority floor.

Choose exactly one:

```text
A0_COMPATIBILITY
A1_MANUAL_PROTOCOL
A2_MACHINE_CONTRACTS
A3_DERIVED_AUTOMATION
A4_FULL_ORCHESTRATION
```

Canonical project fields:

- `v4.adoption_level`: `<A0_COMPATIBILITY | A1_MANUAL_PROTOCOL | A2_MACHINE_CONTRACTS | A3_DERIVED_AUTOMATION | A4_FULL_ORCHESTRATION>`
- `v4.compatibility_mode`: `<v3.4-bridge | native-v4 | project-specific + reason>`
- `v4.assurance.default`: `<manual-minimum | machine-checked | project-specific stronger default>`
- `v4.model_diversity.default_basis`: `<none | provider-diverse | model-family-diverse | architecture-system-diverse | configuration-fingerprint | project-specific>`
- `v4.interchange`: `<disabled | enabled + transport; authority must remain CORRELATION_ONLY_NON_AUTHORITATIVE>`
- `v4.reducer`: `<disabled | enabled + durable fact source>`
- `v4.controllers`: `<disabled | enabled + bounded owned concerns>`
- `v4.fast_path`: `<disabled | canonical | canonical + stricter project disqualifiers>`

Level semantics:

- `A0_COMPATIBILITY`: v4 pin + v3.4-compatible durable execution; v4 machine records/reducer/controllers are not required.
- `A1_MANUAL_PROTOCOL`: A0 + durable Operation/Assurance concepts recorded manually.
- `A2_MACHINE_CONTRACTS`: A1 + schema/semantic verification for adopted v4 records.
- `A3_DERIVED_AUTOMATION`: A2 + reducer/queue/routing/controller-derived state from durable facts.
- `A4_FULL_ORCHESTRATION`: A3 + project-selected full Operation/Assurance/Interchange/controller automation.

Non-weakening rules:

- Project overrides **MUST NOT weaken** any higher-authority required Review, Validation tuple, Candidate Freeze, Release Qualification or Repository Integration requirement.
- `v4.assurance.default` and `v4.model_diversity.default_basis` are defaults only when Frozen PRD/Architecture/Task authority has not already required something stronger.
- Model/reviewer agreement never becomes executable Validation truth.
- `v4.interchange` is correlation/transport only; it never owns lifecycle, Validation, Candidate or Release truth.
- `v4.reducer` / `v4.controllers` may derive routing and dispatch state but cannot manufacture owning facts.
- Disabling reducer/controllers is valid at A0/A1/A2 only if required gates still have a truthful manual/fallback execution path; otherwise the project is `BLOCKED`.
- `v4.fast_path` may be disabled or strengthened, but canonical v4 disqualifiers MUST NOT be removed.
- A low adoption level is not evidence that a Task is low-risk or Fast Path eligible.
- Exact-SHA/current-subject binding remains mandatory; branch/latest/chat identity cannot replace it.
- `NOT_RUN`, `BLOCKED` and `NOT_APPLICABLE` retain their standard meanings; do not rewrite an unavailable required gate as `NOT_APPLICABLE` merely to obtain green state.
- Candidate PREPARED != FROZEN; PR PASS != Release PASS; Release READY != Repository Integration complete at every adoption level.

Migration guidance:

- Existing v3.4 projects SHOULD begin at the smallest truthful level (usually A0/A1) and move upward only when the corresponding mechanisms really execute.
- Historical v3.4 evidence keeps its original subject identity and status; migration MUST NOT relabel old PASS/FAIL/CHANGES_REQUESTED as v4-produced evidence.
- `ai-dev:event:v2` remains valid; v4 adoption does not require event-v3.
- See pinned `standards/PROJECT_ADOPTION.md` and `docs/implementation/4.0.0/MIGRATION_ADOPTION_GUIDE.md` for the compatibility matrix and examples.

## Evolution Governance Profile (v4.2, materiality-driven)

This profile selects project defaults/applicability for v4.2 evolution concerns. It is not a second compatibility/migration owner and it does not grant mutation, Validation, Release or Deployment authority.

- `evolution.compatibility`: `<materiality-driven | always-evaluate | project-specific stronger rule>`
- `evolution.compatibility_window`: `<project policy/ref | determined per material change>`
- `evolution.migration`: `<materiality-driven | always-evaluate | project-specific stronger rule>`
- `evolution.runtime_evidence`: `<required when material | stricter project rule>`

Rules:

- Projects MAY strengthen when compatibility/migration analysis is required, but project defaults **MUST NOT weaken** Frozen Product/Architecture/Task authority or the pinned Interface/Compatibility and Data/Migration owners.
- Fast Path/non-material changes need not create empty Compatibility or Migration records; a material contract or persistent-state transition MUST NOT be hidden as non-applicable to avoid evidence.
- Compatibility window/runtime requirements come from project/domain facts and the owning standards, not from whichever tool/runtime an Agent happens to have installed.
- Historical evidence keeps its original exact subject; adoption MUST NOT retroactively relabel old evidence as proof for a new candidate, consumer window, state transition or runtime.
- Testing, Validation and Release remain their existing authorities. v4.4 Deployment remains the rollout/result owner when Deployment is applicable; compatibility/migration evidence does not imply Deployment success.
- Machine-contract availability, manifest/Golden discovery and technical necessity do not grant Task Pack mutation authority.

## v4.4 Delivery Applicability Profile (materiality-driven; optional concerns)

These fields identify project-owned delivery applicability and evidence locations; they are not new workflow states and do not make all four stages mandatory. For applicable stages, declare the actual product/project authority and exact platform or environment Validation tuples where material. Select each concern independently:

- `v4.delivery.build`: `<REQUIRED | CONDITIONAL + materiality predicate | NOT_APPLICABLE + truthful rationale>`
- `v4.delivery.packaging`: `<REQUIRED + actual format/installation tuple | CONDITIONAL + materiality predicate | NOT_APPLICABLE + truthful rationale>`
- `v4.delivery.distribution`: `<REQUIRED + publication system | CONDITIONAL + materiality predicate | NOT_APPLICABLE + truthful rationale>`
- `v4.delivery.deployment`: `<REQUIRED + exact environment/side-effect authority | CONDITIONAL + materiality predicate | NOT_APPLICABLE + truthful rationale>`
- Material exact immutable artifact identity / source-profile-toolchain refs: `<owning Build & Artifact refs or NOT_APPLICABLE — reason>`
- Applicable distribution publication/binding evidence refs: `<owned evidence refs or NOT_RUN/BLOCKED with reason or NOT_APPLICABLE — reason>`
- Applicable Deployment Plan and executed Result refs: `<separate owned refs or NOT_RUN/BLOCKED with reason or NOT_APPLICABLE — reason>`
- Applicable non-container package/install and real environment Validation tuples: `<actual tested platform × runtime/toolchain × profile or NOT_RUN/BLOCKED with reason>`

Rules:

- Build & Artifact owns exact source/profile/toolchain/output and separate promotion to immutable artifact identity. Distribution owns publication; its alias/tag is only a locator. Deployment owns an exact Plan and an independently observed Result for exact artifact/environment/side-effect authorization. Release qualification stays with its own authority.
- Project overrides MUST NOT weaken Frozen Product/Architecture/Task, applicable package-content security rules, any required exact-subject Validation/Review or Release Qualification.
- `NOT_APPLICABLE` is permitted only when a concern is genuinely non-material (for example no publication for an internal source-only tool, no deployment for a library); missing required tooling/external registry/production access must remain `NOT_RUN` or `BLOCKED`, not fabricated N/A.
- Fast Path may avoid empty delivery records only when changes truly do not materially affect the corresponding stage; material rebuilt bytes, required publication or target deployment cannot inherit historical PASS from matching version/tag/alias text.
- Build succeeded != artifact promoted; artifact published != Deployment succeeded; Deployment Plan exists != executed Result; staging/mock succeeded != production succeeded; Release READY != Deployment SUCCESS.
- The v4 adoption A0–A4 setting controls automation depth, not delivery applicability and not the truth floor. See pinned `standards/PROJECT_ADOPTION.md`, `standards/BUILD_ARTIFACT_GOVERNANCE_STANDARD.md`, `standards/DISTRIBUTION_GOVERNANCE_STANDARD.md`, and `standards/DEPLOYMENT_GOVERNANCE_STANDARD.md`.

### v4.5 Operations / Incident / Maintenance applicability (independent axes)

For projects pinning v4.5+, declare **each** axis independently; do not equate A0–A4 adoption level or repository profile with applicability. These describe project-specific *scope* and implementation evidence, not a global Operations machine or a new mandatory gate.

- `v4.runtime`: `<APPLICABLE — authority / subject / environment / evidence source / execution status | NOT_APPLICABLE — affirmative non-materiality rationale | NOT_RUN — required assessment or execution pending | BLOCKED — required authority/prerequisite unavailable>`
- `v4.incident`: `<APPLICABLE — authority / incident and feedback owner / safe evidence route / execution status | NOT_APPLICABLE — affirmative non-materiality rationale | NOT_RUN — required assessment or execution pending | BLOCKED — required authority/prerequisite unavailable>`
- `v4.maintenance`: `<APPLICABLE — authority / support line / baseline / backport-result validation policy / execution status | NOT_APPLICABLE — affirmative non-materiality rationale | NOT_RUN — required assessment or execution pending | BLOCKED — required authority/prerequisite unavailable>`

`APPLICABLE` is a scope declaration **not** a PASS: specify separate real execution state (`NOT_RUN`, `BLOCKED` or exact-subject evidence with its owning result) for every required activity. An unknown required runtime obligation MUST remain `NOT_RUN/BLOCKED`, never default to `NOT_APPLICABLE`. Non-deployed libraries MAY truthfully set runtime/incident `NOT_APPLICABLE` with concrete reasons, while maintenance/support may still apply. Conversely a deployed service cannot treat missing telemetry as health or `NOT_APPLICABLE` where observation is required. Do not retrofit historical Release/incident/support facts. For owner documents, T01 schemas, migration matrix and negative examples see the pinned `docs/implementation/4.5.0/MIGRATION_ADOPTION.md` and manifest; existing Testing, Test Data, Validation and Release owners remain authoritative.

## v4.6 AI-native / Agentic Governance Profile

This profile is **materiality-driven**. It does not require projects to manufacture empty Intent/Assumption or Skill records for work where those records are not material, and it does not change the A0–A4 adoption level.

Canonical project fields:

- `v4.ai_native.intent_assumption`: `<materiality-driven | always-record + project reason | project-specific stronger policy>`
- `v4.ai_native.context_currentness`: `<canonical | project-specific stricter live-reread policy>`
- `v4.ai_native.skill_admission`: `<disabled | materiality-driven | project-specific stronger admission/evaluation policy>`
- `v4.ai_native.durable_truth_surface`: `<GitHub/repository refs | project-specific durable owner surfaces>`

Rules:

- `standards/INTENT_ASSUMPTION_GOVERNANCE_STANDARD.md`, `standards/CONTEXT_ENGINEERING_STANDARD.md`, and `standards/SKILL_PROCEDURE_GOVERNANCE_STANDARD.md` are the three v4.6 normative AI-native owners. Project overrides may specialize allowed defaults but MUST NOT weaken their hard constraints.
- Material interpretation, assumption, UNKNOWN, promotion and contradiction handling use the Intent/Assumption owner and `schemas/intent-assumption-record-v1.schema.json` when a durable machine record is needed. Record shape never creates Product/Architecture/Task authority.
- Context currentness uses durable owner references and live rereads; do not create a project-local Context Snapshot/database as a substitute for current authority.
- Skill admission is required only when reusable procedure governance is material. Installed/discoverable Skill != trusted Skill, tool capability != side-effect authority, and Skill instructions never override current Product/Architecture/Task/Validation/Release authority.
- Assurance/Review, F0–F3, Dispatch/Handoff, Validation and Release remain owned by their existing standards/contracts. Use `references/AI_NATIVE_EXISTING_OWNER_INTEGRATION.md` for the v4.6 cross-owner map instead of copying those semantics here.
- Fast Path reduces ceremony, not truth. It does **not** require empty Intent/Assumption or Skill records when those concerns are genuinely non-material; material unresolved authority/currentness still fails closed.
- Historical evidence is not retrofitted with v4.6 records or relabeled as newly produced v4.6 evidence.
- This profile does not introduce a repository-wide v4.7 resolver, a second autonomy vocabulary, or parallel Review/Validation/Release state.

Migration guidance: see `docs/implementation/4.6.0/MIGRATION_ADOPTION.md` after the project pins a v4.6 revision.


### v4.7 Convergence Discovery (non-authoritative wiring)

For projects pinned to v4.7+, these are discovery/read surfaces only:

- Canonical owner discovery: `standard-manifest.json#semantic_authorities`
- Qualified state/non-inference discovery when applicable: `registries/state-dimensions-v1.json`
- Derived read routing helper when useful: `scripts/resolve_standard_read_set.py`
- Migration/adoption delta: `docs/implementation/4.7.0/MIGRATION_ADOPTION.md`
- Incompatible future-major planning input: `docs/implementation/4.7.0/FUTURE_MAJOR_REGISTER.md`

Rules:

- These are discovery/read surfaces only and MUST NOT grant mutation, Validation, Review, Closure, or Release authority.
- Resolve/read the canonical owner before acting; compatibility aliases remain compatibility routes, not owners.
- Load optional v4.7 registries/profiles only when they are applicable to the concern; their presence is not a project adoption requirement.
- Fast Path proportionality remains intact: do not force unrelated optional registries/profiles/packs/automation merely because v4.7 contains them.
- An incompatible path/schema/authority change goes to `docs/implementation/4.7.0/FUTURE_MAJOR_REGISTER.md` unless separate current authority explicitly allows it.


### v4.8 Convergence Discovery (non-authoritative wiring)

For projects pinned to v4.8+, these are discovery/read surfaces only:

- Canonical owner discovery: `standard-manifest.json#semantic_authorities`
- Qualified state/non-inference discovery when applicable: `registries/state-dimensions-v1.json`
- Derived read routing helper when useful: `scripts/resolve_standard_read_set.py`
- v4.8 registration/adoption map (non-authoritative): `references/V48_REGISTRY_ADOPTION_REFERENCE.md`
- Migration/adoption delta: `docs/implementation/4.8.0/MIGRATION_ADOPTION.md`
- v4.7 lineage migration/adoption delta (recovered, non-authoritative): `docs/implementation/4.7.0/MIGRATION_ADOPTION.md`
- v4.7 lineage future-major planning input (recovered, non-authoritative): `docs/implementation/4.7.0/FUTURE_MAJOR_REGISTER.md`

Rules:

- These are discovery/read surfaces only and MUST NOT grant mutation, Validation, Review, Closure, or Release authority; `authority_effect=NONE`, `gate_effect=NONE`, `mutation_authorized=false`.
- Resolve/read the canonical owner before acting; compatibility aliases remain compatibility routes, not owners.
- Load optional v4.8 registries/profiles only when they are applicable to the concern; their presence is not a project adoption requirement.
- Fast Path proportionality remains intact: `TASK_LEARNING=NONE_MATERIAL` is a valid complete outcome; do not force unrelated optional registries/profiles/packs/automation merely because v4.8 contains them.
- An incompatible path/schema/authority change is next-major planning input and MUST NOT be silently absorbed into the v4.8 pin unless separate current authority explicitly allows it.

## Execution Pack / Pull Worker Profile (v3.4, optional)

Opt-in; Fast Path projects MAY keep everything disabled.

- execution_pack.enabled: `<true | false>`
- execution_pack.path: `<.agent/execution/ | project-specific>`
- execution_pack.retention: `<durable | transient | full-provenance>`
- execution_pack.package_exclusion: `<packaging rule keeping .agent/ out of shipped artifacts>`
- pull_worker.builder: `<enabled + operator convention | disabled>`
- pull_worker.validator: `<enabled + operator convention | disabled>`
- pull_worker.reviewer: `<enabled + operator convention | disabled>`
- validation_queue.enabled: `<true | false>`
- validation_queue.scope: `<version | project | NOT_APPLICABLE>`
- local_first.enabled: `<true | false>` (default loop per `CI_EXECUTION_STANDARD.md` §10a)

Rules:

- Execution Pack is subordinate to Task Pack; it narrows freedom, never redefines authority.
- A version-scoped validation queue is a projection of Validator dispatches, never a second workflow authority.
- Disabling these capabilities does not weaken any required gate.

## Agent / Operator Attribution Profile

GitHub account identity is transport provenance only. When multiple Web sessions, Local Agents, CI runners or humans may write through the same GitHub account, use `ai-dev:event:v2` logical operator attribution.

Canonical fields:

```text
actor_role
operator_kind
operator_id
session_ref
transport_actor
```

Project conventions:

- Event schema for new events: `<ai-dev:event:v2 | stricter project rule>`
- Operator ID convention: `<kind>:<project-local-id>`
- ChatGPT Web operator examples: `<chatgpt-web:web-a | chatgpt-web:web-b | project-specific>`
- Local Agent operator examples: `<codex:ubuntu-build-01 | claude-code:windows-01 | project-specific>`
- Session reference convention: `<non-secret alias / run id>`
- Transport actor convention: `<github:<account> | project-specific>`
- Role claim policy: `<ROLE_CLAIMED for substantial/concurrent work | custom>`

Rules:

- Role and operator are separate dimensions. The same operator may perform different roles over time.
- `operator_id/session_ref` SHOULD distinguish concurrent ChatGPT Web pages or Local Agent runs even when `transport_actor` is identical.
- Dynamic operator/session IDs SHOULD NOT be encoded as GitHub labels.
- `executor:*` labels are routing hints and do not prove which concrete operator performed an event.
- Required Independent Review must be attributable to a context independent from the Builder context; the same GitHub transport account is allowed.
- Identity fields MUST NOT contain tokens, cookies, signed URLs, credentials or secrets.

## Independent Review Profile

Independent Review is risk-based by default; it is not universally mandatory for every Task/Fix PR.

Choose the project default profile:

```text
risk-based
always
custom
```

- Review profile: `<risk-based | always | custom>`
- Default Task Review Policy under `risk-based`: `<recommended>`
- `required` triggers: `<security/auth | public API/schema/migration | cross-service contract | concurrency/data integrity | high-risk/release-blocker | project-specific>`
- `not-required` examples: `<docs-only | mechanical/generated | low-risk local change | project-specific>`
- Allowed reviewer sources: `<fresh ChatGPT session | human | Codex/Claude reviewer | other>`
- Exact-SHA re-review policy when review is performed: `<standard default | stricter rule>`
- Review queue metadata override: `<state:review-ready etc. | canonical>`

Task/PR policy values are:

```text
required
recommended
not-required
```

Portable label mapping when labels are used:

```text
review:required
review:recommended
review:not-required
```

Rules:

- `required` is a real merge gate and requires PASS on the current merge-candidate SHA.
- `recommended` is optional; if skipped, record the decision/rationale. Review Gate may remain `NOT_RUN` without blocking merge.
- `not-required` means no Review Gate for that concern; use `NOT_APPLICABLE`.
- A project MAY strengthen review rules globally or for sensitive paths/concerns.
- A Task MUST NOT silently downgrade a higher-authority `required` review rule.
- Review is not a substitute for required Validation.

## Validation Execution Profile

Declare the real environments that execute validation:

- Linux validation: `<Ubuntu Build Host | other | NOT_RUN/BLOCKED>`
- Windows validation: `<Windows workstation/build host | NOT_RUN/BLOCKED>`
- macOS validation: `<real macOS host | NOT_RUN/BLOCKED>`
- Other real environment/device: `<...>`

Required validation tuples, when applicable:

```text
<platform> × <runtime/toolchain> × <validation profile>
```

One tuple PASS never implies another tuple PASS. Cross-build is not real platform execution unless the frozen project contract explicitly says otherwise.

## CI Profile

Choose exactly one:

```text
minimal
custom
disabled
```

- CI profile: `<minimal | custom | disabled>`
- CI checks (for `custom`): `<checks>`
- Disabled reason (for `disabled`): `<reason | NOT_APPLICABLE when enabled>`
- Exact-SHA clean-validation fallback: `<policy>`

Default `minimal` CI should remain low-cost and deterministic: project/standard verifier, format/lint/typecheck subset, fast unit/contract smoke, basic build smoke. Do not default full platform matrices, Critical Journeys, Hidden Validation, expensive E2E or packaging into CI.

CI being disabled does not automatically make Independent Review required; Review follows the Review Profile and Task Review Policy.

## CI Execution Profile

Interpret provider-specific workflow syntax only after declaring the real execution model. Follow `standards/CI_EXECUTION_STANDARD.md` from the pinned standard revision.

- CI provider: `<woodpecker | github-actions | gitlab-ci | jenkins | other | NOT_APPLICABLE — reason>`
- CI backend / execution model: `<local | container | hosted-vm | kubernetes | shell | other | NOT_APPLICABLE — reason>`
- CI runner role: `<ubuntu-build-host | windows-build-host | hosted-runner | other | NOT_APPLICABLE — reason>`
- Workflow config: `<repository path | provider-managed identity | NOT_APPLICABLE — reason>`
- Workflow config source: `<pr-head | merge-ref | base-branch | provider-snapshot | other | NOT_APPLICABLE — reason>`
- Execution shell / entrypoint model: `<host shell/path | container entrypoint | provider-managed | NOT_APPLICABLE — reason>`
- Runtime source: `<host-managed | container-image | setup-action/toolcache | other | NOT_APPLICABLE — reason>`
- Clone / checkout model: `<provider default | local plugin | explicit settings | other | NOT_APPLICABLE — reason>`
- Partial clone policy: `<enabled + reason | disabled | provider default | NOT_APPLICABLE — reason>`
- Submodule policy: `<enabled + reason | disabled | provider default | NOT_APPLICABLE — reason>`
- Git LFS policy: `<enabled + reason | disabled | provider default | NOT_APPLICABLE — reason>`
- Fresh-run / rerun policy: `<new exact SHA requires fresh run; rerun only proves its own run subject | stricter project rule | NOT_APPLICABLE — reason>`

Rules:

- Provider/backend semantics are part of the execution contract; do not assume `image`, plugin, service or volume semantics from another backend.
- For host/local backends, verify the host runtime/toolchain before dependency install and tests.
- For a new source SHA, evidence must come from a run whose tested subject resolves to that SHA; restarting an older pipeline does not validate the new HEAD.
- Provider-specific executable paths may be declared here when they are real project/runner facts, but they are not portable global defaults.
- Do not place CI secrets, registration tokens, credentials, cookies or signed URLs in this file.
- If `CI profile: disabled`, CI execution fields may be `NOT_APPLICABLE — <reason>`; the exact-SHA clean-validation fallback still applies.

## Required Commands

- Bootstrap: `<command>`
- Format: `<command>`
- Lint: `<command>`
- Typecheck: `<command>`
- Unit: `<command>`
- Contract: `<command>`
- Integration: `<command>`
- Critical Journey: `<command>`
- Hidden Validation: `<command>`
- Production Build / Package: `<command or NOT_APPLICABLE/NOT_RUN/BLOCKED>`

For an adopted project, replace placeholders with truthful executable commands or explicit states:

- `NOT_RUN — <reason>` when the gate applies but has not been executed / its runner is not yet established;
- `BLOCKED — <reason>` when prerequisites, permission, tooling, environment or a standard defect prevents completion;
- `NOT_APPLICABLE — <reason>` only when the category genuinely does not apply.

Do not invent placeholder commands, and do not use `NOT_APPLICABLE` to hide a required-but-unestablished gate.

## Runtime / Platform Requirements

- Supported OS/platform: `<...>`
- Required runtime/toolchain versions: `<...>`
- Required services: `<db / queue / object storage / external sandbox / ...>`
- Required SDK/device: `<...>`

## Project-specific Hard Boundaries

- `<rule>`

## Required Release Gates

List only gates with a real authority source. Recommended format:

```text
- <gate> — authority: <Frozen PRD / Architecture / Project Override / Task / Standard default>
```

Historical workflows, old scripts or obsolete artifacts do not automatically create mandatory release gates.

## Ownership / Sensitive Areas

- `<path or concern → owner/review rule>`

Project overrides may specialize the global standard but must not weaken its hard requirements on truthfulness, required exact-SHA Validation evidence, frozen product semantics or release claims. When Review is required by project/task authority, its exact-SHA evidence is also mandatory.
