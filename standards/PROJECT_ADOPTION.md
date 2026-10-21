# Project Adoption

## 1. 推荐接入结构

每个业务项目至少增加：

```text
AGENTS.md
.dev-standard/
├── VERSION
└── PROJECT_OVERRIDES.md
```

推荐从 `templates/project/` 初始化，而不是手工重新设计这些文件。

## 2. Immutable Standard Pin

业务项目 MUST 固定到本标准的 immutable commit SHA，不得只引用 `main`、`latest` 或聊天中的“当前版本”。

`.dev-standard/VERSION` canonical 格式：

```text
repository=kaicreator-mm/ai-development-standard
version=<semantic-version>
revision=<40-char-commit-sha>
```

其中 `revision` 是最终、不可变、机器解析的 identity authority。

### 2.1 Immutable Resolution Procedure

Agent / 工程工具解析项目标准时执行：

```text
.dev-standard/VERSION
        ↓
parse repository / version / revision
        ↓
revision is canonical identity
        ↓
resolve exact standard commit
        ↓
verify commit identity == revision
        ↓
read VERSION from exact revision
        ↓
verify VERSION == pinned version
        ↓
read AGENTS / concern-specific standards from same revision
```

规则：

1. 不得 fallback 到 `main/latest`。
2. exact revision 无法解析时不得用其它 revision 替代。
3. 已验证本地 cache 可复用，但必须证明 object identity。
4. 因网络/权限/工具无法解析时为 `BLOCKED`；未执行为 `NOT_RUN`。
5. commit identity 或 VERSION 不一致为 `FAIL`。

### 2.1A v4.12 — latest compatible stable selection is advisory, not a mutable pin

For projects **explicitly adopting the released v4.12+ contract**, the preferred discovery policy MAY be `TRACK_LATEST_COMPATIBLE_STABLE`; the default remains `PINNED/MANUAL`. This is a **read-only recommendation preference**, not an alternative effective revision, a claim admission predicate, a repository updater, an additional workflow gate or a permission for running Tasks to migrate.

The owning project can express its intent in its `PROJECT_OVERRIDES.md` (project-local policy text or a project-recognized key, without inventing a new required global schema field):

```text
standard_update_preference=PINNED/MANUAL
# optional on projects that explicitly opt in:
# standard_update_preference=TRACK_LATEST_COMPATIBLE_STABLE
```

A recommendation MAY be emitted only when all of the following **independently inspected** evidence is current and affirmative:

1. The current project's effective `.dev-standard/VERSION` parses and verifies against the **exact 40-character immutable commit SHA** (§2.1); the selected recommendation names **both** the current and proposed exact revisions, their source refs, and the observed release/compatibility evidence. Equal semver labels with unequal Git SHA are distinct identities; `main`, `latest`, a floating tag or a merely reachable commit is not release proof.
2. The proposed ADS revision is a genuinely **RELEASE_QUALIFIED** published stable standard, with current immutable candidate / actual release integration identity and separately checked release-qualification evidence; `PR PASS`, passing CI, an unsigned tag, an unqualified candidate or an unverified branch head does not meet this requirement. If its provenance is absent or incomplete, the result is `UNKNOWN / NO_SAFE_RECOMMENDATION`, not a guessed upgrade.
3. The current project declares or can prove its *material compatibility requirements*. Check the existing `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` and canonical `compatibility-record-v1` inputs as applicable to **source, wire/schema, behavior, actor/authority, Claim/Review, Validation/Release and external effects**. Compatibility is not implied by major-version equality, JSON-schema equality, a passing parser or declared executor identity. In particular, the v4.11 → v4.12 self-declared logical actor / Owner credential changes require **behavioral and authority compatibility** inspection even if no record schema changed.
4. The project's authorized adoption/checkpoint procedure can evaluate the proposed change, including any project-specific `PROJECT_OVERRIDES.md`, security, consent, permission, required reviewer, test and release floor. Unknown material evidence, incompatible obligations or absent consumer decisions fail closed to `UNKNOWN / NO_SAFE_RECOMMENDATION` while leaving the existing pin intact.

A safe read-only suggestion states `current_revision`, `proposed_revision`, actual qualified release identifier/subject, relevant compatibility evidence refs, source of uncertainty, behavioral risks, and the **next authorized project-local upgrade checkpoint**. It MAY include a manual migration and rollback *plan*. It MUST NOT silently change `.dev-standard/VERSION`, source/manifest files, Issue/Claim facts, live Task pins, frozen Product/L2/DAG/Candidate subjects, historical PASS, or release qualification. Only an **explicit project-local** version-upgrade PR/Task following §6 may adopt the new immutable revision after its real validations and authorization.

The deterministic read-only eligible-candidate selection and its focused negative tests belong to v4.12 S05. This S04 source contract **does not claim that selector has been implemented or run**. A cross-project PR writer, auto-apply, roll-forward or rollback executor is **out of scope until v4.13**; merely declaring the preference starts no background process.

**Focused counterexamples (normative outcomes):**

