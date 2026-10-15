"""V411-T07 focused regression: Merge Controller last-admission exact-state
sweep and guarded merge readiness.

R1 repair (#1014@6118919006 CHANGES_REQUIRED at reviewed HEAD
91a4e83645abdb2a4304e18ea404456b89dbc408, handoff #1014@6118983678): this
successor closes the six findings against the same two owner paths —
P1-01 required-prerequisite absence/failed Validation/missing Review
binding now fail closed; P1-02 the merge guard validates the recorded
sweep inventory itself (partial/duplicated/not-complete/contradicted
records are rejected even under a green verdict flag); P1-03 the merge
mutation is a compare-and-swap on the exact expected HEAD/base-target at
the mutation boundary (observable post-final-read drift aborts with zero
mutation; the uncloseable residual window is acknowledged to remain only
for the other surfaces); P1-04 the post-merge compensating audit is a
real injected integration-identity-bound read sequence over all required
surfaces where incomplete/UNKNOWN leaves the integration unratified with
no retroactive PASS; P2-01 platform generation is modeled distinctly from
the local read sequence (generation-only change over unchanged facts
still invalidates; UNKNOWN generation fails closed); P2-02 relevant merge
permissions currentness joins the required surface inventory, consumed
read-only from the existing authority contract. Each repaired
false-admission is encoded red-before/green-after (R1P1*/R1P2* cases).

Encodes the V411-T07 precompiled L3 (issue comment #1014@6117238049, pack
blob 4604bb8dc1a2bb3ff682e6a3ddc9577fd823120c, controller admission
#1014@6118129585, exact base version/v4.11.0@b501b0825ec79ce6d1742ceabca0bc
dc5dc0a72a) §3 oracles P01-P04 / N01-N12 for the merge-admission owner
concern as:

1. section-scoped textual contract checks binding the decision model to the
   owner-local normative clauses this task appends to
   `standards/EXECUTION_ARCHITECTURE_STANDARD.md` — the FOUR new subordinate
   merge-admission subsections of §14 Merge Controller (`### 14.1
   Last-admission exact-state sweep`, `### 14.2 Merge-boundary guard and
   guarded merge`, `### 14.3 Residual non-atomic window`, `### 14.4 Sweep
   failure routing`), plus byte-span guards that the pre-existing §14
   content, the §12 drift section, the §15 span and the document's
   top-level heading sequence stay byte-unchanged, and read-only blob
   guards for the Interaction Protocol, the shared Execution Architecture
   test, schemas, manifest and verifiers; and
2. a fixture-driven MERGE_ADMISSION decision model over a deterministic
   injected read-boundary adapter (sequential surface reads with explicit
   completeness/watermark facts; no live GitHub call) that binds each
   admission decision to exact subjects, recorded sweep identity and the
   merge-boundary guard outcome.

Purely offline: standard library + local git reads only, no network, no
shared verifier.

No fictitious atomic snapshot: the model never pretends GitHub offers one
multi-surface atomic read. A sweep is a bounded, identity-recorded read
sequence; readiness always comes from a recorded sweep plus a fresh bounded
final admission readback at the merge boundary, and the residual
final-read-to-merge window is explicitly modeled as unclosable (observed
breach fail-closes; a breach in the true gap surfaces only through the
post-merge compensating admission re-readback, which marks the integration
unratified pending re-sweep and never ratifies retroactively).

Known expected RED outside this file (disclosed, neither hidden nor
duplicated, preflighted by #1014@6117230348): any byte change to
EXECUTION_ARCHITECTURE_STANDARD.md necessarily creates a new exact owner
blob outside the admitted v4.11 chain (5588d219… → 04869086…), so the
shared test_v49_gate_currentness.py, test_v49_execution_contract_refs.py
and test_v49_role_execution_profile.py exact-pin subtests and the mechanical
test_v49_conformance_suite.py gate-kernel blob rebind are expected RED at
this PR HEAD. Those shared suites are read-only for this Builder; the
prechecked distinct support closure owns exactly that admission after
source qualification (SHARED_PROJECTION=T11_ONLY).

Known deferrals (honest, never reported as covered): the central machine
projection of LAST_ADMISSION_SWEEP facts (schema/manifest/verifier) and any
common-suite proposal for `scripts/test_execution_architecture.py` route to
the designated wiring task unwritten (DEFERRED_TO_T11) — the model routes,
never writes; the real-tree half asserts no shadow projection exists.
Integrated compound conformance (Product #3 negatives at scale) stays
DEFERRED_TO_T12.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
EA = "standards/EXECUTION_ARCHITECTURE_STANDARD.md"
EA_PATH = ROOT / EA
MANIFEST = ROOT / "standard-manifest.json"

# Exact base of this task (controller admission #1014@6118129585).
BASE_SHA = "b501b0825ec79ce6d1742ceabca0bcdc5dc0a72a"
# Immutable source-reviewed *owner-lane* HEAD: scope changes are attributed
# to this source commit, not to all lawful version descendants of BASE_SHA.
# The new composed HEAD still has to descend from this exact owner commit.
OWNER_QUALIFIED_HEAD = "b144e4cedbc03c87070ea13a608eff67e0717eab"

# ---------------------------------------------------------------------------
# section identity (headings are the section identity; tests slice by them)
# ---------------------------------------------------------------------------

SECTION_14 = "## 14. Merge Controller"
SECTION_15 = "## 15. Candidate Freeze Controller"
S141 = "### 14.1 Last-admission exact-state sweep"
S142 = "### 14.2 Merge-boundary guard and guarded merge"
S143 = "### 14.3 Residual non-atomic window"
S144 = "### 14.4 Sweep failure routing"
NEW_SUBSECTIONS = (S141, S142, S143, S144)

READ_ONLY_PATHS = (
    "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
    "scripts/test_execution_architecture.py",
    "standard-manifest.json",
    "scripts/verify_standard.py",
    "scripts/verify_project_standard.py",
)

# I1122 re-bind (issue #1122; direct user process authorization 2026-10-15,
# #1021@6191737577): the self-declared-executor policy lane lawfully mutates
# the interaction protocol (§5/§7/§8.1.1/§9.4) inside its approved owner
# concern, so its stale "unmutated since BASE_SHA" pin is re-bound to an
# exact integrated-blob identity pin — pin constants only, any further
# mutation of the surface still fails, zero other assertion change. The
# historical base blob stays re-derivable from BASE_SHA (tamper anchor).
PROTOCOL_PATH = "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md"
PROTOCOL_BASE_BLOB = "8c8fc74bd6deaf6987f6cf6d4e8e8e84c2692b75"
PROTOCOL_I1122_BLOB = "b3f1191b2ee0c469e9b425d2336d4adbc47d6ede"

# Owner clauses this task adds (exact normative sentences/bullets).
S141_CLAUSES = (
    "bounded `LAST_ADMISSION_SWEEP`",
    "current PR/source head and base/target",
    "accepted native Review decisions",
    "native blocked_by dependencies",
    "required check state",
    "authoritative Task/Review/Validation links",
    "unresolved release-significant findings",
    "relevant merge permissions currentness (consumed read-only from the existing authority contract through an exact authoritative reference)",
    "Assurance Plan currentness binding (`CURRENT`/`STALE`/`UNKNOWN`, consumed per §29.1)",
    "sweep_id",
    "exact_source_head",
    "exact_base_target",
    "surfaces[{surface, read_ref, identity, completeness}]",
    "blockers",
    "unresolved_findings",
    "plan_currentness",
    "verdict",
    "Completeness is a recorded fact claim supported by that readback, never defaulted",
    "an unread remainder is never treated as empty",
    "Every configured required check must appear in a COMPLETE required-check listing at the exact head",
    "a configured required check that never reported is an unsatisfied condition, never an implicit pass",
    "A Validation or Review link counts as resolved only when its status is `PASS` at the exact subject",
    "The platform generation recorded by a surface read is the source-side change counter, distinct from the controller's local read sequence",
    "a generation change over unchanged facts and watermarks still invalidates the recorded sweep",
    "UNKNOWN generation or currentness can never support readiness",
    "a missing, not-granted or UNKNOWN permission currentness blocks",
    "Two opposite accepted Review decisions at the same exact subject are a CONFLICT, not last-writer-wins",
    "A stale reviewed HEAD never satisfies a current subject (Interaction Protocol §9.1 semantics consumed read-only)",
    "readiness is computed from current facts only; historical facts stay historical",
    "Any admission-relevant event observed after a surface read — later blocker, late Review, new blocked_by edge, required-check or generation change — invalidates the recorded sweep: verdict BLOCKED, zero partial mutation, re-sweep required",
    "GitHub offers no multi-surface atomic snapshot. A sweep is a bounded read sequence, never a snapshot",
    "not a new gate/workflow state",
)
S142_CLAUSES = (
    "The merge step itself re-admits",
    "fresh bounded final admission readback",
    "compares exact source/base/target identity and per-surface completeness/watermark/generation against the recorded sweep",
    "no blocker exists",
    "the plan binding is `CURRENT`",
    "observes no post-sweep late event",
    "Unchanged HEAD alone never admits",
    "The recorded sweep is validated before any use: every required surface present exactly once, every recorded read COMPLETE, and no recorded blocker or conflict contradicting a green verdict",
    "a verdict flag alone is never proof",
    "The merge mutation itself is conditional on the exact expected source head and base/target at the mutation boundary (compare-and-swap)",
    "aborts the merge with zero partial mutation",
    "rejects the merge with zero partial mutation and restarts the sweep",
)
S143_CLAUSES = (
    "A change landing between the final admission readback and the merge attempt is fail-closed when observed: BLOCK/restart, never retroactive ratification",
    "The exact expected HEAD/base-target of the mutation is guarded at the mutation boundary itself, so the uncloseable residual window remains only for the other admission surfaces",
    "the residual window is explicitly documented and compensated",
    "the post-merge record carries a compensating admission re-readback bound to the integration identity",
    "a real bounded read sequence over all required admission surfaces (integration SHA and tree)",
    "any breach it observes marks the integration unratified pending re-sweep",
    "an incomplete, missing-page or transport-UNKNOWN compensating read leaves the integration unratified pending re-sweep",
    "ratification is never granted retroactively",
    "Downstream ready sets are not unlocked from an unratified integration",
)
S144_CLAUSES = (
    "Incomplete or failed surface read, UNKNOWN generation or currentness, watermark gap, late blocker, HEAD/base drift (§12), expected-HEAD compare-and-swap rejection, same-head Review conflict, unresolvable link, a non-`PASS` Validation/Review link status, a configured required check missing from its listing, missing or UNKNOWN permission currentness, an invalid recorded sweep inventory (partial, duplicated or not-complete surface records), or `STALE`/`UNKNOWN` plan binding → `BLOCKED` (or `CONFLICT` where distinct)",
    "recording the exact sweep id, the subject identities and the missing/changed surface",
    "API/transport uncertainty can never be converted to PASS",
    "no merge is ever ratified on an invalidated sweep",
)

# ---------------------------------------------------------------------------
# contract vocabulary (L3 §3/§4; the canonical gate enum is untouched)
# ---------------------------------------------------------------------------

SWEEP_SURFACES = (
    "pr_head",
    "accepted_reviews",
    "blocked_by_dependencies",
    "required_checks",
    "task_validation_links",
    "unresolved_findings",
    "plan_currentness",
    "relevant_permissions",
)

SWEEP_VERDICTS = frozenset({"MERGE_READY", "BLOCKED", "CONFLICT"})
COMPLETENESS = frozenset({"COMPLETE", "INCOMPLETE", "UNKNOWN"})
PLAN_BINDINGS = frozenset({"CURRENT", "STALE", "UNKNOWN"})

MERGE_OUTCOMES = frozenset(
    {"MERGED", "MERGED_UNRATIFIED_RESTART_REQUIRED", "BLOCKED", "REJECTED_RECOMPUTE"}
)

ADMISSION_ROUTES = frozenset(
    {
        "sweep_not_merge_ready",
        "recorded_sweep_invalid_restart_sweep",
        "expected_head_drift_recompute",
        "expected_head_cas_rejected_zero_mutation",
        "identity_mismatch_restart_sweep",
        "late_event_observed_restart_sweep",
        "surface_watermark_changed_restart_sweep",
        "surface_generation_changed_restart_sweep",
        "residual_breach_observed_pre_mutation",
        "final_admission_readback_required",
        "atomic_snapshot_claim_rejected",
        "post_merge_residual_breach_re_sweep_required",
        "post_merge_audit_incomplete_or_unknown",
        "review_conflict_owner",
    }
)

BLOCKER_ROUTES = frozenset(
    {
        "pr_head_unreadable",
        "pr_head_moved_during_sweep",
        "current_acceptance_missing",
        "current_review_p1_blocker",
        "native_blocked_by_dependency",
        "required_check_missing",
        "required_check_not_success",
        "required_check_stale_head",
        "required_link_missing",
        "validation_link_not_pass",
        "review_link_not_pass",
        "link_subject_missing",
        "link_subject_mismatch",
        "link_ambiguous",
        "unresolved_release_significant_finding",
        "plan_currentness_not_current",
        "required_permission_missing",
        "permission_not_granted",
        "permission_currentness_unknown",
        "surface_read_incomplete",
        "surface_read_unknown",
    }
)

# The authoritative Task/Review/Validation links §11 requires to resolve for
# merge (frozen Pack N05 includes the Review binding).
REQUIRED_LINK_KINDS = ("task", "review", "validation")
# Evidence-kind links resolve only with a PASS status at the exact subject;
# FAIL, missing or UNKNOWN status fails closed.
EVIDENCE_LINK_KINDS = ("review", "validation")
# The merge transition's own permission (read-only authority contract).
REQUIRED_PERMISSIONS = ("merge",)

# Deterministic fixture pins (64-hex shaped, distinct per subject).
HEAD_1 = "a1" * 32  # the live candidate head under admission
HEAD_0 = "99" * 32  # a stale, already-superseded reviewed head
BASE_T = "88" * 32  # base/target at sweep time
BASE_T_NEXT = "87" * 32  # a moved base/target (base drift)
INTEGRATION = "ee" * 32
INTEGRATION_TREE = "ef" * 32

CANONICAL_GATE_STATES = frozenset({"PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE"})

# ---------------------------------------------------------------------------
# native fact fixtures (agent-event-v2 shaped; read-only contract reuse)
# ---------------------------------------------------------------------------


def review_event(decision, sha=HEAD_1, accepted=True, operator="op-reviewer-1",
                 session="sess-reviewer-1", event_id="rev-1"):
    """Native REVIEW_DECISION record (agent-event-v2 provenance fields)."""
    return {
        "event": "REVIEW_DECISION",
        "decision": decision,
        "sha": sha,
        "accepted": accepted,
        "actor_role": "reviewer",
        "operator_id": operator,
        "session_ref": session,
        "event_id": event_id,
    }


def base_state(head=HEAD_1, base_target=BASE_T):
    """All §11/§14 prerequisites current at the exact subject."""
    return {
        "pr": 1071,
        "head": head,
        "base_target": base_target,
        "reviews": [review_event("APPROVE")],
        "checks": [{"check": "verify", "state": "SUCCESS", "head_sha": head}],
        "required_checks": ("verify",),
        "blocked_by": [],
        "links": [
            {"kind": "task", "ref": "#1014", "subject_head": head, "status": "OPEN"},
            {"kind": "review", "ref": "review-1", "subject_head": head, "status": "PASS"},
            {"kind": "validation", "ref": "val-1", "subject_head": head, "status": "PASS"},
        ],
        "findings": [],
        "plan": "CURRENT",
        "permissions": [{"permission": "merge", "granted": True, "currentness": "CURRENT"}],
        "generation": 1,
        "watermarks": {
            "accepted_reviews": 0,
            "blocked_by_dependencies": 0,
            "required_checks": 0,
            "task_validation_links": 0,
            "unresolved_findings": 0,
            "plan_currentness": 0,
            "relevant_permissions": 0,
        },
        "merged": False,
    }


def inject_event(state, surface, mutate):
    """A late admission-relevant event: mutates native state and bumps that
    surface's listing watermark (explicit, never silent)."""
    mutate(state)
    state["watermarks"][surface] += 1


