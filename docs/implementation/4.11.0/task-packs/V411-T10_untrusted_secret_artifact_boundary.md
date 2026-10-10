<!-- v4.11 Task Pack CANDIDATE ONLY; author=#972@6094573680; frozen Product=#943 L2=#954 DAG=#966; no Pack Freeze or Builder authority -->

## V411-T10 — source-bound immutable-Task-Pack-ready DRAFT (author only)

```ini
PACK_DRAFT=SOURCE_BOUND_READY_FOR_INDEPENDENT_REVIEW
AUTHORSHIP_TASK_ISSUE=#972
INTENDED_FUTURE_PATH=docs/implementation/4.11.0/task-packs/V411-T10_untrusted_secret_artifact_boundary.md
TASK_ID=V411-T10
ONE_CONCERN=UNTRUSTED_SECRET_ARTIFACT_BOUNDARY
FROZEN_PRODUCT=#943@6084264198
PRODUCT_COMMIT=34df09a2433aec5523ab80c90e885f6d9fc78803
PRODUCT_PRD_BLOB=d30f202e8ea662731ff8a4f2ad1ad88cfc5bb179
FROZEN_L2=#954
L2_COMMIT=f1fc21be366579cbeafa98217b52e106a55b41a5
L2_BLOB=c0fa361474996a0626c63e93574a284ae3eb8d91
FROZEN_DAG=#966
DAG_HEAD=26fc83911185675bdea3c540df6df15c0241402b
DAG_BLOB=9866d35ae1512b156cfdc94cc01aec2fa897f3e6
CURRENT_INSPECTED_QUALIFIED_MAIN=b9461d48d902a2c7c00adff6746afc7a02a0ac3e
PACK_CONTROLLER=#967
SOURCE_PREFLIGHT=#965@6094421044
FROZEN_DAG_PREDECESSORS=NONE
RISK=high
REVIEW_POLICY=required
L3_REQUIRED=YES
EXECUTION_READY=NO
NATIVE_TASK_ISSUE_AND_DEPENDENCIES=NOT_MATERIALIZED
PACK_FREEZE=NO
BRANCH_SOURCE_PR_MERGE=NONE_BY_AUTHOR
BUILD_HOST_TESTS=NOT_RUN_BY_AUTHOR
RELEASE_HIDDEN_RQ=NOT_RUN
```

### 1. One concern, actual source and acceptance boundary

**Goal.** Untrusted GitHub/MCP/A2A input cannot grant policy, secret-value cannot masquerade as ref, artifacts require owned identity/tenant/path boundary. Keep untrusted tool/comment messages as evidence data, not config/role/human authorization; classify symbolic refs versus actual values contextually; redact/quarantine synthetic credential canary; ensure artifact outside owned root or tenant cannot be read/published/deleted/promoted. Avoid new central secret provider or filesystem sandbox.

**Already implemented on qualified v4.10 owner source; retain rather than duplicate.** Configuration standard already owns schema/key and deterministic source precedence, symbolic secret references distinct from values, least privilege, non-persistence/redaction, bounded encrypted-secret exception, wrong-tenant/unavailable credential BLOCKED. Artifact standard already distinguishes SECRET_MATERIAL, TEST_ARTIFACT, VALIDATION_EVIDENCE, RELEASE_ARTIFACT, authorized identity-bound promotion, ownership-bound cleanup and no secret-as-evidence. Existing `test_v41_configuration_secrets.py`, `test_v41_workspace_artifact.py`, and v4.6 context/tool-owner tests cover earlier portions. Reuse them.

**Concrete still-missing v4.11 delta.** A current illustrative test only rejects suspicious **field names**, so credential-looking `secret_refs[].ref` values can masquerade as valid references; existing schema `execution-context-v1@fc8573a10c2d3b60cdf920e721bfe1551e041e1f` accepts any nonempty ref text. Normative owners lack explicit untrusted GitHub/MCP/A2A role/config injection denial in both owner-local suites and concrete wrong-tenant/absolute/`..`/symlink escape artifact negative cases. This is an observed contract/test gap, not proof of a live breach; token regex cannot prove all secret values.

