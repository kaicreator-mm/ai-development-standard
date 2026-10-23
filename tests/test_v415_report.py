"""Frozen L2 sections2/3 and RFC8785 oracles; offline conformance, no runtime PASS."""
import copy
import hashlib
import json
import math
from pathlib import Path
import struct
import subprocess
import sys
import unittest

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import verify_github_structured_interaction as v
from test_github_structured_interaction import WORK, INTENT, EVENT, REPORT, envelope

FIX = ROOT / 'tests/fixtures/v415'
def fixture(name='summary'):
    return json.loads((FIX / (name + '.json')).read_text(encoding='utf8'))
def markdown(record):
    return v.MARKER + '\n```yaml\n' + yaml.safe_dump(record, sort_keys=False, allow_unicode=True) + '```\n\nHuman prose has no authority.\n'
def successor(previous, reason):
    out = copy.deepcopy(previous)
    d = out['data']
    d['revision'] += 1
    d['supersedes'] = {'revision': previous['data']['revision'], 'data_digest': v.data_digest(previous), 'comment_ref': d['subject']['issue_ref'] + '#issuecomment-123'}
    d['manifest_ref'] = 'object:private/task42/attempt1/r2/manifest.json'
    d['manifest_sha256'] = 'f' * 64
    if reason == 'TASK_LEARNING':
        d['learning'] = {'state': 'REFERENCED', 'source_refs': ['github:task-learning-v2:actual-ref']}
    else:
        d['verifier']['source_refs'].append('github:late-ci:run:8')
    return out