# ---------------------------------------------------------------------------
# injected read-boundary adapter (no live GitHub call)
# ---------------------------------------------------------------------------


class GitHubReadBoundary:
    """Deterministic injected read-boundary adapter: models sequential
    surface reads with explicit completeness/watermark facts. Scripted
    faults (truncated listing, missing page, transport failure, unknown
    platform generation) and the platform generation counter are explicit
    and recorded; absence is only ever readable from a COMPLETE listing.

    The adapter distinguishes the source-side platform generation (a real
    source mutation; never moved by reads) from the controller's local read
    sequence (every read bumps it) — request-sequence churn is never
    mistaken for a generation change, and a generation change with
    unchanged facts/watermarks is still detectable through read identity.
    """

    def __init__(self, state, *, truncated=(), missing_pages=(), transport_failures=(),
                 generation_unknown=()):
        self.state = state
        self.truncated = set(truncated)
        self.missing_pages = set(missing_pages)
        self.transport_failures = set(transport_failures)
        self.generation_unknown = set(generation_unknown)
        self.reads = []
        self._read_seq = 0

    def read(self, surface):
        st = self.state
        self._read_seq += 1
        if surface in self.transport_failures:
            record = {
                "surface": surface,
                "read_ref": f"{surface}@transport-error@seq{self._read_seq}",
                "identity": None,
                "completeness": "UNKNOWN",
            }
        elif surface in self.missing_pages:
            record = {
                "surface": surface,
                "read_ref": f"{surface}@page-missing@seq{self._read_seq}",
                "identity": None,
                "completeness": "INCOMPLETE",
            }
        elif surface in self.generation_unknown:
            # The listing and its facts are readable, but the platform
            # cannot establish the source generation for this read:
            # currentness is UNKNOWN and never supports readiness.
            record = {
                "surface": surface,
                "read_ref": f"{surface}@generation-unknown@seq{self._read_seq}",
                "identity": {"generation": None},
                "completeness": "UNKNOWN",
            }
        elif surface in self.truncated:
            record = {
                "surface": surface,
                "read_ref": f"{surface}@truncated@seq{self._read_seq}@ev{st['watermarks'][surface]}",
                "identity": st["watermarks"][surface],
                "completeness": "INCOMPLETE",
            }
        else:
            watermark = st["watermarks"].get(surface, 0)
            record = {
                "surface": surface,
                "read_ref": (
                    f"{surface}@gen{st['generation']}@seq{self._read_seq}@ev{watermark}"
                ),
                "identity": self._identity(surface),
                "completeness": "COMPLETE",
                "facts": self._facts(surface),
            }
        self.reads.append(record)
        return record

    def _identity(self, surface):
        st = self.state
        if surface == "pr_head":
            return {"head": st["head"], "base_target": st["base_target"]}
        return {
            **self._counter_identity(surface),
            "generation": st["generation"],
        }

    def _counter_identity(self, surface):
        st = self.state
        if surface == "required_checks":
            return {"head_sha": st["head"], "watermark": st["watermarks"][surface]}
        if surface == "plan_currentness":
            return {"binding": st["plan"], "watermark": st["watermarks"][surface]}
        return {"listing_watermark": st["watermarks"][surface]}

    def _facts(self, surface):
        st = self.state
        if surface == "pr_head":
            return {"head": st["head"], "base_target": st["base_target"]}
        if surface == "accepted_reviews":
            return {"reviews": list(st["reviews"])}
        if surface == "blocked_by_dependencies":
            return {"blocked_by": list(st["blocked_by"])}
        if surface == "required_checks":
            return {
                "checks": list(st["checks"]),
                "required": list(st["required_checks"]),
            }
        if surface == "task_validation_links":
            return {"links": list(st["links"])}
        if surface == "unresolved_findings":
            return {"findings": list(st["findings"])}
        if surface == "plan_currentness":
            return {"plan": st["plan"]}
        if surface == "relevant_permissions":
            return {"permissions": list(st["permissions"])}
        raise AssertionError(f"unknown surface: {surface}")