- No opt-in → remain `PINNED/MANUAL`; no automatic version advancement.
- Candidate tag/CI exists but **no trustworthy Release Qualification** → `NO_SAFE_RECOMMENDATION`.
- Compatible `compatibility-record-v1` *schema* but changed source permissions, logical Reviewer context or human-approval semantics not evaluated → `UNKNOWN`, not safe.
- Same version string on two commits → preserve both SHA identities; do not treat them as interchangeable.
- Already active Task or open Claim under old revision → keep the old **effective** SHA until lawful project-local version checkpoint; a discovery suggestion never rebinds it.
- Evidence-only/low-automation A0/A1 consumer → no extra machine agent requirement or missing-E3 PASS; required substantive checks are identical to A2–A4.

### 2.1B v4.13 — source-proven prospective planning, opted-in PR, and safe activation

The **v4.12 read-only safe recommendation selector and its refusal semantics remain unchanged.** Current `scripts/v412_ads_compatible_select.py` conservatively reports `NO_SAFE_RECOMMENDATION` with `ACTIVE_OR_UNCLASSIFIED_WORK_ITEM` when a target project has any open Issue/PR. Such refusal is **not** evidence that a release is compatible, and MUST NOT be transformed into `SAFE` or used as authorization for a consumer update PR. This clause adds a **distinct, non-SAFE prospective planning contract** for an adopting project under a qualified v4.13+ effective standard; it does not retrofit the already-published v4.12 selector or invent a new Gate/workflow state.

#### Source-bound prospective evidence (read-only, never activation)

A consumer implementation MAY describe a newer ADS revision as `EVIDENCE_BACKED_COMPATIBLE_PROPOSAL` **only** after independently establishing all of:

1. Current project's effective `.dev-standard/VERSION` exact immutable source and its actual project-local adoption/compatibility requirements.
2. Proposed ADS exact SHA with observed **published stable Release Qualification**, frozen candidate/merge/published identity and actual current source references. Semver, a tag alone, a green PR or mere reachability are not sufficient.
3. Affirmative project-specific compatibility evidence for actual impacted **source/schema, behavior, actor/authority, Claim/Review, Validation/Release, migration and external effects** according to `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` and applicable source records. A parser or schema-only comparison is not affirmative semantic compatibility.
4. A current, auditable source/compatibility evidence reference set for both project and proposed ADS release.

This proposal is a **non-SAFE advisory description**; it does **not** assert that the active project can yet apply the new revision or that its accepted Tasks are isolated. If any material qualification/compatibility/source evidence is missing, stale, contradictory or unknown, return `PROSPECTIVE_UNVERIFIED/UNKNOWN` with evidence gap. A possible candidate may be listed for investigation but MUST NOT be called compatible, `SAFE`, ready-to-merge or the basis for an actual version-update PR. These descriptive labels are **not** new global Gate states; canonical Validation remains `PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE`.

The current v4.12 selector may **simultaneously** refuse a safe recommendation while a *separately proved* prospective compatible proposal is available. Neither evaluator can promote the other's unproven result. Unrelated open GitHub Issues are not by themselves proof of active Task conflict; equally, a lack of classified Claim evidence cannot be invented from open Issue counts.

#### Independent checkpoints: plan → project PR → pre-merge activation

```text
PROSPECTIVE_READ_ONLY_PLAN
  real published candidate + consumer compatibility proofs OR explicit UNKNOWN
  source output only; current effective pin and accepted Task pins unchanged
        ↓
OPTED_IN_PROJECT_UPDATE_PR
  project explicitly opts in; exact old/new SHA, allowed write-set, current
  target branch HEAD/CAS, deduplicated PR, GitHub rights and readback
  missing qualification/compatibility ⇒ NO PR
  PR prepared/open does not change effective pin
        ↓
PROJECT_CHECKPOINT_ACTIVATION (BEFORE PR MERGE)
  re-read target HEAD/effective project pin & overrides, real permission,
  native Issue Dependencies/accepted Claim/current Task frozen versions,
  required Review/Validation/Release obligations and material source impact
  UNKNOWN/conflict/stale base ⇒ HOLD PR without merge
  proof complete ⇒ authorized merge; new effective pin applies only to
  eligible new/checkpointed Tasks, accepted old Task stays on old SHA
        ↓
ROLLBACK IF NECESSARY
  new project-authorized, source-bound reversal PR/current checks/readback;
  no historical Evidence/Claim/Review/Task re-label
```

**Do not merge first and 'activate later'.** Merging a PR that writes effective `.dev-standard/VERSION` **itself changes** the project's effective pin. Thus the real affected Task/Claim/frozen candidate/permission/readback and selected check/Review conditions must be satisfied **before the merge**. Where accepted in-flight Tasks cannot retain their original immutable ADS revision across that transition, activation must fail closed. A prepared update PR does not grant authority to bypass branch protection, currentness, platform rights or external-effect gates.

A project without explicit opt-in remains `PINNED/MANUAL` by default. The updater MAY be built by an external consumer such as Tally v2; its **actual** organization discovery, repository writes/PR creation, Agent or Host orchestration, approval execution and rollback runtime are **not implemented by the ADS standards repository**. ADS v4.13 owns only the qualified evidence/authority contract. No background scan, update service or CLI becomes mandatory for standalone ADS adopters.

**Focused counterexamples (contract-level, not real updater E2E):**

