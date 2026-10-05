# JIT DAG Mutation Governance Reference (v4.9)

Non-normative, bounded wiring reference for v4.9 JIT materialization (`docs/implementation/4.9.0/task-packs/T09_jit_dag_governance.md`, Task `T-009`, issue #728). It deterministically classifies v4.9 runtime/JIT proposals and routes material changes to the canonical owner. It creates **no** second governance lifecycle and never redefines owner semantics: the v4.3 Task DAG Governance remains the only mutation authority — this reference cites it, it does not copy or replace it.

## 1. Exact authority binding (cited, not copied)

All mutation semantics below are owned by existing contracts and consumed by exact reference:

```text
Task DAG mutation owner (normative)   standards/TASK_DAG_GOVERNANCE_STANDARD.md
                                      §3 material mutation classes
                                      §4 required mutation evidence (dag-mutation-record-v1)
                                      §5 task identity preservation
                                      §6 dependency removal and readiness
                                      §7 native mutation execution
                                      §9 mutation currentness
                                      §10 failure handling (fail closed)
                                      §11 non-goals
Mutation record schema (owner)        schemas/dag-mutation-record-v1.schema.json
Owner guidance (non-normative)        references/TASK_DAG_GOVERNANCE_REFERENCE.md
Owner test suites (execution ref)     scripts/test_v43_task_dag_governance.py
                                      scripts/test_v43_dag_mutation_contract.py
JIT predicate this wires into         standards/EXECUTION_ARCHITECTURE_STANDARD.md
                                      §28.2 legal JIT phase predicate (envelope conditions;
                                      "A material topology change ... is not a JIT phase:
                                      it routes to v4.3 Task DAG mutation governance")
                                      §28.3 WAITING_LINEAGE derived non-dispatch projection
                                      §28.7 acceptance binding L -> [K02/K09] + L2 negatives
Frozen Product item L                 docs/implementation/4.9.0/PRD.md "### L. Task-DAG scope
                                      protection" — adaptive orchestration cannot invent new
                                      semantic implementation work/dependencies outside Frozen
                                      Task authority
Frozen L2 negatives                   docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md
Frozen Task DAG v0.2                  blob b9fe0cc7089f64929b4bcf45f7230d950e864db2
Concern authority (immutable)         DAG v0.1 blob 4f358ba2b32e01ae17ddcdf970151cf28e44bb3f
                                      section "### T-009"
Late evidence binding                 #728 comment "V49_LATE_EVIDENCE_BINDING — #775 -> T009"
                                      (consumed only through the v4.3 mutation authority, §6)
```

The material mutation class vocabulary is loaded from the owner standard §3 at runtime — it is never duplicated as an independent definition here. The mutation-record required fields are loaded from the owner schema — never restated as a divergent list here.

## 2. Deterministic classification

Every v4.9 runtime/JIT proposal is classified into exactly one of three outcomes before any execution effect. Classification is a pure function of the proposal and current durable facts; identical inputs produce identical outcomes; classification alone never authorizes mutation (owner §3).

### 2.1 Bookkeeping — execution-container bookkeeping, NOT semantic mutation

Bookkeeping operates the execution container of an **existing** materialized Task. It is legal only while **all** of the following hold (any `true` violation or unprovable `unknown` fails closed):

```text
E1 no new semantic implementation concern is created
E2 no Task ownership changes
E3 no existing dependency semantics change (no native blocked-by edge added/removed/rewired)
E4 no Task write/acceptance scope widens
E5 no semantic Task identity is created, absorbed, closed or superseded
```

Bookkeeping action vocabulary (execution-container operations only):

```json
{
  "bookkeeping_actions": {
    "jit_phase_dispatch_same_issue": "Just-in-time phase materialized on the SAME native Issue inside the §28.2 Task envelope (E1-E4 hold); one Dispatch/Claim lifecycle; per-phase admission",
    "claim_or_dispatch_record": "Claim/dispatch state records for an existing Task; the section 11 lifecycle only",
    "derived_state_projection": "Derived recomputable projections such as §28.3 WAITING_LINEAGE; non-dispatchable, non-authoritative, never a canonical Issue state",
    "branch_or_worktree_creation": "JIT branch/worktree creation per DEVELOPMENT_WORKFLOW JIT branch rules; code ancestry is not DAG authority (owner §8)",
    "pr_stack_creation": "Stacked PRs for a real code-baseline dependency only; they never replace Task DAG dependencies (owner §8)",
    "status_label_or_annotation_update": "Labels, comments, body status tables, checklists; body text MUST NOT substitute for native live dependency edges (owner §2)"
  }
}
```

Bookkeeping NEVER silently changes semantic topology: zero native edge changes, zero semantic Task create/close/supersede, zero identity absorption. A bookkeeping action that carries a topology effect is not bookkeeping — it fails closed as ambiguous (§2.3).

### 2.2 Semantic mutation — routes to the v4.3 owner

A proposal is a **semantic mutation** when its action is a material mutation class in owner §3 (`ADD`, `SPLIT`, `MERGE`, `SUPERSEDE`, `ADD_DEPENDENCY`, `REMOVE_DEPENDENCY`, `CHANGE_LANE`, `CHANGE_INTEGRATION_OWNER`, `DEFER`, or a later owner extension of that vocabulary). Every semantic mutation — including runtime-originated ones — routes through the v4.3 governance: `dag-mutation-record-v1` evidence (owner §4), authorized native mutation execution (owner §7), and read-back of the exact resulting graph. Per EXECUTION_ARCHITECTURE_STANDARD §28.2: a material topology change is not a JIT phase.

### 2.3 Ambiguous — fail closed

Unknown actions, unprovable (`unknown`) conditions/effects, or bookkeeping actions carrying topology effects classify as ambiguous. Ambiguous semantic impact routes to the material mutation path or `BLOCKED`; it is **never** silently materialized as new topology and never downgraded to bookkeeping (owner §10; §28.2 fail-closed posture).

## 3. Routing table (machine-readable)

The routing for each owner mutation class. `record` and `native_action` are owner-consumed requirements; the route identifiers are this reference's wiring names (consistent with `test_v49_execution_core.classify_topology_change`).

```json
{
  "routes": {
    "ADD":                      {"record": "dag-mutation-record-v1", "native_action": "create new native Issue; add native blocked-by edges; read back exact graph", "route": "V43_MUTATION_ADD"},
    "ADD_DEPENDENCY":           {"record": "dag-mutation-record-v1", "native_action": "add native blocked-by edge(s) by authorized executor; read back exact graph", "route": "V43_MUTATION_ADD_DEPENDENCY"},
    "REMOVE_DEPENDENCY":        {"record": "dag-mutation-record-v1", "native_action": "owner §6 readiness re-evaluation first; remove native blocked-by edge; read back exact graph", "route": "V43_MUTATION_REMOVE_DEPENDENCY"},
    "SPLIT":                    {"record": "dag-mutation-record-v1", "native_action": "owner §5 identity preservation; create successor Issue(s); rewire native edges; read back exact graph", "route": "V43_MUTATION_SPLIT"},
    "MERGE":                    {"record": "dag-mutation-record-v1", "native_action": "owner §5 no silent absorption; consolidate native edges; read back exact graph", "route": "V43_MUTATION_MERGE"},
    "SUPERSEDE":                {"record": "dag-mutation-record-v1", "native_action": "mark predecessor superseded; wire successor edges natively; read back exact graph", "route": "V43_MUTATION_SUPERSEDE"},
    "DEFER":                    {"record": "dag-mutation-record-v1", "native_action": "keep Task in live DAG with re-planned target; DEFER never silently removes edges; read back exact graph", "route": "V43_MUTATION_DEFER"},
    "CHANGE_LANE":              {"record": "dag-mutation-record-v1", "native_action": "update lane binding; native edges unchanged unless recorded; read back exact graph", "route": "V43_MUTATION_CHANGE_LANE"},
    "CHANGE_INTEGRATION_OWNER": {"record": "dag-mutation-record-v1", "native_action": "update integration owner binding; read back exact graph", "route": "V43_MUTATION_CHANGE_INTEGRATION_OWNER"}
  },
  "unavailable_native_capability_route": "V43_NATIVE_MUTATION_HANDOFF",
  "fail_closed_route": "FAIL_CLOSED_PRESERVE_PRIOR_LIVE_DAG"
}
```

`REMOVE_DEPENDENCY` additionally obeys owner §6: an edge disappearing never fabricates readiness; if the removed edge encoded a still-material contract/evidence/integration dependency, the removal is invalid. When the native mutation capability is unavailable, the route is an explicit controller/local handoff (owner §7) with exact intended edges and a read-back equality check — a textual dependency list is never the fallback.

## 4. Runtime-originated proposals — binding requirements

A semantic proposal originating at runtime/JIT (not from canonical planning) must satisfy all of:

```text
R1 CLASSIFY FIRST   deterministic §2 classification precedes any effect; bookkeeping stays
                    bookkeeping; ambiguous => material mutation path or BLOCKED (never silent
                    materialization of new topology)
R2 MUTATION RECORD  a complete dag-mutation-record-v1 (all schema-required fields present and
                    non-empty: requested_by/approved_by authority, reason, affected Task
                    identities, old/new topology refs, old/new edges, scope/release impact,
                    Task Pack/Review/Validation impact) — the record documents the decision;
                    it does not perform the mutation by itself (owner §4)
R3 NATIVE HYDRATION the live graph change is performed as native GitHub Issue Dependency
                    mutation by an executor with that capability and task authority (owner §7),
                    then read back; textual dependency lists (body text, Markdown tables, PR
                    stacks, branch names, cherry-pick order) CANNOT substitute for native
                    graph facts (owner §2)
R4 CURRENTNESS      the record binds the exact subject it reviewed (topology digest, Task Pack
                    refs); material target/scope/Task Pack/Review/Validation drift between
                    record approval and native mutation requires re-evaluation before the
                    native mutation (owner §9); stale or unprovable currentness fails closed
                    (owner §10) and preserves the prior live DAG
R5 ENVELOPE         a runtime proposal that would create a new semantic concern, change
                    ownership/dependency semantics, or widen scope is out of the §28.2 JIT
                    envelope by definition and must go through R1-R4; it is never auto-admitted
                    as a JIT phase (Frozen Product L; §28.7 binding L)
R6 SINGLE OWNER     runtime classification adds no mutation authority: no second DAG service,
                    no new state vocabulary, no automatic native dependency mutation inside
                    the schema (owner §11); the v4.3 owner stays canonical
```

## 5. Mutation currentness (fail closed)

The classifier evaluates currentness against current durable facts per proposal:

```text
record digest == live topology digest AND Task Pack refs resolve current  => current, R2-R3 may proceed
record digest != live topology digest                                     => FAIL_CLOSED_STALE_MUTATION_RECORD
digest/refs missing or unprovable                                         => FAIL_CLOSED_UNKNOWN_CURRENTNESS
```

A stale or unprovable proposal fails closed: no native mutation is performed and the prior live DAG is preserved (owner §9/§10). Re-evaluation (a fresh, current record) is the only forward path.

## 6. Telemetry is advisory only (#775 late evidence binding)

Per the `V49_LATE_EVIDENCE_BINDING — #775 -> T009` comment on #728, consumed only through the v4.3 mutation authority already bound above: when an already-frozen live Task proves operationally oversized but still semantically coherent, the only structural responses are explicit authorized owner mutations (`SPLIT`, `SUPERSEDE`, `ADD`, dependency change, or an equivalent owner-defined class) with durable reason/impact/currentness. Operational telemetry — duration, LOC, changed-file count, context growth — is **advisory evidence only**: it cannot independently authorize a mutation, cannot substitute for `requested_by`/`approved_by` authority, and cannot downgrade a semantic mutation to bookkeeping. Task identity, native dependencies and readiness are never silently edited because an agent wants smaller work units; semantic/authority atomicity wins over concurrency; fake parallelism and lineage-as-edge remain forbidden.

A proposal whose only justification is telemetry classifies `FAIL_CLOSED_TELEMETRY_CANNOT_AUTHORIZE` (route `FAIL_CLOSED_PRESERVE_PRIOR_LIVE_DAG`).

## 7. Executable oracles

`scripts/test_v49_jit_dag_governance.py` executes the deterministic classifier against `fixtures/jit-dag-governance/**`:

```text
G01 bookkeeping is NOT semantic mutation and never silently changes semantic topology
G02 ADD / ADD_DEPENDENCY / REMOVE_DEPENDENCY / split / merge / supersede / defer (and the
    remaining owner §3 classes) route exactly per the §3 routing table
G03 runtime-originated semantic proposals require mutation record + native dependency
    hydration; textual dependency lists cannot substitute for native graph facts
G04 mutation-currentness enforced; stale proposals fail closed and preserve the prior live DAG
G05 Frozen Product L + Frozen L2 JIT/DAG negatives executable with exact refs
G06 no second governance lifecycle; v4.3 owner cited (vocabulary/record fields loaded from
    owner artifacts at runtime), not copied
```

These are Builder-level deterministic classification checks (TEST_MATRIX T-009); they are not independent Validation and do not merge anything.
