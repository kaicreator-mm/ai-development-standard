<!-- ads:github -->
```yaml
schema: ads/github/v3
kind: work_item
data:
  profile: type:bug
  contract:
    observed_behavior: "Source-backed unexpected behavior"
    expected_behavior: "Declared contract expectation"
    acceptance:
      - "Regression witness and bounded fix validation"
```

# <Bug|Fix> — <title>

## Contract

- Target version: `<version>`
- Type: `<type:bug|type:fix>`
- State: `<canonical state>`
- Review Policy: `<required|recommended|not-required>`
- Risk: `<low|medium|high|critical>`
- Baseline / integration target: `<refs>`

## Observed Behavior

<reproducible observation>

## Expected Behavior

<contractual expectation>

## Reproduction / Evidence

<steps, fixture, logs, exact identity>

## Scope / Non-scope

- in: <items>
- out: <items>

## Repair Acceptance

- [ ] regression test fails before/fixed after where practical
- [ ] root contract restored
- [ ] required validation/review satisfied

## Allowed / Forbidden Changes

- allowed: <paths/concerns>
- forbidden: <paths/semantics>

## Completion

<merge/closeout rule>
