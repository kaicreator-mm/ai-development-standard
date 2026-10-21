# v4.15 GitHub-only consumer and feedback conformance

This implements frozen L2 sections 2/3 for S03. The normative owner is
`GITHUB_AGENT_INTERACTION_PROTOCOL.md` §16.6. It defines a contract for downstream
Tally, not a Tally TypeScript implementation. Offline examples and the test-only
oracle below do not witness a real publisher, network, grant, or GitHub operation.

## Read boundary and bounded collection

The reader obtains actual canonical Issue bodies, native dependencies, PR commits,
Review/CI results, admitted Claim references and report comments through GitHub.
It resolves the exact immutable ADS pin and per-kind schema before interpreting
records: current v3 Work Item/Intent/Event, historical read-only v3 reports, and
current v4 reports. It never manufactures missing v4 facts for historical v3.
An unsupported pair is rejected, never partially interpreted as an operation.

Every queried collection has its own completeness receipt: repository/Issue,
endpoint/query, page/cursor sequence, terminal-page observation, observed interval,
actual response identities and failure/limit. Follow only API-supplied GitHub
pagination within the intended repository/surface; a partial first page cannot
prove absence, uniqueness, no correction or no dependency. Detect cursor cycles.
Bound pages, elapsed time, request timeouts and retry count. Respect observed
`Retry-After`/rate-limit reset for 429 and applicable rate-limit 403 within the
remaining budget; never busy-loop. Retry transient reads within that budget.
Permission failures, unavailable pages, malformed responses and exhausted budgets
yield UNKNOWN/INSUFFICIENT_EVIDENCE for the affected scope, not an empty collection.
Other independently complete scopes may remain usable. Concurrent native changes
are not an atomic snapshot: material drift requires bounded reread; unresolved
drift keeps that conclusion UNKNOWN.

Strings in `source_refs`, experience/procedure refs, manifest refs or human prose
are untrusted references, not fetch instructions. Private task-meta API, database,
object/manifest, SDK, Trace and private receipt access are excluded. GitHub source
links are resolved only through bounded permitted GitHub endpoints after canonical
repository/Issue/type checks. The reader may derive its own index/digests from
observed GitHub data; this is not a new writable source of execution authority.

## Reconciliation and source limits

Use the validated data-only JCS digest and identity from §16.5. Retain each actual
GitHub comment ID/URL, owning Issue, native timestamps/edit signals, observed
digest and observation interval. Same identity and digest is duplicate evidence,
never another Attempt or independent witness. Different digests for one identity,
or a changed digest on one comment ID, is CONFLICT; input ordering and latest
timestamp cannot choose a winner. Native edit evidence is UNVERIFIED/CONFLICT.
Missing historical edit/original-publication evidence remains UNKNOWN. An
available clear native signal is bounded observation, not cryptographic or
permanent immutability. Revisions are append-only, source-bound predecessors;
missing predecessor or unresolved conflict cannot be repaired by a timestamp.

The consumer verifies actual source SHA/Task/Attempt, effective ADS pin/profile,
native currentness, required source authority and predecessor lineage. The
report's own `CURRENT`, actor, source ref, cost or verifier claim proves none of
these. Source evidence that cannot be observed remains UNKNOWN. Collector-only
Attempts remain collector-only. Public observation, presented experience and
capture completeness never confer Task completion, admitted Claim, Review,
Validation or Release PASS. Late native CI/Review results do not imply that
task-meta captured them or published a new summary revision.

Correction application MUST check the actual target comment (not a body-supplied
URL alone), canonical owning Issue and comment URL prefix, repository, Task and
Attempt, original report ID/revision/kind/namespace/data digest, and current
owning publication/admission authority. The notice's subject must align with that
target scope. Its own ADS pin/profile and native integrity must also be checked.
A syntactically valid but cross-Issue/Task/namespace or mismatched-target notice
is DISPUTED/UNVERIFIED and cannot cancel evidence. Sharing a transport login
is irrelevant to logical publisher ownership. Missing target or ownership proof
is UNVERIFIED. An authorized aligned REVOKE/REDACT notice invalidates only its
target; an aligned DISPUTE keeps it disputed, not replaced with new facts. A
correction cannot supply replacement measurements/outcomes; use a separately
verified revision of the original profile. Authorized privacy removal can leave
a sanitized tombstone without repeating sensitive material. No GitHub cache
erasure guarantee is made.

