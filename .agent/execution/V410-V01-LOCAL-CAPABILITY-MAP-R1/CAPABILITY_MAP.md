# V410-V01 Local Capability Map (R1)

Preparation unit: `V410-V01-LOCAL-CAPABILITY-MAP-R1` — parent Issue `#865`.
Exact base: `30334e8c7b90a327f8597b86c88c785b98df07f7` (= `origin/version/v4.10.0` tip).
Source of subjects: `docs/implementation/4.10.0/V410_V01_VALIDATION_CONTRACT.md` @ this base.

## Status disclaimer (must re-read before use)

**`CANDIDATE_NOT_READY`**. This map was prepared against the current base, NOT against
V410-V01's real validation subject. The real subject is the dependency-complete candidate
after `V410-T08A` integration, which does not exist yet (`V410-T04B/T05B/T06A-T08A`
pending). At real V01 dispatch the Validator MUST re-read every input listed in the last
column at the exact candidate, and MUST NOT treat any AVAILABILITY recorded here as a
Validation PASS. Where a subject needs real-host/GitHub-native facts, the host part is
`BLOCKED` here with owner = GitHub platform; per the Validation contract, PASS is never
inferred from source inspection.

## Human-readable map

Availability legend: `AVAILABLE` = fully executable locally at base_sha; `AVAILABLE (local) / BLOCKED (host)` = local doc/script checks run, host-native fact check BLOCKED (owner: GitHub platform).

