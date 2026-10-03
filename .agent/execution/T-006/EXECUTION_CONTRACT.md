# T-006 Successor Execution Contract

## Authority tuple

```text
ISSUE=#512
BASE=e433c18bef84fea15abbc8d308fd9c9b4384c520
BASE_TREE=b26a75484c60fb797633580e82dad7f5953dc311
V47_SOURCE=d8f613127d0167453297a5a5e983de048607aa07
V47_SOURCE_TREE=721dd393b7693d2ce82ebe0533a7fa51726d0a78
TASK_PACK_BLOB=b9e6eb77a3828cfa8dcdc6f6d54e92cbcdb8e308
L3_BLOB=d566d37abe4df6e0f39732da412b0f7cd00724a4
SUPERSEDED_PR=#741@9b6bd9b38a3ff854269422b3248044933aac8ffe
```

The successor Builder must claim execution before mutation and re-read Issue #512 plus all pinned identities. Any material drift stops execution and requires rebind.

## Required result

Compose the pinned v4.7 T01–T06 portable authority-discovery/read-routing/state/reference/alias stack into the current v4.8 base, then register exactly three v4.8 machine families into that discovery layer without creating a new semantic owner.

Implementation must preserve:

- existing normative owner boundaries;
- registry/read routing as non-authoritative (`authority_effect=NONE`, `gate_effect=NONE`, `mutation_authorized=false`);
- exactly three new v4.8 machine families;
- existing Interchange v1 only;
- Availability as derived, not a durable fourth family;
- provider/model/capability metadata as non-authority;
- exact-subject evidence non-transfer;
- additive historical compatibility;
- Fast Path proportionality and `TASK_LEARNING=NONE_MATERIAL`.

## Mutation authority

Only the 22 Builder paths in `MANIFEST.yaml` / Task Pack are writable. COPY_EXACT paths must retain pinned v4.7 bytes. COMPOSE paths must start from the current v4.8 versions. New v4.8 reference/migration/verifier paths are bounded by the L3.

No Frozen Product/L2/DAG edits, sibling semantic-owner edits, workflow/release/closure work, T013/T014, reuse/merge of PR #741, or write-set expansion.

## Candidate rule

Create a new successor implementation branch from the exact current target. Do not implement on this planning branch and do not reuse PR #741. Open a new PR only after required Builder gates pass.

Builder PASS is implementation evidence only. Independent exact-subject Validation and a genuinely Fresh Independent Review remain required before merge.