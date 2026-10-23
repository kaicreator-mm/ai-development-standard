"""ADS v4.17 P03 shared bounded Golden source-only conformance (G01-G14).

Finite, deterministic standards oracle over source-only fixtures: each pair
proves its positive AND forbidden expected outcome. Language-neutral pair
definitions live in templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md
(#v417-shared-bounded-golden-pairs); this module is only a finite oracle, and
its labels are analysis values, never wire enums, Gates or Task/Review/Release
authority. SOURCE_ONLY_CONFORMANCE only: real task-meta/Tally publication,
real GitHub native readback and protected Host effects stay NOT_RUN.
Reused owners are exercised unchanged: v415_consumer_oracle,
verify_github_structured_interaction (frozen v4/v5 schemas), the v4.16 T03
reader bridge and T02 measurement reducer.
"""
import copy
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from v415_consumer_oracle import (collection_complete, correction_status,
    downstream_witness, feedback_observation, observe)
sys.path.insert(0, str(HERE.parent / 'scripts'))
import verify_github_structured_interaction as wire
import test_v416_t03_reader as t03
from v416_measurement_reconciler import cost_total, metric_total


# ---------------------------------------------------------------------------
# C08 source-only oracle (GAIP §10 v4.17 strategy-trajectory interpretation).
# ---------------------------------------------------------------------------
def _collapse_deliveries(selections):
    """Count a unique original causal selection opportunity once: repeated
    delivery, pagination re-read, late report publication and corrected copies
    share one owning occurrence; a genuinely selected retry keeps its own."""
    seen, out = set(), []
    for s in selections:
        if s['occurrence'] in seen:
            continue
        seen.add(s['occurrence'])
        out.append(s)
    return out


def c08_edge_verdict(prev, sel):
    """One OBSERVED-lane decision for the causal edge prev->sel: eligible only
    with a witnessed causal selection edge and an accepted owner decision that
    covers both governed strategy identities."""
    d = sel.get('decision') or {}
    if not (sel.get('causal') and d.get('accepted') is True
            and d.get('covers') == (prev['strategy'], sel['strategy'])):
        return 'UNKNOWN'
    return 'STRATEGY_CHANGED' if d.get('changed') is True else 'STRATEGY_KEPT'


def c08_pivot_metrics(selections):
    """(N, D, excluded) for N_obs_pivot/D_obs_pivot; UNKNOWN edges are excluded
    from both numerator and eligible denominator."""
    n = d = excluded = 0
    chain = _collapse_deliveries(selections)
    for prev, sel in zip(chain, chain[1:]):
        verdict = c08_edge_verdict(prev, sel)
        if verdict == 'UNKNOWN':
            excluded += 1
        else:
            d += 1
            n += verdict == 'STRATEGY_CHANGED'
    return n, d, excluded


def c08_revisit_metrics(selections):
    """(N, D, excluded) for N_obs_revisit/D_obs_revisit: a selection is an
    eligible return opportunity only after a previous witnessed visit and a
    subsequent witnessed departure of the anchored strategy; the outcome needs
    a witnessed owner equivalence (return_of) or nonmatch (non_return_of)
    decision - never string matching. Undecidable is UNKNOWN, excluded from
    both numerator and eligible denominator."""
    n = d = excluded = 0
    chain = _collapse_deliveries(selections)
    for i, sel in enumerate(chain):
        if i == 0:
            continue
        dec = sel.get('decision') or {}
        eligible = positive = False
        for j in range(i):
            anchor = chain[j]['strategy']
            departed = any(k in range(j + 1, i)
                           and chain[k]['strategy'] != anchor
                           and c08_edge_verdict(chain[k - 1], chain[k]) != 'UNKNOWN'
                           for k in range(j + 1, i))
            if not departed:
                continue
            if dec.get('return_of') == anchor:
                eligible = positive = True
            elif dec.get('non_return_of') == anchor:
                eligible = True
        if not eligible or c08_edge_verdict(chain[i - 1], sel) == 'UNKNOWN':
            excluded += 1
        else:
            d += 1
            n += positive
    return n, d, excluded


def c08_inferred_metrics(comparisons):
    """D_inf/N_inf under ONE fixed labeler revision + feature basis; returns
    None when the cohort/revision/feature basis is not actually fixed."""
    if not comparisons:
        return None
    fixed = (len({c['labeler_revision'] for c in comparisons}) == 1
             and len({tuple(sorted(c['features'])) for c in comparisons}) == 1
             and all(c['source_readable'] for c in comparisons))
    if not fixed:
        return None
    eligible = [c for c in comparisons if c['coverage_complete']]
    return sum(c['label'] == 'PIVOT' for c in eligible), len(eligible)


def c08_pool(*_metrics):
    """OBSERVED and INFERRED lanes, different labeler revisions, incomparable
    scopes or coverage are never pooled into one Pivot/Revisit fraction."""
    return 'NOT_COMPARABLE'


def c08_public_projection(claim, *, clearance, reader_supports):
    """Optional cleared public projection of an analytical claim: withhold any
    incompatible projection instead of inventing properties or zero."""
    if claim.get('ungraded') or claim.get('owner_accepted') is not True:
        return 'WITHHELD'
    if clearance not in ('PUBLISHABLE',):
        return 'WITHHELD'
    if not reader_supports:
        return 'UNSUPPORTED_READER'
    return 'PUBLISHED_BOUNDED'


# ---------------------------------------------------------------------------
# C10 source-only oracle (GAIP §16.6-16.7 dependent requalification).
# ---------------------------------------------------------------------------
def c10_dependent_requalification(premise_status, *, relies):
    """A verified invalidating notice withholds only NEW decisions actually
    reliant on that premise; a DISPUTE (same-owner or foreign) never withholds
    by itself; unrelated qualified decisions stay unaffected."""
    if not relies:
        return 'PROCEED_UNAFFECTED'
    return {'VERIFIED_CURRENT': 'PROCEED_OWNER_DECISION',
            'VERIFIED_REVOKED_OR_STALE': 'WITHHOLD_PENDING_REQUALIFICATION',
            'DISPUTED': 'PROCEED_UNAFFECTED',
            'UNVERIFIABLE_OR_PARTIAL': 'UNKNOWN_FOR_THIS_CONCLUSION'}[premise_status]


