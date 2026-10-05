# Commands

Run from repository root on the task branch. These paths exist on the bound baseline:

```bash
python scripts/test_v33_semantic_regressions.py
python scripts/test_v43_conformance_dogfood.py
python scripts/test_protocol_schemas.py
```

Run any new focused task regression by its checked-in path. Record actual commands and results only. If a required environment cannot execute them, return BLOCKED/handoff evidence rather than fabricate PASS.