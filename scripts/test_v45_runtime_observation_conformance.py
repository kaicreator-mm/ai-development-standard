#!/usr/bin/env python3
"""T05 fixture conformance, NOT real telemetry Validation.

Run: python3 scripts/test_v45_runtime_observation_conformance.py
Only Python stdlib; reads committed frozen-owner sources and bounded fixtures.
"""
import copy
import json
import re
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'schemas/runtime-observation-context-v1.schema.json'
STANDARD = ROOT / 'standards/OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md'
FIXTURES = ROOT / 'docs/implementation/4.5.0/dogfood/runtime-observation/cases.json'
DIMENSIONS = {'health/readiness', 'liveness', 'performance/resource', 'error/failure', 'business/domain'}
SENSITIVE = re.compile(r'(?i)(bearer\s+\S+|-----BEGIN .*PRIVATE KEY-----|(?:password|token|api[_-]?key|secret)\s*[:=]\s*[^\s,}]+|[\w.+-]+@[\w.-]+\.[a-z]{2,})')


def time_value(s):
    try:
        dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
        return dt if dt.tzinfo is not None else None
    except (ValueError, AttributeError, TypeError):
        return None


def expand_cases(raw):
    """Resolve immutable baseline+bounded test deltas; do not mutate source fixture."""
    resolved = {}
    for spec in raw:
        if 'copy' in spec:
            if spec['copy'] not in resolved:
                raise ValueError('fixture parent must precede child')
            case = copy.deepcopy(resolved[spec['copy']])
            case['id'], case['expect'] = spec['id'], spec['expect']
            for path, value in spec.get('overrides', {}).items():
                node, *parts = path.split('.')
                node = case if not parts else case[node]
                for key in parts[:-1]:
                    node = node[int(key)] if isinstance(node, list) else node[key]
                key = parts[-1] if parts else path
                if parts:
                    node[int(key) if isinstance(node, list) else key] = value
                else:
                    node[key] = value
        else:
            case = copy.deepcopy(spec)
        resolved[case['id']] = case
    return list(resolved.values())


def evaluate(case, schema):
    """Fixture-only decision: never a universal runtime health/result object."""
    obs, expected = case.get('observation', {}), case.get('expected_subject', {})
    if not isinstance(obs, dict) or set(schema['required']) - obs.keys():
        return 'BLOCKED'
    if set(obs) - set(schema['properties']):
        return 'BLOCKED'
    if obs.get('schema_version') != 1 or not all(
        isinstance(obs.get(k), str) and obs[k].strip()
        for k in ('observation_id', 'artifact_ref', 'deployment_ref', 'environment_ref')
    ):
        return 'BLOCKED'
    if any(obs.get(k) != expected.get(k) for k in ('artifact_ref', 'deployment_ref', 'environment_ref')):
        return 'BLOCKED'
    if not expected.get('signal_source_ref') or not expected.get('configuration_profile_ref'):
        return 'BLOCKED'
    if obs.get('configuration_profile_ref') != expected['configuration_profile_ref']:
        return 'BLOCKED'
    window = obs.get('observation_window')
    if not isinstance(window, dict) or set(window) != {'start_ref', 'end_ref'}:
        return 'BLOCKED'
    start, end = time_value(window['start_ref']), time_value(window['end_ref'])
    if not start or not end or start > end or window != expected.get('observation_window'):
        return 'BLOCKED'
    signals, refs = case.get('signals', []), obs.get('signal_refs', [])
    if not isinstance(signals, list) or not signals or not isinstance(refs, list) or not refs:
        return 'BLOCKED'
    if any(not isinstance(s, dict) for s in signals):
        return 'BLOCKED'
    if len(refs) != len(set(refs)) or len(signals) != len(refs) or {s.get('ref') for s in signals} != set(refs):
        return 'BLOCKED'
    custom = case.get('project_dimensions', [])
    if not isinstance(custom, list) or any(not isinstance(x, str) or not x.strip() for x in custom):
        return 'BLOCKED'
    if any(s.get('source_ref') != expected['signal_source_ref']
           or s.get('dimension') not in DIMENSIONS | set(custom)
           or not time_value(s.get('observed_at'))
           or not start <= time_value(s['observed_at']) <= end for s in signals):
        return 'BLOCKED'
    for field in ('signal_refs', 'evidence_refs'):
        if not isinstance(obs.get(field, []), list) or any(
            not isinstance(ref, str) or not ref.startswith('ref:') or SENSITIVE.search(ref)
            for ref in obs.get(field, [])):
            return 'BLOCKED'
    if any(SENSITIVE.search(json.dumps(s)) for s in signals):
        return 'BLOCKED'
    if case.get('historical') and not case.get('historical_qualification_ref'):
        return 'BLOCKED'
    required = set(case.get('required_dimensions', []))
    if not required or not required <= DIMENSIONS | set(custom):
        return 'BLOCKED'
    available = {s['dimension'] for s in signals if s.get('state') == 'OBSERVED'}
    if not required <= available:
        return 'NOT_RUN'
    if case.get('attempted_inference') in {
        'DEPLOYMENT_SUCCESS_IS_HEALTHY', 'HEALTH_IS_BUSINESS_PASS',
        'BACKEND_REACHABLE_IS_HEALTHY', 'NO_ALERT_IS_HEALTHY',
        'RUNTIME_OBSERVATION_IS_VALIDATION_PASS', 'RUNTIME_OBSERVATION_IS_RELEASE_READY',
        'RUNTIME_OBSERVATION_IS_TASK_DONE', 'HISTORICAL_RETROACTIVE_PASS',
    }:
        return 'REJECT_INFERENCE'
    return 'FIXTURE_CONFORMANT'


