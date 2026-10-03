# v4.9.0 L1 Product Evidence — Adaptive Proportional Development Orchestration

Status: **COMPLETE RESEARCH / RECONCILED FOR PRD v0.4 / PRE-FREEZE**

Planning parent: `#697`
Primary dogfood input: `#680`
Claude adversarial input: `#702@5966353271`
Current Product candidate: `PRD v0.4`

## 1. Research question

Can ADS make execution materially more proportional and adaptive without weakening authority, currentness, independence, evidence truth or release safety?

## 2. Existing authority substrate

v4.9 is not a greenfield workflow system. It builds on current ADS workflow/review/validation/release semantics and on frozen v4.8 authority.

The v4.8 predecessor authority explicitly reused by v4.9 is:

```text
V48_FROZEN_PRD_BLOB=f26439580e00de6ed8b2e27d732a3095eb566219
V48_FROZEN_L2_BLOB=f88c85454e80101a0fdf56050e21f11a05279841
```

v4.8 already owns:

- Agent capability/eligibility/resource evidence;
- Dispatch/Claim execution ownership;
- Task Learning Evidence v1 including `NONE_MATERIAL`;
- `ADS_EVOLUTION_CANDIDATE` and the existing ADS Evolution Intake path.

Therefore v4.9 Product must extend/reuse these owners rather than create parallel capability, claim, learning or evolution lifecycles.

## 3. Direct ADS dogfood evidence

#680 demonstrates recurring orchestration amplification across v4.x: small/medium work can expand into Builder, Validation, Fresh Review, merge, Stage1, Candidate Freeze, Hidden, Closeout, Release Qualification, integration and currentness/rebind operations.

#680 also records examples where:

- durable Issues were safely reused across role-separated phases;
- branch/target movement sometimes added no new decision value;
- deterministic controller transitions did not always justify separate task containers;
- real Hidden/Release findings still required the complete thaw/repair/review/requalification path.

This supports the Product problem: ADS needs proportional execution **inside existing authority**, not blanket gate removal.

## 4. Quantification boundary

The current L1 corpus does not yet provide a complete representative quantified baseline showing:

```text
which execution objects/gates added new decision value
vs
which duplicated orchestration without changing the decision
```

The evidence is therefore sufficient to support the Product problem and design direction but insufficient for a numeric savings/economic claim.

```text
ORCHESTRATION_AMPLIFICATION=SUPPORTED_QUALITATIVELY
AMPLIFICATION_QUANTIFICATION=PARTIAL
ECONOMIC_BENEFIT=NOT_MEASURED
```

PRD v0.4 closes this evidence gap prospectively: the downstream dogfood baseline must record containers/issues, dispatches/claims, independent gates/sessions, rebind/revalidation events and decision-value accounting. No retrospective numbers may be invented.

## 5. Claude #702 adversarial falsification of PRD v0.3

Claude's second independent adversarial review of exact PRD v0.3 returned:

```text
VERDICT=FAIL
P0=0
P1=3
P2=6
P3=3
CURRENTNESS=PASS
```

The material findings were:

1. single-owner reduction predicates no longer required durable/deterministic proof and ambiguous classification no longer explicitly failed closed;
2. downstream dogfood could pass vacuously without any proportional decision or independent audit;
3. P4 overlapped v4.8 Task Learning/Evolution ownership and lost explicit scope fences;
4. exact-candidate independent Product Review precondition was weakened;
5. specialized-role scope was broadened unintentionally;
6. adverse Review FAIL could be bypassed through redispatch/reviewer shopping;
7. migration could retroactively shorten an in-flight release path;
8. release-applicability ownership was under-specified;
9. reused v4.8 authority was not bound to exact predecessor Product/L2 identities;
10. broken cross-references and undispositioned v0.2 safety deletions remained;
11. #680 entry-criteria quantification remained partial.

PRD v0.4 treats these as Product evidence, not editorial suggestions.

## 6. Monotonic assurance finding

The v0.3 multi-owner conjunction direction was correct but incomplete. A monotonic conjunction is only safe if each reduced owner requirement is itself derived from proven predicates.

Required Product invariant:

```text
OWNER_PERMISSION
+ CURRENT_DURABLE_OR_DETERMINISTIC_PREDICATE_PROOF
=> REDUCTION_MAY_BE_SELECTED

UNKNOWN_OR_AMBIGUOUS_PREDICATE
=> STRONGER_PATH_OR_BLOCKED

MODEL_JUDGMENT_ONLY
=> NOT_SUFFICIENT_FOR_REDUCTION
```

This applies both to cross-owner composition and a single uncontested owner.

## 7. Release applicability evidence

#680's proportionality goal includes concern-level work that should not automatically trigger unrelated full release ceremony. Existing Release authority, however, owns release applicability.

Therefore v4.9 Product direction is:

- Release applicability remains `RELEASE_STANDARD`-owned;
- v4.9 may define **prospective** Release-owned proportional applicability predicates;
- no Orchestrator/model may independently classify out of mandatory release gates;
- unknown predicates fail closed;
- migration cannot retroactively shorten gates already bound to an in-flight Frozen/qualified candidate.

This keeps the Product goal achievable without allowing L2 or an Agent to invent release authority.

## 8. Evidence transfer

Evidence reuse remains a gate-owned positive-permission problem, not a generic topology heuristic.

Different evidence families bind different tuples. Reuse requires:

- a positive transfer rule from the owning Gate Authority;
- equality/proven equivalence across every required binding dimension;
- no changed non-transferable dimension;
- no fresh-only rule;
- durable/current proof.

