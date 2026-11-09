# R3 CAS native experiment

Preserves pre-existing R3 `semantic_challenge.py` and its README. Four new solver cases extend 19 unchanged historical R2 cases; 23 defined, **only four new solver cases executed R3**.

```bash
python formal/suite/run.py --suite formal/v4.19/r3/suite.json --property ADS-P-CAS --z3 /path/to/z3 --cvc5 /path/to/cvc5 --tlc-jar /path/to/tla2tools.jar --out /tmp/ads-r3.json
```

With exact candidate checkout at dac263fa4c0ab155406d2f2117459b34322cc988, add `--source-checkout /path/to/candidate --strict-source`. Without it, maximum `MODEL_ONLY_PASS`. To test invalidation, `--changed-source scripts/v34_rules.py` must select both ADS-P-AUT and ADS-P-CROSS and return STALE/BLOCKED until sources re-pinned.
