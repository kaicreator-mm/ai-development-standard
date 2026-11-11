# ADS #1366 R31 — Reuse-first real consumer source qualification (Tally v2)

**OUTPUT_LABEL:** `ADS_1366_R31_TALLY_SOURCE_CONSUMER_QUALIFICATION`  
**Kind:** Cross-repository source audit and consumer-feasibility decision, *not* native CAS execution, a newly independent semantic review, or an ADS normative defect.  
**Read subject:** ADS experiment `1d44182ebf90a009d9a17addf18a6b7054a1ee04` (R30 complete); Tally `main@e988321439f65b55936a691c02250b6d62a29409`. Prospective ADS candidate PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` remains OPEN, Product #1347 NOT_FROZEN.

## 1. Why this source was selected (and why it is *not* v4.19 acceptance)

R30 identified three bounded model/source evidence gaps, not model formula counterexamples: (P2-01) actual canonical key and CAS/generation authority; (P2-02) real Task Pack write-set and concurrent Writer disjointness; (P2-03) actual Start Record, compatibility grant and publication/resource reconciliation. Instead of implementing a second ADS controller or adding Boolean SMT assertions, inspected the **existing** GitHub-native Claim producer and Host controller in `kaicreator-mm/tally`.

`tally/main` `.dev-standard/VERSION` is Git blob `27c31b0835075af6c66cc42ea868f1d12dcfd225`: **ADS 4.18.0** at `2c395c55569fe2edf3f4135f12d3d069e526d0b7`. Tally Issue [#125](https://github.com/kaicreator-mm/tally/issues/125) explicitly uses that version and still tracks real native Claim/K effect admission; it is OPEN. No newer v4.19 approved Project/Task pin was established. **Do not promote a v4.18 consumer into prospective v4.19 authority.** This source audit does not write a Claim, exercise an external GitHub POST, or invoke Native tools.

## 2. Concrete source and trust boundaries

| Real source at Tally pinned main | Git blob | Observed capability | What it does **not** prove |
| --- | --- | --- | --- |
| `experiments/v2/t06d-host-claim-publication/single-writer.mjs` | `7df6426ffd0086b7480cf9258ffe1e71d2d15bb5` | `store.put(...mustBeAbsent)` CAS reservation; `store.put(...mustMatchRevision)` publication status; ambiguous GitHub POST remains `PENDING_GITHUB_PUBLISH`; accepts only Host-owned exclusive writer | A deployed single writer, real accepted Task/K permit, nondefault groups or generation greater than one |
| `experiments/v2/t06d-host-claim-publication/host-admission-source.mjs` | `0b493e0cd85769ab654538d2edd7b94bd7bef17e` | Host-bound Task/writer identity, native preflight, two-read reservation registry source; denies incomplete/ambiguous facts | Complete production source-to-GitHub atomicity and actual Task Pack write-set rights |
| `packages/tally-github-native-c/src/task-claim-host-preflight.mjs` | `5b161ee6b5cac22275ce15b09ffb24deb451a580` | Current native Task/dependency/comment candidate read, qualified `nativePreflightReady` | Accepted Claim or CAS; `dispatchSourceBound`/`publisherSourceBound` are false before Host binding |
| `packages/tally-github-native-c/src/task-claim-github-publisher.mjs` | `f895b99fc5a97c69bd0cae56b9365d81791ec927` | Host-selected one-shot `DISPATCH_CLAIMED` structured-event POST, exact GitHub comment readback, fail-closed ambiguous ACK | Accepted Claim, runtime authorization, Host registry persistence, Kernel permit |
| `packages/tally-github-native-c/src/task-claim-host-readback-port.mjs` | `39daecbcf4b421e908e27acb4ddce8dec49f18fa` | Native readback bound to Host reservation, operator, generation, source SHA and comment identity | Source facts by themselves authorizing Task execution |
| `packages/tally-github-native-c/src/task-claim-publication-witness.mjs` | `e1f044d11b079cf107d9e067b1e52d532aa33784` | Read-only exact GitHub comment witness | Durable accepted CAS or Task PASS |

The selected Host controller is **bounded to `__default__`, initial expected generation 0 / reserved generation 1**, and explicitly refuses automatic blind retry of ambiguous publication. That is useful safe behavior for its declared v4.18 slice, but **not** proof of R30's richer current-generation, compatible-group or successor Start Record obligations.

Tests actually present at these exact Tally blobs:

- `single-writer.test.mjs` @ `a98b9053e3674e5c3a5946f7f2826e4c33972da6` uses the public DomainHarness `openSqliteCasStore` in its test harness, asserts exclusion of two simultaneous reservations, persisted restart, no retry after lost ACK and readback rejection; GitHub ports in these cases are **mocks**.
- `host-admission-source.test.mjs` @ `e40ffb2c44194e76780a048ce38a940ba84b6e82` exercises Host authority/source composition, registry checks, native readback refusal and the selected controller using mocked Octokit.
- `task-claim-github-publisher.test.mjs` @ `2d2f76f82144981f5c450771c06d46a394e8181b` mocks GitHub create/getComment; `task-claim-host-readback-port.test.mjs` @ `ae07fe70871566fbecc36c65c2250e4b351d90e7` mocks the native read source.
- These are **test definitions inspected, NOT tests executed in R31**. A source test with a real SQLite adapter does not by itself establish a deployed Host or live GitHub accepted Claim.

## 3. R30 P2 reconciliation against this actual consumer

| R30 ID | Real Tally evidence that can be reused | Remaining source-authority gap | R31 status |
| --- | --- | --- | --- |
| P2-01: CAS key, generation, authorization | Default-group canonical key, one physical CAS reservation, Host-only writer, failure/recovery refusal in source; specific SQLite tests exist | Lawful v4.19 Project/Task pin, live shared serialization and deployed writer currentness, nondefault group and monotonic successor generation | `PARTIAL_SOURCE_REUSE_NO_V419_PROOF` |
| P2-02: Writer write-set | Per protected-Claim-key reservation prevents incompatible identical-key claims within the Host slice | Actual **frozen Task Pack write-set ownership**, disjoint/overlap extraction and concurrent writes from real accepted Builder Claims are absent | `NOT_PROVEN` |
| P2-03: Start Record, Grant and publication | Native comment POST/readback implementation and durable Host reservation *shape* exist; ambiguous transport publication stays pending | Real current grant scope/authority, post-terminal successor, resource reconciliation, accepted canonical Start Record + Host/GitHub durable before/after facts | `NOT_PROVEN` |

No confirmed new ADS normative P0/P1/P2 or bounded model P0/P1. R30's **three evidence/coverage P2 remain open**; no semantic coverage percentage is manufactured. An observed GitHub comment is not a linearizable CAS acceptance or Kernel execution permission.

## 4. Delivery-First disposition

1. **Reuse existing Tally/DH source as a bounded reference**, rather than building another proof-specific Controller, Event Writer or Host. Do not migrate Tally's v4.18 authority to v4.19 by inference.
2. Keep a **single conditional real-consumer acceptance path**: after legitimate effective v4.19 Task/Project pin and selected Host/writer exist, bind real Task Pack, canonical protected key, current generation, real accepted Claim, Native GitHub event and Host reservation before/after, and authoritative write-set. Check R30's three concrete negative controls together with one green control. Repair only a source-demonstrated defect and rerun its affected closure.
3. Until that trigger, **STOP** additional R29 Native runs, generic SMT models, repeated eligibility inventories and unauthorized comment/Claim publication. The expected result for production ADS v4.19 Claim/CAS remains `NOT_PROVEN`, not synthetic PASS.
4. The correct evidence owner for actual Tally Host currentness is the owning Tally issue/project; this ADS experiment only tracks the cross-model implication. Tally Issue #125 is OPEN and does **not** qualify a new external production permit.

**Execution boundary for R31:** Direct GitHub API source-tree, issue, file/version and source-test readback only. Python/Node/Native tools, live GitHub mutation and independent reviewer execution: `NOT_RUN`. The R29 97/97 + 35/35 are retained at their historical exact subject, not rerun or promoted.
