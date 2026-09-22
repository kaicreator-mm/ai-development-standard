# T-012 — Canonical GitHub Work Item Contract, Version DAG, Metadata and Golden Templates

Issue: #66
Depends on: T-011 / #64 / PR #65
Integration target: `version/v3.4.0`
Review Policy: `required`
Validation scope: `concern`
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal

Make v3.4 multi-Agent execution recoverable and deterministic by standardizing Version DAG authority, Issue contracts, metadata/state vocabulary, durable prompt semantics, and Golden/Forbidden examples.

## Required outputs

- `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`
- `standards/GOLDEN_TEMPLATE_STANDARD.md`
- Golden index + anti-pattern library
- type-specific Issue/DAG templates for missing v3.4 critical surfaces
- focused machine regression
- alignment with interaction/workflow/documentation standards
- additive v3.4 planning/closure bookkeeping

## Acceptance

See Issue #66. In particular, no live Markdown DAG state authority, no Agent-invented workflow synonyms, no Gate-result labels, no hidden chat task contract, and no normative execution surface without positive/negative conformance guidance.

## Completion

Full required validation + required Fresh Independent Review + merge after T-011 into `version/v3.4.0`; then T-010 performs fresh version closure.
