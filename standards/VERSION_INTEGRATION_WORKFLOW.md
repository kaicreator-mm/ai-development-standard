# Version Integration Workflow — v3.3 Compatibility Entry

This historical path remains for compatibility, but v3.3 removes its duplicated normative workflow text.

The active model is defined by:

- `DEVELOPMENT_WORKFLOW.md` — Version Branch vs Trunk/Fast Path, stage checkpoints and Task flow;
- `EXECUTION_ARCHITECTURE_STANDARD.md` — ready-set scheduling, merge control, validation ownership, freeze/release/repository controllers;
- `RELEASE_STANDARD.md` — Candidate Freeze, Release Qualification and final integration.

Canonical substantial-version shape remains:

```text
main
  └── version/vX.Y.Z
        ├── task/...
        └── fix/...
              ↓
        version/vX.Y.Z
              ↓
             main
```

Task/Fix concerns merge when their own authorized prerequisites are satisfied; full release confidence is re-established on the dependency-complete candidate at closure.

Historical `ai-dev:event:v1` comments remain valid history. New writers emit `ai-dev:event:v2` only.

This file MUST NOT be used as a second source of orchestration semantics.
