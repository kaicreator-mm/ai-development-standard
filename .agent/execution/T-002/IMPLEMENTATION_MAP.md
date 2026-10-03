# T-002 Implementation Map

| Concern | Path | Allowed change |
|---|---|---|
| Same-family normative semantics | `standards/ASSURANCE_PLAN_STANDARD.md` | append v2 proof/composition/currentness sections; preserve sections 1–7 |
| Machine contract | `schemas/assurance-plan-v2.schema.json` | new v2 schema only |
| Human-readable contract examples/invariants | `references/ASSURANCE_PLAN_V2_REFERENCE.md` | new reference |
| v4.2 compatibility evidence | `references/ASSURANCE_PLAN_V2_COMPATIBILITY.json` | compatibility-record-v1 instance binding v1 baseline to v2 candidate |
| Deterministic conformance | `scripts/test_v49_assurance_plan_v2.py` | focused static/schema semantic tests |

No other source file is authorized. T-003 owns registry/adoption discovery; T-007 owns execution architecture consumption/recheck; T-010 owns cross-gate currentness transfer wiring.
