# Research — <question>

## Contract

- Target version/topic: `<ref>`
- Type: `type:research`
- State: `<canonical state>`
- Risk: `<low|medium|high|critical>`
- Review Policy: `<required|recommended|not-required>`
- Research purpose: `PRODUCT_RESEARCH | ARCHITECTURE_RESEARCH`
- Selection basis: `<which existing/static evidence is insufficient for which pending decision>`

## Research Question

<falsifiable/bounded question>

## Lifecycle Binding

This template is a projection of `standards/DEVELOPMENT_WORKFLOW.md` Stage 1 and `standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md`. It owns no lifecycle semantics and adds no stage, gate or authority.

- `PRODUCT_RESEARCH` — Stage 1, **before** Product Freeze; informs the Draft PRD / Scope decision. Owner: the Product lifecycle in `standards/DEVELOPMENT_WORKFLOW.md`.
- `ARCHITECTURE_RESEARCH` — Stage 2, **after** Product Freeze; informs falsifiable architecture assumptions, with `templates/research-demo-issue.md` when executable evidence is required. Owner: `standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md`.
- A Research Issue MUST NOT be opened merely because a stage exists; selection is proportional (see below).
- This Issue produces evidence / independent judgment only. It is **not** Product or Architecture authority, it cannot produce Product Freeze, and it cannot be promoted by a Review `PASS`.
- Architecture Research MUST NOT be used before Product Freeze as product discovery. After Product Freeze, an infeasible or contradictory Product scope routes through the existing Product thaw/contradiction path instead.
- No second Research lifecycle/authority is created by this template.
- Decision relevance: `<which exact decision this evidence informs>`

## Proportionality / Not-Required Outcome

- Open a Research Issue only when existing/static evidence is insufficient for the pending decision, and keep scope proportional to that decision.
- When evidence is already sufficient and no higher-authority owner requires independent research, record the truthful outcome instead of opening an Issue:

```text
NO_RESEARCH_REQUIRED
decided_subject=<exact ref/sha or decision identity>
existing_evidence=<durable evidence identity that already covers it>
```

- `NO_RESEARCH_REQUIRED` / compact / inline is a truthful conclusion, not a waiver: applicable policy-required authority/evidence MUST NOT be skipped, and an equivalent existing evidence identity MUST be cited rather than assumed.
- Mandatory research ceremony is forbidden: no empty Issue, empty research branch or completeness checklist opened for appearance alone.
- Where selection applicability is UNKNOWN or contradictory, fail closed to authority/risk disposition instead of silently downgrading.

## Authority / Inputs

- owning requirement/architecture: `<ref>`
- source baseline(s): `<exact identity>`
- license/provenance requirements: `<requirements>`

## Scope

### In
- <item>

### Out
- <item>

## Evidence Requirements

- source spine: `<required>`
- executable evidence: `<required|not-applicable>`
- positive evidence: `<item>`
- negative/counter evidence: `<item>`

## Required Result

- findings
- KEEP / ADAPT / DROP or equivalent disposition when applicable
- ownership/adoption boundary
- what was proven
- what was NOT proven
- authority disposition: the owning Product or Architecture authority adopts or rejects this evidence; the Issue itself does not freeze, approve or widen scope

## Acceptance

- [ ] evidence identities are durable
- [ ] claims do not exceed evidence strength
- [ ] negative evidence is recorded
- [ ] follow-up work is materialized rather than hidden in chat
- [ ] research purpose is typed and its lifecycle position is legal (`PRODUCT_RESEARCH` before Product Freeze; `ARCHITECTURE_RESEARCH` after)
- [ ] proportionality recorded truthfully: selection basis, or `NO_RESEARCH_REQUIRED` with the existing evidence identity
- [ ] conclusion claims no Product Freeze or architecture-freeze authority
