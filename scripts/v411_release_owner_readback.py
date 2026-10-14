"""Read-only GitHub source witness for v4.11 Release owner proof.

NOT a Release owner, gate arbiter, policy engine, or writer. A passing source
witness never means Release PASS or current gate applicability. No mutation,
human authority, or owner decision can be created by this module.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import os
import re
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPOSITORY = "kaicreator-mm/ai-development-standard"
JOBS = ("J09", "J10", "J11", "J12")
PIN = re.compile(r"^[0-9a-f]{40}$")
COMMENT_URL = re.compile(r"^https://api\.github\.com/repos/kaicreator-mm/ai-development-standard/issues/comments/([1-9][0-9]*)$")
OWNER_EVENT = "VALIDATION_RESULT"  # existing event-v2 family, source-only witness


@dataclass(frozen=True)
class SourceWitness:
    status: str
    reason: str
    exact_subject: str
    observed_required_jobs: tuple[str, ...]
    proof_ids: tuple[int, ...] = ()
    release_gate_state: str = "BLOCKED"


class GitHubCommentReader:
    """Fetch existing durable GitHub facts; never write or infer role grants."""

    def __init__(self, token: str | None = None):
        self._token = token if token is not None else os.getenv("GITHUB_TOKEN", "")

    def __call__(self, comment_id: int) -> dict:
        if type(comment_id) is not int or comment_id <= 0:
            raise ValueError("invalid GitHub comment ID")
        url = f"https://api.github.com/repos/{REPOSITORY}/issues/comments/{comment_id}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "ads-v411-readonly-owner-witness",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        req = Request(url, headers=headers, method="GET")
        with urlopen(req, timeout=12) as response:
            if response.geturl() != url or response.status != 200:
                raise ValueError("untrusted GitHub readback target")
            data = json.load(response)
        if not isinstance(data, dict):
            raise ValueError("GitHub comment is not an object")
        return data


def _event_fields(body: object) -> dict[str, str] | None:
    """Parse exactly one unquoted event block, reject duplicate/invalid keys."""
    if not isinstance(body, str) or not body.startswith("<!-- ai-dev:event:v2 -->"):
        return None
    if body.count("```ini\n") != 1:
        return None
    block = body.split("```ini\n", 1)[1].split("\n```", 1)
    if len(block) != 2:
        return None
    result: dict[str, str] = {}
    for line in block[0].splitlines():
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            return None
        key, value = line.split("=", 1)
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", key) or key in result or not value.strip():
            return None
        result[key] = value.strip()
    return result


def inspect_current_owner_proofs(
    *,
    subject: str,
    declared_jobs: set[str],
    observed_jobs: set[str] | None,
    proof_urls: dict[str, str],
    owner_login: str | None,
    owner_authority_ref: str | None,
    reader: Callable[[int], dict] | None = None,
) -> SourceWitness:
    """Conservative readback only; never an admission or Release verdict.

    owner_login and owner_authority_ref MUST be bound by separate Release
    authority. Their caller-supplied values do not by themselves confer an
    owner role; source success still requires later owning admission.
    """
    valid_jobs = set(JOBS)
    if not isinstance(declared_jobs, set) or not declared_jobs <= valid_jobs:
        return SourceWitness("BLOCKED", "INVALID_DECLARED_JOBS", subject, ())
    if observed_jobs is not None and not isinstance(observed_jobs, set):
        return SourceWitness("BLOCKED", "OBSERVED_MATERIALITY_UNKNOWN", subject, ())
    required = tuple(sorted(declared_jobs | (observed_jobs or set())))
    def hold(reason: str) -> SourceWitness:
        return SourceWitness("BLOCKED", reason, subject, required)
    if not isinstance(subject, str) or PIN.fullmatch(subject) is None:
        return hold("BAD_EXACT_SUBJECT")
    if not declared_jobs:
        return hold("INVALID_DECLARED_JOBS")
    if observed_jobs is None or not observed_jobs <= valid_jobs:
        return hold("OBSERVED_MATERIALITY_UNKNOWN")
    if not observed_jobs <= declared_jobs:
        return hold("OBSERVED_JOB_MISSING_FROM_DECLARATION")
    if not owner_login or not isinstance(owner_authority_ref, str) or not owner_authority_ref.strip():
        return hold("OWNER_AUTHORITY_UNVERIFIED")
    if not isinstance(proof_urls, dict):
        return hold("PROOF_REFS_MISSING")
    actual_reader = reader if reader is not None else GitHubCommentReader()
    verified: list[int] = []
    for job in required:
        url = proof_urls.get(job)
        match = COMMENT_URL.fullmatch(url) if isinstance(url, str) else None
        if match is None:
            return hold(f"PROOF_MISSING_OR_BAD_REF_{job}")
        comment_id = int(match.group(1))
        try:
            item = actual_reader(comment_id)
        except (ValueError, TypeError, KeyError, HTTPError, URLError, OSError):
            return hold(f"PROOF_READBACK_UNAVAILABLE_{job}")
        if (not isinstance(item, dict) or type(item.get("id")) is not int
                or item["id"] != comment_id or item.get("url") != url):
            return hold(f"PROOF_IDENTITY_MISMATCH_{job}")
        author = item.get("user")
        if not isinstance(author, dict) or author.get("login") != owner_login:
            return hold(f"PROOF_UNVERIFIED_OWNER_{job}")
        fields = _event_fields(item.get("body"))
        if fields is None or fields.get("EVENT") != OWNER_EVENT:
            return hold(f"PROOF_UNADMITTED_EVENT_{job}")
        expected = {
            "REPOSITORY": REPOSITORY, "EXACT_SUBJECT": subject,
            "JOB": job, "VERDICT": "PASS", "OWNER_AUTHORITY_REF": owner_authority_ref,
        }
        if any(fields.get(k) != v for k, v in expected.items()):
            return hold(f"PROOF_STALE_OR_MISBOUND_{job}")
        if fields.get("CURRENTNESS") != "CURRENT" or not fields.get("OWNER_PROOF_REF"):
            return hold(f"PROOF_CURRENTNESS_UNKNOWN_{job}")
        verified.append(comment_id)
    return SourceWitness(
        "SOURCE_ONLY_OWNER_REVIEW_REQUIRED",
        "GitHub comments read back; Release owner must separately verify "
        "authority, materiality, revocation, conflicts and gate applicability",
        subject, required, tuple(verified), "BLOCKED",
    )
