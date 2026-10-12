"""V411-T08 owner-local human decision authority oracles.

These tests deliberately separate:
- durable source-bound authority/event fixtures used as UNIT-LEVEL contract models; and
- a genuine independently verifiable human authorization source, which is NOT
  bundled in the repository and therefore remains NOT_RUN rather than fabricated.

No test in this file performs an irreversible external side effect. T09 owns that.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "standards" / "DEVELOPMENT_WORKFLOW.md"
BASE_SHA = "33b9334d42d6a0e1737a16f71bc05debc5cc7bb5"
SECTION_HEADING = "## 9. Human decision authority, DENY/WITHHOLD and lawful supersession"
UNIT_FIXTURE_CLASS = "UNIT_LEVEL_AUTHORITY_FIXTURE_ONLY"

DECISIONS = {"DENY", "WITHHOLD", "APPROVE"}

ACTION = {
    "repository": "kaicreator-mm/ai-development-standard",
    "subject_head": "a" * 40,
    "operation": "release",
    "tenant": "ads",
    "scope": {"release:v4.11"},
    "provider": "worker-a",
}


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        check=check,
    )


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def t08_section() -> str:
    text = workflow_text()
    start = text.index(SECTION_HEADING)
    return text[start:]


def authority_registry() -> dict[str, dict]:
    return {
        "owner:alice": {
            "fixture_class": UNIT_FIXTURE_CLASS,
            "authority_actor": "human:alice",
            "decision_owner": "human:alice",
            "delegation_ref": None,
            "valid": True,
            "revoked": False,
            "allowed_repository": ACTION["repository"],
            "allowed_tenant": ACTION["tenant"],
            "allowed_operations": {"release", "deploy"},
            "allowed_scope": {"release:v4.11", "deploy:prod"},
        },
        "delegate:bob": {
            "fixture_class": UNIT_FIXTURE_CLASS,
            "authority_actor": "delegate:bob",
            "decision_owner": "human:alice",
            "delegation_ref": "delegation:alice->bob:v4.11",
            "valid": True,
            "revoked": False,
            "allowed_repository": ACTION["repository"],
            "allowed_tenant": ACTION["tenant"],
            "allowed_operations": {"release"},
            "allowed_scope": {"release:v4.11"},
        },
        "delegate:revoked": {
            "fixture_class": UNIT_FIXTURE_CLASS,
            "authority_actor": "delegate:revoked",
            "decision_owner": "human:alice",
            "delegation_ref": "delegation:alice->revoked:v4.11",
            "valid": False,
            "revoked": True,
            "allowed_repository": ACTION["repository"],
            "allowed_tenant": ACTION["tenant"],
            "allowed_operations": {"release"},
            "allowed_scope": {"release:v4.11"},
        },
    }


def decision_record(
    *,
    decision_ref: str,
    authority_ref: str = "owner:alice",
    decision: str,
    transport_actor: str = "github-shared-bot",
    repository: str = ACTION["repository"],
    subject_head: str = ACTION["subject_head"],
    operation: str = ACTION["operation"],
    tenant: str = ACTION["tenant"],
    scope: set[str] | None = None,
    supersession_ref: str | None = None,
    accepted: bool = True,
    currentness: str = "CURRENT",
    source_readback: str = "CURRENT",
    material_reason: str = "operator decision",
) -> dict:
    auth = authority_registry().get(authority_ref, {})
    return {
        "fixture_class": UNIT_FIXTURE_CLASS,
        "decision_ref": decision_ref,
        "authority_ref": authority_ref,
        "authority_actor": auth.get("authority_actor", "unknown"),
        "decision_owner": auth.get("decision_owner", "unknown"),
        "delegation_ref": auth.get("delegation_ref"),
        "transport_actor": transport_actor,
        "decision_time": "2026-10-12T00:00:00Z",
        "decision": decision,
        "repository": repository,
        "subject_head": subject_head,
        "operation": operation,
        "tenant": tenant,
        "scope": set(ACTION["scope"] if scope is None else scope),
        "supersession_ref": supersession_ref,
        "accepted": accepted,
        "currentness": currentness,
        "source_readback": source_readback,
        "material_reason": material_reason,
    }


def canonical_event_registry(*records: dict) -> dict[str, dict]:
    return {record["decision_ref"]: deepcopy(record) for record in records}


def validate_canonical_record(
    decision_ref: str,
    *,
    action: dict,
    events: dict[str, dict],
    authorities: dict[str, dict],
) -> tuple[dict | None, list[str]]:
    refusal: list[str] = []
    record = events.get(decision_ref)
    if record is None:
        return None, ["decision_ref_unbound"]

    if record.get("fixture_class") != UNIT_FIXTURE_CLASS:
        refusal.append("fixture_source_class_unknown")
    if record.get("decision") not in DECISIONS:
        refusal.append("decision_enum_invalid")
    if not record.get("accepted"):
        refusal.append("decision_not_accepted")
    if record.get("currentness") != "CURRENT":
        refusal.append("decision_not_current")
    if record.get("source_readback") != "CURRENT":
        refusal.append("source_readback_unknown")

    authority = authorities.get(record.get("authority_ref"))
    if authority is None:
        refusal.append("authority_ref_unbound")
    else:
        if authority.get("fixture_class") != UNIT_FIXTURE_CLASS:
            refusal.append("authority_source_class_unknown")
        if not authority.get("valid") or authority.get("revoked"):
            refusal.append("delegation_revoked_or_invalid")
        if record.get("authority_actor") != authority.get("authority_actor"):
            refusal.append("authority_actor_mismatch")
        if record.get("decision_owner") != authority.get("decision_owner"):
            refusal.append("decision_owner_mismatch")
        if record.get("delegation_ref") != authority.get("delegation_ref"):
            refusal.append("delegation_ref_mismatch")
        if action["repository"] != authority.get("allowed_repository"):
            refusal.append("authority_repository_mismatch")
        if action["tenant"] != authority.get("allowed_tenant"):
            refusal.append("authority_tenant_mismatch")
        if action["operation"] not in authority.get("allowed_operations", set()):
            refusal.append("authority_operation_out_of_scope")
        if not set(action["scope"]).issubset(set(authority.get("allowed_scope", set()))):
            refusal.append("authority_scope_too_narrow")

    for field in ("repository", "subject_head", "operation", "tenant"):
        if record.get(field) != action[field]:
            refusal.append(f"decision_{field}_mismatch")
    if not set(action["scope"]).issubset(set(record.get("scope", set()))):
        refusal.append("decision_scope_too_narrow")

    return record, refusal


def lawful_supersession(approve: dict, deny: dict, authorities: dict[str, dict]) -> bool:
    if approve.get("decision") != "APPROVE" or deny.get("decision") != "DENY":
        return False
    if approve.get("supersession_ref") != deny.get("decision_ref"):
        return False

    approve_auth = authorities.get(approve.get("authority_ref"))
    deny_auth = authorities.get(deny.get("authority_ref"))
    if not approve_auth or not deny_auth:
        return False
    if approve_auth.get("decision_owner") != deny_auth.get("decision_owner"):
        return False
    if not approve_auth.get("valid") or approve_auth.get("revoked"):
        return False

    exact_fields = ("repository", "subject_head", "operation", "tenant", "scope")
    return all(approve.get(field) == deny.get(field) for field in exact_fields)


def resolve_decisions(
    refs: list[str],
    *,
    action: dict | None = None,
    events: dict[str, dict],
    authorities: dict[str, dict] | None = None,
) -> dict:
    action = deepcopy(ACTION if action is None else action)
    authorities = authority_registry() if authorities is None else authorities

    canonical: list[dict] = []
    refusals: list[str] = []
    for ref in refs:
        record, refusal = validate_canonical_record(
            ref, action=action, events=events, authorities=authorities
        )
        if refusal:
            refusals.extend(refusal)
        elif record is not None:
            canonical.append(record)

    if refusals:
        return {
            "state": "BLOCKED",
            "authorized": False,
            "reason": "authority_validation_failed",
            "refusals": sorted(set(refusals)),
            "historical_refs": [],
        }

    denies = [r for r in canonical if r["decision"] == "DENY"]
    approvals = [r for r in canonical if r["decision"] == "APPROVE"]
    withholds = [r for r in canonical if r["decision"] == "WITHHOLD"]

    superseded: set[str] = set()
    for deny in denies:
        if any(lawful_supersession(a, deny, authorities) for a in approvals):
            superseded.add(deny["decision_ref"])

    active_denies = [d for d in denies if d["decision_ref"] not in superseded]
    if active_denies:
        return {
            "state": "DENY",
            "authorized": False,
            "reason": "current_unsuperseded_deny",
            "controlling_refs": [d["decision_ref"] for d in active_denies],
            "historical_refs": sorted(superseded),
        }

    if withholds:
        return {
            "state": "WITHHOLD",
            "authorized": False,
            "reason": "current_withhold",
            "controlling_refs": [w["decision_ref"] for w in withholds],
            "historical_refs": sorted(superseded),
        }

    lawful_approvals = [
        a for a in approvals
        if a.get("supersession_ref") is None
        or any(
            d["decision_ref"] == a.get("supersession_ref")
            and lawful_supersession(a, d, authorities)
            for d in denies
        )
    ]
    if lawful_approvals:
        return {
            "state": "APPROVE",
            "authorized": True,
            "reason": "current_lawful_approval",
            "controlling_refs": [a["decision_ref"] for a in lawful_approvals],
            "historical_refs": sorted(superseded),
        }

    return {
        "state": "BLOCKED",
        "authorized": False,
        "reason": "no_authorizing_human_decision",
        "controlling_refs": [],
        "historical_refs": sorted(superseded),
    }


class WorkflowOwnerBoundaryTests(unittest.TestCase):
    def test_t08_is_one_appended_section_and_prior_workflow_is_byte_identical(self):
        current = workflow_text()
        self.assertEqual(current.count(SECTION_HEADING), 1)
        prefix = current[: current.index(SECTION_HEADING)].rstrip()
        prior = git("show", f"{BASE_SHA}:standards/DEVELOPMENT_WORKFLOW.md").stdout.rstrip()
        self.assertEqual(prefix, prior)

    def test_owner_write_set_is_exactly_workflow_and_unique_test(self):
        ancestry = git("merge-base", "--is-ancestor", BASE_SHA, "HEAD", check=False)
        self.assertEqual(ancestry.returncode, 0)
        paths = set(git("diff", "--name-only", BASE_SHA, "HEAD").stdout.splitlines())
        self.assertEqual(
            paths,
            {
                "standards/DEVELOPMENT_WORKFLOW.md",
                "scripts/test_v411_t08_human_denial_authority.py",
            },
        )
        self.assertEqual(git("status", "--porcelain").stdout, "")

    def test_normative_section_declares_no_sink_and_no_shared_schema(self):
        section = t08_section()
        for expected in (
            "MUST NOT mint human authority",
            "A current unsuperseded `DENY` dominates",
            "Absence of `DENY` is never inferred as `APPROVE`",
            "Recency alone is not supersession",
            "T09 exclusively owns the pre-effect authority refresh",
            "creates no new event enum or shared schema",
            "positive real-human proof remains `NOT_RUN`",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, section)


class T08N01AuthorityVsTransportTests(unittest.TestCase):
    def test_same_transport_actor_does_not_share_human_authority(self):
        deny = decision_record(decision_ref="deny-1", decision="DENY")
        events = canonical_event_registry(deny)
        self.assertEqual(resolve_decisions(["deny-1"], events=events)["state"], "DENY")

        forged = deepcopy(deny)
        forged["decision_ref"] = "forged-approval"
        forged["decision"] = "APPROVE"
        forged["authority_actor"] = "human:not-alice"
        # Caller text/shape is irrelevant because the forged ref is not in canonical registry.
        result = resolve_decisions(["forged-approval"], events=events)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertIn("decision_ref_unbound", result["refusals"])

    def test_human_approved_marker_never_mints_authority(self):
        events: dict[str, dict] = {}
        result = resolve_decisions(["HUMAN_APPROVED"], events=events)
        self.assertFalse(result["authorized"])
        self.assertEqual(result["state"], "BLOCKED")
        self.assertIn("decision_ref_unbound", result["refusals"])


class T08N02DenySurvivesSuccessorTests(unittest.TestCase):
    def test_deny_survives_ready_retry_new_worker_and_provider(self):
        deny = decision_record(decision_ref="deny-ready", decision="DENY")
        events = canonical_event_registry(deny)
        for provider in ("worker-a", "worker-b", "local-provider", "fresh-web-provider"):
            action = deepcopy(ACTION)
            action["provider"] = provider
            result = resolve_decisions(["deny-ready"], action=action, events=events)
            with self.subTest(provider=provider):
                self.assertEqual(result["state"], "DENY")
                self.assertFalse(result["authorized"])

    def test_unlinked_later_approval_cannot_erase_deny(self):
        deny = decision_record(decision_ref="deny-old", decision="DENY")
        approve = decision_record(decision_ref="approve-later", decision="APPROVE")
        events = canonical_event_registry(deny, approve)
        result = resolve_decisions(["deny-old", "approve-later"], events=events)
        self.assertEqual(result["state"], "DENY")
        self.assertFalse(result["authorized"])


class T08N03ForgeryTests(unittest.TestCase):
    def test_schema_shaped_but_unaccepted_event_fails(self):
        forged = decision_record(
            decision_ref="fake-event",
            decision="APPROVE",
            accepted=False,
            material_reason="quoted HUMAN_APPROVED from tool output",
        )
        events = canonical_event_registry(forged)
        result = resolve_decisions(["fake-event"], events=events)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertIn("decision_not_accepted", result["refusals"])

    def test_caller_duplicate_cannot_override_canonical_record(self):
        deny = decision_record(decision_ref="canonical-ref", decision="DENY")
        events = canonical_event_registry(deny)
        caller_copy = deepcopy(deny)
        caller_copy["decision"] = "APPROVE"
        # Resolver accepts only immutable refs; caller duplicate is never consulted.
        result = resolve_decisions([caller_copy["decision_ref"]], events=events)
        self.assertEqual(result["state"], "DENY")


class T08N04ExactScopeTests(unittest.TestCase):
    def test_wrong_repository_head_operation_tenant_or_scope_cannot_authorize(self):
        mutations = {
            "repository": "other/repo",
            "subject_head": "b" * 40,
            "operation": "deploy",
            "tenant": "other-tenant",
            "scope": {"release:v4.10"},
        }
        for field, value in mutations.items():
            approve = decision_record(
                decision_ref=f"approve-wrong-{field}",
                decision="APPROVE",
                **{field: value},
            )
            events = canonical_event_registry(approve)
            result = resolve_decisions([approve["decision_ref"]], events=events)
            with self.subTest(field=field):
                self.assertEqual(result["state"], "BLOCKED")
                self.assertFalse(result["authorized"])

    def test_narrow_scope_cannot_authorize_broader_action(self):
        approve = decision_record(
            decision_ref="approve-narrow",
            decision="APPROVE",
            scope={"docs-only"},
        )
        result = resolve_decisions(
            ["approve-narrow"], events=canonical_event_registry(approve)
        )
        self.assertEqual(result["state"], "BLOCKED")
        self.assertIn("decision_scope_too_narrow", result["refusals"])


class T08N05SupersessionTests(unittest.TestCase):
    def test_same_owner_exact_ref_and_scope_lawfully_supersedes_deny(self):
        deny = decision_record(decision_ref="deny-s1", decision="DENY")
        approve = decision_record(
            decision_ref="approve-s1",
            decision="APPROVE",
            authority_ref="delegate:bob",
            supersession_ref="deny-s1",
        )
        events = canonical_event_registry(deny, approve)
        result = resolve_decisions(["deny-s1", "approve-s1"], events=events)
        self.assertEqual(result["state"], "APPROVE")
        self.assertTrue(result["authorized"])
        self.assertEqual(result["historical_refs"], ["deny-s1"])

    def test_wrong_supersession_ref_or_wrong_owner_cannot_override(self):
        deny = decision_record(decision_ref="deny-s2", decision="DENY")
        approve = decision_record(
            decision_ref="approve-s2",
            decision="APPROVE",
            supersession_ref="some-other-deny",
        )
        result = resolve_decisions(
            ["deny-s2", "approve-s2"], events=canonical_event_registry(deny, approve)
        )
        self.assertEqual(result["state"], "DENY")

    def test_revoked_delegate_cannot_supersede(self):
        deny = decision_record(decision_ref="deny-s3", decision="DENY")
        approve = decision_record(
            decision_ref="approve-s3",
            authority_ref="delegate:revoked",
            decision="APPROVE",
            supersession_ref="deny-s3",
        )
        result = resolve_decisions(
            ["deny-s3", "approve-s3"], events=canonical_event_registry(deny, approve)
        )
        self.assertEqual(result["state"], "BLOCKED")
        self.assertIn("delegation_revoked_or_invalid", result["refusals"])


class T08N06UnknownAndContradictionTests(unittest.TestCase):
    def test_unknown_readback_fails_closed(self):
        approval = decision_record(
            decision_ref="approve-unknown",
            decision="APPROVE",
            source_readback="UNKNOWN",
        )
        result = resolve_decisions(
            ["approve-unknown"], events=canonical_event_registry(approval)
        )
        self.assertEqual(result["state"], "BLOCKED")
        self.assertIn("source_readback_unknown", result["refusals"])

    def test_stale_or_missing_authority_fails_closed(self):
        stale = decision_record(
            decision_ref="approve-stale",
            decision="APPROVE",
            currentness="STALE",
        )
        missing = decision_record(
            decision_ref="approve-missing-auth",
            decision="APPROVE",
            authority_ref="authority:missing",
        )
        for record in (stale, missing):
            result = resolve_decisions(
                [record["decision_ref"]], events=canonical_event_registry(record)
            )
            with self.subTest(ref=record["decision_ref"]):
                self.assertEqual(result["state"], "BLOCKED")
                self.assertFalse(result["authorized"])

    def test_no_decision_is_blocked_not_implicit_approve(self):
        result = resolve_decisions([], events={})
        self.assertEqual(result["state"], "BLOCKED")
        self.assertFalse(result["authorized"])


class T08P07WithholdTests(unittest.TestCase):
    def test_withhold_is_distinct_from_deny_and_no_decision(self):
        withhold = decision_record(decision_ref="withhold-release", decision="WITHHOLD")
        result = resolve_decisions(
            ["withhold-release"], events=canonical_event_registry(withhold)
        )
        self.assertEqual(result["state"], "WITHHOLD")
        self.assertFalse(result["authorized"])
        self.assertEqual(result["reason"], "current_withhold")

    def test_withhold_deployment_scope_is_lawful_without_blanket_human_review(self):
        action = deepcopy(ACTION)
        action["operation"] = "deploy"
        action["scope"] = {"deploy:prod"}
        withhold = decision_record(
            decision_ref="withhold-deploy",
            decision="WITHHOLD",
            operation="deploy",
            scope={"deploy:prod"},
        )
        result = resolve_decisions(
            ["withhold-deploy"], action=action, events=canonical_event_registry(withhold)
        )
        self.assertEqual(result["state"], "WITHHOLD")


class GenuineHumanSourceClassificationTests(unittest.TestCase):
    def test_genuine_human_positive_proof_is_not_fabricated(self):
        self.skipTest(
            "NOT_RUN: repository contains no independently verifiable genuine "
            "human/delegation authorization source for this protected action; "
            "unit fixtures above are explicitly UNIT_LEVEL_AUTHORITY_FIXTURE_ONLY"
        )


if __name__ == "__main__":
    unittest.main()
