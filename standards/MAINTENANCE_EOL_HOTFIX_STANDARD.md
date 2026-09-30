# Maintenance, EOL & Hotfix Standard

Status: **Normative — v4.5**

## 1. Purpose

This standard governs support-line truth, deprecation/EOL posture and maintenance/hotfix execution boundaries. Branch/tag/package existence is not support authority, and this standard does not own Git provenance, Validation, Review or Release results.

## 2. Support policy authority

A supported line or baseline MUST be established by durable project/product maintenance authority. The policy SHOULD state the applicable support status vocabulary, supported baseline/reference and allowed maintenance change classes.

Support vocabulary is project-mappable/extensible; v4.5 does not impose a universal lifecycle enum.

```text
branch exists != line is supported
tag exists != line is supported
package downloadable != line is supported
```

## 3. Deprecation and EOL

Deprecation/EOL decisions MUST have durable authority and, where material, reference replacement/upgrade/migration guidance. EOL does not erase historical artifacts or prior evidence; it changes current support posture under the owning policy.

## 4. Backport / hotfix identity

A backport/cherry-pick/hotfix result MUST preserve provenance linking:

- source change/reference;
- target support line;
- target baseline before change;
- resulting exact SHA/artifact identity;
- applicable result-SHA Testing/Validation refs.

Review/Release refs may be attached when applicable. Git mechanics alone do not establish qualification.

## 5. Evidence non-transfer

Source-branch evidence belongs to the source subject. It MUST NOT automatically transfer to a new maintenance/backport result SHA.

```text
source PASS != backport result PASS
same patch text != same validated subject
```

The resulting exact SHA must obtain its own applicable current Testing/Validation/Review/Release evidence.

## 6. Maintenance Fast Path

Hotfix urgency MAY reduce only ceremony that higher authority has classified as non-required. It MUST NOT bypass material exact-subject Validation, required Review, Release Qualification, mutation/side-effect authority, or required rollback/recovery evidence.

## 7. Failure handling

Unclear support policy, target baseline, maintenance authority or result identity fails closed. If a support line cannot establish its own required evidence, record BLOCKED/NOT_RUN rather than inheriting evidence from another subject.
