#!/bin/bash
# R25 negative probe: real CLI fail-closed check for R24 source-binding repair.
# Red/green: same negative inputs, pre-repair (9ca0139) vs post-repair (6edd2bad) runner.
set -u
S=/home/cc/ads-i1366-r25-negprobe
M=/home/cc/ads-i1366-r25-model
SRC=/home/cc/ads-i1366-r25-source
FIX=/mnt/c/xDev/kAiCreator/ai-development-standard/_tmp/r25-integration
Z3=/home/cc/ads-i1366-tools/z3-5.3.3-x64-glibc-2.39/bin/z3
JAR=/home/cc/ads-i1366-tools/tla2tools.jar

rm -rf "$S"
mkdir -p "$S/models/authority"
cp "$M/formal/models/authority/claim.smt2" "$S/models/authority/claim.smt2"
cp "$FIX/neg-suite.json" "$S/suite.json"
git -C "$M" show 9ca0139:formal/suite/run.py > "$S/run_old.py"
git -C "$M" show 6edd2bad:formal/suite/run.py > "$S/run_new.py"
echo "run_old sha256: $(sha256sum "$S/run_old.py" | cut -d' ' -f1)"
echo "run_new sha256: $(sha256sum "$S/run_new.py" | cut -d' ' -f1)"
echo "model sha256:   $(sha256sum "$S/models/authority/claim.smt2" | cut -d' ' -f1)"

run_one() {
  local runner="$1" map="$2" tag="$3"
  cp "$FIX/$map" "$S/neg-source-map.json"
  python3 "$S/$runner" --suite "$S/suite.json" --z3 "$Z3" --tlc-jar "$JAR" --java java \
    --source-checkout "$SRC" --strict-source --out "$S/out-$tag.json" > "$S/log-$tag.txt" 2>&1
  echo "== $tag EXIT=$?"
  cat "$S/log-$tag.txt"
}

echo "===== SCENARIO A: sources=[] ====="
run_one run_old.py neg-source-map-empty.json A-old
run_one run_new.py neg-source-map-empty.json A-new

echo "===== SCENARIO B: anchors=[] on real source row ====="
run_one run_old.py neg-source-map-emptyanchors.json B-old
run_one run_new.py neg-source-map-emptyanchors.json B-new

for t in A-old A-new B-old B-new; do
  python3 - "$S/out-$t.json" "$t" <<'EOF'
import json, sys
p, tag = sys.argv[1], sys.argv[2]
d = json.load(open(p))
al = d.get("source_alignment", {})
reason = al.get("reason") or (al.get("checks") or [{}])[0].get("reason")
print(f"{tag}: verdict={d.get('model_verdict')} source={al.get('status')} reason={reason} cases={len(d.get('checks', []))}")
EOF
done
