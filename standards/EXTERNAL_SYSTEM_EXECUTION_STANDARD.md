# External System Execution Standard

## 1. Purpose and authority

This standard is the normative owner for execution facts at external-system boundaries: dependency fidelity, provider/project environment, state scope, side-effect authority, account/tenant identity, credential reference, retry/timeout bounds and truthful infrastructure failure classification.

It does **not** own Validation result states, Test Gate policy, Candidate Freeze, Release Qualification or project credentials themselves. `VALIDATION_STANDARD.md` remains authoritative for PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE and exact execution tuples.

`schemas/execution-context-v1.schema.json` may project material external-system facts. Provider/environment labels remain extensible; this standard intentionally avoids one universal provider taxonomy.

## 2. External system definition

An external system is any dependency whose material behavior is outside the executing repository/process boundary, including APIs, databases, queues, cloud services, LLM providers, browsers, remote build hosts, SaaS systems, identity providers or external devices/services.

The same technology may be in-process for one Task and external for another. Material boundary behavior, not brand name, determines applicability.

## 3. Dependency fidelity

Execution MUST distinguish the fidelity actually exercised when that distinction is material. Common dimensions include:

- pure mock/stub/fake;
- simulation/emulation;
- local real service instance;
- provider sandbox/test environment;
- staging/pre-production environment;
- production/real target environment;
- project-defined equivalents.

These labels are examples, not a closed universal enum. A project may use other terms, but MUST preserve enough meaning to prevent evidence from being silently escalated to a higher-fidelity requirement.

A lower-fidelity execution may provide useful concern evidence, but it MUST NOT satisfy an unexecuted higher-fidelity requirement by assertion.

## 4. Provider/project environment identity

When environment matters, evidence SHOULD bind the material provider/project environment identity rather than only a friendly label.

Relevant identity may include provider, project/account, tenant/organization, region, endpoint class, subscription, cluster, database instance or another project-defined environment reference.

Evidence from environment A MUST NOT be substituted for environment B when the distinction is material to the required journey or Validation tuple.

## 5. State scope

External state SHOULD be classified when material, for example:

- ephemeral per execution;
- isolated per Task/test;
- shared test/sandbox;
- persistent staging;
- production/shared live state;
- project-defined scope.

Shared/persistent state increases contamination and cleanup risk. State scope MUST NOT be hidden when it can change behavior, repeatability or side effects.

## 6. Side-effect authority

Read, create, update, delete, publish, send, deploy, charge, notify or other externally visible mutations require explicit applicable authority.

Read-only access does not prove a write journey. A credential capable of writing does not by itself authorize a write. Side-effect authority must come from Task/project/execution authority.

Production/live writes are never assumed merely because an Agent can authenticate successfully.

## 7. Account, tenant and credential references

When material, execution/evidence SHOULD record non-secret account/project/tenant/environment identity plus a credential **reference**, not the secret value.

Secret values remain governed by `CONFIGURATION_SECRETS_STANDARD.md` and MUST NOT be copied into durable external-system evidence.

A credential that authenticates to the wrong tenant/account/environment MUST NOT be silently accepted as equivalent evidence.

## 8. Fidelity non-escalation

The following substitutions are forbidden unless project authority explicitly defines them as equivalent for the requested gate:

```text
mock/simulation PASS -> real service PASS
local real dependency PASS -> provider sandbox/staging PASS
sandbox PASS -> staging/production PASS
read-only PASS -> write-side-effect PASS
one tenant/account PASS -> another material tenant/account PASS
```

Equivalent environments MAY satisfy a requirement only when their equivalence is defined/proven by the owning authority; the Agent cannot invent equivalence after execution.

## 9. Infrastructure unavailability versus product defect

Execution MUST distinguish external infrastructure/access failure from an executed product behavior failure when evidence supports that distinction.

Examples of infrastructure/access blockers include:

- DNS/network/TLS connectivity unavailable;
- required credential missing/expired/unauthorized;
- provider outage or maintenance;
- quota/rate limit prevents the required execution;
- required account/tenant/environment not provisioned;
- remote build host/device/service unavailable.

Such conditions normally produce truthful `BLOCKED`/`NOT_RUN` according to the owning Validation/execution standard, not fabricated product FAIL or PASS.

If the product itself mishandles a validly available external condition, that can be a real product FAIL. Classification must follow evidence rather than convenience.

