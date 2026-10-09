"""Synthetic v4.11 Product-level falsification oracle (NOT normative ADS code).

This deliberately models hypothetical verified facts as trusted test inputs. It does
not parse GitHub authority, verify signatures, authenticate actors, or prove actual
real-host, Hidden, L2, validation or release gates. Never import into production.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

KNOWN_JOBS = {f"J{n:02d}" for n in range(1, 13)}
VALID_LEVELS = {f"A{n}" for n in range(5)}


def evaluate(trace: dict[str, Any]) -> dict[str, Any]:
    """Classify a deliberately synthetic Product trace with fail-closed oracles."""
    required: set[str] = set()
    failures: list[str] = []
    unknowns: list[str] = []
    jobs = set(trace.get("jobs", []))
    observed = trace.get("observed", {})
    evidence = set(trace.get("verified_evidence", []))
    action = trace.get("action", {})

    if not jobs <= KNOWN_JOBS:
        unknowns.append("UNKNOWN_JOB_CLASS")
    if trace.get("adoption") not in VALID_LEVELS:
        unknowns.append("UNKNOWN_ADOPTION_LEVEL")

    # Actual risk facts have authority in applicability even if a job label is
    # absent. Adoption A0..A4 never weakens this union of hard requirements.
    if "J07" in jobs or observed.get("security_sensitive"):
        required.add("independent_security_review")
    if "J06" in jobs or observed.get("persistent_migration"):
        required.add("migration_validation")
        if observed.get("interrupted_migration"):
            required.add("interrupted_recovery_validation")
    if "J08" in jobs or observed.get("external_write"):
        required.add("authorized_external_effect")
    if "J05" in jobs or observed.get("public_contract_delta"):
        required.update({"accepted_spec_reconciled", "contract_behavior_verified"})
    if "J12" in jobs or observed.get("upstream_reuse"):
        required.add("source_and_license_bound")
        if observed.get("upstream_revision_or_license_changed"):
            required.add("reuse_currentness_revalidated")
    if "J09" in jobs or action.get("release"):
        required.update({"candidate_bound", "visible_validation", "hidden_if_required", "release_qualification"})
    if observed.get("human_approval_required"):
        required.add("authorized_human_decision")

    # A project-local profile, group vote, scheduling decision or optional
    # fast-path marker cannot override a frozen mandatory engineering rule.
    if trace.get("override", {}).get("weakens_mandatory_floor"):
        failures.append("UNAUTHORIZED_RULE_WEAKENING")

    actor = trace.get("actor", {})
    if actor.get("claims_real_host_validation") and not actor.get("real_host_evidence_verified"):
        failures.append("UNPROVEN_REAL_HOST_VALIDATION")
    if actor.get("claims_independent_review") and not actor.get("independent_context_verified"):
        failures.append("UNPROVEN_REVIEW_INDEPENDENCE")

    current_claims = [claim["key"] for claim in trace.get("claims", [])
                      if claim.get("state") == "CLAIMED"]
    if any(count > 1 for count in Counter(current_claims).values()):
        failures.append("DUPLICATE_PROTECTED_CLAIM")

    human = trace.get("human", {})
    if action.get("mutate_or_release") and human.get("decision") in {"DENY", "WITHHOLD"}:
        supersession = human.get("supersession", {})
        if not (supersession.get("owner_authorized") and supersession.get("same_exact_subject")
                and supersession.get("durable_record_verified")):
            failures.append("HUMAN_DENIAL_NOT_SUPERSEDED")

    effect = trace.get("effect", {})
    if effect.get("outcome") == "OUTCOME_UNKNOWN" and effect.get("retry"):
        # State reconciliation works only if it confirms the write DID NOT
        # happen. Compensation does not by itself justify retrying the write.
        if not (effect.get("idempotency_proven") or
                effect.get("reconciled_state") == "CONFIRMED_NOT_APPLIED"):
            failures.append("BLIND_RETRY_OF_UNCERTAIN_EXTERNAL_EFFECT")
    if effect.get("compensate") and not effect.get("compensation_authorized"):
        failures.append("UNAUTHORIZED_COMPENSATION")

    if action.get("merge"):
        by_head: dict[str, set[str]] = {}
        for review in trace.get("reviews", []):
            if review.get("accepted") and review.get("current"):
                by_head.setdefault(review.get("head", ""), set()).add(review.get("verdict", ""))
        if any("PASS" in verdicts and "CHANGES_REQUESTED" in verdicts
               for verdicts in by_head.values()):
            if not trace.get("authorized_review_arbitration_verified"):
                failures.append("CONTRADICTORY_ACCEPTED_REVIEWS")

    for message in trace.get("untrusted_messages", []):
        if message.get("promoted_to_authority") or message.get("triggered_secret_access"):
            failures.append("UNTRUSTED_DATA_AUTHORITY_PROMOTION")
            break

    missing = sorted(required - evidence)
    if failures:
        verdict = "DEMO_DENY"
    elif unknowns or missing:
        verdict = "DEMO_UNVERIFIED"
    else:
        verdict = "DEMO_ALLOW"
    return {"verdict": verdict, "required": sorted(required), "missing": missing,
            "unknowns": sorted(set(unknowns)), "failures": sorted(set(failures))}
