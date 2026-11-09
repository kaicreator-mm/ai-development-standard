# R6 native source consumption bridge (optional exact checkout)
`formal/tests/test_r6_source_consumer.py` evaluates the actual pinned candidate
`scripts/v34_rules.py` at PR #1365 HEAD `dac263fa4c0ab155406d2f2117459b34322cc988`.
It verifies HEAD and Git blob before loading any code; no ADS source mutation.
Enable explicitly:

```bash
ADS_FORMAL_CANDIDATE_CHECKOUT=/path/to/exact-candidate-worktree \
python3 -m unittest discover -s formal/tests -p 'test_r6_source_consumer.py' -v
```

This is a **helper-consumer bridge**, not an integrated GitHub admission CAS proof. It
exhaustively checks 54 generation value pairs in a small integer domain, 7 malformed
inputs, and compatibility group ref format. A returned `IDEMPOTENT` from the
generation-only helper DOES NOT attest same-dispatch or same-operator identity.
Similarly `authorize_non_default()` checks the reference syntax but DOES NOT resolve
the governing owner grant's family/currentness/scope by itself. Actual callers
must separately provide those checked facts before eligibility. If checkout is
absent, unittest reports SKIP (SOURCE_CONSUMER_NOT_RUN); do not count it as PASS.

The R5 source-bound full-suite receipt remains 27/27 at its previous exact
experiment HEAD. The R6 new SMT models were executed as 4 incremental checks,
but the full R6 strict double-worktree run and this new source consumer test are
**NOT_RUN** until executed against the new experiment SHA.
