# Version Closure Checklist

Version Closure evaluates one dependency-complete candidate. PR PASS is not Release PASS.

## Authority / Scope

- [ ] Frozen PRD/scope and Architecture/Contract identified.
- [ ] Task DAG terminal or every deferred item has explicit non-blocking authority/rationale.
- [ ] Every mandatory release gate traces to Gate Authority.
- [ ] No historical workflow/Agent guess silently created a blocker.
- [ ] Applicable v4.1 execution-foundation owners are identified for material dependency/toolchain, config/secret, workspace/artifact and external-system facts; Execution Context is treated only as a non-authoritative projection.

## Candidate / Visible Closure

- [ ] Candidate SHA **and tree SHA** recorded.
- [ ] Required concern/integration work is merged.
- [ ] Full required visible regression passes on the intended candidate.
- [ ] Required Critical Journeys/platform/production build/package/install/external boundary tuples are explicit and truthful.
- [ ] Where material to this Product/project, verify evidence is referenced from `standards/BUILD_ARTIFACT_GOVERNANCE_STANDARD.md` for exact build/promoted artifact identity, `standards/DISTRIBUTION_GOVERNANCE_STANDARD.md` for optional publication binding, and `standards/DEPLOYMENT_GOVERNANCE_STANDARD.md` for distinct Plan/executed Result and side-effect authority. Do not manufacture any of those records for genuinely non-applicable stages or replace unexecuted real host/provider proof with fixture/CI success; see `docs/implementation/4.4.0/MIGRATION_ADOPTION.md` for adoption mapping.
- [ ] Dependency/toolchain certification, configuration identity, artifact identity and external environment/fidelity facts match the actual closure subject where material.
- [ ] Secret values are absent from ordinary closure evidence; durable evidence uses authorized refs/identity.
- [ ] Build outputs/caches/runtime state are not promoted to Release artifacts by file existence alone.
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
- [ ] Execution Foundation adoption/profile documentation matches what the integrated candidate actually uses; non-applicable machine contracts were not created merely for ceremony.

## Release Qualification

Choose exactly one:

- `READY`
- `CONDITIONAL`
- `BLOCKED`
- `FAIL`

- [ ] Verdict explains the supporting/unsatisfied facts.
- [ ] No NOT_RUN/BLOCKED/old-SHA evidence was converted into PASS.
- [ ] Dependency risk exceptions, external-system availability and local workspace state were not treated as Release PASS authority.

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