# ---------------------------------------------------------------------------
# merge admission decision model
# ---------------------------------------------------------------------------


def run_admission_sweep(adapter):
    """§14.1: one bounded LAST_ADMISSION_SWEEP — a recorded, identity-bound
    read sequence over the surface inventory. Readiness is computed from
    current facts at the exact subject only; historical facts stay
    historical and are never counted."""
    st = adapter.state
    blockers = []
    blockers_by_surface = {}
    conflicts = []
    surfaces = []
    sweep_head = None
    incomplete = False
    unknown = False
    historical = 0

    def block(surface, route):
        blockers.append(route)
        blockers_by_surface.setdefault(surface, []).append(route)

    for surface in SWEEP_SURFACES:
        read = adapter.read(surface)
        surfaces.append(
            {
                "surface": read["surface"],
                "read_ref": read["read_ref"],
                "identity": read["identity"],
                "completeness": read["completeness"],
            }
        )
        if read["completeness"] != "COMPLETE":
            # An unread remainder is never treated as empty: incompleteness
            # alone denies readiness even with zero observed blockers.
            block(
                surface,
                "surface_read_incomplete"
                if read["completeness"] == "INCOMPLETE"
                else "surface_read_unknown",
            )
            incomplete = incomplete or read["completeness"] == "INCOMPLETE"
            unknown = unknown or read["completeness"] == "UNKNOWN"
            continue
        facts = read["facts"]
        if surface == "pr_head":
            if sweep_head is not None and facts["head"] != sweep_head:
                block(surface, "pr_head_moved_during_sweep")
            sweep_head = facts["head"]
            if facts["head"] != st["head"]:
                block(surface, "pr_head_moved_during_sweep")
        elif surface == "accepted_reviews":
            accepted = [rev for rev in facts["reviews"] if rev["accepted"]]
            current = [rev for rev in accepted if rev["sha"] == sweep_head]
            historical += len(accepted) - len(current)
            approvals = [rev for rev in current if rev["decision"] == "APPROVE"]
            changes = [rev for rev in current if rev["decision"] == "REQUEST_CHANGES"]
            if approvals and changes:
                conflicts.append("opposite_accepted_reviews_same_subject")
            if changes:
                block(surface, "current_review_p1_blocker")
            if not approvals:
                block(surface, "current_acceptance_missing")
        elif surface == "blocked_by_dependencies":
            if facts["blocked_by"]:
                block(surface, "native_blocked_by_dependency")
        elif surface == "required_checks":
            listed = {check["check"] for check in facts["checks"]}
            for required in facts["required"]:
                if required not in listed:
                    # A configured required check that never reported is an
                    # unsatisfied condition, never an implicit pass.
                    block(surface, "required_check_missing")
            for check in facts["checks"]:
                if check["head_sha"] != sweep_head:
                    block(surface, "required_check_stale_head")
                elif check["state"] != "SUCCESS":
                    block(surface, "required_check_not_success")
        elif surface == "task_validation_links":
            groups = {}
            for link in facts["links"]:
                groups.setdefault((link["kind"], link["ref"]), []).append(link)
            kinds_present = {kind for kind, _ in groups}
            for kind in REQUIRED_LINK_KINDS:
                if kind not in kinds_present:
                    block(surface, "required_link_missing")
            for (kind, ref), members in groups.items():
                subjects = {m.get("subject_head") for m in members}
                if None in subjects:
                    block(surface, "link_subject_missing")
                elif len(members) > 1 and len(subjects) > 1:
                    block(surface, "link_ambiguous")
                elif subjects != {sweep_head}:
                    block(surface, "link_subject_mismatch")
                elif kind in EVIDENCE_LINK_KINDS and any(
                    m.get("status") != "PASS" for m in members
                ):
                    # A failed, missing or UNKNOWN evidence status never
                    # satisfies the Validation/Review condition.
                    block(
                        surface,
                        "validation_link_not_pass"
                        if kind == "validation"
                        else "review_link_not_pass",
                    )
        elif surface == "unresolved_findings":
            if facts["findings"]:
                block(surface, "unresolved_release_significant_finding")
        elif surface == "plan_currentness":
            if facts["plan"] != "CURRENT":
                block(surface, "plan_currentness_not_current")
        elif surface == "relevant_permissions":
            listed_permissions = {p["permission"] for p in facts["permissions"]}
            for required in REQUIRED_PERMISSIONS:
                if required not in listed_permissions:
                    block(surface, "required_permission_missing")
            for permission in facts["permissions"]:
                if permission.get("currentness") != "CURRENT":
                    block(surface, "permission_currentness_unknown")
                elif not permission.get("granted"):
                    block(surface, "permission_not_granted")

    if sweep_head is None:
        block("pr_head", "pr_head_unreadable")
    if conflicts:
        verdict = "CONFLICT"
    elif blockers or incomplete or unknown or sweep_head is None:
        verdict = "BLOCKED"
    else:
        verdict = "MERGE_READY"
    return {
        "sweep_id": f"last-admission-sweep@gen{st['generation']}@seq{len(adapter.reads)}",
        "exact_source_head": sweep_head,
        "exact_base_target": st["base_target"],
        "surfaces": surfaces,
        "blockers": tuple(sorted(set(blockers))),
        "blockers_by_surface": {
            surface: tuple(sorted(routes)) for surface, routes in blockers_by_surface.items()
        },
        "conflicts": tuple(sorted(set(conflicts))),
        "unresolved_findings": tuple(st["findings"]),
        "plan_currentness": st["plan"],
        "verdict": verdict,
        "incomplete": incomplete or unknown,
        "historical_reviews_ignored": historical,
        "atomic_snapshot_claim": False,
    }


class CachedCombinedSnapshot:
    """N06 fault: ONE cached combined read presented as GitHub-atomic truth.
    Carries no per-surface read identity and claims snapshot semantics."""

    def __init__(self, state):
        self.state = state

    def as_sweep(self):
        return {
            "sweep_id": "cached-combined-read",
            "exact_source_head": self.state["head"],
            "exact_base_target": self.state["base_target"],
            "surfaces": [],
            "blockers": (),
            "conflicts": (),
            "unresolved_findings": (),
            "plan_currentness": self.state["plan"],
            "verdict": "MERGE_READY",
            "incomplete": False,
            "historical_reviews_ignored": 0,
            "atomic_snapshot_claim": True,
        }


def attempt_unguarded_merge(adapter, expected_head):
    """P03 half: an unchanged HEAD alone never admits. A merge attempt
    without a current final admission readback is always rejected."""
    return {
        "decision": "BLOCKED",
        "routes": ("final_admission_readback_required",),
        "merge_result": None,
    }


def _recorded_sweep_defects(sweep):
    """P1-02: validate the recorded sweep itself — every required surface
    exactly once, all COMPLETE, no recorded blocker/conflict, no incomplete
    flag. A green verdict flag alone is never proof."""
    defects = []
    records = sweep.get("surfaces") or []
    names = [record.get("surface") for record in records]
    if sorted(names) != sorted(SWEEP_SURFACES):
        defects.append("surface_inventory_mismatch")
    if len(names) != len(set(names)):
        defects.append("duplicate_surface_record")
    if any(record.get("completeness") != "COMPLETE" for record in records):
        defects.append("recorded_surface_not_complete")
    if sweep.get("incomplete"):
        defects.append("recorded_incomplete_flag")
    if sweep.get("blockers") or sweep.get("conflicts"):
        defects.append("recorded_blocker_contradicts_green_verdict")
    return defects


