# Intent & Assumption Governance Standard

Status: **Normative — v4.6**. Owns classification, disposition and authority-bound routing of material intent and uncertainty. It does **not** issue Product Freeze, Architecture Freeze, Task scope, Review, Validation, Release or Agent lifecycle decisions.

## 1. Truth classes are distinct

Use the existing `schemas/intent-assumption-record-v1.schema.json` as the **only** v4.6 default Intent / Assumption machine family. Its `classification` values have distinct meanings:

- `USER_INTENT`: traceable statement actually expressed by the user, bound to its approved source reference and currentness. Even an authentic user statement is not automatically Frozen Product.
- `INTERPRETATION`: an Agent's or analyst's understanding of user intent; its author and evidence must remain attributable. Never relabel interpretation as the user's own words.
- `ASSUMPTION`: a stated, potentially falsifiable working proposition awaiting evidence or owner acceptance. Record materiality, source/evidence where available and next decision owner.
- `UNKNOWN`: information not established by available current evidence. Absence of a contrary observation is not positive proof.
- `DECISION_REQUIRED`: explicit unresolved choice/conflict assigned to its applicable owning decision path, not implied Agent authority.
- `DURABLE_REQUIREMENT_REF`: **reference to** a requirement independently promoted through existing Product/Architecture/Task authority; the Intent Record did not create that requirement.

A record does not become more authoritative because a powerful model, long reasoning chain, previous chat, majority of Agents or current tool result expressed it. Materiality and currentness must be explicit; `UNKNOWN` materiality is not silently `NON_MATERIAL`.

## 2. Machine record and provenance

Each material record MUST identify exact `record_id`, `repository`, `subject_ref`, `classification`, `content_ref`, `materiality`, `currentness_ref`, structured `disposition`, `created_by_ref` and `created_at` per the existing T01 contract. `content_ref` is a durable, reviewable statement/evidence pointer or digest, not necessarily a transcript; where interpretation, assumption or promotion depends on a distinct original source, record `source_ref` and applicable `evidence_refs` without copying secrets or granting that source authority. Record `contradiction_refs` and `supersedes_refs` when material; append a new durable fact instead of silently rewriting prior records. Broken or unresolvable source/currentness references must fail closed for material actions.

Historical v4/v4.1–v4.5 Dispatch or Execution Pack payloads without the new optional `intent_assumption_record_refs` remain valid. Record creation is materiality-driven: Fast Path does not require empty records for genuinely non-material intent handling, but it cannot omit a material unresolved question that changes scope, authority or required gate.

## 3. Disposition mapping: Frozen L2 conceptual to actual v1 wire

The Frozen L2 §4 conceptual names express workflow intent, **not extra machine enum values**. The T01 schema intentionally has wire actions `RETAIN`, `CLARIFY`, `PROMOTE_BY_OWNER`, `REJECT`, `SUPERSEDE`, `BLOCK`. Apply this unambiguous mapping:

| Frozen L2 conceptual | v1 wire disposition | Required routing/evidence condition |
| --- | --- | --- |
| retain | `RETAIN` | Preserve source/currentness and explicitly keep classification unchanged. |
| `ROUTE` | `CLARIFY` | For a material question, `disposition.target_ref` identifies an existing owning decision destination; if the owner/target cannot be identified, use `BLOCK`, never invent it. |
| reject | `REJECT` | Record owner/evidence-backed rejection without rewriting the original user/source assertion. |
| `PROMOTE_REF` | `PROMOTE_BY_OWNER` | This is a **request/association**, not proof of promotion. Route to existing Product/Architecture/Task owner using `disposition.target_ref`; a valid promoted outcome additionally requires a separate current owner-issued target requirement fact and the v1 `DURABLE_REQUIREMENT_REF` linkage described in §4. |
| `SUPERSEDE_REF` | `SUPERSEDE` | Identify prior fact(s) with `supersedes_refs` and material replacement/owner decision in `disposition.target_ref`; preserve originals. If the successor or authority is UNKNOWN, `BLOCK`. |
| unresolved conflict | `BLOCK` | Preserve `contradiction_refs`, materiality and owner escalation; do not fabricate a precedence winner. |

`source_ref`, `evidence_refs`, `disposition.target_ref` and top-level promotion references are distinct. A routing target is not evidence of an issued requirement, and the `created_by_ref` actor is not by itself a valid promotion authority.

## 4. Promotion and contradiction gate

An `INTERPRETATION`, `ASSUMPTION` or `UNKNOWN` record MUST NOT self-promote into durable Product/Architecture/Task truth; classification=`USER_INTENT` MUST NOT by itself imply Frozen Product. `PROMOTE_BY_OWNER` on any record is only a request or record of routing, even if an Agent claims success. A legitimate `DURABLE_REQUIREMENT_REF` MUST pass the T01 machine contract's **both** `promotion_authority_ref` and `promoted_requirement_ref` check, and the referenced requirement MUST be an actual current decision from the existing correct owner, backed by applicable source/evidence/currentness. Structurally valid references alone do not prove that owner action occurred. An Agent may not populate those references to manufacture the target authority.

When a material ambiguity can change acceptance, safety, irreversible side effects, public promises or Task scope, stop and route `DECISION_REQUIRED` to the owning human/project Product, Architecture or Task authority with explicit decision target. When material sources contradict, preserve `contradiction_refs` and `BLOCK`/owner routing until a durable owner decision resolves it; never assume the newest source or majority vote wins. Supercession does not erase the contradicted history or stale-identity evidence.

## 5. Failure handling and integration boundaries

Missing source/currentness, stale exact subject, unresolved promotion owner, guessed routing target, or missing promotion fact means `UNKNOWN`, `DECISION_REQUIRED` or `BLOCK` as appropriate; it cannot produce a validated requirement. Do not leak raw secrets, signed URLs or unapproved sensitive user information into ordinary durable records. Reuse v4.1 Configuration/Secrets and the existing secure evidence owner.

Only the existing Frozen Product/L2/Task Pack owners may accept and freeze their respective material. T02 produces no new gate state, Context Snapshot, Skill procedure authority, Dispatch state or v4.7 repository-wide resolver. A reclassification affecting frozen requirements must take the existing formal change/amendment path; neither record serialization nor model consensus authorizes silent mutation.

## 6. Executable adversarial minimum

Conformance MUST distinguish a real cited user statement from Agent interpretation; preserve material assumption/UNKNOWN; reject chat→Frozen Product, interpretation→user fact, assumption/UNKNOWN→durable requirement, `PROMOTE_BY_OWNER` without owner-issued target/current references, one missing `DURABLE_REQUIREMENT_REF` promotion reference, and contradiction→guessed winner. Preserve a positive current owner-issued requirement reference and material owner-routed clarification without declaring Product Freeze from this test.