# ADS v4.14 real GitHub smoke — report summary

Work item: https://github.com/kaicreator-mm/ai-dev-pilot/issues/20
Isolated PR: https://github.com/kaicreator-mm/ai-dev-pilot/pull/21
Source under test: smoke/v414_greeting.py (blob 133e39f1a57d66268869ef01401280a6fc8095a4)
Initial source commit: e3ec778a825569f56bdbbb39f6164b154035509d

Observed:
- Real GitHub Issue and PR created and fetched.
- GitHub source file content matched exact local git blob hash.
- python smoke/v414_greeting.py ran three assertions: expected greeting, Unicode greeting, blank-value rejection.

Not established:
- No actual upstream LLM provider usage, token count or billing.
- No OSS/S3 private object permission test.
- No independent review, source-wide CI or Release PASS.

Coverage: PARTIAL. Claim scope is isolated repository GitHub CRUD + tiny local executable smoke.