- **Positive prospective only:** Project has unrelated open Issues, an accepted Task pinned to ADS A, and independently verified qualified/compatible ADS B. The unchanged v4.12 safe selector still returns `NO_SAFE_RECOMMENDATION`, while a source-proven **non-SAFE** `EVIDENCE_BACKED_COMPATIBLE_PROPOSAL(A→B)` may be emitted. Effective project pin and accepted Task pin remain A until lawful checkpoint; accepted prior Task stays on A after.
- **Unknown candidate:** Same active project but qualification or behavior/authority compatibility unverified ⇒ `PROSPECTIVE_UNVERIFIED/UNKNOWN`, not compatible or safe; no update PR.
- **No opt-in / wrong base / permission denied:** Proposal is not an executable PR authorization. No source change, no fabricated GitHub acceptance.
- **Merge/activation unknown:** Missing Task-isolation proof, native blocker/Claim source currentness or required Review/Validation ⇒ update PR remains unmerged; an unauthorized merge cannot be reported as legitimate activation.
- **Rollback/historical:** A new source-bound rollback never rewrites the ADS SHA of previously accepted/validated Tasks or projects' historic Release/Review outcomes.

### 2.1C v4.15 — independently qualified untagged main commit: manual adoption vs advisory discovery

This prospective v4.15 clarification distinguishes an **explicit project-local `PINNED/MANUAL` upgrade checkpoint** (§6) from the conservative v4.12 read-only `TRACK_LATEST_COMPATIBLE_STABLE` *recommendation selector*. An optional Git Tag or GitHub Release is a discoverability/publication alias; it is **not** a new normative Release Qualification Gate for manual adoption. A semver string, an untagged reachable branch commit, passing CI, or a successfully merged unqualified PR are likewise **not** proof of a releasable standard.

A project MAY manually choose an untagged ADS commit **only when every applicable predicate is independently verified and source-bound**:

1. `revision` resolves to a **full immutable 40-hex SHA** that is **actually integrated into the ADS `main` history**; do not accept a mutable `main` ref, detached candidate, mere open PR or tag alias as the effective pin.
2. A distinct ADS Release Qualification verdict `READY` is present for the **exact frozen version candidate SHA/tree**, and its actual repository-integration record binds that candidate to the chosen main integration SHA/tree; source differences and merge-base/currentness impact are explicitly reconciled under the existing Release/Repository Integration authority. `PR PASS` does not equal `Release PASS`, and `RQ READY` alone does not prove main integration.
3. The selected commit's `VERSION`, `standard-manifest.json`, protocol/schema bytes and required historical/current compatibility expectations are inspected at that exact SHA. The project's existing effective revision, `PROJECT_OVERRIDES.md`, and applicable source/wire/behavior/actor/authority/Claim/Review/Validation/Release/external-effect compatibility are **affirmatively** checked; missing information is `UNKNOWN`, not an automatic compatible choice.
4. The project's explicit authorized version-update PR/Task under §6 passes its own required checks and last-admission/currentness/permission criteria **before merging**; in-flight Tasks/Claims/frozen candidates remain pinned to their accepted former ADS revision unless an independently allowed checkpoint proves a safe transition. A manual choice does not activate merely because an Agent recommends it.
5. The durable adoption evidence identifies `old_revision`, `proposed_revision`, `qualified_candidate_sha/tree`, `release_qualification_ref`, `repository_integration_ref`, exact new `VERSION` evidence, compatibility evidence, project update PR/checkpoint and the **effective pin after authorized merge**. Re-read facts at decision time; `BLOCKED` or `NOT_RUN` stays honest.

**Observed predecessor example (not a waiver):** v4.14.0 was Release-Qualified and merged into `main@584512e8566408bed479192753c12a036309d277`; the user did not require a v4.14.0 Tag/Release alias. That exact commit may be **considered** for a project's manual adoption only if its real RQ/integration source links and *that project's* source/wire/authority compatibility and legal upgrade checkpoint are independently confirmed. This sentence is **not** a blanket approval of every adopter or proof of uninspected refs.

**Legacy selector remains conservative:** `scripts/v412_ads_compatible_select.py` keeps its original published Tag+GitHub Release and active-work refusal behavior for an automated read-only recommendation. Its `NO_SAFE_RECOMMENDATION` for an untagged candidate is **not a manual-upgrade veto** and **not** a proof of compatibility. No automatic selector flag, hidden override, relaxed threshold, cross-repo PR writer or automatic activation is authorized here.

**Pre-Release v4.15 interoperability tests use a different identity:** a *frozen, immutable v4.15 candidate SHA* MAY be selected as an **isolated validation subject** for the real task-meta → GitHub → Tally conformance journey. Record it as `test_subject_revision` with bounded smoke Issue/adapter config and exact source/currentness; **do not set it as the project's effective `.dev-standard/VERSION`**, do not mutate accepted live Claims/Task pins or infer qualified Release from test configuration. Material candidate drift invalidates affected tests. A production adoption becomes eligible only after the exact candidate satisfies the applicable ADS contract-source Release Qualification and is actually integrated into main, with the project-local predicates above independently satisfied. Real task-meta/Tally integration remains separately scoped and `NOT_RUN` until executed (#1210); `REAL_TASKMETA_GITHUB_PUBLICATION_NOT_PROVEN` and `REAL_TALLY_GITHUB_ONLY_READER_FEEDBACK_NOT_PROVEN` remain explicit limitations, not ADS contract-source Release prerequisites or runtime PASS.

