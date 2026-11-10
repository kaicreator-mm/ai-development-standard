"""Source-only bounded DAG serial-edge evidence probe; never mutates native DAG."""
import json


def assess_edge(evidence):
    """Classify serial-edge rationale; no eligibility, Claim or write authority issued."""
    required = ('edge', 'frozen_contract_ref', 'code_baseline_required',
                'write_set_conflict', 'join_only', 'native_dependency')
    if any(key not in evidence for key in required):
        return {'classification': 'UNKNOWN', 'dispatch': 'NOT_AUTHORIZED',
                'reason': 'Missing material source/authority evidence'}
    if not isinstance(evidence['frozen_contract_ref'], str) or not evidence['frozen_contract_ref'].strip():
        return {'classification': 'UNKNOWN', 'dispatch': 'NOT_AUTHORIZED',
                'reason': 'No frozen contract evidence'}
    if any(not isinstance(evidence[key], bool) for key in
           ('code_baseline_required', 'write_set_conflict', 'join_only', 'native_dependency')):
        return {'classification': 'UNKNOWN', 'dispatch': 'NOT_AUTHORIZED',
                'reason': 'Invalid boolean evidence'}
    if evidence['code_baseline_required'] or evidence['write_set_conflict']:
        classification = 'MATERIAL_SERIAL_EDGE'
    elif evidence['join_only']:
        classification = 'POSSIBLE_FALSE_SERIAL_EDGE'
    else:
        classification = 'UNKNOWN'
    return {'classification': classification,
            'dispatch': 'HOLD_NATIVE_DEPENDENCY' if evidence['native_dependency'] else 'NOT_AUTHORIZED',
            'reason': 'Advisory only; current native graph, write-set and accepted Claim remain authoritative',
            'may_mutate_native_dependencies': False,
            'may_issue_claim_or_start_record': False,
            'parallel_source_preparation': 'ONLY_IF_INDEPENDENTLY_AUTHORIZED'}


def run_demo():
    common = {'edge': 'A -> B', 'frozen_contract_ref': 'exact-contract-sha:path',
              'code_baseline_required': False, 'write_set_conflict': False,
              'join_only': True, 'native_dependency': True}
    join = assess_edge(common)
    real = assess_edge({**common, 'code_baseline_required': True})
    conflict = assess_edge({**common, 'write_set_conflict': True})
    unknown = assess_edge({**common, 'frozen_contract_ref': ''})
    assert join['classification'] == 'POSSIBLE_FALSE_SERIAL_EDGE'
    assert join['dispatch'] == 'HOLD_NATIVE_DEPENDENCY'
    assert real['classification'] == conflict['classification'] == 'MATERIAL_SERIAL_EDGE'
    assert unknown['classification'] == 'UNKNOWN'
    assert all(not e.get('may_mutate_native_dependencies', False)
               for e in (join, real, conflict, unknown))
    return {'schema': 'ads/formal-dag-edge-qualification-demo/v1',
            'source_rule': 'prospective TASK_DECOMPOSITION_STANDARD.md §13.1',
            'scenarios': {'join_only': join, 'real_code_baseline': real,
                          'shared_writer': conflict, 'unknown': unknown},
            'verdict': 'PASS_FALSE_SERIAL_ADVISORY_WITHOUT_BYPASSING_NATIVE_DAG',
            'limitations': ['Synthetic frozen-contract premise, not a real approved native DAG',
                            'Does not grant dispatch/Claim, mutate native dependencies, or prove all ADS rules']}


if __name__ == '__main__':
    print(json.dumps(run_demo(), indent=2))
