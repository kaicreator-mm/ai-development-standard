# T-014 JIT Execution Contract

## Exact authority
- Issue: #733 / T-014 Proportional Dogfood / Independent Auditor Contract. Risk: high. L3: required evidence-contract review.
- Base: `version/v4.9.0@d53e943ec7109648485b64a647ed2c7cf553531d`, tree `5ad2dbd8c312a67bb050a3199ab9b29b70c23406`.
- Immutable DAG v0.1 `### T-014` (blob `4f358ba2...`) is the normative concern. Native blockers zero; lineage current at base.
- T-005->T-010->T-014 Release-owner serialization: this lane defines the CONTRACT (document + negative oracles); it edits NO Release surfaces and cannot authorize execution or issue Release Qualification.

## Required result
Define the release-consumable downstream dogfood report/checklist and independent safety-auditor contract from Frozen Product §16 / L2:
1. `references/DOWNSSTREAM_DOGFOOD_AUDIT_CONTRACT_V49.md` — the contract: exact ADS candidate binding (per the T-010 gate matrix binding); legal baseline vs selected workflow accounting; mechanism exercise matrix; NONZERO proportional delta requirement; ambiguous predicate fail-closed exercise; independent auditor eligibility/profile (who may audit: eligibility refs into the v4.8/v4.9 owners; auditor identity cannot grant authority); report/checklist is Release EVIDENCE only.
2. `scripts/test_v49_dogfood_audit_contract.py` — deterministic evidence-contract negatives: exact-candidate binding or reject; nonzero-delta or reject; ambiguous predicates fail closed; auditor without eligibility rejects; report cannot self-authorize execution or RQ; owner surfaces cited not copied.
3. `fixtures/dogfood-audit-contract/**` — contract scenarios.

## Hard boundaries
- No Release surface edits; no Product/L2/DAG mutation; frozen blobs resolve unchanged at candidate; the contract is descriptive/evidence-binding — no execution authorization.

## Mutation authority
Only the three Builder write-set paths in MANIFEST plus the six immutable `.agent/execution/T-014/**` planning files.
