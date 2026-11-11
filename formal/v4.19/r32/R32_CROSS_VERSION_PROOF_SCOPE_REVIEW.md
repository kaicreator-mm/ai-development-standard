# R32 — Baseline-stable Claim semantics vs prospective v4.19 execution-profile delta

**OUTPUT_LABEL:** `ADS_1366_R32_BASELINE_CORE_VS_PROSPECTIVE_DELTA`  
**ADS #1366**, 2026-11-11. **Execution type:** source-first exact Git object comparison and structured Schema static checks, **not** native CAS, SMT, Python, live Host operation or new independent review.

## 1. What R31's blanket version gate missed

R31 correctly refused to treat `kaicreator-mm/tally/main@e988321439f65b55936a691c02250b6d62a29409` (pin ADS **4.18.0** @ `2c395c55569fe2edf3f4135f12d3d069e526d0b7`) as an authorized **v4.19** consumer. But that does **not** mean its legitimate v4.18 source/Host evidence is useless until PR #1365 is frozen. A rule can be unchanged across versions without rewriting the owning subject's authority.

I compared immutable v4.18 exact SHA `2c395c55569fe2edf3f4135f12d3d069e526d0b7` to prospective PR #1365 exact SHA `dac263fa4c0ab155406d2f2117459b34322cc988`, using direct GitHub Git blobs and source lines, not a model's unverified Boolean assertion.

