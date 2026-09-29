# v4.7.0 Authority / State / Schema Convergence Inventory

Status: **REFRESHED FINAL PRE-FREEZE INVENTORY — non-normative**

Refresh date: 2026-09-30
Current canonical main: `bc3feeccf130fcfc7b49efaf44983e4dcdac6e5d`

This inventory records the semantic-owner, state-dimension and machine-contract shape after v4.1–v4.6 Product/L2 authorities became sufficiently stable for final v4.7 Product-currentness review. It does **not** authorize implementation, path migration, schema replacement, state collapse or historical reinterpretation.

## 1. Convergence premise

The repository already has the major mechanisms v4.7 needs:

- `standard-manifest.json` for canonical asset discovery;
- root `AGENTS.md` for progressive-disclosure/read routing;
- explicit Product / Architecture / Task / Task Pack / Execution authority precedence;
- compatibility-entry patterns for stable legacy paths;
- machine contracts for Operation, Dispatch, Execution Pack, Assurance, Review, Validation and related claims;
- exact-SHA/currentness rules and strong non-inference boundaries.

The convergence problem is therefore **discoverability and semantic consistency**, not absence of a universal state object.

## 2. Refreshed semantic-owner map

### Core lifecycle / assurance owners

- Product/L1/PRD Freeze — Development Workflow / Product authority;
- Architecture/L2 — Architecture evidence/freeze authority;
- Task decomposition / Task DAG / Task Pack — planning authorities, with GitHub Issue Dependencies as live DAG after materialization;
- Implementation execution — Execution Pack / Dispatch / Git and Task authority;
- Testing — Testing Standard;
- Validation — Validation Standard / validation-report;
- Review / assurance — Assurance Plan + Review aggregation / Review standards;
- Release Qualification — Release Standard.

### v4.1 Execution Foundation

Distinct owners:

- Dependency & Toolchain Governance;
- Git Execution & Worktree Isolation;
- Configuration & Secrets Governance;
- Workspace & Artifact Governance;
- External System Execution.

Execution Context is non-authoritative reconstruction/evidence, not a second workflow state machine.

### v4.2 Evolution Governance

Distinct owners:

- Interface & Compatibility Governance;
- Data & Migration Governance.

Machine families:

- Compatibility Record;
- Migration Transition.

Compatibility outcome is multi-dimensional and does not become Validation PASS. Migration source→target/recovery does not become Deployment or Incident authority.

### v4.3 Engineering Design & Implementation Profiles

Distinct owners include:

- Architecture Design;
- Task Decomposition;
- Task DAG Governance;
- Implementation Quality;
- subordinate Language and Archetype Profiles.

GitHub Issue Dependencies remain live execution DAG; profiles do not become a repository-wide v4.7 resolver.

### v4.4 Build / Packaging / Deployment

Distinct owners:

- Build & Artifact Governance;
- Distribution Governance;
- Deployment Governance.

Machine families:

- Build Manifest;
- Artifact Promotion;
- Deployment Plan;
- Deployment Result.

`Release READY != Deployment SUCCESS`; artifact rollback != data migration rollback.

### v4.5 Operations / Incident / Maintenance

Distinct owners:

- Observability & Runtime Evidence;
- Incident / Recovery / Engineering Feedback;
- Maintenance / EOL / Hotfix.

Machine families:

- Runtime Observation Context;
- Incident Event;
- Maintenance Policy.

Deployment success does not imply runtime health. Incident recovered does not imply permanent fix/follow-up closure. Backported SHA does not inherit source SHA Validation.

### v4.6 AI-native / Agentic Governance

Frozen Product `e6aa04981110376e623d19b7dd4d0c6d0e139bdf`; Frozen L2 `f47ea81e8f8df32ac6c8b7cc922c405a17b704d9`.

Exactly three new owners:

- Intent & Assumption Governance;
- Context Engineering;
- Skill / Reusable Agent Procedure Governance.

Exactly two new default machine families:

- Intent / Assumption Record;
- Skill Metadata.

No Context Snapshot database/family and no duplicate Assurance, autonomy, Dispatch/Handoff, Validation or Release result state.

## 3. Authority uniqueness rule

v4.7 should make the map `semantic concern -> one canonical normative owner` machine-discoverable where useful.

A registry entry may contain:

```text
semantic_concern
canonical_owner
applicability_tags
machine_contract_refs
compatibility_aliases
read_routing / progressive-disclosure tags
supersession / migration metadata
```

The registry itself is **discovery metadata**. It MUST NOT silently become a second copy of each owner's normative semantics.

## 4. Qualified state dimensions

The following state/result vocabularies remain separate claim dimensions even when strings overlap.

### Work-item/router state

```text
planned
ready
implementing
review-ready
reviewing
changes-requested
validation-needed
merge-ready
blocked
done
```

### Dispatch lifecycle

```text
READY
CLAIMED
RUNNING
COMPLETED
BLOCKED
SUPERSEDED
```

### Execution Pack currentness

```text
PACK_CURRENT
PACK_STALE_NONMATERIAL
PACK_STALE_MATERIAL
PACK_INVALID
```

### Validation state

```text
PASS
FAIL
BLOCKED
NOT_RUN
NOT_APPLICABLE
```

### Review judgment

```text
PASS
CHANGES_REQUESTED
VALIDATION_REQUESTED
BLOCKED
```

### Candidate / Release / Deployment / Runtime / Incident / Maintenance

These remain their owning dimensions. Similar labels such as READY, PASS, BLOCKED, SUCCESS, RECOVERED or SUPPORTED do not collapse their meanings.

