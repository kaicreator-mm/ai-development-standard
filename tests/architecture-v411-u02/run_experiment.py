"""U02 experiment orchestrator (Issue #949) — runs cases E1..E8.

Each case runs in a fresh runtime directory containing a real local git
fact plane and a real persistent sink ledger. Actors are real subprocesses;
lost-ACK cases perform a real hard kill (TerminateProcess) inside the
commit-to-publication window. Counters are asserted directly against the
persistent sink ledger — not merely reported.

Usage:
    python run_experiment.py            # all cases
    python run_experiment.py --case E2  # single case

Runtime root: U02_RUNTIME_ROOT env var, else a fresh temp directory.
Evidence (evidence.json, per-case logs) is written under the runtime root.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from u02 import authority, events  # noqa: E402
from u02.authority import (  # noqa: E402
    ACCEPTED, BLOCKED_DENIED, BLOCKED_DUPLICATE_CLAIM, BLOCKED_NO_CLAIM,
    BLOCKED_NO_EFFECT_IDENTITY, BLOCKED_OUTCOME_UNKNOWN, BLOCKED_STALE_HEAD,
    BLOCKED_TENANT, BLOCKED_UNVERIFIED, COMMITTED_ALREADY,
    RECONCILED_COMMITTED, RECONCILED_NOT_COMMITTED,
)
from u02.plane import GitFactPlane, PlaneError  # noqa: E402
from u02.sink import LedgerSink  # noqa: E402

ENV = "tenant=research-u02-A"
TENANT = "research-u02-A"


class CaseFailure(AssertionError):
    pass


def rmtree_ro(path: Path) -> None:
    """rmtree that tolerates git's read-only object files on Windows."""
    def onexc(func, p, exc):
        import stat
        os.chmod(p, stat.S_IWRITE)
        func(p)
    shutil.rmtree(path, onexc=onexc)


def check(case: str, condition: bool, what: str) -> None:
    if not condition:
        raise CaseFailure(f"{case}: {what}")


