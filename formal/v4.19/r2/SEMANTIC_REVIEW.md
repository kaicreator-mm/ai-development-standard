# R2 finite-DAG repair and lifecycle replay

- Maintains R1 immutably; five-domain model and receipt remain auditable.
- R2 corrects the **model coverage defect** in R1: a three-edge triangle check is insufficient for even all cycles on three nodes.
- R2 rank-based finite model covers **all 12 possible directed edges between four nodes**; each selected edge requires strictly increasing integer rank, making any cycle in that bounded four-node universe UNSAT. The SAT witness allows legitimate edges and the no-edges graph. This is not a general, unbounded DAG theorem or proof that ADS native Task DAG is cycle-free.
- Deliberate mutant omits rank implication for edge D→A, so the injected A→B→C→D→A cycle becomes SAT. Z3/cvc5 each detect it.
- Exact existing R0 TLC model/config Git blobs are reused as-is, NOT replaced by a new lifecycle state machine. Actual TLC 2.19 traversal: normal **27 distinct states, exit 0**; unsafe Claim **7 distinct states, SingleWriter violation, exit 12**; unsafe Release **3 distinct states, LifecycleSafe violation, exit 12**.
- All new and reused native SMT cases verified with Z3 5.3.3 and cvc5 1.4.2; 19 total cases: 13 PASS_MODEL and 6 deliberate COUNTEREXAMPLE; six solver differential comparisons PASS.
- All six source-map Git blobs and text anchors were independently read back from the pinned PR #1365 HEAD in GitHub: 6/6 alignment. This does **not** satisfy the Python runner's separate exact-checkout source byte verification, which stays NOT_RUN.
- No claim of independent semantic reviewer, full ADS rule denominator, actual Claim CAS, liveness with fairness, real CI/Release, or universal graph safety. No normative ADS defect has been demonstrated.
