"""V410-T08A LOCAL-INTEGRATION-IMPACT-R1 verification script.

Pure stdlib, no network. Verifies on the exact integrated candidate:
  1. HEAD == base_sha (30334e8c7b90a327f8597b86c88c785b98df07f7); if this unit's own
     pack commits already sit on top, HEAD must be a descendant of base_sha whose
     diff vs base touches ONLY this unit's allowed write set
  2. Every `python scripts/...` entrypoint in the composed conformance command list
     inside INTEGRATION_IMPACT.md exists on disk
  3. Every per-predecessor merge SHA in the impact table exists in git history

Exits non-zero on any failure; prints INTEGRATION_IMPACT_VERIFIED=PASS on success.
This is visible integration evidence only: it is NOT Hidden Validation and NOT
Release Qualification.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

BASE_SHA = "30334e8c7b90a327f8597b86c88c785b98df07f7"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK_DIR = os.path.join(
    ".agent", "execution", "V410-T08A-LOCAL-INTEGRATION-IMPACT-R1"
)
ALLOWED_WRITE_SET = {
    PACK_DIR.replace(os.sep, "/"),
    "scripts/test_v410_t08a_integration_impact.py",
}
IMPACT_MD = os.path.join(REPO_ROOT, PACK_DIR, "INTEGRATION_IMPACT.md")

MERGE_SHA_RE = re.compile(r"\b([0-9a-f]{40})\b")


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"FAIL: {msg}")
    sys.exit(1)


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", REPO_ROOT, *args],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        fail(f"git {' '.join(args)} exited {proc.returncode}: {proc.stderr.strip()}")
    return proc.stdout.strip()


def check_head() -> None:
    head = git("rev-parse", "HEAD")
    print(f"HEAD={head}")
    if head == BASE_SHA:
        print("base check: HEAD == base_sha (exact integrated candidate)")
        return
    # This unit's own pack commits may sit on top of base; only the allowed
    # write set may differ from base, and base must be an ancestor of HEAD.
    merge_base = git("merge-base", BASE_SHA, "HEAD")
    if merge_base != BASE_SHA:
        fail(f"base_sha {BASE_SHA} is not an ancestor of HEAD {head}")
    changed = git("diff", "--name-only", BASE_SHA, "HEAD").splitlines()
    changed = [c for c in changed if c]
    outside = [
        c
        for c in changed
        if not (
            c in ALLOWED_WRITE_SET or c.startswith(PACK_DIR.replace(os.sep, "/") + "/")
        )
    ]
    print(f"base check: HEAD is descendant of base_sha; changed_paths={len(changed)}")
    if outside:
        fail(f"diff vs base touches paths outside allowed write set: {outside}")


def check_command_entrypoints(text: str) -> list[str]:
    # Parse `python scripts/...` entries from the composed conformance command list
    # (section 2 of INTEGRATION_IMPACT.md, fenced bash block).
    section = text.split("## 2. Composed-candidate conformance command list", 1)
    if len(section) != 2:
        fail("INTEGRATION_IMPACT.md section 2 (conformance command list) not found")
    block = section[1].split("```bash", 1)
    if len(block) != 2:
        fail("bash command block not found in INTEGRATION_IMPACT.md section 2")
    commands = re.findall(r"^\s*python\s+(scripts/\S+)\s*$", block[1], re.MULTILINE)
    if not commands:
        fail("no `python scripts/...` entries parsed from the conformance command list")
    missing = [c for c in commands if not os.path.isfile(os.path.join(REPO_ROOT, c))]
    for c in commands:
        print(f"entrypoint: {c} -> {'OK' if c not in missing else 'MISSING'}")
    if missing:
        fail(f"missing command entrypoints: {missing}")
    return commands


def check_merge_shas(text: str) -> list[str]:
    # Merge SHAs are the 40-hex literals in the impact table (section 1).
    section = text.split("## 1. Per-predecessor impact table", 1)
    if len(section) != 2:
        fail("INTEGRATION_IMPACT.md section 1 (impact table) not found")
    table = section[1].split("## 2.", 1)[0]
    shas = MERGE_SHA_RE.findall(table)
    if len(shas) < 8:
        fail(f"expected at least 8 predecessor merge SHAs, found {len(shas)}")
    for sha in shas:
        proc = subprocess.run(
            ["git", "-C", REPO_ROOT, "cat-file", "-e", sha],
            capture_output=True,
        )
        status = "OK" if proc.returncode == 0 else "MISSING"
        print(f"merge_sha: {sha} -> {status}")
        if proc.returncode != 0:
            fail(f"merge SHA {sha} not found in git history")
    return shas


def main() -> int:
    check_head()
    with open(IMPACT_MD, encoding="utf-8") as fh:
        text = fh.read()
    commands = check_command_entrypoints(text)
    shas = check_merge_shas(text)
    print(f"counts: commands={len(commands)} merge_shas={len(shas)}")
    print("INTEGRATION_IMPACT_VERIFIED=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
