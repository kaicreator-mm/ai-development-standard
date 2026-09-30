# v4.7.0 L2 Architecture Evidence — AI-native Development Convergence

Status: **FROZEN L2 ARCHITECTURE — 2026-09-30**

Frozen Product input: `d4f90e1432b53fe0d30d4673674280f3c5e586ec`
Final Product/currentness Review: #318 PASS / `PRODUCT_FREEZE_AUTHORIZATION=YES`
Architecture baseline main: `6f2fb482812b17289b4f3d89ccf096ef6f618123`

## 1. Architecture decision

v4.7 converges discovery, state qualification, reference conventions and read routing **without creating a new global lifecycle/runtime authority**.

The architecture is:

```text
existing normative owners
        │
        ├── canonical standard-manifest.json
        │       └── additive Authority / Applicability metadata
        │
        ├── qualified State-Dimension / Forbidden-Inference registry
        │
        ├── compatible identity / authority / reference conventions
        │
        ├── AGENTS + PROJECT_OVERRIDES + profiles + exact task authority
        │       └── derived progressive-disclosure read routing
        │
        └── executable cross-standard conformance + fresh-Agent dogfood
```

Registry and routing layers are metadata/derived views. They point to authority; they do not become authority merely because they are machine-readable.

## 2. Architectural invariants

The following are frozen:

1. **one semantic concern -> one canonical normative owner**;
2. `standard-manifest.json` remains the canonical inventory/discovery entry point;
3. registry presence never grants mutation authority;
4. equal-looking state strings remain qualified by owner/dimension;
5. no master lifecycle/state enum;
6. no universal event/result object;
7. exact-SHA/currentness meaning is unchanged;
8. existing owner records remain distinct: Dispatch, Execution Pack, Validation, Review/Aggregation, Assurance, Release, Deployment, Runtime Observation, Incident, Maintenance, Intent/Assumption and Skill metadata;
9. progressive disclosure is deterministic read routing, not a Context Snapshot database;
10. physical path movement remains optional and compatibility-preserving;
11. historical payload meaning is not rewritten;
12. incompatible convergence findings route to future-major/v5 rather than being hidden in v4.7.

## 3. Component A — Canonical Authority / Applicability Registry

### Decision

Evolve the existing `standard-manifest.json`; do **not** create a second canonical registry file that competes with it.

The existing `sections` inventory remains valid and backward-compatible. v4.7 may add an optional semantic registry layer with entries equivalent to:

```text
entry_id
semantic_concern
canonical_owner_ref
applicability_tags[]
lifecycle_tags[]
machine_contract_refs[]
profile_refs[]
compatibility_aliases[]
read_routing_tags[]
supersedes_refs[]
migration_refs[]
notes_refs[]
```

### Authority rule

An entry is discovery metadata. `canonical_owner_ref` points to the normative owner; the registry does not duplicate owner rules and does not authorize writes, merges, side effects, Validation, Review or Release decisions.

### Compatibility rule

- preserve existing `standard-manifest.json.sections`;
- prefer additive optional fields rather than a destructive manifest rewrite;
- do not bump or reinterpret existing manifest schema/version semantics unless implementation evidence requires it;
- existing consumers that only read `sections` must remain valid;
- aliases are compatibility routing metadata, not duplicate normative owners.

## 4. Component B — Qualified State-Dimension / Forbidden-Inference Registry

### Decision

Create one machine-readable metadata family describing **state dimensions and forbidden cross-dimension inferences**, not state instances.

The family may be represented by a schema plus canonical registry data. Conceptual fields:

```text
registry_version
dimensions[]:
  dimension_id
  canonical_owner_ref
  vocabulary_ref / allowed_values when already closed by owner
  open_vocabulary flag when owner is extensible
  authority_scope
  source_contract_refs[]
forbidden_inferences[]:
  source_dimension / source_fact
  forbidden_target_dimension / conclusion
  rationale / owner refs
```

### Critical boundary

This registry never owns or normalizes the live state value. It documents qualification and non-inference. Domain owners continue to own their values and transitions.

Therefore:

```text
state registry knows Validation PASS exists
!= state registry can issue Validation PASS
```

and

```text
same token `BLOCKED`
!= same semantic state across workflow, Validation, Dispatch, Release, provider, etc.
```

## 5. Default machine metadata families

v4.7 freezes exactly **two new default metadata families**:

1. **Authority / Applicability Entry v1** — the typed semantic-entry shape used as an additive extension of canonical `standard-manifest.json`;
2. **State-Dimension / Forbidden-Inference Registry v1** — qualified state metadata and prohibited cross-owner inference rules.

They are metadata contracts, not lifecycle result objects.

v4.7 does **not** freeze new default families for:

- universal Subject Identity object;
- universal Authority object;
- universal Agent/Session state;
- Context Snapshot;
- Convergence Result/PASS object;
- universal lifecycle event;
- global state transition object.

## 6. Component C — Identity / Authority / Reference convergence

### Decision

Freeze compatible **reference conventions**, not mandatory replacement objects.

Existing contracts may continue using established fields such as:

```text
repository
version/task/Issue/PR refs
subject_ref / subject_identity_ref
exact/requested/tested/current SHA
expected_base_sha
authority_ref
operator/executor/session/context refs
artifact_ref
environment_ref
provider/model provenance
validation/review/evidence refs
```

Conformance should prefer stable naming/meaning where additive, but must not rewrite historical schemas merely for cosmetic uniformity.

A future shared reference object is allowed only when evidence proves it reduces ambiguity without creating migration or owner collapse; it is **not a v4.7 default requirement**.

## 7. Component D — Progressive Disclosure Resolver

### Decision

Progressive disclosure is a deterministic algorithm over durable facts, not a new authoritative database.

