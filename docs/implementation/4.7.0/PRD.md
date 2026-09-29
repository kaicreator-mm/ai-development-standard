# ai-development-standard v4.7.0 PRD — AI-native Development Convergence & Repository Refactor

Status: **DRAFT PRODUCT AUTHORITY — requires L1 Product Evidence review and explicit PRD Freeze before implementation**

## 1. Product intent

v4.7.0 is the convergence/refactor release for the complete v4 series. Its purpose is not primarily to add more development capabilities. It restructures, normalizes and self-validates the repository so v4.0–v4.6 capabilities form one coherent AI-native Development Standard rather than a growing collection of individually good but partially overlapping documents.

The final product should allow a capable Agent with no prior chat/session history to read the repository and determine, from durable facts:

1. What standards apply to this project/version/task?
2. Which document/object owns each semantic concern?
3. What is Product, Architecture, Planning, Execution, Assurance, Release, Deployment and Operations authority?
4. Which states belong to which lifecycle dimension and which inferences are prohibited?
5. Which machine contracts, profiles and project overrides apply?
6. What may the Agent decide autonomously, what requires escalation, and what must never be inferred?
7. How can the complete lifecycle be executed and reconstructed without hidden conversational context?

## 2. Problem

Incremental evolution from v4.0 through v4.6 is expected to add many standards, schemas, profiles, templates, checklists and compatibility entries. Without an explicit convergence release, the repository risks:

- duplicate normative rules across multiple files;
- multiple documents appearing to own the same semantic concern;
- inconsistent terminology and state names;
- prose/schema/template/checklist drift;
- Agent context overload and poor discoverability;
- historical compatibility files retaining stale normative text;
- language/archetype/project profiles composing ambiguously;
- AI-native governance remaining scattered across role/handoff/execution documents;
- repository structure reflecting chronological growth rather than the final conceptual model.

## 3. Scope

### 3.1 Unified Canonical Meta Model

Define one conceptual model covering at least:

```text
Intent
Product Authority
Architecture Authority
Planning Authority
Task / Task DAG / Task Pack
Execution Pack / Dispatch / Agent
Git / Toolchain / Config / Workspace / External Systems
Implementation
Testing / Review / Validation
Build / Artifact
Candidate / Release
Deployment
Runtime / Observability
Incident / Recovery
Maintenance / EOL
Feedback / Evolution
```

The model must clearly distinguish authority, immutable identity, derived state and local observations.

### 3.2 Unified Authority Map

Establish one repository-visible authority registry answering:

```text
semantic concern → normative owner
```

Core invariant:

> One semantic concern has one normative owner. Other documents may reference, summarize or map it, but must not create competing authority.

v4.7 must audit and resolve duplicate ownership across standards, README, AGENTS, templates, checklists, schemas and compatibility entries.

### 3.3 Unified State Taxonomy

Normalize states by dimension rather than creating one overloaded global state machine.

At minimum distinguish:

```text
Work Item / Task State
Dispatch / Execution State
Gate / Validation State
Review Result
Candidate State
Release Verdict
Deployment State
Runtime / Incident State
Maintenance / Support State
```

Required non-inference examples include:

```text
Task DONE != Validation PASS
PR merged != Release READY
Release READY != Deployment SUCCESS
Deployment SUCCESS != Runtime Healthy
worktree exists != Task RUNNING
old-SHA PASS != successor-SHA PASS
```

Schemas, prose and examples must agree on these boundaries.

### 3.4 Standard Document Contract

Refactor normative documents toward one consistent structure, where applicable:

```text
1. Purpose
2. Scope
3. Non-goals
4. Terminology
5. Authority
6. Canonical durable facts
7. Required semantics
8. Agent MUST / MUST NOT
9. Evidence
10. Validation / assurance integration
11. Exceptions / waivers
12. Capability fallback
13. Machine contract
14. Conformance tests
15. Migration / adoption
16. References
```

Not every document must mechanically contain empty sections; the objective is predictable semantics and discoverability rather than formatting bureaucracy.

### 3.5 Repository Information Architecture Refactor

Evaluate and, if evidence supports it, reorganize repository content into coherent domains such as:

```text
standards/
  lifecycle/
  execution/
  engineering/
  evolution/
  delivery/
  operations/
  ai-native/

profiles/
  languages/
  archetypes/
```

Existing stable paths required by adopters should retain compatibility entries/pointers during the v4 line. Path reorganization MUST NOT silently break pinned adopters.

### 3.6 Standard Manifest / Progressive Disclosure

Introduce a canonical machine-readable or deterministic top-level manifest/resolver so Agents do not need to scan the entire repository to discover authority.

The effective resolution path should approximate:

```text
repository AGENTS / .dev-standard/VERSION
        ↓
pinned ADS revision
        ↓
Standard Manifest / authority registry
        ↓
project adoption + PROJECT_OVERRIDES
        ↓
applicable lifecycle/execution standards
        ↓
language/archetype profiles
        ↓
Task/Execution-specific authority
```

The design should follow progressive disclosure: read only the standard/profile material required for the current operation while preserving deterministic authority.

### 3.7 Machine Contract Convergence

Audit schemas/events/manifests introduced through v4.x for:

- naming consistency;
- identity fields;
- exact-SHA/tree/artifact bindings;
- state/value reuse;
- override/precedence semantics;
- compatibility/version markers;
- duplicated fields representing the same concept;
- prose/schema mismatch.

