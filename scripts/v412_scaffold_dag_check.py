#!/usr/bin/env python3
"""ADS v4.12 read-only Scaffold↔DAG source-pair reference checker.

Only proves deterministic Git-object/source-contract predicates (E1).
It NEVER authenticates a GitHub Claim, approval, human action or Release Gate.
Run in a repository with --sf/--df pinned commit hashes. No network or writes.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HEX = re.compile(r"^[a-f0-9]{40}(?:[a-f0-9]{24})?$")
EXEMPT = {"DAG_ONLY_INPUT", "DERIVED_NONAUTHORITATIVE_OUTPUT", "FREEZE_RECORD_OUTPUT"}
FORBIDDEN_EXEMPT = (".github/", ".agent/", "src/", "lib/", "packages/", "schemas/", "scripts/")
FORBIDDEN_EXEMPT_NAMES = {"package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
                          "Cargo.lock", "pyproject.toml", "requirements.txt", "go.mod", "go.sum"}


class Reject(ValueError):
    """Source predicate failed; never imply a Gate/Release verdict."""


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def run_git(repo: Path, *args: str) -> bytes:
    # Keep all Git inputs fixed or validated; never run a shell.
    env = dict(os.environ)
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, env=env)
    if result.returncode:
        raise Reject("GIT_UNAVAILABLE_OR_INVALID_OBJECT:" + result.stderr.decode("utf-8", "replace")[:180])
    return result.stdout


def commit(repo: Path, oid: str) -> str:
    if not HEX.fullmatch(oid):
        raise Reject("UNPINNED_OR_INVALID_COMMIT")
    got = run_git(repo, "rev-parse", "--verify", oid + "^{commit}").strip().decode("ascii")
    if got != oid:
        raise Reject("COMMIT_IDENTITY_MISMATCH")
    return got


def tree(repo: Path, oid: str) -> dict[bytes, tuple[str, str, str]]:
    """Use raw Git NUL-delimited entries; tab/newline and non-UTF8 names are safe."""
    raw = run_git(repo, "ls-tree", "-r", "-z", "--full-tree", oid)
    entries = {}
    for rec in raw.split(b"\0"):
        if not rec:
            continue
        try:
            header, path = rec.split(b"\t", 1)
            mode, kind, blob = header.decode("ascii").split(" ")
            if path in entries or not path or path.startswith(b"/") or b"\0" in path:
                raise Reject("INVALID_OR_DUPLICATE_GIT_PATH")
            entries[path] = (mode, kind, blob)
        except (UnicodeError, ValueError) as error:
            raise Reject("INVALID_LS_TREE_RECORD") from error
    return entries


def path_bytes(value: str) -> bytes:
    if not isinstance(value, str) or not value or "\0" in value:
        raise Reject("INVALID_SCOPE_PATH")
    raw = value.encode("utf-8", "surrogateescape")
    if raw.startswith(b"/") or b".." in raw.split(b"/") or b"\\" in raw:
        raise Reject("UNSAFE_SCOPE_PATH")
    return raw


def json_at(repo: Path, revision: str, p: str, inventory: dict) -> dict:
    raw_path = path_bytes(p)
    if raw_path not in inventory:
        raise Reject("SOURCE_OBJECT_MISSING:" + p)
    if inventory[raw_path][0] != "100644":
        raise Reject("UNSUPPORTED_JSON_SOURCE_MODE")
    # Read blob object, not a shell-escaped path: correct for unusual filenames.
    raw = run_git(repo, "cat-file", "blob", inventory[raw_path][2])
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError) as e:
        raise Reject("INVALID_SOURCE_JSON") from e
    if not isinstance(data, dict):
        raise Reject("EXPECTED_JSON_OBJECT")
    return data


def source_inventory(tree_map: dict, excluded: set[bytes]) -> list[list[str]]:
    return [[base64.b64encode(p).decode("ascii"), *info]
            for p, info in sorted(tree_map.items()) if p not in excluded]


def validate_scope(scope: dict, sf_files: dict, scope_path: str) -> set[bytes]:
    if scope.get("schema") != "v412-sf-scope-v1":
        raise Reject("WRONG_SCOPE_SCHEMA")
    for field in ("product_blob", "l2_blob"):
        if not HEX.fullmatch(str(scope.get(field, ""))):
            raise Reject("MISSING_FROZEN_" + field)
    ignored = scope.get("exemptions", {})
    if not isinstance(ignored, dict):
        raise Reject("INVALID_EXEMPTIONS")
    excluded = set()
    for path, info in ignored.items():
        raw = path_bytes(path)
        if raw == path_bytes(scope_path) or not isinstance(info, dict):
            raise Reject("SCOPE_MANIFEST_CANNOT_EXEMPT_SELF")
        if info.get("role") not in EXEMPT:
            raise Reject("UNAPPROVED_ROLE_CLASS")
        if not HEX.fullmatch(str(info.get("approved_l2_blob", ""))) or info["approved_l2_blob"] != scope["l2_blob"]:
            raise Reject("EXEMPTION_WITHOUT_FROZEN_L2_REFERENCE")
        if not info.get("approval_ref") or not isinstance(info["approval_ref"], str):
            raise Reject("EXEMPTION_WITHOUT_SOURCE_OWNER_REFERENCE")
        if path in FORBIDDEN_EXEMPT_NAMES or path.startswith(FORBIDDEN_EXEMPT) or path.endswith((".lock", ".symlink")):
            raise Reject("EXEMPTION_MAY_HIDE_MATERIAL_SOURCE")
        # An exact path may be declared for a future DF/record output not yet in SF.
        excluded.add(raw)
    return excluded


def anchors_and_binding(scope: dict, bind: dict, df_files: dict) -> dict:
    if bind.get("schema") != "v412-df-binding-v1":
        raise Reject("WRONG_DF_SCHEMA")
    if any(field in bind for field in ("df_blob", "mi_digest", "pair_record")):
        raise Reject("SELF_REFERENTIAL_DF_INPUT")
    anchors = scope.get("anchors", [])
    writers = bind.get("writers", [])
    if not isinstance(anchors, list) or not isinstance(writers, list):
        raise Reject("INVALID_ANCHORS_OR_WRITERS")
    aid_to_anchor = {}
    for a in anchors:
        if not isinstance(a, dict) or any(not a.get(k) for k in ("anchor_id", "kind", "location", "contract_ref")):
            raise Reject("INCOMPLETE_STRUCTURAL_ANCHOR")
        aid = str(a["anchor_id"])
        if aid in aid_to_anchor or path_bytes(a["location"]) not in df_files:
            raise Reject("DUPLICATE_OR_DANGLING_ANCHOR")
        aid_to_anchor[aid] = a
    forward, reverse = {}, {}
    for w in writers:
        if not isinstance(w, dict) or not isinstance(w.get("task_id"), str):
            raise Reject("INVALID_WRITER_IDENTITY")
        aid, task = w.get("anchor_id"), w["task_id"]
        if aid not in aid_to_anchor or aid in forward or not isinstance(w.get("issue"), int) or w["issue"] < 1:
            raise Reject("DUPLICATE_OR_UNBOUND_WRITER")
        allowed, forbidden, paths = (w.get(k) for k in ("issue_allowed", "issue_forbidden", "writer_paths"))
        if not all(isinstance(x, list) for x in (allowed, forbidden, paths)):
            raise Reject("MISSING_ISSUE_WRITE_SCOPE")
        allowed_b, forbidden_b, paths_b = (set(map(path_bytes, x)) for x in (allowed, forbidden, paths))
        if not paths_b or not paths_b <= allowed_b or paths_b & forbidden_b:
            raise Reject("WRITER_SCOPE_OUTSIDE_CANONICAL_ISSUE")
        if w.get("claim_ref") is None:
            raise Reject("MISSING_CLAIM_REFERENCE")
        forward[aid] = {"task_id": task, "issue": w["issue"], "writer_paths": sorted(paths)}
        reverse.setdefault(task, []).append(aid)
    if set(forward) != set(aid_to_anchor):
        raise Reject("IMPORTANT_ANCHOR_WITHOUT_WRITER")
    return {"anchor_to_task": dict(sorted(forward.items())),
            "task_to_anchors": {k: sorted(v) for k, v in sorted(reverse.items())}}


def evaluate(repo: Path, sf: str, df: str, scope_path: str, binding_path: str,
             record_path: str | None = None, derived_path: str | None = None) -> dict:
    sf_id, df_id = commit(repo, sf), commit(repo, df)
    sfiles, dfiles = tree(repo, sf_id), tree(repo, df_id)
    scope = json_at(repo, sf_id, scope_path, sfiles)
    exempt = validate_scope(scope, sfiles, scope_path)
    for changed in set(sfiles) | set(dfiles):
        if sfiles.get(changed) != dfiles.get(changed) and changed not in exempt:
            raise Reject("MATERIAL_SOURCE_DRIFT:" + base64.b64encode(changed).decode("ascii"))
    binding = json_at(repo, df_id, binding_path, dfiles)
    if path_bytes(binding_path) not in exempt:
        raise Reject("DF_INPUT_NOT_PREAPPROVED_AS_DAG_ONLY")
    if scope["exemptions"][binding_path]["role"] != "DAG_ONLY_INPUT":
        raise Reject("DF_BINDING_WRONG_EXEMPTION_ROLE")
    maps = anchors_and_binding(scope, binding, dfiles)
    sf_mv = digest(source_inventory(sfiles, exempt))
    current_mv = digest(source_inventory(dfiles, exempt))
    if current_mv != sf_mv:
        raise Reject("MATERIAL_VIEW_INCONSISTENT")
    df_blob = dfiles[path_bytes(binding_path)][2]
    mi_input = {"sf": sf_id, "sf_mv": sf_mv, "df_blob": df_blob,
                "product_blob": scope["product_blob"], "l2_blob": scope["l2_blob"],
                "maps": maps}
    mi = digest(mi_input)
    if derived_path:
        if path_bytes(derived_path) not in exempt or scope["exemptions"][derived_path]["role"] != "DERIVED_NONAUTHORITATIVE_OUTPUT":
            raise Reject("DERIVED_OUTPUT_NOT_PREAPPROVED")
        if json_at(repo, df_id, derived_path, dfiles) != maps:
            raise Reject("FORGED_OR_STALE_DERIVED_OUTPUT")
    if record_path:
        if path_bytes(record_path) not in exempt or scope["exemptions"][record_path]["role"] != "FREEZE_RECORD_OUTPUT":
            raise Reject("FREEZE_OUTPUT_NOT_PREAPPROVED")
        rec = json_at(repo, df_id, record_path, dfiles)
        if (rec.get("sf_commit"), rec.get("df_blob"), rec.get("mi_digest")) != (sf_id, df_blob, mi):
            raise Reject("STALE_OR_SELF_REFERENTIAL_FREEZE")
    return {"subject": {"sf_commit": sf_id, "df_commit": df_id, "sf_mv": sf_mv,
                         "df_blob": df_blob, "mi_digest": mi},
            "source_pair": "PASS_E1", "maps": maps,
            "external_authority": {"source_owner_approval": "NOT_VERIFIED_BY_OFFLINE_CHECKER",
                                   "github_claim": "NOT_RUN", "independent_review": "NOT_RUN",
                                   "release_e3": "NOT_RUN"},
            "warning": "PASS_E1 is not a GitHub Claim, Review or Release PASS"}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("repo", "sf", "df", "scope_path", "binding_path"):
        p.add_argument("--" + name.replace("_", "-"), required=True)
    p.add_argument("--record-path")
    p.add_argument("--derived-path")
    args = p.parse_args()
    try:
        result = evaluate(Path(args.repo), args.sf, args.df, args.scope_path,
                          args.binding_path, args.record_path, args.derived_path)
        print(json.dumps(result, ensure_ascii=True, sort_keys=True))
        return 0
    except (Reject, FileNotFoundError, OSError) as e:
        print(json.dumps({"source_pair": "FAIL_OR_UNKNOWN", "reason": str(e),
                          "github_claim": "NOT_RUN", "independent_review": "NOT_RUN",
                          "release_e3": "NOT_RUN"}, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
