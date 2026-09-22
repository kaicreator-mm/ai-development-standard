# Execution Pack MANIFEST

```yaml
pack_id:                       # stable pack identity
task_id:
repository:
version:
base_sha:                      # exact integration base bound at generation (40-hex)
task_pack_ref:                 # Task Pack identity this pack serves
branch:                        # JIT task branch created from base_sha
parent_issue:                  # "#NN" when materialized
pr:                            # "#NN" when applicable
agent_freedom:                 # F0_MECHANICAL | F1_BOUNDED_IMPLEMENTATION | F2_ENGINEERING_DISCRETION | F3_ARCHITECTURE_REQUIRED
pinned_standard_revision:      # 40-hex standard commit
generated_by:                  # logical operator id (e.g. chatgpt-web:web-a)
generated_at:
dependency_completion: []      # entries: "<task-id>@<40-hex completion/merge SHA>"
material_paths:                # required to prove PACK_STALE_NONMATERIAL; omit => base drift fails closed to MATERIAL
  - <path-or-directory-prefix>
core_artifacts:                # exactly the six core names, no placeholders
  - MANIFEST.yaml
  - EXECUTION_CONTRACT.md
  - TEST_MATRIX.yaml
  - FAILURE_MATRIX.yaml
  - IMPLEMENTATION_MAP.md
  - REVIEW_CHECKLIST.md
optional_artifacts: []         # e.g. INTERFACE_SEED.ts, SEMANTIC_KERNEL.md, LOCAL_AGENT_PROMPT.md
retention:                     # durable | transient | full-provenance
package_excluded: true         # must be excludable from shipped artifacts
pack_state_at_generation: PACK_CURRENT
```

Claim-time verification (by the worker, fail closed):

```text
pack base_sha          vs current integration SHA
task_pack_ref          vs Task Pack identity
dependency_completion  vs current dependency facts
pinned_standard_revision vs pinned standard
branch                 vs branch identity
material_paths         vs current base delta when base_sha moved
core_artifacts         must contain each required core artifact exactly once
```

Classification: `PACK_CURRENT / PACK_STALE_NONMATERIAL / PACK_STALE_MATERIAL / PACK_INVALID`. The executor MUST NOT silently rewrite `base_sha`.

`PACK_STALE_NONMATERIAL` is an optimization that requires positive impact coverage. When the base moved and `material_paths` is absent, empty, malformed, or the delta cannot be established, classification MUST fail closed to `PACK_STALE_MATERIAL`.
