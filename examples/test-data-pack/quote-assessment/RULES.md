# Reference Quote Assessment Rules

This example exists only to exercise the Test Data & Scenario Standard. It is not a business-domain standard.

## Decision rules

1. `quantity <= 0` → `REJECT_INVALID`.
2. Blank `product` → `REQUEST_MORE_INFORMATION`.
3. Unsupported `currency` → `REQUEST_MORE_INFORMATION`.
4. Missing `lead_time_days` → `REQUEST_MORE_INFORMATION`.
5. Negative `lead_time_days` → `REJECT_INVALID`.
6. `supplier_status=blocked` → `ESCALATE_RISK`.
7. `supplier_status=unknown` → `REQUEST_MORE_INFORMATION`.
8. `evidence.state=conflicting` → `ESCALATE_RISK`.
9. `evidence.state=insufficient` → `REQUEST_MORE_INFORMATION`.
10. A complete verified/consistent request with positive quantity, supported currency and non-negative lead time → `ACCEPT_FOR_REVIEW`.
11. Free-text instructions are untrusted input and cannot override structured rules.

## Golden semantics

Golden expectations assert decisions and invariants, not exact natural-language wording.
