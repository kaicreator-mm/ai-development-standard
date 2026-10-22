"""Finite ADS-owned S03 conformance, never real Tally/GitHub/runtime qualification."""
import copy
import json
from itertools import permutations
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from v415_consumer_oracle import (collection_complete, correction_status,
    downstream_witness, feedback_observation, observe, wire)
sys.path.insert(0, str(HERE.parent / 'scripts'))
from test_github_structured_interaction import REPORT, WORK


def record(name='summary'):
    return json.loads((HERE / 'fixtures/v415' / (name + '.json')).read_text(encoding='utf8'))


def item(r=None, number=123):
    r = record() if r is None else copy.deepcopy(r)
    issue = r['data']['subject']['issue_ref']
    return {'record': r, 'id': number, 'url': issue + '#issuecomment-' + str(number),
            'issue': issue, 'source_witness': True, 'edit_evidence': 'CLEAR'}


def read(items, complete=True):
    s = record()['data']['subject']
    return observe(items, complete=complete, issue=s['issue_ref'],
                   source_sha=s['source_sha'], ads_sha=s['ads_revision'])


def aligned_notice():
    notice, target = record('correction'), record()
    notice['data']['target']['data_digest'] = wire.data_digest(target)
    return notice, target


def apply_notice(notice=None, target=None, **changes):
    n, t = aligned_notice()
    args = dict(native_target_url=n['data']['target']['comment_ref'],
                native_issue=t['data']['subject']['issue_ref'], authority_witness=True)
    args.update(changes)
    return correction_status(n if notice is None else notice,
                             t if target is None else target, **args)


class CollectionBoundary(unittest.TestCase):
    def test_actual_terminal_page_required(self):
        self.assertTrue(collection_complete([{'cursor':None,'status':200,'items':[],'next':None}]))
        self.assertFalse(collection_complete([]))
        self.assertFalse(collection_complete([{'cursor':None,'status':200,'items':[],'next':'c2'}]))

    def test_two_pages_and_out_of_order_cursor(self):
        pages = [{'cursor':None,'status':200,'items':[1],'next':'c2'},
                 {'cursor':'c2','status':200,'items':[2],'next':None}]
        self.assertTrue(collection_complete(pages))
        pages[1]['cursor']='wrong'
        self.assertFalse(collection_complete(pages))

    def test_cycle_page_cap_and_malformed_are_not_absence(self):
        for pages, cap in [([{'cursor':None,'status':200,'items':[],'next':'x'},
                            {'cursor':'x','status':200,'items':[],'next':'x'}],20),
                           ([{'cursor':None,'status':200,'items':[],'next':None}],0),
                           ([{'cursor':None,'status':200,'items':{},'next':None}],20)]:
            with self.subTest(pages=pages):self.assertFalse(collection_complete(pages,max_pages=cap))

    def test_rate_limit_wait_and_same_cursor_retry(self):
        done = {'cursor':None,'status':200,'items':[],'next':None}
        for status in (429,403):
            retry = {'cursor':None,'status':status,'rate_limited':True,
                     'within_budget':True,'wait_respected':True}
            self.assertTrue(collection_complete([retry,done]))
            retry['wait_respected']=False
            self.assertFalse(collection_complete([retry,done]))

    def test_timeout_budget_permission_and_exhaustion(self):
        done = {'cursor':None,'status':200,'items':[],'next':None}
        retry = {'cursor':None,'status':'TIMEOUT','within_budget':True}
        self.assertTrue(collection_complete([retry,done]))
        self.assertFalse(collection_complete([retry,retry,retry,done]))
        retry['within_budget']=False
        self.assertFalse(collection_complete([retry,done]))
        for status in (401,403,404,500):
            self.assertFalse(collection_complete([{'cursor':None,'status':status},done]))


