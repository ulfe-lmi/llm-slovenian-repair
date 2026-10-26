"""Merged-PR tail publication reconciliation (012-a requirement 2 / A2).

Builds one synthetic post-merge topology: the prior PR was merged at a frozen
head, and one later report commit exists only on the original retained branch.
Recognition requires the explicit order-carried receipt, proven end to end
against local Git and (fake) remote facts; everything else fails closed.
"""
import base64
import copy
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import test_acceptance as base
import oap_cli
from support import *
from oap_core import (MERGED_TAIL_ACCEPTANCE, MERGED_TAIL_CLASSIFICATION,
                      merged_tail_receipt, protocol_state, transition, verify_report)

BRANCH = 'oap/000-synthetic'
NEXT_BRANCH = 'oap/001-synthetic'
REPORT_REL = 'oap/reports/000-a-synthetic.md'
ORDER_REL = 'oap/orders/000-a-synthetic.md'
NEXT_ORDER_REL = 'oap/orders/001-a-synthetic.md'
API = 'repos/synthetic/project/'


class MergedTail(unittest.TestCase):
    setUp = base.Acceptance.setUp
    tearDown = base.Acceptance.tearDown
    error = base.Acceptance.error
    private = base.Acceptance.private

    # ---- fixture construction ------------------------------------------------

    def report_bytes(self, repo, impl):
        opath = repo / ORDER_REL
        od = read(opath)
        o = validate_order(od, repo, '000-a', ORDER_REL.rsplit('/', 1)[-1])
        r = dict(id='000-a', result='COMPLETE', order_path=ORDER_REL, order_sha256=digest(od),
                 governance=o['governance'], publication_commit='SELF', implementation_head=impl,
                 publication_verified=False, pr_mode='CREATE_NEW_PR', pr=1,
                 pr_url='https://github.com/synthetic/project/pull/1', pr_state='open',
                 branch=BRANCH, base_sha=o['base_sha'], starting_remote_sha=o['base_sha'],
                 no_merge=True, checks=[dict(command='synthetic unit', result='PASSED', sha=impl)],
                 critical_action='NONE',
                 pr_observed_at='2026-09-06T10:00:00+00:00',
                 report_written_at='2026-09-06T10:01:00+00:00')
        for k in ('implementation', 'documentation', 'criteria', 'negative_paths',
                  'boundary_fidelity', 'setup', 'privacy', 'limits', 'human_gates', 'scope'):
            r[k] = 'Synthetic merged-tail fixture observation.'
        return ('# Synthetic report\n\n```oap-report\n' + json.dumps(r, indent=2) + '\n```\n').encode(), r

    def build_merged_tail(self, *, report_impl='I', merge_ref='G',
                          extra_report_file=None, check_sha='auto'):
        """B(main) -> [branch] A -> G(frozen) -> I -> R(report); main merges
        merge_ref (default G) as M; HEAD returns to R on the retained branch.

        Knobs for negative variants: report_impl records a different
        implementation head in the report metadata (local REPORT_PARENT);
        check_sha selects the report check SHA (an existing pre-R commit or a
        syntactically valid nonexistent one); merge_ref selects the commit
        main merges."""
        repo = self.repo
        m, data = order(repo, self.base, '000-a')
        write(repo / ORDER_REL, data)
        write(repo / 'oap/active', '000-a\n')
        git(repo, 'checkout', '-b', BRANCH)
        write(repo / 'work/one.txt', b'synthetic work one\n')
        A = commit(repo, 'Synthetic activation and work')
        write(repo / 'work/frozen.txt', b'synthetic frozen marker\n')
        G = commit(repo, 'Synthetic frozen PR head')
        impl = {'I': None, 'G': G, 'A': A}[report_impl]
        write(repo / 'work/two.txt', b'synthetic implementation bookkeeping\n')
        I = commit(repo, 'Synthetic implementation parent')
        check = {'auto': I, 'A': A, 'G': G, 'I': I, 'bogus': '0' * 40}[check_sha]
        rbytes, rmeta = self.report_bytes(repo, impl or I)
        rmeta['implementation_head'] = impl or I
        rmeta['checks'] = [dict(command='synthetic unit', result='PASSED', sha=check)]
        rbytes = ('# Synthetic report\n\n```oap-report\n' + json.dumps(rmeta, indent=2) + '\n```\n').encode()
        write(repo / REPORT_REL, rbytes)
        if extra_report_file is not None:
            write(repo / extra_report_file, b'synthetic unexpected mutation\n')
        R = commit(repo, 'Synthetic merged-tail report')
        merge = {'G': G, 'A': A, 'I': I}[merge_ref]
        git(repo, 'checkout', 'main')
        git(repo, 'merge', '--no-ff', merge, '-m', 'Synthetic owner merge of frozen head')
        M = git(repo, 'rev-parse', 'HEAD').decode().strip()
        git(repo, 'checkout', BRANCH)
        assert git(repo, 'rev-parse', 'HEAD').decode().strip() == R
        return dict(A=A, G=G, I=I, R=R, M=M,
                    report_sha=digest(rbytes), order_sha=digest(data), rmeta=rmeta,
                    branch_tip=R)

    def receipt(self, ids, **changes):
        r = dict(prior_id='000-a', pr=1, frozen_pr_head=ids['G'], merge_commit=ids['M'],
                 retained_branch=BRANCH, publication_commit=ids['R'],
                 implementation_parent=ids['I'], report_path=REPORT_REL,
                 report_sha256=ids['report_sha'], order_path=ORDER_REL,
                 order_sha256=ids['order_sha'],
                 classification=MERGED_TAIL_CLASSIFICATION, acceptance=MERGED_TAIL_ACCEPTANCE)
        r.update(changes)
        return r

    def fake_pr(self, ids, *, head=None, merged=True, merged_at=True, head_repo='synthetic/project',
                ref=BRANCH, base_ref='main', merge_sha=None):
        return dict(number=1, state='closed' if merged else 'open', merged=merged,
                    merged_at='2026-09-06T10:05:00Z' if merged and merged_at else None,
                    draft=False, created_at='2026-09-06T09:59:00Z',
                    head=dict(sha=head or ids['G'], ref=ref, repo=dict(full_name=head_repo)),
                    base=dict(ref=base_ref, repo=dict(full_name='synthetic/project')),
                    merge_commit_sha=merge_sha or ids['M'])

    def responses(self, ids, *, pr=None, main_tip=None, retained_tip=None,
                  commit_parents=None, commit_files=None, report_content=None,
                  order_content=None, compare_status='identical', main_name='main'):
        repo_r, order_r = read(self.repo / REPORT_REL), read(self.repo / ORDER_REL)
        return {
            API + 'pulls/1': pr or self.fake_pr(ids),
            API + 'branches/' + main_name: {'commit': {'sha': main_tip or ids['M']}},
            API + 'compare/%s...%s' % (ids['M'], main_tip or ids['M']): {'status': compare_status},
            API + 'branches/' + BRANCH.replace('/', '%2F'): {'commit': {'sha': retained_tip or ids['R']}},
            API + 'commits/' + ids['R']: {'parents': [{'sha': p} for p in (commit_parents or [ids['I']])],
                                          'files': [{'filename': f} for f in (commit_files or [REPORT_REL])]},
            API + 'contents/' + REPORT_REL + '?ref=' + ids['R']:
                {'encoding': 'base64', 'content': base64.b64encode(report_content if report_content is not None else repo_r).decode()},
            API + 'contents/' + ORDER_REL + '?ref=' + ids['R']:
                {'encoding': 'base64', 'content': base64.b64encode(order_content if order_content is not None else order_r).decode()},
        }

    def fake_remote(self, ids, **kw):
        remote = FakeGitHub(self.repo)
        for k, v in self.responses(ids, **kw).items():
            rel = k[len(API):]
            if rel.startswith('pulls/'):
                remote.prs[int(rel.rsplit('/', 1)[1])] = v
            else:
                remote.responses[rel] = v
        return remote

    def install_next_order(self, ids, *, with_receipt=True, filename=None, path=None, mutate=None):
        m, data = order(self.repo, ids['M'], '001-a')
        if with_receipt:
            m['merged_tail_recovery'] = self.receipt(ids)
        if mutate is not None:
            mutate(m)
        data = replace_metadata(data, m)
        target = path if path is not None else self.repo / NEXT_ORDER_REL
        if filename is not None and path is None:
            target = self.repo / (filename if '/' in filename else 'oap/orders/' + filename)
        return m, data, write(target, data)

    # ---- focused CLI-boundary regression (first publication deadlock) --------

    def test_publish_dry_run_cli_with_unpublished_receipt_order(self):
        """The not-yet-written source order carries the receipt; the actual
        publish CLI dry run must succeed without the order on disk."""
        ids = self.build_merged_tail()
        m, data, src = self.install_next_order(ids, path=self.root / (NEXT_ORDER_REL.rsplit('/', 1)[-1]))
        remote_calls = self.fake_remote(ids)
        fake_gh = write(self.root / 'fake-gh', read(SOURCE / 'oap/tests/fake_gh.py'))
        fake_gh.chmod(0o700)
        responses_file = write(self.root / 'fake-gh-responses.json',
                               (json.dumps(self.responses(ids)) + '\n').encode())
        with patch.dict(os.environ, {'OAP_ROLE': 'strategic', 'FAKE_GH_RESPONSES': str(responses_file)}):
            rc = oap_cli.main(['publish', '--repo-root', str(self.repo), '--source', str(src),
                               '--id', '001-a', '--dry-run', '--repository', 'synthetic/project',
                               '--gh-bin', str(fake_gh), '--accepted-ref', self.base])
        self.assertEqual(rc, 0)
        # The order was never written by a dry run.
        self.assertFalse((self.repo / NEXT_ORDER_REL).exists())
        self.assertEqual(read(self.repo / 'oap/active'), b'000-a\n')

    # ---- verify_report merged-tail negative boundaries (A2) ------------------

    def test_receipt_pr_mismatch_fails_closed(self):
        """A receipt pinning a different PR than the original validated
        report must not authorize the merged-tail recognition."""
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids)
        bad = self.receipt(ids, pr=2)
        self.error('MERGED_TAIL_RECEIPT_PR_MISMATCH',
                   verify_report, self.repo, '000-a', remote=remote, receipt=bad)

    def test_receipt_branch_mismatch_fails_closed(self):
        """A receipt pinning a different retained branch than the original
        validated report must not authorize the merged-tail recognition."""
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids)
        bad = self.receipt(ids, retained_branch='oap/forged-branch')
        self.error('MERGED_TAIL_RECEIPT_BRANCH_MISMATCH',
                   verify_report, self.repo, '000-a', remote=remote, receipt=bad)

    def test_no_receipt_fails_closed(self):
        """Without any explicit receipt the frozen-head PR head mismatch is
        not a merged-tail recognition."""
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids)
        self.error('REMOTE_HEAD_MISMATCH', verify_report, self.repo, '000-a', remote=remote)

    def test_forked_head_repository_fails_closed(self):
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids, pr=self.fake_pr(ids, head_repo='fork/project'))
        self.error('MERGED_TAIL_PR_SAME_REPOSITORY',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    def test_unmerged_pr_fails_closed(self):
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids, pr=self.fake_pr(ids, merged=False, merged_at=False))
        self.error('MERGED_TAIL_NOT_MERGED',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    def test_stale_retained_branch_tip_fails_closed(self):
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids, retained_tip=ids['G'])
        self.error('MERGED_TAIL_RETAINED_BRANCH_HEAD',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    def test_wrong_merge_shape_fails_closed(self):
        """The default-branch merge must carry the frozen PR head as its
        second parent; merging an earlier commit is not the proven shape."""
        ids = self.build_merged_tail(merge_ref='A')
        remote = self.fake_remote(ids)
        self.error('MERGED_TAIL_MERGE_SHAPE',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    def test_local_report_parent_gate_precedes_merged_tail(self):
        """A report whose recorded implementation head is not its git parent
        fails the local REPORT_PARENT gate before any merged-tail claim, even
        with a valid receipt present."""
        ids = self.build_merged_tail(report_impl='G')
        remote = self.fake_remote(ids)
        self.error('REPORT_PARENT',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    def test_local_report_only_path_gate_precedes_merged_tail(self):
        ids = self.build_merged_tail(extra_report_file='work/extra.md')
        remote = self.fake_remote(ids)
        self.error('REPORT_ONLY_PATH',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    def test_unobserved_check_sha_fails_closed(self):
        ids = self.build_merged_tail(check_sha='bogus')
        remote = self.fake_remote(ids)
        self.error('UNOBSERVED_CHECK_SHA',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    def test_receipt_implementation_parent_mismatch_fails_closed(self):
        """The receipt's implementation parent must be the report commit's
        actual second-parent-level parent."""
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids)
        bad = self.receipt(ids, implementation_parent=ids['G'])
        self.error('MERGED_TAIL_REPORT_PARENT',
                   verify_report, self.repo, '000-a', remote=remote, receipt=bad)

    def test_receipt_report_hash_mismatch_fails_closed(self):
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids)
        bad = self.receipt(ids, report_sha256='0' * 64)
        self.error('MERGED_TAIL_REPORT_BYTES',
                   verify_report, self.repo, '000-a', remote=remote, receipt=bad)

    def test_receipt_order_hash_mismatch_fails_closed(self):
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids)
        bad = self.receipt(ids, order_sha256='0' * 64)
        self.error('MERGED_TAIL_ORDER_BYTES',
                   verify_report, self.repo, '000-a', remote=remote, receipt=bad)

    def test_order_drift_at_head_fails_closed(self):
        """The original order bytes must survive at the branch head; a later
        order commit (with the worktree restored to the report-era bytes) is
        drift even though the worktree looks clean."""
        ids = self.build_merged_tail()
        order_file = self.repo / ORDER_REL
        original = read(order_file)
        write(order_file, original + b'\n# synthetic post-publication edit\n')
        commit(self.repo, 'Synthetic post-publication order edit')
        write(order_file, original)
        remote = self.fake_remote(ids)
        self.error('MERGED_TAIL_ORDER_DRIFT',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    def test_remote_report_parent_drift_fails_closed(self):
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids, commit_parents=[ids['G']])
        self.error('REMOTE_REPORT_PARENT',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    def test_remote_report_only_path_drift_fails_closed(self):
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids, commit_files=[REPORT_REL, 'work/other.md'])
        self.error('REMOTE_REPORT_ONLY_PATH',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    def test_remote_report_content_drift_fails_closed(self):
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids, report_content=b'# tampered report\n')
        self.error('REMOTE_REPORT_CONTENT',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    def test_remote_order_content_drift_fails_closed(self):
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids, order_content=b'# tampered order\n')
        self.error('REMOTE_ORDER_DRIFT',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    # ---- refresh governance routes merged-tail through the shared verifier --

    def _accept_retained_integration(self, ids, *, commit_order=False):
        """Integrate the retained branch into main after the merged-tail PR
        merge, optionally committing the receipt-carrying next order while
        active remains 000-a; the accepted revision N then carries the report
        commit while the old PR stays frozen (head G, merge M) and the
        retained tip stays R. Returns (accepted_sha, remote)."""
        git(self.repo, 'checkout', 'main')
        git(self.repo, 'merge', '--no-ff', BRANCH, '-m', 'Synthetic owner integration of retained branch')
        if commit_order:
            commit(self.repo, 'Synthetic next order with merged-tail receipt')
        accepted = git(self.repo, 'rev-parse', 'HEAD').decode().strip()
        self.private()
        remote = self.fake_remote(ids, main_tip=accepted, compare_status='ahead')
        return accepted, remote

    def test_refresh_governance_proves_merged_tail_via_shared_verifier(self):
        """Refresh must route the merged-tail prior report through the shared
        verifier's own report-publication identity (explicit receipt-gated
        recognition), not the frozen PR head."""
        from oap_install import refresh_governance
        ids = self.build_merged_tail()
        self.install_next_order(ids)
        accepted, remote = self._accept_retained_integration(ids, commit_order=True)
        result = refresh_governance(self.repo, self.strategy, accepted, remote=remote)
        self.assertEqual(result['result'], 'refreshed')
        self.assertEqual(result['changed'], [])
        # Only the merged-tail proof queries the retained branch head remotely:
        # its presence proves routing went through the shared recognition.
        self.assertIn(('api', 'branches/' + BRANCH.replace('/', '%2F')), remote.calls)
        self.assertIn(('pr', 1), remote.calls)

    def test_refresh_governance_without_receipt_fails_closed(self):
        """Without any order carrying the merged_tail_recovery receipt, refresh
        of a merged-tail prior report must fail closed, not fall back to the
        frozen PR head."""
        from oap_install import refresh_governance
        ids = self.build_merged_tail()
        accepted, remote = self._accept_retained_integration(ids, commit_order=False)
        self.error('REMOTE_HEAD_MISMATCH',
                   refresh_governance, self.repo, self.strategy, accepted, remote=remote)

    def test_refresh_governance_requires_merged_pr(self):
        from oap_install import refresh_governance
        ids = self.build_merged_tail()
        self.install_next_order(ids)
        accepted, remote = self._accept_retained_integration(ids, commit_order=True)
        remote.prs[1] = self.fake_pr(ids, merged=False, merged_at=False)
        self.error('REFRESH_NOT_MERGED',
                   refresh_governance, self.repo, self.strategy, accepted, remote=remote)

    # ---- positive scope, transition and protocol_state surfaces -------------

    def test_verify_report_positive_scope_and_evidence(self):
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids)
        result = verify_report(self.repo, '000-a', remote=remote, receipt=self.receipt(ids))
        self.assertEqual(result['result'], 'verified')
        self.assertEqual(result['scope'], 'merged-tail publication evidence only')
        mt = result['merged_tail']
        self.assertEqual(mt['classification'], MERGED_TAIL_CLASSIFICATION)
        self.assertEqual(mt['acceptance'], MERGED_TAIL_ACCEPTANCE)
        self.assertEqual(mt['pr'], 1)
        self.assertEqual(mt['publication_commit'], ids['R'])
        self.assertEqual(mt['implementation_parent'], ids['I'])
        self.assertEqual(mt['frozen_pr_head'], ids['G'])
        self.assertEqual(mt['merge_commit'], ids['M'])
        self.assertEqual(mt['retained_branch'], BRANCH)
        self.assertEqual(mt['report_path'], REPORT_REL)
        self.assertEqual(mt['default_head'], ids['M'])

    def test_merge_not_on_live_default_fails_closed(self):
        """The proven merge must sit on the live default branch; a remote
        main that never reached it (behind the merge) is not the accepted
        topology. The fake facts stay consistent with the real fixture graph:
        the pre-merge base commit is an ancestor of M, hence 'behind'."""
        ids = self.build_merged_tail()
        remote = self.fake_remote(ids, main_tip=self.base, compare_status='behind')
        self.error('MERGED_TAIL_MERGE_NOT_ON_DEFAULT',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    def test_copied_report_on_different_history_fails_closed(self):
        """Copied report bytes on a different history are not the publication:
        the retained branch head must be the exact publication commit, so an
        empty descendant (same bytes, new history) fails at the tip gate."""
        ids = self.build_merged_tail()
        git(self.repo, 'commit', '--allow-empty', '-m', 'Synthetic copied-history descendant')
        r2 = git(self.repo, 'rev-parse', 'HEAD').decode().strip()
        remote = self.fake_remote(ids, retained_tip=r2)
        self.error('MERGED_TAIL_RETAINED_BRANCH_HEAD',
                   verify_report, self.repo, '000-a', remote=remote, receipt=self.receipt(ids))

    def test_transition_requires_merged_tail_receipt(self):
        """With no receipt in any published order file, the shared verifier's
        own receipt gate dominates: the transition fails closed at the
        recognition boundary, not at a fabricated plain merged-PR path."""
        ids = self.build_merged_tail()
        m, data, _ = self.install_next_order(ids, with_receipt=False)
        new = validate_order(data, self.repo, '001-a', '001-a-synthetic.md')
        remote = self.fake_remote(ids)
        self.error('REMOTE_HEAD_MISMATCH',
                   transition, self.repo, new, remote,
                   new_order_data=data, new_order_path=NEXT_ORDER_REL)

    def test_transition_requires_receipt_on_incoming_order(self):
        """A receipt present in some published order file is not a binding for
        the incoming order: the transition requires the receipt on the
        incoming order itself (or passed explicitly)."""
        ids = self.build_merged_tail()
        self.install_next_order(ids)
        m2, data2 = order(self.repo, ids['M'], '001-a')
        new = validate_order(data2, self.repo, '001-a', '001-a-synthetic.md')
        remote = self.fake_remote(ids)
        self.error('MERGED_TAIL_RECEIPT_REQUIRED',
                   transition, self.repo, new, remote,
                   new_order_data=data2, new_order_path=NEXT_ORDER_REL)

    def test_transition_succeeds_with_proven_receipt(self):
        ids = self.build_merged_tail()
        m, data, _ = self.install_next_order(ids)
        new = validate_order(data, self.repo, '001-a', '001-a-synthetic.md')
        remote = self.fake_remote(ids)
        self.assertIsNone(transition(self.repo, new, remote,
                                     new_order_data=data, new_order_path=NEXT_ORDER_REL,
                                     merged_tail_receipt_data=self.receipt(ids)))

    def test_protocol_state_exposes_publication_scope(self):
        """protocol_state must keep the publication-only scope in its evidence
        instead of discarding it into a generic REVIEW_READY."""
        ids = self.build_merged_tail()
        self.install_next_order(ids)
        remote = self.fake_remote(ids)
        state = protocol_state(self.repo, remote=remote)
        self.assertEqual(state['state'], 'REVIEW_READY')
        self.assertEqual(state['id'], '000-a')
        self.assertEqual(state['publication_scope'], MERGED_TAIL_CLASSIFICATION)
        self.assertEqual(state['publication_acceptance'], MERGED_TAIL_ACCEPTANCE)
        self.assertEqual(state['publication_evidence']['pr'], 1)
        self.assertEqual(state['publication_evidence']['merge_commit'], ids['M'])
        self.assertEqual(state['publication_evidence']['publication_commit'], ids['R'])
