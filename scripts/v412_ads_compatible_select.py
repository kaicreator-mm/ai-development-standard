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
    if (not url.startswith("https://api.github.com/repos/kaicreator-mm/ai-development-standard/")
            and not re.fullmatch(r"https://api[.]github[.]com/repos/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/(?:(?:issues|pulls)[?]state=open&per_page=100|git/ref/heads/main)", url)):
        raise Unsafe("UNTRUSTED_READ_ONLY_GITHUB_API")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ADS-v412-read-only-selector"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urlopen(Request(url, headers=headers), timeout=8) as response:
        data = json.load(response)
    if not isinstance(data, (dict, list)):
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


def qualified_integrated_release(repo: Path, published: str, version: str,
                                 item: dict, facts: dict, issue_id: int,
                                 rq_id: int, fetch, base: str) -> None:
    """Actual S06: frozen candidate and published main differ in SHA, not tree."""
    frozen = exact_commit(repo, facts.get("candidate_sha", ""))
    tree = facts.get("candidate_tree", "")
    if (not SHA.fullmatch(tree) or frozen == published
            or not ancestor(repo, frozen, published)
            or git(repo, "rev-parse", frozen + "^{tree}") != tree
            or git(repo, "rev-parse", published + "^{tree}") != tree
            or at(repo, frozen, "VERSION") != version
            or facts.get("version") != version
            or facts.get("release_verdict") != "READY"
            or facts.get("required_gate_results") != "PASS"
            or facts.get("actor_role") != "release-controller"):
        raise Unsafe("PUBLISHED_RELEASE_LINEAGE_MISMATCH")

    def linked(key: str, expected: str) -> dict:
        m = re.fullmatch(r"#([1-9]\d*)@([1-9]\d*)", facts.get(key, ""))
        if not m or int(m.group(1)) != issue_id:
            raise Unsafe("PUBLISHED_RELEASE_EVIDENCE_REF_MISSING")
        ident = int(m.group(2))
        evidence = fetch(base + f"issues/comments/{ident}")
        if (not isinstance(evidence, dict) or evidence.get("id") != ident
                or f"/issues/{issue_id}#issuecomment-{ident}" not in str(evidence.get("html_url", ""))):
            raise Unsafe("PUBLISHED_RELEASE_EVIDENCE_REF_STALE")
        fields = checked_event(evidence.get("body", ""))
        if fields.get("event") != expected or fields.get("candidate_sha") != frozen:
            raise Unsafe("PUBLISHED_RELEASE_EVIDENCE_SUBJECT_MISMATCH")
        return fields

    gate = linked("gate_applicability_ref", "ADS_V412_S06_VERSION_VISIBLE_GATE_APPLICABILITY")
    freeze = linked("candidate_freeze_ref", "ADS_V412_S06_CANDIDATE_FROZEN")
    closure = linked("final_closeout_ref", "ADS_V412_S06_FINAL_CLOSEOUT")
    if (gate.get("candidate_tree") != tree
            or gate.get("source_consistency_result") != "PASS"
            or gate.get("self_dogfood_result") != "PASS_SOURCE_PROCESS_SCOPE"
            or gate.get("full_visible_regression_result") != "PASS_CURRENT_HEAD"
            or freeze.get("candidate_tree") != tree
            or freeze.get("freeze_state") != "FROZEN_OPERATIVE"
            or closure.get("candidate_tree") != tree
            or closure.get("closeout") != "READY_FOR_RELEASE_QUALIFICATION"):
        raise Unsafe("PUBLISHED_RELEASE_SOURCE_GATE_UNPROVEN")

    def real_ci(run_id: str, sha: str) -> None:
        if not re.fullmatch(r"[1-9]\d*", str(run_id)):
            raise Unsafe("PUBLISHED_RELEASE_CI_MISSING")
        successful_run(fetch, run_id, sha)
        executed = fetch(base + "actions/runs/" + run_id)
        if not isinstance(executed, dict) or executed.get("name") != "verify-standard":
            raise Unsafe("PUBLISHED_RELEASE_CI_NOT_STANDARD_VERIFIER")

    real_ci(gate.get("current_version_ci_run"), frozen)
    if gate.get("current_version_ci_run") != facts.get("exact_ci_run"):
        raise Unsafe("PUBLISHED_RELEASE_CI_SUBJECT_MISMATCH")

    reviewer = re.fullmatch(r"PR([1-9]\d*)_COMMENTED_PASS_ON_IDENTICAL_TREE",
                            facts.get("candidate_source_review", ""))
    if not reviewer:
        raise Unsafe("PUBLISHED_RELEASE_SOURCE_REVIEW_MISSING")
    reviews = fetch(base + "pulls/" + reviewer.group(1) + "/reviews?per_page=100")
    if not isinstance(reviews, list) or len(reviews) >= 100:
        raise Unsafe("PUBLISHED_RELEASE_SOURCE_REVIEW_UNKNOWN")
    reviewed = False
    for entry in reviews:
        if not isinstance(entry, dict) or entry.get("state") != "COMMENTED":
            continue
        fields = checked_event(entry.get("body", ""))
        reviewed_head = fields.get("reviewed_head", "")
        if (fields.get("source_review_verdict") == "PASS"
                and fields.get("review_subject") == "PR_" + reviewer.group(1)
                and SHA.fullmatch(reviewed_head)
                and git(repo, "rev-parse", reviewed_head + "^{tree}") == tree
                and fields.get("operator_id")
                and fields["operator_id"] != facts.get("operator_id")):
            reviewed = True
            break
    if not reviewed:
        raise Unsafe("PUBLISHED_RELEASE_SOURCE_REVIEW_UNPROVEN")

    integration_id = item.get("integration_comment")
    if type(integration_id) is not int or integration_id < 1:
        raise Unsafe("PUBLISHED_RELEASE_INTEGRATION_REF_MISSING")
    event = fetch(base + f"issues/comments/{integration_id}")
    if (not isinstance(event, dict) or event.get("id") != integration_id
            or f"/issues/{issue_id}#issuecomment-{integration_id}" not in str(event.get("html_url", ""))):
        raise Unsafe("PUBLISHED_RELEASE_INTEGRATION_NOT_ON_VERSION")
    integrated = checked_event(event.get("body", ""))
    if (integrated.get("event") != "ADS_V412_S06_RELEASE_INTEGRATED_BASELINE"
            or integrated.get("frozen_candidate_sha") != frozen
            or integrated.get("final_main_sha") != published
            or integrated.get("final_main_tree") != tree
            or integrated.get("release_qualification") != f"#{issue_id}@{rq_id}_READY"
            or integrated.get("tree_equivalence") != "CANDIDATE_EQUALS_MAIN"):
        raise Unsafe("PUBLISHED_RELEASE_INTEGRATION_UNVERIFIED")
    merge = re.fullmatch(r"#([1-9]\d*)_MERGED", integrated.get("main_integration_pr", ""))
    if not merge:
        raise Unsafe("PUBLISHED_RELEASE_MERGE_MISSING")
    native = fetch(base + "pulls/" + merge.group(1))
    if (not isinstance(native, dict) or not native.get("merged_at")
            or native.get("merge_commit_sha") != published):
        raise Unsafe("PUBLISHED_RELEASE_MERGE_UNVERIFIED")
    main_run = re.fullmatch(r"([1-9]\d*)_COMPLETED_SUCCESS",
                            integrated.get("post_main_ci", ""))
    if not main_run:
        raise Unsafe("PUBLISHED_RELEASE_MAIN_CI_MISSING")
    real_ci(main_run.group(1), published)


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
            or issue.get("state") != "closed"):
        raise Unsafe("RELEASE_VERSION_NOT_CLOSED")
    event = fetch(base + f"issues/comments/{comment_id}")
    if (not isinstance(event, dict) or event.get("id") != comment_id
            or f"/issues/{issue_id}#issuecomment-{comment_id}" not in str(event.get("html_url", ""))):
        raise Unsafe("RELEASE_EVENT_OUTSIDE_CANONICAL_VERSION")
    facts = checked_event(event.get("body"))
    # The actual canonical S06 issue is titled "v4.12", not "v4.12.0".
    # Its trusted exact patch version comes from the bound qualification event.
    title = str(issue.get("title", ""))
    family = "v" + version.rsplit(".", 1)[0]
    if (version not in title and not (
            facts.get("candidate_tree") is not None
            and family in title and facts.get("version") == version)):
        raise Unsafe("RELEASE_VERSION_NOT_CLOSED")
    if (facts.get("event") != "RELEASE_QUALIFICATION"
            or facts.get("qualification") != "RELEASE_QUALIFIED"):
        raise Unsafe("UNVERIFIED_CURRENT_RELEASE_QUALIFICATION")
    if facts.get("candidate_tree") is not None:
        qualified_integrated_release(repo, sha, version, item, facts, issue_id,
                                     comment_id, fetch, base)
        return base + f"issues/comments/{comment_id}"
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
    # An arbitrary nonempty "admission" string is not a canonical accepted
    # freeze. Read its actual existing Issue comment and exact source subject.
    admitted_ref = re.fullmatch(r"#([1-9]\d*)@([1-9]\d*)",
                                facts["canonical_admission_ref"])
    if not admitted_ref or int(admitted_ref.group(1)) != issue_id:
        raise Unsafe("CANONICAL_RELEASE_ADMISSION_NOT_ACCEPTED")
    admission_id = int(admitted_ref.group(2))
    admission = fetch(base + f"issues/comments/{admission_id}")
    if (not isinstance(admission, dict) or admission.get("id") != admission_id
            or f"/issues/{issue_id}#issuecomment-{admission_id}" not in str(admission.get("html_url", ""))):
        raise Unsafe("CANONICAL_RELEASE_ADMISSION_NOT_ACCEPTED")
    admitted = checked_event(admission.get("body", ""))
    if (admitted.get("event") != "RELEASE_CANDIDATE_ADMISSION"
            or admitted.get("candidate_sha") != sha
            or admitted.get("admission") != "ACCEPTED"):
        raise Unsafe("CANONICAL_RELEASE_ADMISSION_NOT_ACCEPTED")
    # Resolve the applicability matrix admitted for THIS exact candidate.
    # Text "required_gate_results=PASS" and one arbitrary green PR run do not
    # establish the two standards-only Release closure obligations.
    required = ("SOURCE_CONSISTENCY", "SELF_DOGFOOD")
    if admitted.get("required_gate_ids") != ";".join(required):
        raise Unsafe("REQUIRED_RELEASE_APPLICABILITY_NOT_ADMITTED")
    decisions = facts.get("gate_decision_refs", "").split(";")
    if len(decisions) != len(required):
        raise Unsafe("REQUIRED_RELEASE_GATE_DECISIONS_MISSING")
    for gate, ref in zip(required, decisions):
        mdec = re.fullmatch(r"([A-Z_]+):#([1-9]\d*)@([1-9]\d*)", ref)
        if not mdec or mdec.group(1) != gate or int(mdec.group(2)) != issue_id:
            raise Unsafe("REQUIRED_RELEASE_GATE_DECISIONS_MISSING")
        did = int(mdec.group(3))
        decision = fetch(base + f"issues/comments/{did}")
        if (not isinstance(decision, dict) or decision.get("id") != did
                or f"/issues/{issue_id}#issuecomment-{did}" not in str(decision.get("html_url", ""))):
            raise Unsafe("REQUIRED_RELEASE_GATE_DECISIONS_MISSING")
        gatefacts = checked_event(decision.get("body", ""))
        if (gatefacts.get("event") != "RELEASE_GATE_DECISION"
                or gatefacts.get("gate_id") != gate
                or gatefacts.get("candidate_sha") != sha
                or gatefacts.get("decision") != "PASS"):
            raise Unsafe("REQUIRED_RELEASE_GATE_NOT_PASSED")
        proof = re.fullmatch(r"actions:([1-9]\d*):([1-9]\d*)",
                             gatefacts.get("proof_ref", ""))
        if not proof:
            raise Unsafe("REQUIRED_RELEASE_GATE_PROOF_MISSING")
        run_id, job_id = proof.groups()
        successful_run(fetch, run_id, sha)
        gatejob = fetch(base + "actions/jobs/" + job_id)
        if (not isinstance(gatejob, dict)
                or gatejob.get("id") != int(job_id)
                or gatejob.get("run_id") != int(run_id)
                or gatejob.get("status") != "completed"
                or gatejob.get("conclusion") != "success"
                or gatejob.get("name") != "ads-release:" + gate
                or not isinstance(gatejob.get("steps"), list)
                or not any(isinstance(st, dict)
                           and st.get("name") == "release-proof:" + gate + ":" + sha
                           and st.get("conclusion") == "success"
                           for st in gatejob["steps"])):
            raise Unsafe("REQUIRED_RELEASE_GATE_PROOF_NOT_EXECUTED")
    m = re.fullmatch(r"actions:([1-9][0-9]*)", facts["gate_evidence_refs"])
    if not m:
        raise Unsafe("RELEASE_GATE_EXECUTION_REFERENCE_MISSING")
    successful_run(fetch, m.group(1), sha)
    rid = facts["review_comment_id"]
    if not re.fullmatch(r"[1-9][0-9]*", rid):
        raise Unsafe("MISSING_INDEPENDENT_RELEASE_REVIEW")
    review = fetch(base + "issues/comments/" + rid)
    if (not isinstance(review, dict) or review.get("id") != int(rid)
            or f"/issues/{issue_id}#issuecomment-{rid}" not in str(review.get("html_url", ""))):
        raise Unsafe("MISSING_INDEPENDENT_RELEASE_REVIEW")
    rf = checked_event(review.get("body"))
    if (rf.get("event") != "INDEPENDENT_RELEASE_REVIEW"
            or rf.get("review_subject") != "S06_RELEASE_QUALIFICATION"
            or rf.get("actor_role") != "reviewer" or rf.get("review_verdict") != "PASS"
            or rf.get("reviewed_sha") != sha
            or not rf.get("operator_id") or not rf.get("session_ref")
            or rf["operator_id"] == facts["operator_id"]
            or rf["session_ref"] == facts["session_ref"]):
        raise Unsafe("INDEPENDENT_RELEASE_REVIEW_NOT_PROVEN")
    return base + f"issues/comments/{comment_id}"


