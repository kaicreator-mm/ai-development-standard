# ADS #1366 — v2 source-to-atomic review sample (not an ADS proof)

**Source candidate:** PR #1365 @ `dac263fa4c0ab155406d2f2117459b34322cc988`; all 7 changed standards exact-blob verified. **Previous draft:** `99e3d84bdf4db069d794e8831026c40519522857`. The R11 61/61 Python and 35/35 SMT/TLC PASS remain valid for their original exact subject only. This source-review index is not a new SMT run or a semantic theorem.

## Why the first pass was revised

The first-pass 21 rows included some compound rules. Internal adversarial review separated:
- `LOCAL_VALIDATION`: its **validator-only authority**, **exact-SHA subject** and **residual-local-capability-gap** conditions (3 separately assessable propositions).
- Dispatch publication: checking a **fully enriched object** and using the **effective project-pinned schema identity** are not interchangeable (2).
- Architecture execution unavailable: **recording UNKNOWN** and **assigning the first legal bounded check** are two different obligations.

Thus the current sample has **25 proposed atomic interpretations** in **6 review clusters**, based on 7 source files. Exactly **17** rows derive from **12** previously selected candidate-delta observations; the remaining **8** are additional source-direct Dispatch prepublication rows. These 25 are *not* a comprehensive denominator for v4.19 or ADS overall. Interpretation remains **assistant draft, NOT independently reviewed**.

## Atomized source and evidence map

Each row below represents a single proposed constraint and includes in JSON: exact SHA/line/anchor, governing source/version scope, trigger, constraint, proposed negative witness, related *bounded* ADS-P-* property (relevance only), and actual evidence tier.

