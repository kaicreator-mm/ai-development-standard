"""V411-T12 integrated A+B+C conformance runner.

This runner composes already-landed v4.11 owner executable oracles. It does not
reimplement their policy logic and it never turns historical PASS into current
release truth. The committed registry contains expected inputs/oracle bindings
only; actual evidence is emitted at runtime.
"""
from __future__ import annotations

import importlib.util
import io
from contextlib import nullcontext
from unittest.mock import patch
import json
from pathlib import Path
import subprocess
import tempfile
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
REGISTRY = ROOT / "tests" / "fixtures" / "v411" / "t12" / "scenarios.json"
INTEGRATION_BASE = "301ebcdae1ad3a2cec8cd23627b2423282f98997"
EXPECTED_IDS = {f"S{i:02d}" for i in range(1, 19)} | {f"X{i:02d}" for i in range(1, 9)}
REQUIRED_FIELDS = {
    "case_id", "polarity", "archetype", "adoption_profile", "adoption_level",
    "job_labels", "actual_source_refs", "affected_source_base", "affected_source_head",
    "actor", "operator_session", "permissions", "authority_refs", "owner_refs",
    "mandatory_gates", "fidelity", "setup", "runner", "assertions",
    "expected_transition", "expected_effect_count", "equivalence_class", "exceptions",
}
ALLOWED_WRITE_PREFIXES = (
    "scripts/test_v411_t12_abc_conformance.py",
    "tests/fixtures/v411/t12/",
)
DOWNSTREAM_RELEASE_IDS = {"S11", "X04"}
PHYSICAL_DENY_IDS = {"S08", "X01"}
REQUIRED_PHYSICAL_DENY_TEST = (
    "scripts/test_v411_t09_effect_boundary.py",
    "test_claimed_a_current_deny_blocks_before_real_sink_mutation",
)
_module_cache: dict[str, object] = {}


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, encoding="utf-8"
    )
    if proc.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def changed_paths() -> list[str]:
    return [p for p in git("diff", "--name-only", INTEGRATION_BASE, "HEAD").splitlines() if p]


def load_owner_module(rel: str):
    cached = _module_cache.get(rel)
    if cached is not None:
        return cached
    path = ROOT / rel
    if not path.is_file():
        raise AssertionError(f"owner runner missing: {rel}")
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    module_name = "v411_t12_owner_" + path.stem
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load owner runner: {rel}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    _module_cache[rel] = module
    return module


def resolve_test(rel: str, method: str) -> unittest.TestCase:
    module = load_owner_module(rel)
    matches: list[type[unittest.TestCase]] = []
    for value in vars(module).values():
        if isinstance(value, type) and issubclass(value, unittest.TestCase) and hasattr(value, method):
            matches.append(value)
    if len(matches) != 1:
        raise AssertionError(
            f"{rel}::{method} resolves to {len(matches)} unittest cases, expected exactly one"
        )
    return matches[0](method)


def execute_owner_test(spec: dict) -> dict:
    """Execute the real owner's assertion and capture side effects separately.

    unittest success is only an observation of an owner assertion, NOT an
    observed canonical policy transition. For T09, intercept the already
    authoritative SQLite sink boundary after the actual attempted operation;
    no fixture expected value can substitute for readback.
    """
    rel = spec.get("file")
    method = spec.get("test")
    if not isinstance(rel, str) or not isinstance(method, str):
        return {"ok": False, "error": "malformed owner test binding", "spec": spec}
    try:
        case = resolve_test(rel, method)
        module = load_owner_module(rel)
        sink_observations = []
        context = nullcontext()
        if rel == "scripts/test_v411_t09_effect_boundary.py":
            sink_class = module.PersistentSafeSink
            original_execute = sink_class.execute

            def observed_execute(sink, *args, **kwargs):
                result = original_execute(sink, *args, **kwargs)
                sink_observations.append({
                    "outcome": result.get("outcome"),
                    "reported_before": result.get("before"),
                    "reported_after": result.get("after"),
                    "actual_effect_count_readback": sink.effect_count(),
                    "attempt_id": kwargs.get("attempt_id"),
                    "effect_id": kwargs.get("effect_id"),
                    "observation_source": "PersistentSafeSink.execute + SQLite COUNT(*)",
                    "fidelity": "ISOLATED_TEST_SQLITE_NOT_EXTERNAL_HUMAN_AUTHORITY",
                })
                return result
            context = patch.object(sink_class, "execute", observed_execute)

        stream = io.StringIO()
        # Run through an isolated TestSuite so owner setUpClass is honored.
        suite = unittest.TestSuite([case])
        with context:
            result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
        return {
            "ok": result.wasSuccessful() and result.testsRun == 1 and not result.skipped,
            "file": rel,
            "test": method,
            "tests_run": result.testsRun,
            "failures": [msg for _, msg in result.failures],
            "errors": [msg for _, msg in result.errors],
            "skipped": [reason for _, reason in result.skipped],
            "assertion_observation": "PASS" if result.wasSuccessful() and not result.skipped else "FAIL",
            "sink_observations": sink_observations,
            "output": stream.getvalue().strip(),
        }
    except Exception as exc:
        return {"ok": False, "file": rel, "test": method, "error": repr(exc),
                "sink_observations": [], "assertion_observation": "FAIL"}


