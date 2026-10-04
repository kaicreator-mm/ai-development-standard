"""V4.8 T-006 registry/discoverability/adoption composition oracle.

Successor focused verifier for the architecture-aligned rebind: the pinned
v4.7 T01-T06 discovery stack is current v4.8 discovery machinery, and the
three v4.8 machine families are registered into it without a new semantic
owner. Structural/semantic mutations are applied to in-memory fixtures and
must fail closed (RA-N01..RA-N13), including contradiction-aware text probes
that reject an affirmative grant even when every required safe token is
still present. This module is implementation evidence, not a permissions
engine and not independent Validation.
"""
from __future__ import annotations

from copy import deepcopy
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_v47_authority_registry import RegistryError, resolve_registry
from test_v47_compatibility_aliases import validate_current_aliases
from test_v47_state_dimension_registry import consistency_errors
from resolve_standard_read_set import resolve_standard_read_set

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "standard-manifest.json"
ENTRY_SCHEMA = ROOT / "schemas" / "authority-applicability-entry-v1.schema.json"

BASE_MANIFEST_SHA = "e433c18bef84fea15abbc8d308fd9c9b4384c520"
V47_SOURCE_SHA = "d8f613127d0167453297a5a5e983de048607aa07"

V48_MACHINE_FAMILIES = (
    "schemas/task-learning-v1.schema.json",
    "schemas/agent-capability-profile-v1.schema.json",
    "schemas/agent-capability-evidence-v1.schema.json",
)
INTERCHANGE_V1 = "schemas/interchange-envelope-v1.schema.json"

COPY_EXACT = (
    "schemas/authority-applicability-entry-v1.schema.json",
    "schemas/state-dimension-registry-v1.schema.json",
    "scripts/test_v47_convergence_metadata_contracts.py",
    "references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md",
    "scripts/test_v47_authority_registry.py",
    "registries/state-dimensions-v1.json",
    "references/STATE_DIMENSION_REGISTRY_REFERENCE.md",
    "scripts/test_v47_state_dimension_registry.py",
    "standards/REFERENCE_CONVENTION_STANDARD.md",
    "references/REFERENCE_CONVENTION_REFERENCE.md",
    "scripts/test_v47_reference_conventions.py",
    "references/PROGRESSIVE_DISCLOSURE_ROUTING.md",
    "scripts/resolve_standard_read_set.py",
    "scripts/test_v47_progressive_disclosure.py",
    "references/COMPATIBILITY_ALIAS_CONFORMANCE.md",
    "scripts/test_v47_compatibility_aliases.py",
)
COPY_EXACT_BLOBS = {
    "schemas/authority-applicability-entry-v1.schema.json": "2e4a0c26053fbc55ba44aea93d6de377a5ecfb97",
    "schemas/state-dimension-registry-v1.schema.json": "54e3b8f8147e211c5028690c9f1fa72e1e5d1dbd",
    "scripts/test_v47_convergence_metadata_contracts.py": "22337a95afcef0bd4da5ac029f750398a997d098",
    "references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md": "59fd5f842fb27a42db9e7b6bd8e348fcf79d1a3b",
    "scripts/test_v47_authority_registry.py": "731e3fd4b00145dfe3ebf50f8322016b2d420a0c",
    "registries/state-dimensions-v1.json": "c6f955ca576ddd63bbda25a674737d86880209b7",
    "references/STATE_DIMENSION_REGISTRY_REFERENCE.md": "60ce5b58ecbfc46b1c624ebdfd9af01a0d6262b7",
    "scripts/test_v47_state_dimension_registry.py": "4541d57738297a0f2c4524e128e10275e368032f",
    "standards/REFERENCE_CONVENTION_STANDARD.md": "ba6a95b124c1804ea4e13c5c6d058e9ade2cc905",
    "references/REFERENCE_CONVENTION_REFERENCE.md": "4b79f1ad217d090fae4a60f13ec7757fab39ffbd",
    "scripts/test_v47_reference_conventions.py": "bf6888bd0171f1d560766120eeeaa9ffc6802c05",
    "references/PROGRESSIVE_DISCLOSURE_ROUTING.md": "1a9b88411e6249232d514311496ed7170d81d7a2",
    "scripts/resolve_standard_read_set.py": "2adae919945e1381e8a20cad65e9dcf44384771c",
    "scripts/test_v47_progressive_disclosure.py": "b9660f7d066ab9d030b56108762471b76513a4a7",
    "references/COMPATIBILITY_ALIAS_CONFORMANCE.md": "c7009868f3f8f8987635075c7e3c1c755411537a",
    "scripts/test_v47_compatibility_aliases.py": "80d9f4832ad0b81b393216aa7132433e6a06b116",
}

V47_SEMANTIC_AUTHORITY_ENTRIES = [
    {"schema_version": 1, "entry_id": "development-lifecycle", "semantic_concern": "development.lifecycle_and_task_stage", "canonical_owner_ref": "standards/DEVELOPMENT_WORKFLOW.md", "applicability_posture": "ALWAYS", "compatibility_alias_refs": ["standards/VERSION_INTEGRATION_WORKFLOW.md"]},
    {"schema_version": 1, "entry_id": "github-agent-coordination", "semantic_concern": "github.issue_pr_event_coordination", "canonical_owner_ref": "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md", "applicability_posture": "MATERIALITY_DRIVEN", "compatibility_alias_refs": ["standards/GITHUB_WORKFLOW.md"]},
    {"schema_version": 1, "entry_id": "execution-state", "semantic_concern": "execution.controller_and_dispatch_state", "canonical_owner_ref": "standards/EXECUTION_ARCHITECTURE_STANDARD.md", "applicability_posture": "MATERIALITY_DRIVEN"},
    {"schema_version": 1, "entry_id": "work-item-contract", "semantic_concern": "github.work_item_contract", "canonical_owner_ref": "standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md", "applicability_posture": "MATERIALITY_DRIVEN"},
    {"schema_version": 1, "entry_id": "validation-evidence", "semantic_concern": "validation.concern_evidence_and_exact_subject", "canonical_owner_ref": "standards/VALIDATION_STANDARD.md", "applicability_posture": "MATERIALITY_DRIVEN"},
    {"schema_version": 1, "entry_id": "release-qualification", "semantic_concern": "release.qualification_and_candidate_gate", "canonical_owner_ref": "standards/RELEASE_STANDARD.md", "applicability_posture": "MATERIALITY_DRIVEN"},
    {"schema_version": 1, "entry_id": "runner-capability", "semantic_concern": "ci.runner_capability_adoption", "canonical_owner_ref": "standards/CI_RUNNER_CAPABILITY_STANDARD.md", "applicability_posture": "PROJECT_DEFINED"},
    {"schema_version": 1, "entry_id": "research-demo", "semantic_concern": "architecture.research_demo", "canonical_owner_ref": "standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md", "applicability_posture": "OPTIONAL"},
]

