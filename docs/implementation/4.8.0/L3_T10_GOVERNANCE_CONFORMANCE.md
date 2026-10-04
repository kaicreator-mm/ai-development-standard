# v4.8.0 T-010 L3 — Task Learning / Evolution Governance Conformance

Status: **FINAL TASK-SCOPED L3 — JIT EXACT-BASE EXECUTION PACK REQUIRED**

Authority: Frozen Product blob `f26439580e00de6ed8b2e27d732a3095eb566219` + Frozen L2 blob `f88c85454e80101a0fdf56050e21f11a05279841` + Frozen Task DAG R2 commit `d2f18854043c59712c1c9d2518f45843b0ad129c` / blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc` + T-010 Task Pack + Task Issues T-004/#511 and T-005/#509.

This L3 is implementation guidance only. It cannot expand Product/L2/DAG authority, redefine Task Learning or ADS evolution owners, create a new standard-change lifecycle, weaken publication/privacy boundaries, or manufacture Review/Validation/Release truth.

## Tests

Create one deterministic focused conformance module: `scripts/test_v48_governance_conformance.py`.

The suite must exercise explicit scenario records rather than only checking that normative strings exist. It may read current normative files and schemas as oracle inputs, but scenario outcomes must be independently asserted.

At minimum cover:

1. **none-material-fast-path** — literal `TASK_LEARNING=NONE_MATERIAL` is accepted as the proportional closeout path; no empty Task Learning object is required.
2. **material-learning-current** — a material learning record with required work/authority/evidence refs, canonical immutable exact subject/currentness and bounded confidence layers is treated as current evidence only for that exact subject.
3. **stale-learning-historical-only** — a previously valid exact-subject record becomes historical-only when the current subject drifts; no silent rebind to successor code is permitted.
4. **missing-or-mutable-subject-historical-only** — missing, branch/tag/repository-only/short-SHA/malformed currentness cannot establish current behavioral truth.
5. **confidence-not-current-pass** — `IDENTITY_BOUND`, `BEHAVIOR_SUPPORTED` and `INDEPENDENTLY_CHALLENGED` never imply current Validation PASS, Review PASS, merge authorization or a scalar Agent/quality score.
6. **learning-routing-not-authority** — Task Learning `friction_classification`/`disposition` may preserve evidence/routing metadata but cannot itself mutate ADS, approve an intake or substitute for T-005 governance.
7. **project-defect-no-promotion** — `PROJECT_DEFECT` routes to project ownership and cannot open ADS standard change.
8. **agent-execution-defect-no-promotion** — `AGENT_EXECUTION_DEFECT` routes to execution repair and cannot open ADS standard change.
9. **environment-tool-defect-no-promotion** — `ENVIRONMENT_OR_TOOL_DEFECT` routes to environment/tool owner and cannot open ADS standard change.
10. **project-specific-no-promotion** — `PROJECT_SPECIFIC_REQUIREMENT` remains project-local and cannot open ADS standard change.
11. **friction-no-change** — `STANDARD_FRICTION_CANDIDATE` can terminate as `NO_CHANGE` without standard mutation.
12. **friction-more-evidence** — `STANDARD_FRICTION_CANDIDATE` can route to `MORE_EVIDENCE`, including ambiguous cause or insufficient cross-project/counterexample evidence.
13. **numeric-or-provider-auto-promotion-rejected** — count, score, success/failure rate, cost, latency, provider/model label or heuristic cannot automatically promote friction to ADS evolution or authorize standard change.
14. **ads-evolution-intake-only** — `ADS_EVOLUTION_CANDIDATE` permits only `OPEN_ADS_INTAKE`, followed by ordinary `Intake -> L1 -> PRD -> L2 -> Task -> Review/Validation`; it is not approval.
15. **ordinary-governance-no-shortcut** — telemetry, scheduler/ranking output, Task Learning, CI results, dogfood observations or model output may be evidence refs only and cannot edit normative ADS or skip governance stages.
16. **publication-fail-closed** — absent explicit `PUBLISHABLE` classification, evidence remains non-public; `PROJECT_PRIVATE`/`RESTRICTED` cannot be copied into public standard evidence.
17. **publication-independent-of-strength** — publication class does not alter evidence strength, owner authority or promotion status.
18. **sensitive-material-never-publishable** — secrets, credentials, private chain-of-thought and hidden-evaluator/Hidden Validation payloads remain prohibited publication material even if surrounding observation metadata is otherwise `PUBLISHABLE`.
19. **reference-first-minimization** — public/publishable evidence uses refs/digests or minimized non-sensitive summary instead of copying sensitive source bodies.
20. **owner-preservation** — Task Learning/governance evidence cannot become Product/Architecture/Task/ADR/Incident/Intent/Skill/Review/Validation/merge/release authority.
21. **no-new-evolution-lifecycle** — conformance does not introduce a second evolution schema/database/controller lifecycle, numeric promotion engine, or self-amending ADS path.

Regression commands:

```text
python -B scripts/test_v48_governance_conformance.py
python -B scripts/test_v48_task_learning.py
python -B scripts/test_v48_ads_evolution_governance.py
python -B scripts/test_work_item_contract_and_golden_templates.py
python -B scripts/verify_standard.py
```

## Contract

### 1. Task Learning closeout contract

The two closeout routes are explicit and non-equivalent:

```text
no reusable material learning
→ TASK_LEARNING=NONE_MATERIAL

