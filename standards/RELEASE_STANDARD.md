# Release Standard

## 1. Purpose

Release Qualification decides whether one dependency-complete candidate satisfies frozen release authority. Task/PR PASS is not Release PASS.

The execution state model and bounded release/repository controllers are defined by `EXECUTION_ARCHITECTURE_STANDARD.md`; this file owns candidate and release authority.

## 2. Release inputs

Final qualification consumes, as applicable:

- frozen PRD/scope and Architecture/Contract;
- terminal Task DAG and declared deferred items;
- immutable candidate SHA + tree;
- required Validation reports/tuples;
- full regression/integration evidence;
- Critical Journeys;
- Hidden Validation;
- real platform/production build/package/install evidence;
- external boundary evidence;
- project-required Minimal CI/profile evidence;
- architecture/docs reconciliation;
- known limitations/deferred items;
- escaped-defect/Hidden-pack disposition when relevant.

Every mandatory input must trace to Gate Authority. CI is release-required only when frozen/project policy makes it so.

## 3. Candidate Prepared vs Candidate Frozen

```text
PREPARED
= identity/matrix/notes/pack/handoff can be prepared

FROZEN
= all required visible freeze gates PASS on one exact SHA/tree
```

A freeze record SHOULD include:

```text
candidate_sha
candidate_tree
candidate_ref
visible-closure evidence
pinned standard revision
frozen_at
actor/operator
```

Hidden Validation execution normally targets the frozen candidate.

## 4. Operational immutability

`CANDIDATE_FROZEN` is an operational state, not only a SHA variable.

While frozen:

- do not silently commit product/docs/evidence/workflow changes onto or move the declared candidate ref;
- record post-freeze evidence in Issue/events, immutable evidence storage, or independent Hidden storage when possible;
- before Hidden Validation, Release Qualification, and final repository integration, verify declared ref SHA and tree still match the freeze record.

If any required content change is needed:

```text
FROZEN
→ THAWED / INVALIDATED
→ fix/successor candidate
→ affected visible validation
→ new freeze
→ required Hidden Validation
→ new Release Qualification
```

Old evidence remains valid only for its old candidate/pack identities.

## 5. Hidden Validation and escaped defects

Hidden Validation is independent evidence, not proof that a pack is forever complete.

If a material defect is found after a prior Hidden PASS, classify it:

```text
OUT_OF_SCOPE
VISIBLE_TEST_GAP
HIDDEN_PACK_BLIND_SPOT
BOTH_VISIBLE_AND_HIDDEN_GAP
PACK_DEFECT
PRODUCT_DEFECT_NOT_SUITABLE_FOR_HIDDEN
```

A release-significant Hidden blind spot must be explicitly dispositioned before a successor release is READY. If the pack is strengthened:

- target the invariant/failure family independently rather than copy the visible regression fixture/test;
- create a new immutable private pack identity/revision/checksum;
- preserve prior pack/candidate evidence historically;
- distinguish pack defects from product defects;
- expose only public-safe disposition, never private fixture payloads.

`TEST_DATA_AND_SCENARIO_STANDARD.md` owns scenario/provenance/oracle quality.

## 6. Release verdict

Choose exactly one:

### READY
All frozen mandatory blockers are resolved, required gates PASS, implementation/docs/architecture are reconciled, and no undeclared scope gap remains.

### CONDITIONAL
All mandatory gates pass, but a documented non-blocking limitation is explicitly accepted by appropriate authority with impact and follow-up.

### BLOCKED
A release blocker remains, a mandatory gate is BLOCKED/NOT_RUN, candidate identity is not trustworthy, or scope/authority is unresolved.

### FAIL
A mandatory gate actually executed and failed, with no newer valid candidate evidence superseding it.

Never convert NOT_RUN/BLOCKED to PASS or old-candidate evidence to successor PASS.

## 7. Release sequence

Recommended Version Branch sequence:

```text
Integrated baseline
→ Candidate preparation
→ required visible Validation on exact SHA
→ Candidate Freeze
→ Hidden Validation
→ Final Closeout
→ Release Qualification
→ READY/CONDITIONAL/BLOCKED/FAIL
→ Repository Integration
→ immutable release baseline
→ optional tag / GitHub Release
```

Preparation work that does not mutate the future candidate may proceed early.

