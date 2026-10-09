# U02 Closeout — lost-ACK external effect across Agent successor (#949)

## Terminal verdict

```
PASS
```

Overall evidence target **E2** (real internal integration + observable
persistent effect boundary) met; the E2/E3 process-death sub-claim is
supported at **E3** (real hard kill + persistent reopen). This is an
architecture evidence demo, not a feature; it does not qualify v4.11
P1/P2/P3/Hidden/RQ and authorizes no v4.10/main change.

## Tested identity

- Branch: `research/v4.11.0-u02-effect-handoff`
- Baseline (per Issue): `8737240ec52faf595f8d1697fdd7ec581d87cb8f` (L2 candidate #948)
- Tested HEAD: branch tip at review time (harness commit `1ec04df`; docs-only commits on top do not change the harness blobs below)
- Tested tree: `a0f2ca5a726afcce60e83a389b2388bb267e4e8f`
- Harness blobs:
  - `cd8def6cb420e233f02c7c6c964d9f9fa623248b` `tests/architecture-v411-u02/run_experiment.py`
  - `1a89727bed52010cbf0a3338087b8272cbcab549` `tests/architecture-v411-u02/u02/actor.py`
  - `fd657f4ae248c70bf8f9f4c1ccb2a009bef14c9a` `tests/architecture-v411-u02/u02/authority.py`
  - `570de24ea547bab192edba81e821665a2e602c75` `tests/architecture-v411-u02/u02/plane.py`
  - `ae2ba60e71f707f5fec35f4f9503f9b39bf5f728` `tests/architecture-v411-u02/u02/sink.py`
  - `56ab1747938a44fc947b87207c24103d34ce6cc1` `tests/architecture-v411-u02/u02/guard.py`
  - `2ae48ad4c74be3e66288abbad46f5b26d6c71bcd` `tests/architecture-v411-u02/u02/events.py`

## Toolchain / platform

- Windows 10.0.26200 x64 (win32), Git Bash shell
- Python 3.14.6 (`C:\Python314\python.exe`)
- git 2.52.0.windows.1
- No network, no GitHub writes, no CI; Local Build Host only.

## Commands

```bash
cd tests/architecture-v411-u02
U02_RUNTIME_ROOT=/d/xDev/_tmp/ads-i949-u02-research/runtime python run_experiment.py
```

Executed twice on fresh runtime roots; both runs `TERMINAL: PASS`
(evidence: `<runtime-root>/evidence.json`). Clean-checkout repeatability:
the harness creates all runtime state itself; a fresh clone of the branch
plus the command above reproduces the run.

## Actual counters (second run, evidence.json)

| Case | Plane HEAD after case | Real sink count | Key observations |
| --- | --- | --- | --- |
| E1 | `da19e600…` | 1 | B decision `COMMITTED_ALREADY`, `may_mutate=false` |
| E2 | `0ac9afd8…` | **1** | hard kill rc=1, no RESULT publication; B early `BLOCKED_DUPLICATE_CLAIM`; after durable TIMEOUT release B `RECONCILED_COMMITTED`; ledger sha256 `3de1a56d…` observed at kill |
| E3 | `2c954186…` | 1 | killed pre-mutation (count 0); blind B `BLOCKED_OUTCOME_UNKNOWN`; grounded B `RECONCILED_NOT_COMMITTED` → fresh claim `ACCEPTED` → exactly one mutation |
| E4 | `457671d6…` | 1 | concurrent B/C: B `ACCEPTED` (generation 2), C `BLOCKED_STALE_HEAD` (observed HEAD `00da803d…` vs current) |
| E5 | `ebd8a082…` | 0 | `REVIEW_DECISION` status=FAIL by `human:owner` exact-current; B `BLOCKED_DENIED`, never reached admission |
| E6 | `abd8456d…` | 0 | stale HEAD `ffff…` → `BLOCKED_STALE_HEAD`; forged event rejected at writer seam: `field dispatch_state not in enum: CLAMED`, plane HEAD unchanged; tenant B → `BLOCKED_TENANT` |
| E7 | `8665c440…` | 1 | adapter dedup: raw same-identity retry `deduplicated=true`; authority `COMMITTED_ALREADY` |
| E8 | n/a (`.git` destroyed) | 0 | broken plane → `BLOCKED_UNVERIFIED`, no admission; empty effect identity → `BLOCKED_NO_EFFECT_IDENTITY`, no ledger line |

Fail-path traces (negative logs) are captured per case in
`<runtime-root>/evidence.json` under `cases.<E>.outcome`, including killed
process return codes, rejected-forgery text, and every decision JSON.

## What was proven

1. **The U02 hypothesis holds on real seams.** With one authorized
   non-idempotent mutation and a lost ACK after a possibly-committed write,
   a distinct successor consuming current canonical lineage (real git HEAD
   generation + schema-validated event log) plus a real readback of the
   effect boundary did not repeat the mutation: the real observable effect
   counter stayed **1** in every blocked-successor scenario (E2, E3, E4).
2. **Externally-grounded reconciliation is the license to act.** When the
   real sink readback proves the effect committed, the successor records
   the committed outcome without mutating (E2 `RECONCILED_COMMITTED`); when
   it proves absence after durable release, exactly one legal attempt
   follows (E3). Timeout/lineage alone converts nothing:
   `BLOCKED_OUTCOME_UNKNOWN` (E3).
3. **No second state owner is required.** Claim admission is a serialized
   single-writer CAS over the existing git fact plane; durable TIMEOUT
   release + append-only history gave correct successor attribution (E2-E4)
   with no new lifecycle or state database.
4. **Adversarial inputs fail closed.** Exact-current human DENY (E5),
   stale HEAD (E6), schema-forged writer instruction rejected at the real
   writer seam (E6), tenant/environment change (E6), broken plane (E8) and
   missing effect identity (E8) all blocked with no mutation and no false
   proof.
5. **Proven dedup is real enforcement.** The adapter itself refuses a
   duplicate effect identity (E7): a retry that bypasses authority still
   cannot increment the persistent count.
6. **Real process death.** E2/E3 actors were hard-killed
   (`TerminateProcess`, returncode 1, no outcome publication) and the
   successor reopened all state from durable storage in a fresh process.

## What was NOT proven

- Real GitHub/GitHub-API durability semantics (local git only; no network).
- Behavior under real network partition/partial fsync failure modes of a
  remote GitHub plane.
- Exactly-once delivery (explicitly out of scope; not assumed anywhere).
- Concurrency beyond two simultaneous claimants; clock skew; multi-host
  admission writers.
- Production task qualification: this demo does not qualify v4.11 gates and
  creates no runtime obligation.
- The `effect_id` additive event field is demo wiring, not a proposed
  schema change; normative placement remains with the L2 reviewer.

## Architecture implication

**KEEP** the owner/event authority architecture as-is: durable Claim +
Dispatch lineage on the existing git fact plane, fail-closed UNKNOWN until
an externally-grounded reconciliation (real effect-boundary readback),
human DENY precedence, and serialized single-writer admission are
sufficient to prevent duplicate non-idempotent external writes after a
lost ACK — no second state owner, no new event family, no new runtime.

**ADAPT** (documentation-level, at L2 discretion): state explicitly in
EXTERNAL_SYSTEM_EXECUTION_STANDARD §10 / EXECUTION_ARCHITECTURE §27.4
guidance that "unsafe retry" resolution requires an *externally-grounded*
readback of the effect boundary (not timeout inference), and that blocked
successor retry is the default until such reconciliation or authorized
compensation is exact-current. This is wording clarification of existing
authority, not a new mechanism.

**DROP** nothing.
