# T-013 Implementation Map

Builder writes only:

1. `docs/implementation/4.8.0/dogfood/evolution/EVIDENCE_MATRIX.json`
   - structured per-stream/per-scenario evidence rows;
   - minimum two materially distinct real streams; use all three preflight streams when still available/current enough for historical analysis;
   - exact source refs, classification, currentness, privacy/publication and external-claim eligibility are mandatory.

2. `docs/implementation/4.8.0/dogfood/evolution/EVOLUTION_DOGFOOD_REPORT.md`
   - summarize classifications, counterevidence and repeated-friction analysis;
   - distinguish PROJECT_DEFECT / ENVIRONMENT_OR_TOOL / AGENT_OR_EXECUTOR / EVIDENCE_GAP / STANDARD_FRICTION_CANDIDATE;
   - conclude only `NO_CHANGE`, `MORE_EVIDENCE`, or a justified ordinary-governance candidate handoff.

3. `docs/implementation/4.8.0/dogfood/evolution/VALIDATION_HANDOFFS.md`
   - list every external/real claim that remains NOT_RUN/BLOCKED and the exact evidence needed;
   - empty is allowed only if no such claim is made.

Read-only starting streams from preflight:
- ADS T012/#469 historical bounded-agent dogfood;
- domain-ux #162 / PR #161 historical independent review evidence;
- runx PR #143 historical build/security review evidence.

Re-read live dispositions before using them. Historical verdicts never transfer to successor SHAs.