def validate_registry(doc: dict) -> list[str]:
    problems: list[str] = []
    if doc.get("schema_version") != "ai-dev/v411-t12-scenarios-v1":
        problems.append("wrong schema_version")
    if doc.get("integration_base") != INTEGRATION_BASE:
        problems.append("integration_base mismatch")
    if doc.get("logical_case_count") != 26 or doc.get("executable_record_count") != 52:
        problems.append("denominator mismatch")
    scenarios = doc.get("scenarios")
    if not isinstance(scenarios, dict) or set(scenarios) != EXPECTED_IDS:
        problems.append("scenario ID set is not exactly S01-S18 + X01-X08")
        return problems
    for case_id in sorted(EXPECTED_IDS):
        pair = scenarios.get(case_id)
        if not isinstance(pair, dict) or set(pair) != {"positive", "negative"}:
            problems.append(f"{case_id}: requires exactly positive+negative")
            continue
        for polarity in ("positive", "negative"):
            rec = pair[polarity]
            if not isinstance(rec, dict):
                problems.append(f"{case_id}/{polarity}: record is not an object")
                continue
            missing = REQUIRED_FIELDS - set(rec)
            if missing:
                problems.append(f"{case_id}/{polarity}: missing {sorted(missing)}")
            if rec.get("case_id") != case_id or rec.get("polarity") != polarity:
                problems.append(f"{case_id}/{polarity}: identity mismatch")
            if rec.get("affected_source_base") != INTEGRATION_BASE or rec.get("affected_source_head") != INTEGRATION_BASE:
                problems.append(f"{case_id}/{polarity}: owner-source base/head must bind post-T11 merge")
            if not rec.get("actual_source_refs") or not rec.get("owner_refs"):
                problems.append(f"{case_id}/{polarity}: missing real owner source/oracle refs")
            for rel in rec.get("actual_source_refs", []):
                if not isinstance(rel, str) or not (ROOT / rel).exists():
                    problems.append(f"{case_id}/{polarity}: source ref missing: {rel!r}")
            runner = rec.get("runner", {})
            tests = runner.get("tests") if isinstance(runner, dict) else None
            if runner.get("type") != "unittest-owner-methods" or not isinstance(tests, list) or not tests:
                problems.append(f"{case_id}/{polarity}: executable owner tests absent")
            forbidden_actual = {"tested_sha", "tested_tree", "exit", "observed_transition",
                                "observed_effect", "gate_disposition", "result", "currentness",
                                "evidence_refs"}
            if forbidden_actual & set(rec):
                problems.append(f"{case_id}/{polarity}: committed fixture pre-fills runtime truth")
        if case_id in DOWNSTREAM_RELEASE_IDS:
            for polarity in ("positive", "negative"):
                rec = pair[polarity]
                if rec.get("fidelity") != "CONTRACT_SIMULATION_NO_RELEASE_PASS":
                    problems.append(f"{case_id}/{polarity}: release fidelity can mint false release truth")
                if "DOWNSTREAM_RELEASE_NOT_RUN" not in rec.get("expected_transition", ""):
                    problems.append(f"{case_id}/{polarity}: downstream release must stay NOT_RUN")
        if case_id in PHYSICAL_DENY_IDS:
            neg_tests = {
                (x.get("file"), x.get("test"))
                for x in pair["negative"].get("runner", {}).get("tests", [])
                if isinstance(x, dict)
            }
            if REQUIRED_PHYSICAL_DENY_TEST not in neg_tests:
                problems.append(f"{case_id}/negative: physical safe-sink DENY oracle not bound")
            if pair["negative"].get("expected_effect_count") != 0:
                problems.append(f"{case_id}/negative: expected effect count must be zero")
    compound = doc.get("compound")
    if not isinstance(compound, dict) or compound.get("id") != "J09+J10+J11+J12":
        problems.append("mandatory J09+J10+J11+J12 compound absent")
    elif not compound.get("tests"):
        problems.append("mandatory compound has no executable owner tests")
    return problems


