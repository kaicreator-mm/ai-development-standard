"""V410-T04A focused regression: gate applicability and repair-routing convergence.

Encodes the L3_WAVE_B_R1.md V410-T04A positive/negative cases as
deterministic textual contract checks against the gate-routing owner
`standards/DEVELOPMENT_WORKFLOW.md` (§4 Gate Authority) and the exact-subject
validation owner `standards/VALIDATION_STANDARD.md` (§1 states, §13 prohibited
practices). Purely textual; no network, no runtime.
"""

from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_WORKFLOW_STATES = {
    "planned",
    "ready",
    "claimed",
    "implementing",
    "review-ready",
    "reviewing",
    "changes-requested",
    "validation-needed",
    "merge-ready",
    "blocked",
    "done",
}

CANONICAL_GATE_STATES = {"PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE"}

# Authority families that T04A must not redefine.
REVIEW_FINDING_OWNED_TERMS = ("severity", "currentness", "aggregation")
PRODUCT_LIFECYCLE_OWNED_TERMS = (
    "Product Freeze",
    "Product Review",
    "Product Research",
    "semantic L1 Product Evidence",
)
# No arbitrary universal retry cap may be introduced as gate authority.
# The normative text names the prohibited concept ("universal retry cap") on
# purpose, so only concrete configured-cap markers and numeric-bound assertions
# are rejected here.
RETRY_CAP_AUTHORITY_MARKERS = (
    "max_retries",
    "retry_cap",
    "重试上限",
    "最大重试",
)

RETRY_CAP_AUTHORITY_PATTERNS = (
    re.compile(r"最多\s*\d+\s*次"),
    re.compile(r"\d+\s*(?:attempts?|retries|重试)"),
    re.compile(r"after\s+\d+\s+attempts", re.IGNORECASE),
)

GATE_AUTHORITY_HEADING = "## 4. Gate Authority"
BLOCKER_HEADING = "## 5. Blocker Propagation"
APPLICABILITY_HEADING = "### Gate applicability 与合法来源"
FAIL_CLOSED_HEADING = "### Applicability UNKNOWN 或矛盾：fail closed"
ROOT_CLASS_HEADING = "### Repair routing：root defect class"
NON_CONVERGENCE_HEADING = "### Non-converging repair：escalation，而非 universal retry cap"


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def workflow() -> str:
    return read("standards/DEVELOPMENT_WORKFLOW.md")


def validation_standard() -> str:
    return read("standards/VALIDATION_STANDARD.md")


def gate_authority_section() -> str:
    text = workflow()
    start = text.index(GATE_AUTHORITY_HEADING)
    end = text.index(BLOCKER_HEADING)
    return text[start:end]


def gate_subsection(heading: str) -> str:
    section = gate_authority_section()
    start = section.index(heading)
    rest = section[start + len(heading) :]
    next_heading = rest.find("\n### ")
    return rest if next_heading == -1 else rest[:next_heading]


def validation_purpose_section() -> str:
    text = validation_standard()
    start = text.index("## 1. Purpose and states")
    end = text.index("## 2. Gate Authority")
    return text[start:end]


def validation_prohibited_section() -> str:
    text = validation_standard()
    return text[text.index("## 13. Prohibited practices") :]


