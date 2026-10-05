# Commands

Run from repository root on the task branch. These commands exist on the bound baseline:

```bash
python scripts/test_task_dag_lane_parallelism.py
python scripts/test_v43_conformance_dogfood.py
python scripts/test_protocol_schemas.py
```

Run any new focused regression by its checked-in path. Record actual executions only. If required validation cannot run, record BLOCKED/handoff evidence instead of inferring PASS.