def validate_write_set() -> list[str]:
    problems = []
    if git("merge-base", "--is-ancestor", INTEGRATION_BASE, "HEAD") != "":
        pass
    for path in changed_paths():
        if not any(path == prefix or path.startswith(prefix) for prefix in ALLOWED_WRITE_PREFIXES):
            problems.append(f"owner-conflict write outside T12 unique paths: {path}")
    return problems


def execute_x01_same_subject(polarity: str, tested_sha: str, tested_tree: str) -> dict:
    """Exercise T01 fact/owner conjunction and T09 *actual* SQLite effect sink
    on ONE identical work subject, preserving the TEST-ONLY human authority
    class. No actual external human authorization or Release PASS is inferred.
    """
    t01 = load_owner_module("scripts/test_v411_t01_effective_rules.py")
    t09 = load_owner_module("scripts/test_v411_t09_effect_boundary.py")
    subject = t01.SERVICE_X01_SUBJECT
    facts = (
        t01.service_x01_fixture(owner_proofs=t01.all_pass_proofs())
        if polarity == "positive"
        else t01.service_x01_fixture(declared_jobs={"J03_BUG_FIX"})
    )
    policy = t01.resolve_effective_rules(facts)
    with tempfile.TemporaryDirectory(prefix="v411-t12-x01-") as temp:
        sink = t09.PersistentSafeSink(Path(temp) / "x01-effects.sqlite3")
        try:
            human = t09.decision(
                "APPROVE" if polarity == "positive" else "DENY",
                subject_head=subject,
                ref="t12-x01-test-only-authority",
            )
            a = t09.claim("operator:A", 7, subject_head=subject)
            attempt_a = sink.execute(
                claim_record=a, authority=human,
                effect_id="t12-x01-a", attempt_id="t12-x01-attempt-a",
                payload="isolated-test-payload",
            )
            attempts = [{
                "actor": a["actor"], "outcome": attempt_a["outcome"],
                "effect_count_after": sink.effect_count(),
                "attempt_id": "t12-x01-attempt-a",
            }]
            if polarity == "negative":
                b = t09.claim("operator:B", 8, subject_head=subject)
                attempt_b = sink.execute(
                    claim_record=b, authority=human,
                    effect_id="t12-x01-b", attempt_id="t12-x01-attempt-b",
                    payload="denied-successor-retry",
                )
                attempts.append({
                    "actor": b["actor"], "outcome": attempt_b["outcome"],
                    "effect_count_after": sink.effect_count(),
                    "attempt_id": "t12-x01-attempt-b",
                })
            count = sink.effect_count()
        finally:
            sink.close()
    is_positive = polarity == "positive"
    expected_resolution = "ADMITTED" if is_positive else "UNVERIFIED_GATES"
    expected_effect = 1 if is_positive else 0
    expected_outcome = "ACKNOWLEDGED" if is_positive else "BLOCKED"
    ok = (
        facts["exact_subject"] == subject
        and human["subject_head"] == subject
        and a["subject_head"] == subject
        and policy["resolution"] == expected_resolution
        and count == expected_effect
        and all(x["outcome"] == expected_outcome for x in attempts)
        and (not is_positive or len(attempts) == 1)
        and (is_positive or len(attempts) == 2)
    )
    return {
        "test_contract_ok": ok,
        "subject": subject,
        "candidate_sha": tested_sha,
        "candidate_tree": tested_tree,
        "fact_based_owner_resolution": policy["resolution"],
        "declared_jobs": sorted(facts["declared_jobs"]),
        "same_subject_join": facts["exact_subject"] == human["subject_head"] == a["subject_head"],
        "current_human_source_fidelity": "LOCAL_UNIT_AUTHORITY_FIXTURE_NOT_REAL_HUMAN",
        "attempts": attempts,
        "observed_effect_count": count,
        "source_owners": ["T01 effective-rule resolver", "T09 persistent SQLite effect sink"],
        "release_effect": "NONE",
    }


