# v4.8 T-006 L3 — Registry / Discoverability / Adoption Wiring — Architecture Rebind

Status: **TASK-SCOPED L3 — SUCCESSOR BUILDER INPUT**

Authority is bounded by Frozen v4.8 Product/L2/DAG, Issue #512, the successor Task Pack, and `.agent/execution/T-006/**`. This L3 cannot widen the Task Pack write set.

## 1. Objective

Restore the canonical v4.7 discovery/read-routing/state/reference/alias stack as a current v4.8 discovery layer, then register the three already-owned v4.8 machine families without duplicating semantic authority.

The implementation is a composition problem:

```text
CURRENT_V48_BASE
+ PINNED_V47_PORTABLE_DISCOVERY_STACK
+ THREE_V48_MACHINE_FAMILY_REGISTRATIONS
+ V48_ADOPTION/VERIFIER_WIRING
= SUCCESSOR_T006_CANDIDATE
```

No Frozen architecture change is required.

## 2. Exact sources

```text
CURRENT_BASE_SHA=e433c18bef84fea15abbc8d308fd9c9b4384c520
CURRENT_BASE_TREE=b26a75484c60fb797633580e82dad7f5953dc311
V47_SOURCE_SHA=d8f613127d0167453297a5a5e983de048607aa07
V47_SOURCE_TREE=721dd393b7693d2ce82ebe0533a7fa51726d0a78
SUPERSEDED_PR=#741@9b6bd9b38a3ff854269422b3248044933aac8ffe
```

The Builder must re-read both source commits and current Issue #512 before mutation. Drift => stop/rebind.

## 3. Implementation classes

### A. COPY_EXACT

Copy these bytes from `V47_SOURCE_SHA`; do not edit while carrying forward:

```text
schemas/authority-applicability-entry-v1.schema.json
schemas/state-dimension-registry-v1.schema.json
scripts/test_v47_convergence_metadata_contracts.py
references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md
scripts/test_v47_authority_registry.py
registries/state-dimensions-v1.json
references/STATE_DIMENSION_REGISTRY_REFERENCE.md
scripts/test_v47_state_dimension_registry.py
standards/REFERENCE_CONVENTION_STANDARD.md
references/REFERENCE_CONVENTION_REFERENCE.md
scripts/test_v47_reference_conventions.py
references/PROGRESSIVE_DISCLOSURE_ROUTING.md
scripts/resolve_standard_read_set.py
scripts/test_v47_progressive_disclosure.py
references/COMPATIBILITY_ALIAS_CONFORMANCE.md
scripts/test_v47_compatibility_aliases.py
```

`test_v48_registry_adoption.py` must verify COPY_EXACT provenance deterministically (Git blob identity or exact bytes against pinned expected identities).

### B. COMPOSE

#### `standard-manifest.json`

Start from the current v4.8 file, never from the v4.7 whole file.

1. Preserve all current `sections` members/entries.
2. Add the COPY_EXACT paths to the appropriate sections.
3. Carry forward `semantic_authorities.schema_version=1` and the canonical v4.7 entries.
4. Register v4.8 discovery concerns only by pointing to existing normative owners.
5. Add exactly these machine contracts once:
   - `schemas/task-learning-v1.schema.json`
   - `schemas/agent-capability-profile-v1.schema.json`
   - `schemas/agent-capability-evidence-v1.schema.json`
6. Preserve `schemas/interchange-envelope-v1.schema.json` once.
7. Add `references/V48_REGISTRY_ADOPTION_REFERENCE.md` and `scripts/test_v48_registry_adoption.py`.

Registry rules remain: unique `entry_id`; one owner per `semantic_concern`; same canonical owner may serve distinct concerns; broken/ambiguous owner/alias is fail-closed. The registry is discovery metadata only.

#### `standards/PROJECT_ADOPTION.md`

Add a bounded v4.8 convergence-discovery subsection that points to the current manifest semantic registry, state registry, progressive read router and V48 adoption reference. State explicitly that discovery does not grant mutation/gate/PASS/Release authority and optional materiality does not become mandatory adoption.

#### `templates/project/.dev-standard/PROJECT_OVERRIDES.md`

Compose the v4.7 convergence-discovery project profile into the current v4.8 template, but use current v4.8 migration/reference paths. Preserve all current v4.8 template content and non-weakening rules.

### C. ADD

#### `references/V48_REGISTRY_ADOPTION_REFERENCE.md`

Non-authoritative integration map. Must state:

```text
authority_effect=NONE
gate_effect=NONE
mutation_authorized=false
```

Map each new family to its existing owner/reference, map Interchange to v1 reuse, keep Availability derived, and describe the v4.7 carry-forward provenance.

