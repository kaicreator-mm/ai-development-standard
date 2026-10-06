"""v4.9 T-015 integrated dogfood / release evidence handoff kernel.

Deterministic stdlib-unittest integrated-dogfood kernel for the LAST
implementation task of the v4.9 Frozen DAG, executed at base
`version/v4.9.0@a4f1debe663813712d4f740ec70c14ca6342b0ac` (tree
`76e18763c525e357a14e2d21036e597b07151a91`, execution pack head
`046710a2d8ac55ec3e2e517cc447d7b1accc31f0`), binding TEST_MATRIX oracles
I01-I06 over the merged v4.9 surfaces:

  I01  predecessor-lineage exact identity — every merged v4.9 task output
       (T-002..T-014) plus the recovered v4.4-v4.7 families bound at the
       exact base with exact blob refs; frozen Product/L2/DAG blobs and the
       immutable DAG v0.1 resolve unchanged.
  I02  representative positive/negative orchestration journeys executed
       deterministically from the T-007 kernel (§28) + T-012 conformance
       surfaces; the extended integrated regression (recovered v4.4-v4.7
       kernels + v4.8/T-013/T-014 lane kernels) re-executed at the candidate.
  I03  normative docs/contracts/tests/registry reconciliation at the
       candidate (pinned battery definition; manifest/registry/coverage
       agreement; undeclared-late-lane-artifact set pinned exactly).
  I04  handoff completeness — no NOT_RUN/BLOCKED converted to PASS; no
       unsupported generality claim for unexercised mechanisms; downstream
       generality NOT_SATISFIED unless the qualifying T-014 contract is met.
  I05  all safety negatives zero for the in-repo journeys (the only runs
       used as evidence here); no stale predecessor/evidence binding
       laundered.
  I06  handoff documents contain no Version Closure / Release Qualification
       verdict (inputs only; verdict authority stays with the later gates).

Consumes read-only: Frozen PRD §16 (blob a8ec7030a14337a4c2dca853dc474e965679d610),
Frozen L2 §14 (blob bd41ea0175b459a6a490fd37ad579e429a58a1c3), the T-014
downstream contract (`references/DOWNSSTREAM_DOGFOOD_AUDIT_CONTRACT_V49.md`),
the T-010 gate matrix row M10, and the T-007/T-012 owner kernels by import.

This is Builder evidence only: it is not independent Validation, not Fresh
Review, not a gate, and never a source of verdicts. The qualifying downstream
dogfood path (distinct product/repository per PRD §16.2 with an independent
safety audit per §16.7) is honestly NOT_RUN in this lane — real external/
downstream inability is recorded BLOCKED/NOT_RUN, never guessed PASS — so
downstream generality stays NOT_SATISFIED for Version Closure.
"""
from __future__ import annotations

import copy
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

# Owner kernels under integrated dogfood (import-only; each also runs its own
# battery separately — importing here binds THIS kernel to their exact code).
import test_v49_execution_core as core_kernel  # noqa: E402  (T-007 owner kernel)
import test_v49_conformance_suite as conf_surface  # noqa: E402  (T-012 conformance surface)

REPORT = ROOT / "docs" / "implementation" / "4.9.0" / "integration" / "INTEGRATION_DOGFOOD_REPORT.md"
HANDOFF = ROOT / "docs" / "implementation" / "4.9.0" / "integration" / "RELEASE_EVIDENCE_HANDOFF.md"
WORKFLOW = ROOT / ".github" / "workflows" / "verify-standard.yml"
DAG_V01 = ROOT / "docs" / "implementation" / "4.9.0" / "task-dag-history" / "TASK_DAG-v0.1-first-candidate.md"
REGISTRY = ROOT / "registries" / "state-dimensions-v1.json"
MANIFEST_JSON = ROOT / "standard-manifest.json"
COVERAGE = ROOT / "templates" / "golden" / "STANDARD_COVERAGE.json"

BASE_SHA = "a4f1debe663813712d4f740ec70c14ca6342b0ac"
BASE_TREE = "76e18763c525e357a14e2d21036e597b07151a91"
PACK_HEAD_SHA = "046710a2d8ac55ec3e2e517cc447d7b1accc31f0"
FROZEN_PRD_BLOB = "a8ec7030a14337a4c2dca853dc474e965679d610"
FROZEN_L2_BLOB = "bd41ea0175b459a6a490fd37ad579e429a58a1c3"
FROZEN_DAG_V02_BLOB = "b9fe0cc7089f64929b4bcf45f7230d950e864db2"
DAG_V01_BLOB = "4f358ba2b32e01ae17ddcdf970151cf28e44bb3f"

# Exact integrated lineage chain (all asserted ancestors of HEAD in I01).
T011_MERGE_SHA = "d53e943ec7109648485b64a647ed2c7cf553531d"
T012_MERGE_SHA = "4322a8cc2a1810e3b49b5a92b502e869ac4c70b6"
T014_MERGE_SHA = "2484d8df361f70b3419817116a4d179b0dcc5424"
RECOVERY_COMPOSITION_SHA = "4c632256ce403acdbffc321db5cb086ef3dec7f8"
RECOVERY_FAMILY_SIDE_SHA = "56137d88749f9e790327deabe45977bbc0d3add4"
RECOMPOSE_COMPOSITION_SHA = "c1d7c96df9fef9420b944398d420b474aa8e4df8"
RECOMPOSE_MERGE_SHA = "e3a2cc0390647abf22b12bd6b925d10d5693b87e"
T013_REBIND_SHA = "9aa51a7feb52c72472949ddc752de788907577c1"

CANDIDATE = "candidate:v4.9.0@sha:a4f1debe663813712d4f740ec70c14ca6342b0ac"
CANDIDATE_RE = re.compile(r"^candidate:[^@\s]+@sha:[0-9a-f]{40}$")

WRITE_SET = (
    "docs/implementation/4.9.0/integration/INTEGRATION_DOGFOOD_REPORT.md",
    "docs/implementation/4.9.0/integration/RELEASE_EVIDENCE_HANDOFF.md",
    "scripts/test_v49_integrated_dogfood.py",
)

PLANNING_PATHS = tuple(
    f".agent/execution/T-015/{name}"
    for name in (
        "MANIFEST.yaml",
        "EXECUTION_CONTRACT.md",
        "IMPLEMENTATION_MAP.md",
        "TEST_MATRIX.yaml",
        "FAILURE_MATRIX.yaml",
        "REVIEW_CHECKLIST.md",
    )
)

