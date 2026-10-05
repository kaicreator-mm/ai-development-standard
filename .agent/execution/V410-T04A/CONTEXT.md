# Context
Baseline `9029435c6bb06b583b19070a4ab0863d8f4be012`; owner SHAs read directly from exact tree.

Invariants:
- required gates come from authority, never cost/docs-only/model confidence/speed;
- UNKNOWN/contradictory applicability fails closed;
- repair targets root defect class;
- non-converging repair escalates/adjudicates without arbitrary universal retry cap;
- no second gate state machine; Review semantics stay T04B.