class ReportShape(unittest.TestCase):
    def reject(self, record):
        with self.assertRaises(v.ContractError):
            v.validate_record(record)

    def test_three_profiles_and_root_are_real_draft202012(self):
        schema = json.loads(v.REPORT_SCHEMA_FILE.read_text(encoding='utf8'))
        Draft202012Validator.check_schema(schema)
        for name in ('summary','feedback','correction'):
            record = fixture(name)
            self.assertEqual(list(Draft202012Validator(schema).iter_errors(record)), [])
            self.assertEqual(v.verify_markdown(markdown(record), 'report'), 'SHAPE_VALID_ONLY')
            self.assertEqual(v.record_disposition(record), 'CURRENT_OBSERVATION')

    def test_wrong_schema_kind_profiles_and_extra_keys(self):
        for name in ('summary','feedback','correction'):
            for target, key, value in [('root','extra',1), ('root','schema','ads/github/v5'),('root','kind','event'),('data','extra',1),('data','report_kind','EVIDENCE_UPDATE'),('data','report_kind','TASK_LEARNING'),('data','revision',True),('data','revision',0),('data','revision','1')]:
                r = fixture(name)
                (r if target == 'root' else r['data'])[key] = value
                with self.subTest(name=name,key=key,value=value):
                    self.reject(r)

    def test_every_profile_required_field_is_required(self):
        for name in ('summary','feedback','correction'):
            base = fixture(name)
            for key in base['data']:
                r = copy.deepcopy(base); del r['data'][key]
                with self.subTest(name=name,key=key):self.reject(r)

    def test_manifest_free_feedback_and_notice_only_correction(self):
        for name in ('feedback','correction'):
            for key in ('manifest_ref','manifest_sha256','metrics','replacement','cost','data_digest','comment_ref','comment_id'):
                r = fixture(name); r['data'][key] = 'not-allowed'
                with self.subTest(name=name,key=key):self.reject(r)
        r = fixture('correction');r['data']['target']['report_kind']='EXECUTION_CORRECTION';self.reject(r)

    def test_nested_unknown_keys_and_types(self):
        for path in [('subject',),('actor',),('cost',),('verifier',),('learning',),('aggregation',),('subject','currentness')]:
            r=fixture();d=r['data']
            for k in path:d=d[k]
            d['invented']=1
            with self.subTest(path=path):self.reject(r)
        for val in ('12',True,[],{}):
            r=fixture();r['data']['metrics'][0]['value']=val;self.reject(r)

    def test_missing_cost_is_unknown_never_zero(self):
        r=fixture();self.assertIsNone(r['data']['cost']['value']);v.validate_record(r)
        for key,val in [('value',0),('epistemic','OBSERVED'),('basis','BILLED')]:
            r=fixture();r['data']['cost'][key]=val;self.reject(r)
        r=fixture();r['data']['cost'].update(value=1.25,currency='USD',basis='BILLED',pricing_basis='invoice:7',epistemic='OBSERVED',source_refs=['billing:invoice:7']);v.validate_record(r)
        r['data']['cost']['source_refs']=[];self.reject(r)

    def test_epistemic_metric_missing_denominator_and_currentness(self):
        r=fixture();m=r['data']['metrics'][0]
        m['value']=0;self.reject(r)
        m.update(value=17,epistemic='OBSERVED',coverage='PARTIAL',source_refs=['provider:usage:7']);v.validate_record(r)
        del m['currentness'];self.reject(r)

    def test_leaf_dedup_and_exact_verifier_subject(self):
        for action in ('duplicate','parent','missing-attempt','verifier'):
            r=fixture();d=r['data']
            if action=='duplicate':d['aggregation']['attempt_refs']*=2
            elif action=='parent':d['aggregation']['mode']='PARENT_PLUS_CHILD'
            elif action=='missing-attempt':d['aggregation']['attempt_refs']=['another']
            else:d['verifier']['subject_sha']='f'*40
            self.reject(r)

    def test_feedback_distinct_phases_and_independent_verifier(self):
        for phase in ('PRESENTED','ACCEPTED','APPLIED','SKIPPED','OBSERVED_EFFECT'):
            r=fixture('feedback');r['data']['phase']=phase;v.validate_record(r)
        r=fixture('feedback');r['data']['phase']='INDEPENDENTLY_CHECKED';self.reject(r)
        r['data']['verifier_refs']=['github:independent-review:7'];v.validate_record(r)
        r['data']['epistemic']='SELF_REPORTED';self.reject(r)
        r=fixture('feedback');r['data']['ads_subject_sha']='e'*40;self.reject(r)

    def test_source_issue_time_and_manifest_locator(self):
        cases=[('observed_at','2026-99-99T00:00:00Z'),('manifest_ref','https://s3/file?X-Amz-Signature=secret')]
        for key,val in cases:r=fixture();r['data'][key]=val;self.reject(r)
        r=fixture();r['data']['subject']['repository']='other/repo';self.reject(r)

    def test_verifier_outcomes_cannot_double_count_scope(self):
        r=fixture();r['data']['verifier']['failed']=['schema-shape'];self.reject(r)

    def test_cli_public_digest_and_old_pin_rejection(self):
        import tempfile
        # Per-run isolation; callers may set TMP/TEMP to their authorized root.
        with tempfile.TemporaryDirectory(prefix='ads-v415-cli-') as temporary:
            path=Path(temporary)/'report.md';path.write_text(markdown(fixture()),encoding='utf8')
            cmd=[sys.executable,str(ROOT/'scripts/verify_github_structured_interaction.py'),str(path),'--kind','report']
            p=subprocess.run(cmd+['--data-digest'],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr);self.assertEqual(p.stdout.strip(),v.data_digest(fixture()))
            p=subprocess.run(cmd+['--effective-pin','v4.14'],capture_output=True,text=True)
            self.assertEqual(p.returncode,1);self.assertIn('UNSUPPORTED_SCHEMA',p.stdout)

    def test_v3_schema_bytes_and_offline_registry(self):
        raw=v.SCHEMA_FILE.read_bytes()
        blob=hashlib.sha1(('blob '+str(len(raw))+'\0').encode()+raw).hexdigest()
        self.assertEqual(blob,'a8c5d852c239f69850e7d856af75ca8179aff1dd')
        for k,d in [('work_item',WORK),('intent',INTENT),('event',EVENT)]:
            r=envelope(k,d)
            for pin in ('v4.14','v4.15'):
                self.assertEqual(v.record_disposition(r,pin), 'CURRENT_EXECUTABLE_SHAPE_ONLY')
        with self.assertRaises(Exception):v._registry().get_or_retrieve('https://remote.invalid/schema')

    def test_v3_report_is_historical_only_on_new_pin(self):
        r=envelope('report',REPORT)
        self.assertEqual(v.record_disposition(r,'v4.14',True),'CURRENT_OBSERVATION')
        self.assertEqual(v.record_disposition(r),'HISTORICAL_READ_ONLY')
        with self.assertRaises(v.ContractError):v.record_disposition(r,writing=True)
        with self.assertRaises(v.ContractError):v.record_disposition(fixture(),'v4.14')
        with self.assertRaises(v.ContractError):v.record_disposition(fixture(),'main')