| Atom | Review cluster | Source line | Proposed rule (condensed) | Existing abstract property | Evidence tier |
|---|---|---|---|---|---|
| `PR-01` | PROFILE_ROLE_SCOPE | `EXECUTION_PACK_STANDARD.md:148` | Require builder role and WEB environment; profile alone grants no mutation | `ADS-P-AUT` | SOURCE_SCHEMA_ONLY |
| `PR-02V` | PROFILE_ROLE_SCOPE | `EXECUTION_PACK_STANDARD.md:148` | LOCAL_VALIDATION may only perform validation as validator role, never Builder source mutation | `ADS-P-AUT` | SOURCE_SCHEMA_ONLY |
| `PR-02S` | PROFILE_ROLE_SCOPE | `EXECUTION_PACK_STANDARD.md:148` | A LOCAL_VALIDATION run must be bound to the intended exact-SHA validation subject | `ADS-P-AUT` | NO_DIRECT_TEST |
| `PR-02G` | PROFILE_ROLE_SCOPE | `EXECUTION_PACK_STANDARD.md:148` | Only use LOCAL_VALIDATION when a genuine residual local capability gap remains | `ADS-P-AUT` | NO_DIRECT_TEST |
| `PR-03` | PROFILE_ROLE_SCOPE | `EXECUTION_PACK_STANDARD.md:148` | Source edit requires effective Task Pack and accepted Builder Claim authorizing scope | `ADS-P-AUT` | ABSTRACT_MODEL_ONLY |
| `PR-04` | PROFILE_ROLE_SCOPE | `EXECUTION_PACK_STANDARD.md:148` | Continue historic admission until a separately legitimate supersession | `ADS-P-EVO` | ABSTRACT_MODEL_ONLY |
| `PR-05` | PROFILE_ROLE_SCOPE | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:573` | Profile changes environment only, never effective role authority | `ADS-P-AUT` | SOURCE_SCHEMA_ONLY |
| `DP-01F` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:577` | Check the fully enriched object, not an earlier partial dispatch draft | `ADS-P-EVI` | NO_DIRECT_TEST |
| `DP-01S` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:577` | Use the exact schema bytes from the Task's effective project-pinned ADS revision | `ADS-P-EVI` | NO_DIRECT_TEST |
| `DP-02` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:577` | Complete admission before canonical publication | `ADS-P-LC` | NO_DIRECT_TEST |
| `DP-03` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:577` | Map to current pinned schema value only with unique fact-supported resolution | `ADS-P-AUT` | SOURCE_SCHEMA_ONLY |
| `DP-04` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:577` | Reject invalid aliases and unsanctioned profile guessing | `ADS-P-AUT` | SOURCE_SCHEMA_ONLY |
| `DP-05` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:579` | Keep validated object and actual written object identical | `ADS-P-CAS` | ABSTRACT_MODEL_ONLY |
| `DP-06` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:579` | Accept no new canonical Dispatch/Claim mutation | `ADS-P-CAS` | ABSTRACT_MODEL_ONLY |
| `DP-07` | DISPATCH_PUBLICATION | `GITHUB_AGENT_INTERACTION_PROTOCOL.md:581` | Preserve original record, use distinct authorized correction/supersession | `ADS-P-EVO` | ABSTRACT_MODEL_ONLY |
| `TE-01` | TEST_EVIDENCE | `TESTING_STANDARD.md:66` | Qualify coverage only from actual discovered/executed inventory for required scope | `ADS-P-EVI` | SYNTHETIC_DEMO_ONLY |
| `TE-02` | TEST_EVIDENCE | `TESTING_STANDARD.md:66` | Keep omitted scope NOT_RUN; preserve executed subset result | `ADS-P-EVI` | SYNTHETIC_DEMO_ONLY |
| `DG-01` | DAG_DEPENDENCY | `TASK_DECOMPOSITION_STANDARD.md:183` | Do not infer serial source-preparation dependency solely from final join | `ADS-P-DEP` | SYNTHETIC_DEMO_ONLY |
| `DG-02` | DAG_DEPENDENCY | `TASK_DECOMPOSITION_STANDARD.md:183` | Preserve native dependency/ownership/security until authorized resolution | `ADS-P-WRITER-KEYS` | SYNTHETIC_DEMO_ONLY |
| `AR-01` | PUBLIC_SELECTED_PATH | `ARCHITECTURE_DESIGN_STANDARD.md:51` | Identify executable entry→adapter→selected implementation→result and owner of integration check | `ADS-P-CROSS` | NO_DIRECT_TEST |
| `AR-02U` | PUBLIC_SELECTED_PATH | `ARCHITECTURE_DESIGN_STANDARD.md:51` | Keep a material unexecuted architecture seam UNKNOWN, not PASS | `ADS-P-EVI` | NO_DIRECT_TEST |
| `AR-02A` | PUBLIC_SELECTED_PATH | `ARCHITECTURE_DESIGN_STANDARD.md:51` | Assign one bounded selected-path integration check once source dependencies are legally complete | `ADS-P-EVI` | NO_DIRECT_TEST |
| `IM-01` | PUBLIC_SELECTED_PATH | `IMPLEMENTATION_QUALITY_STANDARD.md:43` | Differentiate source/export/load facts from actual selected invocation and observable behavior | `ADS-P-EVI` | NO_DIRECT_TEST |
| `DE-01` | PRODUCT_STAGE_EVIDENCE | `DEVELOPMENT_WORKFLOW.md:141` | Record NOT_RUN, do not promote simulation to Product/Freeze evidence | `ADS-P-EVI` | NO_DIRECT_TEST |
| `DE-02` | PRODUCT_STAGE_EVIDENCE | `DEVELOPMENT_WORKFLOW.md:142` | Stage 1 research cannot substitute post-Freeze Architecture Demo | `ADS-P-LC` | NO_DIRECT_TEST |

Evidence tier counts: {"SOURCE_SCHEMA_ONLY":5,"NO_DIRECT_TEST":11,"ABSTRACT_MODEL_ONLY":5,"SYNTHETIC_DEMO_ONLY":4}. All direct natural-language↔formal-logic equivalence claims remain **NOT_PROVEN**. Source-level checks validate SHA/line/anchor and reject seven intentionally corrupted review records; no actual role/Claim/Publication side effect was exercised by those checks.

## Next executable step, not another batch of toy models

Perform independent, source-first semantic review for these exact **high-risk** atoms: `DP-01S` (effective schema version), `DP-02` (admission-before-publish), `DP-05` (same object at write boundary), `DP-06` (zero accepted mutation), `PR-04` (frozen legacy), `PR-02V/PR-02S/PR-02G` (separate local-validation duties), `TE-02` (unexecuted suite remains NOT_RUN), `DG-02` (native dependency must not be overridden). The reviewer must inspect entire paragraphs and exceptions, then bind or reject model correspondence. If actual contradiction is found, produce the **smallest** falsifiable model and one negative witness; if no effective v4.19 producer is eligible, keep producer/runtime qualification NOT_PROVEN without blocking source review.

**No new CI Gate/Claim authority, ADs normative edit, Local Agent handoff, merge/Freeze or release.**
