# ADS v4.15.0 — L1 Product Evidence (Stage 1 / source draft)

**Status:** `L1_EVIDENCE_DRAFT` — evidence, not Product Freeze or independent Review.
**Stage-0 checkpoint:** [ADS #1207@6283358046](https://github.com/kaicreator-mm/ai-development-standard/issues/1207#issuecomment-6283358046).
**Intake:** [#1207](https://github.com/kaicreator-mm/ai-development-standard/issues/1207), planned bounded concerns [#1208](https://github.com/kaicreator-mm/ai-development-standard/issues/1208), **reuse** [#1205](https://github.com/kaicreator-mm/ai-development-standard/issues/1205), [#1209](https://github.com/kaicreator-mm/ai-development-standard/issues/1209), [#1210](https://github.com/kaicreator-mm/ai-development-standard/issues/1210).
**Frozen predecessor (no mutation):** ADS v4.14.0 released-source baseline `main@584512e8566408bed479192753c12a036309d277`. Stage-1 integration branch `version/v4.15`.
**Related consumers:** [task-meta #10/#12/#14](https://github.com/kaicreator-mm/task-meta/issues/12), [Tally #63/#65](https://github.com/kaicreator-mm/tally/issues/65), Tally real task slice [#62](https://github.com/kaicreator-mm/tally/issues/62).

## L1-1 Problem / actual user
**User request:** have ADS v4.15 define the rules for (1) real task-meta collection, recording and publication **into GitHub**, and (2) how Tally **reads and uses GitHub** ADS records and publishes evidence feedback. The end-to-end evidence must involve actual implementations. ADS v4.14 provided a normalized source-only GitHub v3 Work Item/Intent/Event/Report Envelope, not a live task-meta Publisher or Tally reader.

Affected actors: Agent adapters and task-meta Report Publisher (producer); Tally v2 DomainHarness TypeScript/Node24 C GitHub Adapter + Engineering B/S (consumer); ADS standard publisher/conformance owner; GitHub native Issue/PR/CI/Review fact provider; selected Agent/Host/Tool as measured source.

## L1-2 Observed facts (immutable evidence)
| Evidence / currentness | Actual fact | Relevance |
| --- | --- | --- |
| [ADS v4.14 closure](https://github.com/kaicreator-mm/ai-development-standard/issues/1192#issuecomment-6274795483), main `584512e` | v4.14 candidate passed exact-source CI/Review/RQ, one main merge | Do not reopen historical release |
| `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` blob `ea157842e4780e17cb50697cc687fa7d27128e2a` §§5/8/10/16 | Self-declared Agent identity, passive metadata and Report publication, v3 wrapper, authority separation | Reuse existing normative owner |
| `schemas/github/v4.14/structured-interaction.schema.json` blob `a8c5d852c239f69850e7d856af75ca8179aff1dd` | `kind: report` has fixed type/id/revision/Attempt/Manifest digest/coverage, optional source/correction refs; `additionalProperties:false` | No guaranteed machine-typed Actor/Verifier/Cost/Experience summary visible in GitHub |
| `references/AGENT_EXECUTION_METADATA_COLLECTION_REFERENCE.md` blob `cde978c57c61285c540689d2abc1e6384e0e4326` | Capture provenance, OTel profile/version and observability limits, safe report Markdown | Reuse rather than invent parallel collection or hooks |
| `standards/PROJECT_ADOPTION.md` blob `786cb2a007a15b6f2fca690fc35be1710c33d08c` | Immutable 40-char revision pin; published stable / release and semantic compatibility proof required | Decide qualified-merged SHA vs optional tag without silent weakening |
| [task-meta #12](https://github.com/kaicreator-mm/task-meta/issues/12), [#14](https://github.com/kaicreator-mm/task-meta/issues/14) | Product accepts private capture + GitHub-only safe publication; released-version wire adoption unresolved; implementation NOT_RUN | Real producer/accepted source pin are external dependencies |
| [Tally #65](https://github.com/kaicreator-mm/tally/issues/65), [#62](https://github.com/kaicreator-mm/tally/issues/62) | New TypeScript/DomainHarness Engineering Center, C GitHub reader; no direct task-meta API/object/SDK; Product/L2 and real slice unimplemented | Consumer must use only actual GitHub |
| [ADS #1199](https://github.com/kaicreator-mm/ai-development-standard/issues/1199), [#1205](https://github.com/kaicreator-mm/ai-development-standard/issues/1205) | Existing wider Agent management and exact GitHub-visible report gap proposals | Only narrow cross-project interoperability enters v4.15 |

## L1-3 User-critical journeys
**J1 Producer:** One real supported Agent performs an ADS-pinned task; task-meta captures source-qualified Task/Run/Attempt/Step/Tool/Model/Verifier/Time/Token/Cost or explicit UNKNOWN per field, stores private immutable evidence, publishes ONE safe version-compatible bounded GitHub Report; GitHub readback confirms its accepted comment/revision and original source. Private details are not disclosed to Tally.

**J2 Consumer:** A real TS Tally GitHub reader with **GitHub-only** credentials consumes Issues/native dependencies/PR/CI/Review, current ADS Event/Report/Task Learning and a published Task Report summary. It reconstructs Task/Attempt/Actor, exact code/ADS subject, strict vs partial independently sourced verification, measured/estimated/unknown expenses and applicable experience or INSUFFICIENT_EVIDENCE, **without** task-meta API/DB/object/Manifest/raw trace access. It publishes its own usage/decision/outcome feedback to GitHub.

**J3 Reconciliation:** Retries after accepted remote POST with lost ACK, duplicate/corrected reports, two Attempts, stale source, partial pass with failed mandatory verifier, misattributed logical actors (same GitHub transport), missing tokens/actual billing, pagination/429 and privacy-sensitive raw event. Neither Task nor Gate nor Kernel Effect truth may be minted by Report shape or telemetry. Recovery and negative results are visible.

## L1-4 Domain boundary (do not duplicate authority)
- **ADS** = normative Task/Agent/measurement/interop/compatibility/Validation/Release rules; declarative conformance fixtures. No running collector, GitHub Publisher service, Tally scheduler, Domain Package builder, second Gate or new Agent RPC.
- **task-meta** = native source adapters, capture/correlation/immutable private store, bounded ADS GitHub Report publishing and actual provider observations. Does not decide Task gates/Agent eligibility.
- **GitHub** = durable native Issue/Dependencies/Claim/PR/CI/Review and permitted source-qualified ADS comments; comments are reports/evidence, not canonical Task state mirror.
- **Tally v2** = reads/writes ADS-compliant GitHub evidence through C GitHub only; selects Agents, analyzes experiences and coordinates Engineering B/S workflows. No direct task-meta data channel.
- **DomainHarness K** = Domain App admission/State/Journal/Effect/Replay/UNKNOWN authority; actual remote Host/Provider remains authority for its terminal external I/O.
- **Domain Package evolution** is separate Tally/DomainForge/Harness work; v4.15 only specifies bounded evidence preconditions needed at this GitHub interchange.

## L1-5 Product questions to disposition in PRD/L2
1. Can a deterministic, privacy-safe, bounded *existing* v3 Report Markdown profile suffice for Tally's GitHub-only reader without private manifest, or is a **new versioned machine contract** unavoidable? Must demonstrate positive/negative counterexamples; no undeclared keys in frozen v3.
2. How does a producer map observed vs inferred/self-reported/unknown metrics, root nested counts, retries, model identity, cost pricing revision and verifier evidence to GitHub without declaring false precision? Existing §10 is already normative; only missing consumer projection belongs here.
3. Which immutable ADS revision and qualification/publication evidence allow a lawful **consumer pin** when the qualified and merged v4.14 baseline intentionally lacks an optional Tag? Require actual compatibility evaluation; reject floating `main`.
4. Which Task/Attempt/Report identity, revision/correction and native GitHub readback rules can Tally use without double counting or recasting an Agent self-report as terminal authority?
5. What is the **smallest real cross-repository vertical slice**? One supported Agent/Host + one actual task-meta Publisher + one real Tally GitHub Reader; wider ZCode/Claude/Codex support is not a release obligation.
6. If external producer or consumer does not exist by ADS Candidate Freeze, is release status honest BLOCKED vs an authorized narrower source-only version? The Product objective requires **real E2E**, so fixture-only PASS is insufficient for v4.15's full success.

## L1-6 Risk and test basis
Material classes for anticipated changed **normative** source: `protocol/wire compatibility` (report profile), `cross-project behavior` (reader semantics), `authority/security/privacy` (self-report vs verifier, private Manifest, credential), `release/adoption` (exact pin vs published stable). For actual implementation changed paths the effective-risk inventory will be refreshed by inspecting that diff at exact SHA; this L1 inventory does NOT certify future edits as absent.

**Required independent Product Review:** yes, new public consumer contract + release/authority/compatibility sensitive impact. Product Freeze is a later distinct Product authority action; evidence/Review alone do not freeze. L2 unknown proof, bounded real smoke, independent implementation Review and release qualification belong to later stages.

**Not yet proven:** task-meta agent adapter and writer, Tally TS reader, Github-only E2E, private object ACL, actual remote CAS and affected adopter compatibility. No synthetic PASS.
