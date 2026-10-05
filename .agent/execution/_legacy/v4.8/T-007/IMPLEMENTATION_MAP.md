# T-007 Implementation Map

1. Re-read T-001/T-015/T-016 merged contracts and Frozen L2 compatibility requirements.
2. Build deterministic integrated fixtures covering valid historical and current v4.8 payloads.
3. Add negative cases for every shared L3 oracle owned by this Task.
4. Fail on any attempted fourth family/owner, authority inference, stale rebinding or CoT requirement.
5. Do not patch semantic owners inside this branch; surface an evidence-backed finding against the owning Task instead.
6. Run focused compatibility suite plus repository verifier/protocol regressions required by the current standard.
