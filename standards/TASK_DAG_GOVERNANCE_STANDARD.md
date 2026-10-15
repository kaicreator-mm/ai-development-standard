# Task DAG Governance Standard

Status: **Normative — v4.3**

## 1. Purpose

This standard governs material mutation of the execution Task DAG. Frozen planning DAG documents preserve planning/history authority; after materialization, GitHub native Issue Dependencies are the canonical live execution topology.

## 2. Planning DAG vs live DAG

`TASK_DAG.md` defines the frozen intended topology at planning time. GitHub Issue Dependencies represent the current live blocked-by graph after materialization.

Body text, Markdown status tables, PR stacks, branch names and cherry-pick order MUST NOT substitute for native live dependency edges.

## 3. Material mutation classes

Material DAG changes include at least:

```text
ADD
SPLIT
MERGE
SUPERSEDE
ADD_DEPENDENCY
REMOVE_DEPENDENCY
CHANGE_LANE
CHANGE_INTEGRATION_OWNER
DEFER
```

The vocabulary may be extended where needed; classification alone never authorizes mutation.

## 4. Required mutation evidence

Before applying a material live-DAG mutation, durable evidence MUST identify:

- requested and approving authority;
- reason;
- affected Task identities;
- old and proposed topology references;
- old and new edges;
- scope impact;
- release/version impact;
- affected Task Pack refs;
- Review impact;
- Validation impact/currentness.

`dag-mutation-record-v1` is the default machine evidence shape. It records the decision/evidence; it does **not** perform native GitHub mutation or determine readiness by itself.

## 5. Task identity preservation

A Task may not silently absorb materially different work merely to avoid DAG mutation. If scope changes the concern identity, authority boundary, dependency relationship, merge owner or required evidence materially, use an explicit DAG mutation such as SPLIT/MERGE/SUPERSEDE/ADD or a planning amendment as applicable.

## 6. Dependency removal and readiness

Removing a dependency is a material authority decision. The removal MUST NOT fabricate readiness when the removed edge encoded a still-material contract, evidence or integration dependency.

Before dispatch after a removal, re-evaluate the resulting Task Pack/currentness and native blocked-by state. An edge disappearing does not itself prove implementation prerequisites are satisfied.

## 7. Native mutation execution

Only an executor with the required GitHub/native mutation capability and task authority may change live Issue Dependencies. If that capability is unavailable, create an explicit controller/local handoff. Textual dependency lists are not an acceptable fallback for canonical topology.

## 8. PR stacks and code ancestry

Stacked PRs are appropriate only for a real unmerged code-baseline dependency. They do not replace Task DAG dependencies.

Likewise, cherry-pick order, branch ancestry or merge order MUST NOT be interpreted as canonical Task dependency authority unless the live Task DAG records the dependency.

## 9. Mutation currentness

A mutation decision is current only for the topology/Task Pack/evidence subject it reviewed. Material target, scope, Task Pack, Review or Validation drift requires re-evaluation before native mutation.

## 10. Failure handling

Unauthorized, incomplete or ambiguous mutations fail closed and preserve the prior live DAG. If native mutation cannot be performed, the work remains blocked until an authorized controller executes and reads back the exact graph.

## 11. v4.12 source Scaffold / Task DAG binding pair (SF ↔ DF)

A qualified v4.12+ project MAY freeze a **source-first Scaffold** (`SF`) and a subsequent **Task-side DAG binding** (`DF`) as one source-pinned, cycle-free pair. The canonical writer of each mapping lives on the **Task-side** binding; the frozen SF is structural evidence, not a second mutable Task owner and not an authority for the GitHub live dependency graph.

An accepted binding includes exact, independently verifiable identities for:

- Frozen Product and L2 source pins, the **actual accepted SF commit SHA** (not merely a branch name), its source-root/ref and a material Git-object inventory or reproducible material-view digest; file modes, symlinks and gitlinks are material, and unknown added/deleted/renamed/moved paths fail closed.
- Each structurally relevant SF anchor as a stable tuple `{anchor_id, kind, location, contract_ref}`. `location` must resolve inside the currently accepted material SF source, `contract_ref` to the accepted architectural semantics. A syntactically plausible path is not proof of an existing accepted anchor.
- A **single effective active writing Task** per anchor, its canonical Task Issue / frozen Task Pack identity and immutable DF Git blob; explicitly accepted read-only consumers MAY reference an anchor without becoming co-writers. Any overlap in active writers, dangling material anchor, malformed ID or unbound important output is `MATERIAL/HOLD`, not silently accepted.
- A distinct **mapping-integrity (`MI`) proof/digest**, independently computed from the canonical SF+DF input identities and structural relationships. DF hash and MI digest are different subjects. The output pair must be recomputed from both directions (`anchor → task` and `task → anchor`); the writer cannot accept its own generated JSON/index merely because it carries a self-declared hash.

```text
Frozen Product/L2 (exact)  →  accepted SF commit + material-view identity
                                          ↓ independently inspect
                           structural anchor_id/kind/location/contract_ref
                                          ↓ bind in one DF owner
Frozen planning DF blob + actual GitHub Task Issue identities
                                          ↓ independently recompute
                      SF→DF and DF→SF + separate MI proof
```

The **source view** can narrowly exclude a path only if a current source-owning authority approved the exact exclusion *before* the candidate is evaluated. `DAG_ONLY_INPUT` exempts genuinely DF-only inputs from the **SF material-view digest only**, while their DF/MI mappings are still validated; `DERIVED_NONAUTHORITATIVE` excludes regenerable indexes as source of authority but requires fresh independent regeneration/currentness proof. Never accept a writer-chosen post-hoc path exclusion, auto-ignore `.lock`/CI/manifests, broad wildcard carve-out, path rename, symlink/gitlink substitution or missing Git-object read. Material UNKNOWN → `HOLD`.

A material `SPLIT`, `MERGE`, `SUPERSEDE`, contract or writer change must use the existing `dag-mutation-record-v1` authority and rebind DF/MI and native Issue Dependencies as applicable. The frozen planning DAG is immutable history; GitHub native Issue Dependencies remain live execution truth. A pair verified with only static source/fixtures is **E1 source conformance**, not proof of a running feature, human approval, real-world effects or Version Release. Existing Product/L2 authority and real Claim/Review/Validation/Release requirements remain binding.

## 11. Non-goals

This standard does not create:

- a second DAG service;
- a new Task/workflow state vocabulary;
- Product or Architecture override authority;
- profile semantics;
- automatic native dependency mutation inside the schema.
