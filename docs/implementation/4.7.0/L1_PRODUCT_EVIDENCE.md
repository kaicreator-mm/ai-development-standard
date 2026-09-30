# v4.7.0 L1 Product Evidence — AI-native Development Convergence

Status: **COMPLETE RESEARCH / PRE-FREEZE — Product Freeze intentionally BLOCKED until upstream v4.1–v4.6 owner boundaries are stable**

Research date: 2026-09-30

Baseline reviewed:

- `main@e9eb39235e45e9ad90407b803ab1c8679d348dbf`
- Draft `docs/implementation/4.7.0/PRD.md`
- `docs/implementation/4.7.0/AUTHORITY_STATE_SCHEMA_INVENTORY.md`
- root `AGENTS.md`
- `standard-manifest.json`
- current machine contracts under `schemas/`
- current compatibility entries
- v4.1–v4.6 Product/research candidates available on parallel lanes

This document is L1 evidence only. It MUST NOT authorize repository refactor, schema migration, path moves, alias removal or Product Freeze.

## 1. Recommendation

**PROCEED WITH NARROWING, BUT DO NOT FREEZE YET.**

The convergence problem is real and increasingly material: ADS already has strong individual owners and machine contracts, but a fresh Agent still needs multiple manual routing sources to answer `semantic concern -> owner -> state dimension -> applicable machine contract -> compatibility alias`.

The L1 evidence does **not** support replacing the repository with one giant standard, one global state machine or one universal schema. It supports four convergence products:

1. **Canonical Authority / Applicability Registry** extending the current manifest;
2. **Qualified State-Dimension Taxonomy + forbidden-inference registry**;
3. **Machine-contract identity/reference convergence** through shared definitions/conventions rather than object collapse;
4. **Progressive-disclosure + compatibility-preserving repository information architecture**, with physical path refactor only where evidence proves value.

Unified cross-standard conformance and self-dogfood are acceptance mechanisms, not separate lifecycle owners.

## 2. Internal evidence: convergence mechanisms already exist

### 2.1 `standard-manifest.json` is already the right seed

The manifest already separates:

```text
authority
normative_standards
compatibility_entries
templates
checklists
prompts
machine_contracts
references
verification
```

and explicitly distinguishes compatibility entries from normative authority.

**Finding:** evolve this inventory rather than create a second catalog.

Missing discoverability fields are primarily semantic:

```text
semantic concern -> canonical owner
owner -> lifecycle/state dimension
owner -> machine contracts
owner -> compatibility aliases/supersession
applicability/read-routing tags
profile/project-override relationship
```

### 2.2 Root AGENTS already implements progressive disclosure

`AGENTS.md` routes Agents to different documents based on role and operation instead of requiring the full repository for every task.

**Finding:** v4.7 should formalize/test this behavior rather than replace it with “always load everything”.

### 2.3 State dimensions are intentionally separate today

Current machine contracts already distinguish:

```text
workflow/work-item state
dispatch state
Execution Pack state
Validation state
Review judgment
Candidate state
Release state
provider/execution availability
```

Future v4.4/v4.5 add Deployment and Runtime/Incident/Maintenance dimensions.

The same token (`BLOCKED`, `PASS`, `READY`) may appear in different dimensions with different meaning.

**Finding:** convergence means qualifying/owning dimensions, not mechanically deduplicating strings into one enum.

## 3. External evidence: compatibility-preserving evolution beats aesthetic replacement

### 3.1 Kubernetes deprecation/versioning

Kubernetes explicitly evolves independently versioned API groups under a deprecation policy designed to avoid breaking existing clients. GA APIs are not silently removed within a major version, and version conversion/round-trip behavior preserves compatibility expectations.

Sources:

- https://kubernetes.io/docs/reference/deprecation-policy/
- https://kubernetes.io/docs/concepts/overview/kubernetes-api/

**Finding:** v4.7 path/term/schema cleanup inside the v4 line should use aliases/compatibility entries/migration windows rather than aesthetic breakage. Breaking authority/wire semantics belong to future-major planning.

### 3.2 OpenAPI Overlay separates augmentation from canonical source

OpenAPI Overlay defines a separate document that applies repeatable changes to an existing source description rather than making the overlay itself the original source of truth.

Source: https://spec.openapis.org/overlay/v1.1.0.html