def run_actor(runtime: Path, case: str, actor: str, phase: str, *,
              operator: str | None = None, dispatch: str | None = None,
              effect_id: str = "fx-u02-default", extra: list[str] | None = None,
              wait: bool = True, sleep_after: float = 0.0,
              sleep_before: float = 0.0) -> tuple[subprocess.Popen, dict | None, str]:
    """Launch one real actor process. Returns (proc, result_dict, raw_stdout)."""
    operator = operator or f"claude-code:{case.lower()}-{actor.lower()}"
    dispatch = dispatch or f"d-{case}-{actor.lower()}"
    cmd = [
        sys.executable, "-m", "u02.actor",
        "--runtime", str(runtime), "--case", case.lower(), "--actor", actor,
        "--operator-id", operator, "--session-ref", f"u02-{case}-{actor}-session",
        "--dispatch-id", dispatch, "--effect-id", effect_id,
        "--environment", ENV, "--authorized-environment", ENV, "--tenant", TENANT,
        "--phase", phase,
    ]
    if sleep_after:
        cmd += ["--sleep-after-commit", str(sleep_after)]
    if sleep_before:
        cmd += ["--sleep-before-commit", str(sleep_before)]
    if extra:
        cmd += extra
    env = dict(os.environ, PYTHONPATH=str(HERE))
    proc = subprocess.Popen(cmd, cwd=str(HERE), env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if not wait:
        return proc, None, ""
    out, err = proc.communicate(timeout=120)
    result = parse_result(out)
    return proc, result, out + ("\n[stderr]\n" + err if err.strip() else "")


def parse_result(stdout: str) -> dict | None:
    for line in stdout.splitlines():
        if line.startswith("RESULT "):
            return json.loads(line[len("RESULT "):])
    return None


def sink_for(runtime: Path, case: str) -> LedgerSink:
    return LedgerSink(runtime / "sink" / f"{case.lower()}:external-write.ledger.jsonl", tenant=TENANT)


def plane_for(runtime: Path) -> GitFactPlane:
    return GitFactPlane(runtime / "plane")


def publish(plane: GitFactPlane, case: str, payload: dict) -> str:
    return plane.append_event(f"{case.lower()}:external-write", payload)


def release_timeout(plane: GitFactPlane, runtime: Path, case: str, operator: str, dispatch: str) -> str:
    work = f"{case.lower()}:external-write"
    plane_obj = plane
    gen = sum(1 for e in plane_obj.read_events(work) if e["event"] == "DISPATCH_CLAIMED")
    return publish(plane, case, events.state_changed_event(
        operator_id=operator, dispatch_id=dispatch, head_sha=plane.head_sha(),
        state="TIMEOUT", reason="durable liveness timeout release after lost ACK",
        work_key=work, generation=gen, environment=ENV, liveness_expired=True,
    ))


def case_e1(runtime: Path) -> dict:
    """Positive baseline: A authorized, write commits, ACK/outcome published."""
    plane = plane_for(runtime)
    proc, claim, _ = run_actor(runtime, "E1", "A", "claim")
    check("E1", claim and claim["code"] == ACCEPTED, f"A claim accepted, got {claim}")
    proc, effect, _ = run_actor(runtime, "E1", "A", "effect")
    check("E1", effect and effect["code"] == "EFFECT_COMMITTED", f"A effect committed, got {effect}")
    check("E1", effect["sink"]["count"] == 1, f"sink count 1, got {effect['sink']['count']}")
    proc, resume, _ = run_actor(runtime, "E1", "B", "resume", extra=["--with-readback"])
    decision = resume["decision"]
    check("E1", decision["code"] == COMMITTED_ALREADY, f"B sees committed outcome, got {decision}")
    check("E1", decision["may_mutate"] is False, "B must not mutate")
    count = sink_for(runtime, "E1").readback()["count"]
    check("E1", count == 1, f"real observable effect counter stays 1, got {count}")
    return {"a_claim": claim, "a_effect": effect, "b_resume": resume, "final_count": count}


def case_e2(runtime: Path) -> dict:
    """Uncertain ACK: effect commits, outcome publication lost via hard kill."""
    plane = plane_for(runtime)
    _, claim, _ = run_actor(runtime, "E2", "A", "claim")
    check("E2", claim and claim["code"] == ACCEPTED, f"A claim accepted, got {claim}")
    head_before = plane.head_sha()

    proc, _, _ = run_actor(runtime, "E2", "A", "effect", wait=False, sleep_after=10.0)
    observed = None
    deadline = time.time() + 60
    while time.time() < deadline:
        rb = sink_for(runtime, "E2").readback()
        if rb["count"] == 1:
            observed = rb
            break
        time.sleep(0.2)
    check("E2", observed is not None, "orchestrator observed the real sink mutation before kill window")
    proc.kill()  # real hard process death inside the commit→publication window
    out, err = proc.communicate(timeout=30)
    killed_result = parse_result(out)
    check("E2", killed_result is None, "killed A produced no outcome publication")
    check("E2", proc.returncode != 0, f"hard kill observed (returncode={proc.returncode})")
    check("E2", plane.head_sha() == head_before, "plane has no effect outcome event after kill")

    # While A's durable claim is still active, B must not take over (§11).
    _, early, _ = run_actor(runtime, "E2", "B", "resume",
                            operator="claude-code:e2-b-successor", dispatch="d-e2-b",
                            extra=["--with-readback"])
    check("E2", early["decision"]["code"] == BLOCKED_DUPLICATE_CLAIM,
          f"active claim blocks takeover, got {early['decision']}")
    check("E2", sink_for(runtime, "E2").readback()["count"] == 1, "no repeat while claim active")

    # Durable TIMEOUT release of A's claim, then B reconciles via real readback.
    release_timeout(plane, runtime, "E2", "claude-code:e2-a", "d-E2-a")
    _, resume, _ = run_actor(runtime, "E2", "B", "resume",
                             operator="claude-code:e2-b-successor", dispatch="d-e2-b",
                             extra=["--with-readback"])
    decision = resume["decision"]
    check("E2", decision["code"] == RECONCILED_COMMITTED, f"B reconciles via real readback, got {decision}")
    check("E2", decision["may_mutate"] is False, "B must not re-issue the mutation")
    final = sink_for(runtime, "E2").readback()["count"]
    check("E2", final == 1, f"real observable effect counter remains 1, got {final}")
    return {"a_claim": claim, "killed_returncode": proc.returncode,
            "b_early_block": early, "b_resume_after_release": resume,
            "sink_observed_at_kill": observed, "final_count": final}


def case_e3(runtime: Path) -> dict:
    """Uncertain, NOT committed: timeout alone is UNKNOWN; only grounded
    reconciliation licenses a legal attempt."""
    plane = plane_for(runtime)
    _, claim, _ = run_actor(runtime, "E3", "A", "claim")
    check("E3", claim and claim["code"] == ACCEPTED, f"A claim accepted, got {claim}")

    proc, _, _ = run_actor(runtime, "E3", "A", "effect", wait=False,
                           sleep_before=10.0, sleep_after=10.0)
    time.sleep(1.5)
    proc.kill()
    proc.communicate(timeout=30)
    rb = sink_for(runtime, "E3").readback()
    check("E3", rb["count"] == 0, f"no external commit landed (killed pre-mutation), got {rb['count']}")

    # While A's durable claim is active, B is a duplicate, not a reconciler.
    _, early, _ = run_actor(runtime, "E3", "B", "resume",
                            operator="claude-code:e3-b-blind", dispatch="d-e3-b")
    check("E3", early["decision"]["code"] == BLOCKED_DUPLICATE_CLAIM,
          f"active claim blocks B before release, got {early['decision']}")

    # Durable release. B deciding from timeout/lineage alone: UNKNOWN, no attempt.
    release_timeout(plane, runtime, "E3", "claude-code:e3-a", "d-E3-a")
    _, blind, _ = run_actor(runtime, "E3", "B", "resume",
                            operator="claude-code:e3-b-blind", dispatch="d-e3-b")
    check("E3", blind["decision"]["code"] == BLOCKED_OUTCOME_UNKNOWN,
          f"timeout alone is UNKNOWN, got {blind['decision']}")
    check("E3", sink_for(runtime, "E3").readback()["count"] == 0, "blind B issued no mutation")
    _, grounded, _ = run_actor(runtime, "E3", "B", "resume",
                               operator="claude-code:e3-b-grounded", dispatch="d-e3-b-grounded",
                               extra=["--with-readback", "--attempt"])
    check("E3", grounded["decision"]["code"] == RECONCILED_NOT_COMMITTED,
          f"grounded reconciliation, got {grounded['decision']}")
    check("E3", grounded.get("admission", {}).get("code") == ACCEPTED, f"fresh claim admitted, got {grounded}")
    check("E3", grounded.get("sink", {}).get("count") == 1, f"exactly one mutation total, got {grounded.get('sink')}")
    final = sink_for(runtime, "E3").readback()["count"]
    check("E3", final == 1, f"real observable effect counter is exactly 1, got {final}")
    return {"a_claim": claim, "blind_b": blind, "grounded_b": grounded, "final_count": final}


def case_e4(runtime: Path) -> dict:
    """Concurrent successor recovery: at most one compatible accepted claim."""
    plane = plane_for(runtime)
    _, claim, _ = run_actor(runtime, "E4", "A", "claim")
    check("E4", claim and claim["code"] == ACCEPTED, f"A claim accepted, got {claim}")
    proc, _, _ = run_actor(runtime, "E4", "A", "effect", wait=False,
                           sleep_before=10.0, sleep_after=10.0)
    time.sleep(1.5)
    proc.kill()
    proc.communicate(timeout=30)
    release_timeout(plane, runtime, "E4", "claude-code:e4-a", "d-E4-a")

    b_head = plane.head_sha()
    pb, _, _ = run_actor(runtime, "E4", "B", "claim", wait=False,
                         operator="claude-code:e4-b", dispatch="d-e4-b",
                         effect_id="fx-e4", extra=["--with-readback", "--expected-sha", b_head])
    pc, _, _ = run_actor(runtime, "E4", "C", "claim", wait=False,
                         operator="claude-code:e4-c", dispatch="d-e4-c",
                         effect_id="fx-e4", extra=["--with-readback", "--expected-sha", b_head])
    out_b, err_b = pb.communicate(timeout=120)
    out_c, err_c = pc.communicate(timeout=120)
    raw_b, raw_c = out_b + "\n[stderr]\n" + err_b, out_c + "\n[stderr]\n" + err_c
    res_b, res_c = parse_result(out_b), parse_result(out_c)
    accepted = [r for r in (res_b, res_c) if r["code"] == ACCEPTED]
    rejected = [r for r in (res_b, res_c) if r["code"] in (BLOCKED_DUPLICATE_CLAIM, BLOCKED_STALE_HEAD)]
    check("E4", len(accepted) == 1 and len(rejected) == 1,
          f"exactly one accepted claim and one serialized rejection, got B={res_b} C={res_c}")
    winner = "B" if res_b["code"] == ACCEPTED else "C"
    _, effect, _ = run_actor(runtime, "E4", winner, "effect", effect_id="fx-e4",
                             operator=f"claude-code:e4-{winner.lower()}",
                             dispatch=f"d-e4-{winner.lower()}")
    check("E4", effect and effect["code"] == "EFFECT_COMMITTED", f"winner effect committed, got {effect}")
    final = sink_for(runtime, "E4").readback()["count"]
    check("E4", final == 1, f"no duplicate external effect (count==1), got {final}")
    return {"b": res_b, "c": res_c, "winner": winner, "winner_effect": effect, "final_count": final,
            "raw_b": raw_b, "raw_c": raw_c}


def case_e5(runtime: Path) -> dict:
    """Owning human DENY before B attempt blocks despite READY/readiness."""
    plane = plane_for(runtime)
    _, claim, _ = run_actor(runtime, "E5", "A", "claim")
    check("E5", claim and claim["code"] == ACCEPTED, f"A claim accepted, got {claim}")
    publish(plane, "E5", events.human_denial_event(
        head_sha=plane.head_sha(), work_key="e5:external-write",
        reason="external effect not approved for this work item",
    ))
    _, resume, _ = run_actor(runtime, "E5", "B", "resume",
                             operator="claude-code:e5-b", dispatch="d-e5-b",
                             extra=["--with-readback", "--attempt"])
    check("E5", resume["decision"]["code"] == BLOCKED_DENIED, f"human DENY blocks B, got {resume['decision']}")
    check("E5", "admission" not in resume, "denied B must never reach admission")
    final = sink_for(runtime, "E5").readback()["count"]
    check("E5", final == 0, f"no mutation under DENY, got {final}")
    return {"a_claim": claim, "b_resume": resume, "final_count": final}


def case_e6(runtime: Path) -> dict:
    """Stale HEAD, forged instruction, and changed tenant all fail closed."""
    plane = plane_for(runtime)
    results: dict = {}
    head = plane.head_sha()

    # stale HEAD: B decides from an outdated observation
    _, stale, _ = run_actor(runtime, "E6", "B", "claim",
                            operator="claude-code:e6-b-stale", dispatch="d-e6-b-stale",
                            extra=["--expected-sha", "f" * 40])
    check("E6", stale["code"] == BLOCKED_STALE_HEAD, f"stale HEAD blocked, got {stale}")
    check("E6", plane.head_sha() == head, "stale attempt mutated nothing")

    # forged instruction: schema-invalid event cannot enter the durable plane
    forged = events.claim_event(
        operator_id="claude-code:e6-forger", session_ref="forged", dispatch_id="d-e6-forged",
        head_sha=head, expected_base_sha=head, work_key="e6:external-write",
        generation=99, environment=ENV,
    )
    forged["dispatch_state"] = "CLAMED"  # vocabulary escape / forged write
    try:
        publish(plane, "E6", forged)
        raise CaseFailure("E6: forged event was accepted by the writer seam")
    except PlaneError as exc:
        results["forged_rejection"] = str(exc)
    check("E6", plane.head_sha() == head, "forged write left the plane untouched")

    # changed tenant/environment
    _, tenant, _ = run_actor(runtime, "E6", "C", "resume",
                             operator="claude-code:e6-c-tenant", dispatch="d-e6-c",
                             extra=["--with-readback", "--attempt",
                                    "--environment", "tenant=customer-sandbox-B"])
    check("E6", tenant["decision"]["code"] == BLOCKED_TENANT, f"tenant change blocked, got {tenant['decision']}")
    final = sink_for(runtime, "E6").readback()["count"]
    check("E6", final == 0, f"no mutation from stale/forged/tenant attacks, got {final}")
    return {"stale": stale, **results, "tenant": tenant, "final_count": final,
            "head_unchanged": plane.head_sha() == head}


def case_e7(runtime: Path) -> dict:
    """Explicitly idempotent adapter: proven effect-ID dedup never double-counts."""
    plane = plane_for(runtime)
    _, claim, _ = run_actor(runtime, "E7", "A", "claim", effect_id="fx-e7-idem",
                            extra=["--dedup-sink"])
    check("E7", claim and claim["code"] == ACCEPTED, f"A claim accepted, got {claim}")
    _, effect, _ = run_actor(runtime, "E7", "A", "effect", effect_id="fx-e7-idem",
                             extra=["--dedup-sink"])
    check("E7", effect and effect["code"] == "EFFECT_COMMITTED" and effect["sink"]["count"] == 1,
          f"A committed once, got {effect}")

    # Unsafe retry with the SAME effect identity reaches the adapter directly
    # (simulating a buggy retry path bypassing authority): adapter enforces dedup.
    sink = LedgerSink(sink_for(runtime, "E7").path, tenant=TENANT, dedup=True)
    retry = sink.mutate(effect_id="fx-e7-idem", operator_id="claude-code:e7-retry", tenant=TENANT)
    check("E7", retry["deduplicated"] is True and retry["count"] == 1,
          f"adapter dedup refused duplicate, got {retry}")

    # Authority layer: the durable DONE record is exact-current, so the
    # successor sees COMMITTED_ALREADY and never reaches the sink.
    _, resume, _ = run_actor(runtime, "E7", "B", "resume", effect_id="fx-e7-idem",
                             extra=["--with-readback", "--dedup-sink"])
    check("E7", resume["decision"]["code"] == COMMITTED_ALREADY,
          f"B sees durable committed record, got {resume['decision']}")
    final = sink_for(runtime, "E7").readback()["count"]
    check("E7", final == 1, f"safe retry never increments real count, got {final}")
    return {"a_effect": effect, "adapter_retry": retry, "b_resume": resume, "final_count": final}


def case_e8(runtime: Path) -> dict:
    """Broken writer / missing effect identity: fail closed, no false proof."""
    plane = plane_for(runtime)
    _, claim, _ = run_actor(runtime, "E8", "A", "claim")
    check("E8", claim and claim["code"] == ACCEPTED, f"A claim accepted, got {claim}")

    # broken writer: destroy the durable plane, then a successor resumes
    rmtree_ro(runtime / "plane" / ".git")
    _, broken, _ = run_actor(runtime, "E8", "B", "resume",
                             operator="claude-code:e8-b", dispatch="d-e8-b",
                             extra=["--with-readback", "--attempt"])
    check("E8", broken["code"] == BLOCKED_UNVERIFIED, f"broken plane fails closed, got {broken}")
    check("E8", "admission" not in broken, "broken plane must not reach admission")
    check("E8", not sink_for(runtime, "E8").path.exists()
          or sink_for(runtime, "E8").readback()["count"] == 0, "no mutation on broken writer")

    # missing effect identity: adapter refuses before any write
    runtime2 = runtime.parent / f"{runtime.name}-identity"
    if runtime2.exists():
        rmtree_ro(runtime2)
    plane2 = plane_for(runtime2)
    _, claim2, _ = run_actor(runtime2, "E8", "A", "claim")
    check("E8", claim2 and claim2["code"] == ACCEPTED, f"fresh claim accepted, got {claim2}")
    _, no_id, _ = run_actor(runtime2, "E8", "A", "effect", effect_id="")
    check("E8", no_id["code"] == BLOCKED_NO_EFFECT_IDENTITY, f"missing identity refused, got {no_id}")
    ledger2 = sink_for(runtime2, "E8").path
    check("E8", (not ledger2.exists()) or sink_for(runtime2, "E8").readback()["count"] == 0,
          "missing identity produced no mutation")
    return {"broken_writer": broken, "missing_identity": no_id, "plane2_head": plane2.head_sha()}


CASES = {"E1": case_e1, "E2": case_e2, "E3": case_e3, "E4": case_e4,
         "E5": case_e5, "E6": case_e6, "E7": case_e7, "E8": case_e8}


def collect_case_evidence(runtime: Path, case: str) -> dict:
    plane = GitFactPlane(runtime / "plane") if (runtime / "plane" / ".git").is_dir() else None
    work = f"{case.lower()}:external-write"
    ev: dict = {"case": case}
    if plane is not None:
        ev["plane_head"] = plane.head_sha()
        ev["plane_tree"] = plane.tree_sha()
        ev["event_log_digest"] = plane.event_log_digest(work)
        ev["git_log"] = subprocess.run(
            ["git", "-C", str(runtime / "plane"), "log", "--oneline", "--no-decorate"],
            capture_output=True, text=True).stdout.strip().splitlines()
        ev["events"] = plane.read_events(work)
    sink_path = sink_for(runtime, case).path
    if sink_path.exists():
        ev["sink"] = LedgerSink(sink_path, tenant=TENANT).readback()
    else:
        ev["sink"] = {"count": 0, "effect_ids": [], "entries": []}
    return ev


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=list(CASES), default=None)
    parser.add_argument("--runtime-root", default=os.environ.get("U02_RUNTIME_ROOT"))
    args = parser.parse_args()

    root = Path(args.runtime_root) if args.runtime_root else Path(tempfile.mkdtemp(prefix="u02-runtime-"))
    root.mkdir(parents=True, exist_ok=True)
    print(f"runtime root: {root}")

    selected = [args.case] if args.case else list(CASES)
    report: dict = {"runtime_root": str(root), "platform": sys.platform,
                    "python": sys.version, "cases": {}}
    failed: list[str] = []
    for case in selected:
        runtime = root / case.lower()
        if runtime.exists():
            rmtree_ro(runtime)
        runtime.mkdir(parents=True)
        print(f"== {case} ==")
        try:
            outcome = CASES[case](runtime)
            evidence = collect_case_evidence(runtime, case)
            report["cases"][case] = {"status": "PASS", "outcome": outcome, "evidence": evidence}
            print(f"{case}: PASS (final effect count={evidence['sink']['count']}, "
                  f"plane head={evidence.get('plane_head', 'n/a')[:12]})")
        except (CaseFailure, AssertionError) as exc:
            report["cases"][case] = {"status": "FAIL", "error": str(exc)}
            failed.append(case)
            print(f"{case}: FAIL — {exc}")
        except Exception as exc:  # unexpected harness/actor failure
            report["cases"][case] = {"status": "FAIL", "error": f"unexpected: {exc!r}"}
            failed.append(case)
            print(f"{case}: FAIL (unexpected) — {exc!r}")

    terminal = "PASS" if not failed and len(report["cases"]) == len(CASES) else "FAIL"
    report["terminal"] = terminal
    (root / "evidence.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(f"evidence: {root / 'evidence.json'}")
    print(f"TERMINAL: {terminal}")
    return 0 if terminal == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
