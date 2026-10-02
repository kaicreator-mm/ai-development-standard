# v4.9.0 PRD Revision History

This file is the canonical index of durable PRD revisions for v4.9.0. Historical PRD snapshots are immutable once recorded here. `PRD.md` points to the current candidate; every material revision also receives a versioned snapshot under `docs/implementation/4.9.0/prd-history/`.

| Revision | Snapshot | Exact source identity | Review state | Disposition |
|---|---|---|---|---|
| v0.1 | `prd-history/PRD-v0.1-first-review-candidate.md` | PR #698 HEAD `a6f3d5c1ff134d2a567bfbf2f7cacf6a336acd23`, tree `7650a31fbab5131cb6e9613f44a1ab1a7bd83dd3`, blob `bd4c191f11ffc92fb4ea1b5af8d53d28a56652e5` | superseded before independent review | author-side pre-review found P1/P2 issues; superseded |
| v0.2 | `prd-history/PRD-v0.2-author-pre-review-revised.md` | PR #698 HEAD `6ea8313397fa08f2c79835d718b920efe68243c4`, tree `faeeaccf8fe8a3722a212c211fcfe1cfb539e55b`, blob `86ae3dcd3c36dbc3f0ada20178b7fd8ce7c80edd` | independent Product Review #699@5961556275 PASS; P0=0/P1=0/P2=2/P3=1 | superseded by bounded finding-disposition revision |
| v0.3 | `prd-history/PRD-v0.3-post-independent-review.md` | blob `fbd1b265491415451e8de382069a1b7df8f24321`; commit/tree recorded after materialization | pending bounded currentness/finding-resolution review | current Product candidate; not Frozen |

## Revision rule

For every future material PRD edit:

1. preserve the predecessor snapshot unchanged;
2. create a new monotonically increasing PRD revision;
3. record the exact source HEAD/tree/blob and review evidence;
4. update `PRD.md` to the new revision;
5. never rewrite a historical snapshot to make old evidence appear current;
6. Product Freeze must name the exact frozen PRD revision/blob/commit/tree.

Editorial-only typo corrections after Freeze require the normal authority/currentness rules and must not silently rewrite Frozen Product semantics.