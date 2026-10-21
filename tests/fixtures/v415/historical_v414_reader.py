#!/usr/bin/env python3
"""ADS v4.14 latest-only structured Markdown+YAML checker.

This is STRICTLY a source-independent data validator: never dispatch/claim or write GitHub.
Validation is performed by genuine Draft 2020-12 JSON Schema, not a Python op/profile switch.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource
import yaml
from yaml.events import AliasEvent

ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- ads:github -->"
SCHEMA_FILE = ROOT / "schemas/github/v4.14/structured-interaction.schema.json"
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
          if tag not in ("tag:yaml.org,2002:timestamp", "tag:yaml.org,2002:bool")]
    for key, vals in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
StrictLoader.add_implicit_resolver(
    "tag:yaml.org,2002:bool", re.compile(r"^(?:true|false)$"), list("tf")
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


def validate_record(data: dict) -> str:
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, registry=_registry())
    errors = sorted(validator.iter_errors(data), key=lambda e: (list(map(str, e.absolute_path)), e.message))
    if errors:
        first = errors[0]
        pointer = "/" + "/".join(map(str, first.absolute_path))
        causes = "; ".join(c.message for c in first.context[:4])
        raise ContractError(f"JSON_SCHEMA {pointer}: {first.message}" +
                            (f" (alternatives: {causes})" if causes else ""))
    return "SHAPE_VALID_ONLY"


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
    return obj


def verify_markdown(source: str, expected_kind: str | None = None, **_ignored):
    data = parse_markdown(source)
    if data is None:
        if expected_kind:
            raise ContractError("normalized document required")
        return "UNSTRUCTURED_DISCUSSION"
    verdict = validate_record(data)
    if expected_kind is not None and data["kind"] != expected_kind:
        raise ContractError(f"expected kind={expected_kind}, got kind={data['kind']}")
    return verdict


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("file", type=Path)
    cli.add_argument("--kind", choices=["work_item", "intent", "event", "report"])
    args = cli.parse_args()
    try:
        print(verify_markdown(args.file.read_text(encoding="utf-8"), args.kind))
    except (ContractError, OSError) as exc:
        print("INVALID_SCHEMA: " + str(exc))
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