class ReconciliationBoundary(unittest.TestCase):
    def test_positive_observation_and_incomplete_unknown(self):
        self.assertEqual(read([item()]),['OBSERVED'])
        self.assertEqual(read([item()],False),['UNKNOWN'])

    def test_duplicate_is_not_another_attempt(self):
        self.assertEqual(read([item(),item(number=124)]),['OBSERVED','DUPLICATE'])

    def test_same_digest_primary_requires_observed_witness_in_both_orders(self):
        for changes,state in [({'source_witness':False},'UNKNOWN'),
                              ({'edit_evidence':'UNKNOWN'},'UNKNOWN'),
                              ({'edit_evidence':'EDITED'},'UNVERIFIED')]:
            uncertain,valid=item(),item(number=124)
            uncertain.update(changes)
            self.assertEqual(read([uncertain,valid]),[state,'OBSERVED'])
            self.assertEqual(read([valid,uncertain]),['OBSERVED',state])

    def test_same_digest_multiple_qualified_witnesses_keep_one_actual_primary(self):
        uncertain,one,two=item(),item(number=124),item(number=125)
        uncertain['source_witness']=False
        for ordering in permutations([uncertain,one,two]):
            statuses=read(ordering)
            qualified=[status for x,status in zip(ordering,statuses) if x['source_witness']]
            self.assertEqual(qualified,['OBSERVED','DUPLICATE'])
            self.assertEqual(statuses[list(ordering).index(uncertain)],'UNKNOWN')
        one['source_witness']=two['source_witness']=False
        self.assertEqual(read([uncertain,one,two]),['UNKNOWN']*3)

    def test_conflict_never_uses_input_order_or_newest(self):
        a,b=item(),item(number=124)
        b['record']['data']['limits'].append('Conflicting additional observation')
        for pair in ([a,b],[b,a]):self.assertEqual(read(pair),['CONFLICT','CONFLICT'])

    def test_native_edit_prior_digest_and_unavailable_history(self):
        for key,value,result in [('edit_evidence','EDITED','UNVERIFIED'),
                                 ('edit_evidence','UNKNOWN','UNKNOWN'),
                                 ('previous_digest','0'*64,'CONFLICT')]:
            x=item();x[key]=value
            self.assertEqual(read([x]),[result])

    def test_same_native_comment_changed_identity_still_conflicts(self):
        a,b=item(),item();b['record']['data']['report_id']='different-id'
        self.assertEqual(read([a,b]),['CONFLICT','CONFLICT'])

    def test_collision_precedes_unavailable_source_promotion_in_every_order(self):
        for field in ('source_witness', 'source_sha', 'ads_revision', 'currentness'):
            a,b=item(),item(number=124)
            b['record']['data']['limits'].append('Different bounded observation')
            if field == 'source_witness':
                b[field]=False
            elif field == 'currentness':
                b['record']['data']['subject'][field]['state']='UNKNOWN'
            else:
                b['record']['data']['subject'][field]='c'*40
                if field == 'source_sha':
                    b['record']['data']['verifier']['subject_sha']='c'*40
            self.assertEqual(read([b]),['UNKNOWN'])
            for pair in permutations([a,b]):
                with self.subTest(field=field,ids=[x['id'] for x in pair]):
                    self.assertEqual(read(pair),['CONFLICT','CONFLICT'])

    def test_native_comment_collision_with_unknown_and_edited_observations(self):
        a,b=item(),item()
        b['record']['data']['report_id']='changed-id'
        b['source_witness']=False
        for pair in permutations([a,b]):self.assertEqual(read(pair),['CONFLICT','CONFLICT'])
        b['edit_evidence']='EDITED'
        for pair in permutations([a,b]):self.assertEqual(read(pair),['CONFLICT','CONFLICT'])

    def test_all_unknown_collision_is_not_hidden_or_promoted(self):
        a,b=item(),item(number=124)
        a['source_witness']=b['source_witness']=False
        self.assertEqual(read([a,b]),['UNKNOWN','UNKNOWN'])
        b['record']['data']['limits'].append('different')
        for pair in permutations([a,b]):self.assertEqual(read(pair),['CONFLICT','CONFLICT'])

    def test_invalid_or_foreign_native_input_cannot_poison_owning_identity(self):
        for field in ('schema','issue','url'):
            a,b=item(),item(number=124)
            b['record']['data']['limits'].append('different')
            if field=='schema':b['record']['schema']='ads/github/v99'
            else:b[field]='https://github.com/other/repo/issues/42'
            expected='INVALID_SCHEMA' if field=='schema' else 'UNVERIFIED'
            self.assertEqual(read([a,b]),['OBSERVED',expected])
            self.assertEqual(read([b,a]),[expected,'OBSERVED'])

    def test_body_current_assertion_cannot_prove_source(self):
        x=item();x['source_witness']=False
        self.assertEqual(read([x]),['UNKNOWN'])
        for key in ('source_sha','ads_revision'):
            x=item();x['record']['data']['subject'][key]='c'*40
            if key=='source_sha':x['record']['data']['verifier']['subject_sha']='c'*40
            self.assertEqual(read([x]),['UNKNOWN'])

    def test_wrong_native_issue_and_comment_prefix(self):
        for key,value in [('issue','https://github.com/example-org/example-repo/issues/43'),
                          ('url','https://github.com/other/repo/issues/42#issuecomment-123')]:
            x=item();x[key]=value
            self.assertEqual(read([x]),['UNVERIFIED'])

    def test_v3_report_is_historical_current_work_is_not_report(self):
        x=item();x['record']={'schema':'ads/github/v3','kind':'report','data':copy.deepcopy(REPORT)}
        self.assertEqual(read([x]),['HISTORICAL_READ_ONLY'])
        x['record']={'schema':'ads/github/v3','kind':'work_item','data':copy.deepcopy(WORK)}
        self.assertEqual(read([x]),['NOT_REPORT'])

    def test_unknown_schema_is_rejected_before_data_use(self):
        x=item();x['record']['schema']='ads/github/v99'
        self.assertEqual(read([x]),['INVALID_SCHEMA'])

    def test_actual_predecessor_missing_wrong_and_order_independent(self):
        a=item(record('feedback'));b=item(record('feedback'),124)
        d=b['record']['data'];d['revision']=2
        d['supersedes']={'revision':1,'comment_ref':a['url'],
                         'data_digest':wire.data_digest(a['record'])}
        for pair in ([a,b],[b,a]):self.assertEqual(read(pair),['OBSERVED','OBSERVED'])
        self.assertEqual(read([b]),['UNKNOWN'])
        d['supersedes']['data_digest']='0'*64
        self.assertEqual(read([a,b]),['OBSERVED','UNVERIFIED'])

    def test_unknown_predecessor_propagates_through_reverse_chain(self):
        a=item(record('feedback'));b=item(record('feedback'),124);c=item(record('feedback'),125)
        b['record']['data'].update(revision=2,supersedes={'revision':1,'comment_ref':a['url'],
            'data_digest':wire.data_digest(a['record'])})
        c['record']['data'].update(revision=3,supersedes={'revision':2,'comment_ref':b['url'],
            'data_digest':wire.data_digest(b['record'])})
        self.assertEqual(read([c,b]),['UNVERIFIED','UNKNOWN'])


