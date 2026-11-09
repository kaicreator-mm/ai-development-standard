# R2 concrete counterexamples and positive witnesses

## TLC original model, exact Git blob

Source `formal/v4.19/r0/ADSWorkflow.tla` blob `a1ed4d67716f2c836e8eed5337f003b4da8570d9`. TLC 2.19 actually executed all three exact config files.

- Normal `UnsafeClaim=FALSE, UnsafeRelease=FALSE`: exit 0, 53 states generated, **27 distinct states**, `TypeOK`, `LifecycleSafe`, `SingleWriter` never violated in bounded state graph.
- Injected `UnsafeClaim=TRUE`: exit 12; 7 distinct states; trace `Init → FreezeProduct → FreezeL2 → FreezeDAG → Claim(web) → Claim(local)`. Final state has `activeWriters={"web","local"}`, violating `SingleWriter`. This is a **fault injection**, not an ADS design counterexample.
- Injected `UnsafeRelease=TRUE`: exit 12; 3 distinct states; trace `Init → Release`, `released=TRUE` with every Freeze/CI/Review/Closure prerequisite FALSE. Violates `LifecycleSafe`, again an injected fault.

## Four-node SMT

- `ranked-4.smt2` has 12 directed edge variables, each constrained `edge(U,V) => rank(U)<rank(V)`.
- Two-, three-, four-node cycles are each UNSAT; legal non-cyclic graph A→B, A→C, C→D is SAT; empty graph SAT.
- `ranked-4-mutant.smt2` deliberately removes D→A rank implication. The cycle A→B→C→D→A becomes SAT in both Z3 and cvc5. One concrete satisfying assignment is `rA=0,rB=1,rC=2,rD=3` with those four edges selected and all other edges absent; confirmed SAT independently in both solvers.
- These witnesses establish *finite model checks*, not actual GitHub Task DAG validity or universal theorem.

## Limitations

Solver equality does not validate natural language mapping. Model includes no self-dependency edge (U→U); native Issue Dependency graph ingestion and larger graphs remain NOT_PROVEN. Reviewer independence and current source checkout remain NOT_RUN.
