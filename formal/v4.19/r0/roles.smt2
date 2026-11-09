; ADS v4.19 R0 formal experiment: selected dispatch & source-write properties.
; MODEL of pinned candidate, NOT a normative proof of every natural-language clause.
(set-logic ALL)
(declare-datatypes () ((Role builder validator reviewer)))
(declare-datatypes () ((Profile WEB_BUILDER LOCAL_BUILDER LOCAL_VALIDATION LOCAL_VALIDATOR WEB_REVIEWER)))
(declare-datatypes () ((Env WEB LOCAL)))
(declare-const role Role)
(declare-const profile Profile)
(declare-const env Env)
(declare-const acceptedClaim Bool)
(declare-const authorizedWriteSet Bool)
(declare-const sourceWrite Bool)
(declare-const historicalTask Bool)
(declare-const historicalLocalBuilderEligible Bool)
(declare-const prospectivePolicyAuthorized Bool)

; Role / profile / environment maps, excluding the two orthogonal validation profiles.
(assert (or
  (and (= profile WEB_BUILDER) (= role builder) (= env WEB))
  (and (= profile LOCAL_BUILDER) (= role builder) (= env LOCAL))
  (and (= profile LOCAL_VALIDATION) (= role validator) (= env LOCAL))
  (and (= profile LOCAL_VALIDATOR) (= role validator) (= env LOCAL))
  (and (= profile WEB_REVIEWER) (= role reviewer) (= env WEB))))
; Source mutation requires builder authority, an accepted claim, and accepted write set.
(assert (=> sourceWrite (and (= role builder) acceptedClaim authorizedWriteSet)))
; Prospective v4.19 policy does not retroactively override historical #1353.
(assert (=> (and sourceWrite (= profile LOCAL_BUILDER) historicalTask)
            historicalLocalBuilderEligible))
(assert (=> (and sourceWrite (= profile LOCAL_BUILDER) (not historicalTask))
            prospectivePolicyAuthorized))

; R01: validator cannot mutate product source: UNSAT
(push 1) (assert (= profile LOCAL_VALIDATION)) (assert sourceWrite) (check-sat) (pop 1)
; R02: LOCAL_VALIDATION cannot disguise builder role: UNSAT
(push 1) (assert (= profile LOCAL_VALIDATION)) (assert (= role builder)) (check-sat) (pop 1)
; R03: WEB_BUILDER cannot route to LOCAL: UNSAT
(push 1) (assert (= profile WEB_BUILDER)) (assert (= env LOCAL)) (check-sat) (pop 1)
; R04: writing without accepted claim: UNSAT
(push 1) (assert sourceWrite) (assert (not acceptedClaim)) (check-sat) (pop 1)
; R05: writing outside authorized write set: UNSAT
(push 1) (assert sourceWrite) (assert (not authorizedWriteSet)) (check-sat) (pop 1)
; R06: historic non-grandfathered LOCAL_BUILDER cannot write: UNSAT
(push 1) (assert sourceWrite) (assert (= profile LOCAL_BUILDER)) (assert historicalTask) (assert (not historicalLocalBuilderEligible)) (check-sat) (pop 1)
; R07: new LOCAL_BUILDER without prospective policy cannot write: UNSAT
(push 1) (assert sourceWrite) (assert (= profile LOCAL_BUILDER)) (assert (not historicalTask)) (assert (not prospectivePolicyAuthorized)) (check-sat) (pop 1)
; R08: valid WEB_BUILDER can write: SAT
(push 1) (assert sourceWrite) (assert (= profile WEB_BUILDER)) (check-sat) (pop 1)
; R09: approved prospective LOCAL_BUILDER may write: SAT
(push 1) (assert sourceWrite) (assert (= profile LOCAL_BUILDER)) (assert (not historicalTask)) (assert prospectivePolicyAuthorized) (check-sat) (pop 1)
; R10: historically eligible LOCAL_BUILDER may write: SAT
(push 1) (assert sourceWrite) (assert (= profile LOCAL_BUILDER)) (assert historicalTask) (assert historicalLocalBuilderEligible) (check-sat) (pop 1)
; R11: reviewer cannot write: UNSAT
(push 1) (assert sourceWrite) (assert (= profile WEB_REVIEWER)) (check-sat) (pop 1)
; R12: LOCAL_VALIDATOR cannot claim WEB environment: UNSAT
(push 1) (assert (= profile LOCAL_VALIDATOR)) (assert (= env WEB)) (check-sat) (pop 1)
