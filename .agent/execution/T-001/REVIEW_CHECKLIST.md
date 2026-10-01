# T-001 Review Checklist

- Candidate branch descends from exact JIT base `94cad2b0487e8a552c66d6bcd1cba36b7779383d`.
- Effective source diff stays inside the three-file execution write set.
- Task Learning is one machine family only and does not absorb T-015/T-016.
- Exact identity/currentness and stale-history behavior are fail-closed.
- NONE_MATERIAL Fast Path remains lightweight.
- No private chain-of-thought is required or persisted.
- No Product/Architecture/Task/ADR/Incident/Review/Validation authority is granted.
- Focused positive/negative tests plus applicable repo verifier pass on exact candidate.
- Independent Validation is bound to exact final HEAD.
- Fresh required Review occurs after Validation and before merge; later material commits invalidate prior evidence.
