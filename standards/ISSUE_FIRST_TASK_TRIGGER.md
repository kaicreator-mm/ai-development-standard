# Issue-first Task Trigger Standard

## Purpose

This standard defines how a user, ChatGPT Web, Codex, Claude Code or another execution agent should trigger work that is already represented by a GitHub Issue.

The goal is to keep task execution recoverable from GitHub and avoid stale duplicated instructions in chat prompts.

## Canonical rule

```text
Issue = durable task contract and current Source of Truth
Trigger prompt = short ephemeral execution trigger
```

A trigger prompt MUST NOT become a parallel task specification.

For task-specific facts, authority remains with the current GitHub Issue and its referenced frozen inputs/evidence according to the normal authority order.

## Issue owns execution detail

The Issue SHOULD contain all task-specific information needed to execute the work, including as applicable:

- goal and scope;
- dependencies;
- baseline / target / required branch;
- allowed and forbidden changes;
- acceptance criteria;
- tests and required gates;
- CI / Build Host / platform requirements;
- evidence and exact-SHA requirements;
- completion / closeout rules.

Do not copy these details into the trigger prompt merely for convenience.

If a task detail changes, update the Issue or its authoritative referenced artifact. Do not rely on distributing a new long prompt to every executor.

## Trigger prompt

A trigger prompt SHOULD be as short as practical. Normally it only needs to:

1. identify the repository and Issue;
2. require the executor to re-read the current Issue;
3. state that the Issue is the task Source of Truth;
4. request complete execution and closeout according to the Issue.

Recommended form:

```text
完成 `owner/repo` Issue #N。

重新读取 GitHub Issue，以当前 Issue 为 Source of Truth，完整执行并将成果提交到 Issue 指定的分支。满足 acceptance 后完成 closeout。
```

Equivalent concise wording is valid.

Additional bootstrap text is allowed only when the executor needs information that cannot appropriately live in the Issue or pinned standard. Task-specific execution instructions SHOULD still be moved into the Issue rather than repeated in the trigger.

## Executor behavior

Before doing substantial work, the receiving LLM/Agent MUST re-read the current Issue and relevant pinned standard/frozen inputs.

If the copied trigger prompt conflicts with the current Issue:

```text
current authoritative GitHub facts
> stale copied trigger text
```

The executor must follow the current Issue unless a higher-authority frozen source or project override says otherwise.

A copied prompt MUST NOT freeze an old branch name, SHA, acceptance condition or execution step after the Issue has been updated.

## Prompt presentation

When presenting task trigger prompts for a human to copy:

- one task MUST use one independent copyable block/region;
- multiple tasks MUST NOT be combined inside one copyable block;
- prefer one task = one Issue = one trigger prompt;
- explanatory text may appear outside the copyable block, but the block itself SHOULD remain short.

This rule applies even when several tasks are intended to run in parallel.

## Relationship to Local Agent Handoff

This standard does not weaken `LOCAL_AGENT_HANDOFF_PROTOCOL.md`.

For a Local Agent Handoff:

```text
task-specific facts -> GitHub Handoff/Task Issue
generic execution discipline -> pinned standard / bootstrap
trigger prompt -> repository + Issue reference, plus only essential bootstrap
```

The executor should be able to recover the task without hidden chat history.

## Pull-role pointer invocation (v3.4)

When work is dispatched through the unified dispatch architecture, the same issue-first rule applies per role. The trigger stays a pointer; the dispatch and its Issue remain the contract:

```text
Continue <project> <version> current READY builder work in Issue #NN.
Continue <project> <version> current READY validation work in Issue #NN.
Continue <project> <version> current READY review work in PR #NN.
```

One task = one dispatch = one trigger prompt. The executor MUST re-read the current dispatch/Issue facts (including `requested_head_sha` for validators) rather than trust the copied prompt.

## Anti-patterns

Do not:

- paste the entire Issue body into the trigger prompt;
- maintain a second detailed task contract in chat;
- put several task prompts into one shared copyable region;
- treat an old copied prompt as more authoritative than the current Issue;
- rely on previous conversation context to supply required task facts that should be in GitHub;
- duplicate acceptance/gates/branch rules in prompts unless required to bootstrap access to the Issue itself.

## Completion principle

The trigger prompt starts execution. The Issue defines execution.

A successful handoff should therefore remain valid when a different compatible LLM/Agent receives the same repository + Issue reference and reconstructs the task from GitHub.