# T-010 JIT Execution Contract

## Exact authority
- Issue: #729 / T-010 Gate-Owned Evidence Binding / Currentness Integration. Risk: critical/high. L3: high-capability owner map required.
- Base: `version/v4.9.0@f4fe88542de9d3f5376498e62778e2353391bc57`, tree `82ff224731e854079bdbd40a12eeffe00186b62c`.
- Frozen Product (`a8ec7030...`), Frozen L2 (`bd41ea01...`), Frozen Task DAG v0.2 (`b9fe0cc7...`), current Task Pack and L3 remain authoritative.
- Immutable DAG v0.1 `### T-010` (blob `4f358ba2...`) is the normative concern.
- T-005->T-010->T-014 serializes Release-owner writes when Release surfaces are touched — this lane touches NO Release surfaces (owner-map document only); Release applicability decision BINDING is wired by reference to the T-005 owner, not redefined.

## Required result
Make the Frozen L2 evidence/currentness matrix EXECUTABLE through existing owners without a generic PASS-equivalence engine. Own ONLY cross-owner wiring/explicit owner rules for:
- Assurance Plan currentness (consumes T-002 contract);
- Review successor/full/complete-delta semantics and carried findings;
- existing Validation impact decision use (when does a prior Validation impact a new candidate);
- Hidden/Closeout/RQ fresh/current candidate rules;
- Release applicability decision binding (by reference to the T-005 owner);
- downstream dogfood candidate binding.
Deliverable: the executable owner map (reference doc) + transfer/currentness negative-oracle tests + fixtures. Owner-specific evidence meaning stays canonical; this lane mints NO PASS and no generic equivalence.

## Hard boundaries
- No generic PASS-equivalence engine; owner-specific Review/Validation/Hidden/Closeout/RQ/Release evidence meaning remains canonical (cite owners, never redefine).
- No Product/L2/DAG mutation; frozen blobs resolve unchanged at candidate.

## Mutation authority
Only the three Builder write-set paths in MANIFEST plus the six immutable `.agent/execution/T-010/**` planning files.
