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
- Disabled reason (for `disabled`): `<reason>`
- Exact-SHA clean-validation fallback: `<policy>`

Default `minimal` CI should remain low-cost and deterministic: project/standard verifier, format/lint/typecheck subset, fast unit/contract smoke, basic build smoke. Do not default full platform matrices, Critical Journeys, Hidden Validation, expensive E2E or packaging into CI.

CI being disabled does not automatically make Independent Review required; Review follows the Review Profile and Task Review Policy.

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
