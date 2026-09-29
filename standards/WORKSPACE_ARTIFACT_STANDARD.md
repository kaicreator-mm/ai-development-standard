# Workspace & Artifact Governance Standard

## 1. Purpose and authority

This standard is the normative owner for semantic classification, ownership, lifecycle, cleanup, evidence eligibility and promotion of material workspace/artifact data in v4.1.

It intentionally does **not** define the future full v4.4 build/package Artifact Manifest, package/distribution format or Release Qualification verdict. File existence never creates Validation or Release truth.

`schemas/execution-context-v1.schema.json` may project material artifact references using the canonical classes defined here.

## 2. Canonical semantic classes

The canonical v4.1 classes are:

| Class | Meaning |
|---|---|
| `SOURCE` | Human/Agent-authored source that is authoritative input to the work product. |
| `GENERATED_SOURCE` | Generated content treated as source input for subsequent work and governed by a reproducible or explicitly accepted generation process. |
| `BUILD_OUTPUT` | Output produced by compilation/build/transformation; not release/evidence authority by existence. |
| `CACHE` | Reconstructable acceleration data whose loss should not change product truth. |
| `RUNTIME_STATE` | State required by a running or recoverable system/process; not disposable cache by default. |
| `TEST_ARTIFACT` | Output created by test execution for diagnostics/inspection; not automatically Validation evidence. |
| `VALIDATION_EVIDENCE` | Evidence intentionally bound to a Validation subject/profile/result by the owning Validation process. |
| `RELEASE_ARTIFACT` | Artifact intentionally promoted/bound to an authorized release/candidate identity by the owning release process. |
| `SECRET_MATERIAL` | Credential/key/token/private/bearer material requiring secret-handling rules; never ordinary evidence/release content. |

A path/extension alone MUST NOT determine class when semantics differ.

## 3. Ownership

Every destructive lifecycle action requires sufficient ownership knowledge. Ownership may be project, Task/operator, tool/process or an explicitly shared authority.

`unknown` or `unowned` material MUST NOT be destructively cleaned merely to obtain a green workspace or free disk. If ownership cannot be established, preserve it or isolate a new workspace and escalate.

## 4. Mutability and persistence

Class does not imply one universal retention period. Projects MAY define stronger policies, but the following defaults apply:

- `SOURCE` and accepted `GENERATED_SOURCE`: durable under repository/project authority;
- `BUILD_OUTPUT`: mutable/rebuildable unless promoted/bound elsewhere;
- `CACHE`: mutable and reconstructable;
- `RUNTIME_STATE`: preserve according to recovery/runtime ownership; not disposable by default;
- `TEST_ARTIFACT`: retain according to test/debug policy;
- `VALIDATION_EVIDENCE`: immutable or append-oriented once published for an exact subject;
- `RELEASE_ARTIFACT`: immutable after authorized promotion for the bound identity;
- `SECRET_MATERIAL`: retain only as required by authorized secret mechanism and never in ordinary durable evidence.

## 5. Git eligibility

Git inclusion is a project decision, not a class synonym.

`SOURCE` is commonly tracked. `GENERATED_SOURCE` may be tracked or reproducibly regenerated depending on authority. `BUILD_OUTPUT`, `CACHE`, `RUNTIME_STATE` and `TEST_ARTIFACT` are commonly excluded but MAY be tracked when project authority requires it. `SECRET_MATERIAL` MUST NOT enter ordinary Git source unless covered by the explicit encrypted-secret exception in `CONFIGURATION_SECRETS_STANDARD.md`.

Being committed to Git does not upgrade an item to `VALIDATION_EVIDENCE` or `RELEASE_ARTIFACT`.

## 6. Evidence eligibility

Only an artifact intentionally bound by the owning Validation process to the exact subject/profile/result may be treated as `VALIDATION_EVIDENCE`.

A log, screenshot, junit file, coverage file, binary or test output remains `TEST_ARTIFACT` until that binding exists. A cache hit or successful build output is not Validation PASS.

Evidence identity SHOULD include or reference the exact subject and material execution tuple required by `VALIDATION_STANDARD.md`.

## 7. Release eligibility and promotion

An artifact becomes `RELEASE_ARTIFACT` only through authorized promotion/binding to the relevant candidate/release identity.

Promotion requires, as applicable:

