# v4.2.0 L3 Reference Packs — Evolution Governance

Status: **IMPLEMENTATION REFERENCE — subordinate to Frozen PRD/L2/Task DAG**

## T01 — Shared Evolution Machine Contracts

### Tests
- both new schemas validate against Draft 2020-12;
- operation and compatibility outcome cannot collapse to one field;
- compatibility dimensions accept recommended names and project-defined extension;
- absent dimension never implies compatible;
- migration transition requires source/target identity and recovery strategy/ref;
- transition schema has no Gate PASS/FAIL authority;
- historical v4 payloads remain valid when optional refs are absent.

### Contract
- `compatibility-record-v1` binds contract, baseline, candidate, operations, dimension outcomes and optional producer/consumer evidence;
- `migration-transition-v1` binds source/target state, ordered mechanism/dependencies, applicability and recovery;
- both are domain records, not Validation/Release states.

### Implementation
Prefer additive optional schema references. Do not make all repositories emit these records.

### Failure handling
Schema contradiction or backward-compatibility regression = Task FAIL; unresolved current-owner conflict = BLOCKED/architecture escalation.

## T02 — Interface & Compatibility Governance

### Tests
- wire-safe does not imply source/application compatibility;
- schema compatibility does not imply behavioral compatibility;
- operation kind and compatibility outcome are independent;
- new/new producer-consumer PASS cannot prove old/new pair;
- unknown/unexecuted dimension stays UNKNOWN/NOT_RUN through owning evidence;
- generated SDK/codegen cannot become canonical contract authority;
- deprecation/removal requires identified authority/baseline.

### Contract
Single normative owner for interface baseline identity, material change operations and compatibility outcomes by dimension.

### Implementation
Use protocol-neutral semantics and examples for HTTP/schema, Protobuf/RPC, CLI/SDK/config/file format. Keep concrete tools as references, not mandates.

### Failure handling
Insufficient consumer/baseline evidence must not be upgraded to compatible. Report UNKNOWN/BLOCKED through appropriate owner.

## T03 — Data & Migration Governance

### Tests
- fresh install != upgrade;
- A→B != B→A;
- successful upgrade != interrupted-transition recovery;
- environment/database tuple cannot be substituted;
- no down migration may still have valid backup/restore or forward-repair recovery;
- migration-file presence != executed migration;
- production credential capability != production mutation authority.

### Contract
Single normative owner for persistent-state transition identity/order/dependencies/applicability/recovery strategy.

### Implementation
Provider/database neutral. Examples should include SQLite/local and PostgreSQL-like stateful runtime without making either universal.

### Failure handling
Required real transition not executed => NOT_RUN/BLOCKED under Validation, never synthesized PASS.

## T04 — API/Service Conformance & Dogfood

### Tests / fixtures
At minimum one positive additive case and adversarial cases for wire-vs-source, behavior-vs-schema and old-consumer compatibility.

### Contract
No new normative owner. Fixtures consume T01/T02.

### Implementation
Prefer deterministic local fixtures when sufficient. Real external service is only required if the chosen acceptance claim depends on provider behavior.

### Failure handling
Fixture weakness is a test defect, not compatibility PASS.

## T05 — Stateful DB Conformance & Dogfood

### Tests / fixtures
- initialize supported source state with representative data;
- run A→B transition;
- assert data/contract preservation;
- exercise at least one failure/interruption/recovery path;
- distinguish fresh bootstrap;
- test non-down recovery strategy;
- bind actual database/runtime/environment tuple.

### Contract
No new normative owner. Fixtures consume T01/T03 and v4.1 External System/Validation semantics.

### Implementation
Use deterministic local DB if adequate. If real DB execution is necessary, create local Validation handoff with exact subject and cleanup authority.

### Failure handling
Unavailable required DB/runtime => BLOCKED, not product FAIL/PASS.

## T06 — Adoption & Wiring

### Tests
- manifest discovers both normative owners and both schemas;
- optional adoption remains optional for non-material projects;
- Validation/Release references do not steal domain ownership;
- v4.4 remains deployment owner;
- historical payload/adopter compatibility retained.

### Contract
Central discoverability/adoption only.

### Implementation
Update `standard-manifest.json`, project override guidance and minimal cross-standard links. One concern: wiring, not semantic redesign.

## T07 — Cross-standard Conformance / Closure Inputs

### Tests
Negative families from Frozen PRD/L2; Fast Path; historical compatibility; owner uniqueness; exact identity/currentness; v4.4 boundary.

### Contract
Integration/conformance evidence only; Version Closure/Release Qualification remain existing owners.

### Implementation
Aggregate focused suites without making one giant custom state machine. Produce durable evidence summary for Closure.

### Failure handling
Any P0/P1 semantic inference defect blocks v4.2 closure; environment-only blockers remain truthful BLOCKED with explicit handoff if required.