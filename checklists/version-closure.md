# Version Closure Checklist

Version Closure evaluates one dependency-complete candidate. PR PASS is not Release PASS.

## Authority / Scope

- [ ] Frozen PRD/scope and Architecture/Contract identified.
- [ ] Task DAG terminal or every deferred item has explicit non-blocking authority/rationale.
- [ ] Every mandatory release gate traces to Gate Authority.
- [ ] No historical workflow/Agent guess silently created a blocker.

## Candidate / Visible Closure

- [ ] Candidate SHA **and tree SHA** recorded.
- [ ] Required concern/integration work is merged.
- [ ] Full required visible regression passes on the intended candidate.
- [ ] Required Critical Journeys/platform/production build/package/install/external boundary tuples are explicit and truthful.
- [ ] CI/profile requirement is satisfied or its infrastructure exception/alternate-executor basis is valid.
- [ ] Candidate Freeze occurs only after required visible freeze gates pass.

## Freeze Integrity

- [ ] Freeze record includes SHA/tree/ref/visible evidence/pinned standard.
- [ ] Declared candidate ref still equals frozen SHA and tree before Hidden Validation.
- [ ] No post-freeze candidate mutation occurred; if it did, freeze was explicitly thawed/invalidated and successor evidence rebuilt.

## Hidden Validation

- [ ] Required Hidden Validation targets the frozen candidate.
- [ ] Private pack identity/revision/checksum is recorded without exposing private fixtures.
- [ ] Any release-significant defect discovered after a prior Hidden PASS is classified and its Hidden-pack blind spot is dispositioned.
- [ ] Pack defects are distinguished from product defects.

## Documentation / Reconciliation

- [ ] README/docs/config/migration guidance matches shipped behavior.
- [ ] Architecture amendments reconcile shipped implementation without rewriting historical decisions.
- [ ] Known limitations/deferred items are explicit.

## Release Qualification

Choose exactly one:

- `READY`
- `CONDITIONAL`
- `BLOCKED`
- `FAIL`

- [ ] Verdict explains the supporting/unsatisfied facts.
- [ ] No NOT_RUN/BLOCKED/old-SHA evidence was converted into PASS.

## Repository Integration

After READY:

- [ ] Re-read live candidate/main refs.
- [ ] Integrate version → main without introducing unqualified content.
- [ ] Record integration method, final main SHA/tree and canonical validated candidate SHA/tree.
- [ ] Verify required tree/content equivalence or final-main sanity.
- [ ] Record immutable final baseline SHA.
- [ ] Tag/GitHub Release status recorded if used; tag is optional and never replaces commit identity.

## GitHub State

- [ ] Issues/milestone/current state match actual completion.
- [ ] No active stale dispatch remains for completed release work.
- [ ] Release evidence is recoverable without chat history.
