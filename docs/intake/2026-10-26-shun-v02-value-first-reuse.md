# Practice intake: Shun Assistant v0.2 — user value, dependency slicing, and reuse before new mechanisms

**Status:** prospective ADS practice evidence; not a normative amendment to the released v4.18 baseline and **not** a waiver of any frozen project's safety/release criteria.  
**Sources:** [ADS #1337](https://github.com/kaicreator-mm/ai-development-standard/issues/1337) (xDownload precedent); [ADS #1241](https://github.com/kaicreator-mm/ai-development-standard/issues/1241) (Web-first); [Shun T07 #109](https://github.com/kaicreator-mm/shun-assistant/issues/109); [Shun T08 #110](https://github.com/kaicreator-mm/shun-assistant/issues/110); [kai-tools #1](https://github.com/kaicreator-mm/kai-tools/issues/1).

## Evidence / failure mode

On 2026-10-25/26, Shun Assistant T07 produced nine scoped PRs #179–#187 (eight merged, one under review at observation); the frozen 11-node implementation Task DAG stayed at **6 closed / 11 total**. The work implemented real Win32 file operations and durable safeguards, but **no additional installed, user-operable critical journey was proven**. Rounds F04A, F04B1, F04B2, F04B3a and proposed F04B3b consumed multiple PRs, two CI lanes and review cycles around reconstructing exceptional recovery state. At the same time, T08 Control API/UI and DeepSeek cloud opt-in, T09 portable packaging, T10 integration and T11 release remained blocked.

The frozen DAG mandates `T07→T08→T09→T10→T11`: an incomplete file-mutation crash-phase matrix blocked independent Cloud/UI and packaging work. This is a **dependency modeling error as well as risk/scope proportionality error**. Source PRs and tests are real engineering artifacts but cannot be reported as shipped journeys. A frozen dependency cannot be bypassed by an implementation agent; an authorized prospective Product/L2/DAG revision is needed.

**Causality:** not ADS #1241's Web-first principle alone; Product/L2 scope, overly coarse task decomposition, pre-implementation library selection, and controller behavior jointly optimized internal assurance over product delivery. Agents failed to escalate the imbalance despite repeated zero-Issue-close cycles.

## Normative-update candidates (require ADS owner disposition, not automatic new global gates)

1. **User-critical-journey-first L1/L2 planning:** identify the smallest supported user gesture → trusted approval (when applicable) → real operation → truthful terminal → install/run path. For each prospective infrastructure task state which missing edge it closes and its impact. Report `shipped_journeys` and `Issue/DAG progress` separately, with `NOT_PROVEN` rather than fake PASS.
2. **Build-vs-reuse choice before substantial custom OS/protocol code:** explicitly compare standard OS/Node/Rust/SQLite capabilities, established libraries, and **safe refusal/manual recovery** against bespoke abstractions. For Shun: Node `fs.copyFile(COPYFILE_EXCL)`, Win32 `CopyFile2`/`IFileOperation`/`MoveFileExW`, Rust capability-scoped filesystem libraries (evaluate Windows semantics), and native SQLite WAL transactions. None is a blanket substitute for Shun-specific authorization, reparse constraints or no-overwrite guarantees. Select by demonstrated feature/threat gap; prove a representative supported path before expansion.
3. **Risk-proportionate failure contract:** keep genuine safety boundaries: user consent, no unauthorized file effects, no wrong-target, no unintended overwrite, no false terminal success, no secret leakage. On unprovable crash state use `UNKNOWN` and no automatic replay, with user intervention if appropriate. Distinguish **safe unavailable/unsupported** from **must infer exactly what happened**. Multi-phase fault-injection matrices should follow actual supported journeys/threat, not be manufactured as universal release blockers.
4. **Task DAG uses lanes + subrequirements, not only a stage chain:** do not make all product/UI/packaging work depend on completing one unrelated rare-condition subtask. Model `Contract→Core→Integration→Validation` within **independent feature lanes**, including a real join gate at shared contracts/integration. Validate dependencies at the **minimum interface/artifact granularity**. Cross-lane work on disjoint write sets can begin after its true prerequisites. Preserve atomic review, version-branch and authority boundaries. Changes to frozen DAGs require approved Product/L2/DAG amendment, not stealth dispatch.
5. **Prevent anti-gold-plating by review of value, not a retry counter:** after repeated source PRs/green CI with no journey completion, stop new subtask proliferation; inspect whether the changed code is reachable from installed product and whether a library or conservative fallback suffices. Controller chooses `SHIP_MINIMAL_SUPPORTED`, `REUSE_DEPENDENCY`, `DEFER_EDGE`, `ACCEPT_KNOWN_LIMITATION`, `REQUIRE_SECURITY_FIX`, `REQUEST_PRODUCT_AMENDMENT`. Track lost critical-path time. Do not downgrade required P0/P1 or frozen checks to PASS/waived just for speed.
6. **Library extraction is not a sunk-cost rescue:** do not automatically move project-specific code to `kai-tools` to justify past effort. First identify stable platform-neutral contract/Win32 platform boundary, an independent concrete second consumer, dependency/license/ABI/maintenance cost, and comparison to maintained alternatives. Extract a cohesive minimal module only if net reduction in duplicated code or risk is demonstrated. No project release may depend on the optional extraction.
7. **Practical capacity heuristic:** favor delivered journey work over exploratory edge hardening; 70/20/10 (vertical delivery / assurance / edge) is illustrative only, not a mandatory schedule or CI schema.

## Shun v0.2 prospective correction example

- **Minimum user-facing journey:** Windows Standard User launches portable Core → explicit cloud opt-in → DeepSeek Flash diagnosis → plan preview and authenticated UI gesture where R2 effect applies → execute narrow supported operation → show verified/UNKNOWN receipt → save/reuse Recipe.
- **Independent lanes:** (A) Control API/UI, model posture, consent; (B) supported file operations with safety essentials and `UNKNOWN/no-auto-replay`; (C) portable Windows packager/startup. Align at a reviewed contract and final integration/RQ join. Do **not** retrospectively declare frozen T08/T09 prerequisites fulfilled.
- **Safety must remain:** use of local file APIs or libraries does not itself establish Shun's R2 grant, currentness, path authority, destination collision, or durable replay behavior. The change is to avoid unwarranted *positive* causal reconstruction, not to remove permission checks.
- **Example risk disposition:** unreadable post-crash destination → UNKNOWN/manual reconcile and no repeat; exact third-party move causality need not be proven **unless** a frozen acceptance criterion explicitly demands it. Product/Architecture must approve any revised criterion.
- **Decision ledger:** preserve source code and test evidence already proven, remove from critical path only by authorized change, benchmark maintained alternatives in a bounded branch; no rewrite-for-rewrite and no automatic kai-tools dependency.

## Owner/acceptance handoff

- Product/L1: define supported users, operating conditions, accepted safe-failure UX, real shipped journeys, and accepted limitations.
- L2: choose reuse or custom implementation based on concrete threat exposure; reconcile authorized safety boundaries and release criteria.
- DAG/Scaffold: amend only unjustified cross-lane predecessor edges, keep true integration join and resources/agent fit.
- Implementation/Controller: monitor delivered journeys, exact-SHA review, CI evidence reuse, stop unnecessary subtask cascades; route local-only physical tests to a single scoped Host lane.
- Kai-tools: separately assess extraction; no dependency inversion on a product release.
- ADS owner: decide what parts belong prospectively in Development Workflow/Task Decomposition/Implementation Quality. **This intake doc creates no new universal mandatory artifact and does not change v4.18 normative rules.**

## Outcome metrics for the next Shun review

```ini
AT_OBSERVATION_SHUN_DAG_CLOSED=6/11
USER_OPERABLE_NEW_V02_JOURNEY=NOT_PROVEN
PR_ACTIVITY=9_T07_PRS_2026-10-25_TO_26
REQUIRED_NEXT_DECISION=PRODUCT_L2_DAG_PROSPECTIVE_AMENDMENT
KAI_TOOLS_EXTRACTION=OPTIONAL_NONBLOCKING
FROZEN_RELEASE_GATES=UNCHANGED_UNTIL_AUTHORIZED_AMENDMENT
```
