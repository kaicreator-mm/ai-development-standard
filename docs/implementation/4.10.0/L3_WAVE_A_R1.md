# v4.10.0 Wave A L3 Reference Pack R1

Status: **DURABLE PRE-ADMISSION L3 — NON-EXACT-BASE — JIT EXECUTION PACK STILL REQUIRED**

Checkpoint: `#867`
Refined DAG Freeze: `#848`
Task Packs: `docs/implementation/4.10.0/TASK_PACKS_R1.md`
Wave A Issues: `#850`, `#852`, `#854`, `#855`
Native DAG materialization: `#866` pending

This artifact follows `Tests → Contract/Invariant → Implementation seam → Failure Handling → Reference`. It narrows verifiable intent without binding an execution base, branch, patch or line-level HOW.

Common rules:

```text
EXACT_BASE_BINDING=JIT_EXECUTION_PACK_ONLY
SOURCE_MUTATION_AUTHORITY=NO
TASK_BRANCH=NO
READY_TRANSITION=NO
CURRENT_OWNER_REBIND=REQUIRED_AT_ADMISSION
```

---

## V410-T01A / #850 — Stage-1 canonical lifecycle semantics

### Tests

Positive cases must demonstrate:

1. material/new normative Product scope can reconstruct `Idea/Intent → Intake/Baseline → semantic L1 → Product Research as needed → Draft PRD/Scope → selected Product Review → Product Freeze`;
2. Product Review is independent evidence/judgment and Freeze is an explicit Product-authority act;
3. Product Research can be selected because evidence is insufficient without becoming a second authority.

Negative cases must demonstrate:

1. low-risk/sufficient-evidence work is not forced into mandatory separate Research or Product Review when no owner requires it;
2. L1 is not collapsed into mandatory external research;
3. Architecture Research/Demo is not moved before Product Freeze as a Product-discovery substitute;
4. Review PASS alone cannot manufacture Product Freeze.

### Contract / invariant

- Frozen PRD v0.4 R1 lifecycle semantics;
- Frozen L2 §4 Product lifecycle / Product Review selection and authority boundary;
- `DEVELOPMENT_WORKFLOW.md` remains lifecycle routing owner;
- existing Fast Path remains legal when applicable.

### Implementation seam

Primary semantic mutation belongs to `standards/DEVELOPMENT_WORKFLOW.md` and directly-owned lifecycle tests/references. Product planning projections belong downstream to V410-T01B.

Do not edit central manifest/shared machine projection surfaces here; those converge in T06A/T06B.

### Failure handling

- Product contradiction → stop and route to Product authority; do not weaken Frozen PRD;
- ambiguity requiring a second lifecycle → Task Pack/Architecture defect, stop;
- projection-only mismatch outside lifecycle owner → record for T01B/T06B rather than expanding scope.

### References

- Product Freeze `#837`;
- L2 Freeze `#842`;
- refined DAG `#848`;
- `standards/DEVELOPMENT_WORKFLOW.md`;
- `prompts/L1_PRODUCT_EVIDENCE.md` as downstream projection evidence only.

---

## V410-T02A / #852 — Human + Multi-Agent responsibility/control semantics

### Tests

Positive cases must cover:

1. `DELEGATED_SUBWORK`: delegator retains responsibility while child returns bounded result/evidence;
2. `RESPONSIBILITY_HANDOFF`: active responsibility transfers explicitly within delegatable authority;
3. effective child authority is bounded by delegatable authority ∩ Task/Work authority ∩ role authority ∩ external/project authorization;
4. responsibility/causation is reconstructible for material authority-bearing work;
5. Human Decision/control points allow inspection and authorized stop/cancel/redirect without making humans routine relays.

Negative cases must reject:

1. capability/credentials/tool access expanding authority;
2. nested/parallel second Claim lifecycle;
3. a second Human approval workflow created merely to express controllability;
4. deterministic polling/prompt-relay work requiring human intervention by default.

### Contract / invariant

- Frozen PRD R3/R4;
- Frozen L2 §6;
- `EXECUTION_ARCHITECTURE_STANDARD.md` remains owner of durable execution facts/dispatch/controllers/Human Decision mechanisms;
- responsibility semantics must compose with the existing GitHub interaction/event family.

### Implementation seam

Primary owner-local semantics belong to `standards/EXECUTION_ARCHITECTURE_STANDARD.md` and directly-owned tests/references. Machine/event projection is V410-T02B and must consume settled semantics rather than redefine them.

### Failure handling