V48_NEW_AUTHORITY_ENTRIES = [
    {"schema_version": 1, "entry_id": "task-learning-evidence", "semantic_concern": "execution.task_learning_evidence", "canonical_owner_ref": "standards/EXECUTION_ARCHITECTURE_STANDARD.md", "applicability_posture": "MATERIALITY_DRIVEN"},
    {"schema_version": 1, "entry_id": "logical-agent-capability-profile", "semantic_concern": "execution.logical_agent_capability_claim", "canonical_owner_ref": "standards/EXECUTION_ARCHITECTURE_STANDARD.md", "applicability_posture": "MATERIALITY_DRIVEN"},
    {"schema_version": 1, "entry_id": "agent-capability-evidence", "semantic_concern": "execution.agent_capability_evidence", "canonical_owner_ref": "standards/EXECUTION_ARCHITECTURE_STANDARD.md", "applicability_posture": "MATERIALITY_DRIVEN"},
]

AUTHORIZED_SECTION_ADDITIONS = {
    "discovery_standards": {"standards/REFERENCE_CONVENTION_STANDARD.md"},
    "machine_contracts": set(V48_MACHINE_FAMILIES) | {
        "schemas/authority-applicability-entry-v1.schema.json",
        "schemas/state-dimension-registry-v1.schema.json",
    },
    "registries": {"registries/state-dimensions-v1.json"},
    "references": {
        "references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md",
        "references/COMPATIBILITY_ALIAS_CONFORMANCE.md",
        "references/PROGRESSIVE_DISCLOSURE_ROUTING.md",
        "references/REFERENCE_CONVENTION_REFERENCE.md",
        "references/STATE_DIMENSION_REGISTRY_REFERENCE.md",
        "references/V48_REGISTRY_ADOPTION_REFERENCE.md",
    },
    "verification": {
        "scripts/resolve_standard_read_set.py",
        "scripts/test_v47_authority_registry.py",
        "scripts/test_v47_compatibility_aliases.py",
        "scripts/test_v47_convergence_metadata_contracts.py",
        "scripts/test_v47_progressive_disclosure.py",
        "scripts/test_v47_reference_conventions.py",
        "scripts/test_v47_state_dimension_registry.py",
        "scripts/test_v48_registry_adoption.py",
    },
}

# Frozen pre-T006 baseline inventory (standard-manifest.json at BASE_MANIFEST_SHA).
# Authorization for future additive manifest changes stays with each owning change;
# this constant only pins the exact-candidate diff contract of T-006.
BASELINE_SECTIONS = json.loads(r"""
{
  "authority": ["AGENTS.md", "CHANGELOG.md", "README.md", "VERSION", "standard-manifest.json"],
  "normative_standards": ["standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md", "standards/CHATGPT_WEB_ROLE.md", "standards/CI_EVIDENCE_STANDARD.md", "standards/CI_EXECUTION_STANDARD.md", "standards/CI_RUNNER_CAPABILITY_STANDARD.md", "standards/CODEX_HANDOFF_PROTOCOL.md", "standards/CODEX_ROLE.md", "standards/DEVELOPMENT_WORKFLOW.md", "standards/DOCUMENTATION_STANDARD.md", "standards/EXECUTION_ARCHITECTURE_STANDARD.md", "standards/EXECUTION_PACK_STANDARD.md", "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md", "standards/GITHUB_CAPABILITY_FALLBACK.md", "standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md", "standards/GOLDEN_TEMPLATE_STANDARD.md", "standards/ISSUE_FIRST_TASK_TRIGGER.md", "standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md", "standards/MODEL_USAGE_POLICY.md", "standards/PROJECT_ADOPTION.md", "standards/PROJECT_STRUCTURE.md", "standards/RELEASE_STANDARD.md", "standards/REPOSITORY_STANDARD.md", "standards/TESTING_STANDARD.md", "standards/TEST_DATA_AND_SCENARIO_STANDARD.md", "standards/VALIDATION_STANDARD.md"],
  "compatibility_entries": ["standards/GITHUB_WORKFLOW.md", "standards/VERSION_INTEGRATION_WORKFLOW.md"],
  "templates": ["templates/GOLDEN_INDEX.md", "templates/agent-event-comment.md", "templates/blocker-issue.md", "templates/bug-fix-issue.md", "templates/ci-runner-capability.yaml", "templates/codex-handoff-issue.md", "templates/execution-pack/EXECUTION_CONTRACT.md", "templates/execution-pack/FAILURE_MATRIX.yaml.md", "templates/execution-pack/IMPLEMENTATION_MAP.md", "templates/execution-pack/MANIFEST.yaml.md", "templates/execution-pack/README.md", "templates/execution-pack/REVIEW_CHECKLIST.md", "templates/execution-pack/TEST_MATRIX.yaml.md", "templates/final-closeout.md", "templates/golden/ANTI_PATTERNS.md", "templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md", "templates/golden/STANDARD_COVERAGE.json", "templates/golden/V4_ADOPTION_MIGRATION_EXAMPLES.json", "templates/golden/V4_DOGFOOD_HARDENING_EXAMPLES.json", "templates/golden/V4_OPERATION_ASSURANCE_EXAMPLES.json", "templates/golden/V4_R2_MACHINE_HARDENING_EXAMPLES.json", "templates/golden/V4_REFERENCE_FLOWS.json", "templates/implementation-pr.md", "templates/local-agent-handoff-issue.md", "templates/planning-amendment-issue.md", "templates/project/.dev-standard/PROJECT_OVERRIDES.md", "templates/project/.dev-standard/VERSION", "templates/project/AGENTS.md", "templates/research-demo-issue.md", "templates/research-demo-report.md", "templates/research-issue.md", "templates/task-dag.md", "templates/task-issue.md", "templates/task-pack.md", "templates/test-data-pack.md", "templates/validation-handoff-queue.md", "templates/validation-report.md", "templates/validation-request-issue.md", "templates/version-dag-state-card.md", "templates/version-issue.md"],
  "checklists": ["checklists/pr-review.md", "checklists/project-init.md", "checklists/research-demo-validation.md", "checklists/test-data-review.md", "checklists/version-closure.md"],
  "prompts": ["prompts/CODEX_EXECUTION.md", "prompts/L1_PRODUCT_EVIDENCE.md", "prompts/L2_ARCHITECTURE_EVIDENCE.md", "prompts/L3_IMPLEMENTATION_EVIDENCE.md", "prompts/TEST_DATA_GENERATION.md", "prompts/independent-review-bootstrap.md", "prompts/local-agent-bootstrap.md", "prompts/local-builder-bootstrap.md", "prompts/local-validator-bootstrap.md", "prompts/web-reviewer-bootstrap.md"],
  "machine_contracts": ["schemas/agent-event-v2.schema.json", "schemas/assurance-plan-v1.schema.json", "schemas/dispatch.schema.json", "schemas/execution-pack-manifest.schema.json", "schemas/execution-state.schema.json", "schemas/interchange-envelope-v1.schema.json", "schemas/local-agent-handoff.schema.json", "schemas/operation-binding-v1.schema.json", "schemas/operation-v1.schema.json", "schemas/repository-integration-v4-precondition.schema.json", "schemas/review-aggregation-v1.schema.json", "schemas/review-finding-v1.schema.json", "schemas/task-contract.schema.json", "schemas/validation-report.schema.json"],
  "references": ["references/CI_EVIDENCE_REFERENCE_VALIDATION.md", "references/GITHUB_ENGINEERING_REFERENCES.md", "references/TEST_DATA_ENGINEERING_REFERENCES.md", "references/WOODPECKER_LOCAL_BACKEND_REFERENCE.md", "references/WOODPECKER_UBUNTU_BUILD_01_CAPABILITY_2026-09-18.yaml"],
  "verification": [".github/workflows/verify-standard.yml", "scripts/test_execution_architecture.py", "scripts/test_pointer_only_trigger_contract.py", "scripts/test_project_execution_profile.py", "scripts/test_protocol_schemas.py", "scripts/test_task_dag_lane_parallelism.py", "scripts/test_v33_lifecycle_contracts.py", "scripts/test_v33_semantic_regressions.py", "scripts/test_v34_lifecycle_contracts.py", "scripts/test_v34_review_repairs.py", "scripts/test_v40_adoption_migration.py", "scripts/test_v40_dogfood_hardening.py", "scripts/test_v40_final_hardening.py", "scripts/test_v40_operation_contracts.py", "scripts/test_v40_r2_machine_hardening.py", "scripts/test_v40_r3_carryforward.py", "scripts/test_v40_reference_flows.py", "scripts/test_v40_t010_canonical_surface.py", "scripts/test_v40_t010_successor_hardening.py", "scripts/test_v40_t012_pre_release_hardening.py", "scripts/test_verify_project_standard.py", "scripts/test_verify_standard.py", "scripts/test_work_item_contract_and_golden_templates.py", "scripts/v34_rules.py", "scripts/v40_r2_hardening.py", "scripts/v40_r3_hardening.py", "scripts/v40_rules.py", "scripts/v40_semantics.py", "scripts/v40_t010_successor_hardening.py", "scripts/v40_t012_pre_release_hardening.py", "scripts/verify_event_writer_surfaces.py", "scripts/verify_project_execution_profile.py", "scripts/verify_project_standard.py", "scripts/verify_runner_capability_reference.py", "scripts/verify_standard.py"]
}
""")