# Merged v4.9 task outputs (T-002..T-014), pinned to their exact blobs at the
# integrated candidate. Any mutation of any predecessor output fails I01.
V49_TASK_OUTPUT_BLOBS = {
    "T-002": {
        "references/ASSURANCE_PLAN_V2_COMPATIBILITY.json": "dc68304fb09e0d7e436a2a301117a1d9cc935031",
        "references/ASSURANCE_PLAN_V2_REFERENCE.md": "56605ac0305154b86b72d50069de164a003be0f8",
        "schemas/assurance-plan-v2.schema.json": "92d9c61bc80a3c863aee04f28eebb7ed6291b94a",
        "scripts/test_v49_assurance_plan_v2.py": "c34576aab047b4735aaf24bfb4cfe5659b61db08",
        "standards/ASSURANCE_PLAN_STANDARD.md": "ddc39f2843e7af4b41b1cf2e6b34675c23bcb614",
    },
    "T-003": {
        "references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md": "17d178e579177d93f9641d4e1c4d998459e98b3b",
        "references/STATE_DIMENSION_REGISTRY_REFERENCE.md": "a879afe48f3ca3d1752fa2ea390d91dbe63b6359",
        "registries/state-dimensions-v1.json": "ac92b744f0c751916f226f4d4b60e3ecbb50dd7a",
        "scripts/test_v49_authority_state_registry.py": "228abe554113dd00a84925caa0316fcc5be644ed",
    },
    "T-004": {
        "fixtures/role-execution-profile-v1/capability_profile_as_role_profile.json": "01ac3cdb34c0f2e726c0d45af9040d26f8e93df6",
        "fixtures/role-execution-profile-v1/injected_authority_fields.json": "057c32157d4c1a3aa7e5e7d67f993b2dd4ae225f",
        "fixtures/role-execution-profile-v1/last_writer_wins_reject_profile.json": "022806b206f68df43a18522249fc8c30b89c3f78",
        "fixtures/role-execution-profile-v1/missing_source_ref_profile.json": "4da63a010149e942fad5d53ea185b179d1a15b8e",
        "fixtures/role-execution-profile-v1/over_claim_refs_profile.json": "a45016a1d961183582550dac56229d3328c40141",
        "fixtures/role-execution-profile-v1/source_authority_conflict_profile.json": "31332547df19411d2a4a28846483941575965fd1",
        "fixtures/role-execution-profile-v1/sources/dispatch_requirements_authority.json": "100d1b96f031da0d3e9e75edfd45d6a6b696bbbe",
        "fixtures/role-execution-profile-v1/sources/retired_requirements_authority.json": "9f6916b68f9f6ae33d23bf4bc6a9fff7410b174e",
        "fixtures/role-execution-profile-v1/sources/task_requirements_authority_agreeing.json": "745fc6880999b42e7f7137ea8284152f3649c27a",
        "fixtures/role-execution-profile-v1/sources/task_requirements_authority_conflicting.json": "fc4ca64c5e2cb7ad1b2e7a4ec744c2e8eeeaadfe",
        "fixtures/role-execution-profile-v1/stale_source_ref_profile.json": "dbbed4745ad1147e26951330980c4464b472f474",
        "fixtures/role-execution-profile-v1/valid_builder_profile.json": "fbacb36be42612571ec013ab189157d83dcafbf5",
        "fixtures/role-execution-profile-v1/valid_validator_profile.json": "7806102a312a6cbc73c80652ae0165fc133fca9f",
        "references/ROLE_EXECUTION_PROFILE_V1_REFERENCE.md": "cd16860e72ad26cdcd29f9d26b3c27f787367142",
        "schemas/role-execution-profile-v1.schema.json": "df96fb14dce9f39c753c80483e21c55b27beb685",
        "scripts/test_v49_role_execution_profile.py": "10ed80538bf79f7386f191b5003c34350c079bb4",
    },
    "T-005": {
        "references/RELEASE_APPLICABILITY_REFERENCE.md": "4411d25300542f9d311b0dd4df6be346a0bbda0a",
        "scripts/test_v49_release_applicability.py": "7497f7b07f2086df48112783301cb43d4dbcc006",
        "standards/RELEASE_STANDARD.md": "c4d72506253ca7f3d95e305dbd84aae0e1fbe2cb",
    },
    "T-006": {
        "references/TASK_LEARNING_V2_COMPATIBILITY.json": "feda9fc12b17e91a14597a9130238734d8937c63",
        "references/TASK_LEARNING_V2_REFERENCE.md": "529f2e52fa6ca9e2a41fe154f91c039f33d5eb5f",
        "schemas/task-learning-v2.schema.json": "a7547c2e29bc7551cc066f776d48e3926456022c",
        "scripts/test_v49_task_learning_v2.py": "2cb452ea90838b0660271152637b735048dcc39c",
    },
    "T-007": {
        "fixtures/execution-core-v49/candidates.json": "bbfdf81225164b80302078119e680e2668a5d3d9",
        "fixtures/execution-core-v49/claim_races.json": "ba7c437d541022a040e05bd2b94332ef3ff10241",
        "fixtures/execution-core-v49/facts_current.json": "0327987f0b3bafeaa57d71eb75f2932796e16abc",
        "fixtures/execution-core-v49/facts_lineage_stale.json": "b08cb9ace40a93c9565edce403221a500e18002a",
        "fixtures/execution-core-v49/facts_plan_drift.json": "c36a03004df6a656389541d5912d1ddcbd1ccd92",
        "fixtures/execution-core-v49/facts_successor.json": "62aa1ac8a7b928fb72c693db9903500d75cd461e",
        "fixtures/execution-core-v49/owner_refs.json": "2a9507a8230ca143328ffd742c3b9a692828796b",
        "fixtures/execution-core-v49/phase_table.json": "98b7c5a7dc9323c438ed42f30c723818488da889",
        "references/PROPORTIONAL_ORCHESTRATION_REFERENCE.md": "ccb080d33afcac51b242014b4cafa2a6863df652",
        "scripts/test_v49_execution_core.py": "5ed17b4144fab88e3ce6ca88a70b23288c87b9a9",
        "standards/EXECUTION_ARCHITECTURE_STANDARD.md": "ffe4788beaa342931ddf7c713523fb6f8a53d4c0",
    },
    "T-008": {
        "references/EXECUTION_CONTRACT_REFS_V49_COMPATIBILITY.json": "c05897cb90a8af8aed254ae76addee494f71aa6b",
        "references/EXECUTION_CONTRACT_REFS_V49_REFERENCE.md": "cf8a28880cd50e6cd6191921187edf2f4c0aa1d8",
        "schemas/dispatch.schema.json": "123a66223f6dea42966c4a181dae3cc0776c3ba3",
        "scripts/test_v49_execution_contract_refs.py": "1380174f333de9660957698a6d59f88c020b9476",
    },
    "T-009": {
        "fixtures/jit-dag-governance/classification_table.json": "2706f81915cfc8df73d13be06e84b193237d837e",
        "fixtures/jit-dag-governance/currentness_facts.json": "a7d709665e7447fdd8ffb18c351b5cc43dfd5ebb",
        "fixtures/jit-dag-governance/owner_refs.json": "686dec152ca847cb8694e3fca8267b442f10459d",
        "fixtures/jit-dag-governance/proposals.json": "6ef6ddbc37c2375e09075b9cd974224d0d677e0c",
        "references/JIT_DAG_MUTATION_GOVERNANCE_V49_REFERENCE.md": "a4d58c3610c0e524ae1a2a5ff8018119a254f3e9",
        "scripts/test_v49_jit_dag_governance.py": "e6c3ff4e7156e38abb70302b8e8b3146983a51fd",
    },
    "T-010": {
        "fixtures/gate-currentness/assurance_binding.json": "19d0b1d58046897ca7c81cc320c2a92bb40e337a",
        "fixtures/gate-currentness/dogfood_binding.json": "e5589bdefcba50c4a156c8c05618ddf49439bc61",
        "fixtures/gate-currentness/frozen_candidates.json": "00a36fdb62493d53104f1ac6c6bfd79b6480f6c2",
        "fixtures/gate-currentness/impact_decisions.json": "ff0b0cdbe5984ea0305d39c278777997f3a88fa8",
        "fixtures/gate-currentness/owner_map.json": "1b72e5cdd06d8139cd724374dc3298c7435ddfee",
        "fixtures/gate-currentness/release_applicability.json": "4fb525df247ba39367a0105f3f1de8844f686b0b",
        "fixtures/gate-currentness/stale_pass.json": "f6b4addc27e7b591e55027e1509042c4be99005b",
        "fixtures/gate-currentness/successor_chain.json": "b4d33cb073e0e2f338bd7ca83f7678e99ff3e98b",
        "references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md": "c98b5eeb6e8afda2dc896e4e67edd0383b8a861b",
        "scripts/test_v49_gate_currentness.py": "32519ca9d63bea335a6f71a89297ae2b25351751",
    },
    "T-011": {
        ".github/workflows/verify-standard.yml": "6e81b4d0b767cabb7c06440633a029cd94b17817",
        "docs/implementation/4.9.0/MIGRATION_ADOPTION.md": "467e5e14e88f4acd34649880ea7e8af002df6c8b",
        "references/REGISTRY_ADOPTION_V49_REFERENCE.md": "de303febbc014a35617b00db3ab2d679378eed92",
        "scripts/test_v48_registry_adoption.py": "d947c4e66fea260a1a1ba7b562562e4a4703d1e1",
        "standard-manifest.json": "dc8075c88a155be0e9641ec2aa80bf1c4aff139c",
    },
    "T-012": {
        "fixtures/conformance-suite/carry_forward.json": "f11ce58886dfe1f645050507f550928c5be52807",
        "fixtures/conformance-suite/coverage_manifest.json": "5164a0c647f74082b41bc1c432109a226aac7b5d",
        "fixtures/conformance-suite/currentness_toctou.json": "91cdc3382f611c581beb4809bb23fede444d75be",
        "fixtures/conformance-suite/gate_transfer_currentness.json": "f5176eb773dd99bc9a045f3f2a518a25164f8639",
        "fixtures/conformance-suite/jit_envelope_dag_mutation.json": "a8927180f633ff5b6f907199a7aafe98b2d8ce55",
        "fixtures/conformance-suite/lineage_wait.json": "65b7311f89ee5c5302f50eb160cb27f54b7be873",
        "fixtures/conformance-suite/manual_reconstruction.json": "be2de80338912cb5955e5e8a3112db2fef82cabe",
        "fixtures/conformance-suite/precedence_conjunction.json": "88f102040735341951e91a8f26c33efdd706e681",
        "fixtures/conformance-suite/reduction_fail_closed.json": "971747535753abf8203eaa3bbef486ac0e93d6ed",
        "fixtures/conformance-suite/release_applicability.json": "35a98af0f3101d135e583fe9d3c64e0c62dbdb44",
        "fixtures/conformance-suite/selector_independence.json": "61c15bb08e8d3164dab54bab06aea6cfa3dfb787",
        "fixtures/conformance-suite/task_learning_compat.json": "88b2ed6ec5832dc01ab19fdc19bc0814a85bbc9f",
        "scripts/test_v48_integration_closure.py": "7c4393a4b021b0a65484191532d7e4c53c1378b9",
        "scripts/test_v49_conformance_suite.py": "cc3e29255159233adc0c6e6954c398bad34f80e7",
    },
    "T-013": {
        "fixtures/manual-reference-flow/derived_projections.json": "ec0799d755bbae98a9c8cf75a60ae93aff466096",
        "fixtures/manual-reference-flow/durable_facts.json": "1bf8254c836a3f789f0903498143af9fb486a87e",
        "fixtures/manual-reference-flow/pointer_triggers.json": "478a8c49e0d445810490836af8e051b120971862",
        "fixtures/manual-reference-flow/walkthroughs.json": "8010a113db7e1078f4fa641be035dfd0083aa66a",
        "references/MANUAL_REFERENCE_FLOW_V49.md": "247673d89a4b9b998e15a50222611c3a5a7f3427",
        "scripts/test_v49_manual_reference_flow.py": "fac72340060cc26b51071c4a26ec80aefb159d27",
    },
    "T-014": {
        "fixtures/dogfood-audit-contract/auditor_eligibility.json": "f7eee94f0fc3e79f0ff5629ab6a2e6a75e032008",
        "fixtures/dogfood-audit-contract/fail_closed.json": "5079cda3341dc98f30d648f1ca91f4e6074d2d02",
        "fixtures/dogfood-audit-contract/owner_surfaces.json": "b15a7b7ef355b6757fddb1025898e4a7c994b76a",
        "fixtures/dogfood-audit-contract/report_acceptance.json": "4dc7b68105488eea256518761b0067357dc3bae1",
        "references/DOWNSSTREAM_DOGFOOD_AUDIT_CONTRACT_V49.md": "8c4f6512d44019742957cd99a7a0eca70bc91a1f",
        "scripts/test_v49_dogfood_audit_contract.py": "9c818022c6054fa3905d325627f617abd37de578",
    },
}

