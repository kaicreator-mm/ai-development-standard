# Codex Handoff Protocol

## 1. Status

This file is the Codex-specific compatibility entry for the generic Local Agent Handoff model introduced in v2.1.

New handoffs SHOULD follow:

- `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`
- `templates/local-agent-handoff-issue.md`
- `prompts/local-agent-bootstrap.md`

Codex remains a supported executor, but the task contract MUST NOT depend on Codex-specific chat context.

## 2. Codex-specific labels

For a Codex execution/validation issue, recommended labels include:

```text
type:validation
handoff:local-agent
executor:codex
```

Add gate/environment/release-impact labels as required, for example:

```text
gate:integration
gate:platform
gate:hidden
env:ubuntu-build-host
env:windows
env:macos
env:gpu
release-blocker
blocked:environment
```

Use a version Milestone such as `vX.Y.Z` when supported by the repository.

## 3. Required contract

A Codex handoff MUST satisfy every required field of `LOCAL_AGENT_HANDOFF_PROTOCOL.md`, including:

- Standard Version + immutable revision
- Repository
- integration/target branch
- Baseline Commit
- Scope / Task IDs
- Frozen Inputs
- Web Completed / Existing Validation
- Remaining Work
- Required Gates / Validation Tuples
- Execution Environment
- Validation Profile
- Exact Commands / canonical project entrypoints
- Allowed / Forbidden Changes
- Expected Output
- Completion Rule
- Failure / Blocker Reporting Rule

## 4. Baseline rule

Codex MUST use the Issue's exact baseline commit and pinned standard revision. It MUST NOT silently replace the baseline with a newer branch HEAD.

If source changes are required, Codex creates or uses the declared task/fix branch and targets the correct integration branch. In Version Branch Mode this is normally `version/vX.Y.Z`, not `main`.

## 5. Validation-only rule

A validation-only Codex handoff does not require a branch.

If validation passes without source changes, record exact-SHA evidence and update/close the Issue according to its completion rule.

If validation finds a defect requiring code changes, create a task/fix branch, produce the PR, and rerun affected required gates against the resulting exact SHA.

## 6. Completion

The handoff ends only when:

- all required gates PASS and commit/PR + Validation Report are linked; or
- the remaining path is explicitly FAIL/BLOCKED with reproduction, evidence, impact and any upstream decision required.

A finished command run is not by itself a completed Handoff.
