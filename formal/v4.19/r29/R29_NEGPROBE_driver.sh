#!/usr/bin/env bash
# R29 negative probe driver: forged TLC model identity and forged TLC
# success-status swaps against the real main_v1 entry of the repaired runner
# at the exact Git worktree tip, plus a green control. Each scenario runs
# twice; receipt bytes must be identical (determinism).
set -u
REPO_R29=/mnt/c/xDev/kAiCreator/ai-development-standard/ads-i1366-r20-zcode/formal/v4.19/r29
OUT=/home/cc/ads-i1366-r29-negprobe
TIP=/home/cc/ads-i1366-r29-tip
CAND=/home/cc/ads-i1366-r29-source
LOG="$OUT/R29_NEGATIVE_PROBE_LOG.txt"
mkdir -p "$OUT"
cp "$REPO_R29/R29_NEGPROBE_runner.py" "$OUT/r29_negprobe_runner.py"
tr -d '\r' < "$REPO_R29/R29_NEGPROBE_driver.sh" > "$OUT/r29_negprobe_driver.sh"
: > "$LOG"

{
  echo "=== runner identity (exact Git worktree tip) ==="
  git -C "$TIP" show -s --format="%H %T"
  git -C "$TIP" ls-tree HEAD -- formal/suite/expanded.py formal/suite/execution_inventory.py
  echo "candidate source worktree:"
  git -C "$CAND" show -s --format="%H %T"
  echo "probe runner sha256 (repo vs executed copy):"
  sha256sum "$REPO_R29/R29_NEGPROBE_runner.py" "$OUT/r29_negprobe_runner.py"
} >> "$LOG" 2>&1

run() { # tag forge out exitfile
  echo "=== scenario $1 forge=$2 ===" >> "$LOG"
  python3 "$OUT/r29_negprobe_runner.py" --formal-root "$TIP/formal" --forge "$2" --out "$3" >> "$LOG" 2>&1
  echo "$?" > "$4"
  echo "scenario_exit=$(cat "$4")" >> "$LOG"
}

run P1_tlc_model_id        tlc_model_id        "$OUT/R29_NEGPROBE_OUT_P1_TLC_MODEL_ID.json"        "$OUT/R29_NEGPROBE_EXIT_P1"
run P2_tlc_proof_swap      tlc_proof_swap      "$OUT/R29_NEGPROBE_OUT_P2_TLC_PROOF_SWAP.json"      "$OUT/R29_NEGPROBE_EXIT_P2"
run P3_mutation_swap       mutation_status_swap "$OUT/R29_NEGPROBE_OUT_P3_MUTATION_SWAP.json"      "$OUT/R29_NEGPROBE_EXIT_P3"
run P4_green_control       none                "$OUT/R29_NEGPROBE_OUT_P4_GREEN_CONTROL.json"       "$OUT/R29_NEGPROBE_EXIT_P4"
run P1_tlc_model_id_rerun        tlc_model_id         "$OUT/R29_NEGPROBE_OUT_P1_TLC_MODEL_ID_RERUN.json"        "$OUT/R29_NEGPROBE_EXIT_P1_RERUN"
run P2_tlc_proof_swap_rerun      tlc_proof_swap       "$OUT/R29_NEGPROBE_OUT_P2_TLC_PROOF_SWAP_RERUN.json"      "$OUT/R29_NEGPROBE_EXIT_P2_RERUN"
run P3_mutation_swap_rerun       mutation_status_swap "$OUT/R29_NEGPROBE_OUT_P3_MUTATION_SWAP_RERUN.json"       "$OUT/R29_NEGPROBE_EXIT_P3_RERUN"
run P4_green_control_rerun       none                 "$OUT/R29_NEGPROBE_OUT_P4_GREEN_CONTROL_RERUN.json"       "$OUT/R29_NEGPROBE_EXIT_P4_RERUN"

{
  echo "=== receipt sha256 (determinism) ==="
  sha256sum "$OUT"/R29_NEGPROBE_OUT_P*.json
  echo "=== scenario exit codes ==="
  for f in "$OUT"/R29_NEGPROBE_EXIT_*; do echo "$(basename "$f")=$(cat "$f")"; done
} >> "$LOG" 2>&1

python3 - "$OUT" >> "$LOG" 2>&1 <<'PYEOF'
import hashlib
import json
import sys
from pathlib import Path

out = Path(sys.argv[1])
fail = []


def load(name):
    return json.loads((out / name).read_text("utf8"))


def want(name, cond):
    print("ASSERT[%s]: %s" % (name, "OK" if cond else "MISSING"))
    if not cond:
        fail.append(name)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


p1 = load("R29_NEGPROBE_OUT_P1_TLC_MODEL_ID.json")
p2 = load("R29_NEGPROBE_OUT_P2_TLC_PROOF_SWAP.json")
p3 = load("R29_NEGPROBE_OUT_P3_MUTATION_SWAP.json")
p4 = load("R29_NEGPROBE_OUT_P4_GREEN_CONTROL.json")

