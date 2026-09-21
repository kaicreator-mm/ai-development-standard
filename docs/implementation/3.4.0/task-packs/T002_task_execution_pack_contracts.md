# Task Pack T-002 — Task Pack / Execution Pack Machine Contracts

- Goal: implement machine schemas and pack templates for Task Pack identity and JIT Execution Pack identity, staleness rules, freedom levels, seed semantics and write-set rules.
- Write set: `schemas/**`, `templates/**`, `scripts/**`, `standards/EXECUTION_PACK_STANDARD.md` (new central authority).
- Forbidden: weakening existing schema required fields; introducing `event-v3`; making Execution Pack a second Product/Architecture authority; mandatory empty placeholder artifacts.
- Deliverables:
  - `schemas/execution-pack-manifest.schema.json` — pack identity, base SHA binding, artifact inventory, freedom, retention class.
  - `task-contract.schema.json` extension — machine-readable `agent_freedom`, execution-pack binding fields.
  - `templates/task-pack.md`, `templates/execution-pack/` core artifacts.
  - `standards/EXECUTION_PACK_STANDARD.md` — single normative home preventing duplication across architecture/handoff/validation standards.
- Acceptance: schemas validate under the repository's supported JSON-Schema subset; staleness classification (`PACK_CURRENT / PACK_STALE_NONMATERIAL / PACK_STALE_MATERIAL / PACK_INVALID`) deterministic and fail-closed; freedom levels machine-readable.
- Required gates: verify-standard, test_protocol_schemas, test_v34_lifecycle_contracts.
- Validation ownership: concern.
- Review policy: required (version-level consolidation).
- Agent freedom: F1_BOUNDED_IMPLEMENTATION (public contract shape fixed by T-001 decision).
- Dependencies: T-001.
- Execution Pack: JIT at claim; expected base = integration SHA after T-001 merge.
