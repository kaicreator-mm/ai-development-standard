# ADS v4.11 V02 — Dedicated Candidate Ref and Transition Evidence

## Creation: append-only transition ledger

| Event | State / evidence |
|---|---|
| Scope | `kaicreator-mm/ai-development-standard` v4.11, V02 Issue #1022 |
| Predecessor | V01 #1021 CLOSED, terminal #1021@6194287317, **PASS limited to standards-repository reference conformance** |
| Process actor | `actor_role=release-controller`, `operator_kind=chatgpt-web`, `operator_id=chatgpt-web:ads-v411-v02-ref-controller`, `session_ref=ads-v411-20261015-v02-freeze-controller` |
| Attribution rule | Self-declared per merged #1122 / RELEASE §11.7, GitHub account only transport |
| Date of ref creation/preflight record | 2026-10-15T14:22:03Z — #1022@6194356447 |
| Creation | GitHub `create_branch` source SHA **`aac1e1206e4033601616c295e768e51fbc16efb1`**, new ref `refs/heads/candidate/v4.11.0-aac1e120` |
| Immediate ref readback | GitHub API `git/ref/heads/candidate/v4.11.0-aac1e120` → **`aac1e1206e4033601616c295e768e51fbc16efb1`** |
| Independent commit-tree readback | `git/commits/aac1e1206e4033601616c295e768e51fbc16efb1` → **`cb115035acd2eb7a2c77fb40b2f529a9f5cc10d7`** |
| Integration branch preflight | `version/v4.11.0` → same exact SHA (not itself the immutable candidate ref) |
| V01 actual tested candidate | C SHA **`aac1e1206e4033601616c295e768e51fbc16efb1`**, tree **`cb115035acd2eb7a2c77fb40b2f529a9f5cc10d7`** |
| Source-of-truth V01 evidence | #1021@6194287317 and GitHub Host Actions 38748798489 with explicit checkout at C; registered verify runs 38748429254 / 38748273713 |
| Release-gate currentness | #1021@6194175426 exact-subject applicability including N/A of real E2E to **standards corpus only** |
| Candidate ref immutability | Process-level **DO NOT MOVE**. Git ref is named branch for GitHub tooling, treated as dedicated immutable reference; branch permission mechanics alone are not immutability proof |
| Candidate Frozen | Pending explicit V02 issue terminal/readback/independent policy review (ref creation itself does not assert Freeze) |
| Hidden Validation | V03 #1023, NOT RUN |
| Fresh Final Closeout | V04, NOT RUN |
| Release Qualification | R01, NOT RUN |
| Guarded Integration | R02, NOT RUN |

## Evidence-only successor `E` separation

- The **candidate `C` is immutable**. Two required V02 evidence files are committed only to `refs/heads/evidence/v411-v02-freeze-aac1e120`, which begins at `C`; the evidence branch's final HEAD `E` has a different SHA/tree than `C`. `E` must never be asserted tested in V01.
- The freeze terminal must record actual final evidence HEAD `E` and the exact blobs for both V02 owned files. These are not new product/source facts and must never be merged into the pinned candidate ref just to store a record.
- A source-content mutation in any branch does **not** prove mutation of `C`. Conversely any movement of the **candidate ref**, publication of a newer version candidate presented as frozen, changed release/validation authority or newly found critical defect **invalidates eligibility** until a lawful new freeze.
- Signed V02 terminal and independent Review receipt belong to #1022; this file alone cannot imply PASS of Reviewer, V03 Hidden, RQ or final release.

## Required transitions and checks, to be appended by stage executors

1. **Before V03:** read `refs/heads/candidate/v4.11.0-aac1e120` and Git commit tree; require equal C SHA/tree above. Check #1021 closure and #1022 freeze/review evidence live.
2. **Before V04, R01, R02:** repeat the immutable SHA/tree and standard revision comparison, cite exact readback and stage provenance. A later V01 evidence-only `E` cannot replace `C`.
3. **On any thaw/invalidation:** record actual declaring operator, date/time, reason, prior C ref/tree, affected evidence, successor plan and independent new validation required. There is no in-place ref movement exception; original freeze remains historical.
4. **Negative tests:** mismatch/stale V01 evidence → no freeze; unresolved REQUIRED_NOW / UNKNOWN → no freeze; postfreeze ref drift → INVALIDATED; release name/tag in place of exact SHA → reject; editor/Builder rewriting V01 to fix freeze → reject; inherited concern-only DEFERRED as version PASS → reject; descendant `E` offered as tested `C` → reject.

## Actual known limits

The model-only 52 T12 case dispositions remain **20 PASS / 28 BLOCKED / 4 NOT_RUN**, original guarded runner EXIT=1; old 139 census remains 125 exit0 / 14 exit1; real human DENY E2E and real J09–J12 are NOT_PROVEN/NOT_CERTIFIED. Freeze is a standards-only source snapshot, NOT real protected runtime certification.

**This ledger does not itself perform future stage checks.** Their actual outputs must be added as new durable events by the acting stage executors and inspected against this fixed C identity.
