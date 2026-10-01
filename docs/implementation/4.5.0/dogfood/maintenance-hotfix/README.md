# T07 — Maintenance / Hotfix Conformance & Dogfood (bounded Git fixture)

**Status:** fixture-level source/conformance proof. **NOT** real project maintenance result-SHA Validation, Fresh Independent Review, Release Qualification, or Deployment. This fixture is not a declaration that `maintenance/v2` is supported in ADS or in any actual product.

Authority: Frozen v4.5 Product/L2/Task DAG/L3; real T07 Pack `T07_maintenance_hotfix_conformance.md`; normative `standards/MAINTENANCE_EOL_HOTFIX_STANDARD.md`, `references/MAINTENANCE_EOL_HOTFIX_REFERENCE.md`, and `schemas/maintenance-policy-v1.schema.json`. `support-policy.json` is a **controlled fictional project owner's durable policy fixture**, NOT the mere existence of a Git branch or a product-support declaration.

## Reproducible bounded scenario

`python3 -m unittest scripts/test_v45_maintenance_hotfix_conformance.py -v` creates a **disposable temp Git SHA-1 repository**, never a remote maintenance branch. It commits a fictional maintained `v2` baseline, diverges `main` with a main-only change, commits a `security-fix` on `main`, branches `maintenance/v2` from the exact earlier baseline, and performs a real `git cherry-pick` onto that baseline. Deterministic Git identities/dates plus explicit `core.autocrlf=false` and no global/system config pin the following independent commit identities (also asserted against `case.json`):

| Subject | Exact fixture SHA |
|---|---|
| Source change on `main` | `d95e55c1d0cda233c648f01e7adc079181c68cba` |
| Pre-change maintenance baseline | `fda33c596039f19f124be57053c07c76806572bf` |
| Resulting cherry-pick SHA on `maintenance/v2` | `5488dd2e24b9d1ef38d6d6212b0198ddabb31ac0` |

`case.json` binds policy ID, owner, class, branch locators, source SHA, pre-change baseline SHA and resulting SHA. The conformance suite inspects the **result Git commit's tree** (patched security marker), parent SHA, real source-versus-result patch, and absence of main-only context. Negative cases reject unknown line, mismatched baseline/owner/policy/component, unauthorized class, EOL, source PASS reuse, missing exact-result evidence fields, and hotfix-required-gate waiver. One positive deliberately illustrates that an **identity-shaped** report is not independently authenticated evidence: its presence never changes the real-project gate to PASS.

## Evidence dimensions (must never be conflated)

- **Fixture preparation/cherry-pick:** executed in temporary Git with exact pinned fixture result SHA; recorded by focused tests and `fixture-execution.json` (source-code-file digests, test command/exit, local environment). No real product support policy or authorized maintenance line was used.
- **Fixture focused result testing:** checks the actual temporary Git **result** tree against the security regression. This is not evidence for the repository PR HEAD or any project maintenance result.
- **Real project result-SHA Testing/Validation:** `NOT_RUN` because no authorized product maintenance support-line/baseline/source-change/environment tuple has been provisioned. Source branch PASS cannot fill this dimension.
- **Fresh Independent Review:** `NOT_RUN`; a new read-only reviewer must assess the eventual **exact PR HEAD/tree** after a validator's results, without reuse of this Builder session.
- **Release Qualification, Deployment result, actual project backport completion:** all `NOT_RUN`; preparation and testing do not imply any of them. Optional batch scheduling is the **only illustrative** ceremony reduction in this fictional policy; it is not a project-wide hotfix exemption or real emergency authorization.

See `VALIDATION_REQUEST.md` for the independent local/real-project handoff and immutable evidence tuple; no CI success or fixture PASS may bypass that gate. If `version/v4.5.0` moves before review/validation, record and re-evaluate target-currentness and rerun affected combined tests rather than inherit this result.
