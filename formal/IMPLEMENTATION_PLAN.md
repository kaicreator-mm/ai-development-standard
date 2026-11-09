# ADS Model-Based Formal Verification — 实施计划 R1（实验性，非规范）

**Status**: PLANNED / EXPERIMENT / NO_NORMATIVE_GATE / NOT_PROVEN  
**Repository**: `kaicreator-mm/ai-development-standard`  
**Work branch**: `experiment/v4.19-formal-proof-r0`  
**Known branch HEAD before this plan**: `af710115af0863a9909b84e05bf2ff9916bd2680`  
**Normative baseline**: ADS v4.18 published and effective per actual project pins; historical v4.19 #1353 frozen scope remains immutable.  
**v4.19 candidate under study**: PR #1365 HEAD `dac263fa4c0ab155406d2f2117459b34322cc988`; candidate, not automatically current/frozen.  
**Tools sources**: Google Drive `App` and `formal-toolkit-linux-x86_64` (https://drive.google.com/drive/folders/1a1H87Q95J0z4sU7R_ZoGnT0xXUpN5Lbi).  
**ADS authority**: This research does not replace Product/L2/DAG Freeze, Task Claim, CI, independent Review, Outcome Closure or Release.

## 0. Outcome and design choice

Build **ADS Domain Model + Python Verification Suite + native formal tools + independently challenged evidence**, without designing an FIR or a replacement ADS engine. Primary success: expose real ADS contradictions, unsafe/reachable states, unjustified serial dependencies, missing cases, and version-compatibility defects; when no defects are found, clearly state the bounded proof scope. Formal model is a *hypothesis about* ADS, not a competing normative source.

Retain existing R0 files under `formal/v4.19/r0/` and the Python runner `formal/suite/run.py`. R0 contains 6 cases (3 Z3/3 TLC), a source-map and mutation counterexamples. Preserve historical receipts. New rounds write independently versioned models, plans, and results; do not rewrite past evidence.

### Direct linking, not FIR

Each model declares **Model ID** and **Property ID**. The Python suite indexes:
`source_path + Git blob SHA + exact rule location + effective version/scope + model_id + property_id + case_id + solver + expected result + assumptions/bound + evidence`.
This is lightweight traceability metadata, not an intermediate logic language; mathematical semantics stay inside native `.smt2`, `.tla`, `.als`, `.dl`, `.lp`, etc. A single property may have several verification cases and solvers; several properties may use one shared model. Bidirectional source → property → case → result and result → property → source navigation is required.

## 1. Model coverage and verification obligations

| Model ID | Scope | Minimum propositions to challenge | Preferred tools |
|---|---|---|---|
| `ADS-M-LIFECYCLE` | Product/L1, L2, DAG Freeze, Dispatch, Claim, validation, Review, Closure, integration, Release; failure and repair | Only legal transitions reachable; illegal release never reachable; valid path exists; recoverable states, under specified fairness, can progress | TLA+/TLC, Z3; Apalache/ProB when needed |
| `ADS-M-AUTHORITY` | Owner/Builder/Validator/Reviewer, Writer, permission, profile, effective scope | No Claim → no authoritative mutation; Validator cannot source-write; profile/environment never grants authority; Writer resource exclusion | Z3 + cvc5 comparison; Alloy for relationships |
| `ADS-M-DEPENDENCY` | Task DAG, scheduling, shared write-set, native dependencies, concurrency | No cycles in accepted DAG; no false serial dependency; parallelism preserves write safety; blocked dependents fail closed | Soufflé, Alloy; Clingo where exceptions/selection matter |
| `ADS-M-EVIDENCE` | Exact-SHA CI, source-currentness, Review independence, claim and evidence provenance | Stale evidence cannot satisfy current subject; NOT_RUN/UNKNOWN cannot masquerade as PASS; traceable evidence required for gates | Z3/cvc5, pySHACL/Jena only where graph representation adds value |
| `ADS-M-EVOLUTION` | v4.18→v4.19 inheritance, prospective policy, frozen historical subjects, source scope | Historical frozen authority unchanged without lawful revision; proposed policy cannot self-activate; qualified changes invalidate only materially impacted proof | Z3, TLA+, relation checks |
| `ADS-M-CROSS` | Interfaces among the five models | Authority/Claim and Lifecycle use same effective rules; DAG readiness agrees with Claim admissions; Release consumes current Evidence; conflicts produce BLOCKED/UNKNOWN | Python crosswalk + cross-solver/multi-model scenarios |

All models must include positive *legal* paths (non-vacuity), deliberately illegal negative paths, boundary cases (unknown/stale/conflict), and explicitly declared finite bounds/assumptions. Distinguish **safety** from **liveness**; temporal progress proofs require stated environmental fairness assumptions and cannot promise actual Agent/CI availability.

## 2. Tool roster and activation policy

| Tier | Tools | Use/selection rule |
|---|---|---|
| Core | Z3 5.3.3; TLA+/TLC 2.19; Python 3 | SMT rules, finite-state transitions; every baseline model run |
| First cross-check | cvc5 1.4.2 | Re-run portable SMT-LIB queries for independent comparison; disagreement/UNKNOWN → inconclusive, not PASS |
| Structural | Alloy 6.2.0; Soufflé 2.5 | Bound relationship consistency, DAG reachability and graph inference |
| Policy exceptions | Clingo 5.8.3 | Nonmonotonic exceptions/priority/choice only with an explicitly specified closed-world treatment; unknown external facts must not become false by default |
| State model escalation | Apalache 0.62.4; ProB 1.16.0 | TLC state explosion, symbolic temporal cases, B invariants/refinement where independently valuable |
| Semantic graphs | pySHACL 0.40.2; SHACL; Apache Jena 6.2.0 | Only if graph/traceability model actually requires RDF/SPARQL/SHACL, not an implicit FIR |
| Higher-assurance/algorithmic | Vampire 5.1.0; Dafny 4.11.0; Lean 4.35.0 | Selected FOL entailment or proof of critical helper algorithms or theorem; do not claim Dafny proves Python source directly |
| Runtimes | Temurin JDK 21.0.13; .NET runtime 8.0.33; Python 3.14 for supplied Clingo wheel | Tool dependencies, not ADS/Node version gates |

Tool source roots:
- `App`: https://drive.google.com/drive/folders/1zZV3LcoOebjKqrbDNH2NOsqPMkM9xgJw
- `formal-toolkit-linux-x86_64`: https://drive.google.com/drive/folders/1a1H87Q95J0z4sU7R_ZoGnT0xXUpN5Lbi

The latter directory contains `MANIFEST.json`, `SHA256SUMS`, `install_offline.py`, artifact and wheelhouse directories. Manifest-declared packages: cvc5 1.4.2, Vampire 5.1.0, Jena 6.2.0, ProB 1.16.0, Dafny 4.11.0, Clingo 5.8.3 (wheel for CPython 3.14), Temurin 21, .NET 8. They are **inspected inventory only** until extracted, hashed and smoke-tested. ProB checksum is recorded-on-download (not independently upstream-verified); respect license/trust boundaries. Run installation only in a suitable isolated Linux x86_64 workspace; never assume connector files are executables; no global installation required. For the Python suite, a tool is **AVAILABLE / NOT_AVAILABLE / NOT_RUN / VERIFIED** independently, never silently skipped as PASS.

Tool duplication is useful only when it independently tests a high-value property, adds new bug-finding coverage, or addresses a proven solver limitation. Do **not** execute every tool on every change.

## 3. Implementation tasks and dependencies (small, parallelizable)

| ID | Task (one consistent Writer per write set) | Dependencies | Deliverable | Acceptance |
|---|---|---|---|---|
| T00 | Inventory/checksum/smoke and environment capability registry | — | `formal/tools/` inventory and run receipts | Tool identities, binary hashes, versions, missing dependencies, trust provenance; UNKNOWN/NOT_RUN explicit |
| T01 | Normative version/scope crosswalk and property inventory | — | Source→Rule→Model→Property index for five areas; exact SHA refs | Active v4.18 vs prospective v4.19 vs historical #1353 separated; source locations inspectable |
| T02 | Extend Python verification runner, no FIR | T00 | Pluggable bounded subprocess adapters and uniform evidence receipts | Timeouts, missing tool, stale source, unexpected output fail closed; no arbitrary shell commands from suite data |
| T03 | Lifecycle + Authority core models | T01,T02 | TLA+ and SMT native models, examples, mutations | Legal-path witness, illegal-path UNSAT/invariant, concurrency negative case |
| T04 | Dependency/DAG + parallelism | T01,T02 | Soufflé/Alloy or SMT models with real ADS cases | Cyclic/false-edge/write collision mutants detected; legal parallel case succeeds |
| T05 | Evidence + Evolution models | T01,T02 | SHA/currentness and version-scope models | Old CI/review cannot become current PASS; history remains protected; positive compatibility |
| T06 | Inter-model consistency | T03,T04,T05 | Integrated scenarios and interface assumptions | No contradictory role/claim/readiness/release semantics without explicit finding; mismatches exposed |
| T07 | Independent semantic challenge + checker mutation | Start after T01 and increment after T03–T06 | Positive/negative golden cases, semantic review notes, mutation receipts | Every modeled property has source, assumptions, witnessed legal path, at least one meaningful negative challenge |
| T08 | Incremental recheck and consolidated coverage/qualification | T06,T07 | Python affected-property selection, report and limits | Changed SHA → dependent proof invalidated; fresh source required for source-bound pass; explicit NOT_PROVEN remainder |

T00, T01 can run in parallel. After their completion, T03/T04/T05 are parallel lanes. T07 begins early and continues with each lane. T06 is the sole integrator for shared semantic interfaces, preventing parallel write conflicts. T08 follows integration. This table is an experimental verification Work DAG, **not** a new canonical ADS Task DAG or authorization grant.

## 4. Python suite behavior and receipt contract

1. Read the pinned source specification (branch/HEAD/blob) and version scope; never treat candidate source as approved without explicit authority.
2. Select affected model/property/cases via stable IDs and dependencies; support `--all`, `--model`, `--property`, `--changed-source`; use existing runner while adding support, not a parallel engine.
3. Recompute input SHA-256 and verify Git blob SHA/currentness; if source checkout missing, report `MODEL_ONLY_PASS` at most (or fail under strict mode).
4. Run tool-specific native models in bounded subprocesses with exact version/args, timeout, deterministic fixture, isolated scratch/output paths and parseable results.
5. Compare expected results/independent solvers, store counterexample witnesses, unsat assumptions, finite bounds, negative-mutant detection and semantic review.
6. Aggregate `PASS_MODEL`, `COUNTEREXAMPLE`, `FAIL`, `INCONCLUSIVE`, `BLOCKED`, `NOT_RUN`; no invented actual CI/Host/Release pass; preserve failed/earlier receipts append-only.
7. Link results back to source rules, model and property IDs. Report *scope coverage* by distinct supported obligations rather than raw test count. Keep denominator and unmodeled rules explicit.

**No successful solver result is sufficient to assert model-to-natural-language semantic equivalence.** Independent reviewer must inspect representative source→model mapping and challenge it with positive/negative cases. `SAT` is not always a defect; `UNSAT` is not always correctness; tool output is interpreted against the explicit query and assumptions.

## 5. Proposed monorepo layout (reuse R0)

```text
formal/
  IMPLEMENTATION_PLAN.md            # this non-normative plan
  models/
    lifecycle/ authority/ dependency/ evidence/ evolution/
    cross/
  suite/
    run.py                           # existing runner, extend only
    tools/                           # bounded adapters
    checks/                          # provenance/expectations/incremental
  cases/
    lifecycle/ authority/ dependency/ evidence/ evolution/ cross/
  tools/
    inventory.json                   # external tool refs, versions, trust/smoke status
  tests/
    test_suite.py                    # existing tests, extend
  v4.19/
    r0/                              # immutable historic experiment
    r1/                              # new versioned proof snapshot and receipts
```

Don't create empty directories or abstract interfaces preemptively. Native models own their logic; Python owns orchestration, not semantics.

## 6. Phased verification and stopping rules

- **M0 — Reproducible tool baseline**: existing Z3/TLC runs reproduced from actual binaries; new-tool smoke capability table complete. Missing optional tools do not block core progress.
- **M1 — Core model**: Lifecycle and Authority formally linked to at least their targeted exact ADS source sections, with legal and illegal witnesses and tested version guards.
- **M2 — Full five-domain pilot**: every area has at least one source-bound property, positive witness, negative challenge and valid receipt; cross-model safety tested.
- **M3 — Semantic reliability**: source→model independent checks, deliberate faulty translations detected, positive/negative fixtures and unproven source coverage enumerated.
- **M4 — Incremental usage**: one real ADS delta triggers only material proof invalidation/rechecks and outputs complete evidence; optional new tools evaluated by marginal defect/counterexample value.

Every round is Git-committed independently with exact source/model/tool versions, actual results, counterexample or witness, limitations, and feedback. New material findings may propose a normative ADS change **only through existing ADS authority**. Avoid repetitive rounds when no incremental evidence is produced; stop/reshape a tool path when it only duplicates prior checks.

## 7. Principal risks and mitigations

- **Correct but irrelevant model**: source and rule IDs plus independent semantic challenge and counterexamples, including missing or misleading translation.
- **Vacuous proof**: require satisfiable positive legal witnesses and explicit negative violation queries.
- **Finite bound mistaken for universal theorem**: label as bounded; escalate to inductive/infinite-state proofs only when justified.
- **Inconsistent multi-tool semantics**: direct shared source references, cross-model obligations, cvc5-vs-Z3 differential tests; disagreement→INCONCLUSIVE.
- **Normative drift**: immutable exact-SHA provenance, explicit historical/current/prospective scope; no unreviewed adoption.
- **Overengineering**: no FIR, no new scheduler, no mandatory tool matrix, no automatic normative gate, no heavy installs just for inventory.
- **Trust/toolchain**: SHA-256 and upstream checksum provenance distinguished, Python 3.14 Clingo wheel compatibility, JDK/.NET prerequisites, isolated smoke and no false claim of execution.

## 8. Initial implementation sequence

Start T00/T01 in parallel; reuse R0 instead of recreating its suite. Then implement T02 minimally (first cvc5 cross-check; Soufflé for DAG when needed) while T03 continues R0 models. Advance T04/T05 independently, merge via T06 and T07; finish with T08 based on demonstrated need. Local environment is only requested when a selected binary genuinely cannot run in the current execution environment; pass a repair+validation task rather than a validation-only ping-pong.

**Planning status**: the work items above are a proposal; no source-model semantic equivalence or expanded proof is claimed by writing this plan.
