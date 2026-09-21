# Implementation Map — <task-id> @ <base_sha>

Exact-base implementation orientation. This is the only Task artifact that may reference base-relative file detail.

```yaml
areas:
  - path:                    # file/area on this exact base
    action:                  # create | modify | delete
    contract_link:           # which acceptance/contract item this serves
    notes:

out_of_scope_on_this_base: []
```

If the integration base advances and a mapped area changes materially, the pack classifies `PACK_STALE_MATERIAL` and this map is regenerated — not patched silently at execution time.
