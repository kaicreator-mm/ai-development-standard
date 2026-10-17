# v4.13.1 adversarial consumer-flow acceptance plan (non-normative reference)

This reference is a **test design**, not a new Gate, not a substitute for `RELEASE_STANDARD.md`, and does not qualify a real Tally v2 runtime.

Original objective: prove ADS v4.13.1 process correctness in a fresh adopted project with real immutable root pin, organization preference conflict, materialized GitHub native DAG, bounded CI provider decision, and qualification. A smaller CLI may have source-level PASS but **whole objective HOLD**.

| ID | Negative setup | Expected fail-closed rule | Positive countercase |
|---|---|---|---|
| A1 | v4 pinned project with no `v4.adoption_level` | `verify_project_standard.py` nonzero | one real A0–A4 declaration |
| A2 | nested sample pin but repository root has no ADS configuration | root adopter verification FAIL | real project root AGENTS / VERSION / PROJECT_OVERRIDES |
| D1 | Task B lists `BLOCKED_BY=A` only in Markdown and native `blocked_by=[]` | Task B HOLD / NATIVE_DAG_NOT_PROVEN | actual native edge write/readback before dispatch; after A close source-currentness |
| C1 | Actions PASS, previously required Woodpecker FAIL/PENDING | Release HOLD for required provider | predeclared GH Actions-only selected profile with Woodpecker recorded informational **before** execution, or actual Woodpecker PASS |
| Q1 | source artifact tests PASS but original field objective requires live DAG/Host | `SOURCE_SCOPED_READY` not full-process PASS | every frozen objective cell has actual appropriate evidence |
| FR01 | host reports org-preferred runtime conflicting with project-selected bound | fail CONFLICT / do not force org preference | 2 compatible projects source-proven org suggestion |
| FR02 | Tally cache READY while native Issue blocker open | HOLD; no Claim/dispatch | GitHub blocker closed and Claim admission current |
| FR03 | compatible published ADS candidate B but active Task pinned A | prospective only, no current Task repin or unsafe auto-merge | opted-in PR with source-bound pre-merge checkpoint and actual rollback proof |

Only A1/selected C1 parser checks are executable ADS v4.13.1 checks. D1/FR01–03 require live project/native GitHub/Host or Tally consumer evidence and remain NOT_RUN until actually executed. Avoid interpreting this plan's text as an execution log.
