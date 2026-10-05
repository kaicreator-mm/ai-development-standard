# V410-T04B Commands

Minimum directly relevant checks on the exact candidate:

```text
python scripts/test_protocol_schemas.py
python scripts/verify_event_writer_surfaces.py
python scripts/test_execution_architecture.py
python scripts/test_v410_t02a_collaboration_control.py
python scripts/test_v410_t02b_machine_projection.py
python scripts/test_v410_t04a_gate_repair_routing.py
python scripts/verify_standard.py
```

Also run the directly-owned `scripts/test_v410_t04b_*` focused suite added by this Task and any existing Review-currentness regression explicitly touched by the implementation.

Missing listed command or owner mismatch is a contract/currentness defect to report, not permission to invent an unrelated substitute.