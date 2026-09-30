# v4.6.0 L2 Architecture Evidence — AI-native / Agentic Development Governance

Status: **FROZEN L2 — 2026-09-30**

Frozen Product Authority: `e6aa04981110376e623d19b7dd4d0c6d0e139bdf`

Independent Product-currentness authorization: #280 PASS on `planning/v4.6-l1-ai-native@9b168097cadeb36784f937f645d087a4e7da5d17` against `main@bc3feeccf130fcfc7b49efaf44983e4dcdac6e5d`.

## 1. Architecture question

How should v4.6 make AI-native intent, context and reusable procedures durable enough for independent Agents **without** creating a second Product/Task/Dispatch/Review/Validation/Release state model or duplicating the semantic owners introduced in v4.1–v4.5?

The architecture must support session/model/operator replacement while preserving authority truth and must remain additive/non-weakening inside v4.

## 2. Evidence inspected

Repository evidence establishes that major AI-native concerns already have durable owners:

- `schemas/assurance-plan-v1.schema.json` already owns assurance activities, risk/policy/mode, independence dimensions, model-diversity basis and open `coverage` strings;
- `schemas/review-aggregation-v1.schema.json` already owns Review aggregation/judgment and can record reviewer provider/model/executor/context provenance;
- `schemas/dispatch.schema.json` already owns executable builder/validator/reviewer handoff, F0–F3 freedom, exact base/head identity and task/execution-pack pointers;
- `schemas/execution-pack-manifest.schema.json` already owns Task execution-pack identity, dependency completion, material paths and pinned standard revision;
- existing GitHub Issue/PR/exact-SHA facts remain durable execution currentness surfaces;
- #280 independently confirmed v4.1–v4.5 Product/L2 owner boundaries and found no material semantic-owner contradiction requiring v4.6 to wait for all upstream implementation completion.

The machine architecture therefore follows **reuse/extension first**.

## 3. Frozen architecture decision

v4.6 adds three normative owner documents but only **two new default machine-contract families**.

### 3.1 Normative owners

1. `INTENT_ASSUMPTION_GOVERNANCE_STANDARD`
2. `CONTEXT_ENGINEERING_STANDARD`
3. `SKILL_PROCEDURE_GOVERNANCE_STANDARD`

These are semantic owners, not lifecycle stages.

### 3.2 New default machine-contract families

1. **Intent / Assumption Record v1**
   - durable identity for material intent/interpretation/assumption/unknown distinctions;
   - source/subject reference;
   - classification and materiality;
   - disposition/promotion routing references;
   - authority/evidence refs for any promotion;
   - contradiction/supersession references where relevant.

2. **Skill Metadata v1**
   - reusable procedure identity/version/source/maintenance owner;
   - purpose/scope/applicability;
   - required authority/input refs;
   - allowed tools and side-effect classes as capability declarations, not authorization;
   - output/durable result surface;
   - failure/escalation semantics;
   - validation/evaluation/compatibility/deprecation/security/provenance refs.

### 3.3 No default Context Snapshot contract

v4.6 does **not** create a full `context-snapshot` or repository-wide context database.

Effective context is reconstructed from durable current authorities and references already owned by Product/L2/Task Pack/Execution Pack/Dispatch/Issue/PR/source/evidence. A complete snapshot would be easy to stale, expensive to maintain and likely to become a competing authority surface.

When a material action needs context provenance/currentness, it records **references**, not a copied repository/chat dump.

## 4. Intent / Assumption Record architecture

The machine record is a durable **domain fact**, not Product authority and not a workflow result.

Minimum conceptual fields:

```text
protocol_version
record_id
subject_ref
source_ref
classification = USER_INTENT | INTERPRETATION | ASSUMPTION | UNKNOWN | DECISION_REQUIRED | DURABLE_REQUIREMENT_REF
materiality
statement_ref | statement_digest
created_by_ref
created_at_ref
currentness_ref

disposition
  action = RETAIN | ROUTE | REJECT | PROMOTE_REF | SUPERSEDE_REF
  authority_ref?
  evidence_refs[]
  target_ref?

contradiction_refs[]
supersedes_refs[]
notes_ref?
```

