"""V410-T01A focused regression: canonical Stage-1 lifecycle semantics.

Encodes the L3_WAVE_A_R1.md V410-T01A positive/negative cases as
deterministic textual contract checks against the lifecycle owner
`standards/DEVELOPMENT_WORKFLOW.md`. Purely textual; no network, no runtime.
"""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_SEQUENCE = (
    "Idea/Intent",
    "Intake/Baseline",
    "semantic L1 Product Evidence",
    "Product Research",
    "Draft PRD / Scope",
    "selected Product Review",
    "Product Freeze",
)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def stage1_section() -> str:
    text = read("standards/DEVELOPMENT_WORKFLOW.md")
    start = text.index("### Stage 1 — Product / Scope")
    end = text.index("### Stage 2 — Architecture / Task Definition")
    return text[start:end]


def canonical_sequence_block() -> str:
    section = stage1_section()
    start = section.index("```text")
    end = section.index("```", start + len("```text"))
    return section[start:end]


class Stage1CanonicalSequenceTests(unittest.TestCase):
    """L3 positive cases 1-3."""

    def test_material_scope_can_reconstruct_canonical_sequence_in_order(self) -> None:
        block = canonical_sequence_block()
        pos = 0
        for term in CANONICAL_SEQUENCE:
            with self.subTest(term=term):
                i = block.index(term, pos)
                pos = i + len(term)

    def test_product_review_is_evidence_judgment_and_freeze_is_authority_act(self) -> None:
        section = stage1_section()
        self.assertIn("独立 evidence/judgment", section)
        self.assertIn("Product authority 的显式冻结行为", section)

    def test_product_research_is_as_needed_and_not_a_second_authority(self) -> None:
        section = stage1_section()
        self.assertIn("as needed", section)
        self.assertIn("不持有 Product authority", section)
        self.assertIn("不构成第二产品权威", section)

    def test_product_unknown_disposition_belongs_to_research_stage(self) -> None:
        section = stage1_section()
        self.assertIn("disposition", section)


class Stage1NegativeInvariantTests(unittest.TestCase):
    """L3 negative cases 1-4."""

    def test_low_risk_sufficient_evidence_not_forced_into_research_or_review(self) -> None:
        section = stage1_section()
        self.assertIn("不得被强制加入独立 Product Research 或独立 Product Review", section)
        self.assertIn("可以保持 compact/inline", section)
        # L2 4.1: semantic authority/evidence required by applicable policy may not be skipped
        self.assertIn("applicable policy 要求的语义权威/证据不得因 compact/inline 而被跳过", section)
        workflow = read("standards/DEVELOPMENT_WORKFLOW.md")
        self.assertIn("可跳过 L1/L2/L3", workflow)

    def test_l1_not_collapsed_into_mandatory_external_research(self) -> None:
        section = stage1_section()
        self.assertIn("不得被坍缩为强制外部研究", section)

    def test_architecture_research_stays_on_post_freeze_path(self) -> None:
        section = stage1_section()
        self.assertIn("不得前移到 Product Freeze 之前", section)
        self.assertNotIn("Architecture", canonical_sequence_block())

    def test_review_pass_alone_cannot_manufacture_product_freeze(self) -> None:
        section = stage1_section()
        self.assertIn("Product Review PASS", section)
        self.assertIn("本身不产生冻结效力", section)


class Stage1OwnerBoundaryTests(unittest.TestCase):
    """DOD: no second lifecycle/state/authority family; owner convergence only."""

    def test_stage1_introduces_no_new_state_machine(self) -> None:
        self.assertNotIn("state:", stage1_section())

    def test_product_freeze_bound_to_existing_prd_freeze(self) -> None:
        section = stage1_section()
        self.assertIn("是同一事件", section)
        self.assertIn("不是新增 gate", section)

    def test_product_review_not_a_universal_gate(self) -> None:
        section = stage1_section()
        self.assertIn("不是 universal Product Review gate", section)
        self.assertIn("可选择或省略", section)

    def test_unknown_applicability_fails_closed(self) -> None:
        section = stage1_section()
        self.assertIn("fail closed", section)
        self.assertIn("不得静默降级", section)


if __name__ == "__main__":
    import sys

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
