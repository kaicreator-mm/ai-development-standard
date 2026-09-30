# Incident, Recovery & Engineering Feedback Standard

Status: **Normative — v4.5**

## 1. Purpose

This standard governs append-oriented incident facts, recovery verification and engineering-feedback routing. It does not redefine Deployment rollback/result, persistent-state migration recovery, Task state, Validation or Release authority.

## 2. Append-oriented incident history

Material incident history MUST preserve prior facts rather than rewriting earlier observations to match the latest outcome. Detection, mitigation, recovery, verification and follow-up are distinct facts that may occur at different times.

```text
DETECTED != MITIGATED
RECOVERED != VERIFIED
VERIFIED != FOLLOW_UP_COMPLETE
```

A later recovery event does not erase earlier failure evidence.

## 3. Incident identity and correlation

Where material, incident events SHOULD correlate the affected artifact/deployment/environment/runtime observation and relevant configuration/external-system facts using their owning references. Correlation does not transfer ownership of those concerns.

## 4. Recovery authority boundaries

Recovery actions MUST use the owning authority for the mutated concern:

- deployment rollback/roll-forward remains v4.4 Deployment Governance;
- persistent-state migration/data recovery remains v4.2 Data/Migration Governance;
- configuration/credential change remains its configuration/secret owner;
- external-system mutation requires its applicable side-effect authority.

Ambiguous production mutation authority blocks the action rather than being inferred from incident urgency.

## 5. Verification after recovery

Operational mitigation or apparent recovery MUST NOT be treated as permanent-fix truth without the required verification. Verification must bind the subject/environment/procedure appropriate to the claim.

```text
service responds again != root cause fixed
rollback completed != corrective change verified
```

## 6. Engineering feedback

A material incident MUST route durable follow-up as applicable to one or more of:

- reproducible defect/bug evidence;
- regression or test scenario;
- test-data/fixture improvement;
- product/architecture decision;
- operational/runbook/configuration improvement;
- standard/process gap.

The route MUST preserve a durable reference from the incident/follow-up fact to the created work/evidence. Incident closure MUST NOT erase required unresolved follow-up.

## 7. Prior evidence is immutable history

Incident facts may invalidate confidence or trigger new evidence requirements, but MUST NOT rewrite a prior exact Release/Deployment/Validation result as though the original execution had produced a different outcome.

## 8. Failure handling

If recovery authority, environment identity, incident subject or required verification is unknown, fail closed and record the unresolved fact. Recovery without required verification/follow-up remains explicit and cannot be collapsed to permanent-fix truth.
