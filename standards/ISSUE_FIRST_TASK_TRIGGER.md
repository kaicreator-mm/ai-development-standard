# Issue-first Task Trigger Standard

## Purpose

This standard defines how a user, ChatGPT Web, Codex, Claude Code or another execution agent triggers work that is already represented by a durable GitHub work item.

The goal is to keep task execution recoverable from GitHub and to prevent chat from becoming a second, stale task specification.

## Canonical rule

```text
Issue = durable task contract and current Source of Truth
Trigger prompt = short ephemeral execution trigger
```

For invocation semantics, this is a MUST-level boundary:

```text
GitHub Issue + referenced repository authority = complete executable task contract
user-visible ChatGPT Web trigger = pointer only
```

A trigger prompt MUST NOT become a parallel task specification.

For task-specific facts, authority remains with the current GitHub Issue and its referenced Task Pack / Execution Pack / Dispatch / frozen inputs / evidence according to the normal authority order.

## Durable-contract precondition

Before ChatGPT Web or another dispatcher emits a user-visible task trigger, the assigned Issue MUST contain or reference every task-specific execution fact required by the receiving executor.

As applicable, durable authority MUST cover:

- goal and scope;
- dependencies;
- baseline / target / required branch;
- allowed and forbidden changes;
- acceptance criteria;
- implementation constraints that are required for correctness;
- tests and required gates;
- CI / Build Host / platform requirements;
- evidence and exact-SHA requirements;
- review requirements;
- failure / blocker behavior;
- completion / closeout rules.

The facts MAY live in the Issue body or in authoritative repository/GitHub artifacts referenced by the Issue. They MUST NOT exist only in chat history.

Hard invariant:

```text
No durable contract -> no trigger.
No Issue update -> no new task-specific instruction in chat.
```

If the Issue is incomplete, the dispatcher MUST repair/materialize the Issue or its authoritative referenced artifact first. It MUST NOT compensate by generating a longer handoff prompt.

If a task-specific requirement changes, persist the change to GitHub authority before invoking or re-invoking an executor. Do not distribute an updated long prompt as the primary contract.

## User-visible trigger contract

The user-visible/copyable task trigger MUST be pointer-only.

Allowed content is limited to routing identity needed to locate the durable contract:

```text
repository
Issue or PR number
role, only when needed to disambiguate the ready work
dispatch id, only when multiple dispatches cannot otherwise be distinguished
```

Default Task / Builder form:

```text
完成 `owner/repo` Issue #N。
```

Role-specific forms when disambiguation is required:

```text
执行 `owner/repo` Issue #N 的当前 READY builder dispatch。
执行 `owner/repo` Issue #N 的当前 READY validation dispatch。
完成 `owner/repo` PR #N 的当前 READY Independent Review dispatch。
```

Equivalent concise pointer wording is valid. The trigger does not need to restate that the Issue is authoritative because that behavior is owned by the pinned standard/bootstrap.

## Forbidden task-specific trigger content

A user-visible task trigger MUST NOT duplicate task-specific execution content, including:

- baseline SHA or successor SHA;
- branch/base refresh or rebase instructions;
- scope / non-scope details;
- allowed / forbidden files or write sets;
- acceptance criteria;
- implementation steps or algorithm instructions;
- exact commands or build/test command lists;
- validation gates / tuples / platform requirements;
- review checklist or finding-specific repair procedure;
- failure handling;
- closeout / merge instructions;
- architecture/product decisions;
- special repair instructions;
- exact evidence payload requirements.

If any such information is required to perform the work, it MUST be materialized in the assigned Issue or an authoritative artifact referenced from that Issue before the trigger is emitted.

## ChatGPT Web emission algorithm

When a user asks ChatGPT Web to generate a prompt, hand work to another agent/session, or continue work elsewhere, Web MUST execute this sequence:

```text
1. determine repository + assigned Issue/PR
2. read the current durable task contract
3. determine whether any required task-specific execution instruction is missing
4. if missing: create/update the Issue or authoritative linked artifact first
5. confirm the work item is executable / dispatchable
6. emit only the pointer-only trigger
```

Prompt length is never a fallback storage mechanism for an incomplete task contract.

A Web session that decides, for example, that an executor must refresh to a new base, preserve only one Task scope, rerun specific commands, wait for exact-head CI and request fresh review MUST write those requirements to GitHub first. Its user-visible handoff remains the same short Issue/dispatch pointer.

