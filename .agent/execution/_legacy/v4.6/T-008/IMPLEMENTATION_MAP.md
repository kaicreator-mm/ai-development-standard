# T-008 Exact-base Implementation Map

## Starting identity

```text
version/v4.6.0@a4c5fffe6bab178dcb74b5f47afcda4aa0047c27
TREE=6ae5e1a8b33a6127ecc2e94b6db45e0ca6fa30ea
T06_MERGE=72ea246263b052879833456a33e65e8e9056ab4c
T07_MERGE=a4c5fffe6bab178dcb74b5f47afcda4aa0047c27
```

Builder begins from the final JIT Pack HEAD on `task/311-v46-cross-standard-conformance`, while this pack's immutable integration `base_sha` remains the version target above.

## Authority inputs

| Concern | Exact durable input | Use |
|---|---|---|
| Product forbidden inferences | Frozen Product `e6aa04981110376e623d19b7dd4d0c6d0e139bdf`, PRD §11 | negative-oracle minimum |
| Architecture validation union | Frozen L2 `f47ea81e8f8df32ac6c8b7cc922c405a17b704d9`, §13 | adds ephemeral-only truth and architecture-level negative cases |
| Task decomposition | Frozen DAG `d3607c61f22b2c15fbb07d412c4e222e818b31c9` | T08 scope/dependency authority |
| T08 scope | Task Pack blob `248abb5c468240e702f383b003a93a6f503e4cfa` | write-set, acceptance, gates, failure handling |
| T08 implementation guidance | L3 blob `c219344d8b902bc5053adbdc2328a3147af8f7bf` | integrated tests + closure-input contract |
| v4.1–v4.5 separation | `docs/implementation/4.6.0/UPSTREAM_OWNER_CURRENTNESS.md` | owner-composition oracle; evidence inventory, not Product authority |
| historical/Fast Path | `docs/implementation/4.6.0/MIGRATION_ADOPTION.md` | no retrofit, proportional adoption/gates |
| cross-owner map | `references/AI_NATIVE_EXISTING_OWNER_INTEGRATION.md` | reference existing owners, no duplication |
| T06 fidelity | `docs/implementation/4.6.0/dogfood/**`, #309 terminal evidence, T06 merge `72ea2462...` | preserve exact claim/evidence dimensions |

## Output map

### `scripts/test_v46_cross_standard_conformance.py`

Own deterministic integrated conformance only. Prefer inspecting durable repository facts and fixtures already present at the exact base; do not introduce a new state reducer or authority resolver.

Minimum oracle groups:

1. Product/L2 forbidden-inference union.
2. v4.1–v4.5 + existing Assurance/Review/Dispatch/Handoff/Validation/Release owner separation.
3. historical evidence non-retrofit/additive compatibility.
4. Fast Path proportionality/non-weakening.
5. T06 fidelity: packet digest and evidence-dimension labels; no static→real or partial-real→universal inference.
6. closure-input structure/wording that cannot manufacture Closure/Release verdicts.

### `docs/implementation/4.6.0/CLOSURE_INPUTS.md`

Create a durable ledger whose fields are evidence inputs for a later Version Closure owner. It should include:

- version integration subject identity and currentness status;
- T08 implementation candidate HEAD/tree once it exists;
- focused/integrated test evidence;
- CI evidence identity/status;
- exact-subject T08 Validation evidence identity/status;
- Fresh Independent Review evidence identity/status;
- T06 dogfood fidelity references and actual claim dimensions;
- unresolved findings, including P0/P1 and missing required evidence;
- explicit `NOT_RUN`, `BLOCKED`, `UNKNOWN` where applicable;
- an explicit statement that the document issues no Candidate Freeze, Version Closure, Release Qualification, Release READY or integration authorization.

Do not pre-fill future PASS values. Before their owners execute, use `NOT_RUN/PENDING` rather than predicted success.

### `docs/implementation/4.6.0/conformance/**`

Optional. Add only a minimal deterministic fixture when an acceptance oracle cannot be expressed faithfully from existing durable inputs. Do not duplicate source authorities or historical evidence merely for convenience.

## Builder sequence

1. Re-read live target/issue dependencies/Task Pack/L3/branch Pack and fail closed on drift.
2. Treat final Pack HEAD as the implementation starting HEAD; do not edit Pack files.
3. Implement focused tests first, then closure-input ledger/only-material fixtures.
4. Run focused deterministic conformance and applicable repository verifier/CI.
5. Report actual final HEAD/tree, implementation delta from Pack HEAD, tests run and all NOT_RUN/BLOCKED limitations to #311.
6. Stop for separately owned exact-subject Validation and Fresh Independent Review. Do not self-review, merge, or perform Version Closure.
