# T11 Implementation Map

| Concern | Authorized surface | Owner boundary |
|---|---|---|
| executable shortcut-negative matrix | `scripts/test_v43_conformance_dogfood.py` | consumes existing v4.3 owners/profiles; does not rewrite them |
| planner→bounded-executor dogfood record | `docs/implementation/4.3.0/dogfood/T11_EVIDENCE.md` | evidence only; no Product/Architecture authority |
| deterministic dogfood scenarios | `docs/implementation/4.3.0/dogfood/fixtures/**` | fixtures/evaluation inputs only |
| focused CI invocation | `.github/workflows/verify-standard.yml` only if materially required | one T11 command only; CI is not Validation/Release authority |

The implementation must compose existing T01–T10 behavior. If satisfying an oracle requires changing an existing semantic owner, stop and raise an owner finding rather than repairing it inside T11.

Selected dogfood must expose durable Product/Architecture/Task-Pack facts to a bounded executor/evaluator and demonstrate either successful bounded consumption or explicit clarification/escalation. Any hidden redesign means FAIL/route upward, not oracle weakening.
