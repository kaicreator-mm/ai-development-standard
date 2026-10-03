# T-013 Independent Validation Handoffs

Status: **PENDING_INDEPENDENT_VALIDATION**

These handoffs are deliberately separate from Builder evidence. The Builder must not self-validate or self-review.

## H1 — Exact candidate and source currentness

**Required validator action**

1. Re-read the candidate PR HEAD/tree/base and confirm the diff is limited to:
   - immutable `.agent/execution/T-013/**` JIT planning files; and
   - the three authorized Builder paths under `docs/implementation/4.8.0/dogfood/evolution/`.
2. Confirm Task Pack blob `9b96b567e8b0fec23cab08502f5dd9a907c4ef59` and L3 blob `8af06fd5bd7237b260fe478c23cb410c0e15898f` remain the governing references or identify an explicit successor rebind.
3. Re-read all three REAL source streams at Validation time:
   - ADS `#469`, including durable anchor `#469@5925124956` and live Issue disposition;
   - domain-ux predecessor `#162@5970478893`, repair/supersession lineage, successor `#168@5973293956`, and live PR `#161` merged identity;
   - runx predecessor `#143@5953993544`, supplementary Linux evidence `#143@5953859464`, final review `#143@5958381492`, and live PR `#143` merged identity.
4. Fail closed if any predecessor verdict is presented as current truth for a successor SHA.

**Pass oracle:** every matrix identity/currentness statement is exact or explicitly historical; no verdict transfer occurs.

## H2 — Privacy, publication, and strongest eligible evidence

**Required validator action**

- Confirm private project streams are only minimally referenced and no secret, credential, private chain-of-thought, Hidden payload, raw private project evidence, or unnecessary code detail has been copied.
- Confirm repository/GitHub visibility is not treated as `PUBLISHABLE`.
- Confirm every stream currently has `external_claim_eligible=false`.
- Confirm the report makes no external/generalized claim stronger than the strongest eligible REAL evidence.

**Pass oracle:** privacy/publication classification fails closed and no external claim is silently authorized.

## H3 — Economic/performance/routing claims

```text
STATUS=NOT_RUN|BLOCKED
REASON=no comparable controlled strong-vs-lower-cost token/cost/latency/rework baseline in the rebound evidence
```

A future claim of cost saving, latency saving, rework reduction, or blanket model routing requires comparable measured REAL evidence with exact task class, environment/runtime, executor/profile, baseline, and independent gate identities. S1 alone does not satisfy this.

**Validation rule:** absence of this evidence is not a T-013 failure because the report makes no such claim; it must remain an explicit blocked future claim.

## H4 — Future ADS evolution candidate

```text
STATUS=NOT_RUN|BLOCKED
CURRENT_CANDIDATE=NONE
```

Before an `ADS_EVOLUTION_CANDIDATE` can be produced from this evidence family, a future intake must show repeated materially similar friction across at least two distinct REAL project/task streams **after** rejecting:

- project implementation/security defects;
- environment/tool limitations;
- Agent/executor mistakes;
- evidence-coverage/currentness gaps;
- one-off provider/model observations.

The candidate must identify the ADS-owned semantic/process owner, preserve counterevidence, and enter ordinary ADS Intake/Governance. It must not mutate Frozen Product/L2/DAG or normative owners from dogfood evidence.

## Required independent Validation terminal

At minimum, the independent validator should durably report:

```text
V48_T013_CROSS_PROJECT_VALIDATION=PASS|FAIL|BLOCKED
VALIDATED_HEAD=<exact sha>
VALIDATED_TREE=<exact tree>
VALIDATED_BASE=<exact version/v4.8.0 sha>
WRITE_SET=PASS|FAIL
REAL_STREAM_COUNT=<n>
SOURCE_CURRENTNESS=PASS|FAIL
PREDECESSOR_VERDICT_TRANSFER=NONE|FAIL
EVIDENCE_STRENGTH=PASS|FAIL
FALSE_POSITIVE_REJECTION=PASS|FAIL
PRIVACY_BOUNDARY=PASS|FAIL
PUBLICATION_BOUNDARY=PASS|FAIL
EXTERNAL_CLAIM_BOUNDARY=PASS|FAIL
ECONOMIC_OVERCLAIM=NONE|FAIL
REPEATED_STANDARD_FRICTION=ESTABLISHED|NOT_ESTABLISHED
ADS_EVOLUTION_CANDIDATE=<ref|NONE>
TASK_DISPOSITION=NO_CHANGE|MORE_EVIDENCE|ADS_EVOLUTION_CANDIDATE
BUILDER_VERIFIER=<PASS evidence ref|FAIL|NOT_RUN>
NEXT=FRESH_INDEPENDENT_REVIEW|BOUNDED_REPAIR|BLOCKED
```

Fresh Review must use a genuinely new reviewer/session and the exact same validated candidate HEAD. `PR PASS != Release PASS`.
