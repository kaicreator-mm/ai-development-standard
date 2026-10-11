"""V411-T01 focused test: pinned effective-rule trace resolution.

Encodes the V411-T01 Task Pack §3 oracles (P01-P04, N01-N06) as deterministic
offline checks in two layers:

1. Section-scoped textual contracts binding the decision model to the
   owner-local normative clauses this task adds to
   `standards/PROJECT_ADOPTION.md` (§2.2, §3.4, §3.7) and
   `standards/DEVELOPMENT_WORKFLOW.md` (§4 Effective-rule trace subsection).
2. Fixture-driven decision assertions over a pure, in-test resolution model
   that encodes the Task Pack §4 contract: precedence within concern, then
   cross-owner AND; A0-A4 non-weakening; job-label-set closure plus
   independently inspected material facts; UNKNOWN/CONFLICT fail-closed;
   the minimal `EFFECTIVE_RULE_TRACE` projection.

Purely textual + in-memory; no network, no runtime, no shared verifier.

Review #1032 repairs (fail-closed hardening): positive aggregate admission
requires every applicable required gate to be satisfied by current trusted
owner proof (missing/FAIL/stale proofs yield UNVERIFIED_GATES / REJECTED_GATES,
never a false-green ADMITTED); every covered job class resolves through an
explicit owner-obligation mapping while unknown labels fail closed as
UNVERIFIED_COVERAGE; each trace binds the real owning proof ref/currentness so
the projection stays falsifiable.

Review #1041 R2 bounded repairs (fail-closed hardening, this revision):
an owner NOT_APPLICABLE verdict is admissible only for a dimension
independently observed ABSENT within authorized scope that no other owner or
declared job label demands — anywhere else it contradicts the inspected facts
and the aggregate CONFLICTs/DENies (never silently N/A); the applicable
canonical authority reference set must be complete with exact immutable pins
(a missing member, a non-canonical tier, or an "unresolved" owner blob can
never be current or pass); blank/malformed/misbound/wrong-subject/stale proof
refs are untrusted evidence and fail closed as NOT_RUN/UNKNOWN (never
CURRENT); and the centralized effective-rule projection / real owner-contract
integration oracle is DEFERRED_TO_T11 and explicitly NOT_RUN — this task-local
model is a decision oracle fixture, not the owner contract executor, and no
owner-contract PASS completeness is claimed here.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# contract vocabulary (Task Pack §4; existing gate enum is preserved)
# ---------------------------------------------------------------------------

PINNED_STANDARD_REVISION = "70678e8dae547ec41429970e8473650bce9ab621"

AUTHORITY_TIERS = (
    "FROZEN_PRD_CONTRACT",
    "FROZEN_ARCHITECTURE",
    "PROJECT_OVERRIDES",
    "TASK_ACCEPTANCE",
    "STANDARD_DEFAULTS",
)

CANONICAL_GATE_STATES = {"PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE"}
EPISTEMIC_STATES = {"PRESENT", "ABSENT_WITH_INSPECTED_SCOPE", "UNKNOWN"}
RESOLUTION_VOCABULARY = {
    "ADMITTED",
    "CONFLICT",
    "UNKNOWN_EPISTEMIC",
    "REJECTED_CURRENTNESS",
    "UNVERIFIED_COVERAGE",
    # Review #1032 R01: positive aggregate admission additionally requires
    # every applicable required gate to be satisfied by current trusted proof.
    "UNVERIFIED_GATES",
    "REJECTED_GATES",
}
MATERIAL_DIMENSIONS = ("permission", "security", "migration", "deploy", "external_effect")
WEAKENING_VALUES = {"not-required", "skip", "not_applicable"}

# Minimal EFFECTIVE_RULE_TRACE projection (Task Pack §4).
TRACE_FIELDS = {
    "standard_revision",
    "owner_ref_blob",
    "authority_tier_ref",
    "exact_subject",
    "adoption",
    "archetype",
    "actor_role",
    "declared_jobs",
    "observed_fact_ref",
    "owner_proof_ref",
    "applicability_reason",
    "obligation",
    "required_evidence_currentness",
    "resolution",
    "decision_owner_ref",
}

JOB_OBLIGATIONS = {
    "J02_DOCS_LOW_RISK": "affected docs checks",
    "J03_BUG_FIX": "baseline repair verification",
    # Review #1032 R02: job classes declared as covered (X02/X05) MUST carry an
    # owner-obligation mapping; a declared-but-unmapped job is a fail-closed
    # UNVERIFIED_COVERAGE route, never a KeyError.
    "J04_FEATURE_CONTRACT": "feature contract conformance evidence",
    "J05_PUBLIC_API_CHANGE": "public API change compatibility evidence",
    "J06_PERSISTENT_DATA_MIGRATION": "migration baseline/target state and interrupted recovery evidence",
    "J07_SECURITY_VULNERABILITY": "independent security review",
    "J08_EXTERNAL_WRITE_DEPLOY": "deployment side-effect authorization and idempotency reconciliation",
    "J09_RELEASE_QUALIFICATION": "exact release candidate with visible/hidden/release-qualification evidence",
    "J10_INCIDENT_RECOVERY": "incident target permission and recovery/compensation evidence",
    "J11_DEPRECATION_RETIREMENT": "deprecation window and consumer impact evidence",
    "J12_UPSTREAM_REUSE": "upstream license/provenance/currentness evidence",
}

# Obligations derived from inspected material facts stay bound to their owner
# even when the matching job label is removed from the declared set.
DIMENSION_OBLIGATIONS = {
    "permission": "authorized actor/permission evidence",
    "security": "independent security review",
    "migration": "migration baseline/target state and interrupted recovery evidence",
    "deploy": "deployment side-effect authorization and idempotency reconciliation",
    "external_effect": "external-effect reconciliation evidence",
}

OBLIGATION_OWNERS = {
    "affected docs checks": ("task acceptance owner", "TASK_ACCEPTANCE"),
    "baseline repair verification": ("task acceptance owner", "TASK_ACCEPTANCE"),
    "independent security review": ("independent security review authority", "FROZEN_PRD_CONTRACT"),
    "pinned standard currentness verification": ("standard pin resolution owner", "STANDARD_DEFAULTS"),
    "migration baseline/target state and interrupted recovery evidence": (
        "data migration owner",
        "FROZEN_ARCHITECTURE",
    ),
    "deployment side-effect authorization and idempotency reconciliation": (
        "deploy authorization owner",
        "FROZEN_ARCHITECTURE",
    ),
    "authorized actor/permission evidence": ("project ownership authority", "PROJECT_OVERRIDES"),
    "feature contract conformance evidence": ("interface compatibility owner", "FROZEN_ARCHITECTURE"),
    "public API change compatibility evidence": ("interface compatibility owner", "FROZEN_ARCHITECTURE"),
    "external-effect reconciliation evidence": ("integration owner", "FROZEN_ARCHITECTURE"),
    "exact release candidate with visible/hidden/release-qualification evidence": (
        "release/integration controller",
        "FROZEN_ARCHITECTURE",
    ),
    "incident target permission and recovery/compensation evidence": (
        "incident owner",
        "FROZEN_ARCHITECTURE",
    ),
    "deprecation window and consumer impact evidence": (
        "interface compatibility owner",
        "FROZEN_ARCHITECTURE",
    ),
    "upstream license/provenance/currentness evidence": (
        "dependency governance owner",
        "FROZEN_ARCHITECTURE",
    ),
}

# Representative mandatory intersections (v4.11 PRD §2.3, X01-X08). Coverage is
# judged against declared job-label sets; unlisted combinations stay
# UNVERIFIED instead of silently passing.
COVERED_JOB_CLASSES = {
    frozenset({"J03_BUG_FIX", "J06_PERSISTENT_DATA_MIGRATION", "J07_SECURITY_VULNERABILITY", "J08_EXTERNAL_WRITE_DEPLOY"}): "X01",
    frozenset({"J04_FEATURE_CONTRACT", "J05_PUBLIC_API_CHANGE"}): "X05",
    frozenset({"J05_PUBLIC_API_CHANGE", "J12_UPSTREAM_REUSE"}): "X02",
    frozenset({"J06_PERSISTENT_DATA_MIGRATION", "J08_EXTERNAL_WRITE_DEPLOY", "J10_INCIDENT_RECOVERY"}): "X03",
    frozenset({"J07_SECURITY_VULNERABILITY", "J09_RELEASE_QUALIFICATION"}): "X04",
    frozenset({"J08_EXTERNAL_WRITE_DEPLOY", "J09_RELEASE_QUALIFICATION"}): "X07",
    frozenset({"J02_DOCS_LOW_RISK", "J03_BUG_FIX"}): "X08",
    frozenset({"J11_DEPRECATION_RETIREMENT", "J12_UPSTREAM_REUSE"}): "X06",
}

OWNER_BLOBS = {
    "FROZEN_PRD_CONTRACT": "b" * 40,
    "FROZEN_ARCHITECTURE": "c" * 40,
    "PROJECT_OVERRIDES": "d" * 40,
    "TASK_ACCEPTANCE": "e" * 40,
}

X01_JOBS = frozenset(
    {"J03_BUG_FIX", "J06_PERSISTENT_DATA_MIGRATION", "J07_SECURITY_VULNERABILITY", "J08_EXTERNAL_WRITE_DEPLOY"}
)


# ---------------------------------------------------------------------------
# section extraction (headings are the section identity; tests slice by them)
# ---------------------------------------------------------------------------

def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def adoption() -> str:
    return read("standards/PROJECT_ADOPTION.md")


def workflow() -> str:
    return read("standards/DEVELOPMENT_WORKFLOW.md")


def section_between(text: str, start_heading: str, end_heading: str) -> str:
    start = text.index(start_heading)
    end = text.index(end_heading, start + len(start_heading))
    return text[start:end]


def adoption_section(start_heading: str, end_heading: str) -> str:
    return section_between(adoption(), start_heading, end_heading)


def gate_authority_section() -> str:
    return section_between(workflow(), "## 4. Gate Authority", "## 5. Blocker Propagation")


def gate_subsection(heading: str) -> str:
    section = gate_authority_section()
    start = section.index(heading)
    rest = section[start + len(heading) :]
    next_heading = rest.find("\n### ")
    return rest if next_heading == -1 else rest[:next_heading]


def trace_subsection() -> str:
    return gate_subsection("### Effective-rule trace：pinned revision、跨 owner 合取与 provenance")


# ---------------------------------------------------------------------------
# deterministic in-test resolution model (Task Pack §4 contract; oracle only,
# not a production rules engine and not a shared verifier)
# ---------------------------------------------------------------------------

def proof(
    verdict: str = "PASS",
    ref: str = "",
    fresh: bool = True,
    subject: str | None = None,
) -> dict:
    entry = {"verdict": verdict, "ref": ref or f"proof:{verdict.lower()}@707f", "fresh": fresh}
    if subject is not None:
        entry["subject"] = subject
    return entry


# Review #1041 F04: a trusted owner proof ref must be a non-blank, well-formed
# "source:identity@immutable-blob" pointer; blank or malformed refs (wrong
# source shape, missing/empty blob) are not evidence and fail closed.
PROOF_REF_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*:[A-Za-z0-9._/-]+@[0-9a-f]{4,40}$")


def proof_ref_defect(owner_proof: dict, subject: str) -> str:
    """Return a rejection reason when a proof ref is not trusted evidence.

    Blank refs, malformed refs, and refs bound to a different exact subject
    are untrusted; the caller fails the gate closed instead of binding CURRENT.
    """
    ref = owner_proof.get("ref")
    if not isinstance(ref, str) or not ref.strip():
        return "blank proof ref is not trusted evidence"
    if not PROOF_REF_PATTERN.match(ref):
        return f"malformed proof ref {ref!r}: expected 'source:identity@immutable-blob'"
    bound_subject = owner_proof.get("subject")
    if bound_subject is not None and bound_subject != subject:
        return f"proof ref {ref!r} is bound to subject {bound_subject!r}, not {subject!r}"
    return ""


def all_pass_proofs() -> dict:
    # Review #1032 R03: proof refs are contract-derived and per-obligation, so a
    # trace can be falsified back to the exact owning evidence it claims.
    obligations = set(DIMENSION_OBLIGATIONS.values()) | set(JOB_OBLIGATIONS.values())
    return {
        obligation: proof(ref=f"proof:{re.sub(r'[^a-z0-9]+', '-', obligation).strip('-')}@707f")
        for obligation in sorted(obligations)
    }


def service_x01_fixture(**overrides) -> dict:
    fixture = {
        "exact_subject": "svc/orders@task/fix-compound",
        "standard_revision": PINNED_STANDARD_REVISION,
        "authority_refs": {
            tier: f"{path}@{OWNER_BLOBS[tier]}"
            for tier, path in (
                ("FROZEN_PRD_CONTRACT", "docs/prd.md#freeze"),
                ("FROZEN_ARCHITECTURE", "docs/l2.md#freeze"),
                ("PROJECT_OVERRIDES", ".dev-standard/PROJECT_OVERRIDES.md"),
                ("TASK_ACCEPTANCE", "issues/1007"),
            )
        },
        "adoption": "A0_COMPATIBILITY",
        "archetype": "SERVICE",
        "condition": "BROWNFIELD",
        "actor_role": "BUILDER",
        "declared_jobs": set(X01_JOBS),
        "observations": {
            dimension: {"state": "PRESENT", "ref": f"obs:{dimension}@707a", "fresh": True}
            for dimension in MATERIAL_DIMENSIONS
        },
        "owner_proofs": {},
        "overrides": [],
    }
    fixture.update(overrides)
    return fixture


def cli_docs_fixture(**overrides) -> dict:
    fixture = service_x01_fixture(
        exact_subject="cli/tools@task/docs-only",
        adoption="A0_COMPATIBILITY",
        archetype="CLI",
        condition="NEW",
        declared_jobs={"J02_DOCS_LOW_RISK"},
        observations={
            dimension: {
                "state": "ABSENT_WITH_INSPECTED_SCOPE",
                "ref": f"inventory:{dimension}@707b",
                "fresh": True,
            }
            for dimension in MATERIAL_DIMENSIONS
        },
        owner_proofs={"affected docs checks": proof(ref="proof:docs@707b")},
    )
    fixture.update(overrides)
    return fixture


def resolve_effective_rules(fixture: dict) -> dict:
    """Resolve owner-scoped effective rules for one exact subject.

    Encodes Task Pack §4: currentness first, epistemic facts second,
    job-set + fact closure third, precedence-within-concern then cross-owner
    AND, proportionality by only emitting actually applicable obligations.
    """
    subject = fixture["exact_subject"]
    declared_jobs = tuple(sorted(fixture["declared_jobs"]))
    rules: list[dict] = []
    by_obligation: dict[str, dict] = {}

    def emit(obligation: str, epistemic: str, observed_ref: str, reason: str) -> None:
        if obligation in by_obligation:
            return
        owner, tier = OBLIGATION_OWNERS[obligation]
        evidence_currentness = "CURRENT" if epistemic != "UNKNOWN" else "UNKNOWN"
        rule = {
            "owner": owner,
            "tier": tier,
            "obligation": obligation,
            "epistemic": epistemic,
            "gate_state": "NOT_RUN",
            "trace": {
                "standard_revision": fixture["standard_revision"],
                "owner_ref_blob": fixture["authority_refs"].get(tier, "unresolved"),
                "authority_tier_ref": tier,
                "exact_subject": subject,
                "adoption": fixture["adoption"],
                "archetype": fixture["archetype"],
                "actor_role": fixture["actor_role"],
                "declared_jobs": declared_jobs,
                "observed_fact_ref": observed_ref,
                # Review #1032 R03: the owning proof identity is bound by the
                # proof-resolution pass below, never inferred from epistemic
                # state alone; "NONE" until a real current proof is found.
                "owner_proof_ref": "NONE",
                "applicability_reason": reason,
                "obligation": obligation,
                # Provisional only; step 4 re-binds this from the actual owner
                # proof so a missing proof can never project CURRENT.
                "required_evidence_currentness": evidence_currentness,
                "resolution": "",
                "decision_owner_ref": f"{owner}@{fixture['authority_refs'].get(tier, 'unresolved')}",
            },
        }
        rules.append(rule)
        by_obligation[obligation] = rule

    # 1. Currentness: one immutable pin, the complete applicable canonical
    #    authority reference set with exact immutable pins, exact subject.
    #    Review #1041 F03: omitting tiers a fixture cannot defend is not a
    #    pass — the canonical owner/authority set is required in full, a
    #    non-canonical tier is rejected, and an "unresolved" owner blob can
    #    never count as current.
    currentness_failure = ""
    if fixture["standard_revision"] != PINNED_STANDARD_REVISION:
        currentness_failure = "standard revision is not the single pinned immutable revision"
    elif not subject:
        currentness_failure = "exact subject identity missing"
    else:
        refs = fixture["authority_refs"]
        missing_tiers = sorted(tier for tier in OWNER_BLOBS if tier not in refs)
        noncanonical_tiers = sorted(tier for tier in refs if tier not in OWNER_BLOBS)
        if missing_tiers or noncanonical_tiers:
            currentness_failure = (
                "incomplete/non-canonical authority reference set (missing: "
                + (", ".join(missing_tiers) or "none")
                + "; non-canonical: "
                + (", ".join(noncanonical_tiers) or "none")
                + ")"
            )
        else:
            for tier, authority_ref in refs.items():
                expected = OWNER_BLOBS.get(tier)
                if expected is None or not authority_ref.endswith(f"@{expected}"):
                    currentness_failure = f"owner blob mismatch for {tier}"
                    break
    if currentness_failure:
        emit(
            "pinned standard currentness verification",
            "UNKNOWN",
            "NONE",
            f"currentness rejected: {currentness_failure}; no authority is inferred",
        )
        for rule in rules:
            rule["gate_state"] = "BLOCKED"
            rule["trace"]["resolution"] = "REJECTED_CURRENTNESS"
        return {"resolution": "REJECTED_CURRENTNESS", "rules": rules, "conflict": False}

    # 2. Epistemic facts: PRESENT / ABSENT_WITH_INSPECTED_SCOPE / UNKNOWN.
    for dimension in MATERIAL_DIMENSIONS:
        obligation = DIMENSION_OBLIGATIONS[dimension]
        observation = fixture["observations"].get(dimension)
        if observation is None or not observation.get("fresh") or observation["state"] == "UNKNOWN":
            emit(
                obligation,
                "UNKNOWN",
                "NONE" if observation is None else observation.get("ref", "NONE"),
                "material dimension uninspected or observation stale/missing; fail closed as UNKNOWN",
            )
        elif observation["state"] == "ABSENT_WITH_INSPECTED_SCOPE":
            emit(
                obligation,
                "ABSENT_WITH_INSPECTED_SCOPE",
                observation["ref"],
                "inspected nonmaterial within declared scope; only the owning authority may record N/A",
            )
        else:
            emit(
                obligation,
                "PRESENT",
                observation["ref"],
                "material fact independently inspected; obligation is label-independent",
            )

    # 3. Declared job-label set closure (labels are aids, never waivers).
    # Review #1032 R02: a declared job label with no owner-obligation mapping
    # fails closed as UNVERIFIED_COVERAGE routing, never a bare KeyError.
    unknown_job_labels = [job for job in declared_jobs if job not in JOB_OBLIGATIONS]
    for job in declared_jobs:
        obligation = JOB_OBLIGATIONS.get(job)
        if obligation is None:
            continue
        emit(obligation, "PRESENT", "NONE", "obligation derived from declared job-label set")

    # 4. Owner proofs; UNKNOWN epistemic state can never become PASS.
    # Review #1032 R03: currentness is bound to the real owning proof here —
    # a missing or stale proof projects UNKNOWN with owner_proof_ref "NONE",
    # never CURRENT, and only a fresh PASS proof binds CURRENT + the proof ref.
    # Review #1041 F02: an owner NOT_APPLICABLE verdict is admissible only for
    # a dimension independently observed ABSENT within authorized scope that
    # no other owner or declared label demands; against an inspected PRESENT
    # fact it is a contradiction and the aggregate must DENY. F04: blank/
    # malformed/misbound/wrong-subject proof refs are untrusted and fail
    # closed as NOT_RUN/UNKNOWN, never CURRENT.
    conflict = False
    label_demanded_obligations = {
        JOB_OBLIGATIONS[job] for job in declared_jobs if job in JOB_OBLIGATIONS
    }
    ref_owners: dict[str, set[str]] = {}
    for rule in rules:
        owner_proof = fixture["owner_proofs"].get(rule["obligation"])
        if (
            owner_proof is not None
            and owner_proof.get("fresh")
            and isinstance(owner_proof.get("ref"), str)
        ):
            ref_owners.setdefault(owner_proof["ref"], set()).add(rule["obligation"])
    for rule in rules:
        obligation = rule["obligation"]
        state = rule["epistemic"]
        if state == "ABSENT_WITH_INSPECTED_SCOPE":
            if obligation in label_demanded_obligations:
                # F02(b): a declared job label demands this gate while the
                # dimension is claimed inspected-ABSENT — the contradiction
                # fails closed instead of minting an N/A.
                conflict = True
                rule["gate_state"] = "BLOCKED"
                rule["trace"]["applicability_reason"] += (
                    "; declared job label demands this gate while the dimension is claimed "
                    "ABSENT_WITH_INSPECTED_SCOPE: contradiction fails closed, N/A denied"
                )
                continue
            rule["gate_state"] = "NOT_APPLICABLE"
            rule["trace"]["required_evidence_currentness"] = "NOT_REQUIRED"
            continue
        owner_proof = fixture["owner_proofs"].get(obligation)
        if state == "UNKNOWN" or owner_proof is None or not owner_proof["fresh"]:
            rule["gate_state"] = "NOT_RUN"
            rule["trace"]["owner_proof_ref"] = "NONE" if owner_proof is None else owner_proof["ref"]
            rule["trace"]["required_evidence_currentness"] = "UNKNOWN"
            if owner_proof is not None and not owner_proof["fresh"]:
                rule["trace"]["applicability_reason"] += "; earlier assessment is from a stale HEAD and stays UNKNOWN"
            continue
        # F04: only a non-blank, well-formed, subject-bound, uniquely bound
        # proof ref is trusted evidence; anything else fails closed.
        ref_defect = proof_ref_defect(owner_proof, subject)
        if not ref_defect and len(ref_owners.get(owner_proof["ref"], ())) > 1:
            other = sorted(ref_owners[owner_proof["ref"]] - {obligation})
            ref_defect = (
                f"proof ref {owner_proof['ref']!r} is misbound: already bound to "
                + ", ".join(repr(item) for item in other)
                + " and cannot prove this obligation too"
            )
        if ref_defect:
            rule["gate_state"] = "NOT_RUN"
            rule["trace"]["owner_proof_ref"] = owner_proof["ref"]
            rule["trace"]["required_evidence_currentness"] = "UNKNOWN"
            rule["trace"]["applicability_reason"] += f"; untrusted proof ref rejected ({ref_defect})"
            continue
        rule["trace"]["owner_proof_ref"] = owner_proof["ref"]
        if owner_proof["verdict"] == "PASS":
            rule["gate_state"] = "PASS"
            rule["trace"]["required_evidence_currentness"] = "CURRENT"
        elif owner_proof["verdict"] in {"FAIL", "CHANGES_REQUESTED"}:
            rule["gate_state"] = "FAIL"
            rule["trace"]["required_evidence_currentness"] = "CURRENT"
        elif owner_proof["verdict"] == "NOT_APPLICABLE":
            # F02(a): a rule only reaches the verdict path on independent
            # PRESENT inspection (UNKNOWN continues earlier), so an owner N/A
            # verdict contradicts the inspected fact — aggregate must DENY.
            conflict = True
            rule["gate_state"] = "BLOCKED"
            rule["trace"]["required_evidence_currentness"] = "UNKNOWN"
            rule["trace"]["applicability_reason"] += (
                "; owner NOT_APPLICABLE proof contradicts the independently inspected "
                "PRESENT fact: aggregate must DENY, N/A not admissible"
            )
        else:
            rule["gate_state"] = "BLOCKED"
            rule["trace"]["required_evidence_currentness"] = "UNKNOWN"

    # 5. Precedence within concern: lower authority cannot weaken a higher
    #    owner's gate; contradiction is a CONFLICT, never a silent downgrade.
    for override in fixture["overrides"]:
        rule = by_obligation.get(override["obligation"])
        if rule is None or override["value"] not in WEAKENING_VALUES:
            continue
        if AUTHORITY_TIERS.index(rule["tier"]) < AUTHORITY_TIERS.index(override["tier"]):
            conflict = True
            rule["gate_state"] = "BLOCKED"
            rule["trace"]["applicability_reason"] += (
                "; lower-authority override denied, affected gate stays BLOCKED/NOT_RUN"
            )
        else:
            rule["gate_state"] = "NOT_APPLICABLE"

    # 6. Finite coverage denominator: compound job sets without an equivalent
    #    covered class stay UNVERIFIED with a repair route, never blanket PASS;
    #    declared labels with no owner-obligation mapping fail closed the same way.
    coverage_unverified = bool(unknown_job_labels) or (
        len(declared_jobs) >= 2 and frozenset(declared_jobs) not in COVERED_JOB_CLASSES
    )
    if coverage_unverified:
        for rule in rules:
            if rule["epistemic"] != "ABSENT_WITH_INSPECTED_SCOPE":
                rule["gate_state"] = "BLOCKED"
                if unknown_job_labels:
                    rule["trace"]["applicability_reason"] += (
                        "; unknown job label(s) "
                        + ", ".join(sorted(unknown_job_labels))
                        + ": route to owning authority for an owner-obligation mapping, "
                        "an equivalence class, or an authorized scope exclusion"
                    )
                else:
                    rule["trace"]["applicability_reason"] += (
                        "; uncovered job conjunction: route to owning authority for an "
                        "equivalence class or an authorized scope exclusion"
                    )

    # 7. Cross-owner AND: overall admission requires every owner rule satisfied.
    # Review #1032 R01: ADMITTED only when every applicable required gate is
    # explicitly satisfied (PASS or NOT_APPLICABLE) by current trusted proof;
    # missing/stale proofs (NOT_RUN) and FAIL proofs block the aggregate.
    if conflict:
        resolution = "CONFLICT"
    elif any(rule["epistemic"] == "UNKNOWN" for rule in rules):
        resolution = "UNKNOWN_EPISTEMIC"
    elif coverage_unverified:
        resolution = "UNVERIFIED_COVERAGE"
    elif any(rule["gate_state"] == "FAIL" for rule in rules):
        resolution = "REJECTED_GATES"
    elif any(rule["gate_state"] not in {"PASS", "NOT_APPLICABLE"} for rule in rules):
        resolution = "UNVERIFIED_GATES"
    else:
        resolution = "ADMITTED"
    for rule in rules:
        rule["trace"]["resolution"] = resolution
    return {"resolution": resolution, "rules": rules, "conflict": conflict}


def gate_map(result: dict) -> dict:
    return {rule["obligation"]: rule["gate_state"] for rule in result["rules"]}


def rule_for(result: dict, obligation: str) -> dict:
    return next(rule for rule in result["rules"] if rule["obligation"] == obligation)


# ---------------------------------------------------------------------------
# textual contracts: the decision model is bound to these owner clauses
# ---------------------------------------------------------------------------

class AdoptionStandardContractTests(unittest.TestCase):
    """PROJECT_ADOPTION.md owner clauses added by V411-T01."""

    def test_s22_binds_a0_a4_to_the_same_hard_predicates(self) -> None:
        """Pack P02/N01 grounding: adoption level never changes hard predicates."""
        section = adoption_section(
            "### 2.2 v4 Progressive Adoption（A0–A4）",
            "### 2.3 v3.4 → v4 Compatibility",
        )
        self.assertIn("Effective-rule 解析与 adoption level 解耦", section)
        self.assertIn("A0–A4 任一级 MUST 解析出同一组 required gate 与 hard predicates", section)
        self.assertIn("只选择 evidence 的收集与记录机制", section)
        self.assertIn("MUST NOT 削弱其它 owner 已要求的 gate", section)
        self.assertIn("不得记为已检视的 `ABSENT_WITH_INSPECTED_SCOPE`", section)

    def test_s34_binds_cross_owner_and_and_fail_closed(self) -> None:
        """Pack N03/N04 grounding: AND across owners; UNKNOWN/CONFLICT fail closed."""
        section = adoption_section(
            "### 3.4 Required Gate Authority",
            "### 3.5 Required-but-unestablished command / runner",
        )
        self.assertIn("先在同一 concern 内按上述 precedence 解析 strengthening/narrowing", section)
        self.assertIn("跨所有 applicable owner/concern 取逻辑 AND", section)
        self.assertIn("不解除其它 owner 的 gate", section)
        self.assertIn("不得静默取最低公分母", section)
        self.assertIn("不得以风险 label 单独豁免", section)

    def test_s37_binds_job_set_closure_and_epistemic_states(self) -> None:
        """Pack N01/N03/N05 grounding: multi-label closure, CONFLICT, epistemic trio."""
        section = adoption_section(
            "### 3.7 v4 Override Surface",
            "### 3.8 v4.5 独立适用性：runtime / incident / maintenance",
        )
        self.assertIn("job label 是 multi-label set", section)
        self.assertIn("MUST NOT 因删除某个 label 而解除已检视事实对应的义务", section)
        self.assertIn("与更高 authority 矛盾时为 `CONFLICT`", section)
        self.assertIn("`PRESENT` / `ABSENT_WITH_INSPECTED_SCOPE` / `UNKNOWN`", section)
        self.assertIn("observation 缺失或来自过期 HEAD 为 `UNKNOWN`", section)
        self.assertIn("不是新增 gate 枚举", section)


class WorkflowEffectiveRuleTraceContractTests(unittest.TestCase):
    """DEVELOPMENT_WORKFLOW.md §4 Effective-rule trace subsection."""

    def test_trace_projection_fields_are_bound_verbatim(self) -> None:
        """Pack P01 grounding: the minimal trace projection exists with all fields."""
        subsection = trace_subsection()
        self.assertIn("`EFFECTIVE_RULE_TRACE`", subsection)
        for field in (
            "standard_revision",
            "owner_ref/blob",
            "exact_subject",
            "adoption / archetype / actor_role",
            "declared_jobs",
            "observed_fact / observation ref / freshness",
            "applicability_reason",
            "obligation / required_evidence / freshness",
            "resolution",
            "decision_owner / ref",
        ):
            with self.subTest(field=field):
                self.assertIn(field, subsection)

    def test_precedence_then_cross_owner_and_is_normative(self) -> None:
        """Pack P03/N04 grounding: within-concern precedence, then owner AND."""
        subsection = trace_subsection()
        self.assertIn("先在同一 concern 内按本节 authority chain 解析 precedence", subsection)
        self.assertIn("禁止削弱", subsection)
        self.assertIn("跨所有 applicable owner/concern 取逻辑 AND", subsection)
        self.assertIn("任一 owner 的 required gate 在合取中保持 required", subsection)

    def test_label_removal_cannot_remove_fact_derived_obligations(self) -> None:
        """Pack N01 grounding: inspected facts keep their obligations."""
        subsection = trace_subsection()
        self.assertIn("只是 applicability 的辅助证据", subsection)
        self.assertIn("义务不因删除 label 而消失", subsection)
        self.assertIn("适用性 UNKNOWN 或矛盾时按上一节 fail closed", subsection)

    def test_unknown_fail_closed_and_epistemic_states_are_not_gate_enum(self) -> None:
        """Pack N03 grounding: UNKNOWN never PASS; trio is epistemic, not enum."""
        subsection = trace_subsection()
        self.assertIn("事实记为 `UNKNOWN`", subsection)
        self.assertIn("MUST NOT 记为已检视的 `ABSENT_WITH_INSPECTED_SCOPE`", subsection)
        self.assertIn("MUST NOT 产生 `PASS`", subsection)
        self.assertIn("epistemic fact，不是新增 gate state", subsection)
        self.assertIn("`NOT_RUN` / `BLOCKED`", subsection)

    def test_no_second_methodology_or_new_gate_state_is_introduced(self) -> None:
        """Pack non-goals: no new enum, no shared schema authored here."""
        section = gate_authority_section()
        subsection = trace_subsection()
        self.assertIn("不新增 gate state、workflow state、共享 schema、模板或第二套方法论", subsection)
        gate_states = set(re.findall(r"`(PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE)`", subsection))
        self.assertTrue(gate_states)
        self.assertTrue(gate_states <= CANONICAL_GATE_STATES, gate_states - CANONICAL_GATE_STATES)
        # Review-finding/currentness vocabulary stays with its own owners.
        for owned_term in ("severity", "currentness", "aggregation"):
            with self.subTest(owned_term=owned_term):
                self.assertNotIn(owned_term, section)


# ---------------------------------------------------------------------------
# fixture-driven decision oracles (Task Pack §3 cases)
# ---------------------------------------------------------------------------

class PinnedTraceResolutionTests(unittest.TestCase):
    def test_p01_exact_pin_retains_trace_identity_and_single_methodology(self) -> None:
        """Pack P01: pin/owner/subject/observation/proof refs resolve and persist."""
        fixture = service_x01_fixture(owner_proofs=all_pass_proofs())
        result = resolve_effective_rules(fixture)
        self.assertEqual(result["resolution"], "ADMITTED")
        self.assertTrue(result["rules"])
        revisions = {rule["trace"]["standard_revision"] for rule in result["rules"]}
        self.assertEqual(revisions, {PINNED_STANDARD_REVISION})
        tiers = {rule["trace"]["authority_tier_ref"] for rule in result["rules"]}
        self.assertTrue(tiers <= set(AUTHORITY_TIERS), tiers - set(AUTHORITY_TIERS))
        for rule in result["rules"]:
            trace = rule["trace"]
            with self.subTest(obligation=rule["obligation"]):
                self.assertEqual(trace["exact_subject"], fixture["exact_subject"])
                self.assertTrue(trace["owner_ref_blob"].split("@")[-1], trace["owner_ref_blob"])
                self.assertEqual(trace["required_evidence_currentness"], "CURRENT")

    def test_n05_mixed_pin_wrong_blob_or_missing_subject_rejects_currentness(self) -> None:
        """Pack N05: currentness rejected; no inferred authority, no PASS."""
        cases = {
            "mixed_pin": {"standard_revision": "main@latest"},
            "wrong_owner_blob": {
                "authority_refs": dict(
                    service_x01_fixture()["authority_refs"],
                    FROZEN_PRD_CONTRACT=f"docs/prd.md#freeze@{'9' * 40}",
                ),
            },
            "missing_subject": {"exact_subject": ""},
        }
        for name, overrides in cases.items():
            with self.subTest(case=name):
                result = resolve_effective_rules(service_x01_fixture(**overrides))
                self.assertEqual(result["resolution"], "REJECTED_CURRENTNESS")
                states = set(gate_map(result).values())
                self.assertEqual(states, {"BLOCKED"})
                for rule in result["rules"]:
                    self.assertIn("no authority is inferred", rule["trace"]["applicability_reason"])


class AdoptionNonWeakeningTests(unittest.TestCase):
    def test_p02_a0_and_a4_resolve_identical_gates(self) -> None:
        """Pack P02: same facts under A0 and A4 demand the same hard predicates."""
        base = service_x01_fixture()
        a0 = resolve_effective_rules(base)
        a4 = resolve_effective_rules(service_x01_fixture(adoption="A4_FULL_ORCHESTRATION"))
        self.assertEqual(gate_map(a0), gate_map(a4))
        self.assertEqual(
            [(rule["obligation"], rule["owner"]) for rule in a0["rules"]],
            [(rule["obligation"], rule["owner"]) for rule in a4["rules"]],
        )
        self.assertEqual(
            [rule["trace"]["adoption"] for rule in a0["rules"]], ["A0_COMPATIBILITY"] * len(a0["rules"])
        )
        self.assertEqual(
            [rule["trace"]["adoption"] for rule in a4["rules"]], ["A4_FULL_ORCHESTRATION"] * len(a4["rules"])
        )

    def test_n01_removing_j07_label_keeps_security_gate_required(self) -> None:
        """Pack N01: inspected security materiality outlives its job label."""
        result = resolve_effective_rules(service_x01_fixture(declared_jobs={"J03_BUG_FIX"}))
        security = rule_for(result, "independent security review")
        self.assertEqual(security["epistemic"], "PRESENT")
        self.assertEqual(security["gate_state"], "NOT_RUN")
        self.assertIn("label-independent", security["trace"]["applicability_reason"])
        states = set(gate_map(result).values())
        self.assertNotIn("NOT_APPLICABLE", states)
        self.assertNotIn("PASS", states)
        # Dropping J06/J08 labels cannot drop their inspected obligations either.
        self.assertIn("migration baseline/target state and interrupted recovery evidence", gate_map(result))
        self.assertIn("deployment side-effect authorization and idempotency reconciliation", gate_map(result))
        # Review #1032 R01: a required gate left NOT_RUN by missing owner proof
        # blocks the aggregate; label removal can never yield a false-green
        # ADMITTED.
        self.assertEqual(result["resolution"], "UNVERIFIED_GATES")
        self.assertNotEqual(result["resolution"], "ADMITTED")

    def test_n02_lower_authority_override_cannot_weaken_frozen_review(self) -> None:
        """Pack N02: CONFLICT; affected gate BLOCKED, lower authority never weakens."""
        result = resolve_effective_rules(
            service_x01_fixture(
                declared_jobs={"J07_SECURITY_VULNERABILITY"},
                observations={
                    dimension: {"state": "PRESENT", "ref": f"obs:{dimension}@707a", "fresh": True}
                    for dimension in MATERIAL_DIMENSIONS
                },
                owner_proofs={
                    "independent security review": proof("CHANGES_REQUESTED", ref="review:sec@707c"),
                },
                overrides=[
                    {
                        "obligation": "independent security review",
                        "value": "not-required",
                        "tier": "PROJECT_OVERRIDES",
                    }
                ],
            )
        )
        self.assertEqual(result["resolution"], "CONFLICT")
        self.assertTrue(result["conflict"])
        security = rule_for(result, "independent security review")
        self.assertEqual(security["gate_state"], "BLOCKED")
        self.assertIn("lower-authority override denied", security["trace"]["applicability_reason"])
        states = set(gate_map(result).values())
        self.assertNotIn("PASS", states)
        self.assertNotIn("NOT_APPLICABLE", states)


class ObligationConjunctionTests(unittest.TestCase):
    def test_p03_x01_conjunction_admits_only_when_every_owner_passes(self) -> None:
        """Pack P03: J03+J06+J07+J08 conjunct; no single-label win."""
        result = resolve_effective_rules(service_x01_fixture(owner_proofs=all_pass_proofs()))
        self.assertEqual(result["resolution"], "ADMITTED")
        obligations = set(gate_map(result))
        for obligation in (
            "independent security review",
            "migration baseline/target state and interrupted recovery evidence",
            "deployment side-effect authorization and idempotency reconciliation",
            "baseline repair verification",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, obligations)
                self.assertEqual(gate_map(result)[obligation], "PASS")
        # A single-label decision would have left the other X01 cores out.
        self.assertGreaterEqual(len(obligations), 4)

    def test_n03_missing_or_stale_observation_is_unknown_never_pass(self) -> None:
        """Pack N03: uninspected/stale facts stay UNKNOWN; no PASS, no inspected ABSENT."""
        without_permission = service_x01_fixture(
            declared_jobs={"J07_SECURITY_VULNERABILITY"},
            observations={
                key: value
                for key, value in service_x01_fixture()["observations"].items()
                if key != "permission"
            },
        )
        result = resolve_effective_rules(without_permission)
        permission = rule_for(result, "authorized actor/permission evidence")
        self.assertEqual(permission["epistemic"], "UNKNOWN")
        self.assertEqual(permission["gate_state"], "NOT_RUN")
        self.assertEqual(result["resolution"], "UNKNOWN_EPISTEMIC")

        stale = service_x01_fixture(
            declared_jobs={"J07_SECURITY_VULNERABILITY"},
            observations={
                key: dict(value, fresh=False) if key == "security" else value
                for key, value in service_x01_fixture()["observations"].items()
            },
            owner_proofs={"independent security review": proof(ref="review:sec@old")},
        )
        result = resolve_effective_rules(stale)
        security = rule_for(result, "independent security review")
        self.assertEqual(security["epistemic"], "UNKNOWN")
        self.assertEqual(security["gate_state"], "NOT_RUN")
        self.assertEqual(security["trace"]["required_evidence_currentness"], "UNKNOWN")
        self.assertEqual(gate_map(result)["independent security review"], "NOT_RUN")

    def test_n04_local_na_does_not_lift_other_owner_gates(self) -> None:
        """Pack N04: cross-concern AND keeps migration/security gates required."""
        observations = {
            "permission": {"state": "ABSENT_WITH_INSPECTED_SCOPE", "ref": "inventory:perm@707d", "fresh": True},
            "security": {"state": "PRESENT", "ref": "obs:security@707d", "fresh": True},
            "migration": {"state": "PRESENT", "ref": "obs:migration@707d", "fresh": True},
            "deploy": {"state": "ABSENT_WITH_INSPECTED_SCOPE", "ref": "inventory:deploy@707d", "fresh": True},
            "external_effect": {"state": "ABSENT_WITH_INSPECTED_SCOPE", "ref": "inventory:effect@707d", "fresh": True},
        }
        result = resolve_effective_rules(service_x01_fixture(declared_jobs=set(), observations=observations))
        self.assertEqual(gate_map(result)["authorized actor/permission evidence"], "NOT_APPLICABLE")
        self.assertIn(gate_map(result)["independent security review"], {"NOT_RUN", "BLOCKED"})
        self.assertIn(
            gate_map(result)["migration baseline/target state and interrupted recovery evidence"],
            {"NOT_RUN", "BLOCKED"},
        )
        self.assertEqual(rule_for(result, "independent security review")["epistemic"], "PRESENT")

    def test_n06_uncovered_compound_is_unverified_and_never_blanket_pass(self) -> None:
        """Pack N06: J09-J12 without a covered class is UNVERIFIED/BLOCKED."""
        jobs = {"J09_RELEASE_QUALIFICATION", "J10_INCIDENT_RECOVERY", "J11_DEPRECATION_RETIREMENT", "J12_UPSTREAM_REUSE"}
        result = resolve_effective_rules(
            service_x01_fixture(
                declared_jobs=jobs,
                observations={
                    dimension: {"state": "ABSENT_WITH_INSPECTED_SCOPE", "ref": f"inventory:{dimension}@707e", "fresh": True}
                    for dimension in MATERIAL_DIMENSIONS
                },
                owner_proofs=all_pass_proofs(),
            )
        )
        self.assertEqual(result["resolution"], "UNVERIFIED_COVERAGE")
        material = {
            obligation: state
            for obligation, state in gate_map(result).items()
            if obligation in {JOB_OBLIGATIONS[job] for job in jobs}
        }
        self.assertTrue(material)
        for obligation, state in material.items():
            with self.subTest(obligation=obligation):
                self.assertEqual(state, "BLOCKED")
                self.assertIn("equivalence class", rule_for(result, obligation)["trace"]["applicability_reason"])
        self.assertNotIn("PASS", set(material.values()))


class AggregateAdmissionFailClosedTests(unittest.TestCase):
    """Review #1032 R01: positive admission requires every applicable required
    gate to be satisfied by current trusted owner proof; the aggregate is
    blocked (not merely gate-mapped) on missing/FAIL/stale proof."""

    def test_n07_missing_owner_proofs_block_admission_even_when_job_class_covered(self) -> None:
        """X01 is a covered class with all facts PRESENT, yet no owner proof
        satisfies any required gate: the aggregate must be UNVERIFIED_GATES."""
        result = resolve_effective_rules(service_x01_fixture())
        self.assertEqual(result["resolution"], "UNVERIFIED_GATES")
        self.assertNotEqual(result["resolution"], "ADMITTED")
        self.assertNotIn("ADMITTED", {rule["trace"]["resolution"] for rule in result["rules"]})
        for rule in result["rules"]:
            with self.subTest(obligation=rule["obligation"]):
                self.assertEqual(rule["gate_state"], "NOT_RUN")
                self.assertEqual(rule["trace"]["owner_proof_ref"], "NONE")
                self.assertEqual(rule["trace"]["required_evidence_currentness"], "UNKNOWN")

    def test_n08_fail_owner_proof_blocks_admission(self) -> None:
        """A current FAIL review verdict blocks the aggregate as REJECTED_GATES."""
        proofs = all_pass_proofs()
        proofs["independent security review"] = proof("FAIL", ref="review:sec-fail@707c")
        result = resolve_effective_rules(service_x01_fixture(owner_proofs=proofs))
        self.assertEqual(result["resolution"], "REJECTED_GATES")
        self.assertNotEqual(result["resolution"], "ADMITTED")
        security = rule_for(result, "independent security review")
        self.assertEqual(security["gate_state"], "FAIL")
        self.assertEqual(security["trace"]["owner_proof_ref"], "review:sec-fail@707c")

    def test_n09_stale_owner_proof_blocks_admission(self) -> None:
        """A stale-HEAD proof never satisfies its gate and blocks the aggregate."""
        proofs = all_pass_proofs()
        proofs["independent security review"] = proof(ref="review:sec@stale-head", fresh=False)
        result = resolve_effective_rules(service_x01_fixture(owner_proofs=proofs))
        self.assertEqual(result["resolution"], "UNVERIFIED_GATES")
        self.assertNotEqual(result["resolution"], "ADMITTED")
        security = rule_for(result, "independent security review")
        self.assertEqual(security["gate_state"], "NOT_RUN")
        self.assertEqual(security["trace"]["required_evidence_currentness"], "UNKNOWN")
        self.assertEqual(security["trace"]["owner_proof_ref"], "review:sec@stale-head")

    def test_n10_removed_label_with_unproven_fact_blocks_admission(self) -> None:
        """Even with every other owner proof current, removing the J07 label
        cannot admit: the label-independent security obligation stays NOT_RUN
        and the aggregate is blocked."""
        proofs = all_pass_proofs()
        del proofs["independent security review"]
        result = resolve_effective_rules(
            service_x01_fixture(declared_jobs={"J03_BUG_FIX"}, owner_proofs=proofs)
        )
        self.assertEqual(result["resolution"], "UNVERIFIED_GATES")
        self.assertNotEqual(result["resolution"], "ADMITTED")
        security = rule_for(result, "independent security review")
        self.assertEqual(security["epistemic"], "PRESENT")
        self.assertEqual(security["gate_state"], "NOT_RUN")
        self.assertEqual(security["trace"]["owner_proof_ref"], "NONE")


class SupportedJobClassObligationTests(unittest.TestCase):
    """Review #1032 R02: every declared-covered job class resolves through an
    explicit owner-obligation mapping; unknown labels fail closed."""

    X02_JOBS = frozenset({"J05_PUBLIC_API_CHANGE", "J12_UPSTREAM_REUSE"})
    X05_JOBS = frozenset({"J04_FEATURE_CONTRACT", "J05_PUBLIC_API_CHANGE"})

    def test_x02_public_api_upstream_reuse_obligations_admit_when_proven(self) -> None:
        """Covered class X02 binds both job obligations to a real owner."""
        result = resolve_effective_rules(
            service_x01_fixture(declared_jobs=set(self.X02_JOBS), owner_proofs=all_pass_proofs())
        )
        self.assertEqual(result["resolution"], "ADMITTED")
        for obligation in (
            "public API change compatibility evidence",
            "upstream license/provenance/currentness evidence",
        ):
            with self.subTest(obligation=obligation):
                self.assertEqual(gate_map(result)[obligation], "PASS")
                rule = rule_for(result, obligation)
                self.assertTrue(rule["trace"]["owner_proof_ref"].startswith("proof:"))
                self.assertEqual(rule["trace"]["required_evidence_currentness"], "CURRENT")

    def test_x05_feature_contract_public_api_obligations_admit_when_proven(self) -> None:
        """Covered class X05 binds both job obligations to a real owner."""
        result = resolve_effective_rules(
            service_x01_fixture(declared_jobs=set(self.X05_JOBS), owner_proofs=all_pass_proofs())
        )
        self.assertEqual(result["resolution"], "ADMITTED")
        for obligation in (
            "feature contract conformance evidence",
            "public API change compatibility evidence",
        ):
            with self.subTest(obligation=obligation):
                self.assertEqual(gate_map(result)[obligation], "PASS")
        self.assertEqual(
            rule_for(result, "feature contract conformance evidence")["owner"],
            "interface compatibility owner",
        )

    def test_unknown_job_label_fails_closed_as_unverified_coverage(self) -> None:
        """A declared job with no owner-obligation mapping is UNVERIFIED_COVERAGE
        with a repair route, never a KeyError and never an admission."""
        result = resolve_effective_rules(
            service_x01_fixture(
                declared_jobs={"J13_UNKNOWN_JOB"},
                owner_proofs=all_pass_proofs(),
            )
        )
        self.assertEqual(result["resolution"], "UNVERIFIED_COVERAGE")
        for rule in result["rules"]:
            with self.subTest(obligation=rule["obligation"]):
                self.assertEqual(rule["gate_state"], "BLOCKED")
                self.assertIn("unknown job label", rule["trace"]["applicability_reason"])


class TraceProofBindingTests(unittest.TestCase):
    """Review #1032 R03: required_evidence_currentness and owner_proof_ref are
    bound to the real owning proof; an unfalsifiable CURRENT projection is a bug."""

    def test_missing_proof_never_projects_current_in_trace(self) -> None:
        result = resolve_effective_rules(service_x01_fixture(declared_jobs={"J03_BUG_FIX"}))
        for rule in result["rules"]:
            with self.subTest(obligation=rule["obligation"]):
                self.assertNotEqual(rule["trace"]["required_evidence_currentness"], "CURRENT")
                self.assertEqual(rule["trace"]["owner_proof_ref"], "NONE")

    def test_current_trace_binds_exact_owner_proof_ref(self) -> None:
        """Every admitted trace names the exact proof that satisfied its gate."""
        result = resolve_effective_rules(service_x01_fixture(owner_proofs=all_pass_proofs()))
        self.assertEqual(result["resolution"], "ADMITTED")
        for rule in result["rules"]:
            with self.subTest(obligation=rule["obligation"]):
                self.assertEqual(rule["trace"]["required_evidence_currentness"], "CURRENT")
                expected = all_pass_proofs()[rule["obligation"]]["ref"]
                self.assertEqual(rule["trace"]["owner_proof_ref"], expected)


class ProportionalityTests(unittest.TestCase):
    def test_p04_inspected_docs_only_fast_path_forces_no_blanket_record(self) -> None:
        """Pack P04: only genuinely applicable obligations; inspected N/A stays light."""
        result = resolve_effective_rules(cli_docs_fixture())
        self.assertEqual(result["resolution"], "ADMITTED")
        gate_map_result = gate_map(result)
        self.assertEqual(gate_map_result["affected docs checks"], "PASS")
        for dimension in MATERIAL_DIMENSIONS:
            obligation = DIMENSION_OBLIGATIONS[dimension]
            with self.subTest(obligation=obligation):
                self.assertEqual(gate_map_result[obligation], "NOT_APPLICABLE")
                rule = rule_for(result, obligation)
                self.assertEqual(rule["epistemic"], "ABSENT_WITH_INSPECTED_SCOPE")
                self.assertTrue(rule["trace"]["observed_fact_ref"].startswith("inventory:"))
        self.assertNotIn("UNKNOWN", set(gate_map_result.values()))
        self.assertNotIn("BLOCKED", set(gate_map_result.values()))


class TraceSideEffectBoundaryTests(unittest.TestCase):
    """No unauthorized side effects: pure resolution, canonical states only."""

    def test_resolution_does_not_mutate_protected_fixture_inputs(self) -> None:
        fixtures = [
            service_x01_fixture(),
            service_x01_fixture(owner_proofs=all_pass_proofs()),
            cli_docs_fixture(),
        ]
        for fixture in fixtures:
            with self.subTest(subject=fixture["exact_subject"]):
                snapshot = deepcopy(fixture)
                resolve_effective_rules(fixture)
                self.assertEqual(fixture, snapshot)

    def test_all_fixture_decisions_use_canonical_states_and_vocabulary(self) -> None:
        """Gate enum is preserved; dispositions come from the declared vocabulary."""
        fixtures = [
            service_x01_fixture(owner_proofs=all_pass_proofs()),
            service_x01_fixture(declared_jobs={"J03_BUG_FIX"}),
            service_x01_fixture(
                overrides=[
                    {
                        "obligation": "independent security review",
                        "value": "not-required",
                        "tier": "PROJECT_OVERRIDES",
                    }
                ]
            ),
            cli_docs_fixture(),
        ]
        seen_states: set[str] = set()
        for fixture in fixtures:
            result = resolve_effective_rules(fixture)
            with self.subTest(resolution=result["resolution"]):
                self.assertIn(result["resolution"], RESOLUTION_VOCABULARY)
            for rule in result["rules"]:
                seen_states.add(rule["gate_state"])
        self.assertTrue(seen_states <= CANONICAL_GATE_STATES, seen_states - CANONICAL_GATE_STATES)

    def test_every_trace_carries_exactly_the_minimal_projection_fields(self) -> None:
        result = resolve_effective_rules(service_x01_fixture(owner_proofs=all_pass_proofs()))
        self.assertTrue(result["rules"])
        for rule in result["rules"]:
            with self.subTest(obligation=rule["obligation"]):
                self.assertEqual(set(rule["trace"]), TRACE_FIELDS)


class R2NaBypassDenyTests(unittest.TestCase):
    """Review #1041 F02: an owner NOT_APPLICABLE verdict holds only for a
    dimension independently observed ABSENT within authorized scope that no
    other owner/declared label demands; contradictions DENY the aggregate."""

    def test_f02a_na_owner_proof_against_present_fact_denies_aggregate(self) -> None:
        """PRESENT inspected security fact + NOT_APPLICABLE owner proof → DENY."""
        proofs = all_pass_proofs()
        proofs["independent security review"] = proof("NOT_APPLICABLE", ref="proof:na-vs-present@707f")
        result = resolve_effective_rules(service_x01_fixture(owner_proofs=proofs))
        self.assertEqual(result["resolution"], "CONFLICT")
        self.assertNotEqual(result["resolution"], "ADMITTED")
        security = rule_for(result, "independent security review")
        self.assertEqual(security["gate_state"], "BLOCKED")
        self.assertNotEqual(security["gate_state"], "NOT_APPLICABLE")
        self.assertNotEqual(security["trace"]["required_evidence_currentness"], "CURRENT")
        self.assertIn("aggregate must DENY", security["trace"]["applicability_reason"])

    def test_f02b_label_demanded_gate_vs_claimed_absent_contradiction_denies(self) -> None:
        """Declared J07 label demands the gate while the dimension is claimed
        inspected-ABSENT: the contradiction fails closed, no N/A is minted."""
        observations = {
            dimension: {
                "state": "ABSENT_WITH_INSPECTED_SCOPE",
                "ref": f"inventory:{dimension}@707f",
                "fresh": True,
            }
            for dimension in MATERIAL_DIMENSIONS
        }
        result = resolve_effective_rules(
            service_x01_fixture(declared_jobs={"J07_SECURITY_VULNERABILITY"}, observations=observations)
        )
        self.assertEqual(result["resolution"], "CONFLICT")
        self.assertNotEqual(result["resolution"], "ADMITTED")
        security = rule_for(result, "independent security review")
        self.assertEqual(security["gate_state"], "BLOCKED")
        self.assertNotEqual(security["gate_state"], "NOT_APPLICABLE")
        self.assertIn("contradiction fails closed", security["trace"]["applicability_reason"])

    def test_f02c_independently_inspected_absent_without_label_demand_stays_na(self) -> None:
        """The light N/A route survives: inspected ABSENT + no label/owner
        demand is still admissible proportionality, not a bypass."""
        result = resolve_effective_rules(cli_docs_fixture())
        self.assertEqual(result["resolution"], "ADMITTED")
        for dimension in MATERIAL_DIMENSIONS:
            obligation = DIMENSION_OBLIGATIONS[dimension]
            self.assertEqual(gate_map(result)[obligation], "NOT_APPLICABLE")


class R2AuthorityRefCompletenessTests(unittest.TestCase):
    """Review #1041 F03: the applicable canonical authority reference set must
    be complete with exact immutable pins; an "unresolved" owner blob can never
    be current or pass."""

    def test_f03_empty_authority_ref_set_is_rejected_even_with_full_proofs(self) -> None:
        """authority_refs={} + every other proof PASS → DENY, never current."""
        result = resolve_effective_rules(
            service_x01_fixture(owner_proofs=all_pass_proofs(), authority_refs={})
        )
        self.assertEqual(result["resolution"], "REJECTED_CURRENTNESS")
        self.assertNotEqual(result["resolution"], "ADMITTED")
        for rule in result["rules"]:
            with self.subTest(obligation=rule["obligation"]):
                self.assertNotEqual(rule["trace"]["required_evidence_currentness"], "CURRENT")
                self.assertNotEqual(rule["gate_state"], "PASS")
                self.assertNotEqual(rule["trace"]["resolution"], "ADMITTED")

    def test_f03_missing_single_authority_member_is_rejected(self) -> None:
        refs = dict(service_x01_fixture()["authority_refs"])
        del refs["TASK_ACCEPTANCE"]
        result = resolve_effective_rules(
            service_x01_fixture(owner_proofs=all_pass_proofs(), authority_refs=refs)
        )
        self.assertEqual(result["resolution"], "REJECTED_CURRENTNESS")
        self.assertIn(
            "TASK_ACCEPTANCE",
            rule_for(result, "pinned standard currentness verification")["trace"]["applicability_reason"],
        )

    def test_f03_noncanonical_authority_tier_is_rejected(self) -> None:
        refs = dict(service_x01_fixture()["authority_refs"])
        refs["WIKI_RUMOR"] = f"wiki/rumor@{'f' * 40}"
        result = resolve_effective_rules(
            service_x01_fixture(owner_proofs=all_pass_proofs(), authority_refs=refs)
        )
        self.assertEqual(result["resolution"], "REJECTED_CURRENTNESS")

    def test_f03_unresolved_owner_blob_is_never_current_or_pass(self) -> None:
        partial_refs = {
            tier: ref
            for tier, ref in service_x01_fixture()["authority_refs"].items()
            if tier != "FROZEN_ARCHITECTURE"
        }
        fixtures = [
            service_x01_fixture(owner_proofs=all_pass_proofs(), authority_refs={}),
            service_x01_fixture(declared_jobs={"J03_BUG_FIX"}, authority_refs=partial_refs),
        ]
        for fixture in fixtures:
            result = resolve_effective_rules(fixture)
            with self.subTest(subject=fixture["exact_subject"]):
                self.assertEqual(result["resolution"], "REJECTED_CURRENTNESS")
            for rule in result["rules"]:
                trace = rule["trace"]
                if trace["owner_ref_blob"] == "unresolved" or "unresolved" in trace["decision_owner_ref"]:
                    with self.subTest(obligation=rule["obligation"]):
                        self.assertNotEqual(trace["required_evidence_currentness"], "CURRENT")
                        self.assertNotEqual(rule["gate_state"], "PASS")

    def test_f03_admitted_traces_never_carry_unresolved_owner_blobs(self) -> None:
        for fixture in (service_x01_fixture(owner_proofs=all_pass_proofs()), cli_docs_fixture()):
            result = resolve_effective_rules(fixture)
            self.assertEqual(result["resolution"], "ADMITTED")
            for rule in result["rules"]:
                with self.subTest(obligation=rule["obligation"]):
                    self.assertNotEqual(rule["trace"]["owner_ref_blob"], "unresolved")
                    self.assertNotIn("unresolved", rule["trace"]["decision_owner_ref"])


class R2ProofRefTrustTests(unittest.TestCase):
    """Review #1041 F04: blank/wrong-source/malformed/misbound/wrong-subject/
    stale proof refs are untrusted evidence and fail closed."""

    def test_f04_blank_fresh_proof_ref_is_never_current_and_denies(self) -> None:
        proofs = all_pass_proofs()
        proofs["independent security review"] = {"verdict": "PASS", "ref": "", "fresh": True}
        result = resolve_effective_rules(service_x01_fixture(owner_proofs=proofs))
        self.assertEqual(result["resolution"], "UNVERIFIED_GATES")
        self.assertNotEqual(result["resolution"], "ADMITTED")
        security = rule_for(result, "independent security review")
        self.assertEqual(security["gate_state"], "NOT_RUN")
        self.assertNotEqual(security["trace"]["required_evidence_currentness"], "CURRENT")
        self.assertIn("untrusted proof ref rejected", security["trace"]["applicability_reason"])

    def test_f04_malformed_wrong_source_and_wrong_subject_refs_fail_closed(self) -> None:
        cases = {
            "malformed_no_source": {"verdict": "PASS", "ref": "not-a-valid-ref", "fresh": True},
            "malformed_no_blob": {"verdict": "PASS", "ref": "review:sec@", "fresh": True},
            "wrong_source_shape": {"verdict": "PASS", "ref": "::@", "fresh": True},
            "wrong_subject": {
                "verdict": "PASS",
                "ref": "proof:independent-security-review@707f",
                "fresh": True,
                "subject": "svc/other@task/elsewhere",
            },
            "stale": {"verdict": "PASS", "ref": "review:sec@deadbeef", "fresh": False},
        }
        for name, owner_proof in cases.items():
            with self.subTest(case=name):
                proofs = all_pass_proofs()
                proofs["independent security review"] = owner_proof
                result = resolve_effective_rules(service_x01_fixture(owner_proofs=proofs))
                self.assertNotEqual(result["resolution"], "ADMITTED")
                security = rule_for(result, "independent security review")
                self.assertNotEqual(security["gate_state"], "PASS")
                self.assertNotEqual(security["trace"]["required_evidence_currentness"], "CURRENT")
                if name == "stale":
                    # stale proofs fail closed through the dedicated stale-HEAD
                    # route rather than the untrusted-ref rejection.
                    self.assertIn("stale HEAD", security["trace"]["applicability_reason"])
                else:
                    self.assertIn("untrusted proof ref rejected", security["trace"]["applicability_reason"])

    def test_f04_misbound_shared_ref_cannot_serve_two_obligations(self) -> None:
        proofs = all_pass_proofs()
        shared = "proof:shared-evidence@707f"
        proofs["independent security review"] = proof(ref=shared)
        proofs["authorized actor/permission evidence"] = proof(ref=shared)
        result = resolve_effective_rules(service_x01_fixture(owner_proofs=proofs))
        self.assertEqual(result["resolution"], "UNVERIFIED_GATES")
        for obligation in ("independent security review", "authorized actor/permission evidence"):
            with self.subTest(obligation=obligation):
                rule = rule_for(result, obligation)
                self.assertEqual(rule["gate_state"], "NOT_RUN")
                self.assertNotEqual(rule["trace"]["required_evidence_currentness"], "CURRENT")
                self.assertIn("misbound", rule["trace"]["applicability_reason"])


@unittest.skip(
    "DEFERRED_TO_T11 / NOT_RUN: the centralized effective-rule projection and the real "
    "owner-contract integration (shared verifier / Build Host wiring) are owned by T11. "
    "This file's in-test resolution model is a decision oracle fixture, not the owner "
    "contract executor; no owner-contract PASS completeness is claimed by this task. "
    "Review #1041 F05."
)
class DeferredCentralizedProjectionIntegrationTests(unittest.TestCase):
    """F05 (review #1041): explicit NOT_RUN marker for owner-contract execution.

    Kept as a named, skipped oracle so the deferral stays visible in test
    output instead of being conflated with a passing owner-contract check.
    """

    def test_centralized_projection_wired_to_real_owner_contract(self) -> None:
        raise AssertionError("must stay skipped until T11 wires the centralized projection")

    def test_owner_contract_pass_completeness_against_build_host(self) -> None:
        raise AssertionError("must stay skipped until T11/Build Host integration exists")


if __name__ == "__main__":
    unittest.main(verbosity=2)