# Sequential-integration composition predecessor inventory (standard-manifest.json
# at COMPOSITION_BASE_MAIN f62930bd3512a463358b8b642b1bbc5993566940): the v4.1/v4.2/
# v4.3-sequential registrations that composition authorization #787@5981213563 (rule 5:
# union of both sides' registrations, zero duplicate owner concerns/paths) authorizes
# the composed manifest to carry alongside the frozen v4.8 baseline + T-006 authorized
# additions. Anything outside baseline | authorized | predecessor remains unauthorized;
# removal or duplication of any baseline/predecessor entry remains a problem.
PREDECESSOR_COMPOSITION_SECTIONS = json.loads(r"""
{
  "authority": [
    "AGENTS.md",
    "CHANGELOG.md",
    "README.md",
    "VERSION",
    "standard-manifest.json"
  ],
  "normative_standards": [
    "standards/ARCHITECTURE_DESIGN_STANDARD.md",
    "standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md",
    "standards/CHATGPT_WEB_ROLE.md",
    "standards/CI_EVIDENCE_STANDARD.md",
    "standards/CI_EXECUTION_STANDARD.md",
    "standards/CI_RUNNER_CAPABILITY_STANDARD.md",
    "standards/CODEX_HANDOFF_PROTOCOL.md",
    "standards/CODEX_ROLE.md",
    "standards/CONFIGURATION_SECRETS_STANDARD.md",
    "standards/DATA_MIGRATION_GOVERNANCE_STANDARD.md",
    "standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md",
    "standards/DEVELOPMENT_WORKFLOW.md",
    "standards/DOCUMENTATION_STANDARD.md",
    "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
    "standards/EXECUTION_PACK_STANDARD.md",
    "standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md",
    "standards/GIT_EXECUTION_STANDARD.md",
    "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
    "standards/GITHUB_CAPABILITY_FALLBACK.md",
    "standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md",
    "standards/GOLDEN_TEMPLATE_STANDARD.md",
    "standards/IMPLEMENTATION_QUALITY_STANDARD.md",
    "standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md",
    "standards/ISSUE_FIRST_TASK_TRIGGER.md",
    "standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md",
    "standards/MODEL_USAGE_POLICY.md",
    "standards/PROJECT_ADOPTION.md",
    "standards/PROJECT_STRUCTURE.md",
    "standards/RELEASE_STANDARD.md",
    "standards/REPOSITORY_STANDARD.md",
    "standards/TASK_DAG_GOVERNANCE_STANDARD.md",
    "standards/TASK_DECOMPOSITION_STANDARD.md",
    "standards/TESTING_STANDARD.md",
    "standards/TEST_DATA_AND_SCENARIO_STANDARD.md",
    "standards/VALIDATION_STANDARD.md",
    "standards/WORKSPACE_ARTIFACT_STANDARD.md"
  ],
  "compatibility_entries": [
    "standards/GITHUB_WORKFLOW.md",
    "standards/VERSION_INTEGRATION_WORKFLOW.md"
  ],
  "templates": [
    "templates/GOLDEN_INDEX.md",
    "templates/agent-event-comment.md",
    "templates/blocker-issue.md",
    "templates/bug-fix-issue.md",
    "templates/ci-runner-capability.yaml",
    "templates/codex-handoff-issue.md",
    "templates/execution-pack/EXECUTION_CONTRACT.md",
    "templates/execution-pack/FAILURE_MATRIX.yaml.md",
    "templates/execution-pack/IMPLEMENTATION_MAP.md",
    "templates/execution-pack/MANIFEST.yaml.md",
    "templates/execution-pack/README.md",
    "templates/execution-pack/REVIEW_CHECKLIST.md",
    "templates/execution-pack/TEST_MATRIX.yaml.md",
    "templates/final-closeout.md",
    "templates/golden/ANTI_PATTERNS.md",
    "templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md",
    "templates/golden/STANDARD_COVERAGE.json",
    "templates/golden/V4_ADOPTION_MIGRATION_EXAMPLES.json",
    "templates/golden/V4_DOGFOOD_HARDENING_EXAMPLES.json",
    "templates/golden/V4_OPERATION_ASSURANCE_EXAMPLES.json",
    "templates/golden/V4_R2_MACHINE_HARDENING_EXAMPLES.json",
    "templates/golden/V4_REFERENCE_FLOWS.json",
    "templates/implementation-pr.md",
    "templates/local-agent-handoff-issue.md",
    "templates/planning-amendment-issue.md",
    "templates/project/.dev-standard/PROJECT_OVERRIDES.md",
    "templates/project/.dev-standard/VERSION",
    "templates/project/AGENTS.md",
    "templates/research-demo-issue.md",
    "templates/research-demo-report.md",
    "templates/research-issue.md",
    "templates/task-dag.md",
    "templates/task-issue.md",
    "templates/task-pack.md",
    "templates/test-data-pack.md",
    "templates/validation-handoff-queue.md",
    "templates/validation-report.md",
    "templates/validation-request-issue.md",
    "templates/version-dag-state-card.md",
    "templates/version-issue.md"
  ],
  "checklists": [
    "checklists/pr-review.md",
    "checklists/project-init.md",
    "checklists/research-demo-validation.md",
    "checklists/test-data-review.md",
    "checklists/version-closure.md"
  ],
  "prompts": [
    "prompts/CODEX_EXECUTION.md",
    "prompts/L1_PRODUCT_EVIDENCE.md",
    "prompts/L2_ARCHITECTURE_EVIDENCE.md",
    "prompts/L3_IMPLEMENTATION_EVIDENCE.md",
    "prompts/TEST_DATA_GENERATION.md",
    "prompts/independent-review-bootstrap.md",
    "prompts/local-agent-bootstrap.md",
    "prompts/local-builder-bootstrap.md",
    "prompts/local-validator-bootstrap.md",
    "prompts/web-reviewer-bootstrap.md"
  ],
  "machine_contracts": [
    "schemas/agent-event-v2.schema.json",
    "schemas/assurance-plan-v1.schema.json",
    "schemas/dag-mutation-record-v1.schema.json",
    "schemas/compatibility-record-v1.schema.json",
    "schemas/dependency-risk-exception-v1.schema.json",
    "schemas/dependency-toolchain-profile-v1.schema.json",
    "schemas/dispatch.schema.json",
    "schemas/execution-context-v1.schema.json",
    "schemas/execution-pack-manifest.schema.json",
    "schemas/execution-state.schema.json",
    "schemas/interchange-envelope-v1.schema.json",
    "schemas/local-agent-handoff.schema.json",
    "schemas/migration-transition-v1.schema.json",
    "schemas/operation-binding-v1.schema.json",
    "schemas/operation-v1.schema.json",
    "schemas/repository-integration-v4-precondition.schema.json",
    "schemas/review-aggregation-v1.schema.json",
    "schemas/review-finding-v1.schema.json",
    "schemas/task-contract.schema.json",
    "schemas/validation-report.schema.json"
  ],
  "profiles": [
    "profiles/README.md",
    "profiles/languages/typescript.md",
    "profiles/languages/python.md",
    "profiles/languages/go.md",
    "profiles/languages/java.md",
    "profiles/languages/rust.md",
    "profiles/archetypes/library.md",
    "profiles/archetypes/service.md",
    "profiles/archetypes/cli.md"
  ],
  "references": [
    "references/ARCHITECTURE_DECISION_REFERENCE.md",
    "references/CI_EVIDENCE_REFERENCE_VALIDATION.md",
    "references/CONFIGURATION_SECRETS_REFERENCE.md",
    "references/DATA_MIGRATION_REFERENCE.md",
    "references/DEPENDENCY_TOOLCHAIN_REFERENCE.md",
    "references/EXTERNAL_SYSTEM_EXECUTION_REFERENCE.md",
    "references/GIT_EXECUTION_REFERENCE.md",
    "references/GITHUB_ENGINEERING_REFERENCES.md",
    "references/IMPLEMENTATION_PROFILE_ADOPTION_REFERENCE.md",
    "references/IMPLEMENTATION_QUALITY_REFERENCE.md",
    "references/TASK_DAG_GOVERNANCE_REFERENCE.md",
    "references/TASK_DECOMPOSITION_REFERENCE.md",
    "references/INTERFACE_COMPATIBILITY_REFERENCE.md",
    "references/TEST_DATA_ENGINEERING_REFERENCES.md",
    "references/WOODPECKER_LOCAL_BACKEND_REFERENCE.md",
    "references/WOODPECKER_UBUNTU_BUILD_01_CAPABILITY_2026-09-18.yaml",
    "references/WORKSPACE_ARTIFACT_REFERENCE.md"
  ],
  "verification": [
    ".github/workflows/verify-standard.yml",
    "scripts/test_execution_architecture.py",
    "scripts/test_pointer_only_trigger_contract.py",
    "scripts/test_project_execution_profile.py",
    "scripts/test_protocol_schemas.py",
    "scripts/test_task_dag_lane_parallelism.py",
    "scripts/test_v33_lifecycle_contracts.py",
    "scripts/test_v33_semantic_regressions.py",
    "scripts/test_v34_lifecycle_contracts.py",
    "scripts/test_v34_review_repairs.py",
    "scripts/test_v40_adoption_migration.py",
    "scripts/test_v40_dogfood_hardening.py",
    "scripts/test_v40_final_hardening.py",
    "scripts/test_v40_operation_contracts.py",
    "scripts/test_v40_r2_machine_hardening.py",
    "scripts/test_v40_r3_carryforward.py",
    "scripts/test_v40_reference_flows.py",
    "scripts/test_v40_t010_canonical_surface.py",
    "scripts/test_v40_t010_successor_hardening.py",
    "scripts/test_v40_t012_pre_release_hardening.py",
    "scripts/test_v43_adoption_wiring.py",
    "scripts/test_v43_archetype_profiles.py",
    "scripts/test_v43_architecture_design.py",
    "scripts/test_v43_dag_mutation_contract.py",
    "scripts/test_v43_go_java_rust_profiles.py",
    "scripts/test_v43_implementation_quality.py",
    "scripts/test_v43_profile_framework.py",
    "scripts/test_v43_task_dag_governance.py",
    "scripts/test_v43_task_decomposition.py",
    "scripts/test_v43_ts_python_profiles.py",
    "scripts/test_v41_adoption_wiring.py",
    "scripts/test_v41_configuration_secrets.py",
    "scripts/test_v41_dependency_toolchain.py",
    "scripts/test_v41_execution_foundation_contracts.py",
    "scripts/test_v41_external_systems.py",
    "scripts/test_v41_git_execution.py",
    "scripts/test_v41_workspace_artifact.py",
    "scripts/test_v42_adoption_wiring.py",
    "scripts/test_v42_data_migration.py",
    "scripts/test_v42_interface_compatibility.py",
    "scripts/test_verify_project_standard.py",
    "scripts/test_verify_standard.py",
    "scripts/test_work_item_contract_and_golden_templates.py",
    "scripts/v34_rules.py",
    "scripts/v40_r2_hardening.py",
    "scripts/v40_r3_hardening.py",
    "scripts/v40_rules.py",
    "scripts/v40_semantics.py",
    "scripts/v40_t010_successor_hardening.py",
    "scripts/v40_t012_pre_release_hardening.py",
    "scripts/verify_event_writer_surfaces.py",
    "scripts/verify_project_execution_profile.py",
    "scripts/verify_project_standard.py",
    "scripts/verify_runner_capability_reference.py",
    "scripts/verify_standard.py"
  ]
}
""")

