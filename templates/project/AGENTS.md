# AGENTS.md

This project follows the immutable `kaicreator-mm/ai-development-standard` revision recorded in `.dev-standard/VERSION`.

## Read order

1. Read `.dev-standard/VERSION`.
2. Read `.dev-standard/PROJECT_OVERRIDES.md`.
3. Read the pinned standard's `AGENTS.md`.
4. For lifecycle work, read `standards/DEVELOPMENT_WORKFLOW.md`.
5. For L2 architecture work, unresolved architecture assumptions, executable spikes, or research demos, read `standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md` and `prompts/L2_ARCHITECTURE_EVIDENCE.md`.
6. For Issue-based Task DAG, Builder/Reviewer/Validator queues, structured events, Actor/Operator Attribution, or stacked PR rules, read `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` and `standards/GITHUB_WORKFLOW.md`.
7. For repository structure/docs/tests, read `standards/PROJECT_STRUCTURE.md`, `DOCUMENTATION_STANDARD.md`, `TESTING_STANDARD.md`, and `REPOSITORY_STANDARD.md` as relevant.
8. For validation/release work, read `VALIDATION_STANDARD.md` and `RELEASE_STANDARD.md`.

## Project rules

- GitHub repository state, commit, Issue, Issue Dependency, PR, Review and Validation Evidence are execution facts; chat history is not.
- GitHub username/API account is transport identity only. New v3.1+ structured events SHOULD distinguish `actor_role`, `operator_kind`, `operator_id`, `session_ref`, and `transport_actor`.
- Multiple ChatGPT Web pages or Local Agent runs using one GitHub account must remain distinguishable by logical operator/session attribution. Do not create dynamic GitHub labels for per-session IDs.
- `ROLE_CLAIMED/ROLE_RELEASED` may record who is currently acting in a workflow role; these are attribution/routing events, not Gate PASS or distributed locking.
- Frozen Task DAG is the planning checkpoint; GitHub Issue Dependencies are the canonical live execution DAG when Issue-based execution is enabled.
- Sub-issues express hierarchy, not implicit blocking.
- Stacked PR is only for a real unmerged code-baseline dependency and does not replace Issue Dependency.
- Independent Review is risk-based. Each Task/PR follows its declared `required / recommended / not-required` Review Policy from PROJECT_OVERRIDES / Task DAG / Task Issue.
- `review:required` must be satisfied on the current exact PR HEAD SHA before merge; `review:recommended` may be explicitly performed or skipped; `review:not-required` must not be turned into a mandatory Review Gate merely because Version Branch Mode is used.
- Required Independent Review must be attributable to a context independent from the Builder context. The same GitHub transport account may be used if logical operator/session identity proves the separation.
- If PR HEAD changes after a Review PASS, re-review is required only when the Review Policy is `required` or the optional Review is intentionally being continued for the new SHA.
- Architecture Research Demo is risk-driven evidence, not a universal Task gate. Create one only for a material Architecture UNKNOWN when static/source evidence is insufficient.
- A Research Demo must test the real boundary under study, use deterministic fakes only for unrelated dependencies, include negative/failure evidence, bind conclusions to exact identity, and state `What was NOT proven`.
- After L2 Freeze, normal implementation tasks should implement directly; reopen research only for newly discovered high-impact architecture unknowns.
- Do not change frozen product/architecture semantics to make implementation, review or CI easier.
- Use the commands and project-specific boundaries in `.dev-standard/PROJECT_OVERRIDES.md`.
- Formal Stage/Task outputs that become downstream dependencies require a remote checkpoint.
- Never report a required gate as PASS when it was not executed.

Keep this file short. Project-specific detail belongs in `PROJECT_OVERRIDES.md`; product and architecture facts belong in `docs/`.