def guarded_merge(adapter, sweep, expected_head, *, residual_inject=None,
                  residual_visible=True):
    """§14.2/§14.3: the merge step itself re-admits.

    Order: recorded-sweep admissibility → recorded-sweep inventory
    validation → expected-head guard → fresh bounded final admission
    readback (identity + watermark/generation comparison) → last bounded
    mutation-guard recheck (including the exact head/base-target identity)
    → conditional merge mutation (compare-and-swap on the exact expected
    head/base-target) → post-merge compensating admission re-readback — a
    real read sequence over all required surfaces bound to the integration
    identity. `residual_inject` models a change landing in the
    final-read-to-merge window: visible=True places it before the last
    recheck (observable → zero mutation); visible=False places it after the
    last recheck — head/base-target drift is still rejected by the
    mutation's compare-and-swap, while other-surface changes fall in the
    true residual gap and surface only through the compensating audit
    (unratified pending re-sweep, never ratified retroactively)."""
    outcome = {"decision": None, "routes": [], "merge_result": None, "audit": None}

    if sweep.get("atomic_snapshot_claim") or not sweep.get("surfaces"):
        outcome["decision"] = "BLOCKED"
        outcome["routes"].append("atomic_snapshot_claim_rejected")
        return outcome
    if sweep["verdict"] != "MERGE_READY":
        outcome["decision"] = "BLOCKED"
        outcome["routes"].append("sweep_not_merge_ready")
        return outcome
    inventory_defects = _recorded_sweep_defects(sweep)
    if inventory_defects:
        outcome["decision"] = "BLOCKED"
        outcome["routes"].append("recorded_sweep_invalid_restart_sweep")
        outcome["sweep_defects"] = tuple(sorted(set(inventory_defects)))
        return outcome
    if expected_head != sweep["exact_source_head"]:
        outcome["decision"] = "REJECTED_RECOMPUTE"
        outcome["routes"].append("expected_head_drift_recompute")
        return outcome

    final = run_admission_sweep(adapter)
    if (
        final["exact_source_head"] != sweep["exact_source_head"]
        or final["exact_base_target"] != sweep["exact_base_target"]
    ):
        outcome["decision"] = "BLOCKED"
        outcome["routes"].append("identity_mismatch_restart_sweep")
        return outcome
    if final["verdict"] != "MERGE_READY":
        outcome["decision"] = "BLOCKED"
        outcome["routes"].append("late_event_observed_restart_sweep")
        return outcome

    sweep_identity = {
        s["surface"]: s["identity"] for s in sweep["surfaces"] if s["completeness"] == "COMPLETE"
    }
    final_identity = {
        s["surface"]: s["identity"] for s in final["surfaces"] if s["completeness"] == "COMPLETE"
    }
    changed = sorted(s for s, ident in sweep_identity.items() if final_identity.get(s) != ident)
    if changed:
        watermark_only_changed = all(
            _identity_watermark(sweep_identity[s]) == _identity_watermark(final_identity.get(s))
            for s in changed
        )
        outcome["decision"] = "BLOCKED"
        outcome["routes"].append(
            "surface_generation_changed_restart_sweep"
            if watermark_only_changed
            else "surface_watermark_changed_restart_sweep"
        )
        outcome["changed_surfaces"] = tuple(changed)
        return outcome

    # Last bounded mutation-guard recheck: watermark/generation comparison
    # over the final readback's identities plus the exact head/base-target
    # identity, taken immediately before the mutation.
    def mutation_guard_breaches():
        breaches = set()
        head_identity = _final_identity(final, "pr_head")
        if head_identity is not None and (
            head_identity.get("head") != adapter.state["head"]
            or head_identity.get("base_target") != adapter.state["base_target"]
        ):
            breaches.add("pr_head")
        for surface, watermark in adapter.state["watermarks"].items():
            if _identity_watermark(_final_identity(final, surface)) != watermark:
                breaches.add(surface)
            final_generation = _final_generation(final, surface)
            if final_generation is not None and final_generation != adapter.state["generation"]:
                breaches.add(surface)
        return sorted(breaches)

    if residual_inject is not None and residual_visible:
        # The breach lands after the final readback but before the last
        # bounded recheck: observable, so the mutation aborts with zero
        # partial mutation.
        residual_inject(adapter.state)
        breach_now = mutation_guard_breaches()
        if breach_now:
            outcome["decision"] = "BLOCKED"
            outcome["routes"].append("residual_breach_observed_pre_mutation")
            outcome["changed_surfaces"] = tuple(breach_now)
            return outcome

    st = adapter.state
    if residual_inject is not None and not residual_visible:
        # The breach lands after the last bounded recheck. The merge
        # mutation is still conditional: compare-and-swap on the exact
        # expected head/base-target at the mutation boundary itself.
        residual_inject(st)
    if st["head"] != expected_head or st["base_target"] != sweep["exact_base_target"]:
        outcome["decision"] = "BLOCKED"
        outcome["routes"].append("expected_head_cas_rejected_zero_mutation")
        outcome["changed_surfaces"] = ("pr_head",)
        return outcome
    merge_result = {
        "source_head": expected_head,
        "base_target_before": sweep["exact_base_target"],
        "integration_sha": INTEGRATION,
        "integration_tree": INTEGRATION_TREE,
        "sweep_id": sweep["sweep_id"],
        "final_readback_sweep_id": final["sweep_id"],
        "ratified": True,
    }
    st["merged"] = True

    # §14.3 compensating audit: a real post-merge admission re-readback
    # bound to the integration identity.
    audit = compensating_post_merge_readback(adapter, merge_result)
    if audit["ratified"]:
        outcome["audit"] = {
            "integration_sha": audit["integration_sha"],
            "integration_tree": audit["integration_tree"],
            "compensating_readback_sweep_id": audit["sweep_id"],
            "compensating_readback_surfaces": [],
            "unread_surfaces": (),
            "ratified": True,
            "route": "no_post_merge_breach_observed",
        }
        outcome["decision"] = "MERGED"
    else:
        merge_result["ratified"] = False
        breach_surfaces = sorted(set(audit["unread_surfaces"]) | set(audit["breach_surfaces"]))
        if audit["unread_surfaces"]:
            outcome["routes"].append("post_merge_audit_incomplete_or_unknown")
        if audit["breach_blockers"] or audit["breach_conflicts"]:
            outcome["routes"].append("post_merge_residual_breach_re_sweep_required")
        outcome["audit"] = {
            "integration_sha": audit["integration_sha"],
            "integration_tree": audit["integration_tree"],
            "compensating_readback_sweep_id": audit["sweep_id"],
            "compensating_readback_surfaces": breach_surfaces,
            "unread_surfaces": audit["unread_surfaces"],
            "breach_blockers": audit["breach_blockers"],
            "breach_conflicts": audit["breach_conflicts"],
            "ratified": False,
            "route": "unratified_pending_re_sweep",
        }
        outcome["decision"] = "MERGED_UNRATIFIED_RESTART_REQUIRED"
    outcome["merge_result"] = merge_result
    return outcome


def compensating_post_merge_readback(adapter, merge_result):
    """§14.3: a genuinely injected, integration-identity-bound read sequence
    over ALL required admission surfaces after the merge mutation. An
    incomplete, missing-page or transport-UNKNOWN read is an audit failure:
    the integration stays unratified pending re-sweep; late admission
    facts observed by the audit are breaches, never retroactive PASS."""
    audit_sweep = run_admission_sweep(adapter)
    unread_surfaces = tuple(
        s["surface"] for s in audit_sweep["surfaces"] if s["completeness"] != "COMPLETE"
    )
    return {
        "integration_sha": merge_result["integration_sha"],
        "integration_tree": merge_result["integration_tree"],
        "sweep_id": audit_sweep["sweep_id"],
        "unread_surfaces": unread_surfaces,
        "breach_blockers": tuple(audit_sweep["blockers"]),
        "breach_conflicts": tuple(audit_sweep["conflicts"]),
        "breach_surfaces": tuple(sorted(audit_sweep["blockers_by_surface"])),
        "ratified": not unread_surfaces
        and not audit_sweep["blockers"]
        and not audit_sweep["conflicts"],
    }


def _final_identity(final_sweep, surface):
    for record in final_sweep["surfaces"]:
        if record["surface"] == surface and record["completeness"] == "COMPLETE":
            return record["identity"]
    return None


def _identity_watermark(identity):
    if isinstance(identity, dict):
        if "watermark" in identity:
            return identity["watermark"]
        if "listing_watermark" in identity:
            return identity["listing_watermark"]
    return None


def _final_generation(final_sweep, surface):
    identity = _final_identity(final_sweep, surface)
    if isinstance(identity, dict) and "generation" in identity:
        return identity["generation"]
    return None


def downstream_ready_sets(merge_result):
    """P04: downstream READY is recomputed from MERGE_RESULT only — never
    before it, and never from an unratified integration."""
    if merge_result is None or merge_result.get("ratified") is not True:
        return {"T08": "NOT_READY"}
    return {"T08": "READY"}


def dump(result) -> str:
    return json.dumps(result, sort_keys=True, default=str)


# ---------------------------------------------------------------------------
# repository helpers
# ---------------------------------------------------------------------------


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True
    ).stdout


def git_blob(rev: str, path: str) -> str:
    return git("rev-parse", f"{rev}:{path}").strip()


def ea_text() -> str:
    return EA_PATH.read_text(encoding="utf-8")


def section(text: str, start_marker: str, end_marker: str) -> str:
    start = text.index(start_marker)
    end = text.index(end_marker, start + len(start_marker))
    return text[start:end]


def base_ea_text() -> str:
    return git("show", f"{BASE_SHA}:{EA}")


def headings(text: str):
    return [m.group(0).strip() for m in re.finditer(r"^## .+$", text, re.M)]


