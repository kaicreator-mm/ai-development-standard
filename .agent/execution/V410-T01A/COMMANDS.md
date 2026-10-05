# Commands

Run from repository root on the task branch. These commands exist on the bound baseline:

```bash
python scripts/test_v33_lifecycle_contracts.py
python scripts/test_v34_lifecycle_contracts.py
python scripts/test_pointer_only_trigger_contract.py
python scripts/test_protocol_schemas.py
```

Also run any new focused regression script added by this Task using its checked-in path. Do not claim commands not actually executed. If repository/runtime dependencies prevent a required command, record BLOCKED/validation handoff rather than guessing PASS.