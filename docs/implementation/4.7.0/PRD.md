# ai-development-standard v4.7.0 PRD — AI-native Development Convergence

Status: **REVISED DRAFT — L1/inventory complete, Product Freeze BLOCKED until v4.1–v4.6 owner boundaries are stable**

## 1. Product intent

v4.7.0 is the convergence release for the complete v4 series. Its purpose is not to add another major functional domain or collapse all standards into one system. It makes the accumulated v4 standards deterministically discoverable, state-safe, machine-consistent and self-conformant for fresh Agents.

The target end state is:

> A capable Agent with no historical chat can determine the applicable normative owners, current authority/state dimensions, machine contracts/profiles, allowed autonomy and required evidence from durable repository/GitHub facts, then execute or escalate correctly.

## 2. Product shape

L1 narrows v4.7 to four convergence products plus two acceptance mechanisms:

### Convergence products
1. **Canonical Authority / Applicability Registry**
2. **Qualified State-Dimension & Non-Inference Registry**
3. **Machine-contract Identity / Reference Convergence Rules**
4. **Progressive Disclosure + Compatibility-preserving Repository Information Architecture**

### Acceptance mechanisms
5. **Unified Cross-standard Conformance Suite**
6. **Self-dogfood + Future-major Migration Register**

v4.7 does not create a new global lifecycle owner over all domain standards.

## 3. Canonical Authority / Applicability Registry

Extend the existing `standard-manifest.json` model so a fresh Agent can resolve at least:

```text
semantic concern
canonical normative owner
lifecycle / applicability tags
machine-contract refs
compatibility aliases / prior paths
supersession/version metadata
related non-authoritative references
```

Core invariant:

> **One semantic concern has one discoverable normative owner.**

Other standards/templates/checklists/AGENTS/README/profile files may reference or summarize that owner but MUST NOT create competing normative authority.

The registry must point to owners rather than copying their rules into a second fact source.

## 4. Qualified State-Dimension Registry

v4.7 preserves separate state dimensions rather than one overloaded state machine.

At minimum, the final registry must distinguish equivalents of:

```text
work_item.state
dispatch.state
execution_pack.state
validation.state
review.judgment
candidate.state
release.state
deployment.state
runtime / incident state
maintenance / support state
provider / execution availability
```

The exact naming belongs to L2 after upstream owners are stable.

Required principle:

> Identical-looking strings in different dimensions do not imply identical semantics.

Examples: `BLOCKED`, `PASS`, `READY` may occur under different owners and must remain qualified by owner/dimension.

## 5. Cross-dimension forbidden inferences

The final conformance system must reject at least:

```text
Task DONE -> Validation PASS
PR merged -> Release READY
Review PASS -> Validation PASS
Validation PASS -> Release READY
Release READY -> Deployment SUCCESS
Deployment SUCCESS -> Runtime Healthy
worktree/branch exists -> Task RUNNING/claimed
Dispatch COMPLETED -> product/release PASS
PACK_CURRENT -> implementation correct
old exact-SHA PASS -> successor exact-SHA PASS
provider AVAILABLE -> side-effect authority
waiver/exception -> PASS
fresh DB PASS -> upgrade PASS
mock/sandbox PASS -> higher-fidelity PASS
artifact tag/filename -> immutable artifact identity
incident recovered -> permanent defect/follow-up closed
branch/tag exists -> maintenance-supported
```

Later Frozen v4.1–v4.6 owner semantics may add further families.

## 6. Machine-contract identity/reference convergence

Audit v4 machine contracts for repeated concepts such as:

```text
repository / version / task / Issue / PR
subject identity / exact SHA / candidate
expected base / requested / tested / current head
operator / executor / context / provenance refs
artifact / environment refs
validation tuple / profile / toolchain
protocol/schema version / compatibility marker
```

v4.7 should prefer compatible reusable definitions/conventions where they reduce ambiguity, but MUST NOT collapse distinct owner objects such as:

```text
Dispatch
Validation Report
Review Aggregation
Assurance Plan
Operation
Release / Deployment records
```

Repeated identity data is valid when it intentionally snapshots currentness/evidence for that object's claim.

Existing `operation-v1` remains correlation-oriented/non-authoritative; it MUST NOT become the universal lifecycle state object by convergence.

## 7. Progressive disclosure

The final repository must make the minimum applicable read set deterministic enough that Agents do not need repository-wide guessing.

Candidate resolution path:

```text
repository AGENTS + project .dev-standard/VERSION
        ↓
pinned ADS revision
        ↓
authority/applicability registry
        ↓
project adoption / PROJECT_OVERRIDES
        ↓
applicable lifecycle / execution owners
        ↓
applicable language / archetype profiles
        ↓
Task / Execution-specific authority
```

Required semantics:

- higher-authority/current sources override stale lower-authority history;
- optional/non-applicable capability does not force unnecessary context;
- fail-closed/fallback behavior exists when applicability cannot be determined;
- progressive disclosure improves correctness/context quality, not merely token usage.

## 8. Repository information architecture

A physical directory refactor is **optional/evidence-driven**, not an automatic Product acceptance requirement.

Potential conceptual domains remain useful:

```text
lifecycle
execution
evolution
engineering
delivery
operations
ai-native
profiles
machine-contracts
```

