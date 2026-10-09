# v4.10.0 Wave B L3 Reference Pack R1

Status: **DURABLE PRE-ADMISSION L3 — JIT EXECUTION PACK STILL REQUIRED**

Authority: Frozen Product #837, Frozen L2 #842, refined DAG Freeze #848, Task Packs R1 #849, native DAG #866.

Wave B candidates unlocked by integrated predecessors:
- `V410-T01B` / #851 after #850 DONE;
- `V410-T04A` / #856 after #850 DONE;
- `V410-T05A` / #858 after #854 + #855 DONE.

This artifact narrows verifiable intent using `Tests → Contract/Invariant → Implementation seam → Failure Handling → References`. It does not bind task branches or implementation patches. Exact integration SHA and owner blobs belong to the JIT Execution Pack and MUST be read from the live integration tree.

---

## V410-T01B / #851 — Product evidence/research/review planning projections

### Tests
Positive cases MUST show:
1. L1 Product Evidence remains semantic framing/evidence and is not synonymous with external Product Research;
2. Product Research is selected only when evidence is insufficient and records bounded purpose/decision relevance;
3. Product Research and Architecture Research remain distinct in purpose, timing and owner;
4. low-risk/sufficient-evidence work can truthfully record inline/compact evidence or `NO_RESEARCH_REQUIRED` when policy permits;
5. Product Review remains risk/policy-selected evidence, never Product Freeze authority.

Negative cases MUST reject mandatory research ceremony, architecture research before Product Freeze, a second research lifecycle, and Review PASS manufacturing Product Freeze.

### Contract / invariant
- consume settled Stage-1 semantics integrated by V410-T01A;
- `prompts/L1_PRODUCT_EVIDENCE.md` and existing Product research templates are projections, not new semantic owners;
- R10 is satisfied by convergence onto existing Product/Architecture research owners.

### Implementation seam
Primary candidate surfaces: `prompts/L1_PRODUCT_EVIDENCE.md`, `templates/research-issue.md`, directly-owned Product planning references/tests. Do not rewrite `DEVELOPMENT_WORKFLOW.md` owner semantics or Architecture Research owner.

### Failure handling
If projection cannot express the settled owner without inventing a second lifecycle, stop as Task Pack/architecture defect. If a gap is purely central manifest/conformance wiring, route to T06A/T06B.

### References
#837, #842, #848, #850 DONE, Task Pack R1 V410-T01B, current Stage-1 owner.

---

## V410-T04A / #856 — Gate applicability and repair-routing convergence

### Tests
Positive cases MUST show:
1. required-gate applicability derives from authority, not cost/file count/docs-only/model confidence/speed;
2. `UNKNOWN` or contradictory applicability fails closed to the owning authority;
3. repair targets the root defect class rather than only a cited symptom;
4. repeated non-converging repair is escalated/adjudicated rather than looped indefinitely.

Negative cases MUST reject silent gate downgrade, arbitrary global retry caps, Product lifecycle redefinition, and Review finding/currentness semantics owned by T04B.

### Contract / invariant
- consume the integrated Stage-1 owner after V410-T01A;
- `DEVELOPMENT_WORKFLOW.md` owns lifecycle/gate routing;
- `VALIDATION_STANDARD.md` owns exact-subject validation/currentness semantics where clarification is necessary;
- no second gate state machine.

### Implementation seam
Prefer the smallest owner-local edits and directly-owned regressions. Touch `VALIDATION_STANDARD.md` only for an actual owned ambiguity; do not duplicate T04B Review semantics.

### Failure handling
Product contradiction routes to Product authority. Review aggregation/currentness gaps route to T04B. Gate owner ambiguity remains fail-closed and must not be papered over by controller preference.

### References
#837, #842, #848, #850 DONE, Task Pack R1 V410-T04A, current Development Workflow and Validation owners.

---

## V410-T05A / #858 — Shared-code safety under existing owners

### Tests / evidence question
First perform an evidence-first residual-gap check across the integrated V410-T03A and V410-T03B results plus Interface Compatibility owner.

A material-change path is justified only if a concrete residual gap remains for one or more of:
1. importability/reuse being incorrectly treated as stable/public contract;
2. Task-local implementation silently widening into project-wide promotion/refactor;
3. public compatibility bypassing compatibility authority;
4. textual similarity being treated as mandatory extraction/DRY authority.

A `NO_CHANGE_REQUIRED` outcome is valid when current owners already satisfy all four invariants. That outcome MUST cite exact owner identities and negative evidence; it MUST NOT fabricate Validation/Review PASS or create an empty PR merely for ceremony.

### Contract / invariant
- R5 remains `EXISTING_OWNER_ONLY`;
- Implementation Quality, Task Decomposition and Interface Compatibility remain the owners;
- no component registry, generic shared-code subsystem or mandatory DRY policy.

### Implementation seam
If a real residual gap exists, mutate only the owning standard/reference/test surface that actually owns it. Re-edit of settled T03 semantics requires explicit evidence that the integrated owner remains incomplete. Otherwise return durable `NO_CHANGE_REQUIRED` evidence.

### Failure handling
Ambiguous compatibility/public-contract semantics fail closed to Interface Compatibility authority. Broad refactor pressure is out of scope. Central discovery/manifest wiring routes to T06A/T06B.

### References
#837, #842, #848, #854 DONE, #855 DONE, Task Pack R1 V410-T05A, current Implementation Quality / Task Decomposition / Interface Compatibility owners.

---

## Wave B admission rule

```text
DEPENDENCY_REDUCTION=REQUIRED_FROM_NATIVE_DAG
LIVE_INTEGRATION_HEAD=READ_AFTER_THIS_L3_CHECKPOINT
OWNER_BLOBS=READ_FROM_EXACT_BASELINE_TREE_ONLY
JIT_TASK_BRANCH=AFTER_L3_AND_CURRENTNESS
JIT_EXECUTION_PACK=AFTER_L3_AND_CURRENTNESS
READY=ONLY_AFTER_CONTRACT+NATIVE_DAG+L3+CURRENTNESS
CLAIM=NONE_UNTIL_BUILDER_ACCEPTS
```

The Wave-A dogfood defect is now a hard local rule: **never infer or synthesize an owner blob SHA. Read it directly from the exact integration tree / GitHub contents API before admission.**