def execute_x02_same_subject(polarity: str, tested_sha: str, tested_tree: str) -> dict:
    """T03+T04+T05 one-subject A/B/C contract, test-fixture fidelity only.

    The accepted spec projection, upstream reuse/license decision and actual
    canonical Review event admission all bind to the SAME exact H subject.
    This does not establish actual remote upstream inspection/licensing.
    """
    t03 = load_owner_module("scripts/test_v411_t03_spec_implementation_currentness.py")
    t04 = load_owner_module("scripts/test_v411_t04_reuse_first.py")
    t05 = load_owner_module("scripts/test_v411_t05_event_authority.py")
    subject = t05.H
    spec_facts = dict(t03.P01_PROJECTION)
    spec_facts["implementation_subject_ref"] = subject
    spec_facts["evidence_subject_ref"] = subject
    spec = t03.decide(spec_facts)
    drift = polarity == "negative"
    upstream_facts = t04.h3_case(subject=subject, upstream_license_changed=drift)
    reuse = t04.evaluate_reuse(upstream_facts)
    boundary = t05.make_boundary()
    admitted = boundary.admit(t05.review_pass(subject, "src-review-1"))
    review = boundary.current_review(subject)
    matches = (
        spec_facts["implementation_subject_ref"] ==
        spec_facts["evidence_subject_ref"] ==
        upstream_facts["subject"] ==
        subject == boundary.live_subject
    )
    expected_reuse = "BLOCKED" if drift else "ALLOWED"
    ok = (
        matches and spec["decision"] == "RECONCILED"
        and reuse["decision"] == expected_reuse
        and admitted.status == "ACCEPTED"
        and review.judgment == "PASS"
        and (not drift or "license_notice_observation_at_current_revision" in reuse["missing"])
    )
    # The negative oracle must demonstrate a forbidden composite admission
    # despite separately green spec and Review; it never regards the negative
    # upstream block as a successful permission to reuse.
    allowed = (
        spec["decision"] == "RECONCILED" and reuse["decision"] == "ALLOWED"
        and review.judgment == "PASS"
    )
    if drift and allowed:
        ok = False
    return {
        "test_contract_ok": ok,
        "subject": subject,
        "candidate_sha": tested_sha, "candidate_tree": tested_tree,
        "same_subject_join": matches,
        "spec_owner_state": spec["decision"],
        "reuse_owner_state": reuse["decision"],
        "reuse_missing": reuse["missing"],
        "event_admission": admitted.status,
        "review_owner_state": review.judgment,
        "combined_authorization": "CONTRACT_SIMULATION_POSITIVE" if allowed else "DENIED_BY_CURRENT_LICENSE_OWNER",
        "negative_attempted": drift,
        "source_owners": [
            "T03 spec/implementation reconciler",
            "T04 revision-bound reuse evaluator",
            "T05 canonical event admission+current Review reducer",
        ],
        "fidelity": "LOCAL_SYNTHETIC_SOURCE_AND_OPERATOR_TEST_FIXTURES_NOT_REAL_UPSTREAM_RIGHT",
        "release_effect": "NONE",
    }


