#!/usr/bin/env python3
"""ADS pinned per-kind structured Markdown+YAML checker (v3/v4/v5 report).

This is STRICTLY a source-independent data validator: never dispatch/claim or write GitHub.
Validation is performed by genuine Draft 2020-12 JSON Schema, not a Python op/profile switch.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource
import yaml
from yaml.events import AliasEvent

ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- ads:github -->"
SCHEMA_FILE = ROOT / "schemas/github/v4.14/structured-interaction.schema.json"
REPORT_SCHEMA_FILE = ROOT / "schemas/github/v4.15/report.schema.json"
V5_REPORT_SCHEMA_FILE = ROOT / "schemas/github/v4.16/report.schema.json"
REFERENCED = (
    ROOT / "schemas/task-contract.schema.json",
    ROOT / "schemas/agent-event-v2.schema.json",
)
MAX_BYTES = 256 * 1024
MAX_DEPTH = 64


class ContractError(ValueError):
    """Invalid normalized source document; not a GitHub API verdict."""


class StrictLoader(yaml.SafeLoader):
    """No aliases, duplicate keys, unsafe tags, timestamps, YAML 1.1 implicit booleans."""

    def __init__(self, stream):
        super().__init__(stream)
        self._node_depth = 0

    def compose_node(self, parent, index):
        if self.check_event(AliasEvent):
            raise ContractError("YAML aliases and anchors are forbidden")
        self._node_depth += 1
        if self._node_depth > MAX_DEPTH:
            raise ContractError("YAML nesting too deep")
        try:
            event = self.peek_event()
            if getattr(event, "anchor", None):
                raise ContractError("YAML anchors are forbidden")
            if getattr(event, "tag", None):
                raise ContractError("explicit YAML tags are forbidden")
            return super().compose_node(parent, index)
        finally:
            self._node_depth -= 1

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, yaml.MappingNode):
            raise ContractError("expected YAML mapping")
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=True)
            if not isinstance(key, str):
                raise ContractError("YAML map keys must be strings")
            if key in result:
                raise ContractError("duplicate YAML map key: " + key)
            result[key] = self.construct_object(value_node, deep=deep)
        return result


# Local resolver mutation only; keep yaml.SafeLoader unchanged for other tooling.
StrictLoader.yaml_implicit_resolvers = {
    key: [(tag, pattern) for tag, pattern in vals
          if tag not in ("tag:yaml.org,2002:timestamp", "tag:yaml.org,2002:bool",
                         "tag:yaml.org,2002:int", "tag:yaml.org,2002:float")]
    for key, vals in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
StrictLoader.add_implicit_resolver(
    "tag:yaml.org,2002:bool", re.compile(r"^(?:true|false)$"), list("tf")
)
StrictLoader.add_implicit_resolver(
    "tag:yaml.org,2002:int", re.compile(r"^-?(?:0|[1-9][0-9]*)$"), list("-0123456789")
)
StrictLoader.add_implicit_resolver(
    "tag:yaml.org,2002:float",
    re.compile(r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+(?:[eE][+-]?[0-9]+)?|[eE][+-]?[0-9]+)$"),
    list("-0123456789")
)


def _deny_remote(uri: str):
    raise NoSuchResource(ref=uri)


def _registry():
    refs = []
    for path in REFERENCED:
        obj = json.loads(path.read_text(encoding="utf-8"))
        if not obj.get("$id"):
            raise ContractError(f"referenced Schema lacks immutable ID: {path.name}")
        refs.append((obj["$id"], Resource.from_contents(obj)))
    return Registry(retrieve=_deny_remote).with_resources(refs)


def _json_domain(value, depth=0):
    """Reject coercions before Schema/JCS; integers must survive JS readers exactly."""
    if depth > MAX_DEPTH:
        raise ContractError("JSON nesting too deep")
    if value is None or type(value) is bool:
        return
    if type(value) is str:
        if any(0xD800 <= ord(c) <= 0xDFFF for c in value):
            raise ContractError("lone Unicode surrogate")
    elif type(value) is int:
        if abs(value) > 9007199254740991:
            raise ContractError("integer outside interoperable exact range; encode as string")
    elif type(value) is float:
        if not math.isfinite(value):
            raise ContractError("nonfinite JSON number")
    elif type(value) is list:
        for item in value:
            _json_domain(item, depth + 1)
    elif type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise ContractError("JSON object key must be string")
            _json_domain(key, depth + 1)
            _json_domain(item, depth + 1)
    else:
        raise ContractError("non-JSON YAML/programmatic value")


def _jcs_number(value):
    """Shortest binary64 round-trip digits, with ECMAScript decimal placement.

    CPython repr supplies shortest round-trip digits (ties to even). JCS differs
    from Python in negative zero, decimal/exponent thresholds and exponent zeros.
    RFC8785 Appendix B boundary/tie vectors are exercised by the v4.15 tests.
    """
    if value == 0:
        return "0"
    if type(value) is int:
        return str(value)
    sign = "-" if value < 0 else ""
    raw = repr(abs(value)).lower()
    mantissa, _, exp = raw.partition("e")
    exponent = int(exp or "0")
    whole, _, fraction = mantissa.partition(".")
    digits = (whole + fraction).lstrip("0")
    point = len(whole) + exponent
    if whole == "0":
        zeros = len(fraction) - len(fraction.lstrip("0"))
        point = -zeros + exponent
    digits = digits.rstrip("0") or "0"
    if 0 < point <= 21:
        if len(digits) <= point:
            return sign + digits + "0" * (point - len(digits))
        return sign + digits[:point] + "." + digits[point:]
    if -6 < point <= 0:
        return sign + "0." + "0" * (-point) + digits
    exponent = point - 1
    return sign + digits[0] + ("." + digits[1:] if len(digits) > 1 else "") + "e" + ("+" if exponent >= 0 else "-") + str(abs(exponent))


def canonical_json(value) -> bytes:
    """RFC8785 UTF-8 bytes; no Unicode normalization, UTF-16 property ordering."""
    _json_domain(value)
    def encode(item):
        if item is None:
            return "null"
        if type(item) is bool:
            return "true" if item else "false"
        if type(item) in (int, float):
            return _jcs_number(item)
        if type(item) is str:
            return json.dumps(item, ensure_ascii=False)
        if type(item) is list:
            return "[" + ",".join(encode(x) for x in item) + "]"
        keys = sorted(item, key=lambda x: x.encode("utf-16-be"))
        return "{" + ",".join(encode(k) + ":" + encode(item[k]) for k in keys) + "}"
    return encode(value).encode("utf-8")


def validate_record(data: dict) -> str:
    _json_domain(data)
    if not isinstance(data, dict):
        raise ContractError("canonical record must be an object")
    pair = (data.get("schema"), data.get("kind"))
    if pair == ("ads/github/v4", "report"):
        path = REPORT_SCHEMA_FILE
    elif pair == ("ads/github/v5", "report"):
        path = V5_REPORT_SCHEMA_FILE
    elif pair[0] == "ads/github/v3" and pair[1] in ("work_item", "intent", "event", "report"):
        path = SCHEMA_FILE
    else:
        raise ContractError("UNSUPPORTED_SCHEMA: unrecognized schema/kind pair")
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, registry=_registry())
    errors = sorted(validator.iter_errors(data), key=lambda e: (list(map(str, e.absolute_path)), e.message))
    if errors:
        first = errors[0]
        pointer = "/" + "/".join(map(str, first.absolute_path))
        causes = "; ".join(c.message for c in first.context[:4])
        raise ContractError(f"JSON_SCHEMA {pointer}: {first.message}" +
                            (f" (alternatives: {causes})" if causes else ""))
    if path == REPORT_SCHEMA_FILE:
        _report_semantics(data["data"])
    elif path == V5_REPORT_SCHEMA_FILE:
        _v5_report_semantics(data["data"])
    return "SHAPE_VALID_ONLY"


def record_disposition(record, effective_pin="v4.15", writing=False):
    """Interpret wire compatibility only; CURRENT never means Claim admission."""
    if effective_pin not in ("v4.14", "v4.15", "v4.16"):
        raise ContractError("UNSUPPORTED_SCHEMA: unresolved effective pin")
    if effective_pin == "v4.14" and record.get("schema") != "ads/github/v3":
        raise ContractError("UNSUPPORTED_SCHEMA: v4.14 reader")
    if record.get("schema") == "ads/github/v5" and effective_pin != "v4.16":
        raise ContractError("UNSUPPORTED_SCHEMA: v5 report requires v4.16 reader")
    validate_record(record)
    if effective_pin in ("v4.15", "v4.16") and record["schema"] == "ads/github/v3" and record["kind"] == "report":
        if writing:
            raise ContractError("v4.15 writer cannot emit historical v3 report")
        return "HISTORICAL_READ_ONLY"
    if record.get("schema") == "ads/github/v5":
        return "V5_SHAPE_ONLY"  # never an adopted writer or native authority grant
    return "CURRENT_OBSERVATION" if record["kind"] == "report" else "CURRENT_EXECUTABLE_SHAPE_ONLY"


def _report_semantics(data):
    subject = data["subject"]
    if not subject["issue_ref"].startswith("https://github.com/" + subject["repository"] + "/issues/"):
        raise ContractError("owning repository/Issue mismatch")
    try:
        datetime.fromisoformat(data["observed_at"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError("invalid observed_at calendar time") from exc
    prev = data["supersedes"]
    if prev is not None and (prev["revision"] != data["revision"] - 1 or not prev["comment_ref"].startswith(subject["issue_ref"] + "#issuecomment-")):
        raise ContractError("revision must name its exact preceding owning-Issue publication")
    if data["report_kind"] == "EXECUTION_SUMMARY":
        if subject["attempt_ref"] not in data["aggregation"]["attempt_refs"]:
            raise ContractError("summary Attempt missing from leaf aggregation")
        if set(data["aggregation"]["attempt_refs"]) & set(data["aggregation"]["excluded_attempt_refs"]):
            raise ContractError("included and excluded Attempt overlap")
        if data["verifier"]["subject_sha"] != subject["source_sha"]:
            raise ContractError("verifier/source mismatch")
        groups = [set(data["verifier"][k]) for k in ("checked", "failed", "skipped", "unchecked")]
        if any(a & b for i, a in enumerate(groups) for b in groups[i + 1:]):
            raise ContractError("verifier scopes must be disjoint")
        for metric in data["metrics"]:
            if metric["value"] is None and metric["epistemic"] != "UNKNOWN":
                raise ContractError("missing metric requires UNKNOWN")
        manifest = data["manifest_ref"].lower()
        if any(token in manifest for token in ("?", "#", "token=", "signature=", "credential=")):
            raise ContractError("manifest must be stable opaque/private locator, never signed URL")
    elif data["report_kind"] == "EXPERIENCE_USE_FEEDBACK":
        if data["ads_subject_sha"] != subject["ads_revision"]:
            raise ContractError("feedback ADS subject/effective test profile mismatch")


def _v5_report_semantics(data):
    """Structural consistency only: never native GitHub/producer authority."""
    subject = data["subject"]
    issue = subject["issue_ref"]
    if not issue.startswith("https://github.com/" + subject["repository"] + "/issues/"):
        raise ContractError("v5 owning repository/Issue mismatch")
    try:
        datetime.fromisoformat(data["observed_at"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError("invalid v5 observed_at calendar time") from exc
    prev = data["supersedes"]
    if prev is not None and (prev["revision"] != data["revision"] - 1
                             or not prev["comment_ref"].startswith(issue + "#issuecomment-")):
        raise ContractError("v5 predecessor must be the immediate owning-Issue revision")
    if data["report_kind"] == "EXECUTION_SUMMARY":
        if subject["attempt_ref"] not in data["aggregation"]["attempt_refs"]:
            raise ContractError("v5 summary Attempt absent from leaf aggregation")
        if set(data["aggregation"]["attempt_refs"]) & set(data["aggregation"]["excluded_attempt_refs"]):
            raise ContractError("v5 included/excluded Attempt overlap")
        if data["verifier"]["subject_sha"] is not None and data["verifier"]["subject_sha"] != subject["source_sha"]:
            raise ContractError("v5 verifier original source mismatch")
        sets = [set(data["verifier"][key]) for key in ("checked", "failed", "skipped", "unchecked")]
        if any(a & b for i, a in enumerate(sets) for b in sets[i + 1:]):
            raise ContractError("v5 verifier scopes overlap")
        if any(metric["value"] is None and metric["epistemic"] != "UNKNOWN" for metric in data["metrics"]):
            raise ContractError("v5 missing metric requires UNKNOWN")
        if any(token in data["manifest_ref"].lower() for token in ("?", "#", "token=", "signature=", "credential=")):
            raise ContractError("v5 manifest must be stable opaque locator")
        if "source_association" in data and data["source_association"]["source_sha"] != subject["source_sha"]:
            raise ContractError("v5 associated original source mismatch")
    elif data["report_kind"] == "EXPERIENCE_USE_FEEDBACK":
        if data["ads_subject_sha"] != subject["ads_revision"]:
            raise ContractError("v5 feedback ADS subject mismatch")
        if data["publisher_source_sha"] != subject["publisher_source_sha"]:
            raise ContractError("v5 feedback publisher source mismatch")
    elif data["report_kind"] == "EXECUTION_CORRECTION":
        target = data["target"]
        if target["repository"] != subject["repository"] or target["issue_ref"] != issue:
            raise ContractError("v5 correction foreign Issue target")
        if target["task_ref"] != subject["task_ref"] or target["attempt_ref"] != subject["attempt_ref"]:
            raise ContractError("v5 correction cross-Task/Attempt")
        if target["publisher_namespace"] != data["publisher_namespace"]:
            raise ContractError("v5 correction cross-publisher assertion")
        if target["comment_ref"] != issue + "#issuecomment-" + str(target["comment_id"]):
            raise ContractError("v5 correction native comment identity mismatch")
        if data["notice_publisher_source_sha"] != subject["publisher_source_sha"]:
            raise ContractError("v5 correction publisher source mismatch")


def data_digest(record) -> str:
    """Public validated data comparator, not private-manifest integrity or authority."""
    validate_record(record)
    if record["schema"] not in ("ads/github/v4", "ads/github/v5") or record["kind"] != "report":
        raise ContractError("v4/v5 report required for public data digest")
    return hashlib.sha256(canonical_json(record["data"])).hexdigest()


def report_identity(record):
    validate_record(record)
    if record.get("schema") not in ("ads/github/v4", "ads/github/v5") or record.get("kind") != "report":
        raise ContractError("v4/v5 report identity required")
    d = record["data"]
    return (d["subject"]["issue_ref"], d["publisher_namespace"], d["report_id"], d["revision"], d["report_kind"])


def observation_status(record, *, edited=None, previous_record=None, same_comment=False):
    """Bounded comparator of supplied observations; obtains no GitHub facts itself.

    `edited=False` must be witnessed by a native consumer; absence is UNKNOWN.
    This helper never authenticates publisher/correction authority or grants PASS.
    """
    digest = data_digest(record)
    if edited is True:
        return "UNVERIFIED_EDIT"
    if previous_record is not None:
        previous_digest = data_digest(previous_record)
        if (same_comment or report_identity(record) == report_identity(previous_record)) and digest != previous_digest:
            return "CONFLICT"
        if report_identity(record) == report_identity(previous_record) and digest == previous_digest:
            return "DUPLICATE" if edited is False else "UNKNOWN_INTEGRITY"
    return "OBSERVED_SHAPE_ONLY" if edited is False else "UNKNOWN_INTEGRITY"


def validate_summary_revision(previous, successor, legacy_kind):
    """EVIDENCE_UPDATE/TASK_LEARNING mapping, with actual prior data supplied.

    Checks immutable data lineage, never remote manifest bytes or publication.
    """
    if legacy_kind not in ("EVIDENCE_UPDATE", "TASK_LEARNING"):
        raise ContractError("unsupported legacy revision reason")
    for record in (previous, successor):
        validate_record(record)
        if record.get("schema") != "ads/github/v4" or record["data"]["report_kind"] != "EXECUTION_SUMMARY":
            raise ContractError("late evidence/learning requires an existing v4 summary")
    a, b = previous["data"], successor["data"]
    subject_identity = ("repository", "issue_ref", "task_ref", "attempt_ref", "attempt_binding", "source_sha", "ads_revision", "ads_profile")
    if any(a[k] != b[k] for k in ("report_id", "publisher_namespace")) or any(a["subject"][k] != b["subject"][k] for k in subject_identity) or b["revision"] != a["revision"] + 1:
        raise ContractError("not the same summary/Attempt subject's next revision")
    if b["supersedes"]["data_digest"] != data_digest(previous):
        raise ContractError("predecessor digest mismatch")
    if a["manifest_ref"] == b["manifest_ref"] or a["manifest_sha256"] == b["manifest_sha256"]:
        raise ContractError("new summary revision requires new immutable private manifest")
    if legacy_kind == "TASK_LEARNING" and (b["learning"]["state"] != "REFERENCED" or not (set(b["learning"]["source_refs"]) - set(a["learning"]["source_refs"]))):
        raise ContractError("material learning requires a new actual Task Learning source ref")
    if legacy_kind == "EVIDENCE_UPDATE" and not (set(b["source_refs"] + b["verifier"]["source_refs"]) - set(a["source_refs"] + a["verifier"]["source_refs"])):
        raise ContractError("late evidence requires a new source-bound evidence ref")
    return "SHAPE_VALID_ONLY"


def compare_v5_correction_source(correction, original=None, *,
                                 target_comment_ref=None, original_unedited=False,
                                 complete_collection=False):
    """Bounded caller-supplied source comparison; never applies a GitHub notice.

    Even matched and purportedly native flags do not authenticate a publisher
    namespace grant or authorize REVOKE, REDACT, DISPUTE, or replacement.
    """
    validate_record(correction)
    if correction.get("schema") != "ads/github/v5" or correction["data"]["report_kind"] != "EXECUTION_CORRECTION":
        raise ContractError("v5 correction required")
    if original is None or not complete_collection or not original_unedited:
        return "UNVERIFIED"
    validate_record(original)
    if original.get("schema") != "ads/github/v5" or original["data"]["report_kind"] not in ("EXECUTION_SUMMARY", "EXPERIENCE_USE_FEEDBACK"):
        return "DISPUTED"
    target = correction["data"]["target"]
    old = original["data"]
    subject = old["subject"]
    keys = ("repository", "issue_ref", "task_ref", "attempt_ref")
    if any(target[key] != subject[key] for key in keys):
        return "DISPUTED"
    if (target["comment_ref"] != target_comment_ref
        or target["publisher_namespace"] != old["publisher_namespace"]
        or target["report_id"] != old["report_id"]
        or target["revision"] != old["revision"]
        or target["report_kind"] != old["report_kind"]
        or target["target_source_status"] != subject["source_status"]
        or target["target_source_sha"] != subject["source_sha"]
        or target["data_digest"] != data_digest(original)):
        return "DISPUTED"
    return "SOURCE_MATCH_ONLY"


def compare_v5_summary_revision(previous, successor, *, predecessor_comment_ref=None,
                                previous_unedited=False):
    """A source-only chain: no promotion of collector Attempt to canonical Claim."""
    for record in (previous, successor):
        validate_record(record)
        if record.get("schema") != "ads/github/v5" or record["data"]["report_kind"] != "EXECUTION_SUMMARY":
            raise ContractError("two v5 summaries required")
    a, b = previous["data"], successor["data"]
    stable = ("repository", "issue_ref", "task_ref", "attempt_ref",
              "attempt_binding", "ads_revision", "ads_profile", "publisher_source_sha")
    if (a["report_id"] != b["report_id"] or
        a["publisher_namespace"] != b["publisher_namespace"] or
        any(a["subject"][key] != b["subject"][key] for key in stable) or
        b["revision"] != a["revision"] + 1):
        raise ContractError("v5 next revision changes identity or skips predecessor")
    predecessor = b["supersedes"]
    if predecessor["revision"] != a["revision"] or predecessor["data_digest"] != data_digest(previous):
        raise ContractError("v5 prior data digest/revision mismatch")
    if not previous_unedited or predecessor_comment_ref != predecessor["comment_ref"]:
        return "UNVERIFIED"
    if a["manifest_ref"] == b["manifest_ref"] or a["manifest_sha256"] == b["manifest_sha256"]:
        raise ContractError("v5 revision reuses previous immutable manifest")
    if "source_association" in b:
        if "source_association" in a or a["subject"]["source_status"] not in ("UNKNOWN", "UNPINNED"):
            raise ContractError("v5 source association requires unpinned prior observation")
        if b["subject"]["attempt_binding"] != "COLLECTOR_ONLY":
            raise ContractError("v5 source association cannot mint canonical Attempt")
    elif any(a["subject"][key] != b["subject"][key] for key in ("source_status", "source_sha")):
        raise ContractError("v5 source changed without association")
    return "SOURCE_CHAIN_SHAPE_ONLY"


def inspect_supplied_issue_pages(pages, *, effective_pin="v4.16"):
    """Inspect finite supplied GitHub page data; NEVER fetch/authenticate remotely.

    The caller's edited=False and complete page values are not themselves proof
    of native readback, ACL or publisher grant. Every output remains observational.
    """
    if type(pages) is not list or not pages or len(pages) > 128:
        return {"complete": False, "statuses": []}
    rows, cursor, seen = [], None, set()
    complete = False
    for page in pages:
        if (type(page) is not dict or page.get("cursor") != cursor or
            type(page.get("comments")) is not list or
            page.get("status") != 200 or len(rows) + len(page["comments"]) > 4096):
            break
        rows.extend(page["comments"])
        next_cursor = page.get("next")
        if next_cursor is None:
            complete = True
            break
        if type(next_cursor) is not str or not next_cursor or next_cursor in seen:
            break
        seen.add(next_cursor)
        cursor = next_cursor
    if not complete:
        return {"complete": False, "statuses": ["UNKNOWN_INTEGRITY"] * len(rows)}
    statuses, identities, comment_ids = [], {}, {}
    for item in rows:
        try:
            if type(item) is not dict or type(item.get("body")) is not str:
                raise ContractError("native bytes missing")
            parsed = parse_markdown(item["body"])
            if parsed is None:
                statuses.append("UNSTRUCTURED_DISCUSSION")
                continue
            disposition = record_disposition(parsed, effective_pin)
            if type(item.get("id")) is not int or item["id"] < 1:
                statuses.append("UNVERIFIED")
                continue
            if parsed["kind"] != "report":
                statuses.append(disposition)
                continue
            subject = parsed["data"].get("subject")
            if not subject or item.get("url") != subject["issue_ref"] + "#issuecomment-" + str(item["id"]):
                statuses.append("UNVERIFIED")
                continue
            if item.get("edited") is not False:
                statuses.append("UNVERIFIED_EDIT" if item.get("edited") is True else "UNKNOWN_INTEGRITY")
                continue
            identity = report_identity(parsed)
            digest = data_digest(parsed)
            statuses.append("OBSERVED_SHAPE_ONLY")
            identities.setdefault(identity, []).append((len(statuses) - 1, digest))
            comment_ids.setdefault(item["id"], []).append((len(statuses) - 1, digest))
        except (ContractError, KeyError, TypeError, ValueError):
            statuses.append("INVALID_SCHEMA")
    for groups in (identities, comment_ids):
        for members in groups.values():
            if len({digest for _, digest in members}) > 1:
                for idx, _ in members:
                    statuses[idx] = "CONFLICT"
            elif len(members) > 1:
                for idx, _ in members[1:]:
                    if statuses[idx] == "OBSERVED_SHAPE_ONLY":
                        statuses[idx] = "DUPLICATE"
    return {"complete": True, "statuses": statuses}


def parse_markdown(source: str) -> dict | None:
    if len(source.encode("utf-8")) > MAX_BYTES:
        raise ContractError("source document exceeds MAX_BYTES")
    lines = source.splitlines()
    if not lines or lines[0] != MARKER:
        if any(x.strip() == MARKER for x in lines) or any(
            x.startswith("<!-- ads:github:") or x.startswith("<!-- ai-dev:event:")
            or x.startswith("<!-- ads:task-report:") for x in lines[:1]
        ):
            raise ContractError("legacy, quoted or nonleading ADS structure marker")
        return None
    if sum(line == MARKER for line in lines) != 1:
        raise ContractError("exactly one leading normalized marker required")
    index = 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index == len(lines) or lines[index] != "```yaml":
        raise ContractError("marker must precede one fenced yaml block")
    try:
        end = lines.index("```", index + 1)
    except ValueError as exc:
        raise ContractError("unclosed yaml fence") from exc
    yaml_text = "\n".join(lines[index + 1:end])
    try:
        obj = yaml.load(yaml_text, Loader=StrictLoader)
    except (yaml.YAMLError, TypeError) as exc:
        raise ContractError(f"unsafe or malformed YAML: {exc}") from exc
    if not isinstance(obj, dict):
        raise ContractError("canonical YAML must contain a single root object")
    _json_domain(obj)
    return obj


def verify_markdown(source: str, expected_kind: str | None = None, *, effective_pin="v4.15", writing=False, **_ignored):
    data = parse_markdown(source)
    if data is None:
        if expected_kind:
            raise ContractError("normalized document required")
        return "UNSTRUCTURED_DISCUSSION"
    record_disposition(data, effective_pin, writing)
    if expected_kind is not None and data["kind"] != expected_kind:
        raise ContractError(f"expected kind={expected_kind}, got kind={data['kind']}")
    return "SHAPE_VALID_ONLY"


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("file", type=Path)
    cli.add_argument("--kind", choices=["work_item", "intent", "event", "report"])
    cli.add_argument("--effective-pin", choices=["v4.14", "v4.15", "v4.16"], default="v4.15")
    cli.add_argument("--writing", action="store_true")
    cli.add_argument("--data-digest", action="store_true")
    args = cli.parse_args()
    try:
        source = args.file.read_text(encoding="utf-8")
        verdict = verify_markdown(source, args.kind, effective_pin=args.effective_pin, writing=args.writing)
        print(data_digest(parse_markdown(source)) if args.data_digest else verdict)
    except (ContractError, OSError) as exc:
        print("INVALID_SCHEMA: " + str(exc))
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
