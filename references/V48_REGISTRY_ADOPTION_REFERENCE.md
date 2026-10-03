# v4.8 Registry / Discoverability / Adoption Reference — T-006

Status: **non-authoritative integration reference; metadata only.**

```text
authority_effect=NONE
gate_effect=NONE
mutation_authorized=false
REGISTRY_AUTHORITY_EFFECT=NONE
INTERCHANGE_REUSED=YES
V48_MACHINE_FAMILY_COUNT=3
V47_LINEAGE=LINEAGE_ONLY_NOT_CURRENT_V4_8_AUTHORITY
PROVIDER_IDENTITY=NOT_AUTHORITY
CAPABILITY_EVIDENCE=NOT_CURRENT_VALIDATION_REVIEW_TRUTH
FAST_PATH=LIGHTWEIGHT
```

This reference is the T-006 discovery map for the v4.8 machine-contract families
in `standard-manifest.json`. Manifest membership, this reference, project-adoption
text, provider/model identity, capability claims/evidence, or a successful focused
verifier never grant mutation, merge, Validation PASS, Review PASS, Release READY,
scheduler admission, or any permission. Authority remains with the pinned normative
owners, Frozen Product/L2, the exact Task/Execution Pack write-set, live GitHub
Issue Dependencies, and the exact-currentness Validation/Review/Merge gates.

## 1. Discoverable v4.8 machine families

Exactly three new v4.8 machine-contract families are discoverable from the current
manifest. Each entry routes to its already-merged schema/reference owner; discovery
does not restate, copy, or re-own sibling semantics.

| Family | Schema owner (discovery ref) | Reference owner (discovery ref) |
|---|---|---|
| Task Learning Evidence v1 | `schemas/task-learning-v1.schema.json` | `references/TASK_LEARNING_EVIDENCE_REFERENCE.md` |
| Logical Agent Capability Profile v1 | `schemas/agent-capability-profile-v1.schema.json` | `references/AGENT_CAPABILITY_PROFILE_REFERENCE.md` |
| Agent Capability Evidence v1 | `schemas/agent-capability-evidence-v1.schema.json` | `references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md` |

The focused verifiers for these families are discoverable under
`sections.verification` (`scripts/test_v48_task_learning.py`,
`scripts/test_v48_agent_capability_profile.py`,
`scripts/test_v48_agent_capability_evidence.py`, plus this task's
`scripts/test_v48_registry_adoption.py`). Verifier success is implementation
evidence only and is never a gate verdict.

`V48_MACHINE_FAMILY_COUNT=3` is a closed result for T-006: no fourth v4.8
machine-contract family is introduced by this task.

## 2. Interchange reuse

Interchange remains the existing generic v1 family, listed exactly once:

- `schemas/interchange-envelope-v1.schema.json`
- compatibility owner: `references/V48_INTERCHANGE_PROFILE_COMPATIBILITY.md`

`INTERCHANGE_REUSED=YES` means the already-merged Interchange v1 schema and
`ai-dev:event:v2` writer/admission protocol are reused as-is. T-006 introduces no
Interchange v2, no second Interchange owner, and no new exchange family. The
envelope keeps `authority_effect=CORRELATION_ONLY_NON_AUTHORITATIVE`; it
correlates durable refs and never carries workflow/gate authority.

## 3. Progressive-disclosure read behavior

Discovery is a read-routing convention, not a loading requirement:

1. resolve the project's immutable standard pin (`.dev-standard/VERSION`) and read
   this revision's `standard-manifest.json` as the discoverability inventory — an
   index, not a permission engine;
2. always-available surfaces stay as defined by the pinned owners and project
   overrides; the three new v4.8 families are optional, materiality-driven
   discovery entries;
3. a family's schema/reference is loaded only when the current Task/project
   authority establishes it as applicable to the work; registry presence alone
   never makes optional context mandatory;
4. a project that does not use a family simply does not load it; missing usage is
   not a defect and not evidence of non-compliance;
5. precedence follows authority and currentness (durable GitHub/repository facts
   with exact identity), never file order, context size, or chat assertions.

## 4. Fast Path stays lightweight

`FAST_PATH=LIGHTWEIGHT`: the v4 Fast Path remains one directly eligible executor
plus an ordinary Dispatch/Claim; when a Fast Path task produces no material
learning, `TASK_LEARNING=NONE_MATERIAL` remains a valid, complete outcome. Fast
Path tasks are never required to load every optional family/reference listed in
the manifest, and registry growth never widens the Fast Path's required surface.

## 5. Result-semantics boundary

For every artifact this task wired (manifest entries, this reference,
`standards/PROJECT_ADOPTION.md` §2.5, `docs/implementation/4.8.0/MIGRATION_ADOPTION.md`,
`scripts/test_v48_registry_adoption.py`):

- `PROVIDER_IDENTITY=NOT_AUTHORITY`: provider credentials, availability, model
  identity, or runner labels never imply eligibility, correctness, permission,
  or ranking.
- `CAPABILITY_EVIDENCE=NOT_CURRENT_VALIDATION_REVIEW_TRUTH`: capability profile
  or evidence records describe bounded claims about their exact subject; they are
  never current Validation truth, Review truth, or release truth.
- Discovery/adoption text restates no schema field semantics and no sibling owner
  rules; it only routes to them.

## 6. v4.7 lineage boundary

The predecessor branch `version/v4.7.0` contains
`references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md` and
`references/PROGRESSIVE_DISCLOSURE_ROUTING.md`. Those files are **not present on
the current v4.8 base** and are **not registered** in the current manifest.

`V47_LINEAGE=LINEAGE_ONLY_NOT_CURRENT_V4_8_AUTHORITY`: they are read-only design
inputs. T-006 preserves their compatible discovery principles (bounded index,
materiality-driven reads, metadata-only posture) inside the task-owned artifacts
above, without copying the files, without re-creating the v4.7
`semantic_authorities` manifest model, entry schema, or resolver, and without
claiming that branch-local machinery is current v4.8 integration. If a future
requirement truly needs that machinery as current v4.8 authority, that is an
architecture amendment owned by a Controller rebind, not a T-006 widening.
