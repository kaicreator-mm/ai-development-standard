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
