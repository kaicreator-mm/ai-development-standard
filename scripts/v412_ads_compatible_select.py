#!/usr/bin/env python3
"""ADS v4.12: read-only latest *verified compatible stable* recommendation.

Never changes .dev-standard/VERSION, files, tasks, claims, tags or repositories.
The supplied candidate list is discovery input, NOT qualification authority.
Actual immutable Git objects AND live GitHub Release/Issue evidence are checked;
unavailable, unverifiable or ambiguous proof fails closed without a suggestion.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

SHA = re.compile(r"^[a-f0-9]{40}$")
VERSION = re.compile(r"^\d+\.\d+\.\d+$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
REQUIRED_DIMENSIONS = frozenset({
    "source", "wire", "schema", "behavior", "authority", "claim", "review",
    "validation", "release", "external_effects",
})
PIN = re.compile(r"^([a-z_]+)=(.*)$", re.M)
CURRENT_PROFILE = "TRACK_LATEST_COMPATIBLE_STABLE"


class Unsafe(ValueError):
    pass


def git(repo: Path, *args: str) -> str:
    env = dict(os.environ)
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    p = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, env=env, text=True)
    if p.returncode:
        raise Unsafe("GIT_SOURCE_UNAVAILABLE")
    return p.stdout.strip()


def exact_commit(repo: Path, sha: str) -> str:
    if not isinstance(sha, str) or not SHA.fullmatch(sha):
        raise Unsafe("INVALID_EXACT_COMMIT")
    if git(repo, "rev-parse", "--verify", sha + "^{commit}") != sha:
        raise Unsafe("UNVERIFIED_COMMIT")
    return sha


def at(repo: Path, sha: str, path: str) -> str:
    if not path or path.startswith("/") or ".." in path.split("/") or "\\" in path or ":" in path:
        raise Unsafe("UNSAFE_SOURCE_PATH")
    return git(repo, "show", sha + ":" + path)


def parse_version(blob: str) -> dict:
    values = dict(PIN.findall(blob))
    if (values.get("repository") != "kaicreator-mm/ai-development-standard"
            or not VERSION.fullmatch(values.get("version", ""))
            or not SHA.fullmatch(values.get("revision", ""))):
        raise Unsafe("INVALID_EFFECTIVE_PIN")
    return values


def api_json(url: str) -> dict:
    if not url.startswith("https://api.github.com/repos/kaicreator-mm/ai-development-standard/"):
        raise Unsafe("UNTRUSTED_RELEASE_API")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ADS-v412-read-only-selector"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urlopen(Request(url, headers=headers), timeout=8) as response:
        data = json.load(response)
    if not isinstance(data, dict):
        raise Unsafe("INVALID_API_RECORD")
    return data


def has_source_manifest(repo: Path, sha: str) -> bool:
    raw = at(repo, sha, "standard-manifest.json")
    manifest = json.loads(raw)
    norm = manifest.get("sections", {}).get("normative_standards", [])
    return (isinstance(norm, list) and "standards/PROJECT_ADOPTION.md" in norm
            and "standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md" in norm)


def qualified(repo: Path, sha: str, version: str, item: dict, fetch) -> str:
    """Verify exact immutable local tag, published stable release and live canonical event."""
    if not isinstance(item, dict) or not has_source_manifest(repo, sha):
        raise Unsafe("MISSING_SOURCE_MANIFEST")
    tag = "v" + version
    if item.get("release_tag") != tag or git(repo, "rev-parse", "--verify",
                                                "refs/tags/" + tag + "^{commit}") != sha:
        raise Unsafe("UNPINNED_RELEASE_TAG")
    release = fetch("https://api.github.com/repos/kaicreator-mm/ai-development-standard/releases/tags/" + tag)
    if (release.get("tag_name") != tag or release.get("draft") is not False
            or release.get("prerelease") is not False or not release.get("html_url")):
        raise Unsafe("NOT_PUBLISHED_STABLE_RELEASE")
    issue, comment = item.get("qualification_issue"), item.get("qualification_comment")
    if type(issue) is not int or issue < 1 or type(comment) is not int or comment < 1:
        raise Unsafe("MISSING_QUALIFICATION_EVENT_REFERENCE")
    url = ("https://api.github.com/repos/kaicreator-mm/ai-development-standard/"
           f"issues/comments/{comment}")
    event = fetch(url)
    body = event.get("body", "")
    if (event.get("id") != comment or f"/issues/{issue}#" not in str(event.get("html_url", ""))
            or not isinstance(body, str) or not body.startswith("<!-- ai-dev:event:v2 -->\\n".replace("\\n", "\n"))):
        raise Unsafe("UNVERIFIED_CURRENT_RELEASE_QUALIFICATION")
    fields = {}
    for line in body.splitlines()[1:]:
        match = re.fullmatch(r"([a-z_]+)=([^\r\n]+)", line.strip())
        if match:
            key, value = match.groups()
            if key in fields:
                raise Unsafe("CONFLICTING_RELEASE_EVENT_FIELDS")
            fields[key] = value
    required = ("actor_role", "operator_kind", "operator_id", "session_ref",
                "canonical_admission_ref", "gate_evidence_refs")
    if (fields.get("event") != "RELEASE_QUALIFICATION"
            or fields.get("candidate_sha") != sha
            or fields.get("qualification") != "RELEASE_QUALIFIED"
            or fields.get("actor_role") != "release-controller"
            or any(not fields.get(key) for key in required)):
        raise Unsafe("UNVERIFIED_CURRENT_RELEASE_QUALIFICATION")
    # A release decision comment cannot itself prove that a test was run.
    # Bind one actual objective CI run to this exact candidate via GitHub API.
    runs = re.findall(r"(?:^|;)actions:(\d+)(?:;|$)", fields["gate_evidence_refs"])
    if len(runs) != 1:
        raise Unsafe("RELEASE_GATE_EXECUTION_REFERENCE_MISSING")
    ci = fetch("https://api.github.com/repos/kaicreator-mm/ai-development-standard/actions/runs/" + runs[0])
    if (ci.get("id") != int(runs[0]) or ci.get("head_sha") != sha
            or ci.get("conclusion") != "success" or ci.get("status") != "completed"
            or ci.get("name") != "verify-standard"):
        raise Unsafe("RELEASE_GATE_EVIDENCE_STALE_OR_NOT_EXECUTED")
    return url


def compatible(record: dict, current: str, candidate: str) -> list[str]:
    if (not isinstance(record, dict) or record.get("schema_version") != 1
            or record.get("baseline", {}).get("sha_or_digest") != current
            or record.get("candidate", {}).get("sha_or_digest") != candidate
            or not isinstance(record.get("change_operations"), list)
            or not record["change_operations"]
            or not record.get("producer_refs") or not record.get("consumer_refs")):
        raise Unsafe("INVALID_SOURCE_COMPATIBILITY_RECORD")
    dimensions = record.get("dimensions", [])
    if not isinstance(dimensions, list):
        raise Unsafe("MISSING_MATERIAL_DIMENSIONS")
    seen = set()
    refs = []
    for dim in dimensions:
        if not isinstance(dim, dict) or not isinstance(dim.get("name"), str):
            raise Unsafe("BAD_COMPATIBILITY_DIMENSION")
        name = dim["name"]
        if name in seen:
            raise Unsafe("DUPLICATE_COMPATIBILITY_DIMENSION")
        seen.add(name)
        if (dim.get("outcome") != "COMPATIBLE"
                or not isinstance(dim.get("evidence_refs"), list)
                or not dim["evidence_refs"]
                or not all(isinstance(e, str) and e.strip() for e in dim["evidence_refs"])):
            raise Unsafe("MATERIAL_COMPATIBILITY_UNKNOWN_OR_UNPROVEN")
        refs.extend(dim["evidence_refs"])
    if not REQUIRED_DIMENSIONS <= seen:
        raise Unsafe("MATERIAL_COMPATIBILITY_DIMENSIONS_MISSING")
    return sorted(set(refs))


def ancestor(repo: Path, older: str, newer: str) -> bool:
    p = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", older, newer],
                       capture_output=True, env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"})
    if p.returncode not in (0, 1):
        raise Unsafe("UNKNOWN_RELEASE_LINEAGE")
    return p.returncode == 0


def select(repo: Path, project: dict, candidates: list, fetch=api_json) -> dict:
    """Candidate data cannot elevate missing GitHub API / Git source evidence to PASS."""
    output = {"decision": "NO_SAFE_RECOMMENDATION", "effective_pin_changed": False}
    try:
        if project.get("preference") != CURRENT_PROFILE:
            raise Unsafe("PROJECT_NOT_OPTED_IN")
        if project.get("active_task") or project.get("frozen_candidate"):
            raise Unsafe("ACTIVE_SUBJECT_CANNOT_REBIND")
        current = exact_commit(repo, project.get("current_revision", ""))
        cv = at(repo, current, "VERSION")
        if not VERSION.fullmatch(cv) or project.get("current_version") != cv:
            raise Unsafe("CURRENT_VERSION_SOURCE_DRIFT")
        if not has_source_manifest(repo, current):
            raise Unsafe("UNVERIFIED_CURRENT_MANIFEST")
        if not isinstance(candidates, list) or not candidates:
            raise Unsafe("NO_CANDIDATES")
        valid = []
        for item in candidates:
            if not isinstance(item, dict):
                raise Unsafe("BAD_CANDIDATE")
            sha = exact_commit(repo, item.get("sha", ""))
            if sha == current:
                continue
            ver = at(repo, sha, "VERSION")
            if not VERSION.fullmatch(ver) or not ancestor(repo, current, sha):
                raise Unsafe("INCOMPARABLE_OR_UNRELEASED_CANDIDATE")
            proof = qualified(repo, sha, ver, item, fetch)
            refs = compatible(item.get("compatibility_record"), current, sha)
            valid.append({"revision": sha, "version": ver, "qualification_ref": proof, "compatibility_refs": refs})
        if not valid:
            raise Unsafe("NO_NEW_ELIGIBLE_RELEASE")
        maxima = [v for v in valid if all(ancestor(repo, w["revision"], v["revision"]) for w in valid)]
        if len(maxima) != 1:
            raise Unsafe("MULTIPLE_INCOMPARABLE_LATEST_RELEASES")
        best = maxima[0]
        output.update({"decision": "READ_ONLY_RECOMMENDATION", "current_revision": current,
                       "current_version": cv, "proposed_revision": best["revision"],
                       "proposed_version": best["version"], "release_qualification_ref": best["qualification_ref"],
                       "compatibility_evidence_refs": best["compatibility_refs"],
                       "next_step": "PROJECT_LOCAL_AUTHORIZED_CHECKPOINT_ONLY"})
    except (Unsafe, ValueError, KeyError, TypeError, OSError, HTTPError, URLError, json.JSONDecodeError) as error:
        output["reason"] = str(error) if isinstance(error, Unsafe) else "MISSING_OR_INVALID_SOURCE_EVIDENCE"
    return output


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ads-repo", required=True)
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--candidates", required=True, help="Source-discovery candidates JSON; never authority")
    args = ap.parse_args()
    project_root = Path(args.project_root)
    try:
        # The file is deliberately never overwritten or silently re-pinned.
        pin = parse_version((project_root / ".dev-standard/VERSION").read_text(encoding="utf-8"))
        overrides = (project_root / ".dev-standard/PROJECT_OVERRIDES.md").read_text(encoding="utf-8")
        opted = re.search(r"(?m)^standard_update_preference=([A-Z_]+)\s*$", overrides)
        data = json.loads(Path(args.candidates).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise Unsafe("INVALID_DISCOVERY_INPUT")
        project = {"preference": opted.group(1) if opted else "PINNED/MANUAL",
                   "current_revision": pin["revision"], "current_version": pin["version"],
                   "active_task": data.get("active_task"), "frozen_candidate": data.get("frozen_candidate")}
        result = select(Path(args.ads_repo), project, data.get("candidates", []))
    except (Unsafe, ValueError, TypeError, OSError, json.JSONDecodeError) as err:
        result = {"decision": "NO_SAFE_RECOMMENDATION", "effective_pin_changed": False,
                  "reason": str(err) if isinstance(err, Unsafe) else "PROJECT_OR_DISCOVERY_INPUT_UNAVAILABLE"}
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    return 0 if result["decision"] == "READ_ONLY_RECOMMENDATION" else 2


if __name__ == "__main__":
    sys.exit(main())
