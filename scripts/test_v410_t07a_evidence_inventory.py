#!/usr/bin/env python3
"""V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1 verification.

Pure stdlib, no network. Verifies, from the repository root:
  1. HEAD is bound to pinned base SHA 30334e8c7b90a327f8597b86c88c785b98df07f7:
     either exactly, or as a descendant of it whose only drift is this unit's
     own additive write set (the execution pack directory and this script).
  2. PRD section 19 (Required Product acceptance, gates and release blockers)
     exists in the worktree PRD.
  3. EVIDENCE_INVENTORY.md parses: every producer path in a CURRENT row exists;
     every PENDING row carries an explicit owning concern (a V410-* task id).

Binding case 1b confines every difference from the pinned base to this unit's own
additive write set, so every path outside that set is byte-identical to the base
tree and check 3 evaluates the same content it would have evaluated at base.

Exit non-zero on any failure; print EVIDENCE_INVENTORY_VERIFIED=PASS on success.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

BASE_SHA = "30334e8c7b90a327f8597b86c88c785b98df07f7"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK_PREFIX = ".agent/execution/V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1/"
SELF = "scripts/test_v410_t07a_evidence_inventory.py"
INVENTORY = os.path.join(
    ROOT, ".agent", "execution", "V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1",
    "EVIDENCE_INVENTORY.md",
)
PRD = os.path.join(ROOT, "docs", "implementation", "4.10.0", "PRD.md")

PATH_RE = re.compile(r"(?:docs|scripts|standards|\.agent)/[A-Za-z0-9_./-]+")
OWNER_RE = re.compile(r"V410-(?:T\d+[A-Z]?|V01)")
PRD_SECTION_MARKERS = [
    "## 19. Required Product acceptance, gates and release blockers",
    "### 19.1 Requirement-linked falsification set",
    "### 19.2 Required high-level gates",
    "### 19.3 v4.10 release blockers",
    "### 19.4 Product completion statement",
]


def fail(msg: str) -> "NoReturn":  # noqa: F821 - intentional never-return
    print("EVIDENCE_INVENTORY_VERIFIED=FAIL")
    print("FAILURE: " + msg)
    sys.exit(1)


def check_head() -> None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
            text=True, timeout=30,
        )
    except Exception as exc:  # pragma: no cover - environment failure
        fail("git rev-parse HEAD could not run: %r" % (exc,))
    if out.returncode != 0:
        fail("git rev-parse HEAD failed: %s" % out.stderr.strip())
    head = out.stdout.strip()
    if head == BASE_SHA:
        print("CHECK head_binding: PASS (exact base %s)" % head)
        return
    descends = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE_SHA, "HEAD"],
        cwd=ROOT, capture_output=True, text=True, timeout=30,
    ).returncode == 0
    if not descends:
        fail("HEAD %s does not descend from pinned base_sha %s" % (head, BASE_SHA))
    diff = subprocess.run(
        ["git", "diff", "--name-only", "%s..%s" % (BASE_SHA, head)],
        cwd=ROOT, capture_output=True, text=True, timeout=60,
    )
    if diff.returncode != 0:
        fail("git diff %s..%s failed: %s" % (BASE_SHA, head, diff.stderr.strip()))
    changed = diff.stdout.splitlines()
    outside = [
        p for p in changed
        if not p.startswith(PACK_PREFIX) and p != SELF
    ]
    if outside:
        fail(
            "drift outside the allowed write set: %s" % ", ".join(outside)
        )
    print(
        "CHECK head_binding: PASS (descendant %s; additive-only drift inside "
        "the allowed write set, %d paths)" % (head, len(changed))
    )


def check_prd_section() -> None:
    if not os.path.isfile(PRD):
        fail("PRD not found at %s" % PRD)
    with open(PRD, "r", encoding="utf-8") as fh:
        text = fh.read()
    missing = [m for m in PRD_SECTION_MARKERS if m not in text]
    if missing:
        fail("PRD section 19 markers missing: %s" % "; ".join(missing))
    for r in ("R1", "R2", "R3", "R4", "R6", "R7", "R11", "R12"):
        if ("%s —" % r) not in text and ("%s --" % r) not in text:
            fail("PRD section 18/19 requirement marker %s missing" % r)
    print("CHECK prd_section_19_exists: PASS (%d markers)" % len(PRD_SECTION_MARKERS))


def parse_inventory():
    with open(INVENTORY, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    rows = []
    header = None
    for line in lines:
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            header = None
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if header is None:
            lowered = [c.lower() for c in cells]
            if (
                "currentness" in lowered
                and "owner concern" in lowered
                and any("producer" in c for c in lowered)
            ):
                header = lowered
            continue
        if set("".join(cells)) <= set("-: "):
            continue  # separator row
        if len(cells) != len(header):
            header = None
            continue
        rows.append(dict(zip(header, cells)))
    if not rows:
        fail("no parseable inventory table rows found in %s" % INVENTORY)
    return rows


def check_rows(rows) -> None:
    total = len(rows)
    current = pending = 0
    paths_checked = 0
    failures = []
    for i, row in enumerate(rows, 1):
        producer = row.get("durable producer", "")
        currentness = row.get("currentness", "").strip().upper()
        owner = row.get("owner concern", "").strip()
        if currentness == "CURRENT":
            current += 1
            for raw in PATH_RE.findall(producer):
                path = raw.rstrip(".")
                paths_checked += 1
                if not os.path.exists(os.path.join(ROOT, path)):
                    failures.append("row %d CURRENT producer path missing: %s" % (i, path))
        elif currentness == "PENDING":
            pending += 1
            if not owner:
                failures.append("row %d PENDING without owning concern" % i)
            elif not OWNER_RE.search(owner):
                failures.append(
                    "row %d PENDING owner concern '%s' names no V410-* task" % (i, owner)
                )
        else:
            failures.append("row %d has non CURRENT/PENDING currentness: %r" % (i, currentness))
    print(
        "CHECK inventory_rows: total=%d current=%d pending=%d paths_checked=%d"
        % (total, current, pending, paths_checked)
    )
    if paths_checked == 0:
        failures.append("no producer paths found in CURRENT rows")
    if pending == 0:
        failures.append("no PENDING rows recorded; pending producers must stay visible")
    if failures:
        for f in failures:
            print("FAILURE: " + f)
        print("EVIDENCE_INVENTORY_VERIFIED=FAIL")
        sys.exit(1)


def main() -> int:
    check_head()
    check_prd_section()
    rows = parse_inventory()
    check_rows(rows)
    print("EVIDENCE_INVENTORY_VERIFIED=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
