# ADS #1366 R16 — Source-first search for lawful v4.19 real Dispatch consumer

**Source data:** live GitHub readback of `.dev-standard/VERSION` at **14 specified repo/ref observations** across **12 repositories**, compared to prospective PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` (OPEN and unmerged). Captured at parent experiment HEAD `4de398a02f4c96d20ad763ea11d81a9a40ff0266` / TREE `b533ac4cee2225c6d0b82f5a80af8a1867e28937`. This is an **eligibility survey**, not execution of a real dispatch/Claim/CAS, an exhaustive organization-wide inventory, or an independent semantic review.

## Execution strategy review

R15's exact-source Python integration already executed **13/13 PASS, zero skips** in both WSL2 and Windows at the **fixed** R15 HEAD `4de398a02f4c96d20ad763ea11d81a9a40ff0266`; the original pre-fix HEAD had an import failure. Do not re-run the same unchanged R15 checks simply to produce new evidence. The R11 35 native + 61 Python and R13 32 paired + 7 mutations also retain their own fixed-SHA results; no model/source impact requiring re-run was detected.

R14 established three genuine *proof scope* gaps, not normative defects: READY/QUEUED visibility, event ordering, and real schema/payload/Claim persistence. A meaningful next step is a legitimately effective v4.19 Producer/Task/Claim subject; the initial Tally v4.18 observation was too narrow, so R16 widens source sampling without inventing an unauthorized producer.

## Observed project pins (at exact listed refs only)

| Repository | Observed ref | Declared ADS | R16 eligibility |
|---|---|---|---|
| `domain-harness` | `main` | `4.18.0` | NOT_ELIGIBLE_V419_PROSPECTIVE_CANDIDATE |
| `domain-forge` | `main` | `4.0.0` | NOT_ELIGIBLE_V419_PROSPECTIVE_CANDIDATE |
| `runx` | `main` | `4.14.0` | NOT_ELIGIBLE_V419_PROSPECTIVE_CANDIDATE |
| `shun-assistant` | `main` | `4.9.0` | NOT_ELIGIBLE_V419_PROSPECTIVE_CANDIDATE |
| `xDownload` | `main` | `4.18.0` | NOT_ELIGIBLE_V419_PROSPECTIVE_CANDIDATE |
| `tally` | `main` | `4.18.0` | NOT_ELIGIBLE_V419_PROSPECTIVE_CANDIDATE |
| `domain-harness` | `dis/0.2.0-element-intelligence-r1` | `4.18.0` | NOT_ELIGIBLE_V419_PROSPECTIVE_CANDIDATE |
| `tally` | `version/v2` | `4.18.0` | NOT_ELIGIBLE_V419_PROSPECTIVE_CANDIDATE |
| `ads-plane` | `main` | Version-only | UNKNOWN_NO_VALID_CANDIDATE_PIN |
| `formal-tools` | `main` | No file at ref | UNKNOWN_NO_VALID_CANDIDATE_PIN |
| `devkit` | `main` | No file at ref | UNKNOWN_NO_VALID_CANDIDATE_PIN |
| `task-meta` | `main` | No file at ref | UNKNOWN_NO_VALID_CANDIDATE_PIN |
| `task-meta-e2e` | `main` | No file at ref | UNKNOWN_NO_VALID_CANDIDATE_PIN |
| `ai-dev-pilot` | `main` | No file at ref | UNKNOWN_NO_VALID_CANDIDATE_PIN |

**Results:** 8/14 sampled branch tuples have a real old-version ADS pin (exact version+revision), 1/14 has a version-only string with no authoritative ADS revision, and 5/14 return `404` for **that specific file** at `main`. **0/14 provide a confirmed effective exact candidate v4.19 pin**. These 14 tuples are **not** all repositories or all branches; file absence and a standalone version string are `UNKNOWN`, not "no ADS usage". Current candidate source has not been merged. The two separately checked active branches `domain-harness/dis/0.2.0-element-intelligence-r1` and `tally/version/v2` were both pinned to 4.18.

`R16_CONSUMER_ELIGIBILITY_READBACK.json` includes the complete source head + blob for each successfully fetched file and the exact error class for missing files. **Eight** deliberately perturbed *synthetic* eligibility cases stayed unqualified, including wrong revision, no Task, no Claim, and no accepted readback. These are logic negative controls, not real Host/CAS tests.

## Decision / actionable admission sequence

1. A project/Task must **legally adopt** the effective v4.19 policy, with immutable ADS exact revision, Task scope and accepted current Claim; a bare `.dev-standard/VERSION` is insufficient even if its text says 4.19.
2. The real producer must show fully enriched payload → **actual** schema bytes/validation at the effective source → authorized role/profile/currentness → serialized publication of READY/QUEUED or accepted event, with checked/published identity and durable readback. Transport success and syntactic Schema PASS are not canonical admission.
3. Until such a subject is found, claim **NOT_PROVEN**, not PASS/FAIL for real production. Prioritize a **separate genuinely independent** source-to-model Reviewer for R13/R14/R15 rather than another simulated Controller. The reviewer must not reuse the Builder's conclusion as independent evidence.

## Qualification

`SOURCE_READBACK_ELIGIBILITY_SURVEY_DONE / REAL_V419_PRODUCER_NOT_PROVEN / FULL_ADS_RULE_DENOMINATOR_UNKNOWN`. No formal ADS normative P0/P1/P2 established. No authoritative ADS source, existing proof model, runner, old receipt, approved Task/Claim, GitHub Actions, merge, Freeze or Release changed.
