#!/usr/bin/env python3
"""Validate the latest-only tagged ADS GitHub v2 document; never mutate GitHub."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from test_protocol_schemas import load_schema, validate_subset

MARKER = "<!-- ads:github:v2 -->"
LEGACY = ("<!-- ai-dev:event:v2 -->", "<!-- ads:task-report:v1 -->", "<!-- ads:work-item:v1 -->", "<!-- ads:github-interaction:v1 -->")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
ISSUE = re.compile(r"^#[1-9][0-9]*$")
KIND_KEYS = {
    "type:version": ("version", "goal", "closure_criteria"),
    "type:planning": ("goal", "frozen_inputs", "acceptance"),
    "type:research": ("question", "scope", "acceptance"),
    "type:research-demo": ("hypothesis", "acceptance"),
    "type:task": (),
    "type:bug": ("observed_behavior", "expected_behavior", "acceptance"),
    "type:fix": ("observed_behavior", "expected_behavior", "acceptance"),
    "type:validation": ("target_sha", "validation_scope", "expected_checks"),
    "type:blocker": ("blocking_fact", "unblock_condition"),
    "type:release": ("version", "release_qualification"),
}
REPORT_KINDS = ("EXECUTION_SUMMARY", "TASK_LEARNING", "EVIDENCE_UPDATE", "EXECUTION_CORRECTION")


class ContractError(ValueError):
    pass


def scalar(s):
    if s.startswith(("!", "&", "*", "{", "[", "|", ">", "%", "@", "`")):
        raise ContractError("unsupported YAML tags/anchors/flow/multiline constructs")
    if s.startswith('"'):
        try:
            x = json.loads(s)
        except json.JSONDecodeError as exc:
            raise ContractError("invalid quoted YAML value") from exc
        if not isinstance(x, str):
            raise ContractError("expected quoted string")
        return x
    if s.startswith("'"):
        if len(s) < 2 or not s.endswith("'"):
            raise ContractError("unterminated YAML string")
        return s[1:-1].replace("''", "'")
    if s == "true": return True
    if s == "false": return False
    if s == "null": return None
    if re.fullmatch(r"-?(0|[1-9][0-9]*)", s): return int(s)
    if not s or ": " in s or " #" in s or s.endswith(":"):
        raise ContractError("empty/ambiguous YAML scalar; quote it")
    return s


def parse_yaml(text):
    """Strict small YAML profile: mapping + 2-space indents + scalar lists; no arbitrary YAML."""
    lines = []
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"): continue
        indent = len(line) - len(line.lstrip(" "))
        if "\t" in line or indent % 2 or indent > 40 or line.strip() in ("---", "..."):
            raise ContractError("noncanonical YAML indentation or document separator")
        lines.append((indent, line[indent:]))
    if not lines or lines[0][0]: raise ContractError("root YAML mapping required")

    def parse(pos, depth):
        if lines[pos][0] != depth: raise ContractError("unexpected YAML nesting")
        is_list = lines[pos][1].startswith("- ")
        result = [] if is_list else {}
        while pos < len(lines) and lines[pos][0] == depth:
            row = lines[pos][1]
            if is_list:
                if not row.startswith("- ") or row == "- ":
                    raise ContractError("bounded YAML lists contain only scalars")
                result.append(scalar(row[2:].strip()))
                pos += 1
            else:
                m = re.fullmatch(r"([a-z][a-z0-9_]*):(?: (.*))?", row)
                if not m: raise ContractError("unsupported YAML map key or mapping/list mix")
                key, value = m.groups()
                if key in result: raise ContractError("duplicate key: " + key)
                pos += 1
                if value is None or value == "":
                    if pos == len(lines) or lines[pos][0] != depth + 2:
                        raise ContractError("missing nested YAML value: " + key)
                    item, pos = parse(pos, depth + 2)
                else:
                    item = scalar(value)
                result[key] = item
            if pos < len(lines) and lines[pos][0] > depth:
                raise ContractError("unresolved indented YAML child")
        return result, pos

    value, end = parse(0, 0)
    if end != len(lines) or not isinstance(value, dict):
        raise ContractError("one root mapping only")
    return value


def check_schema(value, name):
    errors = validate_subset(value, load_schema(name))
    if errors:
        raise ContractError(name + ": " + "; ".join(errors[:6]))


def require(value, names):
    if not isinstance(value, dict):
        raise ContractError("expected a typed mapping")
    for key in names:
        if key not in value or value[key] is None or value[key] == "":
            raise ContractError("missing required field " + key)


def refs(value):
    if not isinstance(value, list) or not value or any(not isinstance(x, str) or not x for x in value):
        raise ContractError("expected nonempty durable evidence_refs list")


def work_item(data):
    require(data, ("profile", "contract"))
    profile, contract = data["profile"], data["contract"]
    if profile not in KIND_KEYS:
        raise ContractError("unsupported Work Item profile")
    if profile == "type:task":
        check_schema(contract, "task-contract.schema.json")
    else:
        require(contract, KIND_KEYS[profile])
        for key in ("acceptance", "expected_checks", "closure_criteria"):
            if key in contract:
                refs(contract[key])
    return "SHAPE_VALID_ONLY"


STATES = {"state:" + x for x in ("planned", "ready", "claimed", "implementing",
          "review-ready", "reviewing", "validation-needed", "validating",
          "changes-requested", "merge-ready", "blocked", "done", "superseded", "cancelled")}
CANONICAL = {
    "type": set(KIND_KEYS), "state": STATES,
    "review_policy": {"review:required", "review:recommended", "review:not-required"},
    "risk": {"risk:low", "risk:medium", "risk:high", "risk:critical"},
}
FORBIDDEN_TRUTH_LABELS = {"gate:pass", "gate:fail", "validation:passed",
                          "validation:failed", "validation:pass", "validation:fail"}


def intent(data):
    check_schema(data, "github-intent-v2.schema.json")
    op, target, change = data["operation"], data["target"], data["change"]
    issue, prior = target["issue"], data["expected_ref"]
    if op == "ISSUE_CREATE":
        if issue is not None or prior is not None:
            raise ContractError("create cannot claim an existing Issue/currentness")
    elif not isinstance(issue, str) or not ISSUE.fullmatch(issue) or not isinstance(prior, str) or not prior:
        raise ContractError("existing Issue mutation requires exact issue and currentness ref")

    if op in ("ISSUE_CREATE", "ISSUE_CONTRACT_UPDATE"):
        require(change, ("work_item",))
        work_item(change["work_item"])
        if op == "ISSUE_CONTRACT_UPDATE":
            require(change, ("previous_ref", "reason"))
    elif op == "ISSUE_METADATA_CHANGE":
        require(change, ("field", "before", "after"))
        field = change["field"]
        if field not in ("type", "state", "review_policy", "risk", "labels", "milestone", "title"):
            raise ContractError("unsupported native Issue metadata dimension")
        if field in CANONICAL and (change["before"] not in CANONICAL[field]
                                    or change["after"] not in CANONICAL[field]):
            raise ContractError("unknown canonical metadata vocabulary")
        if field == "labels":
            for name in ("before", "after"):
                value = change[name]
                if (not isinstance(value, list) or not all(isinstance(x, str) and x for x in value)
                    or len(value) != len(set(value)) or FORBIDDEN_TRUTH_LABELS.intersection(value)):
                    raise ContractError("invalid labels or unsupported Gate truth label")
        if change["before"] == change["after"]:
            raise ContractError("no-op metadata change")
    elif op == "ISSUE_DEPENDENCY_CHANGE":
        require(change, ("dependency", "action"))
        if (change["action"] not in ("ADD", "REMOVE") or
                not ISSUE.fullmatch(str(change["dependency"])) or
                change["dependency"] == issue):
            raise ContractError("invalid Issue dependency edge or self-loop")
    elif op in ("ISSUE_CLOSE", "ISSUE_REOPEN"):
        require(change, ("reason", "evidence_refs"))
        refs(change["evidence_refs"])
    else:
        raise ContractError("unsupported Issue operation")
    return "SHAPE_VALID_ONLY"


def event(data, repository=None, issue=None):
    check_schema(data, "agent-event-v2.schema.json")
    if issue:
        for name in ("task", "issue"):
            if name in data and data[name] != issue:
                raise ContractError("event target does not match actual Issue")
    return "SHAPE_VALID_ONLY"


def report(data):
    check_schema(data, "github-report-v2.schema.json")
    if data["report_kind"] == "EXECUTION_CORRECTION" and not data.get("corrects_ref"):
        raise ContractError("correction requires exact previous publication reference")
    if any(key in data["manifest_ref"].lower() for key in ("x-amz-signature=", "x-oss-signature=", "token=", "sig=")):
        raise ContractError("temporary signed URL/secret is not a durable report locator")
    return "SHAPE_VALID_ONLY"


CHECKS = {"work_item": work_item, "intent": intent, "event": event, "report": report}


def verify_markdown(source, expected_kind=None, *, repository=None, issue=None):
    lines = source.splitlines()
    first = next((x.strip() for x in lines if x.strip()), "")
    if first != MARKER:
        if first in LEGACY or any(x.strip() == MARKER for x in lines):
            raise ContractError("latest-only: unsupported old or non-leading structured marker")
        if expected_kind:
            raise ContractError("required latest-only structured document missing")
        return "UNSTRUCTURED_DISCUSSION"
    if not lines or lines[0].strip() != MARKER or sum(x.strip() == MARKER for x in lines) != 1:
        raise ContractError("exactly one first-line v2 marker required")
    for old in LEGACY:
        if any(x.strip() == old for x in lines):
            raise ContractError("mixed old/new marker prohibited")

    index = 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index >= len(lines) or lines[index].strip() != "```yaml":
        raise ContractError("expected exactly one fenced yaml mapping after marker")
    try:
        end = lines.index("```", index + 1)
    except ValueError as exc:
        raise ContractError("unclosed yaml block") from exc
    envelope = parse_yaml("\n".join(lines[index + 1:end]))
    check_schema(envelope, "github-document-v2.schema.json")
    kind, data = envelope["kind"], envelope["data"]
    if expected_kind and kind != expected_kind:
        raise ContractError("wrong kind for requested Issue surface")
    if kind == "event":
        return event(data, repository, issue)
    return CHECKS[kind](data)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file", type=Path)
    p.add_argument("--kind", choices=sorted(CHECKS))
    p.add_argument("--repository", help="actual GitHub repository for source-bound checks")
    p.add_argument("--issue", help="actual GitHub Issue number, e.g. #42")
    args = p.parse_args()
    try:
        result = verify_markdown(args.file.read_text(encoding="utf-8"), args.kind,
                                 repository=args.repository, issue=args.issue)
    except (ContractError, OSError) as exc:
        print("INVALID_SCHEMA: " + str(exc))
        raise SystemExit(1) from exc
    print(result + ": source/currentness/write admission must be verified by GitHub owner")


if __name__ == "__main__":
    main()
