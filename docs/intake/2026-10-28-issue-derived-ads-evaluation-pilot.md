# ADS v4.19 R0 — Issue-derived decision evaluation pilot

Status: **DRAFT / NOT_FROZEN / NO NEW GATE**. This is a practice/evaluation proposal, not an ADS standard amendment and not a second Task Learning authority.
Source: [DomainHarness stage-chain retrospective](2026-10-28-domain-harness-version-delivery-audit.md), [18 candidate machine-readable cases](issue-cases/domain-harness-decision-pilot-r0.json), [ADS #1341](https://github.com/kaicreator-mm/ai-development-standard/issues/1341).

## 1. Reuse existing owners; avoid building a second feedback system

- Development Workflow §8 already owns ADS evolution route and publication class; a source Issue does not automatically become a normative ADS requirement.
- GitHub Agent Interaction Protocol §10 already provides Task decision summary / Level 1–3 feedback, task-meta observation semantics, evidence classes OBSERVED / SELF_REPORTED / INFERRED / UNKNOWN.
- Execution Architecture §30 already governs Task Learning v1/v2 identity, currentness and subordinate use.
- Test Data & Scenario owns evidence provenance and regression cases. Golden Template Standard owns formal positive and forbidden examples. Testing / CI / Validation own physical tests and their real results.

The new opportunity is an **offline evaluation loop**, not new Issue labels, schema, dispatch lifecycle, mandatory time tracking or universal Gate.

## 2. Seven high-value transformations

| Derived output | What to mine from real Issue/PR/Review | Real consumer |
| --- | --- | --- |
| Root-cause fingerprints | First divergence, affected invariant, chosen owner, first falsifier, related earlier versions | Planner, Architect, Reviewer; search only when matching seam exists |
| Paired decision cases | Same reported facts, tempting incorrect next action, bounded correct next action, explicit prohibited shortcuts | Golden/Skill examples and read-only role rehearsal |
| Role-specific counterexamples | Planner false DAG edge, Builder unauthorized patch, Reviewer false PASS, Validator missing suite, Controller wrong RQ | Task Pack/role bootstrap quality |
| First-discovery analysis | Was this genuinely observable before integration, and from what earlier exact evidence? | Correct L2/Task placement; avoid hindsight blame |
| Version traceability | Frozen Product acceptance → L2 → Task → PR → Review round → Repair → CI/Host → qualified installed journey | Version Controller and Task Learning |
| Bounded cost analysis | Real measured attempt/wait/CI/Review/rework evidence with source identity | task-meta/Tally as optional derived analytics |
| ADS rule regression evaluation | Re-run same evidence-bounded decision scenario under pinned old rules and candidate proposed clarification | Independent ADS Product/Review owner |

A successful source-derived outcome may simply be NO_CHANGE, project repair, CI/environment action, narrower skill example or scope-local library reuse. Do not create a new standard by default.

## 3. Delivered first pilot: 18 cases with positive controls

The [candidate JSON corpus](issue-cases/domain-harness-decision-pilot-r0.json) contains 18 manually selected DomainHarness source-linked diagnostic exercises, 15 findings and 3 positive controls. Each record carries:

- source Issue reference and its stage category;
- **reported known facts at the Issue-finding stage**, not a purported pre-discovery transcript;
- proposed primary observation class when applicable and bounded next action;
- an explicit unsafe/wasteful inference the Agent must reject;
- paired controls for contrasting CI runner vs version-branch config, loaded vs called runtime path, unnecessary serial DAG vs efficient verification campaign, and trust-root vs bounded docs adapter;
- unreviewed source classification and a publication/currentness caveat.

Examples: [#162](https://github.com/kaicreator-mm/domain-harness/issues/162) npm test excluded nested suites; [#530](https://github.com/kaicreator-mm/domain-harness/issues/530) v0.7 false dependency; [#586](https://github.com/kaicreator-mm/domain-harness/issues/586) one verification campaign, not an Issue per checkpoint; [#782](https://github.com/kaicreator-mm/domain-harness/issues/782) runner-only git-lfs failure; [#1013](https://github.com/kaicreator-mm/domain-harness/issues/1013) integrated public Host→Kernel path not executable; [#1100](https://github.com/kaicreator-mm/domain-harness/issues/1100) non-waivable stale CAS P0; [#1026](https://github.com/kaicreator-mm/domain-harness/issues/1026) platform Core vs adapter scope; [#1291](https://github.com/kaicreator-mm/domain-harness/issues/1291) sound evidence reuse; [#1393](https://github.com/kaicreator-mm/domain-harness/issues/1393) Provider trust anchor; [#1394](https://github.com/kaicreator-mm/domain-harness/issues/1394) CAS documentation/adapter.

**This corpus does NOT prove that any Planner could have predicted a later issue before its creation.** The source Issues already contain the findings. Correct use: diagnose, route and select proportionate next steps given the findings. Proposed answers are *review candidates*, not approved Golden oracles.

## 4. Future historically blind test design, only when reconstructable

1. Pick a genuine decision checkpoint: exact Task/PR/base HEAD, effective ADS pin, timestamp and role.
2. Reconstruct **INPUT_AT_TIME** from immutable commit tree and timestamped accepted observations actually available then; beware Issue bodies edited later.
3. Separate later **FINDING** and **OUTCOME** into evaluation-only material; never expose it in Agent prompt if claiming a prior-decision test.
4. If the earlier information cannot be reconstructed, mark NOT_RECONSTRUCTABLE and keep a finding-stage case. Do not score hindsight.
5. Use an independent Reviewer to approve expected route and acceptable alternatives under the **then-effective** standard and Product/L2. The later proposed v4.19 rule did not exist at the earlier decision time.
6. Keep public example/training cases separate from genuinely held-out challenge cases. Cross-project holdouts (xDownload, Shun Assistant, app8, Tally) are useful after separate source verification and publication clearance.
7. Baseline and candidate Agents receive identical time-bounded material, roles, tool access and budget. Exercise read-only decisions; no real source edits/merge/side effects while evaluating.

## 5. Proposed evaluation dimensions — not new normative gates

| Diagnostic dimension | Good response | Reject |
| --- | --- | --- |
| Factual and epistemic correctness | Source-backed facts; reporter assertions and missing facts labeled accurately | Future-leakage, fabricated times, treating CI-green as evidence of unexecuted suites |
| Correct existing authority | Routes to Project / Agent execution / Environment / ADS Intake owner with lawful Claim/review bounds | Builder self-authorization, waived mandatory P0/P1, wrong Task owner |
| Falsifiable implementation/test choice | Correct invariant, real public selected path, representative negative, actual failure handling | Module merely imported, CAS concurrency ignored, mock reported as physical evidence |
| Proportionality and value | Local fix when sufficient; one integration owner, reused valid evidence, no invented ceremony | Global refactor for docs adapter, per-checkpoint Issues, repeated full regression without impact |

Independent assessors may issue practice judgments PASS / NEEDS_WORK / UNKNOWN by dimension **only as evaluation notes**, not canonical Validation Gate status or automatic source authority. Multiple genuinely safe approaches may be correct; do not require a particular English phrase. More words and more tests are not inherently better.

## 6. Concrete integration path

- **Pilot 0 (current):** keep this candidate corpus in docs/intake, no new active conformance registration and no normative schema. Independently review source facts, proposed labels and positive counterexamples.
- **Pilot 1 (read-only if authorized):** compare role decisions under current v4.18 and proposed v4.19 prompts/clarifications on a matched subset; preserve actual failures, over-engineering false positives, coverage and UNKNOWN. If change only affects interpretation, update existing role Skill or Golden reference rather than creating another MUST.
- **Pilot 2 (bounded real-project dogfood if authorized):** while doing ordinary planned work, retrieve one matching historical case when material. Record only the changed decision and subsequent actual outcome through existing Task summary/Task Learning; no extra mandatory per-Task Issue or gate.
- **Pilot 3 (normative only if justified):** after cross-project corroboration and independent Product/L2 authorization, amend the narrow existing owner plus maintained Golden/Forbidden/test materials. Follow the ordinary ADS Intake→L1→L2→Task→Review/Validation/release path; no direct promotion from a model score.

## 7. Risks, limitations and negative controls

- Raw Issue count reflects what was recorded, including reviews and coordination, not independent bugs or successful features. Sampling favors discovered, reported failures. Include valid local repairs and good cost-saving practices.
- Do not mistake GitHub Issue lead time, a shared transport username, source commit interval or Reviewer comment latency for active Agent time; without task-meta/provider measurement that figure is UNKNOWN.
- Do not use a later outcome as earlier available evidence, even if it makes a realistic scenario. Rounds of Review are not automatically waste; independent Review may have correctly prevented a serious defect.
- A project defect or local requirement is not by itself an ADS normative defect. ADS may already have the right rule and the project Agent failed to apply it.
- Linking publicly visible historical Issues does not bypass ADS §8 publication classification or sensitive-data constraints. Keep only minimal source refs and paraphrased nonsecret facts pending owning-source clearance for a formally published corpus.
- Never expose private chain-of-thought, tokens/secrets, Hidden Validation cases or unapproved project data. Test prompts are read-only and must not trigger accepted Claims, merge, release or external effects.
- Cross-version timing improvements or lower regression rates remain **NOT_MEASURED** until comparable instrumented observations exist. A favorable pilot score alone cannot promote a new ADS standard.

## 8. Proposed v4.19 Product R0 review question

The strongest likely delta is **turning existing Task Learning/Golden/ADS Evolution mechanisms into a source-grounded decision evaluation cycle**, with case selection, positive controls, independent adjudication and explicit no-hindsight limitations. Much of the behavior is already supported by existing standards. Owner must mark ALREADY_COVERED / REFERENCE_OR_TOOLING_ONLY / NORMATIVE_DELTA per requirement and prefer reference material unless a material real rule omission is proven.
