# ADS v4.12 — Project Adoption Quick Guide (candidate R0)

> **Non-normative preview.** Frozen v4.12 Product scope is PRD R3 blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`; Architecture §12 is not yet frozen. Until a real v4.12 Release and project-specific adoption record exist, use the **currently pinned/approved ADS baseline** for all permissions, required gates, Issue/Claim/Review/Validation/Release decisions. You may shadow-evaluate v4.12 as a future proposal; it cannot authorize new planning-stage source writes.

## One-page workflow for adopting projects

| Stage | Smallest lawful path | Source/decision/output to keep |
|---|---|---|
| 0. Version and authority | Pin the project ADS version, Product and version integration mode, existing frozen requirements and owner policies | `project / ADS exact tag or commit / current Product-L2-Task DAG pins` |
| 1. Product L1 | Choose `INLINE` (default for simple), `BOUNDED_WORKLIST` (few real dependent questions), or `EXPLICIT_DAG` (complex ownable dependencies). Stop when material uncertainties have sufficient source-based evidence. | Product question, real evidence, negative case, owner decision and Product Freeze if required |
| 2. L2 | Inspect current architecture and proven reusable work before any Demo. Classify `STATIC_EVIDENCE_SUFFICIENT | EXECUTABLE_DEMO_REQUIRED | BLOCKED | ARCHITECTURE_CONTRADICTION`. | Source/ADR alternatives, unresolved high-impact UNKNOWN and exact L2 Freeze |
| 3. Planning Scaffold (prospective v4.12 only) | Once the project **legitimately adopts** v4.12 and meets its stage authority: existing canonical `type:planning` Work Item with complete allowed/forbidden paths and Review Policy; **accepted Claim before any actual source write**. Produce only necessary buildable seams and honest unimplemented stubs. | Actual integrated scaffold Git SHA/tree, reviewed public contracts, original accepted Claim, permitted tool effects |
| 4. Implementation DAG-I | Co-evolve single-source Task-side bindings to structural Scaffold anchors, then check Product/L2↔SF↔DF before **paired planning Freeze**. Native GitHub Issue Dependencies are authoritative only after implementation DAG materialization; `INFORMS` is not `BLOCKED_BY`. | Frozen DF, validated SF material scope/owner-approved exact exemptions, derived/recomputed mapping, canonical Task Issue IDs |
| 5. Builder / Reviewer / Validator | Dispatch from current native Issue READY with accepted CAS Claim; one coherent concern/PR. Reuse existing functions/helpers where semantics match, don't over-abstract. Select `required/recommended/not-required` Review under owner risk policy. Validate exact changed subject and required negatives. | Accepted Task Claim, write set, PR review, actual test exit/skip, current evidence |
| 6. Version closure | Reuse exact assertion-level evidence where valid; do **one** required final candidate regression unless new material impact justifies more. Verify real integrated customer path separately from Scaffold structural wiring. | Candidate Git SHA, actual Release-owned E3/Hidden/CJ/packaging proofs or explicit NOT_RUN/UNKNOWN, owner Release qualification |

**Operational invariants:** no Claim → no source execution; a creator cannot self-approve a required independent Review; a generated mapping can't become source-owner authority; unknown changed paths are material/HOLD; a DAG-only document exemption from SF tree does not exempt DF/currentness; a stub is not a feature PASS; a successful PR/CI/test fixture is not Release PASS; human DENY and real E3 requirements cannot be waived by confidence or ROI.

## Existing vs new project

- **New project:** a right-sized actual Scaffold can precede the complete implementation DAG **only after** qualified v4.12 adoption and legitimate accepted Work Item/Claim. Exposed schema/trust changes still require applicable owner Review. Package installation or network effects need separate execution authorization.
- **Existing project:** prefer current source, existing interfaces, tests and history. Do not regenerate the entire source tree merely to demonstrate v4.12; make only justified bounded seam changes under actual Task authority.
- **Lightweight A0/A1 WEB-only project:** may manually inspect Git object/path and negative/owner proofs where existing adoption policy permits; do not falsely report the v4.12 reference machine checker as run. For A2+ automated claim, attach actual invocation and exact-source logs.

## Optional shadow-feedback packet BEFORE v4.12 release

A project on an earlier pinned ADS version may compare its **real** workflow against this *proposal* and report:

```text
Project / pinned approved ADS version:
Project source/review subject exact SHA:
Actual current problem / missed proof / repeated work:
Proposed v4.12 clause:
Observed evidence (Issue / PR / logs / file):
Counterexample / risk floor:
Classification: ALREADY_SATISFIED | NEEDED_DELTA | DEFER | UNKNOWN
Suggested narrow ADS owner/standard file:
Measured duration/Host usage: REAL_VALUE_WITH_LOG | UNKNOWN
```

This form **never** makes a preview clause authoritative. Real adoption waits for a qualified v4.12 baseline, a project-owner adoption decision and a project-local exact pin. Do not create shadow Issue Dependencies or use a separate claim database.

## Candidate handoff and quality

Delivery sequence is defined in [ADS-first Delivery Pack](./V412_ADS_FIRST_DELIVERY_PACK_R0.md). The ADS standard's own conformance suite must include one source-pinned new and one mature fixture with required negative currentness and mapping assertions; **neither fixture nor a generated app's release is the ADS product itself**. Record actual machine results only when they are executed. External project applications become post-qualification feedback streams rather than compulsory prerequisite apps.

```ini
DOCUMENT_STATUS=PREVIEW_NON_NORMATIVE
PRODUCT_R3=FROZEN_EXACT
L2_FREEZE=NOT_RECORDED
V412_VERSION_RELEASE=NOT_QUALIFIED
EXTERNAL_PROJECT_PERMISSION=CURRENT_PINNED_ADS_ONLY
```