| # | Validation subject (contract) | Local executable capability (exact commands) | Availability at base_sha | Limitation / owner if BLOCKED | Validator must re-read at real dispatch |
|---|---|---|---|---|---|
| 1 | Idea/Intent → Intake → L1 → Research → Draft PRD → Product Review → Product Freeze ordering/proportionality | `python scripts/test_v410_stage1_lifecycle_contracts.py`; `grep -n "Product Freeze" standards/DEVELOPMENT_WORKFLOW.md`; existence read of `docs/implementation/4.10.0/PRD.md`, `docs/implementation/4.10.0/L1_PRODUCT_EVIDENCE.md`, `docs/implementation/4.10.0/PRODUCT_FREEZE.md` | AVAILABLE | none | DEVELOPMENT_WORKFLOW.md + Stage-1 script + freeze doc at exact candidate; check ordering claims against actual dispatch history |
| 2 | Frozen Product/L2/refined DAG authority hierarchy and contradiction routing | `python scripts/test_v410_t01b_product_projections.py`; `grep -n FROZEN_PRD_BLOB docs/implementation/4.10.0/REFINED_TASK_DAG_FREEZE_R1.md`; `grep -n contradiction docs/implementation/4.10.0/L2_ARCHITECTURE_EVIDENCE.md` | AVAILABLE | none | PRODUCT_FREEZE.md, L2_FREEZE.md, REFINED_TASK_DAG_FREEZE_R1.md frozen blobs; contradiction routing owner at candidate |
| 3 | Task Pack completeness without exact-base HOW leakage | `grep -n V410-T08A docs/implementation/4.10.0/TASK_PACKS_R1.md`; `grep -ni "base_sha\|exact base" docs/implementation/4.10.0/TASK_PACKS_R1.md` (expect no exact-base HOW; hit set is a fact for the Validator, not a PASS) | AVAILABLE | none | TASK_PACKS_R1.md at candidate; compare pack set vs frozen node set |
| 4 | Canonical live Task DAG == Frozen refined edge set via GitHub native Issue Dependencies | local: parse `docs/implementation/4.10.0/REFINED_TASK_DAG_FREEZE_R1.md` frozen edge block (`grep -n "V410-T08A ->" docs/implementation/4.10.0/REFINED_TASK_DAG_FREEZE_R1.md`); host: `gh issue view <issue> --json dependencies` for every frozen node | AVAILABLE (local) / BLOCKED (host) | host part: GitHub platform — native Issue Dependencies state must be read live at real dispatch | frozen edge block + live GitHub dependency graph at candidate; never infer PASS from the frozen doc alone |
| 5 | No premature task branch or Execution Pack before real dependency/currentness admission | local: `git for-each-ref refs/heads/task/v4.10.0` vs frozen DAG; host: `gh pr list --base version/v4.10.0 --state all` | AVAILABLE (local) / BLOCKED (host) | host part: GitHub platform — live remote branch/PR existence and timing | remote refs and PR creation/merge timestamps vs dependency completion at candidate |
| 6 | JIT Execution Pack binding/claim/currentness behavior on exercised Tasks | `grep -n base_sha .agent/execution/V410-T05A-R3/MANIFEST.yaml`; `grep -n CURRENTNESS .agent/execution/V410-T05A-R3/FAILURE_MATRIX.yaml`; `grep -n claim standards/EXECUTION_PACK_STANDARD.md` | AVAILABLE | none | all `.agent/execution/V410-*` packs at candidate; claim-before-mutation ordering evidence per exercised Task |
| 7 | Issue-first pointer-only triggers reconstruct complete durable contracts | `python scripts/test_pointer_only_trigger_contract.py`; `grep -n pointer-only standards/ISSUE_FIRST_TASK_TRIGGER.md` | AVAILABLE | none | ISSUE_FIRST_TASK_TRIGGER.md + trigger contract script at candidate |
| 8 | Human controllability/auditability with minimal routine relay burden | `python scripts/test_v410_t02a_collaboration_control.py`; `grep -n human standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`; `grep -n "Human Decision Queue" standards/CHATGPT_WEB_ROLE.md` | AVAILABLE | none | GITHUB_AGENT_INTERACTION_PROTOCOL.md, CHATGPT_WEB_ROLE.md at candidate |
| 9 | Automation/evidence-first quality and independent Review separation | `python scripts/test_v410_t03a_implementation_quality.py`; `python scripts/verify_standard.py`; `grep -n independent standards/VALIDATION_STANDARD.md` | AVAILABLE | none | IMPLEMENTATION_QUALITY_STANDARD.md, VALIDATION_STANDARD.md, verify_standard.py at candidate |
| 10 | Product §19 acceptance/release-blocker evidence mapping through existing owners | `grep -n "19.3" docs/implementation/4.10.0/PRD.md`; `python scripts/test_v410_t04a_gate_repair_routing.py` | AVAILABLE | none | PRD §19 at candidate; blocker→owner mapping evidence; real gate outcomes are host facts |
| 11 | Historical exact-subject Review/Validation evidence does not silently transfer after candidate drift | `grep -n superseded .agent/execution/V410-T05A-R3/TEST_MATRIX.yaml`; `grep -n generated_at .agent/execution/V410-T05A-R3/MANIFEST.yaml` (exact-pack identity/recency facts) | AVAILABLE | none | every relied-upon evidence pack's base_sha vs candidate identity at dispatch |
| 12 | `ADS_CORE_FEATURE_FREEZE_ELIGIBLE` remains Product authority, not manufactured by CI/Review/Release | `grep -n ADS_CORE_FEATURE_FREEZE_ELIGIBLE docs/implementation/4.10.0/PRODUCT_FREEZE.md` | AVAILABLE | none | PRODUCT_FREEZE.md + release-blocker evidence; the actual YES/NO decision is a Product-authority fact, never source-inferred |
| 13 | Task/PR PASS does not imply Version Closure/Hidden/Release Qualification PASS | local: `grep -n Qualification standards/RELEASE_STANDARD.md`; `grep -n independent standards/VALIDATION_STANDARD.md`; host: `gh pr checks <pr>` / `gh api` for live CI/gate state | AVAILABLE (local) / BLOCKED (host) | host part: GitHub platform — live PR check suites, Hidden/RQ verdicts are platform facts | RELEASE_STANDARD.md, VALIDATION_STANDARD.md + live gate records at candidate |
| 14 | R5/R8/R9/R10 remain subordinate; no new component registry/learning DB/telemetry authority/research lifecycle | `grep -n R5=EXISTING_OWNER_ONLY docs/implementation/4.10.0/PRODUCT_FREEZE.md`; `python scripts/test_v410_t05a_shared_code_safety.py` (no component registry / new shared-code owner) | AVAILABLE | none | PRODUCT_FREEZE.md R5-R10 lines + shared-code safety invariants at candidate |
| 15 | Visible whole-project conformance and owner/projection discovery reconstructible from clean/fresh observer context | `python scripts/test_verify_standard.py`; `python scripts/resolve_standard_read_set.py` | AVAILABLE | none | standard-manifest.json, verify scripts at candidate; re-derive the read plan from a fresh clone |

## Machine-readable block (parsed by scripts/test_v410_v01_capability_map.py)

Commands are relative to the repository root. Lines prefixed `host:` are host-scope
commands (GitHub platform); they are recorded but not executed by the local verifier.

