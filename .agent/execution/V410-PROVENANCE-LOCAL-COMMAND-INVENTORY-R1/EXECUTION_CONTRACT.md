# V410 Provenance Remediation — Local Command Inventory R1 Execution Contract

Exact base: `30334e8c7b90a327f8597b86c88c785b98df07f7`.
Task Pack: Issue #900 (v4.10 provenance remediation campaign; audit #898, adjudication #899).
Execution environment: `LOCAL` (preparation unit; campaign execution environment per #900, with Fresh Review on WEB).

Purpose: current-state command inventory for re-executing the seven affected historical leaves #850/#851/#852/#853/#854/#855/#856 whose Builder execution used PACK_INVALID legacy-named Execution Packs. For each leaf, map original acceptance criteria to current integrated state and inventory the smallest actual checked-in deterministic concern evidence commands needed to re-establish current acceptance. This unit produces inventory and verification only; it executes no campaign evidence.

## Admission timing

Preparation MAY proceed now per #900 and has proceeded on base `30334e8c7b90a327f8597b86c88c785b98df07f7`. Campaign EXECUTION MUST wait until V410-T08A (#864) is integrated and the implementation DAG is dependency-complete, and MUST then bind to that exact integration SHA/tree. At preparation time #864 is OPEN; all campaign commands must be re-verified for entrypoint existence on the final exact subject.

## Allowed write set

This preparation unit may add only: `.agent/execution/V410-PROVENANCE-LOCAL-COMMAND-INVENTORY-R1/` artifacts and `scripts/test_v410_provenance_command_inventory.py`. Campaign execution adds only durable evidence/claim records under the canonical JIT campaign pack; no product/source mutation.

## Forbidden scope

No product/source mutation; no rewriting old claims/PRs or pretending the original mutation was conformant; no opportunistic repair — a material residual gap stops that unit and routes a bounded repair to its owning concern; no waiver invention; no Candidate Freeze / Release PASS claim; no Frozen DAG mutation merely to schedule the campaign.

## Provenance

Claim: the user dispatch for this preparation unit was recorded BEFORE any file mutation; this pack's write contract precedes its artifacts. For the campaign itself, a serialized Builder/remediation claim MUST be durably published before any campaign execution. For #854 specifically, the campaign proves only that the NEW execution is claim-before-execution; the historical `claim posted post-implementation` finding is retained verbatim and not repaired or rewritten.

## Gates

This unit's gate is `scripts/test_v410_provenance_command_inventory.py`; it binds HEAD to the preparation base (exactly, or as a descendant whose only drift is this unit's additive write set) and its verbatim PASS on this branch is recorded in `IMPLEMENTATION_MAP.md`. Campaign gates per #900: all seven units PASS on one exact subject; LOCAL Validator campaign with separate per-task verdict rows; genuinely fresh independent WEB Reviewer campaign with separate per-task verdicts plus campaign-provenance verification; subject drift supersedes affected gate evidence; historical Validation/Review PASS does not transfer.
