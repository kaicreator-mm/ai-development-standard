; INJECTED DEFECT: generation CAS alone does not exclude an overlapping active writer.
; If the "no incompatible active claim" guard is lost, both can be accepted.
(set-logic QF_LIA)
(declare-const generation Int)
(declare-const expectedFirst Int)
(declare-const expectedSecond Int)
(declare-const firstAccepted Bool)
(declare-const secondAccepted Bool)
(assert (>= generation 0))
(assert (= firstAccepted (= expectedFirst generation)))
(assert (= secondAccepted (= expectedSecond (ite firstAccepted (+ generation 1) generation))))
(assert firstAccepted)
(assert secondAccepted)
(assert (= expectedFirst generation))
(assert (= expectedSecond (+ generation 1)))
; Deliberately no firstClosed, no incompatible-active guard.
(check-sat)
