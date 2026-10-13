# Agent Execution, Verification & E3 — Field Guide (v4.11 reference)

> **NON-NORMATIVE / PRACTICE REFERENCE ONLY.** Bounded dogfood intake as of 2026-10-13. This document does not modify the ADS rule graph, freeze any new requirement, add a Task DAG node, create an Issue dependency, authorize Builder/Reviewer/Validator actions, or issue Validation/Release PASS. It is not a mandatory new gate.
>
> **Precedence:** pinned ADS standards, frozen v4.11 Product #943, L2 #954, 20-node/30-edge DAG #966, reviewed Task Packs #967, live native Task Issues, and applicable Review/Validation/Release owners prevail over this guide. Contradictions must be resolved by an authorized owner; this guide cannot weaken P0/P1 handling, independent review, real-host requirements, Hidden validation, or release qualification.
>
> **Version integration guard:** this reference is a docs-only optional sidecar to version/v4.11.0. Do not merge or rebase it into the active T12 #1020 / PR #1086 candidate. Integrate only after its active exact-HEAD owner gate has concluded, with proportionate docs checks/current independent review, **before** release candidate freeze/visible validation if no currentness impact remains. If the safe window has passed or integration would churn T12/V01 evidence, defer the sidecar to the next release rather than inserting a release blocker. A merged docs change becomes part of the next exact version SHA and must be included honestly in downstream candidate identity.

## 1. Intended use and decision boundary

This playbook collects *operational lessons* from downstream dogfood. Use applicable suggestions to make existing task executions more observable, less repetitive, and more reliable. It does not establish fresh semantic-owner requirements or override the exact Task/Execution Pack. Local environments differ; examples must be adapted to the task's pinned toolchain and authorized environment. An observed success, skipped suite, synthetic oracle, or older SHA cannot be relabeled as production or version PASS.

Before running an expensive local/real-host gate, briefly classify:
- **Subject:** pinned repository/ref/HEAD/tree, Task and approved write set, current accepted Review/Validation policy.
- **Purpose:** what minimal implementation/contract fact will the check establish, what counterexample would refute it, and what remains out of scope?
- **Evidence strength:** source inspection, isolated test fixture, real owner API, true effect boundary, real host, CI, or version gate; none substitutes for a stronger required gate.
- **Stop/route:** PASS with bounded claim; FAIL due to code; BLOCKED/UNKNOWN due to material coverage; SKIPPED or NOT_RUN due to environment; existing owner receives any follow-up.

## 2. Run the cheapest discriminating check first

Observed in #1079 and #1088: an assertion typo or uncovered test-directory type error repeatedly forced a many-minute or hour-scale aggregate gate rerun.

Practical sequence, only where consistent with the owning Task Pack:
1. Read the *entire* configured gate chain, including post-test typecheck, build, legacy checks and packaging/consumer steps. A direct single-file test usually does not cover those trailing checks.
2. Run changed or new tests directly, then affected owner/neighbor tests and any affected test-code typecheck. Fix obvious assertion and compilation defects before expensive whole-suite/packed-journey execution.
3. For a failure outside the touched surface, identify the **exact failing unit** and compare it against a clean original-base checkout (or other non-mutating control), then evaluate platform/privilege/toolchain differences. A baseline failure is evidence of pre-existence **only for that exact base and environment**, not permission to falsify required completion.
4. Route truly environment-dependent or skipped coverage to the owning real-host/CI/Release gate as its existing policy requires. Do not mark an unexecuted path PASS or unilaterally waive it.
5. Avoid overlapping heavy installation, full-regression and multi-toolchain jobs on a resource-constrained shared worker; serialize those workloads while preserving independently safe light source/test tasks.

The task's configured CI/full/hidden requirements remain authoritative even if focused local checks pass.

## 3. Make long-running evidence trustworthy

Sources: #1080, #1082, #1088.

