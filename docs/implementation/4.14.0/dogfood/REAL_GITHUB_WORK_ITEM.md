<!-- ads:github -->
```yaml
schema: ads/github/v3
kind: work_item
data:
  profile: type:task
  contract:
    task_id: ADS-V414-SMOKE-01
    goal: Prove real GitHub Issue and PR lifecycle for ADS v4.14
    integration_target: smoke/v414-base
    baseline_sha: eb1a7328a6d7429fc5ffa502ed762f469c5aedcc
    review_policy: recommended
    required_gates:
      - concern
    acceptance:
      - Exact Issue body readback with validated v3 schema
      - A real isolated code file PR and native GitHub update
      - Direct v3 Agent Event comment and Task Report comment
      - Verified close and reopen readback
      - Pin actual smoke PR and readback source identities
```

# v4.14 live smoke — structured GitHub interaction

This is a **bounded disposable validation project** for [ADS v4.14 #1187](https://github.com/kaicreator-mm/ai-development-standard/issues/1187) on `version/v4.14`. It does not authorize changes to `ai-dev-pilot/main` or ordinary outstanding work.

## Scope and controls
- Source baseline: `ai-dev-pilot/main@eb1a7328a6d7429fc5ffa502ed762f469c5aedcc`.
- Only `smoke/v414-task` → `smoke/v414-base` can merge.
- Smoke code is deliberately tiny; no service/credential/CI secret/deployment effects.
- A v3 machine-contract check establishes **shape only**. Native GitHub readback after each effect is separate.
- Report may only claim a real Manifest checksum if its bytes were independently stored and verified; otherwise record `NOT_RUN`.
- On completion close this smoke Issue; original business Issues remain untouched.
