# U02 — lost-ACK external effect across Agent successor (Issue #949)

Stage-2 architecture research demo, evidence target **E2** (with one E3
sub-claim: real OS-process hard kill + persistent reopen, see E2/E3 below).

## Hypothesis (from Issue #949)

IF Agent A issues one authorized non-idempotent external mutation with unique
effect/subject identity and the ACK is lost after the mutation may have
committed, THEN Agent B consuming current canonical Work/Dispatch/Claim/
authority lineage must NOT issue a second unsafe mutation unless
externally-grounded reconciliation, proven dedup/idempotency, or authorized
compensation has been completed and is exact-current. Under blocked successor
retry the real observable effect counter remains 1 and the attempted
duplicate is rejected/blocked.

## Feasibility verdict

NOT `BLOCKED / MISSING_PRODUCTION_SEAM`. The existing seams suffice:

- **Durable fact plane**: a git repository is the existing supported fact
  plane (EXECUTION_ARCHITECTURE_STANDARD §27.4 reuses "the existing
  GitHub/repository fact plane"). The harness instantiates it as a real
  local git repo; HEAD SHA is the exact-current generation.
- **Supported event path**: payloads are `ai-dev/event-v2` comments
  validated by the repository's own schema
  (`schemas/agent-event-v2.schema.json`) and its own validator from
  `scripts/test_v48_execution_ownership.py` (real lineage, not a copy).
  `effect_id` on the DONE `DISPATCH_STATE_CHANGED` is a demo-additive field
  (schema allows additional properties; same pattern as the T-017 additive
  fields) and is never a substitute for the real sink readback.
- **Claim semantics**: SINGLE_WRITER_ADMISSION claim admission, durable
  terminal release, NO_CLAIM_NO_EXECUTION — exercised against real git, not
  an in-memory oracle.
- No new permanent runtime was written; the harness lives entirely in the
  Issue-authorized research/test paths.

## Real Under Test / Deterministic Fakes

**Real:**

- real local git repository: real objects, commits, HEAD SHA readback;
- real schema-validated event writes through the writer seam (forgery is
  rejected at the seam, not in a mock);
- real append-only file sink ledger: the actual write boundary, persistent
  mutation count, per-mutation sequence and effect IDs;
- real, separately launched OS processes per actor (distinct
  `operator_id` + `session_ref`); E2/E3 hard-kill the actor process
  (`TerminateProcess`, returncode 1, no RESULT publication) between the
  sink commit and the outcome event;
- fresh-process durable readback by the successor (new process, new file
  reads, new `git rev-parse`).

**Deterministic fakes:** the external system behind the sink is a local
file adapter (explicitly authorized by the Issue). LLM responses are not
used. Clock is wall time (only ordering matters).

**Intentionally NOT tested:** real GitHub API writes (kept local per Issue;
Local Build Host is appropriate); network partitions; multi-host git
remotes; exactly-once delivery (explicitly not assumed).

## Cases

| Case | Result |
| --- | --- |
| E1 positive baseline | A claim → effect → outcome published; B sees `COMMITTED_ALREADY`; counter 1 |
| E2 uncertain ACK (hard kill) | A effect commits in sink, process hard-killed pre-publication; B blocked while claim active (`BLOCKED_DUPLICATE_CLAIM`); after durable TIMEOUT release B reconciles via real readback (`RECONCILED_COMMITTED`); **counter stays 1** |
| E3 uncertain, not committed | A killed pre-mutation (counter 0); B blocked while claim active; after release, B-from-timeout-alone is `BLOCKED_OUTCOME_UNKNOWN` (no attempt); grounded B (real readback proves absent) re-claims and executes exactly once (counter 1) |
| E4 concurrency | B/C claim concurrently from the same observed HEAD; serialized admission: exactly one `ACCEPTED`, one `BLOCKED_STALE_HEAD`; winner effects once; counter 1 |
| E5 denial | owning human `REVIEW_DECISION` DENY is exact-current; B blocked (`BLOCKED_DENIED`) despite readiness; counter 0 |
| E6 stale/untrusted/forged | stale observed HEAD → `BLOCKED_STALE_HEAD`, plane untouched; forged schema-invalid event rejected at the writer seam (`PlaneError`), HEAD unchanged; changed tenant → `BLOCKED_TENANT`; counter 0 |
| E7 explicitly idempotent | adapter with proven effect-ID dedup: raw retry with same identity is refused by the adapter (`deduplicated=true`, counter stays 1); authority layer sees durable record (`COMMITTED_ALREADY`) |
| E8 invalid/broken proof | destroyed `.git` → `BLOCKED_UNVERIFIED`, no admission, no mutation; missing effect identity → adapter refusal `BLOCKED_NO_EFFECT_IDENTITY`, counter 0 |

## Run

```bash
cd tests/architecture-v411-u02
python run_experiment.py                 # all cases E1-E8
python run_experiment.py --case E2       # single case
```

Runtime state (fact-plane repos, sink ledgers, evidence.json) is written
under `U02_RUNTIME_ROOT` (default: fresh temp dir). Example:

```bash
U02_RUNTIME_ROOT=/d/xDev/_tmp/ads-i949-u02-research/runtime \
  python run_experiment.py
```

Each run deletes and recreates per-case directories; two consecutive full
runs produced `TERMINAL: PASS` for all eight cases.

## Layout

- `run_experiment.py` — orchestrator: scenarios, direct counter assertions,
  evidence collection (`evidence.json` per runtime root).
- `u02/plane.py` — real git fact plane (append + commit, admission lock,
  fail-closed readback, Windows-safe file mapping for `:` in work keys).
- `u02/sink.py` — persistent append-only effect ledger (real count, effect
  IDs, optional adapter-enforced dedup, tenant refusal).
- `u02/authority.py` — the decision logic under test (fail-closed successor
  decision from exact-current durable facts).
- `u02/actor.py` — actor process CLI (claim / effect / resume), one real OS
  process per invocation.
- `u02/events.py` — schema-conformant event payload builders.
- `u02/guard.py` — event validation via the repo's own v48 validator.

Closeout: `docs/experiments/v4.11-u02/CLOSEOUT.md`.
