# v4.4 Build / Packaging / Distribution / Deployment Adoption

Status: **T07 implementation candidate**, not Version Closure or Release Qualification. This document binds v4.4's Build & Artifact, Distribution and Deployment owners to existing v4/v4.1/v4.2 truth rules; it does not grant an additional delivery-stage authority.

## Applicability profile (project-owned, materiality-driven)

Record the relevant project-selected delivery concerns in the existing `.dev-standard/PROJECT_OVERRIDES.md` only where material:

| Concern | Owner and decision boundary | Truthful non-applicability example |
| --- | --- | --- |
| Build / promotion | Build & Artifact Governance owns exact source/profile/toolchain/output and separately promoted immutable artifact identity; Release owns qualification. | Docs-only change with no produced bytes or promoted artifact. |
| Packaging / installation | Build & Artifact package/content policy and project Product/Architecture determine supported artifact format and material installation tests; platform tuple validation remains with Validation. | Source-only internal change with no distributed/package/install contract. |
| Distribution | Distribution Governance owns publication facts and, where supported, immutable binding to the Build owner artifact; a mutable channel is a locator only. | Private local library or internal executable that requires no publishing step. |
| Deployment | Deployment Governance owns Plan and executed Result for an exact artifact/environment and applicable side-effect authority; Release qualification remains separate. | SDK/library or non-deployed documentation without service rollout. |

Project overrides may select required/conditional/non-material concern applicability and real validation tuples, but MUST NOT weaken a Frozen Product/Architecture/Task gate, material exact-SHA provenance, package-content/security constraints, or required Release Qualification. A deployment CLI, credential, service backend or registry exists => **capability**, never automatic production authority or required global stack. `NOT_APPLICABLE` requires genuine absence of a material concern; unavailable required tooling/environment is `NOT_RUN` or `BLOCKED`, not a fabricated N/A.

Use the smallest truthful profile: a docs-only Fast Path need not produce empty Build/Distribution/Deployment records; an artifact-changing change, required package format, public publication or actual environment rollout cannot skip its material owner evidence. Existing v4 Adoption A0–A4 levels remain independent from delivery applicability. A lower adoption level does not weaken a required delivery concern.

## Discoverability and machine ownership

`standard-manifest.json` should enumerate the three v4.4 normative owners, their three references, the four T01 schemas (`build-manifest-v1`, `artifact-promotion-v1`, `deployment-plan-v1`, `deployment-result-v1`) and each actual owner/T07 focused verifier. Each active new normative standard receives exactly one Golden coverage record in `templates/golden/STANDARD_COVERAGE.json`, linking real positive/forbidden/rationale sections of its owning standard/reference. Discovery, Golden examples and this adoption document are **references**, not second semantic owners or permission to mutate T01–T06 implementations.

The selected Release/Validation/checklist material should **reference** these owners instead of defining generic `SUCCESS/PASS/READY` aliases. An immutable artifact is not proof of publication; publication is not evidence of Deployment SUCCESS; a Deployment Plan is not an executed Result; staging success does not establish production; `Release READY != Deployment SUCCESS` and neither direction is an equivalence. Deployment rollback and v4.2 data/schema rollback remain different owner decisions. Mock/staging fixture success is explicitly test-only and cannot be substituted for an unexecuted real provider/production claim.

## Migration and historical evidence

Historical release artifacts, tags, installation outputs and provider logs retain their original exact subject and claimed evidence strength. No version or stage profile may retroactively rewrite them into new Build Manifest, Artifact Promotion, Distribution publication, Deployment Result, or Release PASS. A new exact-SHA build or new immutable byte identity requires its own applicable qualification even when the version/tag/alias text matches historical evidence. A previous deployment result does not establish current runtime health (owned by v4.5) or a current migration verification result (owned by v4.2).

When adding these v4.4 references to an adopted project, capture the current pinned standard revision, applicable concerns, owner-approved project choices and exact evidence refs. Missing historical proof stays unknown with documented scope; do not invent it for a cosmetically complete migration card.

## Verification / Closure handoff boundaries

T07 focused tests prove inventory, Golden uniqueness, project-profile non-weakening and additive discoverability at their executed SHA. They do **not** prove a real package installation, registry upload, production deployment or qualified release. T05/T06 own their own conformance/dogfood/real-environment evidence where material; T08 integrates those results and prepares separate Version Closure inputs. T07 MUST NOT declare their PASS or any Release/Version Closure verdict. A missing real environment or provider proof becomes a separate exact-subject Validation Request and remains `NOT_RUN`/`BLOCKED` until actually exercised.