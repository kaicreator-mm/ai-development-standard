# Architecture Design Standard

Status: **Normative — v4.3**

## 1. Purpose

This standard owns the durable quality requirements for **material architecture decisions** after/alongside L2 evidence. It does not replace the L2 research workflow, mandate one architecture paradigm, or take compatibility/migration authority from v4.2.

## 2. Applicability and materiality

Use this standard when a decision materially affects one or more of:

- public or cross-component contracts;
- data durability or ownership;
- security/trust boundaries;
- failure isolation/recovery;
- deployment/runtime topology;
- shared infrastructure or platform dependency;
- irreversible/high-cost structural choice;
- multiple Tasks/teams/services through a shared invariant.

Fast Path changes with no material architecture decision need not produce empty design artifacts.

Small diff size does not make a material architecture choice non-material.

## 3. Required design facts

A material architecture decision MUST make the applicable facts durable enough for an unfamiliar implementer/reviewer to recover:

1. **Decision / scope** — what is decided and what is not;
2. **Drivers** — Product requirements, constraints and evidence shaping the decision;
3. **Invariants** — truths that implementations MUST preserve;
4. **Boundaries / ownership** — component, data, authority and dependency ownership;
5. **Contracts / interactions** — interfaces or durable relationships affected;
6. **Alternatives considered** — materially plausible options, not artificial strawmen;
7. **Rationale** — why the chosen option satisfies drivers/invariants better for this subject;
8. **Trade-offs** — accepted costs/limits, including operational or migration burden where material;
9. **Failure modes** — expected failures and ownership/recovery boundary;
10. **Evidence / assumptions / UNKNOWNs** — what is proven, inferred or unresolved;
11. **Compatibility / migration refs** when a decision changes contracts/persistent state;
12. **Escape hatch / evolution path** where lock-in or reversal cost is material.

Not every decision requires every field. Omission is acceptable only when the dimension is genuinely non-material and that is evident from context.

## 4. Evidence and UNKNOWN handling

Architecture evidence may come from source inspection, existing contracts, prototypes/research demos, performance/security experiments, operational history, official technical sources or other applicable evidence.

Evidence strength must match the claim. A mock or toy benchmark does not automatically prove production behavior.

A high-impact `UNKNOWN` MUST NOT silently become implementation freedom. It must be dispositioned by one of:

```text
research / experiment
Product or Architecture decision
explicit bounded assumption with owner
Task-level validation if safely deferrable
BLOCKED until evidence exists
```

An implementation Agent may not select its preferred architecture pattern merely because the UNKNOWN was left unresolved.

## 5. L2 relationship

L2 remains the architecture research/evidence workflow and Freeze mechanism. This standard defines the quality/shape of durable design decisions; it does not replace L2 prompts, Research Demo rules or Architecture Freeze authority.

A Frozen L2 decision outranks later implementation preference. If new implementation evidence contradicts Frozen L2 materially, route an Architecture contradiction/reopen decision rather than silently diverging.

## 6. Ownership and contracts

Architecture should make ownership explicit enough to avoid duplicate authority or hidden shared mutable state.

When material, record:

- who owns writes vs reads;
- canonical source of truth;
- lifecycle/retention responsibility;
- consistency/ordering expectations;
- failure/retry/idempotency boundary;
- external side-effect owner;
- security/privacy boundary;
- observability/recovery responsibility.

Do not create a new owner merely to make a diagram symmetric.

## 7. Compatibility and migration boundary

Architecture design may require that compatibility/migration be considered, but v4.2 remains semantic owner of compatibility outcomes and persistent-state transition/recovery.

Forbidden inferences include:

```text
architecture diagram unchanged -> interface compatible
new component boundary -> migration plan unnecessary
schema compiles -> migration/recovery proven
architecture decision -> compatibility PASS
```

Architecture records should reference v4.2 evidence rather than redefining it.

## 8. No universal paradigm