class GateApplicabilityAuthorityTests(unittest.TestCase):
    """L3 positive case 1: applicability derives from authority, not convenience."""

    def test_applicability_derives_from_the_shared_authority_chain(self) -> None:
        section = gate_authority_section()
        self.assertIn("Required gate 的 applicability 由同一 authority chain 决定", section)
        for authority in (
            "Frozen PRD / Contract",
            "Frozen Architecture",
            "PROJECT_OVERRIDES.md",
            "Task-specific acceptance",
            "Standard defaults",
        ):
            with self.subTest(authority=authority):
                self.assertIn(authority, section)

    def test_illegitimate_reduction_bases_are_enumerated_inside_the_prohibition(self) -> None:
        subsection = gate_subsection(APPLICABILITY_HEADING)
        prohibition = "MUST NOT 收窄、豁免、跳过或降级 required gate"
        self.assertIn(prohibition, subsection)
        self.assertIn("MUST NOT 使其被记为 `NOT_APPLICABLE`", subsection)
        listed_block = subsection[
            subsection.index("```text") : subsection.index("```", subsection.index("```text") + 1)
        ]
        for basis in (
            "cost / 预算 / 资源紧张",
            "effort、turnaround / 交付速度 / 计划或发布压力",
            "变更文件数、行数、diff 大小",
            "docs-only / 机械生成 / 非代码外观",
            "Agent 或模型自评的 confidence",
            "历史惯例 / 旧脚本先例 / 无人反对 / 沉默",
        ):
            with self.subTest(basis=basis):
                self.assertIn(basis, listed_block)

    def test_reduction_bases_cannot_mutate_applicability_or_gate_state(self) -> None:
        subsection = gate_subsection(APPLICABILITY_HEADING)
        self.assertIn("MUST NOT 改变 gate applicability 或 gate 状态", subsection)
        self.assertIn("executor MUST NOT 从变更外观反推 applicability", subsection)
        self.assertIn("MUST NOT 因其结果不便而被追认为 `NOT_APPLICABLE`", subsection)

    def test_docs_only_class_requires_its_own_authority_declaration(self) -> None:
        subsection = gate_subsection(APPLICABILITY_HEADING)
        self.assertIn("只有在 authority 自身声明该类别为 `not-required` 时才产生 `NOT_APPLICABLE`", subsection)

    def test_downgrade_requires_equal_or_higher_authority(self) -> None:
        subsection = gate_subsection(APPLICABILITY_HEADING)
        self.assertIn("需要同级或更高 authority", subsection)
        self.assertIn("lower-authority 的静默降级始终无效", subsection)


class FailClosedApplicabilityTests(unittest.TestCase):
    """L3 positive case 2: UNKNOWN/contradictory applicability fails closed."""

    def test_unknown_or_contradictory_applicability_fails_closed(self) -> None:
        subsection = gate_subsection(FAIL_CLOSED_HEADING)
        self.assertIn("UNKNOWN", subsection)
        self.assertIn("相互矛盾", subsection)
        self.assertIn("MUST fail closed", subsection)

    def test_no_preference_or_discovery_order_adjudication(self) -> None:
        subsection = gate_subsection(FAIL_CLOSED_HEADING)
        self.assertIn("MUST NOT 以 Builder/Controller/Validator 偏好裁决", subsection)
        self.assertIn("MUST NOT 以文件/发现顺序或先到先得裁决", subsection)
        self.assertIn("MUST NOT 以沉默、无人反对或历史先例裁决", subsection)

    def test_ambiguous_gate_stays_unsatisfied_and_never_not_applicable(self) -> None:
        subsection = gate_subsection(FAIL_CLOSED_HEADING)
        self.assertIn("MUST NOT 记为 NOT_APPLICABLE", subsection)
        self.assertIn("MUST NOT 记为 PASS", subsection)
        self.assertIn("该 gate 保持未满足（`NOT_RUN` / `BLOCKED`）", subsection)

    def test_disposition_routes_to_the_owning_authority(self) -> None:
        subsection = gate_subsection(FAIL_CLOSED_HEADING)
        self.assertIn("直到 owning authority 给出 disposition", subsection)
        self.assertIn("并记录为可追溯事实", subsection)

    def test_fail_closed_does_not_stop_independent_work(self) -> None:
        subsection = gate_subsection(FAIL_CLOSED_HEADING)
        self.assertIn("fail closed 只影响该 gate 与真实依赖它的下游", subsection)
        self.assertIn("与其无依赖关系的独立工作继续推进（§5）", subsection)


