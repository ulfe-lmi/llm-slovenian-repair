"""Repository renames retain remote numeric identity; names alone are insufficient."""
import json
import tempfile
import unittest
from pathlib import Path
from support import GitHub, OAPError


class RepositoryRename(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.responses = root / 'responses.json'
        self.exe = root / 'gh'
        self.exe.write_text('#!/usr/bin/env python3\nimport json,sys\n'
                            f'd=json.load(open({str(self.responses)!r}))\n'
                            'v=d.get(sys.argv[2])\n'
                            'if v is None: sys.exit(1)\n'
                            'print(json.dumps(v))\n')
        self.exe.chmod(0o700)
        self.canonical = {'id': 123, 'full_name': 'owner/new'}
        self.data = {'repos/owner/new': self.canonical,
                     'repos/owner/old': dict(self.canonical),
                     'repos/owner/old/pulls/7': {'number': 7, 'base': {'repo': dict(self.canonical)}}}
        self.remote = GitHub('owner/new', str(self.exe))

    def save(self):
        self.responses.write_text(json.dumps(self.data))

    def test_redirected_name_matches_numeric_identity(self):
        self.save()
        self.assertTrue(self.remote.matches_repository('owner/old'))
        self.assertEqual(GitHub('owner/old', str(self.exe)).pr(7)['number'], 7)

    def test_reassigned_old_name_is_rejected(self):
        self.data['repos/owner/old']['id'] = 456
        self.save()
        self.assertFalse(self.remote.matches_repository('owner/old'))
        with self.assertRaisesRegex(OAPError, 'REMOTE_PR_IDENTITY'):
            GitHub('owner/old', str(self.exe)).pr(7)

    def test_missing_or_invalid_ids_are_rejected(self):
        for value in (None, True, 0, '123'):
            with self.subTest(value=value):
                self.data['repos/owner/old']['id'] = value
                self.save()
                self.assertFalse(self.remote.matches_repository('owner/old'))

    def test_canonical_name_mismatch_is_rejected(self):
        self.data['repos/owner/old']['full_name'] = 'other/project'
        self.save()
        self.assertFalse(self.remote.matches_repository('owner/old'))

    def test_unavailable_alias_fails_closed(self):
        del self.data['repos/owner/old']
        self.save()
        with self.assertRaisesRegex(OAPError, 'REMOTE_UNVERIFIED'):
            self.remote.matches_repository('owner/old')

    def test_wrong_pr_number_is_rejected(self):
        self.data['repos/owner/old/pulls/7']['number'] = 8
        self.save()
        with self.assertRaisesRegex(OAPError, 'REMOTE_PR_IDENTITY'):
            GitHub('owner/old', str(self.exe)).pr(7)

    def test_same_name_preserves_existing_path(self):
        self.save()
        self.assertTrue(self.remote.matches_repository('owner/new'))
