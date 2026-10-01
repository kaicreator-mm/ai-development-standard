# Logical Agent Capability Profile v1 Reference

This profile describes **claims about a logical Agent/operator/model execution class**. It is not a runner inventory, current availability record, capability proof, authorization decision, Validation result or Review result.

## Composition boundary

Eligibility may compose this profile with facts from other owners, but those facts stay with those owners:

- OS / architecture / runtimes / toolchains / devices / CPU / memory / disk / provider concurrency / network observations / current resource capacity → existing runner/host/device/resource owners such as `CI_RUNNER_CAPABILITY_STANDARD.md`.
- current `AVAILABLE | UNAVAILABLE | UNKNOWN` → derived Availability view.
- observed success/failure → Agent Capability Evidence v1.
- side-effect or security permission → canonical authorization owner.
- Review/Validation PASS → Review/Validation authority.

The generic Agent Profile references requirements such as `environment_or_runner_requirement_refs`; it never copies mutable infrastructure inventory into itself.

## Claims are not proof

`eligible_role_claims`, reasoning/semantic claims, language archetype claims and logical tool-use claims are routing inputs that still require applicable currentness/evidence/authority checks. `provider_model_provenance` records provenance only; it must not become a global correctness score or universal routing rank.

A `skill_ref` means reusable procedure metadata is available. It does not prove the logical Agent can perform the procedure correctly. Tool or credential possession similarly grants no mutation or side-effect authority.

`max_agent_freedom_claim` is a claimed ceiling. The actual freedom for an execution is set by Task/Execution Pack/Dispatch authority and may only narrow it.

## No fourth family

This contract does not create an Availability or Exchange family. Existing Interchange remains the transport-neutral family and Availability remains derived from current owner facts.

## Example

```json
{
  "schema_version": "ai-dev/agent-capability-profile-v1",
  "profile_id": "logical-agent:web-strong-builder",
  "profile_version": "1",
  "logical_agent_or_runtime_class_ref": "agent-class:chatgpt-web",
  "provider_model_provenance": "provider-model:example/strong-model",
  "eligible_role_claims": ["builder"],
  "reasoning_or_semantic_capability_claims": ["schema-contract-authoring"],
  "max_agent_freedom_claim": "F1_BOUNDED_IMPLEMENTATION",
  "environment_or_runner_requirement_refs": ["runner-class:python3"]
}
```
