# V410-T07B Evidence Input Inventory — Core-Feature-Freeze Product-Decision Support

Pack: `V410-T07B-LOCAL-EVIDENCE-INPUT-INVENTORY-R1`
Base: `30334e8c7b90a327f8597b86c88c785b98df07f7` (HEAD, origin/version/v4.10.0 tip)
Task Pack: `docs/implementation/4.10.0/TASK_PACKS_R1.md#V410-T07B`
Parent Issue: `#863`

This inventory supports — and never makes — the Product-authority decision
`ADS_CORE_FEATURE_FREEZE_ELIGIBLE=YES|NO`. It enumerates each evidence input the decision
needs, why it is required, where a fresh observer re-derives it, whether it exists at
base_sha, and which actors may not manufacture it. Availability is a fact statement at
`base_sha`, not a gate verdict.

## Decision authority (normative — read first)

`ADS_CORE_FEATURE_FREEZE_ELIGIBLE` is an explicit **Product-authority decision** under
PRD §1.1: only the human Product authority owner, or an explicitly delegated actor within
bounded authority, may set it, with the decision and evidence durably recorded.

CI, Review, Release READY, Version Closure, Controller state, Reviewer judgment and
model votes cannot manufacture `ADS_CORE_FEATURE_FREEZE_ELIGIBLE=YES`. They are evidence
inputs only. An evidence-backed `NO` is a legitimate outcome of a successfully delivered
v4.10 (PRD §1.1, §19.4); `NO` must identify the blocking evidence or justified remaining
core concern. Version Closure alone never implies `YES` (PRD §19.4, §20, §22 item 8).

## Input ledger

### A. Decision semantics and Product-authority inputs

| Input | Why required | Source / producer | Reconstructibility | Availability at base_sha | Who may NOT manufacture it |
|---|---|---|---|---|---|
| A1. Frozen Product authority PRD v0.4 (blob `b0b9906035eee253aad4bff0274d3d4c8f90b9db`) | The freeze decision applies only to the frozen Product subject; a material Product-boundary change requires successor thaw/amendment | `docs/implementation/4.10.0/PRODUCT_FREEZE.md` (record `#837`); PRD at `docs/implementation/4.10.0/PRD.md` | Fresh observer runs `git rev-parse HEAD:docs/implementation/4.10.0/PRD.md` and compares to the blob recorded in PRODUCT_FREEZE.md; checks status header FROZEN_V0_4_CURRENT | AVAILABLE | CI/Controller/model vote cannot re-freeze or thaw Product semantics |
| A2. PRD §1.1 eligibility semantics (bounded meaning of YES/NO; minimum evidence inputs 1–5; delegation bounds) | Defines what the decision means and the minimum input set the Product authority must have | `docs/implementation/4.10.0/PRD.md` §1.1 | Read PRD §1.1 at the frozen blob; verify blob equality as in A1 | AVAILABLE | Any non-Product actor cannot redefine YES/NO semantics |
| A3. Fresh external Product re-review `#833@5993569646` PASS and current refreeze record `#837` | Evidence that the Product subject itself passed genuinely Fresh re-review under §22 criteria (item 8 covers §1.1 decision semantics) | `docs/implementation/4.10.0/PRODUCT_FREEZE.md` (lineage block); GitHub review `#833`, refreeze `#837` | Read PRODUCT_FREEZE.md header + lineage; open `#833`/`#837` on GitHub; verdict is attributable only to the exact PRD blob reviewed | AVAILABLE (as historical, exact-subject-bound evidence) | Review PASS cannot itself become Product Freeze; a model/reviewer vote cannot create authority |
| A4. PRD §22 Product Freeze criteria v0.4, item 8 (§1.1 gives the decision bounded meaning, minimum evidence inputs, Product-authority semantics, allows evidence-backed NO) | The criterion that legitimizes this decision path | `docs/implementation/4.10.0/PRD.md` §22 | Read §22 item 8 at the frozen blob | AVAILABLE | — |

### B. Requirement-linked acceptance evidence (PRD §19.1)

