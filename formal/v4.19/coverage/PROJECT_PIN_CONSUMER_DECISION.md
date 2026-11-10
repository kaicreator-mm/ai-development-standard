# ADS #1366 — Prospective v4.19 canonical Dispatch: effective project pin prerequisite

**Context:** [Issue #1366](https://github.com/kaicreator-mm/ai-development-standard/issues/1366), experiment `7580c99f166cd76812f25249452a471fb1667a2c`, candidate PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` (OPEN). Prior audit: `CANONICAL_DISPATCH_CONSUMER_READBACK.json`.

## Execution reassessment and actual Git check

The former question was “Which production Dispatch function can validate ADS v4.19?” The more fundamental predicate is **whether a particular Task or project has actually adopted that effective ADS revision**. Without a valid pin, the producer's behavior cannot discharge a *prospective v4.19* normative clause. A function with the same name is insufficient.

I fetched GitHub's actual `kaicreator-mm/tally` **main** at `e988321439f65b55936a691c02250b6d62a29409` and **version/v2** at `7ebb1cdd0a79fc82cc938e35f852a80dd8e15332`. On **both**, `.dev-standard/VERSION` Git blob `27c31b0835075af6c66cc42ea868f1d12dcfd225` declares:
```text
repository=kaicreator-mm/ai-development-standard
version=4.18.0
revision=2c395c55569fe2edf3f4135f12d3d069e526d0b7
```
Both branches also carry `.dev-standard/PROJECT_OVERRIDES.md` Git blob `eea65d979d0c08522a2a5e9eee376e94391cb0cb`, explicitly noting the scoped v2 source adoption of ADS **4.18.0** at `version/v2` under `A1_MANUAL_PROTOCOL`, with historical main v1.5 and accepted Claim authority maintained. Do not infer that the *root VERSION on main* rewrites a historically frozen Claim. Neither observed branch provides the effective v4.19 adoption prerequisite.

The previously inspected Tally `internal/controlplane/dispatch.go` executes `TaskExecutionRequest`; that Go v1.5 main subsystem cannot be silently reclassified as a v4.19 canonical ADS dispatch publisher. **No global assertion is made** that no other branch/repository has a candidate adopter; only these actual observed heads are in scope.

## Evidence level and stop rule

Current schema and reference evidence:
- Candidate ADS dispatch JSON Schema, exact Git blob `5d9233b6b881d9d92f66fc6cd5307a05a0fdbe2f`, has 7/7 correct profile-role coupling, but schema syntax is not effective authority.
- `scripts/v34_rules.py` is a non-authoritative environment projection and Claim key helper.
- `scripts/test_protocol_schemas.py` provides reference oracles for profile-role and environment mismatch, while `scripts/test_v411_t06_claim_admission.py` is a simulated CAS test oracle.
- Candidate `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` requires an effective pinned ADS schema, fully enriched object, current Claim/Task and a publication-time readback/fence.

A real consumer acceptance must establish **D1–D8** in `PROJECT_PIN_CONSUMER_ELIGIBILITY.json`. D1 fails for the observed Tally heads. The rest are **NOT_PROVEN**, not false positive failures. A five-case strict negative eligibility decision/one positive helper control was executed on the live readback metadata; **zero real producer runtime tests** were executed.

**Decision:** Do not add another mocked SMT dispatcher, re-run historical R11 35/35 or send Local Agent to test an inapplicable project version. Select a producer only after it shows its authorized effective v4.19 pin and actual write-boundary controller. If none is available, keep `UNKNOWN / NOT_PROVEN` and prioritize other source rules where real evidence exists.

No standard source modification, official Gate, merge, Freeze, Release or GitHub Actions. Machine source evidence: `PROJECT_PIN_CONSUMER_ELIGIBILITY.json`.
