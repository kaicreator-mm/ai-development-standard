# Task Pack — T-006 Registry / Discoverability / Adoption Wiring — Architecture-Alignment Rebind

Status: **SUCCESSOR JIT PLANNING — IMPLEMENTATION NOT PERFORMED**

```yaml
task_id: T-006
repository: kaicreator-mm/ai-development-standard
version: 4.8.0
parent_issue: "#512"
lane: registry-adoption
integration_target: version/v4.8.0
merge_target: version/v4.8.0
exact_planning_base: e433c18bef84fea15abbc8d308fd9c9b4384c520
exact_planning_base_tree: b26a75484c60fb797633580e82dad7f5953dc311
v47_canonical_source: d8f613127d0167453297a5a5e983de048607aa07
v47_canonical_source_tree: 721dd393b7693d2ce82ebe0533a7fa51726d0a78
superseded_candidate: "PR #741@9b6bd9b38a3ff854269422b3248044933aac8ffe"
review_policy: required
validation_owner: independent-from-builder
validation_scope: exact-subject-integration
agent_freedom: F1_BOUNDED_IMPLEMENTATION
successor_builder_branch: task/v4.8.0-t06-registry-adoption-r2
execution_pack: .agent/execution/T-006
risk: high
```

## Purpose / corrected authority

This successor pack replaces the stale T-006 planning posture that treated the v4.7 authority registry/read-routing machinery as lineage-only. Frozen v4.8 Product preserves `v4.7 authority registry / read routing / conformance`; Frozen L2 assigns authority discovery to `v4.7 manifest/registry | register new refs | owner rules`. The correction is therefore an implementation-alignment rebind, **not** an Architecture amendment.

PR #741 is superseded historical evidence and is not a merge basis.

## Frozen authority / currentness

