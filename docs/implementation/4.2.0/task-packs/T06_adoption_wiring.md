# T06 — Adoption & Cross-standard Wiring

Depends on: T02 + T03
Frozen Product: `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9`
Frozen L2: `ea4532cacf87c03689351e43363580e2a14acd95`
Review policy: required
Validation scope: concern/integration
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Integrate v4.2 into repository discoverability/adoption without redefining T01–T05 semantics.

## Allowed write-set
- `standard-manifest.json`
- narrowly selected adoption/project-override/reference docs
- compatibility/migration cross-links in existing standards only where additive and ownership-preserving
- `scripts/test_v42_adoption_wiring.py`

## Required semantics
- both normative standards discoverable from manifest;
- both machine contracts discoverable when applicable;
- adoption remains materiality/risk driven;
- existing Testing/Validation/Release owners remain authoritative;
- v4.4 Deployment is explicitly the future rollout/result owner;
- historical payloads/adopters are not retroactively invalidated;
- Fast Path does not require records for non-material evolution concerns.

## Forbidden
No semantic redesign of T01–T05, no deployment implementation, no Product/Architecture rewrite.

## Completion
Focused integration validation + Fresh Independent Review PASS.