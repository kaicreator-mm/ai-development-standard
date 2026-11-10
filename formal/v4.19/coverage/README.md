# ADS v4.19 normative-document coverage and source-delta triage

**Main owner:** [ADS Formal #1366](https://github.com/kaicreator-mm/ai-development-standard/issues/1366). **Status:** EXPERIMENT / DOCUMENT_INVENTORY_ONLY / NOT_FULL_ADS_PROOF.

## Inputs and denominator (actual Git readback)

The **46** files listed in `standard-manifest.json.sections.normative_standards` are the document-level inventory for the observed baseline `ac7e7e51de3a7ac27343f16a96568c0b0f2c5349` and prospective candidate PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988`. The canonical Manifest blob `b0836c3b75cec1e1b20c127a256ac6e963d4c92a` is **the same** at both commits. Exactly **two** listed compatibility entries are outside this denominator. Candidate Git tree `def156ce156c7301c30cf7df1f4bf956b7817c5f` and baseline Git tree `cdf032f629668008a940993713a2bfaa219f5653` were fetched fully (not truncated); every listed path resolved to a blob in both.

`normative-file-matrix.json` binds each of the 46 entries to both observed Git blobs, candidate size, and actual pilot-property source references from `formal/v4.19/r8/source-index.json` (`1dbfb2132fdeb227a33063d66390ede4db249894`).

**Document reference scope:** 3/46 referenced by 10 pilot Properties; 43/46 unreferenced. **Observed candidate diff:** 7/46 normative docs have changed Git blobs, of which only 2/7 are in the current property source index. The other **5/7 changed documents require source-level triage**, not an automatic new proof gate.

**Obligation-level coverage denominator = UNKNOWN.** A mapped document is *not fully proven*, and a changed blob is not proof of a changed rule.

## Actual changed-file matrix

| Manifest normative document | Pilot index | Exact observed baseline → candidate blobs (abbrev.) |
|---|---|---|
| `standards/ARCHITECTURE_DESIGN_STANDARD.md` | **Unmapped** | `19ba240a1501` → `51fad2c5b357` |
| `standards/DEVELOPMENT_WORKFLOW.md` | **Unmapped** | `8d14b25dff70` → `7b867e174b9d` |
| `standards/EXECUTION_PACK_STANDARD.md` | Mapped (4 Properties) | `c7bd2e4ffb87` → `1bd8631dd712` |
| `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` | Mapped (7 Properties) | `49ecd802c5bf` → `935a905d593d` |
| `standards/IMPLEMENTATION_QUALITY_STANDARD.md` | **Unmapped** | `3beba2d0324d` → `c37c4a223e21` |
| `standards/TASK_DECOMPOSITION_STANDARD.md` | **Unmapped** | `b7ffab0b94f4` → `13ded16f7c0a` |
| `standards/TESTING_STANDARD.md` | **Unmapped** | `c32bc97695f5` → `746ec1da78b4` |

The previous R5 Rule Crosswalk's seven paths describe a **selected pilot source subset**, not all 46 normative documents or all candidate changes. Do not conflate its "2 changed mapped standards" with the **seven actual changed normative files**.

## Five changed, unmapped documents — source patch inspection

- **`TESTING_STANDARD.md`**: PR #1365 adds §6.1 test *collection/discovery vs actually executed tests* and §6.2 actual selected public consumer invocation. **Next recommended bounded experiment:** a green but filtered test command cannot discharge a required suite that was never collected/executed; verify by a concrete Python runner fixture and fail-closed `NOT_RUN`, not merely adding SMT tautologies.
- **`TASK_DECOMPOSITION_STANDARD.md`**: §13.1 distinguishes a necessary upstream integrated-code dependency from mere later integration/Review/Release joins; preserve native DAG/Claim/write-set authority. A finite model can challenge a false serial edge but must not authorize dropping real edges.
- **`IMPLEMENTATION_QUALITY_STANDARD.md`**: actual selected public/plugin behavior differs from SOURCE_PRESENT and EXPORTED_OR_LOADED; a loaded module is not proof of the public path.
- **`ARCHITECTURE_DESIGN_STANDARD.md`**: selected executable public-composition path and retained high-impact behaviors must be assigned to owning integration/Validation concern; mocks/import-only are insufficient.
- **`DEVELOPMENT_WORKFLOW.md`**: stage-1 exploratory Product evidence uses a main Issue + versioned Git Demo/receipts (candidate ADS #1361); root-class repair must be causally sufficient, avoid endless task/Issue proliferation.

These observations are based on the exact changed PR #1365 file patches and remain **candidate-only**, not effective universal ADS obligations.

## Recommended delivery order

1. Close current-HEAD `tool_version_report` regression with a **small actual execution receipt**. Reuse R10 historical strict 35/35 at model `671c5fa`; don't fabricate a fresh full 35/35.
2. Create an executable negative case for the **real test discovery** semantics (`TESTING_STANDARD.md` §6.1); record observed execution versus claimed collection and the resulting correct `NOT_RUN` state. It should be a Python conformance probe first, **no new SMT case without evidence that SMT adds value**.
3. Assess the other four changed, unmapped source families using minimal counterexample and source owner; only promote a genuinely cross-cutting invariant to formal model after the concrete failure is established.
4. Full clause/obligation inventory is not materialized yet. Keep its denominator `null`; adding a full automation effort requires concrete benefit and reliable source segmentation.

This document is an **index and future experiment selection**, not an assertion that uncovered rules are incorrect or normative Release gates.
