# ADS v4.13 — Organization Development Environment & Toolkit (L1/L2 Design Candidate)

> **NON-NORMATIVE; PRODUCT_INTAKE / ARCHITECTURE_CANDIDATE; NOT FROZEN.**  
> Parent planning authority: [#1147](https://github.com/kaicreator-mm/ai-development-standard/issues/1147). This source-only design proposes bounded reuse of existing devkit and upstream tools. It grants no new Task/Claim/Review/Release authority or implementation permission. Final tool/provider acceptance, PRD/L2 Freeze and executable Task DAG remain separate.

## 1. Product decision

**Build a unified organization development experience, not a second development orchestration platform.**

- **ADS standards / exact pinned project contract**: what is valid, compatible, testable and releasable.
- **Organization Development Environment Profile (ODEP)**: portable organization defaults and available capabilities; subordinate to material project authority.
- **ADS Dev Toolkit (CLI)**: execution adapter that resolves environment, prepares repos/worktrees, invokes selected tools, reports truthful checks and controlled cleanup.
- **Agent Skill / optional MCP adapter**: thin access surfaces over the same CLI/core. No duplicate Git state machine, scheduler, or validation authority.
- **External tools**: prefer mature provider implementations with explicit fallback, measured benefits and version-pinned supply-chain review before adoption.

Out of scope: forced universal Nix/container/tmux stack; second CI runner/Task DAG; mandatory telemetry/service/database; GitHub account-based agent identity; automatically overwriting project manifests or lockfiles; auto-upgrading a running Task's pinned ADS standard; blind `--force` cleanup.

## 2. Source evidence and reuse choices

| Upstream or existing implementation | Existing useful capability | Decision for v4.13 | Boundary/fallback |
|---|---|---|---|
| [devkit](https://github.com/kaicreator-mm/devkit) (`main@3c0e2c7fada15b9bccc059182800bab84bc27564` reviewed) | bootstrap, Git bare mirrors, task worktrees, diagnostic/cleanup scripts, event gate | **ADAPT/HARDEN** safe native Git mirror/workspace and source checks | Do not directly port Windows paths, force cleanup or unconditional test-green |
| [mise](https://github.com/jdx/mise) / [configuration docs](https://github.com/jdx/mise/blob/main/docs/configuration.md) | global/system/project merged tool declarations, version management, env/tasks | **PREFERRED TOOLCHAIN PROVIDER**, subject to supported host, trust/provenance and compatibility | Organization Profile decides admissible version; mise only installs/selects it. Missing/unavailable provider can use explicit project-approved fallback; no fake success |
| [Worktrunk](https://github.com/max-sixty/worktrunk) | Git worktree switch/list/remove, hooks, CI/PR views, platform-dependent COW caches | **EVALUATE AS PREFERRED WORKTREE UX ADAPTER** | Native `git worktree` is mandatory minimal fallback. No native Worktrunk auto-merge/branch deletion or hook may bypass ADS Task/PR/Claim/Review authority |
| [workmux](https://github.com/raine/workmux) | worktree paired with tmux sessions, agent panes/dashboard | **OPTIONAL TERMINAL/UI ADAPTER** | Not required on Windows, PowerShell, Windows Terminal, zellij, headless or other agents |
| [Agent Skills specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx) | `SKILL.md` entry, on-demand scripts/references, progressive disclosure | **ADOPT SKILL PACKAGING** for instructions and recipes | A Skill invokes existing CLI and never directly becomes independent execution/check authority |
| [MCP Git reference](https://github.com/modelcontextprotocol/servers/tree/main/src/git) | sample Git tools and MCP transport patterns | **REFERENCE ONLY; OPTIONAL ADS MCP ADAPTER** after demonstrated consumer need | Reference servers are not production authority; use same core API with bounded path/permission and no independent state |
| [Dev Container CLI](https://github.com/devcontainers/cli), [DevPod](https://github.com/loft-sh/devpod), [devenv](https://github.com/cachix/devenv) / [Flox](https://github.com/flox/flox) | heavier reproducible/isolation/remote environments | **OPT-IN ENVIRONMENT PROVIDERS**, later if required by real project capability | Do not mandate Docker/Nix/SSH/remote infrastructure for simple TS/Python repos |

The table records **pattern/configuration research**, not approval to copy third-party source (H3), not installation validation and not upstream conformance PASS. Before using vendor code, bind immutable upstream SHA and verify applicable license/NOTICE, provenance, support and host compatibility. Prefer invoking tools rather than vendoring code.

## 3. Organization profile — declarative, not an executor

Proposed logical layers:

```text
Frozen project Product/L2 requirements + authoritative manifests/lockfiles
           |                          ADS pinned revision (immutable)
           v
Project .dev-standard/PROJECT_OVERRIDES / language-archetype selection
           |
           v
Organization Development Environment Profile (defaults, capabilities)
           |
           v
Host profile / local settings (path, proxy, credentials by reference only)
           |
           v
Resolved Environment Plan  ->  TOOLCHAIN_PROVIDER / WORKSPACE_PROVIDER
                                        |
                                  REAL PREFLIGHT/EXECUTION
```

**Authority rules**

1. Source profile and consumer ADS standard identity are explicit **immutable revisions**. Organization default changes do not mutate an active accepted Task/Claim or silently narrow the Project's declared compatibility.
2. The project dictates supported language/runtime **ranges**, canonical package manager and authoritative lockfiles. A project-selected exact development version overrides a compatible organization suggestion; the organization default may apply only where compatible. Neither can waive a declared required certification tuple.
3. The host reports available platform/filesystem/credentials/tool versions/caches, not new Product authority. Actual checked version, successful installation and executed test remain independent facts.
4. A project incompatibility returns `CONFLICT/BLOCKED` with an explainable resolution; do not silently upgrade project dependencies, regenerate locks or fabricate a matching runtime.
5. Machine-local secrets/proxy tokens are references/env injection, not committed to organizational profile; `mise.toml`/hooks/Skill code fetched from a repository are executable content and require the same bounded source/trust discipline as other commands.
6. Profile inheritance is **per-field for organization defaults**, not a blind deep merge of authoritative project contract; tooling must output source path/revision and precedence for every chosen value. `mise` has its own config merge behavior; it is an execution backend, **not** the ADS authority resolver.
7. New profile belongs to an **organization configuration axis**, separate from v4.3 `language | archetype` Profile kinds; any changes to generic Profile schema/catalog must be explicit prospective v4.13 delta, without redefining the v4.3 meanings.

**Minimal candidate config** (illustrative, exact tool versions are a separate organization Product decision):

```yaml
schema_version: 1
profile_id: org.kaicreator-mm.development
organization: kaicreator-mm
toolchains:
  node:
    provider: mise
    preferred: ORGANIZATION_APPROVED_NODE_VERSION
  python:
    provider: mise
    preferred: ORGANIZATION_APPROVED_PYTHON_VERSION
workspace:
  mirror_mode: shared-git-bare
  task_worktree_provider: worktrunk-or-native-git
  cleanup: explicit-lifecycle-and-recoverability
validation:
  policy: affected-first-final-candidate-closure
host_adapters: [windows, linux]
```

Implementation should split portable checked-in organization policy from machine-local config and any secrets. Place the generic optional schema under `schemas/`; a sample under `examples/organization/` or a clearly non-normative organization-config location. The exact current accepted organization values, repository manifest and storage path are Product/L2 decisions, **not** implicit standard requirements for every GitHub organization.

## 4. Toolkit modules and one CLI

```text
ADS monorepo
├── standards/                         # existing canonical owners unchanged
├── profiles/ + schemas/               # explicit ODEP discovery and minimal contracts
├── examples/organization/             # kaicreator-mm example; non-normative
├── toolkit/ads-dev/                    # CLI and shared domain functions
│   ├── profile-resolution
│   ├── toolchain-provider              # mise first, declared fallback
│   ├── workspace-provider              # Worktrunk preferred if compatible; Git native
│   ├── git-mirror-repository
│   ├── task-workspace-lifecycle
│   ├── validation-adapter              # project/CI authoritative commands
│   ├── conformance-adapter             # existing pinned ADS schemas only
│   └── host-adapters                   # Windows/Linux feature detection
├── skills/ads-development/             # SKILL.md -> CLI, no state duplication
└── integrations/mcp/                   # optional bounded wrapper, not v4.13 mandatory
```

Candidate user-facing commands (not committed syntax contracts until L2 Freeze):

| CLI | Responsibility | Preconditions/results |
|---|---|---|
| `ads dev env explain --repo PATH --json` | Read-only effective profile, source revisions and conflicts | Show project vs org vs host facts; no installation implied |
| `ads dev doctor --repo PATH` | Host tooling/filesystem/branch/lock/CI readiness | Real PASS/FAIL/UNKNOWN and remediation; no RELEASE PASS |
| `ads dev bootstrap --plan` / `--apply` | Idempotent minimum tools/runtime/workspace setup | No mass install by default, actual exit and rollback/retry state |
| `ads dev workspace ensure --repo REPO --task ID --base SHA` | Reuse or create correct task worktree | Exact approved integration source, safe branch/path and single-writer check; never guess `origin/main` |
| `ads dev workspace resume --repo REPO --task ID` | Continue previous Task after Agent handoff | Recover existing branch/worktree/current SHA rather than duplicate work |
| `ads dev workspace inspect` / `cleanup --plan` / `cleanup --apply` | Accurate state and safe resource lifecycle | Uncommitted source or uncertain ownership protected; never auto-delete evidence |
| `ads dev validate --scope affected|candidate` | Resolve project-selected checks, impact, remote/local placement and reuse | `NOT_RUN` or `NOT_APPLICABLE` != `PASS`; final candidate closure stays Release-owned |
| `ads dev conformance check` | Load schemas from project effective immutable ADS revision | Schema validity ≠ GitHub publish permission or Task authorization |

`#1119` proactive updater is a **separate opt-in project-adoption concern**; it may call the same resolver and GitHub client but must not be conflated with host Runtime updater or routine workspace cleanup.

## 5. Safe workspace state machine — without inventing a scheduler

Logical workflow of a single Task workspace:

```text
ABSENT -> PREPARED -> ACTIVE -> RETAINED -> CLEANUP_ELIGIBLE -> REMOVED
             |          |          |
           BLOCKED      RESUMABLE  RESUMABLE
```

This is a *local workspace resource lifecycle description*, **not a new ADS Work Item/Claim/Release state**. Existing GitHub task facts and local Git facts decide eligibility.

- **Create**: resolve Task/PR target integration branch and exact accepted base SHA, check mirror currency/offline handling and branch collisions; worktree provider is swappable.
- **Resume**: if same Task+branch+workspace matches, reuse, report material drift; do not reset/overwrite. After Agent context loss, recover from Git and durable Issue references without new task.
- **Inspect**: account for staged, unstaged, **untracked** files, local commits absent remotely, branch ahead/behind, linked Git worktrees, effective workspace root and object availability.
- **Cleanup**: default refuse source loss; preview writes, preserve any unpushed commits/unique data and external evidence; no blanket age-only `rm -rf`. If user explicitly requests destructive discard, use a distinct explicit option with hard root/path containment, recorded consequences and recoverability check. Do not add Owner credential approval gate.
- **Mirror**: preserve devkit bare mirror but avoid per-task redundant remote fetch; separate `observed cache age` from proven GitHub currentness. Offline cache is usable as pinned local object identity only when exact object exists; never claim live remote freshness.
- **Worktrunk boundary**: its `merge`, hook, cache management and `remove` are UX features; ADS wrapper disables/avoids side-effect operations unless existing GitHub/task policy permits the equivalent. Native Git fallback must pass identical safety checks.
- **Cache**: share immutable content-addressed downloads, Git objects and rebuildable artifacts; project environments and mutable `node_modules`/Python virtualenv remain isolated unless a version/provider/filesystem-safe strategy is actually proven. Worktrunk COW capabilities depend on host filesystem, not automatic on Windows NTFS.

## 6. Agent interface: Skill first, optional MCP later

Start with one `ads-development` Agent Skill that teaches *read current pinned standard → explain resolved config → create/resume worktree → run concerned check → record actual evidence → safe cleanup*. Use the [Agent Skills format](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx) and progressive discovery. Provide targeted reference docs for issue handoff, worktree recovery, toolchain debugging, validation reuse and GitHub interaction.

If actual consumers require structured tool invocation, add one thin `ads-dev-mcp` adapter over identical internal domain calls:

```text
env_explain (read-only)
workspace_inspect (read-only)
workspace_ensure (bounded local write)
workspace_resume (read-only or bounded restore)
validation_plan (read-only)
validation_run (executes project-allowed checks)
workspace_cleanup_plan (read-only)
workspace_cleanup_apply (explicit local action)
```

Never expose arbitrary shell, arbitrary filesystem root deletion, secret material, general branch force-push, Release approval or GitHub cross-repo broad write as a convenience MCP API. Use the actual host's existing privilege model; GitHub account is transport, not logical Agent identity. No dedicated server/daemon required for the CLI or Skill.

## 7. Validation cost and v4.12 residual integration

- **Per Task**: project-selected deterministic affected tests, negative oracle when materially needed, source diff review. CI automatically rerunning the exact same tests should not trigger redundant manual full local tests by default.
- **At final candidate**: one dependency-complete required regression/current-SHA applicability decision and executed checks; real required packaging/native/runtime/effect proof remains separately owned. `PR PASS != RELEASE PASS`.
- **ADS v4.13 standards + executable toolkit**: `SELF_COHERENCE` of standards/config/schema/examples; **actual** CLI/toolkit self-dogfood, including at least one real worktree lifecycle and relevant OS adapters. Preserve existing Release Standard owner and honest NOT_PROVEN.
- **After release**: independent real consumers provide bounded FIELD_VALIDATION feedback; do not force synchronized xDownload/runx/domain-harness releases as a release gate for ADS unless frozen Product specifically requires.
- **#1116 remaining issue**: only add the material missing cross-delivery-class/placement wording to existing Validation/Release standards; six elaborate distinct checkers are not required merely because six delivery types are named.
- **#1096 W1–W5 intake**: re-audit vs current v4.12 actual source, keep only deltas that materially unlock v4.13 Dev Environment or execution outcome. No new Project Steward process or Task Learning DB.

## 8. L1→L2 acceptance matrix (candidate; not actual executed tests)

| Case | Positive result | Counterexample / must refuse |
|---|---|---|
| E01 shared versions | Two compatible projects resolve same organization-approved runtime download | A project's incompatible Node or Python range silently overridden |
| E02 isolation | Independent Python venv, project lock and Worktree despite shared tool/runtime cache | Mutable `node_modules`/venv shared cross-project without proof |
| E03 repeat bootstrap | Running bootstrap twice on same host is idempotent and leaves a diagnosable inventory | Hardcoded proxy/Windows path/JDK ignored failure leads false green |
| E04 concurrent worktree | Two Agent Tasks use separate worktrees, exact approved bases and never overwrite source | Blind `origin/main` branch construction, collision, dirty forced delete |
| E05 resume | Interrupted Agent can resume existing Task without fresh clone/reinstall/branch | Session change considered an excuse to erase unpushed branch |
| E06 detached/offline | Cached exact Git object can support declared offline local operation | Offline cache is misreported as fresh GitHub remote state |
| E07 validation | A Python-only Task chooses Python checks, reports any unexecuted steps honestly | No `package.json` means `PASS` or pnpm/npm forced on wrong project |
| E08 CI cost | Actual identical test execution reused within original predicate/SHA/currentness scope | Duplicate local whole suite because remote automatic CI is Pending |
| E09 adapter fallback | Missing Worktrunk still works through safe native Git | No Worktrunk = project BLOCKED without genuine need |
| E10 Skill/MCP | Both call exact same CLI resolver, and no higher-level authority forged | MCP publishes or destroys workspace based on schema green alone |
| E11 updater separation | Opted-in #1119 project pin PR is source-bounded, verified, reversible | Dev env setup silently updates a frozen Task's ADS revision |
| E12 provenance | Tools are invoked as external dependencies with pinned accepted version, copied code reviewed for rights | Public source treated as carte blanche to vendor without license/NOTICE |

Test minimum representative environments: Windows native workspace and Linux/Ubuntu host for **actual code shipped for those platforms**, source-only focused checks before one version closure, fallback tested where Worktrunk/mise is unavailable. Record actual `PASS/FAIL/NOT_RUN/BLOCKED/N/A`; no fabricated platform certification.

## 9. Proposed bounded execution concerns, **not the executable DAG yet**

- **D01 — L1 source-gap / Product**: compare devkit and named tools against current qualified ADS and #1147, #1119, #1116; settle P0 value and exact provenance/licensing without new per-tool Issue.
- **D02 — ODEP + resolution**: minimal org profile, precedence checker, project/host exceptions and deterministic positive/negative fixtures.
- **D03 — Toolkit Bootstrap + Git Workspace**: implement provider adapters and safe mirror, create/resume/inspect/cleanup with Windows/Linux preflight; native Git fallback mandatory.
- **D04 — Validation/Conformance + Skill**: bind existing project commands and ADS pin, real exit/skip and validation budget; minimal Agent Skill. MCP only if a consumer use case is evidenced.
- **D05 — #1119 project updater**: scoped opt-in GitHub PR execution & rollback, separately reviewable write concern; reuse v4.12 read-only resolver.
- **D06 — residual normative delta**: include #1116 and only proven W1–W5 gaps, ideally coalesce if no independent code/owner boundary.
- **Existing Release closure**: one immutable candidate proof and qualified main/tag handling; real project post-release feedback does not silently block.

No estimated performance or cost saving is asserted without baseline measurement. Exit this design stage by Product-approved FR/AC, L2 exact module contract decisions and the smallest legitimate Task DAG/Task Packs; this planning file is not any of those freezes.

## 10. Remaining bounded L2 decisions / stop rules

1. Benchmark **mise vs existing fnm/py managers** for Windows native + Ubuntu, version resolution, auth/proxy/offline, reproducibility and compatibility; if mise adds real cost/unsupported behaviors, use fallback and record why.
2. Run a tiny **Worktrunk + existing mirror + two Tasks** pilot: verify origin fetch/push URL, exact Task base, status, safe cleanup, Windows `git-wt`/Terminal naming and Ubuntu operation. Decide default provider only from real observations; native Git works regardless.
3. Test filesystem cache strategy on NTFS vs actual Ubuntu filesystem. **Do not** assume Worktrunk's COW cache applies to either host without proof; caching must not compromise isolation.
4. Keep MCP **conditional**, not a mandatory server: ship Skill+CLI first, add transport only on actual Agent/client demand.
5. Scope profile and v4.12 residual versions to immutable qualified predecessor; avoid rewriting legacy v4.3 profile semantics or duplicating #1119 Class A read-only selector.

### Useful source links

- ADS authoritative predecessor sources: `standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md`, `standards/WORKSPACE_ARTIFACT_STANDARD.md`, `standards/GIT_EXECUTION_STANDARD.md`, `standards/VALIDATION_STANDARD.md`, `standards/PROJECT_ADOPTION.md`.
- Product sources: [#1147](https://github.com/kaicreator-mm/ai-development-standard/issues/1147), [#1119](https://github.com/kaicreator-mm/ai-development-standard/issues/1119), [#1116](https://github.com/kaicreator-mm/ai-development-standard/issues/1116).
- Upstream evidence: [mise configuration](https://github.com/jdx/mise/blob/main/docs/configuration.md), [Worktrunk](https://github.com/max-sixty/worktrunk), [workmux](https://github.com/raine/workmux), [Agent Skills](https://github.com/agentskills/agentskills), [MCP Git reference](https://github.com/modelcontextprotocol/servers/tree/main/src/git).
