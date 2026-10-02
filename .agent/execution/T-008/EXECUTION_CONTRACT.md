# T-008 Execution Contract — Cross-standard Conformance / Closure Inputs

## Exact authority binding

This pack is subordinate to Frozen Product, Frozen L2, Frozen Task DAG, T08 Task Pack and L3. It is bound to:

```text
TASK=#311 / T-008
CONTROLLER=#580
INTEGRATION_TARGET=version/v4.6.0
BASE_SHA=a4c5fffe6bab178dcb74b5f47afcda4aa0047c27
BASE_TREE=6ae5e1a8b33a6127ecc2e94b6db45e0ca6fa30ea
TASK_BRANCH=task/311-v46-cross-standard-conformance
TASK_PACK_BLOB=248abb5c468240e702f383b003a93a6f503e4cfa
L3_BLOB=c219344d8b902bc5053adbdc2328a3147af8f7bf
T06_MERGE=72ea246263b052879833456a33e65e8e9056ab4c
T07_MERGE=a4c5fffe6bab178dcb74b5f47afcda4aa0047c27
```

Before the first implementation write, Builder MUST re-read the live integration target, #311 dependency state, Task Pack identity and this branch/pack identity. Any material drift, missing authority or mismatch is `STOP/CONTROLLER_REBIND_REQUIRED`; do not silently rewrite `base_sha` or continue on a successor target.

## Builder implementation write-set

The Builder implementation delta **after the JIT Pack HEAD** is limited to:

- `scripts/test_v46_cross_standard_conformance.py`
- `docs/implementation/4.6.0/CLOSURE_INPUTS.md`
- `docs/implementation/4.6.0/conformance/**` only when a narrowly scoped fixture is materially required by Frozen acceptance.

The Controller-generated `.agent/execution/T-008/**` files are pre-build execution authority and are not Builder implementation scope. Builder MUST NOT rewrite this pack to expand authority or make currentness pass.

## Required implementation semantics

T08 must provide integrated executable conformance and durable Version Closure **inputs**. It must not issue a Version Closure verdict.

The implementation must cover all of the following:

1. Product §11 + L2 §13 forbidden-inference union, including ephemeral-only handoff truth.
2. v4.1–v4.5 owner separation: reference/compose existing owners; do not recreate them.
3. Historical compatibility: no retrofit/relabel of historical Issues, PRs, Dispatch, Execution Pack, Review or Validation evidence.
4. Fast Path proportionality: reduce ceremony, not truth; no empty AI-native records required when non-material, but required authority/currentness/gates remain binding.
5. T06 dogfood fidelity: distinguish fixture/static evidence, actually executed fresh logical reconstruction, and dimensions left NOT_RUN.
6. Exact-subject closure-input evidence: record subject SHA/tree, CI/Validation/Review evidence identities and unresolved findings without inferring Release/Closure truth.

## Integrated forbidden-inference matrix

The negative oracle must reject at least:

```text
FI-01 user chat -> Frozen Product automatically
FI-02 Agent interpretation -> user-stated fact
FI-03 ASSUMPTION/UNKNOWN -> durable requirement without authority
FI-04 ephemeral-only truth -> acceptable durable handoff
FI-05 historical chat/memory -> override current Git/GitHub/Frozen authority
FI-06 larger context dump -> higher context quality automatically
FI-07 external resource/tool output -> Product truth automatically
FI-08 tool/Skill capability -> side-effect authority
FI-09 Skill installed -> trusted / action authorized
FI-10 Skill instruction -> override Frozen Product/Architecture/Task
FI-11 model capability/strength -> F3 authority
FI-12 same transport/GitHub account -> same logical operator/context
FI-13 AI-generated code compiles -> intent/domain correctness
FI-14 AI-authored change -> mandatory human review universally
FI-15 recorded model/provider metadata -> independence automatically proven
FI-16 Fast Path label -> required truth/gate waiver
```

## v4.1–v4.5 owner separation

T08 may verify composition but may not take ownership from:

- v4.1: Git/worktree/toolchain/config/secret/artifact/external execution;
- v4.2: interface compatibility and migration;
- v4.3: Architecture/Task decomposition, live DAG and profile mapping;
- v4.4: Build/Artifact/Distribution/Deployment;
- v4.5: runtime observation, incident and maintenance;
- existing cross-version owners: F0–F3 autonomy, Assurance/Independent Review/provenance, Dispatch/Handoff/recovery, Validation truth and Release truth.

Any owner contradiction is recorded as unresolved/BLOCKED input and routed upward; T08 does not resolve it by inventing a new owner.

## T06 fidelity binding

T06 durable facts at the integrated base include:

- canonical packet SHA-256 `33f9c9aad5d28d58e73af52326bc8bffb61a0eb4e44cb9ff49ce16b19ba6f46b`;
- Builder fixture/static result: `STATIC_FIXTURE_CLAIM=PASS`;
- exact-subject Validation: fresh logical reconstruction was actually executed by a genuinely new external Agent/runtime and PASSed against PR #529 exact subject;
- originating Builder chat was not required;
- same transport account and provider/model metadata were treated as non-probative for independence;
- NOT_RUN remained explicit for a wider model/provider-independence sweep, fresh transport-account dimension and production side effects;
- Fresh Independent Review PASSed the same exact subject before T06 merge `72ea2462...`.

T08 MUST NOT collapse those dimensions into a generic `REAL_RUNTIME=PASS`, and MUST NOT infer any unexecuted dimension from fixture or executed fresh-session evidence.

## Closure-input boundary

`CLOSURE_INPUTS.md` is an evidence ledger/input surface only. It may record PASS/FAIL/BLOCKED/NOT_RUN facts issued by their actual owners and exact subjects, but it must not issue or imply:

- Candidate Freeze;
- Version Closure PASS/FAIL;
- Release Qualification / Release READY;
- repository integration authorization;
- v4.7 convergence/resolver semantics.

Unresolved P0/P1, missing required runtime dogfood, owner conflict, stale subject identity or missing required evidence stays visible and blocks the affected Closure input from being treated as satisfied.

## Builder stop conditions

Stop and report `CONTROLLER_REBIND_REQUIRED` on target/Task Pack/L3/dependency/pack drift. Stop and report the owning authority when implementation would require Product/L2/Task authority change, a write outside the bounded set, historical evidence reinterpretation, new lifecycle/owner semantics, or a Closure/Release verdict.
