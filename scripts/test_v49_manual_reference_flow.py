"""T-013 deterministic checks for the manual / GitHub-native reference flow.

TEST_MATRIX oracles (see .agent/execution/T-013/TEST_MATRIX.yaml):

  M01  every artifact reference in the flow doc resolves at the candidate (path + anchor)
  M02  durable-vs-derived examples are accurate: durable facts read from git/GitHub/
       repository surfaces; derived state is marked as a non-authoritative projection
  M03  no scheduler daemon, runtime DB or proprietary transport is implied anywhere
  M04  pointer-only trigger examples match the pointer-only trigger contract
  M05  no normative semantics are created beyond the Frozen L2 / owner standards
       (descriptive reference only)

These are Builder-level evidence checks; they are not independent Validation and never
issue gate verdicts.
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "references" / "MANUAL_REFERENCE_FLOW_V49.md"
FIXTURE_DIR = ROOT / "fixtures" / "manual-reference-flow"
FIXTURE_FILES = (
    "durable_facts.json",
    "derived_projections.json",
    "pointer_triggers.json",
    "walkthroughs.json",
)

FROZEN_BLOBS_AT_HEAD = {
    "docs/implementation/4.9.0/PRD.md": "a8ec7030a14337a4c2dca853dc474e965679d610",
    "docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md": "bd41ea0175b459a6a490fd37ad579e429a58a1c3",
    "docs/implementation/4.9.0/TASK_DAG.md": "b9fe0cc7089f64929b4bcf45f7230d950e864db2",
}
DAG_V01_BLOB = "4f358ba2b32e01ae17ddcdf970151cf28e44bb3f"

# v4.10 integration (claim #779@6084794791 / pre-merge #779@6084805500; merge
# commit e0315b2a): the disclosed composition rebind renumbered the v4.9
# standard section §28 -> §29 in standards/EXECUTION_ARCHITECTURE_STANDARD.md.
# The anchor-form citations this lane resolves (flow doc + fixtures) were
# realigned to the renumbered headings `#291-` .. `#296-` in the same step:
# references/MANUAL_REFERENCE_FLOW_V49.md (12), fixtures/manual-reference-flow/
# durable_facts.json (5), derived_projections.json (5), walkthroughs.json (6) —
# 28 citation strings, zero semantic change (every M01/M02/M05 resolution
# assertion is unchanged and re-verified in this run). The frozen authority
# pins above are untouched: the Frozen Product/L2/DAG v0.2 blobs and immutable
# DAG v0.1 are byte-identical at the integrated tree.

REGISTRY_PATH = ROOT / "registries" / "state-dimensions-v1.json"

# M03: physical surfaces the manual flow must never imply. A token occurrence is
# acceptable only on a line that carries an explicit negation marker.
FORBIDDEN_SURFACE_TOKENS = (
    "scheduler daemon",
    "daemon",
    "database",
    "sqlite",
    "postgres",
    "redis",
    "kafka",
    "rabbitmq",
    "websocket",
    "grpc",
    "message queue",
    "cron",
    "runtime db",
    "proprietary transport",
)
NEGATION_MARKERS = ("no ", "not ", "never", "without", "nothing", "forbidden", "禁止")

# M05: RFC-2119 style keywords this descriptive reference must not issue on its own.
NORMATIVE_KEYWORDS = ("MUST", "MUST NOT", "SHALL", "SHALL NOT", "SHOULD", "REQUIRED")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def github_anchors(text: str) -> set[str]:
    """GitHub-style heading anchors: lowercase, punctuation stripped, spaces -> dashes."""
    anchors = set()
    for line in text.splitlines():
        match = re.match(r"^(#+) (.+)$", line)
        if match is None:
            continue
        segment = match.group(2).strip().lower()
        segment = re.sub(r"[^\w\- ]", "", segment)
        segment = segment.replace(" ", "-")
        anchors.add(segment)
    return anchors


def _json_contains_fragment(node: object, fragment: str) -> bool:
    """True when fragment is a key or a string value anywhere in a JSON tree."""
    if isinstance(node, dict):
        if fragment in node:
            return True
        return any(_json_contains_fragment(value, fragment) for value in node.values())
    if isinstance(node, list):
        return any(_json_contains_fragment(item, fragment) for item in node)
    if isinstance(node, str):
        return node == fragment
    return False


def candidate_paths(ref_path: str) -> list[Path]:
    candidates = [ROOT / ref_path]
    if "/" not in ref_path:
        # Repository convention: executable checks live under scripts/.
        candidates.append(ROOT / "scripts" / ref_path)
    return candidates


def resolve_ref(ref: str) -> None:
    """Assert an exact artifact reference resolves at the candidate (path + anchor).

    Mirrors the owner-ref resolution contract of scripts/test_v49_gate_currentness.py:
    refs are not decorative text; each must resolve against the repository.
    """
    path_part, _, frag = ref.partition("#")
    path = next((c for c in candidate_paths(path_part) if c.is_file()), None)
    if path is None:
        raise AssertionError(f"reference path does not resolve at candidate: {ref}")
    if not frag:
        return
    if path_part.endswith(".md"):
        anchors = github_anchors(path.read_text(encoding="utf-8"))
        if frag not in anchors:
            raise AssertionError(
                f"reference anchor missing in {path_part}: #{frag} "
                f"(available: {sorted(a for a in anchors if a.startswith(frag[:8]))})"
            )
    elif path_part.endswith(".json"):
        tree = json.loads(path.read_text(encoding="utf-8"))
        if not _json_contains_fragment(tree, frag):
            raise AssertionError(f"reference JSON fragment missing in {path_part}: #{frag}")
    # .py and other refs: file existence is the resolution contract.


_EXTRACT_RE = re.compile(
    r"\b[A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:md|json|py|yaml|yml)"
    r"(?:#[A-Za-z0-9_](?:[A-Za-z0-9._-]*[A-Za-z0-9_-])?)?"
)


def extract_exact_refs(text: str) -> list[str]:
    return sorted(set(_EXTRACT_RE.findall(text)))


def load_trigger_contract_module():
    spec = importlib.util.spec_from_file_location(
        "t013_pointer_only_trigger_contract",
        ROOT / "scripts" / "test_pointer_only_trigger_contract.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def collect_fixture_refs() -> list[str]:
    refs: list[str] = []
    for name in FIXTURE_FILES:
        data = load_fixture(name)

        def walk(node: object) -> None:
            if isinstance(node, dict):
                for key, value in node.items():
                    if key in {"owner_refs", "contract_owner_refs", "recompute_owner_ref"} and isinstance(
                        value, str
                    ):
                        refs.append(value)
                    elif key in {"owner_refs", "contract_owner_refs"} and isinstance(value, list):
                        refs.extend(v for v in value if isinstance(v, str))
                    else:
                        walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        walk(data)
    return sorted(set(refs))


class M01ReferenceResolutionTests(unittest.TestCase):
    def test_m01_every_doc_reference_resolves_at_candidate(self) -> None:
        text = DOC_PATH.read_text(encoding="utf-8")
        refs = extract_exact_refs(text)
        self.assertGreater(len(refs), 20, "flow doc must cite exact artifact refs")
        for ref in refs:
            with self.subTest(ref=ref):
                resolve_ref(ref)

    def test_m01_every_fixture_owner_reference_resolves(self) -> None:
        refs = collect_fixture_refs()
        self.assertGreater(len(refs), 10)
        for ref in refs:
            with self.subTest(ref=ref):
                resolve_ref(ref)

    def test_m01_frozen_blobs_resolve_unchanged_at_candidate(self) -> None:
        doc = normalized(DOC_PATH.read_text(encoding="utf-8"))
        for rel_path, blob in FROZEN_BLOBS_AT_HEAD.items():
            with self.subTest(path=rel_path):
                self.assertEqual(git("rev-parse", f"HEAD:{rel_path}"), blob)
                self.assertIn(blob, doc)
                self.assertIn(rel_path, doc)

    def test_m01_immutable_dag_v01_concern_blob_resolves(self) -> None:
        self.assertEqual(git("cat-file", "-t", DAG_V01_BLOB), "blob")
        self.assertIn("### T-013", git("cat-file", "-p", DAG_V01_BLOB))
        self.assertIn(DAG_V01_BLOB, DOC_PATH.read_text(encoding="utf-8"))


class M02DurableVsDerivedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.durable = load_fixture("durable_facts.json")
        cls.derived = load_fixture("derived_projections.json")
        cls.fact_ids = {f["fact_id"] for f in cls.durable["facts"]}
        cls.projection_ids = {p["projection_id"] for p in cls.derived["projections"]}
        cls.registry_rules = {
            rule["rule_id"] for rule in json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))["forbidden_inferences"]
        }

    def test_m02_durable_facts_read_from_git_github_or_repository_surfaces(self) -> None:
        allowed = set(self.durable["allowed_surfaces"])
        self.assertEqual(allowed, {"git", "github-api", "repository-file"})
        for fact in self.durable["facts"]:
            with self.subTest(fact=fact["fact_id"]):
                self.assertEqual(fact["kind"], "durable")
                self.assertIn(fact["surface"], allowed)
                command = fact["read"].strip()
                self.assertTrue(
                    command.startswith("git ") or command.startswith("gh "),
                    f"durable read must be a git/gh surface read: {fact['fact_id']}",
                )
                self.assertTrue(fact["example_observation"].strip())
                self.assertTrue(fact["owner_refs"], "durable fact must cite its owner")
                for ref in fact["owner_refs"]:
                    resolve_ref(ref)

    def test_m02_derived_projections_are_marked_non_authoritative_projections(self) -> None:
        for projection in self.derived["projections"]:
            with self.subTest(projection=projection["projection_id"]):
                self.assertEqual(projection["kind"], "derived")
                self.assertTrue(projection["non_authoritative"])
                self.assertTrue(projection["recomputed_not_cached"])
                self.assertTrue(projection["never_canonical_issue_state"])
                self.assertTrue(projection["derived_from"], "projection must name its fact provenance")
                self.assertTrue(projection["owner_refs"])
                for ref in projection["owner_refs"]:
                    resolve_ref(ref)
                for rule_id in projection["forbidden_inference_avoided"]:
                    self.assertIn(rule_id, self.registry_rules)

    def test_m02_projection_provenance_terminates_in_durable_facts(self) -> None:
        known = self.fact_ids | self.projection_ids
        for projection in self.derived["projections"]:
            for source in projection["derived_from"]:
                self.assertIn(source, known, f"unknown provenance id {source}")

        def reaches_fact(projection_id: str, seen: frozenset[str]) -> bool:
            if projection_id in seen:
                return False
            projection = next(p for p in self.derived["projections"] if p["projection_id"] == projection_id)
            return any(
                source in self.fact_ids
                or (source in self.projection_ids and reaches_fact(source, seen | {projection_id}))
                for source in projection["derived_from"]
            )

        for projection_id in self.projection_ids:
            self.assertTrue(reaches_fact(projection_id, frozenset()))

    def test_m02_doc_states_distinction_and_agrees_with_fixtures(self) -> None:
        doc = normalized(DOC_PATH.read_text(encoding="utf-8"))
        self.assertIn("A **durable fact** lives on a GitHub/repository surface", doc)
        self.assertIn("A **derived state** is a recomputable projection over durable facts", doc)
        self.assertIn("durable_facts.json", doc)
        self.assertIn("derived_projections.json", doc)

        walkthrough_doc_ids = {"W-A", "W-B", "W-C", "W-D", "W-E"}
        fixture_walkthroughs = {
            w["walkthrough_id"] for w in load_fixture("walkthroughs.json")["walkthroughs"]
        }
        self.assertEqual(fixture_walkthroughs, walkthrough_doc_ids)
        for walkthrough_id in fixture_walkthroughs:
            self.assertIn(walkthrough_id, doc)

        mentioned_facts = {fid for fid in self.fact_ids if fid in doc}
        self.assertTrue(mentioned_facts, "doc must name at least its durable-fact examples")

        triggers = load_fixture("pointer_triggers.json")
        for trigger in triggers["conforming"] + triggers["nonconforming"]:
            self.assertIn(trigger, normalized(doc))


class M03NoInfrastructureImpliedTests(unittest.TestCase):
    def test_m03_doc_and_fixtures_imply_no_daemon_db_or_proprietary_transport(self) -> None:
        surfaces: list[tuple[str, str]] = [
            (str(DOC_PATH), DOC_PATH.read_text(encoding="utf-8"))
        ]
        for name in FIXTURE_FILES:
            path = FIXTURE_DIR / name
            surfaces.append((str(path), path.read_text(encoding="utf-8")))
        for source, text in surfaces:
            for line in text.splitlines():
                lowered = line.lower()
                for token in FORBIDDEN_SURFACE_TOKENS:
                    if token not in lowered:
                        continue
                    with self.subTest(source=source, token=token, line=line.strip()[:120]):
                        self.assertTrue(
                            any(marker in lowered for marker in NEGATION_MARKERS),
                            f"forbidden surface token without negation in {source}: {token}",
                        )

    def test_m03_all_reads_are_git_or_gh_commands(self) -> None:
        durable = load_fixture("durable_facts.json")
        for fact in durable["facts"]:
            with self.subTest(fact=fact["fact_id"]):
                self.assertRegex(fact["read"].strip(), r"^(git|gh) \S")

    def test_m03_doc_declares_the_boundary_positively(self) -> None:
        doc = normalized(DOC_PATH.read_text(encoding="utf-8"))
        self.assertIn("requires only:", doc)
        self.assertIn("requires no scheduler daemon, no runtime database, and no proprietary transport", doc)


class M04PointerOnlyTriggerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = load_trigger_contract_module()
        cls.triggers = load_fixture("pointer_triggers.json")
        cls.doc = normalized(DOC_PATH.read_text(encoding="utf-8"))

    def test_m04_conforming_examples_match_the_pointer_only_contract(self) -> None:
        self.assertGreaterEqual(len(self.triggers["conforming"]), 4)
        for trigger in self.triggers["conforming"]:
            with self.subTest(trigger=trigger):
                self.assertTrue(
                    self.contract.is_pointer_only(trigger),
                    f"example advertised as conforming violates the contract: {trigger}",
                )
                self.assertIn(trigger, self.doc)

    def test_m04_nonconforming_examples_are_rejected_by_the_contract(self) -> None:
        self.assertGreaterEqual(len(self.triggers["nonconforming"]), 3)
        for trigger in self.triggers["nonconforming"]:
            with self.subTest(trigger=trigger):
                self.assertFalse(
                    self.contract.is_pointer_only(trigger),
                    f"example advertised as non-conforming passes the contract: {trigger}",
                )
                self.assertIn(trigger, self.doc)

    def test_m04_fixture_and_doc_bind_the_contract_owner(self) -> None:
        self.assertIn(
            "standards/ISSUE_FIRST_TASK_TRIGGER.md#user-visible-trigger-contract",
            self.triggers["contract_owner_refs"],
        )
        self.assertIn(
            "standards/ISSUE_FIRST_TASK_TRIGGER.md#user-visible-trigger-contract",
            collect_fixture_refs(),
        )
        self.assertIn(
            "standards/ISSUE_FIRST_TASK_TRIGGER.md#user-visible-trigger-contract",
            extract_exact_refs(self.doc),
        )


class M05DescriptiveOnlyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = DOC_PATH.read_text(encoding="utf-8")
        cls.doc = normalized(cls.raw)

    def test_m05_status_is_descriptive_and_non_authoritative(self) -> None:
        head = " ".join(self.raw.splitlines()[:6])
        self.assertIn("Status: **descriptive operator/controller reference — non-authoritative.**", head)
        self.assertIn("it creates no normative semantics", self.doc)

    def test_m05_no_self_issued_normative_keywords(self) -> None:
        for keyword in NORMATIVE_KEYWORDS:
            with self.subTest(keyword=keyword):
                self.assertNotIn(keyword, self.raw)

    def test_m05_each_walkthrough_cites_its_owner_refs(self) -> None:
        for walkthrough in load_fixture("walkthroughs.json")["walkthroughs"]:
            with self.subTest(walkthrough=walkthrough["walkthrough_id"]):
                self.assertIn(walkthrough["walkthrough_id"], self.raw)
                self.assertGreater(len(walkthrough["owner_refs"]), 0)
                for ref in walkthrough["owner_refs"]:
                    path_part, _, frag = ref.partition("#")
                    if frag:
                        self.assertIn(f"{path_part}#{frag}", self.raw)
                    else:
                        self.assertIn(path_part, self.raw)
                    resolve_ref(ref)

    def test_m05_closing_non_goals_keep_owner_authority(self) -> None:
        self.assertIn("descriptive only", self.doc)
        self.assertIn("never substitutes a walkthrough for an owner-issued verdict", self.doc)
        self.assertIn(
            "docs/implementation/4.9.0/L3_REFERENCE_PACKS.md#t-013--manual--github-native-reference-flow-732",
            extract_exact_refs(self.raw),
        )


class FixtureInventoryTests(unittest.TestCase):
    def test_fixture_directory_contains_exactly_the_declared_files(self) -> None:
        files = sorted(p.name for p in FIXTURE_DIR.iterdir() if p.is_file())
        self.assertEqual(files, sorted(FIXTURE_FILES))

    def test_walkthroughs_reference_existing_fixture_ids(self) -> None:
        durable = {f["fact_id"] for f in load_fixture("durable_facts.json")["facts"]}
        derived = {p["projection_id"] for p in load_fixture("derived_projections.json")["projections"]}
        for walkthrough in load_fixture("walkthroughs.json")["walkthroughs"]:
            for step in walkthrough["steps"]:
                for fact_id in step["reads"]:
                    self.assertIn(fact_id, durable)
                for projection_id in step.get("derived", []):
                    self.assertIn(projection_id, derived)


if __name__ == "__main__":
    unittest.main()
