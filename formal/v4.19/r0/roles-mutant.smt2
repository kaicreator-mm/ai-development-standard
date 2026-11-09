; Intentionally BROKEN abstraction: a validator source-write capability is accidentally allowed.
; This is a fault-injection positive control, NOT an ADS source defect.
(set-logic ALL)
(declare-datatypes () ((Role builder validator reviewer)))
(declare-datatypes () ((Profile WEB_BUILDER LOCAL_BUILDER LOCAL_VALIDATION)))
(declare-const role Role)
(declare-const profile Profile)
(declare-const acceptedClaim Bool)
(declare-const authorizedWriteSet Bool)
(declare-const sourceWrite Bool)
(assert (=> (= profile LOCAL_VALIDATION) (= role validator)))
; BUG: missing (= role builder) from sourceWrite antecedent.
(assert (=> sourceWrite (and acceptedClaim authorizedWriteSet)))
(assert (= profile LOCAL_VALIDATION))
(assert sourceWrite)
(check-sat)
