# Golden Template / Conformance Index

Status: `ACTIVE`

This index maps critical normative execution surfaces to compliant examples/templates and maintained negative examples. Golden material demonstrates shape; it is not project/task authority.

Every row MUST carry explicit repository references for both the Golden template/example and the Forbidden/rationale linkage. Anchor-qualified references are preferred when the target document contains multiple examples. The focused verifier parses this table row-by-row and validates those references.

| Surface | Owning standard | Golden template/example | Forbidden/rationale | Verification |
|---|---|---|---|---|
| Version Task DAG | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` + `standards/DEVELOPMENT_WORKFLOW.md` | `templates/task-dag.md` | `templates/golden/ANTI_PATTERNS.md#live-dag-document-as-authority` | `scripts/test_work_item_contract_and_golden_templates.py` |
| Version umbrella Issue | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` | `templates/version-issue.md` | `templates/golden/ANTI_PATTERNS.md#incomplete-executable-issue` | `scripts/test_work_item_contract_and_golden_templates.py` |
| Planning/DAG amendment | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` | `templates/planning-amendment-issue.md` | `templates/golden/ANTI_PATTERNS.md#silent-dependency-drift` | `scripts/test_work_item_contract_and_golden_templates.py` |
| Implementation Task Issue | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` + `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` | `templates/task-issue.md` | `templates/golden/ANTI_PATTERNS.md#incomplete-executable-issue` | `scripts/test_work_item_contract_and_golden_templates.py` |
| Research Issue | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` | `templates/research-issue.md` | `templates/golden/ANTI_PATTERNS.md#research-without-evidence-boundary` | `scripts/test_work_item_contract_and_golden_templates.py` |
| Research Demo | `standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md` | `templates/research-demo-issue.md`, `templates/research-demo-report.md` | `templates/golden/ANTI_PATTERNS.md#research-without-evidence-boundary` | `scripts/test_work_item_contract_and_golden_templates.py` |
| Bug/Fix Issue | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` | `templates/bug-fix-issue.md` | `templates/golden/ANTI_PATTERNS.md#incomplete-executable-issue` | `scripts/test_work_item_contract_and_golden_templates.py` |
| Validation request/handoff | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` + `standards/VALIDATION_STANDARD.md` | `templates/validation-request-issue.md`, `templates/validation-handoff-queue.md` | `templates/golden/ANTI_PATTERNS.md#gate-result-as-label` | `scripts/test_work_item_contract_and_golden_templates.py` + validation regressions |
| Blocker | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` | `templates/blocker-issue.md` | `templates/golden/ANTI_PATTERNS.md#incomplete-executable-issue` | `scripts/test_work_item_contract_and_golden_templates.py` |
| Independent Review | `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` | `checklists/pr-review.md`, `templates/agent-event-comment.md` | `templates/golden/ANTI_PATTERNS.md#self-asserted-independent-review` | v3.4 lifecycle/review regressions |
| Pointer-only trigger | `standards/ISSUE_FIRST_TASK_TRIGGER.md` | `standards/ISSUE_FIRST_TASK_TRIGGER.md#user-visible-trigger-contract` | `templates/golden/ANTI_PATTERNS.md#long-chat-task-contract` | `scripts/test_pointer_only_trigger_contract.py` |
| Structured Agent event | `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` | `templates/agent-event-comment.md` | `templates/golden/ANTI_PATTERNS.md#agent-identity-as-label` | `scripts/verify_event_writer_surfaces.py` |
| Implementation PR / exact-head evidence | `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` + `standards/VALIDATION_STANDARD.md` | `templates/implementation-pr.md` | `templates/golden/ANTI_PATTERNS.md#stale-pass-label` | lifecycle/validation regressions |
| Derived Version DAG View | `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` | `templates/version-dag-state-card.md` | `templates/golden/ANTI_PATTERNS.md#live-dag-document-as-authority` | `scripts/test_work_item_contract_and_golden_templates.py` |
| Release/Version closeout | `standards/RELEASE_STANDARD.md` | `templates/final-closeout.md`, `checklists/version-closure.md` | `templates/golden/ANTI_PATTERNS.md#stale-pass-label` | release/lifecycle regressions |

## Repository-wide authoring rule

Every active normative standard MUST either reference a Golden artifact from this index or contain/reference its own Golden Conformance Example and Forbidden example with rationale, per `standards/GOLDEN_TEMPLATE_STANDARD.md`.
