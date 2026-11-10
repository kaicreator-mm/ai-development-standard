; ADS #1366 / old R8 model coverage-gap probe.
; `reservedA` below is copied from the R8 admission-boundaries SMT definition.
; It is a RESERVATION proxy, NOT a real GitHub Claim/Dispatch acceptance.
(set-logic QF_LIA)
(declare-const g Int)
(declare-const expectedA Int)
(declare-const readyA Bool)
(declare-const publicationAmbiguous Bool)
(assert (>= g 0))
(define-fun reservedA () Bool (and readyA (= expectedA g) (not publicationAmbiguous)))
; These new predicates are absent from the R8 reservation guard.
(declare-const pinnedSchemaCurrent Bool)
(declare-const actualPayloadEqualsValidated Bool)
(declare-const schemaPassed Bool)
; G1: A reservation can exist despite an unresolved schema pin.
(push 1)
(assert reservedA)
(assert (not pinnedSchemaCurrent))
(check-sat)
(pop 1)
; G2: A reservation can exist despite a validation-vs-write payload mismatch.
(push 1)
(assert reservedA)
(assert (not actualPayloadEqualsValidated))
(check-sat)
(pop 1)
; G3: A reservation can exist despite an unpassed dispatch schema.
(push 1)
(assert reservedA)
(assert (not schemaPassed))
(check-sat)
(pop 1)
; G4: The old reservation guard is not vacuous.
(push 1)
(assert reservedA)
(check-sat)
(pop 1)
