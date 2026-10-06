"""V410-T06B verification: backcompat/golden/conformance fixture inventory integrity.

Pure stdlib, no network. Run from the repository root:

    python scripts/test_v410_t06b_backcompat_fixture_inventory.py

Checks:
  1. HEAD is bound to base 30334e8c7b90a327f8597b86c88c785b98df07f7 either
     exactly, or via additive-only drift limited to this unit's own allowed
     write set (the execution pack directory and this script).
  2. Every fixture path listed in BACKCOMPAT_FIXTURE_INVENTORY.md exists.
  3. Every `python scripts/...` producer command entrypoint in the inventory exists.
  4. Prints fixture counts by kind.

Exit non-zero on any failure; prints BACKCOMPAT_FIXTURE_INVENTORY_VERIFIED=PASS on success.
"""

from __future__ import annotations

import glob
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

BASE_SHA = "30334e8c7b90a327f8597b86c88c785b98df07f7"
PACK_DIR = ".agent/execution/V410-T06B-LOCAL-BACKCOMPAT-FIXTURE-INVENTORY-R1"
INVENTORY = Path(PACK_DIR) / "BACKCOMPAT_FIXTURE_INVENTORY.md"
SELF = "scripts/test_v410_t06b_backcompat_fixture_inventory.py"

KINDS = ("backcompat", "golden", "conformance", "contract")

FAILURES: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"FAIL: {msg}")


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def check_head_binding() -> None:
    head = git("rev-parse", "HEAD")
    if head == BASE_SHA:
        print(f"HEAD binding: exact base {head}")
        return
    # Additive-only drift: every path changed since base must belong to this unit.
    try:
        changed = git("diff", "--name-only", f"{BASE_SHA}..{HEAD}").splitlines()
    except subprocess.CalledProcessError:
        changed = None
    allowed_prefix = PACK_DIR + "/"
    if changed is not None and changed and all(
        p.startswith(allowed_prefix) or p == SELF for p in changed
    ):
        print(
            f"HEAD binding: additive-only drift from base "
            f"{BASE_SHA} to {head} (allowed write set only, {len(changed)} paths)"
        )
        return
    fail(f"HEAD {head} is not bound to base {BASE_SHA} and drift is outside the allowed write set")


def extract_fixture_paths(text: str) -> list[str]:
    paths: list[str] = []
    for line in text.splitlines():
        if not line.startswith("|") or line.startswith("|---") or "Owning concern" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        first = cells[0]
        for token in first.split():
            if ".." in token:
                break  # range marker: check only the leading anchor path
            token = token.strip("`(),;:")
            token = token.rstrip(".")
            if not token or token in KINDS:
                continue
            if any(ch in token for ch in "*?["):
                paths.append(token)  # glob entry, resolved by caller
            elif "/" in token:
                paths.append(token)
    # also scan prose sections for explicit repo-relative file references
    for match in re.findall(r"`((?:scripts|fixtures|templates|schemas|standards|docs|\.agent|\.github)/[^`\s]+)`", text):
        if ".." in match:
            continue
        paths.append(match)
    seen: set[str] = set()
    unique = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique


def check_fixture_paths(paths: list[str]) -> tuple[int, int]:
    ok = 0
    for p in paths:
        if any(ch in p for ch in "*?["):
            if glob.glob(p):
                ok += 1
            else:
                fail(f"fixture glob matched nothing: {p}")
        elif Path(p).exists():
            ok += 1
        else:
            fail(f"fixture path missing: {p}")
    return ok, len(paths)


def check_producer_commands(text: str) -> tuple[int, int]:
    commands = sorted(set(re.findall(r"python (scripts/[\w./_-]+\.py)", text)))
    ok = 0
    for cmd in commands:
        if Path(cmd).is_file():
            ok += 1
        else:
            fail(f"producer entrypoint missing: {cmd}")
    return ok, len(commands)


def count_kinds(text: str) -> Counter:
    counts: Counter = Counter()
    for line in text.splitlines():
        if not line.startswith("|") or line.startswith("|---") or "Owning concern" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        kind_cell = cells[1].strip("`")
        head = kind_cell.split()[0].split("(")[0] if kind_cell else ""
        if head in KINDS:
            counts[head] += 1
    return counts


def main() -> int:
    check_head_binding()
    if not INVENTORY.is_file():
        fail(f"inventory file missing: {INVENTORY}")
        print(f"BACKCOMPAT_FIXTURE_INVENTORY_VERIFIED=FAIL ({len(FAILURES)} failures)")
        return 1
    text = INVENTORY.read_text(encoding="utf-8")

    fixture_ok, fixture_total = check_fixture_paths(extract_fixture_paths(text))
    producer_ok, producer_total = check_producer_commands(text)
    counts = count_kinds(text)

    print(f"fixture paths verified: {fixture_ok}/{fixture_total}")
    print(f"producer entrypoints verified: {producer_ok}/{producer_total}")
    for kind in KINDS:
        print(f"kind_count[{kind}]={counts.get(kind, 0)}")
    print(f"kind_count[TOTAL]={sum(counts.values())}")

    if FAILURES:
        print(f"BACKCOMPAT_FIXTURE_INVENTORY_VERIFIED=FAIL ({len(FAILURES)} failures)")
        return 1
    print("BACKCOMPAT_FIXTURE_INVENTORY_VERIFIED=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