def compatible(repo: Path, item: dict, current: str, candidate: str,
               consumer_repo: str, consumer_window: str, fetch) -> list[str]:
    """Git-source record + actual exact-subject executed per-dimension test jobs.

    JSON supplied directly by discovery is NOT an evidence authority.
    """
    path = item.get("compatibility_record_path")
    if (not isinstance(path, str) or not path.startswith("docs/compatibility/")
            or not path.endswith(".json")):
        raise Unsafe("COMPATIBILITY_SOURCE_NOT_PINNED")
    # Compatibility records carry candidate SHA and therefore cannot live
    # inside the same self-referential candidate commit. Pin a distinct exact
    # successor evidence commit containing that record (S02 cycle-free rule).
    evidence_sha = exact_commit(repo, item.get("compatibility_source_sha", ""))
    if not ancestor(repo, candidate, evidence_sha):
        raise Unsafe("COMPATIBILITY_PROOF_NOT_FROM_CANDIDATE_LINEAGE")
    record = json.loads(at(repo, evidence_sha, path))
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
    if (not isinstance(consumer_repo, str) or not REPO.fullmatch(consumer_repo)
            or record["consumer_refs"] != [consumer_repo]
            or record["producer_refs"] != ["kaicreator-mm/ai-development-standard"]):
        raise Unsafe("CONSUMER_IDENTITY_NOT_TESTED")
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
    # Bind every probe to the actual local project repository, not merely to a
    # reused support-window label shared by unrelated consumers.
    consumer_key = consumer_repo.replace("/", "__")
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
                or job.get("name") != f"ads-compat:{current[:12]}:{consumer_key}:{name}"
                or not isinstance(job.get("steps"), list)
                or not any(
                    isinstance(st, dict)
                    and st.get("name") == f"probe:{current[:12]}:{consumer_key}:{name}:{consumer_window}"
                    and st.get("conclusion") == "success"
                    for st in job["steps"])):
            raise Unsafe("COMPATIBILITY_TEST_NOT_EXECUTED_ON_EXACT_SUBJECT")
        refs.append(ev[0])
    return refs


