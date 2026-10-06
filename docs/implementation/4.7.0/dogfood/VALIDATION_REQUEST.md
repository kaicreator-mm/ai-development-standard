# T08 Exact-Subject Validation Request

This request is for the independent T08 Validator required by Frozen T08. It is not Builder self-Validation and does not carry a PASS verdict.

## Subject binding

Do **not** copy a historical SHA from this file. At dispatch time, the Controller/Builder handoff must state and the Validator must independently re-read all of the following live durable facts:

- repository: `kaicreator-mm/ai-development-standard`;
- task: Issue #352;
- implementation PR: #624;
- implementation branch: `task/352-v47-fresh-agent-self-dogfood`;
- exact final PR HEAD and its tree;
- PR base branch `version/v4.7.0` and exact current base SHA;
- Frozen T08 Task Pack blob `168acd4acf3e23fbb3ca3f6197e4192cb05a9f50`;
- T08 L3 blob `6a2000cf9b8bf8024450eb5f0f0704960140095f`;
- Execution Pack planning HEAD `92a516c05400fae5c57d70a57c5c36dc085dd1cd` / tree `5b2f75f2896fcc839b1db24b483aced94cf39318`.

The external Validation issue/comment created after the immutable Builder HEAD exists is the exact-subject binding. This file intentionally avoids embedding the final HEAD/tree because editing the file to self-bind would itself create a successor HEAD.

Any mismatch in HEAD/tree, materially changed base, Task/pack identity, or relevant currentness is `BLOCKED`; evidence does not transfer.

## Required environment / independence

Use an independent capable environment and a genuinely fresh logical Agent/session that did not participate in the #352 Builder context. Freshness is about logical task context: same/different user, account, provider, credential, or transport neither proves nor disproves it by itself.

The REAL session must start only from the durable pointers listed in `README.md` / `reconstruction.json` (or their live GitHub equivalents), not from hidden prior task chat.

No private chain-of-thought is requested. Record only observable session/operator reference, durable inputs, recovered structured facts, commands/results where applicable, and the final outcome/blocker.

## Validation matrix

1. Re-read Issue #352, PR #624, branch, final exact HEAD/tree, and `version/v4.7.0` base live.
2. Confirm the implementation delta after planning HEAD `92a516c...` stays within:
   - `docs/implementation/4.7.0/dogfood/**`
   - `scripts/test_v47_fresh_agent_dogfood.py`
3. Run `python scripts/test_v47_fresh_agent_dogfood.py` on the exact implementation HEAD.
4. Run the current T05/T07 focused suites required by their canonical surfaces, including `python scripts/test_v47_semantic_conformance.py` and the repository-required verification commands applicable to the exact subject.
5. Execute a **REAL_FRESH_SESSION** scenario. Give the new logical session only durable pointers and require it to recover:
   - pinned ADS/current authority;
   - canonical owner(s) for the concern, including T05/T07 composition;
   - applicable profiles/overrides;
   - Issue #352 / PR #624 / exact final HEAD/tree / expected base;
   - allowed mutation and workflow side-effect authority;
   - required Validation/Review gates;
   - next action or blocker.
6. Adversarially verify:
   - a prior chat-only fact is unnecessary;
   - stale lower-authority memory cannot override live GitHub/repository facts;
   - same account/transport alone yields no independence claim;
   - static fixture/test PASS cannot be promoted to REAL session PASS;
   - stale Issue/PR/HEAD/base is detected and blocks rather than being silently consumed.
7. Record REAL evidence classification and observable fresh-session identity. If the REAL session cannot actually be executed, result remains `NOT_RUN/BLOCKED`; do not issue Validation PASS.

## Required terminal fields

The Validator should publish a durable terminal bound to the immutable subject containing at least:

- `T08_VALIDATION_RESULT=PASS|FAIL|BLOCKED`
- `VALIDATED_HEAD=<40-char SHA>`
- `VALIDATED_TREE=<40-char tree>`
- `EXPECTED_BASE=<40-char SHA>`
- `TASK_PACK_BLOB=168acd4acf3e23fbb3ca3f6197e4192cb05a9f50`
- `EXECUTION_PACK_HEAD=92a516c05400fae5c57d70a57c5c36dc085dd1cd`
- `WRITE_SET=PASS|FAIL`
- `STATIC_RECONSTRUCTION=PASS|FAIL`
- `REAL_FRESH_SESSION=PASS|FAIL|NOT_RUN/BLOCKED`
- `CURRENTNESS=PASS|FAIL`
- `FRESH_REVIEW_ADMISSION=YES|NO`
- `FINDINGS=<bounded findings or NONE>`

Only `T08_VALIDATION_RESULT=PASS` with `REAL_FRESH_SESSION=PASS` on the unchanged exact subject admits a genuinely new READ-ONLY Fresh Independent Review. Validation never grants merge, Version Closure, or Release authority.