class ParsingAndJCS(unittest.TestCase):
    def test_rfc8785_appendix_b_binary64_vectors(self):
        # Independent numeric oracle: https://www.rfc-editor.org/rfc/rfc8785#appendix-B
        pairs=[('0000000000000000','0'),('8000000000000000','0'),('0000000000000001','5e-324'),('8000000000000001','-5e-324'),('7fefffffffffffff','1.7976931348623157e+308'),('ffefffffffffffff','-1.7976931348623157e+308'),('4340000000000000','9007199254740992'),('c340000000000000','-9007199254740992'),('4430000000000000','295147905179352830000'),('44b52d02c7e14af5','9.999999999999997e+22'),('44b52d02c7e14af6','1e+23'),('44b52d02c7e14af7','1.0000000000000001e+23'),('444b1ae4d6e2ef4e','999999999999999700000'),('444b1ae4d6e2ef4f','999999999999999900000'),('444b1ae4d6e2ef50','1e+21'),('3eb0c6f7a0b5ed8c','9.999999999999997e-7'),('3eb0c6f7a0b5ed8d','0.000001'),('41b3de4355555553','333333333.3333332'),('41b3de4355555554','333333333.33333325'),('41b3de4355555555','333333333.3333333'),('41b3de4355555556','333333333.3333334'),('41b3de4355555557','333333333.33333343'),('becbf647612f3696','-0.0000033333333333333333'),('43143ff3c1cb0959','1424953923781206.2')]
        for bits,expected in pairs:
            with self.subTest(bits=bits):self.assertEqual(v.canonical_json(struct.unpack('>d',bytes.fromhex(bits))[0]).decode(),expected)

    def test_utf16_sorting_strings_arrays_and_no_normalization(self):
        keys=['\u20ac','\r','\ufb33','1','\U0001f600','\u0080','\u00f6']
        expected=['\r','1','\u0080','\u00f6','\u20ac','\U0001f600','\ufb33']
        self.assertEqual(list(json.loads(v.canonical_json(dict.fromkeys(keys,0)))),expected)
        self.assertEqual(v.canonical_json([3,2,1]),b'[3,2,1]')
        self.assertNotEqual(v.canonical_json('é'),v.canonical_json('e\u0301'))
        self.assertEqual(v.canonical_json('\x00\n\\"'),b'"\\u0000\\n\\\\\\""')

    def test_non_json_and_resource_bound_rejection(self):
        for val in (float('nan'),float('inf'),-float('inf'),9007199254740992,b'bytes',{1:2},{1,2},'\ud800'):
            with self.subTest(value=repr(val)),self.assertRaises(v.ContractError):v.canonical_json(val)
        val=0
        for _ in range(66):val=[val]
        with self.assertRaises(v.ContractError):v.canonical_json(val)

    def test_unsafe_yaml_and_duplicate_keys_rejected(self):
        original=markdown(fixture())
        bad=['kind: report\nkind: report','kind: &a report','kind: *a','kind: !unsafe report','kind: !!str report','kind: !!python/object:os.system {}']
        for fragment in bad:
            with self.subTest(fragment=fragment),self.assertRaises(v.ContractError):v.verify_markdown(original.replace('kind: report',fragment))
        for scalar in ('.nan','.inf','!!binary aGVsbG8=','!!set {x: null}','!!timestamp 2026-10-21'):
            text=original.replace('value: null','value: '+scalar,1)
            with self.subTest(scalar=scalar),self.assertRaises(v.ContractError):v.verify_markdown(text)

    def test_equivalent_yaml_and_human_markdown_have_same_data_digest(self):
        record=fixture();a=v.parse_markdown(markdown(record))
        flow=v.MARKER+'\n```yaml\n'+json.dumps(record,ensure_ascii=False)+'\n```\nChanged human prose\n'
        self.assertEqual(v.data_digest(a),v.data_digest(v.parse_markdown(flow)))
        self.assertEqual(v.data_digest(a),hashlib.sha256(v.canonical_json(a['data'])).hexdigest())
        b=copy.deepcopy(a);b['data']['limits'].append('changed');self.assertNotEqual(v.data_digest(a),v.data_digest(b))

    def test_equivalent_yaml_number_spellings_have_same_digest(self):
        r=fixture();r['data']['metrics'][0].update(value=1e-7,epistemic='OBSERVED')
        text=markdown(r)
        self.assertIn('1.0e-07',text)
        variants=[text.replace('1.0e-07',x) for x in ('1e-7','0.0000001','1.000e-7')]
        self.assertEqual({v.data_digest(v.parse_markdown(x)) for x in variants},{v.data_digest(r)})

    def test_parser_marker_and_size_limits(self):
        text=markdown(fixture())
        for bad in ('quote\n'+text,text+'\n'+v.MARKER,text.replace('```yaml','```json',1),text+'x'*v.MAX_BYTES):
            with self.assertRaises(v.ContractError):v.verify_markdown(bad)
        self.assertEqual(v.verify_markdown('TASK_PASS=true'), 'UNSTRUCTURED_DISCUSSION')