```capability-map
SUBJECT 1
AVAILABILITY AVAILABLE
COMMANDS
python scripts/test_v410_stage1_lifecycle_contracts.py
grep -n "Product Freeze" standards/DEVELOPMENT_WORKFLOW.md
grep -c "Product Freeze" docs/implementation/4.10.0/PRODUCT_FREEZE.md
LIMITATION none
END
SUBJECT 2
AVAILABILITY AVAILABLE
COMMANDS
python scripts/test_v410_t01b_product_projections.py
grep -n FROZEN_PRD_BLOB docs/implementation/4.10.0/REFINED_TASK_DAG_FREEZE_R1.md
grep -n contradiction docs/implementation/4.10.0/L2_ARCHITECTURE_EVIDENCE.md
LIMITATION none
END
SUBJECT 3
AVAILABILITY AVAILABLE
COMMANDS
grep -n V410-T08A docs/implementation/4.10.0/TASK_PACKS_R1.md
grep -ni base_sha docs/implementation/4.10.0/TASK_PACKS_R1.md
LIMITATION none
END
SUBJECT 4
AVAILABILITY AVAILABLE_LOCAL_BLOCKED_HOST
COMMANDS
grep -n "V410-T08A ->" docs/implementation/4.10.0/REFINED_TASK_DAG_FREEZE_R1.md
host: gh issue view 865 --json dependencies
LIMITATION host part BLOCKED at preparation; owner=GitHub platform; live native Issue Dependencies must be read at real dispatch
END
SUBJECT 5
AVAILABILITY AVAILABLE_LOCAL_BLOCKED_HOST
COMMANDS
git for-each-ref refs/heads/task/v4.10.0
host: gh pr list --repo kaicreator-mm/ai-development-standard --base version/v4.10.0 --state all
LIMITATION host part BLOCKED at preparation; owner=GitHub platform; remote branch/PR timing facts must be read at real dispatch
END
SUBJECT 6
AVAILABILITY AVAILABLE
COMMANDS
grep -n base_sha .agent/execution/V410-T05A-R3/MANIFEST.yaml
grep -n CURRENTNESS .agent/execution/V410-T05A-R3/FAILURE_MATRIX.yaml
grep -n claim standards/EXECUTION_PACK_STANDARD.md
LIMITATION none
END
SUBJECT 7
AVAILABILITY AVAILABLE
COMMANDS
python scripts/test_pointer_only_trigger_contract.py
grep -n pointer-only standards/ISSUE_FIRST_TASK_TRIGGER.md
LIMITATION none
END
SUBJECT 8
AVAILABILITY AVAILABLE
COMMANDS
python scripts/test_v410_t02a_collaboration_control.py
grep -n human standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md
grep -n "Human Decision Queue" standards/CHATGPT_WEB_ROLE.md
LIMITATION none
END
SUBJECT 9
AVAILABILITY AVAILABLE
COMMANDS
python scripts/test_v410_t03a_implementation_quality.py
python scripts/verify_standard.py
grep -n independent standards/VALIDATION_STANDARD.md
LIMITATION none
END
SUBJECT 10
AVAILABILITY AVAILABLE
COMMANDS
grep -n "19.3" docs/implementation/4.10.0/PRD.md
python scripts/test_v410_t04a_gate_repair_routing.py
LIMITATION none
END
SUBJECT 11
AVAILABILITY AVAILABLE
COMMANDS
grep -n superseded .agent/execution/V410-T05A-R3/TEST_MATRIX.yaml
grep -n generated_at .agent/execution/V410-T05A-R3/MANIFEST.yaml
LIMITATION none
END
SUBJECT 12
AVAILABILITY AVAILABLE
COMMANDS
grep -n ADS_CORE_FEATURE_FREEZE_ELIGIBLE docs/implementation/4.10.0/PRODUCT_FREEZE.md
LIMITATION none
END
SUBJECT 13
AVAILABILITY AVAILABLE_LOCAL_BLOCKED_HOST
COMMANDS
grep -n Qualification standards/RELEASE_STANDARD.md
grep -n independent standards/VALIDATION_STANDARD.md
host: gh pr checks 902
LIMITATION host part BLOCKED at preparation; owner=GitHub platform; live CI/gate records and Hidden/RQ verdicts must be read at real dispatch
END
SUBJECT 14
AVAILABILITY AVAILABLE
COMMANDS
grep -n R5=EXISTING_OWNER_ONLY docs/implementation/4.10.0/PRODUCT_FREEZE.md
python scripts/test_v410_t05a_shared_code_safety.py
LIMITATION none
END
SUBJECT 15
AVAILABILITY AVAILABLE
COMMANDS
python scripts/test_verify_standard.py
python scripts/resolve_standard_read_set.py
LIMITATION none
END
```

## Verification

Run `python scripts/test_v410_v01_capability_map.py` from the repository root. It asserts
that HEAD is bound to `base_sha` (equal to it, or a descendant whose only drift is this
unit's own additive write set), asserts every local command entrypoint marked AVAILABLE
exists, asserts all 15 subjects are covered exactly once, and emits a `CAPABILITY_MAP_VERIFIED`
summary block. A green run verifies the MAP's integrity only — it is not a Validation result.
