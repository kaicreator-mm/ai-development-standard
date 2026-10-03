# T-012 Implementation Map

## Authorized Builder outputs

The Builder writes only under:

```text
docs/implementation/4.8.0/dogfood/469/**
```

Expected durable outputs are:

### `EVIDENCE_MATRIX.md`

Create the BDF-01..BDF-12 evidence matrix and source-task rows where evidence exists. Material factual claims must carry exact source refs. Keep `0`, `NONE_REPORTED`, `NOT_REPORTED`, `NOT_MEASURED`, `NOT_APPLICABLE` and `BLOCKED` distinct.

The matrix must separate source-reported observations from T-012's own Builder observations and from future independent Validation/Fresh Review.

### `EXECUTION_OBSERVATIONS.md`

Record only the actual T-012 Builder execution facts: exact base and Pack identities, Builder execution profile/provider-model provenance when available, F1 freedom, clarifications/escalations, edit/test loops, negative-oracle findings, write-set drift catches, source/base rebinds and resource/time/tokens/cost only when observed.

Leave T-012 independent Validation and Fresh Review as pending. Do not self-certify.

### `RESULT.md`

Synthesize what the exact evidence supports and does not support, counterevidence/Review value, comparability gaps and one allowed evidence-governance disposition:

```text
MORE_EVIDENCE
NO_CHANGE
ADS_EVOLUTION_CANDIDATE
```

If the exact evidence lacks a comparable measured economic methodology, include `ECONOMIC_SAVINGS=NOT_MEASURED` verbatim. Any evolution candidate remains non-normative and routes through ordinary ADS governance.

## Read-only authority/reference inputs

- `docs/implementation/4.8.0/PRD.md`
- `docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md`
- `docs/implementation/4.8.0/TASK_DAG.md`
- `docs/implementation/4.8.0/task-packs/T12_469_bounded_agent_dogfood.md`
- `docs/implementation/4.8.0/L3_T12_469_BOUNDED_AGENT_DOGFOOD.md`
- #469 historical/current dogfood comments, with planning anchor `5925124956`
- T-004/#511, T-007/#513 and T-008/#514 completion/evidence
- `standards/EXECUTION_PACK_STANDARD.md`
- `standards/MODEL_USAGE_POLICY.md`
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md`
- `standards/VALIDATION_STANDARD.md`

These are inputs, not T-012 Builder write authority.

## Builder sequence

1. Re-read live `version/v4.8.0`; require exact base `257e95531551960cb163a3e20ab2b3d13f415d3c`.
2. Re-read #518 native dependency summary; require `blocked_by=0,total_blocked_by=3` and #511/#513/#514 DONE.
3. Confirm Task Pack blob `10168f6ea2a1cb3b0ffff9c1a493b0904d82942f`, L3 blob `82f0ac808f423d861c030413046c2b2e689bfc1d`, branch and six core Execution Pack files match.
4. Re-read #469. If a material successor exists after planning anchor comment `5925124956`, do not author result content; publish a blocker requesting evidence-currentness rebind.
5. Confirm the accepted Builder dispatch/claim grants F1 or narrower freedom and the executor is hard-eligible for the role. Do not infer eligibility from provider/model name.
6. Materialize `EVIDENCE_MATRIX.md`, `EXECUTION_OBSERVATIONS.md` and `RESULT.md` only in the authorized directory.
7. Run and record:
   - `git diff --check <PACK_HEAD>...HEAD`
   - `git diff --name-only <PACK_HEAD>...HEAD`
   - `python -B scripts/verify_standard.py`
8. Verify the changed-path list is entirely under `docs/implementation/4.8.0/dogfood/469/**`.
9. Publish Builder terminal with exact base, Pack HEAD/tree, candidate HEAD/tree, source anchor/currentness result, exact diff, BDF coverage and observed T-012 measurements. Do not claim independent Validation or Fresh Review.
10. Hand the exact candidate to a distinct independent Validator. Only after qualifying Validation may a genuinely Fresh Independent Reviewer begin.

## F1 implementation choices

Allowed discretion:

- Markdown table layout and concise wording;
- grouping of exact source refs where traceability remains explicit;
- adding one small evidence-supporting file under the authorized directory if it reduces ambiguity;
- ordering of source rows while BDF-01..BDF-12 remain complete.

Not discretionary:

- source identities/statuses/currentness;
- measurement null semantics;
- F1 freedom ceiling;
- Builder/Validator/Reviewer independence;
- Builder write set;
- economics/comparability threshold;
- no blanket strong→low-cost rule;
- provider/model provenance boundary;
- ordinary governance requirement for any proposed standard change.

## Stop boundaries

Stop rather than continue when:

- repository or source-evidence currentness fails;
- a material source claim is ambiguous or unsupported;
- the Builder would need to infer missing measurements;
- a path outside the write set is needed;
- a normative ADS edit appears necessary;
- a universal routing/economic conclusion is required to make the report look positive;
- the F1 Builder encounters an authority/comparability question requiring stronger semantic judgment.

T-014 is outside this Execution Pack and remains not started in this phase.
