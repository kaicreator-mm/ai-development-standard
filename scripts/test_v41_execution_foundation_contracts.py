from __future__ import annotations

import unittest

from test_protocol_schemas import load_schema, validate_subset


SHA = "d7273fc7f1300c1fda5d36e38aed641865b0addc"
BASE_SHA = "db1c960459a1eb896cae6c101c0c57347fee5b96"


class V41ExecutionFoundationContractTests(unittest.TestCase):
    def test_execution_context_accepts_material_facts(self) -> None:
        schema = load_schema("execution-context-v1.schema.json")
        value = {
            "schema_version": 1,
            "subject": {
                "repository": "kaicreator-mm/ai-development-standard",
                "sha": SHA,
                "task": "T01",
                "issue": "#192",
            },
            "source_workspace": {
                "kind": "git-worktree",
                "workspace_id": "task-192",
                "branch_ref": "task/192-v41-execution-context-contracts",
                "materialization": "full",
                "working_tree_clean": True,
            },
            "dependency_toolchain": {
                "profile_ref": "profiles/python-tooling.json",
                "manifest_refs": ["pyproject.toml"],
                "lock_refs": [],
                "observed_runtime_toolchain": "python 3.14",
            },
            "configuration": {
                "profile_ref": "project-overrides#execution-foundation",
                "non_secret_fingerprint": "sha256:example",
                "secret_refs": [
                    {
                        "ref": "github-oidc:cloud-role/read-only",
                        "source": "oidc",
                        "scope": "test-read-only",
                    }
                ],
            },
            "artifacts": {
                "relevant": [
                    {
                        "class": "VALIDATION_EVIDENCE",
                        "identity": "sha256:evidence",
                        "ref": "evidence/t01.json",
                    }
                ]
            },
            "external_systems": [
                {
                    "system_id": "example-db",
                    "dependency_fidelity": "real",
                    "environment_class": "ephemeral-real",
                    "environment_ref": "testcontainers:postgres",
                    "state_scope": "ephemeral-isolated",
                    "side_effect_authority": "bounded-write",
                    "credential_ref": "local-test-credential-ref",
                }
            ],
            "executor": {
                "host_role": "ubuntu-build-host",
                "environment_ref": "build-host-01",
            },
        }
        self.assertEqual(validate_subset(value, schema), [])

    def test_execution_context_rejects_authority_state(self) -> None:
        schema = load_schema("execution-context-v1.schema.json")
        value = {
            "schema_version": 1,
            "subject": {
                "repository": "kaicreator-mm/ai-development-standard",
                "sha": SHA,
            },
            "state": "PASS",
        }
        errors = validate_subset(value, schema)
        self.assertTrue(any("state" in error for error in errors), errors)

    def test_execution_context_rejects_secret_value_escape_hatch(self) -> None:
        schema = load_schema("execution-context-v1.schema.json")
        value = {
            "schema_version": 1,
            "subject": {
                "repository": "kaicreator-mm/ai-development-standard",
                "sha": SHA,
            },
            "configuration": {
                "secret_refs": [
                    {
                        "ref": "vault:kv/app/token",
                        "source": "vault",
                        "scope": "integration",
                        "value": "must-never-be-durable",
                    }
                ]
            },
        }
        errors = validate_subset(value, schema)
        self.assertTrue(any("value" in error for error in errors), errors)

    def test_dependency_toolchain_profile_keeps_compatibility_and_certification_distinct(self) -> None:
        schema = load_schema("dependency-toolchain-profile-v1.schema.json")
        value = {
            "schema_version": 1,
            "profile_id": "node-app",
            "repository": "example/app",
            "manifests": [
                {
                    "path": "package.json",
                    "authority": "repository",
                    "dependency_class_scope": ["runtime", "development"],
                }
            ],
            "lock_or_resolution_sources": [
                {
                    "path": "package-lock.json",
                    "mode": "frozen-install",
                    "content_identity": "sha256:lock",
                }
            ],
            "dependency_classes": ["runtime", "development", "transitive"],
            "toolchains": [
                {
                    "name": "node",
                    "compatibility": ">=20 <23",
                    "supported_lines": ["20", "22"],
                    "preferred_development": "22.x",
                    "deployment_identity": "node:22.4.0-image-digest",
                }
            ],
            "certification_tuples": [
                {
                    "toolchain": "node",
                    "version": "22.4.0",
                    "platform": "linux-x64",
                    "validation_profile": "release",
                    "evidence_ref": "validation/node-22.4.0.json",
                }
            ],
            "change_policy": "lockfile delta requires Validation Impact",
        }
        self.assertEqual(validate_subset(value, schema), [])

    def test_dependency_toolchain_profile_requires_real_contract_core(self) -> None:
        schema = load_schema("dependency-toolchain-profile-v1.schema.json")
        value = {
            "schema_version": 1,
            "profile_id": "too-thin",
            "repository": "example/app",
        }
        errors = validate_subset(value, schema)
        for field in ("manifests", "toolchains", "certification_tuples"):
            self.assertTrue(any(field in error for error in errors), errors)

    def test_dependency_risk_exception_is_not_pass(self) -> None:
        schema = load_schema("dependency-risk-exception-v1.schema.json")
        valid = {
            "schema_version": 1,
            "exception_id": "risk-2026-001",
            "advisory_id": "GHSA-example",
            "package": "example-package",
            "version": "1.2.3",
            "dependency_class": "development",
            "dependency_path": ["root", "example-package"],
            "exposure": "development-only",
            "severity": "moderate",
            "reason": "no production exposure; upgrade scheduled",
            "mitigation": "keep package out of production image",
            "authority": "Frozen Task/Release risk decision",
            "owner": "tooling",
            "created_at": "2026-09-29T00:00:00Z",
            "review_by": "2026-10-15T00:00:00Z",
            "release_scope": "4.1.0",
            "status": "accepted-risk",
            "evidence_refs": ["audit/report.json"],
        }
        self.assertEqual(validate_subset(valid, schema), [])

        invalid = dict(valid, status="PASS")
        errors = validate_subset(invalid, schema)
        self.assertTrue(any("status" in error for error in errors), errors)

    def test_historical_v4_dispatch_stays_valid_without_v41_refs(self) -> None:
        schema = load_schema("dispatch.schema.json")
        value = {
            "dispatch_id": "dispatch-T01-builder",
            "repository": "kaicreator-mm/ai-development-standard",
            "version": "4.0.0",
            "task": "T01",
            "issue": "#192",
            "role": "builder",
            "execution_profile": "LOCAL_BUILDER",
            "branch": "task/example",
            "expected_base_sha": BASE_SHA,
            "task_pack_ref": "docs/task-pack.md",
            "pinned_standard_revision": BASE_SHA,
            "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
            "dispatch_state": "READY",
        }
        self.assertEqual(validate_subset(value, schema), [])

        value["execution_context_requirements_ref"] = "execution/context.json"
        value["dependency_toolchain_profile_ref"] = "profiles/toolchain.json"
        self.assertEqual(validate_subset(value, schema), [])
        self.assertIn("execution_context_requirements_ref", schema["properties"])
        self.assertIn("dependency_toolchain_profile_ref", schema["properties"])

    def test_historical_v4_validation_report_stays_valid_without_v41_refs(self) -> None:
        schema = load_schema("validation-report.schema.json")
        value = {
            "repository": "kaicreator-mm/ai-development-standard",
            "tested_sha": SHA,
            "execution_host_role": "ubuntu-build-host",
            "platform": "linux-x64",
            "runtime_toolchain": "python 3.14",
            "validation_profile": "concern",
            "command": "python scripts/test_protocol_schemas.py",
            "state": "BLOCKED",
        }
        self.assertEqual(validate_subset(value, schema), [])

        value["execution_context_ref"] = "evidence/execution-context.json"
        value["dependency_toolchain_profile_ref"] = "profiles/toolchain.json"
        self.assertEqual(validate_subset(value, schema), [])
        self.assertIn("execution_context_ref", schema["properties"])
        self.assertIn("dependency_toolchain_profile_ref", schema["properties"])

    def test_historical_v4_execution_pack_stays_valid_without_v41_refs(self) -> None:
        schema = load_schema("execution-pack-manifest.schema.json")
        value = {
            "pack_id": "pack-T01",
            "task_id": "T01",
            "repository": "kaicreator-mm/ai-development-standard",
            "version": "4.0.0",
            "base_sha": BASE_SHA,
            "task_pack_ref": "docs/task-pack.md",
            "branch": "task/example",
            "agent_freedom": "F1_BOUNDED_IMPLEMENTATION",
            "pinned_standard_revision": BASE_SHA,
            "generated_by": "chatgpt-web",
            "generated_at": "2026-09-29T00:00:00Z",
            "core_artifacts": [
                "MANIFEST.yaml",
                "EXECUTION_CONTRACT.md",
                "TEST_MATRIX.yaml",
                "FAILURE_MATRIX.yaml",
                "IMPLEMENTATION_MAP.md",
                "REVIEW_CHECKLIST.md",
            ],
            "retention": "transient",
        }
        self.assertEqual(validate_subset(value, schema), [])

        value["execution_context_requirements_ref"] = "execution/requirements.json"
        value["dependency_toolchain_profile_ref"] = "profiles/toolchain.json"
        self.assertEqual(validate_subset(value, schema), [])
        self.assertIn("execution_context_requirements_ref", schema["properties"])
        self.assertIn("dependency_toolchain_profile_ref", schema["properties"])


if __name__ == "__main__":
    unittest.main()
