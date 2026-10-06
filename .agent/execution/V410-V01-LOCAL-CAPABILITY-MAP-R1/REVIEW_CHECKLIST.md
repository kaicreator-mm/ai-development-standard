# V410-V01-LOCAL-CAPABILITY-MAP-R1 Review Checklist

Fresh review of this preparation pack must verify on the unchanged exact base
`30334e8c7b90a327f8597b86c88c785b98df07f7`:

- [ ] Pack binds exactly: task `V410-V01`, contract `docs/implementation/4.10.0/V410_V01_VALIDATION_CONTRACT.md`, branch `task/v4.10.0-v410-v01-local-capability-map-r1`, parent issue `#865`, base/pinned SHA `30334e8c7b90a327f8597b86c88c785b98df07f7`.
- [ ] Claim (EXECUTION_CONTRACT.md) was recorded before any other pack file mutation; write set respected (pack dir + one script only); no pre-existing file modified.
- [ ] MANIFEST dependency_completion lists integrated predecessors with exact SHAs and states `CANDIDATE_NOT_READY` with T04B/T05B/T06A-T08A pending.
- [ ] CAPABILITY_MAP.md covers all 15 numbered contract subjects exactly once, each with exact commands, availability, limitation, and real-dispatch re-read obligation.
- [ ] Subjects requiring GitHub-native facts (4 native Issue Dependencies, 5 live branch/PR timing, 13 live CI/gate/Hidden/RQ states) are split: local part AVAILABLE, host part BLOCKED with owner=GitHub platform.
- [ ] `python scripts/test_v410_v01_capability_map.py` exits zero on this pack branch and its verbatim output is recorded; script asserts HEAD bound to base (exactly, or as a descendant whose only drift is the pack directory + this script), 15 subjects exactly once, and existence of every AVAILABLE command entrypoint.
- [ ] No PASS is claimed or implied for any V410-V01 subject; map integrity is explicitly not Validation.
- [ ] Negative invariants honored: validator never repairs source; availability records never transfer across candidate drift; no self-certification; no Hidden/RQ/release verdict fabrication; no PR/issue side effects.
- [ ] Any future use re-reads the map's inputs at the T08A-integrated exact candidate before real V01 dispatch.
