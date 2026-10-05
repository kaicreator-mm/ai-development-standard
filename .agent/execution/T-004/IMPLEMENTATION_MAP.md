# T-004 Implementation Map

Builder writes only:
1. `schemas/role-execution-profile-v1.schema.json` — the v1 JSON Schema (provider-neutral; source-authority projection fields; eligibility/claim/independence refs as references).
2. `references/ROLE_EXECUTION_PROFILE_V1_REFERENCE.md` — contract reference: normalized fields, projection semantics, fail-closed conflict rule, owner-ref table (all references point INTO v4.8 owners).
3. `fixtures/role-execution-profile-v1/**` — positive + negative fixture instances (valid profile; source-authority conflict; stale ref; over-claim; injected authority fields).
4. `scripts/test_v49_role_execution_profile.py` — deterministic stdlib-unittest: schema conformance + negative oracles (see TEST_MATRIX). Style reference (read-only): `scripts/test_v48_agent_capability_profile.py`, `test_v49_assurance_plan_v2.py`.

Read-only starting points: Frozen L2 Role Profile section; `docs/implementation/4.9.0/PRD.md`; v4.8 owner surfaces listed in MANIFEST; L3 T-004 section.
