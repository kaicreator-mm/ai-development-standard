# v4.15 scope revision R2 — ADS contract delivery before consumer implementations

**Historical unaccepted proposal.** R2 was reviewed with blocking findings. The current replacement proposal is [SCOPE_REVISION_R3.md](SCOPE_REVISION_R3.md); do not combine R2's proposed in-place Task edits with R3's explicit SUPERSEDE plan. Neither proposal is an activated Freeze.

Status: **SOURCE_DRAFT / INDEPENDENT_DELTA_REVIEW_NOT_RUN / NOT_REFROZEN**.
This proposal records the human Product direction received on 2026-10-20:

> task-meta 发布器和 Tally TS 消费链尚未实现，真实 E2E 无法通过。这个先不做，完成 v4.15 后 task-meta 和 tally 才能按规范完成

It is a material Product scope revision, not a claim that the earlier frozen scope was satisfied. The earlier Product, L2 and DAG decisions remain immutable historical evidence. This draft does not admit an implementation Claim, assert a review PASS or qualify a release.

## Exact predecessor and bounded replacement

Predecessor version baseline: `a1c2ddd8c7f48374a3425b2e98c5b9dee798534a`.
Governing ADS main: `584512e8566408bed479192753c12a036309d277`.
Historical Product PRD blob: `fbeacd479f5a9a0d3dc1a3f853abe623cc211031`.
Historical L2 blob: `cf4721a90122a9c9bad486209d478f2adf81e0dc`.
Historical DAG blob: `2de26c1f82d29ad0317b219058fe6b3a34147398`.

The revision affects only delivery sequencing and the evidence needed for the ADS-owned release. It does not relax schema validation, privacy, UNKNOWN propagation, verifier authority, compatibility, currentness or lawful admission.

| Earlier frozen source | R2 replacement proposed for new source-bound review/freeze |
| --- | --- |
| PRD §1 desired outcome, D10, FR07, §6 release criteria: actual task-meta/Tally runtime is required for ADS release | v4.15 delivers ADS-owned publication, reading and feedback contracts, schema, validator, positive/negative contract conformance and implementation handoff. Actual task-meta/Tally runtime is a later cross-project integration deliverable. |
| PRD D03/D06/D07/D09 and J1–J6: runtime demonstrations | Keep the normative runtime obligations intact for implementers. ADS tests its own schema/parser/reconciliation contract and documents the externally executable test oracle. Label all synthetic fixtures as contract tests. No fixture proves real credentials, egress isolation, provider capture, runtime retry behavior or external interoperability. |
| L1 open question on narrower source-only delivery; L2 Architecture §7 and Evidence U6; PRODUCT_FREEZE/L2_FREEZE runtime-RQ carry-forward | External implementation absence is recorded as NOT_RUN for future integration, rather than a release blocker for the newly scoped ADS contract deliverable. Earlier decisions are historical, not overwritten. |
| TASK_DAG S05 and TASK_DAG_FREEZE S05 acceptance | S05 becomes ADS-owned contract conformance, compatibility/negative fixtures and precise downstream handoff. It does not implement or qualify task-meta/Tally. |
| TASK_DAG S06 and S06 Issue #1220: S05 actual E2E PASS | S06 requires the revised S05 contract-conformance acceptance plus all applicable ADS regression, independent review, finding disposition, exact-candidate currentness and RQ. It explicitly excludes any assertion of external E2E PASS. |

The wording “no unilateral scope shrink” in historical D10 is respected by recording the new explicit human direction and routing the resulting exact source through review/freeze. This draft alone is not that completed transition.

## Revised implementation acceptance

S01 #1215, S02 #1216, S03 #1217 and S04 #1218 retain their existing ADS-owned source obligations and write boundaries. No existing CI success or corrected historical Claim is newly ratified.

S05 #1219 proposed acceptance:

1. Execute positive and negative fixtures against the exact integrated v4 schema/validator, preserving original v3 schema bytes and the frozen v3/v4 compatibility rules.
2. Check execution-summary, manifest-free feedback and correction profiles, identity/revision/digest handling, missing verifier/cost UNKNOWN, unsafe YAML, privacy boundaries and invalid/mixed source pins to the extent implemented by ADS. Separate schema checks from semantic obligations and runtime behavior; report unsupported executable checks honestly.
3. Deliver downstream implementer instructions with required fields, immutable source-pin procedure, publication/readback and pagination/retry/correction/privacy test oracles. Clearly identify checks requiring actual external code and real GitHub permissions.
4. Preserve a durable deferred integration work item with actual task-meta/Tally owner refs, future immutable builds, real GitHub receipts and positive/negative execution requirements. Its state remains NOT_RUN, not waived, PASS or ADS release-ready evidence.

S06 #1220 proposed acceptance:

All six ADS-owned implementation concerns must be accepted under the revised exact source. Run applicable ADS checks and independent review against the final candidate; resolve valid blockers, bind release evidence/currentness and obtain legitimate RQ for this scope. State in release notes that external task-meta/Tally runtime interoperability is not yet verified. Keep concern PRs targeted at `version/v4.15`; the earlier user prohibition on merging main remains in force.

## Revised DAG and cross-project sequence

```text
S01 -> S02 -> S03 -> S05 contract conformance -> S06 ADS closure
S04 ----------------> S05

qualified ADS v4.15 contract
  -> separately governed task-meta and Tally implementation/adoption
  -> deferred real task-meta -> GitHub -> Tally -> GitHub integration
```

The five existing native dependency edges can remain unchanged because S05 stays an ADS-owned executable concern. Its Task Pack and S06's Task Pack must be revised only after the scoped review/freeze decision; old Task Packs and earlier claims remain historical. External projects retain their own Product/L2/DAG/admission authority.

## Review and activation checklist

- Independently inspect this exact revision, original frozen PRD/L2/DAG and the explicit human scope direction. Check every affected criterion listed above for contradiction or hidden residual dependency.
- Review the retained wire/authority/privacy/compatibility floor and the boundary between ADS conformance and actual runtime proof. No new shared schema or governance bypass is introduced here.
- Record exact source, findings and whether Product/L2/DAG scoped re-freeze is ready. An author self-review cannot supply independent PASS.
- Once legitimately accepted, publish explicit supersession links on #1207, #1219 and #1220 and the external-integration follow-up; update live Task Packs and native metadata accordingly. Until then, this remains a proposal and the old release criteria are not silently replaced.
- #1225's Assurance Plan/currentness and admission findings remain separately open. Changing scope does not cure UNKNOWN platform generation, mutation guards or historical dispatch state.
