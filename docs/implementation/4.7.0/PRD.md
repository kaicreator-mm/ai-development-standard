# ai-development-standard v4.7.0 PRD — AI-native Development Convergence

Status: **FROZEN PRODUCT AUTHORITY — 2026-09-30**

## 1. Product intent

v4.7.0 is the convergence release for the v4 series. It does not add another major functional domain and does not collapse the existing standards into one lifecycle object.

The Product goal is:

> A capable Agent with no historical chat can determine the applicable normative owners, current authority/state dimensions, machine contracts/profiles, allowed autonomy and required evidence from durable repository/GitHub facts, then execute or escalate correctly.

## 2. Evidence basis

Frozen Product evidence:

- `docs/implementation/4.7.0/L1_PRODUCT_EVIDENCE.md`;
- `docs/implementation/4.7.0/AUTHORITY_STATE_SCHEMA_INVENTORY.md` — refreshed through canonical v4.6 integration and #318 PASS;
- `docs/implementation/4.7.0/UPSTREAM_CONVERGENCE_CURRENTNESS.md` — exact v4.1–v4.6 authority/currentness map;
- v4.1–v4.5 Frozen Product/L2 authorities recorded there;
- v4.6 Frozen Product `e6aa04981110376e623d19b7dd4d0c6d0e139bdf` and Frozen L2 `f47ea81e8f8df32ac6c8b7cc922c405a17b704d9`;
- v4.6 canonical planning merge/current main at Freeze basis `6f2fb482812b17289b4f3d89ccf096ef6f618123`;
- v4.6 owner-currentness Review #280 PASS and planning Review #301 PASS;
- final Fresh Independent v4.7 Product/currentness Review #318 PASS with `PRODUCT_FREEZE_AUTHORIZATION=YES`, P0=0, P1=0.

Current implementation findings do not show a known semantic-owner contradiction. In particular, v4.1 #281 is a repaired Task Pack mutation-authority defect rather than Product/L2 semantic-owner drift, while the v4.5 #316 implementation P1 remains bounded to result/evidence association within the already-frozen three-family architecture.

## 3. Frozen Product shape

v4.7 freezes these four convergence products plus two acceptance mechanisms:

### Convergence products

1. **Canonical Authority / Applicability Registry**
2. **Qualified State-Dimension & Non-Inference Registry**
3. **Machine-contract Identity / Reference Convergence Rules**
4. **Progressive Disclosure + Compatibility-preserving Repository Information Architecture**

### Acceptance mechanisms

5. **Unified Cross-standard Conformance Suite**
6. **Self-dogfood + Future-major Migration Register**

v4.7 does not create a new global lifecycle owner.

## 4. Canonical Authority / Applicability Registry

Evolve the existing `standard-manifest.json` discovery model so a fresh Agent can resolve at least:

```text
semantic concern
canonical normative owner
applicability / lifecycle tags
machine-contract refs
compatibility aliases / prior paths
supersession / migration metadata
progressive-disclosure / read-routing tags
related non-authoritative references
```

Frozen invariant:

> One material semantic concern has one discoverable normative owner.

The registry points to owners; it MUST NOT duplicate their normative rules into a second fact source and MUST NOT grant mutation authority by itself.

## 5. Qualified state dimensions

v4.7 preserves separate claim dimensions, including equivalents of:

```text
work_item.state
dispatch.state
execution_pack.state
validation.state
review.judgment
candidate.state
release.state
deployment.state
runtime / incident state
maintenance / support state
provider / execution availability
```

Identical-looking strings such as `PASS`, `BLOCKED`, `READY` or `SUCCESS` do not imply identical semantics across owners.

v4.7 MUST NOT create one master state enum simply to deduplicate vocabulary.

## 6. Required forbidden inferences

The final conformance system must reject at least:

```text
Task DONE -> Validation PASS
Review PASS -> Validation PASS
Validation PASS -> Release READY
PR merged -> Release READY
Release READY -> Deployment SUCCESS
Deployment SUCCESS -> Runtime Healthy
Dispatch COMPLETED -> product/release PASS
PACK_CURRENT -> implementation correct
old exact-SHA PASS -> successor exact-SHA PASS
provider/tool/credential AVAILABLE -> mutation authority
waiver/exception -> PASS
fresh DB/install PASS -> upgrade PASS
wire/schema compatible -> behavior/source/consumer compatible
mock/sandbox PASS -> higher-fidelity PASS
artifact alias/tag -> immutable artifact identity
incident RECOVERED -> permanent fix/follow-up closed
branch/package exists -> maintenance-supported
Skill installed/capable -> trusted/authorized
Intent/Assumption record -> Frozen Product authority
historical chat/memory -> current durable authority
technical necessity -> Task Pack write authority
```

## 7. Machine-contract identity/reference convergence

Audit recurring concepts such as:

```text
repository / version / task / Issue / PR
subject identity / exact SHA / candidate
expected base / requested / tested / current head
authority references
operator / executor / session / context refs
artifact / environment refs
provider/model provenance
validation tuple/profile/toolchain
protocol/schema version / compatibility marker
```

v4.7 may standardize compatible reference conventions where they reduce ambiguity, for example Subject Identity or Authority Reference conventions.

It MUST NOT collapse distinct owner objects such as Dispatch, Validation Report, Review Aggregation, Assurance Plan, Operation, Release, Deployment, Runtime Observation, Incident Event or maintenance records.

Repeated identity data remains valid when it intentionally snapshots currentness/evidence for that object's claim.

## 8. Progressive disclosure

The minimum applicable read set should be deterministic enough that Agents do not need repository-wide guessing.

Frozen resolution direction:

