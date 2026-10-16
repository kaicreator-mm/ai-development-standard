# ADS v4.13 — Source-bound Execution Interoperability Reference

> **Reference / projection, NOT a new normative workflow, schema, Task DAG, Claim system, or runtime.**  
> Source: frozen Product R0 `702bcf562b4292487fa8409cd17dee2d42aae9b3`, L2 R0 `86b9243c065ab909f82d52d1d7b7f945791d3696`. Canonical authorities live in existing `standards/*` and their versioned schemas. Tally v2 is one intended consumer but independent Agents/platforms MAY consume these same contracts without Tally installation.

## 1. Goal and authority boundaries

This reference helps an execution platform map **existing ADS-native GitHub engineering facts** to its own operational scheduling/execution status. It does **not** grant GitHub writes, approve a claim, certify a Gate, authorize a release, or change the standard adopted by an in-flight Task.

```text
Project immutable .dev-standard/VERSION + PROJECT_OVERRIDES
                 |
     frozen Product / L2 / Task Contract / Review policy
                 |
 actual native GitHub Issue blocked_by / accepted Claim / exact Git SHA
                 |
         read-only derived Task readiness
                 |
  Tally/consumer Attempt + Agent Run + Host/Workspace operations
                 |
 immutable ChangeSet/PR HEAD + actual Validation & Review evidence
                 |
 current GitHub PR/Review/Merge/Task facts + Release subject check
                 |
     project/task state projection (reconstructible, not writer authority)
```

## 2. Canonical source map

| External/standard subject | Canonical authority and source | Consumer may store | Consumer MUST NOT infer |
|---|---|---|---|
| effective ADS version | `PROJECT_ADOPTION.md`: `.dev-standard/VERSION` `repository/version/revision` from exact Git source; effective frozen Task source recorded separately | immutable resolved standard revision + audit source | `latest` or `main` is a Task's effective revision |
| project overrides & required gates | Frozen Product/L2 + project `PROJECT_OVERRIDES` + current exact applicable standards | derived applicable policy map with refs | host defaults or org preferred runtime waive a project requirement |
| live implementation Task topology | `TASK_DAG_GOVERNANCE_STANDARD.md`, GitHub native Issue Dependencies, original Issue/Work Item | cached dependency snapshot with source/currentness, ready/hold observation | a local Active TaskDAG, Markdown list, sub-issue or PR stack overwrites a native `blocked_by` |
| accepted work/Claim | `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §12.1 and accepted `DISPATCH_CLAIMED`/current workflow facts | local Attempt and dispatch correlation | Agent summary or `ROLE_CLAIMED` alone authorizes source write |
| logical execution actor | `GITHUB_AGENT_INTERACTION_PROTOCOL.md` §5–8, self-declared `operator_kind/operator_id/session_ref/role` | declared logical actor/ref/actual transport metadata separately | the shared GitHub login **proves** Agent identity or independence |
| workspace, Agent and Host attempts | consumer runtime only; workspace artifact classification under `WORKSPACE_ARTIFACT_STANDARD.md` | runnable/blocked/retry/cancel state, Host process/log, worktree ref | Attempt `DONE` is canonical GitHub Task DONE or candidate PASS |
| executable result and evidence | `VALIDATION_STANDARD.md`: exact tested source, environment/profile, executed command/exit, required Gate | EvidenceRef/log pointer, actual outcome and currentness calculation | PASS from unexecuted/unknown/skipped tests, synthetic mock or stale base |
| Review and merge | Review Policy + actual independent source-bound review as applicable; actual GitHub PR/branch/merge readback | derived merge eligibility and change lineage | PR green means Version Release PASS; reviewer text without actual source basis means current PASS |
| version Release | `RELEASE_STANDARD.md` candidate/current actual gate/qualification/Tag facts | read-only Release status & external evidence refs | a Task PR merged or local project graph complete equals actual Release Qualification |

**All examples assume the exact ADS version adopted by that Project** and must be re-evaluated under that historical revision. The above paths are references to current v4.13 canonical owners, **not a retroactive adoption migration**.

## 3. Safe projections versus writes

An ADS-native consumer may compute `READY | STALLED | BLOCKED | UNKNOWN` as a **dashboard projection** from GitHub and execution facts. Those are not new canonical `state:*` workflow labels or new Gate states. The canonical workflow state vocabulary remains under the Work Item Contract and exactly one current `state:*` label/native equivalent. A consumer owns its Agent/Attempt queue states separately.

At material **dispatch**:
1. Resolve the project's exact ADS revision and Frozen Task/Claim/Review policy, including canonical native Issue dependency edges.
2. Re-read current GitHub Issue, native blocker state and dispatch/accepted Claim predicates; stale/missing source or permission = HOLD, not optimistic READY.
3. Apply existing `state:ready → claimed → implementing` serialized/atomic admission, with source-bound dispatch and self-declared operator data. Tally's local queue reservation is not an accepted Claim.
4. Only the accepted Task writer may mutate allowed Task worktree/source. Isolate per Task and preserve all uncommitted/unique data on uncertain cleanup.

At material **PR merge / Task advancement / version qualification**:
1. Re-read the exact source/PR head/base/merge-result and actual selected Review/Validation currentness.
2. Independently prove applicable owner Gate predicates; `NOT_RUN`/provider timeout is never an executed PASS.
3. Check native issue dependency/Claim and any required integration/branch authority; persist actual GitHub outcome/evidence.
4. Project the result into Tally/consumer snapshot **after** observed GitHub truth. Never mutate native Task graph by writing only local DAG state.

The standard defines task/authority facts; the consumer picks storage/Runtime/OS details. No Tally Go code, SQLite schema, Agent scheduling algorithm, MCP transport, GitHub PR writer or runnable CLI belongs to this reference.

## 4. Exact identity envelope (illustrative, not new required schema)

```yaml
project:
  repository: kaicreator-mm/example-adopter
  pinned_ads_revision: "<actual 40-hex revision>"
  override_source_ref: "<immutable project source>"