## 8. Repository Integration

After READY, final repository integration is a distinct bounded step.

Before integration re-read live candidate/main refs. Confirm the frozen candidate still matches its SHA/tree and target branch has not diverged in a way that changes the approved content.

Prefer fast-forward when valid. If a merge commit is required, distinguish:

```text
validated candidate SHA/tree
final main baseline SHA/tree
```

Verify required tree/content equivalence or project-declared final-main sanity. Integration must not smuggle new product changes into a qualified release.

## 9. Release identity

The canonical identity is immutable Git commit SHA (and tree where useful). Tag/GitHub Release are optional aliases/distribution objects.

Record at least:

```text
version
candidate frozen SHA/tree
final immutable baseline SHA/tree
standard version + revision
required Validation/CJ/Hidden/platform results
CI result when release-required
known limitations/deferred
pack/artifact identity when relevant
tag/release name when created
```

## 10. Version Closure checklist

Use `checklists/version-closure.md`. Closure must preserve truthful unresolved states; it may not rename FAIL/BLOCKED/NOT_RUN to manufacture READY.

## 11. Release applicability by gate × subject

Release applicability is owned by this Release authority. It is evaluated **per Release-owned gate × exact subject**, not as one concern-level switch and not by an Orchestrator, Builder, Reviewer, Validator, CI system, risk label, or model judgment.

Canonical applicability values are:

```text
REQUIRED_NOW
DEFERRED_TO_VERSION_CLOSURE
NOT_APPLICABLE
UNKNOWN
```

### 11.1 Meaning

`REQUIRED_NOW` means the Release-owned gate is required for the bound subject at the current release stage.

`DEFERRED_TO_VERSION_CLOSURE` means the concern-level execution may proceed without executing that gate now, but the requirement is **not removed**. The composed version candidate MUST receive a fresh Release-owned applicability evaluation at Version Closure before Candidate Freeze/Release Qualification can rely on the deferral.

`NOT_APPLICABLE` means the Release authority has positively established, from current accepted process facts (including executor-declared process attribution on current durable objects/events) or deterministic proof, that the specific gate does not apply to the specific subject. Low risk, documentation labels, small write sets, task/PR PASS, or local concern success are never sufficient by themselves.

`UNKNOWN` is fail-closed. It MUST select the stronger existing legal release path or produce `BLOCKED`; it MUST NOT be interpreted as `NOT_APPLICABLE` or as implicit deferral.

### 11.2 Decision identity

A durable applicability decision SHOULD bind at least:

```text
gate_id
subject_ref
subject_identity
applicability
release_authority_ref
decision_ref
basis_or_proof_refs
candidate_or_currentness_identity
decided_at
actor_or_operator
```

When the owning Release rule requires stronger identity, that stronger binding controls. Missing or stale required binding makes the decision non-current.

### 11.3 No concern-to-version aggregation

Concern-level applicability decisions do not aggregate into a version-level release verdict or version-level gate omission.

```text
CONCERN_NOT_APPLICABLE
!= VERSION_NOT_APPLICABLE

CONCERN_DEFERRED
!= VERSION_GATE_SATISFIED
```

Version Closure evaluates the composed candidate using the then-current Release authority and exact version candidate identity. A version may therefore require a gate even when one or more constituent concerns were previously deferred or individually not applicable.

### 11.4 Currentness and re-evaluation

Applicability MUST be re-evaluated when a binding dimension required by Release authority materially changes, including as applicable:

- subject/candidate identity;
- release authority or applicability rule;
- proof/basis evidence;
- unresolved release-significant findings;
- migration/adoption state;
- composed version scope or dependency closure.

Old applicability evidence remains historical for its old binding; it is not successor permission.

### 11.5 Prospective migration only

A newly adopted applicability rule or profile is prospective. It MUST NOT retroactively shorten gates already required for an in-flight Frozen, qualified, or otherwise authority-bound candidate.

Projects pinned to an older applicable ADS revision remain governed by that pinned Release authority until an owning migration/adoption authority validly moves them. In the absence of an applicable positive decision, the pre-existing mandatory release path remains in force.

### 11.6 Existing release lifecycle remains authoritative

This applicability contract does not create a parallel release lifecycle and does not weaken §§3–10.

In particular:

