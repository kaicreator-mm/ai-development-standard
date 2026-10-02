# T06 — Adoption & Cross-standard Wiring

Depends on: T02 + T03
Frozen Product: `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9`
Frozen L2: `ea4532cacf87c03689351e43363580e2a14acd95`
Review policy: required
Validation scope: concern/integration
Validation owner: T06
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Integrate v4.2 into repository discoverability/adoption without redefining T01–T05 semantics.

## Allowed write-set
- `standard-manifest.json`
- `templates/golden/STANDARD_COVERAGE.json`
- `templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md`
- `templates/golden/ANTI_PATTERNS.md`
- `templates/project/.dev-standard/PROJECT_OVERRIDES.md`
- `docs/implementation/4.2.0/MIGRATION_ADOPTION.md`
- `scripts/test_v42_adoption_wiring.py`

## Amendment note — #331
This explicit write-set closes a planning-authority gap discovered before T06 implementation mutation. `GOLDEN_TEMPLATE_STANDARD.md` requires every new active normative standard added to `standard-manifest.json` to update the machine-complete coverage registry plus maintained positive/forbidden/rationale guidance in the same change. These Golden paths are therefore part of T06 central wiring, not retrospective authorization for unrelated writes.

`templates/GOLDEN_INDEX.md` is intentionally not authorized because v4.2 does not introduce a new reusable critical execution surface that requires an index row.

## Required semantics
- both normative standards discoverable from manifest;
- both machine contracts discoverable when applicable;
- every newly active normative standard has exactly one Golden coverage record plus maintained positive/forbidden/rationale guidance;
- adoption remains materiality/risk driven;
- existing Testing/Validation/Release owners remain authoritative;
- v4.4 Deployment is explicitly the future rollout/result owner;
- historical payloads/adopters are not retroactively invalidated;
- Fast Path does not require records for non-material evolution concerns.

## Adversarial minimum
- manifest/Golden discoverability MUST NOT become mutation or Product authority;
- Golden coverage MUST NOT duplicate normative semantics;
- optional/non-material evolution concerns MUST NOT force empty records;
- historical payload/adopter validity MUST NOT be retroactively weakened;
- compatibility/migration semantics MUST NOT absorb Deployment result ownership.

## Forbidden
No semantic redesign of T01–T05, no deployment implementation, no Product/Architecture rewrite, no `templates/GOLDEN_INDEX.md` mutation, and no write outside the explicit allowlist.

## Completion
Focused integration Validation owned by T06 + required Fresh Independent Review PASS on exact HEAD.

## L3
`docs/implementation/4.2.0/L3_REFERENCE_PACKS.md#t06--adoption--cross-standard-wiring`

## Failure handling
If another central/Golden path proves materially required, stop and create an explicit authority amendment before writing it. Technical necessity, CI or Validation does not broaden this Task Pack.
