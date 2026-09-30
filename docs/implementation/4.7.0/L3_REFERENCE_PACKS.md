# v4.7.0 L3 Reference Packs — AI-native Development Convergence

Status: **FROZEN L3 IMPLEMENTATION REFERENCE — 2026-09-30**

Authority chain:

- Frozen Product `d4f90e1432b53fe0d30d4673674280f3c5e586ec`
- Frozen L2 `8a0687807e1c5ec7c415b0031862b0e367c44507`
- Frozen Task DAG `754f76ecd452abb654f9b35fdbb52acd12e9954b`

This pack is implementation guidance subordinate to each Frozen Task Pack. It does not enlarge any Task write-set.

## Shared invariants

Every task must preserve:

```text
registry/discovery != mutation authority
qualified state metadata != live state authority
same token != same state semantics
reference convention != universal replacement object
read routing != context snapshot authority
CI PASS != Validation/Review/Release PASS
old exact-SHA evidence != successor exact-SHA evidence
compatibility alias != duplicate normative owner
technical necessity != Task Pack write authority
```

Historical payloads/manifest consumers remain valid unless an explicit compatible migration is authorized.

## T01 — Convergence Metadata Contracts

### Tests

- Authority/Applicability Entry contract is closed/bounded and contains only discovery metadata;
- canonical owner ref is required while normative rules/body are absent;
- State-Dimension Registry distinguishes dimension identity, owner and vocabulary posture;
- forbidden-inference entries bind source fact/dimension to prohibited target conclusion;
- neither family contains mutation/merge/side-effect/Validation/Release authorization;
- historical `standard-manifest.json` remains valid without the optional semantic registry.

### Contract

Implement the minimum shapes selected by L2. Keep versioning additive. Avoid `$defs`/schema features unsupported by repository verification unless existing verifier support is proven.

### Failure handling

If a proposed field would duplicate owner semantics or live state, stop and route to L2 amendment rather than broadening T01.

## T02 — Authority / Applicability Manifest Registry

### Tests

- existing `sections` inventory is preserved;
- every semantic entry resolves to one existing canonical owner path;
- duplicate competing owner entries fail;
- registry presence does not authorize mutation;
- optional/non-applicable tags do not create mandatory adoption;
- compatibility aliases point to canonical owners without becoming owners.

### Implementation

Prefer additive semantic metadata within canonical `standard-manifest.json`. Add focused verifier/conformance code rather than a second canonical registry file.

### Failure handling

Broken target, duplicate owner or materially ambiguous applicability fails closed.

## T03 — State-Dimension / Forbidden-Inference Registry

### Tests

Cover at least work-item, Dispatch, Execution Pack, Validation, Review, Release, Deployment, Runtime/Incident/Maintenance and provider availability dimensions where current owners expose them.

Required negatives include:

- Task DONE -> Validation PASS;
- Review PASS -> Validation PASS;
- Validation PASS -> Release READY;
- Release READY -> Deployment SUCCESS;
- Deployment SUCCESS -> Runtime Healthy;
- provider/tool AVAILABLE -> mutation authority;
- old exact-SHA PASS -> successor PASS;
- mock/sandbox PASS -> real-environment PASS.

### Failure handling

Do not invent state vocabulary not owned by the source contract. Open/extensible vocabularies remain marked open.

## T04 — Reference Convention Standard

### Tests

- exact SHA and expected base semantics remain consistent;
- mutable refs cannot replace exact subject identity when material;
- authority refs point to durable authority rather than capability;
- evidence refs do not transfer PASS across subjects;
- provenance pointers remain evidence, not normative owner;
- no universal Subject/Authority object is required.

### Failure handling

Cosmetic naming differences alone do not justify schema rewrite. Incompatible normalization becomes future-major input.

## T05 — Progressive Disclosure Routing

### Tests

Build table-driven scenarios from fresh project context through pinned standard, semantic registry, overrides, profiles and task authority. Include stale lower-authority memory/chat and material ambiguity negatives.

### Implementation

A derived read plan/debug trace may be emitted, but no durable Context Snapshot family. Current durable authority wins.

### Failure handling

Ambiguous owner/applicability or missing exact task authority returns a fail-closed routing result/reference to human/planning authority; never pick by file order or model preference.

## T06 — Compatibility / Alias Conformance

### Tests

- every compatibility entry resolves to a canonical target;
- alias cycles/broken targets fail;
- old stable path can remain discoverable without duplicate normative ownership;
- registry canonical target and compatibility entry agree;
- no path move is required merely to make tests green.

### Failure handling

Required path migration needs explicit compatibility plan/authority; this task cannot move normative files on its own.

## T07 — Unified Semantic Conformance

### Tests

Compose T01–T06 plus prior v4.1–v4.6 forbidden inferences. Include mutation-authority regression from #281 and exact-currentness drift cases.

### Implementation

Prefer deterministic repository tests that fail with precise owner/dimension/rule identity. Conformance outcome remains Testing/Validation evidence under existing standards.

### Failure handling

A Product/L2 contradiction triggers planning amendment; an implementation defect remains in the owning Task.

## T08 — Fresh-Agent Self-Dogfood

### Scenario

A fresh logical Agent receives only durable repository/GitHub pointers and must recover:

1. pinned ADS/current project authority;
2. canonical owner(s) for the requested concern;
3. applicable profiles/overrides;
4. current Task/PR/exact SHA/base;
5. allowed write-set/side effects;
6. required Validation/Review gates;
7. next action or blocker.

### Negatives

- no hidden use of prior chat/session knowledge;
- transport-account sameness cannot be claimed as logical independence;
- static fixture does not prove external runtime capability;
- stale issue/PR/currentness must be detected.

## T09 — Adoption / Migration Wiring

### Tests

- project bootstrap discovers v4.7 metadata without requiring all optional capabilities;
- checklists route users to canonical owners rather than duplicating semantics;
- future-major register is discoverable;
- stable aliases remain supported;
- no central wiring path is modified unless explicitly authorized by T09.

## T10 — Cross-standard Closure Inputs

### Tests

Run integrated v4.1–v4.7 semantic regressions, historical compatibility/adoption cases, Fast Path/non-applicability scenarios, and fresh-Agent reconstruction evidence.

### Deliverables

Produce durable closure-input evidence only. Version Closure/Release Qualification remains a separate authority/gate.
