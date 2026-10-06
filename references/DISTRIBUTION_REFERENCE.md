# Distribution Governance Reference

Non-normative guidance for `DISTRIBUTION_GOVERNANCE_STANDARD.md`.

## Publication worksheet

```text
immutable_artifact_ref:
publication_system_ref:
locator_or_alias:
immutable_binding_evidence_ref:
operation_ref:
replacement_or_repoint_ref:
applicability:
```

The artifact ref should point to immutable identity from Build & Artifact Governance. The locator may be mutable.

## Example — container registry

A digest can bind exact image bytes. A tag such as `stable` is a locator that may move. If `stable` is repointed, qualification for the prior digest does not transfer.

## Example — package repository

A package/version locator is useful only to the extent the repository gives trustworthy immutability or content-digest evidence. If a provider permits replacing bytes under the same visible version, record that limitation rather than treating the version string as immutable identity.

## Example — no distribution

An internal source-only tool may set Distribution NOT_APPLICABLE when no publication is part of the Product/Release path. Do not create an empty fake registry record.

## Review prompts

1. What immutable artifact is being published?
2. Does the publication system preserve an immutable binding?
3. Is a mutable alias being promoted into identity?
4. Was an alias repointed or content replaced?
5. Is publication success being misread as Deployment or Release success?
6. Is Distribution actually applicable to this product/change?