| Input | Why required | Source / producer | Reconstructibility | Availability at base_sha | Who may NOT manufacture it |
|---|---|---|---|---|---|
| B1. R1 discovery/proportionality falsification evidence | §1.1 minimum input 1 requires all §19 acceptance evidence on the applicable release subject | Task validation suites (T01A/T01B) + acceptance map produced by V410-T07A + integration evidence by V410-T08A | Fresh observer reads the T07A acceptance-evidence index, then re-runs the mapped R1 validation commands on the exact release subject | PENDING — owning concern V410-T07A (acceptance wiring), completed only with V410-T08A integration | Builder self-certification; CI green; Reviewer/model vote |
| B2. R2 owner/lifecycle convergence evidence | §1.1 minimum input 2: no unresolved material duplicate/contradictory authority | Owner-convergence matrix from V410-T06A; closure evidence via V410-T07A map | Fresh observer reads T06A owner-convergence matrix and re-derives closure status from current owners at the release subject | PENDING — owning concern V410-T06A (central owner discovery) | T08A integration Builder; Controller state |
| B3. R3 collaboration/responsibility evidence | §19.1 active requirement | Task validation suites (T02A) + T07A map + T08A integration | As B1, via T07A index for R3 | PENDING — owning concern V410-T07A | Builder self-certification; model vote |
| B4. R4 human-control + automation-first quality evidence | §19.1 active requirement | Task validation suites (T02A/T03A) + T07A map + T08A integration | As B1, via T07A index for R4 | PENDING — owning concern V410-T07A | Human line-by-line review absence cannot be auto-passed; CI cannot substitute for the authority-sensitive human-control case |
| B5. R6 proportional assurance / repair convergence evidence | §19.1 active requirement | Task validation suites (T04A) + T07A map + T08A integration | As B1, via T07A index for R6 | PENDING — owning concern V410-T07A | A retry counter or CI success cannot convert non-convergence into PASS |
| B6. R7 Agent-oriented granularity evidence | §19.1 active requirement | Task validation suites (T03A/T03B/T05A) + T07A map + T08A integration | As B1, via T07A index for R7 | PENDING — owning concern V410-T07A | Fake parallelism/overlapping write sets cannot be treated as legal concurrency by a Builder summary |
| B7. R11 projection/conformance evidence | §1.1 minimum input 3: no unresolved material prose↔machine contradiction | V410-T06B positive+negative conformance; T07A map | Fresh observer runs the central conformance suites named by T06B and reads the T07A R11 mapping | PENDING — owning concern V410-T06B | A stale passing verifier cannot manufacture this input |
| B8. R12 discoverability/compatibility/lineage evidence | §1.1 minimum input 5: exact-subject/currentness/compatibility truth | V410-T06A/T06B + T07A acceptance map | Fresh observer reconstructs from a clean observer context via T06A discovery surfaces and T07A R12 mapping | PENDING — owning concern V410-T06A/V410-T07A | Historical qualification must not silently bind to a successor |

### C. Required gate inputs (PRD §19.2)

| Input | Why required | Source / producer | Reconstructibility | Availability at base_sha | Who may NOT manufacture it |
|---|---|---|---|---|---|
| C1. Frozen L2 Architecture authority v0.2 (blob `b03f12700153e128f4a4c02b7e8d7adf960fd7d3`) | §19.2 gate: Frozen L2 authority | `docs/implementation/4.10.0/L2_FREEZE.md` (record `#842`) | Read L2_FREEZE.md status; verify `git rev-parse HEAD:docs/implementation/4.10.0/L2_ARCHITECTURE_EVIDENCE.md` equals the recorded blob | AVAILABLE | CI/Controller/model vote cannot re-freeze L2 |
| C2. Frozen refined Task DAG R1 (`#848`) | §19.2 gate: frozen/materialized Task DAG | `docs/implementation/4.10.0/REFINED_TASK_DAG_FREEZE_R1.md` | Read the freeze record header and frozen edge set; compare against GitHub native Issue Dependencies when materialized | AVAILABLE (planning authority; execution issues not yet materialized) | Conceptual relatedness cannot create or drop a DAG edge |
| C3. Required Task/PR Validation on exact subjects | §19.2 gate; evidence must bind to exact subject/currentness | Per-task Validation records; integration Validation `V410-V01` | Fresh observer re-runs the validation commands named in each Execution Pack TEST_MATRIX on the exact candidate | PENDING — owning concern per-task Validation + V410-V01 | A Validator must not self-certify; task Validation must not fabricate release readiness |
| C4. Independent Review per selected policy/risk | §19.2 gate; all eight Tasks initially `required` | Per-task Fresh Independent Review records on the exact candidate | Fresh observer reads each Review record and its exact-subject binding | PENDING — owning concern per-task Review policy | Reviewer/model vote is evidence, not authority; verdicts do not transfer across subject drift |
| C5. Integration / currentness evidence | §19.2 gate; T08A assembles the dependency-complete visible candidate | V410-T08A integration evidence | Fresh observer runs full visible regression/conformance on the integrated candidate | PENDING — owning concern V410-T08A | Integration Builder cannot hide semantic fixes or fabricate Hidden/RQ PASS |
| C6. Version Closure / Hidden / Release Qualification (when required by Release authority) | §19.2 gate; later than this pack by design | Release authority surfaces, after closure | Fresh observer reads the durable closure/release records when they exist | PENDING — owning concern Release authority (downstream of V410-V01) | Closure/Release READY/CI cannot manufacture the freeze decision YES |

