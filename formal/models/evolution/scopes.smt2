; ADS-M-EVOLUTION prospective policy cannot self-activate in frozen historical scope.
(set-logic QF_UF)
(declare-const historicalSubject Bool)
(declare-const historicalEligible Bool)
(declare-const prospectiveApproved Bool)
(declare-const localBuilderMutation Bool)
(assert (=> localBuilderMutation
  (ite historicalSubject historicalEligible prospectiveApproved)))
; Historical denial survives proposed future permission.
(push 1) (assert historicalSubject) (assert (not historicalEligible))
 (assert prospectiveApproved) (assert localBuilderMutation) (check-sat) (pop 1)
; Prospective approval cannot substitute an actual authorization for a new Task.
(push 1) (assert (not historicalSubject)) (assert (not prospectiveApproved))
 (assert localBuilderMutation) (check-sat) (pop 1)
; Historical grandfathering and approved prospective path remain possible.
(push 1) (assert historicalSubject) (assert historicalEligible)
 (assert localBuilderMutation) (check-sat) (pop 1)
(push 1) (assert (not historicalSubject)) (assert prospectiveApproved)
 (assert localBuilderMutation) (check-sat) (pop 1)