ADOPTION = ROOT / "standards" / "PROJECT_ADOPTION.md"
OVERRIDES = ROOT / "templates" / "project" / ".dev-standard" / "PROJECT_OVERRIDES.md"
V48_REFERENCE = ROOT / "references" / "V48_REGISTRY_ADOPTION_REFERENCE.md"
MIGRATION = ROOT / "docs" / "implementation" / "4.8.0" / "MIGRATION_ADOPTION.md"


def git_blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def checkout_normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n") if b"\r\n" in data else data


def carried_blob_problems(overrides: dict[str, bytes] | None = None) -> list[str]:
    """RA-01/RA-N11: every COPY_EXACT path must equal its pinned v4.7 blob."""
    problems = []
    for rel in COPY_EXACT:
        pinned = COPY_EXACT_BLOBS[rel]
        raw = overrides.get(rel) if overrides else None
        if raw is None:
            path = ROOT / rel
            if not path.is_file():
                problems.append(f"missing carried path: {rel}")
                continue
            raw = path.read_bytes()
        staged = git_index_blob(rel)
        if staged is not None and overrides is None:
            actual = staged
        else:
            actual = git_blob_id(checkout_normalized(raw))
        if actual != pinned:
            problems.append(f"carried bytes diverge from pinned v4.7 blob: {rel}")
    return problems


