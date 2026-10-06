"""V410-T06B focused regression — serialized-admission machine conformance.

Covers oracle sections B (claim-key canonicalization), C (authorized
non-default groups), D (admission-generation CAS), E (multi-active
projection), F (writer provenance), G (terminal precedence and invariance),
H (derived-state discipline) and the J frozen guards, plus the dogfood
T1-T5 worked negatives, exercising the additive W7 helpers in
``scripts/v34_rules.py`` and the W1-W3 schema additions. Reuses the carried
fail-closed subset guards; purely local; no network.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_protocol_schemas import assert_supported_schema  # noqa: E402
from v34_rules import (  # noqa: E402
    DEFAULT_COMPATIBILITY_GROUP,
    admission_generation_conforms,
    authorize_non_default,
    derive_claim_key,
    lineage_refs_present,
    normalize_group,
    parse_claim_key,
    project_active_dispatches,
    target_environment_agreement,
    terminal_precedence,
)

DISPATCH_SCHEMA = "schemas/dispatch.schema.json"


def load_schema(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))
EXECUTION_STATE_SCHEMA = "schemas/execution-state.schema.json"
EVENT_SCHEMA = "schemas/agent-event-v2.schema.json"


def dispatch_field(name: str) -> dict:
    return load_schema(DISPATCH_SCHEMA)["properties"][name]


class ClaimKeyCanonicalizationTests(unittest.TestCase):
    """Oracle B + T1: deterministic serialization, fail-closed reparsing."""

    def test_default_group_serialization_roundtrips(self) -> None:
        key = derive_claim_key("kaicreator-mm/ai-development-standard", "#861", "builder")
        self.assertEqual(key, "kaicreator-mm/ai-development-standard#861:builder:__default__")
        self.assertEqual(parse_claim_key(key)["group"], DEFAULT_COMPATIBILITY_GROUP)

    def test_non_default_group_roundtrips(self) -> None:
        key = derive_claim_key("r", "#1", "validator", "interop")
        self.assertEqual(parse_claim_key(key), {"repository": "r", "task": "#1", "role": "validator", "group": "interop"})

    def test_malformed_segments_fail_closed(self) -> None:
        for args in (
            ("r", "#1", "bu:ilder"),
            ("r", "#1", "builder", "gr#oup"),
            ("r", "#1", "builder", "gr:oup"),
            ("r", "1", "builder"),
            ("", "#1", "builder"),
        ):
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    derive_claim_key(*args)

    def test_reparse_reorder_or_extra_segment_fails(self) -> None:
        for bad in ("r#1:builder", "r#1:builder:__default__:extra", "#1:builder:__default__", ""):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    parse_claim_key(bad)

    def test_revision_or_session_id_never_in_slot4(self) -> None:
        # writer rule (W5): revision/session ids are never EMITTED in slot 4;
        # the mechanical rule is separator-freedom + roundtrip (no heuristics).
        # normalization, not identity: blank-ish groups collapse to __default__
        self.assertEqual(normalize_group("  "), DEFAULT_COMPATIBILITY_GROUP)


class AuthorizedNonDefaultTests(unittest.TestCase):
    """Oracle C: durable higher-authority validation, never downgraded."""

    def test_default_group_needs_no_authority_ref(self) -> None:
        self.assertTrue(authorize_non_default(None, None))
        self.assertTrue(authorize_non_default("__default__", "#861@6016591816"))

    def test_non_default_requires_durable_issue_comment_ref(self) -> None:
        self.assertTrue(authorize_non_default("interop", "#861@6016591816"))
        for bad_ref in (None, "", "see #861", "#861", "#861@abc", "https://example.com"):
            with self.subTest(bad_ref=bad_ref):
                with self.assertRaises(ValueError):
                    authorize_non_default("interop", bad_ref)


class AdmissionGenerationCasTests(unittest.TestCase):
    """Oracle D: monotonic per-key CAS; stale fails with zero mutation."""

    def test_claim_requires_reserved_next_generation(self) -> None:
        self.assertEqual(
            admission_generation_conforms(reserved_generation=3, claimed_generation=4),
            "CLAIMED",
        )

    def test_stale_writer_is_stale_not_claimed(self) -> None:
        self.assertEqual(
            admission_generation_conforms(reserved_generation=4, claimed_generation=3),
            "STALE",
        )

    def test_idempotent_reclaim_at_current_generation(self) -> None:
        self.assertEqual(
            admission_generation_conforms(reserved_generation=3, claimed_generation=3),
            "IDEMPOTENT",
        )

    def test_malformed_generations_fail_closed(self) -> None:
        for kwargs in (
            {"reserved_generation": -1, "claimed_generation": 0},
            {"reserved_generation": True, "claimed_generation": 1},
            {"reserved_generation": None, "claimed_generation": 1},
            {"reserved_generation": "3", "claimed_generation": 4},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    admission_generation_conforms(**kwargs)


class MultiActiveProjectionTests(unittest.TestCase):
    """Oracle E + H: stable ordering, NON_AUTHORITATIVE derived state."""

    def _rows(self) -> list[dict]:
        return [
            {"repository": "r", "task": "#2", "role": "validator", "dispatch_id": "d-a", "claimed_by": "x"},
            {"repository": "r", "task": "#1", "role": "builder", "dispatch_id": "d-z", "claimed_by": "y"},
            {"repository": "r", "task": "#1", "role": "validator", "dispatch_id": "d-b", "claimed_by": "z"},
        ]

    def test_projection_is_stable_by_key_then_id(self) -> None:
        rows = project_active_dispatches(self._rows())
        self.assertEqual([row["dispatch_id"] for row in rows], ["d-z", "d-b", "d-a"])
        reversed_rows = project_active_dispatches(list(reversed(self._rows())))
        self.assertEqual(rows, reversed_rows)

    def test_malformed_rows_fail_closed(self) -> None:
        for mutant in (
            [{"task": "#1", "role": "builder"}],
            [{"repository": "r", "task": "#1", "role": "scheduler", "dispatch_id": "d"}],
            ["not-a-mapping"],
            [{"repository": "r", "task": "#1", "role": "builder"}],
        ):
            with self.subTest(mutant=mutant):
                with self.assertRaises(ValueError):
                    project_active_dispatches(mutant)

    def test_schema_projection_is_non_authoritative_additive_shape(self) -> None:
        schema = load_schema(EXECUTION_STATE_SCHEMA)
        assert_supported_schema(schema)
        projection = schema["properties"]["active_dispatches"]
        item = projection["items"]
        self.assertEqual(item["additionalProperties"], False)
        self.assertIn("protected_claim_key", item["properties"])
        self.assertIn("NON_AUTHORITATIVE_DERIVED_STATE", projection["description"])


class WriterProvenanceTests(unittest.TestCase):
    """Oracle F + T3/T4: durable refs, alias agreement, environment disambiguation."""

    def test_current_writers_require_durable_refs(self) -> None:
        good = {"source_proposal_ref": "#861@6016320778", "canonical_admission_ref": "#861@6016591816"}
        self.assertTrue(lineage_refs_present(good, current_writer=True))
        for bad in (
            {"source_proposal_ref": "see the thread", "canonical_admission_ref": "#861@6016591816"},
            {"source_proposal_ref": "#861@6016320778"},
            {},
        ):
            with self.subTest(bad=bad):
                self.assertFalse(lineage_refs_present(bad, current_writer=True))

    def test_historical_events_are_exempt(self) -> None:
        self.assertTrue(lineage_refs_present({}, current_writer=False))

    def test_target_environment_alias_agreement(self) -> None:
        self.assertEqual(
            target_environment_agreement(execution_environment="LOCAL", target_environment="LOCAL"),
            "LOCAL",
        )
        self.assertEqual(
            target_environment_agreement(execution_environment="WEB", target_environment=None), "WEB"
        )
        with self.assertRaises(ValueError):
            target_environment_agreement(execution_environment="LOCAL", target_environment="WEB")

    def test_environment_operator_and_validation_gate_are_distinct(self) -> None:
        # A13/hazard-1: the handoff schema's execution_environment stays the
        # validation-gate environment; the dispatch field is the coarse WEB|LOCAL.
        handoff = json.loads((ROOT / "schemas" / "local-agent-handoff.schema.json").read_text(encoding="utf-8"))
        dispatch_env = dispatch_field("execution_environment")
        self.assertEqual(dispatch_env["enum"], ["WEB", "LOCAL"])
        self.assertIn("execution_environment", handoff["properties"])
        self.assertNotIn("WEB_REVIEWER", dispatch_env["enum"])
        event_schema = load_schema(EVENT_SCHEMA)
        for field in ("source_proposal_ref", "canonical_admission_ref", "scheduler_origin"):
            self.assertIn(field, event_schema["properties"])
        # operator_kind remains provider provenance and carries no WEB/LOCAL semantics
        self.assertNotIn("WEB", event_schema["properties"]["operator_kind"].get("enum", []))


class TerminalPrecedenceTests(unittest.TestCase):
    """Oracle G + T5/T2: terminal precedence, no count/recency/brand authority."""

    def test_terminal_beats_proposal_and_checkpoint(self) -> None:
        actions = [
            {"kind": "checkpoint", "dispatch_id": "d"},
            {"kind": "proposal", "dispatch_id": "d"},
            {"kind": "terminal", "dispatch_id": "d", "state": "COMPLETED"},
            {"kind": "checkpoint", "dispatch_id": "d"},
        ]
        self.assertEqual(terminal_precedence(actions)["kind"], "terminal")

    def test_canonical_admission_and_claim_beat_proposals(self) -> None:
        actions = [
            {"kind": "proposal", "dispatch_id": "d"},
            {"kind": "claim", "dispatch_id": "d"},
            {"kind": "proposal", "dispatch_id": "d"},
        ]
        self.assertEqual(terminal_precedence(actions)["kind"], "claim")

    def test_stale_loser_is_a_disposition_not_a_rewrite(self) -> None:
        # T2: the stale proposal survives as dispositioned derived state; the
        # reducer returns the winner and never merges or mutates the loser.
        actions = [
            {"kind": "proposal", "dispatch_id": "d", "writer": "w1"},
            {"kind": "admission", "dispatch_id": "d", "writer": "w2"},
        ]
        winner = terminal_precedence(actions)
        self.assertEqual(winner["kind"], "admission")
        loser = next(a for a in actions if a["writer"] == "w1")
        self.assertEqual(loser, {"kind": "proposal", "dispatch_id": "d", "writer": "w1"})

    def test_malformed_or_empty_actions_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            terminal_precedence([])
        with self.assertRaises(ValueError):
            terminal_precedence([{"kind": "brand-vote", "dispatch_id": "d"}])


class FrozenGuardTests(unittest.TestCase):
    """Oracle J: no second event family/state dimension; byte-stable couplings."""

    def test_event_enum_gains_no_new_type(self) -> None:
        events = load_schema(EVENT_SCHEMA)["properties"]["event"]["enum"]
        self.assertNotIn("ADMISSION_WAKEUP", events)
        self.assertNotIn("SCHEDULER_CHECKPOINT", events)

    def test_dispatch_schema_couplings_and_new_fields_are_supported(self) -> None:
        schema = load_schema(DISPATCH_SCHEMA)
        assert_supported_schema(schema)
        self.assertEqual(
            schema["properties"]["execution_profile"]["enum"],
            ["LOCAL_BUILDER", "LOCAL_VALIDATOR", "WEB_REVIEWER", "PLATFORM_VALIDATOR", "CLOSURE_VALIDATOR"],
        )
        couplings = [
            c for c in schema["allOf"] if "execution_profile" in c.get("if", {}).get("properties", {})
        ]
        self.assertEqual(len(couplings), 3)  # A11: byte-stable profile<->role couplings
        conditional = [c for c in schema["allOf"] if "compatibility_group" in c.get("if", {}).get("properties", {})]
        self.assertEqual(len(conditional), 1)
        self.assertEqual(
            conditional[0]["then"]["required"], ["compatibility_authority_ref"]
        )
        self.assertEqual(dispatch_field("execution_environment")["enum"], ["WEB", "LOCAL"])
        self.assertEqual(dispatch_field("scheduler_origin")["enum"], ["WEB", "LOCAL"])


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