class ImmutableRevisions(unittest.TestCase):
    def test_p2_1_evidence_update_is_new_same_summary_revision(self):
        a=fixture();b=successor(a,'EVIDENCE_UPDATE');before=copy.deepcopy(a)
        self.assertEqual(v.validate_summary_revision(a,b,'EVIDENCE_UPDATE'),'SHAPE_VALID_ONLY')
        self.assertEqual(a,before);self.assertNotEqual(v.data_digest(a),v.data_digest(b))
        for key,val in [('report_id','other'),('revision',3),('manifest_ref',a['data']['manifest_ref']),('manifest_sha256',a['data']['manifest_sha256'])]:
            wrong=copy.deepcopy(b);wrong['data'][key]=val
            with self.subTest(key=key),self.assertRaises(v.ContractError):v.validate_summary_revision(a,wrong,'EVIDENCE_UPDATE')

    def test_p2_1_learning_requires_new_manifest_and_actual_v2_ref(self):
        a=fixture();b=successor(a,'TASK_LEARNING')
        self.assertEqual(v.validate_summary_revision(a,b,'TASK_LEARNING'),'SHAPE_VALID_ONLY')
        b['data']['learning']={'state':'NONE_MATERIAL','source_refs':[]}
        with self.assertRaises(v.ContractError):v.validate_summary_revision(a,b,'TASK_LEARNING')
        with self.assertRaises(v.ContractError):v.validate_summary_revision(fixture('feedback'),b,'TASK_LEARNING')

    def test_revision_lineage_and_late_ref_cannot_be_synthesized(self):
        a=fixture();b=successor(a,'EVIDENCE_UPDATE')
        for action in ('old-digest','wrong-issue','wrong-prev','no-new-ref','other-attempt'):
            r=copy.deepcopy(b)
            if action=='old-digest':r['data']['supersedes']['data_digest']='0'*64
            elif action=='wrong-issue':r['data']['supersedes']['comment_ref']='https://github.com/other/repo/issues/1#issuecomment-1'
            elif action=='wrong-prev':r['data']['supersedes']['revision']=2
            elif action=='no-new-ref':r['data']['verifier']['source_refs']=a['data']['verifier']['source_refs']
            else:r['data']['subject']['attempt_ref']='other-attempt'
            with self.subTest(action=action),self.assertRaises(v.ContractError):v.validate_summary_revision(a,r,'EVIDENCE_UPDATE')

    def test_correction_is_notice_not_replacement_or_authority(self):
        correction=fixture('correction')
        with self.assertRaises(v.ContractError):v.validate_summary_revision(fixture(),correction,'EVIDENCE_UPDATE')
        # A cross-namespace notice remains observational shape, not cancellation.
        correction['data']['publisher_namespace']='other-agent:namespace'
        v.validate_record(correction)
        self.assertEqual(v.observation_status(correction,edited=False),'OBSERVED_SHAPE_ONLY')

    def test_edit_duplicate_and_conflicting_immutable_key(self):
        a=fixture();b=copy.deepcopy(a);b['data']['limits'].append('changed')
        self.assertEqual(v.observation_status(a),'UNKNOWN_INTEGRITY')
        self.assertEqual(v.observation_status(a,edited=True),'UNVERIFIED_EDIT')
        self.assertEqual(v.observation_status(a,edited=False,previous_record=a),'DUPLICATE')
        self.assertEqual(v.observation_status(b,edited=False,previous_record=a),'CONFLICT')
        b['data']['revision']=2;b['data']['supersedes']={'revision':1,'data_digest':v.data_digest(a),'comment_ref':a['data']['subject']['issue_ref']+'#issuecomment-123'}
        self.assertEqual(v.observation_status(b,edited=False,previous_record=a,same_comment=True),'CONFLICT')

if __name__=='__main__':unittest.main(verbosity=2)
