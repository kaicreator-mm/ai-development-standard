# Deferred real integration oracle — ADS #1210

**NOT_RUN / not waived / not ADS v4.15 scoped RQ evidence.**

The following excerpts are verbatim from predecessor a1c2ddd8c7f48374a3425b2e98c5b9dee798534a. Their old release timing is historical and subject only to SCOPE_REVISION_R3.md §2; their actual runtime behavior remains the future acceptance oracle.

### Immutable excerpt: PRD.md §4 J1–J6

## 4. Real critical journeys and falsifiable negatives

| Journey | Positive witness | Required negative / no-go |
| --- | --- | --- |
| J1 Agent→task-meta→GitHub | One real supported Agent Attempt with source-qualified partial/complete metric coverage, published safe Report, GitHub comment+digest readback | Provider model/cost absent must be UNKNOWN; never expose raw Trace/private Manifest |
| J2 GitHub→Tally | Reader given **GitHub-only** authorization resolves report revision, actual Task/Attempt/exact code/ADS, strict verifier and known/unknown cost, one lesson or NONE_MATERIAL | Independently witnessed credential/endpoint inventory plus denied task-meta private egress/config; no private Manifest read; invalid schema/subject fails closed |
| J3 corrections/retries | Lost POST ACK reconciled, correction cites accepted predecessor; no duplicate metrics when 2 Attempts or parent/child spans | Same report ID/revision with conflicting digest or edited historical body => `UNVERIFIED/CONFLICT`; privacy leak permits authorized redaction plus safe tombstone/readback |
| J4 verifier truth | Real CI/Host/Review predicates checked for bound SHA and exact semantic requirements, Task outcome deduced by lawful owner | 19/20 passing checks or tool ACK ≠ STRICT_TASK_SUCCESS; final verifier failure remains failure |
| J5 usage feedback | Tally publishes the same-v4-family manifest-free `EXPERIENCE_USE_FEEDBACK` GitHub Report (shown vs applied vs checked/outcome) with actor and source refs | Proposals and self-rated progress cannot change GitHub Task or Kernel Effect/Package acceptance |
| J6 compatibility | For **candidate E2E**, both projects bind the same exact frozen v4.15 **test subject without effective adoption**, plus one valid + one invalid wire sample; **after RQ/main merge**, optional project-local adoption pins qualified exact SHA with compatibility proof (Tag not mandatory) | Frozen candidate test pin is never production adoption; v4.14 v3-only reader cleanly rejects/ignores new v4 record; v4.15 reader reads old v3 as incomplete historical evidence; incompatible effective adoption never silently accepted |


### Immutable excerpt: L2_ARCHITECTURE.md §5

## 5. GitHub-only Tally reader and feedback writer witness (FR04 / Product P2)

**Same actual build/entrypoint (P2-2):** execute the true Tally TypeScript GitHub C-adapter reader **and the publishing path that emits `EXPERIENCE_USE_FEEDBACK`** from the same pinned source/build; record any test config differences, `publisher_source_sha` and exact frozen `ads_subject_sha` (test subject, not production adoption). No fixture-only alternate mini-reader is sufficient for E3. A feedback record must distinguish inputs derived solely from GitHub from separately source-qualified Host/runx/Kernel adapter observations; such other evidence never creates a hidden task-meta private dependency.

**Actual permissions (P2-3):** record a secret-redacted, independently verifiable *effective* permission/grant inventory for reader and feedback writer: token type, target repositories and applicable native Issue/PR/CI/Checks READ, Issue-comment WRITE when publishing, probes/currentness. Prefer least-privilege GitHub App installation token with observed installation/repository grants; an existing classic PAT may have `X-OAuth-Scopes` observable. **Fine-grained PAT effective permission grants cannot generally be read back via the API**, so mere secret-redacted token configuration is not proof; if actual grants cannot be established, classify scope proof `UNKNOWN` and do not claim a scoped-negative PASS. No broad PAT issuance is required merely to satisfy a test; user-selected authorized access applies. Never log token bytes.

**Private egress denial:** record the same reader process's environment/config allowlist and actual denied/absent task-meta API, database, SDK, object store or private Manifest endpoint/credential. Inject a private Manifest URL and task-meta API address as negative inputs; they must be refused/denied and yield `INSUFFICIENT_EVIDENCE` while GitHub-only reads work. This applies to the GitHub-only **reader/conformance surface**, not Tally's separate lawfully admitted Host/Tool/Kernel interfaces. A network deny log plus actual code-path instrumentation is stronger evidence than a self-description.


### Immutable excerpt: L2_ARCHITECTURE.md §6 E1–E6

## 6. Bounded conformance layers and executable proof owners (FR07)

| Layer | ADS v4.15 conformance obligation | Real implementation / actual witness |
| --- | --- | --- |
| E1 Schema | v4 **report-only** root with typed profiles, strict parsing and JCS data digest; v3 non-report remains **current executable** across pins, v3 reports historical-only for v4, v3-only reader rejects/ignores v4 reports | ADS verifier/source tests; no GitHub mutation or Gate PASS from schema |
| E2 Publication | one real Agent + private task-meta source report → actual GitHub issue comment/receipt, fail on duplicate/stale/conflict | task-meta #3/#5/#12 source and GitHub readback; must be genuine |
| E3 GitHub-only consumer | actual Tally TS C GitHub adapter reads that report and native GitHub refs, resolves all available actor/attempt/verifier/cost or UNKNOWN, no private Manifest | Tally #62/#65 source + independently inspected credential grants/egress witness |
| E4 Reliability negatives | second/retried/corrected Attempt, failed verifier with many green checks, edited/collision/revoked report, 429/network timeout | source-bound actual affected behaviors; deterministic fakes only for unrelated failure inputs |
| E5 Usage feedback | Tally v4 manifest-free feedback → GitHub post/readback and later source-bound actual CI/Host observed-use comparison | Tally v2 actual publisher + ADS readback; no automatic Candidate activation |
| E6 Version qualification | exact frozen integration SHA/schema+external reader/publisher pins; CI and independent Review + closure/RQ | ADS #1210; missing actual external code gives **`BLOCKED/NOT_RUN`**, not scoped waiver |

At least one real Agent/Host/Task sequence is essential. Broad three-provider hook compatibility, large datasets and actual new Domain Package production deployment are explicitly NOT required in v4.15. No per-step GitHub spam or published raw telemetry.


### Immutable excerpt: TASK_DAG_FREEZE.md S05 P2-2

- S05 must witness one true task-meta producer and one true same-build Tally TS GitHub-only reader+feedback writer, actual effective GitHub grant permissions, absence/denial of task-meta private egress, corrected/late reports, strict independent CI/Host verifier and source-qualified effect comparison, not inferred use=PASS.

## Readback and ownership

ADS #1210 is the durable tracking owner; external owner Issue refs and the enumerated external execution classes are in SCOPE_REVISION_R3.md §4. Require actual immutable task-meta/Tally builds, same-build reader plus feedback publisher, actual effective GitHub grants and absent/denied private egress. Old #1219 is retained as superseded version-path history; neither record is closed as PASS by the scope change.
