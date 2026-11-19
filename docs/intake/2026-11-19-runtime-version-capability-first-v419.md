# ADS v4.19 Product/L2 Intake — Capability-Based Runtime and Toolchain Version Selection

> **Status:** PRODUCT_INTAKE_ONLY / PROSPECTIVE_V4.19 / NOT_FROZEN / NOT_NORMATIVE_YET  
> **Owner direction:** all projects and future tasks; avoid unnecessary mandatory Node 24 (or analogous toolchain version) when the actual task does not require it.  
> **Authority:** [ADS #1359 — Delivery-First](https://github.com/kaicreator-mm/ai-development-standard/issues/1359); [ADS #1347 — v4.19 intake index](https://github.com/kaicreator-mm/ai-development-standard/issues/1347).  
> **Illustrative dogfood:** [DIE #2](https://github.com/kaicreator-mm/domain-intelligence-engineering/issues/2), Forge [#213](https://github.com/kaicreator-mm/domain-forge/issues/213) / [#214](https://github.com/kaicreator-mm/domain-forge/issues/214); not a rewrite of those projects' Product/Task authority.

## 1. Problem and product outcome

An executor may be told `Node >=24` by a stale prompt, inherited workflow template, unrelated test/runner, or an overly broad global default even when the selected changed source, dependencies and relevant tests run correctly on an earlier compatible runtime. The resulting environment switch, local handoff, blocked CI, version migration or repeated tests spend time without increasing evidence quality. Equivalent mistakes occur with Python, Java/JDK, Go, Rust, .NET, compilers, SDKs, operating systems and deployment targets.

**Outcome:** Choose the least restrictive **actually justified and evidenced** runtime/toolchain version for the selected work, while honoring all *currently binding* project and consumer compatibility contracts. Version selection serves the Task's outcome, not a blanket global major-version preference.

## 2. Proposed cross-project rule (prospective ADS v4.19 candidate)

1. **Capability and contract first.** A Task MUST NOT introduce an arbitrary mandatory runtime major (for example, `Node >=24`) merely because a template, past project, default Agent instruction or older receipt used it. Name the actual required language/API feature, supported dependency and package engine, build/test/CI/host/deployment interface, security/support baseline, or binding Product/L2/Release compatibility contract that justifies each minimum. This is general to toolchains, not specific to Node.
2. **Scope the claim.** Distinguish an isolated script/module's verified runtime compatibility from the **monorepo/workspace** build, package manager, install, product distribution, CI and release support matrix. A standalone JavaScript test that passes on Node 22 is not evidence that an entire `engines.node >=24` repository is supported on 22.
3. **Evidence, not assumption.** Use the executable already available when it is consistent with the selected supported contract; record the actual `node -v` (or equivalent), exact commit, selected input/output and relevant exit statuses, and execute the narrow affected tests. A tested version is a *verified compatible version in that scope*; do not assert it is the universal **minimum** without evaluating lower candidates. Missing runtime/host facts remain NOT_RUN/UNKNOWN, never inferred PASS.
4. **Existing gates remain binding until changed lawfully.** If a project actually declares `engines.node >=24`, a CI workflow explicitly enforces 24, a dependency requires it, or Product/Release has selected it, the executor MUST honor that gate for the affected operation unless the competent owning Writer performs a source-scoped compatibility downgrade and the changed contract is independently reviewed/validated as required. Editing an Issue, prompt, Task DAG, or a separate isolated script does NOT silently waive an unchanged root engine, CI, frozen task or release floor.
5. **No ritualistic environment upgrades or extra proof.** If there is no genuine Node24-only API, dependency/engine minimum, host contract or supported release reason, a new scoped Task SHOULD NOT force Node24 merely to create a local-agent dependency. Do not mandate exhaustive version matrices, repeat unchanged PASS receipts, reconfigure a whole workspace or add a new Gate solely for this principle. Test only material runtime and platform risks proportional to the actual supported claim; formal support for a range requires evidence appropriate to that range.
6. **Security and supported lifespan still matter.** EOL, vulnerable or unsupported runtimes cannot be preferred *solely* for convenience when a current binding security/product policy makes them unacceptable; name that real policy or vulnerability rather than pretending a newer syntax feature is needed. A project's documented support decision may legitimately exceed the lowest syntactically capable runtime.
7. **Version-change impact must be explicit.** If reducing a declared minimum would alter package manager installs, lockfiles, transitive dependencies, dynamic imports, native addons, compiler targets, deploy/runtime images, CI or consumers, do a smallest lawful impact analysis and change only the actual owning files; review, CI and release criteria remain as independently owned. Do not retroactively reinterpret earlier exact-SHA receipts.

### Suggested compact execution evidence (not a new schema or mandatory lifecycle)

`SELECTED_RUNTIME=<name/version>; SCOPE=<script|package|workspace|host>; CONSTRAINT_SOURCE=<path/ref or none>; FEATURE_OR_DEPENDENCY_NEED=<specific evidence or none>; TESTED_ACTUAL=<commands/exits/exact SHA>; REMAINING_GATES=<specific unresolved contractual checks>`.

Use existing Task Pack / Execution / Validation receipt fields when present. The compact line above is optional prose for transparency; do not create another Registry, status enum, Scheduler, Agent Claim or artificial Review step.

## 3. Decision examples and falsifiers

| Situation | Correct handling | Must not claim |
| --- | --- | --- |
| New isolated Node script uses features supported by the selected runtime, no scoped 24-only dependency; real affected tests pass on existing Node 22 | Accept **scoped script/test evidence** under that actual version; avoid needless handoff to Node24; retain unmet workspace/host gates | Entire repository supports Node22 or release qualification is done |
| Forge root `package.json` declares `engines.node >=24.0.0`; existing Woodpecker script rejects `<24` | Honor those original install/full CI gates, or undertake a separately reviewed compatibility policy/source change | Task Issue text removing 'Node24 required' nullified the root/CI gates |
| Actual native API/dependency/tooling only works on Node24 | Require Node24 for the *affected* execution, with path/feature/engine evidence | Node22 validation covers a Node24-only feature |
| Legacy prompt says 'must use Node24' but relevant code/tests need only a compatible supported earlier runtime | Remove the ungrounded mandate from future prompts/Task scope; run actual affected validation | A new Node24-only agent transfer is automatically necessary |
| Only an absent or unrelated private-source positive was SKIPPED in CI | Keep real-source positive NOT_RUN, regardless of chosen Node version | A green negative-only CI means real-source POS passed |
| A previous SHA passed on Node24, new SHA only changes docs and no runtime-affecting inputs | Reuse evidence only where provenance and impact permit; do not repeat just to test the same major | Old receipt is magically at new SHA or proves incompatible lower runtime support |
| Runtime is end-of-life or the product has a real current supported-runtime baseline | State the actual security/support requirement; keep affected floor pending authorized change | Lower syntax requirements override supported-product/security policy |

## 4. ADS ownership, acceptance and integration

- Product/L2 owner: ADS [#1359](https://github.com/kaicreator-mm/ai-development-standard/issues/1359) as a Delivery-First **Capability First + Proportionate Assurance** delta; v4.19 intake pointer [#1347](https://github.com/kaicreator-mm/ai-development-standard/issues/1347).
- Normative integration targets **after prospective Product/L2/DAG authorization**: existing `standards/DEVELOPMENT_WORKFLOW.md` environment/capability section and, only if required, existing `standards/EXECUTION_PACK_STANDARD.md` toolchain evidence phrasing. Avoid concurrent edits to these files while [integrated preview PR #1365](https://github.com/kaicreator-mm/ai-development-standard/pull/1365) owns their overlapping v4.19 composition; a single authorized Integrator incorporates the reviewed delta.
- Proposed acceptance: one positive case where a task correctly uses a verified compatible earlier runtime without a fake Node24 block; one negative where root `engines/CI` truly mandates Node24, and a lower-version isolated script must **not** be promoted to workspace or release PASS; one negative where a genuine Node24-only feature requires 24; one UNKNOWN when environment/support metadata are absent. Ensure evidence is attached to exact source and avoid self-declared expected-vs-expected fake passes.
- This candidate does not freeze v4.19, change published v4.18, edit product repositories, invalidate existing CI, reduce a binding security floor or grant a new Review/Release waiver. Real normative adoption follows the existing ADS Product→L2→Task DAG→exact-source review→integration/Closure authority, rather than a special new Gate.

**Design intent:** *Require the runtime that the actual supported work needs—not the runtime that a template happens to mention.*
