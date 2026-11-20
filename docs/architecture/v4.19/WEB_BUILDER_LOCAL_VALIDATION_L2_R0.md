# WEB_BUILDER / LOCAL_VALIDATION — L2 Architecture R0

**Target:** ADS v4.19.0  
**Product input:** `docs/product/v4.19/WEB_BUILDER_LOCAL_VALIDATION_PRODUCT_R0.md`  
**Product Freeze:** #1353 comment 6585179041, Product commit `44562165d715a347a4ee00c010b8fb6e302530c7`  
**Owner bootstrap authority:** #1353 comment 6585163422

## 1. Architecture decision

Extend the existing canonical Dispatch architecture with two prospective execution profiles. Do not add roles, lifecycle states, protected claim-key fields, schedulers, queues, dispatch/event families or automatic handoff.

| Profile | Role | Projected environment | Canonical use |
|---|---|---|---|
| `WEB_BUILDER` | `builder` | `WEB` | Primary implementation and repair executor |
| `LOCAL_VALIDATION` | `validator` | `LOCAL` | Supplementary exact-SHA validation for genuine local-only capability gaps |

Legacy mappings remain:
- `LOCAL_BUILDER → builder / LOCAL`
- `LOCAL_VALIDATOR → validator / LOCAL`
- `WEB_REVIEWER → reviewer / WEB`
- `PLATFORM_VALIDATOR` and `CLOSURE_VALIDATOR` remain environment-orthogonal and require explicit environment when routing needs one.

## 2. Contract layers

### 2.1 Dispatch JSON Schema

- Add both names to `execution_profile.enum`.
- Add exact profile-to-role couplings: `WEB_BUILDER → builder`; `LOCAL_VALIDATION → validator`.
- Existing role conditionals continue to require Task Pack for Builder and requested exact HEAD + validation profile for Validator.
- Keep `execution_environment` as optional WEB/LOCAL metadata; it does not grant authority.
- Keep all legacy enum values and couplings.

### 2.2 Semantic projection

Add only:
- `WEB_BUILDER: WEB`
- `LOCAL_VALIDATION: LOCAL`

The existing contradiction check remains authoritative: an explicit environment inconsistent with the selected profile is rejected. Unknown/orthogonal profiles remain UNKNOWN unless their existing explicit-environment rule applies. Do not change the protected claim-key derivation.

### 2.3 Normative profile inventories

Update the profile lists in:
- `standards/EXECUTION_PACK_STANDARD.md`
- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`

The GitHub protocol continues to require fully enriched schema validation against the effective project-pinned ADS revision before a new canonical Dispatch is published. No free-form profile alias or silent normalization is permitted.

## 3. Authority and admission

- The existing Dispatch role determines Builder/Validator/Reviewer responsibility.
- The profile only selects a bounded execution profile/environment; it does not grant permission.
- The protected claim key remains repository + Task + role + normalized compatibility group. Execution profile, environment, scheduler origin, operator/provider and session remain outside the key.
- Existing CAS generation, serialized admission, Task dependencies, JIT branch/Execution Pack binding, currentness and source write-set rules remain unchanged.
- Profile changes do not bypass Task Pack, Execution Pack, accepted Claim, independence, Validation, Review, Merge or Release requirements.
- v4.18.0 stays immutable and historical Dispatches are not rewritten.

## 4. Execution semantics

### WEB_BUILDER

Owns the implementation path under the existing accepted Builder authority: analyze, design, implement, test, repair, update the PR and publish GitHub evidence. It is the default for ordinary new implementation work in v4.19.

`LOCAL_BUILDER` remains readable for v4.18-pinned history and explicitly grandfathered workflows, but is not the default for new v4.19 work.

### LOCAL_VALIDATION

Consumes an already stabilized exact SHA and a declared validation profile. It:
- checks out/verifies that exact SHA;
- records actual local OS/runtime/toolchain, command, exit status, logs/artifacts and environment identity;
- does not mutate source, tests, fixtures, lockfiles, workflow/configuration or documentation;
- does not repair, commit, create implementation PRs, change scope, merge or close the Builder Task.

A defect is returned as FAIL with reproducible evidence. WEB_BUILDER performs any separately authorized repair; affected validation is repeated against the new exact SHA. Environment inability is BLOCKED, unexecuted is NOT_RUN and ambiguous is UNKNOWN.

### CI-first selection

Use Web/CI for repeatable checks. Local Validation is only selected if the required environment/capability is unavailable to Web and available CI runners. Existing current Web/CI evidence suppresses redundant Local dispatch. No automatic handoff is added.

## 5. Conformance invariants

1. New profile + matching role is accepted.
2. New profile + wrong role is rejected by the actual schema.
3. New profile + contradictory explicit environment is rejected by semantic projection.
4. All five legacy profiles preserve their existing mapping and schema readability.
5. For the same repository/Task/role/compatibility group, changing only profile/environment does not change the protected claim key.
6. Changing role still changes the role slot of the existing key; no attempt is made to collapse Builder and Validator claims.
7. Environment/profile labels never grant source write, validation, approval, merge or release authority.
8. No new scheduler, Claim lifecycle, key slot, queue, event family, automatic Local handoff or Local source-write permission appears.

## 6. Failure handling

| Condition | Result |
|---|---|
| Unknown profile | UNKNOWN / fail closed for dispatch admission |
| Profile-role mismatch | INVALID_SCHEMA / reject before publication |
| Explicit environment contradicts profile | ENVIRONMENT_PROFILE_CONTRADICTION |
| Local environment/capability unavailable | BLOCKED or NOT_RUN, never PASS |
| Local validation detects source defect | FAIL with exact-SHA evidence; Web repairs |
| Repair changes SHA | Prior validation does not transfer; rerun affected checks on new SHA |
| Effective pinned schema unavailable/stale | BLOCKED_STALE_SCHEMA / zero accepted dispatch mutation |

## 7. Implementation boundary

One bounded implementation Task owns the schema, projection, normative profile inventories and conformance tests together. These files form one cross-layer contract and should not be split into competing writers.

Exact write set:
- `schemas/dispatch.schema.json`
- `scripts/v34_rules.py`
- `standards/EXECUTION_PACK_STANDARD.md`
- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`
- `scripts/test_protocol_schemas.py`
- `scripts/test_v410_t06b_multi_dispatch_conformance.py`
- `scripts/test_execution_architecture.py`

Pre-CI sequence:
1. exact-tree syntax preflight for all changed Python and JSON files;
2. focused schema/projection/claim-key tests;
3. full ADS test suite / conformance runner;
4. self-hosted Woodpecker CI on the exact PR SHA;
5. independent source Review and exact-SHA requalification.

The first implementation is a one-time Owner-authorized v4.19 bootstrap recorded in #1353 comment 6585163422 because the released v4.18 schema cannot represent the profile being added. Do not fabricate a v4.18 Web Builder Dispatch/Claim. Once v4.19 is adopted, ordinary source tasks use its canonical `WEB_BUILDER` Dispatch.
