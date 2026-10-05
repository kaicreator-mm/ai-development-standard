from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipapp
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "docs" / "implementation" / "4.4.0" / "dogfood" / "build-package"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def content_policy(source: Path) -> None:
    """Minimal v4.4 dogfood policy; owning project may impose stricter policy."""
    if not (source / "__main__.py").is_file():
        raise ValueError("package entrypoint missing")
    for path in source.rglob("*"):
        relative = path.relative_to(source)
        names = {piece.lower() for piece in relative.parts}
        if names.intersection({".git", "__pycache__", ".env", "secrets", "agent-cache"}):
            raise ValueError(f"package content-policy violation: {relative}")
        if path.is_file() and (path.suffix.lower() in {".pyc", ".key", ".pem"} or "secret" in path.name.lower()):
            raise ValueError(f"package content-policy violation: {relative}")


def tree_digest(source: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in source.rglob("*") if p.is_file()):
        digest.update(path.relative_to(source).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def build_zipapp(source: Path, target: Path, *, profile_ref: str) -> dict:
    if not profile_ref:
        raise ValueError("material build profile ref is required")
    content_policy(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    zipapp.create_archive(source, target=target)
    return {
        "source_ref": source.relative_to(ROOT).as_posix(),
        "exact_source_digest": tree_digest(source),
        "profile_ref": profile_ref,
        "toolchain_tuple": {
            "implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
        "build_output_sha256": sha256(target),
        "artifact_class": "BUILD_OUTPUT_ONLY",
    }


def trial_promote(build: dict, built: Path, store: Path, *, authority_ref: str) -> tuple[Path, dict]:
    """Test-only promotion model; not a real Release/Distribution authorization."""
    if not authority_ref:
        raise PermissionError("trial promotion requires explicit authority reference")
    digest = sha256(built)
    if digest != build["build_output_sha256"]:
        raise ValueError("build output changed after recorded identity")
    store.mkdir(parents=True, exist_ok=True)
    immutable = store / f"sha256-{digest}.pyz"
    if immutable.exists() and sha256(immutable) != digest:
        raise ValueError("immutable artifact identity collision")
    shutil.copyfile(built, immutable)
    return immutable, {
        "artifact_sha256": digest,
        "exact_source_digest": build["exact_source_digest"],
        "profile_ref": build["profile_ref"],
        "toolchain_tuple": build["toolchain_tuple"],
        "trial_authority_ref": authority_ref,
        "evidence_scope": "TEST_ONLY_NOT_RELEASE_QUALIFICATION",
    }


def install_and_run(immutable: Path, install_dir: Path) -> tuple[str, dict]:
    install_dir.mkdir(parents=True, exist_ok=True)
    installed = install_dir / "tool.pyz"  # deliberately mutable local install alias
    shutil.copyfile(immutable, installed)
    completed = subprocess.run([sys.executable, str(installed)], text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise AssertionError(f"installed package execution failed: {completed.stderr}")
    return sha256(installed), json.loads(completed.stdout)


class BuildPackageDogfoodTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="v44-noncontainer-package-")
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def build(self, version: int) -> tuple[Path, dict]:
        source = FIXTURES / f"source_v{version}"
        output = self.root / f"build-v{version}.pyz"
        record = build_zipapp(source, output, profile_ref="dogfood/python-zipapp-v1")
        return output, record

    def test_real_noncontainer_build_promotion_install_execution(self) -> None:
        output, record = self.build(1)
        self.assertEqual(record["artifact_class"], "BUILD_OUTPUT_ONLY")
        self.assertEqual(record["build_output_sha256"], sha256(output))
        immutable, promoted = trial_promote(record, output, self.root / "store", authority_ref="test-only/t05")
        self.assertEqual(promoted["artifact_sha256"], sha256(immutable))
        installed_digest, result = install_and_run(immutable, self.root / "installed")
        self.assertEqual(installed_digest, promoted["artifact_sha256"])
        self.assertEqual(result, {"tool": "ads-v44-package-dogfood", "version": "1", "contract": "cli-json-v1"})
        with zipfile.ZipFile(immutable) as archive:
            self.assertIn("__main__.py", archive.namelist())
            self.assertNotIn(".env", archive.namelist())

    def test_exact_source_profile_toolchain_output_binding(self) -> None:
        output, record = self.build(1)
        self.assertEqual(record["exact_source_digest"], tree_digest(FIXTURES / "source_v1"))
        self.assertEqual(record["profile_ref"], "dogfood/python-zipapp-v1")
        self.assertEqual(record["toolchain_tuple"]["python_version"], platform.python_version())
        self.assertEqual(record["toolchain_tuple"]["platform"], platform.platform())
        self.assertEqual(record["build_output_sha256"], sha256(output))

    def test_rebuilt_bytes_cannot_inherit_prior_promotion_through_install_alias(self) -> None:
        first_output, first = self.build(1)
        first_artifact, first_record = trial_promote(first, first_output, self.root / "store", authority_ref="test-only/t05")
        first_installed, first_run = install_and_run(first_artifact, self.root / "installed")
        second_output, second = self.build(2)
        second_artifact, second_record = trial_promote(second, second_output, self.root / "store", authority_ref="test-only/t05")
        second_installed, second_run = install_and_run(second_artifact, self.root / "installed")
        self.assertNotEqual(first["exact_source_digest"], second["exact_source_digest"])
        self.assertNotEqual(first_record["artifact_sha256"], second_record["artifact_sha256"])
        self.assertNotEqual(first_installed, second_installed)
        self.assertEqual(first_run["version"], "1")
        self.assertEqual(second_run["version"], "2")
        self.assertEqual(second_installed, second_record["artifact_sha256"])
        self.assertNotEqual(first_record["artifact_sha256"], second_installed)

    def test_content_policy_rejects_secrets_cache_and_runtime_leakage(self) -> None:
        for relative in (".env", "secrets/credential.txt", "__pycache__/main.pyc", "agent-cache/log.txt"):
            with self.subTest(relative=relative):
                source = self.root / f"bad-{len(list(self.root.iterdir()))}"
                shutil.copytree(FIXTURES / "source_v1", source)
                extra = source / relative
                extra.parent.mkdir(parents=True, exist_ok=True)
                extra.write_text("not-a-real-credential", encoding="utf-8")
                with self.assertRaises(ValueError):
                    build_zipapp(source, self.root / f"bad-{source.name}.pyz", profile_ref="dogfood/python-zipapp-v1")

    def test_promotion_requires_authority_and_correct_output_identity(self) -> None:
        output, record = self.build(1)
        with self.assertRaises(PermissionError):
            trial_promote(record, output, self.root / "store", authority_ref="")
        tampered = self.root / "tampered.pyz"
        shutil.copyfile(output, tampered)
        with tampered.open("ab") as stream:
            stream.write(b"changed-bytes")
        with self.assertRaises(ValueError):
            trial_promote(record, tampered, self.root / "store", authority_ref="test-only/t05")


if __name__ == "__main__":
    unittest.main()