material reusable learning
→ Task Learning Evidence v1
→ durable refs / bounded summary / evidence layers
→ optional friction classification
```

`NONE_MATERIAL` is not a placeholder object and must remain cheap. Material learning is evidence/history, not a gate or authority mutation.

For code/artifact-specific behavioral claims, currentness requires canonical immutable Git identity and exact equality of the evidenced implementation subject, current subject and currentness ref. Missing, mutable, malformed, ambiguous or drifted identity fails closed to historical-only evidence.

### 2. Evidence-strength boundary

Evidence strength is layered and local to the claim:

```text
IDENTITY_BOUND
BEHAVIOR_SUPPORTED
INDEPENDENTLY_CHALLENGED
```

These labels do not compose into a global scalar score. They do not create current Review/Validation PASS, release readiness or standard-change authority. A stale record with strong historical evidence remains stale for a successor subject.

### 3. Evolution classification contract

Use exactly one primary classification for the current observation:

```text
PROJECT_DEFECT
AGENT_EXECUTION_DEFECT
ENVIRONMENT_OR_TOOL_DEFECT
PROJECT_SPECIFIC_REQUIREMENT
STANDARD_FRICTION_CANDIDATE
ADS_EVOLUTION_CANDIDATE
```

The first four classifications route to their existing owners and do not open an ADS standard change. `STANDARD_FRICTION_CANDIDATE` remains non-normative and may terminate as `NO_CHANGE` or `MORE_EVIDENCE`. Reclassification to `ADS_EVOLUTION_CANDIDATE` is a separate explicit later decision.

If cause or owner is ambiguous, choose `MORE_EVIDENCE`; never promote upward merely to obtain a standard change.

### 4. ADS evolution promotion boundary

`ADS_EVOLUTION_CANDIDATE` is evidence sufficient to consider change, not approval. The only promotion route is ordinary durable ADS governance:

```text
OPEN_ADS_INTAKE
→ Intake
→ L1 Product Evidence
→ PRD / Scope Freeze
→ L2 Architecture Evidence / Freeze
→ Task DAG / Task
→ Implementation
→ required Validation
→ applicable Fresh Review
→ normal integration / release authority
```

No telemetry/model/scheduler/Task-Learning/CI/dogfood artifact can directly mutate standard authority. There is no universal numeric promotion threshold.

### 5. Privacy / publication / minimization

Every evolution evidence item must have a publication class before copied/quoted/linked outside its source boundary:

```text
PROJECT_PRIVATE
RESTRICTED
PUBLISHABLE
```

Publication authority is independent from evidence strength and promotion status. Missing explicit `PUBLISHABLE` fails closed. Prefer refs/digests and minimized non-sensitive summaries.

Secrets, credentials, private chain-of-thought and hidden-evaluator/Hidden Validation payloads are never publication material. T-010 must prove this as a negative oracle, not merely echo the policy text.

## Implementation

Authorized Builder change is exactly:

1. `scripts/test_v48_governance_conformance.py`
   - implement deterministic scenario records and route/evaluation helpers sufficient to prove the TEST matrix;
   - read `schemas/task-learning-v1.schema.json`, `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`, `standards/DEVELOPMENT_WORKFLOW.md` and applicable T-004 templates/checklists as read-only owner inputs;
   - may reuse repository schema helpers from existing tests;
   - keep fixture data inside the module unless an explicit controller rebind authorizes another path;
   - assert outcomes for both valid and invalid routes so a contradictory promotion/publication/currentness path fails the test;
   - do not duplicate or rewrite upstream owner semantics merely to make assertions easy.

Implementation should reuse canonical vocabulary (`TASK_LEARNING=NONE_MATERIAL`, the six classification names, `NO_CHANGE`, `MORE_EVIDENCE`, `OPEN_ADS_INTAKE`, the three publication classes and the three evidence-strength layers). Do not add synonyms or a parallel lifecycle vocabulary.

## Failure Handling

- Current integration base, Task Pack/L3 identity or native blocker state changed before Builder claim → `PACK_STALE`; stop and rebind.
- Need to modify Task Learning schema/reference, Development Workflow, T-004 templates/checklists or any upstream owner semantics → stop with `ARCHITECTURE_AMENDMENT_REQUIRED` or explicit upstream-owner repair request.
- Need a second evolution lifecycle/schema/database/controller or automatic promotion engine → `ARCHITECTURE_AMENDMENT_REQUIRED`.
- Empty Task Learning object becomes mandatory for `NONE_MATERIAL` → blocking Fast Path regression.
- Stale/mutable subject is treated as current behavioral proof → blocking currentness failure.
- Confidence/evidence layer is treated as current Review/Validation PASS or global score → blocking authority failure.
- Project/Agent/environment/project-specific observation opens ADS Intake → blocking classification failure.
- `STANDARD_FRICTION_CANDIDATE` auto-promotes from score/count/provider/cost/latency/heuristic → blocking governance failure.
- `ADS_EVOLUTION_CANDIDATE` directly edits/approves normative ADS or skips ordinary governance → blocking promotion-boundary failure.
- Missing publication classification is treated as public → blocking privacy failure.
- Secret/credential/private-CoT/hidden-evaluator payload is copied into publishable evidence → blocking privacy/security failure.
- Required independent exact-subject Validation unavailable → `BLOCKED` with explicit Validation handoff; never self-certify.
- Any material candidate change after qualifying Validation/Review → stale affected evidence and requalify.

## Evidence expectations

Builder closeout must record exact base SHA/tree, planning/JIT Pack HEAD/tree, candidate HEAD/tree, exact one-path implementation diff and all required command results. Builder must explicitly state that Independent Validation and Fresh Review were not performed by the Builder.

Independent Validator must inspect scenario semantics, not only test exit code. It must falsify at least stale-currentness rebound, upward classification leakage, numeric auto-promotion, direct standard mutation, publication fail-open and hidden-evaluator leakage on the exact candidate.

After qualifying Validation, a genuinely Fresh Independent Reviewer must re-read exact current PR HEAD, Task Pack, L3, execution pack and upstream owner artifacts. Neither role may inherit the Builder conclusion as truth.

## Reference

- Frozen Product: `docs/implementation/4.8.0/PRD.md` blob `f26439580e00de6ed8b2e27d732a3095eb566219`
- Frozen L2: `docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md` blob `f88c85454e80101a0fdf56050e21f11a05279841`
- Frozen DAG R2: `docs/implementation/4.8.0/TASK_DAG.md` blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc`
- Task: #516 / T-010
- Upstream Task Learning closeout: T-004/#511
- Upstream ADS evolution governance: T-005/#509
- Task Learning reference: `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`
- Task Learning schema test: `scripts/test_v48_task_learning.py`
- T-004 closeout/template regression: `scripts/test_work_item_contract_and_golden_templates.py`
- ADS evolution owner: `standards/DEVELOPMENT_WORKFLOW.md` §8
- ADS evolution regression: `scripts/test_v48_ads_evolution_governance.py`
- T-010 Task Pack: `docs/implementation/4.8.0/task-packs/T10_governance_conformance.md`
