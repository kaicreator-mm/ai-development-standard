# V410-T04B Implementation Map

Exact baseline: `7a0ee000174512df85bf3d2cd611e8b2cf55c840`.

## Primary owner-local seam

- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` @ `1a05cb3878000b2be9276ced0d42de6e7544cbd7`
  - Review execution/event semantics, exact-subject currentness, finding/result reconstruction.
- `schemas/agent-event-v2.schema.json` @ `945828741bb634cf4751559673629e040c69e6e2`
  - Existing `REVIEW_RESULT.findings` family; additive structure only if deterministic reconstruction requires it.

## Consumed integrated authority — do not rewrite

- `standards/DEVELOPMENT_WORKFLOW.md` @ `a7fef842927e58a93b671fe9869b9395559845ac`
  - T04A root-defect classes, repair routing, non-converging escalation.
- `standards/VALIDATION_STANDARD.md` @ `1522b85f9e68cc4a1591ea5899b53c224998e5a8`
  - Gate/currentness companion authority.
- `templates/agent-event-comment.md` @ `0a17dc3854368385c8e5e74233e6bf6255f00704`
  - Projection surface only if materially affected.

## Integrated predecessor composition

T02B's `parent_dispatch_ref` / `responsibility_mode` are existing-family causation/provenance facts. T04B may consume them where relevant but must not duplicate or widen their semantics.

Central manifest/discovery changes are excluded and route to T06A/T06B.