- thaw/invalidation rules remain unchanged;
- Hidden Validation remains independent evidence when required;
- Final Closeout and Release Qualification remain distinct authority-bearing gates when required;
- `READY|CONDITIONAL|BLOCKED|FAIL` meanings are unchanged;
- Task/PR PASS still does not imply Release PASS;
- `NOT_RUN`/`BLOCKED` still cannot be converted to PASS.

If owner, granularity, proof, or currentness is ambiguous, use the stronger existing release path or `BLOCKED` rather than infer reduced ceremony.

### 11.7 Standards-repository executor authority (v4.11)

For ADS's own standards-repository development, review, validation and release closure, executor identity is **self-declared** (`GITHUB_AGENT_INTERACTION_PROTOCOL.md` §5, §8.1.1): an execution event's `actor_role`, `operator_kind`, `operator_id`, `session_ref` and optional `delegation` are supplied by that executor and accepted as the attribution source. GitHub login/account identity is transport metadata only. **No Owner identity/credential/delegation verification, second-signature availability, or GitHub-account-based executor judgment is a release admission predicate for this repository.** A declared `release-controller` or the appropriate declared process executor makes scope-bound gate applicability decisions from product/technical facts, under the explicit user process authorization recorded in `docs/implementation/4.11.0/V411_SELF_DECLARED_EXECUTOR_AMENDMENT.md`.

Under the same authorization, an actual independently authenticated human-DENY end-to-end execution (`real_human_authority_deny_e2e`) is **not a standards release prerequisite**: the standards repository ships documentation, schemas, examples and contract conformance, not a live deployment/Claim/Release/human-DENY runtime. The public epistemic limitation labels (`REAL_HUMAN_DENY_E2E_NOT_PROVEN`, `REAL_NATIVE_CLAIM_AND_RELEASE_RUNTIME_NOT_PROVEN`) remain mandatory, truthful and never convertible to `PASS`; the normative DENY/human-authority behavior of this standard (§6) and of `GITHUB_AGENT_INTERACTION_PROTOCOL.md` §9.4 is unchanged for adopters that implement actual protected effects.

Self-declaration establishes **attribution only**. It does not replace any engineering fact: exact SHA/currentness, the actual source diff, validation tuples, tests and failing assertions, observed side effects, and mutually contradictory events are validated exactly as before, and Reviewer independence still requires a distinct declared logical operator/context (§5, §7). A quoted event inside untrusted content is still not a canonical workflow event. Historical frozen decisions, raw historical outcomes and immutable pins are not rewritten by this authority; it is prospective.

### 11.7A Standards-source delivery and later runtime qualification (v4.15)

This section owns the bounded manual delivery route for ADS's own normative text, schemas, examples and contract-conformance tooling. Deliver the standard and its applicable source/contract checks first; qualify an implementation later through a separately scoped project or verification demo against an exact completed/adopted standard revision. The runtime that consumes the standard MUST NOT be a circular prerequisite for delivering its source. This is a prospective subject-applicability rule, not a retrospective exemption or proof of runtime readiness.

Applicability follows actual changes and effects, not an A0 label or a docs-looking repository. Deployment, production operations, scarce/external resource allocation and implemented automated protected effects retain their applicable runtime obligations. Source-contract validator code still requires its actual code tests. Required source-level security, permission, Review, Validation, concern/integration/closure and Release gates are not removed by this separation; a concern PASS is not Version Qualification.

#### Manual source-work admission

The declared process executor MUST bind the exact operation, current Task/scope authority, base/source identity, applicable dependencies/role/resource predicates, permissions and unresolved findings. Assurance Plan currentness under `EXECUTION_ARCHITECTURE_STANDARD.md` §29.1 remains mandatory and may be established from durable manually collected facts. It neither requires a deployed runtime nor confers Gate PASS; absent, stale or ambiguous inputs fail closed. Required Release/finding sets, including explicit empty sets, remain bound under `ASSURANCE_PLAN_STANDARD.md` §12.

