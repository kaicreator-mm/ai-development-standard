# ADS #1366 — Source-to-atom-to-model review, bounded pilot v3

Candidate PR #1365 @ `dac263fa4c0ab155406d2f2117459b34322cc988`, **not released**. Source-only execution, not a native proof run or a complete obligation census.

## Review correction

Earlier v1 split 21 candidate statements; v2's self-adversarial review separated three compound statements into **25 independently reviewable draft atomic constraints** in six topical review clusters. This v3 additionally checks each existing `ADS-P-*` reference against the actual `formal/v4.19/r8/source-index.json` `sources[]` array:

- **14/25** related pilot Properties **cite the same normative source file**. Even these are *only source-file-level links*: R11 model proof does **not** establish per-clause equivalence.
- **11/25** are **analogy-only mappings**: the related Property's existing source index **does not cite the source file at all**. They must not be counted as formal coverage.
- **0/25** have independent direct natural-language↔model semantic equivalence proof. This is a *selected review set*, not 0% of all ADS rules. Total authoritative ADS obligation denominator remains `UNKNOWN`.
- Evidence tiers: {"SOURCE_SCHEMA_ONLY":5,"NO_DIRECT_TEST":11,"ABSTRACT_MODEL_ONLY":5,"SYNTHETIC_DEMO_ONLY":4}. An actual v4.19 pinned consumer is not verified, so live Dispatch/Claim/Release equivalence remains NOT_PROVEN.

### Corrected atomic review table