def recursive_keys(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield key
            yield from recursive_keys(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from recursive_keys(item)


# ---------------------------------------------------------------------------
# Layer 1: section-scoped textual contracts + verbatim owner-span guards
# ---------------------------------------------------------------------------


class Section14PlacementTests(unittest.TestCase):
    def test_new_subsections_exist_once_inside_14_before_15(self):
        text = ea_text()
        for heading in NEW_SUBSECTIONS:
            with self.subTest(heading=heading):
                self.assertEqual(text.count(heading), 1)
        start = text.index(SECTION_14)
        end = text.index(SECTION_15, start)
        positions = [text.index(h, start) for h in NEW_SUBSECTIONS]
        self.assertTrue(start < positions[0] < positions[1] < positions[2] < positions[3] < end)
        # No other new headings were introduced inside §14.
        inside = text[start:end]
        self.assertEqual(
            len(re.findall(r"^### ", inside, re.M)),
            len(NEW_SUBSECTIONS),
        )

    def test_preexisting_section14_content_stays_byte_verbatim(self):
        text = ea_text()
        original = section(base_ea_text(), SECTION_14, SECTION_15).rstrip()
        self.assertIn(original, text)
        # The original span strictly precedes every new subsection.
        original_end = text.index(original) + len(original)
        for heading in NEW_SUBSECTIONS:
            self.assertGreater(text.index(heading), original_end)

    def test_neighbouring_owner_spans_and_heading_sequence_unchanged(self):
        head, base = ea_text(), base_ea_text()
        self.assertEqual(headings(head), headings(base), "top-level heading sequence moved")
        self.assertEqual(section(head, "## 12.", "## 13."), section(base, "## 12.", "## 13."))
        self.assertEqual(section(head, SECTION_15, "## 16."), section(base, SECTION_15, "## 16."))

    def test_read_only_owner_files_unchanged_from_exact_base(self):
        for rel in READ_ONLY_PATHS:
            if rel == PROTOCOL_PATH:
                continue  # I1122 re-bind, exact successor-blob identity pin below
            with self.subTest(path=rel):
                self.assertEqual(git_blob(BASE_SHA, rel), git_blob("HEAD", rel))
        # I1122 re-bind: the historical pin stays re-derivable from the exact
        # base (tamper anchor); the admitted successor blob is exactly the
        # approved policy-change content — any third blob still fails.
        self.assertEqual(PROTOCOL_BASE_BLOB, git_blob(BASE_SHA, PROTOCOL_PATH))
        self.assertEqual(PROTOCOL_I1122_BLOB, git_blob("HEAD", PROTOCOL_PATH))

    def test_schemas_tree_unchanged_from_exact_base(self):
        base_schema_files = set(
            filter(None, git("ls-tree", "-r", "--name-only", BASE_SHA, "schemas").splitlines())
        )
        head_schema_files = set(
            filter(None, git("ls-tree", "-r", "--name-only", "HEAD", "schemas").splitlines())
        )
        self.assertEqual(base_schema_files, head_schema_files)
        for rel in sorted(base_schema_files):
            self.assertEqual(git_blob(BASE_SHA, rel), git_blob("HEAD", rel), rel)

    def test_owner_write_set_is_exactly_two_paths_and_tree_clean(self):
        # Owner write-set is an immutable source-lane fact. The integrated
        # version can lawfully contain other owners' already-reviewed changes;
        # comparing original BASE_SHA to integrated HEAD would falsely blame
        # those unrelated paths on T07.
        changed = set(filter(None, git(
            "diff", "--name-only", BASE_SHA, OWNER_QUALIFIED_HEAD
        ).splitlines()))
        self.assertEqual(changed, {EA, "scripts/test_v411_merge_admission.py"})
        # An unrelated/reconstructed tree must not impersonate the reviewed
        # owner successor merely by copying the text.
        git("merge-base", "--is-ancestor", OWNER_QUALIFIED_HEAD, "HEAD")
        # T07 must preserve the COMPLETE source-reviewed owner standard:
        # checking only §14 allows a clean, committed unauthorized rewrite
        # outside §14 to masquerade as a lawful ancestry-only composition.
        # A later owner (e.g. T14) needs its own exact qualified successor
        # and integration-scoped proof; it is never implicitly whitelisted.
        approved = git("show", f"{OWNER_QUALIFIED_HEAD}:{EA}")
        self.assertEqual(ea_text(), approved)
        self.assertEqual(git("status", "--porcelain").strip(), "")


class Section14ContractTests(unittest.TestCase):
    def test_sweep_surface_inventory_and_projection_clauses_bound(self):
        section_141 = section(ea_text(), S141, S142)
        for clause in S141_CLAUSES:
            with self.subTest(clause=clause):
                self.assertIn(clause, section_141)

    def test_merge_boundary_guard_clauses_bound(self):
        section_142 = section(ea_text(), S142, S143)
        for clause in S142_CLAUSES:
            with self.subTest(clause=clause):
                self.assertIn(clause, section_142)

    def test_residual_window_clauses_bound(self):
        section_143 = section(ea_text(), S143, S144)
        for clause in S143_CLAUSES:
            with self.subTest(clause=clause):
                self.assertIn(clause, section_143)

    def test_failure_routing_clauses_bound(self):
        section_144 = section(ea_text(), S144, SECTION_15)
        for clause in S144_CLAUSES:
            with self.subTest(clause=clause):
                self.assertIn(clause, section_144)

    def test_no_new_gate_enum_and_no_machine_schema_minted_in_14(self):
        section_14 = section(ea_text(), SECTION_14, SECTION_15)
        gate_tokens = set(re.findall(r"`(PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE)`", section_14))
        self.assertTrue(gate_tokens)
        self.assertTrue(gate_tokens <= CANONICAL_GATE_STATES, gate_tokens - CANONICAL_GATE_STATES)
        self.assertNotIn("schema_version", section_14)
        self.assertNotIn("```json", section_14)

    def test_no_snapshot_authority_language(self):
        section_14 = section(ea_text(), SECTION_14, SECTION_15)
        self.assertIn("GitHub offers no multi-surface atomic snapshot", section_14)
        self.assertIn("never a snapshot", section_14)
        self.assertIn("never retroactive ratification", section_14)


# ---------------------------------------------------------------------------
# Layer 2: fixture-driven admission oracles (L3 §3 P01-P04 / N01-N12)
# ---------------------------------------------------------------------------


class P01SweepRecordsExactStateAndAdmitsTests(unittest.TestCase):
    def test_p01_current_facts_sweep_is_recorded_and_merge_admits(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        self.assertEqual(sweep["verdict"], "MERGE_READY")
        self.assertEqual(sweep["exact_source_head"], HEAD_1)
        self.assertEqual(sweep["exact_base_target"], BASE_T)
        self.assertEqual(sweep["blockers"], ())
        self.assertEqual(sweep["plan_currentness"], "CURRENT")
        # Sweep identity + per-surface read refs + completeness facts.
        self.assertTrue(sweep["sweep_id"])
        self.assertEqual(
            [s["surface"] for s in sweep["surfaces"]], list(SWEEP_SURFACES)
        )
        for record in sweep["surfaces"]:
            with self.subTest(surface=record["surface"]):
                self.assertEqual(record["completeness"], "COMPLETE")
                self.assertTrue(record["read_ref"])
                self.assertIsNotNone(record["identity"])
        # Every read is recorded in order — a bounded read sequence.
        pass_len = len(SWEEP_SURFACES)
        self.assertEqual(
            [r["surface"] for r in adapter.reads[:pass_len]], list(SWEEP_SURFACES)
        )
        # Guarded merge executes and the post-merge record binds identities.
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "MERGED")
        # Three full read passes in total: the recorded sweep, the merge's
        # final admission readback and the post-merge compensating audit.
        self.assertEqual(len(adapter.reads), 3 * pass_len)
        self.assertEqual(
            [r["surface"] for r in adapter.reads[-pass_len:]], list(SWEEP_SURFACES)
        )
        result = outcome["merge_result"]
        self.assertEqual(result["source_head"], HEAD_1)
        self.assertEqual(result["base_target_before"], BASE_T)
        self.assertEqual(result["integration_sha"], INTEGRATION)
        self.assertTrue(result["integration_tree"])
        self.assertEqual(result["sweep_id"], sweep["sweep_id"])
        self.assertTrue(result["ratified"])
        self.assertEqual(outcome["audit"]["route"], "no_post_merge_breach_observed")

    def test_p01_unreadable_transport_is_never_a_pass(self):
        adapter = GitHubReadBoundary(base_state(), transport_failures=("accepted_reviews",))
        sweep = run_admission_sweep(adapter)
        self.assertEqual(sweep["verdict"], "BLOCKED")
        self.assertIn("surface_read_unknown", sweep["blockers"])
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIsNone(outcome["merge_result"])


class P02StaleReviewedHeadIsHistoricalTests(unittest.TestCase):
    def test_p02_stale_subject_pass_never_counts_readiness_from_current_only(self):
        state = base_state()
        state["reviews"].append(review_event("APPROVE", sha=HEAD_0, event_id="rev-old"))
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        # The stale-subject PASS stays historical (retained, never counted):
        self.assertEqual(sweep["historical_reviews_ignored"], 1)
        self.assertEqual(sweep["verdict"], "MERGE_READY")
        self.assertEqual(sweep["exact_source_head"], HEAD_1)
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "MERGED")

    def test_p02_stale_head_with_no_current_acceptance_blocks(self):
        state = base_state()
        state["reviews"] = [review_event("APPROVE", sha=HEAD_0, event_id="rev-old")]
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertEqual(sweep["verdict"], "BLOCKED")
        self.assertIn("current_acceptance_missing", sweep["blockers"])
        self.assertEqual(sweep["historical_reviews_ignored"], 1)


class P03MergeBoundaryGuardTests(unittest.TestCase):
    def test_p03_merge_proceeds_on_sweep_plus_confirming_final_readback(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        reviews_before = len(adapter.state["reviews"])
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "MERGED")
        # No re-review was demanded: the confirming final readback observed
        # the same accepted current Review and requested no new one.
        self.assertEqual(len(adapter.state["reviews"]), reviews_before)
        self.assertEqual(outcome["audit"]["ratified"], True)

    def test_p03_unchanged_head_alone_never_admits(self):
        adapter = GitHubReadBoundary(base_state())
        outcome = attempt_unguarded_merge(adapter, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("final_admission_readback_required", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])

    def test_p03_expected_head_change_immediately_before_merge_rejects(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        # The live PR head moves after the sweep, before the merge step.
        inject_event(adapter.state, "accepted_reviews", lambda s: None)
        adapter.state["head"] = HEAD_0
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("identity_mismatch_restart_sweep", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])

    def test_p03_expected_head_guard_rejects_stale_expectation(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)  # live head is HEAD_1
        outcome = guarded_merge(adapter, sweep, HEAD_0)  # expectation is stale
        self.assertEqual(outcome["decision"], "REJECTED_RECOMPUTE")
        self.assertIn("expected_head_drift_recompute", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])


