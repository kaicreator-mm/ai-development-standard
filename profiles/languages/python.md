# Python Language Profile

```yaml
profile_id: language.python
profile_version: 1
profile_kind: language
applicability: Python source/interpreter/package/runtime concern is material to the project
core_owner_refs:
  - standards/IMPLEMENTATION_QUALITY_STANDARD.md
  - standards/DEPENDENCY_TOOLCHAIN_STANDARD.md
source_or_ecosystem_refs:
  - repository pyproject.toml, requirements, constraints and/or selected lock, when applicable
  - project package/import layout and test/build/CI entrypoints
project_check_mappings: project-selected import, type/static, test, build and packaging checks
high_risk_semantics: interpreter range, environment isolation, dependency resolution, public import surface, generated-source ownership
compatibility_notes: supported interpreter range, preferred development interpreter and certified execution/package tuple are different claims
```

Status: **v4.3 subordinate ecosystem mapping**, not a separate policy or mandatory environment manager. Frozen/Core and non-weakening PROJECT_OVERRIDES remain the owning authority.

## Manifest and environment mapping

Python repositories may derive dependency/package truth from `pyproject.toml`, requirements/constraints files, an adopted lockfile or a project-specific combination. Determine which is canonical from durable project facts; do not mandate Poetry, uv, pip, pip-tools, Hatch or any one workflow globally. Distinguish declared interpreter compatibility from a preferred developer interpreter and the exact certified build/test/deployment interpreter. An Agent's locally installed Python cannot redefine repository compatibility or substitute for an unexecuted target tuple.

## Implementation and packaging mapping

Where material, identify package layout, namespace/import paths, editable versus installed-package behavior, public error/API behavior, and environment isolation from project authority. Test invocation from a checkout is not automatically proof that an installed wheel/sdist imports or executes correctly. Generated source, protocol clients and packaged output remain subordinate to their canonical generation sources and regeneration process. Build success, static-check success and runtime/install success are distinct evidence claims.

## Project-owned checks and Fast Path

Map the repository's actual test, type/static, lint, formatter and build entrypoints (e.g. pytest/unittest, mypy/pyright, Ruff, `python -m build`) when explicitly selected and materially relevant; none is universally mandatory. A non-code or non-Python change need not create empty profile records. Unsupported or unverified ecosystem behavior remains UNKNOWN with a bounded exact-tuple Validation request rather than guessed support.

## Composition and failure handling

Apply Frozen/Core requirements, then the language mapping and any independent archetype mapping, then legitimate PROJECT_OVERRIDES specialization. This profile cannot weaken the owning Testing/Dependency/Toolchain/CI/Validation/Release rules. Material profile/project conflicts fail closed to the appropriate project/architecture owner rather than being resolved by file order or Agent preference.