ADS does not mandate microservices, monoliths, event sourcing, CQRS, clean/hexagonal architecture, DDD, Kubernetes, serverless, one database model, or any other universal pattern.

Patterns are options whose applicability must follow Product drivers, constraints and evidence.

`popular pattern -> correct architecture` is forbidden.

## 9. Failure and operational semantics

When material, architecture decisions must describe failure boundaries rather than only happy-path component structure.

Consider applicable dimensions:

- partial failure / retry / timeout;
- consistency and duplicate delivery;
- dependency outage/fallback;
- capacity/resource exhaustion;
- rollout/version skew;
- recovery / degraded mode;
- data corruption/loss boundary;
- operator intervention and evidence.

No universal mechanism is required.

## 10. Security / sensitive boundaries

Material trust/security assumptions belong in durable architecture facts, but secret values do not.

Document trust zones, identity/authentication/authorization boundaries, data sensitivity classes and side-effect authority where material. Reference the owning Secrets/External System standards instead of duplicating their semantics.

## 11. Decision durability / format

Architecture decisions may live in ADRs, design docs, Frozen L2 documents, contracts or equivalent durable repository artifacts. This standard does **not** mandate one ADR filename/template/tool.

The required outcome is recoverable design truth, not a specific document fashion.

## 12. Fast Path

Fast Path may use a short design note or existing authoritative decision reference when architecture impact is low and already bounded.

Fast Path MUST NOT be used to avoid architecture evidence merely because the code change is small or an Agent claims the implementation is obvious.

## 13. Review prompts

A reviewer should be able to answer:

- What Product/evidence drives this decision?
- What invariants and ownership boundaries must survive implementation?
- What alternatives/trade-offs were material?
- What UNKNOWNs remain and who owns them?
- Are failure/security/durability/deployment assumptions explicit when material?
- Does the design reference rather than steal compatibility/migration ownership?
- Is the escape/evolution path adequate for high-cost lock-in?

## 14. Failure handling

If a high-impact UNKNOWN or owner conflict remains unresolved, classify the design as needing research/authority resolution rather than inventing local implementation freedom. Conflict with Frozen Product/L2 routes to the owning authority before implementation proceeds.

## 15. Reuse-first adoption and BUILD_NEW

When a material design decision adopts outside work, the reuse mode is an explicit accountable choice with distinct evidence floors, not a convenience default:

1. **Pattern harvest (H1)** — adopt a cited upstream idea/mechanism inside a locally owned design. Requires the upstream reference and the local design; it does not require copying source, and similarity MUST NOT be read as direct copying or behavior equivalence.
2. **Source-inspired re-specification (H2)** — re-express upstream behavior in a locally specified module. Requires disclosed origin and derivation context, the local contract, and differential/behavior/failure tests exposing divergence and risks. Presenting a material reconstruction as an undisclosed rewrite is provenance laundering and MUST NOT pass as local design.
3. **Direct code reuse (H3)** — take upstream source into the project. Requires the exact immutable upstream identity and material paths, the license/NOTICE observed at that revision with the project license-policy disposition, attribution, and local behavior tests. Bounded H3 is admissible; it is never Validation PASS or release permission, and reliance on a different or drifted revision is stale until freshly re-checked.
4. **BUILD_NEW** — build locally instead of adopting. Admissible only as an accountable decision that considered materially plausible mature comparators and records a concrete incompatible-license/coupling/security/maintenance rationale and a decision owner. It is not a silent default; ignored comparators or a missing owner keep it blocked.

Architecture owns the mode selection, alternatives and local contracts; `DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md` owns upstream identity, license/NOTICE currentness and reuse invalidation; Validation alone owns executed proof. No mode auto-promotes across L1→L2→L3 and no reuse disposition mints a gate or release state.

Fast Path stays proportional: a low-risk, immaterial change with no material upstream dependency and no higher gate requires no mandatory external research or reuse catalog. The label does not erase material obligations — an actual vendored-source or license/NOTICE change keeps the obligations above regardless of how the work was labelled.