**Discriminating examples (expected resolution, not simulated test PASS):**

| Scenario | Normative outcome |
| --- | --- |
| RQ-ready candidate/main integration observed and project-local compatible evidence confirmed, but no Tag or GitHub Release | `PINNED/MANUAL` **MAY proceed** through §6 authorized PR/Validation/checkpoint. Existing auto selector may still refuse. |
| Tag/Release exists but actual RQ verdict, candidate/tree mapping or current project compatibility missing | `UNKNOWN/NO_SAFE_RECOMMENDATION`; **manual activation denied** pending evidence. |
| `main` names latest changes but no exact qualified commit or source linkage | `BLOCKED`; **never** substitute floating main for a revision. |
| Exact RQ-qualified main SHA exists, but project has an incompatible live Claim or unresolved schema/authority change | **Do not adopt** until an authorized non-weakening checkpoint proves safety; old Task remains on old pin. |
| Frozen v4.15 candidate used by isolated smoke Agent before Release Qualification | `test_subject_revision` **only**; required E2E remains `NOT_RUN` until executed, and effective project pin is unchanged. |

This section clarifies **only** the already-required selection/evidence authority. It changes neither the v4.12 selector's published-stable definition nor existing exact-RQ/Project-Upgrade truth, and it does not create a new Gate, Owner account requirement or compulsory GitHub Release.

### 2.2 v4 Progressive Adoption（A0–A4）

v4 adoption level 只描述项目采用多少 Operation / Assurance / machine-contract / automation 能力，**不改变 mandatory truth floor**。低 adoption level 代表实现更轻，不代表 required gate 更少。

项目 pinned 到 v4 后 MUST 在 `PROJECT_OVERRIDES.md` 声明一个 adoption level：

```text
A0_COMPATIBILITY
A1_MANUAL_PROTOCOL
A2_MACHINE_CONTRACTS
A3_DERIVED_AUTOMATION
A4_FULL_ORCHESTRATION
```

语义：

| Level | Required implementation surface | 可不启用 |
|---|---|---|
| `A0_COMPATIBILITY` | v4 immutable pin + v3.4-compatible durable facts / authority / exact identity / required Validation & Review semantics | v4 Operation/Assurance machine records、reducer/controllers、Interchange automation |
| `A1_MANUAL_PROTOCOL` | A0 + 以 durable GitHub/file facts 手工记录 v4 Operation/Assurance 概念 | schema gate、自动 reducer/controller |
| `A2_MACHINE_CONTRACTS` | A1 + 对已采用的 v4 records 运行当前 schema / semantic verification | 自动 reducer/routing/controller |
| `A3_DERIVED_AUTOMATION` | A2 + 从 durable facts 派生 reducer / queue / routing / controller state | 全项目 full orchestration |
| `A4_FULL_ORCHESTRATION` | A3 + 项目真实选择的 Operation / Assurance / Interchange / controller automation | 不要求实现项目不需要的机制 |

A0→A4 能力单调增加，但每一级都共享同一 non-weakening floor：

- immutable standard pin + durable authority；
- exact subject identity；
- required Validation = required tuple 上真实成功执行；
- Review 与 Validation 分离，Review Policy 由 authority 决定；
- P0/P1 blocker 不得被 reviewer/model majority 投票消除；
- Candidate PREPARED != FROZEN；
- PR PASS != Release PASS；
- Release READY != Repository Integration complete；
- Interchange / routing / reducer projection 不拥有 truth；
- `NOT_RUN / BLOCKED / NOT_APPLICABLE` 必须保持真实语义。

因此：项目可以长期停留在 A0/A1，而无需部署 reducer/controller；但不能以“我们只是 A0”为理由跳过 required Validation、required Review、Candidate Freeze 或 Release Qualification。

Effective-rule 解析与 adoption level 解耦（v4.11）：对同一 exact subject 的同一组 independently inspected material facts（permission / security / migration / deploy / external-effect），A0–A4 任一级 MUST 解析出同一组 required gate 与 hard predicates；adoption level 只选择 evidence 的收集与记录机制（A0 手工 durable facts、A4 machine record），不改变义务本身。任何 profile、job label 或更低 authority 的 override MUST NOT 削弱其它 owner 已要求的 gate；observation 缺失或来自过期 HEAD 时事实为 `UNKNOWN`，按 fail-closed 处理，不得记为已检视的 `ABSENT_WITH_INSPECTED_SCOPE`。

### 2.3 v3.4 → v4 Compatibility

v4 不要求把 v3.4 durable history 重写成新协议：

