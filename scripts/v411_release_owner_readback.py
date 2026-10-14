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
from urllib.request import HTTPRedirectHandler, Request, build_opener

REPOSITORY = "kaicreator-mm/ai-development-standard"
JOBS = ("J09", "J10", "J11", "J12")
PIN = re.compile(r"^[0-9a-f]{40}$")
COMMENT_URL = re.compile(r"^https://api\.github\.com/repos/kaicreator-mm/ai-development-standard/issues/comments/([1-9][0-9]*)$")
OWNER_EVENT = "VALIDATION_RESULT"  # existing event-v2 family, source-only witness
ALLOWED_OPERATOR_KINDS = frozenset(("chatgpt-web", "codex", "claude-code", "human", "github-actions", "woodpecker", "other"))


@dataclass(frozen=True)
class SourceWitness:
    status: str
    reason: str
    exact_subject: str
    observed_required_jobs: tuple[str, ...]
    proof_ids: tuple[int, ...] = ()
    release_gate_state: str = "BLOCKED"


class _RejectRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("unexpected redirect from pinned GitHub readback endpoint")


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
        # The default urllib redirect handler may forward Authorization across
        # origins. Disable redirect following BEFORE any redirect can disclose it.
        with build_opener(_RejectRedirect).open(req, timeout=12) as response:
            if response.geturl() != url or response.status != 200:
                raise ValueError("untrusted GitHub readback target")
            data = json.load(response)
        if not isinstance(data, dict):
            raise ValueError("GitHub comment is not an object")
        return data


def _event_fields(body: object) -> dict[str, str] | None:
    """Parse a bounded subset of canonical event-v2 YAML, never INI claims.

    This is still raw GitHub content. Only a separate owner-controlled
    canonical admission may decide trust beyond this source syntax witness.
    """
    marker = "<!-- ai-dev:event:v2 -->"
    if not isinstance(body, str) or not body.startswith(marker):
        return None
    tail = body[len(marker):].lstrip()
    if body.count("```yaml\n") > 1:
        return None
    if tail.startswith("```yaml\n"):
        block = tail.split("```yaml\n", 1)[1].split("\n```", 1)
        if len(block) != 2:
            return None
        tail = block[0]
    else:
        tail = tail.split("\n\n", 1)[0]
    result: dict[str, str] = {}
    for line in tail.splitlines():
        if not line or line.startswith("#"):
            continue
        if ": " not in line:
            return None
        key, value = line.split(": ", 1)
        if not re.fullmatch(r"[a-z][a-z0-9_]*", key) or key in result or not value.strip():
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
    # This P5 witness is specifically for material J09+J10+J11+J12.
    # Until a separately verified, owning inventory can prove applicability,
    # user-supplied declared/observed subsets CANNOT waive any member.
    if declared_jobs != valid_jobs or observed_jobs != valid_jobs:
        return hold("FOUR_WAY_OWNER_INVENTORY_NOT_VERIFIED")
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
        if fields is None or fields.get("event") != OWNER_EVENT:
            return hold(f"PROOF_UNADMITTED_EVENT_{job}")
        expected = {
            "schema": "ai-dev/event-v2", "event": OWNER_EVENT,
            "actor_role": "validator", "repository": REPOSITORY,
            "sha": subject, "gate": job, "status": "PASS",
            "owner_authority_ref": owner_authority_ref, "exit_code": "0",
        }
        if any(fields.get(k) != v for k, v in expected.items()):
            return hold(f"PROOF_STALE_OR_MISBOUND_{job}")
        # Validate all event-v2 VALIDATION_RESULT/PASS identity and scalar
        # requirements before considering it a source witness. This is a
        # strict bounded schema subset, not canonical event admission.
        required_event_fields = (
            "schema", "event", "actor_role", "operator_kind",
            "operator_id", "sha", "gate", "environment", "command",
            "exit_code", "evidence", "status", "requested_head_sha",
            "validation_profile", "actual_checked_out_sha", "provider_state",
        )
        if any(not fields.get(k) for k in required_event_fields):
            return hold(f"PROOF_SCHEMA_INVALID_{job}")
        if (fields.get("operator_kind") not in ALLOWED_OPERATOR_KINDS
                or fields.get("provider_state") != "AVAILABLE"
                or fields.get("requested_head_sha") != subject
                or fields.get("actual_checked_out_sha") != subject
                or PIN.fullmatch(fields.get("requested_head_sha", "")) is None
                or PIN.fullmatch(fields.get("actual_checked_out_sha", "")) is None
                or fields.get("exit_code") != "0"):
            return hold(f"PROOF_SCHEMA_INVALID_{job}")
        # Only an unquoted YAML integer scalar 0 is valid exit_code=0;
        # quoted "0"/'0' are strings and forbidden by event-v2 schema.
        if (fields.get("currentness") != "CURRENT"
                or fields.get("operator_id", "").startswith(("{", "["))
                or fields.get("evidence", "").startswith(("{", "["))):
            return hold(f"PROOF_CURRENTNESS_UNKNOWN_{job}")
        verified.append(comment_id)
    return SourceWitness(
        "SOURCE_ONLY_OWNER_REVIEW_REQUIRED",
        "GitHub comments read back; Release owner must separately verify "
        "authority, materiality, revocation, conflicts and gate applicability",
        subject, required, tuple(verified), "BLOCKED",
    )
