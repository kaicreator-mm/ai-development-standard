; ADS-M-AUTHORITY / ADS-P-CAS: serialized competing admissions.
; Bounded two requests and two protected keys; native SMT-LIB, not an ADS scheduler.
; Source: EXECUTION_ARCHITECTURE_STANDARD.md §11.1 and GITHUB_AGENT_INTERACTION_PROTOCOL.md §8.5
(set-logic QF_LIA)
(declare-const generation Int)
(declare-const otherKeyGeneration Int)
(declare-const expectedFirst Int)
(declare-const expectedSecond Int)
(declare-const firstAuthorized Bool)
(declare-const firstReady Bool)
(declare-const secondAuthorized Bool)
(declare-const secondReady Bool)
(declare-const sameProtectedKey Bool)
(declare-const firstClosed Bool)
(declare-const firstAccepted Bool)
(declare-const secondAccepted Bool)
(assert (>= generation 0))
(assert (>= otherKeyGeneration 0))
(assert (= firstAccepted (and firstAuthorized firstReady (= expectedFirst generation))))
(assert (=> firstClosed firstAccepted))
(define-fun secondCurrentGeneration () Int
  (ite sameProtectedKey (ite firstAccepted (+ generation 1) generation) otherKeyGeneration))
(assert (= secondAccepted
  (and secondAuthorized secondReady (= expectedSecond secondCurrentGeneration)
       (or (not sameProtectedKey) (not firstAccepted) firstClosed))))
; C01: a rejected authorization cannot become an accepted first claim.
(push 1) (assert firstAccepted) (assert (not firstAuthorized)) (check-sat) (pop 1)
; C02: incompatible claims cannot both be active for the same protected key.
(push 1) (assert firstAccepted) (assert secondAccepted)
         (assert sameProtectedKey) (assert (not firstClosed)) (check-sat) (pop 1)
; C03: stale generation does not become current merely because previous claim closed.
(push 1) (assert firstAccepted) (assert firstClosed) (assert sameProtectedKey)
         (assert (= expectedSecond generation)) (assert secondAccepted) (check-sat) (pop 1)
; C04: one sequential, newly current claim can follow a finished claim.
(push 1) (assert firstAccepted) (assert firstClosed) (assert sameProtectedKey)
         (assert (= expectedSecond (+ generation 1)))
         (assert secondAccepted) (check-sat) (pop 1)
; C05: independent protected keys may have two simultaneous accepted claims.
(push 1) (assert firstAccepted) (assert (not firstClosed))
         (assert (not sameProtectedKey))
         (assert (= expectedSecond otherKeyGeneration))
         (assert secondAccepted) (check-sat) (pop 1)
; C06: the second claim also requires its own authority.
(push 1) (assert secondAccepted) (assert (not secondAuthorized)) (check-sat) (pop 1)