## 10. Retries

Retries MUST be bounded by count, elapsed time, deadline or another explicit policy. Retry policy SHOULD distinguish potentially transient failures from deterministic product/contract failures.

An Agent MUST NOT retry indefinitely to wait for a desired result, exhaust provider quota, duplicate unsafe side effects or obscure a deterministic failure.

Non-idempotent writes require special care. A retry MUST NOT duplicate a side effect unless idempotency/deduplication or compensating semantics are proven/authorized.

## 11. Timeouts and deadlines

External operations SHOULD define timeouts/deadlines appropriate to the dependency and requested profile. A timeout is an execution fact, not automatically a product defect.

Increasing a timeout after failure is a configuration/change decision and MAY require re-execution; it does not rewrite the prior outcome.

## 12. Rate limits and quotas

Rate-limit/quota state SHOULD be captured when it materially prevents execution. An Agent MAY wait/retry within authorized bounded policy or use an explicitly allowed equivalent account/environment.

It MUST NOT evade policy by rotating unauthorized credentials/accounts or silently switching tenants/providers.

## 13. Cleanup and reversibility

Tasks that create external state SHOULD define ownership and cleanup/rollback expectations when material. Cleanup itself is a side effect and requires authority.

Failure to clean shared state may become an execution blocker or defect depending on the owning contract. Destructive cleanup MUST NOT target ambiguous/unowned external state.

## 14. External writes and human-impact boundaries

Actions that send messages, publish content, deploy, bill/charge, modify customer data, change infrastructure or create other human/business-visible effects require explicit scope and target authority.

A sandbox/test journey SHOULD be preferred when it can prove the required behavior without unauthorized real-world impact. If production/live execution is the actual required acceptance journey, lower-fidelity substitutes do not satisfy it.

## 15. LLM/browser/build-host examples

An LLM mock can test request shaping but cannot prove provider authentication, quota behavior or real response transport. A browser DOM fixture can test parser logic but cannot prove a real authenticated browser journey. A local build can test compile logic but cannot prove a required remote platform/build-host tuple.

Each may be valid evidence for its declared fidelity only.

## 16. Validation tuple integration

External-system facts extend the execution context; they do not replace the Validation Tuple.

When material, a Validation Report SHOULD reference enough external-system identity/fidelity/environment/side-effect facts to establish what actually executed. PASS remains owned by `VALIDATION_STANDARD.md` and applies only to the executed exact subject/profile/environment facts.

## 17. Agent behavior

An Agent MUST:

- state the fidelity/environment actually used;
- preserve account/tenant/environment identity when material;
- check side-effect authority before external writes;
- use credential references rather than values in durable records;
- distinguish infrastructure/access blockers from observed product defects;
- bound retries/timeouts;
- avoid evidence substitution across material fidelity/environment identities.

An Agent MUST NOT:

- call a mock/sandbox run production PASS;
- invent write authority from credential capability;
- switch accounts/tenants/providers silently;
- retry indefinitely or duplicate unsafe side effects;
- expose secret values in evidence;
- create a new Validation state vocabulary.

## 18. Fast Path and proportionality

Minimal/Fast-Path work need not materialize external-system facts when no external boundary is relevant. If a required test/validation depends on a material external environment, the applicable fidelity/environment/authority facts cannot be omitted merely to stay on Fast Path.

## 19. Failure handling

- required external environment unavailable → `BLOCKED`/`NOT_RUN` according to owning Validation authority;
- account/tenant mismatch → no evidence substitution;
- required write authority absent → do not execute the write; remain blocked/non-run;
- deterministic external contract/product failure after valid execution → preserve FAIL evidence; retries do not erase it;
- retry safety/idempotency unknown for a write → stop before automatic retry;
- fidelity equivalence unknown → do not escalate lower-fidelity evidence.

## 20. Boundary with other owners

- `VALIDATION_STANDARD.md` owns Gate states and exact executed tuples.
- Testing standards own test strategy/profile selection.
- `CONFIGURATION_SECRETS_STANDARD.md` owns secret refs/values and credential handling.
- `WORKSPACE_ARTIFACT_STANDARD.md` owns artifact/evidence class semantics.
- CI/runner standards own execution-channel capabilities.
- Release standards own release/candidate truth.
- T07 owns central adoption/wiring.
