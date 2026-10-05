# Commands
Start with evidence audit and run applicable current suites from a clean checkout:
```bash
python scripts/test_v410_t03a_implementation_quality.py
python scripts/test_v43_task_decomposition.py
python scripts/test_v43_conformance_dogfood.py
python scripts/test_protocol_schemas.py
python scripts/verify_standard.py
```
Run any directly-owned compatibility/shared-code focused test discovered or added only when applicable. Record actual executions only.