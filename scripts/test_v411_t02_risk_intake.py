"""V411-T02 focused regression: affected-source materiality inventory.

Encodes the V411-T02 Task Pack (immutable blob
1c4282038e749199862e339b2a574179e54acb93, frozen at version/v4.11.0) §3
oracles P01-P04 / N01-N05 for the risk-intake owner concern as:

1. section-scoped textual contract checks binding the decision model to the
   owner-local normative clauses this task appends to
   `standards/DEVELOPMENT_WORKFLOW.md` (the ONE new `### 2.3` risk-intake
   subsection, co-located with §2/Stage 0 intake duties); plus verbatim
   guards that every preexisting intake surface (§2 tail, Stage 0) and the
   T01 effective-rule floor (§4 Effective-rule trace subsection) stay
   unchanged, and that the preexisting heading sequence is preserved; and
2. a fixture-driven inventory decision model that binds those clauses to
   concrete outcomes over per-source inspection-evidence projections.

The three epistemic states (PRESENT / ABSENT_WITH_INSPECTED_SCOPE / UNKNOWN)
are inspection facts in this test's decision model only; the standard
deliberately does not mint new Gate/Validation/Release states. The model
derives its required-gate set exclusively through T01 floor semantics
(single resolution path: the inventory calls the floor function; it never
re-derives gates). `CONFLICT` is the §4 fail-closed routing disposition from
the Pack §6, not a new gate state; `DEFERRED_TO_T11` is this file's routing
vocabulary for the v4.11 line's centrally designated wiring task (the
standard itself routes to the existing canonical owner without naming it).

Purely offline: standard library only, no network, no shared verifier.

Known deferrals (honest, never reported as covered): the central machine
projection of the MATERIALITY_INVENTORY trace (schema/manifest/verifier) is
DEFERRED_TO_T11 — the N05 oracle asserts the current tree carries no shadow
projection and the model routes any such proposal to T11 as
DEFERRED_TO_T11; whole-program conformance over a landed T11 projection
stays NOT_RUN. T01 floor coverage semantics for unknown job labels are
consumed read-only and are deliberately not re-implemented here. Known
expected RED outside this file (disclosed in the Builder Claim on #1012,
routed to the Controller per the #1064 F1 shared-pin bridge precedent): any
byte change to DEVELOPMENT_WORKFLOW.md necessarily changes its blob away
from the T01-admitted 57902fbc…, so the shared test_v49_gate_currentness.py
`read_only_rebound` subtest for this path is expected RED at this PR HEAD
until a lawful bridge admits the exact T02 blob; this file neither hides
nor duplicates that check.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "standards" / "DEVELOPMENT_WORKFLOW.md"
MANIFEST = ROOT / "standard-manifest.json"

# ---------------------------------------------------------------------------
# section identity (headings are the section identity; tests slice by them)
# ---------------------------------------------------------------------------

RISK_INTAKE_HEADING = "### 2.3 Risk-intake：受影响源实质性清单（affected-source materiality inventory）"
LIFECYCLE_HEADING = "## 3. 生命周期"
GATE_AUTHORITY_HEADING = "## 4. Gate Authority"
BLOCKER_HEADING = "## 5. Blocker Propagation"
T01_FLOOR_HEADING = "### Effective-rule trace：pinned revision、跨 owner 合取与 provenance"

# §2 tail preserved verbatim; the T02 section appends strictly AFTER it.
SECTION2_TAIL_SENTENCE = "**Integration Mode 不决定 Review 是否 required。** Review 由 Review Policy 单独决定。"

# Stage 0 block preserved verbatim (byte-exact at the v4.11 base).
STAGE0_HEADING = "### Stage 0 — Intake / Baseline"
STAGE0_VERBATIM = """### Stage 0 — Intake / Baseline

确认：

```text
scope
repository
target version/task
integration mode
integration branch / target branch
current default branch
current HEAD
existing PRD/Architecture/Task/Validation/CI state
acceptance criteria
known blockers
required evidence
```

如果任务已经明确且影响小，可以直接进入实现。

