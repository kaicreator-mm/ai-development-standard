#!/usr/bin/env python3
"""Finite source-contract oracle, NOT actual source admission/fence/runtime proof."""
from copy import deepcopy
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / 'docs/implementation/4.15.0/BOUNDED_SOURCE_REPAIR_CASES.json').read_text(encoding='utf8'))


def premises():
    # Explicit fixture premises; caller cannot treat these as observed native facts.
    return dict(adopted=True, prior_owner_amendment=True, exact_artifact=True,
        actual_disjoint_effects=True, all_consumers_verified=True,
        material_obligations_resolved=True, complete_reads=True, plan_current=True,
        permission=True, dependencies=True, minimal_defect_delta=True,
        input_inspected=True, review_policy_bound=True, fresh_task_distinct_obligation=True,
        old_ref_write=False, old_grant_reassigned=False, old_generation_changed=False,
        old_resource_release=False, old_integration_consumer=False, old_pending_request=False,
        material_overlap=False, external_effect_unknown=False, renamed_replacement=False,
        general_rebuild=False, artifact_ref='sha:fixture-old-source', finding_ref='finding:fixture',
        owner_ref='prior-owner-amendment:fixture', allowed=('adoption.md',),
        required_resources=('test-capacity',), allocated_resources=('test-capacity',))


def eligible(p):
    positive = ('adopted', 'prior_owner_amendment', 'exact_artifact', 'actual_disjoint_effects',
        'all_consumers_verified', 'material_obligations_resolved', 'complete_reads',
        'plan_current', 'permission', 'dependencies', 'minimal_defect_delta',
        'input_inspected', 'review_policy_bound', 'fresh_task_distinct_obligation')
    negative = ('old_ref_write', 'old_grant_reassigned', 'old_generation_changed',
        'old_resource_release', 'old_integration_consumer', 'old_pending_request',
        'material_overlap', 'external_effect_unknown', 'renamed_replacement', 'general_rebuild')
    return (all(p.get(k) is True for k in positive) and
            all(p.get(k) is False for k in negative) and
            all(p.get(k) for k in ('artifact_ref','finding_ref','owner_ref','allowed')) and
            set(p['required_resources']) == set(p['allocated_resources']))


class Repair:
    def __init__(self):
        self.old = {'key':'original-builder', 'generation':None, 'binding':'UNKNOWN',
                    'resources':'UNKNOWN', 'terminal':None, 'status':'UNKNOWN/HOLD'}
        self.generation = 0
        self.claim = None
        self.writes = []
        self.integration = None
        self.delivery = None
        self.original_delivery = None
        self.original_done = 0

    def admit(self, p):
        if self.claim is not None or self.generation != 0 or not eligible(p):
            return 'BLOCKED'
        self.claim = deepcopy(p)
        self.generation = 1
        return 'CLAIMED'

    def write(self, p, path):
        if (not self.claim or p != self.claim or not eligible(p) or
                path not in self.claim['allowed']):
            return 'BLOCKED'
        self.writes.append(path)
        return 'AUTHORED'

    def ratify(self, p, actual):
        if (not self.writes or p != self.claim or not eligible(p) or
                actual != {'head':'new-source', 'base':'current-target', 'tree':'tested-tree',
                           'expected_head_guard':True, 'target_reread':True, 'compensation':True,
                           'known_outcome':True, 'qualified_new_operation':True,
                           'full_candidate_validation':True, 'review_current':True}):
            return 'UNRATIFIED'
        self.integration = deepcopy(actual)
        return 'RATIFIED'

    def finish_repair(self, p):
        if not self.integration or p != self.claim or not eligible(p):
            return 'BLOCKED'
        self.delivery = 'repair-final-receipt'
        return self.delivery

    def finish_original(self, *, prior_amendment, fresh_current, original_gates):
        if self.original_delivery:
            return self.original_delivery
        if (not self.delivery or prior_amendment is not True or fresh_current is not True or
                original_gates is not True):
            return 'BLOCKED'
        self.original_delivery = 'original-final-receipt'
        self.original_done += 1
        return self.original_delivery


