; ADS-M-AUTHORITY bounded per-Task source mutation model; not full ADS equivalence.
(set-logic QF_UF)
(declare-const writerIsBuilder Bool)
(declare-const acceptedClaim Bool)
(declare-const writeSetAuthorized Bool)
(declare-const claimCurrent Bool)
(declare-const sourceMutation Bool)
(assert (=> sourceMutation (and writerIsBuilder acceptedClaim writeSetAuthorized claimCurrent)))
; Unauthorized role, missing Claim, or stale Claim is impossible.
(push 1) (assert sourceMutation) (assert (not writerIsBuilder)) (check-sat) (pop 1)
(push 1) (assert sourceMutation) (assert (not acceptedClaim)) (check-sat) (pop 1)
(push 1) (assert sourceMutation) (assert (not claimCurrent)) (check-sat) (pop 1)
(push 1) (assert sourceMutation) (assert (not writeSetAuthorized)) (check-sat) (pop 1)
; Nonvacuous legal Builder witness.
(push 1) (assert sourceMutation) (check-sat) (pop 1)