#### `docs/implementation/4.8.0/MIGRATION_ADOPTION.md`

Additive migration only. Historical evidence keeps original subject/version identity. Existing projects can omit non-material optional context. Fast Path remains lightweight. No destructive rewrite, no Interchange v2, no provider/capability authority inflation.

#### `scripts/test_v48_registry_adoption.py`

This is the successor composition/conformance oracle, not a new authority owner.

## 4. Semantic registration

The manifest semantic registry may expose distinct concerns for the three families, but every entry must resolve to existing normative authority. A safe shape is one entry per distinct semantic concern with a unique `entry_id`, while `canonical_owner_ref` may repeat when the same existing owner truly owns several concerns.

Do not encode schema paths as authority. Schema/reference presence is discoverability only.

Required ownership:

```text
task_learning_evidence -> standards/EXECUTION_ARCHITECTURE_STANDARD.md
logical_agent_capability_claim -> standards/EXECUTION_ARCHITECTURE_STANDARD.md
agent_capability_evidence -> standards/EXECUTION_ARCHITECTURE_STANDARD.md
runner_host_capability -> standards/CI_RUNNER_CAPABILITY_STANDARD.md
availability -> DERIVED / NO_DURABLE_FAMILY
interchange -> existing interchange-envelope-v1 + existing v4.0 owner
```

## 5. Focused verifier requirements

Positive assertions:

- current v4.8 inventory is a subset of candidate inventory unless the authorized T006 composition explicitly replaces an equivalent duplicate (none expected);
- COPY_EXACT files match pinned v4.7 bytes/blob IDs;
- semantic registry resolves all carried entries and v4.8 additions deterministically;
- exactly three v4.8 machine families are added;
- Interchange v1 occurs exactly once;
- all registered local paths exist;
- read resolver stays non-authoritative and fail-closed;
- state registry remains owner-qualified and preserves forbidden inferences;
- project adoption/overrides preserve Fast Path and optional/materiality-driven reads.

### P3 contradiction-aware mutation probes

Do not merely search for required tokens. Create mutated in-memory text/data fixtures and require rejection when they add an explicit contradictory grant while retaining all expected tokens. At minimum:

```text
RA-N03 registry/read-routing authority grant
RA-N04 provider/model authorization/correctness grant
RA-N05 capability profile/evidence becomes current Validation/Review or runner-resource truth
RA-N09 authority_effect/gate_effect/mutation_authorized contradiction
RA-N13 contradictory prose sentence that coexists with all required safe tokens
```

Also test RA-N01/02/06/07/08/10/11/12 from the Task Pack.

A contradiction checker may use bounded normalized statements/forbidden semantic patterns; it must be deterministic and repository-local. It must not attempt general natural-language truth inference.

## 6. Version-specific v4.7 surfaces intentionally not copied

`references/V47_SEMANTIC_CONFORMANCE_MATRIX.md`, `scripts/v47_conformance.py`, and `scripts/test_v47_semantic_conformance.py` bind v4.7 Frozen Product/Task Pack identities and therefore remain source evidence at the pinned v4.7 commit. Their relevant invariants (owner uniqueness, mutation-authority separation, state non-inference, exact-subject non-transfer, alias semantics) are explicitly re-tested by `test_v48_registry_adoption.py` plus the copied T01–T06 focused tests.

Likewise, v4.7 planning/migration/closure/release/dogfood evidence remains historical and must not be reclassified as v4.8 evidence.

## 7. Builder sequence

1. Claim the successor Builder dispatch before material mutation.
2. Require live target = exact planning base and native blockers still clear.
3. Verify Task Pack/L3/Execution Pack identities.
4. Create successor implementation branch from the exact target, not PR #741/head.
5. COPY_EXACT the 16 pinned v4.7 files.
6. COMPOSE manifest, project adoption and project override template.
7. ADD V48 reference, migration note and focused verifier.
8. Verify `git diff --name-only` is exactly a subset of the 22-path authorized write set.
9. Run all Task Pack gates and negative mutation probes.
10. Open a new successor PR; do not reuse/retarget/merge PR #741.
11. Publish exact PR/HEAD/TREE/base/test terminal and hand off to independent Validation.

## 8. Stop conditions

Stop `BLOCKED_CURRENTNESS` for base/source/pack drift. Stop `TASK_PACK_DEFECT` for any necessary path outside the write set. Stop `ARCHITECTURE_AMENDMENT_REQUIRED` only if implementing this composition genuinely contradicts Frozen Product/L2. Do not repair sibling owners, start T013/T014, mutate Frozen docs/DAG, merge, or self-validate/review.