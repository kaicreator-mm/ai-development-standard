# T-013 Implementation Map

Builder writes only:
1. `references/MANUAL_REFERENCE_FLOW_V49.md` — the operator/controller flow (pointer-only triggers; manual currentness/recompute/Claim/adverse-finding/JIT walkthroughs; durable-vs-derived examples). Study `references/PROGRESSIVE_DISCLOSURE_ROUTING*` + existing reference docs for style (read-only).
2. `fixtures/manual-reference-flow/**` — durable-fact examples.
3. `scripts/test_v49_manual_reference_flow.py` — deterministic link/anchor resolution + durable-vs-derived accuracy checks.

Read-only inputs: EXECUTION_ARCHITECTURE_STANDARD §29 (the semantics the flow exercises), T-010 gate matrix, T-009 JIT governance reference, registries, DAG v0.1 `### T-013`, L3 T-013 section.
