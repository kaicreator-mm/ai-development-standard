# v4.7 T07 Unified Semantic Conformance Matrix

Status: **T07 implementation reference — non-authoritative test evidence**

Task authority: `docs/implementation/4.7.0/task-packs/T07_unified_semantic_conformance.md`  
JIT implementation baseline: `fec3d473b2d569073c16c470e80afbc3af8935dc`  
Integration target: `version/v4.7.0`

This matrix describes the executable T07 composition layer. It points to and tests existing owners; it does **not** become a normative owner, a permission engine, a new Gate, a `CONVERGENCE_PASS` family, Validation, Review, Release Qualification or Version Closure authority.

## Scope boundary

T07 may mutate only:

- `references/V47_SEMANTIC_CONFORMANCE_MATRIX.md`
- `scripts/test_v47_semantic_conformance.py`
- `scripts/v47_conformance.py`

Registry/discovery metadata, a provider/tool being available, CI/test success, technical necessity, or this matrix itself cannot enlarge that write-set. Owner corrections remain with the owning task/standard.

## Executable matrix

| ID | Concern | Durable source(s) composed | Positive check | Adversarial / forbidden check | Failure identity |
|---|---|---|---|---|---|
| U01 | canonical owner uniqueness | `standard-manifest.json`, T01/T02 schema/tests | each semantic concern resolves to one canonical normative path | duplicate concern/owner cannot be resolved by order | `U01` + concern/path |
| U02 | mutation authority | Frozen T07 Task Pack | exact three-file write-set is recognized | canonical-owner discovery, registry presence, tooling or test success cannot authorize another file | `U02` + write-set drift/path |
| U03 | qualified state semantics | `registries/state-dimensions-v1.json`, T03 | dimensions retain owner qualification and F01–F10 exact identities | same `PASS` token across Review/Validation is not transferable; corrected Runtime owner must remain exact-pinned | `U03` + dimension/rule id |
| U04 | exact identity/currentness | `standards/REFERENCE_CONVENTION_STANDARD.md`, T04 | evidence applies only to the same exact tuple | old SHA -> successor SHA and sandbox -> real host do not transfer | `U04` + reference/tuple |
| U05 | profile + `PROJECT_OVERRIDES` routing | `scripts/resolve_standard_read_set.py`, project override template, T05 focused suite | profile/override composition remains deterministic and non-authoritative | duplicate/conflicting override, exact-subject drift or unproven mutation authority fail closed | `U05` + resolver contract |
| U06 | compatibility + history | manifest compatibility inventory, T06 | every current alias maps one-hop to one normative owner; legacy `sections` remain consumable | alias-as-owner, duplicate claim, silent stable-path loss or missing current registry cannot prove current conformance | `U06` + alias/history |
| U07 | machine/prose semantic consistency | Frozen Product/L2/L3 + T01–T06 executable surfaces | exact rule identities and reference invariants agree with machine data | altered forbidden-inference tuple reports the precise rule id | owning rule id |
| U08 | v4.1–v4.6 carry-forward negatives | Frozen v4.7 Product/L3 plus current owner tests | Frozen Product negative catalog remains present and T01–T06 focused suites execute together | no cross-owner inference is manufactured by the T07 runner | missing negative / dependency test path |

## Required machine negatives

T03 remains the machine-readable owner for the currently registered cross-dimension rules. T07 composes, but does not rewrite, these identities:

- `F01_TASK_DONE_NOT_VALIDATION_PASS`
- `F02_REVIEW_PASS_NOT_VALIDATION_PASS`
- `F03_VALIDATION_PASS_NOT_RELEASE_READY`
- `F04_RELEASE_READY_NOT_DEPLOYMENT_SUCCESS`
- `F05_DEPLOYMENT_SUCCESS_NOT_RUNTIME_HEALTH`
- `F06_RUNNER_AVAILABLE_NOT_MUTATION_AUTHORITY`
- `F07_OLD_SHA_VALIDATION_NOT_SUCCESSOR_PASS`
- `F08_SANDBOX_PASS_NOT_REAL_ENV_PASS`
- `F09_DISPATCH_COMPLETED_NOT_RELEASE_READY`
- `F10_PACK_CURRENT_NOT_VALIDATION_PASS`

The Runtime dimension is checked against the corrected immutable v4.5 owner pointer:
`github:kaicreator-mm/ai-development-standard@c9ee9249999aa5463ce880bc7674b732979009b3:standards/OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md`.
T07 does not import that v4.5 owner into the local v4.7 normative inventory.

## Commands

Focused unified suite:

```bash
python scripts/test_v47_semantic_conformance.py
```

Combined executable report (runs the unified repository checks plus the already-merged T01–T06 focused suites):

```bash
python scripts/v47_conformance.py
```

The JSON field `ok: true` means only that these deterministic repository checks completed without an observed conformance error. `authority_effect` and `gate_effect` remain `NONE`.

## Failure handling

- owner ambiguity / registry mismatch -> `U01`, route to the owning manifest/metadata task;
- write authority defect -> `U02`, stop rather than broaden the Task Pack;
- state/inference defect -> `U03`/rule id, route to the state-registry owner;
- exact identity/reference defect -> `U04`, route to the owning reference/Validation/Review contract;
- override/profile routing defect -> `U05`, route to T05/owning project authority;
- compatibility/history defect -> `U06`, route to T06/compatibility authority;
- Frozen Product/L2 contradiction -> Planning Amendment; T07 must not silently redefine it;
- local T07 implementation defect -> repair only inside the Frozen T07 three-file write-set.

## What this does not prove

- It does not issue integration Validation or Fresh Independent Review; both remain required after the Builder produces the exact PR HEAD.
- It does not prove a different exact SHA, environment, runtime/toolchain or validation profile.
- It structurally checks immutable upstream owner references already selected by T03; it does not claim live v4.4/v4.5 runtime/deployment execution.
- It does not execute T08 fresh-Agent dogfood, T09 adoption/migration wiring, T10 closure inputs, Version Closure, Release Qualification or merge.
