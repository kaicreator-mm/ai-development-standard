# ADS #1366 — Profile/role source-to-model semantic boundary review

**Review kind:** exact-source-readback semantic coverage **gap analysis**, not an independent proof of formal equivalence. Source candidate: [PR #1365](https://github.com/kaicreator-mm/ai-development-standard/pull/1365) @ `dac263fa4c0ab155406d2f2117459b34322cc988`. ADS Formals experiment input HEAD `6670603a22de9dcf48268d9771fd2825923e65d8`.

## Verified facts

1. `schemas/dispatch.schema.json` Git blob `5d9233b6b881d9d92f66fc6cd5307a05a0fdbe2f`: its `execution_profile` enum contains exactly 7 profiles. Each profile is covered by one `allOf` conditional constraining `role`: `LOCAL_BUILDER` / `WEB_BUILDER` → builder; `LOCAL_VALIDATOR`, `PLATFORM_VALIDATOR`, `CLOSURE_VALIDATOR`, `LOCAL_VALIDATION` → validator; `WEB_REVIEWER` → reviewer. All **7/7 schema source-mapping checks** PASS in the live GitHub readback.
2. Validator condition requires keys `requested_head_sha` and `validation_profile`. Their declared JSON Schema types permit `null`; a required field and a non-null, current authorized value are different propositions. This is **not an observed exploit or policy violation**: a runtime validator must enforce exact-SHA/currentness authorization, but the schema-only check does not prove it.
3. `formal/models/authority/claim.smt2` Git blob `865f1c6876598be9c4eaa4b4f496367324793cca` models `writerIsBuilder`, accepted Claim, authorized write-set and claim currentness as abstract Boolean predicates; `admission-boundaries-r8.smt2` Git blob `73c7ab4d845129b5f6335e275c9e696bc3a5b3d3` adds bounded CAS, publication and role-related assumptions. Neither inspected SMT model names the seven concrete Execution Profile values.
4. `formal/v4.19/r8/source-index.json` links `ADS-P-AUT` to source mutation authority and `ADS-P-EVO` to prospective/frozen history. Those were R11 bounded test subjects, **not direct proof** of all candidate profile-specific permissions and grandfathered version exceptions.

## Disposition

**`SOURCE_SCHEMA_PROFILE_ROLE_MAP=PASS(7/7)`**; **`MODEL_PROFILE_RULE_SEMANTIC_EQUIVALENCE=NOT_PROVEN`**; **`ADS_NORMATIVE_SOURCE_DEFECT=NOT_ESTABLISHED`**.

R11 61/61 Python + 35/35 SMT/TLC strict result remains valid only for its fixed model and candidate Exact-SHA pair. Data-only audit files do not touch any pinned model inputs; **do not rerun the historical suite** for an unchanged tested subject, and do not claim this new audit was a native SMT test.

**Next evidence with highest marginal value:** examine the real candidate controller's effective Task Pack, profile and Claim authorization and historic scope bindings; use an actual contradictory source/consumer counterexample if one exists. Only then decide on a new solver property. No extra Demo rounds, no new Gate or authority mutation.

Machine audit: `PROFILE_AUTHORITY_READBACK.json`. Full ADS rule denominator remains UNKNOWN.
