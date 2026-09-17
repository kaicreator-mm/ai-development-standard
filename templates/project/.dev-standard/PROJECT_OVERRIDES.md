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

Version Branch Mode default is Independent Review required for every Task/Fix PR before merge to the version branch.

- Independent Review required: `<YES | project-authorized narrower exception>`
- Allowed reviewer sources: `<fresh ChatGPT session | human | Codex/Claude reviewer | other>`
- Exact-SHA re-review policy: `<standard default | stricter rule>`
- Review queue metadata override: `<state:review-ready etc. | canonical>`

A project MAY strengthen review rules. A narrower exception must identify its authority and scope; lack of CI, lack of a second human, or convenience alone is not an exception.

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
- Exact-SHA clean-validation fallback/review policy: `<policy>`

Default `minimal` CI should remain low-cost and deterministic: project/standard verifier, format/lint/typecheck subset, fast unit/contract smoke, basic build smoke. Do not default full platform matrices, Critical Journeys, Hidden Validation, expensive E2E or packaging into CI.

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

Project overrides may specialize the global standard but must not weaken its hard requirements on truthfulness, exact-SHA validation/review evidence, frozen product semantics or release claims.
