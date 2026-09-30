# Java Language Profile

```yaml
profile_id: language.java
profile_version: 1
profile_kind: language
applicability: Java source/JDK/build/runtime concern is material
core_owner_refs:
  - standards/IMPLEMENTATION_QUALITY_STANDARD.md
  - standards/DEPENDENCY_TOOLCHAIN_STANDARD.md
source_or_ecosystem_refs: project build descriptors, JDK/toolchain configuration, source/module layout and CI
project_check_mappings: project-selected compile/test/static/package checks
high_risk_semantics: source/target/release compatibility, JDK vendor/runtime tuple, generated sources, public API/module behavior
compatibility_notes: supported Java/JDK target, preferred developer JDK and tested deployment JDK are distinct
```

Status: v4.3 language mapping, not a mandatory Maven/Gradle choice or a second Toolchain/Testing authority.

## Project-owned build and JDK semantics

The repository's Maven `pom.xml`, Gradle settings/build files or other documented build entrypoints determine the applicable build system. Read `--release`, source/target/toolchain settings and public API/module boundaries where material. A JDK available on an Agent workstation cannot redefine declared compatibility, preferred development toolchain, or a certified target/runtime tuple. A successful compile against one JDK does not establish all supported JDK versions or deployment execution.

## Tests, static checks and generated source

Map actual project-selected compiler, unit/integration test, static-analysis, packaging and CI entrypoints. Maven, Gradle, Checkstyle, Error Prone, SpotBugs and other tools are examples only, not universal requirements. Generated sources, annotation-processor output and generated clients must preserve canonical input and regeneration authority; direct edits to output do not satisfy that contract. Public interface and exception behavior changes may require compatibility evidence beyond a green build.

## Applicability and conflict

If this project does not materially use Java, Fast Path permits non-applicability without empty profile records. Unverified vendor/JDK/target behavior stays UNKNOWN with bounded exact-tuple Validation. Compose with an independently applicable archetype and non-weakening PROJECT_OVERRIDES. Frozen/Core/project authority wins conflicts; profile file order, default tools and local JDK availability confer no policy authority or Validation/Release PASS.