Manual admission consumes the existing `SINGLE_WRITER_ADMISSION` contract and EXE_ARCH §§11.1.1/27.3–27.5: one designated logical writer serializes the protected work/role key, actual reservation/generation advancement and Claim, with every actually required resource binding **all-or-none** at the admission point. Accepted reservation/Claim and resource facts MUST be durably published and read back before implementation source writes. Uncertain publication or incompatible ownership blocks; it cannot be bypassed by renaming a Task concern, role, compatibility group or session. Optional machine/audit field recording is not permission to omit substantive generation/ownership truth, and is not a requirement for a new deployed CAS service.

Recovery MUST either reconcile an actually accepted prior binding and its terminal/publication/resource/generation effects, or establish that no binding was accepted under EXE_ARCH §27.4. Missing optional historical fields alone do not establish invalidity or acceptance. New source delivery cannot retrospectively ratify an invalid/unproven Claim, erase actual prior side effects or release ambiguous ownership. Independent new concerns do not authorize work on an old protected key.

#### Manual standards concern integration

Before integration, the executor MUST fully read and record the applicable native surfaces: exact current PR HEAD and target, current Task/scope and dependencies, policy-selected Review, actual required Validation/checks, permissions, unresolved findings and governing Plan `CURRENT`. Pagination, failed/partial reads, unresolved conflicts, missing required checks, stale evidence or UNKNOWN currentness block. A policy that requires a native approval is not satisfied by relabelling a conversation comment as that approval.

Use the actual native expected-head guard. Recheck the target immediately before requesting integration; stop/recompute if observed drift invalidates the evidence. Record the actual request's source identity and observed target. This manual procedure is a bounded read sequence, **not atomic source/target CAS**, and does not claim a source-side change counter for native surfaces. A race not prevented by the native mechanism remains an explicit residual limitation. Source delivery under this route MUST NOT be reported as qualification of EXE_ARCH §14.1–14.4; those guarantees remain required for implementations claiming that controller contract.

After any attempt, reconstruct the result from durable native state. Bind actual source, target-before, integration SHA/tree and method as applicable, then perform the applicable compensating read over current admission surfaces. Unknown acknowledgement, unexpected source/target, invalidating target drift, a new blocker/conflict, incomplete read or failed compensation leaves the integration **UNRATIFIED**. No downstream READY/DONE/RQ is unlocked from it. An actual unexpected mutation is preserved as an incident; it is not rewritten as zero mutation or a successful Gate.

Any subsequent ratification is a **fresh subject-bound decision by the existing declared integration/Release authority**, consuming exact actual integration SHA/tree, expected versus observed source/target, newly impacted dependencies/checks/Review/Validation, permissions, unresolved findings and Plan `CURRENT`. Carry adverse facts forward. A compensating read alone cannot establish an absent atomic guard, and no decision backdates a rejected/unknown admission. If the actual tree cannot be qualified, retain quarantine/UNRATIFIED and downstream hold, and route any repair through the existing authority/Task process. No new ratification authority, state dimension or event family is created here.

#### Distinct immutable-artifact acceptance with an unavailable ledger

This prospective route implements EXE_ARCH23.5. It is a distinct current source
acceptance operation, not old Builder recovery or permission to modify/reapply
source. The old protected key stays held/UNKNOWN without Claim, generation,
resource or terminal mutation. It is limited to ADS standards-source delivery;
actual runtime, deployment, scarce/external effects retain their obligations.
Executors MUST satisfy the following ordered requirements. These uses of existing
manual owner records introduce no new
workflow state, event family, role, admission store or generation epoch.

##### Preconditions for pre-effect selection

The current Product/Task owners must first record the explicit Task-specific
acceptance amendment, binding this adopted route, exact permitted artifact and
the integration/process executor authorized to select it. This amendment grants
no old Builder authority and is not itself an artifact-selection or delivery
result. Its publication/readback must precede selection. Required Product Freeze
and normative adoption must already exist; a Product proposal alone grants nothing.

All six following facts, plus complete current Task/dependency/PR/check/Review/
permission/finding inputs and governing CURRENT, must be established **before**
the integration executor publishes its pre-effect selection. No integration
outcome or final delivery receipt is required to exist at this point.

1. **Exact existing artifact.** Identify its commit, tree and allowed file blobs,
   original PR/producer provenance and historical defects. The artifact was
   published before this decision. No new Builder edit, copy/reapply commit,
   rebase, conflict repair or branch update is authorized by this route.
