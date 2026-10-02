# T-009 Implementation Map

1. Re-read the exact base and the merged T02-T07 owner surfaces before mutation; if `version/v4.7.0` or this branch no longer matches the bound base before Builder work begins, stop for Controller currentness rebind.
2. Map each adoption/checklist/coverage change to an existing canonical owner. Use pointers and concise wiring; do not restate owner rules in central guidance.
3. Modify only the eight Frozen-authorized Builder paths. `STANDARD_COVERAGE.json`, `PROJECT_OVERRIDES.md`, and compatibility/manifest/profile references remain non-authoritative wiring/read surfaces.
4. Add v4.7 migration/adoption guidance and future-major entries only for compatible wiring or explicitly deferred incompatible findings. Do not perform physical path migration, remove stable aliases, or reinterpret historical v4 payload/evidence meaning.
5. Implement `scripts/test_v47_adoption_wiring.py` to cover bootstrap discovery, owner non-duplication, non-authority of central wiring, historical/alias preservation, and optional/non-applicable Fast Path proportionality.
6. Run the focused T09 test, merged T07 semantic conformance regression, and repository verifier. Treat those results as test evidence only; publish an exact candidate for independent Validation, then require a genuinely new Fresh Review before merge.
7. If a defect belongs to T02-T07 or another canonical owner, report it to that owner instead of repairing it in T09. If an incompatible migration is needed, record/route it to future-major planning rather than silently broadening v4.7.
