# Evidence-Driven Validation Loop Convergence — T12 R1–R8 Dogfood

> Status: **NON-NORMATIVE reference / engineering playbook**. Practice intake: [#1092](https://github.com/kaicreator-mm/ai-development-standard/issues/1092). This file does not create a new validation state, mandatory gate, authority, checklist, Task DAG node, or exception to existing standards. Where this reference disagrees with frozen Product/L2/Task Pack or a standard, **the authoritative source wins**.

## 1. Problem and verified history

ADS v4.11 T12 ([Issue #1020](https://github.com/kaicreator-mm/ai-development-standard/issues/1020), [PR #1086](https://github.com/kaicreator-mm/ai-development-standard/pull/1086)) repeatedly looped through source repair, Real Build Host execution, and Fresh Review. **R8 is the eighth revision of the repair/validation *handoff series*, not evidence of eight completed full validations.** Count dispatches separately from actual executions and final accepted gates.

| Iteration | Observed, durable result | Learning |
| --- | --- | --- |
| R1 | Real Host FAIL ([receipt](https://github.com/kaicreator-mm/ai-development-standard/issues/1020#issuecomment-6138277639)) | Execute the bound Task-specific entrypoint early; do not equate candidate creation with an executable oracle |
| R2 | Real Host ran green, but independent exact-HEAD reviewer found **four P1** ([review](https://github.com/kaicreator-mm/ai-development-standard/pull/1086#issuecomment-6139282892)) | A green unit suite can manufacture a false `observed_transition`, `observed_effect`, A/B/C conjunction or compound PASS |
| R3 | 5 commands exit 0, but material integration stays BLOCKED ([receipt](https://github.com/kaicreator-mm/ai-development-standard/issues/1020#issuecomment-6139774117)) | Report owner assertions separately from observed effects and same-work-subject proof |
| R4 | 5 commands exit 0; test-only X01/X02 local joins succeed, unresolved C remains ([receipt](https://github.com/kaicreator-mm/ai-development-standard/issues/1020#issuecomment-6140228558)) | Consolidate equivalent tests, but never turn synthetic source / authority into material Release PASS |
| R5 | Dispatch exists; **no authoritative R5 Real Host completion receipt confirmed** in #1020 at intake | A dispatch is not execution; don't report a fictional PASS or add one to a verified-run count |
| R6 | Real Host 5/5 and 102/102 factual checks green ([receipt](https://github.com/kaicreator-mm/ai-development-standard/issues/1020#issuecomment-6141559487)), while two independent reviewers on the *same HEAD* issued **CHANGES_REQUIRED 4×P1** and **PASS_SOURCE_ONLY** ([review A](https://github.com/kaicreator-mm/ai-development-standard/pull/1086#issuecomment-6143273162), [review B](https://github.com/kaicreator-mm/ai-development-standard/pull/1086#issuecomment-6143598605)) | Resolve concrete, reproducible source falsifiers before merge; latest reviewer verdict alone is not an adjudication |
| R7 | Real Host **0/1/0/0/0**, official ledger not emitted: X01± `KeyError: 'fidelity'` in new reporting path ([receipt](https://github.com/kaicreator-mm/ai-development-standard/issues/1020#issuecomment-6144348398)) | Task test was **absent** from ordinary `verify-standard` CI; a cheap current-candidate smoke/shape check would have caught this before Host dispatch |
| R8 | Exact-HEAD Real Host **dispatch** ([handoff](https://github.com/kaicreator-mm/ai-development-standard/issues/1020#issuecomment-6145161024)); outcome must be read from the latest Issue receipt, not assumed here | Small changes to evidence-reporting code invalidate old Host proof only for the affected exact candidate; rerun the affected gate, not unrelated Release gates |

The defect classes here are **Task-oracle / harness wiring / semantic proof scope / review conflict**. Exact-SHA binding is an essential correct invariant, **not the defect**. Unavailable real authority still means `NOT_RUN` or `BLOCKED`, not `NOT_APPLICABLE` by convenience.

## 2. Recommended workflow: stable source, cheap feedback, authoritative execution

```text
Read frozen Task Pack + declared gate owner
  ↓
Bounded Task implementation & minimal current-scoped tests
  ↓
PRE_HOST_SMOKE: syntax/import, real entrypoint, output schema,
                negative oracle, missing fields, subject/currentness
  ↓ (fix local deterministic failures without Host re-dispatch)
Freeze candidate exact HEAD/tree and Task write-set
  ├─> Real Build Host if required by frozen Task gate
  └─> Truly Fresh Independent source review (in parallel when valid)
  ↓
Reconcile gate facts, conflicts and current SHA — one controller
  ↓
Task merge when all *current Task-owned* gates pass
  ↓
Integration/Version Closure independently establishes its own evidence
```

**Not a change to gate semantics.** A host/platform/device check remains necessary whenever intrinsic to the Task; the aim is to avoid spending that check on a deterministic Python exception or an unreviewed report schema, and to avoid repeating full Release tests at each leaf.

### PRE_HOST_SMOKE (illustrative task-local recipe)

Before a high-cost Real Host handoff, the Builder can execute a **cheap** smoke on an isolated candidate checkout using the *actual task entrypoint*, not just unrelated green CI. In this T12 incident, the following pattern would have caught R7 `KeyError` and absence of the official ledger:

```bash
# Illustration. Use the project's configured task runner/profile.
git rev-parse HEAD
git rev-parse HEAD^{tree}
git status --porcelain
# Keep diagnostic output outside the candidate checkout.
smoke_log="$(mktemp "${TMPDIR:-/tmp}/t12-smoke.XXXXXX.log")"
# -B avoids bytecode cache writes; use the Task's actual entrypoint.
python -B scripts/test_v411_t12_abc_conformance.py > "$smoke_log" 2>&1
test_exit=$?
echo "TASK_SMOKE_EXIT=$test_exit"
python - "$smoke_log" "$test_exit" <<'PY'
import json, pathlib, sys
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
if sys.argv[2] != "0":
    raise SystemExit("FOCUSED_SMOKE_FAIL: actual runner failed; fix before Host")
line = next((s for s in text.splitlines() if s.startswith("V411_T12_EVIDENCE_LEDGER=")), None)
if line is None:
    raise SystemExit("FOCUSED_SMOKE_FAIL: official ledger missing")
data = json.loads(line.split("=", 1)[1])
assert data["record_count"] == len(data["records"]) == 52
assert data["failure_count"] == 0
assert all("P1_A" in r["proof_layers"]
           and "P2_B" in r["proof_layers"]
           and "P3_C" in r["proof_layers"] for r in data["records"])
assert all("observed_transition" in r and "observed_effect" in r
           for r in data["records"])
assert all(
    r["proof_layers"]["P3_C"]["omission_negatives"]["missing_a_denied"]
    and r["proof_layers"]["P3_C"]["omission_negatives"]["missing_b_denied"]
    for r in data["records"]
)
assert data["downstream_release_truth"] == "NOT_RUN"
print("FOCUSED_SMOKE_OK: real runner produced required ledger structure")
PY
git status --porcelain  # must still satisfy the Task's clean-tree policy
```

Run this with logs **outside the protected worktree** when clean status is a Task gate. The example is T12-specific; future Tasks substitute their *own* frozen oracle, expected registry count and output contract. Executing a local smoke **does not replace** a mandatory Real Host/Independent Review, and an emitted ledger **does not** certify the semantic truth of each C, security or Release field. Reviewers still probe counterexamples and physical/currentness provenance.

### Discovery guard for CI

Before declaring a PR CI run covers a Task, record the exact job/step that actually invokes the Task runner:

```text
FOCUSED_TEST_SCRIPT=<repo-relative path>
CI_WORKFLOW=<path/ref>
CI_STEP_EXECUTES_SCRIPT=YES | NO | UNKNOWN
REAL_HOST_REQUIRED_BY_TASK=YES | NO
SOURCE_SMOKE_EXECUTION=PASS | FAIL | NOT_RUN
```

If `CI_STEP_EXECUTES_SCRIPT=NO`, CI PASS is evidence only for the executed jobs. Choose an existing provider-neutral workflow discovery or a separately owned focused test job; **do not edit a frozen implementation Task's non-owned CI paths** to patch this silently. A follow-up may add an automated CI/runner-discovery lint on its own write-set after review.

## 3. Four reusable review/validation checks

**A. Observation ≠ expected value.** Sensors and state transitions come from executed owner operations, exact source/readback and physical effects; expected fixture fields may be compared with observation but never copied into an `observed_*` field. Missing measurement is `UNVERIFIED/BLOCKED`, not observed zero.

**B. Layer A + B + C has a falsifiable conjunction.** Distinct A/B facts must be current and joint on the same exact work subject, with C exercise on that subject. Test withholding A while B still runs, and withholding B while A still runs: C must not PASS either time. An owner unit method passing is not proof of cross-owner conjunction.

**C. Real/synthetic/release truth stays typed.** Local SQLite with test-only authority can prove its local mutation and DENY but not production effect, real human approval, Hidden Validation or Release Qualification. Frozen Pack-required present local Release *prerequisite* predicates are different from later true V/R gates; never create a circular requirement that future Release must PASS before its current Task-local test can merge.

**D. Compound fails closed.** For a declared material intersection, record which owner facts and currentness share a subject, and test each required job omitted. Independent owner-unit PASS results plus shared git blob identity **do not** establish a real compound. Where frozen authority permits, record `MATERIAL_INTERSECTION_UNKNOWN`, `BLOCKED` and an exact repair/owner route.

## 4. Resolve contradictory independent reviews without another broad loop

When two independent terminals disagree on the **same** exact SHA/tree:

1. Pin both review receipt URLs, frozen Pack/L2 blobs, current source HEAD/tree and exact Host receipt.
2. Normalize each finding into `{id, invariant, source line, reproducible counterexample, owner, severity, resolved_on_SHA}`.
3. A reproducible current P0/P1 keeps the Task **not mergeable**, even if a later reviewer wrote PASS. A later PASS may rebut the P1 only by a concrete verified counterexample analysis or a lawful owner ruling, not merely by chronology.
4. Distinguish **scope disputes** (what T12 must prove now vs what V01–R02 proves later) from **implementation defects** (missing subject join, false observed field, KeyError). Settle one frozen-authority applicability decision, then fix only demonstrated defects.
5. Batch the concrete repairs under **one writer / authorized write-set**, rerun focused smoke, pin one new exact candidate, then the required Host and genuinely fresh Review. Never transfer predecessor-SHA PASS if affected source has changed.
6. Keep contradictory terminals as history; publish the new scoped adjudication rather than deleting or calling prior reviews nonexistent.

**Reviewer independence remains required when the frozen Task says so.** This section reduces repetitive review cost; it does not replace independent Review by Builder self-check.

## 5. Practical retry ledger and anti-loop decision

A lightweight single Issue comment or project-local table per candidate is enough; do not create a new workflow state machine.

```text
ITERATION=R<n>
DISPATCH_SHA=<exact head>
TREE=<exact tree>
ACTUALLY_EXECUTED=YES|NO
CI_INVOKED_FOCUSED_TASK=YES|NO|UNKNOWN
LOCAL_SMOKE=PASS|FAIL|NOT_RUN
HOST_RESULT=PASS|FAIL|BLOCKED|NOT_RUN
FRESH_REVIEW=PASS|CHANGES_REQUIRED|CONFLICT|NOT_RUN
ROOT_CAUSE=SOURCE|HARNESS|CI_COVERAGE|ENV|SEMANTIC_REVIEW|MATERIAL_GATE
CHANGED_SCOPE=<bounded paths / concerns>
PREVIOUS_EVIDENCE_REUSABLE=YES|NO + owner reason
NEXT_ACTION=<one bounded remedy / owner>
```

**When to stop:** if another dispatch has unchanged SHA, unchanged inputs, unchanged environment and no additional failing hypothesis, do not re-request the same costly gate. Diagnose the existing receipt or resolve the true external dependency. On repeat deterministic errors, return to source/runner smoke; on a review disagreement, require a claim-level adjudication rather than commissioning a fresh undirected review. This **never** caps retries when safety/security/material gates truly remain unmet.

Suggested telemetry: `dispatches` (including unrun), `actual_host_executions`, `host_fail_after_ci_green`, `same_sha_conflicting_review_count`, `defects_caught_before_host`, `avoidable_repeat_dispatches`. Prioritize observed root-cause reductions; **no universal round/time/token target** is a merge waiver.

## 6. Task size and adoption: reuse existing owners

This reference does **not** introduce a second Task decomposition or verification policy. When a compound Task is oversized, use existing [#775](https://github.com/kaicreator-mm/ai-development-standard/issues/775) (Agent-dispatchable granularity) and [#1072](https://github.com/kaicreator-mm/ai-development-standard/issues/1072) (safe mid-flight partition and collision containment), under `standards/TASK_DECOMPOSITION_STANDARD.md`.

Use [#25](https://github.com/kaicreator-mm/ai-development-standard/issues/25) for tiered Task/Integration/Version-Closure validation ownership, and [#46](https://github.com/kaicreator-mm/ai-development-standard/issues/46) for version-scoped Real Host validation queue and exact-SHA handoff. The frozen v4.11 20-node Task DAG and #1086 write-set are **not** modified by this learning intake.

**Adoptable now:** Task owners may link this reference and use its optional preflight/review conflict/telemetry notes while respecting the frozen authority. **Future automation:** a separately owned test-discovery/CI coverage guard can be proposed and validated as a new bounded concern; do not silently mutate current frozen gates or shared verifiers.

## 7. Whole-standard-first verification convergence (v4.11 V01 dogfood, 2026-10-14)

**Observed anti-pattern:** T01–T14 delivered independently owned normative clauses and task-local oracles, but a later closure retry expanded 14 inherited S cases × positive/negative (28 records) into 28 separately demanded *material* real-host proofs. A new evidence Issue #1098 then split these into four lanes, despite already executed T12 owner assertions (52 records/0 runner failures) and frozen PRD §2.2's allowed tested-equivalence mechanism. This is **gate/Issue amplification**, not evidence that all 28 have failed semantics. Current V01 remains BLOCKED because sufficiency/authority and the unexpected J09+J10+J11+J12 material conjunction have not been resolved.

**Root cause classes (do not blame exact SHA):**
1. `TASK_LOCAL_TEST_PASS` was rightly kept separate from `VERSION_RELEASE_PASS`, but the interim `MATERIAL_UNVERIFIED` ledger was then treated as an automatic independent physical test job per row rather than a *coverage obligation* that may be discharged by a proved common equivalence class.
2. Frozen Product / L2 / Task Pack / Release-stage applicability were reinterpreted by successive agents without one cross-stage proof-sufficiency and authority decision; task-local "future gate NOT_RUN" must not become an impossible prerequisite to the earlier stage.
3. Historical tests pinned to their original authoring state were re-run against later lawful composed version SHAs. At the original 139-suite run, 126 exited 0 and 13 failed; the correct remedy is per-failure **scope/currentness + affected-oracle** disposition, not repeated full-suite looping or converting FAIL to PASS.
4. Auxiliary issue/review/host dispatch counts became a proxy for progress; a new optional proof lane risked becoming another blocker. A genuine Release blocker must derive from frozen owner authority, not the existence of a newly opened Issue.

### Preferred pipeline: define, integrate, prove, qualify

1. **Define the standard first:** freeze Product acceptance and L2 owner/application rules; enumerate hard invariants, actual risks, and a finite evidence/representative-scenario matrix. No research/demo/test machinery expansion without a material unresolved hypothesis and decision owner.
2. **Implement and integrate the standard:** owner-local T tasks get **minimum focused executable smoke/negative tests and risk-required review**, then merge one concern at a time. Shared schema/manifest wiring and central integration stay single-writer. An owner-local PASS means only that owner's tested scope.
3. **One unified conformance selection:** after standard assembly, use *existing* current source, owner operations and Task evidence to build a **gate × material risk × scenario × equivalence class** matrix. Reuse executed proof only with equal hard predicates, source/subject/fidelity/currentness and a falsifying counterexample; a blob match or common method name does **not** establish equivalence. Run missing representative conjunctions on the same actual work subject, not all possible combinations or 28 unrelated Host tasks. Selected high-risk physical boundaries (authentic human DENY, durable effects/lost ACK/recovery, trust/secret promotion, Review/Claim concurrency, materially relied-on upstream source/license) retain actual actor/host authority and negative proof where truly required.
4. **Version closure once per stable candidate:** V01 performs dependency-complete visible regression, CJ, applicable build/package/real-host/environment evidence and current gate×subject applicability. Gate owners explicitly decide historical task-only assertions and in-scope unverified rows, preserving raw FAIL/NOT_RUN. Where no source/affected gate changed, a bounded `VALIDATION_IMPACT_DECISION` should permit reuse rather than an automatic full-139 repeat. Then V02 freeze → V03 private Hidden → V04 Fresh → R01 RQ → R02 integration, with distinct mandatory actors but one orchestrated release chain.
5. **Sufficiency stop rule:** when a new Issue or extra execution is proposed, require `MATERIAL_NEW_PREDICATE | REAL_AUTHORITY_OR_ENV_GAP | NEW_CURRENT_SOURCE_DRIFT | MISSING_NEGATIVE | NONE`, the exact missing hard predicate, proof consumer, cheaper equivalent evidence and incremental expected value. `NONE` means reuse/readback/close advisory lane, **not** fabricate coverage. After repeated same-cause attempts, consolidate to one owner decision and one new candidate.

### Stage/coverage authority and anti-waiver

- Frozen v4.11 Product PRD blob `d30f202e…` §2.2 explicitly permits (a) tested owner/equivalence proof, (b) UNVERIFIED with impact, or (c) owner-accepted scope exclusion; §2.3 requires X01–X08 material intersections and S01–S18 each with required positive/negative oracle. L2 blob `c0fa3614…` §10 assigns P1/P2 S areas and P3 X representative intersections. The T12 frozen Pack blob `a2af3ef4…` §88 distinguishes future Release-terminal evidence from task-local executable predicates. None of these texts alone lets a Builder/WEB controller silently waive an existing V01 `REQUIRED_NOW` Owner decision.
- Explicit Release/T12 Owner #1021@6154154171 classified 14×± as REQUIRED_NOW. Changing their **proof method** from 28 physically separate executions to risk-based shared exact-equivalence evidence requires a **fresh, role-authorized, exact-candidate interpretation** of the frozen gate×subject contract; changing the actual required assurance floor requires formal Product/L2 amendment and review. Until then records remain BLOCKED, compound UNKNOWN and V02 not admitted.
- Human/independent-role proofs cannot come from a synthetic fixture or source prose. Selected real evidence is not universal validation: keep exact positive/negative log exits, source/license/actor permissions, environment, provenance and unproven cases typed.
- **One version = one factual progress denominator:** 14/20 native nodes closed (70%) at intake; `52/52 test runner` is not `28/28 material PASS`. Creating/closing an advisory #1098 has **zero** effect on that numerator/denominator.

**Practical outcome:** Pause broad #1098 Host dispatch pending one validation coverage/sufficiency assessment; keep #1098 source readbacks as evidence; link the convergence decision in V01 #1021. The prospective v4.12 method should measure `material_oracles_executed`, `equivalent_cells_safely_reused`, `avoidable_host_runs`, `new_issue_without_new_predicate`, `time_to_stable_standard` and `release_critical_path_idle` without creating a second authority or mandatory metrics service. This practice is advisory until normal standards governance adopts it.

---

*Sources: [#1020 R1–R8](https://github.com/kaicreator-mm/ai-development-standard/issues/1020), [PR #1086](https://github.com/kaicreator-mm/ai-development-standard/pull/1086), [practice intake #1092](https://github.com/kaicreator-mm/ai-development-standard/issues/1092). Status of R8 and later iterations must always be read live from their actual exact-HEAD receipts.*
