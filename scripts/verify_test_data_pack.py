from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{lineno}: case must be an object")
        rows.append(value)
    return rows


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(pack: Path) -> list[str]:
    errors: list[str] = []

    manifest_path = pack / "manifest.json"
    if not manifest_path.is_file():
        return ["missing manifest.json"]

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for key in ["pack_id", "purpose", "privacy_classification", "provenance", "dimensions", "files"]:
        if key not in manifest:
            errors.append(f"manifest missing {key}")

    files = manifest.get("files", {})
    required_file_keys = ["curated_cases", "generated_cases", "schema_invalid_cases", "scenario_matrix", "coverage"]
    for key in required_file_keys:
        rel = files.get(key)
        if not rel:
            errors.append(f"manifest.files missing {key}")
        elif not (pack / rel).is_file():
            errors.append(f"missing file for {key}: {rel}")

    if errors:
        return errors

    provenance_ids = {item.get("id") for item in manifest.get("provenance", []) if isinstance(item, dict)}
    if None in provenance_ids:
        errors.append("provenance item missing id")

    dimensions = manifest.get("dimensions", {})
    required_dimensions = {name for name, spec in dimensions.items() if spec.get("required")}
    for name, spec in dimensions.items():
        if not spec.get("rationale"):
            errors.append(f"dimension {name} missing rationale")
        if spec.get("required") and not spec.get("values"):
            errors.append(f"required dimension {name} missing declared values")

    curated_path = pack / files["curated_cases"]
    generated_path = pack / files["generated_cases"]
    invalid_path = pack / files["schema_invalid_cases"]

    curated = load_jsonl(curated_path)
    generated = load_jsonl(generated_path)
    invalid = load_jsonl(invalid_path)
    normal_cases = curated + generated

    ids: set[str] = set()
    covered_values: dict[str, set[str]] = {name: set() for name in required_dimensions}

    def check_common(case: dict, source: str) -> None:
        case_id = case.get("id")
        if not case_id:
            errors.append(f"{source}: case missing id")
            return
        if case_id in ids:
            errors.append(f"duplicate case id: {case_id}")
        ids.add(case_id)

        refs = case.get("provenance", [])
        unknown = set(refs) - provenance_ids
        if unknown:
            errors.append(f"{case_id}: unknown provenance {sorted(unknown)}")
        if not case.get("rationale"):
            errors.append(f"{case_id}: missing rationale")

    for case in normal_cases:
        check_common(case, "valid-case")
        case_id = case.get("id", "<unknown>")
        dims = case.get("dimensions", {})
        missing = required_dimensions - set(dims)
        if missing:
            errors.append(f"{case_id}: missing required dimensions {sorted(missing)}")
        for name in required_dimensions:
            if name in dims:
                covered_values[name].add(str(dims[name]))

        expected = case.get("expected")
        if not isinstance(expected, dict):
            errors.append(f"{case_id}: missing expected object")
        else:
            if "decision" not in expected:
                errors.append(f"{case_id}: expected.decision missing")
            if "invariants" not in expected:
                errors.append(f"{case_id}: expected.invariants missing")
            if "allowed_variation" not in expected:
                errors.append(f"{case_id}: expected.allowed_variation missing")

        if case.get("class") in {"golden", "regression"}:
            if case.get("review", {}).get("status") != "approved":
                errors.append(f"{case_id}: golden/regression case is not approved")

    for case in invalid:
        check_common(case, "schema-invalid")
        case_id = case.get("id", "<unknown>")
        if case.get("class") != "schema_invalid":
            errors.append(f"{case_id}: schema-invalid file contains class={case.get('class')!r}")
        if not case.get("expected_validation_error"):
            errors.append(f"{case_id}: expected_validation_error missing")

    for name, spec in dimensions.items():
        if not spec.get("required"):
            continue
        declared = {str(v) for v in spec.get("values", [])}
        missing = declared - covered_values.get(name, set())
        if missing:
            errors.append(f"dimension {name} missing declared values {sorted(missing)}")

    matrix = json.loads((pack / files["scenario_matrix"]).read_text(encoding="utf-8"))
    for risk in matrix.get("required_scenarios", []):
        covered_by = risk.get("covered_by", [])
        if not covered_by:
            errors.append(f"risk {risk.get('risk')} has no covered_by cases")
        unknown = set(covered_by) - ids
        if unknown:
            errors.append(f"risk {risk.get('risk')} references unknown cases {sorted(unknown)}")

    coverage = json.loads((pack / files["coverage"]).read_text(encoding="utf-8"))
    repro = coverage.get("reproducibility", {})
    hash_map = {
        "curated_cases_sha256": curated_path,
        "generated_cases_sha256": generated_path,
        "schema_invalid_sha256": invalid_path,
    }
    for key, path in hash_map.items():
        expected_hash = repro.get(key)
        if not expected_hash:
            errors.append(f"coverage.reproducibility missing {key}")
        elif expected_hash != sha256(path):
            errors.append(f"hash mismatch for {path.relative_to(pack)}")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/verify_test_data_pack.py <pack-dir>")
        return 2

    pack = Path(sys.argv[1]).resolve()
    try:
        errors = verify(pack)
    except Exception as exc:  # audit-friendly single failure surface
        print(f"test-data pack verification: FAIL\n- {exc}")
        return 1

    if errors:
        print("test-data pack verification: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("test-data pack verification: PASS")
    print(f"pack: {pack}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
