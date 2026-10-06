# V410-V01-LOCAL-CAPABILITY-MAP-R1 Execution Contract

Exact base: `30334e8c7b90a327f8597b86c88c785b98df07f7` (= `origin/version/v4.10.0` tip at dispatch).
Validation contract: `docs/implementation/4.10.0/V410_V01_VALIDATION_CONTRACT.md`.
Parent issue: `#865`. Branch: `task/v4.10.0-v410-v01-local-capability-map-r1`.
Execution environment: `LOCAL`.

## Purpose

Map each of V410-V01's 15 required validation subjects (read from
`docs/implementation/4.10.0/V410_V01_VALIDATION_CONTRACT.md` at this exact base) to
locally executable capabilities (commands, scripts, doc verifications) available at
`base_sha`, recording `PASS`/`BLOCKED` availability and limitations. This is validator-side
preparation only: it records what CAN be executed locally at real dispatch; it is NOT a
Validation execution and NOT a PASS of any kind.

## Dependency state (explicit)

`CANDIDATE_NOT_READY`. V410-V01's real validation subject is the dependency-complete
candidate after `V410-T08A` integration; that candidate does NOT exist at this base.
Integrated predecessors at this base:

- `V410-T01A@df1ee51a0d6d1c30092c01102ca320db51091535`
- `V410-T01B@f1daaffb6ae3469dc0e77e881ed73e17e6586295`
- `V410-T02A@2276afe7fdd057f300386ab19925ae37a4065684`
- `V410-T02B@fee097db238b60d97ab2d449dcf210488d03814f`
- `V410-T03A@46fe74936cd88184bbd898643851b585d3299291`
- `V410-T03B@98ccd07ee18f3a8a8f10e91e04295324ebb130d8`
- `V410-T04A@41236cb7250c6854170563d371d7debe7354c936`
- `V410-T05A@30334e8c7b90a327f8597b86c88c785b98df07f7` (R3, = base tip)

Pending: `V410-T04B`, `V410-T05B`, `V410-T06A`, `V410-T06B`, `V410-T07A`, `V410-T07B`,
`V410-T08A`. Real V01 execution MUST wait for the T08A-integrated exact candidate and
re-read every mapped input at that dispatch.

## Allowed write set

- `.agent/execution/V410-V01-LOCAL-CAPABILITY-MAP-R1/` (this pack: contract, manifest,
  capability map, matrices, checklist)
- `scripts/test_v410_v01_capability_map.py` (the map's own verification script)

## Forbidden scope

- The Validator never repairs, mutates, or semantically rewrites source; V01's
  implementation write set is NONE and this pack's write set is no wider than above.
- The Validator never fabricates Hidden / Release-Qualification / release verdicts.
- No self-certification: this pack confers no PASS on any subject, Task, PR, or release.
- No old-evidence transfer: historical Review/Validation evidence is non-authoritative
  input only and never transfers to a changed exact candidate.
- Where a subject requires real-host/GitHub-native facts (e.g. native Issue
  Dependencies, live PR/gate states), the local part may be recorded AVAILABLE while the
  host part is recorded BLOCKED with owner = GitHub platform; per the Validation
  contract, PASS is NEVER inferred from source inspection.
- No PRs, no issue comments, no pushes outside this branch.

## Provenance

Claim: this LOCAL preparation unit was dispatched by the user (controller) as
`V410-V01-LOCAL-CAPABILITY-MAP-R1` under parent Issue `#865`, recorded BEFORE any file
mutation in this worktree. This EXECUTION_CONTRACT.md is the first file written of this
pack and constitutes the serialized claim for the preparation unit only (not for V01
Validation itself, whose claim regime belongs to its real dispatch after T08A).