Preferred sequence:

```text
1. authority/applicability registry
2. deterministic read routing
3. owner/alias conformance
4. measure remaining discoverability/path problems
5. move paths only where evidence supports value
6. preserve compatibility aliases/pointers throughout v4
```

Directory aesthetics alone do not justify breaking stable pinned adopters.

## 9. Compatibility / migration layer

Inside v4.7, compatible convergence may include:

- additive manifest/registry fields;
- stable compatibility aliases for moved/renamed paths;
- shared schema definitions referenced compatibly;
- terminology normalization with documented aliases;
- duplicate prose removal after one canonical owner is established;
- stronger conformance that rejects interpretations never actually authorized.

Not silently allowed in v4.7:

- incompatible core authority hierarchy changes;
- incompatible lifecycle/state semantics;
- destructive schema/wire replacement without migration;
- historical evidence reinterpretation;
- stable path deletion without compatibility path;
- replacing optional capabilities with mandatory global gates.

Such findings are recorded as future **v5.0** migration candidates.

## 10. Standard document consistency

v4.7 may normalize normative-document structure where useful, but MUST NOT require empty boilerplate sections merely for formatting consistency.

A predictable owner document should expose, where applicable:

```text
Purpose / Scope / Non-goals
Terminology / Authority
Canonical durable facts
Required semantics / Agent MUST-MUST NOT
Evidence / Validation-Assurance integration
Exceptions / capability fallback
Machine contract
Conformance
Migration / adoption / references
```

Semantic discoverability matters more than mechanical heading uniformity.

## 11. Unified cross-standard conformance

Build an executable semantic suite covering:

1. owner uniqueness / no competing normative authority;
2. authority precedence;
3. state-dimension non-inference;
4. exact identity/currentness;
5. compatibility alias/path resolution;
6. profile + PROJECT_OVERRIDES resolution;
7. machine-contract/prose consistency;
8. progressive-disclosure read routing;
9. historical payload/alias compatibility;
10. representative fresh-Agent lifecycle reconstruction.

JSON Schema meta-validation alone is insufficient; semantic contradictions between prose/owner boundaries/tests must also be detected.

## 12. Self-hosting / dogfood

Develop and validate v4.7 with the candidate registry/read-routing/conformance as far as practicable.

Principal dogfood test:

> A fresh high-capability Agent with no prior session can locate the correct owners, reconstruct current lifecycle/identity, determine allowed autonomy/evidence and hand off correctly using durable facts only.

Dogfood findings classify as:

```text
product gap
owner ambiguity
state ambiguity
schema/prose drift
read-routing/discoverability gap
compatibility/migration gap
future-major / non-goal
```

## 13. Future-major migration register

v4.7 explicitly records incompatible candidates instead of hiding them inside a v4 convergence PR, including potential:

- core authority-chain redesign;
- incompatible Dispatch/Event protocol redesign;
- state-semantic collapse/change;
- exact-SHA evidence meaning change;
- breaking role/profile/schema renames;
- stable-path removal without compatible aliasing;
- historical evidence reinterpretation.

The register prepares v5; it does not authorize those changes in v4.7.

## 14. Non-goals

v4.7 does not:

- replace all standards with one giant document;
- centralize every lifecycle dimension into one state machine;
- create another major functional domain;
- require physical directory reorganization for aesthetics;
- eliminate domain-specific standards/profiles;
- remove compatibility solely to simplify repository layout;
- require every project to adopt every optional capability;
- turn ADS into a specific CI/orchestrator/IDE/Agent runtime product.

## 15. Product acceptance

v4.7.0 is complete when:

1. every material semantic concern has one discoverable owner in the canonical registry;
2. state dimensions and forbidden cross-state inferences are explicit and conformance-tested;
3. machine contracts use compatible, consistent subject/identity/reference conventions without owner-object collapse;
4. progressive-disclosure routing lets Agents discover applicable standards without repository-wide guessing;
5. stable v4 adopters retain compatibility paths/aliases for changed names/paths/contracts;
6. profile/PROJECT_OVERRIDES resolution is deterministic;
7. cross-standard conformance detects owner/state/schema/prose drift;
8. a fresh Agent can reconstruct and execute a representative lifecycle from durable facts only;
9. v4.7 self-dogfood completes with explicit findings/disposition;
10. incompatible convergence needs are separated into future-major migration planning.

## 16. Freeze basis / next gate

Current evidence:

- `docs/implementation/4.7.0/AUTHORITY_STATE_SCHEMA_INVENTORY.md`
- `docs/implementation/4.7.0/L1_PRODUCT_EVIDENCE.md`

Product Freeze is intentionally BLOCKED until:

1. v4.1–v4.6 canonical Product/L2 semantic-owner boundaries are sufficiently stable;
2. the owner/state/schema inventory is refreshed against those exact revisions;
3. physical-refactor necessity is re-evaluated rather than assumed;
4. future-major candidates are separated from additive v4.7 scope;
5. a final L1 currentness review confirms the convergence target.

Only then may v4.7 explicitly Freeze and run L2 Architecture Evidence.

`LOCAL_ENV=NOT_REQUIRED` for current inventory/L1 work. Repository-wide migration/conformance/self-dogfood execution belongs after Product/L2 Freeze and exact candidate identity.