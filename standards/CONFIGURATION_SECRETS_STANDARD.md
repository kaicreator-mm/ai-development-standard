# Configuration & Secrets Governance Standard

## 1. Purpose and authority

This standard is the normative owner for configuration source authority, deterministic precedence, secret-reference semantics, secret-value handling, least privilege, redaction and credential/configuration unavailability.

It does not mandate one configuration file, secret manager, cloud, identity provider or credential issuance mechanism. It does not own external-system side-effect authority, Validation results or Release Qualification.

When structured execution facts are useful, `schemas/execution-context-v1.schema.json` may carry non-secret configuration fingerprints and secret references. It MUST NOT carry durable secret values.

## 2. Configuration schema/key authority

A project SHOULD identify the authoritative schema, key definitions or configuration contract for material settings. Agent defaults, shell history, machine-global state and prior-chat assumptions are not project authority.

Unknown configuration keys or conflicting interpretations MUST NOT be silently resolved by Agent preference when they affect behavior, safety, security, environment identity or validation.

## 3. Deterministic source precedence

Projects MUST define deterministic precedence for configuration sources that can overlap. A typical project may choose a sequence such as:

```text
Frozen/project contract
→ project override/profile
→ environment-specific authorized config
→ process/environment injection
→ command/dispatch override
→ implementation default
```

This sequence is illustrative; each project may define another order. What is mandatory is deterministic authority and conflict resolution.

An Agent MUST NOT invent precedence from the order in which files happened to be discovered.

## 4. Non-secret configuration identity

Material non-secret configuration SHOULD be representable by stable source references and/or a non-secret fingerprint sufficient to distinguish evidence-relevant configuration.

A fingerprint proves identity of the represented non-secret configuration only. It does not manufacture Validation PASS and MUST NOT include secret values merely to make the hash reproducible.

## 5. Secret references versus secret values

A **secret reference** identifies how authorized execution may obtain a secret without persisting the secret value in ordinary durable project artifacts. It may include reference identity, source/provider class, scope or intended use when non-secret.

A **secret value** is credential/key/token/password/private material, including equivalent bearer material such as signed URLs when possession grants access.

Ordinary durable repository source, logs, GitHub Issues/PR comments, Task Packs, Execution Packs, Validation evidence and normal test fixtures MUST NOT contain secret values.

Durable contracts SHOULD store refs/identity, never plaintext values.

## 6. Least privilege and scope

Credentials MUST be scoped to the minimum practical account/project/tenant/environment/resource/action/time window required by the authorized execution.

Write-capable credentials MUST NOT be used when read-only access satisfies the task. Production credentials MUST NOT be used merely because sandbox/staging credentials are inconvenient.

Short-lived or just-in-time credentials are preferred where the provider/project supports them and they materially reduce risk. Static credentials remain permitted when explicitly authorized and appropriately protected; this standard does not falsely require OIDC/Vault/JIT everywhere.

## 7. Redaction and non-persistence

Tools/Agents MUST avoid echoing secret values in command lines, logs, exception messages, screenshots, fixtures or generated reports when a safer mechanism exists.

Redaction MUST preserve enough non-secret identity for debugging/audit while preventing recovery of the secret value. Partial masking is not safe when the remaining material is itself usable or sufficient to reconstruct the credential.

A secret discovered in ordinary durable output MUST be treated as a security incident/defect according to project policy; deleting the visible line alone does not prove the secret was never exposed elsewhere.

## 8. Authorized encrypted-secret exception

A project MAY intentionally store encrypted secret material in Git or another durable system only when all of the following are explicit:

- project authority permits it;
- ciphertext is not directly usable as the credential;
- key/decryption authority is separate and appropriately controlled;
- rotation/revocation and access policy are defined;
- ordinary logs/evidence still do not expose decrypted values.

This is a bounded exception for encrypted secret material, not permission to commit plaintext `.env`, tokens or passwords.

## 9. Credential/configuration availability

If required configuration or credentials are unavailable, invalid, expired, unauthorized or materially mismatched to the requested environment/account/tenant, the execution MUST remain truthful.

Do not fabricate credentials, downgrade the required environment, silently substitute another account, or report PASS for an unexecuted check. The owning execution/Validation fact remains `BLOCKED` or `NOT_RUN` as appropriate until authority or availability changes.

## 10. Environment-sensitive identity

When behavior/evidence depends on an environment, account, project or tenant, configuration/credential references SHOULD identify those non-secret dimensions sufficiently to prevent evidence substitution across materially different contexts.

Credential identity does not itself grant side-effect authority; `EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` owns external fidelity/environment/side-effect semantics.

## 11. Local files and `.env`

`.env` files are a possible local mechanism, not universal authority. If used, projects MUST distinguish committed template/non-secret examples from local secret-bearing files and ensure secret-bearing files are excluded from ordinary durable source/evidence unless covered by the encrypted-secret exception.

The same principle applies to OS keychains, cloud secret stores, CI secret injection, Vault-like systems, OIDC federation, Kubernetes Secrets or other mechanisms: provider choice is project-specific.

## 12. Agent behavior

An Agent MUST:

- resolve applicable configuration authority and precedence before behavior depends on it;
- keep secret refs separate from secret values;
- request/use only authorized scope;
- avoid durable secret persistence and redact unsafe output;
- preserve truthful BLOCKED/NOT_RUN behavior when required config/credentials are unavailable;
- record non-secret environment/account identity when material to evidence.

An Agent MUST NOT:

- create fake credentials to satisfy a test;
- commit plaintext secrets or place them in Issue comments/evidence;
- infer that a local credential is authorized merely because it works;
- widen credential scope to avoid an authorization failure;
- mandate one provider as a universal implementation.

## 13. Fast Path and proportionality

Minimal/Fast-Path work may omit a formal configuration profile when configuration is immaterial and no secret is required. The moment configuration/credential differences can affect behavior, evidence or side effects, the material facts must be surfaced.

## 14. Failure handling

- conflicting material config with no authoritative precedence → `BLOCKED` pending authority resolution;
- required credential unavailable/expired → `BLOCKED` / not executed, not FAIL by fabrication;
- secret leak detected → stop unsafe publication and follow project security/rotation policy;
- required environment identity cannot be proven → evidence MUST NOT be substituted across environments.

## 15. Boundary with other owners

- `VALIDATION_STANDARD.md` owns executed Validation states.
- `EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` owns external fidelity/environment/side-effect authority.
- `GIT_EXECUTION_STANDARD.md` owns workspace/repository execution.
- `WORKSPACE_ARTIFACT_STANDARD.md` owns artifact class/lifecycle; `SECRET_MATERIAL` remains subject to this standard's value-handling rules.
- T07 owns central adoption/PROJECT_OVERRIDES wiring.