2. **Explicit authority.** The current Product/Task contract permits delivery
   by fresh artifact acceptance. The existing integration/process authority
   is authorized to select the operation under the governing adopted standard.
   A Reviewer cannot create this permission; a proposed document cannot supply it.
3. **Actually disjoint protected effects.** Inspect the original grants,
   Task/PR contracts, native facts and referenced authoritative stores. Show
   that current source acceptance neither consumes/reassigns an old exclusive
   binding nor exercises an old Builder grant. An UNKNOWN historical generation
   is retained; an UNKNOWN *material overlap* fails closed. The human's ledger
   availability statement alone proves none of these conditions.
4. **Real source-acceptance boundary.** Identify the actual current authorized
   integration consumer(s). They must durably exclude old Dispatch/Claim,
   delayed old results and historical CI from qualifying current acceptance.
   Establish the boundary before selection; after publishing selection, read it
   back and verify that every affected authorized consumer binds only that
   selected operation/artifact and current assurance before requesting integration.
   A declaration, branch closure or list of known PRs alone is not that proof.
   A still-authorized independent old integration consumer or unresolved old
   protected integration request blocks this route.
5. **Resource/effect applicability.** Inspect the actual required effects and
   resources of this acceptance operation, and old effects that can affect its
   safety. No absence is inferred from an unavailable ledger. An observed or
   required uncertain external effect, exclusive resource overlap or authoritative
   effect pointer retains its own stronger reconciliation/fence obligation.
   Inaccessible evidence on a material acceptance boundary blocks. Unrelated
   hypothetical private memory does not acquire canonical authority.
6. **Fresh full assurance.** Inspect the entire actual artifact diff against
   current target and permitted scope. Re-execute every applicable source/code,
   schema/compatibility and negative-case check for the current candidate.
   Re-evaluate selected Review and all carried findings. Historical CI or a
   prior recommended Review skip is not current PASS. Any current required
   independent Review must be genuinely independent and exact-subject bound.

##### Selection, integration and post-effect verification

The existing integration executor publishes and reads back a scope-bound
**selection/authorization receipt**, identifying the existing Task, prior
acceptance-amendment ref, exact artifact/source/tree, expected target, adopted
owner refs, CURRENT, current assurance/finding refs, old-key HOLD/incident refs
and the authorized integration operation. Its durable canonical receipt ref
identifies this operation; equal SHA/tree values do not identify its authority.
This is a manual authority record using existing GitHub evidence conventions,
not a new workflow state/event enum, Claim or final Task-delivery result.

After verifying the selected consumer boundary and rereading exact currentness,
the executor may request integration. Apply this section's native expected-head
guard and immediate target reread. Preserve request identity and acknowledgement;
reconstruct the actual source, target-before, integration SHA/tree, method and
native outcome, then perform its applicable compensating/post-effect reads.
Record actual tested checkout SHA/parents/tree, not just run head/API base.

Unknown acknowledgement, conflicting/late facts, failed/partial verification,
unexpected integration or other invalidating drift means UNRATIFIED/HOLD under
the existing manual route. Preserve actual effects and incident; never retry
as presumed failure or infer Task completion. Only when actual integration and
post-effect/current assurance checks satisfy the owning rule may that executor
publish/read back the exact ratified integration result. An actual native merge
or that integration result alone is still not the Task-delivery decision.

##### Final Task-delivery decision and dependency consumption

The existing Task/process executor makes a separate, fresh post-integration
decision. It must consume the Task's prior acceptance amendment, selection
operation/receipt, **actual ratified integration SHA/tree and source/target
lineage**, complete post-effect verification, all applicable current required
gates/dependencies/Review/Validation, permissions, carried findings, old-key
HOLD/effect-owner refs and newly recomputed governing CURRENT. It cannot be
published as successful delivery until all these inputs exist and are current.

Publish and read back its explicit **final Task-delivery acceptance** and exact
evidence refs through the existing Task result/completion record, then perform
the existing native Task completion/routing updates with readback. This final
accepted delivery record is the **only** decision in this route that can satisfy
the Task delivery obligation and permit dependency satisfaction/derived READY.
Selection, a merge request/ACK, CI alone, a bare native merge, an UNRATIFIED
outcome or an integration-only result must never trigger those effects. Required
gates remain required even if a native Task label was changed prematurely.

