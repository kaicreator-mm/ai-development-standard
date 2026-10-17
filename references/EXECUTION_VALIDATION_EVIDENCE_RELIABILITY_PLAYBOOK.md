# Execution and Validation Evidence Reliability — field practice

> **NON-NORMATIVE / field-execution reference recovered from closed-unmerged PR #1085 (original source blob `c10f5587442eb6f1a058c2a3447c80002e24a9e5`), adapted prospectively for current ADS `main`.** Consolidates independent dogfood proposals [#1079](https://github.com/kaicreator-mm/ai-development-standard/issues/1079), [#1080](https://github.com/kaicreator-mm/ai-development-standard/issues/1080) and [#1082](https://github.com/kaicreator-mm/ai-development-standard/issues/1082). Current `VALIDATION_STANDARD`, `EXECUTION_ARCHITECTURE_STANDARD`, `CI_EXECUTION_STANDARD`, `CI_EVIDENCE_STANDARD` and frozen Task Packs retain authority. **No new required Gate, schema, CI waiver, review actor, or v4.11 DAG node** is introduced by this playbook. Project/host constraints override the examples only where current authority permits.

## 1. Why the three reports form one concern

The single concern is **accurate, efficient attribution of an executable validation result**. Ordering tests, observing progress and preserving real toolchain/exit identity are three stages of the same evidence path, not three new mandatory sub-workflows.

- #1079: two 30-second test mistakes were found only after expensive whole-pipeline reruns; a packed-consumer failure was retried before a clean-base reproduction established the likely environment class.
- #1080: background buffered pipes hid progress; dependencies/registry reachability and host load were only checked after repeated blocked runs.
- #1082: `npm test 2>&1 | tail -60` reported the downstream `tail` exit rather than `tsc` exit; an apparent Node22 launcher still delegated to a Node24 subprocess and mismatched SQLite ABI; one blocked registry family was rediscovered one test at a time; multiple agent sessions edited the same worktree.

These are recorded field observations, not measured universal performance guarantees. The affected host and exact command/exit tuple must be re-established for any new candidate.

## 2. Minimal execution sequence

1. **JIT identity / exclusive writer.** Record repository, Task/Claim, exact candidate SHA/tree, target/base, frozen pack/profile, active writer, changed paths, required validation tuple and current authoritative sources. If ownership or subject is UNKNOWN, do not start a production write.
2. **Preflight environment.** Identify lockfile/tool package manager, OS/runtime, **actual subprocess executor**, dependency cache, network/registry route and host load. Probe boundedly; do not contact production endpoints/credentials. Note which tests require external download.
3. **Smallest discriminating test first.** For a changed assertion, run that exact test/file with trustworthy exit code, then directly adjacent tests. Only after local corrections run wider concern/integration suites. An intrinsically owned full/host gate cannot be omitted merely because it is costly.
4. **Attribute first failure before repair.** Record exact failure type, touched source, tool/runtime, transient environment and source scope. For an unexplained failure in untouched code, compare on a separate **clean worktree at exact baseline**, with equivalent toolchain and inputs. Do not blindly stash/reset a shared dirty worktree.
5. **Inventory the failure family.** If registry/network/native ABI/test harness failure affects more than one test, statically enumerate known identical entrypoints before retrying a costly pipeline. Report `matches=N`, actual affected tests, and what remains UNKNOWN.
6. **Run required gate on exact candidate.** Select the authorized concern/integration/closure scope and real environment; capture logs, real exit/status, exact SHA/tree, command/profile/toolchain, test/negative counts, actor and provenance. No runner GREEN or self-reported PASS upgrades Hidden/Release or required independent Review.
7. **Stop / escalate.** Baseline-equal environmental failure => report `BLOCKED` or authorized CI/provider substitution under current Validation authority; material candidate failure => `FAIL` and Builder repair dispatch. Avoid infinite reruns without a new changed condition.

## 3. Capture real exit status and streaming progress

**Never** infer the producer's result from a trailing formatter. A tee/tail/grep pipeline may exit successfully even while the test failed.

Bash / Git Bash — an actual producer exit survives a `tee` pipeline:

```bash
set -o pipefail
log_dir="$(mktemp -d "${TMPDIR:-/tmp}/ads-validation.XXXXXX")"
timeout 900s python scripts/test_example.py 2>&1 | tee "$log_dir/test_example.log"
status=( "${PIPESTATUS[@]}" )  # capture immediately after pipeline
printf 'TEST_EXIT=%s TEE_EXIT=%s\n' "${status[0]}" "${status[1]}"
test "${status[0]}" -eq 0 && test "${status[1]}" -eq 0
```

The `timeout` shown is an **example**, not a universal 900-second budget. A `124` timeout remains a failed/blocked executable outcome, never PASS; provider-specific timeouts and required evidence follow the owner profile. Record both producer and logging errors. `tail` or `grep` may be used **after** the file is written for inspection, not as a silent authoritative exit gate.

For long tests, stream progress into a unique run log; do not hide output behind buffered filters. Include a bounded idle/no-output diagnostic mechanism when the host supports it; identify whether CPU, network, package manager or child process is actually progressing. Kill only the identified execution subtree, not unrelated workers on a shared host.