## Generic bootstrap distinction

Generic role discipline belongs in pinned repository-owned standards and bootstrap files, for example:

- `prompts/local-agent-bootstrap.md`;
- `prompts/local-builder-bootstrap.md`;
- `prompts/local-validator-bootstrap.md`;
- `prompts/web-reviewer-bootstrap.md`.

ChatGPT Web MUST NOT paste or regenerate those generic bootstrap instructions into every task trigger. The receiving executor is responsible for loading the pinned bootstrap/standard from repository facts.

Bootstrap text may appear in chat only when it is genuinely required to gain access to the durable contract itself. It MUST NOT carry task-specific execution semantics that could have been persisted in GitHub.

## Executor behavior

Before substantial work, the receiving LLM/Agent MUST re-read the current Issue/PR, assigned dispatch when present, relevant pinned standard, and referenced frozen inputs.

If copied trigger text conflicts with current authoritative GitHub facts:

```text
current authoritative GitHub facts
> stale copied trigger text
```

The executor follows current durable authority unless a higher-authority frozen source or project override says otherwise.

A copied trigger MUST NOT freeze an old branch name, SHA, acceptance condition or execution step. Such facts are read from GitHub at execution time.

## Prompt presentation

When presenting task trigger prompts for a human to copy:

- one task MUST use one independent copyable block/region;
- multiple tasks MUST NOT be combined inside one copyable block;
- one task = one Issue = one trigger prompt;
- explanatory text MAY appear outside the copyable block;
- the copyable block MUST remain pointer-only.

This applies even when several tasks run in parallel.

## Relationship to Local Agent Handoff

This standard does not weaken `LOCAL_AGENT_HANDOFF_PROTOCOL.md`.

For Local Agent Handoff:

```text
task-specific facts -> GitHub Handoff/Task Issue + referenced durable artifacts
generic execution discipline -> pinned standard / repository bootstrap
trigger prompt -> repository + Issue/PR + optional role/dispatch pointer only
```

A handoff cannot become `HANDOFF_READY` merely because a long chat prompt fills missing Issue fields. If the durable contract is incomplete, repair it first.

## Pull-role pointer invocation (v3.4)

When work is dispatched through the unified dispatch architecture, the same rule applies per role. The dispatch and its Issue/PR remain the contract; the trigger only selects the work. The canonical user-visible forms remain exactly the repository pointer shapes defined above:

```text
执行 `owner/repo` Issue #N 的当前 READY builder dispatch。
执行 `owner/repo` Issue #N 的当前 READY validation dispatch。
完成 `owner/repo` PR #N 的当前 READY Independent Review dispatch。
```

Do not add project name, version, SHA, branch, gate, scope, commands or other task-specific context to these user-visible role triggers. If a dispatch id is required to disambiguate multiple READY dispatches, append only that dispatch identity.

One task = one dispatch = one trigger prompt. The executor MUST re-read current dispatch/Issue facts, including `requested_head_sha` when required, instead of trusting copied chat detail.

## Execution Pack prompt artifacts

An optional `LOCAL_AGENT_PROMPT.md` inside an Execution Pack, when a project retains one, is a durable repository artifact subordinate to the Task Pack / Execution Contract. It is not the user-visible ChatGPT Web task trigger.

ChatGPT Web MUST NOT copy an Execution Pack prompt artifact into chat as the handoff contract. The trigger points to the Issue/dispatch that in turn references the Execution Pack.

## Anti-patterns

Do not:

- paste the Issue body into the trigger prompt;
- maintain a second detailed task contract in chat;
- generate a bespoke long prompt because the Issue is incomplete;
- put baseline SHA, branch rules, commands, gates, review steps or closeout rules in the user-visible trigger;
- put several task prompts into one shared copyable region;
- treat an old copied prompt as more authoritative than current GitHub facts;
- rely on previous conversation context to supply required task facts;
- paste generic role bootstrap text into each per-task trigger;
- copy `LOCAL_AGENT_PROMPT.md` from an Execution Pack into chat as task authority.

## Completion principle

The trigger prompt starts execution. The Issue defines execution.

A successful handoff remains valid when a different compatible LLM/Agent receives only the repository + Issue/PR (+ optional role/dispatch pointer) and reconstructs the complete task from GitHub.