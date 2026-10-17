# Prior-art evidence spine — bounded cross-stage walkthrough (#931)

Status: **NON_NORMATIVE / analytical counterexamples**, not executed upstream test evidence or an asserted Product/Architecture Freeze. Canonical stage execution prompts: `prompts/L1_PRODUCT_EVIDENCE.md`, `L2_ARCHITECTURE_EVIDENCE.md`, `L3_IMPLEMENTATION_EVIDENCE.md`. No new universal schema or central evidence registry.

## Case 1 — app8: GUI/agent CLI competitor

| Stage | What may be reused from the previous stage | Required new decision / prohibited promotion |
| --- | --- | --- |
| L1 Product | [CLI-Anything repository](https://github.com/HKUDS/CLI-Anything) as an adjacent "GUI to agent-native CLI" category, actual observed reference and source timestamp | The project overlaps the *user Job*, which disproves a narrow MCP/Skill-only search claim; no assertion that CLI-Anything solves the whole app8 Product or has a safe compatible license |
| L2 Architecture | Stable upstream identity and L1 caveat can be referenced | Select an exact module/commit, inspect its contracts/tests/dependencies and decide Pattern vs Reconstruction vs Direct Reuse vs Build New. Without real version/readback and license assessment: `UNKNOWN`, **not** "approved reuse" |
| L3 Implementation | If and only if L2 made a source-bound selected decision, consume that ref | Provide exact upstream test/path/revision and local contractual divergence on one Task; otherwise remain `NOT_PROVEN`, not a generic "copy repository" instruction |

**Falsifier:** a future model output which says “L1 competitor exists, therefore L2 direct reuse approved, therefore L3 tests PASS” violates both missing-stage-authority and evidence-currentness requirements.

## Case 2 — unrelated xDownload download manager

| Stage | What may be reused | Required new decision / prohibited promotion |
| --- | --- | --- |
| L1 Product | [AB Download Manager](https://github.com/amir1376/ab-download-manager) as a mainstream conventional download manager and [yt-dlp](https://github.com/yt-dlp/yt-dlp) as source/media extraction prior art | Their presence supports an adjacent alternatives category; neither is evidence that xDownload's model-generated reusable DownloadPlan / Harness behavior is implemented |
| L2 Architecture | Both precise project identities and L1 "not equivalent" boundary | Explicitly choose transport/retry/extraction capability slice, compatibility/license obligations and integration vs reconstruction boundary. No automatic technical endorsement without inspecting the selected version |
| L3 Implementation | Consume only the selected L2 capability with source ref, observed tests/contracts and version constraints | A Task Pack's Tests→Contract→Implementation mapping requires source/currentness; project popularity/docs alone cannot certify a candidate implementation |

**Falsifier:** blindly reusing an old release note/source path without checking current revision or license makes the relevant L3 evidence `STALE/UNKNOWN`, not PASS.

## Proportionality and negative boundary

A small scope with no material upstream decision need not produce a separate evidence-spine file or new Issue. If L1/L2 already captured current durable references, L3 may cite them without new broad web search; only a stale relevant claim calls for targeted refresh. A historical upstream issue or reverted implementation is valuable *failure evidence*, not current source behavior. Neither walkthrough ran an external code checkout, licensing legal review, or live downstream L3 implementation; those outcomes remain unproven.