Resolution order:

```text
repository AGENTS + project .dev-standard/VERSION
        -> pinned ADS
        -> canonical manifest semantic registry
        -> PROJECT_OVERRIDES
        -> applicable lifecycle/domain owners
        -> applicable language/archetype profiles
        -> Frozen Product/L2/Task DAG/Task Pack
        -> Execution Pack / Dispatch / Issue / PR / exact-SHA live facts
        -> referenced evidence/tool/resource data
```

Higher-currentness durable authority beats stale lower-authority/history.

### Output posture

A resolver/read-plan may be emitted for debugging or dogfood, but it is **derived/non-authoritative**. No default `Context Snapshot` schema is created. Chat history, memory, repository search results and tool availability may assist discovery but cannot override current durable authority.

### Fail-closed conditions

- two registry entries claim competing canonical ownership;
- applicability is materially ambiguous;
- alias/canonical target is broken or cyclic;
- project override attempts to weaken Frozen/Core authority;
- required exact task/currentness facts are missing;
- a read-routing decision would require inventing Product/Architecture authority.

## 8. Component E — Compatibility-preserving repository information architecture

Physical file movement is **not** an architecture prerequisite.

Order of operations:

1. improve semantic registry metadata;
2. improve read routing;
3. add conformance for owner/alias consistency;
4. measure remaining path/discoverability failures;
5. move/rename only where evidence shows material value;
6. preserve old stable paths through compatibility entries/aliases and explicit migration.

A path migration is a compatibility concern, not cleanup authority.

## 9. Component F — Unified semantic conformance

The executable conformance layer must test meaning, not only JSON syntax.

Minimum dimensions:

- owner uniqueness and registry-to-owner consistency;
- Task Pack write authority vs registry/discovery metadata;
- qualified state/non-inference rules;
- exact identity/currentness non-transfer;
- compatibility alias/canonical-target integrity;
- profile + PROJECT_OVERRIDES deterministic composition;
- machine-contract/prose consistency;
- progressive-disclosure routing and fail-closed ambiguity;
- historical payload/manifest compatibility;
- Fast Path proportionality;
- representative fresh-Agent reconstruction.

Conformance outputs ordinary test/Validation evidence under existing owners. v4.7 does not introduce a `CONVERGENCE_PASS` state family.

## 10. Component G — Self-dogfood and future-major register

Principal dogfood:

> a genuinely fresh logical Agent/session with no prior chat reconstructs the correct applicable owners, current exact task authority, allowed mutation/side effects, evidence requirements and next action using durable repository/GitHub facts only.

Dogfood must distinguish:

- discovery success from authority;
- static fixture proof from real external/runtime proof;
- logical reviewer/operator independence from transport account identity;
- local implementation defects from Product/L2 owner contradictions.

Findings that cannot remain additive/non-weakening in v4 become explicit future-major/v5 migration entries.

## 11. Cross-version boundary map

| Concern | Canonical owner retained | v4.7 role |
|---|---|---|
| execution foundation | v4.1 owners | discover/reference/conformance only |
| compatibility + migration | v4.2 owners | preserve domain state/non-inference |
| architecture/task/profile quality | v4.3 owners | use profile/applicability metadata; no owner theft |
| build/distribution/deployment | v4.4 owners | qualify dimensions/references |
| runtime/incident/maintenance | v4.5 owners | qualify dimensions/references |
| intent/context/skill | v4.6 owners | compose progressive disclosure and trust boundaries |
| Review/Validation/Release | existing assurance lifecycle owners | never collapse or replace |
| Task mutation authority | Task Pack / current task authority | registry points only; never grants writes |

## 12. Security / side-effect posture

Registry/read-routing data MUST NOT contain ordinary secret values. Tool/provider availability remains capability, not authorization. Side-effect authority continues to come from the owning Task/Execution/External-System/Deployment contracts.

A resolver that can locate a credential-bearing tool has learned capability, not permission.

## 13. Failure and currentness model

All material derived views bind their source authority/currentness refs where useful. Stale derived routing is discarded/recomputed rather than treated as durable truth.

Material owner conflict or broken compatibility routing is fail-closed and requires explicit owner/planning resolution.

Later implementation findings that expose an actual Frozen Product/L2 owner contradiction invalidate the affected convergence assumption and require a Planning Amendment/currentness review. Local test/schema defects do not silently rewrite this L2.

## 14. Task decomposition implications

The architecture supports parallel concerns:

- metadata contract(s);
- manifest authority/applicability extension;
- state/non-inference registry;
- reference-convention standard;
- progressive-disclosure routing;
- compatibility/path alias conformance;
- unified semantic conformance;
- fresh-Agent dogfood;
- central adoption/migration wiring;
- closure inputs.

Central manifest wiring should occur only after owner-specific metadata contracts are stable. Physical repository refactor, if any, is a separately justified future task and is **not required** for v4.7 acceptance.

## 15. Local environment posture

Product/L2 planning and most registry/conformance implementation are repository/Web/CI executable.

Fresh-Agent dogfood may require a genuinely new logical Agent/session. If a claim requires an unavailable external runtime/tool/provider, create an exact-subject Validation handoff. Static fixtures can prove only static reconstruction properties and cannot be promoted to real-runtime PASS.

`LOCAL_ENV=NOT_REQUIRED` for L2 Freeze.

## 16. L2 Freeze decision

**FROZEN.**

v4.7 architecture is frozen as:

```text
canonical manifest extension
+ Authority/Applicability Entry metadata
+ qualified State-Dimension/Forbidden-Inference metadata
+ compatible reference conventions
+ derived progressive-disclosure routing
+ executable semantic conformance
+ fresh-Agent dogfood
```

with exactly two new default metadata families and no global lifecycle/state/object collapse.