def audit_of(report):
    return report.get("execution_inventory_audit") or {}


def problems(report):
    return audit_of(report).get("problems", [])


def has_model_id_problem(report):
    return any(p.get("field") == "model_id" for p in problems(report))


def has_status_mismatch_problem(report):
    return any(p.get("reason") == "SUCCESS_STATUS_PURPOSE_MISMATCH"
               for p in problems(report))


def diff_statuses(report):
    return sorted({d.get("status") for d in report["solver_differential"]})


def source_bound(report):
    return report["coverage"]["source_bound_verified_obligations"]


# P1: foreign model_id on TLC results must block before SMT pairing is consumed.
want("P1_verdict_blocked", p1["model_verdict"] == "BLOCKED")
want("P1_audit_fail", audit_of(p1).get("status") == "FAIL")
want("P1_model_id_problem", has_model_id_problem(p1))
want("P1_source_bound_zero", source_bound(p1) == 0)
want("P1_differential_inconclusive", diff_statuses(p1) == ["INCONCLUSIVE"])

# P2: legal TLC proof returning COUNTEREXAMPLE must block via purpose/status binding.
want("P2_verdict_blocked", p2["model_verdict"] == "BLOCKED")
want("P2_audit_fail", audit_of(p2).get("status") == "FAIL")
want("P2_status_mismatch_problem", has_status_mismatch_problem(p2))
want("P2_identity_legal", not has_model_id_problem(p2))
want("P2_source_bound_zero", source_bound(p2) == 0)
want("P2_differential_inconclusive", diff_statuses(p2) == ["INCONCLUSIVE"])

# P3: legal TLC mutation returning PASS_MODEL must block the same way.
want("P3_verdict_blocked", p3["model_verdict"] == "BLOCKED")
want("P3_audit_fail", audit_of(p3).get("status") == "FAIL")
want("P3_status_mismatch_problem", has_status_mismatch_problem(p3))
want("P3_identity_legal", not has_model_id_problem(p3))
want("P3_source_bound_zero", source_bound(p3) == 0)
want("P3_differential_inconclusive", diff_statuses(p3) == ["INCONCLUSIVE"])

# P4: identical seam with correct results keeps the real runner at full PASS.
want("P4_verdict_pass", p4["model_verdict"] == "MODEL_AND_SOURCE_PASS")
want("P4_audit_pass_35", audit_of(p4).get("status") == "PASS"
     and audit_of(p4).get("expected_count") == 35
     and audit_of(p4).get("observed_count") == 35)
want("P4_differential_pass", diff_statuses(p4) == ["PASS"]
     and len(p4["solver_differential"]) == 16)
want("P4_source_bound_10", source_bound(p4) == 10)

# Exit codes recorded by the driver.
exits = {n: (out / ("R29_NEGPROBE_EXIT_" + n)).read_text("utf8").strip()
         for n in ("P1", "P2", "P3", "P4",
                   "P1_RERUN", "P2_RERUN", "P3_RERUN", "P4_RERUN")}
want("P1_exit_2", exits["P1"] == "2" and exits["P1_RERUN"] == "2")
want("P2_exit_2", exits["P2"] == "2" and exits["P2_RERUN"] == "2")
want("P3_exit_2", exits["P3"] == "2" and exits["P3_RERUN"] == "2")
want("P4_exit_0", exits["P4"] == "0" and exits["P4_RERUN"] == "0")

for a, b, n in (("R29_NEGPROBE_OUT_P1_TLC_MODEL_ID.json",
                 "R29_NEGPROBE_OUT_P1_TLC_MODEL_ID_RERUN.json", "P1"),
                ("R29_NEGPROBE_OUT_P2_TLC_PROOF_SWAP.json",
                 "R29_NEGPROBE_OUT_P2_TLC_PROOF_SWAP_RERUN.json", "P2"),
                ("R29_NEGPROBE_OUT_P3_MUTATION_SWAP.json",
                 "R29_NEGPROBE_OUT_P3_MUTATION_SWAP_RERUN.json", "P3"),
                ("R29_NEGPROBE_OUT_P4_GREEN_CONTROL.json",
                 "R29_NEGPROBE_OUT_P4_GREEN_CONTROL_RERUN.json", "P4")):
    want("DETERMINISM[%s]" % n, sha(out / a) == sha(out / b))

print("PROBE_RESULT:", "ALL_ASSERTIONS_PASS" if not fail
      else "ASSERTIONS_FAILED: " + ",".join(fail))
sys.exit(0 if not fail else 1)
PYEOF

if tail -1 "$LOG" | grep -q "ALL_ASSERTIONS_PASS"; then
  echo "DRIVER_FINAL: PASS" >> "$LOG"
else
  echo "DRIVER_FINAL: FAIL" >> "$LOG"
fi
tail -40 "$LOG"