# Recovered v4.4-v4.7 family surfaces byte-identical since the recovery composition
# 4c632256 (recovery side 56137d88): pinned to that exact blob at HEAD.
RECOVERED_FAMILY_BLOBS = {
    ".gitattributes": "d76983514ae4be23efac3aa9da919f0cfcd2c010",
    "checklists/pr-review.md": "0ae314bca5395d5ecbc31c880d346c893debd944",
    "checklists/project-init.md": "7256f8654c881f135fcd881615005eef35d56e5a",
    "checklists/version-closure.md": "7b736fe51f8534362c0b098191f2326e18dc326e",
    "docs/implementation/4.4.0/MIGRATION_ADOPTION.md": "55a1c6ef7d8cadfe8e706f3c2d7a2b9d25072c1a",
    "docs/implementation/4.4.0/closure-inputs/T08_INPUTS.json": "ffde7529d35dc4778eac5c733f738697357f94ff",
    "docs/implementation/4.4.0/dogfood/build-package/README.md": "da8a6900a0239a9448ae1c3b4dfa124d65b363ea",
    "docs/implementation/4.4.0/dogfood/build-package/source_v1/__main__.py": "b6eb64dccbba54c2b319b7614643684d820e99a8",
    "docs/implementation/4.4.0/dogfood/build-package/source_v2/__main__.py": "d8ed00b75c0cc62acbda219d4363b4cfc68e5fe2",
    "docs/implementation/4.4.0/dogfood/distribution-deployment/STATUS.md": "0c5d53643b5f0b2557407341ca7739f59144435f",
    "docs/implementation/4.4.0/dogfood/distribution-deployment/cases.json": "d7d3d8921e07450acb5774230b4a24f1e9d07d19",
    "docs/implementation/4.4.0/dogfood/distribution-deployment/sandbox_service.py": "4004ea32d6f59f8e748ee6ee813076d44d3309a5",
    "docs/implementation/4.5.0/MIGRATION_ADOPTION.md": "362de1f47d7dcc1e2e328ea1e67b1df8415368c2",
    "docs/implementation/4.5.0/closure-inputs/T09_INPUTS.json": "e5b4f5678b22fe0a00cd2a457dbb1b94505c9c14",
    "docs/implementation/4.5.0/dogfood/incident-feedback/controlled-incident.json": "37554bc6560007f162f9e80a929d12e3603dab6d",
    "docs/implementation/4.5.0/dogfood/maintenance-hotfix/README.md": "7077410f11f6bf2f3a9f8443ff4d5a952ebfbb95",
    "docs/implementation/4.5.0/dogfood/maintenance-hotfix/VALIDATION_REQUEST.md": "e0656f20a6742fb620cd494c6704ceff77b227e6",
    "docs/implementation/4.5.0/dogfood/maintenance-hotfix/case.json": "1ba2dbe40baa70c21369651fbb3b640de83d8228",
    "docs/implementation/4.5.0/dogfood/maintenance-hotfix/fixture-execution.json": "325919ab6b5972544ca5eb029397d7b64a24d18c",
    "docs/implementation/4.5.0/dogfood/maintenance-hotfix/fixture-test.log": "a939d5780ff4ce6579e98b76fa7b5667357e51f5",
    "docs/implementation/4.5.0/dogfood/maintenance-hotfix/support-policy.json": "68937432b135c80afb8b355df5fe004784bf050a",
    "docs/implementation/4.5.0/dogfood/runtime-observation/README.md": "adaf5a078d0a86e2636994303f7d69a22905865c",
    "docs/implementation/4.5.0/dogfood/runtime-observation/cases.json": "b1f32ac8963e72e64f6e70fad6eb26ea5ba70d35",
    "docs/implementation/4.6.0/CLOSURE_INPUTS.md": "a88a2e40f5f33069147f78a227ef00331d4b0bf6",
    "docs/implementation/4.6.0/MIGRATION_ADOPTION.md": "83af22fa73e74d0cbedd36967662ce433e88cfa4",
    "docs/implementation/4.6.0/dogfood/README.md": "1fa2b01409eeb45f7765c6a0f5cf59dd9e40455e",
    "docs/implementation/4.6.0/dogfood/REAL_RUNTIME_VALIDATION_REQUEST.md": "afab787ddaaf8c75e86c2cce4a2f5803291b8b91",
    "docs/implementation/4.6.0/dogfood/session_operator_handoff_packet.json": "a440d195fcbf40d0d56981e9699d11343833ae14",
    "docs/implementation/4.7.0/CLOSURE_INPUTS.md": "bf3cc8be3b9395d6a3657ae669eea712a38dc551",
    "docs/implementation/4.7.0/FUTURE_MAJOR_REGISTER.md": "27ddd0b26c4fd29722131ffae7deb90a27575324",
    "docs/implementation/4.7.0/MIGRATION_ADOPTION.md": "02790a0ccee2d3f60862d7a651d29c6f0529b713",
    "docs/implementation/4.7.0/dogfood/README.md": "7a9a9ed7e4a7a7365b27cc185817f937aa786f52",
    "docs/implementation/4.7.0/dogfood/VALIDATION_REQUEST.md": "7159962b4023ce291e1c640e25f9cfe05a9fdc1e",
    "docs/implementation/4.7.0/dogfood/reconstruction.json": "1028b91b1219b3412640e871ed195f180888e998",
    "references/AI_NATIVE_EXISTING_OWNER_INTEGRATION.md": "87a1babb960fb7bc57d7ed3f6ce062c477e47ee5",
    "references/BUILD_ARTIFACT_REFERENCE.md": "339ba3e7f36c9d91df06d40a485852c63fd18843",
    "references/CONTEXT_ENGINEERING_REFERENCE.md": "e8be26528cba1a5941fd7557ff0169b92aa976fe",
    "references/DEPLOYMENT_REFERENCE.md": "8e02daeb939f3000ac1b3e0f50f70540b170e6c7",
    "references/DISTRIBUTION_REFERENCE.md": "7abc0197e34058f8a502c72bdf5ed4c2f58643d1",
    "references/INCIDENT_RECOVERY_REFERENCE.md": "8ecba8730e2fd850033b67888a3fe8cab8d99946",
    "references/INTENT_ASSUMPTION_REFERENCE.md": "905ebff0533e772428026de60d96029503b8294e",
    "references/MAINTENANCE_EOL_HOTFIX_REFERENCE.md": "14bf5f691c4c033e57356a2186862b67396ba1cf",
    "references/OBSERVABILITY_RUNTIME_REFERENCE.md": "9c55cac4c2cd0e8e2961215f2ba3cb5df1ef7280",
    "references/SKILL_PROCEDURE_REFERENCE.md": "3ff92a375992b641213435042c5e73ae6b7a3a6b",
    "references/V47_CLOSURE_CONFORMANCE_REFERENCE.md": "ffccae693607ef7b1f94339846c5af7931fe19e3",
    "references/V47_SEMANTIC_CONFORMANCE_MATRIX.md": "c566611ff9f8b3d0952f381ae9548093caf49bc9",
    "schemas/artifact-promotion-v1.schema.json": "8ed743e16d617c4a96b8cf82bf38e7aa9be7e3e3",
    "schemas/build-manifest-v1.schema.json": "95335390fcfb155ac31b144394237bd3a533f06c",
    "schemas/deployment-plan-v1.schema.json": "b25d57cfeaa6f97c8842cd6e78aff3379e3ad1ab",
    "schemas/deployment-result-v1.schema.json": "ef34eaf0e79d91606bf887b2b9ce3864635880ec",
    "schemas/execution-pack-manifest.schema.json": "d8840c0fa42ee1c1bf9e0330c6ad16ffaf01b9ae",
    "schemas/incident-event-v1.schema.json": "dd7c87714e2a959f79e9f50dbc1b4ee01555945a",
    "schemas/intent-assumption-record-v1.schema.json": "2795c373eb2f2abcb33e1934de0c4cd503f72717",
    "schemas/maintenance-policy-v1.schema.json": "f6bca628d5b7d3e00eabe2afab9d38ca00627a79",
    "schemas/runtime-observation-context-v1.schema.json": "6dc1c3085595290d17ebb9f185de59832d8a2d1b",
    "schemas/skill-metadata-v1.schema.json": "20f6021d6b2962c1eddc55ddf3baa5d273afcfe2",
    "scripts/test_v44_adoption_wiring.py": "322800b9a0516c2e2044655b4a8efcde06abfabb",
    "scripts/test_v44_build_artifact.py": "0ee01a05815cd48c94952a59466c732a37877480",
    "scripts/test_v44_build_package_conformance.py": "622477a8d2ac54d484bcf159f35198049d842c4e",
    "scripts/test_v44_cross_standard_conformance.py": "a16e31b670bdddc8fe5ea27326248a36b5e36ee8",
    "scripts/test_v44_delivery_contracts.py": "596cc5685578043a90f35ed79f6e40eeb511308c",
    "scripts/test_v44_deployment.py": "8cad526eb8222b8869f7ca1b0e391b483d0ff2ea",
    "scripts/test_v44_distribution.py": "61c957514692605678a255fda89c2c6c7373141d",
    "scripts/test_v44_distribution_deployment_conformance.py": "74fae79ff1e1a188756b70a43455de63b11fc623",
    "scripts/test_v45_adoption_wiring.py": "25e9d499fb3e6b1f1957d04a072ed25e0e5f2c15",
    "scripts/test_v45_cross_standard_conformance.py": "7c4e70fb0726a238610cee9cec07d5c03d77824a",
    "scripts/test_v45_incident_feedback_conformance.py": "6d96d538fbe95e55a6e82ce6a2adee85011b0057",
    "scripts/test_v45_incident_recovery_feedback.py": "af2d2a8e97a9f71029e9e25004eed6ee5e4f208e",
    "scripts/test_v45_maintenance_hotfix.py": "c0d0b0f6ad30cf1529f7adabfbbe7660c3308ef7",
    "scripts/test_v45_maintenance_hotfix_conformance.py": "02940351ccc1610d842dd62d2d2d3ffd96a89e17",
    "scripts/test_v45_observability_runtime.py": "a62e4460e07c94e08639a66f81fb11c41fc252b3",
    "scripts/test_v45_operations_contracts.py": "32330863df17e21fb874f2bd2e90e26fbcfe7f45",
    "scripts/test_v45_runtime_observation_conformance.py": "de49d0541b2974874b88caad2ffd80b769091bff",
    "scripts/test_v46_adoption_wiring.py": "aa2b9c94e2cf07a4d61ce13c96189d9207867b7f",
    "scripts/test_v46_ai_native_contracts.py": "16a4e7788c12abcc5da3a14dfc210a4af40323ac",
    "scripts/test_v46_context_engineering.py": "77fa171f2b3f6d05142ee87c9d722eb9a7668b1f",
    "scripts/test_v46_cross_standard_conformance.py": "46311fa159e420a4a0302a14472213abc1177f9c",
    "scripts/test_v46_existing_owner_integration.py": "08b77a7c8db042c7f5d0833dde9a2ca5a6381c9a",
    "scripts/test_v46_intent_assumption.py": "6985fda9cb94950794b3777ca9a23ef579d1b15c",
    "scripts/test_v46_session_handoff_dogfood.py": "ef9bc603fb7baa8ca29fa1aead14b7aa94cf0db3",
    "scripts/test_v46_skill_procedure.py": "bd1b02742fe5c396f2cdccbdbf0f5692329dc653",
    "scripts/test_v47_adoption_wiring.py": "3a7097abb719c1bd155d411304402e7f64e2eee2",
    "scripts/test_v47_cross_standard_closure.py": "7ba300d0fb5ba680689683aa43dc0eaeed633e10",
    "scripts/test_v47_fresh_agent_dogfood.py": "9d7b0faefe5374fdbfd4064c18924068bd8740c0",
    "scripts/test_v47_semantic_conformance.py": "a0bcbef09acf24c4ebcb65ed0b683970e40c4efb",
    "scripts/v47_conformance.py": "ae917853944bc2370daca876d0ba17f7d1088c9f",
    "standards/BUILD_ARTIFACT_GOVERNANCE_STANDARD.md": "5b74bcbcd475809996c7c6794e5dbdf80895ffd5",
    "standards/CONTEXT_ENGINEERING_STANDARD.md": "f41135fc95b75c1b077cbbd37e9645bd4bc7ff29",
    "standards/DEPLOYMENT_GOVERNANCE_STANDARD.md": "6f4fdfbac6a0a4c5f226ca5da9aeda4a29494fbd",
    "standards/DISTRIBUTION_GOVERNANCE_STANDARD.md": "79a8fc6931bacac99bcef54a02f26af69a6101ca",
    "standards/INCIDENT_RECOVERY_FEEDBACK_STANDARD.md": "c7f1dd6823cd6504321e47308342af3239113ddf",
    "standards/INTENT_ASSUMPTION_GOVERNANCE_STANDARD.md": "dbc2b955c4b707d204cfec7d0124af81582a1f4c",
    "standards/MAINTENANCE_EOL_HOTFIX_STANDARD.md": "9fe8d46bd6bb20b6210d912481b0a54102e61cb7",
    "standards/OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md": "3dddb3b5b81f44491b198a5496ba70f64942a561",
    "standards/PROJECT_ADOPTION.md": "cb1edecc0423a0c34c0b6457cdde18ab36c18bfb",
    "standards/SKILL_PROCEDURE_GOVERNANCE_STANDARD.md": "b4ba0074600dc3a3802663093b663e0f23b57da5",
    "templates/project/.dev-standard/PROJECT_OVERRIDES.md": "0d934401badd1bbdb4f8eb387adbf493a279e8c4",
}

