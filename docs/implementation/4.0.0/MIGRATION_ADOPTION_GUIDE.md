# v3.4 → v4 Migration and Progressive Adoption Guide

Issue: #83 / T-011
Baseline: `version/v4.0.0@f85793d3c05b848ba91ce1c771cbffdb15efbd49`

## 1. Principle

v4 is a protocol and assurance evolution, not a requirement that every project deploy a full orchestration runtime.

**Adoption level controls implementation surface, not truth strength.**

Every project pinned to v4 keeps the same non-weakening floor:

- immutable standard pin and durable authority;
- exact subject identity for Validation/Review evidence;
- required Validation means actual successful execution on the required tuple;
- Review remains separate from Validation and follows its authority-derived policy;
- unresolved P0/P1 blocker dominance is not waived by reviewer/model majority;
- Task/Execution Pack authority remains subordinate to frozen product/architecture authority;
- Candidate PREPARED != FROZEN;
- PR PASS != Release PASS;
- Release READY != Repository Integration complete;
- Interchange/routing/reducer projections do not become owning truth.

A project that adopts only A0 or A1 is therefore simpler, not less truthful.

## 2. Adoption levels

| Level | Name | Required implementation surface | Optional / absent surface |
|---|---|---|---|
| A0 | `A0_COMPATIBILITY` | v4 standard pin, v3.4-compatible durable facts, exact identity, required Validation/Review/release gates | v4 Operation/Assurance machine records, reducer/controllers, Interchange automation |
| A1 | `A1_MANUAL_PROTOCOL` | A0 + durable Operation/Assurance concepts recorded manually in GitHub/files using v4 vocabulary | schema gate, reducer/controller automation |
| A2 | `A2_MACHINE_CONTRACTS` | A1 + adopted v4 records validated by current schemas/semantic verifier | automated reducer/routing/controllers |
| A3 | `A3_DERIVED_AUTOMATION` | A2 + derived reducer/queue/routing/controller state from durable facts | full project-wide orchestration is optional |
| A4 | `A4_FULL_ORCHESTRATION` | A3 + project-selected full Operation/Assurance/Interchange/controller automation | none required beyond what the project actually needs |

Capabilities are monotonic: higher levels include lower-level capabilities. A project MAY stay indefinitely at any level that satisfies its product/engineering needs.

### 2.1 What adoption level does not mean

Adoption level is never:

- a risk score;
- a permission to skip a required gate;
- a Review policy;
- a Validation result;
- a Candidate/Release state;
- a substitute for GitHub Issue Dependencies when that execution DAG is enabled;
- a claim that an automation/controller exists when it does not.

## 3. v3.4 → v4 compatibility matrix

| v3.4 concept | v4 status | Migration action |
|---|---|---|
| immutable `.dev-standard/VERSION` pin | preserved | no semantic migration; pin exact v4 revision when adopting |
| Frozen PRD / Frozen Architecture authority | preserved | no weakening; v4 Operation remains subordinate |
| Task DAG planning checkpoint | preserved | continue using durable Task DAG; live execution authority remains GitHub Issue Dependencies where enabled |
| Task Pack | preserved | may be referenced by Operation; authority does not move |
| Execution Pack | preserved / optional | remains subordinate to Task Pack and may be omitted on Fast Path |
| exact-SHA Validation | preserved and strengthened | keep actual execution tuple/evidence; never replace with model agreement |
| Review policy `required/recommended/not-required` | preserved | may be represented in Assurance Plan; policy authority does not move |
| Builder / Validator / Reviewer role profiles | preserved | may become Assurance activities; independence claims must remain factual |
| `ai-dev:event:v2` event protocol | preserved | no event-v3 migration is required by v4 adoption |
| Fast Path | preserved and hardened | operation elision is allowed only when canonical disqualifiers are false |
| Candidate Freeze | preserved | remains its own authority/state; never inferred from Release or PR PASS |
| Release Qualification | preserved | remains distinct from Candidate Freeze and Repository Integration |
| Repository Integration | preserved | merge/integration outcome does not manufacture Release READY |
| GitHub comments/issues as durable facts | preserved | may carry v4 Operation/Assurance/Exchange records; chat is still not project state |
| routing/queue metadata | clarified | treated as derived projection, never owning truth |
| multi-model review | additive | only claim it when actual context/model/executor/evidence independence is satisfied |

Historical v3.4 records keep their original identity and result. Migrating a project to v4 MUST NOT rewrite prior PASS/FAIL/CHANGES_REQUESTED or pretend historical evidence was produced under v4 machine contracts.

## 4. Recommended migration sequence

