"""Real disposable Git histories for the transcript coherence guard."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from support import *
from oap_core import _transcript_order


def fixture_ignore(directory, names):
    relative = Path(directory).relative_to(SOURCE)
    ignored = {
        name for name in names
        if name in {'.git', '.venv', '__pycache__', '.pytest_cache', '.ruff_cache', '.mypy_cache',
                    'dist', 'build', 'INSTALLATION.json'} or name.endswith('.lock')
    }
    if relative == Path('oap'):
        ignored.add('active')
    if relative == Path('oap/orders'):
        ignored.update(name for name in names if name.endswith('.md'))
    if relative == Path('oap/reports'):
        ignored.update(name for name in names if name.endswith('.md'))
    return ignored


class TranscriptGuard(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='oap-transcript-fixture-')
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        shutil.copytree(SOURCE, self.repo, ignore=fixture_ignore)
        git(self.repo, 'init', '-b', 'main')
        git(self.repo, 'config', 'user.name', 'Synthetic transcript fixture')
        git(self.repo, 'config', 'user.email', 'synthetic@example.invalid')
        self.base = commit(self.repo, 'Synthetic accepted baseline')
        self.remote = FakeGitHub(self.repo)

    def tearDown(self):
        cleanup_owned_temporary_directory(self.temp)

    def commit_fixture(self, message='Synthetic transcript state'):
        git(self.repo, 'add', '--', '.')
        if (self.repo / 'oap/active').exists():
            git(self.repo, 'add', '-f', '--', 'oap/active')
        staged = git(self.repo, 'diff', '--cached', '--quiet', check=False)
        if staged.returncode == 0:
            return git(self.repo, 'rev-parse', 'HEAD').decode().strip()
        git(self.repo, '-c', 'commit.gpgsign=false', 'commit', '-m', message)
        return git(self.repo, 'rev-parse', 'HEAD').decode().strip()

    def install_unfinished(self, ident='000-a', data=None):
        if data is None:
            _, data = order(self.repo, self.base, ident, pr=1 if not ident.endswith('-a') else None)
        write(self.repo / 'oap/orders' / f'{ident}-synthetic.md', data)
        write(self.repo / 'oap/active', ident + '\n')
        return self.commit_fixture('Install unfinished ' + ident)

    def install_report(self, ident='000-a', **kwargs):
        _, data = order(self.repo, self.base, ident, pr=1 if not ident.endswith('-a') else None)
        install_order(self.repo, data, ident)
        result = report(self.repo, self.remote, ident, **kwargs)
        self.commit_fixture('Force-stage active ' + ident)
        return result

    def guard(self, **kwargs):
        return check_transcript(self.repo, **kwargs)

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SOURCE / 'oap/bin/check_transcript.py'), '--repo-root', str(self.repo), *args],
            cwd=self.repo, capture_output=True, text=True, check=False,
        )

    def assert_guard_error(self, code, **kwargs):
        with self.assertRaises(OAPError) as caught:
            self.guard(**kwargs)
        self.assertEqual(caught.exception.code, code)

    def test_inactive_empty_transcript_is_valid_in_both_modes_and_cli(self):
        for kwargs in ({'index': True}, {'revision': 'HEAD'}):
            result = self.guard(**kwargs)
            self.assertEqual(result['active'], None)
            self.assertEqual(result['orders'], [])
        result = self.cli('--revision', 'HEAD')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['result'], 'valid')

    def test_active_unfinished_current_order_is_valid(self):
        self.install_unfinished()
        for kwargs in ({'index': True, 'expected_id': '000-a'}, {'revision': 'HEAD', 'expected_id': '000-a'}):
            self.assertEqual(self.guard(**kwargs)['active'], '000-a')

    def test_current_self_report_is_valid_in_both_modes(self):
        self.install_report()
        self.assertEqual(self.guard(index=True, expected_id='000-a')['reports'], ['000-a'])
        self.assertEqual(self.guard(revision='HEAD', expected_id='000-a')['reports'], ['000-a'])

    def test_suffix_a_to_b_is_valid(self):
        self.install_report('000-a')
        self.install_report('000-b')
        self.assertEqual(self.guard(index=True, expected_id='000-b')['latest'], '000-b')

    def test_full_suffix_prefixes_through_aa_and_ba_are_valid(self):
        for last in ('aa', 'ba'):
            end = SUFFIX_ORDER.index(last) + 1
            ids = [f'000-{suffix}' for suffix in SUFFIX_ORDER[:end]]
            self.assertEqual(_transcript_order(ids), ids)

    def test_missing_initial_objective_and_suffix_origins_are_rejected(self):
        cases = [
            (['001-a'], 'TRANSCRIPT_OBJECTIVE_GAP'),
            (['000-z', '000-aa'], 'TRANSCRIPT_SUFFIX_GAP'),
            (['000-a', '000-c'], 'TRANSCRIPT_SUFFIX_GAP'),
        ]
        for ids, code in cases:
            with self.assertRaises(OAPError) as caught:
                _transcript_order(ids)
            self.assertEqual(caught.exception.code, code)

    def test_historical_order_uses_its_recorded_governance_base(self):
        self.install_report('000-a')
        manifest = jsread(self.repo / 'oap/governance/MANIFEST.json')
        path = next(iter(manifest['identities']))
        manifest['identities'][path]['sha256'] = '0' * 64
        write(self.repo / 'oap/governance/MANIFEST.json', json_bytes(manifest))
        self.commit_fixture('Change current governance candidate')
        result = self.guard(revision='HEAD', expected_id='000-a')
        self.assertEqual(result['reports'], ['000-a'])

    def test_same_size_worktree_index_and_committed_mismatches_are_rejected(self):
        self.install_unfinished()
        original = (self.repo / 'oap/active').read_bytes()
        write(self.repo / 'oap/active', b'000-b\n')
        self.assert_guard_error('ACTIVE_INDEX_MISMATCH', index=True)
        self.assert_guard_error('ACTIVE_COMMIT_MISMATCH', revision='HEAD')
        write(self.repo / 'oap/active', original)
        write(self.repo / 'oap/active', b'000-b\n')
        git(self.repo, 'add', '-f', '--', 'oap/active')
        write(self.repo / 'oap/active', original)
        self.assert_guard_error('ACTIVE_INDEX_MISMATCH', index=True)
        git(self.repo, 'add', '-f', '--', 'oap/active')

    def test_expected_id_mismatch_is_rejected_without_status_or_mtime(self):
        self.install_unfinished()
        self.assert_guard_error('EXPECTED_ACTIVE_MISMATCH', index=True, expected_id='000-b')

    def test_latest_order_mismatch_is_rejected(self):
        self.install_unfinished('000-a')
        _, data = order(self.repo, self.base, '000-b', pr=1)
        write(self.repo / 'oap/orders/000-b-synthetic.md', data)
        self.commit_fixture('Add later unfinished order without advancing active')
        self.assert_guard_error('TRANSCRIPT_LATEST_MISMATCH', revision='HEAD')

    def test_suffix_gap_is_rejected(self):
        self.install_unfinished('000-a')
        _, data = order(self.repo, self.base, '000-c', pr=1)
        write(self.repo / 'oap/orders/000-c-synthetic.md', data)
        write(self.repo / 'oap/active', '000-c\n')
        self.commit_fixture('Install suffix gap')
        self.assert_guard_error('TRANSCRIPT_SUFFIX_GAP', revision='HEAD')

    def test_numeric_gap_is_rejected(self):
        self.install_unfinished('000-a')
        _, data = order(self.repo, self.base, '002-a')
        write(self.repo / 'oap/orders/002-a-synthetic.md', data)
        write(self.repo / 'oap/active', '002-a\n')
        self.commit_fixture('Install numeric gap')
        self.assert_guard_error('TRANSCRIPT_OBJECTIVE_GAP', index=True)

    def test_missing_active_is_allowed_only_for_empty_transcript(self):
        _, data = order(self.repo, self.base, '000-a')
        write(self.repo / 'oap/orders/000-a-synthetic.md', data)
        self.commit_fixture('Install order without active')
        self.assert_guard_error('ACTIVE_REQUIRED', revision='HEAD')

    def test_report_without_order_is_rejected(self):
        write(self.repo / 'oap/reports/000-a-synthetic.md', b'synthetic report fixture\n')
        write(self.repo / 'oap/active', '000-a\n')
        self.commit_fixture('Install report without order')
        self.assert_guard_error('REPORT_ORDER_MISSING', index=True)

    def test_noncurrent_unfinished_order_is_rejected(self):
        self.install_unfinished('000-a')
        _, data = order(self.repo, self.base, '000-b', pr=1)
        write(self.repo / 'oap/orders/000-b-synthetic.md', data)
        write(self.repo / 'oap/active', '000-b\n')
        self.commit_fixture('Install noncurrent unfinished order')
        self.assert_guard_error('TRANSCRIPT_NONCURRENT_UNFINISHED', revision='HEAD')

    def test_extra_path_report_is_rejected(self):
        self.install_report('000-a', extra=True)
        self.assert_guard_error('REPORT_ONLY_PATH', revision='HEAD')

    def test_wrong_parent_report_is_rejected(self):
        self.install_report('000-a', parent=self.base)
        self.assert_guard_error('REPORT_PARENT', index=True)

    def test_draft_order_is_rejected(self):
        metadata_value, data = order(self.repo, self.base, '000-a')
        metadata_value['status'] = 'DRAFT'
        self.install_unfinished('000-a', replace_metadata(data, metadata_value))
        self.assert_guard_error('ORDER_NOT_FINAL', revision='HEAD')

    def test_malformed_and_missing_dha_orders_are_rejected(self):
        _, data = order(self.repo, self.base, '000-a')
        self.install_unfinished('000-a', data.replace(b'```oap-metadata', b'```wrong-metadata', 1))
        self.assert_guard_error('PAYLOAD_FENCE_COUNT', revision='HEAD')

    def test_missing_dha_order_is_rejected(self):
        _, data = order(self.repo, self.base, '000-a')
        self.install_unfinished('000-a', data.replace(b'- Decision: NONE', b'', 1))
        self.assert_guard_error('DHA_DECLARATION', index=True)


if __name__ == '__main__':
    unittest.main()
