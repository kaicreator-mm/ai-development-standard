"""V410 provenance remediation — local command inventory verification.

Preparation-unit gate for V410-PROVENANCE-LOCAL-COMMAND-INVENTORY-R1 (Issue #900).
Pure stdlib; no network; git subprocess allowed; NO gh dependency.

Checks, all fail-closed:
1. HEAD == preparation base SHA 30334e8c7b90a327f8597b86c88c785b98df07f7.
2. COMMAND_INVENTORY.md exists and every `python scripts/...` command entrypoint
   listed in the per-leaf "Commands to re-establish current acceptance" sections
   exists in the repo.
3. All seven affected leaves #850-#856 are covered exactly once as UNIT sections.
4. The #854 section retains the historical 'claim posted post-implementation'
   finding.
5. The campaign-level binding procedure names the exact-SHA re-read step.

On success prints counts and COMMAND_INVENTORY_VERIFIED=PASS, exit 0.
Any failure prints COMMAND_INVENTORY_VERIFIED=FAIL with reasons, exit non-zero.
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = ROOT / ".agent" / "execution" / "V410-PROVENANCE-LOCAL-COMMAND-INVENTORY-R1"
INVENTORY = PACK_DIR / "COMMAND_INVENTORY.md"
BASE_SHA = "30334e8c7b90a327f8597b86c88c785b98df07f7"

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def head_sha() -> str:
    out = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def main() -> int:
    # 1. Exact base binding.
    sha = head_sha()
    check(sha == BASE_SHA, f"HEAD {sha!r} != preparation base {BASE_SHA!r}")

    # 2. Inventory presence.
    check(INVENTORY.is_file(), f"missing inventory: {INVENTORY}")
    if failures:
        return report()

    text = INVENTORY.read_text(encoding="utf-8")

    # 3. Command entrypoints: parse `python scripts/...` tokens, but only from
    #    per-leaf command bullets (lines starting with two spaces + dash +
    #    backtick) so result fields / prose cannot smuggle phantom commands.
    command_lines = [
        line for line in text.splitlines()
        if re.match(r"^\s+- `python scripts/", line)
    ]
    commands = []
    for line in command_lines:
        m = re.search(r"`(python (scripts/[^`]+\.py))`", line)
        if m:
            commands.append(m.group(1))
    check(bool(commands), "no `python scripts/...` command bullets parsed from inventory")
    missing = [c for c in commands if not (ROOT / c.split(" ", 1)[1]).is_file()]
    for c in missing:
        check(False, f"command entrypoint missing in repo: {c}")

    # 4. Seven leaves covered exactly once each as UNIT headings.
    unit_ids = re.findall(r"^### UNIT_(\d{3}) —", text, flags=re.MULTILINE)
    expected = ["850", "851", "852", "853", "854", "855", "856"]
    for leaf in expected:
        count = unit_ids.count(leaf)
        check(count == 1, f"leaf #{leaf} covered {count} times (expected exactly 1)")
    check(len(unit_ids) == 7, f"expected 7 UNIT sections, found {len(unit_ids)}")

    # 5. #854 retains the historical claim-post-implementation finding.
    sec854 = ""
    m = re.search(
        r"^### UNIT_854 .*?(?=^### |\Z)", text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if m:
        sec854 = m.group(0)
    check(bool(sec854), "UNIT_854 section not found")
    check(
        "claim posted post-implementation" in sec854
        or "claim-after-implementation" in sec854,
        "UNIT_854 does not retain the historical claim-posted-post-implementation finding",
    )
    check(
        "HISTORICAL_NONCONFORMANCE_PRESERVED=YES" in sec854,
        "UNIT_854 missing HISTORICAL_NONCONFORMANCE_PRESERVED=YES retention",
    )

    # 6. Binding procedure names the exact-SHA re-read.
    check(
        re.search(r"Re-read the live integration SHA", text) is not None,
        "binding procedure does not name the exact-SHA re-read step",
    )
    check(
        "EXACT_SUBJECT_SHA" in text and "EXACT_SUBJECT_TREE" in text,
        "binding procedure missing EXACT_SUBJECT_SHA/TREE recording",
    )
    check(
        "#864" in text,
        "binding procedure does not reference #864 (T08A) integration confirmation",
    )

    return report(len(commands), len(unit_ids))


def report(commands: int = 0, units: int = 0) -> int:
    if failures:
        print(f"COMMAND_INVENTORY_VERIFIED=FAIL")
        print(f"PARSED_COMMANDS={commands}")
        print(f"UNIT_SECTIONS={units}")
        for f in failures:
            print(f"FAIL: {f}")
        return 1
    print(f"HEAD_SHA={BASE_SHA}")
    print(f"PARSED_COMMANDS={commands}")
    print(f"UNIT_SECTIONS={units}")
    print("LEAVES_COVERED=850,851,852,853,854,855,856")
    print("COMMAND_INVENTORY_VERIFIED=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
