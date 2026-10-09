"""Actor process entry point for the U02 experiment.

Each invocation is one real OS process acting as one identified operator
(session_ref distinguishes transport). The orchestrator launches actors as
subprocesses; the lost-ACK cases hard-kill an actor inside the
--sleep-after-commit window (real process death between the sink commit and
the durable outcome publication).

Protocol: the actor prints exactly one ``RESULT <json>`` line on stdout and
exits 0 when it completed its role (including correct fail-closed blocks).
Exit 3 signals an unexpected actor error. A hard kill is observed by the
orchestrator as a negative return code — no RESULT line is produced.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

from . import authority, events
from .authority import ACCEPTED, Decision
from .plane import GitFactPlane, PlaneError
from .sink import LedgerSink, SinkRefused


def _emit(payload: dict) -> None:
    print("RESULT " + json.dumps(payload, sort_keys=True), flush=True)


def _paths(args) -> tuple[GitFactPlane, LedgerSink]:
    # Actors never (re)create the durable plane: a missing or destroyed fact
    # plane fails closed instead of silently re-seeding authority state.
    plane = GitFactPlane(Path(args.runtime) / "plane", create=False)
    sink = LedgerSink(
        Path(args.runtime) / "sink" / f"{args.work_key}.ledger.jsonl",
        tenant=args.tenant,
        dedup=args.dedup_sink,
    )
    return plane, sink


def _prior_claim_count(plane: GitFactPlane, work_key: str) -> int:
    return sum(1 for e in plane.read_events(work_key) if e["event"] == "DISPATCH_CLAIMED")


def admit_fresh_claim(plane: GitFactPlane, args, work_key: str,
                      readback: dict | None) -> Decision:
    """Serialized compare-and-set admission over durable git facts (SINGLE_WRITER_ADMISSION)."""
    with plane.admission_lock():
        current_head = plane.head_sha()
        if args.expected_sha and args.expected_sha != current_head:
            # Decision computed from a stale observed HEAD is rejected even
            # though the admission itself could have succeeded (E6).
            return Decision(
                authority.BLOCKED_STALE_HEAD, False,
                f"stale observed HEAD {args.expected_sha[:12]} != current {current_head[:12]}",
                authority.Facts(head_sha=current_head),
            )
        facts = authority.derive_facts(plane, work_key)
        decision = authority.successor_decision(
            facts=facts,
            candidate_operator=args.operator_id,
            candidate_dispatch=args.dispatch_id,
            expected_head_sha=current_head,
            environment=args.environment,
            authorized_environment=args.authorized_environment,
            effect_id=args.effect_id,
            sink_readback=readback,
            dedup_proven=args.dedup_sink,
        )
        if decision.code == authority.BLOCKED_OUTCOME_UNKNOWN and facts.claim is None:
            # No prior attempt exists at all: nothing is uncertain.
            decision = Decision(ACCEPTED, True, "first claim for work identity", facts)
        if not decision.may_mutate:
            return decision
        generation = _prior_claim_count(plane, work_key) + 1
        payload = events.claim_event(
            operator_id=args.operator_id,
            session_ref=args.session_ref,
            dispatch_id=args.dispatch_id,
            head_sha=current_head,
            expected_base_sha=current_head,
            work_key=work_key,
            generation=generation,
            environment=args.environment,
        )
        new_head = plane.append_event(work_key, payload, acquire_lock=False)
        return Decision(ACCEPTED, True,
                        f"claim admitted at generation {generation}", authority.Facts(head_sha=new_head))


def _commit_effect(plane: GitFactPlane, args, work_key: str, reason: str) -> dict:
    sink = LedgerSink(
        Path(args.runtime) / "sink" / f"{args.work_key}.ledger.jsonl",
        tenant=args.tenant,
        dedup=args.dedup_sink,
    )
    result = {"pre_commit_wait_s": args.sleep_before_commit}
    if args.sleep_before_commit > 0:
        # Deterministic crash window before the mutation (E3: no external
        # commit ever lands when the actor is killed here).
        time.sleep(args.sleep_before_commit)
    result.update(sink.mutate(effect_id=args.effect_id, operator_id=args.operator_id, tenant=args.tenant))
    if args.sleep_after_commit > 0:
        # Lost-ACK injection window: the sink commit is durable, the outcome
        # publication below has not happened yet. The orchestrator may
        # hard-kill this process inside this window.
        time.sleep(args.sleep_after_commit)
    generation = _prior_claim_count(plane, work_key)
    payload = events.state_changed_event(
        operator_id=args.operator_id,
        dispatch_id=args.dispatch_id,
        head_sha=plane.head_sha(),
        state="DONE",
        reason=reason,
        work_key=work_key,
        generation=generation,
        environment=args.environment,
        effect_id=args.effect_id,
    )
    new_head = plane.append_event(work_key, payload)
    return {"sink": result, "head_sha": new_head}


def phase_claim(args, work_key: str) -> dict:
    plane, sink = _paths(args)
    readback = sink.readback() if args.with_readback else None
    decision = admit_fresh_claim(plane, args, work_key, readback=readback)
    return {"phase": "claim", **decision.to_dict()}


def phase_effect(args, work_key: str) -> dict:
    plane, sink = _paths(args)
    facts = authority.derive_facts(plane, work_key)
    claim = facts.claim
    mine = (
        claim is not None
        and facts.claim_terminal is None
        and claim.get("dispatch_state") in authority.ACTIVE_STATES
        and claim.get("operator_id") == args.operator_id
        and claim.get("dispatch_id") == args.dispatch_id
    )
    if not mine:
        return {"phase": "effect", "code": authority.BLOCKED_NO_CLAIM, "may_mutate": False,
                "reason": "NO_CLAIM_NO_EXECUTION: no active accepted claim held by this operator"}
    try:
        outcome = _commit_effect(plane, args, work_key, "external effect committed")
    except SinkRefused as exc:
        code = (authority.BLOCKED_NO_EFFECT_IDENTITY
                if "effect identity" in str(exc) else authority.BLOCKED_TENANT)
        return {"phase": "effect", "code": code, "may_mutate": False, "reason": str(exc)}
    return {"phase": "effect", "code": "EFFECT_COMMITTED", "may_mutate": True, **outcome}


def phase_resume(args, work_key: str) -> dict:
    plane, sink = _paths(args)
    facts = authority.derive_facts(plane, work_key)
    readback = sink.readback() if args.with_readback else None
    decision = authority.successor_decision(
        facts=facts,
        candidate_operator=args.operator_id,
        candidate_dispatch=args.dispatch_id,
        expected_head_sha=args.expected_sha or facts.head_sha,
        environment=args.environment,
        authorized_environment=args.authorized_environment,
        effect_id=args.effect_id,
        sink_readback=readback,
        dedup_proven=args.dedup_sink,
    )
    if not (decision.may_mutate and args.attempt):
        return {"phase": "resume", "decision": decision.to_dict()}
    admitted = admit_fresh_claim(plane, args, work_key, readback=readback)
    if admitted.code != ACCEPTED:
        return {"phase": "resume", "decision": decision.to_dict(), "admission": admitted.to_dict()}
    try:
        outcome = _commit_effect(plane, args, work_key, "external effect committed by successor")
    except SinkRefused as exc:
        return {"phase": "resume", "decision": decision.to_dict(), "admission": admitted.to_dict(),
                "code": "SINK_REFUSED", "may_mutate": False, "reason": str(exc)}
    return {"phase": "resume", "decision": decision.to_dict(), "admission": admitted.to_dict(),
            **outcome}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="U02 experiment actor process")
    parser.add_argument("--runtime", required=True)
    parser.add_argument("--case", required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--operator-id", required=True)
    parser.add_argument("--session-ref", required=True)
    parser.add_argument("--dispatch-id", required=True)
    parser.add_argument("--work-key", default=None)
    parser.add_argument("--environment", default="tenant=research-u02-A")
    parser.add_argument("--authorized-environment", default="tenant=research-u02-A")
    parser.add_argument("--tenant", default="research-u02-A")
    parser.add_argument("--effect-id", default="")
    parser.add_argument("--expected-sha", default=None)
    parser.add_argument("--dedup-sink", action="store_true")
    parser.add_argument("--sleep-after-commit", type=float, default=0.0)
    parser.add_argument("--sleep-before-commit", type=float, default=0.0)
    parser.add_argument("--with-readback", action="store_true")
    parser.add_argument("--attempt", action="store_true")
    parser.add_argument("--phase", required=True, choices=["claim", "effect", "resume"])
    args = parser.parse_args(argv)
    args.work_key = args.work_key or f"{args.case}:external-write"

    try:
        if args.phase == "claim":
            result = phase_claim(args, args.work_key)
        elif args.phase == "effect":
            result = phase_effect(args, args.work_key)
        else:
            result = phase_resume(args, args.work_key)
    except PlaneError as exc:
        # Fail closed at the real writer seam: broken plane never authorizes.
        _emit({"phase": args.phase, "code": "BLOCKED_UNVERIFIED", "may_mutate": False,
               "reason": f"fail closed: {exc}"})
        return 0
    _emit(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
