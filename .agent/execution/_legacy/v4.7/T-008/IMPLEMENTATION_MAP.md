# T-008 Implementation Map

This map narrows execution on the exact bound base; it does not enlarge the Frozen Task Pack.

| Surface | Builder action | Boundary |
|---|---|---|
| `docs/implementation/4.7.0/dogfood/**` | Add the minimum durable dogfood scenario/evidence artifacts needed to make fresh-context reconstruction reproducible and auditable. Builder chooses filenames only inside this prefix. | Evidence must state `STATIC_OR_RECONSTRUCTION` vs `REAL_FRESH_SESSION`; no private chain-of-thought; no semantic-owner rewrite. |
| `scripts/test_v47_fresh_agent_dogfood.py` | Add deterministic/table-driven checks for the Frozen acceptance and adversarial cases. | Static/unit execution cannot prove a real fresh Agent/session. |

## Read-only composition inputs

The implementation must consume current durable authority rather than copy or replace it. On the bound base, material inputs include the Frozen T08 Task Pack/L3, T05 `references/PROGRESSIVE_DISCLOSURE_ROUTING.md` + `scripts/resolve_standard_read_set.py`, and T07 `references/V47_SEMANTIC_CONFORMANCE_MATRIX.md` + `scripts/v47_conformance.py` + `scripts/test_v47_semantic_conformance.py`.

Use those surfaces as owners/conformance inputs only. Do not modify them from T08. Higher-currentness repository/GitHub facts defeat stale lower-authority chat/history.

## Required implementation behavior

The durable dogfood scenario must make it possible for a fresh logical Agent/session, starting from durable pointers rather than prior task conversation, to recover at least: pinned ADS/current authority, canonical owner routing, applicable profiles/overrides, current Task/PR/exact SHA/base, Frozen mutation/side-effect authority, Validation/Review requirements, and the next action or blocker.

Negative behavior must be explicit: chat-only facts are non-required; stale lower authority cannot win; transport/account sameness is not independence proof; stale issue/PR/currentness is detected; unavailable REAL execution is not replaced by fixture PASS.

If the Builder lacks a capable real fresh-session environment, retain the REAL scenario as `NOT_RUN`/`BLOCKED` and materialize an exact-subject Validation request after the immutable implementation HEAD/tree exists. Do not fabricate a real transcript and do not infer Validation PASS from deterministic tests.

No T08 implementation in this pack is pre-authored; F1 leaves internal implementation choices to the Builder within the two-path Frozen write set and fixed oracles above.