class RootClassRepairRoutingTests(unittest.TestCase):
    """L3 positive case 3: repair targets the root defect class."""

    def test_repair_is_attributed_to_a_root_defect_class(self) -> None:
        subsection = gate_subsection(ROOT_CLASS_HEADING)
        self.assertIn("repair 必须归因到 root defect class", subsection)
        self.assertIn("而不是只处理被引用的表象/症状", subsection)

    def test_root_defect_classes_are_enumerated(self) -> None:
        subsection = gate_subsection(ROOT_CLASS_HEADING)
        for root_class in (
            "product semantics / authority contradiction",
            "architecture / public contract",
            "implementation defect",
            "test / fixture / evidence defect",
            "environment / toolchain / external boundary",
            "execution / attribution defect",
            "gate applicability 或 authority ambiguity",
        ):
            with self.subTest(root_class=root_class):
                self.assertIn(root_class, subsection)

    def test_repair_declares_root_class_and_falsifiable_convergence(self) -> None:
        subsection = gate_subsection(ROOT_CLASS_HEADING)
        self.assertIn("每个 repair MUST 声明它处理的 root class", subsection)
        self.assertIn("可证伪的收敛证据", subsection)
        self.assertIn("该 root class 不再复现", subsection)

    def test_symptom_only_actions_are_not_repair_or_convergence(self) -> None:
        subsection = gate_subsection(ROOT_CLASS_HEADING)
        self.assertIn("让表象消失但不处理 root class 的动作不构成 repair，也不是收敛证据", subsection)
        for symptom_only in (
            "放宽/删除/跳过检查或断言",
            "把 required gate 改判为 `NOT_APPLICABLE`",
            "重写或重新解释既有 evidence",
            "只改文档/注释措辞",
            "只把 finding 标记为已处理",
        ):
            with self.subTest(symptom_only=symptom_only):
                self.assertIn(symptom_only, subsection)

    def test_root_class_outside_write_set_routes_to_its_owner(self) -> None:
        subsection = gate_subsection(ROOT_CLASS_HEADING)
        self.assertIn("当前 Task write set 之外的所有者", subsection)
        self.assertIn("MUST 把 repair 路由到该 owner 的既有路径", subsection)
        self.assertIn("MUST NOT 在同一 PR 内静默扩大 scope", subsection)
        self.assertIn("MUST NOT 就地重定义更高 authority", subsection)

    def test_repair_reuses_existing_routing_without_new_state(self) -> None:
        subsection = gate_subsection(ROOT_CLASS_HEADING)
        self.assertIn("本节不新增 route、workflow state 或 gate state", subsection)


class NonConvergenceEscalationTests(unittest.TestCase):
    """L3 positive case 4: non-converging repair escalates; no universal cap."""

    def test_non_convergence_is_defined_and_escalates(self) -> None:
        subsection = gate_subsection(NON_CONVERGENCE_HEADING)
        self.assertIn("即构成 non-converging", subsection)
        self.assertIn("MUST escalation/adjudication", subsection)
        self.assertIn("MUST NOT 无界循环", subsection)

    def test_escalation_is_decided_by_disposition_not_retry_count(self) -> None:
        subsection = gate_subsection(NON_CONVERGENCE_HEADING)
        self.assertIn("能否继续由 disposition 决定，MUST NOT 由重试计数决定", subsection)

    def test_no_universal_retry_cap_and_no_numeric_verdict(self) -> None:
        subsection = gate_subsection(NON_CONVERGENCE_HEADING)
        self.assertIn("不存在 universal retry cap", subsection)
        self.assertIn(
            "MUST NOT 独立地把 non-convergence 转成 `PASS`、`FAIL`、closeout 或 waiver",
            subsection,
        )
        self.assertIn("operational guard", subsection)

    def test_unbounded_retry_is_also_prohibited(self) -> None:
        subsection = gate_subsection(NON_CONVERGENCE_HEADING)
        self.assertIn("无限重试与无限等待被禁止", subsection)
        self.assertIn("一旦没有新的收敛证据，就必须 escalation", subsection)

    def test_repeated_attempts_cannot_produce_ready_or_pass(self) -> None:
        subsection = gate_subsection(NON_CONVERGENCE_HEADING)
        self.assertIn("没有新的收敛证据时，重复的 repair attempt MUST NOT 产生新的", subsection)
        self.assertIn("`IMPLEMENTATION_READY`", subsection)
        self.assertIn("`state:merge-ready`", subsection)


