; ADS-M-EVIDENCE SHA is an abstract identity sort, not cryptographic verification.
(set-logic QF_UF)
(declare-sort Sha 0)
(declare-const currentHead Sha)
(declare-const ciHead Sha)
(declare-const reviewHead Sha)
(declare-const ciPass Bool)
(declare-const reviewPass Bool)
(declare-const acceptedClaim Bool)
(declare-const qualified Bool)
(assert (=> qualified (and acceptedClaim ciPass reviewPass
  (= currentHead ciHead) (= currentHead reviewHead))))
; Stale CI/review and NOT_PASS cannot qualify.
(push 1) (assert qualified) (assert (distinct currentHead ciHead)) (check-sat) (pop 1)
(push 1) (assert qualified) (assert (distinct currentHead reviewHead)) (check-sat) (pop 1)
(push 1) (assert qualified) (assert (not ciPass)) (check-sat) (pop 1)
(push 1) (assert qualified) (assert (not acceptedClaim)) (check-sat) (pop 1)
; Legitimate current evidence remains satisfiable.
(push 1) (assert qualified) (check-sat) (pop 1)
