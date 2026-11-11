# R30 — Fresh Independent Source-First CAS / Writer / Admission Semantic Review

**OUTPUT_LABEL:** ADS_1366_R30_CAS_WRITER_ADMISSION_SEMANTIC_REVIEW  
**Main issue:** #1366. **Review type:** independent semantic review of bounded formal hypotheses; not a second native execution or an ADS normative approval.  
**Read subject (before review):** experiment/v4.19-formal-proof-r0 at 0a30fbab6c5884e12e4e1c5f2e02d549e635aee8; candidate PR #1365 at dac263fa4c0ab155406d2f2117459b34322cc988, OPEN/not merged/not frozen.  
**Verdict:** PASS_WITH_P2 for the **declared bounded models**, with 0 demonstrated P0/P1 model defects, 0 demonstrated P0/P1/P2 normative-source defects, 3 scoped P2 evidence/coverage limitations. **Semantic equivalence, actual publisher/CAS and full ADS proof: NOT_PROVEN.**
**Review independence order:** first inspected the candidate's canonical rules and source blobs, derived the criteria below, then read the experiment models, declarations and R29 receipts. Prior Builder reviews were not treated as acceptance criteria.

## 1. Independent source-derived criteria

Source at PR #1365 exact HEAD; verified Git blob pins:

- standards/EXECUTION_ARCHITECTURE_STANDARD.md — 1f1601a20db08d263955241607dfd08d8b8f77e1; especially §§6, 11/11.1/11.1.1/11.2, 23.1–23.3, 27.2–27.4.
- standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md — 935a905d593d7aec027cb54b5b137250ca14a4c1; §§8.1, 8.4.2, 8.5 and schema/intent admission.
- standards/EXECUTION_PACK_STANDARD.md — 1bd8631dd7120ef56747731e304632b60d7cb5e1; Task Pack write authority, exact Execution Pack and claim-time checks.
- scripts/v34_rules.py — 0829be09f46dde75710bc54607a14edd7a2c4cea; helper/projection semantics are not proof of a real serialized GitHub publisher.
- standards/TASK_DECOMPOSITION_STANDARD.md §§3–4 and standards/GIT_EXECUTION_STANDARD.md §4 supply distinct scope and writable workspace/isolation obligations.

Derived required behavior before inspecting any formal model:

1. **Claim and dispatch reservation** require current READY/role/Task+Execution Pack/base/source predicates, a real one-writer serialized authority or linearizable conditional write, and a monotone current-generation decision. Re-read-only or last-comment-wins is insufficient. Rejected/stale proposals have no accepted Claim/partial mutation.
2. **Protected key** is deterministically repo#task:role:normalized_compatibility_group; profile, executor, environment and session cannot create a new key. Nondefault groups require a *resolved, current, scoped* higher-authority compatibility grant. Other genuine work keys may coexist only with separate write-set, resource and dependency compatibility.
3. **Source mutation** needs accepted current Builder Claim, current original Task Pack write scope and isolated/conforming write ownership. Distinct Claim keys do not license overlapping concurrent writes. A boolean label or an independent worktree alone is not a canonical Task write grant.
4. **Start Record** is the durable accepted DISPATCH_CLAIMED/current accepted Claim with operator, dispatch and exact subject, preceding protected effects. Same-dispatch/same-operator resume is idempotent; a different dispatch starts with a new accepted Claim after unambiguous terminal/publication/resource/generation reconciliation. State cards/labels are projections only.
5. **Composite admission**, when scarce resources/compatibility bindings are required, must atomically bind the complete set with the Claim; uncertain publication, missing authority, missing resources or incomplete readback fails closed. A source hypothesis may intentionally abstract this but cannot assert the real transaction was verified.

## 2. Model readback and semantic scope

Exact model blobs on review subject:

| Property | Model/blob | Positive bounded meaning | Critical preconditions NOT independently established by the model |
| --- | --- | --- | --- |
| ADS-P-CAS | formal/models/authority/serialized-admission.smt2 @ a405d543f0de43f1455f6018043fd3002ccba923 | Two ordered requests on a supplied same-key flag; stale expected generation rejected; eligible same-key successor after assumed closure; distinct-key coexistence | firstAuthorized/secondAuthorized/ready; mapping sameProtectedKey to actual canonical tuple; real generation frontier, writer linearization, durable terminal and required resource readback |
| ADS-P-WRITER-KEYS | formal/models/cross/writer-exclusion.smt2 @ dd00d7186df5577587f0b3340fe1cbb078bad437 | Two active claims with simultaneous writes cannot overlap *if* the supplied known/overlap flags are correct; legal disjoint witness | claimA/claimB are accepted GitHub facts; active/current authorization; current Task Pack path ownership; actual overlapping files/refs and workspace/resource isolation |
| ADS-P-ADMISSION-EXT | formal/models/authority/admission-boundaries.smt2 @ 66d89305305541d7e095e053fa8fcb55e9e6a9b4 and admission-boundaries-r8.smt2 @ 73c7ab4d845129b5f6335e275c9e696bc3a5b3d3 | Bounded reservation generation, same-operator resume, second Start Record conditioned on supplied original Claim + new accepted authorized Claim; two nondefault groups require all supplied grant predicates | current valid *resolvable* grant family/scope/revocation; actual DISPATCH_CLAIMED readback, serialized outcome, current generation, publication/resource release, real source-authority consumer |

