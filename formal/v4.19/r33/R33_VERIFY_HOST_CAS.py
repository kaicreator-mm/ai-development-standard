"""ADS #1366 R33 — read-only verification of the historical v4.18 Host SQLite CAS databases.

Opens the ORIGINAL files in SQLite read-only URI mode (mode=ro), dumps schema and
every row, recomputes the derived physical claim keys from first principles, and
re-hashes the files after reading to prove the read caused zero mutation.

Never writes to the databases. Never creates substitute databases.
"""
import hashlib
import json
import os
import sqlite3
import sys

BASE = r"C:\xDev\kAiCreator\_tmp\TALLY_V2_T125_CANONICAL_KERNEL_TASK_ADMISSION"
BASE2 = r"C:\xDev\kAiCreator\_tmp\TALLY_V2_OWNER_AUTHORIZED_BOOTSTRAP_IMPLEMENT_AND_COMPLETE"
DBS = {
    (BASE, "kernel-claim-registry.sqlite"): "claim reservation registry #169 (host-bootstrap-config.json reservationRegistry)",
    (BASE, "canonical-dag.sqlite"): "canonical DAG write-set registry (canonical-task-writer.mjs)",
    (BASE2, "claim-registry.sqlite"): "claim reservation registry #166 (bootstrap round)",
}

EXPECTED_KEYS_RAW = [
    "kaicreator-mm/tally#166:builder:__default__",
    "kaicreator-mm/tally#169:builder:__default__",
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def derived_key(raw):
    return "tally:v2:claim-admission:" + hashlib.sha256(raw.encode()).hexdigest()


def main():
    report = {"dbs": {}, "derived_keys": {}}
    for raw in EXPECTED_KEYS_RAW:
        report["derived_keys"][raw] = derived_key(raw)

    for (base, name), label in DBS.items():
        path = os.path.join(base, name)
        before = sha256_file(path)
        size = os.path.getsize(path)
        uri = "file:" + path.replace("\\", "/") + "?mode=ro"
        con = sqlite3.connect(uri, uri=True)
        con.text_factory = lambda b: b.decode("utf-8", "backslashreplace")
        cur = con.cursor()
        schema = [
            r
            for r in cur.execute(
                "SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY name"
            ).fetchall()
        ]
        tables = [r[1] for r in schema if r[0] == "table" and not r[1].startswith("sqlite_")]
        rows = {}
        for t in tables:
            cols = [c[1] for c in cur.execute(f'PRAGMA table_info("{t}")').fetchall()]
            data = cur.execute(f'SELECT * FROM "{t}"').fetchall()
            rows[t] = {"columns": cols, "rows": [list(r) for r in data]}
        con.close()
        after = sha256_file(path)
        report["dbs"][f"{os.path.basename(base)}/{name}"] = {
            "path": path,
            "label": label,
            "size": size,
            "sha256_before": before,
            "sha256_after": after,
            "unmutated": before == after,
            "schema": schema,
            "tables": rows,
        }

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "host_cas_db_dump.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print("WROTE", out)
    for name, d in report["dbs"].items():
        print(f"== {name} size={d['size']} sha256={d['sha256_before']} unmutated={d['unmutated']}")
        print("   schema:", [(s[0], s[1]) for s in d["schema"]])
        for t, tr in d["tables"].items():
            print(f"   table {t}: {len(tr['rows'])} rows, cols={tr['columns']}")
            for r in tr["rows"]:
                one = json.dumps(r, ensure_ascii=False)
                print("   ROW:", one[:1200])
    return 0


if __name__ == "__main__":
    sys.exit(main())
