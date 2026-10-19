#!/usr/bin/env python3
"""Check ADS tagged Markdown/YAML against existing schemas; never admit GitHub mutations."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from test_protocol_schemas import load_schema, validate_subset

MARKERS = {"<!-- ads:github-interaction:v1 -->": "intent",
           "<!-- ads:work-item:v1 -->": "work-item",
           "<!-- ai-dev:event:v2 -->": "event-v2",
           "<!-- ads:task-report:v1 -->": "report-v1"}
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
    if errors: raise ContractError(name + ": " + "; ".join(errors[:6]))


def require(obj, names):
    if not isinstance(obj, dict):
        raise ContractError("payload must be a mapping")
    for name in names:
        if name not in obj or obj[name] is None or obj[name] == "":
            raise ContractError("missing required field " + name)


def check_work_item(obj):
    check_schema(obj, "github-work-item-document-v1.schema.json")
    kind, contract = obj["work_item_type"], obj["contract"]
    if kind == "type:task":
        check_schema(contract, "task-contract.schema.json")
    else:
        require(contract, KIND_KEYS[kind])
        for key in ("acceptance", "expected_checks", "closure_criteria"):
            if key in contract and (not isinstance(contract[key], list) or not contract[key]):
                raise ContractError(key + ": nonempty list required")


def check_intent(obj):
    check_schema(obj, "github-structured-interaction-v1.schema.json")
    op, target, payload = obj["operation"], obj["target"], obj["payload"]
    if op == "ISSUE_CREATE":
        if target["issue_ref"] is not None or obj["expected_source_ref"] is not None:
            raise ContractError("ISSUE_CREATE must not claim existing Issue/currentness")
    else:
        if not isinstance(target["issue_ref"], str) or not ISSUE.fullmatch(target["issue_ref"]):
            raise ContractError("exact Issue required")
        if not isinstance(obj["expected_source_ref"], str) or not obj["expected_source_ref"]:
            raise ContractError("source-currentness precondition ref required")

    if op in ("ISSUE_CREATE", "ISSUE_CONTRACT_UPDATE"):
        require(payload, ("work_item",))
        check_work_item(payload["work_item"])
        if op == "ISSUE_CONTRACT_UPDATE":
            require(payload, ("previous_contract_ref", "change_reason"))
    elif op == "ISSUE_METADATA_CHANGE":
        require(payload, ("field", "before", "after"))
        vocab = {
          "type": set(KIND_KEYS),
          "state": {"state:" + v for v in ("planned", "ready", "claimed", "implementing", "review-ready",
                "reviewing", "validation-needed", "validating", "changes-requested", "merge-ready",
                "blocked", "done", "superseded", "cancelled")},
          "review_policy": {"review:required", "review:recommended", "review:not-required"},
          "risk": {"risk:low", "risk:medium", "risk:high", "risk:critical"},
        }
        field = payload["field"]
        if field not in (*vocab.keys(), "labels", "milestone", "title"):
            raise ContractError("unrecognized native metadata field")
        if field in vocab and (payload["before"] not in vocab[field] or payload["after"] not in vocab[field]):
            raise ContractError("illegal metadata vocabulary")
        if field == "labels" and (not isinstance(payload["before"], list) or not isinstance(payload["after"], list)):
            raise ContractError("before/after labels must be lists")
        if payload["before"] == payload["after"]:
            raise ContractError("no-op change")
    elif op == "ISSUE_DEPENDENCY_CHANGE":
        require(payload, ("dependency_issue_ref", "change"))
        if (payload["change"] not in ("ADD", "REMOVE")
            or not ISSUE.fullmatch(str(payload["dependency_issue_ref"]))
            or payload["dependency_issue_ref"] == target["issue_ref"]):
            raise ContractError("illegal dependency mutation")
    elif op == "ISSUE_COMMENT_EVENT":
        require(payload, ("event",))
        event = payload["event"]
        check_schema(event, "agent-event-v2.schema.json")
        for outer, inner in (("actor_role", "actor_role"), ("operator_kind", "operator_kind"), ("operator_id", "operator_id")):
            if event.get(inner) != obj["actor"].get(outer):
                raise ContractError("nested Event v2 actor attribution conflicts with outer intent")
        for issue_field in ("task", "issue"):
            if event.get(issue_field) is not None and event[issue_field] != target["issue_ref"]:
                raise ContractError("nested Event v2 work-item target conflicts with outer Issue")
    elif op == "ISSUE_COMMENT_REPORT":
        require(payload, ("report_kind", "report_id", "revision", "attempt_ref", "publication_key",
                          "manifest_ref", "manifest_sha256"))
        if payload["report_kind"] not in REPORT_KINDS or type(payload["revision"]) is not int or payload["revision"] < 1:
            raise ContractError("unknown report kind/revision")
        if not SHA256.fullmatch(str(payload["manifest_sha256"])):
            raise ContractError("invalid manifest checksum")
        key = f"github:{target['repository']}{target['issue_ref']} | {payload['report_id']} | {payload['revision']}"
        if payload["publication_key"] != key:
            raise ContractError("publication key mismatch")
    elif op in ("ISSUE_CLOSE", "ISSUE_REOPEN"):
        require(payload, ("reason", "evidence_refs"))
        refs = payload["evidence_refs"]
        if not isinstance(refs, list) or not refs or any(not isinstance(r, str) or not r for r in refs):
            raise ContractError("close/reopen requires durable reason evidence refs")
    else:
        raise ContractError("unknown operation")
    return "SHAPE_VALID_ONLY"


def _yaml_data(lines):
    index = 1
    while index < len(lines) and not lines[index].strip(): index += 1
    if index >= len(lines) or lines[index].strip() != "```yaml":
        raise ContractError("expected fenced YAML immediately after marker")
    try:
        end = lines.index("```", index + 1)
    except ValueError as exc:
        raise ContractError("unclosed YAML fence") from exc
    return parse_yaml("\n".join(lines[index + 1:end]))


def _report_data(lines):
    header = {}
    for line in lines[1:]:
        m = re.fullmatch(r"([A-Z][A-Z0-9_]+)=(.*)", line)
        if m:
            if m.group(1) in header: raise ContractError("duplicate report header")
            header[m.group(1)] = m.group(2).strip()
        elif header:
            break
        elif line.strip():
            raise ContractError("expected report KEY=VALUE header")
    require(header, ("REPORT_KIND", "REPORT_ID", "REPORT_REVISION", "ATTEMPT_REF", "PUBLICATION_KEY",
                     "MANIFEST_REF", "MANIFEST_SHA256"))
    if header["REPORT_KIND"] not in REPORT_KINDS or not header["REPORT_REVISION"].isdigit() or int(header["REPORT_REVISION"]) < 1:
        raise ContractError("invalid legacy report header")
    if not SHA256.fullmatch(header["MANIFEST_SHA256"]):
        raise ContractError("invalid legacy manifest SHA-256")


def verify_markdown(source, expected_surface=None):
    lines = source.splitlines()
    first = next((l.strip() for l in lines if l.strip()), "")
    if first not in MARKERS:
        if any(l.strip() in MARKERS for l in lines):
            raise ContractError("embedded/quoted marker is not an admitted record")
        if expected_surface: raise ContractError("required structured surface not present")
        return "UNSTRUCTURED_DISCUSSION"
    surface = MARKERS[first]
    if expected_surface and surface != expected_surface:
        raise ContractError("incorrect structured surface: " + surface)
    if not lines or lines[0].strip() != first or sum(l.strip() == first for l in lines) != 1:
        raise ContractError("unique marker must be first line")
    if surface == "report-v1":
        _report_data(lines)
    else:
        obj = _yaml_data(lines)
        if surface == "intent": check_intent(obj)
        elif surface == "work-item": check_work_item(obj)
        else: check_schema(obj, "agent-event-v2.schema.json")
    return "SHAPE_VALID_ONLY"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file", type=Path)
    p.add_argument("--surface", choices=sorted(MARKERS.values()))
    args = p.parse_args()
    try:
        verdict = verify_markdown(args.file.read_text(encoding="utf-8"), args.surface)
    except (ContractError, OSError) as exc:
        print("INVALID_SCHEMA: " + str(exc))
        raise SystemExit(1) from exc
    print(verdict + ": GitHub admission/currentness/authorization must be checked separately")


if __name__ == "__main__":
    main()
