# Validation Report

## Identity

```text
repository: <owner/repo>
tested_sha: <40-char SHA>
candidate_sha: <SHA|NOT_APPLICABLE>
branch_ref: <auxiliary ref>
validation_scope: <concern|integration|closure>
validation_profile: <profile>
```

## Execution

```text
execution_host_role: <role>
execution_channel: <provider/local/build-host>
provider_state: <AVAILABLE|INFRA_BLOCKED|TIMED_OUT|CANCELLED|NOT_APPLICABLE>
platform/architecture: <...>
runtime/toolchain: <...>
clean_checkout: <yes/no>
command/entrypoint: <...>
exit_code: <...>
```

## Result

`PASS | FAIL | BLOCKED | NOT_RUN | NOT_APPLICABLE`

Record checks, key logs/artifacts, expected vs actual on failure, and environment-sensitive facts.

## Drift / Evidence Composition

When current candidate/target differs from the actually tested SHA, do not relabel the result. Record instead:

```text
validated_head_sha: <sha>
base_sha_at_validation: <sha>
current_target_sha: <sha>
merge_result_sha/tree: <identity|NOT_APPLICABLE>
validation_impact: <none|affected|unknown>
evidence_reuse_basis: <explicit proof|NOT_APPLICABLE>
```

`validation_impact=none` is a separate decision; it does not mean this tuple executed on the successor/merge result.

## CI Infrastructure Exception

If the normal channel is unavailable, record the provider state/run identity, required underlying profile, alternate executor/evidence, policy basis for substitution, and remaining impact. Provider failure is not candidate PASS/FAIL by itself.