**Finding:** compatibility overlays/aliases/project overlays can remain subordinate transformations/references without becoming competing normative sources. This supports ADS's existing `PROJECT_OVERRIDES` / compatibility-entry pattern.

### 3.3 JSON Schema favors modular reusable identities

JSON Schema's structuring guidance emphasizes logical reusable schemas identified by stable URIs and referenced from other schemas. JSON Schema vocabularies are also purpose-oriented reusable semantic units rather than one monolithic global schema.

Sources:

- https://json-schema.org/understanding-json-schema/structuring
- https://json-schema.org/draft/2020-12/json-schema-core

**Finding:** v4.7 should converge repeated identity/reference concepts through reusable definitions/conventions where compatible, not collapse distinct owner objects such as Dispatch, Validation Report and Review Aggregation into one universal payload.

### 3.4 Agent Skills reinforce progressive disclosure

GitHub Agent Skills load detailed instructions/scripts/resources only when relevant and explicitly distinguish them from simple instructions that apply to nearly every task.

Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills

**Finding:** the final repository should make the minimal applicable read set deterministic. Progressive disclosure is a correctness/context-quality feature, not only a token optimization.

## 4. Product correction 1 — Authority Registry, not giant document

Freeze candidate direction:

```text
semantic concern
canonical normative owner
applicability/lifecycle tags
machine-contract refs
compatibility aliases / previous paths
supersession/version metadata
related non-authoritative references
```

Core invariant:

> **One semantic concern has one discoverable normative owner.**

Other documents may summarize/map/reference it but cannot create competing authority.

The registry should extend/replace fields within the existing manifest architecture compatibly. Exact schema belongs to L2 after upstream owners stabilize.

## 5. Product correction 2 — Qualified State Taxonomy

v4.7 should publish a canonical dimension map such as:

```text
work_item.state
dispatch.state
execution_pack.state
validation.state
review.judgment
candidate.state
release.state
deployment.state
runtime/incident.state
maintenance/support.state
provider.availability
```

The objective is not to force these exact keys; it is to make owner/dimension explicit and prevent cross-dimensional inference.

Required cross-standard negatives include:

```text
Task DONE -> Validation PASS                 MUST fail
PR merged -> Release READY                  MUST fail
Review PASS -> Validation PASS              MUST fail
Release READY -> Deployment SUCCESS         MUST fail
Deployment SUCCESS -> Runtime Healthy       MUST fail
branch/worktree exists -> Task RUNNING      MUST fail
Dispatch COMPLETED -> Release PASS           MUST fail
PACK_CURRENT -> implementation correct       MUST fail
old-SHA PASS -> successor PASS               MUST fail
provider AVAILABLE -> side-effect authority MUST fail
waiver/exception -> PASS                     MUST fail
fresh DB PASS -> upgrade PASS                MUST fail
mock/sandbox PASS -> higher fidelity PASS    MUST fail
artifact tag -> immutable artifact identity MUST fail
incident recovered -> permanent fix closed  MUST fail
branch exists -> supported maintenance line MUST fail
```

## 6. Product correction 3 — Shared identity/reference conventions, not object collapse

Current schemas repeat legitimate evidence identity fields:

```text
repository/version/task/issue/pr
subject identity / exact SHA / candidate
expected base / requested / tested / current head
operator/executor/context
Validation tuple/environment/toolchain
state/result/judgment
```

L2 should audit whether reusable definitions can standardize:

- Subject Identity refs;
- Git exact identity/base refs;
- Operator/Executor provenance refs;
- Artifact/environment refs;
- compatibility/version markers.

But v4.7 MUST preserve object ownership:

```text
Dispatch != Validation Report
Validation Report != Review Aggregation
Review Aggregation != Release Verdict
Operation != lifecycle authority
```

Repeated data is acceptable when it intentionally snapshots currentness/evidence truth for that object's claim.

## 7. Product correction 4 — Progressive disclosure before physical refactor

Current flat `standards/` paths are stable and simple but increasingly hard to discover by domain. A domain-oriented physical layout may help, but L1 does not support making directory refactor a required success criterion by itself.

Preferred sequence:

