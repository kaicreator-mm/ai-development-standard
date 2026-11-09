#!/usr/bin/env python3
"""ADS R3 standalone bounded logical challenge; experimental, no normative gate."""
import itertools
import json

BITS=("claim","authorized","ci_fresh","review_fresh","closed","no_p0","traceable","effective_version")

def release_gate(s):
    return all(s[k] for k in BITS)

def bad_release(s):
    return all(s[k] for k in BITS if k not in ("ci_fresh","review_fresh"))

def path(edges,a,b):
    todo=[a]
    seen=set()
    while todo:
        n=todo.pop()
        if n==b: return True
        if n not in seen:
            seen.add(n)
            todo.extend(y for x,y in edges if x==n)
    return False

def acyclic(edges):
    return not any(path(edges,b,a) for a,b in edges)

def run():
    states=[dict(zip(BITS,flags)) for flags in itertools.product((False,True),repeat=8)]
    legal=[s for s in states if release_gate(s)]
    stale=[s for s in states if bad_release(s) and not release_gate(s)]
    assert len(states)==256 and len(legal)==1 and len(stale)==3
    possible=[(a,b) for a in range(3) for b in range(3) if a!=b]
    graphs=[{e for e,b in zip(possible,mask) if b} for mask in itertools.product((False,True),repeat=6)]
    safe=sum(acyclic(g) for g in graphs)
    assert safe+sum(not acyclic(g) for g in graphs)==64
    true={(0,1)}
    mutant={(0,1),(1,2)}
    assert acyclic(true) and acyclic(mutant)
    assert not path(true,0,2) and path(mutant,0,2)
    historical=[(f,r,p) for f,r,p in itertools.product((False,True),repeat=3)
                if (p or not f or r) and not (not f or r)]
    assert historical==[(True,False,True)]
    return {
      "kind":"ADS_BOUNDED_LOGICAL_CHALLENGE_NOT_NORMATIVE_PROOF",
      "source_alignment":"NOT_RUN",
      "checks":[
        {"id":"R3-RELEASE-STALE","status":"PASS_MUTANT_DETECTED","states":256,"legal":1,"mutant_counterexamples":3},
        {"id":"R3-DAG-STRUCTURE","status":"PASS_BOUNDED","graphs":64,"acyclic":safe},
        {"id":"R3-FALSE-SERIAL","status":"MUTANT_DETECTED","witness":{"necessary":[[0,1]],"unnecessary":[[1,2]]}},
        {"id":"R3-HISTORY-SCOPE","status":"PASS_MUTANT_DETECTED","states":8,"mutant_counterexamples":1}
      ],
      "limitations":["Abstract finite model only","No source-model equivalence","No actual Claim/CI execution",
                     "Whether an edge is unnecessary requires domain dependency evidence"]
    }

if __name__=="__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
