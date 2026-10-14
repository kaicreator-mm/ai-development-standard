# ADS v4.11 — N08 C2 × actual owning admission: bounded pre-Freeze research R1

> **Status: source-only, non-authoritative architecture evidence.** This is a falsifiable C2/owner-interface preflight, not a revised PRD/L2, Task Pack Freeze, Release §11 decision, executable owner integration, runtime PASS or retrospective waiver. Prepared under existing #954/#1107 P5; no native version node is newly completed.

```ini
EVIDENCE_ROLE=ARCHITECTURE_RESEARCH_SOURCE_ONLY
ISSUE=#954
PRODUCT_EXACT_FREEZE=#943@6170435421
PRODUCT_SOURCE=PR_1105@7c4f78b7c6eb9e3f9f5c88961316e1c3267de16f
PRODUCT_TREE=8212b4a337b1f662baefc0f49e1ae22c407ac5af
PRODUCT_PRD_BLOB=edc9ef4d44edec035bac282dcc69467adf338729
PRODUCT_MATRIX_BLOB=2c9320321a70cc2fb51979e88b55af044ebacfde
L2_SOURCE=PR_1106@227f599c0a2b2440b1f422959c943c27403f4426
L2_BLOB=e07fdce9d540872a53b35ba47b04fc64f94db662
BASE_ORIGINAL_CANDIDATE=322e86845f78de8ea8cadb05ec624bfbb3a5de20
N08_C1_REPO_ONLY=SUPPORTED_WITH_SCOPE_LIMIT
N08_C1_FULL_OWNER=UNKNOWN
N08_C2_NO_NOVEL_MATERIAL_PREDICATE=UNVERIFIED
N08_EXCLUSION_EFFECTIVE=NO
OWNER_ADMISSION_REAL_TRANSITION=NOT_IDENTIFIED
EXECUTABLE_REAL_NEGATIVES=NOT_RUN
PRODUCT_S08_REAL_HUMAN_DENY_E2E=NOT_PROVEN
REVIEW_POLICY=required (architecture/authority/security-sensitive)
```

## 1. Falsifiable hypothesis and exact boundaries

**H-C2:** For any one *actual, current* work subject with applicable J09 release, J10 incident/recovery, J11 retirement/consumer and J12 upstream source/license conditions, the conjunction of **existing real owning predicates** (including currentness and side-effect permission) rejects every new joint hazard with an observable `HOLD/BLOCKED` before a release advance/protected effect. If a new interleaving can bypass those owners, then the "no novel material predicate" prerequisite for optional **physical-positive** exclusion is FALSE; if the real owning transition cannot be exercised or compared on the same subject, the prerequisite remains UNKNOWN, **not** proven true by isolated conformance fixtures.

**Real under test (future):** the existing Project Adoption/Workflow affected-source/effective-rule authority + genuine Release §11 gate-by-exact-subject admission and real current side-effect permission; no separately invented scheduler, release engine, database or authority. **Permissible deterministic inputs:** bounded exact-source/actor/tenant/work-item examples and a temporary protected-effect target only where its fidelity is explicitly limited. **Not tested yet:** real owner acceptance, actual GitHub-hosted release transition, protected external provider, real human DENY, multi-host ACK recovery. No PASS asserted.

**Safety-conservative conclusion now:** The source contract is clear about what must happen, but present tests do not exercise that live owner join. C2 is **UNVERIFIED**, and N08 physical four-way E3 positive exclusion remains **ineffective**. This is not evidence that an actual vulnerability exists, nor license to skip a mandatory gate.

## 2. C1 bounded actual-workload inventory (negative evidence, limited scope)

The GitHub Git Trees API at the Product exact HEAD was read recursively: `truncated=false`, 1,237 entries. Top-level namespaces are standard/docs/fixtures/scripts/tests/registries/templates and metadata, with **no** repository `apps/`, `services/`, `src/`, `packages/`, `deploy/`, `infra/`, `workloads/` application-service runtime tree. The single tracked workflow `.github/workflows/verify-standard.yml@9fa6099f867b4ce68c0963fbd012f8970753c4d6` runs Python standard/check scripts, not a production J09+J10+J11+J12 multi-service deployment. Product §2.1/§2.3 describes ADS as the *method/standards* release with bounded cross-concern X cases, not a physically deployed release/incident/retirement/license production workload.

**Truth:** `NO_ADS_OWNED_FOURWAY_WORKLOAD_IN_INSPECTED_REPO_TREE` is supported. **Not supported:** exhaustive external tenant/provider/Build Host workload inventory, owned off-repository workflows, or independently attributable owning C1 acceptance. Such missing facts cannot be upgraded from `UNKNOWN` to `NOT_APPLICABLE`. The C1 AND C2 exemption cannot operate with C2 unknown even if C1 later becomes owner-accepted.

## 3. Existing owner surface readback and executable gap

