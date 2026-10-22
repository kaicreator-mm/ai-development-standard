# T06 JIT Implementation Map
Read these exact baseline owner files at `6d147eac6c86eff620d3695a46ccbb3be452debb`:
1. `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §11 and §28.1–28.5 — parent/child responsibility, Claim, attenuation.
2. `standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` §10 and §21.1–21.3 — pre-effect authority, effect_id/attempt_id, uncertain ACK and safe reconciliation.
3. `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` §5 and §8 — logical operator/role attribution, dispatch/event references.
4. `docs/implementation/4.16.0/R6_AGENT_AUTHORITY_OUTCOME_REPAIR.md` §1–§4 — frozen G requirements and P2-G03.
Deliver exact-source crosswalk + deterministic negative/positive reference fixture tests only. If facts already covered, make **no duplicate normative standard edit**. `test_v416_t06_agent_governance.py` executes source-only contract oracle; this is not Host/DomainHarness runtime evidence.