- need for incompatible new execution state family → architecture contradiction/Task Pack defect;
- exact schema-field necessity discovered → preserve semantic facts here, route additive projection to T02B;
- security/external authorization ambiguity → fail closed to owning authority.

### References

- Product Freeze `#837`;
- L2 Freeze `#842`;
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md`;
- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` as consumer/projection boundary.

---

## V410-T03A / #854 — Automation-first implementation quality

### Tests

Positive coverage must show quality policy catches materially risky patterns through engineering evidence/review semantics, including:

- unnecessary whole-file rewrite that destroys maintained intent;
- unrelated formatting/generated churn mixed with semantic change;
- hidden semantic change outside declared scope;
- direct mutation of generated outputs that ignores regeneration authority;
- unnecessary public-surface widening/abstraction.

Negative coverage must show:

- no universal human line-by-line code-reading gate;
- docs/style churn alone is not automatically a defect without material maintenance/evidence impact;
- automated tests/checks do not by themselves create Release authority.

### Contract / invariant

- Frozen PRD R4 automation/evidence-first quality;
- Frozen L2 §7;
- `IMPLEMENTATION_QUALITY_STANDARD.md` is language-neutral quality owner;
- maintainability/diff hygiene remains enforceable without Human Reviewability as a Product hard gate.

### Implementation seam

Owner-local changes belong to `standards/IMPLEMENTATION_QUALITY_STANDARD.md` and its direct reference/fixture/test surfaces. Task decomposition semantics belong to V410-T03B. Shared-code promotion residuals belong to V410-T05A after T03 semantics settle.

### Failure handling

- finding requires new Product quality requirement → Product contradiction, stop;
- split/parallelism problem rather than implementation quality → route to T03B;
- shared-code compatibility promotion question → route to T05A / compatibility owner.

### References

- Product Freeze `#837`;
- L2 Freeze `#842`;
- `standards/IMPLEMENTATION_QUALITY_STANDARD.md`;
- Task Pack R1 V410-T03A.

---

## V410-T03B / #855 — Agent-dispatchable Task decomposition and safe parallelism

### Tests

Positive cases must exercise:

1. one coherent concern spanning multiple files;
2. one file touched by sequential Tasks with explicit ownership/conflict control;
3. real independent lanes with no shared mutable contract/write collision;
4. central wiring isolated after owner-local siblings;
5. a large atomic invariant retained as one Task when splitting would create partial-invalid states.

Negative cases must reject:

1. file-count/LOC/token/time thresholds as universal split authority;
2. fake parallel branches that each need an unmerged sibling to be correct;
3. dependencies created only from desired conversation/review order;
4. dependency removal used to fabricate READY;
5. stacked PR used as a substitute for Task DAG.

### Contract / invariant

- Frozen PRD R7;
- Frozen L2 §8;
- `TASK_DECOMPOSITION_STANDARD.md` owns `minimum coherent concern + maximum safe parallelism`;
- `TASK_DAG_GOVERNANCE_STANDARD.md` owns material topology mutation after planning;
- native Issue Dependencies become canonical live DAG after materialization.

### Implementation seam

Primary semantics belong to `standards/TASK_DECOMPOSITION_STANDARD.md` and directly-owned examples/tests. DAG mutation governance is referenced, not rewritten unless a concrete owner defect is proven and separately authorized.

### Failure handling

- ambiguous concern atomicity → keep unresolved/together; do not force split;
- missing architecture fact required to decompose safely → architecture contradiction/research disposition;
- native dependency write capability unavailable → explicit capability handoff (#866), never prose fallback.

### References

- Product Freeze `#837`;
- L2 Freeze `#842`;
- refined DAG Freeze `#848` as current dogfood example;
- `standards/TASK_DECOMPOSITION_STANDARD.md`;
- `standards/TASK_DAG_GOVERNANCE_STANDARD.md`;
- `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`.

---

## Wave A pre-admission terminal

```text
L3_V410_T01A=PREPARED
L3_V410_T02A=PREPARED
L3_V410_T03A=PREPARED
L3_V410_T03B=PREPARED
NATIVE_DAG=#866 PENDING
EXACT_BASE_REBIND=NOT_RUN
JIT_BRANCHES=NO
EXECUTION_PACKS=NO
READY=NO
```

After #866 native graph PASS, the Controller must re-read the then-current `version/v4.10.0` exact SHA and owner surfaces. Only then may it create each zero-dependency task branch JIT, generate/bind an exact-base Execution Pack, transition the Issue through valid admission metadata and accept a Builder claim.