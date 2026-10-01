# T-001 R2 Review Checklist

- Exact JIT repair base is `33dfb8f05bca1ba8fd4ea8d9a2c63eaa8f9aa830`; no historical `94cad2b...` Execution Pack is reused as current authority.
- Effective source diff stays inside schema + focused test + reference; six R2 Execution Pack files are checkpoint metadata.
- `implementation_subject_ref` and `currentness_ref`, when present, accept only `git:<owner>/<repo>@<40-lowercase-hex-sha>`.
- Mutable branch/tag/symbolic/repository-only/short/malformed identities fail closed at schema and current-applicability boundaries.
- Missing/drifted exact-subject refs remain historical only.
- NONE_MATERIAL, no-private-CoT, authority and bounded confidence semantics remain unchanged.
- T-005 owns evolution/promotion semantics; T-015/T-016/T-002 scope is untouched.
- Focused test, protocol schema regression and repository verifier pass on the exact candidate.
- Independent Validation is exact-HEAD bound; genuinely Fresh Review follows and #550 verdict does not transfer.
