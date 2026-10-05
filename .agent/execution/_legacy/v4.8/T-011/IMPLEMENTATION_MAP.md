# T-011 Implementation Map

## Authorized Builder outputs

### `scripts/test_v48_orchestration_dogfood.py`

Create one deterministic, self-contained orchestration dogfood harness that composes the already-merged T-007/T-008/T-009/T-017 behavior. It must exercise the ODF scenario matrix and emit auditable per-scenario outcomes/evidence classifications.

The harness must not mutate normative standards or schemas and must not require an external provider/network for deterministic or repository-real scenarios. Existing upstream conformance modules may be imported/reused when stable, or their public test fixtures may be referenced; do not copy/redefine normative semantics.

### `docs/implementation/4.8.0/dogfood/orchestration/**`

Create bounded dogfood artifacts only, expected to include:

- scenario corpus/fixtures or scenario manifest;
- an evidence matrix with ODF IDs, exact candidate/base identities, inputs, oracle, observed result and evidence class;
- a result report recording limitations, counterevidence and external dimensions that remain `NOT_RUN/BLOCKED`;
- optional small deterministic fixture data needed by the focused harness.

No generated artifact may claim external real-host/device/provider/runtime evidence unless an independent exact-subject Validation reference exists.

## Read-only composition inputs

- `docs/implementation/4.8.0/PRD.md`
- `docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md`
- `docs/implementation/4.8.0/TASK_DAG.md`
- T-007/#513 compatibility evidence and focused conformance
- T-008/#514 scheduling/resource evidence and `scripts/test_v48_scheduling_conformance.py`
- T-009/#515 Interchange replay/restart evidence and `scripts/test_v48_interchange_replay_restart.py`
- T-017/#646 ownership/start-timeout evidence and `scripts/test_v48_execution_ownership.py`
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md`
- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`
- existing Interchange v1 and event-v2 schemas/authority

These are inputs, not T-011 write authority.

## Builder sequence

1. Re-read `version/v4.8.0` and stop/rebind if it differs from pack base `94955c6f93fd7316406ea96bce8f7c32a62509ef` before authoritative implementation begins.
2. Re-read #517 native dependency summary; require `blocked_by=0,total_blocked_by=4` and all four canonical upstream Tasks DONE.
3. Confirm Task Pack/L3 blobs match the Manifest and Builder write set is unchanged.
4. Materialize the deterministic scenario corpus and focused harness only inside the authorized write set.
5. Run focused dogfood and the T-007/T-008/T-009/T-017 regressions plus repository verifier.
6. Produce the evidence matrix/result report with explicit evidence classes and external-real `NOT_RUN/BLOCKED` posture where applicable.
7. Publish Builder terminal with exact base, Pack HEAD, candidate HEAD/tree, exact diff and command results; do not self-claim independent Validation/Review.
8. Hand the exact candidate to an independent Validator. Only after qualifying Validation may a genuinely Fresh Independent Review begin.

## Stop boundaries

Stop rather than implement if success requires changing normative standards/schemas, Frozen Product/L2/DAG, adding a scheduler/authority family, weakening hard filters/composite admission/Claim authority, or relabeling synthetic evidence as real execution.

T-014 is outside this Execution Pack and must remain not started.
