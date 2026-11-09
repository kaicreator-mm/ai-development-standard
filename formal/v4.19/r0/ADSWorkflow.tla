----------------------------- MODULE ADSWorkflow -----------------------------
EXTENDS Naturals, FiniteSets
CONSTANTS UnsafeRelease, UnsafeClaim
ASSUME UnsafeRelease \in BOOLEAN /\ UnsafeClaim \in BOOLEAN
Writers == {"web", "local"}
VARIABLES productFrozen, l2Frozen, dagFrozen, claimedEver, activeWriters,
          sourceVerified, ciPass, reviewPass, outcomeClosed, releaseQualified, released
vars == <<productFrozen, l2Frozen, dagFrozen, claimedEver, activeWriters,
          sourceVerified, ciPass, reviewPass, outcomeClosed, releaseQualified, released>>
Init == /\ productFrozen = FALSE /\ l2Frozen = FALSE /\ dagFrozen = FALSE
        /\ claimedEver = FALSE /\ activeWriters = {}
        /\ sourceVerified = FALSE /\ ciPass = FALSE /\ reviewPass = FALSE
        /\ outcomeClosed = FALSE /\ releaseQualified = FALSE /\ released = FALSE
FreezeProduct == /\ ~productFrozen /\ ~released /\ productFrozen' = TRUE
                 /\ UNCHANGED <<l2Frozen, dagFrozen, claimedEver, activeWriters,
                                sourceVerified, ciPass, reviewPass, outcomeClosed, releaseQualified, released>>
FreezeL2 == /\ productFrozen /\ ~l2Frozen /\ ~released /\ l2Frozen' = TRUE
             /\ UNCHANGED <<productFrozen, dagFrozen, claimedEver, activeWriters,
                            sourceVerified, ciPass, reviewPass, outcomeClosed, releaseQualified, released>>
FreezeDAG == /\ l2Frozen /\ ~dagFrozen /\ ~released /\ dagFrozen' = TRUE
              /\ UNCHANGED <<productFrozen, l2Frozen, claimedEver, activeWriters,
                             sourceVerified, ciPass, reviewPass, outcomeClosed, releaseQualified, released>>
Claim(w) == /\ dagFrozen /\ ~released /\ w \in Writers
            /\ (UnsafeClaim \/ activeWriters = {})
            /\ activeWriters' = activeWriters \cup {w}
            /\ claimedEver' = TRUE
            /\ UNCHANGED <<productFrozen, l2Frozen, dagFrozen, sourceVerified,
                           ciPass, reviewPass, outcomeClosed, releaseQualified, released>>
Deliver(w) == /\ w \in activeWriters /\ ~sourceVerified /\ ~released
              /\ sourceVerified' = TRUE
              /\ UNCHANGED <<productFrozen, l2Frozen, dagFrozen, claimedEver, activeWriters,
                             ciPass, reviewPass, outcomeClosed, releaseQualified, released>>
FinishWriter(w) == /\ w \in activeWriters /\ sourceVerified /\ ~released
                   /\ activeWriters' = activeWriters \ {w}
                   /\ UNCHANGED <<productFrozen, l2Frozen, dagFrozen, claimedEver,
                                  sourceVerified, ciPass, reviewPass, outcomeClosed, releaseQualified, released>>
VerifyCI == /\ sourceVerified /\ ~ciPass /\ ~released /\ ciPass' = TRUE
            /\ UNCHANGED <<productFrozen, l2Frozen, dagFrozen, claimedEver, activeWriters,
                           sourceVerified, reviewPass, outcomeClosed, releaseQualified, released>>
Review == /\ sourceVerified /\ ~reviewPass /\ ~released /\ reviewPass' = TRUE
          /\ UNCHANGED <<productFrozen, l2Frozen, dagFrozen, claimedEver, activeWriters,
                         sourceVerified, ciPass, outcomeClosed, releaseQualified, released>>
CloseOutcome == /\ ciPass /\ reviewPass /\ ~outcomeClosed /\ ~released
                /\ outcomeClosed' = TRUE
                /\ UNCHANGED <<productFrozen, l2Frozen, dagFrozen, claimedEver, activeWriters,
                               sourceVerified, ciPass, reviewPass, releaseQualified, released>>
QualifyRelease == /\ outcomeClosed /\ ~releaseQualified /\ ~released
                  /\ releaseQualified' = TRUE
                  /\ UNCHANGED <<productFrozen, l2Frozen, dagFrozen, claimedEver, activeWriters,
                                 sourceVerified, ciPass, reviewPass, outcomeClosed, released>>
Release == /\ (UnsafeRelease \/ releaseQualified) /\ ~released /\ released' = TRUE
           /\ UNCHANGED <<productFrozen, l2Frozen, dagFrozen, claimedEver, activeWriters,
                          sourceVerified, ciPass, reviewPass, outcomeClosed, releaseQualified>>
Next == FreezeProduct \/ FreezeL2 \/ FreezeDAG
        \/ (\E w \in Writers: Claim(w)) \/ (\E w \in Writers: Deliver(w))
        \/ (\E w \in Writers: FinishWriter(w))
        \/ VerifyCI \/ Review \/ CloseOutcome \/ QualifyRelease \/ Release
Spec == Init /\ [][Next]_vars
TypeOK == /\ productFrozen \in BOOLEAN /\ l2Frozen \in BOOLEAN /\ dagFrozen \in BOOLEAN
          /\ claimedEver \in BOOLEAN /\ activeWriters \subseteq Writers
          /\ sourceVerified \in BOOLEAN /\ ciPass \in BOOLEAN /\ reviewPass \in BOOLEAN
          /\ outcomeClosed \in BOOLEAN /\ releaseQualified \in BOOLEAN /\ released \in BOOLEAN
LifecycleSafe == /\ (l2Frozen => productFrozen)
                 /\ (dagFrozen => l2Frozen)
                 /\ (sourceVerified => (claimedEver /\ dagFrozen))
                 /\ (ciPass => sourceVerified)
                 /\ (reviewPass => sourceVerified)
                 /\ (outcomeClosed => (ciPass /\ reviewPass))
                 /\ (releaseQualified => outcomeClosed)
                 /\ (released => (releaseQualified /\ productFrozen /\ l2Frozen
                                  /\ dagFrozen /\ ciPass /\ reviewPass /\ outcomeClosed))
SingleWriter == Cardinality(activeWriters) <= 1
=============================================================================