Path disjointness or unchanged HEAD/tree may be proof inputs but are never universal transfer authority.

## 9. Independence

Independence is multi-dimensional. Relevant dimensions can include principal/logical executor, session/context, model/provider/configuration, Builder/Reviewer author separation, host/environment, evidence source, Hidden holder and Release/Controller separation.

PRD v0.4 also recognizes selector conflict: a Controller/selector that authored or materially controlled a subject may be ineligible to select its required independent evaluator when current authority says that conflict matters.

A different Issue/session alone never proves independence.

## 10. Adverse terminal truth

Adaptive orchestration must consume adverse terminals, not merely preserve them as history.

The existing finding-union/blocker-dominance model implies:

- FAIL/findings cannot be silently superseded;
- repeated dispatch cannot be used to search for a PASS;
- re-review after FAIL requires successor subject or owning-authority disposition.

This is necessary because JIT executor selection otherwise creates a new path for de facto authority laundering.

## 11. Task DAG boundary

The Frozen Task DAG/current Task authority is the semantic work envelope.

JIT orchestration may materialize role phases/containers inside that envelope, but material new concern, dependency, ownership or scope requires ordinary amendment/governance.

Whether a proposed live change is materially inside/outside the envelope is itself subject to the fail-closed predicate-proof rule.

## 12. v4.8 learning/evolution ownership

v4.8 already owns Task Learning Evidence and ADS Evolution Intake. v4.9 P4 therefore has only a bounded delta:

- map execution-friction categories into/back onto v4.8 Task Learning evidence;
- add a bounded recurrence-audit escalation hook;
- feed eligible results into existing `ADS_EVOLUTION_CANDIDATE` governance.

v4.9 does not authorize parallel learning/evolution records, a new intake lifecycle, automated cross-project mining, universal fingerprinting or a dedicated learning database.

## 13. Generality evidence

External interoperability/scheduling systems support the structural idea of separating reasoning, deterministic enforcement and durable task facts. They do **not** prove ADS gate-reduction correctness.

Therefore:

```text
PRODUCT_PROBLEM=SUPPORTED
ADS_DOGFOOD=SUPPORTED
EXTERNAL_ARCHITECTURAL_ANALOGY=SUPPORTED
DOWNSTREAM_GENERALITY=PARTIAL
CROSS_PROJECT_GATE_REDUCTION_PROOF=NOT_YET_PROVEN
```

## 14. Downstream dogfood acceptance evidence needed before Release

A qualifying downstream project must be a distinct real product/repository with its own pinned authority artifacts, not ADS itself or an ADS-governance mirror.

Before v4.9 Release can claim generality, dogfood must:

- bind to an exact v4.9 candidate/revision;
- bind a legal baseline authority/gate contract;
- record the selected proportional execution;
- mark each claimed mechanism `EXERCISED|NOT_EXERCISED`;
- exercise at least one unknown/ambiguous reduction predicate and show stronger path/BLOCKED;
- show at least one nonzero authorized baseline-vs-selected delta;
- independently audit safety negatives against durable evidence;
- prove manual/GitHub-native viability;
- limit generality claims to mechanisms actually exercised.

Required safety negatives include:

```text
UNAUTHORIZED_GATE_OMISSION=0
STALE_PASS_TRANSFER=0
INDEPENDENCE_LOSS=0
CROSS_OWNER_REQUIREMENT_CANCELLATION=0
ADVERSE_TERMINAL_SUPPRESSION=0
```

## 15. Product direction

The evidence supports one integrated v4.9 Product direction:

```text
P1 Proportional Assurance
+ P2 Adaptive Orchestration
+ P3 Agent Operating Model
+ P4 bounded v4.8-compatible Execution Learning/Recurrence extension
```

with these non-negotiable boundaries:

- monotonic multi-owner assurance floor;
- durable/deterministic proof for every reduction predicate;
- fail-closed ambiguity;
- existing Release authority ownership;
- prospective-only migration;
- gate-owned evidence transfer;
- multi-dimensional independence;
- adverse-terminal dominance;
- Task-DAG scope protection;
- exact v4.8 predecessor bindings;
- no second Dispatch/Claim or Learning/Evolution lifecycle;
- non-vacuous downstream release dogfood.

## 16. L1 disposition

```text
L1_STATUS=COMPLETE_RESEARCH_RECONCILED_FOR_V04
PRODUCT_DIRECTION=PROCEED
PRODUCT_PROBLEM=SUPPORTED
AMPLIFICATION_QUANTIFICATION=PARTIAL
ECONOMIC_BENEFIT=NOT_MEASURED
DOWNSTREAM_GENERALITY=PARTIAL
V48_PREDECESSOR_BINDING=REQUIRED
ASSURANCE_FLOOR=MONOTONIC_MULTI_OWNER_WITH_PROVEN_OWNER_PREDICATES
EVIDENCE_TRANSFER=GATE_OWNED_POSITIVE_PERMISSION_ONLY
INDEPENDENCE=MULTI_DIMENSIONAL
ADVERSE_TERMINAL_DOMINANCE=REQUIRED
RELEASE_APPLICABILITY_OWNER=RELEASE_STANDARD_PROSPECTIVE_POLICY
P4_OWNER=V48_TASK_LEARNING_AND_EVOLUTION_INTAKE
PRODUCT_FREEZE=NO
FRESH_V04_PRODUCT_REVIEW=REQUIRED
L2_AUTHORITY=NO
TASK_DAG_AUTHORITY=NO
IMPLEMENTATION_AUTHORITY=NO
```
