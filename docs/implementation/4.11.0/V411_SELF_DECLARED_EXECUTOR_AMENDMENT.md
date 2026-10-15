# V4.11 Scoped Amendment — Self-Declared Executor Identity; Owner-Credential Gates Removed for Standards Closure (Issue #1122)

Status: prospective policy amendment to the v4.11 line, integrated on `version/v4.11.0` (baseline `214f6a97b1eed948e1afef8f5089eb4bf4b97d26`).

## 1. Change authority

Direct current user direction, 2026-10-15 (Issue #1122; process authority also recorded at #1021@6191737577):

> “剔除所有 owner 相关的校验，并且不能用GitHub账号作为执行体的判断方式，由执行体自己声明的为准，并相信执行体的声明，这是正常开发，不需要怀疑这些。”

This amendment supersedes, **prospectively and for this repository only**, the former process requirement to independently establish credentials/delegations of Product/Architecture/Release/Review owners for ADS's own standards-repository development and closure. It introduces no new Owner verification machinery.

## 2. Normative successor behavior

1. **Executor attribution is self-declared.** An execution event's `actor_role`, `operator_kind`, `operator_id`, `session_ref` and optional `delegation` are supplied by that executor and accepted as the attribution source (`GITHUB_AGENT_INTERACTION_PROTOCOL.md` §5, §8.1.1). `transport_actor` is metadata only; GitHub login/account sharing, GitHub-native review identity and separate human credential checks are NOT release admission predicates.
2. **No Owner credential check** for ADS's own design, Task, PR Review, Validation and Release workflow. A declared `release-controller` or appropriate process executor makes scope-bound gate applicability decisions from product/technical facts (`RELEASE_STANDARD.md` §11.7). Reviewer independence, when policy requires it, uses distinct **declared logical operator/context**, not GitHub identity (§7).
3. **Engineering facts are still validated** exactly as before: exact SHA/currentness, actual source diff, validation tuples, tests and failing assertions, observed side effects, mutually contradictory events. Identity self-declaration establishes attribution, not a successful test, an externally executed action or a release PASS. A quoted fake event embedded inside untrusted tool/code content is still not a canonical workflow event (§8.1.1 input classes unchanged).
4. **Standards-only release scope.** An actual independently authenticated human-DENY end-to-end execution (`real_human_authority_deny_e2e`) is removed as a standards release prerequisite. The public labels `REAL_HUMAN_DENY_E2E_NOT_PROVEN` / `REAL_NATIVE_CLAIM_AND_RELEASE_RUNTIME_NOT_PROVEN` remain mandatory, truthful, and never convertible to `PASS`; the synthetic SQLite test nature is unchanged; the normative DENY behavior is preserved for adopters that implement actual protected effects.
5. **Successor semantics, not history rewrite.** Signed prior #1021@6189674540 row7 `REQUIRED_NOW`/`BLOCKED` was accurate at its subject under the then-current workflow and is not retroactively promoted. Postchange successor candidates evaluate release applicability under this new explicit user authorization, identity self-declaration, and real evidence only. Historical raw outcomes (139 scripts 125 exit0/14 exit1, raw guarded T12 exit1, 20/28/4, v4.9 frozen-blob guard failures) remain literal; no rerun, no greenwash.
6. **GBK #1121 is a separate concern** (PR #1121, two encoding-argument edits) with its own review and targeted real-Windows evidence; historical predecessor immutable pins are classified by validation impact, not rewritten.

## 3. Bounded edit surface of this amendment

- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` — §5 (self-declared attribution), §7 (declared-context reviewer independence), §8.1.1 (admission predicate attribution leg; untrusted-quoted-event boundary unchanged), §9.4 (declared reviewer authority; conflict/currentness bullets unchanged).
- `standards/RELEASE_STANDARD.md` — §11.1 (`NOT_APPLICABLE` basis wording) and new §11.7 (standards-repository executor authority; human-DENY E2E not a standards prerequisite).
- `AGENTS.md` — top-level hard-constraint guidance for agents reading the pinned standard.
- Focused deterministic tests: `scripts/test_v411_i1122_self_declared_executor.py` (this amendment's contract) and bounded semantic updates to `scripts/test_v411_t05_event_authority.py` (declared-attribution admission gate, declared-context reviewer independence, human-act boundary preserved), plus exact-successor-blob pin re-binds in the existing shared-pin guards (`test_v411_merge_admission.py`, `test_v49_gate_currentness.py`, `test_v49_conformance_suite.py`, `test_v49_integrated_dogfood.py`) — pin constants only, every other assertion unchanged, historical pins stay re-derivable from their immutable base objects.

## 4. Explicitly preserved (not weakened)

- Canonical event structure and currentness: §8.1 admission predicate, §9.1 exact-subject currentness, §9.3 deterministic aggregation, atomic rejection reasons.
- The untrusted-input boundary: raw/quoted `actor_role=reviewer` / `HUMAN_APPROVED` text acquires no right and mints no Review/human/Claim/gate mutation (§8.1.1 ¶1, §9.4 bullet 1).
- Gate vocabulary `PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE`; `UNKNOWN` stays fail-closed; no new event family, state dimension or schema.
- Frozen v4.11 planning documents (`PRD.md`, `L2_ARCHITECTURE_EVIDENCE.md`, `PRODUCT_PROOF_MATRIX.md`, `TASK_DAG.md`, `task-packs/`) are not edited by this amendment; their historical statements remain accurate at their own subjects.
- All other security, validation and release requirements (Hidden Validation independence, thaw/invalidation, `NOT_RUN`/`BLOCKED` non-conversion) are unchanged.
