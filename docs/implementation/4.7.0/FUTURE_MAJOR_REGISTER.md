# v4.7 Future-major Convergence Register

Status: **T09 PLANNING INPUT ONLY — NON-AUTHORITATIVE**

This register is the durable landing place for evidence-backed convergence needs that cannot be introduced compatibly in v4.7. It does not amend Frozen Product/L2, grant mutation authority, create a gate, approve a future version, or perform Version Closure/Release Qualification.

```text
AUTHORITY_EFFECT=NONE
MUTATION_AUTHORITY=NONE
GATE_EFFECT=NONE
RELEASE_EFFECT=NONE
```

Canonical source for the future-major boundary: `docs/implementation/4.7.0/PRD.md#14-future-major-register` together with the current Frozen L2/Task authority. T09 only wires discoverability and recording.

## 1. Active evidence-backed findings

No incompatible convergence finding is asserted by the T09 Builder merely by creating this register. Add an entry only when a concrete project/task/review/validation finding supplies durable evidence.

| ID | Evidence / source | Incompatible need | Why v4.7 compatible wiring is insufficient | Compatibility impact | Planning status |
|---|---|---|---|---|---|
| _none_ | — | — | — | — | — |

## 2. Seed classes from Frozen Product §14

These are routing classes, not active defects and not approved designs. When a real finding matches one of them, create an evidence-backed entry above rather than implementing the incompatible change under T09.

| Class | Frozen Product source | v4.7 disposition |
|---|---|---|
| authority-chain redesign | PRD §14 | future-major planning input; do not change core authority hierarchy in T09 |
| incompatible Dispatch/Event redesign | PRD §14 | preserve current compatible contracts in v4.7 |
| state-semantic collapse/change | PRD §14 | preserve qualified owner-specific state dimensions |
| exact-SHA evidence meaning change | PRD §14 | preserve current exact-subject semantics |
| breaking role/profile/schema rename | PRD §14 | retain compatible names/routes or plan a future-major migration |
| stable-path removal without compatible aliasing | PRD §14 | keep stable compatibility routes through v4 |
| historical payload reinterpretation | PRD §14 | preserve original historical meaning and identity |
| mandatory adoption of currently optional capability | PRD §14 | preserve progressive/optional adoption and Fast Path proportionality |

## 3. Entry contract

A new active entry SHOULD record:

```text
ID=<FM-###>
OBSERVED_AT=<issue/pr/review/validation + exact subject when material>
SOURCE_AUTHORITY=<Frozen/Product/L2/owner/task pointer>
CONCERN=<short description>
INCOMPATIBILITY=<what cannot be done compatibly in v4.7>
CURRENT_COMPATIBILITY_ROUTE=<alias/additive/defer/none>
AFFECTED_CONSUMERS=<known consumers or UNKNOWN>
EVIDENCE=<durable pointer(s)>
PLANNING_STATUS=OPEN_INPUT|DUPLICATE|SUPERSEDED|ACCEPTED_FOR_FUTURE_PLANNING|REJECTED_BY_FUTURE_AUTHORITY
```

`PLANNING_STATUS` describes only the register item. It is not a Validation, Review, Candidate, Release, Deployment, Runtime, or work-item gate state.

## 4. Routing rules

- A technical need does not expand a current Task Pack write-set.
- A test/CI result does not authorize an incompatible migration.
- A compatibility alias remains a compatibility route, not a second normative owner.
- A register entry does not authorize path movement, schema replacement, semantic rewrite, or optional-capability promotion.
- If a future-major proposal is accepted, that future version must establish its own Product/L2/Task authority and migration/validation/review gates.

## 5. Discoverability

v4.7 adoption guidance points here from `docs/implementation/4.7.0/MIGRATION_ADOPTION.md`, project/checklist wiring, and the non-authoritative Golden coverage index. Those references make the register discoverable; they do not make it normative authority.
