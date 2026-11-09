; ADS-M-DEPENDENCY three-node DAG / two-task concurrent Writer finite abstraction.
(set-logic QF_UF)
(declare-const ab Bool)
(declare-const bc Bool)
(declare-const ca Bool)
(declare-const runA Bool)
(declare-const runB Bool)
(declare-const sharedWriteSet Bool)
(declare-const dependenciesSatisfied Bool)
; Only a length-3 cycle is represented, NOT a general DAG acyclicity proof.
(assert (not (and ab bc ca)))
(assert (=> (or runA runB) dependenciesSatisfied))
(assert (=> (and runA runB) (not sharedWriteSet)))
; Cycle and write-set collision forbidden.
(push 1) (assert ab) (assert bc) (assert ca) (check-sat) (pop 1)
(push 1) (assert runA) (assert runB) (assert sharedWriteSet) (check-sat) (pop 1)
(push 1) (assert runA) (assert (not dependenciesSatisfied)) (check-sat) (pop 1)
; Independent lanes can run together when write sets do not overlap.
(push 1) (assert runA) (assert runB) (assert (not sharedWriteSet)) (check-sat) (pop 1)
