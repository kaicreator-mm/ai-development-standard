# v4.2 T07 Cross-standard Conformance Status

Status: **IMPLEMENTATION CANDIDATE — exact-SHA integration Validation and Fresh Independent Review REQUIRED**

This document is a closure *input*, not a Version Closure or Release Qualification verdict. The authoritative candidate is the current live HEAD of Task #235's PR when Validation executes, not any SHA embedded in narrative documentation.

## 1. Executable evidence path

`scripts/test_v42_cross_standard_conformance.py` subprocess-executes the six existing production-owner concern suites rather than replacing them with a T07-only oracle:

1. `test_v42_evolution_contracts.py` (T01 schema and historical optional references);
2. `test_v42_interface_compatibility.py` (T02 compatibility governance);
3. `test_v42_data_migration.py` (T03 migration governance);
4. `test_v42_api_compatibility_conformance.py` (T04 exact old-consumer/API dogfood);
5. `test_v42_migration_conformance.py` (T05 actual isolated SQLite A→B/fresh/recovery dogfood);
6. `test_v42_adoption_wiring.py` (T06 discovery/Golden/override/adoption).

All six must exit zero for T07's owner-regression method to pass. There is no silent fallback when a required script is missing or an existing owner suite fails. T07 also checks current machine schema ownership and illustrative cross-boundary cases in `dogfood/T07_cross_standard_cases.json`.

The normative owner suites supply behavior and schema evidence. Illustrative T07 fixture decisions are supplementary and must never be described as execution of an external provider, release, real production deployment, or a different database engine.

## 2. Cross-owner boundaries

| Claim boundary | Proof input | Restriction |
| --- | --- | --- |
| Interface compatibility | T01/T02/T04 owner suites + exact old-consumer cases | Wire compatibility does not imply source/behavior compatibility; UNKNOWN is not COMPATIBLE. |
| Stateful migration | T01/T03/T05 owner suites with actual SQLite | Fresh bootstrap B differs from real A→B upgrade and interrupted recovery; SQLite evidence does not transfer to PostgreSQL. |
| Exact identity | T01/T04/T05 + baseline/consumer drift negatives | Changed subject/consumer/runtime invalidates old evidence for material claims. |
| Adoption and Fast Path | T06 tests and non-material positive/material bypass negative | Minimal work need not instantiate empty evolution records, but required evidence is not waived. |
| Disposition and result ownership | Risk exception and result-substitution negatives | Accepted risk is not vulnerability remediation or Validation PASS. Compatibility/migration records cannot issue Validation, Deployment or Release verdicts. |
| Historical compatibility | T01 optional Validation ref tests and T06 adoption tests | Historical v4 evidence retains its original exact subject/meaning. |

## 3. CI and exact-subject posture

Before #387/#391 authority amendment merges, T07 is intentionally **not** registered through `scripts/test_verify_standard.py`; the new script and fixtures alone do not prove central regression integration. Once the authority amendment is independently approved and merged, update the T07 implementation branch to the then-live `version/v4.2.0` and wire T07 from the narrowly permitted central verifier hook. Execute focused suite, central verifier, repository-required regression and `verify_standard.py` on the resulting exact HEAD with a clean executor. Record distinct environment/runtime/SQLite tuple, exact CI run and any required unavailable external environments as BLOCKED/NOT_RUN. No pre-amendment test/CI result authorizes post-amendment HEAD.

## 4. Evidence classifications

- `T07_FOCUSED`: candidate script and illustrative fixture are proposed; requires current exact-SHA run.
- `T01_TO_T06_OWNER_REGRESSION`: executable dependency, not considered PASS until all six actual suites run on current exact tree.
- `T05_SQLITE_DOGFOOD`: meaningful only for actually executed SQLite/Python/platform/fixture identities.
- `CROSS_RUNTIME_OR_REAL_DEPLOYMENT`: **NOT CLAIMED** without an independent applicable run.
- `INTEGRATION_VALIDATION`: **NOT YET DECIDED** for a future final exact HEAD.
- `FRESH_INDEPENDENT_REVIEW`: **NOT YET DECIDED** for a future final exact HEAD.
- `VERSION_CLOSURE`: **NOT EXECUTED BY T07**.
- `RELEASE_QUALIFICATION`: **NOT EXECUTED BY T07**.

A failing production-owner suite is an integration regression, not something a disconnected T07 fixture can vote to PASS.
