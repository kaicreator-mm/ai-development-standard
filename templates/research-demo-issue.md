# Research Demo Issue Template

## Purpose / Architecture UNKNOWN

<What important architecture fact is still unknown?>

## Falsifiable Hypothesis

```text
If <precondition/input/crash window>,
then <observable behavior>,
and <counter/state/effect identity> must equal <expected value>.
```

## Why executable evidence is needed

<Why source/docs/static analysis are insufficient.>

## Frozen inputs

- PRD / Scope: `<path@sha>`
- Architecture candidate / ADR: `<path@sha>`
- Pinned standard: `<version@sha>`

## Fixed baseline / branch

- Baseline SHA: `<40-char-sha>`
- Research branch: `research_<name>`
- Integration rule: research evidence only; do not merge blindly into production.

## Dependencies / consumed exact SHAs

- `<issue/branch>@<sha>`

## Evidence strength

`E1 | E2 | E3`

Reason: <why this level is sufficient/required>

## Real Under Test

- <component/boundary that MUST be real>

## Deterministic Fakes

- <unrelated dependency that may be fake>

## In scope

- ...

## Out of scope

- production rewrite
- unrelated feature work
- ...

## Observable measurements

- `<counter/state/digest>`
- ...

## Executable scenarios

### S1 — positive

- Given:
- Execute:
- Expected observable evidence:

### S2 — boundary

- Given:
- Execute:
- Expected observable evidence:

### S3 — negative / fail closed

- Given:
- Execute:
- Expected observable evidence:

### S4 — failure / recovery（if applicable）

- Given:
- Execute:
- Expected observable evidence:

## Required environment

- runtime/toolchain:
- platform/Build Host:
- persistence/process/device requirements:

## Allowed changes

Prefer:

- `tests/architecture-*/**`
- `docs/experiments/**`
- research fixtures/reference examples

## Forbidden changes

- silent production runtime rewrite
- frozen product/contract changes
- unrelated features
- weakening tests/gates to obtain PASS

If a production seam is missing, document it and create a separate follow-up Issue rather than expanding scope.

## Required validation

- focused executable tests
- exact-SHA clean/repository CI where applicable
- E2/E3 integration/environment evidence as declared above
- all negative/failure scenarios

## Closeout

Use `templates/research-demo-report.md`.

Before closing, record:

- final exact research HEAD;
- commands / environment;
- PASS | FAIL | BLOCKED;
- What was proven;
- What was NOT proven;
- KEEP / ADAPT / DROP;
- architecture implication;
- reusable reference artifacts;
- production seams/follow-up Issues.

Completion is **Evidence complete**, not Feature complete.
