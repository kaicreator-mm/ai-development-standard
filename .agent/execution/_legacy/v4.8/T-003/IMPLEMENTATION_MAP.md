# T-003 Implementation Map

Read first: T-003 Task Pack; v4.8 L3 T-003; Frozen L2 §5; `docs/implementation/4.0.0/AGENT_INTERCHANGE.md`; `schemas/interchange-envelope-v1.schema.json`; `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`; merged T-015 profile contract.

Default implementation path is evidence for `NO_CHANGE_REQUIRED`: create only `references/V48_INTERCHANGE_PROFILE_COMPATIBILITY.md` and `scripts/test_v48_interchange_profile.py`.

Demonstrate that existing envelope correlation (`work_item_ref`, `dispatch_id`, `subject_ref`, `subject_identity_ref`, `payload_ref`, causation) can point to durable Task/Dispatch/eligibility/profile facts without copying their semantics into Interchange. Verify the closed schema rejects ad-hoc receiver-capability/authority fields.

If a concrete required Product field is proven absent and cannot be carried by existing refs/payload correlation, STOP and request Execution Pack rebind before any schema/protocol mutation. Do not manufacture a change merely to produce code.