- source/build identity or immutable digest;
- producer/build provenance sufficient for the owning process;
- authorized owner/controller;
- target candidate/release identity;
- required Validation/Release prerequisites as defined by their owners.

File presence in `dist/`, an upload bucket, package registry or GitHub artifact store MUST NOT by itself constitute release promotion.

## 8. Cache semantics

`CACHE` must be safely reconstructable from authoritative inputs or be explicitly classified otherwise. If deleting it can destroy unique product/runtime truth, it is not disposable cache.

Cache contents MUST NOT be used as sole proof of successful Validation or Release Qualification.

## 9. Runtime state semantics

`RUNTIME_STATE` includes state such as databases, queues, local service data, resumable job state or other mutable state needed for behavior/recovery.

It MUST NOT be treated as disposable cache solely because it lives under a temporary/workspace directory. Cleanup requires runtime/state ownership and recovery implications to be understood.

## 10. Generated source and build output

Generated material becomes `GENERATED_SOURCE` when the project intentionally treats it as source input/contract and governs regeneration/acceptance. Otherwise generated build products remain `BUILD_OUTPUT`.

A generator output changing does not automatically authorize committing it; Task/project authority decides whether the generated source is part of the write set.

## 11. Test artifacts versus Validation evidence

`TEST_ARTIFACT` captures what a test produced. `VALIDATION_EVIDENCE` is the subset intentionally published/bound by Validation authority.

A passing-looking report copied from another SHA/environment remains historical or unrelated test material; it MUST NOT be relabeled as current Validation evidence by filename or location.

## 12. Secret material

`SECRET_MATERIAL` MUST be handled under `CONFIGURATION_SECRETS_STANDARD.md`. Secret values MUST NOT be promoted into ordinary `TEST_ARTIFACT`, `VALIDATION_EVIDENCE` or `RELEASE_ARTIFACT` merely because tooling captured them.

If an evidence bundle contains secret material, publication must stop or redact/separate it under authorized secret policy before durable evidence handling.

## 13. Cleanup authority

Cleanup decisions MUST consider class, owner, reconstructability, persistence requirements and current consumers.

Safe examples may include rebuilding owned `BUILD_OUTPUT` or deleting an explicitly disposable `CACHE`.

Unsafe examples include:

- deleting unknown workspace files to make `git status` clean;
- deleting runtime database state assumed to be cache;
- deleting test evidence still required by a gate;
- deleting an unpromoted artifact that contains the only unpublished work product.

Unknown ownership/classification fails closed for destructive cleanup.

## 14. Reconstruction

Reconstruction claims MUST identify authoritative inputs and mechanism sufficiently to justify deletion/rebuild. "It looks generated" is not proof of reconstructability.

If reconstruction depends on unavailable external state/toolchain/version, destructive cleanup may be unsafe even for a normally generated artifact.

## 15. Promotion is a semantic transition, not a rename

Copying, renaming, moving, uploading or archiving a file does not by itself change semantic class. Promotion is an authorized binding operation owned by the relevant Validation/Release process.

The same bytes may have multiple references under different lifecycle contexts, but their authority comes from durable identity/binding records, not directory names.

## 16. Fast Path and materiality

Execution Context need only list material artifacts. Minimal/Fast-Path tasks do not need a ceremonial inventory of every cache/temp file.

Materiality does not permit misclassifying a release artifact, evidence item, runtime state or secret as disposable just to avoid recording it.

## 17. Failure handling

- class or ownership unknown before destructive cleanup → `BLOCKED` / preserve and escalate;
- cache contains unique non-reconstructable data → reclassify/resolve ownership before deletion;
- promotion lacks identity/authority → no release/evidence promotion;
- secret material appears in ordinary artifact/evidence flow → stop unsafe publication and follow secret policy;
- artifact identity does not match requested subject/candidate → evidence/release substitution forbidden.

## 18. Boundary with other owners

- `VALIDATION_STANDARD.md` owns Validation PASS/FAIL/BLOCKED and exact-subject binding.
- CI evidence standards own CI evidence publication mechanics.
- `RELEASE_STANDARD.md` owns Candidate/Release Qualification and release promotion authority.
- `CONFIGURATION_SECRETS_STANDARD.md` owns secret value/ref handling.
- `GIT_EXECUTION_STANDARD.md` owns repository/workspace execution safety.
- v4.4 retains ownership of the future full build/package Artifact Manifest.
- T07 owns central discovery/adoption wiring.
