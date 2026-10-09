"""V410-T01B focused regression: Product evidence/research/review projections.

Encodes the `L3_WAVE_B_R1.md` V410-T01B positive/negative cases as deterministic
textual contract checks against the existing Product projection surfaces
`prompts/L1_PRODUCT_EVIDENCE.md` and `templates/research-issue.md`.

The projections must mirror the Stage-1 semantics settled by the integrated
V410-T01A owner (`standards/DEVELOPMENT_WORKFLOW.md`):

- L1 Product Evidence stays semantic framing/evidence, never synonymous with
  mandatory external Product Research;
- Product Research is selected only when existing/static evidence is
  insufficient, and records bounded purpose plus decision relevance;
- Product Research and Architecture Research stay distinct in purpose, timing
  and owner (R10 convergence, not a second research family);
- low-risk / sufficient-evidence work keeps a truthful compact/inline or
  `NO_RESEARCH_REQUIRED` path, without skipping policy-required evidence;
- Product Review stays risk/policy-selected evidence and can never manufacture
  Product Freeze.

Negative cases must reject mandatory research ceremony, Architecture Research
before Product Freeze, a second research lifecycle/authority, and Review PASS
manufacturing Product Freeze. Purely textual; no network, no runtime.
"""

from __future__ import annotations

import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

L1_PROMPT = "prompts/L1_PRODUCT_EVIDENCE.md"
RESEARCH_TEMPLATE = "templates/research-issue.md"
WORKFLOW_OWNER = "standards/DEVELOPMENT_WORKFLOW.md"

# Same canonical Stage-1 sequence the V410-T01A owner regression pins.
CANONICAL_PRODUCT_SEQUENCE = (
    "Idea/Intent",
    "Intake/Baseline",
    "semantic L1 Product Evidence",
    "Product Research",
    "Draft PRD / Scope",
    "selected Product Review",
    "Product Freeze",
)

STAGE1_HEADING = "### Stage 1 — Product / Scope"
STAGE2_HEADING = "### Stage 2 — Architecture / Task Definition"

# Sections required of every Research Issue by
# scripts/test_work_item_contract_and_golden_templates.py.
RESEARCH_TEMPLATE_REQUIRED_SECTIONS = (
    "Contract", "Research Question", "Authority / Inputs", "Scope",
    "Evidence Requirements", "Required Result", "Acceptance",
)

# Tokens that would signal an invented gate/lifecycle step or a second
# research authority family rather than a projection of existing owners.
INVENTED_LIFECYCLE_TOKENS = (
    "Research Freeze", "Research Gate", "Product Freeze Gate",
    "PRODUCT_RESEARCH_GATE", "RESEARCH_PASS_AS_FREEZE",
    "second Research authority", "second Product authority",
)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def md_section(text: str, heading: str) -> str:
    """Return the body of a markdown section up to the next same-level heading."""
    start = text.index(heading)
    rest = text[start + len(heading):]
    end = rest.find("\n## ")
    return rest[: end if end >= 0 else len(rest)]


def section_names(text: str) -> set[str]:
    return {
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE)
    }


def fenced_text_block(text: str, heading: str) -> str:
    section = md_section(text, heading)
    start = section.index("```text")
    end = section.index("```", start + len("```text"))
    return section[start:end]


def assert_canonical_order(block: str, label: str) -> None:
    """Reject a missing or reordered canonical Stage-1 step."""
    offsets = {term: block.find(term) for term in CANONICAL_PRODUCT_SEQUENCE}
    missing = sorted(term for term, offset in offsets.items() if offset < 0)
    assert not missing, f"{label}: missing canonical Stage-1 step(s): {missing}"
    actual = [term for term, _ in sorted(offsets.items(), key=lambda item: item[1])]
    assert actual == list(CANONICAL_PRODUCT_SEQUENCE), (
        f"{label}: canonical Stage-1 order violated: {actual}"
    )


def owner_stage1_sequence_block() -> str:
    return fenced_text_block(read(WORKFLOW_OWNER), STAGE1_HEADING)


def require_l1_is_semantic_not_mandatory_research(l1: str) -> None:
    """L3 positive 1: L1 is semantic framing/evidence, not mandatory research."""
    assert "**L1 是语义框架/证据步骤**" in l1, "L1 role sentence missing"
    assert "不得被坍缩为强制外部研究" in l1, "L1-to-mandatory-research collapse guard missing"
    assert "L1 不要求独立成文件" in l1, "L1 standalone-file freedom missing"


