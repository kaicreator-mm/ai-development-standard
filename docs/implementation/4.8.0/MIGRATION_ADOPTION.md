# V4.8 Registry / Discoverability / Adoption — Migration & Adoption Note

Status: additive migration note for v4.8 T-006. This note moves nothing and retitles nothing; it records what becomes discoverable and what stays valid.

## 1. Additive-only posture

The v4.8 registry/adoption wiring is a pure addition on top of the current v4.8 standard revision:

- every pre-v4.8 manifest section, entry and historical relative order is preserved;
- `standard-manifest.json` gains the carried v4.7 discovery paths, the three v4.8 machine-family schemas, a `registries` section, the v4.8 adoption reference/verifier, and the `semantic_authorities` discovery registry;
- no historical entry is removed, renamed or rewritten; no destructive migration exists in this change;
- consumers that read only the legacy `sections` inventory keep working unchanged.

## 2. Historical evidence keeps its original identity

Historical evidence keeps its original subject and version identity. A v4.7 exact-SHA Validation PASS remains evidence for its own v4.7 subject; it is never relabeled, re-baselined or reused as a PASS for a v4.8 subject, and no v4.7 conformance/closure/dogfood/release artifact is reclassified as current v4.8 evidence. The v4.8 candidate re-exercises the relevant invariants with its own focused verifier instead.

The state registry's forbidden inferences stay in force, in particular `F07_OLD_SHA_VALIDATION_NOT_SUCCESSOR_PASS`: an old exact-SHA PASS must not be inferred to be a successor PASS.

## 3. What adopting projects can omit

Optional discovery context stays optional and materiality-driven:

- `registries/state-dimensions-v1.json` is read only when owner-qualified state/non-inference discovery is relevant to the concern;
- `scripts/resolve_standard_read_set.py` is a derived read-routing helper; projects that route manually never have to run it;
- the three v4.8 machine families are adopted only when their owning standard makes them material for the work;
- Agent Capability Profiles/Evidence and Task Learning records are optional; a project with none is not incomplete.

Fast Path remains lightweight: `TASK_LEARNING=NONE_MATERIAL` is a valid complete outcome, and adopting v4.8 does not require loading unrelated optional registries, profiles, packs or automation.

## 4. What does not change

- Canonical owner boundaries are unchanged: Task Learning, logical Agent capability claims and Agent Capability Evidence remain owned by `standards/EXECUTION_ARCHITECTURE_STANDARD.md`; runner/host capability by `standards/CI_RUNNER_CAPABILITY_STANDARD.md`; Interchange by the existing v4.0 owner with `schemas/interchange-envelope-v1.schema.json` reused exactly once — no Interchange v2 and no second interchange owner.
- No Interchange v2, no fourth durable machine family, and no durable Availability family is introduced; Availability stays derived.
- Provider/model identity and availability, and Agent capability profiles/evidence, remain non-authority: they never become correctness, authorization or routing-admission grants and never become current Validation/Review truth.
- Discovery metadata keeps `authority_effect=NONE`, `gate_effect=NONE`, `mutation_authorized=false`; registry or read-routing presence never grants mutation, gate, PASS, Closure or Release authority.
- Existing projects pinned to earlier revisions keep their pinned behavior; upgrading the pin to v4.8 only adds discovery surfaces and the three registerable machine families.

## 5. Upgrade path

1. Re-pin `.dev-standard/VERSION` to the current v4.8 revision (immutable pin procedure per `standards/PROJECT_ADOPTION.md` §2.1).
2. Nothing else is required for existing adoption levels; the discovery layer activates through `standard-manifest.json#semantic_authorities` without project-side changes.
3. Optionally declare the v4.8 convergence-discovery profile in `.dev-standard/PROJECT_OVERRIDES.md` ("v4.8 Convergence Discovery") and use `references/V48_REGISTRY_ADOPTION_REFERENCE.md` as the non-authoritative map of what is discoverable.
