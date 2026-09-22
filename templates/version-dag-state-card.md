# Version DAG State Card — <version>

`NON_AUTHORITATIVE_DERIVED_STATE`

Generated/reduced from GitHub durable facts. This card MUST NOT be edited as the canonical live workflow state.

## Snapshot Identity

- version/milestone: `<version>`
- reduced at: `<timestamp/run/ref>`
- planning DAG: `<ref>`

## Nodes

| Task | Issue | Derived state | Blocking dependencies | PR/dispatch |
|---|---|---|---|---|
| `<T-ID>` | `#N` | `<state>` | `<refs|none>` | `<refs>` |

## READY

- `<T-ID / Issue>`

## RUNNING

- `<T-ID / Issue>`

## BLOCKED

- `<T-ID / Issue> ← <dependency/blocker>`

## Closure

- `<remaining version gates>`

## Authority Notice

If this card disagrees with current Issues, native Issue Dependencies, PR HEAD/evidence, or structured events, recompute the card. Do not rewrite GitHub truth to match this projection.
