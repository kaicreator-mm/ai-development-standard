# ADS #1366 R19 — Source-first adversarial review and repair of R18 over-atomization

**Candidate:** PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` (OPEN/unmerged); exact `IMPLEMENTATION_QUALITY_STANDARD.md:43` Git blob `c37c4a223e21764ebe211f0e7bdd886a2060c5e2`. Cross-owner candidate sources: `ARCHITECTURE_DESIGN_STANDARD.md:51` blob `51fad2c5b35779bcd402eb62cab9a6e563e6dd93` and `TESTING_STANDARD.md:72` blob `746ec1da78b45f2d2c1fa2177549acbcc6587ca2`. Input R18 experimental HEAD `4044557fcf28a9a1b2beda8fcd0d7850f943c633` and ledger blob `79f8b7411b3532bf8098345497a5353e3246e917`.

## What changed after independent-source-style criticism?

The seven R18 facets were useful **draft review prompts**, but counting them as seven disjoint obligations would be incorrect:

1. **`IM43-01` and `IM43-02` overlap:** `SOURCE_PRESENT` and `EXPORTED_OR_LOADED` are alternative *non-qualifying evidence categories*. One selected-invocation qualification rule, with both negative witnesses, covers both. Separate counts would double-count examples.
2. **`IM43-03` needs two counterexamples:** actual selection/invocation can be absent; actual selection may exist yet the observable contract outcome may be wrong. These are independently falsifiable and deserve separate review obligations.
3. **`IM43-04` is NOT an additional workflow state or Gate:** “These are explanatory evidence categories, not new workflow/Gate states” is a **limiting annotation**. Converting it into a novel enforceable Gate or separate proof coverage item would violate the source boundary.
4. **`IM43-05` is conditional and disjunctive:** where only import/activation exists but support is claimed, **repair the real composition OR disclose missing integration evidence**. Honest disclosure keeps the claim unproven, and does not count as a successful behavior test.
5. **`IM43-06` and `IM43-07` remain separate:** Testing/Integration ownership and material installed-package seam evidence have different guards and counterexamples. The latter is **conditional on material public packaging**, not a universal full App/Hidden test requirement.

## Reconciled review candidates (not a formal obligation denominator)

| Candidate | Independently falsifiable claim | Counterexample / limitation |
|---|---|---|
| `IM43-R1` | The claimed supported implementation must distinguish an actually selected invocation from source-present, exported, imported, initialized, or loaded components | A hook is present and registered but routing never selects it; support cannot be claimed |
| `IM43-R2` | Actual selected invocation alone does not establish the promised observable contract outcome; record behavioral evidence or leave missing proof unqualified | The selected hook is invoked but outputs the wrong contract result; the integration claim remains unsupported |
| `IM43-R3` | Choose real composition repair OR an honest NOT_PROVEN/NOT_RUN disclosure; disclosure is not itself proof of feature support | An implementation claims supported with no selected routing evidence and neither repair nor qualification |
| `IM43-R4` | Implementation-quality evidence categorization does not create executable-proof or release certification authority; the applicable Testing/Integration owner owns that evidence | A Builder promotes loaded-source evidence to PASS of a different Testing owner without actual selected contract verification |
| `IM43-R5` | Include a representative clean installed public-entrypoint check for the material seam; a workspace-only import/compile success is not enough | Workspace test passes, clean installed public consumer fails to import required dependency |

**Non-countable guard:** `IM43-SCOPE` — the source's evidence category names are explanatory, not new ADS workflow/Gate states.

**R18→R19:** `IM43-01` and `02` → R1; `03` → R1+R2; `04` → scope guard only; `05` → R3; `06` → R4; `07` → R5. R18 original evidence is **immutable**, this review supersedes only its **proposed segmentation**, not source authority.

## Proof and execution posture

Source-first review and immutable byte/scoping checks pass (see machine receipt). Nine constructed **thought-experiment negative scenarios** distinguish failure conditions; they are *not* executed GitHub or installed-package tests. All five remaining obligations are **source-review candidates**, with actual Python/native proof and live selected-path consumer tests **NOT_RUN**. The first two evidence clauses are source-supported but do **not** automatically have independently proven Natural Language↔Model equivalence; the historical `ADS-P-EVI` relation for `IM-01` was explicitly analogy-only.

This was a fresh adversarial **in-session** read of actual source, **not** an independently signed external human review. It corrects R18 draft granularity, but cannot discharge an external Reviewer requirement. Full ADS atom denominator is `UNKNOWN`; no candidate v4.19 legal adopter/real Claim/CAS publisher is established.

**Decision:** Stop on this one source paragraph after resolving its known counting/owner risks. The next profitable work is comparing a **distinct changed normative paragraph** or executing a **real material public consumer** only when an authorized one is available, not another abstract Bool model or a new global testing framework. Formal standards, GitHub Actions/Gates, Release/Freeze and historical receipts are untouched.
