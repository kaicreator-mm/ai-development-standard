#!/usr/bin/env bash
# Run from this directory: Z3_BIN=/path/to/z3 TLC_JAR=/path/to/tla2tools.jar bash run.sh
set -euo pipefail
: "${Z3_BIN:=z3}"
: "${TLC_JAR:?TLC_JAR must reference tla2tools.jar}"
for smt in roles.smt2 gates.smt2 roles-mutant.smt2; do
  echo "== $smt =="
  "$Z3_BIN" "$smt"
done
java -cp "$TLC_JAR" tlc2.TLC -deadlock -config ADSWorkflow.cfg ADSWorkflow.tla
# Both mutants must produce an invariant error, not a successful check.
for kind in bad-release bad-claim; do
  echo "== intentional mutant $kind =="
  if java -cp "$TLC_JAR" tlc2.TLC -deadlock -config "ADSWorkflow.$kind.cfg" ADSWorkflow.tla >"/tmp/ads-tlc-$kind.log" 2>&1; then
    echo "ERROR: mutant unexpectedly passed" >&2; exit 1
  fi
  grep -q 'Error: Invariant' "/tmp/ads-tlc-$kind.log"
done
