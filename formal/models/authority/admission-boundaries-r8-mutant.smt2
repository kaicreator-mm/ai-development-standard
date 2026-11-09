; R8 deliberate historical-translation mutant: a successor does not require original
; Claim, independently authorized current successor, or an accepted successor Claim.
(set-logic QF_UF)
(declare-const originalClaim Bool)
(declare-const originalTerminal Bool)
(declare-const sameDispatch Bool)
(declare-const currentGeneration Bool)
(declare-const successorAuthorized Bool)
(declare-const successorClaimAccepted Bool)
(declare-const secondStartRecord Bool)
(assert (=> secondStartRecord (and originalTerminal (not sameDispatch) currentGeneration)))
; M01: inherited R6 I05 incorrectly admits a successor without a predecessor Claim.
(push 1) (assert secondStartRecord) (assert (not originalClaim)) (check-sat) (pop 1)
; M02: inherited R6 I05 wrongly admits a successor without its own authority.
(push 1) (assert secondStartRecord) (assert (not successorAuthorized)) (check-sat) (pop 1)
; M03: inherited R6 I05 wrongly calls an unaccepted proposal a Start Record.
(push 1) (assert secondStartRecord) (assert (not successorClaimAccepted)) (check-sat) (pop 1)