- Frozen Product `docs/implementation/4.8.0/PRD.md` blob `f26439580e00de6ed8b2e27d732a3095eb566219`.
- Frozen L2 `docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md` blob `f88c85454e80101a0fdf56050e21f11a05279841`.
- Frozen DAG R2 `docs/implementation/4.8.0/TASK_DAG.md` blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc`.
- Current base `version/v4.8.0@e433c18bef84fea15abbc8d308fd9c9b4384c520`, tree `b26a75484c60fb797633580e82dad7f5953dc311`.
- Canonical predecessor source `version/v4.7.0@d8f613127d0167453297a5a5e983de048607aa07`, tree `721dd393b7693d2ce82ebe0533a7fa51726d0a78`.

Any material target/frozen/source drift before Builder mutation requires an Execution Pack rebind.

## Carry-forward / composition model

### COPY EXACT from pinned v4.7 T01–T06

These portable discovery contracts are current v4.8 inputs and must be copied byte-for-byte from the pinned v4.7 source:

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

They remain discovery/reference/conformance surfaces; none becomes a new semantic owner.

### COMPOSE on current v4.8

`standard-manifest.json`:
- retain every current v4.8 inventory entry;
- carry forward v4.7 `semantic_authorities` and T01–T06 inventory paths;
- add exactly the three v4.8 machine families;
- distinct semantic concerns may point to the same existing canonical owner; competing owners for one concern remain fail-closed;
- keep Interchange v1 exactly once;
- registry metadata has no authority/gate/mutation effect.

`standards/PROJECT_ADOPTION.md` and `templates/project/.dev-standard/PROJECT_OVERRIDES.md`:
- retain current v4.8 content;
- add current v4.8 discovery/read-routing guidance derived from v4.7;
- use current v4.8 migration/reference pointers rather than stale v4.7 migration authority;
- preserve optional/materiality-driven loading and Fast Path proportionality.

### ADD v4.8 T-006 integration surfaces

```text
references/V48_REGISTRY_ADOPTION_REFERENCE.md
docs/implementation/4.8.0/MIGRATION_ADOPTION.md
scripts/test_v48_registry_adoption.py
```

### SOURCE READ-ONLY at v4.7

Do not wholesale port version-bound evidence: `docs/implementation/4.7.0/**`, `references/V47_SEMANTIC_CONFORMANCE_MATRIX.md`, `scripts/v47_conformance.py`, `scripts/test_v47_semantic_conformance.py`, v4.7 dogfood/currentness/closure/release evidence, or v4.7 future-major/checklist/golden evidence. Those bind historical Frozen Product/Task/subject identities; their semantic invariants must be re-exercised by the v4.8 focused verifier instead of rebinding historical evidence.

## Exact Builder write set — 22 paths

```text
standard-manifest.json
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
standards/PROJECT_ADOPTION.md
templates/project/.dev-standard/PROJECT_OVERRIDES.md
references/V48_REGISTRY_ADOPTION_REFERENCE.md
docs/implementation/4.8.0/MIGRATION_ADOPTION.md
scripts/test_v48_registry_adoption.py
```

No other path is authorized. A necessary path outside this set is `TASK_PACK_DEFECT/BLOCKED`, never Builder discretion.

## v4.8 registration / owner routing

Exactly these three new machine families become discoverable:
1. `schemas/task-learning-v1.schema.json`
2. `schemas/agent-capability-profile-v1.schema.json`
3. `schemas/agent-capability-evidence-v1.schema.json`

Task Learning, logical-Agent capability claims and Agent Capability Evidence remain owned semantically by `standards/EXECUTION_ARCHITECTURE_STANDARD.md`. Runner/host capability stays owned by `standards/CI_RUNNER_CAPABILITY_STANDARD.md`. Current Availability is derived and is not a fourth durable family. Interchange remains the existing `schemas/interchange-envelope-v1.schema.json`/v4.0 owner family. Provider/model identity or availability never grants correctness, authorization, routing admission, Validation, Review or Release truth.

## Carry-forward matrix

| v4.7 surface | Disposition | Why |
| --- | --- | --- |
| authority-applicability schema | COPY EXACT | preserved registry grammar, metadata only |
| manifest `semantic_authorities` | COMPOSE | retain current v4.8 inventory while restoring current owner discovery |
| authority registry reference/test | COPY EXACT | portable canonical owner/discovery rules |
| state schema/registry/reference/test | COPY EXACT | preserve owner-qualified state and forbidden inference |
| reference convention standard/reference/test | COPY EXACT | exact-subject/currentness semantics used by routing |
| progressive-disclosure reference/resolver/test | COPY EXACT | canonical non-authoritative read routing |
| compatibility alias reference/test | COPY EXACT | aliases cannot become second owners |
| project overrides/adoption | COMPOSE | current project inputs need discovery wiring without stale version pointers |
| v4.7 T07 unified conformance code/evidence | SOURCE READ-ONLY | version-specific Product/Task bindings; re-exercise invariants in v4.8 verifier |
| v4.7 T09/closure/dogfood/release evidence | SOURCE READ-ONLY | historical exact-subject evidence cannot transfer |

## Fresh Review dispositions

**P1-01:** closed by this planning rebind if implemented exactly: v4.7 registry/read-routing/state/reference/alias machinery is current v4.8 discovery machinery, not lineage-only. No Frozen Product/L2 amendment is required.

**P3-01:** mandatory hardening. `scripts/test_v48_registry_adoption.py` must use executable structural/semantic negative oracles, not required-token-only checks.

## Required negative oracles

The focused verifier must mutation-probe and fail closed for:

- RA-N01 fourth durable v4.8 machine family;
- RA-N02 duplicate/new Interchange family/version/owner;
- RA-N03 registry/read routing gains authority/gate/mutation effect;
- RA-N04 provider/model identity or availability becomes correctness/authorization/routing grant;
- RA-N05 Agent Capability Profile/Evidence absorbs runner/host resources, current capacity/Availability, or current Validation/Review truth;
- RA-N06 Availability becomes a fourth durable family;
- RA-N07 competing/broken owner, alias chain/cycle, unknown materiality;
- RA-N08 stale exact-subject evidence is rebound to successor subject;
- RA-N09 read routing returns anything other than `authority_effect=NONE`, `gate_effect=NONE`, `mutation_authorized=false`;
- RA-N10 Fast Path is forced to load/instantiate unrelated optional families;
- RA-N11 any COPY EXACT v4.7 file differs from its pinned-source bytes/blob identity;
- RA-N12 historical/current v4.8 inventory is removed or destructively rewritten;
- RA-N13 contradictory prose/grant injection still containing required tokens. The mutation must fail, proving the oracle is contradiction-aware rather than token-presence-only.

## Acceptance

- [ ] v4.7 T01–T06 portable stack is current in the exact candidate with pinned-source provenance.
- [ ] current v4.8 manifest inventory is preserved additively.
- [ ] exactly three v4.8 machine families are discoverable and route to existing owners.
- [ ] Interchange v1 remains exactly once; Availability remains derived.
- [ ] registry/router/state/alias surfaces remain non-authoritative and fail closed.
- [ ] project adoption/overrides expose progressive disclosure without forcing optional context.
- [ ] Fast Path remains lightweight with `TASK_LEARNING=NONE_MATERIAL` valid.
- [ ] provider/capability metadata never becomes authority/current truth.
- [ ] historical v4.7 exact-subject evidence is not rebound to v4.8.
- [ ] required focused/regression/repository gates pass on the exact candidate.
- [ ] independent exact-subject Validation then Fresh Independent Review pass before merge.

## Required Builder gates

```text
python -B scripts/test_v47_convergence_metadata_contracts.py
python -B scripts/test_v47_authority_registry.py
python -B scripts/test_v47_state_dimension_registry.py
python -B scripts/test_v47_reference_conventions.py
python -B scripts/test_v47_progressive_disclosure.py
python -B scripts/test_v47_compatibility_aliases.py
python -B scripts/test_v48_registry_adoption.py
python -B scripts/test_v48_task_learning.py
python -B scripts/test_v48_agent_capability_profile.py
python -B scripts/test_v48_agent_capability_evidence.py
python -B scripts/test_v48_interchange_profile.py
python -B scripts/test_v48_contract_compatibility.py
python -B scripts/test_work_item_contract_and_golden_templates.py
python -B scripts/verify_standard.py
```

Builder evidence is not independent Validation.

## Forbidden scope / failure handling

No Frozen Product/L2/DAG mutation; no new lifecycle/authority store/scheduler/Interchange family/fourth machine family; no semantic-owner rewrite; no `.github/workflows/**`, Release/Closure, T013/T014; no merge/close/reuse of PR #741; no path outside the 22-path write set; no historical evidence rebinding.

If implementation contradicts Frozen Product/L2 rather than implementing them, stop `ARCHITECTURE_AMENDMENT_REQUIRED` with exact evidence.