NATIVE_KINDS = ('pull_request', 'issue', 'review', 'ci_run')


def c10_native_dependent_inference(native, *, owner_witness, material_use,
                                   readback_complete):
    """A native GitHub object qualifies a NEW dependent inference by its own
    identity contract (no Report ID needed) only with owner, witnessed
    snapshot/currentness, complete scoped readback AND a consumer-local
    material-use edge; existence/citation alone is not consumption."""
    if (native['kind'] not in NATIVE_KINDS or 'report_id' in native
            or not owner_witness or not native.get('snapshot') or not readback_complete):
        return 'UNKNOWN'
    if not material_use:
        return 'UNKNOWN'
    return 'QUALIFIED_WITHOUT_REPORT_ID'


def c10_readback_verdict(pages):
    """Complete terminal readback may qualify as CURRENT; any partial/error
    collection is UNKNOWN, never clean absence."""
    return 'CURRENT_READBACK' if collection_complete(pages) else 'UNKNOWN'


def c10_prospective_boundary(history, premise_status, *, reliant, unrelated):
    """Requalification is prospective and dependency-bounded: historical
    BUILD/Host receipts are immutable, only new reliant selections are
    withheld, unrelated qualified work proceeds, and a retroactive undo
    request cannot rewrite history."""
    receipts = copy.deepcopy(history)
    if premise_status == 'VERIFIED_REVOKED_OR_STALE' and reliant:
        reliant_outcome = 'WITHHOLD_PENDING_REQUALIFICATION'
    elif premise_status == 'VERIFIED_REVOKED_OR_STALE':
        reliant_outcome = 'WITHHOLD_PENDING_REQUALIFICATION'
    else:
        reliant_outcome = 'PROCEED_OWNER_DECISION'
    return {'receipts': receipts, 'history_unchanged': receipts == history,
            'reliant': reliant_outcome,
            'unrelated': 'PROCEED_UNAFFECTED' if unrelated['qualified'] else 'ABSTAIN',
            'retroactive_undo': 'IMMUTABLE'}


# ---------------------------------------------------------------------------
# C03/C04/C06/C07/C09/C11+C12 source-only oracles.
# ---------------------------------------------------------------------------
def c03_act_admission(claim, capability, credential, effect, ledger):
    """Pre-effect admission only: ACT needs a current claim whose write-set
    covers the effect, the named capability, a valid credential and a
    confirmed-safe effect contract; unclear obligation or lost ACK/503 is
    ABSTAIN/RECONCILE with no unauthorized effect or replay. A refusal after
    the effect already happened is UNAUTHORIZED_EFFECT, not abstention."""
    if effect.get('done') and not effect.get('pre_admitted'):
        ledger.append('UNAUTHORIZED_EFFECT')
        return 'UNAUTHORIZED_EFFECT'
    if not claim.get('current'):
        return 'ABSTAIN_CLAIM_NOT_CURRENT'
    if not set(effect['write_set']) <= set(claim['write_set']):
        return 'ABSTAIN_SCOPE'
    if effect['capability'] not in capability:
        return 'ABSTAIN_CAPABILITY'
    if credential.get('state') != 'VALID':
        return 'ABSTAIN_CREDENTIAL'
    if effect.get('ack') == 'LOST':
        if 'dispatch:' + effect['id'] in ledger:
            return 'RECONCILE_NO_REPLAY'
        ledger.append('dispatch:' + effect['id'])
        return 'RECONCILE_NO_REPLAY'
    if effect['safety'] != 'CONFIRMED_SAFE':
        return 'ABSTAIN_EFFECT_NOT_CONFIRMED_SAFE'
    ledger.append('effect:' + effect['id'])
    return 'ACT'


def c04_integration_verdict(tasks, obligations, *, final_sha, validated_shas,
                            hidden_pack=None):
    """Cumulative multi-target verification: both source targets pass locally
    AND previously-active obligations hold at the final current SHA. A stale
    PASS (SHA drift after validation), a failing cross-target obligation, or
    any result that depends on hidden-oracle contents is never a PASS; the
    verdict function takes no hidden-oracle input and exposes none."""
    verdict = _c04_public_verdict(tasks, obligations, final_sha=final_sha,
                                  validated_shas=validated_shas)
    if hidden_pack is not None:
        without = _c04_public_verdict(tasks, obligations, final_sha=final_sha,
                                      validated_shas=validated_shas)
        if verdict != without:
            return {'verdict': 'FAIL_ORACLE_LEAK'}
    return verdict


def _c04_public_verdict(tasks, obligations, *, final_sha, validated_shas):
    if any(final_sha != sha for sha in validated_shas):
        return {'verdict': 'FAIL_STALE_PASS'}
    if not all(t['local_pass'] for t in tasks):
        return {'verdict': 'FAIL_LOCAL'}
    failed = [o['id'] for o in obligations if not o['holds'](final_sha)]
    if failed:
        return {'verdict': 'FAIL_INTEGRATION', 'failed_obligations': failed}
    return {'verdict': 'PASS_CUMULATIVE', 'failed_obligations': []}