```text
1. canonical owner/applicability registry
2. deterministic progressive-disclosure/read-routing
3. conformance for aliases/owner uniqueness
4. measure discoverability/context problems
5. only then move paths where evidence supports value
6. preserve stable aliases/compatibility entries throughout v4
```

Candidate conceptual domains remain useful:

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

They need not all become physical directories in v4.7.

## 8. Machine-contract convergence boundary

`operation-v1` is already a useful cross-lifecycle correlation object with `CORRELATION_ONLY_NON_AUTHORITATIVE` binding. `assurance-plan-v1`, Dispatch and Review/Validation contracts also have explicit owner boundaries.

L1 does not support replacing them with one meta-schema.

Instead v4.7 should audit:

```text
canonical IDs / URI / protocol versions
shared definitions / refs
exact-subject identity binding
state dimension qualification
additionalProperties / extension posture
compatibility/version markers
prose/schema consistency
alias/supersession metadata
```

Any migration must preserve historical evidence meaning.

## 9. Compatibility / migration Product rules

Within v4.7, allowed convergence changes include:

- additive manifest/registry fields;
- compatibility aliases for moved/renamed paths;
- shared schema definitions referenced compatibly;
- terminology normalization with documented aliases;
- removing duplicate prose after one canonical owner is established;
- stronger conformance that rejects interpretations never actually authorized.

Not silently allowed inside v4.7:

- core authority-chain change;
- incompatible lifecycle/state semantics;
- destructive schema/wire replacement without migration;
- historical evidence reinterpretation;
- stable path deletion without compatibility path;
- replacing optional capabilities with mandatory global gates.

These become future-v5 inputs when incompatibility is real.

## 10. Unified Conformance as acceptance mechanism

v4.7 should build a cross-standard semantic suite covering:

1. owner uniqueness / no duplicate normative ownership;
2. authority precedence;
3. state-dimension non-inference;
4. exact identity/currentness;
5. compatibility alias resolution;
6. profile/PROJECT_OVERRIDES resolution;
7. machine-contract/prose agreement;
8. progressive-disclosure read routing;
9. historical payload/alias compatibility;
10. representative end-to-end fresh-Agent reconstruction.

Schema meta-validation alone is insufficient; OpenAPI itself notes that schemas cannot catch every specification violation and specification text remains authoritative when schema/text disagree.

Reference: https://spec.openapis.org/overlay/

## 11. Self-dogfood target

A v4.7 candidate should be developed using its own candidate authority registry/read-routing/conformance as far as possible.

Principal dogfood test:

> A fresh capable Agent with no historical chat can identify the applicable owner set, current Task/subject identity, allowed autonomy, required evidence and next route using durable repository/GitHub facts only.

Dogfood findings classify into:

```text
product gap
owner ambiguity
state ambiguity
schema/prose drift
read-routing/discoverability gap
compatibility/migration gap
non-goal / future-major input
```

## 12. Counter-evidence / risks

- A central registry can become stale/duplicative if it copies rules rather than points to owners.
- Physical directory cleanup may cost compatibility without improving Agent correctness.
- Shared schema definitions can create tight coupling and make independent evolution harder.
- One universal state machine would destroy the current intentional separation of Task/Review/Validation/Release truth.
- Aggressive terminology cleanup can rewrite historical evidence meaning.
- Progressive disclosure can omit needed context if applicability rules are under-specified; fail-closed discovery/fallback is required.

## 13. L1 verdict

**Evidence strongly supports v4.7 convergence, but Product Freeze is intentionally premature.**

Recommended final Product shape after upstream stabilization:

```text
1. Authority / Applicability Registry
2. Qualified State-Dimension + Non-Inference Registry
3. Machine-contract Identity/Reference Convergence Rules
4. Progressive Disclosure + Compatibility-Preserving Repository IA
5. Unified Cross-standard Conformance
6. Self-dogfood + Future-major Migration Register
```

Before Product Freeze:

- v4.1–v4.6 canonical Product/L2 owner boundaries must be stable enough to inventory accurately;
- authority-owner inventory must be refreshed against those exact integrated revisions;
- future-major candidates must be separated from additive v4.7 work;
- physical refactor must remain optional/evidence-driven.

`LOCAL_ENV=NOT_REQUIRED` for L1/inventory. Repository-wide executable migration/conformance dogfood comes only after Product/L2 Freeze and exact candidate identity.