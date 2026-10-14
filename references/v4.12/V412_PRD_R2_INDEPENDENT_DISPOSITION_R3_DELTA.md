# ADS v4.12 PRD — Independent R2 disposition / R3 delta review

> Status: R2 review supplied by the user (independent, read-only) and R3 fixes authored in the same PR. This record is a disposition and same-author static delta review; it is not a native GitHub independent review, Product Freeze or machine conformance.

## Exact subjects

- Repo: kaicreator-mm/ai-development-standard; Draft PR #1101.
- R2 PRD blob: 3e6964054d898bb75cb517b47212d2036ab77835.
- R2 external reviewer verdict (user-supplied): FREEZE_READY=NO; P0=1, P1=4, P2=9.
- R3 PRD blob: 0bfbf782c8859e79df52c9b57904ad80bcd718e9.
- v4.11 candidate: version/v4.11.0@322e86845f78de8ea8cadb05ec624bfbb3a5de20, not an available released tag.
- main: b9461d48d902a2c7c00adff6746afc7a02a0ac3e. Candidate comparison to R2 planning branch: ahead 28 / behind 182 at review; no v4.11 GitHub release found; #1021 V01 open.

## R2 blockers and R3 changes

| Finding | R3 minimum repair and falsifier | Disposition |
|---|---|---|
| **P0-1** Bootstrap pre-DAG source permission can bypass Claim, Review, merge | FR-03.2/6: existing scoped Work Item and **accepted Claim before any source creation**; Stage 2.6 Review Policy **before dispatch**; public ABI/schema/security required Review when applicable; SF only after original tests, review, merge-ready and authorized merge. Two unclaimed creators and unreviewed schema cannot become integrated SF. No added Bootstrap human gate. | TEXT_FIXED / runtime NOT_RUN |
| **P1-1** released predecessor assumed without exact source | §10/13: explicitly pin v4.11 unreleased candidate 322e8684..., main b9461d4..., and require eventual qualified/integrated predecessor exact commit/tree for v4.12 version branch/release. v4.12 Product review now is permitted; no assertion that a hypothetical R02 passed. | TEXT_FIXED / predecessor qualification OPEN |
| **P1-2** material scope fail-open on docs/anchors/unknown additions | FR-03.5: freeze the scope manifest and exact-path non-material allowlist as immutable inputs; anything else changed, including anchors, new package, CI, scope changes, defaults MATERIAL or UNKNOWN/HOLD. Docs-only exemption only for explicitly allowed paths; post-Freeze ordinary Task source changes follow Task authority/currentness rather than refreezing old historical SF. | TEXT_FIXED / checker NOT_RUN |
| **P1-3** anchor and Task two ownership facts, lifecycle false PASS, SPLIT stale owner | FR-04: anchor only structural id/kind/location/contract_ref (+ PRESENT or PLANNED_FUTURE). Effective writer from one canonical binding/Claim, Issue/PR/gates for implementation status. Materialization binds Task ID to canonical Issue; SPLIT/SUPERSEDE uses existing dag-mutation-record-v1 with effective bindings; reverse index derived only. | TEXT_FIXED / live DAG mutation NOT_RUN |
| **P1-4** A0/A1 manual truth floor absent | §10: manual attestation is **evidence method, not Gate state**; requires GitHub-resolvable SF commit and material-scope tree/object IDs, immutable scope and exact allowlist, DF checkpoint and all nonallowlisted changes checked; unknown holds. V10 NOT_APPLICABLE with reason only if no generator/machine claim; other unrun machine predicates NOT_RUN. | TEXT_FIXED / A0 fixture NOT_RUN |

## Nine P2 decisions

