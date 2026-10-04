# T-003 Execution Contract

Exact base: `version/v4.8.0@33dfb8f05bca1ba8fd4ea8d9a2c63eaa8f9aa830`.
Authority: Frozen Product/L2/DAG R1 > T-003 Task Pack > this contract. Freedom: F1 bounded implementation.

## Source write set
Default no-gap evidence path:
- `references/V48_INTERCHANGE_PROFILE_COMPATIBILITY.md`
- `scripts/test_v48_interchange_profile.py`

Conditional mutation is allowed only if the Builder first proves a concrete compatibility gap in existing `interchange-envelope-v1` / GitHub adapter mapping. If such a gap is proven, stop and rebind the Execution Contract before editing the existing schema or protocol standard; do not silently expand this write set.

Execution Pack files are read-only to the Builder.

## Contract kernel
First attempt to prove `NO_CHANGE_REQUIRED`. Existing Interchange v1 remains the sole generic transport-neutral envelope/correlation family; `ai-dev:event:v2` remains GitHub writer/admission authority. Receiver/eligibility/capability semantics remain owned by Task/Dispatch/Execution Architecture and canonical T-015 profile; Interchange may correlate/reference those durable facts but must not invent an ad-hoc capability shape or another Exchange owner.

ACK/delivery/progress never becomes workflow truth. Replay/conflict/currentness/durable materialization and historical payload compatibility must remain intact.
