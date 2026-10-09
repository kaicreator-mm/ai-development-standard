# ADS v4.11 — A/B/C Product Acceptance Trace Probe (non-authoritative)

> **STAGE-1 ISOLATED SEMANTIC PRODUCT EVIDENCE ONLY.**
> This is a fixed, synthetic Product acceptance probe against the reviewed v4.11.0 Draft PRD v0.3. It is **not** a new normative ADS owner, not a Stage-2 Architecture Research Demo, not formal L2, not an implementation acceptance/PR gate, and not a runnable GitHub Agent/Claim/Review/Release implementation. No Product Freeze has been authorized.

## Pinned provenance

- Canonical PRD Product source: `#938@6067371136`, Git blob `d30f202e8ea662731ff8a4f2ad1ad88cfc5bb179`.
- PRE-FREEZE Product evidence parent: `#945`; Product authority decision remains `#943` **awaiting explicit act**.
- Independent Product R3 `#941@6067535335 PASS` and Git transposition `#942@6068127988 PASS` validate the **PRD**, not this probe.
- Source base: `34df09a2433aec5523ab80c90e885f6d9fc78803`; experimental branch `research/v4.11.0-abc-product-probe`.
- Executed Python source blob `5fcd8e1a8408233f5694fa3c39994357b617ca8a` (SHA256 `3076bbefbbb50bba0681efe335b1be032a2363567178a12b32a47185d4b10bd8`).
- Original 28-test unittest blob (updated) `9fce01fc0fe5470b64de52919b9e8f2f794a1ee2` (SHA256 `6b6edb36f8d25badaae3cb27bc6cf10c26ebc774b56a93b6385510d4290a8c58`).
- Metamorphic unittest blob `319e44dcfc16d6954b27b7650c67f136dd101c86` (SHA256 `495f19181ee80cfd58452d3ec3be56c01fad92c11a3c22d1154260a26579e657`).
- Environment actually executed: Python 3.13.5 / Linux x86_64 container; no real user LOCAL Build Host, real private Hidden, GitHub credential actions or actual external writes.

## Reproduce

In this directory, with Python 3.10+ and no dependencies:

```bash
python3 -m unittest discover -p 'test_product_trace*.py' -v
```

Observed on the exact three blobs above: **42 tests, all OK**, exit 0; no external systems touched. An additional 14-case metamorphic suite covers 4,096 synthetic job subsets and 20,480 adoption profile samples. The earlier #945@6081926269 28/28 terminal remains historical and is not overwritten. A successful synthetic suite is a reproducible *Product oracle model observation*, not evidence that ADS production software implements these rules.

## Behavioral probes represented

| Perspective | Product fixture class | Checked behavior |
| --- | --- | --- |
| A / C | `J03+J06+J07+J08` X01, A0 vs A4 | Security + migration recovery + bugfix regression + external authorization + human approval obligations compose; adoption cannot waive |
| A | `J01/J03/J04/J05/J10/J11/J12` | Product evidence, feature contract, spec delta/behavior, incident recovery, retirement and reuse source/license cannot silently vanish |
| B | Claim and role eligibility | Duplicate protected key denies; different keys allowed; unproven real-host or Fresh independence denies |
| B / C | Human veto and lost ACK | DENY/WITHHOLD persists; unauthorized successor and blind retry rejected; effect reconciliation must prove NOT_APPLIED or idempotency |
| B / C | Reviewer conflict | Contradictory accepted/current same-HEAD PASS/CHANGES_REQUESTED blocks merge absent verified arbitration |
| A / B / C | Untrusted transport | Authenticated GitHub or MCP text cannot be promoted to authority or credential access; inert A2A data remains data |
| A / C | Release evidence | CI-visible/PR success not a substitute for Hidden or Release Qualification |
| C | `J09+J10+J11+J12` | Incident/retirement obligations cannot be lost simply because all visible release+reuse proofs are listed |

`DEMO_ALLOW`, `DEMO_DENY`, `DEMO_UNVERIFIED` are **local output labels**, **not** real ADS Gate states. Input `verified_evidence` and `owner_authorized` booleans are **hypothetical trusted ground truths supplied by controlled unit tests**; the probe **DOES NOT authenticate or verify** these facts. For instance, a caller can lie about `real_host_evidence_verified` — actual ADS must independently bind evidence to authoritative exact SHA/actor/host metadata.

## R2 Product-model counterexamples found and repaired

A new **author-side** red-team probe found three semantic bugs in this non-normative model:
1. A conflicting Review on another HEAD improperly blocked merge of an unrelated current target. Now synthetic merge decision binds `action.head` and filters accepted/current decisions by that exact head.
2. A CLAIMED event without `key` raised `KeyError`. Now it emits `CLAIM_PROTECTED_KEY_MISSING` and `DEMO_UNVERIFIED`.
3. Completely empty/unclassified trace returned `DEMO_ALLOW`. Now it emits `UNCLASSIFIED_EMPTY_TRACE`.

The model now also treats missing merge target identity as `UNVERIFIED`, and a required independent Review with no current PASS as `UNVERIFIED`. These defects are evidenced **only in the experimental model**, not the real ADS owners.

**Metamorphic scope:** all 4096 subsets of the declared 12 job labels are compared against singleton obligation union in this synthetic model; all 20480 subset×A0–A4 combinations preserve the same synthetic hard requirements. This does **not** establish actual software completeness, prove arbitrary context combinations, or bind external evidence sources.

## Explicit limitations and follow-up

1. This module **models only a bounded subset** of mandatory S01–S18 and X01–X08 and never asserts comprehensive P1/P2/P3 PASS or dynamic coverage closure. Every `J01–J12` domain, actor credential and evidence production path requires actual canonical owner/proof treatment later.
2. No real concurrent GitHub Claim, atomic admission, Version-branch rebase, deployment, true human signature, Review arbitration or external-effect reconciliation occurred. The data is synthetic by design.
3. This is not intended to be merged directly into normative ADS: L2 after explicit authorized Product Freeze must decide whether a machine conformance verifier, golden fixtures or existing owner-owned validators are the correct composition mechanism; **do not create a second state engine**.
4. Product behavior contradiction discovered? Record it to `#938` for scope/authority decision, without self-amending PRD. Mechanics-only UNKNOWN stays for the later L2 study.
5. Neither v4.10 `version/v4.10.0`, `main` nor `planning/v4.11.0-product-freeze-prep` was modified by this study. An experimental Draft PR is for isolated evidence review, **not integration authorization**.

## Interpretation

```ini
ACTUAL_TESTS=42/42_PASS (synthetic Product probe only)
NORMALIZED_BEHAVIORAL_PROBE=PASS_WITH_CLEAR_LIMITS
PRODUCTION_ADS_BEHAVIOR_VERIFICATION=NOT_RUN
REAL_HOST_VALIDATION=NOT_RUN
FORMAL_HIDDEN_VALIDATION=NOT_RUN
PRODUCT_FREEZE=NO
FORMAL_L2_TASK_DAG_IMPLEMENTATION=NOT_AUTHORIZED
P1_P2_P3_RELEASE_PROOFS=NOT_RUN
```
