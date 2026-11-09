; ADS-M-CROSS / ADS-P-WRITER-KEYS: protected Claim key and source write set
; are distinct safety dimensions. Bounded 2-claim / 2-writer model.
; Distinct keys do not by themselves grant concurrent overlapping source writes.
(set-logic QF_UF)
(declare-const claimA Bool)
(declare-const claimB Bool)
(declare-const activeA Bool)
(declare-const activeB Bool)
(declare-const authorizedA Bool)
(declare-const authorizedB Bool)
(declare-const sameProtectedKey Bool)
(declare-const writeSetsKnown Bool)
(declare-const writeSetsOverlap Bool)
(declare-const writeA Bool)
(declare-const writeB Bool)
(assert (=> writeA (and claimA activeA authorizedA)))
(assert (=> writeB (and claimB activeB authorizedB)))
; Claim admission must not allow active incompatible same-key claims.
(assert (=> (and claimA claimB activeA activeB) (not sameProtectedKey)))
; Concurrent source writes need disjoint known write sets, even across distinct keys.
(assert (=> (and writeA writeB) (and writeSetsKnown (not writeSetsOverlap))))
; W01: different claim keys cannot bypass write-set collision.
(push 1) (assert writeA) (assert writeB) (assert (not sameProtectedKey))
 (assert writeSetsOverlap) (check-sat) (pop 1)
; W02: unknown write-set relationship is fail-closed for concurrent writes.
(push 1) (assert writeA) (assert writeB) (assert (not writeSetsKnown))
 (check-sat) (pop 1)
; W03: accepted Claim on A alone cannot authorize A after it becomes inactive.
(push 1) (assert writeA) (assert (not activeA)) (check-sat) (pop 1)
; W04: disjoint known source writes with distinct keys are permitted.
(push 1) (assert writeA) (assert writeB) (assert (not sameProtectedKey))
 (assert writeSetsKnown) (assert (not writeSetsOverlap)) (check-sat) (pop 1)
; W05: distinct key Claims can coexist even when their write sets overlap
; as long as they are not both mutating source concurrently.
(push 1) (assert claimA) (assert claimB) (assert (not sameProtectedKey))
 (assert writeSetsKnown) (assert writeSetsOverlap)
 (assert writeA) (assert (not writeB)) (check-sat) (pop 1)
; W06: role/Task authorization for B is never derived from A's Claim.
(push 1) (assert writeB) (assert (not authorizedB)) (check-sat) (pop 1)
