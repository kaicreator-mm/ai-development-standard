# V410-T02B — JIT Task

Issue: #853
Integration target: `version/v4.10.0`
Exact baseline: `67c6828df3129bb8bbddbb36141408a6657a84fe`
Branch: `task/v4.10.0-v410-t02b-machine-projection`
Dependency #852 is DONE and integrated by PR #879.

Goal: project integrated T02A responsibility/control semantics through the existing GitHub/Event/Dispatch machine-contract family with the smallest additive backward-compatible change.

Primary owner snapshots from the exact baseline tree (unchanged by the L3-only baseline commit):
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md` @ `180efe4e1bc589f6a1f67473ff988f479f6be900` (consume only)
- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` @ `3fc300861a579c26f60e6c554f3f20675375c966`
- `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` @ `196f7d9372bcffd6ff801a70e1c1fffb204f4336` (reference boundary)
- `schemas/agent-event-v2.schema.json` @ `fefba14f338bc2e9bf67c16bae1918c1b34005a0`
- `schemas/dispatch.schema.json` @ `4607f6cb4b690bf68137294a9acf5d6ccc49e6bd`
- `templates/agent-event-comment.md` @ `fb98bb45827223235bb8d76f193cb1f250242211`

No source mutation before accepted Builder claim.