- `.dev-standard/VERSION` immutable pin 机制保留；
- Frozen PRD / Frozen Architecture authority 保留；
- Task DAG planning checkpoint 与 GitHub Issue Dependencies live execution DAG 保留；
- Task Pack / Execution Pack 保留，Execution Pack 仍可选且 subordinate；
- exact-SHA Validation 保留并强化，不得用模型共识替代；
- Review Policy `required / recommended / not-required` 保留，可映射为 Assurance activities，但 policy authority 不迁移；
- Builder / Validator / Reviewer role/profile 保留；
- `ai-dev:event:v2` 保留，v4 adoption 不要求 event-v3；
- Fast Path 保留并强化 fail-closed disqualifiers；
- Candidate Freeze / Release Qualification / Repository Integration 三者继续分离；
- GitHub durable facts 继续可承载协议记录，Chat 仍不是项目状态。

历史 v3.4 PASS / FAIL / CHANGES_REQUESTED 必须保留原始 subject identity 与 status。迁移到 v4 不得把历史 evidence 宣称为“已经经过 v4 machine contract”。完整迁移矩阵见 `docs/implementation/4.0.0/MIGRATION_ADOPTION_GUIDE.md`。

### 2.3A v4.13.1 — Executable adopter admission (bounded maintenance)

A consumer claiming **repository-root ADS v4 adoption** MUST run the pinned source's `scripts/verify_project_standard.py <project-root>` (or an equivalent verifier) against the actual *adopted project root* and reject missing, ambiguous, placeholder or unsupported `v4.adoption_level`. A merely present `PROJECT_OVERRIDES.md` or an embedded sample under another repository does not satisfy root adoption. The parser accepts one explicit `v4.adoption_level` A0–A4 declaration; unqualified v1/v3 historical pins retain their previous structural contract. Exact revision resolution remains separate and is `NOT_RUN` unless actually performed. An adapter MAY support explicit independently approved monorepo roots, but MUST bind the declared root to a real project/repository identity instead of assuming nested fixture proof applies to the enclosing repository.

This is an enforcement of the existing §2.2 MUST, not a new gate status, adoption level or Tally runtime requirement.

**Field-validation acceptance identity:** A consumer's original whole-process `verification_objective`, its required evidence matrix, and the narrower source-only `release_subject` MUST be recorded separately before executing tests. A release-controller MAY qualify an isolated source artifact under existing `RELEASE_STANDARD.md` §6/§11, but MUST NOT describe that as a full adopter/native DAG/CI-provider/Tally validation PASS if the original objective included unexecuted cases. Unknown original acceptance remains `HOLD / NOT_PROVEN` in the report; no new gate state or retrospective v4.13.0 change is introduced.

### 2.4 Fast Path 与 adoption level 正交

Fast Path 可以在 A0–A4 任一级使用：

- 项目 MAY 全局禁用 Fast Path；
- 项目 MAY 增加更严格的 disqualifier；
- 项目 MUST NOT 删除 canonical v4 Fast Path disqualifiers；
- adoption level 本身不是风险证明，A0/A1 不自动等于 Fast Path eligible；
- A3/A4 controller 可以派生 eligibility，但派生状态不替代 owning facts。

### 2.5 v4.8 Convergence Discovery（非权威接线）

v4.8 保留 v4.7 的 authority registry / read routing 发现机制，并把三个新 machine family 注册进同一发现层。对 pin 到 v4.8+ 的项目，以下仅为发现/读取面：

- Canonical owner discovery：`standard-manifest.json#semantic_authorities`（entry 指向既有 canonical owner，例如 `standards/EXECUTION_ARCHITECTURE_STANDARD.md`、`standards/CI_RUNNER_CAPABILITY_STANDARD.md`）；
- Qualified state / non-inference discovery（按需）：`registries/state-dimensions-v1.json`；
- Derived read routing helper（可选）：`scripts/resolve_standard_read_set.py`；
- v4.8 注册/采用映射（非权威）：`references/V48_REGISTRY_ADOPTION_REFERENCE.md`；
- 迁移/采用增量：`docs/implementation/4.8.0/MIGRATION_ADOPTION.md`。

规则：

- 发现/路由元数据不授予任何 authority：`authority_effect=NONE`、`gate_effect=NONE`、`mutation_authorized=false`；registry / read routing 不拥有 mutation、Validation、Review、Candidate、Closure 或 Release truth。
- 先解析并读取 canonical owner 再行动；compatibility alias 仍只是兼容路由，不是 owner。
- 三个 v4.8 machine family（Task Learning Evidence、logical Agent Capability Profile、Agent Capability Evidence）由既有 semantic owner 拥有；registry 只是让它们可被发现，不产生第四个语义 owner。
- Current Availability 是派生状态，不是 durable family；provider/model identity 与 capability evidence 描述能力或出处，不是 correctness/authorization/routing admission 的证明，也不是当前 Validation/Review truth。
- Fast Path 保持轻量：`TASK_LEARNING=NONE_MATERIAL` 是合法完整结果；可选 registry/profile/family 只按 materiality 加载，其存在不构成项目采用义务，也不得因 v4.8 包含它们而强制加载无关可选内容。
- 兼容性为纯增量：历史 inventory 与 Fast Path disqualifiers 保持不变；不兼容的 path/schema/authority 变更是 next-major planning input，不得被静默吸收。

## 3. PROJECT_OVERRIDES

`PROJECT_OVERRIDES.md` 只记录项目特有信息：

