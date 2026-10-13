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
# Avoid py_compile side effects in the clean worktree.
python -B scripts/test_v411_t12_abc_conformance.py > t12-smoke.log 2>&1
test_exit=$?
echo "TASK_SMOKE_EXIT=$test_exit"
python - t12-smoke.log "$test_exit" <<'PY'
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

---

*Sources: [#1020 R1–R8](https://github.com/kaicreator-mm/ai-development-standard/issues/1020), [PR #1086](https://github.com/kaicreator-mm/ai-development-standard/pull/1086), [practice intake #1092](https://github.com/kaicreator-mm/ai-development-standard/issues/1092). Status of R8 and later iterations must always be read live from their actual exact-HEAD receipts.*
