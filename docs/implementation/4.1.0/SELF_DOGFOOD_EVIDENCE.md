# v4.1 Execution Foundation — Self-Dogfood Evidence

Status: **REPAIRED T08 CANDIDATE — pending successor exact-SHA Validation and Fresh Independent Review. No Version Closure / Release Qualification claim.**

## Execution subject

T08 consumes dependency-complete v4.1 T01–T07 after their merges. Its primary executable entrypoint is `scripts/test_v41_execution_foundation_conformance.py`, launched by `scripts/test_verify_standard.py` in repository CI. On its actual checked-out SHA it invokes these **seven actual owner suites**, not fixture substitutes:

1. `test_v41_execution_foundation_contracts.py` (including historical v4 Dispatch, Validation Report and Execution Pack payload compatibility).
2. `test_v41_dependency_toolchain.py` (risk exception != Validation PASS/remediation, Node + non-Node toolchains, Agent-local tooling non-authority).
3. `test_v41_git_execution.py` (local/unpushed Git, independent workspaces, SHA rewrite, unknown-ownership cleanup).
4. `test_v41_configuration_secrets.py` (secret reference boundaries).
5. `test_v41_workspace_artifact.py` (classes, producer/build provenance, authorized promotion, destructive cleanup).
6. `test_v41_external_systems.py` (actual fidelity/non-escalation, unavailable BLOCKED/NOT_RUN, bounded retries, project-defined taxonomy).
7. `test_v41_adoption_wiring.py` (integrated adoption/Golden coverage).

The T08 Golden matrix complements these owner suites; it does not replace their assertions. Its additional negatives cover accepted-risk-not-PASS/remediation, unpushed/local Task claim, stale exact-SHA reuse, unknown ownership cleanup, promotion missing producer/build source refs, unavailable/unexecuted external journey, custom project fidelity labels and per-attempt versus overall deadline. The supplementary evaluator's toy records are not real provider/package/build output or production proof.

## Adversarial owner-weakening test

`test_verify_standard.py` clones the repository into an isolated temporary directory (without `.git`/Python bytecode), weakens a material T02 normative phrase, then executes the **same** T08 integrated runner against that copy. It asserts non-zero child exit and identifies the broken owner test by name. The deliberate child FAIL demonstrates that a weakened T01–T07 owner is not masked by an independently green T08 fixture oracle. No canonical owner file is modified by this adversarial test.

## Covered boundaries and carry-forwards

- Fast Path: no empty projection for a non-material concern, while material owner obligations persist.
- Historical/additive: old v4 machine payloads still validate without optional v4.1 fields; optional references do not rewrite historic authority or exact subject.
- Toolchain: Node/npm plus Python; compatibility, preferred development, deployment identity and certified tuple must not collapse; local installed runtime does not rewrite repository authority.
- Security/risk: durable secret *references*, not values; accepted-risk remains a disposition, never PASS or vulnerability remediation.
- Git/workspaces: distinct writable materializations and durable recovery; local branch/unpublished work and rewritten old exact-SHA evidence cannot become canonical live Task/Validation facts. Unknown/unowned state is preserved, isolated and escalated rather than destructively cleaned.
- Artifacts: `CACHE` != evidence, `BUILD_OUTPUT` != RELEASE_ARTIFACT; supplementary trial promotion requires authorization, identity plus explicit source and build references. Actual artifact Release qualification remains a different owner.
- External systems: sandbox cannot claim production, credential capability cannot grant write; required unavailable journey is BLOCKED and available-but-unexecuted is NOT_RUN. Project-defined fidelity labels are extensible, and per-attempt timeout cannot exceed an authorized overall deadline; actual equivalence/retry policy requires real project authority.
- Evidence boundary: Task/integration PASS and CI success never manufacture Release READY or Version Closure.

## Required successor evidence

A clean exact-SHA independent Validator must execute the T08 focused integrated runner, `test_verify_standard.py` (including the adversarial weakening negative) and `verify_standard.py`; capture requested/tested/current HEAD, live base, command exit codes, environment identity and cleanliness. A Fresh Independent reviewer must re-assess the updated evidence against #364's two P1/four P2 without inheriting #363's historical predecessor PASS.

## Explicit evidence limits

This repository dogfood does **not** claim authenticated production provider access, actual external writes, secret-value reads, Hidden Validation, a qualified release artifact, multi-platform installer behavior, or any Release/Version Closure verdict. If a later Gate requires real runtime/provider/platform evidence not executed here, use an exact-subject handoff and preserve BLOCKED/NOT_RUN instead of upgrading fixture/CI truth by assertion.
