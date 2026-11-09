; ADS v4.19 R0: abstract prerequisite implications, NOT actual historical gate receipts.
(set-logic QF_UF)
(declare-const productFrozen Bool)
(declare-const l2Frozen Bool)
(declare-const dagFrozen Bool)
(declare-const acceptedClaim Bool)
(declare-const sourceVerified Bool)
(declare-const ciPassed Bool)
(declare-const reviewPassed Bool)
(declare-const outcomeClosed Bool)
(declare-const releaseQualified Bool)
(declare-const released Bool)
(assert (=> l2Frozen productFrozen))
(assert (=> dagFrozen l2Frozen))
(assert (=> acceptedClaim dagFrozen))
(assert (=> sourceVerified acceptedClaim))
(assert (=> ciPassed sourceVerified))
(assert (=> reviewPassed sourceVerified))
(assert (=> outcomeClosed (and ciPassed reviewPassed)))
(assert (=> releaseQualified outcomeClosed))
(assert (=> released releaseQualified))
; G01: release before Product Freeze forbidden: UNSAT
(push 1) (assert released) (assert (not productFrozen)) (check-sat) (pop 1)
; G02: release without CI forbidden: UNSAT
(push 1) (assert released) (assert (not ciPassed)) (check-sat) (pop 1)
; G03: release without review forbidden: UNSAT
(push 1) (assert released) (assert (not reviewPassed)) (check-sat) (pop 1)
; G04: accepted claim before DAG Freeze forbidden: UNSAT
(push 1) (assert acceptedClaim) (assert (not dagFrozen)) (check-sat) (pop 1)
; G05: fully satisfied path exists: SAT
(push 1) (assert released) (check-sat) (pop 1)
