# ADS v4.15 — L2 Architecture Evidence / UNKNOWN disposition (R0)

**Status:** `ARCHITECTURE_EVIDENCE_DRAFT / L2_REVIEW_NOT_RUN / L2_NOT_FROZEN`.
**Frozen Product:** [Product Freeze #1207@6284631551](https://github.com/kaicreator-mm/ai-development-standard/issues/1207#issuecomment-6284631551) and [checkpoint](PRODUCT_FREEZE.md); PRD blob `fbeacd479f5a9a0d3dc1a3f853abe623cc211031`, L1 blob `34a8833056e8a3e31ba2238777fde21e816ce6ac`; accepted subject `4b1863812b74265bf1d239b1b0da93c6b8a34a6a`.
**Integration:** `version/v4.15` from v4.14.0 qualified main `584512e8566408bed479192753c12a036309d277`. Subsequent Stage-1 checkpoint commits are non-semantic additive files; the accepted Product blobs are immutable.

## A. Inspected source, actual fact and architecture consequence

| Source at baseline immutable Blob | Inspected fact | Architectural effect / consumer |
| --- | --- | --- |
| `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md@ea157842e4780e17cb50697cc687fa7d27128e2a` §§5/8/10/16 | Normalized v3 marker/YAML; report pub/dedupe/correction; logical actor and passive telemetry, authority vs format | Normative **owner remains this protocol**; v4 version branch makes minimal prospective amendment, not a second protocol |
| `schemas/github/v4.14/structured-interaction.schema.json@a8c5d852c239f69850e7d856af75ca8179aff1dd` | Root `schema=ads/github/v3`, `kind` oneOf; `report.data.additionalProperties=false`; manifest required for all report kinds | **New schema identity** is necessary for typed GitHub-visible summary and manifest-free feedback; preserve old Blob and historical v3 |
| `references/GITHUB_STRUCTURED_INTERACTION_REFERENCE.md@5d8ff3ffc470477558e0aa84b287a3edb3a6a9d1` | Current v3 examples, one canonical record, source-only `SHAPE_VALID_ONLY` | v4 examples reference canonical path/format; Markdown prose never machine truth |
| `references/AGENT_EXECUTION_METADATA_COLLECTION_REFERENCE.md@cde978c57c61285c540689d2abc1e6384e0e4326` | OTel as optional versioned source, per-provider hook coverage/quality; private immutable object and GitHub sanitization guidance | #1208 only specifies evidenced missing **published summary/consumer projection**; task-meta owns adapters, DB/spool and private data |
| `standards/PROJECT_ADOPTION.md@786cb2a007a15b6f2fca690fc35be1710c33d08c` | Exact 40-hex revision; v4.12 advisory auto-selector requires release/tag; material semantic compatibility separate | **Manual** qualified+merged immutable main SHA choice under project-local §6 despite no tag, old selector unchanged; test-only frozen candidate before RQ |
| `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md@15e355f6ec86370599f2dda7b61963d93fead66f` | Explicit source/wire/behavior/authority, baseline and candidate, protected consumer windows | v4 needs new schema id; v3-v4 reject/read historical matrix; no silent v3 schema edit |
| `standards/VALIDATION_STANDARD.md@1522b85f9e68cc4a1591ea5899b53c224998e5a8` | Exact verification tuples; actual execution required for PASS; no evidence from parser alone | GitHub Report source claims `SHAPE_VALID_ONLY`; Task/Release validation remains independent |
| `standards/RELEASE_STANDARD.md@da82aa7d387d8f190c4ddff88b4c8782af804ac4` | Candidate RQ independent; optional Tag/Release are aliases | RQ requires real external producer/consumer E2E; frozen candidate proof precedes qualified adoption |
| [task-meta #12](https://github.com/kaicreator-mm/task-meta/issues/12), [#14](https://github.com/kaicreator-mm/task-meta/issues/14) | task-meta actual writer/adapter not yet implemented, selected final ADS wire contract unresolved | External implementation dependency; ADS can ship design/test oracle but **no external E2E PASS** without code |
| [Tally #63](https://github.com/kaicreator-mm/tally/issues/63), [#65](https://github.com/kaicreator-mm/tally/issues/65), [#62](https://github.com/kaicreator-mm/tally/issues/62) | TS/DomainHarness v2 design; C GitHub-only reader and real vertical slice unimplemented | Keep C GitHub only; external consumer implementation is independent blocker to cross-system Release |

## B. Architectural invariants

1. One fixed first-line `<!-- ads:github -->`, one fenced YAML mapping of **exactly** `schema`, `kind`, `data`; no KEY=VALUE or Markdown-as-machine alternate path. `schema: ads/github/v4` identifies new current report family; v3 canonical schema stays unchanged.
2. Only `kind: report` gains v4 typed execution/feedback semantics; Work Item, Intent and Event retain existing native GitHub and original Task/Agent Event authority. Use local `$ref` or source-bound schema definitions without drift, not Python-only field logic.
3. A report is an **observation with source**. `SHAPE_VALID_ONLY` cannot become Task PASS, authorized Claim, Gate/Review verdict, Provider remote completion, DomainHarness K effect, or a transferable Package credential.
4. `EXECUTION_SUMMARY` is task-meta-published from observed/private immutable evidence; `EXPERIENCE_USE_FEEDBACK` is Tally-published from GitHub native facts and its **own** action evidence, without any private task-meta manifest.
5. GitHub-only means Tally's *entire* relevant input dependency is GitHub; no direct task-meta API/store/SDK/object/Manifest/Trace. Live credential scopes and absence/denial of private egress must be witnessed, not asserted.
6. Published data is bounded and redacted. Duplicate/new-revision/correction/edited-history, privacy-removal tombstones and GitHub rate limits preserve uncertainty; missing billed cost, temporal provenance, independent verifier, experience relevance = UNKNOWN/INSUFFICIENT_EVIDENCE.
7. Full ADS v4.15 Release Qualification requires actual producer + actual consumer code on real GitHub. A static demo/schema test alone **cannot** replace the external E2E Product requirement.
8. Immutable code/ADS/Task candidate under test is separate from effective consumer adoption. During pre-RQ compatibility E2E, isolate the *frozen candidate* as test subject in a bounded smoke project; never change production project-local pin or active accepted Claim.

## C. Architecture drivers / material UNKNOWN and disposition

| ID | Material question | Evidence / provisional answer | Disposition (Stage-2 R0) | Release effect |
| --- | --- | --- | --- | --- |
| U1 | Can v4 manifest-free feedback exist within a single report family without retroactive v3 wire mutation? | JSON Schema Draft 2020-12 v3 strict discriminator: a **separate root schema identity** can express conditional required sets under report_kind. No external wire change until v4 accepted. | `STATIC_EVIDENCE_SUFFICIENT` for L2 design; executable valid/invalid schema oracle remains implementation Task. | v4 schema negative tests required |
| U2 | Can v3/v4 clients fail closed without schema alias confusion? | Exact `schema` discriminator and pinned offline schema registry; v3 reader only v3, v4 reader v3 read-only historical + v4 current. | `STATIC_EVIDENCE_SUFFICIENT` for architecture; executable cross-version parser tests still required. | Real adapter compatibility negative required |
| U3 | Can Tally prove it is GitHub-only and has no private collector read capability? | Credential/permission and egress model can be described with Github-only token grants + executable deny-list or isolated network; v4 PRD requires actual witness. | `EXECUTABLE_DEMO_REQUIRED` for **actual E2E acceptance**, not a new normative source authority; scope one true Tally TS reader environment. | Missing real reader⇒`BLOCKED/NOT_RUN` |
| U4 | Does a GitHub POST timeout yield genuine exactly-once? | v3 §16.3 derived key + source readback; simultaneous writers/GitHub updates are not atomic. | `STATIC_EVIDENCE_SUFFICIENT` for bounded dedupe semantics; no cross-writer exactly-once assertion. | Retry/collision negative tests |
| U5 | Can pre-RQ candidate be tested without silently adopting a release? | Isolated smoke Issue/repo + explicitly selected immutable *candidate validation subject* and unchanged production `.dev-standard/VERSION`/Claims. | `STATIC_EVIDENCE_SUFFICIENT` for architecture; actual GitHub smoke with pinned consumer source required. | Test subject drift invalidates witness |
| U6 | Are real task-meta writer and Tally TS GitHub Reader available? | As of Stage-1 R0 independent review: task-meta repository has no code; Tally TS v2 new reader not built. | `BLOCKED` for external E2E **now**; architecture scope defines smallest vertical implementation in owning repos. No synthetic adapter as substitute. | **Full v4.15 RQ BLOCKED** until live implementations |
| U7 | Do existing v3 passive metadata classes need a second new telemetry schema? | §10 already owns observed/self-reported/inferred/UNKNOWN/source data. | `STATIC_EVIDENCE_SUFFICIENT`: **reuse** owner; #1208 only real missing publication/consumer projection and fixtures, no new telemetry platform. | No duplicated contract |
| U8 | Exact GitHub App permissions/PAT scopes necessary for safe Tally-only read and comment feedback? | GitHub native permissions depend on token/provider; distinguish observer (read Issue/PR/Checks/etc) and feedback publisher (Issue-comment write) + report actual effective granted permission scope, deny private access. | `STATIC_EVIDENCE_SUFFICIENT` for split-role architecture; actual provider-scopes/grants witnessed in U3 real test. | R1 Product P2 must close at L2/validation |

**L2 Freeze eligibility:** require independent review of this evidence and [L2_ARCHITECTURE.md](L2_ARCHITECTURE.md), affirmative design sufficiency for U1/U2/U4/U5/U7/U8, and clear conditional ownership of U3/U6. A required **executable architecture demo** must precede L2 Freeze only if static evidence cannot establish the chosen **architectural contract**; actual cross-project execution E2E is a separate explicit Product release requirement. No automatic `PASS` or `NOT_APPLICABLE` for unperformed runtime checks.

## D. Planned actual test ownership (not admitted Task DAG yet)

- ADS #1208: source §10 reuse crosswalk, bounded observation/metric/causal semantics and negative examples.
- ADS **existing** #1205: one schema identity `ads/github/v4`, v3 historical reader, source-only type validator with strict format, one v4 typed execution summary/feedback profile.
- ADS #1209: Tally GitHub-only read/reconcile/use-feedback normative contract, expected credential-scope/egress witness.
- ADS #1210: actual task-meta / actual Tally source commit and controlled E2E evidence, one real Task + negative retry, stale, strict-verifier, privacy, access denial; qualified final version gates. External tasks stay owned by task-meta #5/#12 and Tally #62/#65.
- No autonomous builder Task/PR/Claim authority until separate L2 Freeze and executable Task DAG/current native Issue dependencies.

**R0 limits:** no runtime of task-meta/Tally inspected in this L2 evidence, no v4 Schema built, no v4 external GitHub comment published, no independent L2 review, no Product thaw or new Gate invented.
