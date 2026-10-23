# T06 JIT Execution Contract
- Exact owner: ADS #1270; frozen Product #1261@6338348925, L2 #1261@6338359775, DAG #1261@6338768231.
- Baseline and pinned standard: `6d147eac6c86eff620d3695a46ccbb3be452debb`. Branch: `task/v416-t06-agent-governance`; dependency blocked_by=[] at generation; T07 depends on this issue.
- Allowed **implementation**: `docs/implementation/4.16.0/G_AGENT_OWNER_CROSSWALK.md`, `scripts/test_v416_t06_agent_governance.py`, `tests/fixtures/v416/t06/*`; editing `standards/EXECUTION_ARCHITECTURE_STANDARD.md` requires proven specific gap and prior Task amendment. No runtime tool implementation.
- JIT-only core files under `.agent/execution/T06/` are scheduler artifacts, not an expansion of implementation freedom.
- Source facts: Exec Arch §28 and External Execution §§10/21 remain normative, preserved unmodified. Historical Capability Profile/Evidence/Role v1 schemas remain unchanged. New selection refs, if justified, may only be optional audit evidence, never execution authority.
- Builder: follow accepted single-writer Claim/Dispatch after real READY; never claim validation/review PASS. Single concern PR into `version/v4.16`, `review:required`.
