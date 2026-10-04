# v4.4 T05 non-container build/package/install dogfood

Status: **implementation candidate; real exact-SHA Validation and Fresh Independent Review required**. This is a Python-stdlib `zipapp` exercise, **not** a production package, approved release artifact, multi-OS guarantee or universal installer requirement.

## Executable subject

`python scripts/test_v44_build_package_conformance.py` runs on the actual executor's Python/platform tuple and uses committed `source_v1/__main__.py` and `source_v2/__main__.py`. It builds real `.pyz` files, records source-tree digest + explicit test build-profile reference + interpreter/platform tuple + output SHA-256, applies a bounded content-policy scan, requires a test-only promotion authority reference to copy bytes into a content-addressed immutable store, copies that artifact into an isolated mutable install location, executes the **installed** `.pyz` using the actual interpreter, upgrades that same install alias to v2 and executes it again. The script also injects `.env`, `secrets/`, `__pycache__/` and Agent-cache leakage negatives and exercises tampered bytes / missing promotion authority.

These fixtures intentionally test **one non-container Python zipapp build/install tuple only**. The actual platform/interpreter and source/output digests must be reported from the exact-SHA clean Validation run, not inferred from this document. The `test-only/t05` promotion authority proves an explicit gate in the dogfood model; it does not grant production publication, live side effects, Distribution or Release Qualification.

## Required evidence and boundaries

Validation must bind exact PR HEAD, version-branch baseline, actual interpreter/platform, fixture paths/digests, command/exit codes, generated package/content digest, installed version 1 and upgraded version 2 behavior, negative policy results and clean worktree. A different rebuilt SHA does not inherit previous qualification merely because the install filename is unchanged. A package/build check cannot prove historical consumer compatibility, unrelated target OS installation, hidden validation, real provider access, Deployment SUCCESS or Release READY.

If the validator lacks an actual runnable Python/zipapp tuple, record `BLOCKED` and hand off the exact subject to a real Build Host; do not label the static fixtures `PASS`. The owning Build/Artifact standard and Release/Validation owners retain their independent conclusions.
