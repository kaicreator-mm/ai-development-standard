# v4.9.0 PRD Revision History

Historical PRD snapshots are immutable evidence. `PRD.md` is the current Product document; Freeze status is owned by `PRODUCT_FREEZE.md` and related status records without rewriting the reviewed PRD blob.

| Revision | Status | Review / reason | PRD blob | First materialization |
|---|---|---|---|---|
| v0.1 | superseded | first review candidate | `bd4c191f11ffc92fb4ea1b5af8d53d28a56652e5` | HEAD `a6f3d5c1ff134d2a567bfbf2f7cacf6a336acd23`, tree `7650a31fbab5131cb6e9613f44a1ab1a7bd83dd3` |
| v0.2 | superseded | author-side pre-review fixes; independently reviewed by #699 | `86ae3dcd3c36dbc3f0ada20178b7fd8ce7c80edd` | HEAD `6ea8313397fa08f2c79835d718b920efe68243c4`, tree `faeeaccf8fe8a3722a212c211fcfe1cfb539e55b` |
| v0.3 | superseded / rejected for Freeze | #699 findings revision; #701 PASS later falsified by #702 | `fbd1b265491415451e8de382069a1b7df8f24321` | first materialized HEAD `d924af785d2432bfa6621380ba1923dae9bd4fcb`, tree `7997e835eb0779fd1da960772eeebb320d603e52`; review subject HEAD `0c9b352c106f0068cec2f15baab96b4add724ff4`, tree `f5c20c25422f9f28284e2c59f583b7c98ead3c27` |
| v0.4 | **FROZEN PRODUCT AUTHORITY** | #702 FAIL disposition under #706; fresh complete-delta review #707 PASS; Freeze Controller #709 | `a8ec7030a14337a4c2dca853dc474e965679d610` | HEAD `cda014c8a5ed4df2b7577faca189dc88339a4cd9`, tree `51773b6eb7ed1ec0b4a7c53c17f804748414c300` |

## Review lineage

### v0.1

Generation-1 review request was superseded before claim by author-side adversarial pre-review fixes. No independent review executed on v0.1.

### v0.2

- author-side adversarial pre-review: PR #698 comment `5961233246`, non-independent, `P0=0/P1=6/P2=3`;
- independent Product Review: #699 comment `5961556275`, PASS, `P0=0/P1=0/P2=2/P3=1`.

### v0.3

- #699 findings disposition incorporated;
- #701 bounded successor review comment `5961762616`: PASS / no findings;
- #702 Claude second adversarial review comment `5966353271`: FAIL, `P0=0/P1=3/P2=6/P3=3` on the same exact v0.3 subject;
- #702 therefore superseded #701 as Freeze-readiness evidence for v0.3; #701 remains historical evidence only.

### v0.4

- generated under #706 from #702 F1–F12;
- dedicated disposition artifact: `CLAUDE_702_FINDING_DISPOSITION.md`;
- PRD blob `a8ec7030a14337a4c2dca853dc474e965679d610`;
- first materialization HEAD `cda014c8a5ed4df2b7577faca189dc88339a4cd9`, tree `51773b6eb7ed1ec0b4a7c53c17f804748414c300`;
- exact reviewed branch subject: HEAD `6c419e9a78752471d16c1b2bafbc5c96cd75ac59`, tree `26b25826910f106ae894eefb49e040d22ec4ecb3`, same PRD blob;
- #707 comment `5966587978`: fresh complete-delta PASS, `P0=0/P1=0/P2=0/P3=0`, `UNEXPLAINED_MATERIAL_DELTA=0`, Freeze recommendation READY;
- #707 comment `5966886681`: second fresh complete-delta PASS on the same exact subject, `P0=0/P1=0/P2=0/P3=0`, Freeze recommendation READY;
- #709 Product Freeze Controller re-read currentness and froze the unchanged reviewed PRD blob through `PRODUCT_FREEZE.md`.

## Freeze identity

```text
FROZEN_PRD_REVISION=v0.4
FROZEN_PRD_BLOB=a8ec7030a14337a4c2dca853dc474e965679d610
REVIEWED_HEAD=6c419e9a78752471d16c1b2bafbc5c96cd75ac59
REVIEWED_TREE=26b25826910f106ae894eefb49e040d22ec4ecb3
FRESH_PRODUCT_REVIEW=#707@5966886681
PRODUCT_FREEZE_CONTROLLER=#709
PRODUCT_FREEZE_RECORD=docs/implementation/4.9.0/PRODUCT_FREEZE.md
```

Freeze bookkeeping after `REVIEWED_HEAD` does not create PRD v0.5 because `PRD.md` remains byte-identical; it records the authority transition only.

## Invariants

1. Never edit an existing historical snapshot to make prior Review appear current.
2. A Review terminal is valid only for the exact revision/blob/HEAD/tree it reviewed.
3. A material successor PRD revision requires successor Review under current Product/Review authority.
4. The Frozen Product identity is the reviewed PRD blob plus its exact reviewed subject and Freeze record; administrative status commits are not successor Product content.
5. Any later material Product change requires explicit thaw/amendment and a new revision; it must not silently rewrite v0.4.