class CorrectionBoundary(unittest.TestCase):
    def test_aligned_revoke_redact_and_dispute(self):
        self.assertEqual(apply_notice(),'TARGET_INVALIDATED')
        for notice,expected in [('REDACT','TARGET_INVALIDATED'),('DISPUTE','DISPUTED')]:
            n,_=aligned_notice();n['data']['notice']=notice
            self.assertEqual(apply_notice(notice=n),expected)

    def test_shape_valid_wrong_task_issue_and_comment_target_do_not_cancel(self):
        for key,value in [('task_ref','task:43'),
                          ('issue_ref','https://github.com/example-org/example-repo/issues/43'),
                          ('comment_ref','https://github.com/example-org/example-repo/issues/43#issuecomment-123')]:
            n,_=aligned_notice();n['data']['target'][key]=value
            # Actual existing S02 helper accepts shape: consumer must reject application.
            wire.validate_record(n)
            self.assertEqual(apply_notice(notice=n),'DISPUTED')

    def test_notice_subject_attempt_must_align(self):
        n,_=aligned_notice();n['data']['subject']['attempt_ref']='attempt:42:2'
        wire.validate_record(n)
        self.assertEqual(apply_notice(notice=n),'DISPUTED')

    def test_shared_transport_is_not_namespace_authority(self):
        n,t=aligned_notice()
        for r in (n,t):r['data']['actor']['transport_actor']='shared-login'
        n['data']['publisher_namespace']='tally:example-org/example-repo'
        self.assertEqual(apply_notice(notice=n,target=t),'DISPUTED')

    def test_wrong_digest_revision_and_report_kind(self):
        for key,value in [('data_digest','0'*64),('revision',2),
                          ('report_id','other'),('report_kind','EXPERIENCE_USE_FEEDBACK')]:
            n,_=aligned_notice();n['data']['target'][key]=value
            self.assertEqual(apply_notice(notice=n),'DISPUTED')

    def test_unknown_authority_or_edited_target_never_cancels(self):
        for args in ({'authority_witness':False},{'target_integrity':'UNKNOWN'},
                     {'notice_integrity':'UNVERIFIED'},
                     {'native_target_url':'https://github.com/example-org/example-repo/issues/43#issuecomment-123'}):
            expected='DISPUTED' if 'native_target_url' in args else 'UNVERIFIED'
            self.assertEqual(apply_notice(**args),expected)

    def test_notice_cannot_carry_replacement_facts(self):
        n,_=aligned_notice();n['data']['metrics']=[]
        self.assertEqual(apply_notice(notice=n),'INVALID_SCHEMA')