**Frozen convergence direction:** qualify state by owner/dimension rather than deduplicate equal strings into one global enum.

## 5. Cross-dimension forbidden-inference registry

At minimum v4.7 conformance must preserve these negatives:

```text
work item done != Validation PASS
PR merged != Release READY
Review PASS != Validation PASS
Validation PASS != Release READY
Release READY != Deployment SUCCESS
Deployment SUCCESS != Runtime Healthy
Dispatch COMPLETED != product/release PASS
PACK_CURRENT != implementation correct
old exact-SHA PASS != successor exact-SHA PASS
provider/tool/credential AVAILABLE != mutation authority
waiver/exception != PASS
fresh install PASS != upgrade PASS
wire/schema compatible != behavior/source/consumer compatible
mock/sandbox PASS != higher-fidelity PASS
artifact alias/tag != immutable artifact identity
incident RECOVERED != permanent defect/follow-up closed
branch/package exists != maintenance-supported
Skill installed/capable != trusted/authorized
Intent/Assumption record != Frozen Product authority
historical chat/memory != current durable authority
```

## 6. Machine-contract convergence

Recurring machine concepts include:

```text
repository / version / task / issue / PR
subject_ref / subject_identity_ref
exact/requested/tested/current SHA
expected base
operator / executor / session / context refs
provider/model provenance
validation tuple/profile/environment/toolchain
state/result/judgment
```

Repeated fields are not automatically duplication defects because each record owns a different claim.

v4.7 may standardize **reference conventions** such as subject identity, authority reference, applicability and provenance pointers, but MUST preserve object ownership and historical wire meaning.

Candidate convergence targets:

- common Subject Identity reference vocabulary;
- common Authority Reference convention;
- qualified state-dimension metadata;
- optional applicability/read-routing tags;
- compatibility alias/canonical-target metadata.

Non-targets:

- one universal event/result object;
- one master state enum;
- rewriting historical Validation/Review/Dispatch payloads;
- converting correlation objects into normative authority.

## 7. Assurance / provenance / handoff relationship

`assurance-plan-v1` already owns activity policy, independence dimensions and open coverage. `review-aggregation-v1` already owns Review judgment/finding aggregation and can carry reviewer provider/model/executor/context provenance. Dispatch already owns executable handoff; Execution Pack owns Task execution identity.

v4.6 correctly reuses these rather than creating a new AI Assurance/Handoff state family.

v4.7 may improve discoverability/naming/reference consistency, but MUST NOT create a duplicate assurance or Agent lifecycle merely for symmetry.

## 8. #281 authority-repair lesson

Fresh Independent Review #281 on v4.1 T07 found a concrete planning-authority defect: a technically required Golden coverage file was modified without being present in the Frozen Task Pack allowed write-set.

This is important convergence evidence:

- Task Pack remains durable mutation authority;
- a registry/discovery layer MUST NOT imply mutation authority;
- technical necessity, CI PASS or Validation PASS does not retroactively create write authority;
- authority amendments must be explicit/current and scoped;
- current repair path is #285 / PR #286 / Fresh Review #288.

The finding does **not** reveal a semantic-owner contradiction in v4.1 Product/L2 and therefore does not justify redesigning the owner map.

## 9. Repository information architecture

The flat `standards/` layout is increasingly crowded, but stable paths are valuable compatibility surfaces.

Current evidence supports this order:

1. improve concern→owner discovery through manifest/registry metadata;
2. improve progressive disclosure/read routing;
3. inventory all stable paths and downstream aliases;
4. move/rename files only when evidence shows material benefit exceeding compatibility cost;
5. retain compatibility aliases/entries for any stable path migration.

Aesthetic directory cleanup alone is not sufficient reason for a breaking refactor.

## 10. Compatibility-entry and migration posture

Existing compatibility entries demonstrate the preferred migration shape:

```text
old stable path -> compatibility entry / alias -> canonical owner
```

v4.7 may formalize canonical-target metadata and deprecation/sunset evidence, but must not remove aliases merely because the registry can point elsewhere.

## 11. Progressive disclosure

Root `AGENTS.md` already routes readers by operation/role and avoids unconditional repository-wide loading. v4.6 Context Engineering freezes the same principle at the AI-native layer.

v4.7 should make this routing more deterministic through registry tags, not replace it with a “load everything” context snapshot.

## 12. Future-major / v5 register

The following remain outside additive/non-weakening v4.7 if they prove necessary:

- collapsing state dimensions into one enum/state machine;
- replacing dispatch/event protocol incompatibly;
- changing Product/Architecture/Task/Task Pack authority precedence;
- deleting/moving stable normative paths without compatible aliases/migration;
- changing exact-SHA evidence semantics;
- changing Review/Validation/Release/Deployment result semantics incompatibly;
- reinterpreting historical events/payloads;
- mandatory adoption of optional capabilities;
- destructive role/object renames requiring downstream simultaneous migration.

If required, v4.7 should produce explicit v5 migration inputs instead of hiding the break inside “convergence.”

## 13. Final pre-Freeze verdict

Current evidence supports a narrowed v4.7 Product centered on:

- authority/applicability discovery;
- qualified state dimensions and forbidden-inference registry;
- compatible machine reference conventions;
- progressive disclosure;
- compatibility-preserving repository IA;
- integrated semantic conformance/self-dogfood;
- future-major separation.

Current evidence does **not** support a global state machine, object collapse, mandatory physical directory refactor, historical reinterpretation or incompatible v4 wire rewrite.

`LOCAL_ENV=NOT_REQUIRED` for this inventory. The next gate is a Fresh Independent final L1/currentness review before any explicit v4.7 Product Freeze.
