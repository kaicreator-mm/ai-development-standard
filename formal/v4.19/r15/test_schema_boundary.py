"""R15 syntax-vs-authority negatives; fixture is the candidate's exact Git blob."""
import unittest
from pathlib import Path

from schema_boundary import PINNED_SCHEMA_BLOB, assess, git_blob

FIXTURE = Path(__file__).parent / "fixtures" / "dispatch.schema.json"


def builder():
    return {"dispatch_id": "D1", "repository": "example/repo", "version": "v1", "task": "#1",
            "role": "builder", "execution_profile": "WEB_BUILDER", "branch": "main",
            "expected_base_sha": "0" * 40, "pinned_standard_revision": "d" * 40,
            "agent_freedom": "F1_BOUNDED_IMPLEMENTATION", "dispatch_state": "READY",
            "task_pack_ref": "taskpack"}


def validator():
    d = builder()
    d.pop("task_pack_ref")
    d.update(role="validator", execution_profile="LOCAL_VALIDATION",
             requested_head_sha="1" * 40, validation_profile="host-validation")
    return d


class CandidateSchemaShapeVsAuthority(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = FIXTURE.read_bytes()

    def check_case(self, value, shape_status):
        output = assess(self.raw, value)
        self.assertEqual(output["source_binding"], "EXACT_BLOB_PASS")
        self.assertEqual(output["shape_status"], shape_status)
        self.assertFalse(output["publication_authorized"])
        self.assertEqual(output["canonical_admission"], "NOT_PROVEN")
        return output

    def test_exact_candidate_fixture_bytes(self):
        self.assertEqual(git_blob(self.raw), PINNED_SCHEMA_BLOB)

    def test_web_builder_shape_only(self):
        self.check_case(builder(), "SHAPE_VALID_ONLY")

    def test_local_validator_shape_only(self):
        self.check_case(validator(), "SHAPE_VALID_ONLY")

    def test_null_requested_sha_schema_valid_not_admitted(self):
        d = validator()
        d["requested_head_sha"] = None
        self.check_case(d, "SHAPE_VALID_ONLY")

    def test_null_validation_profile_schema_valid_not_admitted(self):
        d = validator()
        d["validation_profile"] = None
        self.check_case(d, "SHAPE_VALID_ONLY")

    def test_validator_missing_requested_head_rejected(self):
        d = validator()
        del d["requested_head_sha"]
        self.check_case(d, "INVALID_SCHEMA")

    def test_unknown_profile_rejected(self):
        d = validator()
        d["execution_profile"] = "WEB_VALIDATOR"
        self.check_case(d, "INVALID_SCHEMA")

    def test_profile_role_mismatch_rejected(self):
        d = validator()
        d["role"] = "reviewer"
        self.check_case(d, "INVALID_SCHEMA")

    def test_malformed_sha_rejected(self):
        d = validator()
        d["requested_head_sha"] = "123"
        self.check_case(d, "INVALID_SCHEMA")

    def test_wrong_well_formed_project_pin_still_shape_valid(self):
        d = builder()
        d["pinned_standard_revision"] = "a" * 40
        self.check_case(d, "SHAPE_VALID_ONLY")

    def test_missing_builder_task_pack_rejected(self):
        d = builder()
        del d["task_pack_ref"]
        self.check_case(d, "INVALID_SCHEMA")

    def test_tampered_schema_rejected_before_validation(self):
        output = assess(self.raw + b"\n", builder())
        self.assertEqual(output["source_binding"], "BLOCK")
        self.assertEqual(output["shape_status"], "NOT_RUN")
        self.assertFalse(output["publication_authorized"])


if __name__ == "__main__":
    unittest.main()