**False-green falsifier:** run a process that prints `PASS` but exits with code 2 through tee/tail. The gate must return NONZERO and record `PRODUCER_EXIT=2`, even when the last output line appears green.

## 4. Verify the real executor, not just the launcher

If the required tuple is Node22, `/opt/node22/bin/node npm-cli.js` does **not** prove the `npm run test` child used Node22. Put the selected runtime first on `PATH` for the whole command subtree, then log actual child process identity.

```bash
export PATH="/opt/node22/bin:$PATH"   # example location; discover on this host
command -v node; node --version
node -p 'process.execPath + " " + process.version'
node -e 'if (!process.version.startsWith("v22.")) process.exit(2)'
npm run test
rc=$?
printf 'GATE_EXIT=%s\n' "$rc"
exit "$rc"
```

Also test within the actual test runner process when feasible. Native addons (SQLite and similar) require ABI-sensitive build/install/evaluation under the **same selected runtime**. Do not count a Node24 test result as Node22 evidence or report hundreds of ABI-incompatible failures as source regressions without diagnosis.

**Wrong-executor falsifier:** launcher advertises Node22 but child logs Node24. The declared Node22 tuple is `INVALID/NOT_RUN`, not PASS, irrespective of test count.

## 5. Network, registry and sandbox reproductions

Preflight package/registry reachability using **short bounded** checks against the *configured* registry or mirror, honoring explicit environment overrides. Cache and install prerequisites should be recorded. A failed probe never authorizes automatically skipping a required gate; classify it `BLOCKED` and select a provider substitution only if applicable authority permits.

When CI logs are unavailable (404/expired/runner transport failure), stop repeated API polling without new evidence. Perform **clean, isolated** reproduction of the CI command chain if a trustworthy host exists: checkout exact SHA + required history, install with frozen lockfile, build, lint, typecheck, test, package as applicable. Preserve exit and local evidence, mark it as alternate execution, not the original remote CI PASS. A required provider-specific attestation remains BLOCKED until satisfied.

**Failure-family falsifier:** one test exits due to registry unavailability, and at least two other equivalent tests download through the same helper. The controller must enumerate all known affected entrypoints before an expensive full rerun; absence of inspection is `UNKNOWN`, not proof there are only one or two.

## 6. Shared worktrees and concurrent Agents

The existing Claim/write-set governance is canonical. A worktree with unrecognized untracked files, unexpected mtime churn, or a source file changing between two inspections has a possible **concurrent writer**. Stop writes, read live Claims and repository status, attribute the changed paths and choose the authorized canonical owner. Do not blindly `git clean`, `reset --hard`, stash somebody else's changes, or merge multiple green PRs touching one owner. Record the exact conflict and preserve non-owner work as source-qualified, read-only evidence when lawful.

**Writer-negative:** two agents attempt to modify the same owned file on an active protected Claim. Only the lawful first owner may write; the other must stop/escalate, with no self-generated Release or Review evidence. This is a test specification, **not an assertion that this document executed the live Claim controller**.

## 7. Evidence record and disposition

```ini
REPOSITORY=<owner/repo>
TASK_CLAIM=<exact accepted ref>
CANDIDATE_SHA=<40hex>
CANDIDATE_TREE=<40hex>
BASE_SHA=<40hex>
HOST_OS=<real observed>
TOOLCHAIN_LAUNCHER=<path/version>
TOOLCHAIN_EXECUTOR=<actual child path/version>
SOURCE_WRITESET=<exact paths>
WORKTREE_CLEAN_BEFORE=<YES|NO>
WORKTREE_CLEAN_AFTER=<YES|NO>
REQUIRED_PROFILE=<concern|integration|closure + intrinsic gates>
PREFLIGHT=<deps/network/load summary>
EXECUTION_COMMAND=<exact command>
PRODUCER_EXIT=<integer>
LOG_SINK_EXIT=<integer or NONE>
TEST_COUNTS=<actual>
BASELINE_COMPARISON=<same|different|NOT_RUN>
FAILURE_FAMILY_COUNT=<integer or UNKNOWN>
CLASSIFICATION=<SOURCE_DEFECT|TEST_DEFECT|ENV_BLOCKED|PROVIDER_BLOCKED|UNKNOWN>
VALIDATION_GATE=<PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE>
INDEPENDENT_REVIEW=<exact current ref or NOT_RUN>
RELEASE_GATE=NOT_INFERRED
```

Only report what actually executed. A green partial test and red full required profile means the required profile is not PASS. A clean-base reproduction is diagnostic evidence, not permission to rewrite tests or waive an intrinsic real-host gate.

## 8. Owner routing and stop rule

