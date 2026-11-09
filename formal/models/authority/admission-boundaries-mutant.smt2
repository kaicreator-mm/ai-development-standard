; THREE intentionally weakened translations; these are MODEL mutants, not ADS defects.
(set-logic QF_UF)
; Lost S1 serialized-reservation guard: two same-key active READY dispatches.
(declare-const reserveA Bool)
(declare-const reserveB Bool)
(declare-const sameKey Bool)
(declare-const activeA Bool)
(push 1) (assert reserveA) (assert reserveB) (assert sameKey) (assert activeA)
 (check-sat) (pop 1)
; Lost S2 idempotency guard: re-claim emits an extra Start Record.
(declare-const sameDispatch Bool)
(declare-const sameOperator Bool)
(declare-const resume Bool)
(declare-const secondStartRecord Bool)
(push 1) (assert sameDispatch) (assert sameOperator) (assert resume)
 (assert secondStartRecord) (check-sat) (pop 1)
; Lost S3 grant-currentness guard: unauthorized parallel same-work claims.
(declare-const parallelSameWorkRole Bool)
(declare-const nonDefaultGroup Bool)
(declare-const grantCurrent Bool)
(push 1) (assert parallelSameWorkRole) (assert nonDefaultGroup)
 (assert (not grantCurrent)) (check-sat) (pop 1)
