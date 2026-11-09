# R5 source-scope crosswalk — exact Git readback (non-normative)

Subject: PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` unmerged/prospective. Baseline reference: `version/v4.18@ac7e7e51de3a7ac27343f16a96568c0b0f2c5349` observed, not an immutable tag. Historical #1353 owner Product/L2/DAG freezes remain frozen at their *separate* exact commits and cannot be reinterpreted by the newer candidate.

The machine-readable `RULE_CROSSWALK.json` binds each of 7 source paths to actual Git blob SHA-1, literal anchor's first line and nearest Markdown heading; 9 model Property IDs reference those source paths with historical/prospective scope. All anchors were found at candidate HEAD and all blob identities matched.

Classes at observed baseline:
- `standards/EXECUTION_PACK_STANDARD.md`: `PROSPECTIVE_CANDIDATE_DIFF_FROM_V418`, baseline blob `c7bd2e4ffb87a0ac7fabc54fd78c4eb1fae6ef0d`
- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`: `PROSPECTIVE_CANDIDATE_DIFF_FROM_V418`, baseline blob `49ecd802c5bf14237e23d5e321c56c220eb8974e`
- `schemas/dispatch.schema.json`: `PROSPECTIVE_CANDIDATE_DIFF_FROM_V418`, baseline blob `90bea62524beb0215d5f40cf0be9986786648fec`
- `scripts/v34_rules.py`: `PROSPECTIVE_CANDIDATE_DIFF_FROM_V418`, baseline blob `ad55439de06126e8684972e590c5ad0e648a9f59`
- `docs/architecture/v4.19/INTEGRATED_DELIVERY_L2_R0.md`: `CANDIDATE_ONLY_NOT_PRESENT_AT_BASELINE`, baseline blob `ABSENT`
- `docs/implementation/v4.19/INTEGRATED_DELIVERY_DAG_R0.md`: `CANDIDATE_ONLY_NOT_PRESENT_AT_BASELINE`, baseline blob `ABSENT`
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md`: `VERBATIM_INHERITED_AT_OBSERVED_V418`, baseline blob `1f1601a20db08d263955241607dfd08d8b8f77e1`

Counts: {"PROSPECTIVE_CANDIDATE_DIFF_FROM_V418":4,"CANDIDATE_ONLY_NOT_PRESENT_AT_BASELINE":2,"VERBATIM_INHERITED_AT_OBSERVED_V418":1}.

**Qualification:** SOURCE_LOCATION_READBACK_PASS, **NOT** full Source→Model semantic equivalence, a v4.19 Freeze, full ADS rule enumeration, or an executed local candidate checkout. R5 closes a T01 *metadata* gap only. Next native execution needs the experimental HEAD and candidate HEAD as separate exact pinned worktrees; script checks should use `--model-head`, `--source-checkout` and `--strict-source`.
