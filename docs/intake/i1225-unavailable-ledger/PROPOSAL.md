# Unavailable Web ledger: bounded immutable-artifact acceptance

Status: **PROPOSED PRODUCT AMENDMENT; NOT EFFECTIVE AUTHORITY**.
Owner: [Issue #1244](https://github.com/kaicreator-mm/ai-development-standard/issues/1244).
Baseline: `9ad4dc97109f91004e96918c79b9a158c88d1aaa`.
Target: `version/v4.15`; main integration is not authorized.

## 1. Evidence and the decision that is missing

The human reports that S01/S04 ran on Web and their execution ledger existed
but is now unavailable: [#1225 factual receipt](https://github.com/kaicreator-mm/ai-development-standard/issues/1225#issuecomment-6316329147).
This is an availability report, not a recovered admission/termination receipt.
Old accepted bindings, pending outcomes and generations remain UNKNOWN.

The accepted [#1235 Product](../i1235-github-recovery/PROPOSAL.md) and implemented
EXE_ARCH23.2-23.3 correctly prohibit a replacement Builder on an uncertain key.
They intentionally offer no numerical escape hatch. The old
[generation-jump P1](https://github.com/kaicreator-mm/ai-development-standard/pull/1236#issuecomment-6309593617)
remains valid: a larger number, new epoch label, complete comment snapshot or
closed PR does not reconcile an old acceptance.

That route cannot reconstruct an unavailable decision. Repeating its inventory,
asking for an original chat or repeating accepted Review does not add evidence.
The new decision is whether *a different, nonconflicting operation* may accept
already-published immutable bytes while leaving the old Builder key held.
Current text does not positively grant that permission. This amendment must be
reviewed, frozen, implemented and prospectively adopted before use.

Unchanged inputs: #1235 P1-P6 goals, #1232 source/manual architecture,
RELEASE11.7A currentness and manual integration, normal Task dependencies,
Review/Validation and Release floors. No full Product/L2/DAG replay is proposed.

## 2. Product outcome and explicit limits

An authorized current integration/process executor may **consider accepting a
pre-existing immutable source artifact under a fresh source-acceptance decision**.
This is not successor Builder execution, same-key recovery, Claim ratification
or permission to resume/edit the old branch. The decision has its own exact
operation/subject and Assurance Plan CURRENT under existing authority; it does
not mint a new workflow state, event, admission store, role or generation epoch.

The delivery obligation of the existing Task may be fulfilled only by the
final post-integration Task-delivery decision defined in section 3.3, after its
Product/Task owners explicitly allow this route and all unchanged acceptance/
dependency/Review/Validation gates are satisfied. Pre-effect artifact selection
is authorization to attempt integration, never delivery acceptance or Task DONE.
Task delivery acceptance must be recorded separately from the unresolved old
dispatch/ownership incident. It does not mean every historical role is terminal.

The old protected key remains the SAME key with its original UNKNOWN frontier.
No reservation/Claim/generation transition, resource reuse/release, terminal,
new Builder write or replacement is performed on it. Its historical findings
remain on the owning Task and incident. Known accepted bindings remain accepted
history and retain their owning cancellation obligations.

This route is limited to ADS standards-source delivery under RELEASE11.7A.
It must not silently apply to deployments, data migrations, live controllers,
scarce resources or external operations. It proves source delivery only;
runtime and deferred task-meta/Tally limitations stay NOT_PROVEN/NOT_RUN.

## 3. Ordered decisions under existing authority

### 3.1 Preconditions for pre-effect selection

The current Product/Task owners must first record the explicit Task-specific
acceptance amendment, binding this adopted route, exact permitted artifact and
the integration/process executor authorized to select it. This amendment grants
no old Builder authority and is not itself an artifact-selection or delivery
result. Its publication/readback must precede selection. Required Product Freeze
and normative adoption must already exist; the proposed file grants nothing.

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

### 3.2 Selection, integration and post-effect verification

The existing integration executor publishes and reads back a scope-bound
**selection/authorization receipt**, identifying the existing Task, prior
acceptance-amendment ref, exact artifact/source/tree, expected target, adopted
owner refs, CURRENT, current assurance/finding refs, old-key HOLD/incident refs
and the authorized integration operation. Its durable canonical receipt ref
identifies this operation; equal SHA/tree values do not identify its authority.
This is a manual authority record using existing GitHub evidence conventions,
not a new workflow state/event enum, Claim or final Task-delivery result.

After verifying the selected consumer boundary and rereading exact currentness,
the executor may request integration. Apply RELEASE11.7A's native expected-head
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

### 3.3 Final Task-delivery decision and dependency consumption

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
genuine material overlapping accepted binding follows section 4's incident HOLD.

| Ordered owner action | Evidence available at that point | Allowed consequence |
| --- | --- | --- |
| Product/Task owner authorizes acceptance amendment | Adopted route, current Task and exact allowed source scope | Permission to assess/select only; not Task DONE |
| Integration executor selects artifact | Section 3.1 current preconditions; no future integration receipt assumed | Publish/read back selection; verify consumers; attempt guarded integration only |
| Integration executor requests/reconstructs/verifies integration | Actual request/outcome and source/target/integration SHA/tree; post-effect/current gates | Ratified integration result or UNRATIFIED/HOLD; no delivery/dependency unlock |
| Task/process executor decides and publishes final delivery | All section 3.3 actual ratified integration/current gate inputs and old-HOLD refs | Accepted delivery/readback may satisfy Task and wake true dependents once; otherwise HOLD |

These are ordered uses of existing owner records and workflow semantics, not
new lifecycle states. There is no requirement for final delivery evidence to
exist before selection or for successful delivery before its integration.

These conditions do not assert that the source boundary already exists for
S01/S04. Actual applicability must be inspected after adoption. In particular,
manual source integration's bounded race limitation remains explicit; it is
not transformed into atomic CAS or a physical fence by this amendment.

## 4. Conflicts, late facts and stop conditions

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
the incident and apply RELEASE11.7A UNRATIFIED/compensation and any fresh
ratification requirements. No downstream readiness or RQ is inferred.

If the actual source-acceptance boundary cannot be established, name that exact
current capability/owner once. Do not rerun the unavailable-ledger request or
the unchanged Product Review. This proposal does not promise unconditional
liveness when a real safety predicate cannot be established.

## 5. Independent expected-decision cases

This table is a proposed Product oracle, not executed native/runtime evidence.

| Case | Input | Expected outcome |
| --- | --- | --- |
| A01 | Ledger unavailable; prior Task amendment plus section 3.1 current preconditions proven; exact existing artifact; no protected overlap | Select/read back artifact, then guarded integration and actual post-verification; only a later fresh section 3.3 accepted delivery can satisfy Task/dependencies. Old key stays held/UNKNOWN throughout |
| A02 | Same, but current source consumer boundary is only asserted | BLOCKED; no acceptance from prose |
| A03 | Another still-authorized consumer can integrate under an old grant | BLOCKED until that material authority is actually resolved/fenced |
| A04 | Source accepted by new decision; old Builder publishes a different HEAD | Old publication has no current assurance; expected-head mismatch blocks any later integration; re-evaluate current native effects |
| A05 | Fresh validation finds a source bug or a merge conflict | FAIL/BLOCKED as appropriate; no repair write under this route; no new key used to evade Builder HOLD |
| A06 | Counter is UNKNOWN; executor proposes a large number/new epoch/renamed Task | Reject replacement; zero accepted reservation/Claim/generation mutation |
| A07 | Old accepted exclusive resource overlaps this operation | BLOCKED; no source-route resource reuse or fabricated release |
| A08 | An observed deployment/request outcome is UNKNOWN | Stronger effect reconciliation/fence remains; no inference from a docs label |
| A09 | Only old CI or old Review is provided | Current required assurance NOT_RUN; no merge eligibility |
| A10 | Same bytes, current late blocking finding/changed permission/partial page | Recompute or BLOCKED; old CURRENT cannot override it |
| A11 | CI reports the right PR head but checkout used the old synthetic merge | Reject as current integration proof; inspect actual checkout context |
| A12 | Merge acknowledgement unknown or post-effect tree differs | UNRATIFIED/downstream HOLD; reconstruct before retry or ratification |
| A13 | Later receipt reveals an omitted material overlapping accepted binding | HOLD affected acceptance/downstream, preserve both histories and incident; no retrospective zero-effects assertion |
| A14 | Artifact delivered under all gates; old execution incident still unresolved | Distinct current delivery record only; no old-role/resource closure and no full-version RQ inferred |
| A15 | Executor attempts to rely on this proposed file before adoption | BLOCKED; no effective permission |
| A16 | After selection or ratified integration, same-byte old Claim/result/validation or duplicate request arrives under an old/different grant | Byte equality conveys no current operation authority; preserve current selection/final attribution, no substituted receipt, second delivery/Task-DONE/wake or old generation/resource/terminal mutation. Genuine material overlapping accepted binding instead triggers A13 HOLD |
| A17 | Selection published, but merge ACK unknown or post-effect verification fails; consumer tries to complete Task | Reject delivery/dependency unlock; UNRATIFIED/HOLD remains, no final accepted delivery can be published from selection |

All previous G01-G24 replacement-recovery cases remain unchanged. A01 does not
turn G05/G08/G10 into replacement eligibility; it selects no replacement at all.

## 6. Minimal implementation and Review boundary

Selected required Product Review covers only this new source-acceptance route,
its non-overlap proof, consumer/fence sufficiency, ordered selection/integration/
final-delivery decisions, old-role separation, late-fact behavior and A01-A17.
It must explicitly judge whether this
is a real disjoint acceptance operation or a disguised stolen Claim/gate waiver.
The prior numerical-jump P1 remains adverse precedent. Do not replay accepted
#1238 implementation Review, unchanged #1235 goals or the six-Task DAG.

On accepted exact-source Product judgment, the existing Product controller must
record explicit Freeze before implementation. The compact L2 mapping is then:
EXE_ARCH23 owns the distinction from same-key replacement; RELEASE11.7A owns
source acceptance and integration conditions; existing Task/handoff clauses
surface distinct delivery/old-incident records. Existing schemas/events remain
unchanged. A bounded implementation needs discriminating behavioral guards,
full rejected-state snapshots, meaningful positive execution and late-overlap
negative cases linked to this independent oracle. Local model evidence cannot
prove native fences or runtime behavior. Required implementation Review covers
the actual new normative/model delta once; unchanged evidence is reused.

Before applying the adopted rule to S01/S04, inspect their actual scopes and
consumer grants. Explicitly record the Task acceptance amendment, exact bytes,
actual acceptance boundary, CURRENT and fresh validation. If all conditions
hold, integrate each original immutable PR under that current decision and
resume the native six-Task chain. If they do not, publish the precise unmet
predicate without manufactured admission or another generic audit loop.

## 7. Evidence limits and handoff

This proposal establishes a reviewable alternative to reconstructing unavailable
historical data. It does not establish that the alternative is already lawful,
that its acceptance boundary exists, or that S01/S04 pass any gate. No actual
source acceptance, successor execution, old resource cleanup, native race test,
runtime qualification, release qualification or main merge has occurred here.

The owning Issue and exact PR source are sufficient for a fresh independent
receiver. Its result, actual declared operator/session, per-finding judgment
and terminal must be written back to GitHub. Source changes after judgment
require only the affected exact-source delta Review; no PASS is transferred.
