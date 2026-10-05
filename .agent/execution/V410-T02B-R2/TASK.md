# V410-T02B R2 — JIT Task

Issue: #853
Integration target: `version/v4.10.0`
Exact baseline: `f1daaffb6ae3469dc0e77e881ed73e17e6586295`
Branch: `task/v4.10.0-v410-t02b-machine-projection-r2`
Dependency #852 is DONE/integrated. Prior T02B pack @ `fbb9fb6046621ea29b660f51a8bae2f63eac32b2` is `PACK_STALE_NONMATERIAL` after #851 merge and is historical only.

Goal: project integrated T02A responsibility/control semantics through the existing GitHub/Event/Dispatch machine-contract family with the smallest additive backward-compatible change.

Current owner snapshots read/revalidated against the current integration lineage:
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md` @ `180efe4e1bc589f6a1f67473ff988f479f6be900` (consume only)
- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` @ `3fc300861a579c26f60e6c554f3f20675375c966`
- `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` @ `196f7d9372bcffd6ff801a70e1c1fffb204f4336` (reference boundary)
- `schemas/agent-event-v2.schema.json` @ `fefba14f338bc2e9bf67c16bae1918c1b34005a0`
- `schemas/dispatch.schema.json` @ `4607f6cb4b690bf68137294a9acf5d6ccc49e6bd`
- `templates/agent-event-comment.md` @ `fb98bb45827223235bb8d76f193cb1f250242211`

No source mutation before accepted serialized Builder claim.