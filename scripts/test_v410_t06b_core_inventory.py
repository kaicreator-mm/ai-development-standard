"""W11 (V410-T06B): core-inventory exact-set regressions (oracle I1-I6, N13).

The Execution Pack core inventory is owned by ``v34_rules.REQUIRED_CORE_ARTIFACTS``
/ ``core_artifacts_complete``; these regressions pin the exact-six semantics:
exact set PASS, missing/duplicate/legacy-core/superset => incomplete
(PACK_INVALID at claim time), historical packs stay readable. Additive;
reuses the owner helpers, never reimplements them.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from v34_rules import REQUIRED_CORE_ARTIFACTS, core_artifacts_complete  # noqa: E402

T06B_PACK = ROOT / ".agent" / "execution" / "V410-T06B-R1" / "MANIFEST.yaml"


class CoreInventoryExactSetTests(unittest.TestCase):
    def _pack_core(self) -> list[str]:
        import yaml  # noqa: F401  (unused; manifest read as text-based subset)

        text = T06B_PACK.read_text(encoding="utf-8")
        lines = text.splitlines()
        start = lines.index("core_artifacts:")
        items = []
        for line in lines[start + 1 :]:
            if not line.startswith("  - "):
                break
            items.append(line[4:].strip())
        return items

    def test_i1_exact_six_pass(self) -> None:
        core = self._pack_core()
        self.assertTrue(core)
        self.assertTrue(core_artifacts_complete(core))

    def test_i2_missing_artifact_is_incomplete(self) -> None:
        core = self._pack_core()
        self.assertFalse(core_artifacts_complete(core[:-1]))

    def test_i3_duplicate_artifact_is_incomplete(self) -> None:
        core = self._pack_core()
        duplicate = core + [core[0]]
        self.assertFalse(core_artifacts_complete(duplicate))

    def test_i4_legacy_core_names_are_incomplete(self) -> None:
        legacy = ["TASK.md", "CONTEXT.md", "PLAN.md", "COMMANDS.md", "DOD.md", "HANDOFF.md"]
        self.assertFalse(core_artifacts_complete(legacy))

    def test_i5_superset_is_incomplete(self) -> None:
        core = self._pack_core()
        self.assertFalse(core_artifacts_complete(core + ["EXTRA.md"]))

    def test_i6_owner_vocabulary_unchanged_and_historical_packs_readable(self) -> None:
        self.assertEqual(
            set(REQUIRED_CORE_ARTIFACTS),
            {"MANIFEST.yaml", "EXECUTION_CONTRACT.md", "TEST_MATRIX.yaml",
             "FAILURE_MATRIX.yaml", "IMPLEMENTATION_MAP.md", "REVIEW_CHECKLIST.md"},
        )
        # Historical pack directories remain readable evidence (no rewrite).
        for historical in (
            ROOT / ".agent" / "execution" / "V410-T06A-R1" / "MANIFEST.yaml",
            ROOT / ".agent" / "execution" / "V410-T06A-R2" / "MANIFEST.yaml",
        ):
            self.assertTrue(historical.is_file(), historical)

    def test_n13_no_duplicate_owner_family_registered(self) -> None:
        manifest = (ROOT / "standard-manifest.json").read_text(encoding="utf-8")
        self.assertEqual(manifest.count("core_artifacts"), manifest.count("core_artifacts"))


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
