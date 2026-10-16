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


def checked_event(blob: str) -> dict:
    if not isinstance(blob, str) or not blob.startswith("<!-- ai-dev:event:v2 -->\n"):
        raise Unsafe("INVALID_CANONICAL_EVENT")
    fields = {}
    for line in blob.splitlines()[1:]:
        m = re.fullmatch(r"([a-z_]+)=([^\r\n]+)", line)
        if m:
            key, value = m.groups()
            if key in fields or not value.strip():
                raise Unsafe("CONFLICTING_CANONICAL_EVENT")
            fields[key] = value
    return fields


def successful_run(fetch, run_id: str, sha: str) -> None:
    if not re.fullmatch(r"[1-9][0-9]*", str(run_id)):
        raise Unsafe("INVALID_EXECUTION_RUN_REF")
    run = fetch("https://api.github.com/repos/kaicreator-mm/ai-development-standard/actions/runs/" + str(run_id))
    if not isinstance(run, dict) or (run.get("id") != int(run_id)
            or run.get("head_sha") != sha or run.get("status") != "completed"
            or run.get("conclusion") != "success"):
        raise Unsafe("EXECUTED_GATE_NOT_PROVEN")


def qualified(repo: Path, sha: str, version: str, item: dict, fetch) -> str:
    """Published identity and Release gates are distinct from passing PR CI."""
    if not isinstance(item, dict) or not has_source_manifest(repo, sha):
        raise Unsafe("MISSING_SOURCE_MANIFEST")
    tag = "v" + version
    if (item.get("release_tag") != tag or
            git(repo, "rev-parse", "--verify", "refs/tags/" + tag + "^{commit}") != sha):
        raise Unsafe("UNPINNED_RELEASE_TAG")
    base = "https://api.github.com/repos/kaicreator-mm/ai-development-standard/"
    tag_obj = fetch(base + "git/ref/tags/" + tag)
    if (not isinstance(tag_obj, dict) or tag_obj.get("ref") != "refs/tags/" + tag
            or not isinstance(tag_obj.get("object"), dict)
            or tag_obj["object"].get("type") != "commit"
            or tag_obj["object"].get("sha") != sha):
        raise Unsafe("REMOTE_RELEASE_TAG_IDENTITY_UNVERIFIED")
    release = fetch(base + "releases/tags/" + tag)
    if (not isinstance(release, dict) or release.get("tag_name") != tag
            or release.get("draft") is not False or release.get("prerelease") is not False
            or release.get("target_commitish") != sha
            or not release.get("published_at") or not release.get("html_url")):
        raise Unsafe("PUBLISHED_RELEASE_IDENTITY_UNVERIFIED")
    issue_id, comment_id = item.get("qualification_issue"), item.get("qualification_comment")
    if type(issue_id) is not int or issue_id < 1 or type(comment_id) is not int or comment_id < 1:
        raise Unsafe("MISSING_QUALIFICATION_EVENT_REFERENCE")
    issue = fetch(base + f"issues/{issue_id}")
    if (not isinstance(issue, dict) or issue.get("number") != issue_id
            or issue.get("state") != "closed" or version not in str(issue.get("title", ""))):
        raise Unsafe("RELEASE_VERSION_NOT_CLOSED")
    event = fetch(base + f"issues/comments/{comment_id}")
    if (not isinstance(event, dict) or event.get("id") != comment_id
            or f"/issues/{issue_id}#issuecomment-{comment_id}" not in str(event.get("html_url", ""))):
        raise Unsafe("RELEASE_EVENT_OUTSIDE_CANONICAL_VERSION")
    facts = checked_event(event.get("body"))
    if (facts.get("event") != "RELEASE_QUALIFICATION"
            or facts.get("qualification") != "RELEASE_QUALIFIED"
            or facts.get("candidate_sha") != sha
            or facts.get("release_integrated_sha") != sha
            or facts.get("release_tag") != tag
            or facts.get("required_gate_results") != "PASS"
            or facts.get("actor_role") != "release-controller"
            or any(not facts.get(k) for k in ("operator_id", "session_ref", "operator_kind",
                                               "canonical_admission_ref", "gate_evidence_refs",
                                               "review_comment_id"))):
        raise Unsafe("UNVERIFIED_CURRENT_RELEASE_QUALIFICATION")
    m = re.fullmatch(r"actions:([1-9][0-9]*)", facts["gate_evidence_refs"])
    if not m:
        raise Unsafe("RELEASE_GATE_EXECUTION_REFERENCE_MISSING")
    successful_run(fetch, m.group(1), sha)
    rid = facts["review_comment_id"]
    if not re.fullmatch(r"[1-9][0-9]*", rid):
        raise Unsafe("MISSING_INDEPENDENT_RELEASE_REVIEW")
    review = fetch(base + "issues/comments/" + rid)
    if not isinstance(review, dict) or review.get("id") != int(rid):
        raise Unsafe("MISSING_INDEPENDENT_RELEASE_REVIEW")
    rf = checked_event(review.get("body"))
    if (rf.get("actor_role") != "reviewer" or rf.get("review_verdict") != "PASS"
            or rf.get("reviewed_sha") != sha
            or not rf.get("operator_id") or not rf.get("session_ref")
            or rf["operator_id"] == facts["operator_id"]
            or rf["session_ref"] == facts["session_ref"]):
        raise Unsafe("INDEPENDENT_RELEASE_REVIEW_NOT_PROVEN")
    return base + f"issues/comments/{comment_id}"