| Atom | Topic | Exact source | Existing related Property | Pilot directly cites file? | Evidence tier |
|---|---|---|---|---|---|
| `PR-01` | PROFILE_ROLE_SCOPE | `EXECUTION_PACK_STANDARD.md:148` | `ADS-P-AUT` | **YES (not semantic proof)** | SOURCE_SCHEMA_ONLY |
| `PR-02V` | PROFILE_ROLE_SCOPE | `EXECUTION_PACK_STANDARD.md:148` | `ADS-P-AUT` | **YES (not semantic proof)** | SOURCE_SCHEMA_ONLY |
| `PR-02S` | PROFILE_ROLE_SCOPE | `EXECUTION_PACK_STANDARD.md:148` | `ADS-P-AUT` | **YES (not semantic proof)** | NO_DIRECT_TEST |
| `PR-02G` | PROFILE_ROLE_SCOPE | `EXECUTION_PACK_STANDARD.md:148` | `ADS-P-AUT` | **YES (not semantic proof)** | NO_DIRECT_TEST |
| `PR-03` | PROFILE_ROLE_SCOPE | `EXECUTION_PACK_STANDARD.md:148` | `ADS-P-AUT` | **YES (not semantic proof)** | ABSTRACT_MODEL_ONLY |
| `PR-04` | PROFILE_ROLE_SCOPE | `EXECUTION_PACK_STANDARD.md:148` | `ADS-P-EVO` | **YES (not semantic proof)** | ABSTRACT_MODEL_ONLY |
| `PR-05` | PROFILE_ROLE_SCOPE | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:573` | `ADS-P-AUT` | **YES (not semantic proof)** | SOURCE_SCHEMA_ONLY |
| `DP-01F` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:577` | `ADS-P-EVI` | **YES (not semantic proof)** | NO_DIRECT_TEST |
| `DP-01S` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:577` | `ADS-P-EVI` | **YES (not semantic proof)** | NO_DIRECT_TEST |
| `DP-02` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:577` | `ADS-P-LC` | **NO (analogy only)** | NO_DIRECT_TEST |
| `DP-03` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:577` | `ADS-P-AUT` | **YES (not semantic proof)** | SOURCE_SCHEMA_ONLY |
| `DP-04` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:577` | `ADS-P-AUT` | **YES (not semantic proof)** | SOURCE_SCHEMA_ONLY |
| `DP-05` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:579` | `ADS-P-CAS` | **YES (not semantic proof)** | ABSTRACT_MODEL_ONLY |
| `DP-06` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:579` | `ADS-P-CAS` | **YES (not semantic proof)** | ABSTRACT_MODEL_ONLY |
| `DP-07` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:581` | `ADS-P-EVO` | **YES (not semantic proof)** | ABSTRACT_MODEL_ONLY |
| `TE-01` | TEST_EVIDENCE | `TESTING_STANDARD.md:66` | `ADS-P-EVI` | **NO (analogy only)** | SYNTHETIC_DEMO_ONLY |
| `TE-02` | TEST_EVIDENCE | `TESTING_STANDARD.md:66` | `ADS-P-EVI` | **NO (analogy only)** | SYNTHETIC_DEMO_ONLY |
| `DG-01` | DAG_DEPENDENCY | `TASK_DECOMPOSITION_STANDARD.md:183` | `ADS-P-DEP` | **NO (analogy only)** | SYNTHETIC_DEMO_ONLY |
| `DG-02` | DAG_DEPENDENCY | `TASK_DECOMPOSITION_STANDARD.md:183` | `ADS-P-WRITER-KEYS` | **NO (analogy only)** | SYNTHETIC_DEMO_ONLY |
| `AR-01` | PUBLIC_SELECTED_PATH | `ARCHITECTURE_DESIGN_STANDARD.md:51` | `ADS-P-CROSS` | **NO (analogy only)** | NO_DIRECT_TEST |
| `AR-02U` | PUBLIC_SELECTED_PATH | `ARCHITECTURE_DESIGN_STANDARD.md:51` | `ADS-P-EVI` | **NO (analogy only)** | NO_DIRECT_TEST |
| `AR-02A` | PUBLIC_SELECTED_PATH | `ARCHITECTURE_DESIGN_STANDARD.md:51` | `ADS-P-EVI` | **NO (analogy only)** | NO_DIRECT_TEST |
| `IM-01` | PUBLIC_SELECTED_PATH | `IMPLEMENTATION_QUALITY_STANDARD.md:43` | `ADS-P-EVI` | **NO (analogy only)** | NO_DIRECT_TEST |
| `DE-01` | PRODUCT_STAGE_EVIDENCE | `DEVELOPMENT_WORKFLOW.md:141` | `ADS-P-EVI` | **NO (analogy only)** | NO_DIRECT_TEST |
| `DE-02` | PRODUCT_STAGE_EVIDENCE | `DEVELOPMENT_WORKFLOW.md:142` | `ADS-P-LC` | **NO (analogy only)** | NO_DIRECT_TEST |

Atom semantics, preconditions, proposed negative witnesses, exact Git blob and source line anchors are in `ATOMIC_RULE_SAMPLE.json`. **Do not** convert source citation into effective applicability or a successful runtime admission.

## Next verification with real value

1. Independently scrutinize high-risk candidate `DP-01S / DP-02 / DP-05 / DP-06`: schema pin, complete enriched object, source/schema/Claim alignment at write time, zero accepted mutations when rejected. Identify actual checked object and immutable publish readback; use the effective task standard pin, not a similar-looking unadopted downstream system.
2. `PR-02V/S/G`: cross-check LOCAL_VALIDATION's validator-only, exact-SHA and genuine local-gap predicates separately; source enum verifies one, not all.
3. `TE-02`, `DG-02`, `AR-02U`: require honest NOT_RUN, preserve native dependencies, avoid mislabeling an unproven public path. Existing synthetic negative probes are bounded, not real GitHub facts.
4. For any new candidate proving obligation, carry frozen/version scope, responsible authority, exception/unknown, candidate proof and negative witness to independent review. Add a tiny SMT/TLC model *only when* actual source semantics expose an uncovered falsifiable invariant. No 25 individual Issues or regenerated 35-case run.

**Metadata verification:** 25/25 exact source anchors checked in v2, 7 failed corruption mutants; now 25/25 model source-index relationships checked in v3 and three false-mapping mutations rejected. Neither is a formal model/test execution. R11 native 35/35/Python 61/61 remain historically correct for the original exact model head; no change to pinned sources or test runner here.