def require_l1_holds_no_product_authority(l1: str) -> None:
    """L3 positive 1/5: the L1 projection consumes authority, it does not hold it."""
    assert "执行面投影，不是语义 owner" in l1, "projection-not-owner declaration missing"
    for token in ("不持有 Product authority", "不产生 Product Freeze", "不构成第二产品权威"):
        assert token in l1, f"missing L1 authority boundary token: {token}"
    assert WORKFLOW_OWNER in l1, "projection does not cite the Stage-1 lifecycle owner"


def require_research_selection_is_proportional(l1: str, research_template: str) -> None:
    """L3 positive 2: selection is as-needed and proportional to the decision."""
    assert "仅当现有/静态证据不足以做出当前 PRD 决策时" in l1, "as-needed selection rule missing in L1 prompt"
    assert "范围与所需决策成比例" in l1, "proportional scope rule missing in L1 prompt"
    assert "as needed" in l1, "as-needed marker missing in L1 prompt"
    assert "Selection basis" in research_template, "bounded selection basis field missing in template"
    assert "不足" in l1 or "insufficient" in research_template, "evidence-insufficiency basis missing"


def require_purpose_typing_and_decision_relevance(l1: str, research_template: str) -> None:
    """L3 positive 2/3: research is purpose-typed and bound to a decision."""
    assert "PRODUCT_RESEARCH" in research_template, "product research purpose type missing"
    assert "ARCHITECTURE_RESEARCH" in research_template, "architecture research purpose type missing"
    assert "Decision relevance" in research_template, "decision relevance field missing"
    assert "有界 purpose" in l1, "bounded purpose requirement missing in L1 prompt"
    assert "decision relevance" in l1, "decision relevance requirement missing in L1 prompt"


def require_product_vs_architecture_separation(l1: str, research_template: str) -> None:
    """L3 positive 3: distinct purpose, timing and owner."""
    assert "**Product Research** 属于 **Stage 1**" in l1, "Product Research Stage-1 placement missing"
    assert "**Architecture Research / Research Demo** 属于 **Stage 2**" in l1, (
        "Architecture Research Stage-2 placement missing"
    )
    assert "standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md" in l1, "architecture research owner not cited"
    assert "不得把 Architecture Research / Demo 前移到 Product Freeze 之前" in l1, (
        "pre-Freeze architecture research guard missing in L1 prompt"
    )
    assert "MUST NOT be used before Product Freeze as product discovery" in research_template, (
        "pre-Freeze architecture research guard missing in research template"
    )
    assert "before** Product Freeze" in research_template or "before Product Freeze" in research_template, (
        "product research timing missing in research template"
    )


def require_truthful_not_required_path(l1: str, research_template: str) -> None:
    """L3 positive 4: truthful compact/inline or NO_RESEARCH_REQUIRED outcome."""
    for text, label in ((l1, "L1 prompt"), (research_template, "research template")):
        assert "NO_RESEARCH_REQUIRED" in text, f"NO_RESEARCH_REQUIRED path missing in {label}"
    assert "不得被强制加入独立 Product Research 或独立 Product Review" in l1, (
        "no-forced-research guard missing in L1 prompt"
    )
    assert "可以保持 compact/inline" in l1, "compact/inline legality missing in L1 prompt"
    assert "applicable policy 要求的证据不得因 compact/inline 而被跳过" in l1, (
        "policy-required-evidence guard missing in L1 prompt"
    )
    assert "MUST NOT be skipped" in research_template, "policy-required-evidence guard missing in template"
    for token in ("decided_subject=", "existing_evidence="):
        assert token in research_template, f"truthful not-required record field missing: {token}"


def require_review_is_evidence_not_freeze_authority(l1: str, research_template: str) -> None:
    """L3 positive 5 + negative: Review PASS cannot manufacture Product Freeze."""
    assert "按 applicable policy 与风险选择" in l1, "Product Review selection rule missing"
    assert "Product Review PASS 不能替代或自动产生 Product Freeze" in l1, (
        "Review PASS to Freeze separation missing in L1 prompt"
    )
    assert "是同一事件" in l1, "Product Freeze to existing PRD/Scope Freeze binding missing"
    assert "cannot be promoted by a Review" in research_template, (
        "Review PASS must not promote research conclusion in template"
    )
    assert "claims no Product Freeze" in research_template, (
        "freeze-authority acceptance guard missing in template"
    )


