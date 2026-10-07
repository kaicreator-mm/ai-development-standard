"""V410-T06B focused regression — serialized-admission machine conformance.

Covers oracle sections B (claim-key canonicalization incl. B5/B6 persisted-key
conformance), C (authorized non-default groups, durable-format level), D
(admission-generation CAS), E/H (multi-active projection and derived-state
discipline incl. exact subject refs), F (writer provenance), G (terminal
precedence and invariance) and the J frozen guards, plus the dogfood T1-T5
worked negatives, exercising the additive W7 helpers in
``scripts/v34_rules.py`` and the W1-W3 schema additions. The keyed race
extension (D1/D4/E3/G3/G8) lives in ``test_execution_architecture.py``; the
A-section schema verdicts live in ``test_protocol_schemas.py``. Reuses the
carried fail-closed subset guards; purely local; no network. Exact per-case
coverage is pinned by the pack TEST_MATRIX (``covers`` + ``dispositions``).

R4 (bounded repair after Validation R3 #861@6025948290): the reducer emits
only the contracted row with profile-aware environment projection
(LOCAL_BUILDER/LOCAL_VALIDATOR/WEB_REVIEWER via ``project_dispatch_environment``)
and B5/B6 persisted-key mismatch fail-closed; the integration regression embeds
``project_active_dispatches`` output into a complete execution-state instance
and validates it through the real ``schemas/execution-state.schema.json``
(legacy-profile positives plus leak/missing-field/non-null-group/UNKNOWN and
mismatch negatives), which replaces the withdrawn trim-expectation assertion.

R5 (bounded repair after Fresh Review R4 #861@6033098161): the C2 gate no
longer accepts syntax-only durable refs — ``resolve_non_default_authority``
requires a controller-resolved owning-family grant at the keyed admission
boundary (P1-2); the execution-state schema conditionally enforces the H2
legacy singular null rule and ``execution_state_projection_problems`` adds the
duplicate-active-key probe (P1-3); the full-state positive fixture uses
distinct tasks instead of an impossible same-key multi-active validator state
(P2-1).
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_protocol_schemas import assert_supported_schema, validate_subset  # noqa: E402
from v34_rules import (  # noqa: E402
    DEFAULT_COMPATIBILITY_GROUP,
    ENVIRONMENT_PROFILE_CONTRADICTION,
    admission_generation_conforms,
    authorize_non_default,
    derive_claim_key,
    execution_state_projection_problems,
    lineage_refs_present,
    normalize_group,
    parse_claim_key,
    project_active_dispatches,
    project_dispatch_environment,
    protected_claim_key_conforms,
    resolve_non_default_authority,
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

    def test_default_group_resolves_without_any_grant_inventory(self) -> None:
        # R5 (P1-1): blank-only input normalizes to the reserved default and an
        # explicit __default__ stays readable — neither needs a ref or grants.
        for group in ("  ", "__default__", None):
            with self.subTest(group=group):
                self.assertTrue(
                    resolve_non_default_authority(
                        repository="r",
                        task="#1",
                        role="validator",
                        compatibility_group=group,
                        authority_ref=None,
                        authority_grants=None,
                    )
                )

    def test_non_default_requires_resolved_owning_family_grant(self) -> None:
        # R5 (P1-2): the ref shape alone never authorizes. The controller-
        # resolved grant inventory is the owned proof path; resolution must be
        # family-fit and tuple-exact, and every ambiguity fails closed.
        grant = {
            "ref": "#861@6000000000",
            "authority_family": "VALIDATION",
            "repository": "r",
            "task": "#861",
            "role": "validator",
            "groups": ["interop"],
        }
        grants = {"#861@6000000000": grant}
        self.assertTrue(
            resolve_non_default_authority(
                repository="r",
                task="#861",
                role="validator",
                compatibility_group="interop",
                authority_ref="#861@6000000000",
                authority_grants=grants,
            )
        )
        for mutant_grants, token in (
            (None, "AUTHORITY_UNRESOLVED"),
            ({}, "AUTHORITY_UNRESOLVED"),
            ({"#861@6000000000": dict(grant, authority_family="TASK_PACK")}, "AUTHORITY_FAMILY_MISMATCH"),
            ({"#861@6000000000": dict(grant, task="#999")}, "AUTHORITY_NOT_APPLICABLE"),
            ({"#861@6000000000": dict(grant, role="builder")}, "AUTHORITY_NOT_APPLICABLE"),
            ({"#861@6000000000": dict(grant, groups=["other"])}, "AUTHORITY_NOT_APPLICABLE"),
            ({"#861@6000000000": {"authority_family": "VALIDATION"}}, "AUTHORITY_UNRESOLVED"),
        ):
            with self.subTest(token=token):
                with self.assertRaises(ValueError) as caught:
                    resolve_non_default_authority(
                        repository="r",
                        task="#861",
                        role="validator",
                        compatibility_group="interop",
                        authority_ref="#861@6000000000",
                        authority_grants=mutant_grants,
                    )
                self.assertIn(token, str(caught.exception))


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


class ProtectedClaimKeyConformanceTests(unittest.TestCase):
    """Oracle B5/B6 (+FC3): the persisted key is audit provenance, never trusted."""

    def _dispatch(self, **overrides) -> dict:
        value = {
            "repository": "kaicreator-mm/ai-development-standard",
            "task": "#861",
            "role": "builder",
            "dispatch_id": "D-A",
        }
        value.update(overrides)
        return value

    def test_persisted_key_must_equal_rederivation(self) -> None:
        dispatch = self._dispatch(protected_claim_key="kaicreator-mm/ai-development-standard#861:builder:__default__")
        self.assertTrue(protected_claim_key_conforms(dispatch))
        mutant = self._dispatch(protected_claim_key="kaicreator-mm/ai-development-standard#861:builder:interop")
        self.assertFalse(protected_claim_key_conforms(mutant))

    def test_scheduler_supplied_claim_key_is_rejected(self) -> None:
        supplied = self._dispatch(
            claim_key="kaicreator-mm/ai-development-standard#861:builder:__default__",
            protected_claim_key="kaicreator-mm/ai-development-standard#861:builder:__default__",
        )
        self.assertFalse(protected_claim_key_conforms(supplied))

    def test_absent_persisted_key_stays_readable(self) -> None:
        self.assertTrue(protected_claim_key_conforms(self._dispatch()))

    def test_malformed_identity_fails_closed(self) -> None:
        for mutant in (
            self._dispatch(task="861", protected_claim_key="anything"),
            self._dispatch(role="bu:ilder", protected_claim_key="anything"),
        ):
            with self.subTest(mutant=mutant):
                self.assertFalse(protected_claim_key_conforms(mutant))


class EnvironmentProfileProjectionTests(unittest.TestCase):
    """FC1/A7-A10: environment projection never guesses and never reinterprets."""

    def test_unknown_profile_projects_unknown_and_stays_readable(self) -> None:
        self.assertEqual(
            project_dispatch_environment({"execution_profile": "LEGACY_HOST_AGENT"}),
            "UNKNOWN",
        )

    def test_contradiction_token_is_stable(self) -> None:
        with self.assertRaises(ValueError) as caught:
            project_dispatch_environment(
                {"execution_profile": "LOCAL_BUILDER", "execution_environment": "WEB"}
            )
        self.assertIn(ENVIRONMENT_PROFILE_CONTRADICTION, str(caught.exception))

    def test_agreeing_explicit_environment_matches_the_legacy_mapping(self) -> None:
        self.assertEqual(
            project_dispatch_environment(
                {"execution_profile": "WEB_REVIEWER", "execution_environment": "WEB"}
            ),
            "WEB",
        )


class MultiActiveProjectionTests(unittest.TestCase):
    """Oracle E + H: stable ordering, NON_AUTHORITATIVE derived state."""

    def test_zero_active_rows_project_empty(self) -> None:
        self.assertEqual(project_active_dispatches([]), [])

    def _rows(self) -> list[dict]:
        return [
            {"repository": "r", "task": "#2", "role": "validator", "dispatch_id": "d-a", "claimed_by": "x", "execution_profile": "LOCAL_VALIDATOR"},
            {"repository": "r", "task": "#1", "role": "builder", "dispatch_id": "d-z", "claimed_by": "y", "execution_profile": "LOCAL_BUILDER"},
            {"repository": "r", "task": "#1", "role": "validator", "dispatch_id": "d-b", "claimed_by": "z", "execution_profile": "PLATFORM_VALIDATOR", "execution_environment": "LOCAL"},
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
            [{"repository": "r", "task": "#1", "role": "builder", "dispatch_id": "d", "execution_profile": "LOCAL_BUILDER", "execution_environment": "REMOTE"}],
            [{"repository": "r", "task": "#1", "role": "builder", "dispatch_id": "d", "claimed_by": ""}],
            [{"repository": "r", "task": "#1", "role": "builder", "dispatch_id": "d"}],  # missing execution_profile
            [{"repository": "r", "task": "#1", "role": "builder", "dispatch_id": "d", "execution_profile": ""}],
            [{"repository": "r", "task": "#1", "role": "builder", "dispatch_id": "d", "execution_profile": "LOCAL_BUILDER", "execution_environment": "WEB"}],  # A8 contradiction
        ):
            with self.subTest(mutant=mutant):
                with self.assertRaises(ValueError):
                    project_active_dispatches(mutant)

    def test_non_string_group_and_bad_keys_fail_closed(self) -> None:
        with self.assertRaises(TypeError):
            project_active_dispatches(
                [{"repository": "r", "task": "#1", "role": "builder", "dispatch_id": "d", "execution_profile": "LOCAL_BUILDER", "compatibility_group": 5}]
            )
        for mutant in (
            # B5: persisted key does not match the deterministic re-derivation
            {"repository": "r", "task": "#1", "role": "builder", "dispatch_id": "d", "execution_profile": "LOCAL_BUILDER", "protected_claim_key": "r#1:builder:interop"},
            # B6: a scheduler-supplied claim_key authority field is rejected outright
            {"repository": "r", "task": "#1", "role": "builder", "dispatch_id": "d", "execution_profile": "LOCAL_BUILDER", "claim_key": "r#1:builder:__default__"},
        ):
            with self.subTest(mutant=mutant):
                with self.assertRaises(ValueError):
                    project_active_dispatches([mutant])

    def test_metadata_cannot_alter_keys_membership_or_ordering(self) -> None:
        # E/G: scheduler origin, provider/model and parent-dispatch provenance
        # must not change key derivation, row membership or projected ordering.
        decorated = [
            dict(row, scheduler_origin="WEB", provider="provider-x", model="model-x", parent_dispatch="d-parent")
            for row in self._rows()
        ]
        self.assertEqual(project_active_dispatches(decorated), project_active_dispatches(self._rows()))

    def test_exact_subject_refs_are_carried_and_validated(self) -> None:
        rows = project_active_dispatches(
            [
                {"repository": "r", "task": "#861", "role": "builder", "dispatch_id": "d-a", "execution_profile": "LOCAL_BUILDER", "issue": "#861", "pr": "#927"},
                {"repository": "r", "task": "#862", "role": "reviewer", "dispatch_id": "d-b", "execution_profile": "WEB_REVIEWER", "pr": None},
                {"repository": "r", "task": "#863", "role": "validator", "dispatch_id": "d-c", "execution_profile": "LOCAL_VALIDATOR"},
            ]
        )
        self.assertEqual(rows[0]["issue"], "#861")
        self.assertEqual(rows[0]["pr"], "#927")
        self.assertNotIn("issue", rows[2])
        for mutant in (
            [{"repository": "r", "task": "#1", "role": "builder", "dispatch_id": "d", "execution_profile": "LOCAL_BUILDER", "issue": "861"}],
            [{"repository": "r", "task": "#1", "role": "builder", "dispatch_id": "d", "execution_profile": "LOCAL_BUILDER", "pr": "#abc"}],
        ):
            with self.subTest(mutant=mutant):
                with self.assertRaises(ValueError):
                    project_active_dispatches(mutant)

    def test_group_normalization_introduces_no_trim(self) -> None:
        # normalize_group semantics are fixed: blank-only -> __default__; a
        # non-blank string (including padded) is emitted UNCHANGED — the
        # reducer introduces no trim/canonicalization rule, and the derived
        # key serializes exactly the emitted group.
        item = load_schema(EXECUTION_STATE_SCHEMA)["properties"]["active_dispatches"]["items"]
        self.assertEqual(normalize_group("  "), DEFAULT_COMPATIBILITY_GROUP)
        self.assertEqual(normalize_group(" blue "), " blue ")
        rows = project_active_dispatches(
            [
                {
                    "repository": "r",
                    "task": "#861",
                    "role": "builder",
                    "dispatch_id": "d-a",
                    "execution_profile": "LOCAL_BUILDER",
                    "compatibility_group": " blue ",
                    "claimed_by": "agent-a",
                    "issue": "#861",
                    "pr": "#927",
                }
            ]
        )
        self.assertEqual(
            rows,
            [
                {
                    "dispatch_id": "d-a",
                    "role": "builder",
                    "execution_environment": "LOCAL",
                    "compatibility_group": " blue ",
                    "protected_claim_key": "r#861:builder: blue ",
                    "claimed_by": "agent-a",
                    "issue": "#861",
                    "pr": "#927",
                }
            ],
        )
        self.assertEqual(rows[0]["protected_claim_key"], derive_claim_key("r", "#861", "builder", " blue "))
        self.assertEqual(validate_subset(rows[0], item), [])
        self.assertNotIn("repository", rows[0])
        self.assertNotIn("task", rows[0])
        self.assertNotIn("execution_profile", rows[0])

    def test_schema_projection_is_non_authoritative_additive_shape(self) -> None:
        schema = load_schema(EXECUTION_STATE_SCHEMA)
        assert_supported_schema(schema)
        projection = schema["properties"]["active_dispatches"]
        item = projection["items"]
        self.assertEqual(item["additionalProperties"], False)
        # W8-R4: the row contract requires all six projected fields; the
        # projected group is a normalized non-null non-empty string.
        self.assertEqual(
            item["required"],
            [
                "dispatch_id",
                "role",
                "execution_environment",
                "compatibility_group",
                "protected_claim_key",
                "claimed_by",
            ],
        )
        self.assertEqual(item["properties"]["compatibility_group"], {"type": "string", "minLength": 1})
        self.assertIn("protected_claim_key", item["properties"])
        for ref_field in ("issue", "pr"):
            self.assertIn(ref_field, item["properties"])
        self.assertIn("NON_AUTHORITATIVE_DERIVED_STATE", projection["description"])


class ExecutionStateIntegrationTests(unittest.TestCase):
    """Oracle W8-R4: reducer output inside a complete execution-state instance.

    Embeds ``project_active_dispatches(source)`` directly as
    ``active_dispatches`` of a minimal execution-state and validates the whole
    state through the real ``schemas/execution-state.schema.json`` — helper-only
    and schema-shape-only assertions are not a substitute.
    """

    def _source(self) -> list[dict]:
        return [
            {
                # legacy builder profile -> LOCAL; default group; absent claimed_by;
                # derivation-only fields plus non-row metadata that must not leak.
                "repository": "r",
                "task": "#861",
                "role": "builder",
                "dispatch_id": "d-builder",
                "execution_profile": "LOCAL_BUILDER",
                "issue": "#861",
                "pr": "#927",
                "scheduler_origin": "LOCAL",
                "operator_kind": "claude-code",
                "admission_generation": 4,
            },
            {
                # environment-orthogonal profile with NO explicit environment -> null;
                # task differs from the other validators: a same-key multi-active
                # validator state is impossible (#861 rule 2) and must not appear
                # in a full-state positive fixture (R5 P2-1)
                "repository": "r",
                "task": "#860",
                "role": "validator",
                "dispatch_id": "d-orthogonal",
                "execution_profile": "PLATFORM_VALIDATOR",
                "claimed_by": "val-1",
                "compatibility_authority_ref": "#861@6023707736",
            },
            {
                # environment-orthogonal profile WITH explicit environment -> LOCAL
                # (distinct task again — R5 P2-1)
                "repository": "r",
                "task": "#862",
                "role": "validator",
                "dispatch_id": "d-orthogonal-local",
                "execution_profile": "PLATFORM_VALIDATOR",
                "execution_environment": "LOCAL",
            },
            {
                # legacy reviewer profile -> WEB; null group -> __default__;
                # explicit null pr ref is carried as supplied.
                "repository": "r",
                "task": "#862",
                "role": "reviewer",
                "dispatch_id": "d-reviewer",
                "execution_profile": "WEB_REVIEWER",
                "compatibility_group": None,
                "pr": None,
            },
            {
                # legacy validator profile -> LOCAL; blank group -> __default__;
                # no issue/pr fields -> refs stay absent (distinct task — R5 P2-1)
                "repository": "r",
                "task": "#864",
                "role": "validator",
                "dispatch_id": "d-legacy-validator",
                "execution_profile": "LOCAL_VALIDATOR",
                "compatibility_group": "  ",
            },
        ]

    def _expected_rows(self) -> list[dict]:
        # stably ordered by (derived protected claim key, dispatch_id)
        return [
            {
                "dispatch_id": "d-orthogonal",
                "role": "validator",
                "execution_environment": None,
                "compatibility_group": "__default__",
                "protected_claim_key": "r#860:validator:__default__",
                "claimed_by": "val-1",
            },
            {
                "dispatch_id": "d-builder",
                "role": "builder",
                "execution_environment": "LOCAL",
                "compatibility_group": "__default__",
                "protected_claim_key": "r#861:builder:__default__",
                "claimed_by": None,
                "issue": "#861",
                "pr": "#927",
            },
            {
                "dispatch_id": "d-reviewer",
                "role": "reviewer",
                "execution_environment": "WEB",
                "compatibility_group": "__default__",
                "protected_claim_key": "r#862:reviewer:__default__",
                "claimed_by": None,
                "pr": None,
            },
            {
                "dispatch_id": "d-orthogonal-local",
                "role": "validator",
                "execution_environment": "LOCAL",
                "compatibility_group": "__default__",
                "protected_claim_key": "r#862:validator:__default__",
                "claimed_by": None,
            },
            {
                "dispatch_id": "d-legacy-validator",
                "role": "validator",
                "execution_environment": "LOCAL",
                "compatibility_group": "__default__",
                "protected_claim_key": "r#864:validator:__default__",
                "claimed_by": None,
            },
        ]

    def test_full_execution_state_with_reducer_output_validates(self) -> None:
        schema = load_schema(EXECUTION_STATE_SCHEMA)
        assert_supported_schema(schema)
        rows = project_active_dispatches(self._source())
        # exact contracted rows, stably ordered by (derived key, dispatch_id)
        self.assertEqual(rows, self._expected_rows())
        state = {
            "repository": "r",
            "work_item": "#861",
            "workflow_state": "implementing",
            "ready_queues": [],
            "derived_from": ["test"],
            "active_dispatches": rows,
        }
        self.assertEqual(validate_subset(state, schema), [])

    def test_projection_is_order_independent(self) -> None:
        self.assertEqual(
            project_active_dispatches(list(reversed(self._source()))),
            project_active_dispatches(self._source()),
        )

    def test_derived_key_equals_deterministic_rederivation(self) -> None:
        for row in project_active_dispatches(self._source()):
            source = next(e for e in self._source() if e["dispatch_id"] == row["dispatch_id"])
            self.assertEqual(
                row["protected_claim_key"],
                derive_claim_key(source["repository"], source["task"], source["role"], source.get("compatibility_group")),
            )

    def test_row_schema_rejects_leaked_or_missing_or_malformed_fields(self) -> None:
        item = load_schema(EXECUTION_STATE_SCHEMA)["properties"]["active_dispatches"]["items"]
        assert_supported_schema(item)
        valid_row = {
            "dispatch_id": "d",
            "role": "builder",
            "execution_environment": "LOCAL",
            "compatibility_group": "__default__",
            "protected_claim_key": "r#1:builder:__default__",
            "claimed_by": None,
        }
        self.assertEqual(validate_subset(valid_row, item), [])
        for name, mutant in (
            ("leaked repository", dict(valid_row, repository="r")),
            ("leaked task", dict(valid_row, task="#1")),
            ("leaked execution_profile", dict(valid_row, execution_profile="LOCAL_BUILDER")),
            ("leaked scheduler_origin", dict(valid_row, scheduler_origin="WEB")),
            ("missing execution_environment", {k: v for k, v in valid_row.items() if k != "execution_environment"}),
            ("missing compatibility_group", {k: v for k, v in valid_row.items() if k != "compatibility_group"}),
            ("missing protected_claim_key", {k: v for k, v in valid_row.items() if k != "protected_claim_key"}),
            ("missing claimed_by", {k: v for k, v in valid_row.items() if k != "claimed_by"}),
            ("raw null group", dict(valid_row, compatibility_group=None)),
            ("empty group", dict(valid_row, compatibility_group="")),
            ("UNKNOWN sentinel", dict(valid_row, execution_environment="UNKNOWN")),
            ("empty key", dict(valid_row, protected_claim_key="")),
        ):
            with self.subTest(mutant=name):
                self.assertNotEqual(validate_subset(mutant, item), [])


class ExecutionStateConformanceTests(unittest.TestCase):
    """H2 + duplicate-active-key machine enforcement (R5, P1-3/P2-1 probe).

    The owned execution-state conformance path is the pair of the real
    ``schemas/execution-state.schema.json`` conditional and the
    ``v34_rules.execution_state_projection_problems`` probe; both must fail
    closed on the same contradictory states.
    """

    def _rows(self) -> list[dict]:
        source = [
            {
                "repository": "r",
                "task": "#861",
                "role": "builder",
                "dispatch_id": "d-a",
                "execution_profile": "LOCAL_BUILDER",
            },
            {
                "repository": "r",
                "task": "#862",
                "role": "reviewer",
                "dispatch_id": "d-b",
                "execution_profile": "WEB_REVIEWER",
            },
        ]
        return project_active_dispatches(source)

    def _state(self, rows: list[dict], **extra) -> dict:
        state = {
            "repository": "r",
            "work_item": "#861",
            "workflow_state": "implementing",
            "ready_queues": [],
            "derived_from": ["test"],
            "active_dispatches": rows,
        }
        state.update(extra)
        return state

    def test_h2_singular_primary_with_multi_active_fails_closed_everywhere(self) -> None:
        schema = load_schema(EXECUTION_STATE_SCHEMA)
        assert_supported_schema(schema)
        state = self._state(
            self._rows(),
            active_dispatch="d-a",
            active_dispatch_role="builder",
        )
        self.assertNotEqual(validate_subset(state, schema), [])
        self.assertEqual(
            execution_state_projection_problems(state),
            ["H2_SINGULAR_PRIMARY_WITH_MULTI_ACTIVE"],
        )

    def test_h2_null_singular_fields_with_multi_active_are_conformant(self) -> None:
        schema = load_schema(EXECUTION_STATE_SCHEMA)
        state = self._state(
            self._rows(),
            active_dispatch=None,
            active_dispatch_role=None,
        )
        self.assertEqual(validate_subset(state, schema), [])
        self.assertEqual(execution_state_projection_problems(state), [])

    def test_h2_singular_primary_with_single_active_row_stays_readable(self) -> None:
        schema = load_schema(EXECUTION_STATE_SCHEMA)
        rows = [self._rows()[0]]
        state = self._state(rows, active_dispatch="d-a", active_dispatch_role="builder")
        self.assertEqual(validate_subset(state, schema), [])
        self.assertEqual(execution_state_projection_problems(state), [])

    def test_duplicate_active_claim_keys_are_flagged_by_the_conformance_probe(self) -> None:
        # #861 rule 2 / oracle H6: two active rows with the same derived claim
        # key are an impossible canonical state; the projection boundary must
        # detect it. The schema subset cannot express cross-row key uniqueness,
        # so the machine probe is the owned detection surface.
        rows = self._rows()
        rows[1]["protected_claim_key"] = rows[0]["protected_claim_key"]
        state = self._state(rows)
        self.assertEqual(validate_subset(state, load_schema(EXECUTION_STATE_SCHEMA)), [])
        self.assertEqual(
            execution_state_projection_problems(state),
            ["DUPLICATE_ACTIVE_CLAIM_KEY"],
        )

    def test_malformed_rows_fail_closed_in_the_probe(self) -> None:
        state = self._state([{"dispatch_id": "d-x"}])
        self.assertEqual(
            execution_state_projection_problems(state),
            ["ACTIVE_DISPATCH_ROW_MALFORMED"],
        )
        self.assertEqual(
            execution_state_projection_problems(dict(self._state(self._rows()), active_dispatches="nope")),
            ["ACTIVE_DISPATCH_ROW_MALFORMED"],
        )


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
        # R5 (P1-1): nested conditional — non-default groups require the ref,
        # the reserved __default__ and blank-only normalized defaults do not.
        self.assertEqual(
            conditional[0]["then"]["else"]["else"]["required"],
            ["compatibility_authority_ref"],
        )
        self.assertEqual(dispatch_field("execution_environment")["enum"], ["WEB", "LOCAL"])
        self.assertEqual(dispatch_field("scheduler_origin")["enum"], ["WEB", "LOCAL"])


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