Prefer extending canonical shared concepts over parallel schemas with subtly different meanings.

### 3.8 Unified Conformance Suite

Build a cross-standard conformance suite that tests semantic invariants, not only JSON Schema syntax.

Required negative families should include examples such as:

```text
PR PASS → Release PASS                 MUST fail
old SHA Validation → new SHA PASS      MUST fail
mock PASS → real external PASS         MUST fail
worktree exists → Task RUNNING         MUST fail
Agent overrides Frozen Architecture    MUST fail
waiver → PASS                          MUST fail
Release READY → Deployment SUCCESS     MUST fail
fresh DB PASS → upgrade PASS           MUST fail
```

Conformance should cover normative owner uniqueness, authority precedence, state separation, schema/prose compatibility and profile/override resolution.

### 3.9 Compatibility & Migration Layer

v4.7 must provide a clear migration/adoption path from earlier v4 releases:

- stable path compatibility entries where needed;
- deprecated path/term inventory;
- schema compatibility/migration notes;
- project adoption guidance;
- no retroactive rewriting of historical evidence;
- explicit distinction between compatibility alias and canonical authority.

### 3.10 Self-hosting / Dogfood

v4.7 development must use the v4.7 candidate model to develop and validate itself as far as practicable:

```text
Product
→ Architecture
→ Task DAG
→ Task Packs / Execution
→ Git/Toolchain/Context/Profile resolution
→ Testing / Review / Validation
→ Build / Release / Deployment simulation where applicable
→ Operations/incident feedback simulation
```

Dogfood findings are first-class product evidence. Any point where a fresh Agent cannot locate authority, resolve context, reconstruct state or execute safely is a v4.7 product defect or an explicitly documented non-goal.

## 4. SemVer / breaking-change boundary

v4.7 is intended as a convergence release inside the v4 compatibility line.

Allowed:

- directory reorganization with stable compatibility pointers;
- terminology normalization with aliases/migration guidance;
- additive schemas/manifests/resolvers;
- duplicate-rule removal while preserving semantics;
- stronger conformance that exposes invalid interpretations not actually authorized by prior v4 rules.

Not allowed to be silently introduced as v4.7:

- incompatible core authority hierarchy changes;
- incompatible lifecycle semantics that make compliant v4 projects invalid without migration;
- destructive schema/wire changes without compatibility path;
- rewriting historical evidence meanings.

If convergence demonstrates that a truly incompatible architecture is required, v4.7 must document/prepare the migration and route the breaking semantic change to a future **v5.0** rather than forcing it into v4.7.

## 5. Non-goals

v4.7 does not:

- add another major functional domain merely because one is interesting;
- replace all standards with one giant document;
- eliminate domain-specific standards/profiles;
- centralize every workflow into one state machine;
- remove compatibility solely for repository aesthetic cleanup;
- require all projects to adopt every optional capability;
- turn ADS into a specific CI/orchestrator/IDE/runtime product.

## 6. Final target architecture

The v4.7 repository should express a coherent layered model approximately like:

```text
Lifecycle
Product → Architecture → Planning → Implementation → Assurance → Release → Deployment → Operations

Execution Foundation
Git / Dependency / Toolchain / Config / Workspace / External Systems

Evolution
Interface / Compatibility / Data / Migration

Engineering
Architecture Design / Task Decomposition / DAG Governance / Implementation Profiles / Testing

AI-native Vertical
Intent / Context / Skills / Autonomy / Provenance / Assurance / Handoff / Recovery

Profiles
Language + Archetype + Project Overrides

Machine Layer
Manifest / Schemas / Events / Conformance / Resolver
```

This is a conceptual target; L2 may choose a different physical directory arrangement if it better preserves compatibility and discoverability.

## 7. Product acceptance

v4.7.0 is complete when:

1. every material semantic concern has one discoverable normative owner;
2. authority/state terminology is consistent across prose, schemas, templates and examples;
3. a top-level manifest/resolution path lets an Agent discover applicable standards without repository-wide guessing;
4. stable v4 adopters retain a documented compatibility path;
5. no required project truth depends on historical chat context;
6. negative conformance rejects known cross-layer inference shortcuts;
7. a fresh high-capability Agent can reconstruct and execute a representative project lifecycle using only durable GitHub/repository facts;
8. v4.7 self-dogfood completes with explicit findings and disposition;
9. unresolved breaking semantic changes are separated into a future-major migration plan rather than hidden in v4.7.

## 8. Success criterion

The principal end-state test is:

> A capable Agent that has never participated in the project can read the repository and durable GitHub facts, determine which standards apply, understand the current lifecycle/authority/state, know its permitted autonomy and required evidence, execute or escalate correctly, and hand off without relying on prior chat memory.

## 9. Next gate

Before Freeze:

1. complete v4.1–v4.6 or establish stable candidate authorities sufficient for convergence design;
2. run L1 Product Evidence focused on standards architecture, progressive disclosure, schema governance and self-hosted Agent development;
3. perform full repository authority/duplicate/information-architecture inventory;
4. revise and explicitly Freeze this PRD;
5. run L2 Architecture Evidence with compatibility/migration constraints;
6. generate a Task DAG separating inventory/meta-model/repository-refactor/schema/conformance/dogfood lanes with an explicit convergence task.