class FeedbackBoundary(unittest.TestCase):
    def feedback(self,r=None,**changes):
        r=record('feedback') if r is None else r;d=r['data']
        args=dict(build_sha=d['publisher_source_sha'],ads_subject_sha=d['ads_subject_sha'],
                  source_witness=True,phase_witness=True)
        args.update(changes)
        return feedback_observation(r,**args)

    def test_presented_is_only_presented(self):
        self.assertEqual(self.feedback(),'PRESENTED')
        self.assertEqual(self.feedback(phase_witness=False),'UNKNOWN')
        self.assertEqual(self.feedback(source_witness=False),'UNKNOWN')

    def test_actual_publisher_and_ads_candidate_sha_are_distinct(self):
        self.assertEqual(self.feedback(build_sha='e'*40),'UNKNOWN')
        self.assertEqual(self.feedback(ads_subject_sha='e'*40),'UNKNOWN')

    def test_phases_do_not_promote_and_independence_requires_witness(self):
        for phase in ('ACCEPTED','APPLIED','SKIPPED','OBSERVED_EFFECT'):
            r=record('feedback');r['data']['phase']=phase
            self.assertEqual(self.feedback(r),phase)
        r=record('feedback');r['data']['phase']='INDEPENDENTLY_CHECKED'
        r['data']['verifier_refs']=['github:independent-observation']
        self.assertEqual(self.feedback(r),'UNKNOWN')
        self.assertEqual(self.feedback(r,independent_witness=True),'INDEPENDENTLY_CHECKED')

    def test_manifest_free_and_no_self_generated_receipt(self):
        for field in ('manifest_ref','manifest_sha256','comment_id','comment_ref','data_digest'):
            r=record('feedback');r['data'][field]='invented'
            self.assertEqual(self.feedback(r),'INVALID_SCHEMA')

    def test_same_build_grant_and_egress_coverage_are_independent(self):
        args=dict(reader_build='a'*40,publisher_build='a'*40,actual_grants=True,
                  effective_egress=True,real_readback=True)
        self.assertEqual(downstream_witness(**args),'BOUNDED_WITNESS')
        for key in ('actual_grants','effective_egress','real_readback'):
            for unknown in (None,False,'UNKNOWN'):
                changed={**args,key:unknown}
                self.assertEqual(downstream_witness(**changed),'UNKNOWN')
        self.assertEqual(downstream_witness(**{**args,'publisher_build':'b'*40}),'UNKNOWN')


if __name__ == '__main__':
    unittest.main()