# Shared surfaces composed as unions by the post-recovery recompose (current blobs):
RECOVERED_COMPOSED_SHARED_BLOBS = {
    "CHANGELOG.md": "1c36737f35e7ca2b08f94d79e4ee8873efddea1b",
    "README.md": "d2ee8b0a54cc30357979ad31fe36090b18a154b4",
    "VERSION": "6ed7776bf321979a606a12b2ebfb6a9b6c51ac37",
    "schemas/dispatch.schema.json": "123a66223f6dea42966c4a181dae3cc0776c3ba3",
    "scripts/test_v48_integration_closure.py": "7c4393a4b021b0a65484191532d7e4c53c1378b9",
    "scripts/test_v48_registry_adoption.py": "d947c4e66fea260a1a1ba7b562562e4a4703d1e1",
    "standard-manifest.json": "dc8075c88a155be0e9641ec2aa80bf1c4aff139c",
    "templates/golden/STANDARD_COVERAGE.json": "5149d74063433fba6c867bd4bfed015fe0d321c4",
}

# Late-lane dogfood/conformance kernels and reference surfaces that the
# standard-manifest verification section does not declare (the manifest by
# design inventories active standards/schemas/references/scripts, not
# docs/implementation/** planning records). Pinned EXACTLY so any drift in
# either direction is caught; declarative registration is owned by the
# registry-adoption owner in later maintenance and is NOT repaired in this
# lane (standard-manifest.json is outside the T-015 write set).
UNDECLARED_LATE_LANE_SURFACES = (
    "references/DOWNSSTREAM_DOGFOOD_AUDIT_CONTRACT_V49.md",
    "references/MANUAL_REFERENCE_FLOW_V49.md",
    "scripts/test_v43_conformance_dogfood.py",
    "scripts/test_v48_integration_closure.py",
    "scripts/test_v49_conformance_suite.py",
    "scripts/test_v49_dogfood_audit_contract.py",
    "scripts/test_v49_manual_reference_flow.py",
)

# Shared surfaces composed as unions by the post-recovery recompose
# (c1d7c96/e3a2cc0): their recovery-commit blob deliberately differs from the
# current composed blob; any FURTHER mutation still fails the current-blob pin.
RECOVERED_COMPOSED_SHARED_PATHS = (
    "CHANGELOG.md",
    "README.md",
    "VERSION",
    "schemas/dispatch.schema.json",
    "scripts/test_v48_integration_closure.py",
    "scripts/test_v48_registry_adoption.py",
    "standard-manifest.json",
    "templates/golden/STANDARD_COVERAGE.json",
)

SAFETY_COUNTERS = (
    "UNAUTHORIZED_GATE_OMISSION",
    "STALE_PASS_TRANSFER",
    "INDEPENDENCE_LOSS",
    "CROSS_OWNER_REQUIREMENT_CANCELLATION",
    "ADVERSE_TERMINAL_SUPPRESSION",
)

MECHANISM_VOCAB = {
    "OWNER_PERMITTED_REDUCTION",
    "CROSS_OWNER_FLOOR_COMPOSITION",
    "SAME_CONTAINER_PHASE_COALESCING",
    "GATE_OWNED_EVIDENCE_TRANSFER",
    "FAIL_CLOSED_UNKNOWN_AMBIGUOUS_PREDICATE",
    "NON_DISPATCH_WAIT",
    "PROSPECTIVE_RELEASE_APPLICABILITY_SELECTION",
}

