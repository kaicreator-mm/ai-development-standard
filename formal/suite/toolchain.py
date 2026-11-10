"""Exact binary identity for opt-in ADS formal checks; does not establish solver correctness."""
import hashlib
import shutil
import subprocess
from pathlib import Path


def _digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _binary(command):
    if not isinstance(command, str) or not command:
        return None
    resolved = shutil.which(command)
    path = Path(resolved or command).resolve()
    return path if path.is_file() else None


def _version(path, arg):
    try:
        proc = subprocess.run([str(path), arg], stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True, errors="replace",
                              check=False, timeout=15)
        return proc.returncode, proc.stdout[:4096]
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)


def toolchain_alignment(options, selected, inventory):
    """Check only tools used by selected cases, against a Git-pinned inventory.

    Run before and after solver execution; comparing hashes alone is not a proof
    that external binaries, dynamic dependencies, or their host are trustworthy.
    """
    kinds = sorted({case["tool"] for case in selected})
    if not kinds:
        return {"status": "NOT_RUN", "reason": "No selected tool cases", "checks": []}
    smokes = inventory.get("smokes", {}) if isinstance(inventory, dict) else {}
    checks = []
    for kind in kinds:
        expected = smokes.get(kind, {})
        if kind in ("z3", "cvc5"):
            command = getattr(options, kind, None)
            exe = _binary(command)
            required_hash = expected.get("binary_sha256")
            if not exe:
                checks.append({"tool": kind, "status": "NOT_RUN", "reason": "Tool executable unavailable"})
                continue
            try:
                observed = _digest(exe)
            except OSError as exc:
                checks.append({"tool": kind, "status": "FAIL",
                               "reason": "Cannot hash solver executable", "error": str(exc)})
                continue
            if not (isinstance(required_hash, str) and len(required_hash) == 64
                    and observed == required_hash):
                # Never call --version on an unknown binary. Version probing
                # itself executes executable code.
                checks.append({"tool": kind, "status": "FAIL",
                               "reason": "Solver SHA256 mismatch; version probe suppressed",
                               "binary_path": str(exe), "binary_sha256": observed,
                               "inventory_sha256": required_hash,
                               "version_probe_executed": False})
                continue
            code, output = _version(exe, "-version" if kind == "z3" else "--version")
            expected_version = expected.get("version")
            ok = (code == 0 and isinstance(expected_version, str)
                  and expected_version in output)
            checks.append({"tool": kind, "status": "PASS" if ok else "FAIL",
                           "binary_path": str(exe), "binary_sha256": observed,
                           "inventory_sha256": required_hash, "expected_version": expected_version,
                           "version_output": output[:180], "version_exit": code})
        elif kind == "tlc":
            jar_arg = getattr(options, "tlc_jar", None)
            jar = Path(jar_arg).resolve() if isinstance(jar_arg, str) and jar_arg else None
            java = _binary(getattr(options, "java", None))
            if not jar or not jar.is_file() or not java:
                checks.append({"tool": kind, "status": "NOT_RUN", "reason": "Java or TLC JAR unavailable"})
                continue
            try:
                observed = _digest(jar)
            except OSError as exc:
                checks.append({"tool": kind, "status": "FAIL",
                               "reason": "Cannot hash TLC JAR", "error": str(exc)})
                continue
            required_hash = expected.get("jar_sha256")
            if not (isinstance(required_hash, str) and len(required_hash) == 64
                    and observed == required_hash):
                checks.append({"tool": kind, "status": "FAIL",
                               "reason": "TLC JAR SHA256 mismatch; Java probe suppressed",
                               "jar_sha256": observed, "inventory_sha256": required_hash,
                               "java_version_probe_executed": False})
                continue
            # Java itself is not byte-pinned by this inventory; this probe
            # establishes runtime availability, not Java provenance.
            code, output = _version(java, "-version")
            ok = code == 0
            checks.append({"tool": kind, "status": "PASS" if ok else "FAIL",
                           "jar_sha256": observed, "inventory_sha256": required_hash,
                           "java_path": str(java), "java_version_output": output[:180],
                           "java_version_exit": code,
                           "java_binary_hash_pinned": False})
        else:
            checks.append({"tool": kind, "status": "FAIL", "reason": "Unsupported tool"})
    status = ("PASS" if all(c["status"] == "PASS" for c in checks) else
              "FAIL" if any(c["status"] == "FAIL" for c in checks) else "NOT_RUN")
    return {"status": status, "checks": checks,
            "note": "Binary/JAR hashes identify bytes only; Java and shared libraries are not fully provenance-pinned"}