- repository profile / intentional structure deviation；
- bootstrap / lint / test / build commands；
- validation execution environments；
- CI profile；
- CI provider/backend/runner/workflow execution profile；
- platform/runtime/toolchain requirements；
- project-specific hard boundaries；
- release gates；
- sensitive area / ownership rule；
- v4 adoption level / compatibility mode / adopted automation surface。

不得复制整套全局标准，也不得削弱关于事实、Validation、冻结语义和 release claim 的硬约束。

PROJECT_OVERRIDES MAY 选择较轻的 v4 implementation surface，也 MAY 加强 Assurance、Validation、Review、Fast Path 或 release gate；但 MUST NOT weaken 更高 authority 已经要求的 gate，也不得把 Interchange/model consensus/controller projection 提升为 owning truth。

### 3.1 Validation Execution Profile

项目 SHOULD 明确声明真实验证环境，例如：

```text
Linux validation = Ubuntu Build Host
Windows validation = Windows workstation
macOS validation = real macOS host
```

需要矩阵时，required tuple 应明确到：

```text
<platform> × <runtime/toolchain> × <profile>
```

cross-build 不得替代 frozen authority 要求的真实 platform execution。

### 3.2 CI Profile

项目 MUST 明确 CI profile：

```text
minimal
custom
disabled
```

默认推荐 `minimal`。

`minimal` SHOULD 只运行低成本、确定性、clean-checkout checks，例如 project verifier、format/lint/typecheck 子集、快速 unit/contract smoke、basic build smoke。

`custom` 必须列出具体 checks 与使用理由。

`disabled` 必须记录：

- 为什么不使用 CI；
- exact-SHA clean validation 替代路径；
- review/merge policy。

CI profile 不能改变 frozen product/release gate。

### 3.3 CI Execution Profile

当 CI profile 为 `minimal` 或 `custom` 时，项目 SHOULD 按 `CI_EXECUTION_STANDARD.md` 声明真实执行模型，至少包括：

```text
CI provider
CI backend / execution model
CI runner role
workflow config path
workflow config source semantics
execution shell / entrypoint model
runtime/toolchain source
fresh-run / rerun policy
```

如果 clone/checkout 的 provider 默认值会影响可复现性或稳定性，还 SHOULD 明确：

```text
partial clone/filtering
submodule recursion
Git LFS
clone plugin/entrypoint model
```

规则：

1. provider/backend 是执行语义，不是装饰性 metadata；修改 provider-specific workflow 前必须先解析它们。
2. 不得因为字段名叫 `image` 就假设一定代表 container image；含义由 provider + backend 决定。
3. Local/host backend 使用宿主机 runtime 时，应声明 runtime source 并在 CI preflight 中验证真实版本。
4. workflow config source 必须足以解释 provider 是读取当前 PR HEAD、merge ref、base branch、stored snapshot 或其它来源。
5. 新 source SHA 需要能证明该 SHA 的 fresh run；旧 pipeline 的 rerun/restart 不得作为新 HEAD evidence。
6. provider-specific 绝对路径可以作为项目/runner contract 记录，但不得反向成为全局标准硬编码。
7. secrets/registration token/private credential 不得写入 `PROJECT_OVERRIDES.md`。

当 CI profile 为 `disabled` 时，CI execution fields MAY 使用 `NOT_APPLICABLE — <reason>`，但 exact-SHA clean-validation fallback 仍必须真实可执行。

### 3.4 Required Gate Authority

项目 mandatory gate 必须遵循：

```text
Frozen PRD / Contract
→ Frozen Architecture
→ PROJECT_OVERRIDES
→ Task acceptance
→ Standard defaults
```

PROJECT_OVERRIDES 可以增加项目真实需要的 gate，但不得因为历史 workflow/旧脚本存在而推导新 mandatory gate。

对于 v4 adoption，PROJECT_OVERRIDES 只能在自身 authority 层选择 default/implementation surface；若 Frozen PRD、Frozen Architecture 或 Task 已要求更强 Assurance/Validation/Review/Release gate，override MUST NOT downgrade。

Effective rule 在 exact subject 上解析时（v4.11），先在同一 concern 内按上述 precedence 解析 strengthening/narrowing，再跨所有 applicable owner/concern 取逻辑 AND：任一 owner 的 required gate 保持 required，一个 owner 内合法的 `NOT_APPLICABLE` 不解除其它 owner 的 gate。observation 缺失、过期或 owner 之间相互矛盾时 fail closed（gate 保持 `NOT_RUN` / `BLOCKED`，见 `DEVELOPMENT_WORKFLOW.md` §4），不得静默取最低公分母，也不得以风险 label 单独豁免。

### 3.5 Required-but-unestablished command / runner

命令字段必须描述真实可执行能力，不得为满足 checklist 编造 shell command。

- 尚未执行且 runner 待建立：`NOT_RUN — <reason>`；
- 因前置条件/权限/工具/环境当前无法建立/执行：`BLOCKED — <reason>`；
- 只有确实不适用时：`NOT_APPLICABLE — <reason>`。

不得用 `NOT_APPLICABLE` 隐藏 required gate，也不得用 placeholder command 冒充 executable validation。

### 3.6 Execution Pack / Pull Worker / Validation Queue（v3.4，可选）

v3.4 能力是渐进可选的；不启用不削弱任何 required gate。项目 MAY 在 `PROJECT_OVERRIDES.md` 声明：