def require_no_mandatory_ceremony(l1: str, research_template: str) -> None:
    """L3 negative: mandatory research ceremony is rejected, not implied."""
    assert "不得为了形式制造 research ceremony" in l1, "anti-ceremony rule missing in L1 prompt"
    assert "Mandatory research ceremony is forbidden" in research_template, (
        "anti-ceremony rule missing in research template"
    )
    assert "fail closed" in l1 and "不得静默降级" in l1, "fail-closed applicability rule missing"


def require_no_second_research_lifecycle(l1: str, research_template: str) -> None:
    """L3 negative: one research family over existing owners, no second lifecycle."""
    assert "不合并为第二个 Research authority" in l1, "second-research-authority guard missing in L1 prompt"
    assert "No second Research lifecycle/authority is created by this template." in research_template, (
        "second-lifecycle declaration missing in research template"
    )
    assert "projection of `standards/DEVELOPMENT_WORKFLOW.md`" in research_template, (
        "research template does not declare its projection boundary"
    )
    for text, label in ((l1, "L1 prompt"), (research_template, "research template")):
        assert "state:" not in text, f"{label} introduces workflow-state vocabulary"
        for token in INVENTED_LIFECYCLE_TOKENS:
            assert token not in text, f"{label} invents lifecycle/authority token: {token}"


def require_standards_product_considerations(l1: str) -> None:
    """Frozen PRD §15: standards/governance products keep the extra L1 inputs."""
    for token in (
        "现有 normative owner",
        "dogfood",
        "compatibility / SemVer",
        "duplicate authority",
        "不引入新的研究家族",
    ):
        assert token in l1, f"missing standards-product L1 consideration: {token}"


def require_projection_sequence_converges(l1: str) -> None:
    """R10 convergence: the projection repeats the owner sequence, unchanged."""
    owner_block = owner_stage1_sequence_block()
    projection_block = fenced_text_block(l1, "## 生命周期位置与投影边界")
    for label, block in (("owner", owner_block), ("projection", projection_block)):
        assert_canonical_order(block, label)
    assert "Architecture" not in owner_block, "owner Stage-1 sequence must not contain Architecture"
    assert "Architecture" not in projection_block, (
        "projection Stage-1 sequence must not contain Architecture"
    )
    assert "Product Research（as needed）" in l1, "as-needed qualifier must survive projection"


def require_research_template_contract_sections(research_template: str) -> None:
    """The projection is additive: existing contract sections must survive."""
    missing = sorted(set(RESEARCH_TEMPLATE_REQUIRED_SECTIONS) - section_names(research_template))
    assert not missing, f"research template lost required contract section(s): {missing}"


def l1_text() -> str:
    return read(L1_PROMPT)


def template_text() -> str:
    return read(RESEARCH_TEMPLATE)


class ProductEvidenceProjectionPositiveTests(unittest.TestCase):
    """L3 positive cases 1-5 over the two projection surfaces."""

    def test_l1_is_semantic_framing_not_mandatory_external_research(self) -> None:
        require_l1_is_semantic_not_mandatory_research(l1_text())

    def test_l1_projection_holds_no_product_authority_or_freeze_effect(self) -> None:
        require_l1_holds_no_product_authority(l1_text())

    def test_product_research_selection_is_as_needed_and_proportional(self) -> None:
        require_research_selection_is_proportional(l1_text(), template_text())

    def test_research_is_purpose_typed_with_bounded_decision_relevance(self) -> None:
        require_purpose_typing_and_decision_relevance(l1_text(), template_text())

    def test_product_and_architecture_research_stay_distinct(self) -> None:
        require_product_vs_architecture_separation(l1_text(), template_text())

    def test_low_risk_sufficient_evidence_keeps_truthful_inline_path(self) -> None:
        require_truthful_not_required_path(l1_text(), template_text())

    def test_product_review_is_selected_evidence_not_freeze_authority(self) -> None:
        require_review_is_evidence_not_freeze_authority(l1_text(), template_text())

    def test_projection_sequence_converges_on_the_stage1_owner(self) -> None:
        require_projection_sequence_converges(l1_text())

    def test_standards_product_l1_considerations_survive_projection(self) -> None:
        require_standards_product_considerations(l1_text())


