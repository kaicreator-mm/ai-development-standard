<!-- ads:github:v2 -->
```yaml
schema: ads/github/v2
kind: work_item
data:
  profile: type:blocker
  contract:
    blocking_fact: "Observed blocker and source"
    unblock_condition: "Falsifiable recovery condition"
```

# Blocker — <title>

## Contract

- Target version/task: `<ref>`
- Type: `type:blocker`
- State: `state:blocked`
- Risk: `<low|medium|high|critical>`

## Blocking Fact

<verified blocking condition>

## Affected Work

- `<issue/PR/task>`

## Evidence

<durable evidence/reference>

## Unblock Condition

<observable condition that permits recomputation>

## Owner / Handoff

<who/what can resolve the blocker>

## Forbidden

Do not mark BLOCKED merely because an Agent did not attempt an available required action; distinguish execution failure from unavailable authority/environment.