```text
execution_pack.enabled / path / retention / package_exclusion
pull_worker.builder / validator / reviewer
validation_queue.enabled / scope
local_first.enabled
```

语义：

- Execution Pack 权威低于 Task Pack，只能收窄执行自由（`EXECUTION_PACK_STANDARD.md`）；
- Builder/Validator/Reviewer 是同一个 canonical dispatch 架构的 role/profile，不是三套队列状态机；
- version-scoped Validation Handoff Queue 是 Validator dispatch 的投影（`templates/validation-handoff-queue.md`），不是第二工作流权威；
- Execution Pack 材料（`.agent/execution/`）必须可从 shipped package/product artifacts 中排除，package leakage 属于 packaging gate defect；
- Fast Path 小任务可省略 large Execution Pack / seed / validation queue / dedicated worker，但保留 authority、exact identity、validation、evidence、merge safety。

### 3.7 v4 Override Surface

项目 MAY 在 `PROJECT_OVERRIDES.md` 声明：

```text
v4.adoption_level
v4.compatibility_mode
v4.assurance.default
v4.model_diversity.default_basis
v4.interchange
v4.reducer
v4.controllers
v4.fast_path
```

规则：

1. `v4.adoption_level` MUST 是 A0–A4 之一。
2. `v4.compatibility_mode` 描述 migration 状态，不得改变 frozen authority。
3. `v4.assurance.default` 与 `v4.model_diversity.default_basis` 仅在没有更高 authority 已经指定更强要求时作为默认值。
4. `v4.interchange` 若启用，authority semantics MUST 仍是 `CORRELATION_ONLY_NON_AUTHORITATIVE`。
5. `v4.reducer` / `v4.controllers` 只能声明真实存在的 automation；关闭它们时 required gate 必须有真实 manual/fallback path，否则为 `BLOCKED`。
6. `v4.fast_path` MAY 禁用或加强 eligibility，MUST NOT 移除 canonical disqualifiers。
7. override MUST NOT 把 Review/model majority 变成 Validation truth。
8. override MUST NOT 把 Candidate Freeze、Release Qualification 与 Repository Integration 合并成单状态。
9. override MUST NOT 用 branch/latest/chat identity 替代 exact subject identity。
10. override MUST NOT 通过把 `BLOCKED/NOT_RUN` 改写成 `NOT_APPLICABLE` 获得 green state。
11. 声明的 job label 是 multi-label set，只是识别义务的辅助证据：obligation closure 由 declared job set 与 independently observed material facts（permission / security / migration / deploy / external-effect，含 observation ref 与时效）共同推导；MUST NOT 因删除某个 label 而解除已检视事实对应的义务。
12. override MUST NOT 以风险 label、profile、adoption level 或更低 authority 削弱其它 owner 已要求的 gate；跨 owner 合取中一个 owner 的合法 `NOT_APPLICABLE` 不解除其它 owner 的 required gate；与更高 authority 矛盾时为 `CONFLICT`，受影响 gate 保持 `BLOCKED`。
13. 事实维度只有 `PRESENT` / `ABSENT_WITH_INSPECTED_SCOPE` / `UNKNOWN` 三种 epistemic 状态：observation 缺失或来自过期 HEAD 为 `UNKNOWN`，fail closed，MUST NOT 记为 `PASS`；这三种状态不是新增 gate 枚举。

### 3.7A v4.12 — risk-bounded value and least-ceremony adoption

Before proposing *optional* Scaffold/DAG work, another independent review/Host rerun, a new template, large-scale empirical research or non-core features, classify actual obligations from frozen Product/Architecture, security/permission/external effects and observed source facts: `CORE_MANDATORY`, `CONDITIONAL_MATERIAL`, `NONCORE_OPTIONAL` or `UNKNOWN` (descriptive reasoning labels, **not** new workflow states). For truly optional work, compare falsifiable consumer benefit with whole-life implementation, review/Host/CI, delay, maintenance and opportunity cost; prefer existing reusable source/tests and the smallest discriminating check. A compact source-grounded explanation is enough; **no required ROI score/form, extra Task, three-LLM vote or human sign-off** is created.

Permitted advice includes `DO_MINIMAL`, `REUSE_EXISTING`, `BATCH`, `TIMEBOX_RESEARCH`, `DEFER_WITH_TRIGGER` or `EXCLUDE_WITH_REASON`, only within the actually authorized product scope. Record owner decision, user impact, residual risk and reconsideration trigger when excluding material work. A low expected ROI, a Fast/A0 label or a model opinion **never** downgrades frozen commitments, required independent Review, a real human-deny/external consent obligation, security/permission, accepted CAS Claim, executed validation or Release Qualification. `NOT_RUN` may not become `NOT_APPLICABLE` just to cut cost; a post-Freeze mandatory change requires the proper authority-bound amendment.

New projects may generate a **bounded** Scaffold only after valid version adoption and an actual accepted source Claim; mature projects SHOULD reuse existing source, data and fixtures instead of regenerating a full Task DAG. A0/A1 manual fact collection and A2+ automation share the same technical admission and Release truth requirements. LLM-generated Gold or forum self-reports do not become blinded human empirical evidence by declaration.