def live_project_state(project: dict, fetch) -> None:
    """Conjunct a locally source-pinned checkpoint with current GitHub truth.

    Discovery JSON is never evidence that a Claim or frozen candidate is absent.
    This strict optional advisory may decline projects lacking an adoption state
    snapshot. It does not add a Task or Gate to their normal development.
    """
    repo_name = project.get("project_repository")
    project_root = project.get("project_root")
    if (not isinstance(repo_name, str) or not REPO.fullmatch(repo_name)
            or not isinstance(project_root, (str, Path)) or not str(project_root)):
        raise Unsafe("MISSING_VERIFIABLE_PROJECT_REPOSITORY")
    root = Path(project_root)
    if git(root, "status", "--porcelain"):
        raise Unsafe("PROJECT_WORKTREE_NOT_CLEAN")
    if git(root, "branch", "--show-current") != "main":
        raise Unsafe("PROJECT_CHECKPOINT_NOT_MAIN")
    current_head = exact_commit(root, git(root, "rev-parse", "HEAD"))
    prior = exact_commit(root, git(root, "rev-parse", "HEAD^"))
    # The adoption checkpoint itself is the exact latest source commit; the
    # event binds its predecessor, avoiding self-referential SHA literals.
    if ".dev-standard/ADOPTION_STATUS.json" not in git(
        root, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"
    ).splitlines():
        raise Unsafe("PROJECT_CHECKPOINT_NOT_CURRENT")
    try:
        status = json.loads(at(root, current_head, ".dev-standard/ADOPTION_STATUS.json"))
    except (ValueError, TypeError) as error:
        raise Unsafe("PROJECT_CHECKPOINT_INVALID") from error
    if (not isinstance(status, dict) or status.get("schema_version") != 1
            or status.get("project_repository") != repo_name
            or status.get("checked_parent_sha") != prior
            or status.get("effective_ads_revision") != project.get("current_revision")
            or status.get("active_claim") != "NONE"
            or status.get("frozen_candidate") != "NONE"):
        raise Unsafe("ACTIVE_FROZEN_OR_UNVERIFIED_CHECKPOINT")
    prefix = "https://api.github.com/repos/" + repo_name
    remote = fetch(prefix + "/git/ref/heads/main")
    if (not isinstance(remote, dict) or remote.get("ref") != "refs/heads/main"
            or not isinstance(remote.get("object"), dict)
            or remote["object"].get("type") != "commit"
            or remote["object"].get("sha") != current_head):
        raise Unsafe("PROJECT_REMOTE_CHECKPOINT_STALE")
    issues = fetch(prefix + "/issues?state=open&per_page=100")
    pulls = fetch(prefix + "/pulls?state=open&per_page=100")
    if (not isinstance(issues, list) or not isinstance(pulls, list)
            or len(issues) >= 100 or len(pulls) >= 100):
        raise Unsafe("UNKNOWN_PROJECT_LIVE_STATE_OR_PAGINATION")
    # Do not guess the Task type from labels: project-specific labels may vary.
    # Any open Issue/PR makes the advisory wait for a project-local checkpoint.
    if pulls or issues:
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
        # Source checkpoint and live GitHub currentness are required; discovery
        # booleans are ignored even when they claim "false".
        live_project_state(project, fetch)
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
            refs = compatible(repo, item, current, sha, project.get("project_repository"),
                              project.get("consumer_window"), fetch)
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
        origin = git(project_root, "remote", "get-url", "origin")
        match = re.fullmatch(
            r"(?:https://github[.]com/|git@github[.]com:)([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:[.]git)?",
            origin,
        )
        if not match:
            raise Unsafe("UNVERIFIED_PROJECT_GIT_REMOTE")
        window = re.search(r"(?m)^ads_consumer_window=([^\s]+)\s*$", overrides)
        project = {"preference": opted.group(1) if opted else "PINNED/MANUAL",
                   "current_revision": pin["revision"], "current_version": pin["version"],
                   "project_repository": match.group(1),
                   "project_root": project_root,
                   "consumer_window": window.group(1) if window else None}
        result = select(Path(args.ads_repo), project, data.get("candidates", []))
    except (Unsafe, ValueError, TypeError, OSError, json.JSONDecodeError) as err:
        result = {"decision": "NO_SAFE_RECOMMENDATION", "effective_pin_changed": False,
                  "reason": str(err) if isinstance(err, Unsafe) else "PROJECT_OR_DISCOVERY_INPUT_UNAVAILABLE"}
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    return 0 if result["decision"] == "READ_ONLY_RECOMMENDATION" else 2


if __name__ == "__main__":
    sys.exit(main())