class P04DownstreamRecomputeFromMergeResultTests(unittest.TestCase):
    def test_p04_downstream_not_ready_before_merge_ready_from_result_after(self):
        adapter = GitHubReadBoundary(base_state())
        self.assertEqual(downstream_ready_sets(None), {"T08": "NOT_READY"})
        sweep = run_admission_sweep(adapter)
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "MERGED")
        self.assertEqual(
            downstream_ready_sets(outcome["merge_result"]), {"T08": "READY"}
        )

    def test_p04_downstream_never_unlocked_from_unratified_integration(self):
        unratified = {"integration_sha": INTEGRATION, "ratified": False}
        self.assertEqual(downstream_ready_sets(unratified), {"T08": "NOT_READY"})


class N01LateBlockerInvalidatesSweepTests(unittest.TestCase):
    def test_n01_blocker_after_sweep_before_merge_blocks_with_zero_mutation(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        self.assertEqual(sweep["verdict"], "MERGE_READY")

        def late_release_significant_finding(s):
            s["findings"].append("F-RES-LATE-1")
            s["watermarks"]["unresolved_findings"] += 1

        inject_event(adapter.state, "unresolved_findings", late_release_significant_finding)
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("late_event_observed_restart_sweep", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])
        self.assertFalse(adapter.state["merged"])
        # The recorded sweep is invalidated: a re-sweep is required.
        resweep = run_admission_sweep(adapter)
        self.assertEqual(resweep["verdict"], "BLOCKED")
        self.assertIn("unresolved_release_significant_finding", resweep["blockers"])


class N02PaginationIncompletenessNeverAbsenceTests(unittest.TestCase):
    def test_n02_truncated_sweep_listing_blocks_without_inference(self):
        adapter = GitHubReadBoundary(base_state(), truncated=("accepted_reviews",))
        sweep = run_admission_sweep(adapter)
        self.assertTrue(sweep["incomplete"])
        self.assertEqual(sweep["verdict"], "BLOCKED")
        self.assertIn("surface_read_incomplete", sweep["blockers"])
        # Zero observed blockers is irrelevant: absence is never inferred
        # from an unread remainder.
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIsNone(outcome["merge_result"])


class N03OppositeAcceptedReviewsConflictTests(unittest.TestCase):
    def test_n03_same_subject_opposite_accepted_reviews_conflict_not_lww(self):
        state = base_state()
        state["reviews"].append(
            review_event("REQUEST_CHANGES", operator="op-reviewer-2",
                         session="sess-reviewer-2", event_id="rev-2")
        )
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertEqual(sweep["verdict"], "CONFLICT")
        self.assertIn("opposite_accepted_reviews_same_subject", sweep["conflicts"])
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("sweep_not_merge_ready", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])
        # CONFLICT routes to the Review-conflict owner (read-only contract).
        self.assertIn("review_conflict_owner", ADMISSION_ROUTES)


class N04DriftAfterEvidenceTests(unittest.TestCase):
    def test_n04_head_drift_after_evidence_old_evidence_stays_historical(self):
        state = base_state()
        state["reviews"] = [
            review_event("APPROVE", sha=HEAD_0, event_id="rev-at-old-head")
        ]
        state["checks"] = [{"check": "verify", "state": "SUCCESS", "head_sha": HEAD_0}]
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertEqual(sweep["exact_source_head"], HEAD_1)
        self.assertEqual(sweep["historical_reviews_ignored"], 1)
        self.assertIn("current_acceptance_missing", sweep["blockers"])
        self.assertIn("required_check_stale_head", sweep["blockers"])
        self.assertEqual(sweep["verdict"], "BLOCKED")

    def test_n04_base_drift_between_sweep_and_merge_restarts(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        adapter.state["base_target"] = BASE_T_NEXT
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("identity_mismatch_restart_sweep", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])


