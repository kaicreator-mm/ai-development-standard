# S05 ADS source conformance and downstream handoff

Task [#1227](https://github.com/kaicreator-mm/ai-development-standard/issues/1227).
The [machine-readable matrix](S05_CONFORMANCE_MATRIX.json) maps every frozen
R4 §3 obligation to actual source commands. Exact tested commit/tree, exits,
platform/toolchain and independent Review belong to the post-commit GitHub
receipts. This document is a contract/checklist, not its own PASS certificate.

## Accepted source lineage and scope

The operative overlay is [R4 at 4e914369](https://github.com/kaicreator-mm/ai-development-standard/blob/4e91436944734a3a4314c9f36cb69e530080d02a/docs/implementation/4.15.0/SCOPE_REVISION_R3.md),
separately frozen by Product/L2/DAG decisions #1207@6295923251,
6295930232 and 6295938443. It is integrated at
`2c1e0a8f98c628e0257ac52e0f27fd8ebbfdf6dc`, ratified
[#1207@6325920318](https://github.com/kaicreator-mm/ai-development-standard/issues/1207#issuecomment-6325920318).
The immutable predecessor files retain their historical status text; the actual
Freeze/overlay decisions govern. They are not rewritten to advertise acceptance.

| Source concern | Exact source / actual final delivery |
| --- | --- |
| S01 observation/capture contract | `fc8e29ce50e39b648c81fba2390b4e25aa246bd2`; #1215@6320071314 |
| S02 report schema/parser/JCS/revision helpers | `11d008378b7674519cd9a432e62acec19cd13fc1`; #1216@6321144360 |
| S03 GitHub-only consumer/feedback contract | `d3e794cc85785c1cce86c4be60a80ac95c35f5b0`; #1217@6324813478 |
| S04 exact-qualified-main manual adoption | `9d295a20566133bbdcfd1bdfbbf28cca3713fc2f`; separate repair #1252@6325777070 and original final #1218@6325787365 |

Original S01/S04 execution keys remain UNKNOWN/HOLD. Source acceptance does not
recover their missing ledger, generation, resource state or terminal. No old
Claim or historical CI is promoted into a current source permission.

## What deterministic execution covers

The tests exercise the actual report-only schema/parser/digest helpers and a
clearly named **test-only** finite consumer oracle. The integrated cases chain
publication-shaped YAML, public digest, supplied native readback, immutable late
evidence/learning revisions, conflicts, corrections and feedback. They preserve
missing cost/verifier information and failed/skipped/unchecked scope. Nineteen
green checks and a Tool ACK remain observations; neither produces Task PASS.

Lost-ACK/429/page/retry cases supply response observations, not an HTTP client.
Same identity/digest duplicates are not additional Attempts. Conflicting valid
digests dominate even when source witness/currentness is UNKNOWN; foreign
native owning scope and invalid schema cannot poison an unrelated collection.
An incomplete collection cannot prove absence, uniqueness or no correction.

The privacy case constructs a sanitized known-target REDACT tombstone without
copying removed sensitive text or replacement facts. Missing actual target
integrity stays UNVERIFIED. A socket-denying source test and offline schema
registry refusal show this finite path does not resolve private manifest refs;
they do not prove effective process/network isolation, deletion or cache erasure.

The verbatim pinned v4.14 reader fixture has Git blob
`c92cec520c315565d9d05ffbc5254ac803e346a3`, from qualified main
`584512e8566408bed479192753c12a036309d277`. Only its schema file locations are
adapted to the unchanged original v3 root and offline references. Tests run that
original parser, compare all 11 normalized template/pilot source carriers, check
old-reader refusal of all three v4 profiles and the current per-kind pin matrix.
There is no network/floating-main or full Git-history requirement in these tests.
The prior reviewer's separate 49-input experiment is retained historical evidence;
this test does not claim to reproduce that uncommitted corpus.

## Explicit nonblocking finding disposition

These dispositions preserve the original severities; they do not erase findings
or replace the required exact-source S05 Review. Owning-Task authorizations:
[#1217@6326047562](https://github.com/kaicreator-mm/ai-development-standard/issues/1217#issuecomment-6326047562),
[#1216@6326048450](https://github.com/kaicreator-mm/ai-development-standard/issues/1216#issuecomment-6326048450).

| Finding | Current bounded disposition / evidence / next owner |
| --- | --- |
| S03-R1-P2-01 | Test-only grouping moved before source promotion; permutations cover missing witness, stale source/pin, UNKNOWN currentness, edited/same-native-ID and all-UNKNOWN collisions. Invalid schema/foreign native inputs stay excluded. Actual affected delta must pass this initial S05 Review before resolution. Normative/wire semantics unchanged. |
| S02-R1-P3-5 | CLI test now uses an isolated TemporaryDirectory per run; TMP/TEMP can select an authorized external temp root. Actual affected test must pass S05 Review. |
| S02-R1-P2-1 | Retained lexical-profile limitation, not repaired or generalized away. New strict loader applies JSON-safe rules to v3 too: `session_ref: !!str x` and `1e5` are accepted by the actual old reader and refused by the new one; `0x1F` is refused as an old integer and accepted as a new string. Differential assertions make these changes visible. Original v3 schema/refs are byte-identical and the actual template/pilot corpus is checked. New `--effective-pin v4.14` controls record disposition, **does not emulate historical lexical parsing**. A project requiring literal historical-reader behavior must use its exact qualified parser. Any later public compatibility correction follows the owning compatibility process; this nonblocking limitation carries into S06/RQ/release notes. |
| S02-R1-P2-2 | Shape-only validator still accepts internally inconsistent correction target fields. Actual consumer application checks owning native Issue/comment, Task/Attempt, namespace, subject, digest and authority. Existing CorrectionBoundary negative cases must run; no schema-valid cancellation or claim that shape helper was repaired. Carry this implementation boundary into S06/RQ. |
| S02-R1-P2-3 | CI wiring is still pending, owned by S06 [#1228@6323806878](https://github.com/kaicreator-mm/ai-development-standard/issues/1228#issuecomment-6323806878). Existing native generic CI does not automatically run standalone v4.15 tests; actual local exact-source runs are separate evidence. Minimal workflow wiring and deliverable manifest registration must complete before RQ. |
| S02-R1-P3-4 | Retained explicit publisher-claim boundary: verifier coverage COMPLETE can coexist with skipped/unchecked arrays. Integrated negative demonstrates this remains SHAPE_VALID_ONLY/OBSERVED, never strict verification or Task PASS. Owners must inspect actual required scope; no claim of consistency repair. Carry into S06/RQ. |
| #1232 existing P2 carry | Source delivery vs runtime qualification remains distinct. Deterministic reference fixtures/manual receipts are not native controller, resource arbitration, race, lease/fencing or external operation proof. Native demonstration remains #1231 NOT_RUN. No historical Claim recovery is inferred. |

## Downstream executable receiving contract

[ADS #1210](https://github.com/kaicreator-mm/ai-development-standard/issues/1210)
owns the six deferred real execution classes and the
[verbatim retained runtime oracle](DEFERRED_E2E_ORACLE.md). It does not own ADS
source conformance or scoped ADS RQ. S06 #1228 owns exact candidate regression,
required closure Review, CI/manifest packaging, finding dispositions and RQ.

| Receiver | Required actual input and proof after its own local admission |
| --- | --- |
| task-meta [#5](https://github.com/kaicreator-mm/task-meta/issues/5), [#12](https://github.com/kaicreator-mm/task-meta/issues/12), [#14](https://github.com/kaicreator-mm/task-meta/issues/14) | Pin actual publisher source/build plus the **actual qualified immutable ADS SHA and report.schema.json blob** from S06 qualification and lawful PROJECT_ADOPTION §6 selection. Capture one real supported Attempt/private immutable manifest, sanitize typed summary, POST/read back native comment/digest; preserve unavailable metrics and billing as UNKNOWN. No imaginary source refs or prefilled self receipt. |
| Tally [#62](https://github.com/kaicreator-mm/tally/issues/62), [#65](https://github.com/kaicreator-mm/tally/issues/65) | Pin actual TS reader **and feedback writer from the same source/build**, effective ADS revision/profile and tested ADS SHA; independently witness complete GitHub native collections, actual source/edit/correction scope, and manifest-free feedback POST/readback. Phase and observed effect need their own evidence. Never fetch private task-meta API/store/SDK/manifest. |
| #1210 real integration executor | Record exact publisher SHA/build, same Tally build/config, exact qualified ADS/schema blob, Task/Attempt, source-qualified sanitized public receipt IDs/digests and true positive/negative exits. Inventory effective credential grants for every reader/writer/fallback, with actual endpoint probes and same-build denied/absent private egress. Unobservable grants/routes remain UNKNOWN, never a declared allowlist PASS. Execute actual pagination/429/lost-ACK/edit/correction/privacy/verifier/feedback cases; consume the finite ADS fixtures as expected contract only. |

**Qualification is not yet supplied by S05.** Its exact source under test is bound
by the external GitHub Validation Tuple. S06 must publish actual candidate/RQ
identity and resulting schema blob before any downstream agent fills a qualified
ADS pin; this document deliberately cannot invent that future SHA. Qualified
v4.14 main above is historical compatibility authority, not a qualified v4.15 pin.
Project-local authorization/compatibility and exact main integration predicates
remain necessary for effective adoption. A qualified candidate may be an isolated
test subject; existing effective pins/Claims never change incidentally. No main
merge is authorized by this work.

## Mandatory limits and closeout boundary

`REAL_TASKMETA_GITHUB_PUBLICATION_NOT_PROVEN` and
`REAL_TALLY_GITHUB_ONLY_READER_FEEDBACK_NOT_PROVEN` remain mandatory, together
with other applicable prior release limitations. All actual cross-project runtime
execution is NOT_RUN, not waived. Same-build/grant/egress fixture BOUNDED_WITNESS
is not a production witness. Native runtime #1231 remains NOT_RUN.

S05 can finish only after all listed ADS checks actually pass on the exact
integrated subject, its required independent source Review, lawful current
version-only integration/ratification and separate final Task delivery. S06
cannot infer Release PASS from that Task receipt; it retains its own gates.