def c06_parallel_admission(claims, *, current_generation):
    """Disjoint protected keys with no contract collision admit genuine
    parallel work; stale generation, overlapping protected keys, incompatible
    shared-ABI versions or a shared generated index never silently merge."""
    admitted, rejected = [], []
    for claim in claims:
        if claim['generation'] != current_generation:
            rejected.append({'claim': claim['id'], 'reason': 'STALE_GENERATION'})
    live = [c for c in claims if c['generation'] == current_generation]
    for i, a in enumerate(live):
        for b in live[i + 1:]:
            if set(a['paths']) & set(b['paths']):
                rejected.append({'claim': b['id'], 'reason': 'PROTECTED_KEY_OVERLAP'})
            elif (a.get('abi') and b.get('abi')
                  and a['abi']['interface'] == b['abi']['interface']
                  and a['abi']['version'] != b['abi']['version']):
                rejected.append({'claim': b['id'], 'reason': 'CONTRACT_COLLISION'})
            elif (a.get('generated_index') and a.get('generated_index') == b.get('generated_index')):
                rejected.append({'claim': b['id'], 'reason': 'GENERATED_INDEX_OVERLAP'})
    admitted = [c['id'] for c in live
                if c['id'] not in {r['claim'] for r in rejected}]
    return {'admitted': admitted, 'rejected': rejected}


def c07_trial_qualification(trial):
    """A harness/Skill trial is comparable only with matched baseline/policy/
    model/environment/verifier pins and an independently witnessed clean
    holdout; training-only gains, hidden-oracle access, contamination or
    unmeasured regressions never promote."""
    pins = ('baseline_ref', 'policy_ref', 'model_ref', 'environment_ref', 'verifier_ref')
    if any(not trial.get(p) for p in pins):
        return 'NOT_COMPARABLE'
    if trial['verifier_ref'] == trial.get('training_oracle_ref'):
        return 'ORACLE_NOT_INDEPENDENT'
    if set(trial['holdout_items']) & set(trial['training_items']):
        return 'CONTAMINATED_HOLDOUT'
    if not trial.get('holdout_independent_witness'):
        return 'HOLDOUT_NOT_INDEPENDENT'
    if not trial.get('regression_suite_executed'):
        return 'REGRESSION_UNMEASURED'
    return 'COMPARABLE_WITH_COVERAGE'


def c09_feedback_chain(steps):
    """PRESENTED -> APPLIED -> INDEPENDENTLY_CHECKED each need their own
    source-qualified receipt; a phase never proves the next, and a transport
    login is neither an Agent identity nor an effect authority."""
    phase = None
    for step in steps:
        kind = step['receipt']['kind']
        if phase is None:
            if kind == 'PRESENTED' and step['receipt'].get('owner_witness'):
                phase = 'PRESENTED'
            continue
        if phase == 'PRESENTED' and kind == 'APPLIED':
            if step['receipt'].get('operator_id') and step['operator_id'] == step['receipt']['operator_id'] \
                    and step['receipt'].get('transport_actor') != step['receipt']['operator_id']:
                phase = 'APPLIED'
        elif phase == 'APPLIED' and kind == 'INDEPENDENTLY_CHECKED':
            if step['receipt'].get('verifier_ref') and step['receipt'].get('owner_witness') \
                    and step['receipt'].get('verifier_operator') != step['receipt'].get('applier_operator'):
                phase = 'INDEPENDENTLY_CHECKED'
    return phase or 'UNQUALIFIED'


def c1112_public_summary(reconciled, *, clearance, route):
    """A bounded public metric summary needs a supported reader path, a
    comparable reconciled basis and publishable clearance; a guessed private
    provider route is withheld, never guessed into comparability."""
    if reconciled['status'] != 'COMPARABLE_OBSERVATION':
        return 'WITHHELD_' + reconciled['status']
    if clearance.get('classification') != 'PUBLISHABLE':
        return 'WITHHELD_PRIVACY'
    if route['basis'] == 'GUESSED':
        return 'WITHHELD_ROUTE'
    return 'PUBLISHED_BOUNDED'


# ---------------------------------------------------------------------------
# Local source-only fixture builders (data only; no normative logic here).
# ---------------------------------------------------------------------------
FIX = HERE / 'fixtures/v415'


def record(name='summary'):
    return json.loads((FIX / (name + '.json')).read_text(encoding='utf8'))