def execute_s17_same_subject_review(polarity: str, tested_sha: str, tested_tree: str) -> dict:
    """Observe T05 accepted current Review facts and reducer, not fixture text.

    One subject; opposite accepted outcomes must make current review BLOCKED,
    never latest-wins. This proves B/Interaction at owner-model fidelity, not
    independent Product/risk/A evidence or Release merge authority.
    """
    t05 = load_owner_module("scripts/test_v411_t05_event_authority.py")
    subject = t05.H
    boundary = t05.make_boundary()
    first = boundary.admit(t05.review_pass(subject, "src-review-1"))
    decisions = [{"kind": "PASS", "admission": first.status}]
    if polarity == "negative":
        second = boundary.admit(t05.review_fail(subject, "src-review-2"))
        decisions.append({"kind": "FAIL", "admission": second.status})
    review = boundary.current_review(subject)
    actual = review.judgment
    expected = "PASS" if polarity == "positive" else "BLOCKED"
    ok = (
        all(x["admission"] == "ACCEPTED" for x in decisions)
        and actual == expected and boundary.live_subject == subject
        and (polarity != "negative" or len(review.conflict_refs) == 2)
    )
    return {
        "test_contract_ok": ok, "subject": subject,
        "candidate_sha": tested_sha, "candidate_tree": tested_tree,
        "admission_events": decisions,
        "observed_review_judgment": actual,
        "observed_conflicting_refs": list(review.conflict_refs),
        "expected_review_judgment": expected,
        "fidelity": "T05_OWNER_CANONICAL_EVENT_FIXTURE_NOT_LIVE_GITHUB",
        "source_owners": ["T05 event admission and Review reducer"],
        "release_effect": "NONE",
    }


def execute_docs_risk_role_same_subject(
    case_id: str, polarity: str, tested_sha: str, tested_tree: str
) -> dict:
    """S01/X08: T02 inspected risk -> T13 role conduct, one exact subject.

    An inspected-absence A0 docs path is a proportionate legal trace. A
    docs-only label over material code is rejected by T02; T13 receives the
    ACTUAL T02 inventory as its input and denies the uncovered required
    evidence. No fresh risk facts are invented by this adapter.
    """
    t02 = load_owner_module("scripts/test_v411_t02_risk_intake.py")
    t13 = load_owner_module("scripts/test_v411_t13_role_conduct.py")
    subject = t02.HEAD_A
    if polarity == "positive":
        source = t02.inspected_absent_fixture(subject=subject, docs_only_claim=True)
    else:
        source = t02.base_fixture()
        source["subject"] = subject
        source["declared_jobs"] = {"J02_DOCS_LOW_RISK"}
        source["label_claims"] = {"docs_only": True}
    risk = t02.inventory(source)
    conduct_input = t13.docs_a0_fixture()
    conduct_input["subject_head"] = source["candidate_head"]
    conduct_input["input_refs"] = dict(source["candidate_tree"])
    conduct_input["allowed_acts_scope"] = tuple(sorted(source["candidate_tree"]))
    conduct_input["inventory"] = [
        t13._inventory_record(
            rec["source_path"],
            rec["material_class_observed"] if rec["epistemic_state"] == "PRESENT" else None,
            rec["epistemic_state"],
            rec["currentness"],
            rec["inspected_ref"],
        )
        for rec in risk["records"]
    ]
    conduct = t13.conduct_trace(conduct_input)
    same_subject = (
        risk["subject"] == source["subject"]
        == source["candidate_head"] == conduct_input["subject_head"]
        == subject
    )
    positive = polarity == "positive"
    ok = (
        same_subject
        and (
            risk["decision"] == "PROPORTIONATE_ABSENT_FAST_PATH"
            and conduct["decision"] == "CONDUCT_TRACE_COMPLETE"
            and not risk["required_gate_set"]
            and not conduct["required_gate_set"]
            if positive else
            risk["decision"] == "BLOCKED"
            and conduct["decision"] == "EXIT_DENIED"
            and bool(risk["required_gate_set"])
            and risk["required_gate_set"] == conduct["required_gate_set"]
            and "required_evidence_missing" in conduct["refusal_grounds"]
        )
    )
    return {
        "test_contract_ok": ok,
        "case_id": case_id,
        "subject": subject,
        "candidate_sha": tested_sha,
        "candidate_tree": tested_tree,
        "same_subject_join": same_subject,
        "risk_owner_state": risk["decision"],
        "risk_required_gates": sorted(risk["required_gate_set"]),
        "material_inventory_records": risk["records"],
        "conduct_owner_state": conduct["decision"],
        "conduct_required_gates": sorted(conduct["required_gate_set"]),
        "conduct_refusal_grounds": sorted(conduct["refusal_grounds"]),
        "fidelity": "LOCAL_T02_T13_SYNTHETIC_SOURCE_INSPECTION_NOT_REAL_RISK_READBACK",
        "source_owners": [
            "T02 material-risk inspection inventory",
            "T13 floor-preserving role conduct trace",
        ],
        "release_effect": "NONE",
    }