class N05LinkResolutionTests(unittest.TestCase):
    def _link(self, state, kind):
        return next(l for l in state["links"] if l["kind"] == kind)

    def test_n05_link_bound_to_different_subject_blocks(self):
        state = base_state()
        self._link(state, "validation")["subject_head"] = HEAD_0
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertEqual(sweep["verdict"], "BLOCKED")
        self.assertIn("link_subject_mismatch", sweep["blockers"])

    def test_n05_link_missing_subject_blocks(self):
        state = base_state()
        self._link(state, "validation")["subject_head"] = None
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertIn("link_subject_missing", sweep["blockers"])

    def test_n05_ambiguous_link_blocks(self):
        state = base_state()
        state["links"].append(
            {"kind": "validation", "ref": "val-1", "subject_head": HEAD_0, "status": "PASS"}
        )
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertIn("link_ambiguous", sweep["blockers"])
        self.assertEqual(sweep["verdict"], "BLOCKED")

    def test_n05_missing_required_link_kind_blocks(self):
        # The required Validation link is absent entirely: the condition is
        # unsatisfied, never guessed from the remaining surface.
        state = base_state()
        state["links"] = [state["links"][0]]
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertIn("required_link_missing", sweep["blockers"])
        self.assertEqual(sweep["verdict"], "BLOCKED")
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIsNone(outcome["merge_result"])

    def test_n05_all_required_links_current_admits(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        self.assertNotIn("required_link_missing", sweep["blockers"])
        self.assertEqual(sweep["verdict"], "MERGE_READY")


class N06NoAtomicSnapshotClaimTests(unittest.TestCase):
    def test_n06_cached_combined_read_never_admits(self):
        adapter = GitHubReadBoundary(base_state())
        snapshot = CachedCombinedSnapshot(adapter.state).as_sweep()
        self.assertTrue(snapshot["atomic_snapshot_claim"])
        outcome = guarded_merge(adapter, snapshot, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("atomic_snapshot_claim_rejected", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])

    def test_n06_sweep_without_per_surface_reads_is_not_admissible(self):
        empty = {
            "sweep_id": "no-surfaces",
            "exact_source_head": HEAD_1,
            "exact_base_target": BASE_T,
            "surfaces": [],
            "verdict": "MERGE_READY",
        }
        outcome = guarded_merge(GitHubReadBoundary(base_state()), empty, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("atomic_snapshot_claim_rejected", outcome["routes"])


class N07PlanCurrentnessAtMergeTests(unittest.TestCase):
    def test_n07_stale_or_unknown_plan_binding_blocks_merge_transition(self):
        for binding in ("STALE", "UNKNOWN"):
            with self.subTest(binding=binding):
                state = base_state()
                state["plan"] = binding
                adapter = GitHubReadBoundary(state)
                sweep = run_admission_sweep(adapter)
                self.assertEqual(sweep["verdict"], "BLOCKED")
                self.assertIn("plan_currentness_not_current", sweep["blockers"])
                self.assertEqual(sweep["plan_currentness"], binding)
                outcome = guarded_merge(adapter, sweep, HEAD_1)
                self.assertEqual(outcome["decision"], "BLOCKED")
                self.assertIsNone(outcome["merge_result"])


class N08LateSameHeadReviewRestartsTests(unittest.TestCase):
    def test_n08_late_contradictory_accepted_review_same_head_blocks(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        self.assertEqual(sweep["verdict"], "MERGE_READY")

        def late_contradictory(s):
            s["reviews"].append(
                review_event("REQUEST_CHANGES", operator="op-reviewer-2",
                             session="sess-reviewer-2", event_id="rev-late-2")
            )

        inject_event(adapter.state, "accepted_reviews", late_contradictory)
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("late_event_observed_restart_sweep", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])
        self.assertFalse(adapter.state["merged"])
        resweep = run_admission_sweep(adapter)
        self.assertIn("opposite_accepted_reviews_same_subject", resweep["conflicts"])
        self.assertEqual(resweep["verdict"], "CONFLICT")


class N09LateDependencyEdgeRestartsTests(unittest.TestCase):
    def test_n09_late_blocked_by_edge_after_sweep_blocks(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        inject_event(
            adapter.state,
            "blocked_by_dependencies",
            lambda s: s["blocked_by"].append({"blocked_by": 1010}),
        )
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIsNone(outcome["merge_result"])
        resweep = run_admission_sweep(adapter)
        self.assertIn("native_blocked_by_dependency", resweep["blockers"])


class N10WatermarkChangeDetectionTests(unittest.TestCase):
    def test_n10_pure_generation_change_without_new_blocker_restarts(self):
        # A second current APPROVE creates no fact-level blocker, but the
        # accepted_reviews listing watermark moved: the merge-boundary guard
        # must detect the generation change by watermark comparison alone.
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        inject_event(
            adapter.state,
            "accepted_reviews",
            lambda s: s["reviews"].append(
                review_event("APPROVE", operator="op-reviewer-2",
                             session="sess-reviewer-2", event_id="rev-2")
            ),
        )
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("surface_watermark_changed_restart_sweep", outcome["routes"])
        self.assertEqual(outcome["changed_surfaces"], ("accepted_reviews",))
        self.assertIsNone(outcome["merge_result"])

    def test_n10_required_check_state_change_after_sweep_is_detected(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)

        def flip_check(s):
            s["checks"][0]["state"] = "FAILED"

        inject_event(adapter.state, "required_checks", flip_check)
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("late_event_observed_restart_sweep", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])
        resweep = run_admission_sweep(adapter)
        self.assertIn("required_check_not_success", resweep["blockers"])


class N11FinalReadbackMissingPageTests(unittest.TestCase):
    def test_n11_missing_page_in_final_readback_fails_closed(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        self.assertEqual(sweep["verdict"], "MERGE_READY")
        # A page goes missing only for the final admission readback.
        adapter.missing_pages.add("unresolved_findings")
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("late_event_observed_restart_sweep", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])
        self.assertFalse(adapter.state["merged"])


class N12ResidualWindowTests(unittest.TestCase):
    def test_n12_observable_residual_breach_aborts_with_zero_mutation(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)

        def residual(s):
            s["reviews"].append(
                review_event("REQUEST_CHANGES", operator="op-reviewer-2",
                             session="sess-reviewer-2", event_id="rev-residual")
            )
            s["watermarks"]["accepted_reviews"] += 1

        outcome = guarded_merge(
            adapter, sweep, HEAD_1, residual_inject=residual, residual_visible=True
        )
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("residual_breach_observed_pre_mutation", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])
        self.assertFalse(adapter.state["merged"])

    def test_n12_true_gap_breach_is_unratified_and_never_retro_ratifed(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)

        def residual(s):
            s["reviews"].append(
                review_event("REQUEST_CHANGES", operator="op-reviewer-2",
                             session="sess-reviewer-2", event_id="rev-gap")
            )
            s["watermarks"]["accepted_reviews"] += 1

        outcome = guarded_merge(
            adapter, sweep, HEAD_1, residual_inject=residual, residual_visible=False
        )
        # The merge mutation executed in the model, but the compensating
        # audit observes the same-HEAD late event: unratified, downstream
        # not unlocked, re-sweep required, never ratified retroactively.
        self.assertEqual(outcome["decision"], "MERGED_UNRATIFIED_RESTART_REQUIRED")
        self.assertIn("post_merge_residual_breach_re_sweep_required", outcome["routes"])
        self.assertIn("accepted_reviews", outcome["audit"]["compensating_readback_surfaces"])
        self.assertFalse(outcome["merge_result"]["ratified"])
        self.assertEqual(downstream_ready_sets(outcome["merge_result"]), {"T08": "NOT_READY"})
        resweep = run_admission_sweep(adapter)
        self.assertNotEqual(resweep["verdict"], "MERGE_READY")

    def test_n12_no_residual_breach_keeps_audit_clean(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "MERGED")
        self.assertTrue(outcome["merge_result"]["ratified"])
        self.assertEqual(outcome["audit"]["compensating_readback_surfaces"], [])


class ModelVocabularyAndRoutingTests(unittest.TestCase):
    """Contract hardening: model vocabulary stays inside declared sets and
    every failure route is fail-closed, never green."""

    def test_merge_outcomes_stay_inside_declared_sets(self):
        scenarios = [
            GitHubReadBoundary(base_state()),
            GitHubReadBoundary(base_state(), truncated=("accepted_reviews",)),
            GitHubReadBoundary(base_state(), transport_failures=("plan_currentness",)),
        ]
        for adapter in scenarios:
            sweep = run_admission_sweep(adapter)
            with self.subTest(verdict=sweep["verdict"]):
                self.assertIn(sweep["verdict"], SWEEP_VERDICTS)
                self.assertTrue(set(sweep["blockers"]) <= BLOCKER_ROUTES)
                for record in sweep["surfaces"]:
                    self.assertIn(record["completeness"], COMPLETENESS)
        state = base_state()
        state["plan"] = "STALE"
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertIn(sweep["plan_currentness"], PLAN_BINDINGS)

    def test_admission_routes_stay_declared_and_never_mint_gate_states(self):
        outcomes = []
        good = GitHubReadBoundary(base_state())
        outcomes.append(guarded_merge(good, run_admission_sweep(good), HEAD_1))
        drifted = GitHubReadBoundary(base_state())
        outcomes.append(
            guarded_merge(drifted, run_admission_sweep(drifted), HEAD_0)
        )
        for outcome in outcomes:
            with self.subTest(decision=outcome["decision"]):
                self.assertIn(outcome["decision"], MERGE_OUTCOMES)
                self.assertTrue(set(outcome["routes"]) <= ADMISSION_ROUTES)
                self.assertNotIn('"PASS"', dump(outcome))

    def test_failed_merges_mutate_nothing(self):
        failing = [
            (lambda a: GitHubReadBoundary(a, truncated=("required_checks",)), HEAD_1),
        ]
        for build, expected in failing:
            adapter = build(base_state())
            sweep = run_admission_sweep(adapter)
            outcome = guarded_merge(adapter, sweep, expected)
            with self.subTest(decision=outcome["decision"]):
                self.assertIn(outcome["decision"], {"BLOCKED", "REJECTED_RECOMPUTE"})
                self.assertIsNone(outcome["merge_result"])
                self.assertFalse(adapter.state["merged"])

    def test_review_conflict_and_projection_routes_are_declared(self):
        routed = {"review_conflict": "review_conflict_owner",
                  "sweep_projection": "DEFERRED_TO_T11"}
        self.assertIn(routed["review_conflict"], ADMISSION_ROUTES)
        self.assertEqual(routed["sweep_projection"], "DEFERRED_TO_T11")


# ---------------------------------------------------------------------------
# R1 repair oracles (#1014@6118919006 findings P1-01..P1-04, P2-01, P2-02)
# ---------------------------------------------------------------------------


class R1P1RequiredPrerequisiteTests(unittest.TestCase):
    """P1-01: a missing configured required check, a failed/unknown
    Validation link and a missing required Review binding can never become
    MERGE_READY (Interaction §11 prerequisites, read-only)."""

    def test_p1_missing_configured_required_check_blocks(self):
        state = base_state()
        state["checks"] = []  # the configured required check never reported
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertIn("required_check_missing", sweep["blockers"])
        self.assertEqual(sweep["verdict"], "BLOCKED")
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIsNone(outcome["merge_result"])
        self.assertFalse(adapter.state["merged"])

    def test_p1_failed_validation_link_blocks(self):
        state = base_state()
        validation = next(l for l in state["links"] if l["kind"] == "validation")
        validation["status"] = "FAIL"
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertIn("validation_link_not_pass", sweep["blockers"])
        self.assertEqual(sweep["verdict"], "BLOCKED")
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIsNone(outcome["merge_result"])

    def test_p1_unknown_validation_link_status_blocks(self):
        state = base_state()
        validation = next(l for l in state["links"] if l["kind"] == "validation")
        validation["status"] = None
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertIn("validation_link_not_pass", sweep["blockers"])
        self.assertEqual(sweep["verdict"], "BLOCKED")

    def test_p1_missing_required_review_binding_blocks(self):
        # A Review binding absent entirely: the Review condition is
        # unsatisfied, never guessed from the accepted-reviews listing.
        state = base_state()
        state["links"] = [state["links"][0], state["links"][1]]
        state["links"] = [l for l in state["links"] if l["kind"] != "review"]
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertIn("required_link_missing", sweep["blockers"])
        self.assertEqual(sweep["verdict"], "BLOCKED")
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIsNone(outcome["merge_result"])


class R1P1RecordedSweepInventoryTests(unittest.TestCase):
    """P1-02: the merge guard validates the recorded sweep inventory itself;
    a verdict flag is never accepted as proof."""

    def _green_sweep(self):
        adapter = GitHubReadBoundary(base_state())
        return adapter, run_admission_sweep(adapter)

    def test_p1_partial_recorded_sweep_rejected_even_with_green_verdict(self):
        adapter, sweep = self._green_sweep()
        sweep["surfaces"] = sweep["surfaces"][:1]  # misrepresent the sweep
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("recorded_sweep_invalid_restart_sweep", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])
        self.assertFalse(adapter.state["merged"])

    def test_p1_duplicated_surface_record_rejected(self):
        adapter, sweep = self._green_sweep()
        sweep["surfaces"] = [sweep["surfaces"][0], *sweep["surfaces"]]
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("recorded_sweep_invalid_restart_sweep", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])

    def test_p1_incomplete_flag_contradicting_green_verdict_rejected(self):
        adapter, sweep = self._green_sweep()
        sweep["incomplete"] = True  # verdict flag asserts ready anyway
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("recorded_sweep_invalid_restart_sweep", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])

    def test_p1_recorded_blocker_contradicting_green_verdict_rejected(self):
        adapter, sweep = self._green_sweep()
        sweep["blockers"] = ("native_blocked_by_dependency",)
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("recorded_sweep_invalid_restart_sweep", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])


class R1P1ExpectedHeadCasTests(unittest.TestCase):
    """P1-03: the merge mutation is conditional on the exact expected HEAD
    and base/target at the mutation boundary; observable post-final-read
    drift aborts with zero mutation. The uncloseable residual window remains
    only for the other admission surfaces."""

    def test_p1_observable_head_drift_after_final_read_aborts_zero_mutation(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)

        def residual_head_move(s):
            s["head"] = HEAD_0  # observable after the final readback

        outcome = guarded_merge(adapter, sweep, HEAD_1,
                                residual_inject=residual_head_move,
                                residual_visible=True)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("residual_breach_observed_pre_mutation", outcome["routes"])
        self.assertIn("pr_head", outcome["changed_surfaces"])
        self.assertIsNone(outcome["merge_result"])
        self.assertFalse(adapter.state["merged"])

    def test_p1_observable_target_drift_after_final_read_aborts_zero_mutation(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)

        def residual_target_move(s):
            s["base_target"] = BASE_T_NEXT

        outcome = guarded_merge(adapter, sweep, HEAD_1,
                                residual_inject=residual_target_move,
                                residual_visible=True)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("residual_breach_observed_pre_mutation", outcome["routes"])
        self.assertIn("pr_head", outcome["changed_surfaces"])
        self.assertIsNone(outcome["merge_result"])

    def test_p1_head_drift_in_true_gap_is_cas_rejected_zero_mutation(self):
        # The mutation itself is compare-and-swap on the exact expected head:
        # head/target drift is never part of the uncloseable residual gap.
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)

        def gap_head_move(s):
            s["head"] = HEAD_0

        outcome = guarded_merge(adapter, sweep, HEAD_1,
                                residual_inject=gap_head_move,
                                residual_visible=False)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("expected_head_cas_rejected_zero_mutation", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])
        self.assertFalse(adapter.state["merged"])

    def test_p1_base_target_drift_in_true_gap_is_cas_rejected_zero_mutation(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)

        def gap_target_move(s):
            s["base_target"] = BASE_T_NEXT

        outcome = guarded_merge(adapter, sweep, HEAD_1,
                                residual_inject=gap_target_move,
                                residual_visible=False)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("expected_head_cas_rejected_zero_mutation", outcome["routes"])
        self.assertIsNone(outcome["merge_result"])
        self.assertFalse(adapter.state["merged"])


