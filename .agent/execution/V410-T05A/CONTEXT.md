# Context
Baseline `9029435c6bb06b583b19070a4ab0863d8f4be012`; all owner SHAs were read directly from that tree.

R5 remains EXISTING_OWNER_ONLY. Required invariants:
- importability/reuse does not imply stable/public contract;
- Task-local work cannot silently widen into project-wide promotion/refactor;
- public compatibility stays with Interface Compatibility authority;
- textual similarity does not create mandatory extraction/DRY authority;
- no component registry or generic shared-code subsystem.

`NO_CHANGE_REQUIRED` is legitimate when exact current owners already cover these invariants.