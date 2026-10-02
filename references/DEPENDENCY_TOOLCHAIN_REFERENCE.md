# Dependency & Toolchain Reference

This document is non-normative implementation guidance for `DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md`.

## 1. Node/npm example

A repository may declare:

```text
manifest authority: package.json
lock authority: package-lock.json
runtime dependencies: dependencies
development/test/build dependencies: devDependencies
compatibility: Node >= 22 < 27
supported lines: 22, 24, 26
preferred development: 26.x
certified tuple: Node 26.8.1 × ubuntu-24.04 × concern-regression
production deployment identity: Node 26.8.1
```

When `package-lock.json` is authoritative, `npm ci` is a reasonable frozen-install mapping. It is an example, not a universal command.

A transitive runtime vulnerability should retain a path such as:

```text
app -> framework-x -> parser-y@3.2.1
class=runtime
exposure=runtime-exposed
```

If the same package appears only below a test runner, the class/exposure should remain `test` / `test-only`; scanner severity alone should not collapse the distinction.

## 2. Python example

A Python project might use `pyproject.toml` as manifest authority and a generated lock file from uv/Poetry/PDM as authoritative resolution. Another project might intentionally use pinned requirements files. The project, not the Agent, decides which is authoritative.

Example facts:

```text
compatibility: Python >=3.12,<3.15
supported lines: 3.12, 3.13, 3.14
preferred development: 3.14
certification tuple: Python 3.14.7 × win32 × focused-contracts
```

A local Agent running Python 3.15-dev cannot rewrite the project to `>=3.15` because that runtime happens to be installed.

## 3. Rust example

For Rust/Cargo, `Cargo.toml` is normally the manifest and `Cargo.lock` may be authoritative depending on repository type/policy. A frozen build may use Cargo's locked resolution behavior. The project should distinguish the MSRV/compatibility floor from the current preferred stable toolchain and from actually certified tuples.

## 4. Risk exception example

A durable exception could state:

```text
exception_id=dep-risk-2026-014
advisory_id=GHSA-example
package=parser-y
version=3.2.1
dependency_class=runtime
dependency_path=app/framework-x/parser-y
exposure=runtime-exposed
severity=high
reason=no fixed version compatible with current public contract
mitigation=request size limit + disabled vulnerable feature
authority=security-owner
review_by=2026-10-31
release_scope=v4.1.x
status=accepted-risk
```

This record means risk was explicitly accepted for a scope. It does not mean the vulnerability was remediated, Validation passed, or a release is READY.

## 5. Applicability decision examples

Good:

```text
advisory present
class=test
path=project/test-runner/package-z
exposure=test-only
applicability=not runtime reachable under released artifact
reason/evidence recorded
```

Bad:

```text
severity=critical
therefore product FAIL
```

Also bad:

```text
scanner says vulnerable
package is transitive
therefore not applicable
```

Both skip required class/path/exposure reasoning.

## 6. Validation Impact examples

Changes that normally require explicit impact disposition include:

- lockfile resolves a different runtime transitive dependency;
- package registry/source changes;
- Node/Python/Rust compatibility floor changes;
- build toolchain version changes generated output;
- dependency moves from test-only to runtime path.

A documentation-only edit that merely explains an unchanged certified tuple may be evidence-preserving, but that conclusion belongs to the existing Validation Impact owner.

## 7. Supply-chain controls

SLSA-style provenance, registry allow-lists, signature verification, license checks and SBOM generation are useful patterns. They should become mandatory only when repository/project authority requires them. This reference intentionally does not select a universal scanner, registry, SBOM format or SLSA level.