These consumer checks specifically cover S02-R1-P2-2. They do not claim that
S02's source-only shape verifier rejects every cross-Issue/Task correction or
that its observation helper classifies DISPUTED. That implementation finding
remains OPEN for owning integration/closure disposition.

## Manifest-free feedback and actual publication

Tally uses exactly `EXPERIENCE_USE_FEEDBACK` in `ads/github/v4:report`, with actual
`publisher_source_sha` for its running build, `ads_subject_sha` for the exact
tested/qualified ADS subject, effective ADS revision/profile, source-bound Task/
Attempt, experience and procedure revision, epistemic status and explicit limits.
A pre-RQ candidate is a test subject, not production adoption. The running build,
ADS under test and subject Task source are distinct identities; never substitute
one for another. Missing witness stays UNKNOWN even when a field is well shaped.
No private manifest or invented self comment ID/URL/digest is needed or permitted.

PRESENTED means displayed; ACCEPTED, APPLIED, SKIPPED, INDEPENDENTLY_CHECKED and
OBSERVED_EFFECT require their own actual evidence. None follows automatically
from another, nor does a click or successful publication prove application,
independence, causal improvement or outcome. Only INDEPENDENTLY_CHECKED carries
the profile's actual independent `verifier_refs`; observed outcome evidence can
be cited in `source_refs` with bounded attribution and limits. Never relabel an
estimate as billed cost or unobserved effect as success.

Before POST the publisher reads actual permissions and target currentness,
validates/sanitizes the record and computes its public data digest. After POST
read back actual GitHub comment ID/URL/body and data digest. Keep a separate
receipt with source/build/pin, identity, request outcome and actual readback.
Lost acknowledgement requires complete paginated search of the owning Issue:
same identity+digest reuses that real receipt, different digest is CONFLICT;
incomplete search or unresolved concurrent publication is UNKNOWN, never blind
re-POST or atomic exactly-once. A new revision references its actual predecessor;
no in-place edit to fake a successful earlier publication.

## Independently witnessable downstream evidence

Downstream real validation must witness the **same exact Tally TS build** doing
GitHub-only reading and manifest-free feedback publication. Record build source
SHA and artifact/config identity, ADS test subject/pin/profile, actual native
read/publication receipts, test positive/negative paths, credential coverage and
observation interval. A fixture, Python oracle, different build, source-only
lint, network design or one successful request is not that witness.

Inventory every actual credential path used by reader, feedback publisher and
fallbacks. For a GitHub App record observed installation/repository scope,
permission grants and endpoint needs; distinguish granted permissions from
permissions requested in a manifest. For PATs record effective observable grant
facts and limitations, never the token. Classic token scope headers alone do not
prove all repository/org restrictions; unavailable fine-grained PAT grants are
UNKNOWN. Source code or a declared allowlist cannot prove effective credentials.
Match actual Issue/PR/Review/CI read needs and Issue-comment publication write
need against the observed grants without inventing a new authority mechanism.

No-private-task-meta-egress evidence requires independently observed effective
network/config/credential coverage for that same build, including redirects,
fallbacks and failure paths. Exercise a permitted GitHub path and a denied
private egress path without exporting secrets or fetching a real private
manifest. An inaccessible grant inventory or unobserved route remains UNKNOWN;
absence in a sampled log alone is not proof of absence. A broader credential
does not by itself prove it was used for a private fetch, but cannot support a
least-privilege claim. Record partial coverage explicitly.

This downstream obligation belongs to deferred #1210 (and applicable runtime
work), **not an entry prerequisite for ADS normative source delivery** under
the accepted R4 scope. ADS source conformance may pass while
`REAL_TASKMETA_GITHUB_PUBLICATION_NOT_PROVEN` and
`REAL_TALLY_GITHUB_ONLY_READER_FEEDBACK_NOT_PROVEN` remain mandatory. No real
Tally/runtime/permission-isolation PASS is claimed here.

## Executable boundary

`tests/v415_consumer_oracle.py` is a test-only deterministic contract oracle:
finite supplied GitHub observations in, bounded derived observation states out.
`tests/test_v415_consumer.py` exercises existing S02 wire/digest/compatibility
helpers plus the oracle's failure/correction/feedback cases. It performs no
network or private fetch and cannot witness production behavior. Tests keep
explicit expected outcomes for malformed input, incomplete collections, stale
source, edit/conflict, cross-namespace/same-login correction and unknown grants.
Their PASS means only these finite ADS-owned conformance cases ran. Existing
native CI does not automatically invoke these standalone tests; exact local
execution and native generic checks must be reported separately until an
authorized integration owner connects them before RQ.