class ProductEvidenceProjectionNegativeTests(unittest.TestCase):
    """L3 negative cases: the oracles must reject weakened projections."""

    def test_negative_mandatory_research_ceremony_is_rejected(self) -> None:
        require_no_mandatory_ceremony(l1_text(), template_text())

        stripped = l1_text().replace("不得为了形式制造 research ceremony", "")
        self.assertNotEqual(stripped, l1_text(), "ceremony mutation fixture did not match")
        with self.assertRaises(AssertionError):
            require_no_mandatory_ceremony(stripped, template_text())

    def test_negative_architecture_research_before_product_freeze_is_rejected(self) -> None:
        require_product_vs_architecture_separation(l1_text(), template_text())

        weakened = l1_text().replace("不得把 Architecture Research / Demo 前移到 Product Freeze 之前", "")
        self.assertNotEqual(weakened, l1_text(), "pre-Freeze mutation fixture did not match")
        with self.assertRaises(AssertionError):
            require_product_vs_architecture_separation(weakened, template_text())

    def test_negative_second_research_lifecycle_is_rejected(self) -> None:
        require_no_second_research_lifecycle(l1_text(), template_text())

        duplicated = template_text().replace(
            "No second Research lifecycle/authority is created by this template.", ""
        )
        self.assertNotEqual(duplicated, template_text(), "second-lifecycle mutation fixture did not match")
        with self.assertRaises(AssertionError):
            require_no_second_research_lifecycle(l1_text(), duplicated)

        invented = l1_text() + "\nResearch Freeze 由 Research 结论自动产生。\n"
        with self.assertRaises(AssertionError):
            require_no_second_research_lifecycle(invented, template_text())

    def test_negative_review_pass_manufacturing_freeze_is_rejected(self) -> None:
        require_review_is_evidence_not_freeze_authority(l1_text(), template_text())

        manufacturing = l1_text().replace(
            "Product Review PASS 不能替代或自动产生 Product Freeze", "Product Review PASS 即 Product Freeze"
        )
        self.assertNotEqual(manufacturing, l1_text(), "Review-PASS mutation fixture did not match")
        with self.assertRaises(AssertionError):
            require_review_is_evidence_not_freeze_authority(manufacturing, template_text())

        acceptance = template_text().replace(
            "- [ ] conclusion claims no Product Freeze", "- [ ] Review PASS authorizes Product Freeze"
        )
        self.assertNotEqual(acceptance, template_text(), "template acceptance mutation fixture did not match")
        with self.assertRaises(AssertionError):
            require_review_is_evidence_not_freeze_authority(l1_text(), acceptance)

    def test_negative_sequence_reordering_or_architecture_insertion_is_rejected(self) -> None:
        projection_block = fenced_text_block(l1_text(), "## 生命周期位置与投影边界")
        assert_canonical_order(projection_block, "baseline projection")

        reordered = projection_block.replace(
            "→ semantic L1 Product Evidence\n→ Product Research（as needed）",
            "→ Product Research（as needed）\n→ semantic L1 Product Evidence",
        )
        self.assertNotEqual(reordered, projection_block, "reorder mutation fixture did not match")
        with self.assertRaises(AssertionError):
            assert_canonical_order(reordered, "reordered projection")

        with_architecture = projection_block + "\n→ Architecture Research\n"
        with self.assertRaises(AssertionError):
            self.assertNotIn("Architecture", with_architecture, "Architecture entered the Stage-1 sequence")

    def test_negative_mandatory_research_collapse_is_rejected(self) -> None:
        require_l1_is_semantic_not_mandatory_research(l1_text())

        collapsed = l1_text().replace("不得被坍缩为强制外部研究", "即为强制外部研究")
        self.assertNotEqual(collapsed, l1_text(), "L1 collapse mutation fixture did not match")
        with self.assertRaises(AssertionError):
            require_l1_is_semantic_not_mandatory_research(collapsed)


class ResearchTemplateProjectionTests(unittest.TestCase):
    """The Research template keeps its contract and gains only additive projections."""

    def test_required_contract_sections_survive(self) -> None:
        require_research_template_contract_sections(template_text())

    def test_additive_lifecycle_binding_sections_present(self) -> None:
        names = section_names(template_text())
        for heading in ("Lifecycle Binding", "Proportionality / Not-Required Outcome"):
            self.assertIn(heading, names, f"missing additive projection section: {heading}")

    def test_proportionality_section_is_not_a_gate(self) -> None:
        section = md_section(template_text(), "## Proportionality / Not-Required Outcome")
        self.assertIn("MUST NOT be skipped", section)
        self.assertIn("forbidden", section)

    def test_lifecycle_binding_declares_owner_and_timing(self) -> None:
        section = md_section(template_text(), "## Lifecycle Binding")
        self.assertIn("standards/DEVELOPMENT_WORKFLOW.md", section)
        self.assertIn("standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md", section)
        self.assertIn("**before** Product Freeze", section)
        self.assertIn("**after** Product Freeze", section)


if __name__ == "__main__":
    import sys

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
