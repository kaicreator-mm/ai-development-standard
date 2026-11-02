# WEB_BUILDER / LOCAL_VALIDATION — Product R0

**Target:** ADS v4.19.0  
**Status:** Product Review PASS_WITH_P2; Owner-authorized Product Freeze candidate  
**Source intake:** [ADS #1353](https://github.com/kaicreator-mm/ai-development-standard/issues/1353)  
**Independent Product Review:** #1353 comment 6585120296  
**Owner unblocking authority:** #1353 comment 6585163422

## 1. Problem

The published ADS v4.18.0 Dispatch contract cannot represent the intended Web-first execution model without a false profile/environment mapping:

- `LOCAL_BUILDER` projects to `LOCAL`.
- `LOCAL_VALIDATOR` projects to `LOCAL`.
- `WEB_REVIEWER` projects to `WEB` but is constrained to `role=reviewer`.
- There is no conforming `role=builder + execution_environment=WEB` profile.

This is a real normative gap, not a free-form naming issue: the Dispatch JSON Schema, semantic environment projection and conformance tests all enforce the legacy profile mapping. Released v4.18.0 remains immutable.

## 2. Product outcome

Make Web the primary source Builder and keep Local Agent as a supplementary validation-only executor, using the existing single Dispatch/Claim architecture.

| Canonical profile for new work | Dispatch role | Environment | Responsibility |
|---|---|---|---|
| `WEB_BUILDER` | `builder` | `WEB` | Primary source analysis, design, implementation, tests, repair, PR authoring and integration preparation |
| `LOCAL_VALIDATION` | `validator` | `LOCAL` | Exact-SHA validation only for a genuine local-environment capability gap |

## 3. User and system behavior

1. Ordinary new implementation work uses `WEB_BUILDER`; Web owns source implementation and the GitHub progress record.
2. Prefer Web and CI/Woodpecker for repeatable validation. Do not dispatch Local Validation if current Web/CI evidence already satisfies the Task's validation requirements.
3. Use `LOCAL_VALIDATION` only when a declared validation obligation cannot be truthfully satisfied by Web or available CI runners (for example Windows-specific Host/runtime, installed browser/driver, physical hardware/peripheral, or designated credential boundary).
4. Local Validation consumes a stabilized exact SHA and returns environment, toolchain, command, exit status and reproducible evidence. It does not edit source, tests, fixtures, lockfiles, workflow/configuration or documentation; it does not repair, create implementation commits/PRs, change scope, merge or close the Builder Task.
5. If Local Validation finds a defect, it returns FAIL with exact-SHA evidence. WEB_BUILDER performs any separately authorized repair and submits a new SHA; affected validation is repeated against that new SHA.
6. Environment inability is BLOCKED; a real defect is FAIL; unexecuted work is NOT_RUN; ambiguous evidence is UNKNOWN. None is silently promoted to PASS.
7. Existing `LOCAL_BUILDER`, `LOCAL_VALIDATOR`, `WEB_REVIEWER`, `PLATFORM_VALIDATOR` and `CLOSURE_VALIDATOR` mappings remain readable and semantically unchanged for historical pinned records.
8. `LOCAL_BUILDER` is not the default for new v4.19 work. Retain it for v4.18-pinned historical records and explicitly grandfathered workflows only; ordinary new implementation uses `WEB_BUILDER`. Do not add a new claim key or authority-bearing field to encode this policy.

## 4. Authority and compatibility invariants

- Profile and execution environment are routing/provenance metadata; neither grants source, validation, approval, merge or release authority.
- Role remains the authority boundary. `WEB_BUILDER` is builder-only; `LOCAL_VALIDATION` is validator-only.
- Existing role requirements remain: Builder requires its Task Pack; Validator requires exact `requested_head_sha` and `validation_profile`.
- The protected claim key remains based on the existing repository/task/role/compatibility-group tuple. Profile, execution environment, scheduler origin, provider and session identity do not enter the key.
- Keep one canonical Dispatch lifecycle, one CAS/Claim protocol and the existing Builder/Validator queues. No second scheduler, second Claim lifecycle, automatic Local handoff or environment-derived authority.
- New Dispatch publication still validates the fully enriched object against the exact effective project-pinned schema and existing admission/currentness predicates before canonical publication.
- v4.18.0 is not edited, reinterpreted or retroactively migrated.

## 5. Scope

### In scope

- Add the two prospective profile names to the canonical Dispatch schema and role/profile constraints.
- Add deterministic environment projection for `WEB_BUILDER → WEB` and `LOCAL_VALIDATION → LOCAL`.
- Update the normative profile inventories in Execution Pack and GitHub Agent Interaction Protocol.
- Extend schema, semantic projection, legacy-compatibility and protected-claim-key conformance tests.
- Preserve CI-first and exact-SHA validation ownership already defined by ADS #1241.

### Explicitly out of scope

- Any v4.18.0 source/tag change or retroactive Dispatch rewrite.
- New role values, Claim keys, state machines, schedulers, queues, event families or automatic handoff.
- Direct Local Agent source implementation or repair.
- New authority inferred from profile/environment labels.
- Changes to Tally, runx, Shun Assistant or any downstream repository's source/Task state.
- Merge to main, v4.19.0 publication, tag or release under this Product Freeze.

## 6. Acceptance criteria

- [ ] `WEB_BUILDER + role=builder` is schema-valid and projects to `WEB`.
- [ ] `LOCAL_VALIDATION + role=validator` is schema-valid and projects to `LOCAL`.
- [ ] Each new profile paired with the wrong role is rejected fail-closed.
- [ ] Each new profile paired with a contradictory explicit environment is rejected fail-closed.
- [ ] All five legacy profiles preserve their exact historical schema/readability and environment semantics.
- [ ] Profile/environment changes do not alter the protected claim key for the same repository/task/role/compatibility group.
- [ ] The new profiles add no source/approval/merge/release authority.
- [ ] Local Validation remains exact-SHA and validation-only; Web/CI evidence prevents unnecessary Local dispatch.
- [ ] Missing local capability or environment yields BLOCKED/NOT_RUN, never PASS.
- [ ] Exact effective-schema prepublication admission and serialized Claim/CAS remain unchanged.
- [ ] Full exact-tree syntax preflight runs before any CI qualification; independent source review and exact-SHA CI are completed before release consideration.

## 7. Product Review dispositions

The independent Product Review is PASS_WITH_P2 (P0=0, P1=0, P2=3). The P2 requirements are resolved here:
1. Update `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` profile inventory.
2. Extend `scripts/test_protocol_schemas.py`, `scripts/test_v410_t06b_multi_dispatch_conformance.py` and `scripts/test_execution_architecture.py`.
3. Preserve `LOCAL_BUILDER` only for historical pinned records/explicitly grandfathered workflows; new ordinary work defaults to `WEB_BUILDER`.

These are bounded implementation details, not Product blockers.
