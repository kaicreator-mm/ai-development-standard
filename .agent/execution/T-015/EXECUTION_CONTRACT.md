# T-015 Execution Contract

Exact base: `version/v4.8.0@94cad2b0487e8a552c66d6bcd1cba36b7779383d`.
Authority: Frozen Product/L2/DAG R1 > T-015 Task Pack > this contract. Freedom: F1 bounded implementation.

## Source write set
- `schemas/agent-capability-profile-v1.schema.json`
- `scripts/test_v48_agent_capability_profile.py`
- `references/AGENT_CAPABILITY_PROFILE_REFERENCE.md`

Execution Pack files are read-only to the Builder.

## Contract kernel
Implement only Logical Agent Capability Profile v1: provider-neutral claims about logical Agent/operator/model execution capability. Provider/model identity is provenance only. Skill/procedure metadata is not proof. Tool or credential possession is not mutation/side-effect authority.

Do not own or copy host OS/architecture, installed toolchain/runtime/device inventory, CPU/memory/disk, network reachability, provider concurrency or current resource capacity; those remain existing runner/host/device/resource facts referenced by identity when needed. Do not create current Availability authority, Agent Capability Evidence, a global scalar Agent score, or a fourth Availability/Exchange family.

Any need to duplicate infrastructure ownership or turn capability claims into authorization is an upward architecture/task-pack failure, not Builder discretion.
