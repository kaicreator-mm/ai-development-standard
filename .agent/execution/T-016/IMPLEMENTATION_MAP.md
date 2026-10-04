# T-016 Implementation Map

Read first: T-016 Task Pack, v4.8 L3 T-016, Frozen L2 evidence model and L1/#469 economic boundary.

Create `schemas/agent-capability-evidence-v1.schema.json`, `scripts/test_v48_agent_capability_evidence.py`, and `references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md` only.

Bind subject/environment/role/result/evidence refs explicitly. Keep measured economic/performance fields nullable or explicitly NOT_MEASURED. Represent bounded evidence strength without a global ranking score. Preserve positive and negative evidence and historical status after subject drift.
