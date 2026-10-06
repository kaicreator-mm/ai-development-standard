# V410-T04B R4 implementation map

Repair base exact subject:
- HEAD `e03beedd9d02336407365efa66efc43d34e96954`
- tree `17a713fd7e65e879b4bf76a8d364e1ade20cfb51`

Pinned owner/readback blobs at R3 subject:
- GITHUB_AGENT_INTERACTION_PROTOCOL.md @ d5dbf810efb11db4f5cd6cfede4eb110beca8c36
- agent-event-v2.schema.json @ f7e7af8462278f507f94f84b05a4b1faf38bdd39
- agent-event-comment.md @ 9018af8b3b2b8b9c5db347cfc1ea88bc24ab3477
- review-finding-v1.schema.json @ 508d43f65573fa2b0bcaca4405282114d5479481
- review-aggregation-v1.schema.json @ 4c69f568d6521182cd8c50983e28a9ad6062440b
- v40_rules.py @ 0567e744b5f53ca0244c95ce660a64901f2a0bd2
- v40_semantics.py @ 85dacf8fcf24ddea2f79b8a43bd6ce52bc1928ba
- focused test @ a52de9c2183ca0c75f4002069a0c487c7bf03b98

R4 minimal seams:
1. Fix canonical writer fixture first; add bucket↔records exact consistency oracle.
2. Treat REVIEW_RESULT finding emission and later review-finding-v1 disposition as separate durable facts.
3. Build equivalence from original finding facts + current same-subject disposition facts, not by mutating/re-emitting the original reviewer event.
4. Use explicit disposition currentness/subject identity; competing accepted dispositions are conflict, not latest-wins.
5. Preserve both reviewer provenance sets in the derived equivalence class.
6. Touch v40_rules/v40_semantics only if their existing review-finding validator cannot express the required durable disposition transition.