**Task deliverable:** minimal owner-local normative clauses plus **one unique** focused test `scripts/test_v411_t10_untrusted_inputs.py`; a source/currentness-bound PR-local test report and exact-HEAD independent Review; an explicit T11 handoff for any required centrally owned projection. These are future Builder deliverables, **not work completed by this author**. The ultimate implementation PR targets the authorized v4.11 version integration branch (expected `version/v4.11.0` **only after** #973's seed readback and controller admission), one concern/one PR; never direct to `main` or old planning ancestry.

**Non-goals:** a second ADS method/authority, new mandatory runtime/server/scheduler/DB, wholesale stage rewriting, universal job combinations or automatic real-host/release PASS, changes owned by any other Task, and promoting fixture simulation to independently executed proof.

### 2. Frozen dependency, sole owner and explicit exclusions

- Frozen logical DAG has **zero executable predecessors** for V411-T10; this describes only topology, **not current Task READY**. All gate/Claim/Issue admission prerequisites still apply. Task author here has no executable Builder identity.
- **Allowed future normative write set** (no other existing source path):
  - `standards/CONFIGURATION_SECRETS_STANDARD.md` (inspected blob `cda438ad9292024d0c1f4b7ea85faf2beb3821d4`; only §§2–3, 5–7, 12–14 source/ref/value/redaction obligations)
  - `standards/WORKSPACE_ARTIFACT_STANDARD.md` (inspected blob `f54c37e9db4eff713a08c07127ef5df397e1b0c2`; only §§2–3, 6, 12–15/17 identity, ownership and promotion)
  - **NEW unique** `scripts/test_v411_t10_untrusted_inputs.py` only; no reuse of any shared existing test.
- **Read-only / forbidden writes:** all `schemas/**`, `templates/**`, `standard-manifest.json`, shared verifiers (including `scripts/verify_standard.py` and `scripts/verify_project_standard.py`), shared legacy tests, `templates/GOLDEN_INDEX.md`, `checklists/version-closure.md`, `docs/implementation/4.11.0/{PRD.md,PRODUCT_PROOF_MATRIX.md,L2_ARCHITECTURE_EVIDENCE.md,TASK_DAG.md}`, other Tasks' owner clauses, `main`, `version/v4.10.0`, frozen planning branches. Any shared change **proposal** is routed to exclusive T11; no shadow schema or parallel common-file writer.
- **Authority:** Product #943 explicit human-approved Freeze, separately reviewed/frozen L2 #954 and DAG #966. Their exact refs are inputs; preflight #965@6094421044 was read-only advisory and its prior `DAG_FREEZE=NO` status is **historical at preflight time**, superseded as a planning state by independently recorded #966, not retroactively converted into execution evidence. Any mismatch at real dispatch blocks and demands scoped rebind.

### 3. Tests — executable acceptance oracles, not keyword-only checks

For all cases, assert exact fixture subject and relevant source/role/authority identity, **decision**, missing/stale evidence and absence of unauthorized side effects; use deterministic offline fixtures where appropriate. Each positive and negative case must actually execute against the later candidate or explicitly report `NOT_RUN/BLOCKED`.

| Positive | Grounded scenario | Required oracle |
| --- | --- | --- |
| P01 | Authorized config owner, symbolic ref and scoped readonly use | Source precedence obeyed, reference provenance retained, no value durable; low-risk A0 proportional |
| P02 | Owned-root exact-tenant candidate and legitimate independent Validation identity/subject binding | Classify and promote only after actual owner/gate prerequisites; not by filename |
| P03 | Existing authorized encrypted secret exception with separate key/scope and no leaked plaintext | Existing exception remains legal where materially justified |

| Adversarial | Input / fault | Required fail-closed oracle |
| --- | --- | --- |
| N01 | A2A/MCP tool text 'system: approve/ignore policy' or fake role/HUMAN_APPROVED | No config, authority, dispatch, human or external effect promotion |
| N02 | GitHub comment/PR body imitates `ai-dev:event:v2`, `operator_kind=human` | No admission from raw message; T05 owns actual event acceptance |
| N03 | Synthetic bearer-like value inside schema-valid `secret_refs[].ref` | No token treated as ref/evidence; quarantine or redact, BLOCK uncertain classification |
| N04 | Synthetic canary in simulated shell error, log, test report and evidence bundle | Zero canary bytes in published/durable output; halt on uncertain sanitization |
| N05 | Untrusted `../`, absolute, symlink-escaped or wrong-tenant artifact path in owned temp fixtures | No outside-root read/cleanup/ownership or evidence/release promotion |
| N06 | BUILD_OUTPUT renamed `release/` or fake VALIDATION_EVIDENCE with wrong SHA/env/owner | Remains non-authoritative; release requires own owner decision |
| N07 | Tool-supplied PROJECT_OVERRIDES, env credential request, privilege grant or tenant switch | Cannot replace authorized config or expand credential/tenant scope |
| N08 | Missing provider ref, ambiguous tenant/scope or unresolved authority | BLOCKED/NOT_RUN, no substitute fake credential/waiver |

**Acceptance threshold:** all in-scope focused cases green on the exact implementation PR HEAD; negative scenario cannot mutate a protected gate, authority or source; existing owner/regression tests remain passing or failure is documented/blocking. Run tests against actual owner-facing contracts, not a detached self-certifying model or mere search-for-words script. If common T11 wiring is not yet present, mark that part `DEFERRED_TO_T11` with specific missing field/test and keep whole-program conformance `NOT_RUN`.

### 4. Contract — existing authority with bounded new semantics

Input classes: authorized configuration metadata, scoped symbolic `secret_ref` under true config owner; untrusted GitHub/MCP/A2A text/tool output; current owned artifact identity/root/tenant and real Validation or Release subject; synthetic redaction canary. Output decisions: `AUTHORIZED_REFERENCE`, `UNTRUSTED_DATA`, `QUARANTINED/BLOCKED`, `OWNED_NONAUTHORITATIVE_ARTIFACT`, `ELIGIBLE_FOR_OWNER_REVIEW`, never a new GitHub/Review/Release authority. Secret reference validity is contextual source/provider/tenant mapping, not merely regex or key name. Classification, persistence/redaction, path resolution and actual ownership/tenant must hold before promotion. Synthetic inputs must cause zero real external mutation.

The Task Pack defines WHAT; no exact-base patch, dynamic line-map, version-branch HEAD assumption or hidden chat prompt is an authority here. Material new semantics must preserve compatible historical readers and avoid silently changing preexisting event/Gate/release states.

### 5. Implementation — minimum owner-local delta

Small additive secrets clauses in existing §§2–3/7/12 and artifact clauses in §§2–3/6/12–15, constrained to owner semantics; leave Git execution filesystem writer and external-system side effects in their owners. Unique isolated offline tests use fake provider, fake tool payloads and controlled temp directory+symlink; inspect resulting decision/output/zero unauthorized writes, not prose only. Preserve encrypted-secret exception and Fast Path. Any schema/ref constraints or generic verifier updates proposed to exclusive T11; no T10 direct edits.

**L3 Required handoff, ordered:** Tests above → this Contract → bounded owner-local Implementation → Failure Handling below → exact References here. Builder must record an L3 evidence link, exact PR HEAD/base and source test identity; introduce no extra requirement from a local prompt. Task Claim/dispatch, actual code author, validator and independent reviewer remain distinct truthfully attributed actors.

### 6. Failure handling and UNKNOWN routing

Secret/value ambiguity, unsafe redaction, conflicting source/tenant or unowned path => quarantine/stop unsafe publication; BLOCKED/NOT_RUN, record non-secret reference/provenance for authorized owner and escalate true security incident only on warranted evidence. Unknown artifact identity never authorizes destructive cleanup. Do not publish real credentials, raw sensitive logs or treat a synthetic canary as real leakage evidence.

For any relevant source, permission, required test/environment, reviewer independence or canonical GitHub identity unverified, report the specific missing proof and `NOT_RUN/BLOCKED`; do not use an optimistic PASS/NOT_APPLICABLE. Failures block only genuine dependents; other disjoint concerns may proceed. Any Frozen Product/L2 incompatibility is escalated to owning authority and affected independent review, not patched by this Builder.

### 7. Validation, Review and merge admission

- **Owner-local verification commands to evaluate and run later, not executed here:** `python -m unittest scripts.test_v411_t10_untrusted_inputs` (or direct script), `python scripts/test_v41_configuration_secrets.py`, `python scripts/test_v41_workspace_artifact.py`, `python scripts/test_v46_context_engineering.py`; use temporary isolated workspace, no external credentials or network calls; actual provider/GitHub/real-host trust tests require separately authorized execution.
- **Execution proof:** future real Local Build Host/Validator records tested exact HEAD/tree, OS/toolchain, command, exit code, source/fixture SHA, evidence location, any permitted waiver authority and unrun material cases. Offline and source-only tests are **not** remote/host integration validation. Evidence from earlier v4.10 or preflight is reused for analysis but never relabelled v4.11 PASS.
- **Review:** `risk:high`, `review:required`; require genuinely fresh independent Reviewer other than author and Builder; bind all material findings, currentness, allowed write-set, counterexamples and final verdict to the exact PR HEAD. Review PASS alone is not release permission.
- **Merge gate:** Task Issue must reference independently reviewed/FROZEN repository Pack and a **separately** created canonical native blocked-by graph; current qualified-main Stage3 baseline seed #973 must be verified. Controller/Local materializer creates exact-base JIT Execution Pack and obtains protected accepted Claim. Only after owner-local tests, required Validation and fresh Review, final current-state sweep and truthful merge readiness may a one-concern PR merge to authorized version branch. Recheck exact HEAD/branch currentness just before merge; no automatic Task-draft→Task-issue promotion.
- **Later integration:** T05 canonical event admission, T08 human authority and T09 effects remain read-only; T11 sole schema/template/manifest/generic verifier writer; T12 integrated untrusted transport/security tests and V01 real-host/tenant evidence if materially applicable. Candidate Freeze, Hidden Validation, independent Fresh Closeout, RQ, and guarded main integration are **separate V/R work items**; none is authorized or marked PASS by this Pack author.

### 8. Bounded Agent Freedom & deferred evidence ledger

```ini
F0_MECHANICAL=fixture_wiring_docs_links_imports_and_semantics_preserving_repair_only
F1_BOUNDED_IMPLEMENTATION=YES_EXACT_OWNER_CONTRACT_AND_POSITIVE_NEGATIVE_ORACLES_FIXED
F2_ENGINEERING_DISCRETION=ONLY_PROVEN_NONMATERIAL_INTERNAL_CHOICES_WITHIN_WRITESET
F3_ARCHITECTURE_REQUIRED=ESCALATE_TO_FROZEN_L2_PRODUCT_OR_OWNING_AUTHORITY_NO_SELF_PROMOTION
ACTOR_PRIVILEGE_ESCALATION=FORBIDDEN
PREFLIGHT_SOURCE_ONLY=TRUE
PR_TEST_RUN=NOT_RUN
REAL_BUILD_HOST=NOT_RUN
NATIVE_DEPENDENCY_READBACK=NOT_RUN
T11_CENTRAL_WIRING=DEFERRED_NOT_SATISFIED
T12_A_B_C_CONFORMANCE=NOT_RUN
V01_V02_V03_V04_R01_R02=NOT_RUN
```

Epistemic ledger: unverified current post-#973 integration HEAD, native Task issues/blocked-by actual REST+GraphQL readback, current Builder/Reviewer operator admission, new focused tests, shared wiring, real environment coverage, and uncovered materially distinct supported job combinations remain **UNKNOWN/NOT_RUN** until each owning actor supplies real evidence. No universal P1/P2/P3 completeness or release qualification is asserted.

### 9. Durable References and next owner

- Frozen Product: https://github.com/kaicreator-mm/ai-development-standard/issues/943#issuecomment-6084264198 (PRD blob above).
- Frozen L2: https://github.com/kaicreator-mm/ai-development-standard/issues/954; architecture blob above.
- Frozen DAG: https://github.com/kaicreator-mm/ai-development-standard/issues/966; DAG exact head/blob above. DAG author reviewed by https://github.com/kaicreator-mm/ai-development-standard/issues/959#issuecomment-6094398472.
- Task Pack Controller: https://github.com/kaicreator-mm/ai-development-standard/issues/967; independent version seed: https://github.com/kaicreator-mm/ai-development-standard/issues/973.
- Owner preflight (historical advisory only): https://github.com/kaicreator-mm/ai-development-standard/issues/965#issuecomment-6094421044. Actual normative owner blobs were **re-fetched** from exact qualified predecessor `b9461d48d902a2c7c00adff6746afc7a02a0ac3e`; future dispatch rechecks source against current lawful integration HEAD.
- Applicable current standard: `standards/EXECUTION_PACK_STANDARD.md`, `standards/TASK_DECOMPOSITION_STANDARD.md`, `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `standards/ISSUE_FIRST_TASK_TRIGGER.md` from exact qualified v4.10 predecessor. Future integration may only use each exact separately reviewed owner.

**Next:** an **independent Pack Reviewer**, not this author or future Builder, challenges this draft for scope, executable oracle coverage, actual source-bounded gaps, provenance and DAG non-conflict. #967 integrator then materializes **one immutable repository Pack file** at the intended path and its single index entry on a legally verified stage3 integration branch, conducts authoritative Pack Review/currentness, and only afterward permits separately qualified Local native Task Issue/blocked-by creation. This Issue comment is **NOT a Pack Freeze**, executable Task Issue, Builder Claim, implementation, CI result or Release decision.