`DURABLE_REQUIREMENT_REF` does not mean the record itself created a requirement. It means the record points to a requirement already promoted by the existing Product/Architecture/Task authority path.

Forbidden machine inference:

```text
classification=USER_INTENT -> Frozen Product
classification=INTERPRETATION -> user fact
classification=ASSUMPTION/UNKNOWN -> durable requirement
action=PROMOTE_REF -> promotion valid without authority_ref + target authority fact
```

## 5. Context Engineering architecture

Context resolution is deterministic **precedence + currentness + progressive disclosure**, not a new state machine.

### 5.1 Precedence invariant

Current higher-authority durable facts beat stale/lower-authority historical context. At minimum:

```text
system/organization constraints
  > pinned/current project standard and overrides
  > Frozen Product / Frozen Architecture
  > Task DAG / Task Pack / Execution Pack / Dispatch
  > current Issue / PR / exact source/test/evidence facts
  > approved external evidence/resources
  > historical chat / memory
```

This ordering does not let a lower level overwrite a higher level merely because it is newer.

### 5.2 Currentness invariant

Before exact-currentness-sensitive actions, the executor re-reads the live identity needed for that action, such as:

- PR HEAD/base;
- version branch SHA;
- open/closed dependency state;
- current Frozen authority ref;
- live side-effect target/environment where applicable.

Historical context is useful background but cannot substitute for this read.

### 5.3 Progressive disclosure

Agents should load the minimum sufficient authoritative context first and expand only when uncertainty, dependency, conflict, or task scope requires it.

`larger context dump -> higher context quality` is explicitly false.

### 5.4 Existing machine surfaces reused

No new context schema is required for v4.6 default architecture because:

- Dispatch already identifies repository/version/task/role/base/standard/task pack/execution pack;
- Execution Pack already identifies task, base, dependencies, material paths and artifacts;
- reviewer provenance already carries `context_ref` when material;
- GitHub/source/evidence refs can identify the live durable facts.

T01 MAY add narrowly scoped optional `intent_assumption_record_refs` / `skill_refs` / `context_refs` to Dispatch or Execution Pack schemas if implementation proves deterministic discoverability requires named fields. Such fields are references only and remain backward-compatible/optional.

## 6. Skill Metadata architecture

A Skill is reusable procedural content, not Product/Architecture/Task or side-effect authority.

Minimum conceptual fields:

```text
protocol_version
skill_id
version
source_ref
maintenance_owner_ref
purpose
scope
applicability
required_input_refs[]
required_authority_classes[]
allowed_tool_classes[]
side_effect_classes[]
output_contract_refs[]
durable_result_surface_refs[]
failure_route_ref
escalation_ref
validation_refs[]
evaluation_refs[]
compatibility_refs[]
deprecation_ref?
security_refs[]
provenance_refs[]
```

Normative architectural rules:

- possession/installation is capability, not trust or authorization;
- `allowed_tool_classes` describes what the procedure may need, not permission to perform a side effect;
- Task/Execution/Dispatch/External-system authority remains decisive at invocation time;
- imported Skill source/provenance is retained when material;
- secrets and project-only authority are references to owning secure surfaces, not embedded values;
- one-off Task facts remain in Task/Execution authority rather than being copied into Skill metadata.

## 7. Assurance / Review reuse

No new AI-change assurance plan/result schema is created.

Existing `assurance-plan-v1` already provides:

- activity kinds and policies;
- model-diverse-adversarial mode;
- independence requirements;
- free-form coverage dimensions;
- conflict routing.

Existing `review-aggregation-v1` already provides:

- judgment and finding aggregation;
- blocker dominance;
- reviewer model/executor/context provenance.

v4.6 implementation may add AI-native coverage strings such as intent alignment, unsupported assumptions, invented contract/domain semantics, scope/write-set compliance and silent test weakening. No wire change is required merely to name those coverage dimensions.

## 8. Autonomy / Dispatch / Handoff reuse

F0–F3 remains the only Agent freedom vocabulary. Dispatch remains the executable handoff object.

