# V410-T04B R3 Repair Implementation Map

Exact baseline: `30334e8c7b90a327f8597b86c88c785b98df07f7`.

Current owner/readback blobs:

- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` @ `1a05cb3878000b2be9276ced0d42de6e7544cbd7`
- `schemas/agent-event-v2.schema.json` @ `945828741bb634cf4751559673629e040c69e6e2`
- `templates/agent-event-comment.md` @ `0a17dc3854368385c8e5e74233e6bf6255f00704`
- `schemas/review-finding-v1.schema.json` @ `508d43f65573fa2b0bcaca4405282114d5479481`
- `schemas/review-aggregation-v1.schema.json` @ `4c69f568d6521182cd8c50983e28a9ad6062440b`
- `scripts/v40_rules.py` @ `0567e744b5f53ca0244c95ce660a64901f2a0bd2`
- `scripts/v40_semantics.py` @ `85dacf8fcf24ddea2f79b8a43bd6ce52bc1928ba`
- Task Pack R1 @ `3300f8494ecb2120d96fff520cd09270b538344b`
- L3 Wave D R1 @ `9a0d133c6cf82e6a49d2ee37e58e8ad342a79495`
- Execution Pack Standard @ `c7bd2e4ffb87a0ac7fabc54fd78c4eb1fae6ef0d`

Historical candidate input only:
- PR #901 HEAD `82ac1e909875bea1b4838cf010f768e601802ca8`
- Fresh Review R1: P1-1 + P1-2, no verdict transfer.

Reuse-first direction:
1. Preserve historical REVIEW_RESULT compatibility.
2. Strengthen new/current material-finding writer/admission/conformance behavior rather than making old payloads invalid.
3. Reuse `review-finding-v1` duplicate disposition/equivalence semantics instead of inventing identity coordination or a registry.
4. Aggregate only current exact-subject accepted facts; ambiguous equivalence/conflict fails closed.
5. Preserve all independent reviewer provenance.