ITEM_STATES = {"EXERCISED", "NOT_EXERCISED", "NOT_RUN", "BLOCKED"}
DOWNSTREAM_ITEM_STATES = {"NOT_EXERCISED", "NOT_RUN", "BLOCKED", "NOT_SATISFIED"}

# Verdict/authority tokens that must never appear in the handoff documents
# (I06): the handoff is inputs only; closure/RQ verdict authority stays with
# the later gates. Chosen as exact substrings that no lawful bounded-input
# phrasing in these documents contains.
FORBIDDEN_DOC_TOKENS = (
    "Version Closure: PASS",
    "Release Qualification: PASS",
    "closure verdict: PASS",
    "RQ verdict: PASS",
    "VERSION_CLOSURE=PASS",
    "RELEASE_QUALIFICATION=PASS",
    "release_qualification_verdict",
    "gate_pass",
    "authorizes_execution: true",
    "authorizes_release_qualification: true",
    "downstream_generality: SATISFIED",
    "downstream_generality=SATISFIED",
    "VALIDATION=PASS",
    "FRESH_REVIEW=PASS",
    "INDEPENDENT_VALIDATION=PASS",
    "LG_SEQ_FULL=PASS",
)


# ---------------------------------------------------------------------------
# fixture / repository helpers
# ---------------------------------------------------------------------------

def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT, check=False, capture_output=True, text=True,
    ).returncode == 0


def git_blob_sha(rev: str, rel_path: str) -> str:
    return git("rev-parse", f"{rev}:{rel_path}")


def github_anchors(text: str) -> set[str]:
    """GitHub-style heading anchors: lowercase, punctuation stripped, spaces -> dashes."""
    anchors = set()
    for line in text.splitlines():
        match = re.match(r"^(#+) (.+)$", line)
        if match is None:
            continue
        segment = match.group(2).strip().lower()
        segment = re.sub(r"[^\w\- ]", "", segment)
        segment = segment.replace(" ", "-")
        anchors.add(segment)
    return anchors


def resolve_owner_ref(ref: str) -> None:
    """Assert an owner ref resolves in-repository (exact path + heading anchor)."""
    path_part, _, frag = ref.partition("#")
    path = ROOT / path_part
    if not path.is_file():
        raise AssertionError(f"owner ref path does not resolve: {ref}")
    if frag and path_part.endswith(".md"):
        anchors = github_anchors(path.read_text(encoding="utf-8"))
        if frag not in anchors:
            raise AssertionError(
                f"owner ref anchor missing in {path_part}: #{frag} "
                f"(available: {sorted(a for a in anchors if a.startswith(frag[:8]))})"
            )
    # other ref kinds (py/json/yml): file existence is the resolution contract.


def resolve_proof_ref(ref: str) -> None:
    """Resolve one evidence proof ref (path[#anchor]); md anchors must resolve."""
    resolve_owner_ref(ref)


def resolve_doc_anchor(doc_text: str, ref: str, doc_name: str) -> None:
    """Resolve an in-document anchor ref (`#heading-anchor`) against its own doc."""
    if not ref.startswith("#"):
        raise AssertionError(f"{doc_name}: reason_ref must be an in-document anchor: {ref}")
    frag = ref[1:]
    if frag not in github_anchors(doc_text):
        raise AssertionError(f"{doc_name}: reason_ref anchor missing: {ref}")


def pinned_battery() -> list[str]:
    """The pinned CI battery: the workflow's `python scripts/...` run lines."""
    text = WORKFLOW.read_text(encoding="utf-8")
    return re.findall(r"^\s*-\s*run:\s*python\s+(\S+)\s*$", text, re.M)


def parse_machine_block(text: str, header: str) -> dict:
    """Parse the deterministic record blocks authored in the two T-015 docs.

    Grammar (strict subset, no ambiguity): the fenced ```text block whose
    first line is `header`; `key: value` scalars at indent 0; `key:` at
    indent 0 opens a list of `  - k: v` items with `    k: v` continuations.
    """
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == "```text" and index + 1 < len(lines) and lines[index + 1].strip() == header:
            start = index + 1
            break
    if start is None:
        raise AssertionError(f"machine block {header} not found")
    data: dict = {}
    current_list: list | None = None
    current_item: dict | None = None
    for line in lines[start + 1:]:
        if line.strip() == "```":
            break
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith("  - "):
            key, _, value = line[4:].strip().partition(":")
            current_item = {key.strip(): value.strip()}
            if current_list is None:
                raise AssertionError(f"machine block {header}: list item before list key")
            current_list.append(current_item)
            continue
        if line.startswith("  ") and current_item is not None:
            key, _, value = line.strip().partition(":")
            current_item[key.strip()] = value.strip()
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "":
            current_list = []
            current_item = None
            data[key] = current_list
        else:
            current_item = None
            current_list = None
            data[key] = value
    return data


def collect_states(block: dict) -> list[tuple[str, str]]:
    """All (owner_key, state) pairs declared in a machine block."""
    states: list[tuple[str, str]] = []
    for key, value in block.items():
        if key == "mechanism_matrix_scope" or not isinstance(value, list):
            continue
        for item in value:
            if isinstance(item, dict) and "state" in item:
                label = item.get("mechanism") or item.get("item") or key
                states.append((str(label), str(item["state"])))
    if "downstream_generality" in block:
        states.append(("downstream_generality", str(block["downstream_generality"])))
    return states


# ---------------------------------------------------------------------------
# kernel tests
# ---------------------------------------------------------------------------

