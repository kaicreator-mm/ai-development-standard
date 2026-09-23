# v4.0 Task DAG — Planning Checkpoint

Status: CANDIDATE planning checkpoint; becomes frozen with T-001/#73 merge
Version: 4.0.0
Version Issue: #72
Released baseline: `7ebaf66cba8fdc3a672e9b1d7fe9bd9e730a3805`
Integration branch: `version/v4.0.0`

This file is the frozen-planning/history DAG checkpoint once T-001 merges. Per the v3.4 Work Item Contract, the canonical live execution DAG is GitHub Task Issues + native Issue Dependencies after materialization.

## Capability fallback

The currently exposed GitHub connector does not expose native Issue Dependency mutation. Therefore the dependency relations below are also mirrored in Issue bodies, but that mirror is **NON_AUTHORITATIVE_CAPABILITY_FALLBACK**. A capable executor SHOULD materialize native Issue Dependency edges when available. No Agent may claim those edges already exist.

## DAG

```text
T-001 / #73  Authority / Vocabulary / Compatibility Freeze
  ↓
T-002 / #74  Canonical Operation Contract + Lifecycle Mapping
  ├─────────────────────────────┐
  ↓                             ↓
T-003 / #75                  T-005 / #77
Assurance Plan +             Agent Interchange /
Independence Axes            Correlation + GitHub Mapping
  ↓                             │
T-004 / #76                    │
Multi-Model Adversarial        │
Review + Findings /            │
Conflict / Aggregation         │
  └──────────────┬──────────────┘
                 ↓
T-006 / #78  Operation Routing / Reducer / Orthogonal State Integration
                 ├───────────────────────────┐
                 ↓                           ↓
T-007 / #79                              T-008 / #80
Work Item / Task Pack /                  Validation / Release /
Execution Pack / Fast Path               Freeze / Hidden Integration
                 └──────────────┬────────────┘
                                ↓
T-009 / #81  Schemas + Golden/Forbidden Examples + Verifier Regressions
                                ↓
T-010 / #82  Reference Flows + Self-Dogfood Multi-Model Review Scenario
                                ↓
T-011 / #83  Migration / Adoption / PROJECT_OVERRIDES Guidance
                                ↓
T-012 / #84  Version Closure + Fresh Model-Diverse Architecture Review
                                ↓
T-013 / #85  Release Qualification + Immutable v4 Baseline
```

## Task table

| Task | Issue | Depends on | Primary concern | Expected execution boundary |
|---|---:|---|---|---|
| T-001 | #73 | — | authority/vocabulary/compatibility | Web + GitHub; repository verifier required before merge |
| T-002 | #74 | T-001 | Operation contract/lifecycle mapping | Web + GitHub |
| T-003 | #75 | T-002 | Assurance Plan/independence axes | Web + GitHub |
| T-004 | #76 | T-003 | model-diverse adversarial review/aggregation | Web + GitHub; external fresh model needed for later dogfood, not for authoring |
| T-005 | #77 | T-002 | exchange envelope/GitHub mapping | Web + GitHub |
| T-006 | #78 | T-004,T-005 | reducer/routing integration | Web + GitHub; executable regression deferred to T-009 |
| T-007 | #79 | T-006 | Work Item/Pack/Fast Path integration | Web + GitHub |
| T-008 | #80 | T-006 | Validation/Release/Freeze/Hidden integration | Web + GitHub; executable regression deferred to T-009 |
| T-009 | #81 | T-007,T-008 | schemas/examples/verifier regressions | **repository-real Local Agent / CI required for authoritative PASS** |
| T-010 | #82 | T-009 | end-to-end reference flows + dogfood | Web + GitHub + fresh model-diverse reviewer evidence |
| T-011 | #83 | T-010 | migration/adoption/overrides | Web + GitHub |
| T-012 | #84 | T-011 | full closure + fresh model-diverse architecture review | Web orchestration + repository-real validation + external independent model review |
| T-013 | #85 | T-012 | release qualification/integration | Web control + repository-real final evidence |

## Execution rules

1. JIT task branches are created only when dependencies are satisfied, except a real stacked-code dependency.
2. One concern, one PR remains the default.
3. Each PR targets `version/v4.0.0` unless a real stacked dependency requires another parent.
4. Required Review is exact-head bound; Builder context cannot self-assert PASS.
5. Validation truth remains exact subject × environment/toolchain × profile; no Operation abstraction can infer an unexecuted PASS.
6. T-009 is the first Task whose authoritative acceptance explicitly requires repository-real verifier execution; Web static inspection alone is insufficient.
7. T-010/T-012 require model-diverse independent review evidence; the implementing model/context cannot satisfy those independence requirements by self-review.
8. Blockers propagate only through actual DAG edges; independent work may continue where frozen authority allows.

## Live execution materialization

Issues #73–#85 are the materialized Work Items. Their dependency text is currently a capability-fallback mirror. When native dependency mutation becomes available, materialize exactly the graph above and record the action; do not invent a different live DAG without an explicit planning/architecture amendment.
