"""R20: fail-closed audit of recorded R17 unittest IDs, not a fresh test run."""
from __future__ import annotations
import ast
import hashlib
import json
import re
import sys
from pathlib import Path

PINNED = {
    "formal/v4.19/r13/test_binding_preflight.py": "b9aff1904388a22203a902dce122b45c56cb0cd9",
    "formal/v4.19/r13/test_source_binding.py": "10702d29c0609cac171a86f8149dd23de88f02a3",
    "formal/v4.19/r17/R17_PYTHON_BINDING_TESTS_LOG.txt": "ccbfc7563a9387b8fe49d879376b8363dfc470ab",
    "formal/v4.19/r17/R17_PYTHON_BINDING_TESTS_RECEIPT.json": "e0aa244fbb7304a299088ea27139d24bbafe71fc",
}
SUBJECT_HEAD = "c5eb69c3fcd47ca934b4b87c8004131add6ad5d2"
SOURCE_FILES = tuple(path for path in PINNED if path.endswith(".py"))
LOG_PATH = "formal/v4.19/r17/R17_PYTHON_BINDING_TESTS_LOG.txt"
RECEIPT_PATH = "formal/v4.19/r17/R17_PYTHON_BINDING_TESTS_RECEIPT.json"
HEADER = re.compile(r"^== R17 Python input-binding tests — environment ([12]):", re.M)
CASE = re.compile(r"^(test_\w+) \((test_\w+)\.(\w+)\.(test_\w+)\)", re.M)
SUMMARY = re.compile(r"^Ran (\d+) tests? in ", re.M)


class AuditBlocked(ValueError):
    pass


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def declared_ids(data: bytes, module: str) -> set[str]:
    tree = ast.parse(data.decode("utf-8"))
    result: set[str] = set()
    for cls in tree.body:
        if not isinstance(cls, ast.ClassDef):
            continue
        for member in cls.body:
            if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)) and member.name.startswith("test_"):
                key = f"{module}.{cls.name}.{member.name}"
                if key in result:
                    raise AuditBlocked("duplicate test declaration: " + key)
                result.add(key)
    if not result:
        raise AuditBlocked("empty declared test source: " + module)
    return result


def execution_sections(log: str) -> list[str]:
    positions = [m.start() for m in HEADER.finditer(log)]
    labels = [m.group(1) for m in HEADER.finditer(log)]
    if labels != ["1", "2"] or not positions:
        raise AuditBlocked("missing/reordered R17 environment headers")
    if log[:positions[0]].strip():
        raise AuditBlocked("unexpected prefix before first environment")
    return [log[positions[i]:positions[i + 1] if i + 1 < len(positions) else len(log)]
            for i in range(len(positions))]


def observed_ids(block: str) -> list[str]:
    result = []
    for m in CASE.finditer(block):
        if m.group(1) != m.group(4):
            raise AuditBlocked("test name disagrees with fully qualified identity")
        result.append(f"{m.group(2)}.{m.group(3)}.{m.group(4)}")
    successes = len(re.findall(r"\.\.\. ok\s*$", block, re.M))
    if successes != len(result) or not block.rstrip().endswith("OK"):
        raise AuditBlocked("non-OK/missing unittest method outcome")
    if not result:
        raise AuditBlocked("zero observed tests")
    return result


def audit(root: Path) -> dict:
    root = root.resolve()
    inputs = {}
    for path, pin in PINNED.items():
        file = (root / path).resolve()
        if not file.is_relative_to(root) or not file.is_file():
            raise AuditBlocked("missing/escaping exact-source input: " + path)
        data = file.read_bytes()
        if git_blob(data) != pin:
            raise AuditBlocked("exact Git blob mismatch: " + path)
        inputs[path] = data
    declared = set()
    file_counts = {}
    for path in SOURCE_FILES:
        entries = declared_ids(inputs[path], Path(path).stem)
        if declared & entries:
            raise AuditBlocked("duplicate ID across source files")
        declared.update(entries)
        file_counts[path] = len(entries)
    if len(declared) != 13 or sorted(file_counts.values()) != [6, 7]:
        raise AuditBlocked("R17 frozen declared inventory unexpectedly changed")
    receipt = json.loads(inputs[RECEIPT_PATH].decode("utf-8"))
    if receipt["worktree"]["head_at_execution"] != SUBJECT_HEAD:
        raise AuditBlocked("receipt claims wrong exact execution HEAD")
    if hashlib.sha256(inputs[LOG_PATH]).hexdigest() != receipt["combined_log_sha256"]:
        raise AuditBlocked("combined original log SHA256 mismatch")
    registered = {row["path"]: row for row in receipt["tested_code"]["test_files"]}
    if set(registered) != set(SOURCE_FILES) or any(
        registered[path]["git_blob"] != PINNED[path] or
        registered[path]["tests"] != file_counts[path] for path in SOURCE_FILES
    ):
        raise AuditBlocked("receipt source/count provenance mismatch")
    sections = execution_sections(inputs[LOG_PATH].decode("utf-8"))
    runs = receipt["executions"]
    if len(runs) != 2:
        raise AuditBlocked("missing execution receipt for either environment")
    results = []
    for i, (block, run) in enumerate(zip(sections, runs, strict=True)):
        observed = observed_ids(block)
        if len(set(observed)) != len(observed):
            raise AuditBlocked("duplicate executed test ID in environment " + str(i + 1))
        if set(observed) != declared:
            raise AuditBlocked("missing/extra executed test IDs in environment " + str(i + 1))
        summary = SUMMARY.findall(block)
        if len(summary) != 1 or int(summary[0]) != len(observed):
            raise AuditBlocked("unittest reported count differs from ID inventory")
        if (run["tests_run"] != len(observed) or run["exit_code"] != 0 or
            any(run[k] != 0 for k in ("skipped", "errors", "failures")) or
            run["result"] != "OK"):
            raise AuditBlocked("machine receipt disagrees with observed execution")
        if (i == 0 and "WSL2" not in run["environment"]) or (
            i == 1 and "Windows" not in run["environment"]):
            raise AuditBlocked("execution environment metadata is missing")
        results.append({"environment": run["environment"], "observed_ids": sorted(observed),
                        "executed_count": len(observed), "missing": [], "extra": [],
                        "result": "PASS_RECORDED_LOG_INVENTORY"})
    return {"schema": "ads/formal-r20-executed-inventory-audit/v1",
            "source_execution_head": SUBJECT_HEAD,
            "status": "PASS_RECORDED_EXACT_BLOB_EXECUTION_INVENTORY",
            "declared_count": len(declared), "declared_ids": sorted(declared),
            "source_git_blobs": dict(PINNED), "environments": results,
            "limits": ["Readback of existing execution logs; tests were NOT rerun",
                       "Does not independently attest the host or reconstruct raw per-host log digests",
                       "Does not prove candidate natural-language/SMT equivalence, real Claim/CAS or all ADS rules"]}


if __name__ == "__main__":
    try:
        print(json.dumps(audit(Path(__file__).resolve().parents[3]), indent=2))
    except (AuditBlocked, OSError, ValueError, KeyError, SyntaxError) as exc:
        print(json.dumps({"status": "BLOCK", "reason": str(exc)}, indent=2))
        sys.exit(2)
