# Build & Artifact Governance Reference

Non-normative guidance for `BUILD_ARTIFACT_GOVERNANCE_STANDARD.md`.

## Minimal build evidence

Record enough identity to answer:

```text
which exact source?
which material build profile?
which toolchain/runtime?
which dependency/input set?
which outputs/digests?
which content-policy checks?
which builder/workflow?
```

A filename such as `app.zip` or tag such as `latest` is a locator, not immutable identity.

## Example — release vs debug

If release and debug profiles differ in optimization, symbols, feature flags or packaging, treat them as distinct build subjects even when they originate from the same source SHA.

## Example — rebuild

Rebuilding source SHA A tomorrow may produce candidate bytes B2 rather than prior bytes B1. Validation or Release evidence for B1 does not transfer to B2 unless the owning evidence establishes the required equivalence.

## Example — content policy

A successful archive step does not prove safe package contents. Inspect or test material exclusions such as `.env`, credential files, caches, local DB/runtime state, Agent scratch files, private keys and unrelated workspace files.

## Promotion worksheet

```text
build_manifest_ref:
output_ref:
immutable_artifact_identity:
promotion_evidence_refs:
content_policy_evidence_refs:
mutable_aliases_if_any:
```

Promotion establishes an artifact identity; it does not establish Distribution publication, Deployment execution or Release qualification.

## Review prompts

1. Is source identity exact?
2. Are material profile/toolchain differences preserved?
3. Is build output being confused with promoted artifact?
4. Is a mutable alias being treated as identity?
5. Are rebuilt bytes inheriting old evidence?
6. Does package-content evidence cover material leakage risks?
7. Are provider-specific conventions being promoted into universal policy without authority?
