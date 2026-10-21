"""S03 test-only finite contract oracle; no network, runtime or authority proof."""
from pathlib import Path
import sys
import re

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import verify_github_structured_interaction as wire


def collection_complete(pages, max_pages=20, max_retries=2):
    """Supplied response observations only; never treats an error as empty data."""
    cursor = None
    visited = set()
    retries = 0
    accepted = 0
    for index, page in enumerate(pages):
        if page.get('cursor') != cursor or accepted >= max_pages:
            return False
        status = page.get('status')
        if status in (429, 503, 'TIMEOUT') or (status == 403 and page.get('rate_limited')):
            retries += 1
            if retries > max_retries or not page.get('within_budget'):
                return False
            if status in (429, 403) and not page.get('wait_respected'):
                return False
            continue
        if status != 200 or not isinstance(page.get('items'), list):
            return False
        accepted += 1
        nxt = page.get('next')
        if nxt is None:
            return index == len(pages) - 1
        if nxt in visited or nxt == cursor:
            return False
        visited.add(nxt)
        cursor = nxt
    return False


def identity(record):
    d = record['data']
    return (d['subject']['issue_ref'], d['publisher_namespace'], d['report_id'],
            d['revision'], d['report_kind'])


def observe(items, *, complete, issue, source_sha, ads_sha):
    """A status per supplied native comment; OBSERVED is never an engineering PASS."""
    if not complete:
        return ['UNKNOWN'] * len(items)
    results = []
    groups = {}
    comments = {}
    for pos, item in enumerate(items):
        r = item['record']
        try:
            wire.validate_record(r)
            disposition = wire.record_disposition(r)
        except wire.ContractError:
            results.append('INVALID_SCHEMA')
            continue
        if disposition == 'HISTORICAL_READ_ONLY':
            results.append('HISTORICAL_READ_ONLY')
            continue
        if r['kind'] != 'report' or r['schema'] != 'ads/github/v4':
            results.append('NOT_REPORT')
            continue
        d = r['data']
        sub = d['subject']
        if (sub['issue_ref'] != issue or item['issue'] != issue or
                item['url'] != issue + '#issuecomment-' + str(item['id'])):
            results.append('UNVERIFIED')
            continue
        if (sub['source_sha'] != source_sha or sub['ads_revision'] != ads_sha or
                sub['currentness']['state'] != 'CURRENT' or not item.get('source_witness')):
            results.append('UNKNOWN')
            continue
        digest = wire.data_digest(r)
        state = 'OBSERVED'
        edit = item.get('edit_evidence', 'UNKNOWN')
        if edit == 'EDITED':
            state = 'UNVERIFIED'
        elif edit != 'CLEAR':
            state = 'UNKNOWN'
        if item.get('previous_digest', digest) != digest:
            state = 'CONFLICT'
        results.append(state)
        groups.setdefault(identity(r), []).append((pos, digest))
        comments.setdefault(item['id'], []).append((pos, digest))
    for entries in [*groups.values(), *comments.values()]:
        if len({digest for _, digest in entries}) > 1:
            for pos, _ in entries:
                results[pos] = 'CONFLICT'
        elif len(entries) > 1:
            for pos, _ in entries[1:]:
                if results[pos] == 'OBSERVED':
                    results[pos] = 'DUPLICATE'
    # Resolve actual supplied native predecessors, independent of input ordering.
    candidates = [(pos, item) for pos, item in enumerate(items)
                  if results[pos] in ('OBSERVED', 'DUPLICATE')]
    for pos, item in sorted(candidates, key=lambda pair: pair[1]['record']['data']['revision']):
        d = item['record']['data']
        prior = d['supersedes']
        if prior is None:
            continue
        matches = [(i, x) for i, x in enumerate(items) if x['url'] == prior['comment_ref']]
        if not matches:
            results[pos] = 'UNKNOWN'
            continue
        for i, native in matches:
            pd = native['record']['data']
            aligned = (results[i] in ('OBSERVED', 'DUPLICATE') and
                       identity(native['record'])[:3] == identity(item['record'])[:3] and
                       pd['report_kind'] == d['report_kind'] and pd['revision'] == prior['revision'] and
                       wire.data_digest(native['record']) == prior['data_digest'] and
                       all(pd['subject'][k] == d['subject'][k] for k in
                           ('task_ref', 'attempt_ref', 'source_sha', 'ads_revision', 'ads_profile')))
            if not aligned:
                results[pos] = 'UNVERIFIED'
                break
    return results


def correction_status(notice, target, *, native_target_url, native_issue,
                      authority_witness, target_integrity='OBSERVED',
                      notice_integrity='OBSERVED'):
    """Application checks omitted by a shape-only validator are explicit here."""
    try:
        wire.validate_record(notice)
        wire.validate_record(target)
    except wire.ContractError:
        return 'INVALID_SCHEMA'
    n, d = notice['data'], target['data']
    if (n.get('report_kind') != 'EXECUTION_CORRECTION' or
            d.get('report_kind') not in ('EXECUTION_SUMMARY', 'EXPERIENCE_USE_FEEDBACK')):
        return 'INVALID_SCHEMA'
    t = n['target']
    same_scope = all(n['subject'][k] == d['subject'][k]
                     for k in ('repository', 'issue_ref', 'task_ref', 'attempt_ref',
                               'source_sha', 'ads_revision', 'ads_profile'))
    matches = (same_scope and native_issue == d['subject']['issue_ref'] and
               native_target_url.startswith(native_issue + '#issuecomment-') and
               t['comment_ref'] == native_target_url and t['issue_ref'] == native_issue and
               n['publisher_namespace'] == t['publisher_namespace'] == d['publisher_namespace'] and
               t['task_ref'] == d['subject']['task_ref'] and
               all(t[k] == d[k] for k in ('report_id', 'revision', 'report_kind')) and
               t['data_digest'] == wire.data_digest(target))
    if not matches:
        return 'DISPUTED'
    if not authority_witness or target_integrity != 'OBSERVED' or notice_integrity != 'OBSERVED':
        return 'UNVERIFIED'
    return 'DISPUTED' if n['notice'] == 'DISPUTE' else 'TARGET_INVALIDATED'


def feedback_observation(record, *, build_sha, ads_subject_sha, source_witness,
                         phase_witness, independent_witness=False):
    try:
        wire.validate_record(record)
    except wire.ContractError:
        return 'INVALID_SCHEMA'
    d = record['data']
    if d['report_kind'] != 'EXPERIENCE_USE_FEEDBACK':
        return 'INVALID_SCHEMA'
    if (d['publisher_source_sha'] != build_sha or d['ads_subject_sha'] != ads_subject_sha or
            not source_witness or not phase_witness or d['epistemic'] == 'UNKNOWN'):
        return 'UNKNOWN'
    if d['phase'] == 'INDEPENDENTLY_CHECKED' and not independent_witness:
        return 'UNKNOWN'
    return d['phase']


def downstream_witness(*, reader_build, publisher_build, actual_grants,
                       effective_egress, real_readback):
    """Caller-supplied witness flags are fixtures, not observed real capability."""
    return ('BOUNDED_WITNESS' if re.fullmatch('[0-9a-f]{40}', reader_build) and
            reader_build == publisher_build and
            all(x is True for x in (actual_grants, effective_egress, real_readback))
            else 'UNKNOWN')