| Source | Baseline blob → Candidate blob | Exact changed scope | Authority meaning |
| --- | --- | --- | --- |
| `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | `1f1601a20d…` → **same blob** | Zero changes across all 1418 lines | §11.1/11.1.1 Claim serialization and derived key, reservation/current generation, atomic rejection, recovery remain text-identical |
| `standards/GIT_EXECUTION_STANDARD.md` | `23568a9a28…` → **same blob** | Zero changes | Existing Git write authority/ownership baseline unchanged |
| `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` | `49ecd802c5…` → `935a905d59…` | **Only line 573** changes, describing new execution profiles | §8.5 accepted Claim as Start Record, source admission and event writer core remain text-identical; older v4.18 Task policy explicitly retained |
| `standards/EXECUTION_PACK_STANDARD.md` | `c7bd2e4ffb…` → `1bd8631dd7…` | **Only line 148** changes, describing new execution profiles | Task authority not silently migrated; profile chooses execution *context*, not role authority |
| `standards/TASK_DECOMPOSITION_STANDARD.md` | `b7ffab0b94…` → `13ded16f7c…` | Adds §13.1, 10 lines of feasibility/shared-write ownership/coordination-cost guidance | This is *new candidate* planning guidance, not retrospective v4.18 freeze |
| `schemas/dispatch.schema.json` | `90bea62524…` → `5d9233b881…` | Adds profiles `WEB_BUILDER`, `LOCAL_VALIDATION` and role guards | New values valid in candidate schema only; cannot be used to bypass an effective v4.18 pin |
| `scripts/v34_rules.py` | `ad55439de0…` → `0829be09f4…` | Profile environment mapping changes (not asserted identical overall) | Do not infer current authorization from a profile→WEB/LOCAL projection |

Structured candidate `dispatch.schema.json` readback confirms `WEB_BUILDER→builder`, `LOCAL_VALIDATION→validator`, `WEB_REVIEWER→reviewer`, while the original five profiles remain enumerated. The source comparison and static assertions actually executed in the Web code environment: **14/14 PASS**; see exact IDs and raw blob SHA in [R32 machine receipt](R32_CROSS_VERSION_OBLIGATION_PARTITION.json). This checks declared schema predicates and text, **not full AJV/jsonschema evaluation, runtime enforcement or semantic equivalence**.

## 2. Refined execution lanes

**Lane A — existing effective v4.18 baseline core:** Subject is the authorized owner of an actual v4.18 Task (for example Tally Issue #125's owning workflow), not a synthetic upgrade. May re-use its Host SQLite CAS and Native GitHub source code to examine *unchanged* Claim Key, serialization, event/readback and current Task authority evidence. Its actual implementation tests and source must be bound to the v4.18 pin and correct Task. Even if a real v4.18 accepted Claim and CAS proof appears, it closes only the specified **baseline-rule** evidence, **not** a v4.19 adoption proof. The current Tally Host source explicitly limits itself to initial generation 1 and default group; the Host's physical CAS row has not been independently reread here; historical native Claim comments are directly observed in §5.

**Lane B — prospective v4.19 delta:** `WEB_BUILDER` versus `LOCAL_VALIDATION` role, profile/environment mapping, actual cost-based selection and Task DAG feasibility/ownership additions are candidate-only until effective Product/L2/Task approval and adoption. Existing R23 schema/role review and R26 crosswalk should be **reused**, not reimplemented. No selected valid v4.19 publisher has been proven; PR #1365 remains OPEN, Product #1347 NOT_FROZEN.

The two lanes cannot exchange source authority or receipt identity. Stable source text makes a bounded **reuse opportunity**, not proof that any project's accepted Claim/CAS or Task Pack semantics are true at runtime. It also does not certify all source-to-model equivalence: `v34_rules.py`, `dispatch.schema.json` and planning guidance do change.

## 3. Impact on R30 P2 and acceptance

- **R30-P2-01, Key/Generation**: baseline code/authority can be checked under *the real v4.18 Task* without waiting for v4.19 publication. Existing Tally source is candidate evidence, **real current accepted Host CAS is not demonstrated**.
- **R30-P2-02, Writer**: requires the authoritative frozen Task Pack write-set, actual simultaneous writer attempts and mutation provenance. Two non-overlapping Git revisions or separate Claim Keys are not sufficient.
- **R30-P2-03, Start/Grant**: requires an accepted durable Claim, current grant scoped to source authority and terminal/resource publication reconciliation. Tally default group and Gen1 do **not** discharge future nondefault group/successor duties.

All three P2 evidence gaps remain open; **0 confirmed ADS normative defects**; no new model, Runner test or solver execution is needed at this point. Do not request unrelated Owner approval or mutate external Tally Issue #125 from the ADS formal experiment.

## 4. Delivery-First next action

Reuse R29's 97/97 Python and 35/35 strict Native as historical exact-subject model result; R30 semantic review already done. **No repeated generic check**. After an owner-controlled *real baseline* Host Task Claim event is actually eligible, perform one source-qualified v4.18 proof/readback against the stable core. Separately, when a lawfully frozen v4.19 Project/Task and selected publisher exist, validate the candidate-only profile and Task changes. If concrete counterexamples are identified, issue one repair+affected-tests closure, not a validation-only handoff.

No Gate, GitHub Actions, Release/Freeze/Merge, published Claim, external project source change, or auto-upgrade was made in R32. Full ADS rule denominator and source↔SMT semantic equivalence remain UNKNOWN/NOT_PROVEN.

## 5. R32 direct native GitHub readback — historical v4.18 source evidence

After the version-split source audit, checked actual native GitHub comments and the Task-to-PR source boundary instead of relying only on Tally's test source and owner reports:

- [#166 native Claim event](https://github.com/kaicreator-mm/tally/issues/166#issuecomment-6507893767): direct unedited GitHub comment, `DISPATCH_CLAIMED`, Task #166, source `7823e18e4b9f4d4df9a2c9065de1b1fed6421264`, key `kaicreator-mm/tally#166:builder:__default__`, generation 1; created=updated 2026-10-29T20:44:11Z.
- [#169 native Claim event](https://github.com/kaicreator-mm/tally/issues/169#issuecomment-6511046226): direct unedited GitHub comment, `DISPATCH_CLAIMED`, Task #169, source `3293aace8a07c2a4f79a75c6539245980f77e2b4`, key `kaicreator-mm/tally#169:builder:__default__`, generation 1; created=updated 2026-10-29T23:35:02Z.
- #169 exact source commit's `.dev-standard/VERSION` Git Blob `27c31b0835075af6c66cc42ea868f1d12dcfd225` pins **ADS 4.18.0** revision `2c395c55569fe2edf3f4135f12d3d069e526d0b7`.
- [#169 original Task frozen scope](https://github.com/kaicreator-mm/tally/issues/169) lists seven paths; [PR #170 changed-path API](https://github.com/kaicreator-mm/tally/pull/170/files) returns **exactly seven identical paths, 0 out of scope**. PR #170 is merged, source head `16046d3446c769f9a1010812f11af823b86a2d6`, merge commit `2c9a9b42426c1af9aae823c98d79eb570a0b4594`, merged 2026-10-30T06:45:40Z. The seven paths exist in integrated tree `2c6631dbdc3458d4dea43fdc7d78cd292c0aebe9`.
- [#169 terminal report](https://github.com/kaicreator-mm/tally/issues/169#issuecomment-6517259345) and [#125 summary](https://github.com/kaicreator-mm/tally/issues/125#issuecomment-6517260617) report physical public DH SQLite CAS `PUBLISHED_VERIFIED`, K `ADMITTED_PENDING_AGENT_EFFECT`, and Woodpecker #98 PASS with `taskPass=false`, `agentLaunch=false`, `releasePass=false`. These are historical authored **claims**; R32 does not independently read a live Host SQLite DB, and comment publication by itself is not a verified CAS lock.

**Executed R32 scoped checks:** immutable baseline-vs-candidate source/schema **14/14 static PASS**; native comment identity, no-edit timestamps, exact source pin and Task-scope **16/16 direct-readback assertions PASS**; Task #169 frozen paths vs merged PR #170 **7/7 match, 0 extra**. These are source/provenance checks, not a complete YAML/AJV event-schema run, native Solver execution, concurrency proof, or Host CAS acceptance result.

**R30 P2 qualified progress, not closure:** P2-01 now has *observed* native Key/Gen1/source event; physical CAS proof is still owner-reported. P2-02 has observed Task write-set-to-code 7/7 identity but not actual concurrent Writer exclusion. P2-03 has unedited published Start Record candidates but no successor/current grant/terminal-resource reconciliation. **All three P2 stay OPEN.** Current #169 Issue is closed while the derived `state:ready` label remains, hence historical terminal status cannot be inferred from that label.

Next task is to reuse real v4.18 owner-controlled Host evidence only when available; do not manufacture a v4.19 Project pin, true CAS authority, Agent launch or Release PASS. Do not repeat R29 native execution.