```text
repository AGENTS + project .dev-standard/VERSION
        ↓
pinned ADS revision
        ↓
authority/applicability registry
        ↓
PROJECT_OVERRIDES / project adoption
        ↓
applicable lifecycle/domain owners
        ↓
applicable language/archetype profiles
        ↓
Task / Execution / exact-subject authority
```

Required semantics:

- current higher-authority durable facts beat stale/lower historical context;
- optional/non-applicable capability does not force unnecessary context;
- applicability uncertainty fails closed/routes to the owner;
- larger context volume is not automatically higher context quality;
- no required truth may exist only in ephemeral chat/session state.

## 9. Repository information architecture

Physical directory refactor is optional and evidence-driven.

Preferred sequence:

1. authority/applicability registry;
2. deterministic read routing;
3. owner/alias conformance;
4. measure remaining discoverability/path problems;
5. move paths only where evidence demonstrates value;
6. preserve compatibility entries/aliases through v4.

Directory aesthetics alone do not justify breaking stable pinned adopters.

## 10. Compatibility and migration posture

Compatible v4.7 convergence may include:

- additive manifest/registry metadata;
- stable compatibility aliases for moved/renamed paths;
- shared identity/reference conventions;
- terminology normalization with aliases;
- duplicate prose removal only after canonical ownership is unambiguous;
- stronger conformance for already-invalid inferences.

Not silently allowed in v4.7:

- incompatible authority hierarchy changes;
- state/object collapse;
- destructive wire/schema replacement without migration;
- historical evidence reinterpretation;
- stable path deletion without compatibility route;
- exact-SHA evidence meaning changes;
- turning optional capabilities into mandatory global gates.

Such findings become future-major/v5 migration inputs.

## 11. Task Pack / mutation authority convergence lesson

v4.1 #281 is explicit Product evidence for a convergence boundary:

- Task Pack remains durable mutation authority;
- registry/discovery information is not mutation authority;
- CI/Validation technical success does not retroactively authorize an out-of-write-set change;
- authority amendments must be explicit and current.

v4.7 may improve discoverability of write authority but MUST NOT weaken it.

## 12. Unified cross-standard conformance

Build executable semantic conformance covering:

1. owner uniqueness / no competing normative authority;
2. authority precedence;
3. state-dimension non-inference;
4. exact identity/currentness;
5. Task Pack/mutation authority boundaries;
6. compatibility alias/path resolution;
7. profile + PROJECT_OVERRIDES resolution;
8. machine-contract/prose consistency;
9. progressive-disclosure read routing;
10. historical payload/alias compatibility;
11. representative fresh-Agent lifecycle reconstruction.

JSON Schema meta-validation alone is insufficient.

## 13. Self-hosting / dogfood

Principal dogfood:

> A fresh high-capability Agent with no prior session can locate the correct owners, reconstruct current lifecycle/identity, determine allowed autonomy/evidence and hand off correctly using durable facts only.

Dogfood findings classify as Product gap, owner ambiguity, state ambiguity, schema/prose drift, read-routing gap, compatibility/migration gap, execution-authority gap, or future-major/non-goal.

## 14. Future-major register

Potentially incompatible needs remain explicit future-major inputs, including:

- core authority-chain redesign;
- incompatible Dispatch/Event redesign;
- state-semantic collapse/change;
- exact-SHA evidence meaning change;
- breaking role/profile/schema renames;
- stable-path removal without compatible aliasing;
- historical payload reinterpretation;
- mandatory adoption of currently optional capabilities.

## 15. Non-goals

v4.7 does not:

- replace all standards with one giant document;
- centralize lifecycle dimensions into one state machine;
- create another major functional domain;
- require physical directory reorganization for aesthetics;
- remove domain-specific standards/profiles;
- remove compatibility solely to simplify layout;
- require every project to adopt every optional capability;
- turn ADS into one CI/orchestrator/IDE/Agent runtime product.

## 16. Product acceptance

v4.7.0 Product is complete when:

1. material semantic concerns have one discoverable canonical owner;
2. state dimensions and forbidden cross-state inferences are explicit;
3. compatible subject/identity/authority-reference conventions reduce ambiguity without owner-object collapse;
4. progressive disclosure deterministically discovers applicable authority;
5. stable v4 adopters retain compatibility routes for changed names/paths/contracts;
6. profile/PROJECT_OVERRIDES resolution remains deterministic and subordinate;
7. conformance detects owner/state/schema/prose/mutation-authority drift;
8. a fresh Agent can reconstruct representative work from durable facts only;
9. incompatible convergence needs are separated into future-major planning.

## 17. Product Freeze record

Product Freeze is explicitly authorized and recorded after Fresh Independent final L1/currentness Review #318:

```text
review_subject_head = c7aaef0839be9a5765b19c57b51d2cd28d36c2bd
review_main = 6f2fb482812b17289b4f3d89ccf096ef6f618123
review_verdict = PASS
product_freeze_authorization = YES
P0 = 0
P1 = 0
P2 = 1 (currentness-hygiene only; closed before this Freeze record)
```

The Product Freeze does not authorize implementation, repository path moves, schema migration, alias removal, historical reinterpretation, global state collapse or provider/model mandates. Those actions require Frozen L2/Task authority and their own gates.

Full implementation completion of v4.1–v4.6 is not a prerequisite to this Product Freeze because their semantic owner authorities are stable. Any later implementation finding that demonstrates a real Product/L2 contradiction MUST trigger explicit currentness review; local implementation defects do not silently rewrite this Frozen Product.

`LOCAL_ENV=NOT_REQUIRED` for Product Freeze. Proceed next to L2 Architecture Evidence/Freeze.
