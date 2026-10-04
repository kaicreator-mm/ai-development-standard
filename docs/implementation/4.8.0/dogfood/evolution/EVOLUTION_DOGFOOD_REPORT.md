# T-013 Cross-Project ADS Evolution Dogfood Report

## Exact execution binding

- Task: `T-013` / Issue `#519`.
- Integration target at Builder admission: `version/v4.8.0@4c49487423e4aabc7bb1e296da74eee2a6f55da8`, tree `4cb78609ef805559e3fcd023dc4215a7e596d149`.
- JIT Execution Pack: `188465e660bd0e418d91a2167367b3af3bdd919b`, tree `7856fe48cce5436393ccb0d02b0979d2c3932fdd`.
- Task Pack blob: `9b96b567e8b0fec23cab08502f5dd9a907c4ef59`.
- L3 blob: `8af06fd5bd7237b260fe478c23cb410c0e15898f`.
- Structured evidence: `EVIDENCE_MATRIX.json`.
- This Builder output is evidence production only. It is **not** independent Validation, Fresh Review, Version Closure, Release Qualification, or authority to amend ADS.

The live version target was re-read immediately before Builder mutation and still matched the admitted exact target. Each preflight stream was also re-read live; predecessor verdicts below are retained only as historical exact-subject evidence.

## Rebound REAL evidence streams

### S1 — ADS #469 / UX Harness bounded-agent dogfood

The live source remains the non-normative ADS evidence Issue `#469`, with durable evidence anchor `#469@5925124956`. At that exact anchor, multiple bounded lower-cost Builder tasks had reached independent real-host Validation and fresh high-capability Review, with several paths merged. The source also records repeated zero-clarification executions and bounded edit/test loops.

This is useful task-class execution evidence, but it does **not** establish an economic or universal routing policy. Comparable strong-vs-lower-cost token/cost/latency/rework baselines were not measured, fresh high-capability Review still surfaced material nonblocking findings, and the source itself terminates at `MORE_EVIDENCE`.

**Classification:** `BOUNDED_AGENT_DOGFOOD` + `EVIDENCE_GAP_FOR_ECONOMICS_AND_UNIVERSAL_ROUTING`.

**Disposition:** `MORE_EVIDENCE`.

### S2 — domain-ux V007-003

The preflight anchor `domain-ux #162@5970478893` was a historical `CHANGES_REQUESTED` review at exact head `a2ddaf592b5bc7a699209b24cc0b991521436cf6`. It identified two bounded P1 implementation defects and one P2 durable-evidence gap.

Live rebinding shows that those findings were closed by bounded repair and evidence backfill. A successor review subject was then correctly superseded after the version base moved rather than transferring the old verdict. The currentness-rebound subject at exact head `bb1f5dc651b48d8626908483a26b70d2af484ae2`, tree `f778ac3933025dd1c31caa7b3210c1dc5f5e603a`, received a genuinely fresh independent PASS at `#168@5973293956`; PR `#161` was subsequently merged as `ff57c34d46e8808643cdb8a5d995dfe0017665b5`.

This is strong evidence that the observed failures were **project/evidence defects successfully handled by existing currentness, repair, and review gates**, not a durable ADS standard defect.

**Classification:** `PROJECT_DEFECT` + `EVIDENCE_GAP` + `CURRENTNESS_REBIND_SUCCESS`.

**Disposition:** `NO_CHANGE`.

### S3 — runx RT002

The preflight anchor `runx #143@5953993544` was a historical `CHANGES_REQUESTED` security review at exact head `2caf4f0d3f779aad124520d3c3c1047ac0cc1b0d`. It found bounded project security-contract defects plus an environment/evidence-coverage gap. A supplementary WSL run exercised the Windows-skipped symlink case. Successor repair/review rounds then addressed implementation semantics and stale L3 wording rather than transferring the predecessor verdict.

Live rebinding reaches final exact head `1362a74413a2b77c18872dfb2c2d69dce4552f3d`, tree `be2092be48eefe71e3f064200d1522076fdc697f`; `#143@5958381492` is `REVIEW_PASS` with P0/P1/P2/P3 all zero, and PR `#143` was subsequently merged as `2189c48459ec954fcc11a1aea701fa0d8b20445d`.

The repair sequence demonstrates that serious project-local defects and evidence gaps can be caught, rebound, repaired, and independently reviewed under the existing ADS mechanisms. It does not establish an ADS-owned repeated-friction defect.

**Classification:** `PROJECT_DEFECT` + `ENVIRONMENT_OR_EVIDENCE_COVERAGE` + `DOCUMENTATION_CURRENTNESS`.

**Disposition:** `NO_CHANGE`.

## Cross-project challenge

Three materially distinct `REAL` streams are available; no synthetic stream is needed to satisfy T-013.

The strongest apparent common pattern is exact-subject/currentness discipline plus independent Validation/Review. That pattern fails the promotion test for `STANDARD_FRICTION_CANDIDATE`: in S2 and S3, existing ADS-style gates were the mechanism that prevented stale verdict transfer, surfaced local defects, and forced bounded repair. Treating successful enforcement as evidence that the standard itself is defective would invert the evidence.

The following promotions are therefore rejected:

- bounded lower-cost execution -> universal model/provider capability;
- unmeasured execution -> economic savings;
- project implementation/security defect -> ADS standard defect;
- environment/evidence-coverage gap -> ADS standard defect;
- historical verdict -> successor-SHA verdict;
- repository/GitHub visibility -> `PUBLISHABLE`.

No evidence here justifies a numeric/global threshold, automatic standard mutation, or a blanket strong-to-low-cost routing rule.

## Privacy, publication, and external claims

The two project streams are private-project evidence and are represented here only by the minimal durable identities, result classes, and merge/review facts needed for T-013. Their code or private evidence bodies are not copied. They are `PRIVATE_PROJECT_INTERNAL_REFERENCE_ONLY` and `external_claim_eligible=false`.

ADS #469 is also fail-closed for publication: GitHub visibility is not treated as explicit `PUBLISHABLE` authorization. Therefore **none of the three streams authorizes a new external/generalized claim** from this artifact.

Any future public or external claim must first obtain explicit publication eligibility and exact-subject REAL evidence appropriate to that claim. Until then it is `NOT_RUN|BLOCKED`, not synthetic PASS.

## Result

```text
T013_REAL_STREAMS=3
T013_SYNTHETIC_STREAMS=0
REPEATED_CROSS_PROJECT_STANDARD_FRICTION=NOT_ESTABLISHED
ADS_EVOLUTION_CANDIDATE=NONE
T013_DISPOSITION=NO_CHANGE
MORE_EVIDENCE_REQUIRED=ECONOMICS|BLANKET_ROUTING|REPEATED_ADS_OWNED_FRICTION|EXTERNAL_GENERALIZED_CLAIMS
ECONOMIC_SAVINGS=NOT_MEASURED
BLANKET_STRONG_TO_LOW_COST_RULE=NOT_SUPPORTED
STANDARD_AUTO_AMEND=NONE
EXTERNAL_GENERALIZED_CLAIMS=NOT_AUTHORIZED
```

`NO_CHANGE` is the bounded ADS-authority result: no repeated standard-owned failure survives the cross-project false-positive challenge. `MORE_EVIDENCE` remains the correct route for the broader economic/routing hypotheses in S1 and for any future evolution candidate that would require repeated ADS-owned friction.

The next gate is independent exact-subject cross-project currentness/privacy/evidence-strength Validation using `VALIDATION_HANDOFFS.md`. A genuinely Fresh Independent Review may occur only after that Validation passes on the same candidate HEAD.
