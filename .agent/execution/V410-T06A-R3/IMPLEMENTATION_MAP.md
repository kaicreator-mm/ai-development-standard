# V410-T06A R3 implementation map — durable-form repair on the unmerged candidate

Bound to `eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601` (tree `09db8216ec49caf84b45f404474cfbf4cb5e6ad2`), branch `task/v4.10.0-v410-t06a-owner-convergence`, PR #925 (open, unmerged). This map is the controller's generation record; the Builder's evidence goes to the PR, not into this pack.

## 0. Controller actions in this round (pack material only — no source mutation)

| Action | Surface | Result |
|---|---|---|
| R1 machine-conformance correction | `.agent/execution/V410-T06A-R1/TEST_MATRIX.yaml`, `IMPLEMENTATION_MAP.md`, `MANIFEST.yaml` (`conformance_corrections`, `superseded_by`, `execution_state`) | false claim + machine-incompatible registration instruction replaced with the measured behavior and the R2 resolution; provenance attached; `classify_pack_staleness` re-read `PACK_CURRENT` |
| Frozen-v4.8 inventory disposition | `V410-T06A-R3/MANIFEST.yaml` `dispositions[FROZEN_V48_INVENTORY_VS_V410_REGISTRY_GROWTH]`, `EXECUTION_CONTRACT.md` §2 | authority chain, invariant-vs-pin split, T06A-scope readings, gap stays open |
| Successor pack | `.agent/execution/V410-T06A-R3/*` (six core artifacts) | successor execution authority, `PACK_CURRENT` at generation |
| Successor write set | `V410-T06A-R3/MANIFEST.yaml` `successor_write_set`, `EXECUTION_CONTRACT.md` §3 | two surfaces, properties P1–P5 / Q1–Q5 |

`standard-manifest.json` delta: **NONE** (blob `21730a0251e35e13591d2c84de1c66d6ab2c2408`, unchanged). No guard, schema, template, prompt, checklist, golden, verifier/CI or upstream owner file touched. `V410-T06A-R2` pack artifacts are byte-identical (executed authority for `f294173`).

## 1. Builder work item A — durable-form repair of `scripts/test_v410_owner_convergence.py`

**Diagnosis to preserve (measured).** The R2 suite's `CandidateShapeTests` and the zero-delta assertions encode the T06A candidate-local resolution as live invariants against a frozen base:

```text
test_candidate_diff_shape_is_exact        git diff --name-only eea3e69 == the 14 declared paths
test_manifest_blob_identity_proves_zero_delta  hash-object standard-manifest.json == 21730a02...
test_no_manifest_rows_added_for_gap_families   entry-id set == the 11 carried ids
test_reference_and_test_are_not_manifest_registered  neither surface registered in any section
test_carried_guards_are_not_amended_by_this_task     guard additions constant lacks the two paths
```

Collision evidence (to reproduce, not to re-derive): staging a single new path fails the first with the new path named; the authorized T06B shape (guard allow-list + manifest moved together) fails four; the full target shape plus the seven gap rows fails six. No successor configuration keeps the R2 suite green.

**Repair shape (properties fixed, code free).**

- Move the candidate-shape proof into a dated in-tree record (a record of what T06A resolved, with the recorded identities) and assert the *record*, not the live tip.
- Replace the guard *source-freeze* assertion with a *behavioral* guard probe: mutate the manifest in memory (unauthorized section addition; count deviation) and require the carried guard functions to report problems.
- Keep every fail-closed case (N1–N7) and the non-authority/declaration/reconstructibility checks.
- Evidence obligation: on a scratch copy, (i) the authorized paired evolution must leave the repaired suite green, (ii) manifest-only growth must still be rejected by the carried guard suite. Record both.

**Acceptance for this surface.** Suite PASS on the committed candidate; properties P1–P5 hold; no negative case weakened; no assertion depends on the branch tip being exactly this candidate.

## 2. Builder work item B — scope correction in `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md`

Apply the disposition (EXECUTION_CONTRACT.md §2) to the prose that currently over-broadens T06A-scope constraints:

- §2 legacy table row for `scripts/test_v48_registry_adoption.py`: state "not amended by T06A" and record the evolution ownership (T06B #861) under the Frozen L2 §3 authorization, instead of a bare "must remain unmodified" reading.
- §3 / §5: keep `STATUS=GAP`, `ACTION=STOP_FOR_DISPOSITION`, `ROUTED_TO=T06B(#861)`, `DISCOVERY_REGISTRATION=BLOCKED_BY_V48_FROZEN_INVENTORY_GUARD`; no closure claim; update §5(b) to the corrected state of the R1 pack defect (correction landed this round; residual conformance-wiring ownership with T06B).
- Preserve §0 declarations, exact-SHA refs and §4 reconstructibility. No resolver/runtime contract/precedence layer/lifecycle/service. Reference stays **unregistered** (Option A).

## 3. Measurement record at the rebind (clean detached worktree, committed tree)

```text
scripts/test_*.py (77 suites)          PASS=77 FAIL=0
scripts/verify_standard.py             PASS; manifest files: 220; bootstrap-required: 41
scripts/test_v410_owner_convergence.py Ran 22 tests ... OK
pack conformance probe (R1, R2)        schema PASS; core_artifacts complete; classify_pack_staleness PACK_CURRENT
authoritative remote at the rebind      version/v4.10.0 = eea3e69 (unchanged); branch head = f294173; refs/pull/925/merge = 1b68c331
```

After this round's pack commit: `test_candidate_diff_shape_is_exact` fails on the rebind tip by design (six added pack paths) and `PACK_CURRENT` re-reads hold for R1 and R3; the Builder's repair restores green at the candidate.

## 3.1 Authorized-evolution and evolution-channel probes (first-hand, scratch detached worktree at the rebind tip)

```text
case H  guard AUTHORIZED_SECTION_ADDITIONS += the two T06A surfaces
        AND manifest sections.references/verification += the same two paths
        guard suite      OK (19 tests)
        verify_standard  PASS (manifest files 222)
        focused suite    FAILED (failures=4) -> C1 diff-shape, C5 guard-not-amended,
                         C2 manifest-blob-identity, C4 not-registered
        => the authorized evolution is mechanically possible and stays green where it must;
           the R2 suite's four candidate-scope assertions are precisely what must be repaired (P1)

probe   embedded BASELINE_SECTIONS += the same two paths (baseline mutation instead of the
        authorized channel)
        guard suite      FAILED (failures=1) -> RA-01 "embedded BASELINE_SECTIONS no longer match
                         the frozen base manifest"
        => growth is additive-only through the authorized channel; green-by-deletion/baseline-rewrite
           is impossible by guard design, which is why the section-2 disposition scopes N7 to T06A
           rather than to the authorized T06B evolution

scratch removed after measurement (git worktree remove); no tree outside _tmp was mutated
```

## 4. T06B boundary (unchanged)

schemas/agent-event-v2, review-finding-v1, review-aggregation-v1, templates, prompts, checklists, golden, verifier/CI wiring, registry growth and frozen-inventory-guard evolution, execution-environment WEB|LOCAL refinement = **#861**. Any residual stale projection is recorded as `ACTION=REWIRE_PROJECTION` and routed, never repaired here.
