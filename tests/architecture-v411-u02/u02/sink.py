"""Real persistent effect sink for the U02 experiment.

A local append-only JSONL ledger stands in for the external system's write
boundary (explicitly authorized by Issue #949 as a controlled safe local
effect sink). The real under-test boundary is the *actual write and the
persistent count*: every mutation appends one durable ledger line with a
monotonic sequence number; ``readback`` is a fresh file read every call.

``dedup`` mode models a proven effect-ID deduplication adapter: the adapter
itself refuses to append a duplicate effect identity, so a retried write
with the same effect ID never increments the real count.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import time


class SinkRefused(Exception):
    """Adapter-level refusal (tenant mismatch, missing identity, dedup hit)."""


class LedgerSink:
    def __init__(self, path: Path, *, tenant: str, dedup: bool = False):
        # Sanitize the file stem: work keys contain ':'/'#' which NTFS would
        # silently treat as alternate-data-stream syntax.
        from .plane import safe_stem
        path = Path(path)
        self.path = path.with_name(f"{safe_stem(path.stem)}{path.suffix}")
        self.tenant = tenant
        self.dedup = dedup
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _entries(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [
            json.loads(line)
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def mutate(self, *, effect_id: str, operator_id: str, tenant: str) -> dict:
        """Perform one real persistent external mutation.

        Returns {"appended": bool, "deduplicated": bool, "count": int,
        "seq": int|None}. Refusals raise SinkRefused before any write.
        """
        if not effect_id:
            raise SinkRefused("missing effect identity: non-idempotent write refused")
        if tenant != self.tenant:
            raise SinkRefused(f"tenant mismatch: sink tenant={self.tenant} got={tenant}")
        entries = self._entries()
        if self.dedup and any(e["effect_id"] == effect_id for e in entries):
            return {
                "appended": False,
                "deduplicated": True,
                "count": len(entries),
                "seq": None,
            }
        seq = len(entries) + 1
        record = {
            "seq": seq,
            "effect_id": effect_id,
            "operator_id": operator_id,
            "tenant": tenant,
            "committed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")
            fh.flush()
        return {"appended": True, "deduplicated": False, "count": seq, "seq": seq}

    def readback(self) -> dict:
        """Exact-current readback of the persistent effect boundary."""
        entries = self._entries()
        digest = hashlib.sha256(self.path.read_bytes()).hexdigest() if self.path.exists() else hashlib.sha256(b"").hexdigest()
        return {
            "count": len(entries),
            "effect_ids": [e["effect_id"] for e in entries],
            "entries": entries,
            "ledger_sha256": digest,
        }