def git_index_blob(rel: str) -> str | None:
    result = subprocess.run(
        ["git", "ls-files", "-s", "--", rel], cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    return result.stdout.split()[1]


def base_manifest_binding_problems() -> list[str]:
    """Bind the embedded baseline to the frozen base manifest when git is available."""
    try:
        shown = subprocess.run(
            ["git", "show", f"{BASE_MANIFEST_SHA}:standard-manifest.json"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        )
    except OSError:
        return []
    if shown.returncode != 0:
        return []
    embedded = json.loads(json.dumps(BASELINE_SECTIONS))
    frozen = json.loads(shown.stdout).get("sections")
    if embedded != frozen:
        return ["embedded BASELINE_SECTIONS no longer match the frozen base manifest"]
    return []


def section_conformance_problems(candidate: dict) -> list[str]:
    """RA-02/RA-N12: candidate sections == frozen v4.8 baseline + T-006 authorized
    additions + sequential-composition predecessor inventory exactly.

    The carried reference-convention standard is registered under the dedicated
    non-normative ``discovery_standards`` section: it is a discovery/conformance
    surface, never a new normative semantic owner, so the golden-coverage
    contract over ``normative_standards`` stays exactly as frozen.

    Composition re-binding (#787@5981213563 rule 5): the sequential integration
    successor composes the RQ-qualified v4.8 candidate 0ac1a3d4 onto main
    f62930bd, so PREDECESSOR_COMPOSITION_SECTIONS pins the predecessor
    (v4.1/v4.2/v4.3-sequential) registrations the composed union is authorized to
    carry. The guard stays exact-set over baseline | authorized | predecessor:
    any unlisted path, any removal of a baseline/predecessor entry and any
    duplicate remains a problem. Manifest list order is not a governed semantic.
    """
    problems = []
    sections = candidate.get("sections")
    if not isinstance(sections, dict):
        return ["candidate manifest has no sections object"]
    baseline = BASELINE_SECTIONS
    predecessor = PREDECESSOR_COMPOSITION_SECTIONS
    expected_sections = set(baseline) | set(AUTHORIZED_SECTION_ADDITIONS) | set(predecessor)
    if set(sections) != expected_sections:
        problems.append(
            f"manifest section set changed: only {sorted(expected_sections)} are allowed"
        )
    for section in sorted(expected_sections):
        base = set(baseline.get(section, ())) | set(predecessor.get(section, ()))
        expected_additions = set(AUTHORIZED_SECTION_ADDITIONS.get(section, ()))
        got = sections.get(section)
        if not isinstance(got, list):
            problems.append(f"missing authorized section: {section}")
            continue
        got_set = set(got)
        if len(got) != len(got_set):
            problems.append(f"duplicate manifest entry in {section}")
        if not base.issubset(got_set):
            problems.append(f"historical inventory removed from {section}: {sorted(base - got_set)}")
        if got_set - base != expected_additions:
            problems.append(
                f"unauthorized additions to {section}: {sorted(got_set - base - expected_additions)}"
            )
    return problems


def machine_family_problems(candidate: dict) -> list[str]:
    """RA-03/RA-04/RA-N01/RA-N02/RA-N06 at manifest level."""
    problems = []
    contracts = candidate.get("sections", {}).get("machine_contracts", [])
    for family in V48_MACHINE_FAMILIES:
        count = contracts.count(family)
        if count != 1:
            problems.append(f"v4.8 machine family must be registered exactly once: {family}")
    if contracts.count(INTERCHANGE_V1) != 1:
        problems.append("interchange v1 must remain registered exactly once")
    for rel in contracts:
        if "interchange" in rel.lower() and rel != INTERCHANGE_V1:
            problems.append(f"second interchange-like owner is forbidden: {rel}")
    for rel in contracts:
        stem = rel.split("/")[1].lower()
        if stem.startswith(("availability", "provider-capability", "capability-availability")):
            problems.append(f"availability/provider metadata must stay a derived non-family: {rel}")
        if "interchange" in stem and stem.endswith("-v2.schema.json"):
            problems.append(f"second-version envelope owner is forbidden: {rel}")
    return problems


def semantic_registry_problems(candidate: dict) -> list[str]:
    """RA-05/RA-N07: carried + new entries resolve deterministically and add exactly three."""
    problems = []
    schema = json.loads(ENTRY_SCHEMA.read_text(encoding="utf-8"))
    try:
        resolve_registry(candidate, schema, root=ROOT)
        validate_current_aliases(candidate, schema, root=ROOT)
    except RegistryError as exc:
        return [f"semantic registry does not resolve: {exc}"]
    entries = candidate.get("semantic_authorities", {}).get("entries", [])
    v47_ids = {v["entry_id"] for v in V47_SEMANTIC_AUTHORITY_ENTRIES}
    carried = [e for e in entries if e.get("entry_id") in v47_ids]
    expected_carried = {v["entry_id"]: v for v in V47_SEMANTIC_AUTHORITY_ENTRIES}
    if any(e != expected_carried.get(e.get("entry_id")) for e in carried):
        problems.append("v4.7 semantic authority entries were not carried forward intact")
    if len(carried) != len(V47_SEMANTIC_AUTHORITY_ENTRIES):
        problems.append("v4.7 semantic authority entries were not carried forward intact")
    by_id = {e.get("entry_id"): e for e in entries}
    for expected in V48_NEW_AUTHORITY_ENTRIES:
        got = by_id.get(expected["entry_id"])
        if got != expected:
            problems.append(f"missing or altered v4.8 discovery entry: {expected['entry_id']}")
    if len(entries) != len(V47_SEMANTIC_AUTHORITY_ENTRIES) + len(V48_NEW_AUTHORITY_ENTRIES):
        problems.append("semantic registry entry count deviates from carried + exactly three new")
    return problems


def state_registry_problems() -> list[str]:
    """RA-07: owner-qualified dimensions with resolvable forbidden inferences."""
    problems = []
    registry = json.loads((ROOT / "registries" / "state-dimensions-v1.json").read_text(encoding="utf-8"))
    problems.extend(consistency_errors(registry))
    registered = ROOT / "standard-manifest.json"
    if "registries/state-dimensions-v1.json" not in registered.read_text(encoding="utf-8"):
        problems.append("state dimension registry is not discoverable through the manifest")
    return problems


def doc_slice(text: str, start: str, end: str | None) -> str:
    begin = text.index(start)
    finish = text.index(end, begin) if end else len(text)
    return text[begin:finish]


NEGATION_TOKENS = (
    "must not", "never", "cannot", "can not", "does not", "do not", "not ",
    "non-authoritative", "no authority", "not.", "not,", "stay",
    "remains", "remain", "不得", "不能", "不会", "并非", "禁止", "不授予", "不是",
    "不产生", "不拥有", "非权威", "不构成", "不取代",
)

FORBIDDEN_DOC_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("RA-N03", re.compile(r"\b(registr\w+|read[- ]routing|routing metadata|discovery)\b[^.!?\n]{0,90}\b(grants?|authoriz\w+|gives?|confers?|gates?|owns?)\b[^.!?\n]{0,60}\b(mutation|authority|gate|validation|review|release|merge)\b", re.I)),
    ("RA-N04", re.compile(r"\b(provider|model)\b[^.!?\n]{0,70}\b(identit\w+|availabilit\w+)\b[^.!?\n]{0,70}\b(certif\w+|proves?|proved|authoriz\w+|grants?|admits?|warrants?)\b", re.I)),
    ("RA-N05", re.compile(r"\bcapabilit\w+\b[^.!?\n]{0,80}\b(owns?|absorbs?|replaces?|becomes?)\b[^.!?\n]{0,80}\b(current (validation|review|availabilit\w+)|validation or review truth|runner[- ]host resources)\b", re.I)),
    ("RA-N06/PROSE", re.compile(r"\b(availability|capabilit\w+ evidence|task learning)\b[^.!?\n]{0,70}\bis a durable\b", re.I)),
    ("RA-N09", re.compile(r"\b(authority_effect|gate_effect)\s*=\s*(?!NONE\b)[A-Za-z_]+")),
    ("RA-N09", re.compile(r"\bmutation_authorized\s*=\s*true\b", re.I)),
    ("RA-N10", re.compile(r"\bFast Path\b[^.!?\n]{0,90}\b(must|shall)\b[^.!?\n]{0,60}\b(load|instantiat\w+|includ\w+)\b", re.I)),
    ("RA-N13/IDENTITY", re.compile(r"\b(PASS|evidence)\b[^.!?\n]{0,50}[0-9a-f]{40}[^.!?\n]{0,60}\b(applies to|valid for|successor)\b", re.I)),
)

GUARDED_DOCS = {
    "references/V48_REGISTRY_ADOPTION_REFERENCE.md": (
        V48_REFERENCE,
        ["authority_effect=NONE", "gate_effect=NONE", "mutation_authorized=false",
         "EXACTLY_3", "REUSE_EXISTING_V1_EXACTLY_ONCE", "PROVIDER_IDENTITY=NOT_AUTHORITY",
         "CAPABILITY_EVIDENCE=NOT_CURRENT_VALIDATION_REVIEW_TRUTH", "TASK_LEARNING=NONE_MATERIAL"],
        None,
        None,
    ),
    "standards/PROJECT_ADOPTION.md": (
        ADOPTION,
        ["standard-manifest.json#semantic_authorities", "registries/state-dimensions-v1.json",
         "resolve_standard_read_set", "V48_REGISTRY_ADOPTION_REFERENCE",
         "MIGRATION_ADOPTION", "authority_effect=NONE", "gate_effect=NONE",
         "mutation_authorized=false", "TASK_LEARNING=NONE_MATERIAL"],
        "### 2.5 v4.8 Convergence Discovery",
        "## 3. PROJECT_OVERRIDES",
    ),
    "docs/implementation/4.8.0/MIGRATION_ADOPTION.md": (
        MIGRATION,
        ["original subject", "never", "TASK_LEARNING=NONE_MATERIAL", "authority_effect=NONE",
         "gate_effect=NONE", "mutation_authorized=false", "interchange-envelope-v1.schema.json",
         "no Interchange v2"],
        None,
        None,
    ),
    "templates/project/.dev-standard/PROJECT_OVERRIDES.md": (
        OVERRIDES,
        ["standard-manifest.json#semantic_authorities", "authority_effect=NONE",
         "gate_effect=NONE", "mutation_authorized=false", "TASK_LEARNING=NONE_MATERIAL",
         "MIGRATION_ADOPTION"],
        "### v4.8 Convergence Discovery",
        "## Execution Pack / Pull Worker Profile",
    ),
}


def guarded_text(name: str) -> str:
    path, _, start, end = GUARDED_DOCS[name]
    text = path.read_text(encoding="utf-8")
    return doc_slice(text, start, end) if start else text


def contradiction_problems(text: str) -> list[str]:
    """RA-N03/04/05/09/10/13: bounded contradiction oracle, not token presence.

    A sentence is contradictory when it affirmatively joins a guarded topic
    with an authority grant and carries no negation marker. Bounded, ordered,
    deterministic; it performs no general natural-language inference.
    """
    problems = []
    for rule_id, pattern in FORBIDDEN_DOC_PATTERNS:
        for match in pattern.finditer(text):
            begin = text.rfind("\n", 0, match.start()) + 1
            nxt = text.find("\n", match.end())
            sentence = text[begin: nxt if nxt != -1 else len(text)].lower()
            if any(token in sentence for token in NEGATION_TOKENS):
                continue
            problems.append(f"{rule_id}: contradictory grant sentence: {sentence.strip()[:120]}")
    return problems


def adoption_fast_path_problems() -> list[str]:
    """RA-08/RA-N10 positive wiring: optional materiality and Fast Path preserved."""
    problems = []
    overrides = OVERRIDES.read_text(encoding="utf-8")
    for token in ("`v4.fast_path`", "`v4.adoption_level`", "MUST NOT weaken",
                  "execution_pack.enabled", "validation_queue.enabled"):
        if token not in overrides:
            problems.append(f"project overrides lost Fast Path/adoption surface: {token}")
    adoption = ADOPTION.read_text(encoding="utf-8")
    for token in ("TASK_LEARNING=NONE_MATERIAL", "不构成项目采用义务",
                  "Fast Path 保持轻量"):
        if token not in adoption:
            problems.append(f"project adoption lost optional-materiality/Fast Path statement: {token}")
    return problems


def historical_binding_problems() -> list[str]:
    """RA-09/RA-N08: no v4.7 historical evidence path is registered or rebound."""
    problems = []
    sections = json.loads(MANIFEST.read_text(encoding="utf-8"))["sections"]
    for section, values in sections.items():
        for rel in values:
            if rel.startswith("docs/implementation/4.7.0/") or "V47_SEMANTIC_CONFORMANCE_MATRIX" in rel:
                problems.append(f"historical v4.7 evidence registered as current: {rel}")
    return problems


class RegistryAdoptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.schema = json.loads(ENTRY_SCHEMA.read_text(encoding="utf-8"))

    # --- positive structure -------------------------------------------------

    def test_ra01_carried_v47_stack_matches_pinned_blobs(self) -> None:
        self.assertEqual(carried_blob_problems(), [])
        problems = base_manifest_binding_problems()
        self.assertEqual(problems, [])

    def test_ra02_base_inventory_preserved_additively(self) -> None:
        self.assertEqual(section_conformance_problems(self.manifest), [])

    def test_ra03_exactly_three_v48_machine_families_once(self) -> None:
        self.assertEqual(machine_family_problems(self.manifest), [])
        contracts = self.manifest["sections"]["machine_contracts"]
        for family in V48_MACHINE_FAMILIES:
            self.assertEqual(contracts.count(family), 1)
        registered_v48 = [p for p in contracts if "-v1.schema.json" in p and p in set(V48_MACHINE_FAMILIES)]
        self.assertEqual(len(registered_v48), 3)

    def test_ra04_interchange_v1_exactly_once_no_second_owner(self) -> None:
        contracts = self.manifest["sections"]["machine_contracts"]
        self.assertEqual(contracts.count(INTERCHANGE_V1), 1)
        self.assertEqual(machine_family_problems(self.manifest), [])

    def test_ra05_registry_resolves_one_owner_per_concern_without_authority(self) -> None:
        self.assertEqual(semantic_registry_problems(self.manifest), [])
        resolved = resolve_registry(self.manifest, self.schema, root=ROOT)
        for expected in V48_NEW_AUTHORITY_ENTRIES:
            self.assertEqual(resolved[expected["semantic_concern"]], expected["canonical_owner_ref"])
        self.assertEqual(resolved["ci.runner_capability_adoption"], "standards/CI_RUNNER_CAPABILITY_STANDARD.md")
        for entry in self.manifest["semantic_authorities"]["entries"]:
            for forbidden in ("mutation_allowed", "merge_allowed", "release_ready", "normative_body"):
                self.assertNotIn(forbidden, entry)

    def test_all_registered_local_paths_exist(self) -> None:
        for section, values in self.manifest["sections"].items():
            for rel in values:
                self.assertTrue((ROOT / rel).is_file(), f"{section}: {rel}")

    def test_ra06_read_router_is_fail_closed_and_non_authoritative(self) -> None:
        with self._router_fixture() as (project, ads):
            request = {
                "task_issue_ref": "https://github.com/kaicreator-mm/demo/issues/7",
                "task_pack_ref": "docs/tasks/T06.md",
                "subject_sha": "b" * 40,
                "base_sha": "c" * 40,
                "requested_concerns": ["execution.task_learning_evidence"],
                "requested_capabilities": [],
                "stage": "read",
                "intent": "read",
                "chat_history": "",
                "provider_available": True,
            }
            facts = {
                "task_issue_ref": request["task_issue_ref"],
                "task_pack_ref": request["task_pack_ref"],
                "current_subject_sha": request["subject_sha"],
                "current_base_sha": request["base_sha"],
                "materiality": {"execution.task_learning_evidence": {"decision": "APPLICABLE", "source_ref": request["task_issue_ref"]}},
            }
            result = resolve_standard_read_set(
                project, ads, request,
                authority_reader=lambda _request: deepcopy(facts),
                revision_probe=lambda _root: "a" * 40,
                authority_reader_scope="TEST_FIXTURE",
            )
            self.assertEqual(result["status"], "RESOLVED")
            self.assertEqual(result["authority_effect"], "NONE")
            self.assertEqual(result["gate_effect"], "NONE")
            self.assertFalse(result["mutation_authorized"])
            owners = [item["ref"] for item in result["read_set"] if item["kind"] == "semantic-owner"]
            self.assertIn("ads:standards/EXECUTION_ARCHITECTURE_STANDARD.md", owners)

            drift = deepcopy(request)
            drift["requested_concerns"] = ["runtime.future_unmerged_owner"]
            blocked = resolve_standard_read_set(
                project, ads, drift,
                authority_reader=lambda _request: deepcopy(facts),
                revision_probe=lambda _root: "a" * 40,
                authority_reader_scope="TEST_FIXTURE",
            )
            self.assertEqual(blocked["status"], "BLOCKED")
            self.assertFalse(blocked["mutation_authorized"])

    def test_ra07_state_registry_stays_owner_qualified(self) -> None:
        self.assertEqual(state_registry_problems(), [])

    def test_ra08_adoption_and_overrides_preserve_optional_materiality(self) -> None:
        self.assertEqual(adoption_fast_path_problems(), [])
        for name in GUARDED_DOCS:
            text = guarded_text(name)
            for token in GUARDED_DOCS[name][1]:
                self.assertIn(token, text, f"{name} missing {token}")

    def test_ra09_no_historical_v47_evidence_rebound(self) -> None:
        self.assertEqual(historical_binding_problems(), [])
        for name in GUARDED_DOCS:
            self.assertEqual(contradiction_problems(guarded_text(name)), [], name)

    # --- negative mutation oracles (in-memory, fail closed) ------------------

    def expect_structural_rejection(self, mutant: dict) -> None:
        problems = (
            section_conformance_problems(mutant)
            + machine_family_problems(mutant)
            + semantic_registry_problems(mutant)
        )
        self.assertTrue(problems, "mutation unexpectedly passed all structural oracles")

    def test_ra_n01_fourth_machine_family_fails(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["sections"]["machine_contracts"].append("schemas/provider-capability-v1.schema.json")
        self.expect_structural_rejection(mutant)

    def test_ra_n02_duplicate_interchange_and_v2_fail(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["sections"]["machine_contracts"].append(INTERCHANGE_V1)
        self.expect_structural_rejection(mutant)
        mutant = deepcopy(self.manifest)
        mutant["sections"]["machine_contracts"].append("schemas/interchange-envelope-v2.schema.json")
        self.expect_structural_rejection(mutant)

    def test_ra_n06_availability_as_durable_family_fails(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["sections"]["machine_contracts"].append("schemas/availability-current-v1.schema.json")
        self.expect_structural_rejection(mutant)
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"].append({
            "schema_version": 1, "entry_id": "availability",
            "semantic_concern": "execution.current_availability",
            "canonical_owner_ref": "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
            "applicability_posture": "MATERIALITY_DRIVEN",
        })
        self.expect_structural_rejection(mutant)

    def test_ra_n07_competing_broken_alias_and_unknown_materiality_fail(self) -> None:
        contender = deepcopy(self.manifest["semantic_authorities"]["entries"][0])
        contender["entry_id"] = "competing"
        contender["canonical_owner_ref"] = "standards/RELEASE_STANDARD.md"
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"].append(contender)
        with self.assertRaises(RegistryError):
            resolve_registry(mutant, self.schema)
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][0]["canonical_owner_ref"] = "standards/DOES_NOT_EXIST.md"
        with self.assertRaises(RegistryError):
            resolve_registry(mutant, self.schema, root=ROOT)
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][0]["applicability_posture"] = "IMPLICIT_MANDATORY"
        with self.assertRaises(RegistryError):
            resolve_registry(mutant, self.schema)
        mutant = deepcopy(self.manifest)
        mutant["semantic_authorities"]["entries"][1]["compatibility_alias_refs"] = ["standards/VERSION_INTEGRATION_WORKFLOW.md"]
        with self.assertRaises(RegistryError):
            validate_current_aliases(mutant, self.schema, root=ROOT)

    def test_ra_n08_stale_evidence_rebinding_is_rejected(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["sections"]["references"].append("docs/implementation/4.7.0/CONFORMANCE_EVIDENCE.md")
        self.assertTrue(
            any("unauthorized additions" in p for p in section_conformance_problems(mutant)),
            "historical evidence path registration was not rejected",
        )
        contradictory = (
            "Historical Task Learning PASS d8f613127d0167453297a5a5e983de048607aa07 applies to "
            "v4.8 successor subjects without re-execution."
        )
        for name in GUARDED_DOCS:
            problems = contradiction_problems(guarded_text(name) + "\n" + contradictory)
            self.assertTrue(problems, f"{name} accepted stale-evidence rebinding")

    def test_ra_n11_single_byte_change_to_carried_file_fails(self) -> None:
        target = "standards/REFERENCE_CONVENTION_STANDARD.md"
        raw = (ROOT / target).read_bytes()
        mutated = raw.replace(b"\n", b" \n", 1)
        self.assertNotEqual(mutated, raw)
        problems = carried_blob_problems(overrides={target: mutated})
        self.assertTrue(any("diverge from pinned" in p for p in problems))

    def test_ra_n12_removed_base_inventory_entry_fails(self) -> None:
        mutant = deepcopy(self.manifest)
        mutant["sections"]["references"].remove("references/CI_EVIDENCE_REFERENCE_VALIDATION.md")
        self.expect_structural_rejection(mutant)

    # --- contradiction-aware text oracles ------------------------------------

    def test_ra_n03_n04_n05_n09_n10_n13_contradiction_probes_fail_closed(self) -> None:
        probes = {
            "RA-N03": ("The semantic registry grants mutation authority for adopted concerns and gates their validation outcome.", ("RA-N03",)),
            "RA-N04": ("Provider model identity and availability certify routing admission for the interchange family.", ("RA-N04",)),
            "RA-N05": ("Agent Capability Evidence owns current Validation and Review truth and absorbs runner-host resources.", ("RA-N05",)),
            "RA-N09": ("authority_effect=CONDITIONAL when the registry resolves a concern, and mutation_authorized=true for owners it resolves.", ("RA-N09",)),
            "RA-N10": ("Fast Path must load the state registry and capability profile families before any read.", ("RA-N10",)),
            "RA-N06": ("Current Availability is a durable machine family registered alongside the other three.", ("RA-N06/PROSE",)),
            "RA-N13": ("Historical Task Learning PASS " + "d" * 40 + " applies to v4.8 successor subjects without re-execution.", ("RA-N13/IDENTITY",)),
        }
        for name in GUARDED_DOCS:
            base_text = guarded_text(name)
            self.assertEqual(contradiction_problems(base_text), [], f"{name} baseline must be clean")
            for rule_id, (sentence, expected_prefixes) in probes.items():
                mutated = base_text + "\n" + sentence
                problems = contradiction_problems(mutated)
                self.assertTrue(
                    any(p.startswith(prefix) for p in problems for prefix in expected_prefixes),
                    f"{name} did not reject {rule_id} probe: {problems}",
                )

    def test_negated_versions_of_grant_sentences_are_accepted(self) -> None:
        safe = (
            "The semantic registry does not grant mutation authority for adopted concerns.\n"
            "Provider model identity and availability do not certify routing admission.\n"
            "Fast Path must not load the state registry before any read.\n"
        )
        for name in GUARDED_DOCS:
            self.assertEqual(contradiction_problems(guarded_text(name) + "\n" + safe), [], name)

    # --- read-router fixture --------------------------------------------------

    @classmethod
    @contextmanager
    def _router_fixture(cls):
        tmp = tempfile.TemporaryDirectory()
        try:
            base = Path(tmp.name)
            project = base / "project"
            (project / ".dev-standard").mkdir(parents=True)
            (project / "AGENTS.md").write_text("project authority\n", encoding="utf-8")
            (project / ".dev-standard/VERSION").write_text(
                "repository=kaicreator-mm/ai-development-standard\nversion=4.8.0\nrevision=" + "a" * 40 + "\n",
                encoding="utf-8",
            )
            (project / ".dev-standard/PROJECT_OVERRIDES.md").write_text(
                "# Project Overrides\n"
                "- v4.reducer: enabled + durable facts\n"
                "- v4.controllers: enabled + bounded concerns\n"
                "- v4.interchange: disabled\n"
                "- v4.fast_path: canonical\n"
                "- execution_pack.enabled: false\n"
                "- validation_queue.enabled: false\n",
                encoding="utf-8",
            )
            (project / "docs" / "tasks").mkdir(parents=True)
            (project / "docs/tasks/T06.md").write_text("task T06\n", encoding="utf-8")
            ads = base / "ads"
            (ads / "schemas").mkdir(parents=True)
            (ads / "standards").mkdir()
            (ads / "AGENTS.md").write_text("ads authority\n", encoding="utf-8")
            shutil.copyfile(ROOT / "schemas/authority-applicability-entry-v1.schema.json",
                            ads / "schemas/authority-applicability-entry-v1.schema.json")
            manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
            (ads / "standard-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            for rel in (manifest["sections"]["normative_standards"]
                        + manifest["sections"]["compatibility_entries"]
                        + manifest["sections"].get("references", [])):
                path = ads / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(rel + "\n", encoding="utf-8")
            yield project, ads
        finally:
            tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