### D. Decision-path visibility inputs

| Input | Why required | Source / producer | Reconstructibility | Availability at base_sha | Who may NOT manufacture it |
|---|---|---|---|---|---|
| D1. Release-blocker visibility for PRD §19.3 blocker set | §19.3 blockers must be visible without redefining Release authority; §1.1 input 1 depends on it | Acceptance-evidence index / blocker projection from V410-T07A | Fresh observer reads the T07A blocker projection and maps each §19.3 bullet to a durable evidence producer | PENDING — owning concern V410-T07A | T07B itself cannot create this projection; no second Release verdict may be introduced |
| D2. V410-V01 self-dogfood Validation output (15 required verdict lines) | Independent validation of the dependency-complete candidate, including subject 12 (freeze decision remains Product authority) | `V410_V01_VALIDATION_CONTRACT.md` defines output; Validator produces it after T08A | Fresh observer reads the durable `VALIDATION_ID=V410-V01` output block bound to `CANDIDATE_HEAD` | PENDING — owning concern V410-V01 (contract FROZEN, NOT_YET_DISPATCHABLE at base_sha) | Integration Builder cannot manufacture its own Validation PASS; Validator must report BLOCKED/NOT_RUN, never infer PASS |
| D3. Dogfood evidence (Minimum-ADS and Advanced-ADS paths) | PRD acceptance requires both paths remain possible; §19.1 cross-cutting acceptance | V410-T07A acceptance map (Minimum/Advanced dogfood refs) + V410-T08A dogfood runs | Fresh observer follows the T07A dogfood refs and re-runs the recorded dogfood checks | PENDING — owning concern V410-T07A/V410-T08A | Agent summaries cannot self-certify dogfood success |
| D4. §10.4 disposition of reachable legacy/backlog ambiguity | §1.1 minimum input 4 | Legacy/stale-owner classification from V410-T06A | Fresh observer reads the T06A stale/legacy classification matrix | PENDING — owning concern V410-T06A | Silently reachable stale owners cannot be ignored by Controller convenience |
| D5. The explicit, durable Product-authority decision record | The decision itself, recorded with evidence, per §1.1 | Human Product authority (or explicitly delegated actor) — outside any Task | Fresh observer reads the durable record naming the deciding authority, the evidence set used, and YES/NO | PENDING — by design; owning concern Product authority | CI, Review, Release READY, Version Closure, Controller, Reviewer and model votes cannot manufacture ADS_CORE_FEATURE_FREEZE_ELIGIBLE=YES |

## Availability summary

- AVAILABLE at base_sha: A1, A2, A3, A4, C1, C2 — the frozen planning/authority inputs and the normative decision semantics.
- PENDING at base_sha: B1–B8, C3–C6, D1–D4 — produced by V410-T06A/T06B/T07A/T08A/V410-V01/Release authority.
- PENDING by design: D5 — only Product authority may produce it.

## Negative invariants for this inventory

- `ci_review_release_cannot_manufacture_freeze_yes`: no CI/Review/Release/Closure/Controller/Reviewer/model-vote surface may be listed as a producer of the decision input D5.
- `no_new_release_state_dimension`: this pack introduces no second Release verdict or state machine.
- `pending_inputs_never_marked_available`: every PENDING input names its owning concern; the verification script enforces this mechanically.
