# Manual / GitHub-Native Reference Flow (v4.9 T-013)

Status: **descriptive operator/controller reference — non-authoritative.**

This reference documents how the v4.9 proportional-orchestration workflow can be operated
by hand, from durable GitHub/repository facts only, with git and the GitHub CLI/API as the
only tooling. It is a descriptive walkthrough for operators and controllers; it creates
no normative semantics. Every normative rule below is owned by the exact reference cited
next to it, and the owner text always controls over this summary.

## 1. Consumed authorities (exact refs, cited not copied)

```text
standards/EXECUTION_ARCHITECTURE_STANDARD.md#4-durable-facts-derived-state-actions
standards/EXECUTION_ARCHITECTURE_STANDARD.md#41-durable-facts
standards/EXECUTION_ARCHITECTURE_STANDARD.md#42-derived-state
standards/EXECUTION_ARCHITECTURE_STANDARD.md#5-separate-state-dimensions
standards/EXECUTION_ARCHITECTURE_STANDARD.md#8-pointer-only-agent-invocation
standards/EXECUTION_ARCHITECTURE_STANDARD.md#11-dispatch-lifecycle-atomic-claim-and-staleness
standards/EXECUTION_ARCHITECTURE_STANDARD.md#111-required-claim-serialization-capability
standards/EXECUTION_ARCHITECTURE_STANDARD.md#291-assurance-plan-currentness-consumption-at-architecture-owned-transitions
standards/EXECUTION_ARCHITECTURE_STANDARD.md#292-legal-jit-phase-predicate
standards/EXECUTION_ARCHITECTURE_STANDARD.md#293-waiting_lineage-derived-non-dispatch-projection
standards/EXECUTION_ARCHITECTURE_STANDARD.md#295-adverse-finding-carry-forward-and-no-review-shopping-routing
standards/EXECUTION_ARCHITECTURE_STANDARD.md#296-deterministic-recompute-on-currentness-drift-racedrift-fail-closed
standards/EXECUTION_ARCHITECTURE_STANDARD.md#26-non-goals
standards/ISSUE_FIRST_TASK_TRIGGER.md#canonical-rule
standards/ISSUE_FIRST_TASK_TRIGGER.md#durable-contract-precondition
standards/ISSUE_FIRST_TASK_TRIGGER.md#user-visible-trigger-contract
standards/ISSUE_FIRST_TASK_TRIGGER.md#forbidden-task-specific-trigger-content
standards/ASSURANCE_PLAN_STANDARD.md#12-currentness-binding
standards/ASSURANCE_PLAN_STANDARD.md#13-adverse-finding-carry-forward
standards/TASK_DAG_GOVERNANCE_STANDARD.md
registries/state-dimensions-v1.json#F11_TASK_DONE_NOT_LINEAGE_CURRENT
registries/state-dimensions-v1.json#F13_ASSURANCE_CURRENT_NOT_VALIDATION_PASS
registries/state-dimensions-v1.json#F17_WAITING_LINEAGE_NOT_WORKFLOW_BLOCKED
references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md
references/JIT_DAG_MUTATION_GOVERNANCE_V49_REFERENCE.md
docs/implementation/4.9.0/task-packs/T13_manual_reference_flow.md
docs/implementation/4.9.0/L3_REFERENCE_PACKS.md#t-013--manual--github-native-reference-flow-732
scripts/test_v49_manual_reference_flow.py
fixtures/manual-reference-flow/durable_facts.json
fixtures/manual-reference-flow/derived_projections.json
fixtures/manual-reference-flow/pointer_triggers.json
fixtures/manual-reference-flow/walkthroughs.json
```

Frozen authority blobs, verified to resolve unchanged at this Task's base
`version/v4.9.0@d53e943ec7109648485b64a647ed2c7cf553531d`:

```text
docs/implementation/4.9.0/PRD.md                  blob a8ec7030a14337a4c2dca853dc474e965679d610
docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md blob bd41ea0175b459a6a490fd37ad579e429a58a1c3
docs/implementation/4.9.0/TASK_DAG.md             blob b9fe0cc7089f64929b4bcf45f7230d950e864db2
```

The immutable concern for this Task is section `### T-013` of DAG v0.1 blob
`4f358ba2b32e01ae17ddcdf970151cf28e44bb3f` (resolved from the repository object store,
not from any mutable copy).

