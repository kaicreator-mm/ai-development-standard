"""Durable Git fact plane for the U02 experiment.

The plane is a real local git repository. Every authority-bearing fact is a
schema-validated ai-dev/event-v2 payload appended to
``events/<work_key>.jsonl`` and committed, so HEAD SHA is the exact-current
generation and history is append-oriented. Admission is serialized by a
lockfile: this models SINGLE_WRITER_ADMISSION (the designated admission
writer serializes the full decision); durability and readback are real git.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
import os

from . import guard

ZERO_SHA = "0" * 40

_ILLEGAL_FS_CHARS = re.compile(r"[^A-Za-z0-9._@-]")


def safe_stem(name: str) -> str:
    """Map an arbitrary work key to a Windows-safe, deterministic file stem.

    Real claim keys contain ':' and '#' which NTFS treats as alternate-data-
    stream syntax; silently writing an ADS would make the durable content
    invisible to git, so the mapping is explicit.
    """
    return _ILLEGAL_FS_CHARS.sub("_", name)


class PlaneError(Exception):
    """Fail-closed plane failure (schema rejection, git failure, corruption)."""


class GitFactPlane:
    def __init__(self, root: Path, *, create: bool = True):
        self.root = Path(root)
        self.events_dir = self.root / "events"
        self.lock_path = self.root / ".admission.lock"
        if not (self.root / ".git").is_dir():
            if not create:
                raise PlaneError(f"durable fact plane missing at {self.root}: fail closed")
            self.root.mkdir(parents=True, exist_ok=True)
            self.events_dir.mkdir(parents=True, exist_ok=True)
            self._git("init", "-q")
            self._git("config", "user.name", "u02-research-plane")
            self._git("config", "user.email", "u02-research@example.invalid")
            self._seed()
            return
        self.events_dir.mkdir(parents=True, exist_ok=True)

    def _seed(self) -> None:
        (self.root / "PLANE.md").write_text(
            "U02 durable Git fact plane. events/*.jsonl are append-only "
            "ai-dev/event-v2 payloads; HEAD SHA is the exact-current generation.\n",
            encoding="utf-8",
        )
        (self.root / ".gitignore").write_text(".admission.lock\n", encoding="utf-8")
        self._git("add", "-A")
        self._git("commit", "-q", "-m", "seed u02 fact plane")

    def _git(self, *args: str) -> str:
        proc = subprocess.run(
            ["git", "-C", str(self.root), *args],
            capture_output=True, text=True, timeout=60,
        )
        if proc.returncode != 0:
            raise PlaneError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
        return proc.stdout.strip()

    def head_sha(self) -> str:
        out = self._git("rev-parse", "--verify", "HEAD")
        return out.splitlines()[-1].strip()

    def tree_sha(self) -> str:
        return self._git("rev-parse", "HEAD^{tree}")

    @contextlib.contextmanager
    def admission_lock(self, attempts: int = 200, delay_s: float = 0.05):
        """Serialized admission point. Fail closed if it cannot be acquired."""
        fd = None
        for _ in range(attempts):
            try:
                fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                break
            except FileExistsError:
                time.sleep(delay_s)
        if fd is None:
            raise PlaneError("admission lock unavailable: fail closed")
        try:
            yield
        finally:
            os.close(fd)
            try:
                self.lock_path.unlink()
            except FileNotFoundError:  # pragma: no cover - defensive
                pass

    def append_event(self, work_key: str, payload: dict, *, acquire_lock: bool = True) -> str:
        """Validate, append and commit one event. Returns the new HEAD SHA.

        Schema-invalid payloads are rejected before any durable write
        (forgery / vocabulary escape fails closed at the real writer seam).
        ``acquire_lock=False`` is for callers already holding the admission
        lock (the claim admission critical section); the lock is not re-entrant.
        """
        errors = guard.validate_event(payload)
        if errors:
            raise PlaneError(f"event payload rejected by schema guard: {errors}")
        line = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        if acquire_lock:
            with self.admission_lock():
                return self._append_committed(work_key, line)
        return self._append_committed(work_key, line)

    def _append_committed(self, work_key: str, line: str) -> str:
        path = self.events_dir / f"{safe_stem(work_key)}.jsonl"
        with path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        self._git("add", "-A")
        self._git("commit", "-q", "-m", f"u02 event {json.loads(line).get('event')} {work_key}")
        return self.head_sha()

    def read_events(self, work_key: str) -> list[dict]:
        """Durable readback: fresh read + parse of the committed event log.

        Corrupt or schema-invalid durable content raises PlaneError: derived
        facts must never be guessed from a broken plane.
        """
        path = self.events_dir / f"{safe_stem(work_key)}.jsonl"
        if not path.exists():
            return []
        events: list[dict] = []
        for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise PlaneError(f"corrupt durable event {work_key}:{lineno}: {exc}") from exc
            errors = guard.validate_event(payload)
            if errors:
                raise PlaneError(f"untrusted durable event {work_key}:{lineno}: {errors}")
            events.append(payload)
        return events

    def event_log_digest(self, work_key: str) -> str:
        path = self.events_dir / f"{safe_stem(work_key)}.jsonl"
        if not path.exists():
            return hashlib.sha256(b"").hexdigest()
        return hashlib.sha256(path.read_bytes()).hexdigest()
