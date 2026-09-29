# ai-development-standard v4.5.0 PRD — Operations, Incident & Maintenance

Status: **DRAFT PRODUCT AUTHORITY — requires L1 Product Evidence review and explicit PRD Freeze before implementation**

## 1. Product intent

v4.5.0 extends the standard beyond deployment into runtime operations. The objective is to make production behavior observable, failures recoverable and maintenance/support decisions explicit, without turning ADS into an infrastructure platform or prescribing one monitoring stack.

The version should let a project answer:

1. Is the deployed system healthy, and what evidence supports that conclusion?
2. Can material user-visible/runtime failures be diagnosed without ad-hoc access?
3. What happens when a production incident occurs?
4. How does an incident become a regression, Hidden/Visible coverage update or product/architecture correction?
5. Which versions are supported, maintained, deprecated or EOL?
6. How are hotfix/backport/maintenance releases governed without weakening current release truth?

## 2. Problem

Current ADS is strong through Candidate/Release and will gain Deployment in v4.4, but after rollout there is no unified normative owner for observability, incident recovery or product-version maintenance.

Without such standards, projects may:

- declare a deployment successful without enough runtime observability to detect latent failure;
- conflate liveness/readiness/health/business success;
- leak secrets or PII through logs/telemetry;
- perform production fixes without a durable incident record or regression path;
- repeatedly rediscover the same failure because incidents never feed tests/scenarios/Hidden Validation;
- maintain unsupported branches indefinitely or backport changes without explicit support policy;
- treat a hotfix as exempt from normal exact-SHA/release evidence.

## 3. Scope

### 3.1 Observability Standard

Create a technology-neutral standard for runtime evidence. It should support, where applicable:

```text
logs
metrics
traces
health / liveness / readiness
business/critical-journey runtime signals
alerts
runtime version/artifact identity
```

Required principles:

- critical runtime behavior should be observable at a level proportional to risk;
- health, readiness and liveness are distinct concepts where the platform uses them;
- user-visible failures should be diagnosable through bounded identifiers/context rather than secret-bearing raw dumps;
- runtime evidence should bind version/artifact/environment identity when material;
- secret/credential/unapproved PII MUST NOT be emitted as ordinary telemetry;
- observability quality is evidence input, not automatic proof that product behavior is correct;
- SLO/SLI targets are project/product authority, not universal ADS thresholds.

### 3.2 Incident & Recovery Standard

Define a minimal incident lifecycle such as:

```text
DETECTED
→ CLASSIFIED
→ CONTAINED / MITIGATED
→ RECOVERED
→ VERIFIED
→ FOLLOW_UP / CLOSED
```

The exact state model may be refined in L2, but must preserve these semantics:

- incident severity/impact is evidence-based and project-defined;
- emergency mitigation and permanent fix are distinct;
- recovery may involve rollback, failover, configuration correction, data repair or forward fix;
- an incident record should preserve affected version/artifact/environment and timeline/evidence sufficient for later diagnosis;
- incident handling MUST NOT rewrite previous Release/Deployment evidence; it adds new runtime facts;
- material product defects should create a durable follow-up path.

### 3.3 Incident → Engineering Feedback Loop

Establish the canonical learning loop:

```text
Production Incident / Escaped Defect
        ↓
Minimal Reproduction
        ↓
Regression Case / Scenario
        ↓
Visible Test / Hidden Pack / Architecture / Product gap classification
        ↓
Fix Task
        ↓
Validation / Release
        ↓
Standard or project-rule feedback when systemic
```

The standard should compose with existing `TEST_DATA_AND_SCENARIO_STANDARD.md` and `RELEASE_STANDARD.md` escaped-defect classifications.

### 3.4 Maintenance & EOL Standard

Create explicit lifecycle concepts for product versions, such as:

```text
CURRENT
MAINTENANCE
SECURITY_ONLY
DEPRECATED
EOL
```

Projects may use a different vocabulary, but must be able to represent:

- currently supported line(s);
- allowed change classes per support state;
- hotfix/backport authority;
- security-fix policy where applicable;
- deprecation/EOL announcement/effective date when external consumers matter;
- maintenance branch/source baseline identity;
- migration/upgrade guidance to a supported line.

### 3.5 Hotfix / Backport Governance

Define a bounded path for urgent fixes that reduces ceremony without weakening truth.

Required rules:

- hotfix scope is minimized and explicit;
- backport/cherry-pick provenance is recorded;
- exact-SHA testing/validation remains truthful;
- release qualification may use a risk-adjusted Fast Path only if project authority permits it;
- emergency deployment does not retroactively become normal PASS without required follow-up evidence;
- follow-up tasks may be mandatory for skipped/non-blocking evidence.

## 4. Non-goals

v4.5 does not:

- prescribe Prometheus, OpenTelemetry, Grafana, Sentry, PagerDuty or a specific observability stack;
- establish universal SLO values;
- replace organization-specific incident management/compliance policy;
- authorize production data access by default;
- make every minor runtime warning an incident;
- exempt hotfixes from immutable identity, testing or release truth.

## 5. Cross-standard model

```text
Release-qualified Artifact
        ↓
Deployment
        ↓
Runtime
        ↓
Observability
        ↓
Healthy ──────────────┐
        │             │
        └→ Incident → Recovery
                     ↓
                Engineering Feedback
                     ↓
         Product / Architecture / Test / Standard
```

The lifecycle is a feedback system, not a one-way pipeline.

## 6. Machine-readable expectations

L2 should evaluate lightweight records for:

- Runtime Identity / Deployment-to-runtime binding;
- Incident Record;
- Recovery/Verification Result;
- Maintenance Policy / Version Support Matrix;
- Backport/Hotfix provenance.

Do not require centralized telemetry storage to conform to ADS; durable references may point to approved external systems when policy permits.

## 7. Compatibility posture

Target: additive/non-weakening minor release. Projects without production deployment remain able to mark operational capabilities NOT_APPLICABLE with rationale. Historical releases are not retroactively assigned operational evidence that did not exist.

## 8. Product acceptance

v4.5.0 is complete when:

1. Observability, Incident/Recovery and Maintenance/EOL have clear normative ownership;
2. deployment success is not equivalent to runtime health;
3. runtime evidence is version/artifact/environment attributable where material;
4. incident handling has a deterministic engineering-feedback path;
5. security/privacy constraints apply to telemetry and incident evidence;
6. maintenance/hotfix/backport policy cannot silently weaken exact-SHA/release truth;
7. one real or simulated production-incident dogfood demonstrates detection → recovery → regression/follow-up closure.

## 9. Next gate

Before Freeze:

1. run L1 Product Evidence against mature SRE/observability/incident/version-maintenance practices;
2. verify overlap with Release, Deployment, Testing and Test Data standards;
3. revise and Freeze this PRD;
4. run L2 Architecture Evidence;
5. generate Task DAG with observability/incident/maintenance/conformance lanes where safe.
