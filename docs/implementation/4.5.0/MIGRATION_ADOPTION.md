# v4.5 Operations / Incident / Maintenance Adoption

Status: v4.5 T08 central adoption guidance. This is **wiring**, not a new lifecycle, Operations, Testing, Validation or Release authority. Read the *exact pinned revision* of `standard-manifest.json`, `standards/PROJECT_ADOPTION.md`, and `templates/project/.dev-standard/PROJECT_OVERRIDES.md` before making project claims. The normative owner documents are `standards/OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md`, `standards/INCIDENT_RECOVERY_FEEDBACK_STANDARD.md` and `standards/MAINTENANCE_EOL_HOTFIX_STANDARD.md`; their corresponding `references/` documents are engineering guidance, not alternate owners. T01's `schemas/runtime-observation-context-v1.schema.json`, `schemas/incident-event-v1.schema.json` and `schemas/maintenance-policy-v1.schema.json` describe machine records, not lifecycle verdicts. Verify actual paths at the pinned revision; never substitute `main` or stale names.

## Scoped applicability, independent of A0–A4

Projects declare independently whether `v4.runtime`, `v4.incident`, and `v4.maintenance` apply and why. Do not derive applicability from repository profile or adoption level alone. For each applicable capability, identify owning Product/Architecture/Task requirement, exact subject identity, evidence source and environment when material, required validation, and its implementation state. `NOT_APPLICABLE` requires an affirmative *non-materiality reason*, not just missing infrastructure. Applicable but not executed is `NOT_RUN`; applicable but unable to execute due to missing runner, authority, telemetry, secrets clearance, or environment is `BLOCKED`. An unassessed requirement is not `NOT_APPLICABLE`; resolve it or preserve `NOT_RUN/BLOCKED` until authoritative scope is known. Applicability of one capability does not force the others: a non-runtime library can omit deployed runtime/incident observation while retaining a real maintenance/support policy.

| Project scenario | Runtime | Incident | Maintenance | Claim boundary |
|---|---|---|---|---|
| Pure non-deployed library with no owned runtime or on-call incident workflow | `NOT_APPLICABLE` with project rationale | `NOT_APPLICABLE` with project rationale | Evaluate independently; may apply to support lines/backports | No invented runtime-health or incident infrastructure. |
| Running service with required but unavailable telemetry | `BLOCKED` if prerequisites prevent required execution; otherwise `NOT_RUN` | Independently assess incident materiality and evidence | Independently assess support obligations | Signal silence and deployment success are not health. |
| Runtime service with incident workflow but no approved real production mutation | Scoped observation evidence according to requirement | Controlled simulation can prove only conformance; real side effects remain `BLOCKED` if required | Independently assess | Do not call simulation a real production incident. |
| Maintained library with backported fix | Runtime may be `NOT_APPLICABLE` | Incident may be `NOT_APPLICABLE` | Applicable and result-SHA validation required | Source validation and branch/tag presence do not establish backport support or PASS. |

`v4.adoption_level` remains `A0_COMPATIBILITY` through `A4_FULL_ORCHESTRATION` under existing v4 rules. A0/A1 projects can record scoped facts manually; later levels may validate adopted machine records or derive automation. Automation cannot invent owning facts, downgrade required gates, or create a universal runtime-health gate.

## Owner routing, reference only

- **Runtime observation:** `standards/OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md`; reuse exact artifact/deployment/environment identity owned by v4.4. Deployment success **does not** imply runtime health; distinguish health/readiness, liveness, performance/resource, error and business dimensions. Use T01 Runtime Observation Context only where applicable; classify missing required evidence truthfully. No mandated backend/SLO/threshold.
- **Incident and feedback:** `standards/INCIDENT_RECOVERY_FEEDBACK_STANDARD.md`; keep incident events append-oriented. `DETECTED != MITIGATED`, `RECOVERED != VERIFIED`, and verification does not complete follow-up. Route new changes to normal engineering work and the existing v4.2 recovery owners. No retroactive rewriting of past Release/Deployment truth.
- **Maintenance and backport:** `standards/MAINTENANCE_EOL_HOTFIX_STANDARD.md`; explicit support authority, line, baseline, and source→result provenance. Branch/tag/package presence is not support status. A backport must have its own result-SHA focused validation, required broader validation and applicable review; urgent Fast Path cannot waive required gates.
- **Testing and Test Data:** `standards/TESTING_STANDARD.md` and `standards/TEST_DATA_AND_SCENARIO_STANDARD.md` continue to own test truth and scenarios. Current sibling T05/T06/T07 conformance fixtures must be discovered on the eventual integrated target, not assumed from this frozen T08 baseline.
- **Validation, Release and project adoption:** `standards/VALIDATION_STANDARD.md`, `standards/RELEASE_STANDARD.md` and `standards/PROJECT_ADOPTION.md` retain their authority. A T08 source test PASS is neither independent integration Validation nor Release Qualification. Any required unavailable real tuple remains `NOT_RUN/BLOCKED`; a PR may merge only after its current-target required gates and fresh independent review.

## Migration steps and historical compatibility

1. Pin the exact standard commit and verify `.dev-standard/VERSION`; preserve prior v3.4/v4.1/v4.2/v4.4 files, facts, owners and exact identities.
2. Select and document the independent applicability of runtime, incident and maintenance; record reasons and owning requirements in project overrides. Assess actual implementation and evidence availability separately from applicability.
3. Discover the three standards, their matching references and T01 machine contracts from the pinned manifest; do not copy or redefine normative owner text into overrides, checklists, Testing, Validation or Release.
4. Adopt incrementally within the existing A0–A4 adoption level. Only apply schema conformance to records that are actually created. Do not reclassify old records, retrofit historical releases/incidents/support policy, or infer past runtime health from deployment logs.
5. Where a current version explicitly requires runtime observations, incident recovery or backport evidence, retain its real exact-subject validation and independent review requirements. Missing prerequisites remain `NOT_RUN/BLOCKED`, never synthetic PASS or `NOT_APPLICABLE`.
6. Validate the combined **current** integration candidate, including any sibling T05/T06/T07 artifacts material to discoverability. Rebind stale HEAD/base/tree/test results after merges; T08's standalone source checks do not authorize merging or Version Closure.

## Forbidden inferences

- Deployment/activation successful → runtime healthy: **forbidden**.
- Telemetry backend alive, silence or no alerts → healthy: **forbidden**.
- Simulated observation/incident → real production execution: **forbidden**.
- Incident recovered → incident verified/follow-up completed: **forbidden**.
- Backport source PASS → result-SHA PASS: **forbidden**.
- Support branch/tag present → supported: **forbidden**.
- Adoption A0/A1 or non-runtime profile → skip a separately required gate: **forbidden**.
- Required but missing capability → `NOT_APPLICABLE`: **forbidden**.
- Legacy release/incident/support record → newly v4.5-conformant historical record: **forbidden**.
- T08 test PASS or PR PASS → Version Closure PASS: **forbidden**.
