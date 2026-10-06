# V410-T06A R2 execution contract — owner convergence / discovery / legacy classification (rebind)

Integration base: `eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601` (tree `09db8216ec49caf84b45f404474cfbf4cb5e6ad2`), current `version/v4.10.0` tip = merge of PR #918 (T04B R4).
Task: #860. Execution environment: LOCAL. Dispatch: `V410-T06A-BUILDER-R2` on branch `task/v4.10.0-v410-t06a-owner-convergence`.
Frozen authorities: Product #837, L2 #842 §§3/5, refined DAG #848, Task Pack R1 §V410-T06A. Predecessors #851/#857/#858/#859 all durable DONE. Supersedes `V410-T06A-R1` for execution (R1 stays published history, metadata-corrected in place).

## Why R2 (bounded rebind, one material change)

R1's prescribed write set (additive `semantic_authorities` rows + registration of the new reference/test) is machine-incompatible with the carried v4.8 frozen-inventory conformance guards, which the same pack requires to PASS unmodified:

```text
semantic_authorities row        -> test_v48_registry_adoption.semantic_registry_problems
                                   -> "semantic registry entry count deviates from carried + exactly three new"
(sections.references/verification) += new files
                                -> test_v48_registry_adoption.section_conformance_problems
                                   -> "unauthorized additions to references: ..." / "... verification: ..."
```

Full reproduction and outputs: BLOCKED terminal `#860@6013810495`. Adopted resolution (that terminal's Option A, recommended): **zero manifest delta**. The v4.10 authorization for registry growth exists (Frozen L2 #842 §3: "v4.10 extends that registry only when a material current owner is missing"), but the mechanical mechanism — evolving the frozen-inventory guard — is conformance-wiring territory (T06B/#861), not a builder self-amendment. The manifest-side discovery gap is therefore recorded in the convergence reference as an explicit `STATUS=GAP` / `ACTION=STOP_FOR_DISPOSITION` row with `ROUTED_TO=T06B(#861)`, plus `T06B_FEEDBACK` in the terminal.

## L3 (materialized, bound to exact base)

- **Tests** — one new focused suite `scripts/test_v410_owner_convergence.py` executing the real merged manifest/checkout (never a fixture copy): imports `resolve_registry` / `RegistryError` from `test_v47_authority_registry.py` and the carried guards `semantic_registry_problems` / `section_conformance_problems` from `test_v48_registry_adoption.py` (reuse, not reimplementation). Positive: unique-owner, order-permutation invariance, coverage-gap truthfulness (zero rows added AND all seven families documented in the reference), manifest invariants incl. **blob-identity `standard-manifest.json == 21730a02…`** (the zero-delta proof), alias one-hop non-owner, legacy dispositions present, fresh-observer reconstructibility shape, non-authority declarations. Negative: competing owner both orders, broken targets, alias deletion/promotion, stale/historical-owner rejection, gap discipline `STOP_FOR_DISPOSITION`, guard-intactness (no unauthorized additions are representable). Carried suites and `verify_standard` must keep passing unmodified.
- **Contract/invariant** — one semantic concern has exactly one current canonical owner or an explicit L2 composition rule; `standard-manifest.json#semantic_authorities` is discovery metadata only (registry, never authority); compatibility aliases are one-hop non-owners; projections/evidence never create authority; historical evidence is preserved byte-identical but cannot transfer currentness; a material concern without uniquely reconstructible owner/composition fails closed and is recorded as `GAP` + `STOP_FOR_DISPOSITION`, never guessed; and a machine-blocked registration is recorded as a routed gap, never resolved by amending the guarding contract.
- **Implementation seam** — exactly two new source surfaces, no others: (B) `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md` — non-authoritative L2 §5.1-shaped convergence matrix for the v4.10 material concerns, explicit registry-growth `GAP` row (routed to #861), legacy classification table (7 `CURRENT_CARRIED_FORWARD` + 2 `COMPATIBILITY_ONLY`), `authority_effect=NONE` / `gate_effect=NONE` / `mutation_authorized=false` declarations, exact-SHA evidence refs; (C) `scripts/test_v410_owner_convergence.py`. `standard-manifest.json` is **not** modified (registered-path registrations remain blocked; `verify_standard.py` only verifies declared paths exist, so unregistered new files keep it green — verified by reading `scripts/verify_standard.py`).
- **Failure handling** — competing/missing owner, stale predecessor identity, ambiguous legacy/current classification, unexplained manifest delta, integration-head drift, or any attempt to achieve conformance by amending the guarding contract/deleting inventory/weakening negatives => `STOP_FOR_DISPOSITION` / replan; never ordering, latest-PASS, alias promotion, deletion or guessed fallback.
- **References** — `#860@6001754071` (owner map), `#860@6012404321` (R6 recheck set), `#860@6012773360` (LOCAL snapshot + stable-blob ledger), `#860@6013406812` (P1-P10/N1-N10 oracle), `#860@6013810495` (write-set contradiction + Option A), manifest `@21730a02…`; `standards/REFERENCE_CONVENTION_STANDARD.md@ba6a95b1…`; legacy assets per MANIFEST.yaml `legacy_classification`.

## Allowed write set (exactly three surfaces on this candidate)

1. `.agent/execution/V410-T06A-R2/*` (this pack; plus the R1 metadata correction already committed) — pack artifacts only.
2. `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md` — new, explicitly non-authoritative.
3. `scripts/test_v410_owner_convergence.py` — new focused discovery regression.

**`standard-manifest.json` delta MUST be NONE.** Any manifest hunk fails this contract and the carried guards.

## Forbidden

- Any hunk in `standard-manifest.json`, `schemas/*`, `templates/*`, `prompts/*`, `checklists/*`, golden fixtures, verifier/CI wiring, `v40_*` semantics, registries, or any upstream semantic-owner standard (DEVELOPMENT_WORKFLOW, EXECUTION_ARCHITECTURE, GITHUB_AGENT_INTERACTION_PROTOCOL, VALIDATION_STANDARD, TASK_DECOMPOSITION_STANDARD, TASK_DAG_GOVERNANCE_STANDARD, EXECUTION_PACK_STANDARD, IMPLEMENTATION_QUALITY_STANDARD, INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD, PROJECT_ADOPTION, REFERENCE_CONVENTION_STANDARD, RELEASE_STANDARD, ARCHITECTURE_*).
- No amendment of `scripts/test_v48_registry_adoption.py` or any carried conformance guard (the registry-growth question is routed to #861, not self-resolved).
- No second owner registry, resolver, runtime contract, lifecycle or precedence layer; no T06B machine wiring (stale-projection defects are recorded with `ACTION=REWIRE_PROJECTION` and routed to #861).
- No verdict/gate/mutation semantics anywhere in the source diff; no historical blob rewrite/deletion/reinterpretation.
- No merge by the Builder; no merge before fresh exact-candidate Concern Validation PASS + genuinely Fresh Independent Review PASS on one unchanged HEAD/tree (review:required, risk:high).

## Gate obligations

On the exact candidate: LOCAL Concern Validation PASS, then WEB Fresh Independent Review PASS (independence by context separation), both bound to the candidate HEAD/tree; Review PASS is not Release PASS. Terminal on #860:

```text
V410_T06A_BUILDER_R2=DONE|BLOCKED; CANDIDATE_HEAD=<sha>; CANDIDATE_TREE=<tree>; GATES=<pending>; NEXT=VALIDATOR_R1|REPAIR
```
