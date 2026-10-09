"""U02 lost-ACK external-effect experiment harness (Issue #949).

Stage-2 architecture research demo. Real components under test:

- a real local git repository as the durable Git fact plane (real objects,
  real commits, real HEAD SHA / generation readback);
- event payloads validated against the repository's own
  ``schemas/agent-event-v2.schema.json`` via the repo's own validator
  (``scripts/test_v48_execution_ownership.py``);
- a real append-only file effect sink whose persistent mutation count and
  effect IDs are observable;
- real, separately launched OS processes for actor A / successor B (and C),
  including real hard process kill for the lost-ACK injection.

Deterministic fakes: the "external system" behind the sink is a local file
adapter (authorized by the Issue); no LLM, no network, no GitHub writes.
"""