No new autonomy scale, Agent lifecycle state, queue state or handoff result is introduced.

A handoff/session-loss dogfood must prove a fresh Agent can reconstruct:

```text
requested work
frozen/current authority
exact subject identity
completed evidence
open findings/blockers
next owner/action
forbidden assumptions
```

from durable repository/GitHub facts without requiring the lost chat transcript.

## 9. Side-effect authority

Skill installation, tool availability, model capability, credentials, external connection and successful dry-run are all **capability/evidence facts**. None grants side-effect authority.

Actual mutation follows the existing applicable execution/external-system/deployment/production authority.

## 10. Compatibility and historical evidence

v4.6 is additive/non-weakening:

- existing Dispatch/Execution Pack/Assurance/Review payloads remain valid when new optional refs are absent;
- historical events/reviews are not retroactively required to contain Skill/Intent records;
- Product/Architecture/Task precedence is unchanged;
- model/provider provenance remains proportional rather than universally mandatory;
- no historical chat is promoted to authority merely because v4.6 exists.

Any incompatible event/dispatch rewrite or authority-chain change is future-major/v4.7 migration input rather than v4.6 implementation.

## 11. Failure model

Fail closed when required currentness or authority cannot be reconstructed:

| Condition | Required handling |
|---|---|
| material intent interpretation uncertain | preserve `ASSUMPTION` / `UNKNOWN` or route `DECISION_REQUIRED` |
| current Frozen/Task/PR identity unavailable | BLOCKED/currentness handoff; no guessed successor |
| imported Skill trust/provenance unresolved | Skill not trusted for material execution |
| Skill requests action outside current Task/side-effect authority | refuse/escalate; do not self-promote freedom |
| context sources contradict at same authority level | preserve conflict and route to owning authority |
| external evidence unavailable | record missing evidence; do not infer Product truth |

## 12. Implementation decomposition guidance

A later Frozen Task DAG should separate at least:

1. shared machine contracts (Intent/Assumption Record + Skill Metadata + narrowly justified optional refs);
2. Intent & Assumption normative owner;
3. Context Engineering normative owner;
4. Skill/Procedure normative owner;
5. AI-native Assurance/Review/Dispatch/Handoff reference integration, without new owner objects;
6. session-loss / operator-handoff dogfood;
7. adoption/manifest/project-profile wiring;
8. cross-standard conformance / closure inputs.

Tasks 2–4 should be parallel after the shared contract where they consume it; reference integration may be independently parallel if write-sets do not overlap.

## 13. Validation strategy

Concern-level tests must include adversarial negatives for at least:

```text
chat -> Frozen Product
interpretation -> user fact
assumption/unknown -> durable requirement
ephemeral-only truth -> acceptable handoff
historical memory -> override current Git authority
large context dump -> higher quality automatically
Skill installed -> trusted/authorized
Skill tool capability -> side-effect authority
Skill instruction -> override Task/Product authority
model strength -> F3 authority
same transport account -> same logical independent operator
AI code compiles -> intent/domain correctness
model metadata present -> independence automatically proven
Fast Path -> required truth/gate waiver
```

Integration dogfood must include a fresh-session/Agent recovery case bound to durable Issue/PR/SHA/authority facts.

## 14. Local environment posture

`LOCAL_ENV=NOT_REQUIRED` for Frozen L2 and initial normative/schema implementation.

A real multi-Agent/session-loss/tool-capability experiment is required only when a later dogfood Task claims those executable dimensions. If unavailable in Web/CI, create an exact-subject handoff; do not simulate PASS.

## 15. L2 Freeze decision

Architecture is frozen with:

- **3 normative owners**;
- **2 new default machine-contract families**;
- **0 new Context Snapshot / Agent lifecycle / Assurance result families**;
- reuse of existing Dispatch, Execution Pack, Assurance, Review, Validation and authority chains;
- additive optional-reference extensions only where implementation evidence requires deterministic discoverability.

The next authorized planning step is Frozen Task DAG + L3/Task Packs. Product or L2 must be reopened only if implementation/review exposes a material owner or machine-contract contradiction; convenience alone is insufficient.