def run_record(record: dict, tested_sha: str, tested_tree: str) -> dict:
    test_results = [execute_owner_test(spec) for spec in record["runner"]["tests"]]
    ok = all(item.get("ok") for item in test_results)
    case_id = record["case_id"]
    release_contract = case_id in DOWNSTREAM_RELEASE_IDS
    sink = [entry for test in test_results for entry in test.get("sink_observations", [])]
    # Never project "expected_effect_count" as a sensor reading.  In the
    # physical DENY cases, insist on a real executed sink attempt and its
    # persisted database COUNT readback. Other scenarios lack effect sensors.
    actual_effect_count = (
        max(entry["actual_effect_count_readback"] for entry in sink)
        if sink else None
    )
    expectation = record.get("expected_effect_count")
    physical_deny = case_id in PHYSICAL_DENY_IDS and record["polarity"] == "negative"
    physical_ok = (
        not physical_deny or
        (bool(sink) and actual_effect_count == 0 and
         all(x["outcome"] == "BLOCKED" for x in sink))
    )
    if physical_deny and expectation != 0:
        physical_ok = False
    x01_probe = (
        execute_x01_same_subject(record["polarity"], tested_sha, tested_tree)
        if case_id == "X01" else None
    )
    x02_probe = (
        execute_x02_same_subject(record["polarity"], tested_sha, tested_tree)
        if case_id == "X02" else None
    )
    docs_probe = (
        execute_docs_risk_role_same_subject(case_id, record["polarity"], tested_sha, tested_tree)
        if case_id in {"S01", "X08"} else None
    )
    local_probe = next((x for x in (x01_probe, x02_probe, docs_probe) if x is not None), None)
    review_probe = (
        execute_s17_same_subject_review(record["polarity"], tested_sha, tested_tree)
        if case_id == "S17" else None
    )
    contract_ok = (
        ok and physical_ok
        and (local_probe is None or local_probe["test_contract_ok"])
        and (review_probe is None or review_probe["test_contract_ok"])
    )
    if x01_probe is not None:
        # An actual, separate, physical adapter readback overrides no source
        # field blindly.  The same-subject probe has stronger fidelity than
        # the standalone owner test's fixture assertions.
        actual_effect_count = x01_probe["observed_effect_count"]
    # Executed unittest assertions are observed. A domain policy transition
    # is NOT observed merely because the assertions passed; only a recorded
    # owner operation (here an actual safe SQLite effect attempt) can give
    # a bounded transition observation.
    transition = (
        [x["outcome"] for x in x01_probe["attempts"]] if x01_probe is not None
        else [x["outcome"] for x in sink] if sink
        else [review_probe["observed_review_judgment"]] if review_probe
        else [docs_probe["risk_owner_state"], docs_probe["conduct_owner_state"]] if docs_probe
        else None
    )
    source_readbacks = []
    for rel in sorted(set(record["actual_source_refs"])):
        # A checked-in source is a material identity only if its exact blob
        # resolves at the frozen integration base AND current candidate.
        # The current candidate SHA is not inferred from the fixture.
        base_blob = git("rev-parse", f"{INTEGRATION_BASE}:{rel}")
        current_blob = git("rev-parse", f"HEAD:{rel}")
        source_readbacks.append({
            "path": rel,
            "base_blob": base_blob,
            "actual_current_blob": current_blob,
            "candidate_sha": tested_sha,
            "same_as_post_t11_base": base_blob == current_blob,
            "evidence_kind": "GIT_SOURCE_BLOB_NOT_MATERIAL_RISK_INSPECTION",
        })
    owner_facts = [{
        "file": t.get("file"),
        "method": t.get("test"),
        "tested_sha": tested_sha,
        "tested_tree": tested_tree,
        "assertion_observation": t.get("assertion_observation"),
    } for t in test_results]
    # A, B and C have different meanings. We do not fan one suite-wide
    # Boolean into three purported independent material proofs.
    a_files = (
        "test_v411_t01_", "test_v411_t02_", "test_v411_t03_",
        "test_v411_t04_", "test_v411_t10_", "test_v411_t13_",
    )
    b_files = (
        "test_v411_t05_", "test_v411_t06_", "test_v411_t08_",
        "test_v411_t09_", "test_v411_merge_admission",
    )
    def layer_fact(t, prefixes):
        return any(t.get("file", "").split("/")[-1].startswith(p) for p in prefixes)
    a_facts = [x for x in owner_facts if layer_fact(x, a_files)]
    b_facts = [x for x in owner_facts if layer_fact(x, b_files)]
    a_ok = bool(a_facts) and all(x["assertion_observation"] == "PASS" for x in a_facts)
    b_ok = bool(b_facts) and all(x["assertion_observation"] == "PASS" for x in b_facts)
    # Even with two sets of owner-method successes, their *internal fixture*
    # subjects are not necessarily the same S/X work item. That actual
    # fact-composition proof remains unresolved. A common Git HEAD alone
    # cannot establish common subject.
    if local_probe is not None and local_probe["test_contract_ok"]:
        b_ok = True  # Genuine B owner invocation on the same test subject.
    if review_probe is not None and review_probe["test_contract_ok"]:
        b_ok = True  # T05 admitted event and current reducer, not source prose.
    p3_state = (
        "PASS" if contract_ok and local_probe is not None
        else "BLOCKED" if contract_ok else "FAIL"
    )
    proof_layers = {
        "P1_A": {"state": "PASS" if a_ok else ("NOT_RUN" if not a_facts else "FAIL"),
                 "fidelity": "OWNER_UNIT_ASSERTIONS", "evidence": a_facts},
        "P2_B": {"state": "PASS" if b_ok else ("NOT_RUN" if not b_facts else "FAIL"),
                 "fidelity": "LOCAL_OWNER_ADAPTER_SAME_SUBJECT" if local_probe else "OWNER_UNIT_ASSERTIONS",
                 "evidence": b_facts,
                 "same_subject_probe": local_probe if local_probe is not None else review_probe},
        "P3_C": {"state": p3_state,
                 "fidelity": "LOCAL_OWNER_ADAPTER_SIMULATION_SAME_SUBJECT" if local_probe else "INTEGRATED_SAME_SUBJECT_NOT_ESTABLISHED",
                 "reason": "TEST-ONLY shared subject with executed owner decisions" if local_probe else "owner unit fixtures are independently constructed",
                 "a_supported": a_ok, "b_supported": b_ok},
    }
    return {
        "case_id": case_id,
        "polarity": record["polarity"],
        "tested_sha": tested_sha,
        "tested_tree": tested_tree,
        "command": "python scripts/test_v411_t12_abc_conformance.py",
        "exit": 0 if contract_ok else 1,
        "asserted_expected_transition": record["expected_transition"],
        "observed_transition": transition,
        "observed_owner_assertions": "PASS" if ok else "FAIL",
        "source_readbacks": source_readbacks,
        "same_subject_execution": local_probe,
        "review_same_subject_execution": review_probe,
        "source_currentness_scope": "GIT_BLOB_READBACK_ONLY_NO_AFFECTED_RISK_CLAIM",
        "expected_effect_count": expectation,
        "observed_effect": actual_effect_count,
        "sink_readback_provenance": sink,
        "gate_disposition": "NOT_RUN" if release_contract else p3_state,
        "proof_layers": proof_layers,
        "result": (
            "PASS_TEST_ONLY_SAME_SUBJECT_CONTRACT"
            if contract_ok and local_probe is not None
            else "PASS_OWNER_ASSERTIONS_INTEGRATION_BLOCKED"
            if contract_ok else "FAIL"
        ),
        "currentness": (
            "CURRENT_TEST_SUBJECT_BUT_REAL_AUTHORITY_NOT_PROVEN"
            if contract_ok and local_probe is not None
            else "SOURCE_HEAD_CURRENT_OWNER_ASSERTIONS;WORK_SUBJECT_NOT_PROVEN"
            if contract_ok else "UNVERIFIED"
        ),
        "fidelity": record["fidelity"],
        "evidence_refs": [f"{x['file']}#{x['test']}" for x in record["runner"]["tests"]],
        "owner_test_results": test_results,
    }