## 2. Execution environment: GitHub-native and manual

Operating this workflow requires only:

1. a local clone/worktree of the repository (git);
2. GitHub Issues, native Issue Dependencies, PRs, and comments (read through `gh` or any
   GitHub API client);
3. repository files at exact revisions (Task Packs, standards, schemas, registries,
   Assurance Plans, fixtures).

The flow requires no scheduler daemon, no runtime database, and no proprietary transport:
every fact that authorizes a step is read from git objects or GitHub surfaces at the
moment it is needed. Section 26 of the execution architecture standard declares the same
posture normatively for the system; this section merely observes that a human with `git`
and `gh` can perform every step by hand.

## 3. Durable facts vs derived state

The distinction is owned by the execution architecture standard
(standards/EXECUTION_ARCHITECTURE_STANDARD.md#4-durable-facts-derived-state-actions):

- A **durable fact** lives on a GitHub/repository surface, can be re-read by anyone at any
  time, and survives every crash and conversation end. Examples: an Issue state, a native
  blocked-by edge, a git SHA, a frozen blob digest, an Assurance Plan document at an exact
  revision, a review verdict comment.
- A **derived state** is a recomputable projection over durable facts (for example a JIT
  `READY` verdict or a `WAITING_LINEAGE` posture). It is non-authoritative, must never be
  persisted as a canonical Issue state or a competing source of truth, and is recomputed
  from facts at every recompute point
  (standards/EXECUTION_ARCHITECTURE_STANDARD.md#296-deterministic-recompute-on-currentness-drift-racedrift-fail-closed).

Verdict-shaped inferences from currentness or wait posture remain forbidden by the
authority/state registry (`registries/state-dimensions-v1.json`, rules F11-F19): a
predecessor `state:done` never proves lineage currentness, a `CURRENT` plan never mints a
gate PASS, and a wait posture never becomes a workflow or gate verdict.

The fixture mirrors used by the deterministic checks:
`fixtures/manual-reference-flow/durable_facts.json` (durable reads),
`fixtures/manual-reference-flow/derived_projections.json` (marked projections).

## 4. Pointer-only trigger examples

The trigger contract is owned by standards/ISSUE_FIRST_TASK_TRIGGER.md#user-visible-trigger-contract.
The user-visible trigger carries only the pointer to the durable contract
(repository + Issue/PR + optional role/dispatch id); all task-specific facts stay in the
Issue or referenced repository artifacts (standards/ISSUE_FIRST_TASK_TRIGGER.md#durable-contract-precondition).

Conforming examples (canonical shapes; fixture mirror
`fixtures/manual-reference-flow/pointer_triggers.json`):

```text
完成 `owner/repo` Issue #732。
执行 `owner/repo` Issue #732 的当前 READY builder dispatch。
执行 `owner/repo` Issue #732 的当前 READY validation dispatch dispatch-17。
完成 `owner/repo` PR #792 的当前 READY Independent Review dispatch。
```

Non-conforming examples — each carries task-specific payload that must live in the Issue
instead (standards/ISSUE_FIRST_TASK_TRIGGER.md#forbidden-task-specific-trigger-content):

```text
完成 `owner/repo` Issue #732，baseline d53e943e，只改 references/**。
完成 `owner/repo` Issue #732，先跑 verify_standard.py 再跑 focused test。
Continue repo-x v4.9 current READY validation work in Issue #732.
```

The dispatch that materialized this very Task was emitted in the conforming pointer-only
form: it named the repository, Issue #732, and the ready builder dispatch, and every
execution fact (base SHA, write set, pack head) was read from the Issue's dispatch
comment and `.agent/execution/T-013/**` at the pack head — not from the trigger text.

## 5. Walkthrough W-A — manual currentness check before an authority-bearing transition

Owner: standards/EXECUTION_ARCHITECTURE_STANDARD.md#291-assurance-plan-currentness-consumption-at-architecture-owned-transitions
and standards/ASSURANCE_PLAN_STANDARD.md#12-currentness-binding. Before Dispatch
materialization, Claim admission, merge/merge-ready, Candidate Freeze, or Release
Qualification, the operator re-reads the governing Assurance Plan's `currentness_binding`
and proceeds only on `CURRENT`:

1. Read the plan document at its exact repository path (repository file — durable).
2. Re-derive each bound digest from current facts: subject SHA (`git rev-parse`), owner
   authority/proof/Task Pack/release-decision references (repository files at the exact
   revision), unresolved finding references (GitHub review/validation records).
3. Compare the re-derived values against the stored `binding_digest`.
4. Classify per the owner rule: all components exact and current => `CURRENT`; any
   material drift => `STALE`; missing/unprovable => `UNKNOWN`.
5. `CURRENT` => the transition may proceed to its remaining owner predicates. `STALE` or
   `UNKNOWN` => route to recomputation/rebinding, a stronger legal path, or `BLOCKED`;
   never to a lower-assurance path.

Steps 1-3 are durable reads; the `CURRENT`/`STALE`/`UNKNOWN` classification in step 4 is
a derived projection (recomputed, never stored as authority). A `CURRENT` result creates
no gate PASS and no Task READY (registry F13-F16).

Example durable reads (see `fixtures/manual-reference-flow/durable_facts.json`,
fact ids `F-SUBJECT-SHA`, `F-PLAN-BINDING`):

```bash
git rev-parse version/v4.9.0
git cat-file -p version/v4.9.0:docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md | git hash-object --stdin
gh api repos/OWNER/REPO/pulls/792 --jq '.merge_commit_sha'
```

## 6. Walkthrough W-B — manual deterministic recompute of the JIT verdict

Owner: standards/EXECUTION_ARCHITECTURE_STANDARD.md#292-legal-jit-phase-predicate.
The verdict is a pure function of current durable facts; identical facts always produce
the identical outcome, so any operator can recompute it at any time
(standards/EXECUTION_ARCHITECTURE_STANDARD.md#296-deterministic-recompute-on-currentness-drift-racedrift-fail-closed):

1. P1 — dependencies: read the native blocked-by edges of the work item from GitHub
   (native Issue Dependencies; body text and Markdown tables never substitute,
   standards/TASK_DAG_GOVERNANCE_STANDARD.md). Every native dependency `DONE`?
2. P2 — lineage currentness: for each required predecessor-owned surface reference,
   verify it resolves and is byte-identical at the current base
   (`git rev-parse <ref>:<path>` equals the bound blob digest; exact SHAs/anchors resolve).
3. P3 — plan/admission: the phase is inside the current Task envelope (declared by the
   current Task Pack or required/recommended by the current Assurance Plan) and the
   composite work+resource admission is available and passing.
4. Verdict: all of P1-P3 (with E1 or E2, and no envelope violation) => `READY`; any input
   unknown or lineage not current => `WAITING_LINEAGE` (derived projection, W-E2 below);
   any input failed or envelope violation => `BLOCKED`.

All steps are durable reads; `READY`/`WAITING_LINEAGE`/`BLOCKED` is the only derived
output, and it is recomputed at the next recompute point instead of being cached.

## 7. Walkthrough W-C — manual Claim admission and race resolution

Owner: standards/EXECUTION_ARCHITECTURE_STANDARD.md#11-dispatch-lifecycle-atomic-claim-and-staleness
with standards/EXECUTION_ARCHITECTURE_STANDARD.md#111-required-claim-serialization-capability.

1. Re-read the Dispatch on the Issue (durable GitHub record): exact subject, expected
   base, role, independence axes.
2. Re-run the currentness consumption of W-A for the governing plan.
3. Post the Claim against the still-current predicates. The platform's compare-and-swap
   serialization (owner §11.1) decides: at most one claim linearizes.
4. A competitor claiming afterwards re-reads the Issue, observes the accepted claim or
   drifted predicates, and is rejected as duplicate/stale — it publishes nothing and
   mutates nothing.

Race resolution is fail-closed on drift: outcomes are one accepted claim, or no accepted
claim with `BLOCKED`/recompute. "Both claims accepted" and "accepted claim silently lost"
are impossible outcomes. The Claim record on the Issue is the durable fact; any local
note an operator keeps about "having" the claim is derived, non-authoritative, and
worthless after a crash.

## 8. Walkthrough W-D — adverse-finding carry-forward without review shopping

Owner: standards/EXECUTION_ARCHITECTURE_STANDARD.md#295-adverse-finding-carry-forward-and-no-review-shopping-routing,
standards/ASSURANCE_PLAN_STANDARD.md#13-adverse-finding-carry-forward, and Frozen L2 §9
(docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md#9-adverse-findings-and-successor-subjects).

1. Read the durable unresolved-finding set (GitHub review/validation records) for the
   subject lineage.
2. A new reviewer, model, route, SHA, or unrelated PASS never removes an unresolved
   finding; same-subject re-dispatch to obtain PASS is rejected.
3. Re-review happens only against a successor subject from an authorized repair path.
   Every unresolved predecessor finding relevant to the repair lineage is carried into
   the successor review contract.
4. A finding leaves the unresolved set only through per-finding successor verification
   (`RESOLVED` / `STILL_PRESENT` / `NOT_APPLICABLE_TO_SUCCESSOR`, with evidence refs and
   an owning-rule basis) or an explicit owning-authority disposition.

The unresolved set is durable (GitHub records); "latest verdict" chronology is derived
and never governs. The gate-owned evidence routing for these records is wired in
references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md (rows M01/M04).

## 9. Walkthrough W-E — JIT phase admission, worked on this Task

Owner: standards/EXECUTION_ARCHITECTURE_STANDARD.md#292-legal-jit-phase-predicate; the
deterministic classification of runtime/JIT proposals is wired in
references/JIT_DAG_MUTATION_GOVERNANCE_V49_REFERENCE.md.

This Task's own admission is a worked example of the manual flow (all reads are durable;
recomputed, not remembered):

1. P1 — the native dependencies of issue #732 (T-008/T-010/T-011) were read as `DONE`
   from GitHub native facts at dispatch time.
2. P2 — lineage: the full sequential predecessor lineage was physically present at base
   `d53e943ec7109648485b64a647ed2c7cf553531d`; the frozen planning blobs above resolve
   byte-identical at the execution pack head (`git rev-parse HEAD:<path>` recheck).
3. P3 — envelope: DAG v0.1 `### T-013` (blob `4f358ba2b32e01ae17ddcdf970151cf28e44bb3f`)
   plus the current Task Pack declare the concern and write set; the execution pack at
   `585762f5115bb359461e49dee5e62b80f445d557` materialized them; composite admission
   passed. No envelope condition (new concern, ownership change, dependency change,
   scope widening) was violated, so no proposal routed to Task DAG mutation governance
   (standards/TASK_DAG_GOVERNANCE_STANDARD.md).
4. Verdict `READY` was derived, the JIT branch and pack were materialized as
   execution-container bookkeeping, and the pointer-only trigger was emitted.

A runtime proposal that instead created a new semantic concern, rewired dependencies, or
widened scope would classify as a material topology change and route to the v4.3
mutation authority with `dag-mutation-record-v1` evidence — it is never auto-admitted as
a JIT phase.

## 10. WAITING_LINEAGE — the wait posture stays derived

Owner: standards/EXECUTION_ARCHITECTURE_STANDARD.md#293-waiting_lineage-derived-non-dispatch-projection.
When W-B step 2 fails (a required predecessor surface is not integrated/current), the
work item is held in the `WAITING_LINEAGE` projection instead of dispatching work whose
only possible result is a guaranteed-`BLOCKED` sequence block. The projection is
non-dispatchable, non-authoritative, recomputable, and reason-bound; it never appears in
the workflow routing vocabulary and never becomes a canonical Issue state or a gate
verdict (registry F17-F19). When the predecessor surface becomes current, recompute
drops the projection and normal evaluation resumes. A manual operator implements this as:
leave the Issue untouched, record nothing canonical, and re-run W-B when lineage changes.

## 11. Non-goals of this reference

This reference is descriptive only. It does not define, redefine, or weaken any owner
contract; it introduces no new lifecycle, scheduler, verdict vocabulary, or state store;
and it never substitutes a walkthrough for an owner-issued verdict. If any example above
exposed a semantic gap, the route is the owning Task/DAG amendment, not an edit here
(docs/implementation/4.9.0/L3_REFERENCE_PACKS.md#t-013--manual--github-native-reference-flow-732).
Executable checks for the properties claimed above live in
scripts/test_v49_manual_reference_flow.py with the fixtures under
fixtures/manual-reference-flow/; they are Builder evidence, not independent Validation.