These are **conditional invariants**. In particular, the SMT assumptions are not established by matching model source strings against an unchanged Git blob. Source blob/anchor matching confirms provenance, not the runtime truth of a Boolean input.

## 3. Reproducible assumption-boundary witnesses (NOT real production counterexamples)

The following values were substituted directly into the source model formulas during this review. This was propositional/arithmetic evaluation only; **Z3/cvc5/TLC NOT_RUN for R30**, and these are **not** counterexamples to the model's own asserted implications.

- **CAS key-identity gap (P2-01):** generation=7, otherKeyGeneration=7, expectedFirst=expectedSecond=7, firstAuthorized=secondAuthorized=firstReady=secondReady=true, sameProtectedKey=false, firstClosed=false. Model evaluates firstAccepted=true, secondAccepted=true. If two real dispatches differed only by profile/environment and had the same canonical repo/task/role/group, source §11.1.1 instead makes them one protected key and forbids the second active admission. The model cannot determine whether sameProtectedKey=false is legitimate. **No actual invalid dispatch observed.**
- **Writer source/write-set gap (P2-02):** claimA=claimB=activeA=activeB=authorizedA=authorizedB=writeA=writeB=true; sameProtectedKey=false, writeSetsKnown=true, writeSetsOverlap=false. All writer-exclusion assertions hold and the simultaneous-write witness is permitted. If authoritative Task Packs actually overlap, the assumed overlap=false would be incorrect and source parallelism/write authority would forbid the writes. The model cannot read the Pack/path facts and does not establish their truth. **No actual overlapping write observed.**
- **Start/Grant admission gap (P2-03):** originalClaim=originalTerminal=currentGeneration=successorAuthorized=successorClaimAccepted=true, sameDispatch=false, publicationAmbiguous=false permits secondStartRecord=true in R8. The model has no actual event/current object, independent permission-currentness or required resource binding/release readback. If those real source facts were unresolved, §§11.2/23.1/27.4 would forbid successor start despite the Boolean assignment. Likewise, all R8 grantRef/current/family/scope flags can be set true without consulting an actual #issue@comment grant. **No actual false accepted Start Record observed.**

For each witness, the *missing concrete-source predicate* is outside the current bounded SMT encoding. Thus classification is an **evidence/semantic-coverage limitation**, not a proven contradiction in the actual ADS standard, nor proof that the bounded solver itself returned a wrong result. The published R8 source-index already discloses several of these assumptions; R30 makes the exact false-qualification risk auditable.

## 4. R29 case/mutation adequacy and separation of defects

R29's executed subject is **151e218d638a184a74a59df2cf0ede0f388dea42** × candidate **dac263fa4c0ab155406d2f2117459b34322cc988**, not the later evidence-only experiment tip. R29 receipts state 97/97 Python (0 skipped), 35/35 native cases, 16/16 SMT solver pair checks, 3/3 TLC and native-result-seam probes with 3 forged results BLOCKED plus a green control. Compare 151e218d... to 0a30fb... shows **only** implementation-plan changes and R29 evidence file additions: no touched model, runner, source map or suite input. This review performs **readback, not an invented rerun**.

- Normal CAS/writer/grant examples and their native model mutants are meaningful regression checks of those **specified conditional formulas**; their existence prevents trivially deleting the guarded implication. They do not validate values of independent authorization/write-set/currentness inputs.
- R29's main_v1 negative probes concern (a) TLC foreign model ID, (b) proof-vs-mutation success-status swap, and (c) a legal control. They test inventory/result binding and fail-closed reporting, **not** the above three source-to-Boolean bridges.
- Thus model's scoped safety tests: **not contradicted by identified valuation**; semantic completeness of its assumptions: **NOT_PROVEN**; real normative fault: **NOT_ESTABLISHED**. It would be incorrect to call the 35 cases a complete CAS/Writer source semantics proof, but also incorrect to invalidate their historic exact-subject model PASS.

## 5. Disposition and next admissible proof

**P0=0, P1=0, P2=3 (coverage disclosures, open until actual source-consumer evidence).** No concrete P0/P1 implementation defect in the three scoped model formulas is established by this review; therefore **no speculative model/code repair** and no unnecessary R29 97+35 full rerun. R30 changes only this audit document. Historic R29 evidence and corresponding Exact-SHA remain unmodified; an evidence-only new commit does not claim new native execution.

The shortest useful next step is **one selected, legally authorized real publisher/consumer** after effective project/task pin and native admission authority exist: capture two actual conflicting profile variants with same canonical key; a real writer write-set overlap conflict; and a successor after uncertain terminal/resource publication. Bind original Task Pack + accepted Claim/Event + generation/authority readbacks and the current source SHA, then test only a newly demonstrated false admission or assumption gap. Until this material is available: **REAL_GITHUB_CAS = NOT_RUN; AUTHORIZATION_SOURCE_CURRENTNESS = NOT_PROVEN; WRITE_SET_GROUNDED = NOT_PROVEN; START_RECORD_DURABILITY = NOT_PROVEN; OVERALL_SEMANTIC_EQUIVALENCE = NOT_PROVEN.**

No amendment to formal ADS standards, no new model, no new Gate, no GitHub Actions, no Merge/Freeze/Release, no change to PR #1365.
