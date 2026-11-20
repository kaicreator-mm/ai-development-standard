# ADS three-phase adaptive engineering — recovered design and source candidate R0

> Status: **prospective source candidate / NOT normative v4.19.0 / not Product-L2-DAG Freeze**. Origin: [ADS #1383](https://github.com/kaicreator-mm/ai-development-standard/issues/1383). Recovered owner: [#1100 v4.12 W1](https://github.com/kaicreator-mm/ai-development-standard/issues/1100). Base: released `main@933c4fd3e0e1b9f1a73ed6a9b552077baaf5376c`. This document maps existing rules; it does not create new work-state, dispatch, Gate, Review, Release, Claim or Domain Package runtime authority.

## 1. The recovered model, not a new scheduler

ADS v4.12 #1100 already defined **ONE conceptual Development Work Graph**, **THREE conditional phase-scoped DAG views**. The simplified Stage-1/Stage-2 paths in the current v4.19 workflow must not be interpreted as *forbidding* fine-grained work planning:

| View | Semantic layer | Actual question and work | Exit/authority |
| --- | --- | --- | --- |
| **DAG-P** | L1 Product/Requirements Engineering | User/problem/need evidence; elicitation, clarification, stakeholder conflicts, requirement analysis/specification/validation, Product Research if needed; bounded independent studies and decisions | Adopted/rejected Product evidence; the existing **Product Authority** alone freezes the selected PRD/Scope |
| **DAG-A** | L2 Solution Architecture & Design | Map accepted requirements to architectural drivers, modules, interfaces, data/ownership, nonfunctional constraints, options, invariants, tests/probes and design decisions; Research Demo only when necessary | Architectural decisions and source-backed design; the existing **L2 Authority** alone freezes L2 |
| **DAG-I** | L3 Detailed Design & Implementation | Implementation Task DAG; task-specific design/tests/contract/failure path, scoped Agent work, actual code, review/validation/integration/closure | Existing Task/Issue/Claim/Review/Validation/Release owners; when materialized, **GitHub native Issue Dependencies** are canonical live implementation edges |

The three views are not three mandatory files or three mutable task authorities. Stage artifacts and decisions remain owned by existing standards. **DAG-I is the existing implementation DAG**; L3 does not mint a fourth execution graph or independent Task status store.

## 2. Per-phase complexity, not a one-time project label

Before costly phase work or JIT dispatch, resolve the *phase/concern-specific* facts from existing context:

- Business/core obligation, safety/rights/permission/validation floor and materiality.
- Uncertainty: sufficient existing evidence, bounded unknown, material unknown or contradictory/stale evidence.
- Coordination: one owner, multiple independent owners, or real dependent work.
- Source/workspace ownership and overlap; required real host, independent person or tool.
- Expected evidence/decision value and total work/verification/coordination cost; unknown cost stays UNKNOWN.
- Authority whose decision, Freeze or Claim is needed; absence of current proof remains UNKNOWN/BLOCKED.

Select an **organizational shape independently in P, A and I**:

| Shape | When applicable | Persist only |
| --- | --- | --- |
| `INLINE` | Existing current evidence suffices, one owner, no material independently schedulable dependency | One concise source-qualified decision and acceptance references; no empty planning Issue |
| `BOUNDED_WORKLIST` | A few small checks/questions, with no important scheduling dependency or write conflict | Named questions, owner, results, stop rule and compact evidence links |
| `EXPLICIT_DAG` | Material dependent studies/design tasks, independently owned executable work, costly real-Human/Host stages, write conflict, or critical-path need | Phase-tagged nodes, **actual** predecessors, decision consumer and stop rule; authorize native Issues/edges only when required by owner |

`FAST`, `STANDARD`, `EXPLORATORY`, `HIGH_ASSURANCE` describe intent/depth, **not four exclusive global project modes**: exploratory research and high assurance can co-occur. Fast never cancels a hard floor. A complex L1 does not require an equally complex L2 or L3.

## 3. Phase deliverables and minimum checks

### L1: Requirements Engineering / Product truth

Use existing Product Evidence and as-needed Product Research; do not replace them. As material, express:

- User Job / stakeholder / business outcome; scope, exclusions and constraints.
- Functional and nonfunctional requirements; important business rules and acceptance behavior.
- Ambiguity, conflict, assumptions, infeasible promises and unresolved material questions.
- Origin/source, version/currentness, priority/rationale and change implications.
- Acceptance criteria that a future verifier can observe (not merely prose such as 'usable').
- Research/study/review evidence as *decision input*; **Product Freeze remains an explicit authority act**.

Examples of DAG-P work: compare alternative user workflows; interview or run a blinded study where genuinely necessary; analyze authorization and per-project isolation requirement; converge conflicting requirements. Same-owner prose cleanup is not a DAG node.

**L1→L2 handoff:** agreed requirements and acceptance map with exact Product revision + any material evidence/assumption/UNKNOWN. Review PASS / study PASS cannot be promoted into Product Freeze.

### L2: Solution Architecture & Design / design truth

Consume the accepted L1 baseline; reuse `ARCHITECTURE_DESIGN_STANDARD.md`, `ARCHITECTURE_RESEARCH_DEMO_STANDARD.md` and the L2 prompt, not a new architecture owner. As material, express:

- Requirement/quality-attribute coverage of architecture decisions.
- Modules and boundaries, interfaces, state/data ownership, trust, failure/recovery, deployment and migrations.
- Key invariants, alternatives/trade-offs, reuse/buy/build and architecture currentness.
- Real dependencies between architectural questions/contract versions/experiments.
- Evidence sufficiency and falsifiable Demo only for unresolved architecture-changing unknowns.
- Open decisions, owners, rationale and **L2 Freeze** binding.

Examples of DAG-A: dependency order `public contract → state ownership decision → bounded executable durability probe → architecture decision`, with independent side analyses only if facts genuinely permit. A Demo PASS is never implementation PASS.

**L2→L3 handoff:** exact frozen architecture/ADR/contract and mapped requirements, ownership/invariant constraints, named integration seams, validation obligations and still-open bounded risks.

### L3: Task-level Detailed Design & Implementation / execution truth

Keep `TASK_DECOMPOSITION_STANDARD.md`, `TASK_DAG_GOVERNANCE_STANDARD.md`, Task/Execution Pack, native Issue Dependency/Claim/CAS/Review/Validation/Release ownership unchanged. For a Task that materially benefits from L3 detail, provide:

- Goal, accepted Product/L2 refs, exact base, work scope, current allowed/forbidden paths.
- Local design slice: affected modules, interface, algorithm/state transitions, invariants, dependency currentness.
- Tests/negative oracle, failures/cancel/recovery, targeted regression and real-host obligations.
- Bounded selected references/versions/licensing, intentional divergence; **reuse existing L3 Reference Pack**.
- Proposed implementation and integration deliverables; expected outcome and definition of done.

Implementation Task DAG remains canonical DAG-I; one atomic, low-risk Task may omit a separate L3 document. Do **not** create a second technical DAG for its private internal checklist. Real dependency/writeset collisions are not 'related-to' metadata.

## 4. Shared bounded node/edge facts (no new schema)

For a phase DAG node, when material to actual scheduling/decision, recover: `PHASE=P|A|I`, question/primary concern, owner/role, source/authority refs, expected decision/deliverable, verifiable acceptance/stop criterion, real predecessors, informational evidence refs, execution capability/environment and relevant write scope, scope/risk/unknowns, stop/escalation, current Issue/Attempt if applicable.

- **`BLOCKED_BY`** represents a real dependency between independently executable work; materialize to native GitHub for implementation Tasks under existing governance.
- **`CONSUMES_EVIDENCE` / `INFORMS` / `TRACE_TO`** provides source/decision lineage; does not produce readiness, a GitHub blocked-by edge or PASS.
- Same study/Source Evidence may be used by multiple phases, but acceptance authority is not inherited. Verify exact ref/currentness only for changed material slice.
- L1 scope change invalidates affected L2/L3 references and tests; L2 amendment invalidates affected DAG-I/L3 subjects, not unrelated L1 evidence; L3 defect first uses scoped root-cause repair. Existing Freeze amendment/Claim/Review owners govern changes.

## 5. Minimal decision protocol for a controller / Tally

1. Read actual current product/version/phase, canonical source/authority, remaining critical-path outcome and the phase's applicable hard floor.
2. Identify first material unresolved question, outcome and known dependencies. Reuse current evidence, do not start broad research by default.
3. Select `INLINE` / `BOUNDED_WORKLIST` / `EXPLICIT_DAG` **separately for L1, L2 and L3**; explain the selected shape and an explicit stop condition in ordinary project records.
4. Only for real independently ownable work, choose a task/Issue, admissible actor and required environment; leave existing Claims/K/Host authority untouched.
5. Converge evidence to the phase decision. Never let the Controller or Builder auto-approve Product/L2 Freeze, high-impact scope changes, Release or other protected decisions.
6. When evidence contradicts a previously accepted decision, determine the earliest affected owning layer, request its authorized amendment, and recompute only the affected downstream nodes.
7. When no remaining critical-path outcome is blocked, proceed immediately to the next authorized phase using current evidence; do not rerun unchanged successful checks.

## 6. Example conformance scenarios

| Situation | P / L1 | A / L2 | I / L3 | Required negative assertion |
| --- | --- | --- | --- | --- |
| Trivial config/typo repair | INLINE | INLINE | one lawful Task / Fast Path | no empty P/A DAG or blanket review |
| Complex ambiguous business requirements | EXPLICIT_DAG-P if actually dependent | INLINE or WORKLIST after Product Freeze | small DAG-I if needed | L1 study completion != Product Freeze |
| Novel architecture + stable requirements | INLINE | EXPLICIT_DAG-A for genuine experiments | subsequent DAG-I | Demo PASS != implementation PASS |
| Multi-Agent UI/API/Host implementation | INLINE | WORKLIST if existing architecture | EXPLICIT_DAG-I with accepted writer fences | no shared mutable writer concurrency |
| High-risk simple permission fix | INLINE | INLINE / WORKLIST | narrow Task with high assurance | FAST cannot waive mandatory security proofs |
| Requirements conflict discovered during implementation | target changed L1 questions | impact-dependent amended L2 | affected Task/L3 replan | no silent Product edit or unrelated DAG reset |
| Current evidence becomes stale | relevant slice refresh only | relevant slice refresh only | exact refs recheck | stale evidence cannot be promoted to PASS |
| Development of software by Tally | Tally governs product/requirements | Tally consumes qualified Engineering Domain Package | Agent/tool implementation and verification | delivered application does **not** require ADS/Tally runtime |

## 7. Compiler-consumer boundary (separate downstream qualification)

ADS owns normative **development-time** semantics. A future DomainForge-qualified compilation may transform current, pinned ADS rules/Workflow/evidence semantics plus separately qualified software-engineering knowledge into a Tally Engineering Domain Package. Tally consumes that package as a **software-development Domain App**; the programs it creates do not load ADS as runtime policy. Transformation must preserve source/authority/version/applicability and reject semantic loss, but this proposal **does not implement a compiler or require every code project to deploy DomainHarness**. The engineering Package maps to existing Business/Rule/Workflow/Validation interfaces; no second scheduler.

## 8. Existing owner crosswalk and acceptance

- #1100 — source design for three DAG views and depth; restore rather than redesign.
- #1081 — L1 bounded Evidence DAG / stop; #931 — progressive L1/L2/L3 evidence.
- `standards/DEVELOPMENT_WORKFLOW.md` — lifecycle/phase handoff and selecting phase work shape.
- `prompts/L1_PRODUCT_EVIDENCE.md`, `prompts/L2_ARCHITECTURE_EVIDENCE.md`, `prompts/L3_IMPLEMENTATION_EVIDENCE.md` — stage-level guidance and deliverables.
- `standards/ARCHITECTURE_DESIGN_STANDARD.md` — existing architecture quality authority.
- `standards/TASK_DECOMPOSITION_STANDARD.md`, `standards/TASK_DAG_GOVERNANCE_STANDARD.md`, Task/Execution Pack, GitHub Agent Interaction — **sole** implementation/native DAG/Claim/dispatch owners.

Acceptance requires crosswalk completeness; representative positive/negative scenarios above; unchanged prior v4.19 source/release authority; no duplicated scheduler/Claim/schema/gate; independent source review before adoption. **This is a draft proposal for a successor release and cannot retroactively change v4.19.0.**