class R1P1PostMergeCompensatingReadbackTests(unittest.TestCase):
    """P1-04: the post-merge compensating audit is a real injected read
    sequence over all required surfaces bound to the integration identity;
    incomplete/UNKNOWN audit reads leave the integration unratified."""

    def test_p1_post_merge_audit_is_real_read_sequence_bound_to_integration(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "MERGED")
        # Three full read passes: recorded sweep, final admission readback,
        # and the post-merge compensating audit — a real read sequence, not
        # an in-memory watermark peek.
        self.assertEqual(len(adapter.reads), 3 * len(SWEEP_SURFACES))
        post_merge_reads = adapter.reads[-len(SWEEP_SURFACES):]
        self.assertEqual(
            [r["surface"] for r in post_merge_reads], list(SWEEP_SURFACES)
        )
        self.assertTrue(outcome["audit"])
        self.assertEqual(
            outcome["audit"]["integration_sha"],
            outcome["merge_result"]["integration_sha"],
        )
        self.assertEqual(
            outcome["audit"]["integration_tree"],
            outcome["merge_result"]["integration_tree"],
        )

    def test_p1_post_merge_missing_page_leaves_integration_unratified(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)

        def gap_fault(s):
            # A page goes missing only after the final admission readback.
            adapter.missing_pages.add("required_checks")

        outcome = guarded_merge(adapter, sweep, HEAD_1,
                                residual_inject=gap_fault,
                                residual_visible=False)
        self.assertEqual(outcome["decision"], "MERGED_UNRATIFIED_RESTART_REQUIRED")
        self.assertIn("post_merge_audit_incomplete_or_unknown", outcome["routes"])
        self.assertIn("required_checks", outcome["audit"]["unread_surfaces"])
        self.assertFalse(outcome["merge_result"]["ratified"])
        self.assertEqual(
            downstream_ready_sets(outcome["merge_result"]), {"T08": "NOT_READY"}
        )

    def test_p1_post_merge_transport_unknown_leaves_integration_unratified(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)

        def gap_fault(s):
            adapter.transport_failures.add("plan_currentness")

        outcome = guarded_merge(adapter, sweep, HEAD_1,
                                residual_inject=gap_fault,
                                residual_visible=False)
        self.assertEqual(outcome["decision"], "MERGED_UNRATIFIED_RESTART_REQUIRED")
        self.assertIn("post_merge_audit_incomplete_or_unknown", outcome["routes"])
        self.assertFalse(outcome["merge_result"]["ratified"])

    def test_p1_unratified_record_is_never_retroactively_pass(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)

        def gap_late_review(s):
            s["reviews"].append(
                review_event("REQUEST_CHANGES", operator="op-reviewer-2",
                             session="sess-reviewer-2", event_id="rev-gap-2")
            )
            s["watermarks"]["accepted_reviews"] += 1

        outcome = guarded_merge(adapter, sweep, HEAD_1,
                                residual_inject=gap_late_review,
                                residual_visible=False)
        unratified = outcome["merge_result"]
        self.assertFalse(unratified["ratified"])
        # A later clean read can never rewrite the recorded integration's
        # ratification: no retroactive PASS.
        recheck = run_admission_sweep(adapter)
        self.assertEqual(
            downstream_ready_sets(unratified), {"T08": "NOT_READY"}
        )
        self.assertIsNot(unratified["ratified"], True)
        self.assertFalse(recheck.get("atomic_snapshot_claim", False))


class R1P2PlatformGenerationTests(unittest.TestCase):
    """P2-01: platform/source generation is distinct from the controller's
    local read sequence; a generation change over unchanged facts and
    watermarks still invalidates, and UNKNOWN generation fails closed."""

    def test_p2_generation_change_with_unchanged_facts_and_watermarks_restarts(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        # Pure platform regeneration: no fact, watermark or head change.
        adapter.state["generation"] += 1
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIn("surface_generation_changed_restart_sweep", outcome["routes"])
        self.assertTrue(outcome["changed_surfaces"])
        self.assertIsNone(outcome["merge_result"])

    def test_p2_unknown_generation_is_never_promoted_to_ready(self):
        adapter = GitHubReadBoundary(
            base_state(), generation_unknown=("task_validation_links",)
        )
        sweep = run_admission_sweep(adapter)
        self.assertEqual(sweep["verdict"], "BLOCKED")
        self.assertIn("surface_read_unknown", sweep["blockers"])
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIsNone(outcome["merge_result"])

    def test_p2_local_read_sequence_is_not_platform_generation(self):
        # Reads themselves never mutate source truth: two consecutive sweeps
        # over an unchanged source both admit, while every read stays
        # individually recorded (local request sequence, not generation).
        adapter = GitHubReadBoundary(base_state())
        generation_before = adapter.state["generation"]
        first = run_admission_sweep(adapter)
        second = run_admission_sweep(adapter)
        self.assertEqual(adapter.state["generation"], generation_before)
        self.assertEqual(first["verdict"], "MERGE_READY")
        self.assertEqual(second["verdict"], "MERGE_READY")
        self.assertNotEqual(
            [r["read_ref"] for r in first["surfaces"]],
            [r["read_ref"] for r in second["surfaces"]],
        )


class R1P2RelevantPermissionsTests(unittest.TestCase):
    """P2-02: relevant merge permissions currentness is a required admission
    surface (frozen Pack §4), consumed read-only from the existing authority
    contract; missing/UNKNOWN fails closed."""

    def test_p2_permission_surface_is_swept_with_read_identity(self):
        adapter = GitHubReadBoundary(base_state())
        sweep = run_admission_sweep(adapter)
        surface_names = [s["surface"] for s in sweep["surfaces"]]
        self.assertIn("relevant_permissions", surface_names)
        record = next(
            s for s in sweep["surfaces"] if s["surface"] == "relevant_permissions"
        )
        self.assertEqual(record["completeness"], "COMPLETE")
        self.assertTrue(record["read_ref"])
        self.assertIsNotNone(record["identity"])

    def test_p2_permission_currentness_unknown_blocks(self):
        state = base_state()
        state["permissions"] = [
            {"permission": "merge", "granted": True, "currentness": "UNKNOWN"}
        ]
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertIn("permission_currentness_unknown", sweep["blockers"])
        self.assertEqual(sweep["verdict"], "BLOCKED")
        outcome = guarded_merge(adapter, sweep, HEAD_1)
        self.assertEqual(outcome["decision"], "BLOCKED")
        self.assertIsNone(outcome["merge_result"])

    def test_p2_required_permission_missing_blocks(self):
        state = base_state()
        state["permissions"] = []
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertIn("required_permission_missing", sweep["blockers"])
        self.assertEqual(sweep["verdict"], "BLOCKED")

    def test_p2_permission_not_granted_blocks(self):
        state = base_state()
        state["permissions"] = [
            {"permission": "merge", "granted": False, "currentness": "CURRENT"}
        ]
        adapter = GitHubReadBoundary(state)
        sweep = run_admission_sweep(adapter)
        self.assertIn("permission_not_granted", sweep["blockers"])
        self.assertEqual(sweep["verdict"], "BLOCKED")


class NoShadowCentralProjectionTests(unittest.TestCase):
    """Real-tree half: no LAST_ADMISSION_SWEEP projection outside the owner
    section. (Pre-T11 integration state; T11's own landing owns the central
    wiring and its conformance.)"""

    def test_manifest_carries_no_merge_admission_projection(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        shadowed = [k for k in recursive_keys(manifest) if "admission_sweep" in str(k).lower()]
        self.assertEqual(shadowed, [])

    def test_no_merge_admission_schema_file_exists(self):
        schemas = ROOT / "schemas"
        shadowed = [p.name for p in schemas.glob("*") if "admission" in p.name.lower()]
        self.assertEqual(shadowed, [])

    def test_no_sweep_projection_in_templates(self):
        shadowed = []
        for path in (ROOT / "templates").rglob("*"):
            if path.is_file() and "LAST_ADMISSION_SWEEP" in path.read_text(
                encoding="utf-8", errors="replace"
            ):
                shadowed.append(str(path.relative_to(ROOT)))
        self.assertEqual(shadowed, [])

    def test_common_suite_proposal_routes_to_t11_unwritten(self):
        # R2-F07: any proposal to extend the shared Execution Architecture
        # suite routes to T11; this Builder never edits that file (its blob
        # equality is asserted in Section14PlacementTests).
        proposal = {"target": "scripts/test_execution_architecture.py", "written": False}
        self.assertFalse(proposal["written"])
        self.assertEqual(proposal["target"], READ_ONLY_PATHS[1])


if __name__ == "__main__":
    unittest.main()
