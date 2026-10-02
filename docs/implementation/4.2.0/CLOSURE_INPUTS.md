# v4.2 T07 — Version Closure Inputs (non-verdict)

Version: 4.2.0 | Task: #235/T07 | Integration target: `version/v4.2.0`

**This is a candidate handoff checklist, not a Version Closure or Release Qualification result.** A Closure executor must re-read GitHub's live target ref, final merged SHA/tree, exact Validation/Review evidence and current pinned-standard/version authority; no candidate branch HEAD substitutes for the final merge identity.

## Minimum authoritative inputs for separate Closure

| Input | Required identity and proof | Owner |
| --- | --- | --- |
| Frozen Product/L2/DAG | Exact frozen artifacts and no unauthorized semantic drift | Frozen planning owners |
| Implemented T01–T06 | Merge SHAs, effective current target, unchanged normative-owner boundaries | Concern task/PR history |
| T07 integrated test | Final exact target/HEAD, six real owner suite exit results and 15 bounded cross-boundary cases | T07 integration Validation |
| API compatibility dogfood | Actual T04 tested old-consumer/new-producer and baseline tuple; distinct wire/source/behavior dimensions | T04 / API conformance |
| Migration dogfood | T05 actual SQLite/runtime/fixture digest: isolated A→B, separate fresh B, interrupted rollback/forward recovery | T05 / stateful conformance |
| v4.1 and historical v4 | Representatively accepted old payloads and optional additive projection checks; preserve prior evidence identity | Contract/Validation/adoption owners |
| External-required profile | Exact environment/authority/fidelity proof or truthful BLOCKED/NOT_RUN/NOT_APPLICABLE with rationale | External/Validation owner |
| Regression security | Risk exception != remediation/PASS; migration != deployment; compatibility != validation; validation != release; no silent owner fallback | T01–T07 + independent Review |
| Closure tests and packaging | Full regression, applicable hidden Validation, critical journeys, package/install tuples and Release qualification where required | Dedicated Version Closure and Release owners |

## Forbidden inference register

- A compatibility record does **not** issue a Validation PASS or certify an untested old consumer.
- A migration-transition record or successful SQLite dogfood does **not** issue a v4.4 Deployment result or prove an untested datastore runtime.
- Fresh installation at B does **not** prove upgrade A→B; an interrupted transition must preserve a proven recovery strategy rather than requiring universal down migrations.
- Accepted vulnerability risk is **not** remediation or permission to bypass an applicable security gate.
- `VALIDATION PASS` and `REVIEW PASS` at Task level are **not** `RELEASE READY`.
- A mutable branch/tag, changed PR HEAD or historical candidate evidence is **not** sufficient proof for the new exact subject.
- A non-material Fast Path positive does **not** waive relevant material compatibility/migration proof.
- A manifest/Golden index change is discoverability, not a second semantic or mutation owner.

## Current T07 gate handoff

1. Obtain #391 independent authority review PASS, merge PR #388 expected-head to the live version integration target, then refresh T07 implementation branch without sibling semantic change.
2. Bind central verifier invocation to the actual T07 integration runner on the approved exact write-set.
3. Run clean exact-HEAD integration Validation, storing per-command exit code, Python/platform/SQLite tuple, exact effective base and final checked-out SHA.
4. Obtain a **separate genuinely Fresh Independent Review** for that exact HEAD, then expected-head merge T07 only with currentness still valid.
5. Only after #235 DONE dispatch separate Version Closure; do not infer any of its gates are already PASS.

Unresolved P0/P1, material UNKNOWN, stale exact identity or unavailable required runtime blocks the corresponding Closure input; it must not be called optional merely to produce a green dashboard.
