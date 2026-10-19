# Agent Task Feedback Metadata — Levels 1–3 Reference

**Status: non-normative examples and consumption guidance; no machine event/schema or new Gate.**
Normative source: [GitHub Agent Interaction Protocol](../standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md), section 10 `Agent completion decision note` and `Task feedback metadata levels and evidence semantics`.
Current source owner: ADS; future collector/evaluator runtime is NOT part of ADS. Consumer need is tracked at [Tally #57](https://github.com/kaicreator-mm/tally/issues/57) (requirement intake only).

## 1. Levels, record shape and exact authority

| Level | Producer / materiality | Durable placement | May decide |
| --- | --- | --- | --- |
| **L1 Task decision note** | Every actually completed Agent Task; failed/blocked/superseded attempts SHOULD report | Append-only Issue comment, or accepted pointer to that exact existing comment | Explain a decision and point to actual results; **not** Gate PASS |
| **L2 reusable learning** | Only when a genuinely reusable engineering lesson was found | Existing Task Learning v1/v2 source/currentness contract, linked from Issue note | Inform future design/validation/ADS Evolution Intake; **not** auto-standard change |
| **L3 evidence-qualified synthesis** | Optional downstream read-only consumer, by cohort and source resolution | Derived report with source refs, coverage, uncertainty, missing data | Propose improvements; **not** overwrite GitHub/Review/Validation or assign Agent permissions |

There is no L1 -> L2 -> L3 stage transition, no new lifecycle, and no requirement to emit a machine object for ordinary work. Project-pinned ADS version and authoritative GitHub/CI refs determine which protocol is effective; a new standard on `main` does not retroactively alter the immutable released tag.

## 2. Level 1 minimum semantic fields

| Field | Meaning / reliable empty value |
| --- | --- |
| `TASK_DECISION_SUMMARY` | `REPORTED` on publication; on failed transport, `NOT_PUBLISHED` is only a visible handoff report, **not** a fabricated GitHub comment |
| `ACTOR` | Self-declared execution role + logical operator id, session reference when known; **GitHub login is transport only** |
| `SUBJECT` | Owning Issue, actual PR / exact 40-hex implementation commit or immutable artifact ref; exact subject is not inferred from a moving branch |
| `DECISION` | Selected design, why it fits authority/constraints, one substantive alternative/trade-off when applicable; no hidden chain-of-thought |
| `EXECUTION` | Encountered failures/ambiguities, diagnosis supported by artifacts and what was actually fixed; `NONE` if none |
| `EVIDENCE` | Actual source / test / CI / independent Review / Host refs, plus exact attempted scope and outcomes; `NOT_RUN` for untouched gates |
| `LIMITS` | Known unproven behavior, remaining risk, deferred external issue ref; `NONE_KNOWN` is not a guarantee of defect freedom |
| **`REUSE`** | Existing function/library/tool/Skill/architecture pattern actually reused, with file or API refs; `NONE` if none used/identified, `UNKNOWN` if not assessed |
| `TASK_LEARNING` | `NONE_MATERIAL` for routine work; otherwise resolvable existing v1/v2 learning ref(s) |

**Minimality:** A single compact comment may combine fields in prose; the field labels make the note discoverable without inventing an `ai-dev:event:v3` or enforcing a new JSON parser. A claim is never independent proof merely because it is well formatted.

## 3. Role-specific optional contributions (never mandatory subforms)

| Role | Useful bounded addition | Real authority stays at |
| --- | --- | --- |
| Builder | `REUSE` (functions/shared helpers), rejected option, source write-set, actual tests, technical debt | Source PR, accepted builder Claim, actual test and merge |
| Reviewer | Review strategy, counterexample attempted, severity/false positive, escaped blind spot | Existing exact-head structured `REVIEW_RESULT` |
| Validator | Executed/aborted/skipped check, environment/tool prerequisites, fault witness, observed behavior | Existing exact-subject validation/evidence and CI/Host result |
| Planner / Architect | L1 evidence/assumption, ADR trade-off, Task split/convergence constraint, downstream unknown | Frozen Product/L2/DAG authority; note does not amend Freeze |

## 4. Compact positive Builder Issue comment (illustrative, not actual PASS)

```text
TASK_DECISION_SUMMARY=REPORTED
ACTOR=Builder; operator_id=agent:builder-example; session_ref=example-session-01
SUBJECT=github:example-org/example-repo#42; PR #46; git:example-org/example-repo@0123456789abcdef0123456789abcdef01234567
DECISION=Reused existing encodeReceipt() instead of adding a second parser; reduces duplication and preserves the current contract. Alternative new parser rejected because two sources of truth would drift.
EXECUTION=Found a null-return edge in the selected helper; added bounded error handling and a targeted negative test. See PR #46 diff.
REUSE=existing packages/core/src/receipt.ts::encodeReceipt; contract: docs/api/receipt.md
EVIDENCE=PR #46 exact HEAD; focused test link with observed PASS; independent Review=NOT_RUN; E3 Host=NOT_RUN
LIMITS=No E3 host/physical integration claim; follow-up github:example-org/example-repo#47 if acceptance requires it
TASK_LEARNING=NONE_MATERIAL
```

The above URLs/SHAs are **illustrative placeholders**, not real evidence. A user of this template replaces them with actual resolvable refs; a missing link makes the *claim* unverified, not PASS.

## 5. Failure or blocked attempt — don't erase adverse evidence

```text
TASK_DECISION_SUMMARY=REPORTED
ACTOR=Validator; operator_id=agent:validator-example; session_ref=example-session-02
SUBJECT=github:example-org/example-repo#48; candidate git:example-org/example-repo@abcdef0123456789abcdef0123456789abcdef01
DECISION=Attempted two-process SQLite CAS witness to challenge idempotency.
EXECUTION=Host has no usable SQLite extension; preflight failed before concurrency test. No implementation fault is established from this event.
REUSE=existing scripts/run_sqlite_probe.sh
EVIDENCE=Host preflight log ref (illustrative), FAILED_ENVIRONMENT; actual CAS witness=NOT_RUN; CI=NOT_RUN; Review=NOT_RUN
LIMITS=No CAS property was proven or disproven; environment repair required before assertion.
TASK_LEARNING=NONE_MATERIAL
```

This is an example of **reported attempt**, not a `COMPLETED` or `PASS` canonical event. The workflow state remains that of accepted GitHub facts.

## 6. Reviewer example: evidence-bearing but no duplicate verdict

```text
ACTOR=Reviewer; operator_id=agent:reviewer-example; session_ref=example-session-03
SUBJECT=PR #51 @ exact current HEAD
DECISION=Compared expectedTargetSequence precondition against both competing writers.
EXECUTION=Found one missing stale-writer rejection; included a reproducible interleaving in the owning structured review.
REUSE=existing concurrency counterexample fixture path/ref
EVIDENCE=exact-head REVIEW_RESULT event ref / finding-id; Host retest=NOT_RUN
LIMITS=Source review cannot claim actual two-process SQLite proof.
TASK_LEARNING=existing v2 record ref only if its root-cause and immutable subject evidence are valid
```

An optional Reviewer note is not a substitute for the canonical `REVIEW_RESULT` findings machine structure.

## 7. Level 2: reusable engineering lessons vs ordinary completion

Record a material finding in the **existing** `task-learning-v2` contract only when independently useful and source-cited, e.g. a repeated null-helper integration defect, a provider-specific CI false-green failure, or a reproducible missing contract. Use the actual schema fields:

- `execution_friction_class`: `workflow_waste`, `missing_contract`, `execution_ambiguity`, `repeated_failure_mode`, `useful_pattern`, `bad_pattern`.
- `root_cause_relation`, `recurrence_refs`, `recurrence_audit_ref`: `SAME`/`RELATED`/`UNKNOWN`/`DIFFERENT` only after resolved audit. Text similarity alone cannot prove common cause.
- `prevention_point_refs`: earliest demonstrably relevant Task Pack/L3, reusable utility, deterministic checker, tool/Skill or policy contract. A prevention candidate is not automatic authority to change a standard.
- `confidence_layers` and `currentness_ref` retain the versioned v2 semantics and immutable exact-source equality.

For routine work with no material transferable lesson, `TASK_LEARNING=NONE_MATERIAL` suffices; do not fabricate a learning object for compliance.

## 8. Level 3: source-qualified measurements and comparison boundaries

Every *derived factual claim* needs a source and epistemic label:

| Evidence label | Example | Limitation |
| --- | --- | --- |
| `OBSERVED` | GitHub PR integrated on exact commit; actual CI run completed FAIL; exact-head Review findings | Does not prove unrelated tests or hidden cases |
| `SELF_REPORTED` | Agent explains choosing existing helper, estimates difficulty, reports "I checked it" without durable test | Agent statement alone does not establish quality or elapsed time |
| `INFERRED` | Retrospective infers recurring root-cause class from several resolved failures | Must cite sources, limits and distinguish from observed event |
| `UNKNOWN` | Token/cost/time/model actuals not instrumented; missing pagination/readback or stale SHA | Never silently substitute zero or a guessed value |

A future report may show *cohort-filtered* metrics only with denominators and observation coverage, e.g. Task kind, role, risk and acceptance difficulty, CI availability, environment/host, required Review policy, measured cost/time and rework/escaped-defect evidence. Separate **defects discovered by a Reviewer** from **defects introduced by a Builder** and independently attributable environment failures. Failure and abandoned attempts remain in denominators, with source limitations; missing observations never imply success or absence of defects.

**Do not** grade/rank or route agents by GitHub account, model/provider marketing name, text verbosity, sheer closes, duration guessed from comments, CI run count or unstratified PASS. An evidence-qualified comparative report must state sample size, comparable cohort, missing proportion, later regression/reopen window and uncertainty; a small or mismatched sample is `INSUFFICIENT_EVIDENCE` for ranking rather than fabricated numerical confidence. Agent identity remains self-declared logical context; actual model identity/cost requires its own trusted source if used.

## 9. Boundary / negative examples

- **No readback:** `I passed all tests` in a comment with no tests/CI -> `SELF_REPORTED`, not observed PASS.
- **Duplicate identity:** Builder and Reviewer share a GitHub transport login but different declared role/operator/session -> preserve distinct actors.
- **Source drift:** Task Learning referring to old SHA stays historical; cannot be credited as current-success evidence for new code.
- **No measured cost:** Token/speed/currency/call totals remain `UNKNOWN`; no default estimates.
- **Mixed cohorts:** A one-line doc patch and a multi-process Host integration must not be ranked as equally difficult successes.
- **No new authority:** Posting the note does not mint/waive gates, mutate the Task DAG, change Frozen Product/L2, supply a new event schema, or initiate a Tally runtime implementation.
