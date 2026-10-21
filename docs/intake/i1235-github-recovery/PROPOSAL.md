# GitHub-only exit receipts and abandoned source-work recovery

Status: proposed Product/recovery contract; NOT effective normative authority.
Owner work item: [#1235](https://github.com/kaicreator-mm/ai-development-standard/issues/1235).
Exact proposal baseline: `6b404dbe4c1b3a685d9c6ca6484e4075d225ca9e`.
Integration target: `version/v4.15`; no main integration is authorized.

## 1. Incident and existing authority

ADS already requires GitHub-only recovery. The baseline's
`LOCAL_AGENT_HANDOFF_PROTOCOL.md` sections 1, 8 and 12 require a durable contract,
GitHub-first result publication and continuation by a replacement worker from
GitHub facts alone. `EXECUTION_ARCHITECTURE_STANDARD.md` sections 1, 11.1.1,
11.2, 23 and 29.6 exclude unrecoverable runtime/chat authority. `AGENTS.md`
requires handoffs executable from repository and Issue alone.

The following are different defects:

1. Execution defect: S01/S04 published an invalid initial Claim and later a
   shape-valid Claim without proven governing CURRENT. Required durable
   reservation/terminal/resource/generation evidence was not reconstructed.
2. Controller execution defect: requests #1215@6307490337 and
   #1218@6307490789 made the original conversation/firsthand private memory the
   apparent recovery prerequisite. That requirement is absent from ADS and
   contradicts the existing GitHub-only recovery guarantee. It is withdrawn at
   #1215@6308406398 and #1218@6308407017.
3. Specification gap: sections 11.2/27.4/27.5 correctly hold ambiguous
   admission, but do not specify a complete bounded procedure for resolving
   an absent producer's incomplete publication using the canonical fact plane.
   Section 23 promises recoverability without specifying the missing-receipt
   obligations and the conditions for prospective fencing of abandoned source
   proposals. That omission encouraged indefinite investigation of private
   state rather than an owner decision over published authority and real effects.

Evidence is already on GitHub: #1215@6308320620 and #1218@6308313725 record the
latest fresh-context readbacks and unavailable private observations;
#1225@6296327167 preserves independent adverse findings. These records are
evidence of an incomplete handoff, not proof that physical side effects are
absent. The source-only manual amendment #1232/#1233 is adopted at the baseline
above; it supplies no retrospective Claim acceptance or resource cleanup.

## 2. Product requirements

P1. Every execution phase publishes its current result/exit and next route to
GitHub before returning a final chat response. This includes PASS, FAIL,
BLOCKED, partial work, cancellation and a deliberate stop. A crash cannot be
assumed to run a finalizer: publish admission and material checkpoints before
allowing the protected work they authorize.

P2. A receiver needs only the repository and work-item pointer. The original
conversation, a specific model/provider, private memory and the continued
availability of the producing worker are never project authority or a required
recovery environment. Asking a producer to supply missing evidence is optional
evidence collection, not the only legal recovery route.

P3. Missing publication is a durable evidence/producer defect. A fresh receiving
executor repairs reconstructible records from their actual sources, preserving
producer attribution and its own reconstruction provenance. It never signs as
the absent producer, invents a historical terminal or changes an old failure to
PASS. A currently authorized recovery controller owns decisions that cannot be
made by mechanical reconstruction.

P4. Recovery has bounded, explicit canonical scope and an actionable result:
continue a proven current binding; perform a prospective authorized cancellation
and successor admission after actual reconciliation/fencing; or hold a specific
unresolved effect/resource with its real owner and required observation. It must
not repeatedly route to an unavailable conversation or treat every imaginable
undocumented process as an accepted canonical owner.

P5. GitHub-only authority does not mean physical-effect erasure. A known or
actually required external resource, accepted active binding, unresolved durable
admission reference or uncertain protected-effect request remains a real blocker
until its owner/source is reconciled or an actually effective fence is verified.
No cleanup, stopped-process, zero-mutation, released-capacity or runtime PASS is
inferred from a missing receipt.

P6. No mandatory runtime deployment, new scheduler/database, role, workflow
state, event family, original-owner credential or second signature is introduced.
Use existing dispatch/events, SINGLE_WRITER_ADMISSION, owner decisions, exact
CURRENT bindings and source/manual integration checks. Existing required Review,
Validation, dependencies and unresolved-finding authority remain unchanged.

## 3. Required durable exit/handoff information

These are semantic contents of existing records, not a new schema/event family.
The owning Issue links immutable sources and current accepted event refs:

| Content | Required distinction |
| --- | --- |
| Repository, Task, role, protected key, dispatch and declared operator | Producer identity versus current receiver/recovery authority |
| Exact source/base/target and Task/Execution Pack refs | Tested, reviewed, proposed and integrated identities kept separate |
| Accepted reservation/Claim decision and generation authority | Accepted/rejected/uncertain; real before/after decisions, never a guessed counter |
| Allowed effects and actual required resources | Empty-by-contract and observed unallocated versus unknown actual effects |
| Source/PR/checkpoint mutations and external-effect request/result refs | Observed published results versus pending/unknown acknowledgement |
| Current work/dispatch outcome and publications still pending | Logical cancellation versus physical process/runner termination |
| Actual command/exit/toolchain/profile and Review selection | PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE with genuine exact tuples |
| Remaining findings, hold scope, next receiving owner/action | Explicit scope of a blocker; no chat-only next step |
| Publication readback and reconstruction provenance | A successful send/ACK alone is not a verified durable receipt |

Do not put secrets, private prompts or chain of thought in the receipt. Link
sanitized durable external evidence when physical resources need their own
authoritative stores. If a field is unavailable, publish UNKNOWN with its exact
missing source, current owner and next safe action. UNKNOWN is not a PASS.

## 4. Proposed bounded recovery algorithm

This section proposes the missing owner rule. It MUST NOT be used on #1215 or
#1218 before required independent Product Review, explicit exact-source Freeze,
normative implementation/validation and prospective adoption.

### R1. Establish the canonical boundary and current recovery authority

The current process/recovery controller identifies the protected key, applicable
frozen authority, Task/Execution Pack, all dispatch/Claim/admission/result refs,
Issue/PR timelines, native dependencies, source/target refs, permissions, checks,
Review and unresolved findings. Read every page and follow every authoritative
admission/effect/resource pointer to closure. Record the inspected scope and
exact identities; a search hit count is not proof of completeness.

A genuinely inaccessible authoritative pointer, conflict, partial read or
unknown required resource keeps the affected key held. Unrelated unknown private
memory is not an additional authority surface: canonical accepted facts must
already have been durably published by the original admission contract.

### R2. Separate three admission outcomes

- Proven accepted binding: preserve its authority and history; use the existing
  owning cancellation/terminal/recovery authority. The unclaimed-reroute shortcut
  cannot steal it. Its required resources/effects need actual reconciliation.
- Proven rejected/unadmitted proposal: preserve its invalidity, source artifacts
  and any actual side effects; it cannot become an accepted historical Claim.
- Uncertain durable admission/effect: inspect the actual referenced sources.
  A missing producer cannot resolve it by assertion. Continue only after the
  existing owning authority records a lawful prospective recovery with the
  actual affected effects fenced, or retain the specific hold.

Absence of a valid Claim does not prove absence of a physical effect. Equally,
an undocumented hypothetical process cannot acquire accepted Claim authority.

### R3. Narrow source-only prospective recovery

This route is limited to normative/source/contract work under RELEASE §11.7A.
Any deployment, irreversible/external effect or actually required scarce resource
retains its own stronger recovery obligations. A docs/A0 label is insufficient.

The current recovery controller must establish all of the following:

1. The complete canonical fact boundary from R1 is readable; no conflicting
   accepted owner or unresolved authoritative admission/effect pointer remains.
2. All actually required resource/effect sets for the proposed successor are
   known. Existing externally allocated resources are neither reused nor called
   released from missing evidence. An observed old external effect remains held
   until its own owner supplies reconciliation or an effective physical fence.
3. Every observed old source branch/PR/commit is explicitly quarantined from
   acceptance. Preserve its immutable history; close superseded proposals without
   merge where authorized. New source work starts from the exact current
   authorized integration base on an independently admitted successor branch,
   under the same protected work/role key. No role/group/Task rename evades it.
4. The actual admission writer publishes a prospective cancellation/supersession
   and source-effect fence decision. It states whose authority is revoked now,
   which old proposals/branches cannot be accepted, and how late old results are
   rejected. It does not assert that the old process stopped or that all old
   physical effects were zero. Accepted active Claims require their own lawful
   owning cancellation; this route cannot call them unclaimed.
5. Before successor admission the controller verifies that native exact-source
   guarded integration will consume only the freshly bound candidate; complete
   pre/post reads, current target checks and uncertainty holds remain mandatory.
   A logically fenced old source branch is not a physical runtime fence and must
   never be reported as one.

### R4. Reconcile the same serialized authority before any generation advance

**The exceptional `new generation > max(published bounds)` rule is withdrawn.**
Independent Product Review [P1-01](https://github.com/kaicreator-mm/ai-development-standard/pull/1236#issuecomment-6309593617)
demonstrated that a complete comment snapshot cannot exclude an in-flight old
acceptance. A larger number, a branch quarantine or an owner's declaration alone
does not fence it. Unknown historical numerical state is not proof of no Claim.

The proposed procedure uses only the existing §11/§27 serialized admission
authority on the **same protected key**. It adds a durable recovery checklist,
not a new acceptance store, epoch, lifecycle or generation-jump power. The current
controller publishes its recovery authority, inspected predecessor refs and the
following independently checkable fence-completion evidence on the owning Issue:

1. **Common decision order.** Identify the single actual writer and all current
   grants that can accept a Claim for this key, plus the actual source-integration
   consumers. The existing serialized authority must order all old acceptance
   attempts, cancellation/revocation and successor admission. GitHub comment
   creation time/ID is not that order. A second writer or an acceptance-capable
   pending request outside this order means HOLD; do not call an inventory a CAS.
2. **Close pending admission outcomes.** Reconcile every referenced or observed
   pending/uncertain admission and its composite work/resource result at that
   authority: accepted (with actual generation and binding), rejected (with no
   accepted binding), or still uncertain. Preserve the actual result. For an
   accepted active binding, its owning cancellation authority must resolve it
   and its resource/effect obligations before replacement. A fence cannot turn
   an already accepted binding into an unclaimed proposal. Still uncertain means
   HOLD under §27.4, even if no Claim comment is currently visible.
3. **Revoke future old acceptance.** At the same serialized authority, withdraw
   outstanding old writer grants and old dispatch eligibility prospectively,
   publish/read back the decision and its exact predecessor/decision refs. Show
   how every admission/integration consumer rejects that revoked authority.
   For the manual source route, the designated sole writer must actually cease
   old acceptance duties before successor admission; the current integrating
   controller consumes the revoked-dispatch and exact-source exclusion records.
   If an old autonomous writer can still commit accepted decisions, a grant
   revocation comment does not complete the fence: reconcile/drain that writer
   or verify its actual common acceptance fence. No original-chat reply or
   stopped-process assertion is required when the shared authority/effect fence
   is independently proven. If neither route is provable, HOLD with that writer
   or consumer surface and its existing owner explicitly named.
4. **Reconstruct the exact frontier.** Derive the actual current generation and
   accepted binding set from the reconciled serialized decisions, including any
   lawful cancellation/reroute advancement. Record the predecessor lineage and
   real before/after values. Merely knowing all published lower bounds does not
   satisfy this step. If the exact current counter remains UNKNOWN, no barrier,
   reservation, successor Claim or source write is permitted. Do not reset to
   zero, invent a larger value or change the protected key to escape the hold.
5. **Consume the fence at fresh admission.** Re-read fence completion, current
   authority, exact generation, resources, findings and §29.1 CURRENT immediately
   before the ordinary all-or-none reservation/Claim operation. Use the existing
   once-only generation transitions, not a recovery-specific increment. Publish
   and read back its actual decision before source work. Conflicting/late facts
   that defeat any predicate trigger HOLD/reconciliation, never dual acceptance.

Canonical precedence follows the **accepted serialized decisions**, not arrival
order or a numeric maximum. An old Claim accepted *before* effective revocation
must be reconciled as accepted history; if still active it prevents replacement.
An old proposal presented *after* effective revocation is rejected STALE with
zero canonical mutation, even if it quotes a large/equal generation or arrives
as a well-formed GitHub comment. Its publication is retained as an attempted
proposal, never silently promoted to acceptance. A delayed receipt of a genuine
pre-revocation accepted decision is historical only **after** its binding and
terminal were included in reconciliation. If it exposes a previously unresolved
accepted binding, fence completion was not established: HOLD the successor and
reconcile the incident; do not retroactively erase either observation or infer
zero source/resource effects. Late source results similarly cannot become current
Validation, Review or integration eligibility for the freshly bound candidate.

Fence completion therefore requires **all five** evidenced predicates; closing
an old PR proves only source exclusion. This is source/manual authority fencing,
not physical process isolation or proof of native atomic CAS. If the existing
authority cannot establish the exact frontier and exclusion of pending accepted
operations, the current proposal deliberately supplies no escape hatch. Publish
the precise remaining surface and route any materially different prospective
authority design through its owning Product/L2/Task process before use. Do not
repeatedly request private chat evidence or claim this proposal already unlocks
S01/S04; their actual recovery predicates remain to be established after adoption.

### R5. Fresh admission, re-execution and current validation

After actual recovery, construct independently recomputable §29.1/Assurance
Plan §12 CURRENT over exact source/owner/proof/Task Pack/Release/finding inputs.
Publish/read back the actual new serialized reservation/Claim and all required
resources before new source writes. Reapply only authorized source changes to
the current base; retain original artifact provenance as historical input.

Rerun real required source tests, obtain the actually selected independent Review,
and consume the actual exact candidate/target at integration. Old synthetic CI,
NOT_RUN Review or a historical diff is not transferred into new PASS. Recovery
alone never makes a Task DONE or unlocks its dependents.

### R6. Publish the receiving contract and stop conditions

Publish the recovery outcome, exact evidence, CURRENT/admission refs, state,
remaining findings and next receiving owner/action to GitHub, with readback.
The next worker can be new. If held, name the actual missing authoritative
surface/physical effect and the action the current controller/resource owner
must take. “Return to the original conversation” is not a valid required route.

## 5. Discriminating scenario/expected-decision table

This is a Product decision oracle, not runtime/native verification or a Claim
acceptance. It is independently readable and must guide future executable
conformance. It does not close #1232 P2-01/#1227's existing implementation work.

| ID | Scenario | Expected decision and reason |
| --- | --- | --- |
| G01 | Original chat lost; complete accepted result, exact source and resources all durably resolved | Continue from GitHub; never ask for original chat |
| G02 | Producer omitted exit; original chat unavailable; source-only effects known, complete published bounds inventoried but exact current counter not yet reconciled | HOLD successor admission; owner may collect R1–R4 evidence, bounds alone never authorize a generation |
| G03 | Same as G02, but only “no heartbeat” supports termination | Reject that termination claim; require actual source/effect fence, not elapsed time |
| G04 | A known accepted active Claim remains and no owning cancellation exists | Hold; no unclaimed reroute or stolen Claim |
| G05 | A referenced admission record is inaccessible, despite the Issue comments being complete | Hold; incomplete authoritative closure cannot issue a barrier |
| G06 | Source proposal used invalid RUNNING; actual cloud allocation is observed | Preserve invalid Claim; hold cloud/resource recovery; never infer zero allocation |
| G07 | A0/docs-labelled task actually deploys a service | Runtime obligations apply; source-only recovery is inapplicable |
| G08 | Old PR excluded; an old acceptance request is known pending with unknown outcome; no common fence/drain evidence; no observed external resource | HOLD; source exclusion and apparently empty resources do not resolve admission uncertainty; no new branch admission |
| G09 | Proposed generation comes from comment count, timestamp or resetting UNKNOWN to zero | Reject; no genuine generation decision |
| G10 | Every published bound is known, but one unresolved authoritative ref might name a higher accepted generation | HOLD; exact current generation and binding set not reconstructed |
| G11 | Only private undocumented speculative process is cited as an accepted owner | Do not create owner authority; inspect actual declared effect surfaces and record evidence defect |
| G12 | Fenced recovery completed; new CURRENT absent or stale | Hold successor Claim/source writes |
| G13 | Fresh Claim accepted; new source not tested; old synthetic CI is green | Validation NOT_RUN; no merge eligibility |
| G14 | Same source HEAD; new blocking Review/finding arrives after preflight | Recompute/hold; earlier CURRENT cannot override blocker |
| G15 | Native target changed, permission revoked or a required page failed | Recompute/hold; no merge from partial/stale inputs |
| G16 | Merge acknowledgement unknown or compensating read failed | UNRATIFIED/downstream hold; do not retry as presumed failure/success |
| G17 | Fresh source concern validated and merged under its actual required gates | Concern result only; no full-version RQ, runtime PASS or main merge |
| G18 | Current receiver changes operator label to impersonate old producer or Reviewer | Reject; preserve producer/reconstructor provenance and actual independence |
| G19 | All R4 predicates evidenced: same serialized writer resolves old rejected request, revokes old grant, proves exact frontier; source consumers exclude old PR; required/observed external effects and resources empty; old process unobserved | CONTINUE to fresh CURRENT and ordinary admission on the same key; do not assert process termination or completed validation |
| G20 | After the completed G19 fence, old writer publishes an old g1 or equal-number Claim proposal; no accepted predecessor decision exists | STALE, zero accepted Claim/resource/generation mutation; preserve attempted publication; a number does not restore revoked authority |
| G21 | Same source fence as G19, but an actually observed deployment/request has unknown outcome and no physical fence | HOLD affected successor; source-only recovery cannot erase external effects; name existing effect/resource owner and reconciliation action |
| G22 | Old Claim accepted before revocation; its delayed receipt arrives before fence completion, binding still active | HOLD; reconcile real accepted binding and owning cancellation, no unclaimed-reroute shortcut |
| G23 | Late receipt proves an accepted old binding omitted from a claimed completed fence, after successor Start | HOLD successor/downstream; fence completion was false; preserve incident and actual effects, reconcile at common authority, no retroactive ratification |
| G24 | Late old source result refers to an accepted pre-revocation binding already fully reconciled/terminated in completed fence; new source differs | Historical only; no transfer of old PASS or new terminal; continue only under current successor's own gates |

## 6. Implementation plan after Product Review and Freeze

One bounded normative implementation concern should:

- Extend LOCAL_AGENT_HANDOFF_PROTOCOL sections 8/12 with mandatory semantic exit
  contents, checkpoint-before-effect discipline, fresh receiver reconstruction
  and forbidden original-conversation prerequisite.
- Extend EXE_ARCH section 23 and the existing section 11/27 owning recovery rules
  with the reviewed R1–R6 boundary, especially the exact R4 decision. Cross-link
  the existing authority rather than create a parallel recovery lifecycle.
- Synchronize existing handoff/terminal templates and source-specific manual
  reference with the adopted semantic obligations; no new event/schema family.
- Implement small deterministic source-decision tests from G01–G24 with
  independently anchored expected outcomes. Keep actual resource/native/runtime
  verification separate and disclose every unproved capability.
- After validation and required implementation Review, explicitly adopt the
  exact source, then recover S01/S04 through real GitHub receipts under that
  source. Re-execute/validate their source under new lawful admission before
  merging into version/v4.15. Continue the six-task DAG and version closure.

No existing core concern is renamed or marked completed by this proposal.
Required independent Review is confined to the new recovery authority/contract;
do not replay old Product/source reviews without a material change.

## 7. What this proposal proves and does not prove

Proven by cited sources: GitHub-only recovery was already required; the old-chat
prerequisite was an execution error; the selected incident has missing durable
recovery evidence; existing rules lack the precise proposed abandoned-publication
reconciliation procedure. Independent Review P1-01 rejected the numerical-jump
design; this successor withdraws it and specifies same-authority fence and
reconciliation obligations instead. The decision table is an inspectable safety
specification.

NOT proven: a historical Claim was valid; an old counter/process/resource is
known/released; a real controller/native runtime implements R1–R6; a source fence
is a physical isolation boundary; any case in the table has been executed against
native GitHub races; actual task-meta/Tally E2E; version Release Qualification.
The current proposal is not effective authority and unlocks no legacy key.

## 8. Exact-source Review and handoff contract

Required independent Product Review assesses P1–P6, the historical diagnosis,
R1–R6 (especially R4's repaired authority/fence boundary), G01–G24 and cross-owner integration.
It must distinguish acceptance of the existing GitHub-only invariant from
acceptance of the proposed recovery rule. Findings refer to the immutable PR
HEAD/source, preserve actual reviewer operator/session independence and remain
on #1235/its PR. Review alone is not Freeze or admission.

On PASS with any properly disposed nonblocking findings, the declared Product
controller records explicit exact-source Freeze on #1235, then a bounded L2/Task
contract and real source implementation admission. On changes requested, revise
this same proposal concern; do not ask the human to locate private old chats.
Every receiver reads this work item, current PR, exact evidence and current
next-action record from GitHub; chat carries only a pointer.

Focused successor Review must explicitly dispose of carried P1-01/P2-01 against
this exact source. The Builder's proposed repair is not a verified resolution.
The prior CHANGES_REQUESTED verdict remains immutable for its original SHA;
do not replay unrelated accepted Product directions or relabel the refused
native GitHub Review submission as successful. This Task requires independent
logical Review evidence, not a native approval object; any separately selected
native requirement would still need its actual distinct transport reviewer.