Consumers bind the current Task, selection-operation ref and final exact
integration identity to its canonical accepted delivery receipt. A duplicate
request returns that existing receipt without another delivery acceptance,
Task-DONE transition or dependency wake; any conflicting attempted operation
requires explicit owner resolution, not last-writer-wins. Same-byte old Claim/
result/validation has no current operation authority and cannot substitute for
or overwrite selection, ratified integration or final delivery attribution.
It causes no old-key generation/resource/terminal mutation. A newly exposed
genuine material overlapping accepted binding follows the conflicts subsection's incident HOLD.

| Ordered owner action | Evidence available at that point | Allowed consequence |
| --- | --- | --- |
| Product/Task owner authorizes acceptance amendment | Adopted route, current Task and exact allowed source scope | Permission to assess/select only; not Task DONE |
| Integration executor selects artifact | All pre-effect selection preconditions; no future integration receipt assumed | Publish/read back selection; verify consumers; attempt guarded integration only |
| Integration executor requests/reconstructs/verifies integration | Actual request/outcome and source/target/integration SHA/tree; post-effect/current gates | Ratified integration result or UNRATIFIED/HOLD; no delivery/dependency unlock |
| Task/process executor decides and publishes final delivery | All final Task-delivery inputs: actual ratified integration, current gates and old-HOLD refs | Accepted delivery/readback may satisfy Task and wake true dependents once; otherwise HOLD |

These are ordered uses of existing owner records and workflow semantics, not
new lifecycle states. There is no requirement for final delivery evidence to
exist before selection or for successful delivery before its integration.

These conditions do not assert that the source boundary already exists for
S01/S04. Actual applicability must be inspected after adoption. In particular,
manual source integration's bounded race limitation remains explicit; it is
not transformed into atomic CAS or a physical fence by this amendment.

##### Conflicts, late facts and stop conditions

A current source HEAD/target change invalidates affected evidence. A conflict or
needed repair ends this route without source modification; ordinary Builder
admission is still blocked until its real prerequisites are satisfied. A new
Task/role/group/epoch cannot be used to perform those otherwise blocked edits.

A late old proposal/result cannot acquire current acceptance merely by quoting
an equal/larger generation or the same source bytes. Its actual history remains
preserved. A genuine delayed accepted-binding receipt is recorded as history;
if it reveals material overlap, an old authorized integration consumer/request,
or a fence premise that was false, hold the current/downstream scope and
reconcile the incident. Do not silently erase the old acceptance or current
mutation, fabricate zero effects, or retroactively bless the earlier decision.

An unexpected native merge/target mutation is not successful delivery. Preserve
the incident and apply this section's UNRATIFIED/compensation and any fresh
ratification requirements. No downstream readiness or RQ is inferred.

If the actual source-acceptance boundary cannot be established, name that exact
current capability/owner once. Do not rerun the unavailable-ledger request or
an unchanged Product Review. This route does not promise unconditional
liveness when a real safety predicate cannot be established.

#### Source closure and deferred verification lineage

Source-delivery conformance and runtime qualification MUST be reported separately. While unqualified, retain `REAL_NATIVE_CLAIM_AND_RELEASE_RUNTIME_NOT_PROVEN`, `REAL_HUMAN_DENY_E2E_NOT_PROVEN` and the version-required task-meta/Tally not-proven limitations; none becomes PASS from a source release. Required source closure/hidden-validation applicability and RQ still consume the exact integrated candidate and their actual owner rules.

Where a project/demo verification obligation has been selected, the source delivery's durable handoff/closure MUST name its follow-up owner and Issue or equivalent ref, the tested standard's immutable adopted SHA and exact source/schema scope (or explicitly mark that future pin unselected until adoption), negative oracles, and outstanding limitations. Before the later demo is dispatched its exact standard pin and own admission/resource/cleanup contract MUST be resolved. For v4.15, controller verification planning is tracked by [#1231](https://github.com/kaicreator-mm/ai-development-standard/issues/1231), with ADS runtime-verification planner as routing owner until a mechanism owner is selected; external task-meta/Tally interoperability remains [#1210](https://github.com/kaicreator-mm/ai-development-standard/issues/1210). These follow-ups do not become bootstrap blockers of standards-source delivery. No universal demo prerequisite for every standards change is introduced.