def run_compound(compound: dict, tested_sha: str, tested_tree: str) -> dict:
    """One declared integration subject; never equate distinct owner fixtures."""
    results = [execute_owner_test(spec) for spec in compound["tests"]]
    ok = all(item.get("ok") for item in results)
    required = ("J09", "J10", "J11", "J12")
    subject = {
        "work_subject": "kaicreator-mm/ai-development-standard#1020:T12:J09+J10+J11+J12",
        "candidate_sha": tested_sha, "candidate_tree": tested_tree,
        "required_jobs": list(required),
    }
    source_bindings = [{
        "job": job, "path": p,
        "actual_blob": git("rev-parse", f"HEAD:{p}"),
        "candidate_sha": tested_sha,
        "work_subject": subject["work_subject"],
        "evidence_kind": "CURRENT_SOURCE_READBACK_NOT_WORK_SUBJECT_OUTCOME",
    } for job, p in zip(required, compound["actual_source_refs"])]
    # Test that omission of any material category is rejected by the
    # completeness checker; no new owner transition policy is implemented.
    def complete(facts):
        return all(job in facts for job in required) and all(
            facts[job].get("actual_blob") and facts[job].get("work_subject") == subject["work_subject"]
            for job in required
        )
    fact_map = {row["job"]: row for row in source_bindings}
    omission_negatives = {
        job: not complete({k: v for k, v in fact_map.items() if k != job})
        for job in required
    }
    completeness = complete(fact_map) and all(omission_negatives.values())
    # Git blob equality and passing independent unit methods do NOT prove
    # that a single real work item underwent all four owner operations.
    # J09 future release is also lawfully absent at this stage.
    return {
        "id": compound["id"], "subject": subject,
        "tested_sha": tested_sha, "tested_tree": tested_tree,
        "owner_source_readbacks": source_bindings,
        "omission_negative_tests": omission_negatives,
        "source_completeness_checked": completeness,
        "owner_assertion_tests_pass": ok,
        "contract_coverage_oracle": "PASS" if ok and completeness else "FAIL",
        "result": "BLOCKED",
        "material_disposition": "MATERIAL_INTERSECTION_UNKNOWN",
        "unverified_reasons": [
            "independent owner unit methods do not share one runtime work-subject",
            "release J09 cannot receive future V01-R02 authority at T12 time",
        ],
        "resolution_owner": "T12 exact-subject integration adapter; release J09 to V01-R02",
        "release_gate": "NOT_RUN",
        "owner_test_results": results,
    }


