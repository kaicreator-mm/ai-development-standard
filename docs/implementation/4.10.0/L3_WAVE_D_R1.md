# v4.10.0 L3 Wave D R1

Status: JIT implementation evidence for `V410-T04B` only.

Authority: Frozen Product #837; Frozen L2 #842; refined DAG Freeze #848; Task Pack R1 `V410-T04B`; integrated predecessors #856/T04A and #853/T02B; Web preplan #857@6001258854; partial rebind #857@6002219747.

## V410-T04B — Review finding / aggregation / currentness convergence

### Tests

Positive:
1. Current-subject `REVIEW_RESULT` findings are machine-reconstructible with stable finding identity, severity, root-defect class and evidence/provenance reference.
2. Current aggregate is derived only from accepted Review facts bound to the live exact candidate subject.
3. Multiple reviewers preserve provenance and converge duplicate/same-root findings without model-count authority.
4. Root-defect classification binds to integrated T04A repair-routing vocabulary; T04B does not create a second repair lifecycle.
5. Integrated T02B causality/responsibility projection composes without redefining Review authority.

Negative:
1. Findings/verdicts on stale HEAD remain historical and are excluded from the current aggregate.
2. Conflicting current-subject verdicts/classifications fail closed; majority/model count cannot manufacture PASS.
3. Missing/ambiguous finding identity, severity or root-defect class cannot be guessed into a current authoritative aggregate.
4. Cost, speed, file count, docs-only appearance, model confidence or provider brand cannot waive required Review or change verdict authority.
5. No new Review event family, workflow/state dimension, scheduler, registry or Validation/Release authority may be introduced.

### Contract / invariants

- Review currentness is exact-subject.
- `Evidence != Verdict != Authority` remains true.
- Material findings have stable identity, severity, root-defect classification and evidence/provenance sufficient for deterministic reconstruction.
- Current aggregation consumes only current-subject accepted durable facts; stale evidence remains immutable history.
- Conflicts/ambiguity fail closed; event order and reviewer/model count create no authority.
- Root-defect classes are consumed from integrated T04A; repair routing/escalation remains owned there.
- T02B fields (`parent_dispatch_ref`, `responsibility_mode`) are consumed only as integrated same-family provenance/causation facts where relevant; they do not create Review authority.

### Implementation seam

Primary owner-local seam:
- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` Review execution/event invariants.
- Existing `REVIEW_RESULT.findings` machine shape in `schemas/agent-event-v2.schema.json` only where deterministic finding reconstruction requires additive structure.
- Existing directly-owned review/finding templates or focused tests only if materially required.

Do not rewrite `standards/DEVELOPMENT_WORKFLOW.md` or `standards/VALIDATION_STANDARD.md`; consume integrated T04A semantics. Do not introduce a second Review lifecycle or central manifest wiring (reserved for T06A/T06B).

### Failure handling

- Stale subject -> exclude from current aggregate and require applicable successor Review; never transfer PASS.
- Conflicting/ambiguous current facts -> fail closed; no majority vote.
- Repeated unresolved root defect -> durable finding evidence + route to integrated T04A escalation; no universal retry count.
- Owner/schema drift or semantic conflict with integrated T02B -> stop and return to Controller for L3/JIT rebind.
- Need for new semantic owner/event/state family -> architecture contradiction; stop rather than widen scope.

### References

- Frozen Product #837 / `docs/implementation/4.10.0/PRD.md`
- Frozen L2 #842 / `docs/implementation/4.10.0/L2_ARCHITECTURE_EVIDENCE.md`
- refined DAG Freeze #848
- `docs/implementation/4.10.0/TASK_PACKS_R1.md#V410-T04B`
- #856 / PR #884 integrated T04A
- #853 / PR #887 integrated T02B
- #857 Web JIT Pre-Plan R1 + Partial Rebind R2
