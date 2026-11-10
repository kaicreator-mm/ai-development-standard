"""#1366: source-bound admission must not PASS with zero actual source anchors."""
from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "suite"))


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


legacy = _load("formal_r24_legacy", ROOT / "suite" / "run.py")
expanded = _load("formal_r24_expanded", ROOT / "suite" / "expanded.py")
HEAD = "a" * 40


def _blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class SourceBindingNonVacuityTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.data = b"An actual, selected source rule.\n"
        (self.root / "rule.md").write_bytes(self.data)
        self.row = {"path": "rule.md", "blob": _blob(self.data),
                    "anchors": ["selected source rule"]}

    def _readbacks(self, sources):
        source_map = {"candidate_head": HEAD, "sources": sources}
        with mock.patch.object(legacy, "tool", return_value={"code": 0, "text": HEAD}), \
             mock.patch.object(expanded, "execute", return_value={"code": 0, "text": HEAD}):
            return (
                legacy.source_check(str(self.root), source_map),
                expanded.source_alignment(str(self.root), source_map),
            )

    def test_empty_list_must_fail_both_runners(self):
        for verdict in self._readbacks([]):
            self.assertEqual(verdict["status"], "FAIL", verdict)
            self.assertEqual(verdict["reason"], "SOURCE_BINDINGS_EMPTY_OR_MALFORMED")

    def test_missing_or_invalid_source_collection_fails(self):
        for entries in (None, {}, "source", [1]):
            with self.subTest(entries=entries):
                for verdict in self._readbacks(entries):
                    self.assertEqual(verdict["status"], "FAIL", verdict)

    def test_zero_anchors_must_not_vacuously_pass(self):
        for verdict in self._readbacks([dict(self.row, anchors=[])]):
            self.assertEqual(verdict["status"], "FAIL", verdict)
            self.assertEqual(verdict["checks"][0]["reason"], "SOURCE_ANCHORS_EMPTY_OR_MALFORMED")

    def test_invalid_anchor_entries_must_fail(self):
        for anchors in (None, ["", "selected source rule"], [12]):
            with self.subTest(anchors=anchors):
                for verdict in self._readbacks([dict(self.row, anchors=anchors)]):
                    self.assertEqual(verdict["status"], "FAIL", verdict)

    def test_real_nonempty_matching_source_keeps_pass(self):
        for verdict in self._readbacks([self.row]):
            self.assertEqual(verdict["status"], "PASS", verdict)
            self.assertEqual(len(verdict["checks"]), 1)
            self.assertEqual(verdict["checks"][0]["status"], "PASS")

    def test_wrong_or_missing_anchor_still_fails(self):
        for changed in (dict(self.row, anchors=["missing unique marker"]),
                        dict(self.row, blob="0" * 40)):
            with self.subTest(changed=changed):
                for verdict in self._readbacks([changed]):
                    self.assertEqual(verdict["status"], "FAIL", verdict)

    def test_no_checkout_retains_not_run(self):
        for verdict in (legacy.source_check(None, {"candidate_head": HEAD, "sources": []}),
                        expanded.source_alignment(None, {"candidate_head": HEAD, "sources": []})):
            self.assertEqual(verdict["status"], "NOT_RUN", verdict)


if __name__ == "__main__":
    unittest.main()
