# T-013 Review Checklist

## Exact subject / write set
- [ ] Candidate PR HEAD/TREE/base are exact and current.
- [ ] Diff is limited to the three Builder paths declared in MANIFEST plus immutable `.agent/execution/T-013/**` planning files.
- [ ] Task Pack blob `9b96b567e8b0fec23cab08502f5dd9a907c4ef59` and L3 blob `8af06fd5bd7237b260fe478c23cb410c0e15898f` remain current or have an explicit successor rebind.

## Evidence quality
- [ ] At least two materially distinct REAL streams are represented with exact durable identities.
- [ ] Historical source verdicts are not transferred to successor SHAs.
- [ ] Evidence rows contain required provenance/currentness/environment/privacy/publication fields.
- [ ] `external_claim_eligible` never exceeds the strongest eligible REAL evidence.
- [ ] Synthetic evidence, if any, remains explicitly synthetic and cannot satisfy real-world claims.

## False-positive / governance boundaries
- [ ] Project/environment/Agent/evidence-gap defects are not automatically promoted to STANDARD_FRICTION.
- [ ] `NO_CHANGE` and `MORE_EVIDENCE` are preserved as successful bounded outcomes.
- [ ] T012 economics remain NOT_MEASURED unless comparable eligible evidence actually exists.
- [ ] Any ADS evolution candidate is only a handoff into ordinary ADS Intake/Governance; no self-amendment occurs.
- [ ] No Product/L2/DAG/normative owner mutation is present.

## Privacy / external claims
- [ ] Public visibility is not conflated with PUBLISHABLE authorization.
- [ ] No secrets, private chain-of-thought, Hidden payloads or private project evidence are copied.
- [ ] Every unavailable required real/external validation is recorded as NOT_RUN|BLOCKED with an explicit handoff.

## Gates
- [ ] Builder verifier evidence is present but not treated as independent Validation.
- [ ] Independent exact-subject cross-project currentness/privacy/evidence-strength Validation PASS exists.
- [ ] Genuinely Fresh Independent Review occurs only after Validation PASS on the same exact HEAD.