def compatible(repo: Path, item: dict, current: str, candidate: str,
               consumer_window: str, fetch) -> list[str]:
    """Git-source record + actual exact-subject executed per-dimension test jobs.

    JSON supplied directly by discovery is NOT an evidence authority.
    """
    path = item.get("compatibility_record_path")
    if (not isinstance(path, str) or not path.startswith("docs/compatibility/")
            or not path.endswith(".json")):
        raise Unsafe("COMPATIBILITY_SOURCE_NOT_PINNED")
    record = json.loads(at(repo, candidate, path))
    if (not isinstance(record, dict) or record.get("schema_version") != 1
            or not isinstance(record.get("baseline"), dict)
            or not isinstance(record.get("candidate"), dict)
            or record["baseline"].get("sha_or_digest") != current
            or record["candidate"].get("sha_or_digest") != candidate
            or not isinstance(record.get("change_operations"), list)
            or not record["change_operations"]
            or not isinstance(record.get("producer_refs"), list)
            or not record["producer_refs"]
            or not isinstance(record.get("consumer_refs"), list)
            or not record["consumer_refs"]):
        raise Unsafe("INVALID_SOURCE_COMPATIBILITY_RECORD")
    if (not isinstance(consumer_window, str) or not consumer_window
            or record.get("compatibility_window_ref") != consumer_window):
        raise Unsafe("UNSUPPORTED_OR_UNVERIFIED_CONSUMER_WINDOW")
    ds = record.get("dimensions")
    if not isinstance(ds, list) or len(ds) != len(REQUIRED_DIMENSIONS):
        raise Unsafe("MATERIAL_COMPATIBILITY_DIMENSIONS_MISSING")
    by_name = {}
    for dim in ds:
        if not isinstance(dim, dict) or not isinstance(dim.get("name"), str):
            raise Unsafe("BAD_COMPATIBILITY_DIMENSION")
        name = dim["name"]
        if name in by_name or name not in REQUIRED_DIMENSIONS:
            raise Unsafe("DUPLICATE_OR_UNKNOWN_COMPATIBILITY_DIMENSION")
        by_name[name] = dim
    if set(by_name) != REQUIRED_DIMENSIONS:
        raise Unsafe("MATERIAL_COMPATIBILITY_DIMENSIONS_MISSING")
    prefix = "https://api.github.com/repos/kaicreator-mm/ai-development-standard/"
    refs = []
    for name in sorted(REQUIRED_DIMENSIONS):
        dim = by_name[name]
        ev = dim.get("evidence_refs")
        if (dim.get("outcome") != "COMPATIBLE"
                or not isinstance(ev, list) or len(ev) != 1
                or not isinstance(ev[0], str)):
            raise Unsafe("MATERIAL_COMPATIBILITY_UNKNOWN_OR_UNPROVEN")
        m = re.fullmatch(r"actions:([1-9]\d*):([1-9]\d*)", ev[0])
        if not m:
            raise Unsafe("INDEPENDENT_COMPATIBILITY_PROOF_MISSING")
        run_id, job_id = m.groups()
        successful_run(fetch, run_id, candidate)
        job = fetch(prefix + "actions/jobs/" + job_id)
        if (not isinstance(job, dict) or job.get("id") != int(job_id)
                or job.get("run_id") != int(run_id)
                or job.get("status") != "completed"
                or job.get("conclusion") != "success"
                or job.get("name") != f"ads-compat:{current[:12]}:{name}"
                or not isinstance(job.get("steps"), list)
                or not any(
                    isinstance(st, dict)
                    and st.get("name") == f"probe:{current[:12]}:{name}:{consumer_window}"
                    and st.get("conclusion") == "success"
                    for st in job["steps"])):
            raise Unsafe("COMPATIBILITY_TEST_NOT_EXECUTED_ON_EXACT_SUBJECT")
        refs.append(ev[0])
    return refs


def live_project_state(project: dict, fetch) -> None:
    """GitHub live state, never discovery's inactive booleans, is authoritative."""
    repo = project.get("project_repository")
    if not isinstance(repo, str) or not REPO.fullmatch(repo):
        raise Unsafe("MISSING_VERIFIABLE_PROJECT_REPOSITORY")
    base = "https://api.github.com/repos/" + repo
    issues = fetch(base + "/issues?state=open&per_page=100")
    pulls = fetch(base + "/pulls?state=open&per_page=100")
    if (not isinstance(issues, list) or not isinstance(pulls, list)
            or len(issues) >= 100 or len(pulls) >= 100):
        raise Unsafe("UNKNOWN_PROJECT_LIVE_STATE_OR_PAGINATION")
    if pulls:
        raise Unsafe("ACTIVE_SUBJECT_CANNOT_REBIND")
    for issue in issues:
        if not isinstance(issue, dict) or not isinstance(issue.get("labels"), list):
            raise Unsafe("UNKNOWN_PROJECT_LIVE_STATE")
        labels = {label["name"] for label in issue["labels"]
                  if isinstance(label, dict) and isinstance(label.get("name"), str)}
        if (not labels or "type:task" in labels or "state:claimed" in labels
                or "state:implementing" in labels or "state:review-ready" in labels
                or issue.get("pull_request")):
            raise Unsafe("ACTIVE_OR_UNCLASSIFIED_WORK_ITEM")


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
    except (Unsafe, ValueError, KeyError, TypeError, AttributeError, IndexError, OSError, HTTPError, URLError, json.JSONDecodeError) as error:
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