class BoundedSourceRepair(unittest.TestCase):
    def test_fixed_independent_premise_matrix_rejects_whole_snapshot(self):
        # Cases are committed independently of eligible(), not generated from its implementation.
        for field in CASES['reject_false_or_unknown']:
            for value in (False,None):
                p=premises();p[field]=value;r=Repair();before=deepcopy(vars(r))
                with self.subTest(field=field,value=value):
                    self.assertEqual(r.admit(p),'BLOCKED');self.assertEqual(vars(r),before)
        for field in CASES['reject_true_or_unknown']:
            for value in (True,None):
                p=premises();p[field]=value;r=Repair();before=deepcopy(vars(r))
                with self.subTest(field=field,value=value):
                    self.assertEqual(r.admit(p),'BLOCKED');self.assertEqual(vars(r),before)

    def test_fresh_known_generation_not_epoch_or_existing_key(self):
        for generation in (None,1,2):
            r=Repair();r.generation=generation;before=deepcopy(vars(r))
            self.assertEqual(r.admit(premises()),'BLOCKED');self.assertEqual(vars(r),before)
        r=Repair();self.assertEqual(r.admit(premises()),'CLAIMED')
        before=deepcopy(vars(r));self.assertEqual(r.admit(premises()),'BLOCKED');self.assertEqual(vars(r),before)

    def test_refs_and_composite_resources_required_before_any_source_write(self):
        for field,value in [('artifact_ref',''),('finding_ref',''),('owner_ref',''),
                            ('allocated_resources',()),('allocated_resources',('extra',))]:
            p=premises();p[field]=value;r=Repair();before=deepcopy(vars(r))
            self.assertEqual(r.admit(p),'BLOCKED');self.assertEqual(vars(r),before)

    def test_write_requires_admission_and_exact_current_minimal_allowed_delta(self):
        r=Repair();p=premises();before=deepcopy(vars(r))
        self.assertEqual(r.write(p,'adoption.md'),'BLOCKED');self.assertEqual(vars(r),before)
        r.admit(p);before=deepcopy(vars(r))
        for path,changed in [('old-ref.md',p),('feature.md',p),
                             ('adoption.md',{**p,'plan_current':False})]:
            self.assertEqual(r.write(changed,path),'BLOCKED');self.assertEqual(vars(r),before)

    def test_ordered_success_preserves_old_unknown_and_original_delivery_once(self):
        r=Repair();old=deepcopy(r.old);p=premises()
        self.assertEqual(r.admit(p),'CLAIMED');self.assertEqual(r.generation,1)
        self.assertEqual(r.write(p,'adoption.md'),'AUTHORED')
        self.assertEqual(r.finish_repair(p),'BLOCKED');self.assertEqual(r.original_done,0)
        actual=dict(head='new-source',base='current-target',tree='tested-tree',expected_head_guard=True,
                    target_reread=True,compensation=True,known_outcome=True,qualified_new_operation=True,
                    full_candidate_validation=True,review_current=True)
        self.assertEqual(r.ratify(p,actual),'RATIFIED');self.assertEqual(r.original_done,0)
        self.assertEqual(r.finish_repair(p),'repair-final-receipt');self.assertEqual(r.original_done,0)
        for args in [(False,True,True),(True,None,True),(True,True,False)]:
            self.assertEqual(r.finish_original(prior_amendment=args[0],fresh_current=args[1],original_gates=args[2]),'BLOCKED')
        for _ in range(2):self.assertEqual(r.finish_original(prior_amendment=True,fresh_current=True,original_gates=True),'original-final-receipt')
        self.assertEqual(r.original_done,1);self.assertEqual(r.old,old)

    def test_unknown_actual_effect_or_late_old_result_never_ratifies(self):
        for field,value in [('head','old-source'),('base','drifted-target'),('tree','other-tree'),
                            ('known_outcome',False),('compensation',False),
                            ('qualified_new_operation',False),('expected_head_guard',False),
                            ('full_candidate_validation',False),('review_current',False)]:
            r=Repair();p=premises();r.admit(p);r.write(p,'adoption.md');before=deepcopy(vars(r))
            actual=dict(head='new-source',base='current-target',tree='tested-tree',expected_head_guard=True,
                        target_reread=True,compensation=True,known_outcome=True,qualified_new_operation=True,
                        full_candidate_validation=True,review_current=True)
            actual[field]=value
            self.assertEqual(r.ratify(p,actual),'UNRATIFIED');self.assertEqual(vars(r),before)
            self.assertEqual(r.finish_repair(p),'BLOCKED')

    def test_normative_owner_and_old_route_remain_separate(self):
        exe=(ROOT/'standards/EXECUTION_ARCHITECTURE_STANDARD.md').read_text(encoding='utf8')
        release=(ROOT/'standards/RELEASE_STANDARD.md').read_text(encoding='utf8')
        for text in ('### 23.5 Distinct immutable-artifact source acceptance',
                     '### 23.6 Bounded new source-defect repair',
                     'Unknown historical generation alone', 'ordinary designated single writer'):
            self.assertIn(text,exe)
        for text in ('#### Bounded new source-defect authoring',
                     'the immutable\nacceptance procedure below stays read-only',
                     'prior explicit\nowner delivery amendment'):
            self.assertIn(text,release)
        # Original independently frozen A01-A17/model must still reject repair writes.
        from test_v415_artifact_acceptance import Facts
        self.assertFalse(Facts(repair_write=True).eligible())


if __name__ == '__main__':
    unittest.main()
