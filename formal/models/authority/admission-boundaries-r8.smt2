; ADS-M-AUTHORITY / three R5 semantic gaps: reservation, idempotence, group grants.
; Bounded two schedulers and one protected key. No real GitHub transaction is modeled.
(set-logic QF_LIA)
; S1: reservation and later claim must share one generation/serialization point.
(declare-const g Int)
(declare-const expectedA Int)
(declare-const expectedB Int)
(declare-const readyA Bool)
(declare-const readyB Bool)
(declare-const terminalA Bool)
(declare-const publicationAmbiguous Bool)
(assert (>= g 0))
(define-fun reservedA () Bool (and readyA (= expectedA g) (not publicationAmbiguous)))
(define-fun reservedB () Bool (and readyB
  (= expectedB (ite reservedA (+ g 1) g))
  (or (not reservedA) terminalA) (not publicationAmbiguous)))
; R01: simultaneous incompatible READY/QUEUED reservations cannot both succeed.
(push 1) (assert reservedA) (assert reservedB) (assert (not terminalA)) (check-sat) (pop 1)
; R02: stale second proposal cannot win after first reservation becomes terminal.
(push 1) (assert reservedA) (assert terminalA) (assert reservedB)
  (assert (= expectedB g)) (check-sat) (pop 1)
; R03: unresolved publication outcome blocks another acceptance.
(push 1) (assert publicationAmbiguous) (assert reservedB) (check-sat) (pop 1)
; R04: new current-generation reservation after durable terminal is possible.
(push 1) (assert reservedA) (assert terminalA) (assert reservedB)
  (assert (= expectedB (+ g 1))) (check-sat) (pop 1)
; R05: one fresh reservation is possible, not vacuously blocked.
(push 1) (assert reservedA) (assert (not reservedB)) (check-sat) (pop 1)
; S2: same operator + same dispatch at current generation may resume, once.
(declare-const originalClaim Bool)
(declare-const sameDispatch Bool)
(declare-const sameOperator Bool)
(declare-const currentGeneration Bool)
(declare-const originalTerminal Bool)
(declare-const resume Bool)
(declare-const secondStartRecord Bool)
(assert (=> resume (and originalClaim sameDispatch sameOperator currentGeneration
                         (not originalTerminal) (not secondStartRecord))))
(declare-const successorAuthorized Bool)
(declare-const successorClaimAccepted Bool)
; R8: a successor is a NEW accepted Claim, not an idempotent re-claim.
; It can follow a durable terminal only when original claim and successor authority are explicit.
(assert (=> secondStartRecord
  (and originalClaim originalTerminal (not sameDispatch) currentGeneration
       successorAuthorized successorClaimAccepted)))
; I01: resume must not create a second Start Record.
(push 1) (assert resume) (assert secondStartRecord) (check-sat) (pop 1)
; I02: stale generation cannot authorize idempotent resume.
(push 1) (assert resume) (assert (not currentGeneration)) (check-sat) (pop 1)
; I03: different operator cannot borrow another operator's claim.
(push 1) (assert resume) (assert (not sameOperator)) (check-sat) (pop 1)
; I04: legal same-operator resume with one Start Record exists.
(push 1) (assert resume) (assert (not secondStartRecord)) (check-sat) (pop 1)
; I05: post-terminal different-dispatch new Claim may start.
(push 1) (assert secondStartRecord) (check-sat) (pop 1)
; I06: no original Claim, therefore no legitimate post-terminal successor.
(push 1) (assert secondStartRecord) (assert (not originalClaim)) (check-sat) (pop 1)
; I07: terminal does not grant authority to a successor by itself.
(push 1) (assert secondStartRecord) (assert (not successorAuthorized)) (check-sat) (pop 1)
; I08: an unaccepted proposed successor is never a canonical Start Record.
(push 1) (assert secondStartRecord) (assert (not successorClaimAccepted)) (check-sat) (pop 1)
; S3: compatible parallel Claims of this same work/role require verified grants.
; Scope: two distinct non-default compatibility groups, not arbitrary independent Tasks.
(declare-const parallelSameWorkRole Bool)
(declare-const distinctGroups Bool)
(declare-const nonDefaultA Bool)
(declare-const nonDefaultB Bool)
(declare-const grantRefA Bool)
(declare-const grantRefB Bool)
(declare-const grantCurrentA Bool)
(declare-const grantCurrentB Bool)
(declare-const grantFamilyA Bool)
(declare-const grantFamilyB Bool)
(declare-const grantScopeA Bool)
(declare-const grantScopeB Bool)
(assert (=> parallelSameWorkRole
  (and distinctGroups nonDefaultA nonDefaultB grantRefA grantRefB
       grantCurrentA grantCurrentB grantFamilyA grantFamilyB
       grantScopeA grantScopeB)))
; G01: presence of a group string without durable grant is insufficient.
(push 1) (assert parallelSameWorkRole) (assert (not grantRefA)) (check-sat) (pop 1)
; G02: stale grant or wrong authority family must block.
(push 1) (assert parallelSameWorkRole) (assert (not grantCurrentA)) (check-sat) (pop 1)
(push 1) (assert parallelSameWorkRole) (assert (not grantFamilyB)) (check-sat) (pop 1)
; G03: authorization for a different scope cannot authorize this parallelism.
(push 1) (assert parallelSameWorkRole) (assert (not grantScopeB)) (check-sat) (pop 1)
; G04: complete explicit current grants admit the nonvacuous parallel witness.
(push 1) (assert parallelSameWorkRole) (check-sat) (pop 1)