def main() -> int:
    doc = load_registry()
    problems = validate_registry(doc) + validate_write_set()
    if problems:
        print(json.dumps({"V411_T12": "REGISTRY_OR_WRITESET_FAIL", "problems": problems}, indent=2))
        return 1

    tested_sha = git("rev-parse", "HEAD")
    tested_tree = git("rev-parse", "HEAD^{tree}")
    records = []
    for case_id in sorted(EXPECTED_IDS):
        for polarity in ("positive", "negative"):
            records.append(run_record(doc["scenarios"][case_id][polarity], tested_sha, tested_tree))

    compound = run_compound(doc["compound"], tested_sha, tested_tree)
    failures = [r for r in records if r["exit"] != 0]
    if compound["contract_coverage_oracle"] != "PASS":
        failures.append({"compound": compound})
    ledger = {
        "event": "V411_T12_RUNTIME_EVIDENCE_LEDGER",
        "pack_blob": doc["pack_blob"],
        "integration_base": INTEGRATION_BASE,
        "tested_sha": tested_sha,
        "tested_tree": tested_tree,
        "record_count": len(records),
        "records": records,
        "compound": compound,
        "downstream_release_truth": "NOT_RUN",
        "material_integration_state": "BLOCKED",
        "material_unverified_count": sum(
            r["proof_layers"]["P3_C"]["state"] == "BLOCKED" for r in records
        ) + int(compound["result"] == "BLOCKED"),
        "material_resolution_owner": "#1020 T12 same-work-subject integration; V01-R02 later release facts",
        "failure_count": len(failures),
    }
    print("V411_T12_EVIDENCE_LEDGER=" + json.dumps(ledger, sort_keys=True))
    if failures:
        print(json.dumps({"V411_T12": "FAIL", "failure_count": len(failures)}, indent=2))
        return 1
    print("V411_T12=OWNER_ASSERTIONS_PASS_INTEGRATED_PROOF_BLOCKED records=52 compound=BLOCKED downstream_release=NOT_RUN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