class OwnerBoundaryNegativeTests(unittest.TestCase):
    """L3 negative cases: no silent downgrade, no second state machine,
    no Product lifecycle redefinition, no Review finding/currentness takeover."""

    def test_no_new_gate_state_or_workflow_state_is_introduced(self) -> None:
        section = gate_authority_section()
        gate_states = set(re.findall(r"`(PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE)`", section))
        self.assertTrue(gate_states)
        self.assertTrue(gate_states <= CANONICAL_GATE_STATES, gate_states - CANONICAL_GATE_STATES)
        used_states = set(re.findall(r"state:([a-z-]+)", workflow()))
        self.assertTrue(used_states)
        self.assertTrue(
            used_states <= CANONICAL_WORKFLOW_STATES, used_states - CANONICAL_WORKFLOW_STATES
        )

    def test_no_arbitrary_retry_cap_marker_is_introduced(self) -> None:
        section = gate_authority_section()
        lowered = section.lower()
        for marker in RETRY_CAP_AUTHORITY_MARKERS:
            with self.subTest(marker=marker):
                self.assertNotIn(marker.lower(), lowered)
        for pattern in RETRY_CAP_AUTHORITY_PATTERNS:
            with self.subTest(pattern=pattern.pattern):
                self.assertIsNone(pattern.search(section))

    def test_product_lifecycle_semantics_are_not_redefined(self) -> None:
        section = gate_authority_section()
        for owned_term in PRODUCT_LIFECYCLE_OWNED_TERMS:
            with self.subTest(owned_term=owned_term):
                self.assertNotIn(owned_term, section)

    def test_review_finding_and_currentness_semantics_are_not_duplicated(self) -> None:
        section = gate_authority_section()
        for owned_term in REVIEW_FINDING_OWNED_TERMS:
            with self.subTest(owned_term=owned_term):
                self.assertNotIn(owned_term, section)

    def test_silent_downgrade_has_no_allowing_construction(self) -> None:
        section = gate_authority_section()
        self.assertNotIn("MAY 降级", section)
        self.assertNotIn("可以跳过 required", section)
        self.assertIn("只有 owning authority 的显式 disposition 才可改变 applicability", section)


class ValidationOwnerClarificationTests(unittest.TestCase):
    """VALIDATION_STANDARD owns exact-subject validation/currentness states;
    T04A clarifies only the owned `NOT_APPLICABLE` / re-run ambiguity."""

    def test_not_applicable_is_authority_derived_not_convenience(self) -> None:
        section = validation_purpose_section()
        self.assertIn(
            "`NOT_APPLICABLE` is an authority-derived determination about applicability, "
            "not an executor convenience.",
            section,
        )
        self.assertIn(
            "MUST NOT be produced from cost, effort/turnaround, change size/file count, "
            "a docs-only or mechanical appearance, Agent/model confidence, historical "
            "habit, or the absence of an objection.",
            section,
        )

    def test_ambiguous_applicability_does_not_become_not_applicable(self) -> None:
        section = validation_purpose_section()
        self.assertIn("When applicability is `UNKNOWN` or contradictory", section)
        self.assertIn("it remains not satisfied (`NOT_RUN`/`BLOCKED`)", section)
        self.assertIn("routes to the owning authority", section)
        self.assertIn("`DEVELOPMENT_WORKFLOW.md`", section)

    def test_canonical_gate_state_family_is_unchanged(self) -> None:
        section = validation_purpose_section()
        self.assertIn("PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE", section)
        invented = set(re.findall(r"`(ESCALATED|ADJUDICATED|CONVERGING|WAIVED|DEFERRED)`", section))
        self.assertFalse(invented, invented)

    def test_prohibited_practices_cover_applicability_rerun_and_bounds(self) -> None:
        section = validation_prohibited_section()
        for practice in (
            "recording a required gate as `NOT_APPLICABLE` from cost, effort/turnaround, "
            "change size/file count, docs-only or mechanical appearance, Agent/model "
            "confidence, historical habit or silence instead of authority",
            "re-running an unchanged subject without new evidence",
            "a later incidental `PASS` does not erase the recorded `FAIL`",
            "treating an arbitrary retry/timeout bound as a gate verdict",
            "as a substitute for escalating a non-converging repair to its owning authority",
        ):
            with self.subTest(practice=practice):
                self.assertIn(practice, section)

    def test_existing_prohibitions_are_preserved(self) -> None:
        section = validation_prohibited_section()
        for preserved in (
            "changing a required gate to optional to obtain READY",
            "unlimited retries/timeouts that mask deterministic defects",
            "claiming PASS without execution",
        ):
            with self.subTest(preserved=preserved):
                self.assertIn(preserved, section)


if __name__ == "__main__":
    import sys

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