1. **Pin v4 exactly.** Update `.dev-standard/VERSION` to an immutable v4 revision and verify VERSION/revision consistency.
2. **Declare adoption level.** Add the v4 Adoption / Compatibility Profile to `PROJECT_OVERRIDES.md`.
3. **Audit non-weakening floor.** Confirm exact identity, required Validation, Review policy, Candidate/Release separation and real environment tuples remain true.
4. **Start at the smallest useful level.** Existing projects normally begin at A0 or A1; do not deploy reducer/controllers merely to claim v4 adoption.
5. **Migrate durable records incrementally.** New work may use v4 Operation/Assurance records while historical v3.4 records remain immutable history.
6. **Enable A2 only when machine contracts are actually executed.** Do not claim A2 because schema files exist elsewhere.
7. **Enable A3/A4 only with real derived-state/controller execution.** Record provider/backend/runtime facts and fail closed when unavailable.
8. **Run project verifier + project-required validation.** The migration PR itself is subject to normal Review/Validation policy.

A project MAY skip directly to a higher level when it already has the required mechanisms and evidence.

## 5. PROJECT_OVERRIDES boundaries

Projects MAY configure:

- `v4.adoption_level`;
- compatibility/migration status;
- default Assurance activities for concerns that do not already have stronger authority;
- default model-diversity basis for project-selected adversarial reviews;
- Interchange transport and whether it is enabled;
- reducer/routing/controller enablement;
- stricter Fast Path defaults/disqualifiers;
- project-specific runtime/provider/backend locations;
- stronger Validation/Review/release gates.

Projects MUST NOT configure away:

1. a higher-authority required Review or Validation tuple;
2. exact-SHA/current-subject binding;
3. required actual Validation execution;
4. blocker dominance;
5. Candidate Freeze evidence;
6. Release Qualification authority;
7. Repository Integration separation;
8. `CORRELATION_ONLY_NON_AUTHORITATIVE` semantics of Interchange;
9. canonical Fast Path disqualifiers;
10. truthful `NOT_RUN/BLOCKED/NOT_APPLICABLE` semantics.

Precedence remains:

```text
Frozen PRD / Contract
→ Frozen Architecture
→ PROJECT_OVERRIDES
→ Task acceptance
→ Standard defaults
```

An override MAY strengthen a rule below it. It MUST NOT weaken a rule above it.

## 6. Fast Path across adoption levels

Fast Path is orthogonal to A0–A4.

- A0 project: may use Fast Path with manual durable facts.
- A1 project: may omit large Operation/Assurance packs while recording the minimal required durable facts.
- A2+ project: may use machine eligibility checks.
- A3/A4 project: controller may derive eligibility, but eligibility remains fail-closed and non-authoritative until owning conditions are satisfied.

A project MAY disable Fast Path globally or add stricter disqualifiers. It MUST NOT remove the canonical v4 disqualifiers or treat `A0/A1` as evidence that work is low risk.

## 7. Example — small project

Profile:

```text
v4.adoption_level: A1_MANUAL_PROTOCOL
compatibility_mode: v3.4-bridge
CI profile: minimal
reducer: disabled
controllers: disabled
interchange: disabled
fast_path: enabled with canonical disqualifiers + project-sensitive-path disqualifier
```

Behavior:

- GitHub Issues/PRs remain the durable coordination surface.
- Operations/Assurance are recorded manually only when useful.
- No project-local reducer service is required.
- Exact-head tests/Validation and required Review still bind to the real candidate SHA.
- Release still requires Candidate Freeze and Release Qualification according to project authority.

This is a fully valid v4 adoption.

## 8. Example — substantial project

Profile:

```text
v4.adoption_level: A3_DERIVED_AUTOMATION
compatibility_mode: native-v4
machine_contracts: enabled
reducer: enabled
routing/controllers: enabled for declared concerns
interchange: enabled over GitHub-backed correlation transport
model_diversity.default_basis: provider-diverse for selected critical assurance plans
fast_path: enabled with canonical + project-specific disqualifiers
```

Behavior:

- canonical Operation/Assurance records are schema/semantic checked;
- reducer derives queue/routing state from durable facts;
- controllers dispatch work but cannot manufacture Validation/Review/Candidate/Release truth;
- GitHub Task Issues + Issue Dependencies remain the live execution DAG when enabled;
- model-diverse review remains evidence/assurance, never executable Validation;
- Release READY still does not equal repository merge completion.

## 9. Downgrade and rollback

A project MAY reduce automation from A4→A3→A2→A1/A0 when automation is unavailable or no longer justified, provided:

- durable facts remain readable;
- required gates continue to execute through a truthful manual/fallback path;
- no PASS/result is migrated across subject identity;
- controller-derived state is discarded/rebuilt rather than promoted to authority;
- the change is reviewed as a project-standard adoption change.

A downgrade that removes the only real path to a mandatory gate is `BLOCKED`, not a valid adoption simplification.

## 10. Relation to v4 release work

T-011 defines migration/adoption guidance only. It does not execute v4 version Closure (T-012) or Release Qualification/main integration (T-013). Open machine-hardening debt from T-010 R4 remains tracked separately in #158 and is not silently resolved by migration documentation.