如果选择 Version Branch Mode，应尽早建立或确认 `version/vX.Y.Z` 远端 integration branch，使后续正式 checkpoint 与 Task PR 有稳定目标。
"""

# Preexisting heading sequence (relative order guard; T02 adds exactly one
# heading between the §2 tail and §3 and touches no other heading).
PREEXISTING_HEADINGS = (
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
    "## 5. Blocker Propagation",
    "## 6. Stage Checkpoint Push",
    "## 7. 快速路径",
    "## 8. ADS Evolution Feedback / Intake",
    "### 8.1 Observation classification and deterministic route",
    "### 8.2 Promotion boundary: ordinary ADS governance only",
    "### 8.3 Privacy / publication classification",
)

# T01 floor subsection: load-bearing sentences that must stay verbatim
# (mirrors test_v411_t01_effective_rules.py contract assertions, read-only).
T01_FLOOR_SENTENCES = (
    "`EFFECTIVE_RULE_TRACE`",
    "先在同一 concern 内按本节 authority chain 解析 precedence",
    "禁止削弱",
    "跨所有 applicable owner/concern 取逻辑 AND",
    "任一 owner 的 required gate 在合取中保持 required",
    "只是 applicability 的辅助证据",
    "义务不因删除 label 而消失",
    "适用性 UNKNOWN 或矛盾时按上一节 fail closed",
    "事实记为 `UNKNOWN`",
    "MUST NOT 记为已检视的 `ABSENT_WITH_INSPECTED_SCOPE`",
    "MUST NOT 产生 `PASS`",
    "epistemic fact，不是新增 gate state",
    "不新增 gate state、workflow state、共享 schema、模板或第二套方法论",
)

# Risk-intake owner clauses this task adds (exact normative sentences).
RISK_INTAKE_CLAUSES = (
    "MUST 为每个 changed subject 产出一份受影响源实质性清单",
    "`MATERIALITY_INVENTORY` risk trace",
    "read-only",
    "只向其供给 observed facts",
    "不是第二 applicability 权威",
    "不新增 gate state、workflow state、共享 schema 或第二套方法论",
    "material class 是从实际 diff 检视中观察到的实质效果事实（permission / API / security / migration / deployment / external-effect 等），不是新枚举权威",
    "subject",
    "source_path",
    "inspected_ref（实际检视所依据的 immutable blob/HEAD ref）",
    "material_class_observed",
    "epistemic_state ∈ {PRESENT, ABSENT_WITH_INSPECTED_SCOPE, UNKNOWN}",
    "currentness",
    "required_gate_ref（自 §4 floor 继承，只读）",
    "resolution_route",
    "epistemic state 是关于检视本身的 epistemic fact，不是新增 gate 枚举",
    "`PRESENT`：在该 source 上实际观察到某 material class，MUST 附 inspection ref",
    "`ABSENT_WITH_INSPECTED_SCOPE`：在明确陈述的 inspected scope 内实际检视并确认该 class 真实缺失，MUST 附 inspected scope ref",
    "没有 affirmative inspection evidence 时 MUST NOT 使用",
    "`UNKNOWN`：未实际检视、不可检视或 currentness 未证明，是未检视 source 的默认状态",
    "“未检视” MUST NOT 与“已检视且缺失”混同",
    "`inspected_ref` MUST 解析到 candidate tree/HEAD 中该 source 的实际 blob",
    "MUST 降级为 `UNKNOWN` 并要求重新检视",
    "MUST NOT 推断 currentness",
    "MUST NOT 把过期的 ABSENT 提升为当前缺失",
    "缺失或乐观的 job label 从来不是安全捷径",
    "由 independently inspected material fact 导出的义务不因删除或缺失 label 而消失（§4 floor）",
    "MUST fail closed `BLOCKED`",
    "MUST NOT 记为 `NOT_APPLICABLE`",
    "MUST NOT 产生 `PASS`",
    "按 `CONFLICT` 路由 owning authority 并保留历史事实",
    "MUST NOT 用清单解除、降级或豁免 floor 或更高 authority 已要求的任何 gate",
    "MUST NOT 以清单为据铸造新 gate/枚举",
    "既有 proportionate/快速路径（§7）保持不变",
    "MUST NOT 因清单强加 speculative 的全版本记录",
    "集中式 trace schema / manifest / verifier 投影归其既有 canonical owner",
    "additive 提案按既有路由升级",
    "本节不铸造 shadow schema/template/manifest 字段",
)

# ---------------------------------------------------------------------------
# contract vocabulary (Pack §4; existing gate enum is preserved)
# ---------------------------------------------------------------------------

EPISTEMIC_STATES = frozenset({"PRESENT", "ABSENT_WITH_INSPECTED_SCOPE", "UNKNOWN"})

# Fixture-level material class observation vocabulary (diff-derived facts,
# aligned with the T01 floor's inspected-fact classes; not a new authority).
MATERIAL_CLASSES = frozenset(
    {"permission", "api", "security", "migration", "deployment", "external_effect"}
)

CANONICAL_GATE_STATES = frozenset({"PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE"})

# Decision outcomes of the inventory model (test-level risk-trace vocabulary;
# the standard mints no new gate/workflow state).
DECISIONS = frozenset(
    {
        "INVENTORY_COMPLETE_GATES_STANDING",
        "PROPORTIONATE_ABSENT_FAST_PATH",
        "BLOCKED",
    }
)

# T01 floor inheritance, fixture-level: required-gate refs per material class
# and per declared job label. Real gate applicability stays with §4 authority;
# this mapping exists so the model can assert set identity with the floor.
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

BLOB_HEX = re.compile(r"^[0-9a-f]{64}$")

# Deterministic fixture pins (64-hex shaped, distinct per surface).
HEAD_A = "a1" * 32
BLOB_AUTHZ = "b1" * 32
BLOB_ROUTES = "b2" * 32
BLOB_DEPLOY = "b3" * 32
BLOB_DOCS = "b4" * 32
BLOB_CONFIG = "b5" * 32
BLOB_STALE = "c9" * 32

# ---------------------------------------------------------------------------
# T01 floor (read-only consumption) + T02 inventory decision model
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


def _record(source_path, cls, state, currentness, inspected_ref="", scope=None,
            route="fail_closed_unknown"):
    return {
        "subject": None,  # bound by inventory() to the fixture subject
        "source_path": source_path,
        "inspected_ref": inspected_ref,
        "material_class_observed": cls,
        "epistemic_state": state,
        "currentness": currentness,
        "required_gate_ref": FLOOR_GATE_BY_CLASS.get(cls) if cls else None,
        "resolution_route": route,
        "inspected_scope": scope,
    }


def inventory(fixture):
    """Build the MATERIALITY_INVENTORY risk trace for one subject (Pack §4).

    Single resolution path: the required-gate set is delegated to
    floor_required_gates(); the inventory only attaches observations.
    """
    subject = fixture["subject"]
    tree = fixture["candidate_tree"]
    inspections = fixture["inspections"]
    records = []
    inspected_facts = set()
    unknown_paths = []
    uncovered_present_routes = {}

    for path in fixture["changed_sources"]:
        insp = inspections.get(path)
        if insp is None:
            # N02: no real inspection — UNKNOWN by default, never ABSENT.
            rec = _record(path, None, "UNKNOWN", "NOT_PROVEN", route="fail_closed_unknown")
            rec["subject"] = subject
            records.append(rec)
            unknown_paths.append(path)
            continue
        ref = insp.get("inspected_ref", "")
        if not BLOB_HEX.match(ref):
            rec = _record(path, None, "UNKNOWN", "NOT_PROVEN", inspected_ref=ref,
                          route="malformed_inspection_ref")
            rec["subject"] = subject
            records.append(rec)
            unknown_paths.append(path)
            continue
        if ref != tree.get(path):
            # N03: stale inspection ref — currentness fails; demote to UNKNOWN.
            rec = _record(path, None, "UNKNOWN", "STALE", inspected_ref=ref,
                          route="reinspection_required")
            rec["subject"] = subject
            records.append(rec)
            unknown_paths.append(path)
            continue
        findings = insp.get("findings") or {}
        if not findings:
            rec = _record(path, None, "UNKNOWN", "CURRENT", inspected_ref=ref,
                          route="empty_inspection_scope")
            rec["subject"] = subject
            records.append(rec)
            unknown_paths.append(path)
            continue
        for cls in sorted(findings):
            observed = findings[cls]
            if cls not in MATERIAL_CLASSES:
                rec = _record(path, None, "UNKNOWN", "CURRENT", inspected_ref=ref,
                              route="unowned_class_vocabulary")
                rec["subject"] = subject
                records.append(rec)
                unknown_paths.append(path)
                continue
            if observed is True:
                inspected_facts.add(cls)
                rec = _record(path, cls, "PRESENT", "CURRENT", inspected_ref=ref,
                              route="floor_gate_standing")
            elif insp.get("scope"):
                rec = _record(path, cls, "ABSENT_WITH_INSPECTED_SCOPE", "CURRENT",
                              inspected_ref=ref, scope=insp["scope"],
                              route="proportionate_absent")
            else:
                # ABSENT without a stated inspected scope proves nothing.
                rec = _record(path, None, "UNKNOWN", "CURRENT", inspected_ref=ref,
                              route="absent_without_stated_scope")
                unknown_paths.append(path)
            rec["subject"] = subject
            records.append(rec)

    required_gates = floor_required_gates(
        frozenset(fixture["declared_jobs"]), inspected_facts
    )
    # N01/§6 coverage is judged against the declared JOB closure only: a
    # PRESENT material fact always enters the floor conjunction, but a label
    # that does not admit it never makes the inventory green — the optimistic
    # or missing label is not a shortcut (P01 vs N01).
    job_gates = floor_required_gates(frozenset(fixture["declared_jobs"]), set())

    # N01/§6: a PRESENT material fact whose floor gate is not covered by any
    # declared job label keeps its obligation; the optimistic/missing label
    # never waives it. A docs-only label claim contradicted by a PRESENT
    # observation routes as CONFLICT to the owning authority.
    contradiction = bool(fixture.get("label_claims", {}).get("docs_only")) and any(
        r["epistemic_state"] == "PRESENT" for r in records
    )
    for rec in records:
        if rec["epistemic_state"] == "PRESENT":
            if rec["required_gate_ref"] not in job_gates:
                uncovered_present_routes[rec["source_path"]] = (
                    "conflict_routed_to_owning_authority"
                    if contradiction
                    else "floor_conjunction_label_insufficient"
                )
            elif contradiction:
                uncovered_present_routes[rec["source_path"]] = (
                    "conflict_routed_to_owning_authority"
                )

    blocked = bool(unknown_paths) or bool(uncovered_present_routes)
    if blocked:
        decision = "BLOCKED"
    elif not inspected_facts:
        decision = "PROPORTIONATE_ABSENT_FAST_PATH"
    else:
        decision = "INVENTORY_COMPLETE_GATES_STANDING"

    return {
        "subject": subject,
        "candidate_head": fixture["candidate_head"],
        "records": records,
        "required_gate_set": required_gates,
        "decision": decision,
        "blocked_routes": dict(
            sorted({**{p: "fail_closed_unknown" for p in unknown_paths},
                    **uncovered_present_routes}.items())
        ),
        "fast_path_retained": decision == "PROPORTIONATE_ABSENT_FAST_PATH",
        "shared_projection": "DEFERRED_TO_T11",
        "new_gate_states_minted": frozenset(),
    }


def waive_required_gate(inventory_result, gate):
    """N04: the inventory output can never waive/demote a floor-required
    gate; the higher-authority requirement persists unchanged."""
    return {
        "rejected": True,
        "reason": "inventory supplies observed facts only; the gate set is owned by the §4 floor",
        "required_gate_set": inventory_result["required_gate_set"],
        "gate": gate,
    }


def register_central_projection(target):
    """N05: materiality data has no central template/schema/manifest route;
    additive proposals are routed to the designated wiring task unwritten."""
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
    tokens = {result["decision"], result["shared_projection"]}
    for rec in result["records"]:
        tokens.add(rec["epistemic_state"])
        tokens.add(rec["currentness"])
        if rec["resolution_route"]:
            tokens.add(rec["resolution_route"])
    return tokens


ALLOWED_MODEL_VOCABULARY = (
    EPISTEMIC_STATES
    | CANONICAL_GATE_STATES
    | DECISIONS
    | {"DEFERRED_TO_T11", "CONFLICT"}
    | {
        "CURRENT",
        "STALE",
        "NOT_PROVEN",
        "floor_gate_standing",
        "proportionate_absent",
        "fail_closed_unknown",
        "malformed_inspection_ref",
        "reinspection_required",
        "empty_inspection_scope",
        "absent_without_stated_scope",
        "unowned_class_vocabulary",
        "conflict_routed_to_owning_authority",
        "floor_conjunction_label_insufficient",
    }
)

# ---------------------------------------------------------------------------
# fixtures (deterministic; diff-surface ground truth vs. inspection input)
# ---------------------------------------------------------------------------


def base_fixture():
    return {
        "subject": "service-x01",
        "candidate_head": HEAD_A,
        "candidate_tree": {
            "src/authz.py": BLOB_AUTHZ,
            "api/routes.py": BLOB_ROUTES,
            "deploy/stack.yaml": BLOB_DEPLOY,
        },
        "changed_sources": ["src/authz.py", "api/routes.py", "deploy/stack.yaml"],
        "inspections": {
            "src/authz.py": {
                "inspected_ref": BLOB_AUTHZ,
                "findings": {"permission": True},
            },
            "api/routes.py": {
                "inspected_ref": BLOB_ROUTES,
                "findings": {"api": True},
            },
            "deploy/stack.yaml": {
                "inspected_ref": BLOB_DEPLOY,
                "findings": {"deployment": True},
            },
        },
        "declared_jobs": {"J_PERMISSION_REVIEW", "J_API_COMPATIBILITY", "J_DEPLOY_PLAN"},
    }


def inspected_absent_fixture(subject="docs-x02", docs_only_claim=False):
    docs_inspection = {
        "inspected_ref": BLOB_DOCS,
        "scope": "tree-grep: permission/api/security/migration/deployment/external-effect markers within docs/guide.md@blob",
        "findings": {
            "permission": False,
            "api": False,
            "security": False,
            "migration": False,
            "deployment": False,
            "external_effect": False,
        },
    }
    return {
        "subject": subject,
        "candidate_head": HEAD_A,
        "candidate_tree": {"docs/guide.md": BLOB_DOCS},
        "changed_sources": ["docs/guide.md"],
        "inspections": {"docs/guide.md": docs_inspection},
        "declared_jobs": {"J02_DOCS_LOW_RISK"},
        "label_claims": {"docs_only": docs_only_claim},
    }


def inspected_facts_of(fixture) -> set:
    """Ground-truth facts a CURRENT inspection exposes (oracle helper)."""
    facts = set()
    for path in fixture["changed_sources"]:
        insp = fixture["inspections"].get(path)
        if not insp:
            continue
        if insp.get("inspected_ref") != fixture["candidate_tree"].get(path):
            continue
        for cls, observed in (insp.get("findings") or {}).items():
            if observed and cls in MATERIAL_CLASSES:
                facts.add(cls)
    return facts


# ---------------------------------------------------------------------------
# repository helpers
# ---------------------------------------------------------------------------


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def risk_intake_section() -> str:
    text = workflow_text()
    start = text.index(RISK_INTAKE_HEADING)
    end = text.index(LIFECYCLE_HEADING, start + len(RISK_INTAKE_HEADING))
    return text[start:end]


def gate_authority_section() -> str:
    text = workflow_text()
    start = text.index(GATE_AUTHORITY_HEADING)
    end = text.index(BLOCKER_HEADING, start + len(GATE_AUTHORITY_HEADING))
    return text[start:end]


def t01_floor_subsection() -> str:
    section = gate_authority_section()
    start = section.index(T01_FLOOR_HEADING)
    rest = section[start + len(T01_FLOOR_HEADING):]
    next_heading = rest.find("\n### ")
    return rest if next_heading == -1 else rest[:next_heading]


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
# section-scoped textual contract tests (Pack §5 implementation clauses)
# ---------------------------------------------------------------------------


class RiskIntakeSectionPlacementTests(unittest.TestCase):
    def test_section_exists_exactly_once_between_intake_tail_and_lifecycle(self):
        text = workflow_text()
        self.assertEqual(text.count(RISK_INTAKE_HEADING), 1)
        tail = text.index(SECTION2_TAIL_SENTENCE)
        start = text.index(RISK_INTAKE_HEADING)
        end = text.index(LIFECYCLE_HEADING, start)
        self.assertLess(tail, start)
        self.assertLess(start, end)
        # Nothing but the T02 section lives between the §2 tail and §3.
        between = text[tail:end]
        self.assertIn(RISK_INTAKE_HEADING, between)
        self.assertNotIn("### 2.4", between)

    def test_preexisting_headings_keep_relative_order(self):
        found = headings(workflow_text())
        pos = 0
        for expected in PREEXISTING_HEADINGS:
            with self.subTest(heading=expected):
                while pos < len(found) and found[pos] != expected:
                    pos += 1
                self.assertLess(pos, len(found), f"heading missing/out of order: {expected}")
                pos += 1

    def test_stage0_block_is_byte_verbatim(self):
        text = workflow_text()
        self.assertIn(STAGE0_VERBATIM, text)
        # §2.3 sits at the intake tail, BEFORE the lifecycle's Stage 0.
        self.assertLess(text.index(RISK_INTAKE_HEADING), text.index(STAGE0_HEADING))

    def test_section2_tail_sentence_is_verbatim_and_unique(self):
        text = workflow_text()
        self.assertEqual(text.count(SECTION2_TAIL_SENTENCE), 1)
        self.assertIn(
            "不得为了简化流程而反向破坏既有 candidate/integration facts", text
        )


class RiskIntakeSectionContractTests(unittest.TestCase):
    """Pack §1/§4/§5/§6 normative clauses, bound sentence-by-sentence."""

    def test_all_owner_clauses_are_normative_in_section(self):
        section = risk_intake_section()
        for clause in RISK_INTAKE_CLAUSES:
            with self.subTest(clause=clause):
                self.assertIn(clause, section)

    def test_inventory_consumes_t01_floor_read_only(self):
        section = risk_intake_section()
        floor = t01_floor_subsection()
        self.assertIn("§4", section)
        self.assertIn("Effective-rule trace", section)
        # The floor itself stays verbatim (read-only consumption).
        for sentence in T01_FLOOR_SENTENCES:
            with self.subTest(t01_floor_sentence=sentence):
                self.assertIn(sentence, floor)

    def test_no_new_gate_enum_is_minted_in_section(self):
        section = risk_intake_section()
        gate_tokens = set(
            re.findall(r"`(PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE)`", section)
        )
        self.assertTrue(gate_tokens)
        self.assertTrue(gate_tokens <= CANONICAL_GATE_STATES, gate_tokens - CANONICAL_GATE_STATES)
        self.assertIn("epistemic_state ∈ {PRESENT, ABSENT_WITH_INSPECTED_SCOPE, UNKNOWN}", section)
        # CONFLICT appears only as the §4/§6 routing disposition.
        self.assertIn("按 `CONFLICT` 路由 owning authority", section)

    def test_section_mints_no_machine_schema(self):
        section = risk_intake_section()
        self.assertNotIn("schema_version", section)
        self.assertNotIn("```json", section)
        self.assertIn("本节不铸造 shadow schema/template/manifest 字段", section)
        self.assertIn("additive 提案按既有路由升级", section)


class NoShadowCentralProjectionTests(unittest.TestCase):
    """Pack N05 real-tree half: no materiality projection outside the owner
    section. (Pre-T11 integration state; T11's own landing owns the central
    wiring and its conformance.)"""

    def test_manifest_carries_no_materiality_projection(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        shadowed = [k for k in recursive_keys(manifest) if "materiality" in str(k).lower()]
        self.assertEqual(shadowed, [])

    def test_no_materiality_schema_file_exists(self):
        schemas = ROOT / "schemas"
        shadowed = [p.name for p in schemas.glob("*") if "materiality" in p.name.lower()]
        self.assertEqual(shadowed, [])

    def test_no_materiality_projection_in_templates(self):
        shadowed = []
        for path in (ROOT / "templates").rglob("*"):
            if path.is_file() and "MATERIALITY_INVENTORY" in path.read_text(encoding="utf-8", errors="replace"):
                shadowed.append(str(path.relative_to(ROOT)))
        self.assertEqual(shadowed, [])


# ---------------------------------------------------------------------------
# fixture-driven decision oracles (Pack §3 cases)
# ---------------------------------------------------------------------------


class P01InspectedMaterialPresentTests(unittest.TestCase):
    def test_p01_present_records_bind_refs_and_floor_gate_set_is_enforced(self):
        fixture = base_fixture()
        result = inventory(fixture)
        self.assertEqual(result["decision"], "INVENTORY_COMPLETE_GATES_STANDING")
        present = [r for r in result["records"] if r["epistemic_state"] == "PRESENT"]
        self.assertEqual(
            sorted((r["source_path"], r["material_class_observed"]) for r in present),
            [("api/routes.py", "api"), ("deploy/stack.yaml", "deployment"), ("src/authz.py", "permission")],
        )
        for rec in present:
            with self.subTest(path=rec["source_path"]):
                self.assertEqual(rec["currentness"], "CURRENT")
                self.assertEqual(rec["inspected_ref"], fixture["candidate_tree"][rec["source_path"]])
                self.assertIsNotNone(rec["required_gate_ref"])
        self.assertEqual(
            result["required_gate_set"],
            {
                "floor:gate-material-permission",
                "floor:gate-material-api",
                "floor:gate-material-deployment",
            },
        )
        # Floor gates stay standing: the inventory mints no PASS.
        dumped = dump(result)
        self.assertNotIn('"PASS"', dumped)
        self.assertNotIn('"NOT_APPLICABLE"', dumped)


class P02FullInspectionAbsentTests(unittest.TestCase):
    def test_p02_per_class_absent_with_scope_and_fast_path_retained(self):
        fixture = inspected_absent_fixture(subject="config-x02")
        result = inventory(fixture)
        self.assertEqual(result["decision"], "PROPORTIONATE_ABSENT_FAST_PATH")
        self.assertTrue(result["fast_path_retained"])
        absent = [r for r in result["records"] if r["epistemic_state"] == "ABSENT_WITH_INSPECTED_SCOPE"]
        self.assertEqual(len(absent), len(MATERIAL_CLASSES))
        for rec in absent:
            with self.subTest(cls=rec["material_class_observed"]):
                self.assertEqual(rec["currentness"], "CURRENT")
                self.assertEqual(rec["inspected_ref"], BLOB_DOCS)
                self.assertTrue(rec["inspected_scope"])
        # No speculative blanket full-version record: records stay per-source
        # per-class.
        self.assertEqual(len(result["records"]), len(MATERIAL_CLASSES))


class P03ProportionateDocsOnlyTests(unittest.TestCase):
    def test_p03_a0_path_stands_and_states_still_listed(self):
        fixture = inspected_absent_fixture(docs_only_claim=True)
        result = inventory(fixture)
        self.assertEqual(result["decision"], "PROPORTIONATE_ABSENT_FAST_PATH")
        self.assertTrue(result["fast_path_retained"])
        self.assertEqual(result["required_gate_set"], frozenset())
        self.assertEqual(len(result["records"]), len(MATERIAL_CLASSES))
        self.assertTrue(all(r["source_path"] == "docs/guide.md" for r in result["records"]))


class P04SingleResolutionPathTests(unittest.TestCase):
    def test_p04_gate_conjunction_identical_to_t01_floor_observations_only(self):
        fixture = base_fixture()
        result = inventory(fixture)
        floor_direct = floor_required_gates(
            frozenset(fixture["declared_jobs"]), inspected_facts_of(fixture)
        )
        # Conjunction identity with the T01 floor.
        self.assertEqual(result["required_gate_set"], floor_direct)
        # The inventory adds observations only: records carry epistemic fields,
        # the floor projection carries gate refs only (no second authority).
        for rec in result["records"]:
            with self.subTest(path=rec["source_path"]):
                self.assertIn(rec["epistemic_state"], EPISTEMIC_STATES)
                if rec["required_gate_ref"] is not None:
                    self.assertIn(rec["required_gate_ref"], FLOOR_GATE_BY_CLASS.values())
        self.assertEqual(
            result["shared_projection"], "DEFERRED_TO_T11"
        )


class N01MissingOrOptimisticLabelTests(unittest.TestCase):
    def test_n01a_docs_only_label_over_material_diff_is_blocked_as_conflict(self):
        fixture = base_fixture()
        fixture["declared_jobs"] = {"J02_DOCS_LOW_RISK"}
        fixture["label_claims"] = {"docs_only": True}
        result = inventory(fixture)
        self.assertEqual(result["decision"], "BLOCKED")
        self.assertTrue(result["blocked_routes"])
        for route in result["blocked_routes"].values():
            self.assertEqual(route, "conflict_routed_to_owning_authority")
        dumped = dump(result)
        self.assertNotIn('"PASS"', dumped)
        self.assertNotIn('"NOT_APPLICABLE"', dumped)
        # Missing label never waives observed materiality.
        self.assertEqual(
            result["required_gate_set"],
            {
                "floor:gate-material-permission",
                "floor:gate-material-api",
                "floor:gate-material-deployment",
            },
        )

    def test_n01b_missing_label_over_material_diff_is_blocked(self):
        fixture = base_fixture()
        fixture["declared_jobs"] = set()
        result = inventory(fixture)
        self.assertEqual(result["decision"], "BLOCKED")
        for route in result["blocked_routes"].values():
            self.assertEqual(route, "floor_conjunction_label_insufficient")
        self.assertEqual(
            result["required_gate_set"],
            {
                "floor:gate-material-permission",
                "floor:gate-material-api",
                "floor:gate-material-deployment",
            },
        )


class N02UninspectedMaterialSourceTests(unittest.TestCase):
    def test_n02_uninspected_source_is_unknown_never_absent(self):
        fixture = base_fixture()
        del fixture["inspections"]["src/authz.py"]
        result = inventory(fixture)
        self.assertEqual(result["decision"], "BLOCKED")
        authz = [r for r in result["records"] if r["source_path"] == "src/authz.py"]
        self.assertEqual(len(authz), 1)
        self.assertEqual(authz[0]["epistemic_state"], "UNKNOWN")
        self.assertEqual(authz[0]["currentness"], "NOT_PROVEN")
        self.assertIsNone(authz[0]["material_class_observed"])
        self.assertNotEqual(authz[0]["epistemic_state"], "ABSENT_WITH_INSPECTED_SCOPE")
        self.assertIn("src/authz.py", result["blocked_routes"])
        # Downstream stays fail-closed: no positive verdict is emitted.
        dumped = dump(result)
        self.assertNotIn('"PASS"', dumped)


class N03StaleInspectionRefTests(unittest.TestCase):
    def test_n03_stale_ref_demotes_to_unknown_and_forbids_promotion(self):
        fixture = base_fixture()
        fixture["inspections"]["src/authz.py"] = {
            "inspected_ref": BLOB_STALE,
            "findings": {"permission": False},
            "scope": "stale-scope",
        }
        result = inventory(fixture)
        authz = [r for r in result["records"] if r["source_path"] == "src/authz.py"]
        self.assertEqual(len(authz), 1)
        self.assertEqual(authz[0]["epistemic_state"], "UNKNOWN")
        self.assertEqual(authz[0]["currentness"], "STALE")
        self.assertEqual(authz[0]["resolution_route"], "reinspection_required")
        # A stale observed-ABSENT is never promoted to current absence.
        self.assertNotEqual(authz[0]["epistemic_state"], "ABSENT_WITH_INSPECTED_SCOPE")
        self.assertEqual(result["decision"], "BLOCKED")
        # The stale fact never ENTERS the floor conjunction as an inspected
        # fact; the gate set equals the floor resolution over jobs plus the
        # still-current facts only (permission's job label keeps its gate
        # required independently of the stale finding).
        self.assertEqual(
            result["required_gate_set"],
            floor_required_gates(
                frozenset(fixture["declared_jobs"]), inspected_facts_of(fixture)
            ),
        )
        self.assertNotIn("permission", inspected_facts_of(fixture))


class N04NoWaiveNoMintTests(unittest.TestCase):
    def test_n04_inventory_cannot_waive_or_demote_floor_gates(self):
        result = inventory(base_fixture())
        before = result["required_gate_set"]
        for gate in sorted(before):
            with self.subTest(gate=gate):
                attempt = waive_required_gate(result, gate)
                self.assertTrue(attempt["rejected"])
                self.assertEqual(attempt["required_gate_set"], before)

    def test_n04_inventory_mints_no_new_gate_state(self):
        result = inventory(base_fixture())
        self.assertEqual(result["new_gate_states_minted"], frozenset())
        self.assertTrue(gate_state_vocabulary(result) <= ALLOWED_MODEL_VOCABULARY)
        dumped = dump(result)
        self.assertNotIn("GATE_MATERIALITY_OK", dumped)
        self.assertNotIn("MATERIALITY_PASS", dumped)


class N05CentralProjectionRoutingTests(unittest.TestCase):
    def test_n05_central_targets_route_deferred_to_t11_unwritten(self):
        for target in ("schemas/materiality-inventory-v1.schema.json", "standard-manifest.json", "templates/task.md"):
            with self.subTest(target=target):
                routed = register_central_projection(target)
                self.assertEqual(routed["routed"], "DEFERRED_TO_T11")
                self.assertFalse(routed["written"])

    def test_n05_model_vocabulary_stays_inside_declared_sets(self):
        for fixture in (base_fixture(), inspected_absent_fixture(), inspected_absent_fixture(docs_only_claim=True)):
            result = inventory(fixture)
            with self.subTest(subject=result["subject"]):
                self.assertIn(result["decision"], DECISIONS)
                self.assertTrue(gate_state_vocabulary(result) <= ALLOWED_MODEL_VOCABULARY)


class ModelCurrentnessFailClosedTests(unittest.TestCase):
    """Contract hardening: malformed/empty evidence fails closed, never green."""

    def test_malformed_ref_is_unknown(self):
        fixture = base_fixture()
        fixture["inspections"]["api/routes.py"] = {
            "inspected_ref": "short-ref",
            "findings": {"api": False},
            "scope": "scope",
        }
        result = inventory(fixture)
        routes_rec = [r for r in result["records"] if r["source_path"] == "api/routes.py"][0]
        self.assertEqual(routes_rec["epistemic_state"], "UNKNOWN")
        self.assertEqual(routes_rec["resolution_route"], "malformed_inspection_ref")
        self.assertEqual(result["decision"], "BLOCKED")

    def test_absent_without_stated_scope_is_unknown(self):
        fixture = inspected_absent_fixture()
        fixture["inspections"]["docs/guide.md"]["scope"] = ""
        result = inventory(fixture)
        self.assertEqual(result["decision"], "BLOCKED")
        rec = result["records"][0]
        self.assertEqual(rec["epistemic_state"], "UNKNOWN")
        self.assertEqual(rec["resolution_route"], "absent_without_stated_scope")

    def test_empty_inspection_scope_is_unknown(self):
        fixture = base_fixture()
        fixture["inspections"]["deploy/stack.yaml"] = {
            "inspected_ref": BLOB_DEPLOY,
            "findings": {},
        }
        result = inventory(fixture)
        rec = [r for r in result["records"] if r["source_path"] == "deploy/stack.yaml"][0]
        self.assertEqual(rec["epistemic_state"], "UNKNOWN")
        self.assertEqual(rec["resolution_route"], "empty_inspection_scope")
        self.assertEqual(result["decision"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
