"""S05 finite ADS source integration. No HTTP, publisher, TS or authority proof."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import socket
import sys
import unittest
from unittest.mock import patch
from referencing.exceptions import NoSuchResource

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(HERE))
from test_v415_report import fixture, markdown, successor
from test_v415_consumer import (item, read, aligned_notice, apply_notice,
                               collection_complete, downstream_witness, wire)
from test_github_structured_interaction import WORK, INTENT, EVENT, REPORT, envelope


def blob(raw):
    return hashlib.sha1(('blob '+str(len(raw))+'\0').encode()+raw).hexdigest()


def historical_reader():
    # Verbatim qualified-main source; no floating git ref or network dependency.
    source=HERE/'fixtures/v415/historical_v414_reader.py'
    assert blob(source.read_bytes())=='c92cec520c315565d9d05ffbc5254ac803e346a3'
    spec=importlib.util.spec_from_file_location('qualified_v414_reader',source)
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    # Only schema location is adapted; original parser/validator bytes unchanged.
    old.ROOT=ROOT
    old.SCHEMA_FILE=wire.SCHEMA_FILE
    old.REFERENCED=wire.REFERENCED
    return old


class IntegratedWire(unittest.TestCase):
    def test_publish_read_digest_and_immutable_late_evidence_chain(self):
        first=fixture();late=successor(first,'EVIDENCE_UPDATE')
        learned=successor(late,'TASK_LEARNING')
        learned['data']['manifest_ref']='object:private/task42/attempt1/r3/manifest.json'
        learned['data']['manifest_sha256']='e'*64
        learned['data']['supersedes']['comment_ref']=first['data']['subject']['issue_ref']+'#issuecomment-124'
        original=copy.deepcopy(first)
        self.assertEqual(wire.validate_summary_revision(first,late,'EVIDENCE_UPDATE'),'SHAPE_VALID_ONLY')
        self.assertEqual(wire.validate_summary_revision(late,learned,'TASK_LEARNING'),'SHAPE_VALID_ONLY')
        native=[item(wire.parse_markdown(markdown(r)),n) for r,n in
                [(first,123),(late,124),(learned,125)]]
        self.assertEqual(read(native[::-1]),['OBSERVED']*3)
        self.assertEqual(first,original)
        self.assertEqual(len({wire.data_digest(x['record']) for x in native}),3)
        # Missing actual predecessor cannot be inferred from a new manifest ref.
        self.assertEqual(read([native[2]]),['UNKNOWN'])

    def test_retry_lost_ack_reconciles_actual_identity_not_attempt_count(self):
        wanted=item();retry=item(number=124)
        pages=[{'cursor':None,'status':429,'within_budget':True,'wait_respected':True},
               {'cursor':None,'status':200,'items':[wanted],'next':'p2'},
               {'cursor':'p2','status':200,'items':[retry],'next':None}]
        self.assertTrue(collection_complete(pages))
        self.assertEqual(read([wanted,retry]),['OBSERVED','DUPLICATE'])
        self.assertEqual(read([wanted],collection_complete(pages[:-1])),['UNKNOWN'])
        conflicting=copy.deepcopy(retry)
        conflicting['record']['data']['limits'].append('lost-ACK competing payload')
        self.assertEqual(read([wanted,conflicting]),['CONFLICT','CONFLICT'])
        # These are supplied readbacks, not actual POST retry or exactly-once proof.

    def test_second_attempt_uses_distinct_report_identity_and_leaf_aggregation(self):
        a=fixture();b=copy.deepcopy(a);d=b['data']
        d['report_id']='report:42:execution-attempt2'
        d['subject']['attempt_ref']='attempt:42:2'
        d['aggregation']['attempt_refs']=['attempt:42:2']
        d['manifest_ref']='object:private/task42/attempt2/r1/manifest.json'
        wire.validate_record(b)
        self.assertEqual(read([item(a),item(b,124)]),['OBSERVED','OBSERVED'])
        invalid=copy.deepcopy(b);invalid['data']['aggregation']['attempt_refs']*=2
        with self.assertRaises(wire.ContractError):wire.validate_record(invalid)

    def test_partial_green_checks_and_ack_remain_observations(self):
        r=fixture();v=r['data']['verifier']
        v.update(checked=['check:'+str(i) for i in range(19)],failed=['critical-journey'])
        r['data']['source_refs'].append('tool:ACK:accepted-not-terminal')
        self.assertEqual(wire.verify_markdown(markdown(r)),'SHAPE_VALID_ONLY')
        self.assertEqual(read([item(r)]),['OBSERVED'])
        self.assertEqual(wire.parse_markdown(markdown(r))['data']['verifier']['failed'],['critical-journey'])
        self.assertNotIn('PASS',read([item(r)]))
        # Known P3-4: COMPLETE is not checked against skipped/unchecked lists.
        v['coverage']='COMPLETE'
        self.assertTrue(v['skipped'] and v['unchecked'])
        self.assertEqual(wire.verify_markdown(markdown(r)),'SHAPE_VALID_ONLY')
        self.assertEqual(read([item(r)]),['OBSERVED'])

    def test_sanitized_redaction_tombstone_never_carries_replacement(self):
        notice,target=aligned_notice();notice['data']['notice']='REDACT'
        secret='PRIVATE-RAW-TRACE-MUST-NOT-BE-COPIED'
        target['data']['limits'].append(secret)
        notice['data']['target']['data_digest']=wire.data_digest(target)
        notice['data']['reason']='Sanitized privacy tombstone for known prior identity only.'
        self.assertNotIn(secret,markdown(notice))
        self.assertEqual(apply_notice(notice,target),'TARGET_INVALIDATED')
        self.assertEqual(apply_notice(notice,target,target_integrity='UNKNOWN'),'UNVERIFIED')
        notice['data']['replacement']=target['data']
        with self.assertRaises(wire.ContractError):wire.validate_record(notice)

    def test_private_references_do_not_trigger_resolver_or_socket(self):
        summary=fixture();feedback=fixture('feedback')
        summary['data']['manifest_ref']='https://private.invalid/task42/immutable-manifest.json'
        with patch.object(socket,'socket',side_effect=AssertionError('unexpected network')):
            wire.validate_record(summary)
            self.assertEqual(read([item(summary)]),['OBSERVED'])
            self.assertEqual(read([item(feedback)]),['OBSERVED'])
            with self.assertRaises(NoSuchResource):
                wire._registry().get_or_retrieve('https://private.invalid/schema')
        # Only this source execution has no resolver path; no effective egress proof.

    def test_same_build_and_permission_evidence_are_not_schema_fields(self):
        r=fixture('feedback');d=r['data'];wire.validate_record(r)
        args=dict(reader_build=d['publisher_source_sha'],publisher_build=d['publisher_source_sha'],
                  actual_grants=True,effective_egress=True,real_readback=True)
        self.assertEqual(downstream_witness(**args),'BOUNDED_WITNESS')
        for field,value in [('publisher_build','e'*40),('actual_grants',None),
                            ('effective_egress',False),('real_readback',False)]:
            self.assertEqual(downstream_witness(**{**args,field:value}),'UNKNOWN')

    def test_carrier_human_truth_and_no_prefilled_feedback_receipt(self):
        r=fixture('feedback');text=markdown(r)
        self.assertEqual(wire.data_digest(wire.parse_markdown(text)),
                         wire.data_digest(wire.parse_markdown(text+'\nTASK_PASS=true\n# PASS\n')))
        self.assertEqual(wire.verify_markdown('TASK_PASS=true\n# PASS'),'UNSTRUCTURED_DISCUSSION')
        for key in ['comment_id','comment_ref','data_digest','manifest_ref']:
            bad=copy.deepcopy(r);bad['data'][key]='prefilled'
            with self.subTest(key=key),self.assertRaises(wire.ContractError):wire.validate_record(bad)
        for text in ['intro\n'+text,text+'\n'+wire.MARKER,
                     text.replace('kind: report','kind: report\nextra: true',1)]:
            with self.assertRaises(wire.ContractError):wire.verify_markdown(text)


class PinnedCompatibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.old=historical_reader()

    def test_actual_old_reader_refuses_all_new_profiles_without_partial_parse(self):
        for profile in ['summary','feedback','correction']:
            with self.subTest(profile=profile),self.assertRaises(self.old.ContractError):
                self.old.verify_markdown(markdown(fixture(profile)),'report')
            self.assertEqual(wire.verify_markdown(markdown(fixture(profile)),'report'),'SHAPE_VALID_ONLY')

    def test_original_v3_nonreport_and_report_pin_matrix(self):
        for kind,data in [('work_item',WORK),('intent',INTENT),('event',EVENT),('report',REPORT)]:
            r=envelope(kind,copy.deepcopy(data));text=markdown(r)
            self.assertEqual(self.old.verify_markdown(text,kind),'SHAPE_VALID_ONLY')
            self.assertEqual(wire.verify_markdown(text,kind),'SHAPE_VALID_ONLY')
            self.assertEqual(wire.record_disposition(r,'v4.14',writing=True),
                             'CURRENT_OBSERVATION' if kind=='report' else 'CURRENT_EXECUTABLE_SHAPE_ONLY')
            if kind=='report':
                self.assertEqual(wire.record_disposition(r,'v4.15'),'HISTORICAL_READ_ONLY')
                with self.assertRaises(wire.ContractError):wire.record_disposition(r,'v4.15',writing=True)
            else:
                self.assertEqual(wire.record_disposition(r,'v4.15',writing=True),'CURRENT_EXECUTABLE_SHAPE_ONLY')

    def test_actual_current_v3_template_and_pilot_corpus(self):
        paths=sorted((ROOT/'templates').rglob('*.md'))
        paths+=sorted((ROOT/'docs').rglob('*.md'))
        checked=[]
        for path in paths:
            text=path.read_text(encoding='utf8')
            if not text.startswith(wire.MARKER+'\n'):continue
            r=wire.parse_markdown(text)
            if r['schema']!='ads/github/v3':continue
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertEqual(self.old.verify_markdown(text),'SHAPE_VALID_ONLY')
                self.assertEqual(wire.verify_markdown(text),'SHAPE_VALID_ONLY')
            checked.append(path)
        # Explicit repository carriers, not the reviewer's separate 49-input
        # experiment. Removing any known normalized input must fail this test.
        expected={'templates/'+n+'-issue.md' for n in
                  ['blocker','bug-fix','planning-amendment','research-demo',
                   'research','task','validation-request','version']}
        expected.update('docs/implementation/4.14.0/dogfood/REAL_GITHUB_'+n+'.md'
                        for n in ['EVENT','REPORT','WORK_ITEM'])
        self.assertEqual({p.relative_to(ROOT).as_posix() for p in checked},expected)
        print('actual v3 normalized template/pilot corpus:',len(checked))

    def test_known_lexical_profile_difference_is_explicit_not_historical_emulation(self):
        base=envelope('event',{**EVENT,'session_ref':'x'})
        text=markdown(base)
        cases=[('!!str x',True,False),('1e5',True,False),('0x1F',False,True)]
        for spelling,old_accept,new_accept in cases:
            document=text.replace('session_ref: x','session_ref: '+spelling)
            self.assertNotEqual(document,text)
            for reader,accept in [(self.old,old_accept),(wire,new_accept)]:
                with self.subTest(spelling=spelling,reader=reader.__name__):
                    if accept:self.assertEqual(reader.verify_markdown(document),'SHAPE_VALID_ONLY')
                    else:
                        with self.assertRaises(reader.ContractError):reader.verify_markdown(document)

    def test_invalid_pair_and_pin_never_fallback_to_another_kind(self):
        for kind in ['work_item','intent','event']:
            r=envelope(kind,copy.deepcopy({'work_item':WORK,'intent':INTENT,'event':EVENT}[kind]))
            r['schema']='ads/github/v4'
            with self.subTest(kind=kind),self.assertRaises(wire.ContractError):wire.validate_record(r)
        for pin in ['main','v4.16','latest']:
            with self.assertRaises(wire.ContractError):wire.record_disposition(fixture(),pin)

    def test_frozen_predecessors_schema_and_level1_learning_are_unchanged(self):
        expected=json.loads((ROOT/'docs/implementation/4.15.0/S05_CONFORMANCE_MATRIX.json').read_text())['immutable_blobs']
        for name,value in expected.items():
            with self.subTest(path=name):self.assertEqual(blob((ROOT/name).read_bytes()),value)
        protocol=(ROOT/'standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md').read_text(encoding='utf8')
        self.assertIn('TASK_LEARNING=NONE_MATERIAL | resolvable task-learning-v1/v2 ref(s)',protocol)
        self.assertIn('The §10 Level-1 NONE_MATERIAL/ref convention stays unchanged.',protocol)


if __name__=='__main__':unittest.main(verbosity=2)
