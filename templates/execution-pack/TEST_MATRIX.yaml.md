# Test Matrix — <task-id> @ <base_sha>

Required checks mapped onto the exact base. Focused first; full required set before publication.

```yaml
focused:                     # fastest signal for the implementation loop
  - name:
    command:
    expected:

required:                    # must pass on the stable candidate HEAD before push
  - name:
    command:
    expected:

task_owned_platform:         # real-host/platform checks this task intrinsically owns
  - name:                    # use "NOT_RUN — reason" / "BLOCKED — reason" honestly
    command:
    expected:
```

Rules:

- PASS binds to the exact tested SHA × real environment × toolchain × profile.
- After any source change, rerun affected validation before publishing.
- Never delete/weaken a check to obtain green.
