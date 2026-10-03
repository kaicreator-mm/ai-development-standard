# v4.8 Registry / Adoption Migration Note — T-006

Task-scoped additive migration/adoption guidance for the v4.8 registry,
discoverability and adoption wiring (Issue #512 / T-006). This document is
guidance and implementation evidence, **not** normative authority: it creates no
gate, no permission, and no lifecycle state.

```text
HISTORICAL_COMPATIBILITY=PRESERVED
NO_DESTRUCTIVE_REWRITE
NO_NEW_INTERCHANGE_FAMILY
```

## 1. Posture

v4.8 registry/adoption wiring is **additive metadata**. Existing projects remain
valid under their pinned standard revision and historical contracts; nothing in
T-006 requires a destructive migration, a payload rewrite, or a new evidence
identity. Historical Task Packs, Execution Packs, Dispatch/Claim records,
Interchange v1 envelopes, `ai-dev:event:v2` events, and Validation/Review
evidence keep their original subject identity and status forever.

`NO_DESTRUCTIVE_REWRITE`: no historical manifest inventory is removed, no
historical PASS/FAIL/CHANGES_REQUESTED is restated, and no old artifact must be
converted to a new family to stay valid.

`NO_NEW_INTERCHANGE_FAMILY`: Interchange remains the existing v1 family
(`schemas/interchange-envelope-v1.schema.json`, listed exactly once). Old
envelopes stay valid; new correlated exchanges keep using v1 with
`authority_effect=CORRELATION_ONLY_NON_AUTHORITATIVE`.

## 2. Additive adoption steps

A project adopts the v4.8 discovery surface only when it wants it:

1. keep the immutable pin procedure from `standards/PROJECT_ADOPTION.md` §2
   unchanged (pin → resolve exact revision → verify identity);
2. optionally read `standard-manifest.json` from the pinned revision as the
   discoverability inventory — an index, never a permission engine;
3. for each new v4.8 family, load its schema/reference **only** when the current
   Task/project authority establishes material applicability:
   - `schemas/task-learning-v1.schema.json` /
     `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`;
   - `schemas/agent-capability-profile-v1.schema.json` /
     `references/AGENT_CAPABILITY_PROFILE_REFERENCE.md`;
   - `schemas/agent-capability-evidence-v1.schema.json` /
     `references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md`;
4. record the chosen posture in `PROJECT_OVERRIDES.md` if the project wants it
   durable; absence of such a declaration is a valid steady state;
5. run the focused verifiers only for adopted families
   (`scripts/test_v48_task_learning.py`,
   `scripts/test_v48_agent_capability_profile.py`,
   `scripts/test_v48_agent_capability_evidence.py`); a project that adopts
   nothing new has nothing new to run.

## 3. Projects that skip one or more new families

Not using an optional family is explicitly supported and is not a defect:

- registry/reference presence alone never makes a family mandatory;
- no gate, Validation tuple, Review policy, or release step may be derived from
  unused discovery entries;
- old projects that never mention the three families remain fully compliant
  under their existing pin; no lint/verifier may fail them for absence of usage;
- discovery entries are consulted only when a task actually touches the
  corresponding concern.

## 4. Fast Path example (descriptive)

A small task that does not produce durable learning proceeds exactly as before:

```text
one directly eligible executor
→ ordinary Dispatch / DISPATCH_CLAIMED
→ implement inside the exact Task Pack write-set
→ task-scoped checks
→ hand off for independent Validation
→ Task Learning outcome: TASK_LEARNING=NONE_MATERIAL
```

`TASK_LEARNING=NONE_MATERIAL` is a valid, complete Fast Path outcome. The Fast
Path never requires loading every optional family/reference registered in the
manifest; `FAST_PATH=LIGHTWEIGHT` is preserved by construction because registry
growth only widens the optional read set, never the required floor.

## 5. Stop / escalation for owner gaps

`STOP_ESCALATION_OWNER_GAP`: if an adoption attempt discovers that a needed
semantic owner, schema, or reference is missing, stale, or contradictory, stop
and escalate to the owning Task/Controller instead of repairing it inside an
adoption surface. In particular:

- do not create a fourth v4.8 machine-contract family;
- do not introduce a new Interchange owner/family/version;
- do not copy v4.7 branch-only registry/progressive-disclosure machinery
  (`references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md`,
  `references/PROGRESSIVE_DISCLOSURE_ROUTING.md`) into v4.8 or claim it as
  current authority — they are lineage/read-only design inputs;
- do not widen the T-005/T-006 task write-sets to fix sibling semantics;
- route genuine resolver/schema/semantic-authority needs to a Controller
  rebind / `ARCHITECTURE_AMENDMENT_REQUIRED`.