class I01PredecessorLineageIdentity(unittest.TestCase):
    """I01: every merged v4.9 task output + recovered family bound at the exact base."""

    def test_i01_exact_base_and_integrated_lineage_ancestry(self) -> None:
        self.assertEqual(BASE_TREE, git("rev-parse", f"{BASE_SHA}^{{tree}}"))
        for sha in (
            T011_MERGE_SHA, T012_MERGE_SHA, T014_MERGE_SHA,
            RECOVERY_FAMILY_SIDE_SHA, RECOVERY_COMPOSITION_SHA,
            RECOMPOSE_COMPOSITION_SHA, RECOMPOSE_MERGE_SHA,
            T013_REBIND_SHA, BASE_SHA, PACK_HEAD_SHA,
        ):
            self.assertTrue(is_ancestor(sha), f"lineage commit not an ancestor of HEAD: {sha}")
        # The T-015 execution pack is the direct predecessor of the candidate work.
        self.assertEqual(PACK_HEAD_SHA, git("rev-parse", "HEAD^"))
        # The exact-base postulate binds the frozen DAG v0.1 section for T-015.
        self.assertEqual(DAG_V01_BLOB, git_blob_sha("HEAD", DAG_V01.relative_to(ROOT).as_posix()))

    def test_i01_frozen_authority_blobs_resolve_unchanged(self) -> None:
        self.assertEqual(FROZEN_PRD_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/PRD.md"))
        self.assertEqual(FROZEN_L2_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md"))
        self.assertEqual(FROZEN_DAG_V02_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/TASK_DAG.md"))
        dag_text = DAG_V01.read_text(encoding="utf-8")
        section = dag_text.split("### T-015", 1)[1].split("\n### ", 1)[0] if "### T-015" in dag_text else ""
        self.assertIn("Integrated v4.9 Dogfood / Release Evidence Handoff", section)
        self.assertIn("no unsupported generality claim", section)
        self.assertIn("NOT_SATISFIED", section)
        self.assertIn("safety negatives remain zero", section)
        self.assertIn("stale predecessor/evidence binding is laundered", section)
        self.assertIn("without converting NOT_RUN/BLOCKED into PASS", section)

    def test_i01_v49_task_outputs_exact_blobs(self) -> None:
        merged_tasks = [t for t in V49_TASK_OUTPUT_BLOBS if t != "T-015"]
        self.assertEqual(
            ["T-002", "T-003", "T-004", "T-005", "T-006", "T-007", "T-008",
             "T-009", "T-010", "T-011", "T-012", "T-013", "T-014"],
            sorted(merged_tasks),
        )
        total = 0
        for task, pins in V49_TASK_OUTPUT_BLOBS.items():
            for rel_path, blob in pins.items():
                with self.subTest(task=task, path=rel_path):
                    self.assertNotIn(rel_path, WRITE_SET)
                    self.assertEqual(blob, git_blob_sha("HEAD", rel_path))
                total += 1
        self.assertGreaterEqual(total, 90)

    def test_i01_recovered_families_byte_identical_since_recovery(self) -> None:
        # Pure recovered surfaces: byte-identical from the recovery composition
        # (4c632256) through the candidate — no laundering since recovery.
        for rel_path, blob in RECOVERED_FAMILY_BLOBS.items():
            with self.subTest(recovered=rel_path):
                self.assertEqual(blob, git_blob_sha("HEAD", rel_path))
                self.assertEqual(blob, git_blob_sha(RECOVERY_COMPOSITION_SHA, rel_path))
        # Shared surfaces recomposed as unions: pinned to the exact current
        # composed blob; the recovery-commit blob deliberately differs.
        for rel_path in RECOVERED_COMPOSED_SHARED_PATHS:
            with self.subTest(composed_union=rel_path):
                current = git_blob_sha("HEAD", rel_path)
                self.assertEqual(RECOVERED_COMPOSED_SHARED_BLOBS[rel_path], current)
                self.assertNotEqual(current, git_blob_sha(RECOVERY_COMPOSITION_SHA, rel_path))

    def test_i01_t015_planning_files_immutable_since_pack_head(self) -> None:
        for rel_path in PLANNING_PATHS:
            with self.subTest(planning_path=rel_path):
                self.assertEqual(git_blob_sha(PACK_HEAD_SHA, rel_path), git_blob_sha("HEAD", rel_path))

    def test_i01_working_tree_stays_in_write_set(self) -> None:
        changed = set()
        for line in git("status", "--porcelain", "-uall").splitlines():
            if not line.strip():
                continue
            changed.add(line[2:].strip().strip('"'))
        for path in changed:
            with self.subTest(changed_path=path):
                self.assertTrue(
                    any(path == w or path.startswith(w) for w in WRITE_SET),
                    f"path outside Builder write set: {path}",
                )


class I02OrchestrationJourneys(unittest.TestCase):
    """I02: representative positive/negative journeys from the T-007 kernel + T-012 surfaces."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.facts_current = core_kernel.load_fixture("facts_current.json")
        cls.facts_drift = core_kernel.load_fixture("facts_plan_drift.json")
        cls.facts_stale = core_kernel.load_fixture("facts_lineage_stale.json")
        cls.facts_successor = core_kernel.load_fixture("facts_successor.json")
        cls.candidates = core_kernel.load_fixture("candidates.json")["candidates"]
        cls.races = core_kernel.load_fixture("claim_races.json")
        cls.phase_table = core_kernel.load_fixture("phase_table.json")

    # ---------- positive journey: legal dispatch -> claim -> merge (§28.1/§11) ----------

    def test_i02_positive_journey_dispatch_claim_merge_ready(self) -> None:
        facts = copy.deepcopy(self.facts_current)
        facts["composite_admission"] = {"mode": "SINGLE_WRITER_ADMISSION", "state": "AVAILABLE"}
        materialized = core_kernel.dispatch_materialize(facts)
        self.assertEqual("MATERIALIZED", materialized["outcome"])
        self.assertEqual(1, materialized["dispatches_created"])
        state = core_kernel.ClaimState()
        outcome, state = core_kernel.claim_attempt(state, facts, "op-1", 0)
        self.assertEqual("ACCEPTED", outcome)
        ready, reason = core_kernel.merge_ready(facts, state, "op-1")
        self.assertTrue(ready)
        self.assertEqual("MERGE_READY", reason)
        # In-envelope JIT phase is READY (E2 pack declaration, all floors hold).
        proof = next(p for p in self.phase_table["envelope_proofs"] if p["proof_id"] == "IN_PACK")
        phase = {"dependency_state": "DONE", "envelope_proof": proof}
        self.assertEqual("READY", core_kernel.jit_verdict(phase, facts))

    # ---------- negative journeys (Frozen PRD acceptance scenarios) ----------

    def test_i02_negative_duplicate_claim_race_fails_closed(self) -> None:
        # PRD F -> K07/K09: at most one canonical claim; never both, never lost.
        protected_key = tuple(self.races["protected_claim_key"])
        for ordering in self.races["orderings"]:
            with self.subTest(ordering=ordering["ordering_id"]):
                first, final = core_kernel.run_race(ordering, protected_key)
                second, _ = core_kernel.run_race(ordering, protected_key)
                self.assertEqual(first, second)  # deterministic replay
                accepted = [op for op, outcome in first if outcome == "ACCEPTED"]
                self.assertEqual(ordering["expected"]["accepted"], accepted)
                self.assertLessEqual(len(final.accepted), 1)

    def test_i02_negative_wrong_role_independence_rejected_before_ranking(self) -> None:
        # PRD G -> K04/K09: hard predicates/profile blocks rank before any ranking input.
        self.assertEqual(["c-eligible-low-rank"], core_kernel.rank_eligible(self.candidates))
        self.assertEqual("INELIGIBLE", core_kernel.resolve_eligibility(self.candidates[2]))
        reordered = [dict(c, rank=0) for c in self.candidates]
        self.assertEqual(["c-eligible-low-rank"], core_kernel.rank_eligible(reordered))

    def test_i02_negative_known_sequence_block_waits_without_dispatch(self) -> None:
        # PRD K -> K03/K09: WAITING_LINEAGE stays a derived non-dispatch projection.
        projection = core_kernel.reduce(self.facts_stale)
        waiting = projection["waiting_lineage"]
        self.assertIsNotNone(waiting)
        self.assertFalse(waiting["dispatchable"])
        self.assertFalse(waiting["claimable"])
        self.assertIsNone(waiting["workflow_state"])
        self.assertIsNone(waiting["gate_verdict"])
        materialized = core_kernel.dispatch_materialize(self.facts_stale)
        self.assertEqual("WAITING_LINEAGE_NO_DISPATCH", materialized["outcome"])
        self.assertEqual(0, materialized["dispatches_created"])
        outcome, untouched = core_kernel.claim_attempt(core_kernel.ClaimState(), self.facts_stale, "op-1", 0)
        self.assertEqual("NOT_DISPATCHABLE_WAITING_LINEAGE", outcome)
        self.assertEqual(core_kernel.ClaimState(), untouched)

    def test_i02_negative_out_of_envelope_and_topology_routes_blocked(self) -> None:
        # PRD L -> K02/K09: undeclared/violated JIT phases BLOCK; topology mutates via governance.
        undeclared = next(p for p in self.phase_table["envelope_proofs"] if p["proof_id"] == "UNDECLARED")
        violated = next(p for p in self.phase_table["envelope_proofs"] if p["proof_id"] == "VIOLATED")
        facts = copy.deepcopy(self.facts_current)
        self.assertEqual("BLOCKED", core_kernel.jit_verdict({"dependency_state": "DONE", "envelope_proof": undeclared}, facts))
        self.assertEqual("BLOCKED", core_kernel.jit_verdict({"dependency_state": "DONE", "envelope_proof": violated}, facts))
        self.assertEqual("V43_MUTATION_ADD", core_kernel.classify_topology_change({"action": "new_task"}))
        self.assertEqual(
            "V43_MUTATION_ADD_DEPENDENCY",
            core_kernel.classify_topology_change({"action": "add_dependency"}),
        )

    def test_i02_negative_ambiguous_reduction_predicate_fails_closed(self) -> None:
        # PRD M -> K01/K09: model judgment never authorizes an unproven reduction.
        self.assertEqual(
            "STRONGER_EXISTING_PATH_OR_BLOCKED",
            core_kernel.reduction_decision("UNPROVEN", "model: reduce, it looks safe"),
        )
        self.assertEqual(
            "REDUCED_PER_OWNER_RULE",
            core_kernel.reduction_decision("PROVEN_TRUE", "n/a"),
        )
        self.assertEqual("UNKNOWN", core_kernel.resolve_eligibility(self.candidates[3]))

    def test_i02_negative_adverse_finding_cannot_be_shopped(self) -> None:
        # PRD N -> K05/K09: unresolved blocker stands; re-review only via authorized paths.
        shopping = copy.deepcopy(self.facts_drift)
        shopping["verdict_chronology"].append(
            {"reviewer": "R2", "subject_ref": "issue:900", "verdict": "PASS", "evidence_ref": "review-evidence:R2-S1"}
        )
        self.assertEqual(["F-101"], core_kernel.apply_chronology(shopping["unresolved_findings"], shopping["verdict_chronology"]))
        self.assertEqual(
            "REJECTED_REVIEW_SHOPPING",
            core_kernel.route_re_review({"request": "same-subject redispatch to a new reviewer for PASS"}),
        )
        state = core_kernel.ClaimState()
        outcome, state = core_kernel.claim_attempt(state, self.facts_successor, "op-1", 0)
        self.assertEqual("ACCEPTED", outcome)
        ready, reason = core_kernel.merge_ready(self.facts_successor, state, "op-1")
        self.assertFalse(ready)
        self.assertEqual("UNRESOLVED_BLOCKING_FINDINGS", reason)

    def test_i02_negative_stale_pass_never_transfers(self) -> None:
        # PRD I -> K10: stale PASS -> successor PASS without an owner transfer rule rejects.
        self.assertEqual(
            "REJECTED_HISTORICAL_ONLY_NO_TRANSFER_RULE",
            core_kernel.transfer_pass({"subject_ref": "issue:900", "current": False}, "issue:900@S2"),
        )
        # Stale plan binding is rejected at Dispatch, Claim and merge (K01/K10).
        drifted = core_kernel.dispatch_materialize(self.facts_drift)
        self.assertEqual("BLOCKED_PLAN_BINDING_STALE", drifted["outcome"])
        self.assertEqual(0, drifted["dispatches_created"])
        outcome, state = core_kernel.claim_attempt(core_kernel.ClaimState(), self.facts_drift, "op-1", 0)
        self.assertEqual("STALE_PLAN_BINDING_RECOMPUTE", outcome)
        outcome, state = core_kernel.claim_attempt(state, self.facts_current, "op-1", 0)
        self.assertEqual("ACCEPTED", outcome)
        ready, reason = core_kernel.merge_ready(self.facts_drift, state, "op-1")
        self.assertFalse(ready)
        self.assertEqual("PLAN_BINDING_STALE", reason)

    # ---------- T-012 conformance surface executed green in this run ----------

    def test_i02_t012_conformance_surface_c01_c12_executed_green(self) -> None:
        suite = unittest.defaultTestLoader.loadTestsFromModule(conf_surface)
        result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
        self.assertTrue(result.wasSuccessful())
        self.assertGreaterEqual(result.testsRun, 12)
        class_prefixes = {
            name[:3] for name in dir(conf_surface)
            if re.fullmatch(r"C\d{2}\w*", name)
        }
        self.assertEqual({f"C{i:02d}" for i in range(1, 13)}, class_prefixes)
        manifest_json = json.dumps(
            json.loads((ROOT / "fixtures" / "conformance-suite" / "coverage_manifest.json").read_text(encoding="utf-8"))
        )
        for i in range(1, 13):
            self.assertIn(f"C{i:02d}", manifest_json)

    # ---------- extended integrated regression at the candidate ----------

    def test_i02_extended_integrated_regression_recovered_and_lane_kernels_green(self) -> None:
        # The recovered v4.4-v4.7 family kernels plus the v4.8/T-013/T-014 lane
        # kernels re-executed at the integrated candidate (in-repo only; this is
        # compatibility/integration evidence, never downstream generality).
        extended = sorted(
            p for pattern in (
                "scripts/test_v44_*.py", "scripts/test_v45_*.py", "scripts/test_v46_*.py",
                "scripts/test_v47_*.py", "scripts/test_v48_*.py",
                "scripts/test_v49_manual_reference_flow.py", "scripts/test_v49_dogfood_audit_contract.py",
            )
            for p in git("ls-files", pattern).splitlines() if p.strip()
        )
        self.assertGreaterEqual(len(extended), 50)
        failures = []
        for rel_path in extended:
            run = subprocess.run(
                [sys.executable, "-B", rel_path], cwd=ROOT, check=False, capture_output=True, text=True
            )
            if run.returncode != 0:
                failures.append((rel_path, run.stdout[-400:], run.stderr[-400:]))
        self.assertEqual([], failures)


class I03Reconciliation(unittest.TestCase):
    """I03: normative docs/contracts/tests/registry reconciliation at the candidate."""

    def test_i03_pinned_battery_definition_complete(self) -> None:
        battery = pinned_battery()
        self.assertEqual(37, len(battery))
        for rel_path in battery:
            with self.subTest(battery=rel_path):
                self.assertTrue((ROOT / rel_path).is_file())

    def test_i03_manifest_declares_integrated_surfaces(self) -> None:
        manifest = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
        declared = {p for values in manifest["sections"].values() for p in values}
        for surface in (
            "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
            "standards/ASSURANCE_PLAN_STANDARD.md",
            "standards/RELEASE_STANDARD.md",
            "standards/TASK_DAG_GOVERNANCE_STANDARD.md",
            "registries/state-dimensions-v1.json",
            "schemas/assurance-plan-v2.schema.json",
            "schemas/role-execution-profile-v1.schema.json",
            "schemas/task-learning-v2.schema.json",
            "schemas/dispatch.schema.json",
        ):
            with self.subTest(declared=surface):
                self.assertIn(surface, declared)
        # Late-lane dogfood/conformance kernels are executed by the pinned
        # battery / required_builder_checks but are NOT manifest-declared; the
        # gap is pinned exactly (see UNDECLARED_LATE_LANE_SURFACES) and routed
        # to the registry-adoption owner — never silently "fixed" in this lane.
        undeclared = sorted(
            s for s in UNDECLARED_LATE_LANE_SURFACES
            if not s.startswith("references/") and not s.startswith("docs/")
        )
        self.assertEqual(undeclared, sorted(set(undeclared) - declared))
        for rel_path in battery_paths_in(declared):
            self.assertTrue((ROOT / rel_path).is_file())

    def test_i03_registry_owner_bindings_and_forbidden_inferences(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        dims = {d["dimension_id"]: d for d in registry["dimensions"]}
        self.assertIn("waiting_lineage", dims)
        self.assertEqual("standards/EXECUTION_ARCHITECTURE_STANDARD.md", dims["waiting_lineage"]["canonical_owner_ref"])
        self.assertEqual("OWNER_DEFINED", dims["waiting_lineage"]["vocabulary_posture"])
        rule_ids = {r["rule_id"] for r in registry["forbidden_inferences"]}
        for rule in (
            "F11_TASK_DONE_NOT_LINEAGE_CURRENT",
            "F13_ASSURANCE_CURRENT_NOT_VALIDATION_PASS",
            "F14_ASSURANCE_CURRENT_NOT_REVIEW_PASS",
            "F15_ASSURANCE_CURRENT_NOT_RELEASE_READY",
            "F16_ASSURANCE_CURRENT_NOT_TASK_READY",
            "F17_WAITING_LINEAGE_NOT_WORKFLOW_BLOCKED",
            "F18_WAITING_LINEAGE_NOT_GATE_PASS",
            "F19_WAITING_LINEAGE_NOT_GATE_FAIL",
        ):
            self.assertIn(rule, rule_ids)

    def test_i03_contract_and_gate_owner_refs_resolve(self) -> None:
        # T-014 downstream contract consumed authorities (exact refs).
        t014_refs = json.loads(
            (ROOT / "fixtures" / "dogfood-audit-contract" / "owner_surfaces.json").read_text(encoding="utf-8")
        )["consumed_authority_refs"]
        for ref in t014_refs:
            with self.subTest(t014_owner=ref):
                resolve_owner_ref(ref)
        # T-010 gate matrix row M10 binding refs.
        for ref in (
            "docs/implementation/4.9.0/PRD.md#163-exact-candidate-binding",
            "docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md#14-downstream-dogfood-evidence-architecture",
        ):
            with self.subTest(m10=ref):
                resolve_owner_ref(ref)
        # T-007 consumed contracts resolve (owner fixture).
        core_refs = core_kernel.load_fixture("owner_refs.json")
        standard_text = (ROOT / "standards" / "EXECUTION_ARCHITECTURE_STANDARD.md").read_text(encoding="utf-8")
        anchors = github_anchors(standard_text)
        for anchor in core_refs["standard_sections"].values():
            self.assertIn(anchor.rsplit("#", 1)[1], anchors)

    def test_i03_task_packs_and_dag_agree(self) -> None:
        packs = sorted(p.name for p in (ROOT / "docs" / "implementation" / "4.9.0" / "task-packs").glob("T*.md"))
        self.assertEqual(15, len(packs))
        dag = (ROOT / "docs" / "implementation" / "4.9.0" / "TASK_DAG.md").read_text(encoding="utf-8")
        self.assertIn("T-015: deps=[T-011, T-012, T-013, T-014]", dag)
        materialization = (ROOT / "docs" / "implementation" / "4.9.0" / "TASK_MATERIALIZATION_STATUS.md").read_text(encoding="utf-8")
        for task_id in (f"T-{i:03d}" for i in range(1, 16)):
            self.assertIn(f"| {task_id} |", materialization)

    def test_i03_golden_coverage_parses_and_lists_standards(self) -> None:
        coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
        standards = {row["standard"] for row in coverage["coverage"]}
        for surface in (
            "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
            "standards/ASSURANCE_PLAN_STANDARD.md",
            "standards/RELEASE_STANDARD.md",
        ):
            self.assertIn(surface, standards)


def battery_paths_in(declared: set[str]) -> list[str]:
    return [p for p in pinned_battery() if p in declared]


class I04HandoffCompleteness(unittest.TestCase):
    """I04: no NOT_RUN/BLOCKED converted; no unsupported generality; NOT_SATISFIED posture."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.report_text = REPORT.read_text(encoding="utf-8")
        cls.handoff_text = HANDOFF.read_text(encoding="utf-8")
        cls.report = parse_machine_block(cls.report_text, "INTEGRATED_DOGFOOD_RECORD_V1")
        cls.handoff = parse_machine_block(cls.handoff_text, "RELEASE_EVIDENCE_HANDOFF_V1")

    def test_i04_records_bound_to_exact_candidate(self) -> None:
        for block, header in ((self.report, "report"), (self.handoff, "handoff")):
            candidate = block["bound_ads_candidate"]
            self.assertTrue(CANDIDATE_RE.match(candidate), header)
            self.assertEqual(CANDIDATE, candidate)
        self.assertEqual(BASE_TREE, self.report["base_tree"])
        self.assertEqual(PACK_HEAD_SHA, self.report["execution_pack_head"])

    def test_i04_downstream_exercises_stay_not_run_or_blocked(self) -> None:
        for key in (
            "qualifying_downstream_dogfood",
            "ambiguous_predicate_exercise_downstream",
            "independent_safety_audit",
            "manual_github_native_viability",
        ):
            rows = self.report[key]
            with self.subTest(downstream_item=key):
                self.assertEqual(1, len(rows))
                self.assertIn(rows[0]["state"], DOWNSTREAM_ITEM_STATES)
        for row in self.report["qualifying_downstream_dogfood"]:
            resolve_doc_anchor(self.report_text, row["reason_ref"], "report")
        for row in self.report["ambiguous_predicate_exercise_downstream"]:
            resolve_doc_anchor(self.report_text, row["reason_ref"], "report")
        for row in self.report["independent_safety_audit"]:
            resolve_doc_anchor(self.report_text, row["reason_ref"], "report")
        for row in self.report["manual_github_native_viability"]:
            self.assertTrue(str(row.get("claim_boundary") or "").strip())
        # The handoff preserves the same postures — never upgrades them.
        preserved = {row["item"]: row["state"] for row in self.handoff["closure_inputs_preserved"]}
        expected = {
            "downstream_generality": "NOT_SATISFIED",
            "qualifying_downstream_dogfood": "NOT_RUN",
            "ambiguous_predicate_exercise_downstream": "NOT_RUN",
            "independent_safety_audit": "NOT_RUN",
            "manual_github_native_viability": "NOT_EXERCISED",
        }
        for item, state in expected.items():
            self.assertEqual(state, preserved[item], item)

    def test_i04_mechanism_matrix_rows_are_bounded(self) -> None:
        matrix = self.report["inrepo_kernel_conformance_mechanism_matrix"]
        mechanisms = {row["mechanism"] for row in matrix}
        self.assertEqual(MECHANISM_VOCAB, mechanisms)
        for row in matrix:
            with self.subTest(mechanism=row["mechanism"]):
                self.assertIn(row["state"], ITEM_STATES)
                refs = [r.strip() for r in str(row.get("proof_refs") or "").split(",") if r.strip()]
                if row["state"] == "EXERCISED":
                    self.assertTrue(refs, f"EXERCISED without proof: {row['mechanism']}")
                    for ref in refs:
                        resolve_proof_ref(ref)
                if row["state"] == "NOT_EXERCISED":
                    self.assertTrue(str(row.get("claim_boundary") or "").strip())
                if row["state"] in ("NOT_RUN", "BLOCKED"):
                    self.assertTrue(str(row.get("reason_ref") or "").strip())

    def test_i04_downstream_generality_stays_not_satisfied(self) -> None:
        self.assertEqual("NOT_SATISFIED", self.report["downstream_generality"])
        self.assertEqual("QUALIFYING_DOWNSTREAM_RUN_NOT_RUN", self.report["generality_reason"])
        self.assertEqual("IN_REPO_KERNEL_AND_CONFORMANCE_SURFACES_ONLY", self.report["matrix_scope"])
        # No state anywhere in either block was upgraded to a PASS-like token.
        for block in (self.report, self.handoff):
            for label, state in collect_states(block):
                with self.subTest(state_owner=label):
                    self.assertNotIn(state, {"PASS", "READY", "SATISFIED", "EXERCISED_DOWNSTREAM"})


class I05SafetyNegativesAndStaleBindings(unittest.TestCase):
    """I05: safety negatives zero for the in-repo journeys; no stale binding laundered."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.report = parse_machine_block(REPORT.read_text(encoding="utf-8"), "INTEGRATED_DOGFOOD_RECORD_V1")
        cls.core = core_kernel

    def _journey_outcome(self, negative: str) -> str:
        facts_current = core_kernel.load_fixture("facts_current.json")
        facts_drift = core_kernel.load_fixture("facts_plan_drift.json")
        facts_successor = core_kernel.load_fixture("facts_successor.json")
        candidates = core_kernel.load_fixture("candidates.json")["candidates"]
        if negative == "UNAUTHORIZED_GATE_OMISSION":
            undeclared = {"dependency_state": "DONE", "envelope_proof": {"proof_id": "UNDECLARED", "declared_in": None, "envelope_conditions": None}}
            return core_kernel.jit_verdict(undeclared, facts_current)
        if negative == "STALE_PASS_TRANSFER":
            return core_kernel.transfer_pass({"subject_ref": "issue:900", "current": False}, "issue:900@S2")
        if negative == "INDEPENDENCE_LOSS":
            return core_kernel.resolve_eligibility(candidates[2])
        if negative == "CROSS_OWNER_REQUIREMENT_CANCELLATION":
            return core_kernel.reduction_decision("UNPROVEN", "model judgment")
        if negative == "ADVERSE_TERMINAL_SUPPRESSION":
            outcome, _state = core_kernel.claim_attempt(core_kernel.ClaimState(), facts_successor, "op-1", 0)
            ready, reason = core_kernel.merge_ready(facts_successor, core_kernel.ClaimState(accepted=("op-1",)), "op-1")
            del outcome
            self.assertFalse(ready)
            return reason
        raise AssertionError(f"unknown negative: {negative}")

    EXPECTED_NEGATIVE_GUARDS = {
        "UNAUTHORIZED_GATE_OMISSION": "BLOCKED",
        "STALE_PASS_TRANSFER": "REJECTED_HISTORICAL_ONLY_NO_TRANSFER_RULE",
        "INDEPENDENCE_LOSS": "INELIGIBLE",
        "CROSS_OWNER_REQUIREMENT_CANCELLATION": "STRONGER_EXISTING_PATH_OR_BLOCKED",
        "ADVERSE_TERMINAL_SUPPRESSION": "UNRESOLVED_BLOCKING_FINDINGS",
    }

    def test_i05_every_negative_guard_holds_in_this_run(self) -> None:
        for negative, expected in self.EXPECTED_NEGATIVE_GUARDS.items():
            with self.subTest(negative=negative):
                self.assertEqual(expected, self._journey_outcome(negative))

    def test_i05_recorded_inrepo_negatives_are_zero_and_scoped(self) -> None:
        rows = {
            key: value
            for row in self.report["inrepo_journey_safety_negatives"]
            for key, value in row.items()
        }
        for counter in SAFETY_COUNTERS:
            with self.subTest(counter=counter):
                self.assertIn(counter, rows)
                self.assertEqual("0", str(rows[counter]))
        self.assertEqual(
            "IN_REPO_DETERMINISTIC_JOURNEYS_ONLY_NOT_A_DOWNSTREAM_AUDIT",
            self.report["negative_scope"],
        )

    def test_i05_no_stale_binding_laundered(self) -> None:
        # The lineage posture is THIS lane's own recompute, never an inherited verdict.
        self.assertEqual("SELF_RECOMPUTED_AT_CANDIDATE", self.report["lineage_recompute"])
        # Candidate binding is the exact admitted base — not any earlier tip.
        self.assertEqual(CANDIDATE, self.report["bound_ads_candidate"])
        # Predecessor outputs are blob-identical right now (I01 pins re-asserted
        # cheaply for the frozen authority trio; the full pin map runs in I01).
        self.assertEqual(FROZEN_PRD_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/PRD.md"))
        self.assertEqual(FROZEN_L2_BLOB, git_blob_sha("HEAD", "docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md"))
        # No predecessor gate/verdict is restated as this lane's own result.
        for doc in (REPORT.read_text(encoding="utf-8"), HANDOFF.read_text(encoding="utf-8")):
            for token in ("VALIDATION=PASS", "FRESH_REVIEW=PASS", "INDEPENDENT_VALIDATION=PASS"):
                self.assertNotIn(token, doc)


class I06EvidenceOnlyPosture(unittest.TestCase):
    """I06: the handoff contains no closure/RQ verdict — inputs only."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.report_text = REPORT.read_text(encoding="utf-8")
        cls.handoff_text = HANDOFF.read_text(encoding="utf-8")
        cls.handoff = parse_machine_block(cls.handoff_text, "RELEASE_EVIDENCE_HANDOFF_V1")

    def test_i06_no_verdict_or_self_authorizing_tokens(self) -> None:
        for doc_name, text in (("report", self.report_text), ("handoff", self.handoff_text)):
            for token in FORBIDDEN_DOC_TOKENS:
                with self.subTest(doc=doc_name, token=token):
                    self.assertNotIn(token, text)

    def test_i06_authority_explicitly_remains_with_later_gates(self) -> None:
        self.assertEqual("LATER_GATES_ONLY", self.handoff["verdict_authority_version_closure"])
        self.assertEqual("RELEASE_OWNER_ONLY", self.handoff["verdict_authority_release_qualification"])
        self.assertEqual("NONE", self.handoff["closure_rq_verdict_issued_by_this_handoff"])
        self.assertEqual("false", self.handoff["authorizes_execution"])
        self.assertEqual("false", self.handoff["authorizes_release_qualification"])
        self.assertEqual("false", parse_machine_block(self.report_text, "INTEGRATED_DOGFOOD_RECORD_V1")["authorizes_execution"])
        self.assertEqual(
            "false",
            parse_machine_block(self.report_text, "INTEGRATED_DOGFOOD_RECORD_V1")["authorizes_release_qualification"],
        )

    def test_i06_handoff_inputs_reference_the_report(self) -> None:
        self.assertEqual("V49-T015-INTEGRATED-DOGFOOD-001", self.handoff["report_record"])
        consumables = {row["item"] for row in self.handoff["consumable_by_version_closure"]}
        self.assertIn("predecessor_lineage_exact_identity", consumables)
        for row in self.handoff["consumable_by_version_closure"]:
            resolve_proof_ref(row["proof_ref"])


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