- **Exit integrity:** log the actual exit status of the executed test/process, not the trailing tail/grep/tee pipeline or wrapper. A displayed green summary with a masked nonzero compiler result is a false PASS. In Bash, use pipefail and/or capture the left-side PIPESTATUS *immediately*; otherwise run the command with direct file redirection and record the command exit before inspecting the file.
- **Bounded observability:** use explicit per-phase log files, stage labels, output timestamps/checkpoints where feasible, and an authorized per-stage timeout. Do not interpret a stalled terminal tail as proof of a dead process when buffered output or progressing child processes remain.
- **Real executor:** record the **actual child process** toolchain versions and resolution path, not merely the binary used to launch a wrapper (e.g., Node/npm subprocess version drift and native module ABI mismatch).
- **Preflight:** inspect lockfile/package-manager, network/registry/credential path, disk/worker load and sandbox availability *before* spending the full gate budget. Never print secrets as part of diagnostics.
- **CI blind spot:** if remote CI logs are inaccessible, reproduce its exact declared command chain in a clean isolated worker and report both the local facts and the unresolved remote status separately; do not promote a local reproduction to CI success.
- **Concurrent writers:** if the same working tree is actively modified by another worker, stop shared-file writes, preserve own evidence, reconcile exact diff/HEAD and use isolated worktrees before proceeding.

For a Bash/Linux-only illustrative command, preserve the test's left-hand status:

~~~bash
set -o pipefail
# Preserve exact-SHA checkout cleanliness by logging in a temporary directory.
log_dir="$(mktemp -d "${TMPDIR:-/tmp}/ads-e3-evidence.XXXXXX")"
timeout 900s python scripts/test_example.py 2>&1 | tee "$log_dir/run.log"
status=( "${PIPESTATUS[@]}" )  # capture producer and tee exits immediately
printf 'TEST_EXIT=%s TEE_EXIT=%s\n' "${status[0]}" "${status[1]}"
test "${status[0]}" -eq 0 && test "${status[1]}" -eq 0
~~~

The command above is an example, **not** a prescribed universal command or a substitute for task-specific timeout policy. On Windows or shells without timeout/PIPESTATUS, use that host's equivalent while preserving the invoked process exit code.

## 4. Security and fresh review: falsification, surface inventory, skip disclosure

Source: #1089, with non-convergence evidence #696. When a reviewer supplies a concrete counterexample, prefer to encode a stable, authorized regression test and demonstrate **red on the vulnerable exact SHA, green on the repaired successor**. Preserve test logs and identities. If testing the older commit is unsafe or the negative check itself is hazardous, use isolated inert fixtures and report that limitation; never replay production effects.

A fix to one gateway/port/getter is not automatically a fix to its *class* of externally callable authority or secret surfaces. Enumerate sibling entrypoints and account for them explicitly. An environment-guarded test suite must disclose counts and reasons for **executed vs skipped**; a no-fail exit with all network/packed journeys skipped is not evidence those journeys passed. Use bounded delta review where current Review policy permits it; do not impose a new automatic round cap, excuse a current P1, or substitute the builder's own verdict for an independent Review.

## 5. E3 real-environment execution: canary, capability readiness, fixture, cleanup

Sources: #1087 and #1090. These are **optional operator techniques** for E3 environments already required/authorized by an owner, not authorization to provision or mutate cloud, external systems or credentials.

1. **Isolated dependency canaries:** separately probe cloud API invocation, remote-agent readiness, image/package ability, external service capability, transport, and teardown. Only compose the expensive full chain once the minimum dependencies are evidenced. Treat a process-ready banner as weaker than a *capability-ready* proof (for example, actual authorized NFS export+mount+readback).
2. **Typed probes:** check the probe's real process exit, expected output shape and semantic capability. Validate numeric text before comparing it; a diagnostic error string or nonzero grep count is not a successful readiness measurement. Bound all retries/waits.
3. **Durable fixture recipe:** record base image, build commands/Dockerfile, package variants, required initialization sequence, lifetime/daemon management, configuration redaction and exact resulting digest. A detached server fixture needs a known sustained process lifetime; do not assume every image's default command stays alive. When reusing a predecessor, inspect the **complete** init chain, not just a README.
4. **Isolation before comparability:** give each repeated or parallel workload a separate mutable storage/export/workspace/queue. Otherwise one workload's artifacts can silently appear in another oracle. Capture healthy-state latency/cost evidence *before* injecting faults.
5. **Failure-phase readback:** after server restart/crash injection, a shared client can have unrelated hard-mounted I/O stuck. Prefer the authoritative server-side readback defined by the test contract; do not infer client success from contaminated paths.
6. **Remote observability and artifact integrity:** use per-step CHECKPOINT markers, bounded command logs, a canary for remote-agent availability and checksums before consuming transferred artifacts. Shell xtrace can leak tokens or presigned URLs; enable it only for **redacted, nonsecret portions**, never blindly on credential-bearing commands. Log safe raw-response metadata for ambiguous provider API shape; do not assume one cloud API's parameter encoding generalizes to another.
7. **Cleanup as a bounded state machine:** record all created resource IDs, delete in reverse dependency order with state-aware retries and timeouts, then inventory remaining resources from the authorized scope. A failed cleanup is not success; distinguish residual resources and manual recovery instructions. No unapproved destructive actions.
8. **Persistent audit trail:** keep intermediate events/logs/recipes in a stable evidence directory with precise environmental provenance rather than ephemeral session temp. Record actual execution result, skipped cases, operational substitutions and remaining UNKNOWNs.

