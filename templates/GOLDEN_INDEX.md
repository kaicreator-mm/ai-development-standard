# Golden Template / Conformance Index

Status: `ACTIVE`

This index maps critical normative execution surfaces to compliant examples/templates and maintained negative examples. Golden material demonstrates shape; it is not project/task authority.

All rows use `templates/golden/ANTI_PATTERNS.md` as the shared negative-example library unless a more specific negative example is embedded in the owning standard/template.

| Surface | Owning standard | Golden template/example | Forbidden/rationale | Verification |
|---|---|---|---|---|
| Version Task DAG | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` + `DEVELOPMENT_WORKFLOW.md` | `templates/task-dag.md` | `templates/golden/ANTI_PATTERNS.md#live-dag-document-as-authority` | `scripts/test_work_item_contract_and_golden_templates.py` |
| Version umbrella Issue | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` | `templates/version-issue.md` | `templates/golden/ANTI_PATTERNS.md#incomplete-executable-issue` | focused verifier |
| Planning/DAG amendment | same | `templates/planning-amendment-issue.md` | `templates/golden/ANTI_PATTERNS.md#silent-dependency-drift` | focused verifier |
| Implementation Task Issue | same + `GITHUB_AGENT_INTERACTION_PROTOCOL.md` | `templates/task-issue.md` | `templates/golden/ANTI_PATTERNS.md#incomplete-executable-issue` | focused verifier |
| Research Issue | same | `templates/research-issue.md` | `templates/golden/ANTI_PATTERNS.md#research-without-evidence-boundary` | focused verifier |
| Research Demo | `ARCHITECTURE_RESEARCH_DEMO_STANDARD.md` | `templates/research-demo-issue.md`, `templates/research-demo-report.md` | shared anti-pattern library | existing + focused verifier |
| Bug/Fix Issue | Work Item Contract | `templates/bug-fix-issue.md` | shared anti-pattern library | focused verifier |
| Validation request/handoff | Work Item Contract + `VALIDATION_STANDARD.md` | `templates/validation-request-issue.md`, `templates/validation-handoff-queue.md` | `templates/golden/ANTI_PATTERNS.md#gate-result-as-label` | focused + validation regressions |
| Blocker | Work Item Contract | `templates/blocker-issue.md` | shared anti-pattern library | focused verifier |
| Independent Review | `GITHUB_AGENT_INTERACTION_PROTOCOL.md` | `checklists/pr-review.md`, `templates/agent-event-comment.md` | `templates/golden/ANTI_PATTERNS.md#self-asserted-independent-review` | v3.4 lifecycle/review regressions |
| Pointer-only trigger | `ISSUE_FIRST_TASK_TRIGGER.md` | canonical trigger examples in owning standard | `templates/golden/ANTI_PATTERNS.md#long-chat-task-contract` | `scripts/test_pointer_only_trigger_contract.py` |
| Structured Agent event | `GITHUB_AGENT_INTERACTION_PROTOCOL.md` | `templates/agent-event-comment.md` | `templates/golden/ANTI_PATTERNS.md#agent-identity-as-label` | `verify_event_writer_surfaces.py` |
| Implementation PR / exact-head evidence | interaction + validation standards | `templates/implementation-pr.md` | `templates/golden/ANTI_PATTERNS.md#stale-pass-label` | lifecycle/validation regressions |
| Derived Version DAG View | Work Item Contract | `templates/version-dag-state-card.md` | `templates/golden/ANTI_PATTERNS.md#live-dag-document-as-authority` | focused verifier |
| Release/Version closeout | `RELEASE_STANDARD.md` | `templates/final-closeout.md`, `checklists/version-closure.md` | shared anti-pattern library | release/lifecycle regressions |

## Repository-wide authoring rule

Every active normative standard MUST either reference a Golden artifact from this index or contain/reference its own Golden Conformance Example and Forbidden example with rationale, per `standards/GOLDEN_TEMPLATE_STANDARD.md`.