| Existing owner or implementation | Exact existing owner blob at L2 subject | What it currently supplies | What it **does not** establish |
| --- | --- | --- | --- |
| `standards/PROJECT_ADOPTION.md` | `a8c2d7a01a3610d9444d17df614ec6cacf58b67e` | § effective-rule non-weakening/AND, pin and scoped applicability | An exposed/current production admit-or-deny function with real proof source |
| `standards/DEVELOPMENT_WORKFLOW.md` | `28c537e12c03f3f0cef501b8b5505e8ee28ca532` | affected-file materiality inspection, observed actual facts and same-subject effective-rule trace | That T01 test fixture acts as the GitHub/Release state transition owner |
| `standards/RELEASE_STANDARD.md` | `c4d72506253ca7f3d95e305dbd84aae0e1fbe2cb` | §11.2 gate×subject decision identity, §11.4 currentness, §11.5 prospective migration only | A signed gate-row/new-version acceptance, or an executable side-effect guard |
| `standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` | `3f7189301f7292200a98ebd027372513a801bc03` | §21 pre-effect re-check of current authority; ACK loss ⇒ HOLD | That a current human/source/effect has actually been authenticated on new subject |
| `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` | `15e355f6ec86370599f2dda7b61963d93fead66f` | current affected consumer/deprecation identity | Joint Release+Recovery+Upstream revocation tested |
| `standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md` | `e0a26a45e7e45a211ad4bdfef9b8d122779669bd` | actual source/license/provenance/currentness and no optimistic N/A | Cross-owner effect veto on dynamically changed upstream |
| T01 `scripts/test_v411_t01_effective_rules.py` | `c4f2c42f19efb751e5ef9aa80187d9d581da198a` | **Pure in-test** rule-resolution model with explicit fixture-only inventory; fail-closed oracle | Real material observation provider or Release current-state mutation |
| T06 `scripts/test_v411_t06_claim_admission.py` | `109a169e3523ddc29027e5913d60a500f5ee2e02` | isolated serialized **test adapter** and deterministic claim counterexamples | Native concurrent GitHub claim, authoritative Release decision |
| T08 `scripts/test_v411_t08_human_denial_authority.py` | `63089e8da9d4077ef206c1b9977afc90382f91a3` | source/role/deny fixture decisions; explicitly denies genuine source proof | Live authenticated human DENY E2E |
| T12 `scripts/test_v411_t12_abc_conformance.py` | `e66eaee20b452f570665bff3e83be493a9eaef6b` | metadata `run_compound.complete(facts)`, selected owner test composition | Observed full four-way actual-owner Release refusal |
| v4.9 `scripts/test_v49_release_applicability.py` | `7497f7b07f2086df48112783301cb43d4dbcc006` | checks that Release owner contract **text** includes §11 applicability semantics | Live Release admission API or owner signature |

All SHA values above are GitHub content blobs read on the same reviewed L2 source revision, not assumed from a moving branch. An executable test that calls only these local model functions could demonstrate a **model property**, never by itself claim that the actual Release Owner has refused a real work item.

## 4. C2 joint-predicate falsifiers (test cases, not PASS)

Every test uses **one exact** `repository + candidate SHA/tree + work item + actor/role + tenant + operation + effect_id` and a current owning proof set; compare *accepted authoritative transition* and *protected effect count* across cases. Risk is conjunctive, not a 4-way metadata set count.

| Falsifier | Actual material condition | Required owning outcome (before effect) |
| --- | --- | --- |
| C2-N01 | J09 release otherwise READY; J10 lost ACK/external mutation outcome unknown | `HOLD` until real reconciliation, no duplicate side effect |
| C2-N02 | During N01, J11 retires the consumer and J12 upstream license/source proof becomes revoked/stale | `HOLD/BLOCKED`; re-evaluate all newly material currentness, permissions and consumer constraints, not "last PASS wins" |
| C2-N03 | Declared J09+J10+J11 but **inspected actual** upstream/source/license drift makes J12 material | Actual four-job AND and unresolved joint-predicate `HOLD`; label omission cannot bypass |
| C2-N04 | Truly only three jobs and J12 current scoped-inspection evidence is ABSENT | Do not invent J12; still require the three-owner conjunction and any material joint-risk gate |
| C2-N05 | Each of J09–J12 proof separately omitted, or stale SHA/tenant/actor/work item or forged `human:` label provided | Fail closed; no release qualification advance or protected effect |
| C2-N06 | A historical old-sha APPROVE or test-only synthetic DENY is passed as live human authority for new SHA | Refuse authority promotion; `REAL_HUMAN_DENY_E2E_NOT_PROVEN` remains |
| C2-N07 | A release applicability row is generated without §11.2 owner authority_ref, exact subject or current basis | Row = `UNKNOWN`; stronger existing gate or BLOCKED, never automatic N/A |
| C2-N08 | Incident/retirement/upstream proof changes after a prior positive admission but before effect boundary | Re-read authoritative current owner facts at last effect boundary; stale permission cannot be relied on |

