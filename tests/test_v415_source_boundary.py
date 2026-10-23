"""#1232 P2-01 finite source counterexamples, NOT a native controller proof.

Expected decisions are anchored to the adopted RELEASE11.7A/EXE14/23/29.1
owners below. Premises are supplied fixtures, never recovered S01/S04 facts.
"""
from copy import deepcopy
from dataclasses import replace
import hashlib
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from test_v415_github_recovery import Facts, RecoveryApplicationHarness
from test_v415_artifact_acceptance import Acceptance, Facts as ArtifactFacts, outcome

# These are finite fixture classifications, not new workflow/Gate states.
RUNTIME_EFFECTS={'deployment','production-operation','scarce-resource',
                 'external-resource','automated-protected-effect'}
def source_route(*, actual_effects, complete_effect_read, label, adoption):
    del label, adoption  # Labels cannot stand in for actual effects/currentness.
    if complete_effect_read is not True or actual_effects is None:
        return 'HOLD'
    if any(effect not in {'source-edit','source-validation'} for effect in actual_effects):
        return 'RUNTIME_REQUIREMENTS_RETAINED'
    return 'SOURCE_ROUTE_WITH_REQUIRED_SOURCE_GATES'


class AdoptedSourceBoundary(unittest.TestCase):
    def test_expected_scenarios_bind_exact_adopted_owner_blobs(self):
        owners={'standards/EXECUTION_ARCHITECTURE_STANDARD.md':'1f1601a20db08d263955241607dfd08d8b8f77e1',
                'standards/RELEASE_STANDARD.md':'da3b78b113be238bdce650ccb646f5aa23bc1f9b'}
        for name,expected in owners.items():
            raw=(ROOT/name).read_bytes()
            self.assertEqual(hashlib.sha1(('blob '+str(len(raw))+'\0').encode()+raw).hexdigest(),expected)
        # Blob pins anchor the expected cases; presence assertions alone would
        # not exercise any decision or accepted state/effect below.

    def test_docs_a0_labels_do_not_mask_actual_runtime_effects(self):
        for effect in sorted(RUNTIME_EFFECTS):
            for label,adoption in [('docs-only','A0'),('code','A2')]:
                with self.subTest(effect=effect,label=label,adoption=adoption):
                    self.assertEqual(source_route(actual_effects=['source-edit',effect],
                        complete_effect_read=True,label=label,adoption=adoption),
                        'RUNTIME_REQUIREMENTS_RETAINED')
        self.assertEqual(source_route(actual_effects=['source-edit','source-validation'],
            complete_effect_read=True,label='docs-only',adoption='A0'),
            'SOURCE_ROUTE_WITH_REQUIRED_SOURCE_GATES')
        for effects,complete in [(None,True),([],None),(['unclassified-effect'],False)]:
            self.assertEqual(source_route(actual_effects=effects,complete_effect_read=complete,
                label='docs-only',adoption='A0'),'HOLD')
        self.assertEqual(source_route(actual_effects=['unclassified-effect'],complete_effect_read=True,
            label='docs-only',adoption='A0'),'RUNTIME_REQUIREMENTS_RETAINED')

    def test_stale_and_duplicate_claim_cannot_write_again(self):
        h=RecoveryApplicationHarness();proposal=h.proposal
        before=h.snapshot()
        self.assertEqual(h.apply(Facts(),proposal=replace(proposal,head_sha='f'*40)),'INELIGIBLE')
        self.assertEqual(h.snapshot(),before)
        self.assertEqual(h.apply(Facts()),'ACCEPTED')
        accepted=h.snapshot()
        self.assertEqual(h.apply(Facts()),'STALE')
        self.assertEqual(h.snapshot(),accepted)
        self.assertEqual(len(h.source_effects),1)

    def test_unreconciled_or_unknown_claim_never_consumes_a_fresh_binding(self):
        cases=[Facts(generation=None),Facts(old_outcome='UNCERTAIN'),
               Facts(old_outcome='ACCEPTED',old_active=True),Facts(current=None)]
        for facts in cases:
            h=RecoveryApplicationHarness(active='old' if facts.old_active else 'none')
            before=h.snapshot()
            self.assertEqual(h.apply(facts),'HOLD')
            self.assertEqual(h.snapshot(),before)

    def test_failed_incomplete_native_reads_and_currentness_block_before_effect(self):
        for field in ['complete_reads','plan_current','dependencies','permission']:
            for unavailable in [False,None]:
                model=Acceptance();before=model.snapshot()
                facts=replace(ArtifactFacts(),**{field:unavailable})
                self.assertEqual(model.select(facts,'selection/1'),'BLOCKED')
                self.assertEqual(model.snapshot(),before)
                self.assertEqual((model.done,model.wakes),(0,0))

    def test_unknown_merge_and_failed_compensation_preserve_incident_and_hold(self):
        for change in [{'ack':'unknown'},{'compensation':False},{'post_checks':False}]:
            model=Acceptance();facts=ArtifactFacts();old=deepcopy(model.old)
            self.assertEqual(model.select(facts,'selection/1'),'SELECTED')
            self.assertEqual(model.readback('selection/1',facts),'READ_BACK')
            self.assertEqual(model.request_integration('selection/1',facts),'REQUESTED')
            actual=outcome(**change)
            self.assertEqual(model.observe(actual,facts),'UNRATIFIED')
            self.assertEqual(model.actual,actual)  # Never rewrite actual effect as zero.
            self.assertTrue(model.incidents and model.hold)
            self.assertEqual(model.publish_ratification('selection/1','ratification/1'),'BLOCKED')
            self.assertEqual(model.consume_delivery('delivery/1'),'BLOCKED')
            self.assertEqual((model.done,model.wakes),(0,0))
            self.assertEqual(model.old,old)


if __name__=='__main__':unittest.main(verbosity=2)
