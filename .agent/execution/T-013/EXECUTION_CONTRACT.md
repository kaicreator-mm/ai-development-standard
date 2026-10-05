# T-013 JIT Execution Contract

## Exact authority
- Issue: #732 / T-013 Manual / GitHub-Native Reference Flow. Risk: medium. Review: recommended (skip only with current Assurance Plan owner-positive permission + proven predicates — default: run the review).
- Base: `version/v4.9.0@d53e943ec7109648485b64a647ed2c7cf553531d`, tree `5ad2dbd8c312a67bb050a3199ab9b29b70c23406`.
- Immutable DAG v0.1 `### T-013` (blob `4f358ba2...`) is the normative concern. LG_SEQ_FULL current at base (full integrated predecessor lineage physically present).

## Required result
Prove the v4.9 workflow can be executed from durable GitHub/repository facts WITHOUT scheduler daemon, runtime DB or proprietary transport:
1. `references/MANUAL_REFERENCE_FLOW_V49.md` — concise operator/controller reference flow: pointer-only trigger examples; manual currentness/recompute/Claim/adverse-finding/JIT examples; examples distinguishing durable facts from derived state. Every cited artifact binds an exact repo ref.
2. `fixtures/manual-reference-flow/**` — durable-fact examples used by the flow.
3. `scripts/test_v49_manual_reference_flow.py` — deterministic checks: every reference in the flow doc resolves at the candidate (path+anchor); durable-vs-derived distinction examples are accurate (durable facts read from git/registry surfaces; derived state marked as projection); no scheduler daemon/runtime DB/proprietary transport implied anywhere.

## Hard boundaries
- Must not create normative semantics absent from Frozen L2/owner standards (descriptive reference only).
- No Product/L2/DAG mutation; frozen blobs resolve unchanged at candidate.

## Mutation authority
Only the three Builder write-set paths in MANIFEST plus the six immutable `.agent/execution/T-013/**` planning files.