1. Paths corrected to prompts/L1_PRODUCT_EVIDENCE.md and prompts/L2_ARCHITECTURE_EVIDENCE.md (verified exist on v4.11 candidate).
2. T00 clarified as shun-assistant project practice, not normative v4.11 standard.
3. Technical Architecture Research Demo remains after Product Freeze; L1 technical feasibility is not silently allowed as ordinary product discovery.
4. Duplicate Task/Claim/Release detail treated as inherited existing owners; new six-value code reuse vocabulary removed from normative contract.
5. AC-01/02/06 rephrased as bounded source-backed fixtures and expected outcomes.
6. W2/W3/W4 P1 delivery narrowed to ALREADY_SATISFIED / NECESSARY_BOUNDED_DELTA / DEFER, not unconditional new services.
7. Failed already-merged SF goes through lawful supersede/revert/repair and explicit rebaseline.
8. P0 project evidence limited to one new-project and one mature-project **source-pinned** fixture, others optional.
9. Scaffold source file creation never automatically authorizes install/postinstall/network effects; safe no-script/pinned/offline route or explicit current owner.

## R3 next-round adversarial checks (author-led, TEXT ONLY)

| ID | Counterexample → required result |
|---|---|
| R3-X01 | New-repo two agents write same public contract before Claim → DENY source edit |
| R3-X02 | Public ABI compiles but required independent Review not obtained → cannot call SF accepted/merged |
| R3-X03 | Candidate v4.11 unreleased while PR base main v4.10 → cannot imply predecessor Release/RQ PASS |
| R3-X04 | Change docs/planning/scaffold-anchors.json, pretend docs-only → MATERIAL |
| R3-X05 | Add packages/new-adapter and alter CI outside narrow scope → MATERIAL by default |
| R3-X06 | Legitimate post-DAG Task adds private file → normal bounded Task currentness, no historical pair thaw |
| R3-X07 | Anchor says owner T02 but binding says T05 IMPLEMENTS → anchor cannot carry competing owner fact |
| R3-X08 | T02 SPLIT to T02a/T02b → same authorized DAG-mutation record rebinds effective Task/Issue owners |
| R3-X09 | A0 cannot resolve tree identity yet says MANUAL_ATTESTED PASS → unknown HOLD, no extra Gate enum |
| R3-X10 | A0 no generated map, V10 asserted PASS → require reasoned NOT_APPLICABLE, no fictitious machine proof |
| R3-X11 | Planned manifest install runs network hook → actual execution rights needed separately from file creation |
| R3-X12 | Scaffold+DAG match but Frozen L2 semantic DENY differs → three-way check blocks paired Freeze |

## Disposition and next-stage constraint

R3 file was re-read at exact blob above and 15 focused document predicates covering Claim, Review, merged SF, source pins, closed materiality scope, single writer, mutation and manual Git proof evaluated TRUE. This is **static documentary verification only**, no executable semantics, Claim race, Git tree validator, A0 proof or Product authority action was run. No new definite Product P0/P1 was found in this same-author bounded delta check. That finding is NOT an independent approval.

FREEZE_READY=NO_PENDING_R3_INDEPENDENT_DELTA_AND_PRODUCT_AUTHORITY. The original independent R2 findings remain open evidence on the historical R2 subject; R3 textual repairs still require one exact-blob independent delta review. The v4.11 predecessor candidate remains not a released baseline; v4.12 integration/release must not assume it has already qualified.

## R3 independent delta trigger

Perform a read-only independent adversarial delta audit of kaicreator-mm/ai-development-standard PR #1101, PRD file docs/product/PRD-v4.12.0-review-candidate.md, REQUIRED blob SHA 0bfbf782c8859e79df52c9b57904ad80bcd718e9. Verify pinned v4.11 candidate 322e86845f78de8ea8cadb05ec624bfbb3a5de20, original Development Workflow Stage 2.6, GITHUB_AGENT_INTERACTION_PROTOCOL §8.5/§11, PROJECT_ADOPTION, native DAG mutation. Concentrate ONLY on R2 P0-1 and P1-1–P1-4 repairs and their new edge cases (Claim→Review→merge-ready; predecessor release; immutable fail-closed material scope; single binding ownership + SPLIT; manual A0/A1 Git proof). Recheck install hook side effects and L2 semantic drift. Do not inherit author self-review PASS. Output new P0/P1/P2 and each old blocker CLOSED/PARTIAL/OPEN, source-exact citations, minimal fix, FREEZE_READY YES/NO. Do not edit, merge or Freeze.

R3_INDEPENDENT_REVIEW=NOT_RUN; R3_PRODUCT_FREEZE=NO; L2=NOT_STARTED.