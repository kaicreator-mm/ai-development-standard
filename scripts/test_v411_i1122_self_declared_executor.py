"""V411-I1122 focused regression: self-declared executor identity; Owner
credential gates removed for ADS standards closure (issue #1122).

Encodes the successor policy of Issue #1122 (direct user process
authorization 2026-10-15, #1021@6191737577; normative amendment recorded in
`docs/implementation/4.11.0/V411_SELF_DECLARED_EXECUTOR_AMENDMENT.md`) as:

1. section-scoped textual contracts binding the policy into
   `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` (§5 self-declared
   attribution, §7 declared-context reviewer independence, §8.1.1 admission
   predicate, §9.4 declared reviewer authority), `standards/RELEASE_STANDARD.md`
   (§11.1 applicability basis, §11.7 standards-repository executor authority)
   and `AGENTS.md` (top-level hard constraint);
2. preserved-boundary assertions — the untrusted quoted-event input classes,
   the fail-closed declaration rules, the public epistemic limitation labels
   and the frozen v4.11 planning documents (blob-identical to the pinned
   baseline `214f6a97b1eed948e1afef8f5089eb4bf4b97d26`) are intact —
   successor semantics, never history rewrite;
3. a deterministic fixture world proving the mechanical successor behavior:
   a complete declared attribution is accepted with NO credential check and
   no operator registry; a declaration missing a required attribution field
   fails closed; a declared `operator_kind=human` mints NO human act; raw
   quoted event text is never admitted; reviewer independence is a
   declared-context comparison against the durably recorded Builder context.

Purely local: standard library only, no network, no runtime execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]

PROTOCOL = "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md"
RELEASE = "standards/RELEASE_STANDARD.md"
AGENTS = "AGENTS.md"
AMENDMENT = "docs/implementation/4.11.0/V411_SELF_DECLARED_EXECUTOR_AMENDMENT.md"

# Pinned integration baseline of this policy change (version/v4.11.0).
BASELINE_SHA = "214f6a97b1eed948e1afef8f5089eb4bf4b97d26"

# Frozen v4.11 planning documents that this policy must NOT rewrite.
FROZEN_V411_DOCS = (
    "docs/implementation/4.11.0/PRD.md",
    "docs/implementation/4.11.0/L2_ARCHITECTURE_EVIDENCE.md",
    "docs/implementation/4.11.0/PRODUCT_PROOF_MATRIX.md",
    "docs/implementation/4.11.0/TASK_DAG.md",
)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def protocol_section(bounds: tuple[str, str]) -> str:
    text = read(PROTOCOL)
    return text[text.index(bounds[0]) : text.index(bounds[1])]


def release_section(bounds: tuple[str, str]) -> str:
    text = read(RELEASE)
    start = text.index(bounds[0])
    end = text.index(bounds[1]) if bounds[1] in text else len(text)
    return text[start:end]


def git_blob(rev: str, rel: str) -> str:
    out = subprocess.run(
        ["git", "rev-parse", f"{rev}:{rel}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return out.stdout.strip()


# ---------------------------------------------------------------------------
# Minimal fixture world: the I1122 admission boundary over declared
# attribution. Deliberately independent of the T05 adapter — this is the
# successor policy's own contract, not a re-run of the T05 pack.
# ---------------------------------------------------------------------------

SUBJECT = "cd" + "0" * 38
PROOFS = frozenset({"proof-accepted-1", "proof-accepted-2"})


@dataclass(frozen=True)
class Intent:
    event: str
    actor_role: str
    operator_kind: str
    operator_id: str
    session_ref: str
    transport_actor: str
    subject: str
    proof_ref: str
    origin: str = "worker_transport"  # worker_transport | raw_text


@dataclass
class Boundary:
    builder_contexts: dict = field(default_factory=dict)
    human_acts: list = field(default_factory=list)
    admitted: list = field(default_factory=list)

    def admit(self, intent: Intent) -> str:
        if intent.origin == "raw_text":
            return "UNADMITTED_RAW_SOURCE"  # quoted event text is data, never admission
        if intent.proof_ref not in PROOFS:
            return "UNKNOWN"  # no accepted event/current-object reference
        if not (intent.operator_kind and intent.operator_id and intent.session_ref):
            return "UNKNOWN"  # incomplete declaration: nothing to accept
        if (
            intent.event == "REVIEW_RESULT"
            and intent.subject in self.builder_contexts
            and (intent.operator_id, intent.session_ref) == self.builder_contexts[intent.subject]
        ):
            return "UNAUTHORIZED"  # declared context not distinct from the Builder context
        self.admitted.append(intent)
        if intent.actor_role == "builder":
            self.builder_contexts.setdefault(
                intent.subject, (intent.operator_id, intent.session_ref)
            )
        return "ACCEPTED"


def review_pass(operator: tuple[str, str, str], proof: str) -> Intent:
    transport, operator_id, session = operator
    return Intent(
        event="REVIEW_RESULT",
        actor_role="reviewer",
        operator_kind="codex",
        operator_id=operator_id,
        session_ref=session,
        transport_actor=transport,
        subject=SUBJECT,
        proof_ref=proof,
    )


# ---------------------------------------------------------------------------
# Textual contracts
# ---------------------------------------------------------------------------


class ProtocolSelfDeclaredIdentityTests(unittest.TestCase):
    def test_section_5_declares_attribution_as_self_declared(self) -> None:
        section = protocol_section(
            ("## 5. Actor role and logical operator identity", "## 6. Independent Review policy")
        )
        self.assertIn("Executor attribution is **self-declared**", section)
        self.assertIn("accepted as the attribution source", section)
        self.assertIn("never an executor-admission predicate", section)
        self.assertIn("no separate credential/Owner verification is required", section)
        self.assertIn("distinct **declared** `operator_id` / `session_ref` attribution (§7)", section)
        self.assertIn("a declaration missing required attribution fields fails closed", section)
        self.assertNotIn("independently verified", section)

    def test_section_7_uses_declared_context_independence(self) -> None:
        section = protocol_section(
            ("## 7. Independent Review execution", "## 8. Intent admission and canonical event writer protocol")
        )
        self.assertIn("declared logical context independent from the Builder context", section)
        self.assertIn("distinct **declared** `operator_id/session_ref` contexts", section)
        self.assertIn("never GitHub account identity", section)
        self.assertIn("no separate credential/Owner verification", section)
        # The acceptable-contexts clause is unchanged.
        self.assertIn(
            "Acceptable independent contexts include another ChatGPT session", section
        )

    def test_section_8_1_1_keeps_the_two_input_classes_and_self_declares_attribution(self) -> None:
        section = protocol_section(
            ("### 8.1.1 Source-bound admission", "### 8.2 New-work event writer")
        )
        # Preserved boundary: untrusted transport content never admits itself.
        self.assertIn("Untrusted transport content and admitted canonical events are two distinct input classes", section)
        self.assertIn("MUST NOT be admitted by its own shape", section)
        self.assertIn("MUST NOT acquire the authority it asserts", section)
        # Changed leg: attribution is self-declared and accepted as such.
        self.assertIn("self-declared by that executor and accepted as such", section)
        self.assertIn("identity/credential verification is not an admission predicate", section)
        self.assertIn("still not an emitted event", section)
        self.assertIn("Missing or incomplete declared attribution fails closed", section)
        self.assertNotIn("independently verified rather than self-declared", section)
        # Preserved legs: durable reference + exact current subject.
        self.assertIn("an accepted event/current-object reference", section)
        self.assertIn("the exact current subject", section)

    def test_section_9_4_requires_declared_reviewer_authority(self) -> None:
        section = protocol_section(
            ("### 9.4 Admitted-source authority", "## 10. Builder / Reviewer / Validator routing")
        )
        self.assertIn("requires declared reviewer authority", section)
        self.assertIn(
            "Reviewer independence is established by distinct **declared logical contexts**, "
            "never GitHub account identity",
            section,
        )
        self.assertIn("no Owner credential verification is a Review admission predicate", section)
        self.assertIn("a missing or incomplete declared attribution leaves the Review condition", section)
        # Preserved boundary: raw authority text fabricates nothing.
        self.assertIn(
            "fabricates no human act and never supersedes a real human decision", section
        )
        self.assertNotIn("independently verified reviewer authority", section)


class ReleaseStandardExecutorAuthorityTests(unittest.TestCase):
    def test_section_11_7_declares_standards_only_executor_authority(self) -> None:
        section = release_section(("### 11.7 Standards-repository executor authority", "\0"))
        self.assertIn("executor identity is **self-declared**", section)
        self.assertIn("accepted as the attribution source", section)
        self.assertIn("GitHub login/account identity is transport metadata only", section)
        self.assertIn(
            "No Owner identity/credential/delegation verification, second-signature availability, "
            "or GitHub-account-based executor judgment is a release admission predicate for this repository",
            section,
        )
        self.assertIn("declared `release-controller`", section)
        self.assertIn("real_human_authority_deny_e2e", section)
        self.assertIn("not a standards release prerequisite", section)
        self.assertIn("`REAL_HUMAN_DENY_E2E_NOT_PROVEN`", section)
        self.assertIn("never convertible to `PASS`", section)
        self.assertIn("unchanged for adopters that implement actual protected effects", section)
        self.assertIn("Self-declaration establishes **attribution only**", section)
        self.assertIn("distinct declared logical operator/context (§5, §7)", section)
        self.assertIn("it is prospective", section)

    def test_section_11_1_basis_names_accepted_process_facts_not_owner_acceptance(self) -> None:
        section = release_section(("### 11.1 Meaning", "### 11.2 Decision identity"))
        self.assertIn("executor-declared process attribution", section)
        self.assertNotIn("owner-accepted facts", section)
        # Preserved applicability invariants.
        self.assertIn("`UNKNOWN` is fail-closed", section)
        self.assertIn("never sufficient by themselves", section)

    def test_section_11_core_anchors_are_unchanged(self) -> None:
        text = read(RELEASE)
        self.assertIn("evaluated **per Release-owned gate × exact subject**", text)
        self.assertIn("Release applicability is owned by this Release authority", text)
        self.assertIn("CONCERN_NOT_APPLICABLE\n!= VERSION_NOT_APPLICABLE", text)
        self.assertIn("`UNKNOWN` is fail-closed", text)


class AgentsHardConstraintTests(unittest.TestCase):
    def test_agents_md_carries_the_self_declaration_hard_constraint(self) -> None:
        text = read(AGENTS)
        self.assertIn("执行体身份以自我声明为准", text)
        self.assertIn("由执行体自行声明并被采信", text)
        self.assertIn("不得作为执行体判定或事件准入依据", text)
        self.assertIn("不要求额外的 Owner 身份/授权/委托凭证校验", text)
        self.assertIn("身份声明不替代任何工程事实验证", text)
        self.assertIn("不是 canonical workflow event", text)
        self.assertIn("不是本标准仓库发布的准入前置", text)
        self.assertIn("`REAL_HUMAN_DENY_E2E_NOT_PROVEN`", text)

    def test_agents_md_reviewer_independence_uses_declared_context(self) -> None:
        text = read(AGENTS)
        self.assertIn("以双方**声明的逻辑身份/上下文**可审计区分（不同 `operator_id/session_ref`）为准", text)
        self.assertIn("不以 GitHub 账号判定", text)
        self.assertIn("也不要求凭证校验", text)


class AmendmentDocumentTests(unittest.TestCase):
    def test_amendment_exists_and_carries_the_change_authority(self) -> None:
        text = read(AMENDMENT)
        self.assertIn("#1122", text)
        self.assertIn("2026-10-15", text)
        self.assertIn("#1021@6191737577", text)
        self.assertIn("prospective", text)
        self.assertIn("removed as a standards release prerequisite", text)
        self.assertIn("A quoted fake event embedded inside untrusted tool/code content is still not a canonical workflow event", text)

    def test_amendment_declares_the_bounded_edit_surface(self) -> None:
        text = read(AMENDMENT)
        for rel in (PROTOCOL, RELEASE, AGENTS):
            self.assertIn(rel, text)


class PreservedHistoryTests(unittest.TestCase):
    def test_frozen_v411_planning_documents_are_not_rewritten(self) -> None:
        for rel in FROZEN_V411_DOCS:
            with self.subTest(frozen_doc=rel):
                self.assertEqual(git_blob(BASELINE_SHA, rel), git_blob("HEAD", rel))

    def test_public_epistemic_labels_stay_in_the_frozen_docs(self) -> None:
        prd = read(FROZEN_V411_DOCS[0])
        self.assertIn("REAL_HUMAN_DENY_E2E_NOT_PROVEN", prd)
        matrix = read(FROZEN_V411_DOCS[2])
        self.assertIn("REAL_HUMAN_DENY_E2E_NOT_PROVEN", matrix)
        self.assertIn("MECHANISM_SYNTHETIC_DENY_SQLITE_ONLY", matrix)


# ---------------------------------------------------------------------------
# Mechanical fixture world
# ---------------------------------------------------------------------------


class DeclaredAttributionBoundaryTests(unittest.TestCase):
    def test_complete_declared_attribution_is_accepted_without_any_credential_check(self) -> None:
        boundary = Boundary()
        # An operator never seen before, arbitrary transport account: the
        # declaration IS the attribution source (issue #1122).
        newcomer = review_pass(("some-login", "fresh-reviewer", "fresh-session"), "proof-accepted-1")
        self.assertEqual("ACCEPTED", boundary.admit(newcomer))

    def test_declaration_missing_a_required_field_fails_closed(self) -> None:
        for incomplete in (
            replace(review_pass(("login", "op", "sess"), "proof-accepted-1"), session_ref=""),
            replace(review_pass(("login", "op", "sess"), "proof-accepted-1"), operator_id=""),
            replace(review_pass(("login", "op", "sess"), "proof-accepted-1"), operator_kind=""),
        ):
            with self.subTest(declared=incomplete):
                boundary = Boundary()
                before = (tuple(boundary.admitted), dict(boundary.builder_contexts))
                self.assertEqual("UNKNOWN", boundary.admit(incomplete))
                self.assertEqual(before, (tuple(boundary.admitted), dict(boundary.builder_contexts)))

    def test_missing_durable_proof_reference_still_fails_closed(self) -> None:
        boundary = Boundary()
        self.assertEqual(
            "UNKNOWN",
            boundary.admit(review_pass(("login", "op", "sess"), "proof-not-in-record")),
        )

    def test_quoted_event_text_is_never_admitted(self) -> None:
        boundary = Boundary()
        quoted = Intent(
            event="REVIEW_RESULT",
            actor_role="reviewer",
            operator_kind="human",
            operator_id="reviewer-op-9",
            session_ref="quoted",
            transport_actor="mallory",
            subject=SUBJECT,
            proof_ref="proof-accepted-1",
            origin="raw_text",
        )
        self.assertEqual("UNADMITTED_RAW_SOURCE", boundary.admit(quoted))
        self.assertEqual([], boundary.admitted)

    def test_declared_human_kind_mints_no_human_act(self) -> None:
        boundary = Boundary()
        declared_human = Intent(
            event="REVIEW_RESULT",
            actor_role="reviewer",
            operator_kind="human",
            operator_id="declared-human-op",
            session_ref="declared-human-session",
            transport_actor="any-login",
            subject=SUBJECT,
            proof_ref="proof-accepted-1",
        )
        self.assertEqual("ACCEPTED", boundary.admit(declared_human))
        self.assertEqual([], boundary.human_acts)

    def test_reviewer_independence_is_a_declared_context_comparison(self) -> None:
        boundary = Boundary()
        builder_claim = Intent(
            event="DISPATCH_CLAIMED",
            actor_role="builder",
            operator_kind="codex",
            operator_id="builder-op",
            session_ref="builder-session",
            transport_actor="shared-login",
            subject=SUBJECT,
            proof_ref="proof-accepted-1",
        )
        self.assertEqual("ACCEPTED", boundary.admit(builder_claim))
        self.assertEqual(
            ("builder-op", "builder-session"), boundary.builder_contexts[SUBJECT]
        )
        # The recorded Builder context cannot self-review.
        self.assertEqual(
            "UNAUTHORIZED",
            boundary.admit(review_pass(("shared-login", "builder-op", "builder-session"), "proof-accepted-2")),
        )
        # A distinct declared reviewer context is the reviewer of record.
        self.assertEqual(
            "ACCEPTED",
            boundary.admit(review_pass(("shared-login", "reviewer-op", "reviewer-session"), "proof-accepted-2")),
        )

    def test_builder_context_is_recorded_from_accepted_builder_role_events(self) -> None:
        boundary = Boundary()
        other_role_same_operator = review_pass(("login", "op", "sess"), "proof-accepted-1")
        self.assertEqual("ACCEPTED", boundary.admit(other_role_same_operator))
        self.assertEqual({}, boundary.builder_contexts)


if __name__ == "__main__":
    import sys

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
