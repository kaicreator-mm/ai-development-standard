"""Verify the real two-solver checker fails when vital constraints are removed."""
import hashlib
import json
import tempfile
from pathlib import Path
import run_proofs as proof

MUTATIONS = [
    ("drop_effective_pin", "pinResolved schemaBytesVerified", "schemaBytesVerified"),
    ("drop_checked_schema_identity", "(= checkedSchema pinnedSchema)", "true"),
    ("drop_published_payload_identity", "(= publishedPayload validatedPayload)", "true"),
    ("drop_schema_pass", "prePublicationCheckCompleted schemaPass authorityAndClaimCurrent", "prePublicationCheckCompleted authorityAndClaimCurrent"),
    ("drop_publish_serialization", "publicationSerialized (= checkedSchema pinnedSchema)", "(= checkedSchema pinnedSchema)"),
    ("drop_acceptance_guard", "(assert (=> (or acceptedDispatch acceptedClaimMutation) publishAdmissible))", "(assert true)"),
]

def test():
    proof.assert_model_hashes("mutation-source-preflight")
    proof.assert_tool_hashes()
    source = (proof.ROOT / "publish-safety.smt2").read_text()
    results = []
    with tempfile.TemporaryDirectory(prefix="ads1366-mutate-") as tmp:
        tmp = Path(tmp)
        for name, needle, replacement in MUTATIONS:
            assert source.count(needle) == 1, (name, source.count(needle))
            trial = tmp / "publish-safety.smt2"
            trial.write_text(source.replace(needle, replacement, 1))
            checks = [proof.run_solver(tool, trial) for tool in proof.COMMANDS]
            first_difference = [i + 1 for i, (actual, expect) in enumerate(zip(checks[0]["statuses"], proof.EXPECTED[trial.name])) if actual != expect]
            rejected = (all(r["exit_code"] == 0 for r in checks)
                        and not any(r["matched"] for r in checks)
                        and checks[0]["statuses"] == checks[1]["statuses"]
                        and bool(first_difference))
            results.append({"mutation":name,"rejected":rejected,"changed_query_indices_one_based":first_difference,
                "z3_actual":checks[0]["statuses"],"cvc5_actual":checks[1]["statuses"],
                "mutated_sha256":hashlib.sha256(trial.read_bytes()).hexdigest()})
    proof.assert_model_hashes("mutation-source-postflight")
    proof.assert_tool_hashes()
    return {"schema":"ads/formal-r13-adversarial-mutation/v2","mutations":results,
       "tested_count":len(results),"rejected_count":sum(r["rejected"] for r in results),
       "verdict":"PASS" if all(r["rejected"] for r in results) else "FAIL"}
if __name__ == "__main__":
    r = test()
    print(json.dumps(r, indent=2))
    raise SystemExit(0 if r["verdict"] == "PASS" else 1)
