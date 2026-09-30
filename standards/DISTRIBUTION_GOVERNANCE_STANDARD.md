# Distribution Governance Standard

Status: **Normative — v4.4**

## 1. Purpose

This standard governs publication/distribution facts for already-identified immutable artifacts. Distribution is optional and does not own canonical artifact bytes identity, Release qualification, or Deployment execution.

## 2. Authority boundary

Owned here:

- whether and where an immutable artifact was published;
- publication locator/registry/channel facts;
- evidence binding publication to immutable artifact identity where the mechanism supports it;
- publication replacement/repointing semantics;
- explicit NOT_APPLICABLE posture when no distribution mechanism is material.

Not owned here:

- artifact construction/promotion identity — Build & Artifact Governance;
- Release READY/PASS — Release authority;
- environment rollout/result — Deployment Governance;
- provider-specific registry/package-store implementation.

## 3. Immutable artifact binding

A distribution claim SHOULD bind the publication to the immutable artifact identity established by the artifact owner. A registry digest, checksum/content digest, immutable package revision or equivalent mechanism-specific evidence MAY support that binding.

A mutable locator alone is not sufficient proof of bytes identity.

Forbidden inference:

```text
tag/channel/package-name points somewhere -> exact qualified bytes established
```

## 4. Mutable aliases

Tags, channels, package names, URLs and similar aliases MAY be useful locators. They MUST remain distinguishable from canonical immutable artifact identity.

If an alias is repointed or the bytes behind a mutable locator are replaced, prior qualification/publication evidence for the old immutable artifact MUST NOT transfer to the new bytes merely because the locator text is unchanged.

## 5. Publication result is not Deployment result

Publication success means only that the distribution operation established the publication fact it actually proves. It does not prove that any target environment fetched, activated, rolled out or successfully ran the artifact.

Required negative:

```text
publication success != Deployment success
```

Likewise, Release READY does not follow from publication alone.

## 6. Optionality and NOT_APPLICABLE

Distribution is not mandatory for every product or change. A local library, internal source-only tool, documentation-only package or other product may truthfully record Distribution as NOT_APPLICABLE when no publication concern is material.

NOT_APPLICABLE requires truthful scope/rationale where material; it is not a way to hide a required distribution step.

## 7. Publication evidence

A useful publication record/reference may capture:

```text
immutable_artifact_ref
publication_system_ref
locator / alias / channel
publication_time or operation ref
publication evidence/digest ref
operator/authority ref where material
replacement/repoint history ref where material
```

v4.4 does not mandate a standalone Distribution schema. Existing project/provider evidence MAY be referenced when it preserves these semantics.

## 8. Required forbidden inferences

| Input fact | Forbidden conclusion |
|---|---|
| tag/channel exists | immutable artifact identity proven |
| same alias after repoint | old artifact qualification transfers |
| upload/publish command succeeded | Deployment succeeded |
| artifact published | Release READY |
| locator resolves | bytes equal previously qualified bytes |
| distribution optional | required publication may be skipped without authority |

## 9. Failure handling

If a publication system cannot expose immutable binding, record that limitation and require alternative evidence appropriate to the owning project. Do not upgrade mutable locator evidence into canonical bytes identity.

If publication truth requires an unavailable external registry/provider, create an exact-subject Validation handoff or leave the dimension NOT_RUN/BLOCKED. Simulated publication cannot become real publication PASS.