def item(r=None, number=123):
    r = record() if r is None else copy.deepcopy(r)
    issue = r['data']['subject']['issue_ref']
    return {'record': r, 'id': number,
            'url': issue + '#issuecomment-' + str(number),
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


def selection(sid, strategy, occurrence, *, causal=True, decision=None):
    return {'id': sid, 'strategy': strategy, 'occurrence': occurrence,
            'causal': causal, 'decision': decision}


def owner_decision(prior, current, changed=True, **extra):
    d = {'accepted': True, 'covers': (prior, current), 'changed': changed}
    d.update(extra)
    return d


class G01_C08_ObservedTrajectory(unittest.TestCase):
    def test_owner_qualified_a_b_a_prime_yields_pivot_2_2_and_revisit_1_1(self):
        a = selection('A', 'strategy:A', 'occ:A')
        b = selection('B', 'strategy:B', 'occ:B',
                      decision=owner_decision('strategy:A', 'strategy:B'))
        a2 = selection("A'", 'strategy:A', "occ:A'",
                       decision=owner_decision('strategy:B', 'strategy:A',
                                               return_of='strategy:A'))
        self.assertEqual(c08_pivot_metrics([a, b, a2]), (2, 2, 0))
        # (N, D)=(1, 1); the excluded entry is B: before A' it has no earlier
        # witnessed visit+departure, so it is no Revisit opportunity at all.
        self.assertEqual(c08_revisit_metrics([a, b, a2]), (1, 1, 1))
        # A later eligible selection with a witnessed departure and an owner
        # proven NON-return is a legitimate Revisit-negative 0/1 entry.
        c = selection('C', 'strategy:C', 'occ:C',
                      decision=owner_decision('strategy:A', 'strategy:C',
                                              non_return_of='strategy:B'))
        self.assertEqual(c08_pivot_metrics([a, b, a2, c]), (3, 3, 0))
        self.assertEqual(c08_revisit_metrics([a, b, a2, c]), (1, 2, 1))
        # An observed unchanged strategy on a qualified pivot opportunity is
        # a real 0/1, not UNKNOWN.
        a3 = selection('A3', 'strategy:A', 'occ:A3',
                       decision=owner_decision('strategy:A', 'strategy:A',
                                               changed=False))
        self.assertEqual(c08_pivot_metrics([a, a3]), (0, 1, 0))

    def test_forbidden_mere_rollback_string_match_or_missing_middle_is_unknown(self):
        a = selection('A', 'strategy:A', 'occ:A')
        b = selection('B', 'strategy:B', 'occ:B',
                      decision=owner_decision('strategy:A', 'strategy:B'))
        # Mere code rollback: bytes/strategy name return without a witnessed
        # owner-equivalence decision - no observed Revisit, just UNKNOWN.
        rollback = selection("A'", 'strategy:A', "occ:A'")
        n, d, excluded = c08_revisit_metrics([a, b, rollback])
        self.assertEqual((n, d, excluded > 0), (0, 0, True))
        # Missing middle state breaks the causal chain: UNKNOWN, not 0/1.
        broken = selection("A'", 'strategy:A', "occ:A'",
                           causal=False,
                           decision=owner_decision('strategy:B', 'strategy:A',
                                                   return_of='strategy:A'))
        self.assertEqual(c08_pivot_metrics([a, b, broken])[2], 1)
        self.assertEqual(c08_revisit_metrics([a, b, broken])[2], 2)
        # The first A->B selection is not a Revisit denominator entry at all.
        self.assertEqual(c08_revisit_metrics([a, b]), (0, 0, 1))


class G02_C08_InferredLane(unittest.TestCase):
    def comparisons(self):
        return [{'labeler_revision': 'labeler:v7', 'features': ('diff', 'refs'),
                 'source_readable': True, 'coverage_complete': True,
                 'label': 'PIVOT'},
                {'labeler_revision': 'labeler:v7', 'features': ('diff', 'refs'),
                 'source_readable': True, 'coverage_complete': True,
                 'label': 'KEEP'}]

    def test_fixed_labeler_revision_yields_distinct_inferred_diagnostic(self):
        self.assertEqual(c08_inferred_metrics(self.comparisons()), (1, 2))

    def test_forbidden_label_or_self_report_cannot_promote_or_pool(self):
        a = selection('A', 'strategy:A', 'occ:A')
        b = selection('B', 'strategy:B', 'occ:B',
                      decision={'accepted': False, 'covers': ('strategy:A', 'strategy:B'),
                                'changed': True})
        # Classifier-positive labels and an LLM/self-reported intent summary
        # never move the OBSERVED lane: the edge stays UNKNOWN.
        self.assertEqual(c08_pivot_metrics([a, b]), (0, 0, 1))
        mixed = self.comparisons() + [{'labeler_revision': 'labeler:v8',
                                       'features': ('diff', 'refs'),
                                       'source_readable': True,
                                       'coverage_complete': True, 'label': 'PIVOT'}]
        self.assertIsNone(c08_inferred_metrics(mixed))
        self.assertIsNone(c08_inferred_metrics([]))
        self.assertEqual(c08_pool(c08_pivot_metrics([a, b]),
                                  c08_inferred_metrics(self.comparisons())),
                         'NOT_COMPARABLE')


class G03_C08_OccurrenceDedup(unittest.TestCase):
    def chain(self):
        a = selection('A', 'strategy:A', 'occ:A')
        b = selection('B', 'strategy:B', 'occ:B',
                      decision=owner_decision('strategy:A', 'strategy:B'))
        return a, b

    def test_duplicate_delivery_and_late_copy_count_once(self):
        a, b = self.chain()
        late = selection('B', 'strategy:B', 'occ:B',
                         decision=owner_decision('strategy:A', 'strategy:B'))
        corrected = selection('B', 'strategy:B', 'occ:B',
                              decision=owner_decision('strategy:A', 'strategy:B'))
        self.assertEqual(c08_pivot_metrics([a, b, late, corrected]), (1, 1, 0))
        self.assertEqual(c08_pivot_metrics([a, b]), (1, 1, 0))

    def test_distinct_selected_retry_stays_its_own_opportunity(self):
        a, b = self.chain()
        retry = selection('B2', 'strategy:B2', 'occ:B2-retry',
                          decision=owner_decision('strategy:B', 'strategy:B2'))
        self.assertEqual(c08_pivot_metrics([a, b, retry]), (2, 2, 0))

    def test_forbidden_unordered_branches_and_unknown_excluded_both(self):
        a, b = self.chain()
        branch1 = selection('X', 'strategy:X', 'occ:X', causal=False)
        branch2 = selection('Y', 'strategy:Y', 'occ:Y', causal=False)
        n, d, excluded = c08_pivot_metrics([a, branch1, branch2])
        self.assertEqual((n, d), (0, 0))
        self.assertEqual(excluded, 2)
        n, d, excluded = c08_pivot_metrics([a, b, branch1])
        self.assertEqual((n, d, excluded), (1, 1, 1))
        rn, rd, rexcluded = c08_revisit_metrics([a, b, branch1])
        self.assertEqual((rn, rd, rexcluded), (0, 0, 2))


class G04_C08_PublicProjection(unittest.TestCase):
    def test_cleared_owner_supported_projection_publishes_bounded(self):
        claim = {'owner_accepted': True, 'ungraded': False}
        self.assertEqual(c08_public_projection(
            claim, clearance='PUBLISHABLE', reader_supports=True),
            'PUBLISHED_BOUNDED')

    def test_forbidden_private_ungraded_or_unsupported_reader_withheld(self):
        claim = {'owner_accepted': True, 'ungraded': False}
        for clearance in ('PROJECT_PRIVATE', 'RESTRICTED'):
            self.assertEqual(c08_public_projection(
                claim, clearance=clearance, reader_supports=True), 'WITHHELD')
        self.assertEqual(c08_public_projection(
            {'owner_accepted': True, 'ungraded': True}, clearance='PUBLISHABLE',
            reader_supports=True), 'WITHHELD')
        self.assertEqual(c08_public_projection(
            {'owner_accepted': False, 'ungraded': False}, clearance='PUBLISHABLE',
            reader_supports=True), 'WITHHELD')
        # A v4-only reader of a v5 report is UNSUPPORTED, never a zero/absence
        # (reused frozen-schema reader bridge, unchanged).
        with self.assertRaisesRegex(wire.ContractError, 'UNSUPPORTED_SCHEMA'):
            t03.reader_disposition(t03.v5(), 'v4.15')
        page = [{'cursor': None, 'status': 200, 'comments': [t03.source_comment(t03.v5())],
                 'next': None}]
        self.assertEqual(wire.inspect_supplied_issue_pages(
            page, effective_pin='v4.15')['statuses'], ['UNSUPPORTED'])


class G05_C10_RevokeVsDispute(unittest.TestCase):
    def test_aligned_revoke_invalidates_dispute_does_not(self):
        # Reused unchanged: aligned REVOKE invalidates its target; DISPUTE is
        # a non-revoking notice (test_v415_consumer.CorrectionBoundary).
        self.assertEqual(apply_notice(), 'TARGET_INVALIDATED')
        n, _ = aligned_notice()
        n['data']['notice'] = 'DISPUTE'
        self.assertEqual(apply_notice(notice=n), 'DISPUTED')

    def test_future_material_dependency_gating_and_unaffected(self):
        # NEW: only NEW materially reliant decisions are gated by a verified
        # revocation; DISPUTE withholds nothing; unrelated work proceeds.
        self.assertEqual(c10_dependent_requalification(
            'VERIFIED_REVOKED_OR_STALE', relies=True),
            'WITHHOLD_PENDING_REQUALIFICATION')
        self.assertEqual(c10_dependent_requalification(
            'DISPUTED', relies=True), 'PROCEED_UNAFFECTED')
        self.assertEqual(c10_dependent_requalification(
            'VERIFIED_CURRENT', relies=True), 'PROCEED_OWNER_DECISION')
        self.assertEqual(c10_dependent_requalification(
            'UNVERIFIABLE_OR_PARTIAL', relies=True), 'UNKNOWN_FOR_THIS_CONCLUSION')
        for status in ('VERIFIED_REVOKED_OR_STALE', 'DISPUTED',
                       'UNVERIFIABLE_OR_PARTIAL'):
            self.assertEqual(c10_dependent_requalification(status, relies=False),
                             'PROCEED_UNAFFECTED')


class G06_C10_NativeVsReport(unittest.TestCase):
    def native(self):
        return {'kind': 'pull_request', 'repo': 'kaicreator-mm/ai-development-standard',
                'native_id': 1309, 'snapshot': 'sha256:' + 'a' * 64}

    def test_native_with_witnessed_material_use_qualifies_without_report_id(self):
        self.assertEqual(c10_native_dependent_inference(
            self.native(), owner_witness=True, material_use=True,
            readback_complete=True), 'QUALIFIED_WITHOUT_REPORT_ID')

    def test_forbidden_no_consumption_edge_or_fabricated_report_fields(self):
        self.assertEqual(c10_native_dependent_inference(
            self.native(), owner_witness=True, material_use=False,
            readback_complete=True), 'UNKNOWN')
        self.assertEqual(c10_native_dependent_inference(
            self.native(), owner_witness=False, material_use=True,
            readback_complete=True), 'UNKNOWN')
        self.assertEqual(c10_native_dependent_inference(
            self.native(), owner_witness=True, material_use=True,
            readback_complete=False), 'UNKNOWN')
        fabricated = copy.deepcopy(self.native())
        fabricated['report_id'] = 'report:invented'
        self.assertEqual(c10_native_dependent_inference(
            fabricated, owner_witness=True, material_use=True,
            readback_complete=True), 'UNKNOWN')
        # A fake v4 Report envelope built from a native PR fails the frozen
        # schema before any data use.
        fake = {'schema': 'ads/github/v4', 'kind': 'report',
                'data': {'report_id': 'report:invented'}}
        with self.assertRaises(wire.ContractError):
            wire.validate_record(fake)
        # Reused unchanged: same-comment identity collisions stay CONFLICT.
        a, b = item(), item()
        b['record']['data']['report_id'] = 'changed-id'
        self.assertEqual(read([a, b]), ['CONFLICT', 'CONFLICT'])


class G07_C10_StrictProfilesAndPartialRead(unittest.TestCase):
    def test_v4_8key_target_valid_v5_14key_target_valid(self):
        v4corr, _ = aligned_notice()
        wire.validate_record(v4corr)
        v5corr = t03.v5('correction')
        wire.validate_record(v5corr)
        self.assertEqual(set(v5corr['data']['target']) -
                         set(v4corr['data']['target']),
                         {'repository', 'comment_id', 'ads_profile', 'attempt_ref',
                          'target_source_status', 'target_source_sha'})

    def test_forbidden_v5_only_key_in_v4_and_missing_v5_key(self):
        v4corr, _ = aligned_notice()
        v4corr['data']['target']['comment_id'] = 123
        with self.assertRaises(wire.ContractError):
            wire.validate_record(v4corr)
        v5corr = t03.v5('correction')
        del v5corr['data']['target']['target_source_sha']
        with self.assertRaises(wire.ContractError):
            wire.validate_record(v5corr)
        # Wrong digest stays DISPUTED, not clean cancellation (reused oracle).
        n, _ = aligned_notice()
        n['data']['target']['data_digest'] = '0' * 64
        self.assertEqual(apply_notice(notice=n), 'DISPUTED')

    def test_forbidden_partial_pagination_is_unknown_not_absence(self):
        done = {'cursor': None, 'status': 200, 'items': [], 'next': None}
        self.assertEqual(c10_readback_verdict([done]), 'CURRENT_READBACK')
        for pages in ([{'cursor': None, 'status': 200, 'items': [], 'next': 'c2'}],
                      [{'cursor': None, 'status': 403, 'rate_limited': True,
                        'within_budget': True, 'wait_respected': False}, done],
                      [{'cursor': None, 'status': 429, 'within_budget': True}, done]):
            self.assertEqual(c10_readback_verdict(pages), 'UNKNOWN')


class G08_C10_HistoricalImmutable(unittest.TestCase):
    def history(self):
        return [{'kind': 'BUILD', 'ref': 'build:' + 'b' * 40, 'accepted': True},
                {'kind': 'HOST_EFFECT', 'host': 'K', 'ref': 'effect:1',
                 'accepted': True}]

    def test_verified_revoke_gates_only_future_reliant_choices(self):
        out = c10_prospective_boundary(self.history(), 'VERIFIED_REVOKED_OR_STALE',
                                       reliant=True, unrelated={'qualified': True})
        self.assertEqual(out['reliant'], 'WITHHOLD_PENDING_REQUALIFICATION')
        self.assertEqual(out['unrelated'], 'PROCEED_UNAFFECTED')
        self.assertTrue(out['history_unchanged'])
        self.assertEqual(out['retroactive_undo'], 'IMMUTABLE')

    def test_forbidden_retroactive_undo_and_global_block(self):
        out = c10_prospective_boundary(self.history(), 'VERIFIED_REVOKED_OR_STALE',
                                       reliant=False, unrelated={'qualified': True})
        self.assertEqual(out['reliant'], 'WITHHOLD_PENDING_REQUALIFICATION')
        self.assertEqual(out['unrelated'], 'PROCEED_UNAFFECTED')
        current = c10_prospective_boundary(self.history(), 'VERIFIED_CURRENT',
                                           reliant=True, unrelated={'qualified': True})
        self.assertEqual(current['reliant'], 'PROCEED_OWNER_DECISION')
        self.assertTrue(current['history_unchanged'])
        # Reused unchanged: a differing publisher build is UNKNOWN witness.
        self.assertEqual(downstream_witness(
            reader_build='a' * 40, publisher_build='b' * 40, actual_grants=True,
            effective_egress=True, real_readback=True), 'UNKNOWN')


class G09_C03_ActAbstain(unittest.TestCase):
    def claim(self):
        return {'current': True, 'write_set': ['src/a.py', 'src/b.py']}

    def effect(self, **extra):
        e = {'id': 'e1', 'write_set': ['src/a.py'], 'capability': 'deploy',
             'safety': 'CONFIRMED_SAFE', 'done': False, 'pre_admitted': False}
        e.update(extra)
        return e

    def test_fully_authorized_confirmed_safe_act(self):
        ledger = []
        self.assertEqual(c03_act_admission(self.claim(), {'deploy': True},
                                           {'state': 'VALID'}, self.effect(),
                                           ledger), 'ACT')
        self.assertEqual(ledger, ['effect:e1'])

    def test_forbidden_missing_scope_capability_credential_abstain_before_effect(self):
        ledger = []
        cases = [(self.claim(), {'deploy': True}, {'state': 'VALID'},
                  self.effect(write_set=['src/a.py', 'src/c.py']), 'ABSTAIN_SCOPE'),
                 (self.claim(), {}, {'state': 'VALID'}, self.effect(),
                  'ABSTAIN_CAPABILITY'),
                 (self.claim(), {'deploy': True}, {'state': 'REVOKED'}, self.effect(),
                  'ABSTAIN_CREDENTIAL'),
                 (self.claim(), {'deploy': True}, {'state': 'VALID'},
                  self.effect(safety='UNCONFIRMED'), 'ABSTAIN_EFFECT_NOT_CONFIRMED_SAFE'),
                 ({'current': False, 'write_set': ['src/a.py']}, {'deploy': True},
                  {'state': 'VALID'}, self.effect(), 'ABSTAIN_CLAIM_NOT_CURRENT')]
        for claim, cap, cred, effect, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(c03_act_admission(claim, cap, cred, effect, ledger),
                                 expected)
        self.assertEqual(ledger, [])

    def test_lost_ack_503_reconciles_without_unauthorized_replay(self):
        ledger = []
        self.assertEqual(c03_act_admission(self.claim(), {'deploy': True},
                                           {'state': 'VALID'},
                                           self.effect(ack='LOST'), ledger),
                         'RECONCILE_NO_REPLAY')
        self.assertEqual(c03_act_admission(self.claim(), {'deploy': True},
                                           {'state': 'VALID'},
                                           self.effect(ack='LOST'), ledger),
                         'RECONCILE_NO_REPLAY')
        self.assertEqual(ledger, ['dispatch:e1'])
        # Post-hoc refusal after an unauthorized effect is not abstention.
        ledger2 = []
        self.assertEqual(c03_act_admission(self.claim(), {'deploy': True},
                                           {'state': 'VALID'},
                                           self.effect(done=True), ledger2),
                         'UNAUTHORIZED_EFFECT')
        self.assertEqual(ledger2, ['UNAUTHORIZED_EFFECT'])


class G10_C04_CumulativeAndHiddenOracle(unittest.TestCase):
    def tasks(self):
        return [{'id': 't1', 'local_pass': True}, {'id': 't2', 'local_pass': True}]

    def obligations(self, cross_target_holds=True):
        return [{'id': 'shared-contract', 'holds': lambda sha: cross_target_holds}]

    def test_two_local_passes_plus_integration_obligations_pass(self):
        out = c04_integration_verdict(self.tasks(), self.obligations(),
                                      final_sha='f' * 40,
                                      validated_shas=['f' * 40])
        self.assertEqual(out['verdict'], 'PASS_CUMULATIVE')

    def test_forbidden_integration_gap_drift_and_oracle_leak(self):
        out = c04_integration_verdict(self.tasks(), self.obligations(False),
                                      final_sha='f' * 40, validated_shas=['f' * 40])
        self.assertEqual(out['verdict'], 'FAIL_INTEGRATION')
        out = c04_integration_verdict(self.tasks(), self.obligations(),
                                      final_sha='f' * 40, validated_shas=['e' * 40])
        self.assertEqual(out['verdict'], 'FAIL_STALE_PASS')
        out = c04_integration_verdict(self.tasks(), self.obligations(),
                                      final_sha='f' * 40, validated_shas=['f' * 40],
                                      hidden_pack={'secret_expected': 'x'})
        self.assertEqual(out['verdict'], 'PASS_CUMULATIVE')
        # Non-disclosure witness: mutating the hidden pack cannot change the
        # verdict, and no hidden payload appears in the verdict.
        other = c04_integration_verdict(self.tasks(), self.obligations(),
                                        final_sha='f' * 40,
                                        validated_shas=['f' * 40],
                                        hidden_pack={'secret_expected': 'y'})
        self.assertEqual(out, other)
        self.assertNotIn('secret_expected', json.dumps(out))


class G11_C06_ParallelClaims(unittest.TestCase):
    def test_disjoint_claims_without_contract_collision_admit_parallel(self):
        out = c06_parallel_admission(
            [{'id': 't1', 'paths': ['src/a.py'], 'abi': None, 'generation': 2},
             {'id': 't2', 'paths': ['src/b.py'], 'abi': None, 'generation': 2}],
            current_generation=2)
        self.assertEqual(out['admitted'], ['t1', 't2'])
        self.assertEqual(out['rejected'], [])

    def test_forbidden_abi_collision_stale_generation_and_index_overlap(self):
        out = c06_parallel_admission(
            [{'id': 't1', 'paths': ['src/a.py'],
              'abi': {'interface': 'Codec', 'version': 2}, 'generation': 2},
             {'id': 't2', 'paths': ['src/b.py'],
              'abi': {'interface': 'Codec', 'version': 3}, 'generation': 2}],
            current_generation=2)
        self.assertEqual(out['admitted'], ['t1'])
        self.assertEqual(out['rejected'],
                         [{'claim': 't2', 'reason': 'CONTRACT_COLLISION'}])
        out = c06_parallel_admission(
            [{'id': 't1', 'paths': ['src/a.py'], 'abi': None, 'generation': 2},
             {'id': 't2', 'paths': ['src/b.py'], 'abi': None, 'generation': 1}],
            current_generation=2)
        self.assertEqual(out['rejected'],
                         [{'claim': 't2', 'reason': 'STALE_GENERATION'}])
        out = c06_parallel_admission(
            [{'id': 't1', 'paths': ['src/a.py'], 'abi': None, 'generation': 2,
              'generated_index': 'idx/registry.json'},
             {'id': 't2', 'paths': ['src/b.py'], 'abi': None, 'generation': 2,
              'generated_index': 'idx/registry.json'}],
            current_generation=2)
        self.assertEqual(out['admitted'], ['t1'])
        self.assertEqual(out['rejected'],
                         [{'claim': 't2', 'reason': 'GENERATED_INDEX_OVERLAP'}])


class G12_C07_HoldoutQualification(unittest.TestCase):
    def trial(self, **extra):
        t = {'baseline_ref': 'baseline:sha-' + '1' * 8, 'policy_ref': 'policy:v1',
             'model_ref': 'model:m1', 'environment_ref': 'env:e1',
             'verifier_ref': 'verifier:independent',
             'training_items': ['q1', 'q2', 'q3'], 'holdout_items': ['h1', 'h2'],
             'holdout_independent_witness': True, 'regression_suite_executed': True,
             'training_oracle_ref': 'verifier:training'}
        t.update(extra)
        return t

    def test_matched_pinned_trial_with_clean_holdout_comparable(self):
        self.assertEqual(c07_trial_qualification(self.trial()),
                         'COMPARABLE_WITH_COVERAGE')

    def test_forbidden_contamination_oracle_leak_and_unpinned(self):
        self.assertEqual(c07_trial_qualification(
            self.trial(holdout_items=['h1', 'q1'])), 'CONTAMINATED_HOLDOUT')
        self.assertEqual(c07_trial_qualification(
            self.trial(verifier_ref='verifier:training')), 'ORACLE_NOT_INDEPENDENT')
        self.assertEqual(c07_trial_qualification(
            self.trial(baseline_ref=None)), 'NOT_COMPARABLE')
        self.assertEqual(c07_trial_qualification(
            self.trial(holdout_independent_witness=False)),
            'HOLDOUT_NOT_INDEPENDENT')
        self.assertEqual(c07_trial_qualification(
            self.trial(regression_suite_executed=False)), 'REGRESSION_UNMEASURED')


class G13_C09_FeedbackChain(unittest.TestCase):
    def feedback_record(self):
        return record('feedback')

    def test_reused_report_side_phase_boundaries(self):
        d = self.feedback_record()['data']
        args = dict(build_sha=d['publisher_source_sha'],
                    ads_subject_sha=d['ads_subject_sha'], source_witness=True,
                    phase_witness=True)
        self.assertEqual(feedback_observation(self.feedback_record(), **args),
                         'PRESENTED')
        r = self.feedback_record()
        r['data']['phase'] = 'APPLIED'
        self.assertEqual(feedback_observation(r, **args), 'APPLIED')
        r['data']['phase'] = 'INDEPENDENTLY_CHECKED'
        r['data']['verifier_refs'] = ['github:independent-observation']
        self.assertEqual(feedback_observation(r, **args), 'UNKNOWN')
        self.assertEqual(feedback_observation(r, independent_witness=True, **args),
                         'INDEPENDENTLY_CHECKED')

    def test_source_qualified_chain_presented_applied_independently_checked(self):
        steps = [{'operator_id': 'agent:1', 'receipt': {
            'kind': 'PRESENTED', 'owner_witness': True, 'transport_actor': 'github:shared'}},
            {'operator_id': 'agent:1', 'receipt': {
                'kind': 'APPLIED', 'owner_witness': True,
                'operator_id': 'agent:1', 'transport_actor': 'github:shared'}},
            {'operator_id': 'agent:1', 'receipt': {
                'kind': 'INDEPENDENTLY_CHECKED', 'owner_witness': True,
                'verifier_ref': 'github:independent-observation',
                'verifier_operator': 'agent:2', 'applier_operator': 'agent:1'}}]
        self.assertEqual(c09_feedback_chain(steps), 'INDEPENDENTLY_CHECKED')

    def test_forbidden_phase_skipping_and_transport_login_authority(self):
        presented = [{'operator_id': 'agent:1', 'receipt': {
            'kind': 'PRESENTED', 'owner_witness': True, 'transport_actor': 'github:shared'}}]
        claimed_applied = presented + [{'operator_id': 'agent:1', 'receipt': {
            'kind': 'APPLIED', 'owner_witness': True,
            'operator_id': None, 'transport_actor': 'github:shared'}}]
        # No declared operator identity; the shared transport login cannot be
        # the effect authority, so the chain stalls at PRESENTED.
        self.assertEqual(c09_feedback_chain(claimed_applied), 'PRESENTED')
        applied = presented + [{'operator_id': 'agent:1', 'receipt': {
            'kind': 'APPLIED', 'owner_witness': True,
            'operator_id': 'agent:1', 'transport_actor': 'github:shared'}}]
        # Self-attested "independent" check by the applier never promotes.
        self.assertEqual(c09_feedback_chain(applied + [{'operator_id': 'agent:1', 'receipt': {
            'kind': 'INDEPENDENTLY_CHECKED', 'owner_witness': True,
            'verifier_ref': 'github:self-check', 'verifier_operator': 'agent:1',
            'applier_operator': 'agent:1'}}]), 'APPLIED')
        self.assertEqual(c09_feedback_chain([]), 'UNQUALIFIED')


class G14_C11_C12_ReaderAndMetric(unittest.TestCase):
    def test_supported_reader_path_v5_vs_v4_only(self):
        # Reused unchanged: v4.16 opt-in reader accepts v5 shapes only;
        # a v4-only reader raises UNSUPPORTED_SCHEMA (G04 shows page-level).
        self.assertEqual(t03.reader_disposition(t03.v5(), 'v4.16'), 'V5_SHAPE_ONLY')
        with self.assertRaisesRegex(wire.ContractError, 'UNSUPPORTED_SCHEMA'):
            t03.reader_disposition(t03.v5(), 'v4.15')
        historical = record()
        self.assertEqual(t03.reader_disposition(historical, 'v4.15'),
                         'CURRENT_OBSERVATION')

    def test_dedup_window_and_unknown_attempts_before_comparable(self):
        base = json.loads((HERE / 'fixtures/v416/t02/scenarios.json')
                          .read_text(encoding='utf8'))['cases']
        case = next(c for c in base if c['id'] == 'C02_one_delta')
        self.assertEqual(metric_total(case['rows']),
                         {'status': 'COMPARABLE_OBSERVATION', 'total': '10',
                          'reason': ''})
        replayed = case['rows'] + [copy.deepcopy(case['rows'][0])]
        self.assertEqual(metric_total(replayed)['total'], '10')
        no_attempt = copy.deepcopy(case['rows'])
        del no_attempt[0]['physical_attempt_ref']
        self.assertEqual(metric_total(no_attempt)['status'], 'UNKNOWN')
        mixed_window = case['rows'] + [dict(case['rows'][0],
                                            window_id='interval:B')]
        self.assertEqual(metric_total(mixed_window)['status'], 'UNKNOWN')

    def test_forbidden_estimate_bill_double_count_and_private_route(self):
        base = json.loads((HERE / 'fixtures/v416/t02/scenarios.json')
                          .read_text(encoding='utf8'))['cases']
        overlap = next(c for c in base if c['id'] == 'C05_quote_overlaps_bill')
        self.assertEqual(cost_total(overlap['rows'])['status'], 'COMPARABLE_BILLED')
        estimate_only = next(c for c in base if c['id'] == 'C05_only_estimate')
        self.assertEqual(cost_total(estimate_only['rows'])['status'], 'UNKNOWN')
        comparable = {'status': 'COMPARABLE_OBSERVATION', 'total': '10', 'reason': ''}
        clear = {'classification': 'PUBLISHABLE', 'clearance_ref': 'fixture'}
        self.assertEqual(c1112_public_summary(comparable, clearance=clear,
                                              route={'basis': 'WITNESSED'}),
                         'PUBLISHED_BOUNDED')
        self.assertEqual(c1112_public_summary(comparable, clearance=
                                              {'classification': 'RESTRICTED'},
                                              route={'basis': 'WITNESSED'}),
                         'WITHHELD_PRIVACY')
        self.assertEqual(c1112_public_summary(comparable, clearance=clear,
                                              route={'basis': 'GUESSED'}),
                         'WITHHELD_ROUTE')
        self.assertEqual(c1112_public_summary({'status': 'UNKNOWN', 'total': None,
                                               'reason': 'population_absent'},
                                              clearance=clear,
                                              route={'basis': 'WITNESSED'}),
                         'WITHHELD_UNKNOWN')


if __name__ == '__main__':
    unittest.main()
