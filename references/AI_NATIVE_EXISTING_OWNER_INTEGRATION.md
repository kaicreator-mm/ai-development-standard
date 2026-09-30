# AI-native Existing-owner Integration Reference

Status: non-normative integration map for v4.6.

v4.6 adds Intent/Assumption, Context Engineering and Skill governance. It does **not** create replacement owners for autonomy, Assurance/Review, Dispatch/Handoff, Validation or Release.

## 1. Autonomy / execution freedom

Canonical vocabulary remains:

```text
F0_MECHANICAL
F1_BOUNDED_IMPLEMENTATION
F2_ENGINEERING_DISCRETION
F3_ARCHITECTURE_REQUIRED
```

Execution Pack / Dispatch/Task authority decides applicability. A stronger model does not self-promote a task to F3 and a lower-cost model cannot downgrade F3 architecture requirements.

## 2. Assurance coverage

`assurance-plan-v1` already owns:

- review / validation / hidden-validation / coherence / authority-review activity kinds;
- required/recommended/not-required policy;
- independence dimensions for context/model/executor/evidence;
- model-diverse adversarial mode;
- open `coverage[]` strings;
- blocker-dominant aggregation policy.

AI-native concerns therefore use existing `coverage[]` values such as intent-authority, context-currentness or skill-trust-boundary rather than creating an AI Assurance result family.

## 3. Review result and provenance

`review-aggregation-v1` already owns Review judgment, activity results, findings/conflicts and reviewer provenance. Provenance can record provider/model/executor/context facts.

Important negatives:

```text
provider/model recorded != independence proven
strong model != correct by authority
majority vote != blocker override
review judgment != workflow mutation authority
```

Independence remains a property that must be established against the reviewed subject and required dimensions.

## 4. Dispatch / handoff

`dispatch.schema.json` remains the executable handoff for builder/validator/reviewer work. v4.6 optional Intent/Skill refs may accompany Dispatch but do not replace Task Pack, expected base, pinned standard, role, execution profile or Agent freedom.

Same transport identity is not the same concept as logical operator/context identity. Two executions may use one GitHub/API account while still requiring distinct fresh logical contexts; conversely, different model/provider strings alone do not establish independence.

## 5. Validation / Release

Validation remains exact-subject execution evidence under Validation authority. Review aggregation may reference validation results but cannot manufacture them. Release remains downstream Release authority.

No new AI-native PASS/READY state is introduced.

## 6. Handoff and lost-session recovery

Existing GitHub/Issue/Dispatch/Local Agent protocols remain durable handoff owners. v4.6 Context Engineering strengthens the invariant that required truth is recoverable from durable facts, but does not create a second handoff object or transcript authority.

## 7. Model usage

Model/provider metadata is provenance/capability context. Risk, Task authority, required independence and evidence determine whether a model/executor is suitable. Model strength by itself does not grant F3, mutation, merge or side-effect authority.

## 8. Required non-inferences

| Fact | Forbidden inference |
|---|---|
| model is stronger | F3 authority granted |
| provider/model recorded | independent review proven |
| same GitHub/API account | necessarily same logical context/operator |
| different provider/model | necessarily independent |
| AI-authored change | human review universally mandatory |
| assurance covers AI concern | new AI Assurance lifecycle/state required |
| Dispatch has Intent/Skill refs | refs grant mutation authority |
