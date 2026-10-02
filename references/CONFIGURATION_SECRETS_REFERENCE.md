# Configuration & Secrets Reference

This document is non-normative guidance for `CONFIGURATION_SECRETS_STANDARD.md`.

## 1. Deterministic precedence example

A project may define:

```text
1. Frozen project contract / typed config schema
2. PROJECT_OVERRIDES execution profile
3. environment-specific non-secret config file
4. CI/process environment injection
5. dispatch-scoped override
6. implementation default
```

If `API_REGION` appears in levels 3 and 4, level 4 wins because authority explicitly says so. File discovery order is irrelevant.

## 2. Non-secret fingerprint example

For material non-secret configuration:

```text
profile_ref=config/prod-readonly-v2
non_secret_fingerprint=sha256:<digest-of-canonical-non-secret-config>
```

Do not include token/password values in the fingerprint input merely to bind them. Secret identity should be represented separately by refs.

## 3. Secret reference example

Good durable record:

```text
secret_ref=github-actions:environment/prod/API_TOKEN
source=github-actions-secret
scope=read:catalog
environment=prod
```

Bad durable record:

```text
API_TOKEN=ghp_xxxxxxxxxxxxxxxxx
```

The bad form is a secret value, even if placed in a private Issue or Validation log.

## 4. Short-lived credential example

A CI job may exchange an OIDC identity for a short-lived cloud credential or use a Vault-like broker. This is preferred when supported because it reduces long-lived secret exposure.

It is not a universal requirement. A legacy deployment may use a project-authorized static credential stored in an approved secret store with rotation and least-privilege controls.

## 5. Encrypted-in-Git example

A project may authorize SOPS-like encrypted material in Git when ciphertext is not directly usable, decryption keys are controlled separately, and decrypted values never enter normal logs/evidence. This does not authorize plaintext `.env` files.

## 6. Credential unavailable scenario

Required:

```text
target=provider sandbox A
credential_ref=ci:sandbox-A/write-token
```

Observed:

```text
credential missing or expired
```

Correct result:

```text
execution BLOCKED / check NOT_RUN
```

Incorrect substitutions:

```text
use production token instead
use another tenant
mock the provider and call it PASS
invent placeholder credentials
```

## 7. Redaction examples

Prefer:

```text
auth=Bearer <redacted>; credential_ref=ci:sandbox-A/write-token
```

Avoid printing a full request/response object if it includes cookies, signed URLs, tokens or private keys. When a signed URL is itself bearer access, treat it as secret value.

## 8. `.env` example

A repository may commit `.env.example` containing non-secret key names/defaults while keeping `.env.local` or equivalent secret-bearing files ignored and local. Another project may not use `.env` at all. Both are conformant when authority/precedence and secret handling are clear.
