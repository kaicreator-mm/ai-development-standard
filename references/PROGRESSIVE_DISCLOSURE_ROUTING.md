# Progressive Disclosure Routing Reference

Status: **derived routing reference; non-authoritative**.

This reference defines the v4.7 T05 read-routing convention. It does not create a Context Snapshot, a registry, an authority store, a lifecycle state, or a mutation/merge/release permissions engine. The canonical semantic registry remains `standard-manifest.json` and is interpreted with the merged T01 authority/applicability schema and T02 resolver.

## Inputs and trust boundary

A routing request begins from durable project context and an immutable ADS checkout:

1. repository `AGENTS.md`;
2. project `.dev-standard/VERSION` immutable ADS pin;
3. pinned ADS `AGENTS.md` and `standard-manifest.json`;
4. canonical owners resolved by T02 for actually applicable concerns;
5. project `.dev-standard/PROJECT_OVERRIDES.md`;
6. only project-selected language/archetype profiles;
7. the exact Task Pack and current GitHub Task/PR subject;
8. when execution is requested, an already-existing exact-subject Dispatch and Execution Pack.

`resolve_standard_read_set.py` accepts current Task/PR/Dispatch facts only through an injected synchronous `authority_reader`. That adapter is a trust boundary: in production it must re-read the durable GitHub/repository source during the routing invocation. A caller-provided Boolean such as `current=true`, `review_passed=true`, provider availability, or a chat assertion is not currentness evidence.

Unit tests may inject deterministic authority facts, but the result must remain labelled `TEST_FIXTURE`. Fixture proof is not live external-authority validation.

## Precedence and omission

Precedence follows authority/currentness, never context size or file ordering. Repository/GitHub durable facts with the required exact identity defeat stale chat, memory, summaries, or copied handoff text.

`ALWAYS` semantic registry entries are read. `MATERIALITY_DRIVEN`, `PROJECT_DEFINED`, and `OPTIONAL` entries are omitted unless the current durable Task/project authority establishes applicability. Unknown materiality fails closed. Optional capability context omitted by the project is not added merely because the file/tool/provider exists.

A project may select language/archetype profile files in `PROJECT_OVERRIDES.md` using:

```text
- language_profile_ref: ads:<relative-path> | project:<relative-path>
- archetype_profile_ref: ads:<relative-path> | project:<relative-path>
```

Only explicit selections are loaded. Missing/escaping selections fail closed; no default profile is guessed.

## Fail-closed cases

Routing is `BLOCKED` and names the owner/source when any material input is unresolved, including:

- missing or mismatched project ADS pin;
- duplicate/conflicting/broken canonical registry owners;
- requested concern with unknown or contradictory applicability;
- disabled/unknown project capability requested by the Task;
- missing Task Pack/Issue identity;
- stale or mismatched exact Task/PR subject or expected base;
- execution without current Dispatch + Execution Pack bound to the same exact subject;
- a semantic concern for which no merged canonical owner exists;
- mutation intent without separate Task/Dispatch mutation authority.

No fallback owner is chosen by file order, context volume, model preference, tool availability, provider availability, or an unmerged historical proposal.

## Result semantics

`RESOLVED` means only **the derived read plan is internally resolvable for the supplied current authority observations**. It never means Task READY, Validation PASS, Review PASS, Release READY, deployment success, runtime health, or mutation authorization. The result always reports `authority_effect=NONE`, `gate_effect=NONE`, and `mutation_authorized=false`; the owning Task/Dispatch/Validation/Review/Release authorities retain those decisions.

The emitted read set and trace are debug/provenance aids. They are not durable Context Snapshots and must not be persisted as a competing source of truth.
