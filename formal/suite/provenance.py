"""Read-only Git binding for the ADS experimental model inputs; no policy gate."""
import hashlib
import re
import subprocess
from pathlib import Path

SHA40 = re.compile(r"^[0-9a-f]{40}$")


def git(args, cwd):
    try:
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                           errors="replace", timeout=15, check=False)
        return r.stdout.strip() if r.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def model_alignment(formal_root, relative_inputs, expected_head):
    """Bind every consumed byte, runner included, to one exact Git commit.

    A GitHub candidate source checkout is verified separately. This function
    cannot assert anything about remote currentness or source/model equivalence.
    """
    if not expected_head:
        return {"status": "NOT_RUN", "reason": "No pinned experiment model HEAD"}
    if not isinstance(expected_head, str) or not SHA40.fullmatch(expected_head):
        return {"status": "BLOCKED", "reason": "Invalid experiment model HEAD"}
    root = Path(formal_root).resolve()
    repo = git(["rev-parse", "--show-toplevel"], root)
    if not repo or (Path(repo).resolve() / "formal") != root:
        return {"status": "BLOCKED", "reason": "Not a formal/ directory in an exact Git worktree"}
    actual_head = git(["rev-parse", "HEAD"], root)
    if actual_head != expected_head:
        return {"status": "BLOCKED", "reason": "Experiment HEAD mismatch",
                "expected_head": expected_head, "observed_head": actual_head}
    checks = []
    for relative in sorted(set(relative_inputs)):
        entry = {"path": relative, "status": "FAIL"}
        try:
            if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
                raise ValueError("Invalid relative path")
            p = (root / relative).resolve()
            if not p.is_relative_to(root) or not p.is_file():
                raise ValueError("Missing or escaping input")
            raw = p.read_bytes()
            actual_blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            git_path = "formal/" + relative.replace("\\", "/")
            pinned_blob = git(["rev-parse", "HEAD:" + git_path], root)
            entry.update({"git_blob": pinned_blob, "actual_blob": actual_blob,
                          "status": "PASS" if pinned_blob == actual_blob else "FAIL"})
        except (OSError, ValueError) as e:
            entry["error"] = str(e)
        checks.append(entry)
    return {"status": "PASS" if checks and all(c["status"] == "PASS" for c in checks) else "FAIL",
            "experiment_head": expected_head, "checks": checks}