**Potentially novel material predicate:** *joint temporal invalidation* — a J12 upstream revocation may make a previously reconciled J10 ACK operation or J11 retired consumer ineligible while J09 candidate advances. Separate X02/X03/X04/X06/X07 tests do not prove that the same exact work subject re-checks **all** changes at the final Release/effect boundary. This may be **materially novel** until same-subject executable evidence explicitly refutes it. Therefore no affirmative `C2_NO_NOVEL_PREDICATE=YES` recommendation is defensible yet.

## 5. Minimal owner-seam contract required before test authoring

**Do not create a second policy owner.** The bounded adapter, only if no existing real transition can be found, is a *read-only current-fact join + pre-existing owning-action request*:

1. **Inputs (read from authoritative owners, not caller-supplied trust labels):** exact immutable repository/candidate/tree/work/tenant/effect; declared job set; independently inspected *actual* material facts including license, incident ACK state, retirement/consumer status; current source+blob/provenance/role and human decision refs; applicable gate list and prior Release §11.2 rows.
2. **Owning evaluation (no fresh custom Gate):** Project Adoption/Workflow computes observed-material union and constraint AND using actual source facts; relevant compatibility/license/security/effect/human owners attest their own current predicates. An UNKNOWN, disagreement, stale ref, changed subject, revoked license, lost ACK or unauthorized supersession must produce a **deny/hold** request, never be normalized into an allowed Release decision.
3. **Output / effect:** existing owning Release admission transition consumes the conjunction for one exact subject, **before** any release state advance or protected external effect. Observe its actual denial/accepted record and effect count. The adapter may publish evidence references, but neither invent a new Release owner signature nor upgrade old test fixture authority. If the owner transition is absent, integration remains `UNVERIFIED_OWNER_SEAM`, negative suite remains `NOT_RUN`.
4. **Cost bound:** One owner-local real admission interface and a focused matrix covering C2-N01–N08, four omissions and undeclared J12 are sufficient if source/owner semantic equivalence is established. No synthetic full microservice stack, no blanket 139-script rerun, no repeated preexisting #1105–#1108 source review.

A proposed interface cannot be promoted from this research directly to production: first choose existing owning path/current subject and complete a **new separate admitted owner Task Pack/PR** under #1107 P5; review semantic equivalence and authorized write set; then execute exact-head focused positive/negative on the actual transition. No embedded adapter or new test may self-certify Release authority.

## 6. Decision / owner handoff and closure eligibility

| Proposition | R1 disposition | Next proof/owner |
| --- | --- | --- |
| C1 no actual repository-owned four-job running service | Source-bounded supported | External/owner-scope inventory still UNKNOWN; Architecture + Release must accept full C1 |
| C2 no new four-way material safety predicate | **UNVERIFIED / potentially falsified** by temporal revocation interleaving | Owning L2+Release must refute C2-N02/N08 with same-subject actual owner evidence |
| Real four-way physical-positive exclusion | **NOT EFFECTIVE** (C1∧C2 absent) | Do not waive N08; stronger original gate/BLOCKED |
| Actual owner union-negative admission | **NOT RUN; interface not verified** | Existing owner authority or bounded accepted real adapter, focused execution |
| S08 P2 synthetic same-file-backed SQLite | Source-reviewed #1108 only, Host `NOT_RUN` | Legally admitted successor + targeted real Host |
| True human DENY E2E | **NOT PROVEN**, intentionally excluded from reduced *standards-only* demonstration | Separate genuine current owner proof if real consumer requires it |
| L2 exact successor Freeze | **HOLD**, reviewed source does not resolve material UNKNOWN | #954 owning Architecture disposition |
| Release §11.2/§11.5 gate×new subject | **UNKNOWN / NOT ISSUED** | Actual owning Release decision, not this research |
| Old V01 #1021 and V02–R02 | Old V01 BLOCKED; others not admitted | Only a lawful new subject + full required evidence can advance |

### Evidence acceptance and review

Review this **one-file source-only delta** against its actual PR HEAD and pinned owners above. Independent Architecture/Release/security reviewer must (a) challenge missing off-repo C1, (b) independently attempt to refute or strengthen C2 temporal counterexample, (c) reject hidden release-authority minting, and (d) distinguish a design-time interface proposal from a truly executing owner transition. Permitted review outcome: `PASS_SOURCE_RESEARCH_FOR_OWNER_DISPOSITION | NEEDS_REVISION`. Neither outcome is L2 Freeze, C2 PASS, Release migration, Host execution nor V01 PASS.

**Explicit NOT proven:** no external ADS ownership census, no genuine Release gate decision for prospective exact candidate, no current human DENY, no live owner admission API, no side-effect/ACK interleaving execution, no no-novelty proof, no physical four-job system. Historical original `322e868...` remains immutable.
