# T-003 Review Checklist

- Exact JIT base is `33dfb8f05bca1ba8fd4ea8d9a2c63eaa8f9aa830`; T-015/#522 is merged and canonical.
- Builder first proves or disproves a concrete Interchange gap; `NO_CHANGE_REQUIRED` is acceptable.
- Existing `ai-dev/interchange-v1` remains the sole generic envelope family and `ai-dev:event:v2` remains GitHub writer/admission authority.
- Receiver/capability/eligibility semantics are referenced through durable owner facts; no ad-hoc capability object or fourth Exchange family is introduced.
- Envelope remains `CORRELATION_ONLY_NON_AUTHORITATIVE`; ACK/delivery/progress is not Review/Validation/workflow truth.
- Replay/conflict/currentness/durable reconstruction and historical compatibility remain intact.
- Default source diff is compatibility reference + focused test only. Any schema/protocol mutation requires proven gap and explicit Execution Pack rebind.
- Focused test, protocol regression and repository verifier pass on exact candidate.
- Independent Validation precedes genuinely Fresh required Review.
