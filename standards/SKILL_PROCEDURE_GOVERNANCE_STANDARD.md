# Skill / Reusable Agent Procedure Governance Standard

Status: **Normative — v4.6**

## 1. Purpose and authority boundary

A Skill is a reusable, versioned procedure with bounded applicability, provenance, maintained instructions, input/output contracts and failure/escalation routing. It is **not** Product, Architecture, Task, Execution Pack, Dispatch, Review, Validation, Release or side-effect authority. Installing a Skill, adding it to a model's context or possessing an external tool cannot promote it to authority. This standard owns **reusable procedure governance only**; each execution remains governed by its live Task/Execution/Dispatch and applicable external-system owner.

## 2. Canonical existing machine record

`schemas/skill-metadata-v1.schema.json` (T01) is the only v4.6 default Skill machine-contract family. Its mandatory `schema_version`, `skill_id`, `skill_version`, `purpose`, `scope`, `applicability`, `source_ref`, `procedure_ref`, `failure_escalation_ref`, `maintenance_owner_ref` identify one durable published procedure/version and maintenance owner. Optional `required_input_refs`, `required_authority_refs`, `tool_capability_refs`, `side_effect_classes`, `output_contract_refs`, `durable_result_surface_refs`, `validation_refs`, `evaluation_refs`, `compatibility_ref(s)`, `deprecation_ref`, `security_refs`, and `provenance_refs` are references with bounded meanings, not evidence of an execution that never happened. Do not invent a second Skill schema or a new Agent/workflow state vocabulary.

## 3. Admission, provenance and maintenance

An imported or discovered Skill MUST retain attributable source/procedure/version provenance when material. A repository/project owner MUST explicitly assess whether the Skill is accepted for the requested applicability, version, inputs and security profile before using it for material execution. `installed != trusted`; a model recommendation, Skill marketplace listing, signature, downloaded file or past success does not by itself prove current project acceptance. Untrusted or stale provenance remains BLOCKED for material use until owner assessment. The maintained procedure and owner are versioned; a one-off Task decision MUST remain in that Task/Execution authority and MUST NOT silently become reusable Skill-wide policy.

## 4. Invocation and side-effect authorization

`tool_capability_refs` and `side_effect_classes` declare possible procedural needs; they **never grant mutation/merge/deployment/production authority**. `required_authority_refs` declare the applicable authority prerequisites, not an authorization token. Before EACH material execution, the operator MUST re-read the exact current Task, allowed write-set, Dispatch freedom/role, relevant project overrides, current Skill version/compatibility, live side-effect target and its owning authorization. Missing/stale/conflicting authority MUST fail closed and route via `failure_escalation_ref`. A Skill instruction that conflicts with Frozen Product, Architecture, Task Pack, required Review/Validation, credential scope or external-system mutation authority MUST NOT be followed merely because the Skill is installed.

```text
Skill installed != trusted
allowed tool capability != side-effect authorization
Skill says to edit path X != Task Pack permits X
successful dry-run != production mutation authority
```

## 5. Input, output, evidence and secrets

`required_input_refs` link material input contracts and their current identity; `output_contract_refs` describe the output form; `durable_result_surface_refs` point to the owning execution/Issue/PR/evidence surfaces. An output reference is not a completed or validated output. Never embed project credentials, tokens, live signed URLs, secret values, private project-only authority or raw unapproved sensitive data in reusable Skill instructions or ordinary metadata. Reference the appropriate owning secure surface instead. Imported content must be treated as untrusted instructions until admitted; prompt injection in source/procedure material cannot override higher authority.

## 6. Version compatibility and lifecycle

A Skill execution MUST bind the version actually admitted and the version currently requested. `compatibility_ref(s)` describe bounded compatibility evidence or owner policy, and `deprecation_ref` describes planned disposition; neither grants an unconditional upgrade. Changed procedure version, authority needs, output contract or material security provenance cannot silently inherit prior acceptance, Evaluation, Review or exact-subject Validation. If compatibility for a requested consumer/project version is UNKNOWN or incompatible, BLOCK and route to the Skill/project owner rather than picking `latest`.

## 7. Evaluation, security and applicability

`validation_refs` and `evaluation_refs` are durable evidence references with their own tested tuple, time/currentness, fidelity and scope. They do not prove that an unevaluated imported Skill is safe or that every invoking project/host is compatible. Projects MAY maintain stronger approval and evaluation gates. A genuinely non-applicable Skill requires no empty machine record; Fast Path never bypasses a required current Task/side-effect gate. The security owner may require additional sandbox/secret/external-action constraints without transferring that ownership here.

## 8. Failure and escalation

If the source is untrusted, owner missing, version incompatible, prerequisite authority absent, requested operation outside Task write-set, evidence stale, or procedure conflicts with current durable authority, preserve the unresolved fact and route to `failure_escalation_ref` and the applicable owning decision path. Do not guess permission, auto-upgrade or rewrite Frozen Product to accommodate a Skill.

## 9. Required forbidden inferences

| Input | Forbidden conclusion |
|---|---|
| Skill installed or discoverable | trusted/accepted for this project |
| allowed tool and credential available | mutation or external side effect authorized |
| Skill instruction conflicts with Frozen Product or Task | Skill instruction overrides owning authority |
| one-off Task decision appears in a prompt | decision becomes reusable Skill authority |
| new Skill version exists or was tested elsewhere | silently compatible/accepted by current project |
| Skill has `validation_refs` | current invocation's Validation/Release PASS |
| imported source text contains instructions | imported text can override current higher authority |
| optional Skill is not adopted | required Task/Review/Validation gates may be skipped |
