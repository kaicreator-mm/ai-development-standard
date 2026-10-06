# V410-V01-LOCAL-CAPABILITY-MAP-R1 Verification Record

Prepared unit execution evidence. This records the preparation pack's OWN verification
only. It is NOT a V410-V01 Validation result and confers no PASS on any subject, Task,
PR, or release (see `EXECUTION_CONTRACT.md`).

## Binding

- Unit: `V410-V01-LOCAL-CAPABILITY-MAP-R1` (parent Issue `#865`)
- Exact base: `30334e8c7b90a327f8597b86c88c785b98df07f7` (= `HEAD^` of this branch;
  merge-base with `origin/version/v4.10.0` at execution time)
- Branch: `task/v4.10.0-v410-v01-local-capability-map-r1`
- Executed at (UTC): `2026-10-06T09:35Z` — environment: Windows 10 (Git Bash),
  `git version 2.52.0.windows.1`, `Python 3.14.6`

## Procedure

1. Created a temporary local clone (`git clone --shared --no-checkout`) of this
   worktree, checked out detached at the exact base `30334e8c7b90a327f8597b86c88c785b98df07f7`.
   No resident repository's metadata was modified; the temp checkout lived only under
   the workspace `_tmp` scratch area and was discarded after the run.
2. Overlaid this pack (`.agent/execution/V410-V01-LOCAL-CAPABILITY-MAP-R1/`) and
   `scripts/test_v410_v01_capability_map.py` onto that base checkout — required because
   the verifier asserts `HEAD == base_sha`, and both files exist only in this pack
   commit, one commit above the base.
3. Ran `python scripts/test_v410_v01_capability_map.py` from the base checkout root
   (map-integrity gate), then every `required` command in `TEST_MATRIX.yaml` from the
   same base checkout root.
4. Host-scope commands (`gh ...`) were NOT executed — GitHub API was unreachable from
   this host during execution (TLS handshake timeout); host parts of subjects 4, 5, 13
   remain `BLOCKED` with owner = GitHub platform, exactly as recorded in the map.

## 1. Map integrity verifier — verbatim output

```
CAPABILITY_MAP_VERIFIED
BASE_SHA=30334e8c7b90a327f8597b86c88c785b98df07f7
HEAD=30334e8c7b90a327f8597b86c88c785b98df07f7
SUBJECTS_TOTAL=15
SUBJECTS_AVAILABLE=12
SUBJECTS_AVAILABLE_LOCAL_BLOCKED_HOST=3
SUBJECTS_BLOCKED=0
HOST_SCOPE_COMMANDS=RECORDED_NOT_EXECUTED
CANDIDATE_STATE=CANDIDATE_NOT_READY
NOTE=this verifies map integrity only; not a V410-V01 validation PASS
```

Exit code: `0`. All 15 contract subjects covered exactly once; every AVAILABLE local
command entrypoint exists at the exact base tree.

## 1b. Gate repair (R1, post-generation)

Section 1 was produced out-of-band (temp clone at the exact base with the pack overlaid)
because the verifier then required `HEAD == base_sha`, a condition that cannot hold at
this pack's own committed revision: the pack commit necessarily sits one commit above the
pinned base. A reviewer checking out this branch got FAIL, and the PASS existed only via
that reconstruction.

The verifier now asserts the campaign's binding rule instead: HEAD must equal the pinned
base, or descend from it with every changed path inside this unit's additive write set
(pack directory + `scripts/test_v410_v01_capability_map.py`). The descendant case confines
every difference from base to that write set, so every other path — including every
AVAILABLE command entrypoint this gate checks — is byte-identical to the base tree. The
gate is therefore runnable in-band and still proves the map was derived on the pinned base.

In-band run on this pack branch (verbatim, exit `0`):

```
CAPABILITY_MAP_VERIFIED
BASE_SHA=30334e8c7b90a327f8597b86c88c785b98df07f7
HEAD=c94d9ad2c1afda8edb3a8084eb13f46ab0b13179
HEAD_BINDING=descendant_additive_only
SUBJECTS_TOTAL=15
SUBJECTS_AVAILABLE=12
SUBJECTS_AVAILABLE_LOCAL_BLOCKED_HOST=3
SUBJECTS_BLOCKED=0
HOST_SCOPE_COMMANDS=RECORDED_NOT_EXECUTED
CANDIDATE_STATE=CANDIDATE_NOT_READY
NOTE=this verifies map integrity only; not a V410-V01 validation PASS
```

Subject counts are unchanged from the section 1 run (`15/12/3/0`), so no map claim
depended on the check that was repaired.

## 2. TEST_MATRIX capability commands — results

All commands run from the exact-base checkout root; every entry exited `0`:

| capability id | command | exit | result |
|---|---|---|---|
| capability_map_integrity | `python scripts/test_v410_v01_capability_map.py` | 0 | CAPABILITY_MAP_VERIFIED (above) |
| lifecycle_ordering_capability | `python scripts/test_v410_stage1_lifecycle_contracts.py` | 0 | 12 tests OK |
| pointer_only_trigger_capability | `python scripts/test_pointer_only_trigger_contract.py` | 0 | 10 tests OK |
| collaboration_control_capability | `python scripts/test_v410_t02a_collaboration_control.py` | 0 | 19 tests OK |
| implementation_quality_capability | `python scripts/test_v410_t03a_implementation_quality.py` | 0 | 12 tests OK |
| gate_repair_routing_capability | `python scripts/test_v410_t04a_gate_repair_routing.py` | 0 | 31 tests OK |
| shared_code_safety_capability | `python scripts/test_v410_t05a_shared_code_safety.py` | 0 | 38 tests OK |
| product_projection_capability | `python scripts/test_v410_t01b_product_projections.py` | 0 | 19 tests OK |
| standard_surface_capability | `python scripts/verify_standard.py` | 0 | `standard verification: PASS`; manifest files 220; bootstrap-required files 41 |
| clean_observer_capability | `python scripts/test_verify_standard.py` | 0 | 6 tests OK |

## 3. Drift and limitation notes (honest record)

- `origin/version/v4.10.0` tip has advanced to `eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601`
  since this pack pinned base `30334e8c…`. This preparation unit is intentionally pinned
  to `30334e8c…`; per `EXECUTION_CONTRACT.md` and the Validation contract, real V01
  dispatch MUST re-read every mapped input at the T08A-integrated exact candidate.
- Host-native facts (subjects 4, 5, 13) could not be read live (GitHub API unreachable);
  they stay `BLOCKED`, owner = GitHub platform. No PASS was inferred from source.
- Dependency state remains `CANDIDATE_NOT_READY` (T04B/T05B/T06A–T08A pending at this
  base). This record transfers to no other candidate and must be re-established after any
  candidate change.

## Negative-invariant reaffirmation

No source repair/mutation, no PR, no issue comment, no push outside this branch, no
Hidden/Release-Qualification/release verdict fabricated, no self-certification. Write set
for this record: this pack directory only.
