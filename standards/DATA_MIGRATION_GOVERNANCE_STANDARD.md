# Data & Migration Governance Standard

Status: **Normative — v4.2**

## 1. Purpose

This standard owns persistent-state transition semantics: exact source and target state identity, ordered transition/dependency intent, environment applicability, destructive/high-risk treatment, and recovery strategy.

It does not own Deployment result, Incident lifecycle, Validation PASS/FAIL, Release Qualification, or a universal migration framework/database.

## 2. Authority boundary

This standard owns:

- persistent-state source and target identity;
- migration/transition direction;
- transition mechanism, ordered steps and dependencies when material;
- applicability to runtime/database/environment tuples;
- migration risk and destructive-change treatment;
- recovery strategy and prerequisites;
- evidence distinctions among fresh install, upgrade, interrupted recovery and other transition subjects.

It references but does not redefine:

- Deployment orchestration/result;
- external side-effect authority and credential governance;
- Validation evidence truth;
- Incident/operational recovery;
- Release Qualification.

A Migration Transition is a durable description/evidence subject. It is not a workflow Gate result.

## 3. Exact source and target state

A material migration MUST identify both the source persistent-state identity and the intended target persistent-state identity.

Identity SHOULD be strong enough for the selected datastore and migration mechanism and MAY include schema revision, migration-set digest, application/runtime version, database-engine version, environment identity, or other durable references.

`migration files exist` MUST NOT substitute for either the actual source state or the observed target state.

## 4. Directionality

A transition is directional: `A -> B` is not evidence for `B -> A`.

A successful forward transition MUST NOT imply that an inverse/down migration exists, is safe, or is the selected recovery strategy.

Likewise, a documented rollback/down migration MUST NOT be treated as executed recovery evidence until it is actually exercised on the applicable subject.

## 5. Fresh install, upgrade, and recovery are distinct subjects

These subjects MUST NOT be collapsed:

- **fresh install**: initializes persistent state from an empty/new baseline;
- **upgrade**: transforms an existing source state into a target state;
- **interrupted recovery**: restores or advances from a partially executed or failed transition;
- **rollback/reversion**: moves to a prior or alternate supported state where that strategy is valid.

Therefore:

- fresh-install PASS **MUST NOT imply** upgrade PASS;
- successful upgrade **MUST NOT imply** interrupted-recovery PASS;
- one recovery strategy **MUST NOT imply** another strategy is valid.

## 6. Applicability tuple and non-substitution

Migration evidence is valid only for the dimensions actually exercised. Material applicability MAY include:

- datastore kind and engine/version;
- source and target schema/data baseline;
- application/runtime version;
- environment class or exact environment;
- extensions, collation, feature flags, storage mode, or other mechanism-specific dimensions.

A tuple proven for one materially different engine/version/environment MUST NOT be substituted for another without explicit compatibility evidence.

Staging success MUST NOT automatically become production transition evidence. A local SQLite fixture MUST NOT automatically prove a production PostgreSQL upgrade. Equivalent substitutions require explicit evidence rather than naming similarity.

## 7. Migration presence is not execution

The following facts are not equivalent:

- migration definition/file exists;
- planner/tool can enumerate it;
- dry-run parses successfully;
- migration was executed;
- target state was verified;
- recovery was exercised.

A repository artifact or generated migration script is mechanism evidence only. `migration file exists -> migration executed` is a forbidden inference.

## 8. Risk and destructive changes

High-risk or destructive transitions require explicit risk and recovery treatment proportional to impact.

Examples MAY include destructive column/table removal, irreversible encoding conversion, lossy transforms, large backfills, long locks, constraint enforcement on existing data, storage-engine changes, or transitions that cannot be retried safely.

No universal risk enum is required by this standard. Projects MAY strengthen classification through PROJECT_OVERRIDES, but MUST NOT weaken evidence or recovery obligations for a material destructive transition.

## 9. Recovery is required semantics; down migration is not universal

A material migration MUST identify a recovery strategy and its prerequisites. The strategy MAY be one or more of:

- restore from validated backup/snapshot;
- forward repair / roll-forward;
- expand/contract sequencing;
- application compatibility bridge;
- compensating transition;
- explicit down/rollback migration where safe and supported;
- environment rebuild combined with persistent-state restore.

This standard does **not** require every migration to provide an inverse migration.

`no down migration -> no recovery strategy required` is forbidden.

## 10. Production mutation authority

Ability to connect, credentials, tooling, a generated plan, or a valid migration record does not authorize a production mutation.

Production or otherwise material external mutation MUST have explicit applicable side-effect authority under the owning execution/external-system rules. Credential capability is never mutation authority.

`credential available -> production migration authorized` is a forbidden inference.

## 11. Required forbidden-inference matrix

| Input fact | Forbidden inferred conclusion |
|---|---|
| fresh install succeeds | upgrade succeeds |
| `A -> B` succeeds | `B -> A` succeeds |
| migration file/definition exists | migration executed |
| credentials/tool can mutate production | production mutation authorized |
| no down migration exists | no recovery strategy is required |

Implementations and conformance tests MUST preserve these negatives.

## 12. Fast Path and materiality

Fast Path remains proportional. Changes with no persistent-state transition need not create empty migration records.

A small code diff MUST NOT bypass migration evidence when it changes durable state, upgrade ordering, data interpretation, compatibility window, or recovery obligations.

## 13. Machine-contract relation

`schemas/migration-transition-v1.schema.json` is the default v4.2 machine representation for transition identity, applicability and recovery references. It intentionally does not define Validation PASS/FAIL or Deployment result state.

Tools/frameworks MAY emit mechanism-specific plans, histories or checksums referenced from the transition. Those artifacts remain subordinate evidence.

## 14. Failure handling

Unknown source state, unresolved dependency ordering, unavailable target environment, missing recovery prerequisites, or absent production authority MUST remain explicit uncertainty/BLOCKED in the owning workflow. They MUST NOT be normalized into migration success.

When required executable proof cannot run in Web/CI, create an exact-subject Validation handoff that binds the datastore/runtime/environment tuple and side-effect boundary actually required.
