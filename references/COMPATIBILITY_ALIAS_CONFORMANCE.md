# Compatibility / Alias Conformance — v4.7

Status: **T06 CONFORMANCE REFERENCE — derived from Frozen v4.7 Product/L2/Task authority**

This reference defines executable compatibility checks for stable v4 paths already exposed by `standard-manifest.json`. It does **not** authorize moving, deleting or rewriting repository paths, and it does not create a second normative owner registry.

## 1. Authority boundary

`standard-manifest.json.sections.compatibility_entries` remains the legacy/stable-path inventory. `standard-manifest.json.semantic_authorities.entries[*].compatibility_alias_refs` provides the v4.7 semantic routing edge from a compatibility path to the one canonical owner for the indexed semantic concern.

The canonical owner remains a member of `sections.normative_standards`. A compatibility entry is never itself a normative owner merely because it is discoverable, readable or listed by a resolver.

T06 consumes the T02 authority/applicability registry and validates compatibility integrity. It does not mutate that registry and does not decide Product, Task, migration, side-effect, Validation, Review, Release, Deployment or runtime authority.

## 2. Current stable compatibility baseline

At the T06 JIT baseline, these existing stable paths are compatibility commitments:

- `standards/GITHUB_WORKFLOW.md`
- `standards/VERSION_INTEGRATION_WORKFLOW.md`

They must remain present in the compatibility inventory, remain real repository files, and resolve through current semantic metadata to exactly one canonical normative owner for the indexed concern. A later retirement or physical move requires separately authorized compatibility/migration work; deleting a baseline path from both the inventory and registry is not a valid way to make conformance green. Conformance **cannot silently delete** these committed stable paths even if their canonical owner file remains discoverable.

## 3. One-hop resolution invariants

For the current v4 registry:

1. every compatibility entry resolves to exactly one canonical normative owner;
2. every referenced alias is listed in `sections.compatibility_entries`;
3. each canonical target is listed in `sections.normative_standards` and exists in the checkout when filesystem validation is requested;
4. compatibility and normative inventories are disjoint;
5. an alias cannot be the canonical target of another alias;
6. the same compatibility path cannot be claimed by multiple semantic entries, regardless of file or entry order;
7. broken, missing, recursive, duplicate or path-escaping entries fail closed;
8. all current compatibility inventory entries must be covered — an unindexed legacy compatibility path is ambiguity, not permission to guess a target.

The one-hop shape deliberately prevents alias chains from becoming a second resolution graph. If a future migration genuinely needs chained compatibility, it requires its own evidence and authority rather than being inferred by discovery order.

## 4. Stable path versus canonical authority

A stable compatibility file may summarize or link several standards for older adopters. That does not make all linked documents co-owners of one semantic concern. The v4.7 semantic entry chooses the canonical owner **for that indexed concern**, while other linked documents can remain related references for their own concerns.

Accordingly:

```text
alias present/readable      != normative owner
canonical owner discoverable != alias retirement authority
file order                  != conflict resolution
path cleanup desirability   != migration authority
```

The resolver returns routing metadata only. It never returns mutation, merge, adoption, side-effect or release authorization.

## 5. Compatibility failure posture

Conformance fails closed when:

- a current stable compatibility path is removed from the inventory or registry;
- a compatibility path points to a missing/non-normative canonical target;
- two entries claim the same compatibility path;
- a compatibility path is promoted into the normative owner inventory;
- an alias chain/cycle is attempted by using an alias as a canonical owner;
- the current manifest has no usable semantic registry from which a unique mapping can be established;
- a path is absolute, traverses above repository root, uses backslash normalization ambiguity, or otherwise is not a canonical repository-relative POSIX path.

Historical manifests that predate the optional T02 semantic registry remain historical inputs for legacy readers. T06 does not reinterpret those historical manifests as currently conformant v4.7 alias routing: current alias conformance requires current routing metadata.

## 6. Migration boundary

T06 validates only current routing and stable-path retention. It does not authorize physical repository refactor, compatibility-entry deletion or historical meaning reinterpretation. Evidence that a path should move becomes a separate migration/adoption decision under its proper owner and must preserve an authorized compatibility route for v4 adopters.

## 7. Acceptance evidence

`scripts/test_v47_compatibility_aliases.py` executes the current manifest and adversarial mutations. Required evidence includes:

- exact coverage of the compatibility inventory;
- current stable-path presence;
- single canonical owner per alias;
- broken/duplicate/recursive/path-escaping alias rejection;
- alias-not-owner and registry-not-authority negatives;
- deletion-from-both-inventory-and-registry rejection against the pinned stable baseline;
- explicit distinction between historical legacy readability and current v4.7 conformance.

A focused test PASS is concern evidence only. It is not Version Closure, Release Qualification or authorization to remove/move any path.