Existing **Validation Standard** controls gate meaning/currentness and fallback; **Execution Architecture** controls actor/Claim/write ownership and concern/integration/closure cost placement; **CI standards** control runner checkout/profile/log evidence; related practice [#1072](https://github.com/kaicreator-mm/ai-development-standard/issues/1072) controls mid-flight task partition/collision recovery. Normative promotion, if an actual gap remains, requires ordinary future standard-owner authority and risk-selected Review. Do not revise historical frozen Task DAGs or create separate review/implementation gates for operational tips. Executing this reference never replaces the actual project's existing required tests and validated currentness.


## 9. Real-environment / E3 field lessons (#1087, #1090)

These are **operational practices** for a project whose existing Frozen product/Task acceptance truly requires E3. No ADS-only Task, mandatory cloud provider, unconditional infrastructure gate, or permission to waive real required verification is introduced.

- **Probe capability, not a startup banner.** A ready check requires the actual producer exit = 0, parsed output of the expected type (e.g. numeric count matches `^[0-9]+$` before comparison), and a successful probe of the requested capability (NFS export *mount and readback*, not just server process PID). A failed/malformed probe is `BLOCKED/FAIL` under the selected tuple, not PASS.
- **Smallest independent remote operation first.** Run bounded local/cheap probes of API shape, cloud auth, package mirrors, canary command execution, SSH/agent readiness and artifact transfer before running the expensive full chain. Detect whether a VM and its remote-command agent are *actually* ready. Keep the verified request/response structure and avoid assuming a provider's parameter encoding from another operation.
- **Reproducible fixtures.** Record pinned base images/Dockerfiles, OS package/source revisions, init-chain and service lifetime; persistent fixture containers need a real keepalive. When reusing earlier E3 material, read the old setup scripts and their dependency initialization, not README alone. Each run has unique resource IDs and segregated mutable storage, so comparison workloads cannot contaminate one another.
- **Evidence survives failures.** Stream step checkpoints, real exit statuses and hashes to append-only persistent `events.ndjson` (not volatile `/tmp`); keep incomplete and failed-run events. A final `result.json` must not be trusted if cleanup or the run itself never reached terminal. Shell tracing (`set -x`) may be used only where secrets, tokens and presigned URLs cannot enter trace logs: otherwise use deliberately redacted checkpoints.
- **Fault injection ordering.** Capture baseline health/cost *before* injecting the fault. After a storage/network fault, the client and other resources sharing it may hang; use an unaffected authoritative side for final readback and an explicit timeout/recovery plan. The failure probe's evidence must not come from a corrupted side channel.
- **Cleanup is a bounded state machine.** Reverse dependency order, wait for provider lifecycle states, retry known transients with bounded attempts and reconcile leaked objects through provider readback. Never assert `CLEANUP_PASS` without an actual scoped resource inventory; track budget/cost of failed iterations as well as the final pass. No unbounded calls in cleanup.
- **Version/provider-sensitive transport.** Use provider-supported internal mirrors or private object storage when public network is unavailable; quote presigned links correctly and check content hash. A test-owned transport substitute must preserve tested product code and semantics, disclose the substitute and **must not decide validation outcomes**.
- **Baseline comparison and observed posture.** For an unrelated failing case, inspect source diff, reproduce at the exact unmodified baseline and compare relevant execution posture (e.g. root versus non-root permissions) before attribution. A baseline failure does not auto-waive a required gate: record the failing tuple, owning scope and real blocker.

**Negative field oracles:** PID-only ready while export unavailable → `NOT_READY`; grep-count error text while exit nonzero → `NOT_READY`; shared NFS export contaminates comparison → `INVALID_COMPARISON`; leaked cloud resource or only final summary with no terminal event → `CLEANUP/TERMINAL_NOT_PROVEN`. These examples are **specified** here, not new experiments executed by ADS.

## 10. Gate composition, security-review and skip-aware field lessons (#1088, #1089)

- Before a *required* costly gate, inspect the exact command chain, not only its entrypoint. Identify tail steps like test-directory typecheck or packaging omitted by the fastest local probe; run the tiny missing checks first. One unchanged failure does not trigger repeat full gate loops absent new information.
- Distinguish a buffered log from a stalled subprocess by the actual process tree, state/start times and last producer checkpoint; a quiet console alone does not justify killing a test. Keep high-I/O full suites serial on a constrained shared host rather than multiplying contention-induced false negatives.
- For material safety fixes, prefer **committed falsification tests** that demonstrate the original failing HEAD as RED, then repair at a new exact SHA and establish GREEN. Enumerate the full *class* of exposed paths (not only the first reported gateway/API) before closing a security class; maintain reviewed acceptance/currentness boundaries.
- Report executed, failed and skipped test counts distinctly. `PASS with 17 skipped journeys` is **not** proof that all 17 ran; when an intrinsic required journey was skipped due to registry/host, its current validation tuple is still unsatisfied. No historical suite count from a different host/runtime/checkout proves this candidate.

### Operational closeout boundary

The paragraphs above collect field reports, not a new binding validation lifecycle. `VALIDATION_STANDARD.md`, `CI_EXECUTION_STANDARD.md`, `CI_EVIDENCE_STANDARD.md`, frozen acceptance and actual platform/provider permissions decide required scope and terminal. Requirements for live runx environments and Tally scheduling remain in those projects. No fresh Host E3 or multi-hour regression was executed to publish this reference.
