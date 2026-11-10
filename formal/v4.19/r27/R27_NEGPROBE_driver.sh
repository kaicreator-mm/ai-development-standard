#!/usr/bin/env bash
# R27 negative probe driver: forged TLC result identity against two runner
# generations (old = 1695615 pre-repair, new = ca13e9b repaired).
# Each scenario runs twice; receipt bytes must be identical (determinism).
set -u
OUT=/home/cc/ads-i1366-r27-negprobe
OLD=/home/cc/ads-i1366-r27-oldrunner/formal
NEW=/home/cc/ads-i1366-r27-model/formal
LOG="$OUT/R27_NEGATIVE_PROBE_LOG.txt"
: > "$LOG"

{
  echo "=== runner generation identities ==="
  echo "OLD worktree HEAD/TREE:"
  git -C /home/cc/ads-i1366-r27-oldrunner rev-parse HEAD
  git -C /home/cc/ads-i1366-r27-oldrunner rev-parse 'HEAD^{tree}'
  git -C /home/cc/ads-i1366-r27-oldrunner ls-tree HEAD -- formal/suite/expanded.py
  echo "NEW worktree HEAD/TREE:"
  git -C /home/cc/ads-i1366-r27-model rev-parse HEAD
  git -C /home/cc/ads-i1366-r27-model rev-parse 'HEAD^{tree}'
  git -C /home/cc/ads-i1366-r27-model ls-tree HEAD -- formal/suite/expanded.py formal/suite/execution_inventory.py
  echo "candidate source worktree HEAD/TREE:"
  git -C /home/cc/ads-i1366-r27-source rev-parse HEAD
  git -C /home/cc/ads-i1366-r27-source rev-parse 'HEAD^{tree}'
  echo "driver sha256:"
  sha256sum "$OUT/r27_negprobe_runner.py"
} >> "$LOG" 2>&1

run() { # tag root forge out exitfile
  echo "=== scenario $1 forge=$3 ===" >> "$LOG"
  python3 "$OUT/r27_negprobe_runner.py" --formal-root "$2" --forge "$3" --out "$4" >> "$LOG" 2>&1
  echo "$?" > "$5"
  echo "scenario_exit=$(cat "$5")" >> "$LOG"
}

run P1_old_forged        "$OLD" tlc_model_id "$OUT/R27_NEGPROBE_OUT_P1_OLD.json"         "$OUT/R27_NEGPROBE_EXIT_P1"
run P2_new_forged        "$NEW" tlc_model_id "$OUT/R27_NEGPROBE_OUT_P2_NEW.json"         "$OUT/R27_NEGPROBE_EXIT_P2"
run P3_new_correct       "$NEW" none         "$OUT/R27_NEGPROBE_OUT_P3_NEW.json"         "$OUT/R27_NEGPROBE_EXIT_P3"
run P1_old_forged_rerun  "$OLD" tlc_model_id "$OUT/R27_NEGPROBE_OUT_P1_OLD_RERUN.json"  "$OUT/R27_NEGPROBE_EXIT_P1_RERUN"
run P2_new_forged_rerun  "$NEW" tlc_model_id "$OUT/R27_NEGPROBE_OUT_P2_NEW_RERUN.json"  "$OUT/R27_NEGPROBE_EXIT_P2_RERUN"
run P3_new_correct_rerun "$NEW" none         "$OUT/R27_NEGPROBE_OUT_P3_NEW_RERUN.json"  "$OUT/R27_NEGPROBE_EXIT_P3_RERUN"

{
  echo "=== receipt sha256 (determinism) ==="
  sha256sum "$OUT"/R27_NEGPROBE_OUT_P*.json
  echo "=== scenario exit codes ==="
  for f in "$OUT"/R27_NEGPROBE_EXIT_*; do echo "$(basename "$f")=$(cat "$f")"; done
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


p1 = load("R27_NEGPROBE_OUT_P1_OLD.json")
p2 = load("R27_NEGPROBE_OUT_P2_NEW.json")
p3 = load("R27_NEGPROBE_OUT_P3_NEW.json")

# P1: pre-repair runner emits a false MODEL_AND_SOURCE_PASS on a foreign TLC
# model identity, with no execution-inventory audit in the receipt at all.
want("P1_verdict_false_pass", p1["model_verdict"] == "MODEL_AND_SOURCE_PASS")
want("P1_no_audit_key", "execution_inventory_audit" not in p1)
want("P1_source_bound_10", p1["coverage"]["source_bound_verified_obligations"] == 10)
want("P1_differential_pass", all(d.get("status") == "PASS" for d in p1["solver_differential"])
     and len(p1["solver_differential"]) == 16)

# P2: repaired runner blocks the same forged input before consuming SMT pairing.
want("P2_verdict_blocked", p2["model_verdict"] == "BLOCKED")
audit = p2.get("execution_inventory_audit") or {}
want("P2_audit_fail", audit.get("status") == "FAIL")
want("P2_model_id_problem", any(p.get("field") == "model_id" for p in audit.get("problems", [])))
want("P2_source_bound_zero", p2["coverage"]["source_bound_verified_obligations"] == 0)
want("P2_differential_inconclusive",
     len(p2["solver_differential"]) >= 1
     and all(d.get("status") == "INCONCLUSIVE" for d in p2["solver_differential"]))

# P3: correct Z3/cvc5/TLC results keep the repaired runner at full PASS.
want("P3_verdict_pass", p3["model_verdict"] == "MODEL_AND_SOURCE_PASS")
a3 = p3.get("execution_inventory_audit") or {}
want("P3_audit_pass_35", a3.get("status") == "PASS"
     and a3.get("expected_count") == 35 and a3.get("observed_count") == 35)
want("P3_differential_pass", all(d.get("status") == "PASS" for d in p3["solver_differential"])
     and len(p3["solver_differential"]) == 16)
want("P3_source_bound_10", p3["coverage"]["source_bound_verified_obligations"] == 10)

# Exit codes recorded by the driver.
exits = {n: (out / ("R27_NEGPROBE_EXIT_" + n)).read_text("utf8").strip()
         for n in ("P1", "P2", "P3", "P1_RERUN", "P2_RERUN", "P3_RERUN")}
want("P1_exit_0", exits["P1"] == "0" and exits["P1_RERUN"] == "0")
want("P2_exit_2", exits["P2"] == "2" and exits["P2_RERUN"] == "2")
want("P3_exit_0", exits["P3"] == "0" and exits["P3_RERUN"] == "0")

for a, b, n in (("R27_NEGPROBE_OUT_P1_OLD.json", "R27_NEGPROBE_OUT_P1_OLD_RERUN.json", "P1"),
                ("R27_NEGPROBE_OUT_P2_NEW.json", "R27_NEGPROBE_OUT_P2_NEW_RERUN.json", "P2"),
                ("R27_NEGPROBE_OUT_P3_NEW.json", "R27_NEGPROBE_OUT_P3_NEW_RERUN.json", "P3")):
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
tail -25 "$LOG"
