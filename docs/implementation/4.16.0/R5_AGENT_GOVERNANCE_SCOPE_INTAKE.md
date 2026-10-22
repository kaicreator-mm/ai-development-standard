# ADS v4.16.0 — R5 Agent Management / Delegation Scope Addition (Product Intake)

**Status:** `PRE_FREEZE_SCOPE_EXPANSION / NOT_FROZEN / INDEPENDENT_REVIEW_NOT_RUN / NO_BUILDER_CLAIM`.  
**Parent:** [#1261](https://github.com/kaicreator-mm/ai-development-standard/issues/1261) · [planning PR #1262](https://github.com/kaicreator-mm/ai-development-standard/pull/1262).  
**Existing R4 current foundation:** [R4_PRODUCT_L2_REPAIR.md](R4_PRODUCT_L2_REPAIR.md), including six bounded concerns and **unresolved** independent R3 findings P1-02/03/P2-01/02/03. Nothing here asserts that R4 Review passed or these findings are fixed.

## 1. Disposition of the remaining open Issue families

### INCLUDE in v4.16 Product candidate — independent Concern G, not folded into Report v5

| Issue | Disposition | Actual standards task to consider | Excluded implementation |
| --- | --- | --- | --- |
| [#1199](https://github.com/kaicreator-mm/ai-development-standard/issues/1199) | INCLUDE AS UMBRELLA / NO DUPLICATE TASK | Normative Agent profile/selection/delegation architecture and interfaces, owner crosswalk and one end-to-end evidence-only flow | ADS agent service/registry, Tally worker scheduler, new DomainHarness Kernel, second Issue/Claim authority |
| [#1200](https://github.com/kaicreator-mm/ai-development-standard/issues/1200) | INCLUDE SCOPED PRODUCT+L2 | Immutable per-Task effective Agent/Role/Profile/Tool/Host capability selection snapshot: self-declared profile claim vs independently observed capability, exact Agent/session/source/ADS revision, environment constraints, expiry/revocation/missing evidence, role and currentness, safe fallback and handoff | Capability matching algorithm, live provider auth, model router, provider/Host provisioning, GitHub login as Agent identity |
| [#1201](https://github.com/kaicreator-mm/ai-development-standard/issues/1201) | INCLUDE SCOPED PRODUCT+L2 | Delegated Agent/session and Tool-call causal evidence: parent/child refs tied to accepted Task/Claim and immutable selection, tool intent vs accepted dispatch vs remote ACK/RUNNING vs independently observed terminal effect, duplicate/retry/lost response/timeout and safe UNKNOWN, explicit caller/child authority boundary | Universal Tool RPC, private chat event bus, DomainHarness K permission, automatic external effect retry, alternate Task state model |

**Existing normative source owners (read before any schema mutation):**
- `schemas/agent-capability-profile-v1.schema.json` blob `ed5095898558df3d5ce83ec927a243a06b58ab32` (provider-neutral *claims*, not proof), `schemas/agent-capability-evidence-v1.schema.json` blob `64c19e0a9a1d529a03cb7aef3282806a0953d341` (historical exact-subject evidence), `schemas/role-execution-profile-v1.schema.json` blob `df96fb14dce9f39c753c80483e21c55b27beb685`.
- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` blob `67516c36f4d202123224b1c2054419aa913b872d` §5 (GitHub transport is not logical Agent identity), §9 and §10; `standards/EXECUTION_ARCHITECTURE_STANDARD.md` blob `1f1601a20db08d263955241607dfd08d8b8f77e1` §2/§8/§11 (unique Claim, durable admission/effect boundary), `LOCAL_AGENT_HANDOFF_PROTOCOL.md`, `EXECUTION_PACK_STANDARD.md`.
- Do not reimplement fields or mint new canonical event kinds where existing exact-source Profile/Evidence/Role/Handoff fields and refs are sufficient. If new published machine projection is necessary, independently review schema compatibility and ownership, and decide whether that data belongs in Task/Execution Pack vs optional report-only v5; Agent declaration is not proof of real model/provider identity.

**Minimal verified-normative connection to existing six R4 groups:**
- #1241 Plan-first/Web-first consumes **observed available capabilities** and exact current Task selection: Web may author what its actual connected tools permit, Local required only for remaining physical/permission work; no automatic delegation from textual `capability=true`.
- #1258 Report v5 binds producer/Attempt/physical call to **actual observed** model/provider and Task role/profile snapshot when source-qualified; do not treat private runtime profile as a public cost authority.
- #1198/#1206 and existing Evolution §8 use capability/environment provenance to bound applicability, negative cases and optional experiment comparators; no self-selection of a new model based on one successful synthetic probe.
- External Tally owns actual selection/dispatch implementation; task-meta owns capture/private Trace; DomainHarness K owns Business effect; ADS defines only stable cross-app evidence and safety conditions.

### INCLUDE only as practice/conformance evidence, not feature owners

- [#1173](https://github.com/kaicreator-mm/ai-development-standard/issues/1173): optional parent outcome / child execution planning, evidence×environment matrix; no mandatory child Issue fan-out.
- [#1239](https://github.com/kaicreator-mm/ai-development-standard/issues/1239): recovery/repair-vs-rebuild and bounded source-currentness Review; no invented cost savings.
- [#1240](https://github.com/kaicreator-mm/ai-development-standard/issues/1240): real native Host capability preflight and target checks; don't treat esbuild/Vitest as Node native startup.
- [#1255](https://github.com/kaicreator-mm/ai-development-standard/issues/1255): threat-model negative class vs single regex witness; no new universal security gate.
- [#1204](https://github.com/kaicreator-mm/ai-development-standard/issues/1204): optional independent **docs-only P2** small concern for historical audit snapshot and Markdown render, not a prerequisite to Report v5 or Agent management.

### DO NOT add to the v4.16 *standards-source* feature DAG

- [#1205](https://github.com/kaicreator-mm/ai-development-standard/issues/1205), [#1208](https://github.com/kaicreator-mm/ai-development-standard/issues/1208), [#1209](https://github.com/kaicreator-mm/ai-development-standard/issues/1209): v4.15 source-normalized baseline **already covered in material part**, exact source/owner closeout required; no duplicate GitHub envelope implementation. Deferred real products separately #1210.
- [#1210](https://github.com/kaicreator-mm/ai-development-standard/issues/1210), [#1231](https://github.com/kaicreator-mm/ai-development-standard/issues/1231): **actual runtime** task-meta/Tally/controller/Host integration with independent credentials and effects remains NOT_RUN, later external Product/Host proof and *not mandatory merely to validate a normative spec*.
- [#1207](https://github.com/kaicreator-mm/ai-development-standard/issues/1207) + version PR #1211: v4.15 QUALIFICATION=CONDITIONAL, main unmerged, requires original Release authority and main integration ordering; cannot claim v4.16 main release or retroactively rewrite v4.15.
- [#1229](https://github.com/kaicreator-mm/ai-development-standard/issues/1229) / stale PR #1230: prior source/runtime boundary and manual admission governance; reconcile against already integrated v4.15 #1233 §11.7A and close/supersede only if byte/source-equivalence confirmed. Not a new Agent management schema concern.

## 2. Focused Plan-first and explicit admission/refusal examples (NEW planned A01–A08)

| Case | Input / bounded evidence | Expected governing action | Forbidden inference |
| --- | --- | --- | --- |
| A01 | Two independent Agent sessions share one GitHub transport login but have different declared operator/session IDs | Distinguishable *claims*; actual permissions/role/independence require source-qualified evidence | transport login = operator identity or distinct account = independent Review |
| A02 | Agent capability profile says `can_run_linux:true` but no real runner/Host capability evidence | task capability UNKNOWN/UNSATISFIED; bounded Web/CI/Local alternative with actual check | self-declared capability → real Linux PASS |
| A03 | Effective Task pin cites Agent profile P1; producer publishes P2 after Task Claim | Task stays on P1 until authorized source-bound selection change; P2 not auto-upgrade | latest profile wins, presumed model selection |
| A04 | Planner delegates work to child Builder with parent Task but child lacks required tool authorization | child operation refused; parent/child causal refs retained; no permission widening | parent Task Claim makes child Tool/DomainHarness effect permitted |
| A05 | Remote Tool accepted effect and only ACK/STARTED returned, later response lost | hold/UNKNOWN; reconcile provider-side receipt; never blind duplicate non-idempotent action | ACK = terminal business effect or retry is safe |
| A06 | Web completes source/schema/CI evidence, physical Host check still not run | only physical remaining Local dispatch; no second protected Writer; own Review independent | all Task needs Local, CI PASS substitutes physical truth |
| A07 | Agent/Skill/Tool effective profile mismatch vs Task risk or source/currentness | typed INELIGIBLE/UNKNOWN and evidence handoff, not dynamic privilege escalation | auto choose latest/cheapest by prose |
| A08 | Same Task selected Agent/Tool path reports success, but independent verifier fails semantic effect | strict Task Gate not PASS; Task Learning/Evolution may carry negative candidate | Agent self-report or observed token value makes Domain Package qualified |

All above are **planned normative source-only conformance inputs**, not real Agent/Host tests or new implemented Event schemas. Reviewer must identify which are already covered vs missing. At most one narrowly scoped Agent-selection/delegation implementation concern after owner Product/L2 agreement; independent source Review still required. Avoid a second review loop for individual test cases.

## 3. Version / exact-SHA / workflow status

- **Retain ADS v4.16.0 MINOR** and candidate opt-in Report wire `ads/github/v5`; current R4 P1-02/03 + P2 issues remain unresolved until independent re-review. Adding #1199–#1201 does not itself repair them.
- **One Product/L2 planning subject, implementation by concerns**: A–F in R4 plus optional G (Agent management normative), and small independent doc P2 if justified. Product review should judge whether agent concern G can be assessed in a bounded R5 round without slowing A core; if no actual normative gap remains, close G as `ALREADY_COVERED/IMPLEMENTATION_ONLY` and hand back to Tally.
- **No scope Freeze yet.** Exact R4 #1262 head `fdf2b15f3b3ae34a0e50e9f2ff85cc9c621d1c03` is historical once this R5 doc is added. A fresh independent Review must pin the new HEAD; earlier R3 verdict remains negative source evidence, not an approved result on the successor.
