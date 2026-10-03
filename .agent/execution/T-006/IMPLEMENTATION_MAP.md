# T-006 Implementation Map

## Authorized outputs

| Path | Action | Purpose |
|---|---|---|
| `standard-manifest.json` | modify | add the three v4.8 machine-contract discoveries plus already-merged v4.8 references/verifiers |
| `standards/PROJECT_ADOPTION.md` | modify | expose bounded v4.8 adoption / progressive-disclosure guidance |
| `references/V48_REGISTRY_ADOPTION_REFERENCE.md` | create | non-authoritative discovery map and lineage boundary |
| `docs/implementation/4.8.0/MIGRATION_ADOPTION.md` | create | additive migration/adoption note |
| `scripts/test_v48_registry_adoption.py` | create | deterministic focused verifier |

## Read-only owner composition

The Builder composes these already-merged concerns without changing them:

- Task Learning schema/reference/test;
- Logical Agent Capability Profile schema/reference/test;
- Agent Capability Evidence schema/reference/test;
- Execution Architecture Core;
- Interchange v1 schema/profile compatibility;
- Task Learning closeout wiring;
- ADS Evolution Governance.

The current manifest, project-adoption standard, frozen planning artifacts, and sibling conformance tests are also inputs.

## Manifest edit shape

Keep all existing inventory. Add:

- three schema paths to `sections.machine_contracts`;
- the three owner references, `V48_INTERCHANGE_PROFILE_COMPATIBILITY.md`, and `V48_REGISTRY_ADOPTION_REFERENCE.md` to `sections.references`;
- the four sibling focused verifiers and the T-006 focused verifier to `sections.verification`.

Do not add a fourth v4.8 family, duplicate Interchange, or invent a new authority registry model.

## Documentation edit shape

`PROJECT_ADOPTION.md` should link rather than restate owner semantics. The T-006 reference should map discoverability with explicit zero authority effect. The migration note should preserve historical objects and incremental adoption.

## Test implementation shape

The focused verifier should use only Python standard library and repository files. It should produce deterministic, precise failures for inventory count, duplicate paths, missing files, forbidden authority wording, Fast Path regression, and migration compatibility.

It must not contact GitHub, a provider, a runner, or an external host.

## Execution ordering

1. currentness/dependency check;
2. manifest additions;
3. adoption/reference/migration text;
4. focused verifier;
5. focused tests;
6. sibling regressions and repository verifier;
7. exact write-set diff audit;
8. Builder terminal;
9. independent Validation handoff;
10. Fresh Independent Review only after Validation PASS.

## Stop boundaries

Any required mutation outside the five authorized outputs stops execution. In particular, do not fix failing sibling schemas/references/tests inside T-006 and do not import v4.7 branch-only registry resolver/schema machinery.