task:
  github_issue: "#123"
  task_contract_source: "<frozen repo tree/blob>"
  native_blockers_readback: "<GitHub API exact observation>"
  accepted_claim_ref: "#123@<canonical event id>"
attempt:
  runtime_owner: "consumer platform, e.g. Tally"
  dispatch_ref: "<actual accepted dispatch id>"
  logical_actor: {operator_kind: "chatgpt-web", operator_id: "builder-example", session_ref: "session-ref"}
  workspace_ref: "<per Task worktree>"
evidence:
  candidate_sha: "<actual immutable candidate SHA>"
  validation_tuple_ref: "<actual executed profile/command/exit/result>"
  review_result_ref: "<actual independent review if required>"
outcome:
  pr_merge_readback: "<actual GitHub PR/merge observation>"
  release_ref: "<only if actually qualified>"
```

A projection may omit unavailable nonessential fields but MUST report material missing currentness truthfully; the sample does not grant permission to invent a current Claim/PR/release or to store credentials in public records. Source identities and roles shown in angle markers are placeholders, **not valid passing executable evidence**.

## 5. Focused consumer scenarios

| ID | GitHub/native facts and consumer observation | Correct outcome |
|---|---|---|
| P01 | GitHub Task A native `blocked_by B`; Tally cached A=READY while B is still open | **HOLD A**; readback wins over stale derived READY, no execution/Claim |
| P02 | GitHub B closed with real accepted facts; A Issue ready, actual current Task Pack and no conflicting Claim | eligible for canonical **CAS Claim** (not automatically claimed by dashboard) |
| P03 | two self-declared `operator_id/session_ref` contexts share GitHub transport login | logical actors distinct by their own declarations, **not** proof of two independent executed validation subjects |
| P04 | Task accepted at ADS SHA A; newer compatible release B has a prospective non-SAFE update proposal | Task remains SHA A; B does not retarget existing Task/Claim/Review/Validation |
| N01 | Agent states “completed”, but no immutable ChangeSet, actual required test or GitHub merge | no PASS and no Task DONE |
| N02 | Tally executor has a green local test result bound to old head; PR/target changed materially | no current PASS without valid `VALIDATION_IMPACT_DECISION`/re-execution |
| N03 | GitHub read unavailable, local Issue snapshot appears unblocked | materially consequential dispatch/merge HOLD; unrelated source-sufficient operations may proceed |
| N04 | project uses historical Tally `version: 1.2.1` YAML pin | do not parse it silently as ADS v4.12+ `repository/version/revision`; project-local prospective migration required |

## 6. Failure, compatibility and ownership

The future Tally v2 migration of its existing `Active TaskDAG`, frozen Requirements/Plan/Architecture/Task/Completion models and old YAML standard pin is **owned in Tally**; this reference does not claim a completed migration. Existing Tally v1.5.x records remain under their original exact authority. New high-impact contradictions with ADS canonical owners must be resolved through the owning standard, not a Tally-specific shadow Gate schema.

- GitHub missing/blocked source fact → `UNKNOWN/HOLD` for relevant operation; not `NOT_APPLICABLE` and not global project FAIL.
- Tool/Host unavailable → factual execution `BLOCKED/NOT_RUN`; independent repo specification checks may continue as their authority allows.
- Permission denied → no write, no invented “merge approved”; record real platform failure.
- Agent instruction/model changes → do not rewrite current accepted Task identity/source; preserve proven evidence only within identical actual predicates/currentness.
- Project moves its effective ADS revision by a lawful #1119 checkpoint → new eligible Tasks use new pinned SHA; old accepted Tasks and historical Reviews remain pinned to their original source.

**Scope & strength:** This document is static source guidance for consumers. No real native multi-Agent Task/Claim/CAS race, Tally v2 execution, consumer deployment or real GitHub updater E2E is claimed by creating this reference. Product/Architecture/Issue changes remain governed by ordinary Review and Release rules.