An operator-owned substitute transport/CLI may be acceptable **only when the owning gate allows it**, the product under test remains unchanged, and the substitute does not decide the oracle outcome. An E3 canary cannot grant current human authorization or stand in for actual downstream Release/Hidden requirements.

## 6. Task oversize and L1 research convergence: references, not live DAG mutations

- **#1072 / #775:** a semantically coherent task may still be too large for one agent. Prefer pre-dispatch decomposition where independent contracts are real, with one shared wiring owner. Once a canonical DAG/Claim/PR is active, splitting requires an authorized native dependency and claim/currentness change; never silently split or overlap writes merely because a task runs long. In **v4.11**, the frozen 20 nodes/30 edges and active T12 are unchanged by this guide.
- **#1081:** explicit, phase-scoped Evidence DAG and an L1 research exit can help end recursive experiment-tooling hardening, but neither this reference nor an advisory planning list becomes a second canonical implementation DAG. Consume the already merged [Research Convergence & Exit playbook](RESEARCH_CONVERGENCE_AND_EXIT_PLAYBOOK.md) rather than duplicating it. Formal L1 process/prompt changes require normal later-version ownership and dogfood.

## 7. Intake and future normative disposition

| Existing feedback | v4.11 treatment | Future owner decision |
| --- | --- | --- |
| [#1079](https://github.com/kaicreator-mm/ai-development-standard/issues/1079), [#1088](https://github.com/kaicreator-mm/ai-development-standard/issues/1088) | §2 proportional local checking / gate-chain inventory, advisory | Evaluate narrower Testing/Validation standard deltas |
| [#1080](https://github.com/kaicreator-mm/ai-development-standard/issues/1080), [#1082](https://github.com/kaicreator-mm/ai-development-standard/issues/1082) | §3 observability, executor identity, true exits, advisory | Evaluate execution/CI evidence rules without duplicate authority |
| [#1089](https://github.com/kaicreator-mm/ai-development-standard/issues/1089), [#696](https://github.com/kaicreator-mm/ai-development-standard/issues/696) | §4 regression and review efficiency, advisory | Review owner decides severity/blocking/round policy |
| [#1087](https://github.com/kaicreator-mm/ai-development-standard/issues/1087), [#1090](https://github.com/kaicreator-mm/ai-development-standard/issues/1090) | §5 E3 operator reference, advisory | E3 Validation owner evaluates portable normative subset |
| [#1072](https://github.com/kaicreator-mm/ai-development-standard/issues/1072), [#775](https://github.com/kaicreator-mm/ai-development-standard/issues/775) | §6 safe split warning only | Task DAG Governance/Decomposition owner decides later-version amendment |
| [#1081](https://github.com/kaicreator-mm/ai-development-standard/issues/1081), [#680](https://github.com/kaicreator-mm/ai-development-standard/issues/680), [#931](https://github.com/kaicreator-mm/ai-development-standard/issues/931) | Reuse existing Research Convergence reference | L1/L2 research-process owner decides future normative treatment |

**No feedback Issue is closed merely because this reference cites it.** Reference adoption is not equivalent to fulfilling the Issue's full acceptance criteria. Later owners can close, consolidate or defer with source-bound proof without reopening frozen v4.11 authority.

## 8. v4.11 acceptance boundaries

- New files: exactly this reference document. No edits to standards, Product/L2/DAG/Pack, native Issue deps, schemas, fixtures, verification scripts, manifest, CI rules or Release checklists.
- v4.11 remains **20 nodes, 30 edges**; T12 #1020 / PR #1086 keeps its original admission, HEAD-bound real-host and fresh-review duties. **No claim that T12 or V01–R02 has passed** is created by this reference.
- A docs-only PR needs correct target/base currentness, a bounded non-self independent review and relevant docs/CI evidence before merging. Merge is optional and nonblocking; if it cannot safely enter before next candidate freeze without invalidating required evidence, **defer rather than force**.
- Preserve historical failures/skips and exact SHA distinctions. No decision in this file changes the canonical source of truth.
