# T11 Conformance & Dogfood Evidence

Status: **BUILDER EVIDENCE / CLOSURE INPUT ONLY**

This artifact is owned by T11 / Issue #257. It records integrated conformance and planner→bounded-executor dogfood evidence. It does **not** issue Version Closure, Candidate Freeze, Hidden Validation, Release Qualification, or merge authority.

## Bound subject

- Repository: `kaicreator-mm/ai-development-standard`
- Integration target at dispatch: `version/v4.3.0@ea5b39bb27ae36886748420d282350dd1a16476e`
- Base tree: `1a88c724e4971ff2c35b88315cc8114b329adcad`
- Execution Pack generation HEAD: `d9ac745f0897903e95c09eb33b6c54aa49c84cb5`
- Execution Pack tree: `116eb8a901bef1ec142c69f2c4e6941e3545ad22`
- Task Pack: `docs/implementation/4.3.0/task-packs/T11_conformance_dogfood.md`
- L3: `docs/implementation/4.3.0/L3_REFERENCE_PACKS.md#t11--conformance--dogfood`

Any later target or authority drift requires successor rebinding; this evidence does not transfer across material drift.

## Executable conformance matrix

`scripts/test_v43_conformance_dogfood.py` consumes `fixtures/shortcut_negative_matrix.json` and executes all ten Frozen negative families against their existing v4.3 semantic owners:

| ID | Shortcut that must be rejected | Existing authority consumed |
|---|---|---|
| N01 | popularity → architecture decision | `standards/ARCHITECTURE_DESIGN_STANDARD.md` |
| N02 | unresolved high-impact UNKNOWN → implementation freedom | `standards/ARCHITECTURE_DESIGN_STANDARD.md` |
| N03 | file count → coherent Task boundary | `standards/TASK_DECOMPOSITION_STANDARD.md` |
| N04 | atomic shared invariant → safe parallelism | `standards/TASK_DECOMPOSITION_STANDARD.md` |
| N05 | dependency removal → READY | `standards/TASK_DECOMPOSITION_STANDARD.md` |
| N06 | PR stack/cherry-pick → canonical live DAG | `standards/TASK_DAG_GOVERNANCE_STANDARD.md` |
| N07 | mutation without reason/authority/impact → valid DAG mutation | `schemas/dag-mutation-record-v1.schema.json` |
| N08 | Agent-local tool version → repository profile authority | `profiles/README.md` |
| N09 | profile mapping → universal style/tool mandate | `profiles/README.md` |
| N10 | `PROJECT_OVERRIDES` → weakening Frozen/Core authority | `profiles/README.md` |

The T11 suite does not become a new semantic owner. It asserts the existing owners and composes the pinned T01–T10 regression commands listed by the Execution Pack.

## D01 — profile/DAG composition

The focused T11 suite executes these existing regression/verification entrypoints as subprocesses and fails closed if any fails:

- `scripts/test_v43_dag_mutation_contract.py`
- `scripts/test_v43_profile_framework.py`
- `scripts/test_v43_task_decomposition.py`
- `scripts/test_v43_task_dag_governance.py`
- `scripts/test_v43_implementation_quality.py`
- `scripts/test_v43_ts_python_profiles.py`
- `scripts/test_v43_go_java_rust_profiles.py`
- `scripts/test_v43_archetype_profiles.py`
- `scripts/test_v43_adoption_wiring.py`
- `scripts/test_protocol_schemas.py`
- `scripts/verify_standard.py`

## D02 — planner → bounded executor dogfood

Fixture: `fixtures/planner_bounded_executor.json`

- Exact subject: T11 on the dispatch-bound v4.3 integration target and pack identities above.
- Planner role: high-capability ADS planner/controller that produced the durable Task Pack + Execution Pack.
- Bounded executor/evaluator role: **synthetic bounded lower-cost executor interpretation/evaluation**.
- Evidence kind: **SYNTHETIC**.
- Expected oracle: `CONSUMABLE_WITHOUT_PRODUCT_OR_ARCHITECTURE_REDESIGN`.
- Report fields remain `actual_result=PASS` and `redesign_needed=NO`, but neither field is an oracle.
- Clarification/escalation is `NONE_REQUIRED` only after the authority-derived interpretation exact-matches the selected durable Product/Architecture/Task/Execution facts.

The executable D02 oracle now reconstructs its expected bounded interpretation from durable authority rather than trusting fixture self-assertions. It derives and exact-compares:

- the Execution Contract Builder write-set;
- Task Pack forbidden scope plus the stricter Execution Contract `MUST NOT` scope;
- Task Pack acceptance and required gates;
- Execution Contract required semantic actions;
- Task Pack failure handling and Execution Pack failure actions;
- exact Product/L2/Task DAG/Task Pack/L3/Execution Pack refs, blobs, base SHA/tree, dependency completion, and T11→T10 binding.

The test also executes fail-closed negative probes for an unauthorized allowed path, weakened forbidden scope, missing/wrong required action, missing required gate, weakened failure handling, and mismatched exact subject/binding. Every probe keeps the fixture's `actual_result=PASS` and `redesign_needed=NO`; the computed oracle must still return failure. This is the durable proof that self-assertions are evidence/report fields only.

The evaluator may not redesign Product/Architecture, mutate existing v4.3 semantic owners, weaken a gate, or adapt an oracle to force green. Any authority mismatch fails closed and routes according to the durable failure/escalation handling.

## D03 — SYNTHETIC / REAL non-transfer

Selected dogfood does not materially require a real external agent/toolchain, so real execution status is explicitly `NOT_RUN`. The executable oracle rejects any transfer from this synthetic result into a real-host/provider `PASS` claim.

If a later selected subject requires unavailable real execution, the exact scope must become a Validation handoff and remain `NOT_RUN`/`BLOCKED` until real evidence exists.

## Gate identities and current dispositions

| Gate / evidence | Current builder disposition |
|---|---|
| Focused T11 suite | MUST run on successor PR exact HEAD; Builder records actual execution separately |
| Applicable T01–T10 regressions | Invoked by the focused T11 suite; exact-head result must come from execution evidence |
| CI | `.github/workflows/verify-standard.yml` with one T11 invocation; exact successor run identity/result must be bound after execution |
| Integration Validation | **PENDING successor after this repair**; required, independent, exact-head |
| Fresh Independent Review | **PENDING successor after successor Validation**; required, genuinely new, exact-head |
| Version Closure | **NOT_READY / not owned by T11** |
| Candidate Freeze | **NOT_AUTHORIZED** |

## P0–P3 disposition ledger

Fresh Review #619 identified one P1 on D02: the predecessor oracle trusted fixture self-assertions and did not exact-compare durable authority. This bounded repair implements an authority-derived exact oracle and negative probes, but the Builder does not close its own finding. Successor Validation and then a genuinely new Fresh Review must independently determine whether the P1 is closed.

- P0: `OPEN=0`.
- P1: `REPAIR_IMPLEMENTED=1; INDEPENDENT_CLOSURE=PENDING`.
- P2: `OPEN=0`.
- P3: `OPEN=0`.

Any unresolved P0/P1 remains blocking for closure handoff.

## Builder stop boundary

Builder completion requires a successor exact HEAD/tree on the SAME PR #610, actual focused/applicable execution evidence, exact repair write-set binding, then stop. Independent successor Integration Validation and a genuinely new Fresh Review are mandatory before merge.
