#!/usr/bin/env python3
"""V410-T07B evidence-input inventory verification (pure stdlib, no network).

Asserts:
  1. git HEAD is the pinned base_sha 30334e8c7b90a327f8597b86c88c785b98df07f7
     or descends from it (currentness: the pack was built on the exact
     pinned base and was not rebased away from it).
  2. Every repo-relative producer path in an inventory row marked AVAILABLE exists.
  3. Every row marked PENDING names an owning concern.
  4. The inventory contains the explicit authority statement that CI/Review/Release
     (and Closure/Controller/Reviewer/model vote) cannot manufacture
     ADS_CORE_FEATURE_FREEZE_ELIGIBLE=YES.

Prints counts; exits non-zero on failure; prints
EVIDENCE_INPUT_INVENTORY_VERIFIED=PASS on success.
"""

import os
import re
import subprocess
import sys

BASE_SHA = "30334e8c7b90a327f8597b86c88c785b98df07f7"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY_REL = os.path.join(
    ".agent", "execution",
    "V410-T07B-LOCAL-EVIDENCE-INPUT-INVENTORY-R1",
    "EVIDENCE_INPUT_INVENTORY.md",
)

failures = []


def fail(msg):
    failures.append(msg)
    print("FAIL: " + msg)


def main():
    # 1. exact base / currentness: HEAD must be the pinned base or a descendant
    #    of it, proving the pack was built on the exact pinned standard revision.
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True,
            text=True, check=True,
        ).stdout.strip()
        on_base = subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASE_SHA, "HEAD"],
            cwd=REPO_ROOT, capture_output=True,
        ).returncode == 0
    except Exception as exc:  # pragma: no cover - environment failure
        fail("could not read git HEAD: %s" % exc)
        head = None
        on_base = False
    if head is not None and not on_base:
        fail("HEAD %s does not descend from pinned base_sha %s"
             % (head, BASE_SHA))
    else:
        print("base_check: HEAD descends from base_sha %s" % BASE_SHA)

    # 2/3. parse inventory tables
    inv_path = os.path.join(REPO_ROOT, INVENTORY_REL)
    if not os.path.isfile(inv_path):
        fail("inventory not found: %s" % INVENTORY_REL)
        report(0, 0, 0, 0)
        return 1
    with open(inv_path, encoding="utf-8") as fh:
        text = fh.read()

    total = available = pending = 0
    paths_checked = 0
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        avail_cells = [c for c in cells
                       if c.startswith("AVAILABLE") or c.startswith("PENDING")]
        if not avail_cells:
            continue  # header or separator row
        avail = avail_cells[0]
        row = line
        total += 1
        label = cells[0][:40]
        if avail.startswith("AVAILABLE"):
            available += 1
            for tok in re.findall(r"`([^`]+)`", row):
                # repo-relative path tokens only: contain '/', no space/colon/@
                if "/" in tok and not re.search(r"[\s:@]", tok):
                    full = os.path.join(REPO_ROOT, tok)
                    paths_checked += 1
                    if not os.path.isfile(full):
                        fail("AVAILABLE row '%s' producer path missing: %s"
                             % (label, tok))
        elif avail.startswith("PENDING"):
            pending += 1
            if "owning concern" not in avail:
                fail("PENDING row '%s' does not name an owning concern" % label)
        else:  # pragma: no cover - defensive
            fail("unrecognized availability cell: %s" % avail)

    if total == 0:
        fail("no inventory rows parsed")

    # 4. explicit decision-authority statement
    if "cannot manufacture" not in text or "ADS_CORE_FEATURE_FREEZE_ELIGIBLE=YES" not in text:
        fail("explicit authority statement (CI/Review/Release cannot manufacture "
             "ADS_CORE_FEATURE_FREEZE_ELIGIBLE=YES) not found in inventory")
    else:
        print("authority_statement: present")

    report(total, available, pending, paths_checked)
    return 1 if failures else 0


def report(total, available, pending, paths_checked):
    print("counts: total_inputs=%d available=%d pending=%d producer_paths_checked=%d"
          % (total, available, pending, paths_checked))
    if failures:
        print("EVIDENCE_INPUT_INVENTORY_VERIFIED=FAIL")
    else:
        print("EVIDENCE_INPUT_INVENTORY_VERIFIED=PASS")


if __name__ == "__main__":
    sys.exit(main())
