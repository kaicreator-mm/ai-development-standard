# V410-T02B Commands

Run from a clean checkout of the exact task candidate:

```text
python scripts/test_protocol_schemas.py
python scripts/verify_event_writer_surfaces.py
python scripts/test_execution_architecture.py
python scripts/test_v410_t02a_collaboration_control.py
python scripts/verify_standard.py
```

Also run the directly-owned `scripts/test_v410_t02b_*` focused suite added by this Task. If a listed command does not exist on the exact baseline, stop and record the mismatch instead of inventing a substitute.