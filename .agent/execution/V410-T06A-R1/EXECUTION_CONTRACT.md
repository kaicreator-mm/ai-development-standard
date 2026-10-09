# V410-T06A R1 execution contract — owner convergence / discovery / legacy classification

Integration base: `eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601` (tree `09db8216ec49caf84b45f404474cfbf4cb5e6ad2`), current `version/v4.10.0` tip = merge of PR #918 (T04B R4).
Task: #860. Execution environment: LOCAL. Dispatch: `V410-T06A-BUILDER-R1` on branch `task/v4.10.0-v410-t06a-owner-convergence`.
Frozen authorities: Product #837, L2 #842 §§3/5, refined DAG #848, Task Pack R1 §V410-T06A. Predecessors #851/#857/#858/#859 all durable DONE.

## L3 (materialized, bound to exact base)

- **Tests** — implement the positive/negative discovery/currentness/legacy cases below by reusing the carried v4.7/v4.8 registry+alias conformance semantics (`scripts/test_v47_authority_registry.py` resolver invariants) and adding only the smallest v4.10-focused stale-owner/coverage assertions in one new focused suite `scripts/test_v410_owner_convergence.py`. The focused test executes the real merged manifest/checkout, never a fixture copy. Carried suites must keep passing unmodified: `test_v47_authority_registry`, `test_v47_compatibility_aliases`, `test_v48_registry_adoption`, `test_v47_reference_conventions`, plus `verify_standard.py`.
- **Contract/invariant** — one semantic concern has exactly one current canonical owner or an explicit L2 composition rule; `standard-manifest.json#semantic_authorities` is discovery metadata only (registry, never authority); compatibility aliases are one-hop non-owners; projections/evidence never create authority; historical evidence is preserved byte-identical but cannot transfer currentness; a material v4.10 concern without uniquely reconstructible owner/composition fails closed.
- **Implementation seam** — after the R1 preplan/R2-R5 rebinds/R6 checklist/LOCAL snapshot/WEB oracle (all COMPLETE) and the #857 merge, the rebind on `eea3e69` confirms the manifest blob unchanged (`21730a02…`, 11 rows, schema_version=1) and recomputes the coverage gap: exactly seven material owner families remain without a discovery row. Minimal write set = (A) additive `semantic_authorities` rows only where still materially missing, (B) one non-authoritative evidence reference, (C) one focused regression test. No upstream semantic-owner file is edited.
- **Failure handling** — competing/missing owner, stale predecessor identity, ambiguous legacy/current classification, unexplained manifest delta, or integration-head drift => `STOP_FOR_DISPOSITION` / replan; never resolve by ordering, latest-PASS, alias promotion, deletion, or guessed fallback.
- **References** — `#860@6001754071` (owner map), `#860@6012404321` (R6 recheck set), `#860@6012773360` (LOCAL snapshot + stable-blob ledger), `#860@6013406812` (P1-P10/N1-N10 oracle + review checks); manifest `@21730a02…`; `standards/REFERENCE_CONVENTION_STANDARD.md@ba6a95b1…`; legacy assets per MANIFEST.yaml `legacy_classification`.

## Allowed write set (exactly three surfaces)

1. `standard-manifest.json` — additive `semantic_authorities` entries only; preserve top-level/envelope `schema_version=1`, all sections, the 11 existing entry_ids/owners/aliases/postures, and `normative_standards ∩ compatibility_entries = ∅`.
2. `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md` — new, explicitly non-authoritative (carries `authority_effect=NONE` / `gate_effect=NONE` / `mutation_authorized=false`-equivalent declarations); L2 §5.1-shaped matrix with columns CONCERN / CANONICAL_OWNER / PROJECTION_SURFACES / MACHINE_CONTRACTS / COMPATIBILITY_ALIASES / LEGACY_SURFACES / STATUS / ACTION / EVIDENCE_REFS; every row carries exact-SHA evidence refs; legacy classification dispositions included; no resolver/runtime contract/lifecycle/service.
3. `scripts/test_v410_owner_convergence.py` — new focused discovery regression (or a strictly smaller existing directly-owned seam, justified in the PR).

## Forbidden

- Any hunk in `schemas/*`, `templates/*`, `prompts/*`, `checklists/*`, golden fixtures, verifier/CI wiring, `v40_*` semantics, registries, or any upstream semantic-owner standard (DEVELOPMENT_WORKFLOW, EXECUTION_ARCHITECTURE, GITHUB_AGENT_INTERACTION_PROTOCOL, VALIDATION_STANDARD, TASK_DECOMPOSITION_STANDARD, TASK_DAG_GOVERNANCE_STANDARD, EXECUTION_PACK_STANDARD, IMPLEMENTATION_QUALITY_STANDARD, INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD, PROJECT_ADOPTION, REFERENCE_CONVENTION_STANDARD, RELEASE_STANDARD, ARCHITECTURE_*).
- No second owner registry, no new event family/state dimension/lifecycle, no T06B machine-wiring (stale-projection defects are recorded in the matrix with `ACTION=REWIRE_PROJECTION` and routed to #861, never fixed here).
- No verdict/gate/mutation semantics anywhere in the diff; no historical blob rewrite/deletion/reinterpretation.
- No merge by the Builder; no merge before fresh exact-candidate Concern Validation PASS + genuinely Fresh Independent Review PASS on one unchanged HEAD/tree (review:required, risk:high).

## Gate obligations

On the exact candidate: LOCAL Concern Validation PASS, then WEB Fresh Independent Review PASS (independence by context separation), both bound to the candidate HEAD/tree; Review PASS is not Release PASS.
