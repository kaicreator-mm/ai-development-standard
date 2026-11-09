; Deliberately broken model: permits mutation without accepted Claim.
(set-logic QF_UF)
(declare-const writerIsBuilder Bool)
(declare-const acceptedClaim Bool)
(declare-const sourceMutation Bool)
(assert (=> sourceMutation writerIsBuilder))
(assert sourceMutation)
(assert (not acceptedClaim))
(check-sat)
