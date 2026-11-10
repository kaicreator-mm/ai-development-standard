# DAG serial edge reason: bounded non-authoritative probe

**Main Issue:** [#1366](https://github.com/kaicreator-mm/ai-development-standard/issues/1366).

## Candidate source and test purpose

PR #1365 adds `standards/TASK_DECOMPOSITION_STANDARD.md` §13.1. It says
a material serial edge must be supported by actual code baseline or another
real prerequisite, not merely a future compatibility/Review/Release join.
But a possibly redundant edge **cannot be removed by a source probe**:
native GitHub Issue Dependencies, frozen contract, approved mutation,
protected write sets and Task Claim remain authoritative.

This small Python probe uses explicit frozen-contract and edge evidence
inputs. `join_only` without a real code/writer dependency is merely a
`POSSIBLE_FALSE_SERIAL_EDGE` advisory; it still returns
`HOLD_NATIVE_DEPENDENCY`. Actual code baseline or write-set collision
returns `MATERIAL_SERIAL_EDGE`; missing evidence is `UNKNOWN` and
`NOT_AUTHORIZED`. Even with `native_dependency=false`, the probe never
issues readiness, accepts a Claim or authorizes mutation.

## Executed Python evidence

Python 3.13.5: **7/7** isolated repository-layout unit tests PASS.
Native-mutation-negative and evidence-unknown cases checked.
Execution log SHA256:
`b43285892603c8548ad551983db113c17b490095fd4c12748630fa73b93f8711`.
Standalone demo output SHA256:
`8eb3ed9bd73c7c117c4d8bdf70806ae57e25ac9b77cba25f6d32683058f95911`.

Both Git source file blobs were computed locally and must match the
GitHub readback. Evidence in `DAG_EDGE_EXECUTION.json`.

**NOT_PROVEN:** real Task dependencies or dispatch eligibility, complex DAG,
contract source semantics or normative ADS equivalence. No extra SMT
model case; no GitHub dependency mutation; no Gate, Freeze, Release.
