# ADS Formal R4 — Claim key ≠ write-set concurrency
**Non-normative, finite.** PR #1365 candidate `dac263fa4c0ab155406d2f2117459b34322cc988`, not a new Freeze. R3 and earlier receipts are immutable.
## Material gap addressed
R3 shows two **distinct protected Claim keys** can be simultaneously accepted. That does **not** authorize simultaneous source writes when Task write sets overlap. A missing/UNKNOWN write-set relationship is not a positive disjointness witness.
New property `ADS-P-WRITER-KEYS` tests:
- forbidden overlapping writes across different Claim keys: UNSAT;
- UNKNOWN write-set relation never proves safe concurrent mutation: UNSAT;
- inactive Claim cannot mutate: UNSAT;
- verified-disjoint concurrent writes allowed: SAT;
- simultaneous distinct-key Claims with only one current Writer allowed: SAT;
- unauthorized second Writer forbidden: UNSAT.
Mutant omits write-set exclusion and returns SAT for two overlapping writers, despite distinct Claim keys.
Native Z3 5.3.3 and cvc5 1.4.2 were actually run on both models, with exact blob readback. This is a **model mutation**, not a demonstrated ADS source defect.
## Baseline and command
R4 suite contains **27 defined cases**: 23 preserved from R2/R3 and 4 newly executed R4; do not count the first 23 as rerun here.
```bash
python formal/suite/run.py --suite formal/v4.19/r4/suite.json --property ADS-P-WRITER-KEYS \
  --z3 /path/to/z3 --cvc5 /path/to/cvc5 --tlc-jar /path/to/tla2tools.jar \
  --out /tmp/ads-formal-r4.json
```
Strict source-bound verification still needs independent Git checkout at candidate HEAD, with `--source-checkout` and `--strict-source`. GitHub 7/7 pinned blob/anchor readback is separate provenance. No real Claim/CAS, CI, Release or independent model-to-natural-language equivalence is demonstrated.
