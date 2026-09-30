from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
import sqlite3
import sys
import tempfile
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DOGFOOD = ROOT / "docs" / "implementation" / "4.2.0" / "dogfood"
SOURCE = DOGFOOD / "T05_source_A.sql"
MIGRATION = DOGFOOD / "T05_migration_A_to_B.sql"
FRESH = DOGFOOD / "T05_fresh_B.sql"
INTERRUPTED = DOGFOOD / "T05_interrupted_transition.sql"


def fixture_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def statements(path: Path) -> list[str]:
    return [part.strip() for part in path.read_text(encoding="utf-8").split(";") if part.strip()]


def execute_statements(conn: sqlite3.Connection, sql: Iterable[str]) -> None:
    for statement in sql:
        conn.execute(statement)


def schema_version(conn: sqlite3.Connection) -> int:
    return int(conn.execute("SELECT version FROM schema_meta").fetchone()[0])


def rows(conn: sqlite3.Connection) -> list[tuple]:
    columns = [item[1] for item in conn.execute("PRAGMA table_info(accounts)").fetchall()]
    order = "id"
    data = conn.execute(f"SELECT * FROM accounts ORDER BY {order}").fetchall()
    return [tuple([*columns]), *[tuple(row) for row in data]]


def create_source_a(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    execute_statements(conn, statements(SOURCE))
    conn.commit()
    return conn


def migrate_a_to_b(conn: sqlite3.Connection) -> None:
    conn.execute("BEGIN IMMEDIATE")
    try:
        execute_statements(conn, statements(MIGRATION))
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()


def create_fresh_b(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    execute_statements(conn, statements(FRESH))
    conn.commit()
    return conn


def exercise_interrupted_then_recover(path: Path) -> dict:
    conn = create_source_a(path)
    source_rows = rows(conn)
    failure_type = None
    conn.execute("BEGIN IMMEDIATE")
    try:
        execute_statements(conn, statements(INTERRUPTED))
    except sqlite3.IntegrityError as exc:
        failure_type = type(exc).__name__
        conn.rollback()
    else:
        conn.rollback()
        raise AssertionError("interrupted fixture did not fail as required")

    recovered_source_version = schema_version(conn)
    recovered_source_rows = rows(conn)
    partial_table_count = int(
        conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='accounts_v2'"
        ).fetchone()[0]
    )
    if recovered_source_version != 1 or recovered_source_rows != source_rows or partial_table_count != 0:
        raise AssertionError("transaction rollback did not restore source state A")

    migrate_a_to_b(conn)
    result = {
        "failure_type": failure_type,
        "source_restored_after_failure": True,
        "recovery_strategy": "rollback-source-transaction-then-rerun-forward-A-to-B",
        "down_migration_required": False,
        "final_schema_version": schema_version(conn),
        "final_rows": rows(conn),
    }
    conn.close()
    return result


def run(workdir: Path) -> dict:
    workdir.mkdir(parents=True, exist_ok=True)

    migrated_path = workdir / "migrated.sqlite3"
    migrated = create_source_a(migrated_path)
    source_rows = rows(migrated)
    migrate_a_to_b(migrated)
    migrated_rows = rows(migrated)
    migrated_version = schema_version(migrated)
    migrated.close()

    fresh_path = workdir / "fresh.sqlite3"
    fresh = create_fresh_b(fresh_path)
    fresh_rows = rows(fresh)
    fresh_version = schema_version(fresh)
    fresh.close()

    recovery = exercise_interrupted_then_recover(workdir / "recovery.sqlite3")

    evidence = {
        "engine": "sqlite",
        "sqlite_runtime_version": sqlite3.sqlite_version,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "fixture_sha256": {
            path.name: fixture_sha256(path)
            for path in (SOURCE, MIGRATION, FRESH, INTERRUPTED)
        },
        "subjects": {
            "migration_A_to_B": {
                "source_schema_version": 1,
                "target_schema_version": migrated_version,
                "source_rows": source_rows,
                "target_rows": migrated_rows,
            },
            "fresh_bootstrap_B": {
                "target_schema_version": fresh_version,
                "rows": fresh_rows,
                "separate_subject": True,
            },
            "interrupted_recovery": recovery,
        },
    }
    return evidence


def main() -> int:
    if len(sys.argv) > 1:
        workdir = Path(sys.argv[1]).resolve()
        evidence = run(workdir)
    else:
        with tempfile.TemporaryDirectory(prefix="v42-sqlite-dogfood-") as tmp:
            evidence = run(Path(tmp))
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
