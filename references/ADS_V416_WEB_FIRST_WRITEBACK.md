# ADS v4.16 T05 — Web-first plan and native validator publication guidance

**Source-only candidate** for [Task #1269](https://github.com/kaicreator-mm/ai-development-standard/issues/1269), based on accepted Product/L2/DAG #1261@6338348925/#6338359775/#6338768231 and exact `version/v4.16@6d147eac6c86eff620d3695a46ccbb3be452debb`. This reference consumes existing authority and **does not create a Gate, Dispatch family, universal WEB stage, automatic validator or Local Host obligation**. Required independent T05 source Review remains NOT_RUN.

## 1. Source owner matrix — extend guidance, never duplicate authority

| Decision | Existing source owner | What T05 adds (bounded reference only) |
| --- | --- | --- |
| Task/Execution Pack and exact JIT materiality | `standards/EXECUTION_PACK_STANDARD.md` §§2–7; `standards/DEVELOPMENT_WORKFLOW.md` Stage 3 | Compact per-Task step table of capability vs evidence, completed/remaining state |
| Work Item, native blocked_by, Claim serialization, ambiguous old Writer HOLD | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §§5/10/12 and `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §§11/27/29 | Explicit mandatory *existing* admission check before the first real source mutation |
| Web/CI/Local handoff and exact Task/PR/Host constraints | `standards/CHATGPT_WEB_ROLE.md`, `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md` §§2–5, 8, 12 | Web does allowed work, CI executes configured checks, Local receives only verified remaining physical/environment requirements |
| Native PR/Issue evidence versus admitted machine Event / gate | `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` §§5–9, 16; `standards/VALIDATION_STANDARD.md` | One compact writeback matrix with **native immutable subject + receipt + environment/command/exit + outcome limits** |
| Qualified release and true external Provider/Host effects | `standards/RELEASE_STANDARD.md` §§6–11, `standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` §21 | No inference from source-only evidence to runtime or Release PASS; no universal Host Gate |

### Step 0: 1–N-step proportionate Execution Plan

The existing Task Issue or Task/Execution Pack MAY display a short *read-only* plan like:

| Step | Deliverable / evidence class | Real capability needed | Preferred executor | State |
| --- | --- | --- | --- | --- |
| A | Frozen Task/L2 and affected-source/readset, negative hypotheses | GitHub READ | WEB | OBSERVED when read |
| B | Contract/docs/tests in allowed write set | current accepted Claim; GitHub write | WEB when capable; otherwise rightful executor | NOT_RUN until Claim |
| C | Focused source tests + exact SHA/runner IDs | actual Python/Node and configured CI | WEB/CI | PASS only for witnessed tuple |
| D | External Linux/Host/provider physical proof **if materially required** | exact environment, credentials, observable effect | LOCAL only for remaining obligation | NOT_APPLICABLE only with owner decision; else NOT_RUN |
| E | Independent source Review and native evidence publication | distinct Reviewer context + native GitHub readback | independent reviewer / owning validator | NOT_RUN until witnessed |

**Do not create a child Issue for each step.** Do not default to Local when WEB+CI evidence suffices. A Plan alone is not READY, accepted Claim, code permission, native GitHub event, Gate or version release. A source-only T05 reference is not proof that every downstream runtime has a functioning Web/Host planner.

## 2. Mandatory existing first-write preflight (C15)

Before **any** effect/commit: re-read exact Task Issue/native `type:task` and `state:*`, real blocked_by dependencies, source/current Task/Pack, expected integration SHA, allowed files and Review Policy; check one accepted serialized `DISPATCH_CLAIMED` for the protected key and no incompatible active/uncertain old Claim. Verify actual resource/environment and source owner permission at the effect boundary.

- `state:planned`, stale source, an unconfirmed/disputed Claim, missing Pack currentness or unknown permission ⇒ STOP/HOLD before source write.
- A Web preference or an agent saying `ROLE_CLAIMED` cannot replace the existing `SINGLE_WRITER_ADMISSION`/Claim admission, source verification or independent Review.
- If a Local physical proof is genuinely required after Web implementation, first durably record completed source, exact PR HEAD/test tuple, remaining physical evidence and valid terminal/handoff state. A different Local Agent cannot steal the same unresolved Builder Claim.
- If the Task consists solely of GitHub docs/Schema/tests + CI, Local is **not** a new prerequisite; an independent Reviewer remains a **role separation**, not by itself a physical Build Host requirement.

## 3. Native validation writeback vs structured REVIEW_RESULT (C16)

Two distinct claims can be made, and neither is inferred from comment shape alone:

1. **Observational/native evidence:** an actual GitHub PR/Issue comment or native CI run is an inspectable evidence carrier **only** when its numeric native ID/URL, owning repo, exact reviewed/tested subject SHA, source-verified environment tuple, command and exit code (or genuine reason NOT_RUN), findings/limits and successful readback are available. A native comment can preserve an independent validator's first-hand evidence even if it is not an admitted canonical `kind:event`; it does *not* by its own prose set Task/Gate PASS. Future successor controllers must re-evaluate applicable native/structured admission rules and exact source scope.
2. **Machine workflow decision:** `<!-- ads:github -->` + `schema: ads/github/v3` + `kind: event` + `data.event: REVIEW_RESULT | VALIDATION_RESULT` can be an **admitted** canonical workflow event only after §8.1 source/role/Claim/currentness/admission plus required schema/Review/Validation owner checks. A shape-valid quoted blob, chat text or reviewer self-report is merely input; native publication with no readback is `NOT_PUBLISHED`, not PASS. The independent reviewer and validator roles may write in their normal GitHub surface; the user's transport account alone is not reviewer independence.

Minimal evidence at handoff: `target repo/Issue/PR, exact subject SHA, native comment/run ID, operator/session, observed environment/commands/exit, result + P0–P3 where relevant, covered and excluded cases, required next receiver`. A standalone user-visible prompt should remain **pointer-only** under `ISSUE_FIRST_TASK_TRIGGER.md`. No new Event subtype, second validator gate, forced heavy `findings.records` for arbitrary native prose or replacement for the current v3 REVIEW_RESULT schema is introduced.

Missing GitHub ID or readback, conflicting comment edits, incomplete page/permission, failed real test, stale Source/Claim, or UNKNOWN independent attribution ⇒ hold the claimed machine outcome. An exact CI check PASS is a check/run fact, not a substitute for Review, external Tool permission, Provider Effect or Release Qualification. If controller evidence is source-qualified but not machine-admitted, preserve the native fact and report `EVIDENCE_AVAILABLE / ADMISSION_NOT_PROVEN` instead of backdating Event authority.

## 4. Deterministic source-only negative oracles

`scripts/test_v416_t05_writeback.py` consumes `tests/fixtures/v416/t05/scenarios.json` to exercise C15 (WEB-only, WEB+CI, WEB+LOCAL, stale/ambiguous Claim) and C16 (true native receipt vs chat-only/shape-only/unpublished/unknown exit code). The local oracle returns *illustrative routing/evidence classifications*, **not** canonical ADS Task/Event/Gate states. These fixtures do not call GitHub or prove a real Host, actual OSS permission, Tally scheduler or external cancellation.

Real task-meta/Tally #1210, controller #1231 and any future runtime credential/sink proof are separately `NOT_RUN` until their own admitted context. The current Task #1269 still requires executed conformance, independent exact-HEAD Review and a qualified version-only merge before `state:done`.
