from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "profiles" / "languages"
FRAMEWORK = (ROOT / "profiles" / "README.md").read_text(encoding="utf-8")


class GoJavaRustProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = {name: (PROFILES / f"{name}.md").read_text(encoding="utf-8") for name in ("go", "java", "rust")}

    def test_stable_profile_identity_and_authority_boundary(self) -> None:
        for name, text in self.profiles.items():
            for token in (f"language.{name}", "profile_version: 1", "profile_kind: language", "core_owner_refs:", "source_or_ecosystem_refs:", "project_check_mappings:", "high_risk_semantics:", "compatibility_notes:", "PROJECT_OVERRIDES", "Frozen/Core"):
                self.assertIn(token, text)
            self.assertIn("UNKNOWN", text)
            self.assertIn("Fast Path", text)
            self.assertIn("Agent", text)
        self.assertIn("File/discovery order MUST NOT choose a winner", FRAMEWORK)

    def test_go_module_toolchain_concurrency_and_generated_mapping(self) -> None:
        text = self.profiles["go"]
        for token in ("go.mod", "go.sum", "go.work", "toolchain", "go test", "go build", "go vet", "race", "concurrency", "context", "build tags", "generated-source", "certified build tuple"):
            self.assertIn(token, text)
        self.assertIn("installed `go` binary does not prove", text)

    def test_java_jdk_build_static_and_generated_mapping(self) -> None:
        text = self.profiles["java"]
        for token in ("JDK", "Maven", "Gradle", "--release", "source/target", "deployment JDK", "static-analysis", "annotation-processor", "generated", "examples only", "not universal"):
            self.assertIn(token, text)
        self.assertIn("A JDK available on an Agent workstation cannot redefine", text)

    def test_rust_cargo_msrv_features_targets_and_unsafe_mapping(self) -> None:
        text = self.profiles["rust"]
        for token in ("Cargo.toml", "Cargo.lock", "rust-toolchain.toml", "MSRV", "features", "target", "unsafe", "FFI", "cargo check", "cargo test", "cargo build", "cargo fmt", "cargo clippy", "generated"):
            self.assertIn(token, text)
        self.assertIn("installed compiler is execution capability", text)

    def test_no_language_profile_grants_result_or_local_tool_authority(self) -> None:
        for text in self.profiles.values():
            self.assertIn("Validation", text)
            self.assertIn("authority", text)
        self.assertIn("profile says check X -> CI X passed", FRAMEWORK)
        self.assertIn("tool installed -> project selected that tool", FRAMEWORK)


if __name__ == "__main__":
    unittest.main()