class RuntimeObservationConformance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
        cls.standard = STANDARD.read_text(encoding='utf-8')
        cls.fixture = json.loads(FIXTURES.read_text(encoding='utf-8'))
        cls.cases = expand_cases(cls.fixture['cases'])

    def test_source_binding(self):
        self.assertEqual(self.schema['$schema'], 'https://json-schema.org/draft/2020-12/schema')
        self.assertEqual(self.schema['properties']['schema_version']['const'], 1)
        for field in ('artifact_ref', 'deployment_ref', 'environment_ref', 'observation_window', 'signal_refs'):
            self.assertIn(field, self.schema['required'])
        self.assertFalse({'validation_result', 'release_ready', 'task_done', 'healthy'} & set(self.schema['properties']))
        for phrase in ('DEPLOYMENT_SUCCEEDED != RUNTIME_HEALTHY',
                       'no alert observed != healthy', 'backend reachable != runtime healthy',
                       'signal source unavailable != NOT_APPLICABLE'):
            self.assertIn(phrase, self.standard)

    def test_positive_and_negative_fixtures(self):
        self.assertEqual(self.fixture['evidence_level'], 'COMMITTED_FIXTURE_ONLY_NOT_REAL_RUNTIME')
        self.assertGreaterEqual(len(self.cases), 20)
        self.assertEqual(len({c['id'] for c in self.cases}), len(self.cases))
        seen = set()
        for case in self.cases:
            with self.subTest(case=case['id']):
                self.assertEqual(evaluate(case, self.schema), case['expect'])
                seen.add(case['expect'])
        self.assertEqual(seen, {'FIXTURE_CONFORMANT', 'BLOCKED', 'NOT_RUN', 'REJECT_INFERENCE'})

    def test_schema_and_privacy_boundary(self):
        self.assertFalse(self.schema.get('additionalProperties', True))
        self.assertNotIn('raw_payload', self.schema['properties'])
        self.assertNotIn('secret', self.schema['properties'])
        self.assertIn('secret', self.standard.lower())
        valid = next(c for c in self.cases if c['id'] == 'dimensioned-positive')
        for name, secret in [('bearer', 'Bearer abc123'), ('email', 'person@example.com'),
                             ('token', 'token=plaintext')]:
            with self.subTest(secret=name):
                leaked = copy.deepcopy(valid)
                leaked['observation']['evidence_refs'] = ['ref:' + secret]
                self.assertEqual(evaluate(leaked, self.schema), 'BLOCKED')


if __name__ == '__main__':
    unittest.main(verbosity=2)
