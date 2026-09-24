from __future__ import annotations

import copy
import unittest

import v40_r2_hardening
import v40_semantics


class T010CanonicalSurfaceTests(unittest.TestCase):
    def test_fast_path_export_is_closed_world_canonical_implementation(self) -> None:
        self.assertIs(v40_semantics.fast_path_eligible, v40_r2_hardening.fast_path_eligible)
        context = {
            "scope_bounded": True,
            "validation_ownership_known": True,
            "review_policy_resolved": True,
        }
        for key in v40_r2_hardening.FAST_PATH_DISQUALIFIERS:
            context[key] = False
        self.assertTrue(v40_semantics.fast_path_eligible(context))

        missing = copy.deepcopy(context)
        del missing["material_dependency_graph"]
        self.assertFalse(v40_semantics.fast_path_eligible(missing))

        unknown = copy.deepcopy(context)
        unknown["material_dependency_grap"] = False
        self.assertFalse(v40_semantics.fast_path_eligible(unknown))

        non_boolean = copy.deepcopy(context)
        non_boolean["public_contract_change"] = "false"
        self.assertFalse(v40_semantics.fast_path_eligible(non_boolean))


if __name__ == "__main__":
    unittest.main()
