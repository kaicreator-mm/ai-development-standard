#!/usr/bin/env python3
"""Derive a fail-closed, non-authoritative progressive-disclosure read plan.

Consumes current durable authority through an injected ``authority_reader``
trust boundary and reuses the v4.7 T02 manifest resolver. ``RESOLVED`` means
only that a deterministic read plan could be derived; no gate is satisfied.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import subprocess
from typing import Callable, Iterable, Mapping, Any

from test_v47_authority_registry import RegistryError, resolve_registry

SHA40 = re.compile(r"^[0-9a-f]{40}$")
CAPABILITY_KEYS = {
    "v4.interchange", "v4.reducer", "v4.controllers", "v4.fast_path",
    "execution_pack.enabled", "validation_queue.enabled",
}
PROFILE_KEYS = {"language_profile_ref", "archetype_profile_ref"}
STAGES = frozenset({"read", "task", "execution"})
INTENTS = frozenset({"read", "mutation"})


@dataclass(frozen=True)
class RoutingBlocker:
    code: str
    owner: str
    detail: str
    source: str | None = None

    def as_dict(self) -> dict[str, str | None]:
        return {"code": self.code, "owner": self.owner, "detail": self.detail, "source": self.source}


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def _parse_version(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if "=" in raw:
            key, value = raw.split("=", 1)
            result[key.strip()] = value.strip()
    return result


def _parse_overrides(text: str) -> tuple[dict[str, str], list[str], list[RoutingBlocker]]:
    """Reject any repeated routing-relevant declaration, regardless of order.

    Even identical repetitions are ambiguous configuration provenance; silently
    deduplicating them would conceal contradictory project adoption or profiles.
    """
    values: dict[str, str] = {}
    profiles: list[str] = []
    first_line: dict[str, int] = {}
    blockers: list[RoutingBlocker] = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        match = re.match(r"^\s*-\s*`?([A-Za-z0-9_.-]+)`?\s*:\s*(.*?)\s*$", raw)
        if not match:
            continue
        key, value = match.groups()
        if key in CAPABILITY_KEYS | PROFILE_KEYS and key in first_line:
            code = "CONFLICTING_PROJECT_OVERRIDE" if values[key] != value else "DUPLICATE_PROJECT_OVERRIDE"
            blockers.append(RoutingBlocker(
                code, "project overrides",
                f"{key}: repeated declaration at line {lineno}; first declared at line {first_line[key]}",
                "project:.dev-standard/PROJECT_OVERRIDES.md",
            ))
            continue
        values[key] = value
        first_line.setdefault(key, lineno)
        if key in PROFILE_KEYS and value and not value.startswith("<"):
            profiles.append(value)
    return values, profiles, blockers


def _safe_relative(root: Path, relative: str) -> Path:
    if not relative or relative.startswith(("/", "\\")):
        raise ValueError("absolute/empty path is not allowed")
    candidate = (root / relative).resolve()
    real_root = root.resolve()
    if candidate != real_root and real_root not in candidate.parents:
        raise ValueError("path escapes root")
    return candidate


def _git_head(root: Path) -> str | None:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    head = proc.stdout.strip()
    return head if SHA40.fullmatch(head) else None


def _profile_path(ref: str, project_root: Path, standard_root: Path) -> tuple[str, Path]:
    if ref.startswith("project:"):
        rel = ref.removeprefix("project:")
        return f"project:{rel}", _safe_relative(project_root, rel)
    if ref.startswith("ads:"):
        rel = ref.removeprefix("ads:")
        return f"ads:{rel}", _safe_relative(standard_root, rel)
    raise ValueError("profile ref must start with project: or ads:")


def _append_unique(read_set: list[dict[str, str]], kind: str, ref: str, reason: str) -> None:
    if not any(item["ref"] == ref for item in read_set):
        read_set.append({"kind": kind, "ref": ref, "reason": reason})


def _blocked(read_set: list[dict[str, str]], blockers: Iterable[RoutingBlocker], trace: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "status": "BLOCKED", "complete": False,
        "read_set": read_set,
        "blockers": [b.as_dict() for b in blockers], "trace": trace,
        "authority_effect": "NONE", "gate_effect": "NONE",
        "mutation_authorized": False,
        "note": "Routing metadata is non-authoritative; BLOCKED routes to the named owner/human authority.",
    }


def resolve_standard_read_set(
    project_root: Path,
    standard_root: Path,
    request: Mapping[str, Any],
    *,
    authority_reader: Callable[[Mapping[str, Any]], Mapping[str, Any]] | None,
    revision_probe: Callable[[Path], str | None] | None = None,
    authority_reader_scope: str = "LIVE_DURABLE",
) -> dict[str, Any]:
    """Derive a read plan using a trustworthy synchronous authority adapter.

    Production adapters MUST re-read durable Issue/PR/branch and any existing
    Dispatch/Execution source at this invocation. Tests use deterministic
    adapters explicitly marked TEST_FIXTURE; their PASS is not external proof.
    Arbitrary input flags cannot replace this adapter or grant side effects.
    """
    project_root, standard_root = Path(project_root), Path(standard_root)
    blockers: list[RoutingBlocker] = []
    trace: list[dict[str, Any]] = []
    read_set: list[dict[str, str]] = []
    # Only omitted/None/empty legacy modes receive defaults. Never trim or
    # normalize an unsupported nonempty mode into an authorized read plan.
    stage = request.get("stage", "task")
    intent = request.get("intent", "read")
    if stage is None or stage == "":
        stage = "task"
    if intent is None or intent == "":
        intent = "read"
    if not isinstance(stage, str) or stage not in STAGES:
        blockers.append(RoutingBlocker("INVALID_ROUTING_STAGE", "planning/human authority", f"unsupported stage {stage!r}; expected one of {sorted(STAGES)}"))
    if not isinstance(intent, str) or intent not in INTENTS:
        blockers.append(RoutingBlocker("INVALID_ROUTING_INTENT", "planning/human authority", f"unsupported intent {intent!r}; expected one of {sorted(INTENTS)}"))
    if blockers:
        return _blocked(read_set, blockers, trace)

    project_agents = project_root / "AGENTS.md"
    version_file = project_root / ".dev-standard" / "VERSION"
    overrides_file = project_root / ".dev-standard" / "PROJECT_OVERRIDES.md"
    standard_agents = standard_root / "AGENTS.md"
    manifest_path = standard_root / "standard-manifest.json"
    schema_path = standard_root / "schemas" / "authority-applicability-entry-v1.schema.json"
    for path, owner in (
        (project_agents, "project repository authority"),
        (version_file, "project ADS pin"),
        (overrides_file, "project overrides"),
        (standard_agents, "pinned ADS"),
        (manifest_path, "T02 semantic registry"),
        (schema_path, "T01 authority/applicability schema"),
    ):
        if not path.is_file():
            blockers.append(RoutingBlocker("MISSING_DURABLE_SOURCE", owner, f"missing {path}", str(path)))
    if blockers:
        return _blocked(read_set, blockers, trace)

    _append_unique(read_set, "project-authority", "project:AGENTS.md", "repository-local Agent instructions")
    _append_unique(read_set, "project-pin", "project:.dev-standard/VERSION", "immutable ADS pin")
    pin = _parse_version(version_file)
    revision = pin.get("revision", "")
    if pin.get("repository") != "kaicreator-mm/ai-development-standard" or not SHA40.fullmatch(revision):
        blockers.append(RoutingBlocker("INVALID_ADS_PIN", "project ADS pin", "repository/revision is not an immutable ADS pin", "project:.dev-standard/VERSION"))
    probe = revision_probe or _git_head
    actual_revision = probe(standard_root)
    if actual_revision is None:
        blockers.append(RoutingBlocker("ADS_REVISION_UNVERIFIED", "project ADS pin", "pinned ADS checkout revision could not be verified", "project:.dev-standard/VERSION"))
    elif actual_revision != revision:
        blockers.append(RoutingBlocker("ADS_PIN_MISMATCH", "project ADS pin", f"project pins {revision} but ADS checkout is {actual_revision}", "project:.dev-standard/VERSION"))
    if blockers:
        return _blocked(read_set, blockers, trace)
    _append_unique(read_set, "standard-authority", "ads:AGENTS.md", "pinned ADS Agent instructions")
    _append_unique(read_set, "registry", "ads:standard-manifest.json", "T02 semantic owner discovery")

    manifest = _load_json(manifest_path)
    schema = _load_json(schema_path)
    try:
        resolved = resolve_registry(manifest, schema, root=standard_root)
    except (RegistryError, KeyError, TypeError, ValueError) as exc:
        blockers.append(RoutingBlocker("REGISTRY_UNRESOLVED", "T02 semantic registry", str(exc), "ads:standard-manifest.json"))
        return _blocked(read_set, blockers, trace)
    entries = {e["semantic_concern"]: e for e in manifest.get("semantic_authorities", {}).get("entries", [])}
    override_values, selected_profiles, override_blockers = _parse_overrides(overrides_file.read_text(encoding="utf-8"))
    if override_blockers:
        return _blocked(read_set, override_blockers, trace)
    requested_capabilities = request.get("requested_capabilities", [])
    if not isinstance(requested_capabilities, list) or any(not isinstance(v, str) for v in requested_capabilities):
        return _blocked(read_set, [RoutingBlocker("INVALID_REQUEST", "planning/human authority", "requested_capabilities must be a string list")], trace)
    for capability in requested_capabilities:
        if capability not in CAPABILITY_KEYS:
            blockers.append(RoutingBlocker("UNKNOWN_CAPABILITY", "project overrides", capability, "project:.dev-standard/PROJECT_OVERRIDES.md"))
            continue
        value = override_values.get(capability)
        if value is None or value.startswith("<"):
            blockers.append(RoutingBlocker("CAPABILITY_APPLICABILITY_UNKNOWN", "project overrides", capability, "project:.dev-standard/PROJECT_OVERRIDES.md"))
        elif value.lower().startswith(("disabled", "false", "not_applicable")):
            blockers.append(RoutingBlocker("CAPABILITY_DISABLED", "project overrides", capability, "project:.dev-standard/PROJECT_OVERRIDES.md"))
    if blockers:
        return _blocked(read_set, blockers, trace)

    if authority_reader is None:
        return _blocked(read_set, [RoutingBlocker("CURRENT_AUTHORITY_UNVERIFIED", "Task/Issue authority", "no synchronous durable authority reader was supplied")], trace)
    try:
        facts = dict(authority_reader(request))
    except Exception as exc:
        return _blocked(read_set, [RoutingBlocker("CURRENT_AUTHORITY_UNAVAILABLE", "Task/Issue authority", str(exc))], trace)

    issue_ref = request.get("task_issue_ref")
    task_pack_ref = request.get("task_pack_ref")
    expected_subject = request.get("subject_sha")
    if not isinstance(issue_ref, str) or not re.fullmatch(r"https://github\.com/[^/]+/[^/]+/issues/\d+", issue_ref):
        blockers.append(RoutingBlocker("INVALID_TASK_ISSUE_REF", "Task/Issue authority", "exact durable GitHub Issue URL required"))
    if facts.get("task_issue_ref") != issue_ref:
        blockers.append(RoutingBlocker("TASK_ISSUE_CURRENTNESS_MISMATCH", "Task/Issue authority", "live issue differs from requested task", str(issue_ref)))
    if not isinstance(task_pack_ref, str):
        blockers.append(RoutingBlocker("MISSING_TASK_PACK_REF", "Task Pack", "exact Task Pack path required"))
    else:
        try:
            pack_path = _safe_relative(project_root, task_pack_ref)
            if not pack_path.is_file():
                blockers.append(RoutingBlocker("MISSING_TASK_PACK", "Task Pack", task_pack_ref, f"project:{task_pack_ref}"))
        except ValueError as exc:
            blockers.append(RoutingBlocker("INVALID_TASK_PACK_REF", "Task Pack", str(exc), str(task_pack_ref)))
        if facts.get("task_pack_ref") != task_pack_ref:
            blockers.append(RoutingBlocker("TASK_PACK_IDENTITY_MISMATCH", "Task Pack", "durable task authority points at a different Task Pack", str(task_pack_ref)))
    if not isinstance(expected_subject, str) or not SHA40.fullmatch(expected_subject):
        blockers.append(RoutingBlocker("MISSING_EXACT_SUBJECT", "Task/Issue authority", "40-char exact subject SHA required"))
    elif facts.get("current_subject_sha") != expected_subject:
        blockers.append(RoutingBlocker("EXACT_SUBJECT_DRIFT", "Task/Issue authority", f"expected {expected_subject}, current {facts.get('current_subject_sha')}", str(issue_ref)))
    expected_base = request.get("base_sha")
    if expected_base is not None:
        if not isinstance(expected_base, str) or not SHA40.fullmatch(expected_base):
            blockers.append(RoutingBlocker("INVALID_BASE_SHA", "Task/Issue authority", "base_sha must be exact SHA"))
        elif facts.get("current_base_sha") != expected_base:
            blockers.append(RoutingBlocker("EXACT_BASE_DRIFT", "Task/Issue authority", f"expected {expected_base}, current {facts.get('current_base_sha')}", str(issue_ref)))
    if blockers:
        return _blocked(read_set, blockers, trace)

    requested_concerns = request.get("requested_concerns", [])
    if not isinstance(requested_concerns, list) or any(not isinstance(v, str) for v in requested_concerns):
        return _blocked(read_set, [RoutingBlocker("INVALID_REQUEST", "planning/human authority", "requested_concerns must be a string list")], trace)
    unknown = sorted(set(requested_concerns) - set(resolved))
    if unknown:
        return _blocked(read_set, [RoutingBlocker("UNKNOWN_SEMANTIC_OWNER", "planning/human authority", ", ".join(unknown), "ads:standard-manifest.json")], trace)
    materiality = facts.get("materiality", {})
    if not isinstance(materiality, dict):
        materiality = {}
    selected_concerns: list[str] = []
    for concern, owner_ref in resolved.items():
        entry = entries[concern]
        posture = entry["applicability_posture"]
        if posture == "ALWAYS":
            selected_concerns.append(concern)
            continue
        if concern not in requested_concerns:
            trace.append({"concern": concern, "decision": "OMITTED", "reason": f"{posture} not requested/adopted"})
            continue
        evidence = materiality.get(concern)
        if not isinstance(evidence, dict) or evidence.get("decision") not in {"APPLICABLE", "NOT_APPLICABLE"}:
            blockers.append(RoutingBlocker("MATERIALITY_UNKNOWN", owner_ref, concern, str(issue_ref)))
            continue
        if evidence.get("source_ref") not in {issue_ref, "project:.dev-standard/PROJECT_OVERRIDES.md"}:
            blockers.append(RoutingBlocker("MATERIALITY_SOURCE_UNQUALIFIED", owner_ref, concern, str(evidence.get("source_ref"))))
            continue
        if evidence["decision"] == "NOT_APPLICABLE":
            blockers.append(RoutingBlocker("REQUEST_CONFLICTS_WITH_NONAPPLICABILITY", owner_ref, concern, str(evidence["source_ref"])))
            continue
        selected_concerns.append(concern)
    if blockers:
        return _blocked(read_set, blockers, trace)
    for concern in selected_concerns:
        owner_ref = resolved[concern]
        _append_unique(read_set, "semantic-owner", f"ads:{owner_ref}", concern)
        trace.append({"concern": concern, "decision": "INCLUDED", "owner": owner_ref, "posture": entries[concern]["applicability_posture"]})
    _append_unique(read_set, "project-overrides", "project:.dev-standard/PROJECT_OVERRIDES.md", "project adoption/materiality specialization")
    for profile_ref in selected_profiles:
        try:
            normalized, path = _profile_path(profile_ref, project_root, standard_root)
        except ValueError as exc:
            blockers.append(RoutingBlocker("INVALID_PROFILE_REF", "project overrides", str(exc), profile_ref))
            continue
        if not path.is_file():
            blockers.append(RoutingBlocker("MISSING_SELECTED_PROFILE", "project overrides", profile_ref, normalized))
            continue
        _append_unique(read_set, "selected-profile", normalized, "explicit project-selected language/archetype profile")
    if blockers:
        return _blocked(read_set, blockers, trace)
    _append_unique(read_set, "task-pack", f"project:{task_pack_ref}", "exact durable Task authority")
    _append_unique(read_set, "task-issue", issue_ref, "current GitHub Task/currentness authority")

    if stage == "execution":
        dispatch_ref = facts.get("dispatch_ref")
        execution_pack_ref = facts.get("execution_pack_ref")
        if not dispatch_ref or not execution_pack_ref:
            blockers.append(RoutingBlocker("EXECUTION_AUTHORITY_MISSING", "Dispatch/Execution Pack authority", "execution requires both durable sources", str(issue_ref)))
        elif facts.get("dispatch_subject_sha") != expected_subject or facts.get("execution_pack_subject_sha") != expected_subject:
            blockers.append(RoutingBlocker("EXECUTION_SUBJECT_DRIFT", "Dispatch/Execution Pack authority", "both sources must bind current exact subject", str(dispatch_ref)))
        else:
            for ref in (dispatch_ref, execution_pack_ref):
                if not isinstance(ref, str) or not ref.startswith("project:"):
                    blockers.append(RoutingBlocker("INVALID_EXECUTION_SOURCE", "Dispatch/Execution Pack authority", "expected project-local verified source ref", str(ref)))
                    continue
                try:
                    source_path = _safe_relative(project_root, ref.removeprefix("project:"))
                    if not source_path.is_file():
                        blockers.append(RoutingBlocker("MISSING_EXECUTION_SOURCE", "Dispatch/Execution Pack authority", str(ref)))
                except ValueError as exc:
                    blockers.append(RoutingBlocker("INVALID_EXECUTION_SOURCE", "Dispatch/Execution Pack authority", str(exc), str(ref)))
            if not blockers:
                _append_unique(read_set, "execution-pack", str(execution_pack_ref), "existing subordinate execution authority")
                _append_unique(read_set, "dispatch", str(dispatch_ref), "existing exact-subject dispatch/currentness authority")
    if intent == "mutation" and (not facts.get("mutation_authority_ref") or facts.get("mutation_subject_sha") != expected_subject):
        blockers.append(RoutingBlocker("MUTATION_AUTHORITY_NOT_PROVEN", "Task/Dispatch authority", "exact-subject authority not independently verified; provider availability is irrelevant", str(issue_ref)))
    if blockers:
        return _blocked(read_set, blockers, trace)
    return {
        "status": "RESOLVED", "complete": True,
        "read_set": read_set, "blockers": [], "trace": trace,
        "authority_reader_scope": authority_reader_scope,
        "ignored_lower_authority_inputs": ["chat", "memory", "context_volume", "provider_or_tool_availability"],
        "authority_effect": "NONE", "gate_effect": "NONE",
        "mutation_authorized": False, "subject_sha": expected_subject,
        "base_sha": expected_base,
        "note": "RESOLVED is routing metadata, never Task/Validation/Review/Release READY or PASS.",
    }


if __name__ == "__main__":
    raise SystemExit(
        "Import this module from an owning controller with a synchronous durable authority_reader. "
        "Raw JSON flags are insufficient to claim current GitHub authority."
    )