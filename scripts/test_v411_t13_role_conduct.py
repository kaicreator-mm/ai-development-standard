"""V411-T13 focused regression: role-scoped individual engineering conduct.

Encodes the V411-T13 Task Pack (immutable blob
d487e016ae1efd551808b498c09d0f52253ec1f8, frozen at version/v4.11.0,
docs/implementation/4.11.0/task-packs/V411-T13_role_conduct_boundaries.md)
§3 oracles P01-P04 / N01-N06 for the role-conduct owner concern as:

1. section-scoped textual contract checks binding the decision model to the
   owner-local normative clauses this task appends to
   `standards/DEVELOPMENT_WORKFLOW.md` (the ONE new unnumbered `### Role
   conduct trace` subsection of §4 Gate Authority) and to
   `standards/TASK_DECOMPOSITION_STANDARD.md` (the ONE new `### 2.1 Role /
   Task-entry requirements` subsection adjacent to §2 Required durable Task
   facts); plus verbatim byte-span guards that the T01 effective-rule floor
   subsection, the T02 risk-intake section and the preexisting heading
   sequences stay byte-unchanged; and
2. a fixture-driven ROLE_CONDUCT_TRACE decision model that consumes the T01
   floor and the T02 materiality inventory facts read-only (single
   resolution path: the trace never re-derives gates, it calls the floor
   function) and binds each actor-subject's Input → Allowed acts → Required
   evidence → Handoff/Exit chain to concrete outcomes.

Placement adjudication (recorded honestly, per the pack's own authority
rules): the frozen pack §2 pins the new Workflow section only by SEQUENCE —
"sequential to (not overlapping) T02's risk-intake section AND T01's §4
effective-rule subsection" — and pack §4 states "no exact-base patch, line
map or transient-HEAD assumption is authority", so the heading NUMBER is a
lawful builder choice (pack §8 F2). The section is therefore placed as an
unnumbered §4 subsection immediately after T01's effective-rule trace (its
content span is byte-pinned below) and before §5, satisfying sequential-to-
both; the numbered `### 2.4` form in the §2-tail→§3 span was avoided because
the frozen T02 boundary guard (test_v411_t02_risk_intake.py,
`assertNotIn("### 2.4", between)`) lawfully reserves that span for T02. No
existing test or shared file was touched.

Purely offline: standard library only, no network, no shared verifier.

The trace is a per-actor-subject RESOLUTION record over existing authority;
`GAP/UNVERIFIED`, `CONFLICT`, `HANDOFF_REQUIRED_TO_LOCAL` and the decision
vocabulary below are this test's routing/disposition vocabulary (the pack's
failure-handling terms), not new Gate/Validation/Release states — the gate
enum stays `PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE`. `DEFERRED_TO_T11` is
this file's routing vocabulary for the v4.11 line's centrally designated
wiring task; the standard itself routes to the existing canonical owner
without naming it.

Known deferrals (honest, never reported as covered): the central machine
projection of ROLE_CONDUCT_TRACE (schema/manifest/verifier) is
DEFERRED_TO_T11 — the model routes any such proposal to T11 unwritten and
the real-tree half asserts no shadow projection exists; whole-program
role-scoped conformance (T12) stays NOT_RUN. T01 floor semantics and T02
inventory semantics are consumed read-only and deliberately not
re-implemented here.

Known expected RED outside this file (disclosed, neither hidden nor
duplicated): any byte change to DEVELOPMENT_WORKFLOW.md necessarily changes
its blob away from the T02-admitted a12fc755…, so the shared
test_v49_gate_currentness.py `read_only_rebound` subtest is expected RED at
this PR HEAD until a lawful bridge admits the exact T13 successor blob, and
the shared test_v49_conformance_suite.py gate-kernel blob rebind fails
mechanically with it; the preflighted support lane (#1015@6117229584,
precedent #1064) owns exactly those two files.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "standards" / "DEVELOPMENT_WORKFLOW.md"
TDS = ROOT / "standards" / "TASK_DECOMPOSITION_STANDARD.md"
MANIFEST = ROOT / "standard-manifest.json"

# ---------------------------------------------------------------------------
# section identity (headings are the section identity; tests slice by them)
# ---------------------------------------------------------------------------

ROLE_CONDUCT_HEADING = "### Role conduct trace：角色行为链（role-conduct trace）"
T01_FLOOR_HEADING = "### Effective-rule trace：pinned revision、跨 owner 合取与 provenance"
BLOCKER_HEADING = "## 5. Blocker Propagation"
T02_HEADING = "### 2.3 Risk-intake：受影响源实质性清单（affected-source materiality inventory）"
LIFECYCLE_HEADING = "## 3. 生命周期"
TDS_ROLE_HEADING = "### 2.1 Role / Task-entry requirements"
TDS_SEC2_HEADING = "## 2. Required durable Task facts"
TDS_SEC3_HEADING = "## 3. Primary concern boundary"

# Owner sections preserved verbatim (byte-exact at the v4.11 base); the T13
# section appends strictly AFTER the T01 floor span, and the TDS §2.1 section
# appends strictly AFTER the §2 durable-facts span.
T02_SECTION_VERBATIM = (
    '### 2.3 Risk-intake：受影响源实质性清单（affected-source materiality inventory）\n'
    '\n'
    'Intake 阶段 MUST 为每个 changed subject 产出一份受影响源实质性清单（`MATERIALITY_INVENTORY` risk trace）：对每个 actually inspected 的 changed source，按实际 diff 检视记录 per-source epistemic state。清单消费 §4 “Effective-rule trace” floor 的解析语义 **read-only**，只向其供给 observed facts；它不是第二 applicability 权威，不新增 gate state、workflow state、共享 schema 或第二套方法论。\n'
    '\n'
    'material class 是从实际 diff 检视中观察到的实质效果事实（permission / API / security / migration / deployment / external-effect 等），不是新枚举权威。每条 inventory record MUST 绑定：\n'
    '\n'
    '```text\n'
    'subject\n'
    'source_path\n'
    'inspected_ref（实际检视所依据的 immutable blob/HEAD ref）\n'
    'material_class_observed\n'
    'epistemic_state ∈ {PRESENT, ABSENT_WITH_INSPECTED_SCOPE, UNKNOWN}\n'
    'currentness\n'
    'required_gate_ref（自 §4 floor 继承，只读）\n'
    'resolution_route\n'
    '```\n'
    '\n'
    'epistemic state 是关于检视本身的 epistemic fact，不是新增 gate 枚举；gate 状态仍使用既有枚举，未满足时保持 `NOT_RUN` / `BLOCKED`：\n'
    '\n'
    '- `PRESENT`：在该 source 上实际观察到某 material class，MUST 附 inspection ref。\n'
    '- `ABSENT_WITH_INSPECTED_SCOPE`：在明确陈述的 inspected scope 内实际检视并确认该 class 真实缺失，MUST 附 inspected scope ref；没有 affirmative inspection evidence 时 MUST NOT 使用。\n'
    '- `UNKNOWN`：未实际检视、不可检视或 currentness 未证明，是未检视 source 的默认状态。“未检视” MUST NOT 与“已检视且缺失”混同。\n'
    '\n'
    'currentness 绑定：`inspected_ref` MUST 解析到 candidate tree/HEAD 中该 source 的实际 blob；ref 缺失、过期（不匹配 candidate）或与 authority 矛盾时，该记录 MUST 降级为 `UNKNOWN` 并要求重新检视；MUST NOT 推断 currentness，MUST NOT 把过期的 ABSENT 提升为当前缺失。\n'
    '\n'
    '缺失或乐观的 job label 从来不是安全捷径：由 independently inspected material fact 导出的义务不因删除或缺失 label 而消失（§4 floor）。diff 检视显示 material change 而声明 label 未覆盖或缺失、source 未实际检视时，MUST fail closed `BLOCKED` 并按 §4 “Applicability UNKNOWN 或矛盾：fail closed” 路由到 owning authority；MUST NOT 记为 `NOT_APPLICABLE`，MUST NOT 产生 `PASS`。label 与检视矛盾时按 `CONFLICT` 路由 owning authority 并保留历史事实。\n'
    '\n'
    '清单只供给观察事实：MUST NOT 用清单解除、降级或豁免 floor 或更高 authority 已要求的任何 gate；MUST NOT 以清单为据铸造新 gate/枚举。全部 changed source 检视为当前缺失且无 `PRESENT` class 时，既有 proportionate/快速路径（§7）保持不变，MUST NOT 因清单强加 speculative 的全版本记录。集中式 trace schema / manifest / verifier 投影归其既有 canonical owner；投影缺失时相关集成保持 `NOT_RUN` / `BLOCKED`，additive 提案按既有路由升级，本节不铸造 shadow schema/template/manifest 字段。\n'
    '\n'
)
T01_FLOOR_VERBATIM = (
    '### Effective-rule trace：pinned revision、跨 owner 合取与 provenance\n'
    '\n'
    'Required gate 的 effective rule 在 exact subject 上解析时，MUST 产生可审计的最小 `EFFECTIVE_RULE_TRACE` 投影，至少绑定：\n'
    '\n'
    '```text\n'
    'standard_revision（immutable pin）\n'
    'owner_ref/blob（义务所属 canonical owner 与 authority tier/ref）\n'
    'exact_subject\n'
    'adoption / archetype / actor_role\n'
    'declared_jobs（multi-label set）\n'
    'observed_fact / observation ref / freshness\n'
    'applicability_reason\n'
    'obligation / required_evidence / freshness\n'
    'resolution\n'
    'decision_owner / ref\n'
    '```\n'
    '\n'
    '解析规则：\n'
    '\n'
    '- 先在同一 concern 内按本节 authority chain 解析 precedence（允许合法 strengthening，禁止削弱），再跨所有 applicable owner/concern 取逻辑 AND；任一 owner 的 required gate 在合取中保持 required，一个 owner 内合法的 `NOT_APPLICABLE` 不解除其它 owner 的 gate。\n'
    '- job label、profile、adoption level 或更低 authority 的 override 只是 applicability 的辅助证据；由 independently inspected material fact（permission/security/migration/deploy/external-effect）导出的义务不因删除 label 而消失。适用性 UNKNOWN 或矛盾时按上一节 fail closed。\n'
    '- observation 缺失、来自过期 HEAD 或与 authority 矛盾时，事实记为 `UNKNOWN`，MUST NOT 记为已检视的 `ABSENT_WITH_INSPECTED_SCOPE`，MUST NOT 产生 `PASS`；`PRESENT` / `ABSENT_WITH_INSPECTED_SCOPE` / `UNKNOWN` 是 epistemic fact，不是新增 gate state，gate 状态仍使用既有枚举，未满足时保持 `NOT_RUN` / `BLOCKED`。\n'
    '- 本节不新增 gate state、workflow state、共享 schema、模板或第二套方法论；集中式 trace schema / manifest / verifier 投影归其既有 canonical owner，该投影缺失时相关集成保持 `NOT_RUN` / `BLOCKED` 并按既有路由升级。\n'
    '\n'
)
TDS_SEC2_VERBATIM = (
    '## 2. Required durable Task facts\n'
    '\n'
    'Every material execution Task MUST make these facts recoverable from durable planning authority:\n'
    '\n'
    '```text\n'
    'Task identity\n'
    'primary concern / goal\n'
    'Frozen/Product/Architecture inputs\n'
    'expected output\n'
    'allowed write-set / ownership\n'
    'forbidden scope\n'
    'acceptance criteria\n'
    'required gates\n'
    'Validation scope / owner\n'
    'Review policy\n'
    'integration / merge target\n'
    'dependencies\n'
    'L3 / implementation reference when required\n'
    'agent freedom / executor constraints\n'
    'failure / escalation handling\n'
    '```\n'
    '\n'
    'Issue text may point to a Frozen Task Pack rather than duplicate the whole contract. The durable authority must still exist and be current.\n'
    '\n'
    'A Task is **Agent-dispatchable** only when a qualified Agent can resolve identity, allowed scope, required gates and completion from these durable facts plus the frozen authority they reference, without hidden conversation or chat context. A decomposition that depends on undocumented side-channel context to execute, validate or review correctly is not a valid Task boundary.\n'
    '\n'
)

# Preexisting Workflow heading sequence (relative order guard; T13 adds
# exactly one heading between the T01 floor and §5 and touches no other).
PREEXISTING_WORKFLOW_HEADINGS = (
    "# Development Workflow",
    "## 1. 目标",
    "## 2. Intake 时先选择 Integration Mode",
    "### 2.1 Version Branch Mode",
    "### 2.2 Trunk / Fast Path",
    "## 3. 生命周期",
    "### Stage 0 — Intake / Baseline",
    "### Stage 1 — Product / Scope",
    "#### Stage 1 Checkpoint",
    "### Stage 2 — Architecture / Task Definition",
    "#### Stage 2.1 — Architecture UNKNOWN disposition",
    "#### Stage 2.2 — Architecture Research Demo / Spike（按需）",
    "#### Stage 2.3 — L2 Architecture Freeze",
    "#### Stage 2.4 — Task DAG",
    "#### Stage 2 Checkpoint",
    "#### Stage 2.5 — Execution DAG Materialization",
    "### Stage 2.6 — Review Policy Selection",
    "### Stage 3 — Implementation Concerns",
    "#### 3.1 Optional Stacked PR",
    "### Stage 4 — Task Candidate / Minimal CI / Required Validation / Optional Review",
    "#### 4.1 Candidate Preparation + Cheap / Scoped Validation",
    "#### 4.2 PR + Minimal CI Before Expensive Validation",
    "#### 4.3 Expensive / Real-host Task-owned Validation",
    "#### 4.4 Independent Review（按需）",
    "#### 4.5 Task Merge Readiness",
    "#### 4.6 Local Agent Handoff（按需）",
    "### Stage 5 — Integrated Baseline / Candidate Preparation",
    "### Stage 6 — Candidate Freeze / Hidden Validation / Closure",
    "### Stage 7 — Version PR / Release Baseline / Optional Tag / Release",
    "## 4. Gate Authority",
    "### Gate applicability 与合法来源",
    "### Applicability UNKNOWN 或矛盾：fail closed",
    "### Repair routing：root defect class",
    "### Non-converging repair：escalation，而非 universal retry cap",
    "### Effective-rule trace：pinned revision、跨 owner 合取与 provenance",
    "### Role conduct trace：角色行为链（role-conduct trace）",
    "## 5. Blocker Propagation",
    "## 6. Stage Checkpoint Push",
    "## 7. 快速路径",
    "## 8. ADS Evolution Feedback / Intake",
    "### 8.1 Observation classification and deterministic route",
    "### 8.2 Promotion boundary: ordinary ADS governance only",
    "### 8.3 Privacy / publication classification",
)

# Preexisting Task Decomposition heading sequence (T13 adds exactly one
# ### 2.1 subsection between §2 and §3; no renumbering anywhere).
PREEXISTING_TDS_HEADINGS = (
    "# Task Decomposition Standard",
    "## 1. Purpose",
    "## 2. Required durable Task facts",
    "### 2.1 Role / Task-entry requirements",
    "## 3. Primary concern boundary",
    "## 4. Safe parallelism",
    "## 5. Atomicity and shared invariants",
    "## 6. Dependencies",
    "## 7. Stacked PR boundary",
    "## 8. Central wiring pattern",
    "## 9. Task lanes are advisory",
    "## 10. Anti-patterns",
    "### 10.1 File-count split",
    "### 10.2 Giant mixed-authority Task",
    "### 10.3 Fake parallelism",
    "### 10.4 Readiness fabrication",
    "## 11. Validation / Review decomposition",
    "## 12. Fast Path",
    "## 13. Decomposition decision prompts",
    "## 14. Failure handling",
)

# Role-conduct owner clauses this task adds (exact normative sentences).
ROLE_CONDUCT_CLAUSES = (
    "conduct 解析 MUST 产出一份角色行为链（`ROLE_CONDUCT_TRACE`）",
    "从 durable authority（而非 hidden conversation / chat context）解析 Input → Allowed acts → Required evidence → Handoff/Exit",
    "actor",
    "transport",
    "role/job/profile/archetype",
    "legality_ref",
    "input_refs",
    "allowed_acts_scope（write set）",
    "required_evidence[]（per material class，含 freshness）",
    "refusal_grounds",
    "exit_or_handoff_condition",
    "resolution_route",
    "本节消费 §4 “Effective-rule trace” floor 与 §2.3 “Risk-intake” inventory 的解析语义 **read-only**",
    "它不是第二 applicability 权威，不新增 gate state、workflow state、共享 schema、模板或第二套方法论",
    "role/job/profile/archetype MUST 自 durable authority 解析出 `legality_ref`",
    "unsupported / undeclared 的 role、archetype 或 actor class 没有默认权力，MUST fail closed（`GAP/UNVERIFIED` / `BLOCKED`）",
    "按 §4 “Applicability UNKNOWN 或矛盾：fail closed” 路由 owning authority",
    "`legality_ref` 缺失或不可解析时同样 fail closed",
    "WEB actor 的 source-bound authenticated GitHub remote readback（exact repository/ref/SHA/tree/read timestamp/actor）只是 scoped source metadata，不是 host 证据",
    "WEB actor 完成其 allowed acts 后 MUST 以 handoff 结束并要求 LOCAL/host owner 供给 host/build/runtime 证据",
    "MUST NOT 断言其无法观察的 checkout、build/run 结果、side-effect 或 future-freshness 事实",
    "MUST NOT 由此铸造 Validation `PASS`",
    "WEB/LOCAL provenance 冲突按 `CONFLICT` 路由 owning authority 并保留历史事实",
    "Builder 不能自我满足 `review:required`",
    "exit 只能由该 Builder 未产出的 genuinely independent accepted current Review admission 满足（Reviewer 是 distinct actor，self-review 按 `CONFLICT` 拒绝）",
    "合法的 `review:recommended` / `review:not-required`（按 Stage 2.6 与 `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §6 解析）保持 proportionate",
    "MUST NOT 被强加 fabricated 的 universal Fresh Review 前置 gate",
    "Review Policy 解析 UNKNOWN 或矛盾时按 Stage 2.6 fail closed",
    "低风险 A0（如 docs-only）conduct 保持 proportionate——不施加 speculative 的 research ceremony 或 blanket gates",
    "但 T01 floor 与 T02 inventory 的 applicable duties 不因此消失，更低 authority 的 profile/override 不削弱 floor（上一节 “Effective-rule trace” 非削弱条款）",
    "required_evidence 缺失、过期（stale freshness / HEAD）或与 T02 inventory 的 `PRESENT` class 不符时，exit/handoff MUST 被拒绝",
    "MUST NOT 记 `NOT_APPLICABLE`，MUST NOT 产生 `PASS`",
    "有限 declared role × transport × job-set × profile/archetype denominator 上的每个 material combination MUST 解析出完整 trace 或显式 `GAP/UNVERIFIED` 处置",
    "允许 equivalence-class 采样覆盖，但未证明的 material combination MUST NOT 被报告为 complete，也不得省略或记 `NOT_APPLICABLE`",
    "unsupported role/class 或 `legality_ref` 缺失 → `GAP/UNVERIFIED` / `BLOCKED`",
    "required evidence 缺失或过期 → exit denied",
    "WEB/LOCAL provenance 冲突或 self-review → `CONFLICT` / 拒绝",
    "集中式 trace schema / manifest / verifier 投影缺失 → 相关集成保持 `NOT_RUN` / `BLOCKED`，additive 提案按既有路由升级",
    "Frozen Product/L2 冲突 → STOP/escalate，不自行修复",
    "本节不铸造第二 gate authority、Dispatch/Claim authority、human-decision authority、merge authority 或 Task-Learning authority",
    "本节不铸造 shadow schema/template/manifest 字段",
)

# TDS role/Task-entry clauses this task adds (exact normative sentences).
TDS_ROLE_ENTRY_CLAUSES = (
    "A material execution Task MUST resolve, before dispatch, its acting role denominator from durable authority",
    "the declared role/job/profile/archetype that acts on the Task, the transport (WEB/LOCAL) it acts through, and a legality reference resolving to that durable authority",
    "Every material actor-subject resolves one conduct trace per the Workflow role-conduct section",
    "consuming the effective-rule floor and the affected-source materiality inventory read-only",
    "A Task entry whose material role/job/profile/archetype denominator cannot be resolved from these durable facts is not agent-dispatchable and stays `GAP/UNVERIFIED`, never READY by default",
    "Incomplete material role/job/profile coverage MUST NOT be reported complete",
    "an unsupported role/archetype/class has no default powers and fails closed",
    "These entry requirements create no new gate authority, dispatch/claim authority, merge authority or Task-Learning authority",
    "belongs to its existing canonical owner",
    "affected integration stays `NOT_RUN` / `BLOCKED` and additive proposals follow the existing routing",
)

# ---------------------------------------------------------------------------
# contract vocabulary (Pack §3/§4; existing gate enum is preserved)
# ---------------------------------------------------------------------------

TRANSPORTS = frozenset({"WEB", "LOCAL"})

# Declared actor denominator: the Builder/Reviewer/Validator engineering
# roles plus the Product/Architect/Planner/Controller actors already
# described in the Frozen PRD actor model (fixture-level reading of the
# pack; not a new authority).
DECLARED_ROLES = frozenset(
    {"builder", "reviewer", "validator", "planner", "architect", "product", "controller"}
)

ARCHETYPES = frozenset({"A0", "A1", "A2", "A3", "A4"})

EPISTEMIC_STATES = frozenset({"PRESENT", "ABSENT_WITH_INSPECTED_SCOPE", "UNKNOWN"})

CANONICAL_GATE_STATES = frozenset({"PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE"})

REVIEW_POLICIES = frozenset({"required", "recommended", "not-required"})

# Material classes / floor gates / job closure: T01+T02 vocabulary consumed
# read-only (identical mapping to the T02 focused test's floor projection).
MATERIAL_CLASSES = frozenset(
    {"permission", "api", "security", "migration", "deployment", "external_effect"}
)

FLOOR_GATE_BY_CLASS = {
    "permission": "floor:gate-material-permission",
    "api": "floor:gate-material-api",
    "security": "floor:gate-material-security",
    "migration": "floor:gate-material-migration",
    "deployment": "floor:gate-material-deployment",
    "external_effect": "floor:gate-material-external-effect",
}

JOB_GATE_CLOSURE = {
    "J_PERMISSION_REVIEW": frozenset({"floor:gate-material-permission"}),
    "J_API_COMPATIBILITY": frozenset({"floor:gate-material-api"}),
    "J_SECURITY_REVIEW": frozenset({"floor:gate-material-security"}),
    "J_MIGRATION_PLAN": frozenset({"floor:gate-material-migration"}),
    "J_DEPLOY_PLAN": frozenset({"floor:gate-material-deployment"}),
    "J_EXTERNAL_EFFECT_HANDOFF": frozenset({"floor:gate-material-external-effect"}),
    "J02_DOCS_LOW_RISK": frozenset(),
}

# Decision outcomes of the conduct model (test-level routing vocabulary; the
# standard mints no new gate/workflow state).
DECISIONS = frozenset(
    {
        "CONDUCT_TRACE_COMPLETE",
        "HANDOFF_REQUIRED_TO_LOCAL",
        "EXIT_DENIED",
        "BLOCKED",
    }
)

LEGALITY_ROUTES = frozenset(
    {
        "unsupported_role_fail_closed",
        "unsupported_archetype_fail_closed",
        "unsupported_transport_fail_closed",
        "unsupported_class_fail_closed",
        "missing_legality_ref",
        "review_policy_unresolved_fail_closed",
    }
)

BLOB_HEX = re.compile(r"^[0-9a-f]{64}$")

# Deterministic fixture pins (64-hex shaped, distinct per surface).
HEAD_A = "a1" * 32
BLOB_AUTHZ = "b1" * 32
BLOB_ROUTES = "b2" * 32
BLOB_DOCS = "b4" * 32
BLOB_STALE = "c9" * 32
LEGALITY_BUILDER = "d1" * 32
LEGALITY_VALIDATOR = "d2" * 32
ADMISSION_REF = "e1" * 32
REMOTE_READBACK_REF = "f1" * 32

# ---------------------------------------------------------------------------
# T01 floor (read-only consumption) + T13 conduct decision model
# ---------------------------------------------------------------------------


def floor_required_gates(declared_jobs, inspected_facts):
    """T01 floor semantics, read-only: declared job-label closure AND
    independently inspected material facts. Job labels are auxiliary
    evidence; a fact-derived required gate never disappears because a label
    is missing or removed. Unknown labels fail closed (T01's concern, not
    re-implemented here)."""
    gates = set()
    for job in declared_jobs:
        if job not in JOB_GATE_CLOSURE:
            raise ValueError(f"unknown job label fails closed at the floor: {job!r}")
        gates |= JOB_GATE_CLOSURE[job]
    for cls in inspected_facts:
        if cls not in MATERIAL_CLASSES:
            raise ValueError(f"unowned material class fails closed: {cls!r}")
        gates.add(FLOOR_GATE_BY_CLASS[cls])
    return frozenset(gates)


def _inventory_record(source_path, cls, state, currentness, inspected_ref):
    return {
        "source_path": source_path,
        "material_class": cls,
        "epistemic_state": state,
        "currentness": currentness,
        "inspected_ref": inspected_ref,
    }


def conduct_trace(fixture):
    """Resolve ONE ROLE_CONDUCT_TRACE for one actor-subject (Pack §4).

    Single resolution path: the required-gate set is delegated to
    floor_required_gates() over the T02 inventory's PRESENT/CURRENT facts;
    the trace attaches binding, evidence resolution and routing only. It
    never re-derives gates and never mints a gate state.
    """
    refusal = []  # blocking fail-closed routes
    rejected = []  # recorded rejected attempts (non-blocking)

    trace = {
        "actor": fixture["actor"],
        "transport": fixture["transport"],
        "role": fixture["role"],
        "job_set": frozenset(fixture["job_set"]),
        "profile": fixture["profile"],
        "archetype": fixture["archetype"],
        "legality_ref": fixture.get("legality_ref", ""),
        "input_refs": dict(fixture["input_refs"]),
        "allowed_acts_scope": tuple(fixture["allowed_acts_scope"]),
        "required_evidence": [],
        "refusal_grounds": (),
        "exit_or_handoff_condition": "exit_denied",
        "resolution_route": "conduct_chain_unresolved",
        "required_gate_set": frozenset(),
        "decision": "BLOCKED",
        "disposition": "GAP/UNVERIFIED",
        "rejected_attempts": (),
        "shared_projection": "DEFERRED_TO_T11",
        "new_gate_states_minted": frozenset(),
    }

    # 1. legality: unsupported denominator or missing legality fails closed.
    if fixture["role"] not in DECLARED_ROLES:
        refusal.append("unsupported_role_fail_closed")
    if fixture["archetype"] not in ARCHETYPES:
        refusal.append("unsupported_archetype_fail_closed")
    if fixture["transport"] not in TRANSPORTS:
        refusal.append("unsupported_transport_fail_closed")
    if any(job not in JOB_GATE_CLOSURE for job in fixture["job_set"]):
        refusal.append("unsupported_class_fail_closed")
    if not BLOB_HEX.match(fixture.get("legality_ref", "") or ""):
        refusal.append("missing_legality_ref")
    policy = fixture.get("review_policy")
    if fixture["role"] == "builder" and policy not in REVIEW_POLICIES:
        refusal.append("review_policy_unresolved_fail_closed")

    # 2. consume T02 inventory facts (read-only): only PRESENT+CURRENT
    # observations enter the floor conjunction.
    present_classes = set()
    for rec in fixture["inventory"]:
        if rec["epistemic_state"] == "PRESENT" and rec["currentness"] == "CURRENT":
            present_classes.add(rec["material_class"])

    # 3. consume the T01 floor (single resolution path, read-only). An
    # unsupported job class already failed closed above; the floor function
    # itself raises on unknown labels (T01 semantics) and is not invoked.
    if "unsupported_class_fail_closed" in refusal:
        required = frozenset()
    else:
        required = floor_required_gates(frozenset(fixture["job_set"]), present_classes)
    trace["required_gate_set"] = required

    # 4. floor non-weakening: a lower-authority profile override cannot
    # demote a floor-required gate; the attempt is rejected and recorded.
    for gate, action in sorted((fixture.get("profile_override") or {}).items()):
        if action == "demote" and gate in required:
            rejected.append("floor_weakening_override_rejected")

    # 5. required evidence resolution: per material class, currentness-bound
    # and subject-bound; missing/stale/unbound evidence denies exit.
    input_blobs = set(fixture["input_refs"].values())
    for gate in sorted(required):
        matches = [e for e in fixture["evidence"] if e.get("gate") == gate]
        if not matches:
            refusal.append("required_evidence_missing")
            continue
        current = [e for e in matches if e.get("currentness") == "CURRENT"]
        if not current:
            refusal.append("stale_evidence_ref")
            continue
        ev = current[0]
        if not BLOB_HEX.match(ev.get("ref", "") or "") or ev["ref"] not in input_blobs:
            refusal.append("evidence_not_subject_bound")
            continue
        trace["required_evidence"].append(
            {"gate": gate, "currentness": "CURRENT", "ref": ev["ref"]}
        )

    # 6. WEB/LOCAL provenance split (no invented powers).
    if fixture["transport"] == "WEB":
        host_claims = list(fixture.get("web_host_claims") or [])
        host_evidence = [e for e in fixture["evidence"] if e.get("kind") == "host_evidence"]
        if host_claims or host_evidence:
            refusal.append("web_host_evidence_rejected_handoff_required")
        readbacks = [e for e in fixture["evidence"] if e.get("kind") == "remote_readback"]
        if readbacks:
            # Source-bound remote readback is scoped source metadata only;
            # provenance is recorded, never promoted to host evidence.
            trace["input_refs"]["remote_readback"] = readbacks[0]["ref"]

    # 7. review proportionality (builder exit only).
    if fixture["role"] == "builder" and policy in REVIEW_POLICIES:
        admission = fixture.get("independent_review_admission")
        if policy == "required":
            if admission is None:
                refusal.append("review_admission_required")
            elif admission.get("reviewer") == fixture["actor"] or admission.get("self_review"):
                refusal.append("self_review_rejected")
            elif not BLOB_HEX.match(admission.get("admission_ref", "") or ""):
                refusal.append("review_admission_required")
        else:
            # lawful recommended/not-required: no hard Fresh Review
            # prerequisite; a fabricated universal gate is not honored.
            if fixture.get("fabricated_fresh_gate"):
                rejected.append("unauthorized_fresh_gate_rejected")

    # 8. decision (fail-closed routing).
    if refusal:
        trace["decision"] = (
            "BLOCKED" if any(r in LEGALITY_ROUTES for r in refusal) else "EXIT_DENIED"
        )
        trace["disposition"] = "GAP/UNVERIFIED"
        trace["refusal_grounds"] = tuple(sorted(refusal))
        trace["exit_or_handoff_condition"] = "exit_denied_refusal_grounds_bound"
        trace["resolution_route"] = "owner_routed_fail_closed"
    elif fixture["transport"] == "WEB":
        trace["decision"] = "HANDOFF_REQUIRED_TO_LOCAL"
        trace["disposition"] = "HANDOFF_LAWFUL"
        trace["exit_or_handoff_condition"] = (
            "handoff: LOCAL/host owner supplies host/build/runtime evidence"
        )
        trace["resolution_route"] = "web_handoff_resolved"
    else:
        trace["decision"] = "CONDUCT_TRACE_COMPLETE"
        trace["disposition"] = "COMPLETE"
        trace["exit_or_handoff_condition"] = (
            "exit: required evidence current + review admission per resolved policy"
        )
        trace["resolution_route"] = "conduct_chain_resolved"

    trace["rejected_attempts"] = tuple(sorted(rejected))
    return trace


def waive_required_gate(trace, gate):
    """N05 half: the trace output can never waive/demote a floor-required
    gate; the higher-authority requirement persists unchanged."""
    return {
        "rejected": True,
        "reason": "the trace binds and routes only; the gate set is owned by the §4 floor",
        "required_gate_set": trace["required_gate_set"],
        "gate": gate,
    }


def is_material_combo(combo):
    """A declared denominator combination is material when any non-low-risk
    job obligation applies (J02 docs-only is the proportional A0 lane)."""
    return any(job != "J02_DOCS_LOW_RISK" for job in combo["job_set"])


def coverage_ledger(combos):
    """P01/N06: equivalence-coverage ledger over the finite declared
    role × transport × job-set × profile/archetype denominator. Every
    material combination stays recorded: COVERED with a direct or
    equivalence-class proof, or GAP/UNVERIFIED with an owner-routed
    disposition — never omitted, never NOT_APPLICABLE."""
    entries = []
    for combo in combos:
        if not is_material_combo(combo):
            continue
        covered_by = combo.get("covered_by")
        covered = covered_by in ("direct", "equivalence_class")
        entries.append(
            {
                "role": combo["role"],
                "transport": combo["transport"],
                "job_set": frozenset(combo["job_set"]),
                "archetype": combo["archetype"],
                "status": "COVERED" if covered else "GAP/UNVERIFIED",
                "proof": covered_by,
                "resolution_route": (
                    "equivalence_class_coverage"
                    if covered
                    else "coverage_gap_owner_routed"
                ),
            }
        )
    return {
        "entries": entries,
        "complete": bool(entries) and all(e["status"] == "COVERED" for e in entries),
        "uncovered": [e for e in entries if e["status"] != "COVERED"],
        "not_applicable_used": False,
    }


def register_central_projection(target):
    """Shared projection: conduct traces have no central template/schema/
    manifest route in this task; additive proposals are routed to the
    designated wiring task unwritten (DEFERRED_TO_T11)."""
    return {"routed": "DEFERRED_TO_T11", "written": False, "target": target}


def dump(result) -> str:
    """JSON view of a model result (frozensets become sorted lists)."""
    return json.dumps(
        result,
        sort_keys=True,
        default=lambda o: sorted(o) if isinstance(o, (set, frozenset)) else str(o),
    )


def gate_state_vocabulary(result) -> set:
    """Every gate-shaped token the model can emit."""
    tokens = {result["decision"], result["shared_projection"], result["disposition"]}
    tokens.update(result["refusal_grounds"])
    tokens.update(result["rejected_attempts"])
    for ev in result["required_evidence"]:
        tokens.add(ev["currentness"])
    return tokens


ALLOWED_MODEL_VOCABULARY = (
    EPISTEMIC_STATES
    | CANONICAL_GATE_STATES
    | DECISIONS
    | {"GAP/UNVERIFIED", "COMPLETE", "HANDOFF_LAWFUL", "DEFERRED_TO_T11", "CONFLICT", "CURRENT"}
    | {
        "conduct_chain_resolved",
        "web_handoff_resolved",
        "conduct_chain_unresolved",
        "owner_routed_fail_closed",
        "unsupported_role_fail_closed",
        "unsupported_archetype_fail_closed",
        "unsupported_transport_fail_closed",
        "unsupported_class_fail_closed",
        "missing_legality_ref",
        "review_policy_unresolved_fail_closed",
        "web_host_evidence_rejected_handoff_required",
        "self_review_rejected",
        "review_admission_required",
        "unauthorized_fresh_gate_rejected",
        "required_evidence_missing",
        "stale_evidence_ref",
        "evidence_not_subject_bound",
        "floor_weakening_override_rejected",
        "coverage_gap_owner_routed",
        "equivalence_class_coverage",
    }
)

# ---------------------------------------------------------------------------
# fixtures (deterministic; exact-subject ground truth vs actor input)
# ---------------------------------------------------------------------------


def builder_local_fixture():
    """P01/P03 base: LOCAL builder, one PRESENT permission class, distinct
    independent reviewer admission, authority-resolved review:required."""
    return {
        "actor": "builder-1",
        "transport": "LOCAL",
        "role": "builder",
        "job_set": {"J_PERMISSION_REVIEW"},
        "profile": "p-engineering",
        "archetype": "A1",
        "legality_ref": LEGALITY_BUILDER,
        "input_refs": {"src/authz.py": BLOB_AUTHZ},
        "allowed_acts_scope": ("src/authz.py",),
        "inventory": [
            _inventory_record("src/authz.py", "permission", "PRESENT", "CURRENT", BLOB_AUTHZ)
        ],
        "evidence": [
            {"gate": "floor:gate-material-permission", "currentness": "CURRENT", "ref": BLOB_AUTHZ}
        ],
        "review_policy": "required",
        "independent_review_admission": {
            "reviewer": "reviewer-1",
            "admission_ref": ADMISSION_REF,
        },
    }


def web_validator_fixture():
    """P02 base: WEB validator completes allowed acts (source-bound remote
    readback) and hands off for LOCAL/host evidence."""
    return {
        "actor": "validator-web",
        "transport": "WEB",
        "role": "validator",
        "job_set": {"J02_DOCS_LOW_RISK"},
        "profile": "p-validation",
        "archetype": "A1",
        "legality_ref": LEGALITY_VALIDATOR,
        "input_refs": {"docs/guide.md": BLOB_DOCS},
        "allowed_acts_scope": ("docs/guide.md",),
        "inventory": [
            _inventory_record(
                "docs/guide.md", None, "ABSENT_WITH_INSPECTED_SCOPE", "CURRENT", BLOB_DOCS
            )
        ],
        "evidence": [{"gate": None, "kind": "remote_readback", "currentness": "CURRENT", "ref": REMOTE_READBACK_REF}],
        "review_policy": "not-required",
    }


def docs_a0_fixture(review_policy="not-required"):
    """P04 base: low-risk A0 docs-only LOCAL builder, all classes inspected
    absent, authority-resolved proportional policy."""
    fixture = builder_local_fixture()
    fixture.update(
        {
            "actor": "builder-docs",
            "role": "builder",
            "job_set": {"J02_DOCS_LOW_RISK"},
            "profile": "p-docs",
            "archetype": "A0",
            "legality_ref": LEGALITY_BUILDER,
            "input_refs": {"docs/guide.md": BLOB_DOCS},
            "allowed_acts_scope": ("docs/guide.md",),
            "inventory": [
                _inventory_record(
                    "docs/guide.md", None, "ABSENT_WITH_INSPECTED_SCOPE", "CURRENT", BLOB_DOCS
                )
            ],
            "evidence": [],
            "review_policy": review_policy,
            "independent_review_admission": None,
        }
    )
    return fixture


# ---------------------------------------------------------------------------
# repository helpers
# ---------------------------------------------------------------------------


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def tds_text() -> str:
    return TDS.read_text(encoding="utf-8")


def role_conduct_section() -> str:
    text = workflow_text()
    start = text.index(ROLE_CONDUCT_HEADING)
    end = text.index(BLOCKER_HEADING, start + len(ROLE_CONDUCT_HEADING))
    return text[start:end]


def tds_role_entry_section() -> str:
    text = tds_text()
    start = text.index(TDS_ROLE_HEADING)
    end = text.index(TDS_SEC3_HEADING, start + len(TDS_ROLE_HEADING))
    return text[start:end]


def headings(text: str) -> list:
    return [m.group(0).strip() for m in re.finditer(r"^#{1,6} .+$", text, re.M)]


def recursive_keys(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield key
            yield from recursive_keys(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from recursive_keys(item)


# ---------------------------------------------------------------------------
# Layer 1: section-scoped textual contracts + verbatim owner-span guards
# ---------------------------------------------------------------------------


class RoleConductSectionPlacementTests(unittest.TestCase):
    def test_section_exists_exactly_once_after_t01_floor_before_blocker(self):
        text = workflow_text()
        self.assertEqual(text.count(ROLE_CONDUCT_HEADING), 1)
        t01_start = text.index(T01_FLOOR_HEADING)
        start = text.index(ROLE_CONDUCT_HEADING)
        end = text.index(BLOCKER_HEADING, start)
        self.assertLess(t01_start, start)
        self.assertLess(start, end)
        # The T01 floor span is byte-identical and abuts the new section:
        # nothing was rewritten inside the T01 owner subsection.
        self.assertEqual(text[t01_start:start], T01_FLOOR_VERBATIM)
        # Nothing but the T13 section lives between its heading and §5.
        between = text[start:end]
        self.assertNotIn("\n### ", between.replace(ROLE_CONDUCT_HEADING, "", 1))

    def test_t02_section_stays_byte_verbatim_and_24_numbering_never_appears(self):
        text = workflow_text()
        t02_start = text.index(T02_HEADING)
        end = text.index(LIFECYCLE_HEADING, t02_start)
        self.assertEqual(text[t02_start:end], T02_SECTION_VERBATIM)
        # The frozen T02 boundary guard reserves the §2-tail→§3 span: this
        # tree lawfully keeps the literal "### 2.4" out of the whole document.
        self.assertNotIn("### 2.4", text)

    def test_preexisting_workflow_headings_keep_relative_order(self):
        found = headings(workflow_text())
        pos = 0
        for expected in PREEXISTING_WORKFLOW_HEADINGS:
            with self.subTest(heading=expected):
                while pos < len(found) and found[pos] != expected:
                    pos += 1
                self.assertLess(pos, len(found), f"heading missing/out of order: {expected}")
                pos += 1

    def test_tds_role_entry_section_adjacent_to_sec2_without_renumbering(self):
        text = tds_text()
        self.assertEqual(text.count(TDS_ROLE_HEADING), 1)
        sec2_start = text.index(TDS_SEC2_HEADING)
        start = text.index(TDS_ROLE_HEADING)
        end = text.index(TDS_SEC3_HEADING, start)
        self.assertLess(sec2_start, start)
        self.assertLess(start, end)
        # §2 Required durable Task facts stays byte-identical: the §2.1
        # section appends strictly AFTER it, before §3.
        self.assertEqual(text[sec2_start:start], TDS_SEC2_VERBATIM)
        self.assertNotIn("\n## 3.", text[start:end].replace(TDS_SEC3_HEADING, "", 1))

    def test_preexisting_tds_headings_keep_relative_order(self):
        found = headings(tds_text())
        pos = 0
        for expected in PREEXISTING_TDS_HEADINGS:
            with self.subTest(heading=expected):
                while pos < len(found) and found[pos] != expected:
                    pos += 1
                self.assertLess(pos, len(found), f"heading missing/out of order: {expected}")
                pos += 1


class RoleConductSectionContractTests(unittest.TestCase):
    """Pack §1/§4/§5/§6 normative clauses, bound sentence-by-sentence."""

    def test_all_owner_clauses_are_normative_in_section(self):
        section = role_conduct_section()
        for clause in ROLE_CONDUCT_CLAUSES:
            with self.subTest(clause=clause):
                self.assertIn(clause, section)

    def test_trace_consumes_t01_floor_and_t02_inventory_read_only(self):
        section = role_conduct_section()
        self.assertIn("**read-only**", section)
        self.assertIn("Effective-rule trace", section)
        self.assertIn("Risk-intake", section)
        self.assertIn("epistemic states（`PRESENT` / `ABSENT_WITH_INSPECTED_SCOPE` / `UNKNOWN`）", section)

    def test_no_new_gate_enum_is_minted_in_section(self):
        section = role_conduct_section()
        gate_tokens = set(
            re.findall(r"`(PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE)`", section)
        )
        self.assertTrue(gate_tokens)
        self.assertTrue(gate_tokens <= CANONICAL_GATE_STATES, gate_tokens - CANONICAL_GATE_STATES)
        # GAP/UNVERIFIED appears only as the pack's explicit disposition
        # vocabulary, never inside the canonical gate-token positions.
        self.assertIn("`GAP/UNVERIFIED`", section)

    def test_section_mints_no_machine_schema_and_no_new_authority(self):
        section = role_conduct_section()
        self.assertNotIn("schema_version", section)
        self.assertNotIn("```json", section)
        self.assertIn("本节不铸造 shadow schema/template/manifest 字段", section)
        self.assertIn(
            "本节不铸造第二 gate authority、Dispatch/Claim authority、human-decision authority、merge authority 或 Task-Learning authority",
            section,
        )
        self.assertIn("additive 提案按既有路由升级", section)


class TdsRoleEntryContractTests(unittest.TestCase):
    """Pack §4 TDS half: role/Task-entry requirements, bound sentence-by-sentence."""

    def test_all_owner_clauses_are_normative_in_tds_section(self):
        section = tds_role_entry_section()
        for clause in TDS_ROLE_ENTRY_CLAUSES:
            with self.subTest(clause=clause):
                self.assertIn(clause, section)

    def test_tds_section_mints_no_new_authority_and_no_machine_schema(self):
        section = tds_role_entry_section()
        self.assertNotIn("schema_version", section)
        self.assertNotIn("```json", section)
        self.assertIn("no new gate authority, dispatch/claim authority, merge authority or Task-Learning authority", section)


class NoShadowCentralProjectionTests(unittest.TestCase):
    """Real-tree half: no ROLE_CONDUCT_TRACE projection outside the owner
    sections. (Pre-T11 integration state; T11's own landing owns the central
    wiring and its conformance.)"""

    def test_manifest_carries_no_role_conduct_projection(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        shadowed = [k for k in recursive_keys(manifest) if "conduct" in str(k).lower()]
        self.assertEqual(shadowed, [])

    def test_no_role_conduct_schema_file_exists(self):
        schemas = ROOT / "schemas"
        shadowed = [p.name for p in schemas.glob("*") if "conduct" in p.name.lower()]
        self.assertEqual(shadowed, [])

    def test_no_role_conduct_projection_in_templates(self):
        shadowed = []
        for path in (ROOT / "templates").rglob("*"):
            if path.is_file() and "ROLE_CONDUCT_TRACE" in path.read_text(encoding="utf-8", errors="replace"):
                shadowed.append(str(path.relative_to(ROOT)))
        self.assertEqual(shadowed, [])


# ---------------------------------------------------------------------------
# Layer 2: fixture-driven decision oracles (Pack §3 P01-P04 / N01-N06)
# ---------------------------------------------------------------------------


class P01CompleteConductChainTests(unittest.TestCase):
    def test_p01_declared_denominator_resolves_complete_trace_bound_to_facts(self):
        fixture = builder_local_fixture()
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "CONDUCT_TRACE_COMPLETE")
        self.assertEqual(result["resolution_route"], "conduct_chain_resolved")
        # All ten contract fields bind (non-empty where applicable).
        for field in (
            "actor", "transport", "role", "job_set", "profile", "archetype",
            "legality_ref", "input_refs", "allowed_acts_scope", "required_evidence",
            "exit_or_handoff_condition", "resolution_route",
        ):
            with self.subTest(field=field):
                self.assertTrue(result[field])
        # A complete chain lawfully carries empty refusal grounds.
        self.assertEqual(result["refusal_grounds"], ())
        # Consumes T01/T02 facts: required set is EXACTLY the floor
        # resolution over declared jobs + T02 PRESENT observations (identity,
        # not re-derivation).
        self.assertEqual(
            result["required_gate_set"],
            floor_required_gates(frozenset(fixture["job_set"]), {"permission"}),
        )
        self.assertEqual(result["required_evidence"][0]["ref"], BLOB_AUTHZ)
        self.assertEqual(result["input_refs"]["src/authz.py"], BLOB_AUTHZ)
        dumped = dump(result)
        self.assertNotIn('"PASS"', dumped)
        self.assertNotIn('"NOT_APPLICABLE"', dumped)

    def test_p01_equivalence_coverage_ledger_proves_finite_denominator(self):
        combos = [
            {"role": "builder", "transport": "LOCAL", "job_set": {"J_PERMISSION_REVIEW"}, "archetype": "A1", "covered_by": "direct"},
            {"role": "reviewer", "transport": "LOCAL", "job_set": {"J_SECURITY_REVIEW"}, "archetype": "A2", "covered_by": "equivalence_class"},
            {"role": "validator", "transport": "WEB", "job_set": {"J_EXTERNAL_EFFECT_HANDOFF"}, "archetype": "A2", "covered_by": "direct"},
            {"role": "builder", "transport": "WEB", "job_set": {"J_API_COMPATIBILITY"}, "archetype": "A1", "covered_by": "equivalence_class"},
            {"role": "builder", "transport": "LOCAL", "job_set": {"J02_DOCS_LOW_RISK"}, "archetype": "A0", "covered_by": None},
        ]
        ledger = coverage_ledger(combos)
        self.assertTrue(ledger["complete"])
        self.assertEqual(ledger["uncovered"], [])
        self.assertFalse(ledger["not_applicable_used"])
        # Equivalence-class sampling (no Cartesian explosion): every material
        # combination carries an explicit proof kind.
        proofs = {e["proof"] for e in ledger["entries"]}
        self.assertEqual(proofs, {"direct", "equivalence_class"})
        self.assertEqual(
            len(ledger["entries"]),
            sum(1 for c in combos if is_material_combo(c)),
        )

    def test_p01_unproven_material_combination_stays_gap_never_omitted(self):
        combos = [
            {"role": "builder", "transport": "LOCAL", "job_set": {"J_PERMISSION_REVIEW"}, "archetype": "A1", "covered_by": "direct"},
            {"role": "reviewer", "transport": "WEB", "job_set": {"J_DEPLOY_PLAN"}, "archetype": "A2", "covered_by": None},
        ]
        ledger = coverage_ledger(combos)
        self.assertFalse(ledger["complete"])
        uncovered = ledger["uncovered"]
        self.assertEqual(len(uncovered), 1)
        self.assertEqual(uncovered[0]["status"], "GAP/UNVERIFIED")
        self.assertEqual(uncovered[0]["resolution_route"], "coverage_gap_owner_routed")
        self.assertFalse(ledger["not_applicable_used"])


class P02WebHandoffProvenanceTests(unittest.TestCase):
    def test_p02_web_chain_ends_in_lawful_handoff_without_host_assertions(self):
        fixture = web_validator_fixture()
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "HANDOFF_REQUIRED_TO_LOCAL")
        self.assertEqual(result["resolution_route"], "web_handoff_resolved")
        self.assertIn("handoff", result["exit_or_handoff_condition"])
        self.assertIn("LOCAL/host owner", result["exit_or_handoff_condition"])
        # Provenance recorded: source-bound remote readback stays source
        # metadata, no host/build/runtime fact is asserted anywhere.
        self.assertEqual(result["input_refs"]["remote_readback"], REMOTE_READBACK_REF)
        dumped = dump(result)
        # No evidence item (host or otherwise) is echoed as an asserted fact.
        self.assertNotIn('"kind"', dumped)
        self.assertNotIn('"PASS"', dumped)


class P03ReviewProportionalityTests(unittest.TestCase):
    def test_p03_review_required_satisfied_only_by_independent_admission(self):
        fixture = builder_local_fixture()
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "CONDUCT_TRACE_COMPLETE")
        self.assertEqual(fixture["independent_review_admission"]["reviewer"], "reviewer-1")
        self.assertNotEqual(fixture["independent_review_admission"]["reviewer"], fixture["actor"])

    def test_p03_lawful_recommended_skip_stays_proportional(self):
        fixture = docs_a0_fixture(review_policy="recommended")
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "CONDUCT_TRACE_COMPLETE")
        self.assertEqual(result["required_gate_set"], frozenset())
        self.assertNotIn("review_admission_required", result["refusal_grounds"])

    def test_p03_lawful_not_required_gains_no_fabricated_fresh_gate(self):
        fixture = docs_a0_fixture(review_policy="not-required")
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "CONDUCT_TRACE_COMPLETE")
        # Only floor-derived gates: no pseudo fresh-review gate was injected.
        self.assertEqual(
            result["required_gate_set"],
            floor_required_gates(frozenset(fixture["job_set"]), set()),
        )
        dumped = dump(result)
        self.assertNotIn("fresh-review", dumped)
        self.assertNotIn("FRESH_REVIEW", dumped)
        self.assertEqual(result["rejected_attempts"], ())


class P04A0ProportionalityWithDutiesTests(unittest.TestCase):
    def test_p04_a0_docs_only_stays_proportional_with_no_speculative_ceremony(self):
        result = conduct_trace(docs_a0_fixture())
        self.assertEqual(result["decision"], "CONDUCT_TRACE_COMPLETE")
        self.assertEqual(result["required_gate_set"], frozenset())
        self.assertEqual(result["required_evidence"], [])
        self.assertEqual(result["archetype"], "A0")

    def test_p04_a0_duties_from_floor_and_inventory_stay_binding(self):
        # Same A0 docs-only actor, but the T02 inventory observed a PRESENT
        # permission class: the proportional lane never waives floor duties.
        fixture = docs_a0_fixture()
        fixture["input_refs"] = {"docs/guide.md": BLOB_DOCS, "src/authz.py": BLOB_AUTHZ}
        fixture["inventory"] = [
            _inventory_record("docs/guide.md", None, "ABSENT_WITH_INSPECTED_SCOPE", "CURRENT", BLOB_DOCS),
            _inventory_record("src/authz.py", "permission", "PRESENT", "CURRENT", BLOB_AUTHZ),
        ]
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "EXIT_DENIED")
        self.assertIn("required_evidence_missing", result["refusal_grounds"])
        self.assertEqual(
            result["required_gate_set"],
            floor_required_gates(frozenset(fixture["job_set"]), {"permission"}),
        )


class N01FabricatedWebHostEvidenceTests(unittest.TestCase):
    def test_n01_web_host_claim_is_gap_no_exit_no_pass_minted(self):
        fixture = web_validator_fixture()
        fixture["role"] = "builder"
        fixture["legality_ref"] = LEGALITY_BUILDER
        fixture["review_policy"] = "required"
        fixture["independent_review_admission"] = {
            "reviewer": "reviewer-1",
            "admission_ref": ADMISSION_REF,
        }
        fixture["web_host_claims"] = ["Build Host main was checked out and tests passed"]
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "EXIT_DENIED")
        self.assertEqual(result["disposition"], "GAP/UNVERIFIED")
        self.assertIn("web_host_evidence_rejected_handoff_required", result["refusal_grounds"])
        self.assertNotEqual(result["resolution_route"], "conduct_chain_resolved")
        dumped = dump(result)
        self.assertNotIn('"PASS"', dumped)
        # No host evidence is admitted into the trace: the only host-shaped
        # token is the refusal route itself, and required_evidence stays empty.
        self.assertEqual(result["required_evidence"], [])
        self.assertNotIn('"kind"', dumped)

    def test_n01_host_evidence_item_is_rejected_the_same_way(self):
        fixture = web_validator_fixture()
        fixture["evidence"] = list(fixture["evidence"]) + [
            {"gate": None, "kind": "host_evidence", "currentness": "CURRENT", "ref": "0f" * 32}
        ]
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "EXIT_DENIED")
        self.assertIn("web_host_evidence_rejected_handoff_required", result["refusal_grounds"])


class N02SelfReviewAndFabricatedUniversalGateTests(unittest.TestCase):
    def test_n02a_self_review_never_satisfies_review_required(self):
        fixture = builder_local_fixture()
        fixture["independent_review_admission"] = {
            "reviewer": "builder-1",
            "admission_ref": ADMISSION_REF,
            "self_review": True,
        }
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "EXIT_DENIED")
        self.assertEqual(result["disposition"], "GAP/UNVERIFIED")
        self.assertIn("self_review_rejected", result["refusal_grounds"])
        # No exit route is produced; admission stays denied until a genuinely
        # independent reviewer supplies it.
        self.assertNotEqual(result["resolution_route"], "conduct_chain_resolved")

    def test_n02b_fabricated_universal_fresh_gate_against_not_required_is_rejected(self):
        fixture = docs_a0_fixture(review_policy="not-required")
        fixture["fabricated_fresh_gate"] = True
        result = conduct_trace(fixture)
        # The fabricated gate is NOT honored (recorded rejection); the
        # lawful not-required exit with complete other evidence stands.
        self.assertEqual(result["decision"], "CONDUCT_TRACE_COMPLETE")
        self.assertIn("unauthorized_fresh_gate_rejected", result["rejected_attempts"])
        self.assertNotIn("unauthorized_fresh_gate_rejected", result["refusal_grounds"])
        self.assertEqual(result["required_gate_set"], frozenset())

    def test_n02b_policy_unresolved_fails_closed_per_stage_2_6(self):
        fixture = docs_a0_fixture(review_policy="contradicted")
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("review_policy_unresolved_fail_closed", result["refusal_grounds"])


class N03UnsupportedDenominatorTests(unittest.TestCase):
    def test_n03_undeclared_role_gets_no_default_powers(self):
        fixture = builder_local_fixture()
        fixture["role"] = "superadmin"
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertEqual(result["disposition"], "GAP/UNVERIFIED")
        self.assertIn("unsupported_role_fail_closed", result["refusal_grounds"])

    def test_n03_unsupported_archetype_fails_closed(self):
        fixture = builder_local_fixture()
        fixture["archetype"] = "A9"
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("unsupported_archetype_fail_closed", result["refusal_grounds"])

    def test_n03_unsupported_job_class_fails_closed(self):
        fixture = builder_local_fixture()
        fixture["job_set"] = {"J08_UNDECLARED_EXTERNAL_WRITE"}
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("unsupported_class_fail_closed", result["refusal_grounds"])

    def test_n03_missing_legality_ref_fails_closed(self):
        fixture = builder_local_fixture()
        fixture["legality_ref"] = "chat-context-says-fine"
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertIn("missing_legality_ref", result["refusal_grounds"])
        dumped = dump(result)
        self.assertNotIn('"PASS"', dumped)


class N04RequiredEvidenceOmittedTests(unittest.TestCase):
    def test_n04_omitted_evidence_with_present_class_denies_exit(self):
        fixture = builder_local_fixture()
        fixture["evidence"] = []
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "EXIT_DENIED")
        self.assertEqual(result["disposition"], "GAP/UNVERIFIED")
        self.assertIn("required_evidence_missing", result["refusal_grounds"])
        dumped = dump(result)
        self.assertNotIn('"NOT_APPLICABLE"', dumped)
        self.assertNotIn('"PASS"', dumped)

    def test_n04_stale_evidence_ref_denies_exit(self):
        fixture = builder_local_fixture()
        fixture["evidence"] = [
            {"gate": "floor:gate-material-permission", "currentness": "STALE", "ref": BLOB_STALE}
        ]
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "EXIT_DENIED")
        self.assertIn("stale_evidence_ref", result["refusal_grounds"])

    def test_n04_evidence_not_bound_to_exact_subject_denies_exit(self):
        fixture = builder_local_fixture()
        fixture["evidence"] = [
            {"gate": "floor:gate-material-permission", "currentness": "CURRENT", "ref": "9a" * 32}
        ]
        result = conduct_trace(fixture)
        self.assertEqual(result["decision"], "EXIT_DENIED")
        self.assertIn("evidence_not_subject_bound", result["refusal_grounds"])


class N05FloorNonWeakeningTests(unittest.TestCase):
    def test_n05_lower_authority_override_cannot_weaken_t01_floor(self):
        fixture = builder_local_fixture()
        fixture["profile_override"] = {"floor:gate-material-permission": "demote"}
        result = conduct_trace(fixture)
        # The attempt fails; the higher requirement persists unchanged.
        self.assertIn("floor_weakening_override_rejected", result["rejected_attempts"])
        self.assertEqual(
            result["required_gate_set"],
            floor_required_gates(frozenset(fixture["job_set"]), {"permission"}),
        )
        self.assertIn("floor:gate-material-permission", result["required_gate_set"])

    def test_n05_trace_output_can_never_waive_floor_gates(self):
        result = conduct_trace(builder_local_fixture())
        before = result["required_gate_set"]
        for gate in sorted(before):
            with self.subTest(gate=gate):
                attempt = waive_required_gate(result, gate)
                self.assertTrue(attempt["rejected"])
                self.assertEqual(attempt["required_gate_set"], before)


class N06IncompleteCoverageCannotBeCompleteTests(unittest.TestCase):
    def test_n06_builder_only_coverage_never_reports_complete(self):
        combos = [
            # The proven lane: Builder / CLI LOCAL / A0-J02 proportional case.
            {"role": "builder", "transport": "LOCAL", "job_set": {"J02_DOCS_LOW_RISK"}, "archetype": "A0", "covered_by": "direct"},
            {"role": "builder", "transport": "LOCAL", "job_set": {"J_PERMISSION_REVIEW"}, "archetype": "A1", "covered_by": "direct"},
            # Otherwise-identical role carrying multi-J security/deploy
            # obligation, left unchecked.
            {"role": "validator", "transport": "LOCAL", "job_set": {"J_SECURITY_REVIEW", "J_DEPLOY_PLAN"}, "archetype": "A4", "covered_by": None},
        ]
        ledger = coverage_ledger(combos)
        self.assertFalse(ledger["complete"])
        self.assertEqual(len(ledger["uncovered"]), 1)
        gap = ledger["uncovered"][0]
        self.assertEqual(gap["status"], "GAP/UNVERIFIED")
        self.assertEqual(gap["resolution_route"], "coverage_gap_owner_routed")
        self.assertEqual(gap["job_set"], frozenset({"J_SECURITY_REVIEW", "J_DEPLOY_PLAN"}))
        self.assertEqual(gap["archetype"], "A4")
        self.assertFalse(ledger["not_applicable_used"])
        # The uncovered combination is RECORDED, not omitted.
        self.assertEqual(
            len(ledger["entries"]),
            sum(1 for c in combos if is_material_combo(c)),
        )


class ModelVocabularyAndRoutingTests(unittest.TestCase):
    """Contract hardening: model vocabulary stays inside declared sets and
    every failure route is fail-closed, never green."""

    def test_model_vocabulary_stays_inside_declared_sets(self):
        fixtures = [
            builder_local_fixture(),
            web_validator_fixture(),
            docs_a0_fixture(),
            docs_a0_fixture(review_policy="recommended"),
        ]
        for fixture in fixtures:
            result = conduct_trace(fixture)
            with self.subTest(actor=result["actor"]):
                self.assertIn(result["decision"], DECISIONS)
                self.assertTrue(gate_state_vocabulary(result) <= ALLOWED_MODEL_VOCABULARY)
                self.assertEqual(result["shared_projection"], "DEFERRED_TO_T11")
                self.assertEqual(result["new_gate_states_minted"], frozenset())

    def test_denied_chain_mints_no_pass_and_routes_to_owner(self):
        for fixture in (
            {**builder_local_fixture(), "evidence": []},
            {**builder_local_fixture(), "role": "superadmin"},
            {**web_validator_fixture(), "web_host_claims": ["tests passed on host"]},
        ):
            result = conduct_trace(fixture)
            with self.subTest(decision=result["decision"]):
                self.assertIn(result["decision"], {"EXIT_DENIED", "BLOCKED"})
                self.assertEqual(result["disposition"], "GAP/UNVERIFIED")
                self.assertTrue(set(result["refusal_grounds"]) <= ALLOWED_MODEL_VOCABULARY)
                self.assertNotIn('"PASS"', dump(result))

    def test_shared_projection_routes_deferred_to_t11_unwritten(self):
        for target in (
            "schemas/role-conduct-trace-v1.schema.json",
            "standard-manifest.json",
            "templates/task.md",
        ):
            with self.subTest(target=target):
                routed = register_central_projection(target)
                self.assertEqual(routed["routed"], "DEFERRED_TO_T11")
                self.assertFalse(routed["written"])


if __name__ == "__main__":
    unittest.main()
