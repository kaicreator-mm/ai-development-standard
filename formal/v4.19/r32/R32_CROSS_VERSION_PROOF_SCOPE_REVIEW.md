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

**Lane A — existing effective v4.18 baseline core:** Subject is the authorized owner of an actual v4.18 Task (for example Tally Issue #125's owning workflow), not a synthetic upgrade. May re-use its Host SQLite CAS and Native GitHub source code to examine *unchanged* Claim Key, serialization, event/readback and current Task authority evidence. Its actual implementation tests and source must be bound to the v4.18 pin and correct Task. Even if a real v4.18 accepted Claim and CAS proof appears, it closes only the specified **baseline-rule** evidence, **not** a v4.19 adoption proof. The current Tally Host source explicitly limits itself to initial generation 1 and default group; actual deployed current Host/Claim has not been established.

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
