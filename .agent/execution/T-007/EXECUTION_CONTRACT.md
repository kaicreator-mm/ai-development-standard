# T-007 Execution Contract

Exact base: `version/v4.8.0@22e8e1701661689fb39a5c363eed424cf827c403`.

This is a test-only conformance concern. Add only integrated v4.8 compatibility tests/golden fixtures. Do not repair or redefine T-001/T-015/T-016 schemas, T-002 execution semantics, ownership, Availability or Interchange.

Required negative oracles: claim->proof; Capability Evidence->current PASS; provider/model->authority; runner/host fact->Logical Agent owner; fourth Availability/Exchange family; stale exact-subject rebinding; private-CoT requirement. Preserve historical v4 payload compatibility required by Frozen L2.

Allowed paths: `scripts/test_v48_contract_compatibility.py` and `fixtures/v48_contract_compatibility/**`. Any other path requires Controller rebind. Builder cannot self-certify Validation or Fresh Review.
