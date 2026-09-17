# AGENTS.md

This project follows the immutable `kaicreator-mm/ai-development-standard` revision recorded in `.dev-standard/VERSION`.

## Read order

1. Read `.dev-standard/VERSION`.
2. Read `.dev-standard/PROJECT_OVERRIDES.md`.
3. Read the pinned standard's `AGENTS.md`.
4. For lifecycle work, read `standards/DEVELOPMENT_WORKFLOW.md`.
5. For Issue-based Task DAG, Builder/Reviewer/Validator queues, structured events, or stacked PR rules, read `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` and `standards/GITHUB_WORKFLOW.md`.
6. For repository structure/docs/tests, read `standards/PROJECT_STRUCTURE.md`, `DOCUMENTATION_STANDARD.md`, `TESTING_STANDARD.md`, and `REPOSITORY_STANDARD.md` as relevant.
7. For validation/release work, read `VALIDATION_STANDARD.md` and `RELEASE_STANDARD.md`.

## Project rules

- GitHub repository state, commit, Issue, Issue Dependency, PR, Review and Validation Evidence are execution facts; chat history is not.
- Frozen Task DAG is the planning checkpoint; GitHub Issue Dependencies are the canonical live execution DAG when Issue-based execution is enabled.
- Sub-issues express hierarchy, not implicit blocking.
- Stacked PR is only for a real unmerged code-baseline dependency and does not replace Issue Dependency.
- Version Branch Task/Fix PRs require Independent Review on the current exact HEAD SHA unless the pinned project override defines an authorized narrower exception.
- If PR HEAD changes after review PASS, affected review must be re-run.
- Do not change frozen product/architecture semantics to make implementation, review or CI easier.
- Use the commands and project-specific boundaries in `.dev-standard/PROJECT_OVERRIDES.md`.
- Formal Stage/Task outputs that become downstream dependencies require a remote checkpoint.
- Never report a required gate as PASS when it was not executed.

Keep this file short. Project-specific detail belongs in `PROJECT_OVERRIDES.md`; product and architecture facts belong in `docs/`.
