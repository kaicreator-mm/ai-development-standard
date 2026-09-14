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

## Required Commands

- Bootstrap: `<command>`
- Format: `<command>`
- Lint: `<command>`
- Typecheck: `<command>`
- Unit: `<command>`
- Contract: `<command>`
- Integration: `<command>`
- E2E / Critical Journey: `<command>`
- Hidden Validation: `<command>`
- Production Build / Package: `<command>`

Use `NOT_APPLICABLE` for a category that genuinely does not apply. Do not invent placeholder commands in an adopted project.

## Runtime / Platform Requirements

- Supported OS/platform: `<...>`
- Required services: `<db / queue / object storage / external sandbox / ...>`
- Required SDK/toolchain: `<...>`

## Project-specific Hard Boundaries

- `<rule>`

## Required Release Gates

- `<gate>`

## Ownership / Sensitive Areas

- `<path or concern → owner/review rule>`

Project overrides may specialize the global standard but must not weaken its hard requirements on truthfulness, validation evidence, frozen product semantics or release claims.
