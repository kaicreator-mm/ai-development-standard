# V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1 Execution Contract

Exact base: `30334e8c7b90a327f8597b86c88c785b98df07f7` (= `origin/version/v4.10.0` tip at dispatch).
Task Pack: `docs/implementation/4.10.0/TASK_PACKS_R1.md#V410-T07A`.
Execution environment: `LOCAL`.
Parent issue: `#862`.

## Provenance

**Claim recorded BEFORE any file mutation (this contract is the first file written of this pack):**

> User dispatch (zcode:local-dispatch), received 2026-10-06T15:40:06+06:30: execute LOCAL
> preparation unit `V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1` under parent Issue `#862`. Build a
> read-only evidence inventory that makes PRD §19 acceptance/release-blocker obligations
> reconstructible through existing owners at base SHA `30334e8c7b90a327f8597b86c88c785b98df07f7`,
> plus one verification script. No semantic mutation of any pre-existing file. Only additions
> under `.agent/execution/V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1/` and
> `scripts/test_v410_t07a_evidence_inventory.py` are allowed. Commit 1-3 conventional commits
> and push `-u origin HEAD`; no PRs, no issue comments.

This claim is durably published in this contract before the first implementation/evidence
mutation, per the T07A pack provenance rule (accepted serialized Builder claim against this
exact current pack MUST be published before first mutation).

## Dependency and currentness state at generation

- T07A admission is gated on `V410-T06B` per `TASK_PACKS_R1.md` (`dependencies=[V410-T06B]`).
- At base SHA `30334e8c7b90a327f8597b86c88c785b98df07f7` the following tasks are **NOT yet
  integrated** into `version/v4.10.0`: `V410-T04B`, `V410-T05B`, `V410-T06A`, `V410-T06B`,
  `V410-T07A` (this unit is a LOCAL preparation/inventory unit only), `V410-T07B`,
  `V410-T08A`, `V410-V01`.
- Integrated predecessors with exact SHAs (verify with `git merge-base --is-ancestor`):

```text
V410-T01A  = df1ee51 (merge commit on version/v4.10.0)
V410-T02A  = 2276afe (merge PR #879)
V410-T01B  = f1daaff (merge PR #880)
V410-T03A  = 46fe74936cd88184bbd898643851b585d3299291 (merge)
V410-T03B  = 98ccd07ee18f3a8a8f10e91e04295324ebb130d8 (merge)
V410-T02B-R2 = fee097d (merge PR #887)
V410-T04A  = 41236cb (merge PR #884)
V410-T05A-R3 = 30334e8c7b90a327f8597b86c88c785b98df07f7 (merge PR #902, = base tip)
```

- Consequence: every producer owned by a not-yet-integrated task is marked **PENDING** in
  `EVIDENCE_INVENTORY.md` with an explicit owning concern. No PASS is inferred for any PRD §19
  R-item whose acceptance evidence is owned by a pending task. This inventory is a
  reconstruction aid, not an acceptance verdict.

## Purpose

Make PRD §19 acceptance criteria and release blockers `R1,R2,R3,R4,R6,R7,R11,R12`
reconstructible through existing owners (per TASK_PACKS §V410-T07A), by mapping each
requirement to durable evidence producers that already exist at base SHA — merged PR numbers,
docs, verification scripts/commands, and `.agent` execution packs — while:

- keeping blockers visible without redefining Release authority;
- preserving exact candidate/currentness identity (base SHA, frozen PRD/L2/DAG blobs);
- ensuring historical qualification cannot silently bind to a successor (negative invariant
  recorded, enforcement tests owned by pending tasks stay PENDING);
- keeping Minimum and Advanced ADS evidence paths identifiable.

## Allowed write set

Additions only:

1. `.agent/execution/V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1/` — `EXECUTION_CONTRACT.md`
   (this file, written first), `MANIFEST.yaml`, `EVIDENCE_INVENTORY.md`, `TEST_MATRIX.yaml`,
   `FAILURE_MATRIX.yaml`, `IMPLEMENTATION_MAP.md`, `REVIEW_CHECKLIST.md`.
2. `scripts/test_v410_t07a_evidence_inventory.py` — pure-stdlib verification script.

## Forbidden scope

- No second Release verdict/state machine (Release authority stays with its existing owner).
- No Product requirement redefinition (PRD §18/§19 semantics are read-only input).
- No historical evidence transfer to successor candidates (negative invariant only).
- No source/product semantic mutation; no modification of any pre-existing file.
- No PRs, no issue comments, no touching other worktrees or the `main` clone.

## Verification

Run `python scripts/test_v410_t07a_evidence_inventory.py` from the worktree root; it must
print `EVIDENCE_INVENTORY_VERIFIED=PASS`. Verbatim output is recorded in
`IMPLEMENTATION_MAP.md`.
