# T07 LOCAL_VALIDATOR — exact-result maintenance/hotfix validation request

**State: VALIDATION_REQUEST / REAL_PROJECT_RESULT_VALIDATION=BLOCKED (not attempted).** Dedicated **local** validator identity, separate from #276 Builder and from a later **NEW READ-ONLY** Fresh Independent Reviewer. This request does **not** authorize touching production, making a real hotfix release, changing support state, pushing a maintenance branch, or declaring PASS.

## A. Immediately executable independent reproduction (fixture only)

- Source repository: `kaicreator-mm/ai-development-standard`.
- Integration baseline originally selected: `version/v4.5.0@c9ee9249999aa5463ce880bc7674b732979009b3`.
- Builder branch: `task/276-v45-maintenance-hotfix-conformance` (record and rebind its **actual HEAD and TREE** on assignment; reject SHA drift).
- Fixture `SOURCE_SHA=d95e55c1d0cda233c648f01e7adc079181c68cba`, `TARGET_BASELINE_SHA=fda33c596039f19f124be57053c07c76806572bf`, `RESULT_SHA=5488dd2e24b9d1ef38d6d6212b0198ddabb31ac0` are **commits in a deterministic disposable repository only**, not existing ADS Git commits.
- Host: isolated Linux/Windows local host with Python >= 3.10, Git >= 2.28, SHA-1 Git repo support, writable temp directory, no external access/production credentials required; record OS, Python/Git versions, config and timezone. Do not confuse this local re-run with real-project validation.
- Re-run command from clean checked-out **exact PR HEAD**: `python3 -m unittest scripts/test_v45_maintenance_hotfix_conformance.py -v`; record start/end UTC, exit, full unredacted *nonsecret* output, log SHA-256, tested code HEAD/TREE, fixture source/baseline/result SHAs and actual `git show`/`git diff` equivalence. `python3 scripts/test_v45_maintenance_hotfix.py` may separately check the upstream T04 normative assertions. Do not reuse logs if PR HEAD changes.

## B. Real maintenance/hotfix exact-result proof (requires Controller's explicit bounded tuple)

**Unprovisioned inputs — do not invent:** durable actual project policy/owner/support state; authorized target support line and exact pre-change baseline; source repo/ref/exact source change SHA; approved class/scope; local host/toolchain; packaging or external test environment when required; explicit disposable versus actual branch mutation authority. The controlled fixture above demonstrates mechanics only, so an actual project Validation claim stays `BLOCKED` until these fields are explicitly assigned.

The LOCAL_VALIDATOR must, after authorization, produce a separate immutable result tuple:

```text
project_repository / policy_ref / owner_authority_ref / support_state / allowed_change_class
source_branch_ref / exact_source_change_sha / source_evidence_ref (source only)
target_support_line_ref / exact_prechange_target_baseline_sha
cherry_pick_or_backport_command / resulting_exact_SHA / resulting_tree_SHA
focused_test_commands+exits+logs+SHA256 bound to resulting_exact_SHA
required_environment_tuple (OS / Git / Python / build/runtime / artifact / packaging where material)
independent_result_SHA_Validation_commands+exits+logs+SHA256+authority
exact PR_HEAD/TREE and target-currentness/rebase assessment (when applicable)
Review request (NEW read-only reviewer), Release Qualification and Deployment: distinct NOT_RUN until their owners act
```

### Mandatory negatives and stop conditions

1. Validate owner, policy effective support state, supported line, **pre-change exact baseline**, allowed class and mutation authority **before** any cherry-pick or side effect. Branch/tag/package existence is insufficient; EOL or mismatched/unknown owner/baseline/class => `BLOCKED`.
2. Construct the resulting SHA from the exact approved baseline and the exact approved source change; record both SHA and tree, independently inspect `git show`/`git diff`, and reject source/result SHA substitution. Do not update/push the real maintenance branch without explicit separate permission.
3. Re-run all applicable focused tests and actual environment-dependent Validation on **resulting exact SHA**; commit logs and SHA-256/provenance in the specifically authorized destination. Source-side PASS, historical CI, another environment or another SHA never transfers.
4. Model preparation, actual backport completion, exact-result Validation, required independent Review, Release Qualification and Deployment as **separate evidence dimensions**. Hotfix urgency does not waive required gates or rollback/recovery authority.
5. If any required host/tool/authority/actual support line is absent, record `NOT_RUN/BLOCKED` with the missing exact tuple; no simulated/fixture result may be reclassified as real-project Validation.
6. Re-read live `version/v4.5.0` and this PR's exact HEAD immediately before final independent Review; if target advanced, reassess changed files and request affected combined-current-target Validation as needed.

**Return to #276:** `LOCAL_VALIDATOR_RESULT` with `fixture_reproduction=PASS/FAIL/NOT_RUN`, `real_project_result_validation=PASS/FAIL/BLOCKED/NOT_RUN` (only real if provisioned), all exact identities, commands/exits/digests, missing prerequisites and fresh review handoff. Only Controller can authorize the subsequent separate Reviewer; local validator cannot self-review or merge.
