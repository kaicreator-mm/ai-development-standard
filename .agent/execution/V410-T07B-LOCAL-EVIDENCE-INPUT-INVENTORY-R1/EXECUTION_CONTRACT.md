# V410-T07B-LOCAL-EVIDENCE-INPUT-INVENTORY-R1 Execution Contract

Exact base: `30334e8c7b90a327f8597b86c88c785b98df07f7` (origin/version/v4.10.0 tip; current HEAD).
Task Pack: `docs/implementation/4.10.0/TASK_PACKS_R1.md#V410-T07B`.
Execution environment: `LOCAL` (user dispatch to zcode local agent; no network authority actions).
Branch: `task/v4.10.0-v410-t07b-local-evidence-input-inventory-r1`.
Parent Issue: `#863`.

## Purpose

Support — never decide — `ADS_CORE_FEATURE_FREEZE_ELIGIBLE=YES|NO` by inventorying the
evidence inputs a Product-authority freeze decision needs, per TASK_PACKS §V410-T07B:

- the Product-authority decision path is explicit (PRD §1.1, §19.4, §22 item 8);
- required evidence inputs are referenceable and reconstructible by a fresh observer;
- `NO` is a legitimate, evidence-backed outcome;
- Closure/Release READY/CI/Controller/Reviewer/model vote cannot manufacture `YES`.

This unit produces an inventory and a verification script only. It produces no verdict,
no release state, and no semantic mutation.

## Provenance — user dispatch claim (recorded BEFORE any file mutation)

Claim: the user dispatched this LOCAL preparation unit
`V410-T07B-LOCAL-EVIDENCE-INPUT-INVENTORY-R1` (parent Issue `#863`, agent_freedom
`F1_BOUNDED_IMPLEMENTATION`) with the exact base `30334e8c7b90a327f8597b86c88c785b98df07f7`
and the exact allowed write set below. This contract file is the first and only mutation
of the worktree for this pack; the acceptance claim of this dispatch is
`EVIDENCE_INPUT_INVENTORY` preparation only, not any freeze decision.

- Claim recorded at: 2026-10-06T15:41:00+06:30, before any other pack file or script existed.
- Claim scope: inventory + executable verification of the inventory's own internal consistency.
- Claim explicitly excludes: setting `ADS_CORE_FEATURE_FREEZE_ELIGIBLE`, touching any
  source/product document, and creating any release/closure/Hidden/RQ state.

## Allowed write set

1. `.agent/execution/V410-T07B-LOCAL-EVIDENCE-INPUT-INVENTORY-R1/` (new pack directory, seven files).
2. `scripts/test_v410_t07b_evidence_input_inventory.py` (new pure-stdlib verification script).

## Forbidden scope

- No new execution/release state dimension (no second Release verdict/state machine).
- No automatic `YES` from CI, Review, Release READY, Closure, Controller, Reviewer or model vote.
- No source/product semantic mutation; no edit to any pre-existing file.
- No implementation Task making the final Product decision; the decision stays with Product authority.
- No historical evidence transfer: every input is attributed to its exact subject at base_sha.

## Dependency state (T07B admission is gated on T07A)

- `V410-T07A` (Product acceptance / release-blocker evidence wiring) is **NOT integrated**
  at base `30334e8c7b90a327f8597b86c88c785b98df07f7`; no T07A commit exists on the branch.
- Integrated predecessors at base: T01A `df1ee51a0d6d1c30092c01102ca320db51091535`,
  T01B `3d735304f40064128554ff4dca24b45c37149f6b`,
  T02A `2276afe7fdd057f300386ab19925ae37a4065684`,
  T02B `fee097db238b60d97ab2d449dcf210488d03814f`,
  T03A `46fe74936cd88184bbd898643851b585d3299291`,
  T03B `98ccd07ee18f3a8a8f10e91e04295324ebb130d8`,
  T04A `41236cb7250c6854170563d371d7debe7354c936`,
  T05A-R3 `30334e8c7b90a327f8597b86c88c785b98df07f7` (HEAD).
- Pending notes: T06A/T06B (owner convergence/projection), T07A (acceptance wiring — direct
  admission dependency), T08A (integration) and V410-V01 (validation) are all PENDING at
  base_sha. This inventory marks them PENDING and never AVAILABLE.
- This pack is a local preparation unit; its PENDING markings are evidence-state facts at
  base_sha, not gates being waived.

## Authority statement

Only Product authority may set `ADS_CORE_FEATURE_FREEZE_ELIGIBLE=YES|NO`. CI green,
Review PASS, Release READY, Version Closure, Controller state, Reviewer judgment or model
votes are evidence inputs only and cannot manufacture `YES`. An evidence-backed `NO` is a
legitimate outcome of a successfully delivered v4.10.
