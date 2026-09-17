from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


def load_schema(name: str) -> dict:
    with (SCHEMA_DIR / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_subset(value, schema: dict, path: str = "$") -> list[str]:
    """Validate the JSON-Schema subset used by the standard's machine contracts.

    The repository intentionally avoids a third-party jsonschema dependency in its
    minimal verifier. This covers the contract keywords currently used here:
    type, required, properties, additionalProperties, enum, const, pattern,
    minLength, minItems, and items.
    """
    errors: list[str] = []
    schema_type = schema.get("type")
    if schema_type is not None:
        allowed = schema_type if isinstance(schema_type, list) else [schema_type]
        matches = False
        for expected in allowed:
            matches |= {
                "object": isinstance(value, dict),
                "array": isinstance(value, list),
                "string": isinstance(value, str),
                "integer": isinstance(value, int) and not isinstance(value, bool),
                "null": value is None,
            }.get(expected, True)
        if not matches:
            return [f"{path}: expected type {allowed}, got {type(value).__name__}"]

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} not in enum")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: string shorter than minLength")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            errors.append(f"{path}: string does not match pattern {schema['pattern']!r}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: array shorter than minItems")
        if "items" in schema:
            for index, item in enumerate(value):
                errors.extend(validate_subset(item, schema["items"], f"{path}[{index}]"))
    if isinstance(value, dict):
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{path}: missing required property {required!r}")
        properties = schema.get("properties", {})
        for key, item in value.items():
            if key in properties:
                errors.extend(validate_subset(item, properties[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected property {key!r}")
    return errors


class ProtocolSchemaTests(unittest.TestCase):
    def test_schema_documents_parse(self) -> None:
        for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
            with self.subTest(schema=path.name):
                schema = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(schema.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(schema.get("type"), "object")
                self.assertTrue(schema.get("required"))

    def test_agent_event_examples(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        valid = {
            "schema": "ai-dev/event-v2",
            "event": "REVIEW_RESULT",
            "actor_role": "reviewer",
            "operator_kind": "chatgpt-web",
            "operator_id": "chatgpt-web:web-b",
            "session_ref": "review-session-b",
            "transport_actor": "github:kaicreator-mm",
            "task": "#14",
            "pr": "#18",
            "sha": "d7273fc7f1300c1fda5d36e38aed641865b0addc",
            "status": "PASS",
            "next_state": "merge-ready",
        }
        self.assertEqual(validate_subset(valid, schema), [])
        invalid = dict(valid, sha="short", actor_role="builder-ish")
        errors = validate_subset(invalid, schema)
        self.assertTrue(any("sha" in error for error in errors), errors)
        self.assertTrue(any("actor_role" in error for error in errors), errors)

    def test_task_contract_examples(self) -> None:
        schema = load_schema("task-contract.schema.json")
        valid = {
            "task_id": "T02",
            "goal": "Machine-verifiable standard contracts",
            "integration_target": "version/v3.2.0",
            "baseline_sha": "db1c960459a1eb896cae6c101c0c57347fee5b96",
            "review_policy": "required",
            "required_gates": ["verify-standard"],
            "acceptance": ["manifest-declared asset deletion fails"],
            "dependencies": [],
        }
        self.assertEqual(validate_subset(valid, schema), [])
        invalid = dict(valid, review_policy="sometimes", required_gates=[])
        errors = validate_subset(invalid, schema)
        self.assertTrue(any("review_policy" in error for error in errors), errors)
        self.assertTrue(any("required_gates" in error for error in errors), errors)

    def test_validation_report_examples(self) -> None:
        schema = load_schema("validation-report.schema.json")
        valid = {
            "repository": "kaicreator-mm/ai-development-standard",
            "tested_sha": "d7273fc7f1300c1fda5d36e38aed641865b0addc",
            "execution_host_role": "github-actions",
            "platform": "ubuntu-latest",
            "runtime_toolchain": "Python 3.13",
            "validation_profile": "minimal-ci",
            "command": "python scripts/verify_standard.py",
            "exit_code": 0,
            "state": "PASS",
        }
        self.assertEqual(validate_subset(valid, schema), [])
        invalid = dict(valid, tested_sha="main", state="GREEN")
        errors = validate_subset(invalid, schema)
        self.assertTrue(any("tested_sha" in error for error in errors), errors)
        self.assertTrue(any("state" in error for error in errors), errors)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(ProtocolSchemaTests)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
