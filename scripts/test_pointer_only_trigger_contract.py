from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def render_trigger(
    repository: str,
    number: int,
    *,
    work_item: str = "Issue",
    role: str | None = None,
    durable_contract_complete: bool,
    new_task_instruction_persisted: bool = True,
) -> str:
    """Reference conformance oracle for user-visible task invocation.

    This is intentionally not a runtime scheduler. It encodes only the normative
    admission rule introduced by v3.4 T-011: materialize task-specific facts first,
    then emit a pointer-only trigger.
    """
    if not durable_contract_complete:
        raise ValueError("DURABLE_CONTRACT_INCOMPLETE")
    if not new_task_instruction_persisted:
        raise ValueError("TASK_INSTRUCTION_NOT_PERSISTED")
    if role:
        return f"执行 `{repository}` {work_item} #{number} 的当前 READY {role} dispatch。"
    return f"完成 `{repository}` {work_item} #{number}。"


FORBIDDEN_TASK_DETAIL_PATTERNS = (
    r"\b[0-9a-f]{40}\b",
    r"\b(?:rebase|refresh|checkout|cherry-pick)\b",
    r"\b(?:npm|pnpm|yarn|pytest|python|go test|cargo test)\b",
    r"\b(?:acceptance|forbidden scope|allowed changes|required gates?|closeout)\b",
)


def is_pointer_only(trigger: str) -> bool:
    if len(trigger.splitlines()) > 2:
        return False
    lowered = trigger.lower()
    return not any(re.search(pattern, lowered, re.IGNORECASE) for pattern in FORBIDDEN_TASK_DETAIL_PATTERNS)


class NormativeSurfaceTests(unittest.TestCase):
    def test_issue_first_is_must_level_and_removes_permissive_wording(self) -> None:
        text = read("standards/ISSUE_FIRST_TASK_TRIGGER.md")
        required = (
            "user-visible ChatGPT Web trigger = pointer only",
            "No durable contract -> no trigger.",
            "No Issue update -> no new task-specific instruction in chat.",
            "The user-visible/copyable task trigger MUST be pointer-only.",
            "If the Issue is incomplete, the dispatcher MUST repair/materialize the Issue",
            "one task = one Issue = one trigger prompt",
            "LOCAL_AGENT_PROMPT.md",
            "MUST NOT copy an Execution Pack prompt artifact into chat",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, text)

        forbidden = (
            "The Issue SHOULD contain all task-specific information needed to execute the work",
            "A trigger prompt SHOULD be as short as practical",
            "Additional bootstrap text is allowed only when the executor needs information",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, text)

    def test_local_handoff_requires_durable_completeness_before_trigger(self) -> None:
        protocol = read("standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md")
        template = read("templates/local-agent-handoff-issue.md")
        for text in (protocol, template):
            self.assertIn("No durable contract -> no trigger.", protocol)
            self.assertIn("pointer-only", text.lower())
            self.assertIn("MUST NOT", text)
        self.assertIn("An incomplete Issue MUST be repaired before invocation", template)

    def test_execution_pack_prompt_is_not_user_visible_trigger(self) -> None:
        readme = read("templates/execution-pack/README.md")
        self.assertIn("durable repository artifact", readme)
        self.assertIn("not the user-visible ChatGPT Web handoff trigger", readme)
        self.assertIn("MUST NOT be copied into chat", readme)

    def test_existing_web_and_interaction_authority_points_to_github_facts(self) -> None:
        web_role = read("standards/CHATGPT_WEB_ROLE.md")
        interaction = read("standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md")
        self.assertIn("任务特定事实必须进入 GitHub Issue", web_role)
        self.assertIn("GitHub carries durable execution facts.", interaction)
        self.assertIn("A handoff becomes dispatchable only after its durable Issue contract is complete", interaction)
        self.assertIn("Pointer-only invocation applies to every role", interaction)


class EmissionConformanceTests(unittest.TestCase):
    def test_complete_issue_emits_only_pointer(self) -> None:
        trigger = render_trigger(
            "owner/repo",
            123,
            durable_contract_complete=True,
        )
        self.assertEqual(trigger, "完成 `owner/repo` Issue #123。")
        self.assertTrue(is_pointer_only(trigger))

    def test_role_dispatch_pointer_is_allowed(self) -> None:
        trigger = render_trigger(
            "owner/repo",
            123,
            role="validation",
            durable_contract_complete=True,
        )
        self.assertEqual(trigger, "执行 `owner/repo` Issue #123 的当前 READY validation dispatch。")
        self.assertTrue(is_pointer_only(trigger))

    def test_incomplete_issue_must_be_materialized_not_expanded_prompt(self) -> None:
        with self.assertRaisesRegex(ValueError, "DURABLE_CONTRACT_INCOMPLETE"):
            render_trigger("owner/repo", 123, durable_contract_complete=False)

        bad_fallback = (
            "完成 owner/repo Issue #123。\n"
            "先 refresh 到 current base，再运行 npm test，然后按 acceptance 完成 closeout。"
        )
        self.assertFalse(is_pointer_only(bad_fallback))

    def test_changed_requirement_must_be_persisted_before_same_short_trigger(self) -> None:
        original = render_trigger("owner/repo", 123, durable_contract_complete=True)
        with self.assertRaisesRegex(ValueError, "TASK_INSTRUCTION_NOT_PERSISTED"):
            render_trigger(
                "owner/repo",
                123,
                durable_contract_complete=True,
                new_task_instruction_persisted=False,
            )
        after_issue_update = render_trigger(
            "owner/repo",
            123,
            durable_contract_complete=True,
            new_task_instruction_persisted=True,
        )
        self.assertEqual(after_issue_update, original)

    def test_task_specific_sha_branch_commands_gates_are_nonconformant(self) -> None:
        samples = (
            "完成 owner/repo Issue #1，baseline aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa。",
            "完成 owner/repo Issue #1，然后 rebase 到 version/v3.4.0。",
            "完成 owner/repo Issue #1，并运行 pytest。",
            "完成 owner/repo Issue #1，required gates 全部 PASS 后 closeout。",
        )
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertFalse(is_pointer_only(sample))


if __name__ == "__main__":
    unittest.main()
