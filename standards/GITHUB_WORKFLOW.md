# GitHub Workflow — v3.3 Compatibility Entry

This file is retained as a stable path for older adopters. v3.3 no longer maintains a second full copy of GitHub workflow rules here.

For new work, use the following authorities:

1. `DEVELOPMENT_WORKFLOW.md` — lifecycle, integration modes, Task/Review/Validation stages.
2. `EXECUTION_ARCHITECTURE_STANDARD.md` — reducer, ready queues, dispatch, drift, controllers, Candidate Freeze and execution-state separation.
3. `GITHUB_AGENT_INTERACTION_PROTOCOL.md` — Issue/PR/events/operator attribution and GitHub-native coordination.
4. `VALIDATION_STANDARD.md` — exact-SHA Validation authority.
5. `RELEASE_STANDARD.md` — Candidate/Release/Repository Integration authority.

GitHub remains the durable execution fact source. Issue Dependencies remain the canonical live execution DAG when Issue-based execution is used.

Historical `ai-dev:event:v1` records remain readable historical evidence. **All newly emitted structured Agent events use `ai-dev:event:v2` unless a future protocol supersedes it.**

This compatibility entry is intentionally short to prevent normative drift between multiple copies of the same workflow.