### 3.8 v4.5 独立适用性：runtime / incident / maintenance

对采用 v4.5+ 的项目，`PROJECT_OVERRIDES.md` SHOULD 明确三项**相互独立**的适用性声明：`v4.runtime`、`v4.incident`、`v4.maintenance`。项目 MUST 依据 Frozen Product/Architecture/Task 和真实项目责任分别判断，而不是由 A0–A4 或 repository profile 自动推断。适用性与能力实现/验证状态是两维；声明 `APPLICABLE` 不构成 PASS。

- `v4.runtime`：指明运行时观测的适用性、需求 authority、精确 artifact/deployment/environment/observation-window subject、数据来源及 required execution status。无部署或运行时责任的库 MAY 用有根据的 `NOT_APPLICABLE`，但 required runtime 信号缺失时 MUST 保持 `NOT_RUN` 或 `BLOCKED`。
- `v4.incident`：指明 incident/recovery/engineering-feedback 是否属本项目责任，关联 incident owner、可批准的生产副作用 authority、证据来源与后续路由。不实际负责 incident 的非运行时库 MAY 用有根据的 `NOT_APPLICABLE`；仅模拟的 conformance 不能冒充真实生产事故或生产恢复 PASS。
- `v4.maintenance`：单独指明 support-line、baseline、EOL/hotfix/backport 责任及 result-SHA validation policy。一个 runtime/incident 为 `NOT_APPLICABLE` 的 library 仍可能需要真实维护、支持与回移。分支、标签和安装包存在不构成 support status。

`NOT_APPLICABLE` 必须有明确的非适用理由；未完成必须执行的评估或活动为 `NOT_RUN`，受阻为 `BLOCKED`，不得用不可用的 telemetry、runner、权限或 environment 推导出 `NOT_APPLICABLE` 或健康事实。新项目只对自身当前实际范围记录事实；不得回写历史 Release、incident、support 或 v4.1/v4.2/v4.4 evidence 的语义。三项规范及对应 reference、T01 schema 的路径以 pinned `standard-manifest.json` 为准；完整场景与禁止推断详见 `docs/implementation/4.5.0/MIGRATION_ADOPTION.md`。Testing、Test Data、Validation、Release 均沿用现有 owner，不创设第二套 Operations/Validation/Release 状态机。


## 4. 业务项目 AGENTS.md

最小逻辑：

```text
Read .dev-standard/VERSION and .dev-standard/PROJECT_OVERRIDES.md first.
Resolve the exact pinned standard revision.
Then read pinned AGENTS.md and concern-specific standards.
```

推荐使用 `templates/project/AGENTS.md`。

## 5. 首次接入

1. 确认 repository baseline 和 project type。
2. 复制 `templates/project/` 中适用文件。
3. 写入当前采用标准的 version + 40-char revision。
4. 填写真实 commands、validation environments、CI profile、CI execution profile、platform/toolchain matrix、release gates。
5. v4 项目声明 adoption level；已有 v3.4 项目优先从 A0/A1 开始，除非已经真实具备更高层 machine/automation 能力。
6. 完成 immutable resolution 与 version/revision consistency 验证。
7. 执行 `scripts/verify_project_standard.py <project-root>` 或 pinned revision 中等价 verifier。
8. 按 `checklists/project-init.md` 检查 repository structure、docs、tests、Validation、Minimal CI execution/evidence policy、v4 non-weakening floor 和 release gates。
9. 作为独立 PR 合并接入变更。

## 6. 升级标准版本

标准升级必须作为显式 PR/Task：

1. 选择目标标准 commit SHA 并确认 VERSION/CHANGELOG。
2. 阅读 breaking changes 与新增/变化 standards/templates。
3. 判断与项目 override、Validation、CI profile、CI execution profile、release policy 是否冲突。
4. 对 v3.4→v4 升级，选择最小真实 adoption level，并明确 compatibility mode；不得为了“看起来先进”虚报 A2/A3/A4。
5. 更新 `.dev-standard/VERSION`。
6. 必要时同步项目模板；不要机械覆盖已有定制。
7. 重新完成 immutable resolution。
8. 运行 project verifier 与项目 required validation。
9. 确认历史 evidence 保留原 subject/status，不做 PASS migration。
10. 合并后从新 revision 开始执行。

## 7. 不推荐做法

- 声明永远使用 standard `main/latest`。
- 只记录 semantic version 没有 immutable SHA。
- exact revision 失败后偷偷读取 main/latest。
- 每项目复制整套 standards 后各自漂移。
- 把领域规则反向塞入全局工程标准。
- 依赖聊天记忆判断采用 revision。
- 把 CI 当成完整 Validation 或 Release Qualification。
- 未声明 backend 就按另一个 CI/backend 的语义修改 workflow。
- 用旧-SHA pipeline rerun 冒充当前 PR HEAD 的 Validation Evidence。
- 为追求“绿”把 required gate 从 override 中删除。
- 把低 v4 adoption level 当成降低 truth/Validation/Review 标准的理由。
- 声明 A2/A3/A4，却没有执行对应 machine contract / derived automation。
- 迁移时重写历史 PASS/FAIL/CHANGES_REQUESTED 或改变原 evidence identity。
