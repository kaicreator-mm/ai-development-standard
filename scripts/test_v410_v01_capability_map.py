#!/usr/bin/env python3
"""Verify the V410-V01 local capability map (preparation unit R1).

Pure stdlib, no network. ``git`` subprocess is used only to assert HEAD binding.

This script verifies the MAP'S OWN INTEGRITY ONLY:
  * HEAD is bound to the pinned base SHA: equal to it, or a descendant whose only
    drift is this unit's own additive write set (pack directory + this script);
  * the capability map covers all 15 contract subjects exactly once;
  * every local command entrypoint recorded as AVAILABLE exists at base_sha.

Binding case 2 confines every difference from the pinned base to this unit's own
additive write set, so every path outside that set is byte-identical to the base
tree and AVAILABLE-entrypoint existence carries the same assurance it had at base.

It does NOT execute the mapped validation commands and confers no PASS on any
V410-V01 subject, Task, PR, or release. Host-scope commands (GitHub platform)
are recorded but never executed or checked beyond this disclaimer.
"""

from __future__ import annotations

from pathlib import Path
import shlex
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE_SHA = "30334e8c7b90a327f8597b86c88c785b98df07f7"
PACK_PREFIX = ".agent/execution/V410-V01-LOCAL-CAPABILITY-MAP-R1/"
SELF = "scripts/test_v410_v01_capability_map.py"
MAP_PATH = ROOT / ".agent" / "execution" / "V410-V01-LOCAL-CAPABILITY-MAP-R1" / "CAPABILITY_MAP.md"
REQUIRED_SUBJECTS = set(range(1, 16))

VALID_AVAILABILITY = {
    "AVAILABLE",
    "AVAILABLE_LOCAL_BLOCKED_HOST",
    "BLOCKED",
}


def fail(msg: str) -> "NoReturn":  # noqa: F821 - deliberate; never returns
    print(f"FAIL: {msg}")
    sys.exit(1)


def head_sha() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"cannot read git HEAD: {exc}")
    return out.stdout.strip()


def check_head_binding() -> str:
    """Return the binding class of HEAD against the pinned base, or fail closed."""
    head = head_sha()
    if head == BASE_SHA:
        return "exact_base"
    descends = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE_SHA, "HEAD"],
        cwd=ROOT, capture_output=True, text=True,
    ).returncode == 0
    if not descends:
        fail(
            f"HEAD {head} does not descend from base_sha {BASE_SHA}; map is not "
            "current — re-derive at exact candidate"
        )
    diff = subprocess.run(
        ["git", "diff", "--name-only", f"{BASE_SHA}..{head}"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if diff.returncode != 0:
        fail(f"git diff {BASE_SHA}..{head} failed: {diff.stderr.strip()}")
    outside = [
        path for path in diff.stdout.splitlines()
        if not path.startswith(PACK_PREFIX) and path != SELF
    ]
    if outside:
        fail("drift outside the allowed write set: " + ", ".join(outside))
    return "descendant_additive_only"


def parse_map(text: str) -> dict[int, dict]:
    marker = "```capability-map"
    start = text.find(marker)
    if start == -1:
        fail(f"machine block {marker!r} not found in {MAP_PATH}")
    end = text.find("```", start + len(marker))
    if end == -1:
        fail("machine block not closed")
    block = text[start + len(marker):end]

    subjects: dict[int, dict] = {}
    current: dict | None = None
    in_commands = False
    for raw in block.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("SUBJECT "):
            if current is not None:
                fail("new SUBJECT before END of previous record")
            try:
                subject_id = int(line.split()[1])
            except (IndexError, ValueError):
                fail(f"malformed SUBJECT line: {line!r}")
            if subject_id in subjects:
                fail(f"subject {subject_id} declared more than once")
            if not 1 <= subject_id <= 15:
                fail(f"subject id out of range: {subject_id}")
            current = {"id": subject_id, "availability": None, "commands": [], "limitation": None}
            in_commands = False
        elif current is None:
            fail(f"content outside record: {line!r}")
        elif line.startswith("AVAILABILITY "):
            current["availability"] = line.split(None, 1)[1].strip()
        elif line == "COMMANDS":
            in_commands = True
        elif line.startswith("LIMITATION "):
            current["limitation"] = line.split(None, 1)[1].strip()
            in_commands = False
        elif line == "END":
            subjects[current["id"]] = current
            current = None
            in_commands = False
        elif in_commands:
            current["commands"].append(line)
        else:
            fail(f"unexpected line: {line!r}")
    if current is not None:
        fail(f"record for subject {current['id']} not closed with END")
    return subjects


def entrypoint_for(command: str) -> str | None:
    """Resolve the local existence-check target of one mapped command."""
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError as exc:
        fail(f"unparsable command {command!r}: {exc}")
    if not tokens:
        return None
    tool = tokens[0]
    if tool in ("python", "python3", "py"):
        return tokens[1] if len(tokens) > 1 else None
    if tool in ("gh", "git"):
        return None  # executable presence checked separately
    if tool == "grep":
        return tokens[-1]
    return tool


def check_command(command: str) -> None:
    host_scope = False
    body = command
    if body.startswith("host:"):
        host_scope = True
        body = body[len("host:"):].strip()
    if host_scope:
        return  # host-scope commands are GitHub-platform facts, never executed here
    try:
        tokens = shlex.split(body, posix=True)
    except ValueError as exc:
        fail(f"unparsable command {command!r}: {exc}")
    if not tokens:
        fail(f"empty command for subject availability check: {command!r}")
    tool = tokens[0]
    if tool in ("gh", "git"):
        if shutil.which(tool) is None:
            fail(f"required executable not on PATH: {tool}")
        return
    target = entrypoint_for(body)
    if target is None:
        fail(f"cannot resolve entrypoint for command: {command!r}")
    if not (ROOT / target).exists():
        fail(f"entrypoint missing at base tree: {target} (from command: {command!r})")


def main() -> int:
    binding = check_head_binding()

    text = MAP_PATH.read_text(encoding="utf-8")
    subjects = parse_map(text)

    missing = REQUIRED_SUBJECTS - set(subjects)
    if missing:
        fail(f"capability map missing subjects: {sorted(missing)}")

    available = blocked = split = 0
    for subject_id in sorted(subjects):
        record = subjects[subject_id]
        availability = record["availability"]
        if availability not in VALID_AVAILABILITY:
            fail(f"subject {subject_id}: invalid availability {availability!r}")
        if not record["commands"]:
            fail(f"subject {subject_id}: no commands recorded")
        if record["limitation"] is None:
            fail(f"subject {subject_id}: no LIMITATION recorded")
        if availability == "AVAILABLE":
            available += 1
        elif availability == "BLOCKED":
            blocked += 1
        else:
            split += 1
        for command in record["commands"]:
            check_command(command)

    print("CAPABILITY_MAP_VERIFIED")
    print(f"BASE_SHA={BASE_SHA}")
    print(f"HEAD={head_sha()}")
    print(f"HEAD_BINDING={binding}")
    print(f"SUBJECTS_TOTAL={len(subjects)}")
    print(f"SUBJECTS_AVAILABLE={available}")
    print(f"SUBJECTS_AVAILABLE_LOCAL_BLOCKED_HOST={split}")
    print(f"SUBJECTS_BLOCKED={blocked}")
    print("HOST_SCOPE_COMMANDS=RECORDED_NOT_EXECUTED")
    print("CANDIDATE_STATE=CANDIDATE_NOT_READY")
    print("NOTE=this verifies map integrity only; not a V410-V01 validation PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
