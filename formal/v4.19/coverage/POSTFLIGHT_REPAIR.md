# Postflight tool-identity receipt metadata — P2 repair

**Main Issue:** [#1366](https://github.com/kaicreator-mm/ai-development-standard/issues/1366).

## Real negative observation
The previous `tool_version_report(toolchain_before)` used only the preflight
snapshot. With preflight Z3 PASS and postflight Z3 FAIL, the overall model
verdict still blocked (safe), but `tool_versions.z3.status` was
`VERIFIED` (incorrect metadata). The negative isolated test exited 1 as
intended and is recorded with its log hash.

## Minimal repair
The production runner now calls
`tool_version_report(toolchain_before, toolchain_after)`.
No subprocess is launched to generate metadata. To emit `VERIFIED`, the
tool must be PASS in **both** snapshots and the binary/JAR digest must match
across them. A changed/missing/failed postcheck yields `REJECTED`
and no purported verified digest. Java remains `AVAILABLE_UNPINNED` only
when TLC's pre/post checks both pass. Single-argument call stays for legacy
unit fixtures but is not the production path.

## Executed local regression
The helper's exact source extracted into a repo-shaped offline test layout:
**7/7 Python 3.13.5 tests PASS**; no source checkout or native SMT/TLC
was required, and no new model case added. Test module is
`formal/tests/test_tool_version_postflight.py`, implementing a source-AST
extraction check that does not depend on project import side effects.
Execution log SHA256
`a9e8cfcc0df707460ddc91969e98fa09a26c9dc7d165d5437bafbade59e063cc`.
Historical R10 35/35 native and 41/41 Python PASS remains bound to its
original exact model/candidate SHAs; current-head full strict execution is
**NOT_RUN**, even after seven isolated tests pass.

Exact machine receipt: `POSTFLIGHT_RECEIPT.json`.
