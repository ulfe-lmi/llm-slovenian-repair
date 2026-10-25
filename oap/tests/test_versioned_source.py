"""Versioned-source enumeration at Git worktrees and copied file-only
workspaces (the development baseline driver's copied-workspace boundary).
Tiny owned synthetic Git repos; no production tree copy, no model or
network activity."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from support import VERSIONED_HISTORY_SOURCE_ENV, copy_versioned_source, versioned_source_paths
from oap_core import OAPError


def sh(repo, *args):
    p = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, timeout=30)
    assert p.returncode == 0, (args, p.stderr)
    return p.stdout.strip()


class VersionedSourceBoundaries(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='oap-versioned-source-')
        self.root = Path(self.temp.name)
        self.history = self.root / 'history repo'
        self.history.mkdir()
        sh(self.history, 'init', '-b', 'main')
        sh(self.history, 'config', 'user.name', 'Synthetic OAP fixture')
        sh(self.history, 'config', 'user.email', 'synthetic@example.invalid')
        (self.history / 'a.txt').write_bytes(b'alpha v1\n')
        (self.history / 'sub').mkdir()
        (self.history / 'sub' / 'b.txt').write_bytes(b'bravo v1\n')
        sh(self.history, 'add', '--', '.')
        sh(self.history, 'commit', '-m', 'base')

    def tearDown(self):
        self.temp.cleanup()

    def file_only_copy(self, mutate=None, drop=None):
        ws = self.root / 'file-only workspace'
        ws.mkdir()
        for src in ('a.txt', 'sub/b.txt'):
            if src in (drop or ()):
                continue
            dst = ws / src
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes((mutate or {}).get(src, (self.history / src).read_bytes()))
        return ws

    def expect_error(self, code):
        with self.assertRaises(OAPError) as caught:
            versioned_source_paths(self.ws)
        self.assertEqual(caught.exception.code, code)

    def test_worktree_names_come_from_index_and_exclude_untracked(self):
        (self.history / 'untracked.txt').write_bytes(b'not indexed\n')
        self.assertEqual(
            sorted(versioned_source_paths(self.history)), ['a.txt', 'sub/b.txt'])

    def test_copied_workspace_uses_validated_history_names_and_own_bytes(self):
        ws = self.file_only_copy(mutate={'a.txt': b'alpha v2 changed\n'})
        (ws / 'sentinel-untracked.txt').write_bytes(b'sentinel\n')
        self.ws = ws
        with patch.dict(os.environ, {VERSIONED_HISTORY_SOURCE_ENV: str(self.history)}):
            self.assertEqual(sorted(versioned_source_paths(ws)), ['a.txt', 'sub/b.txt'])
            target = self.root / 'target'
            copy_versioned_source(ws, target)
        self.assertEqual((target / 'a.txt').read_bytes(), b'alpha v2 changed\n')
        self.assertEqual((target / 'sub' / 'b.txt').read_bytes(), b'bravo v1\n')
        self.assertFalse((target / 'sentinel-untracked.txt').exists())

    def test_copied_workspace_without_history_fails_closed(self):
        self.ws = self.file_only_copy()
        env = {k: v for k, v in os.environ.items() if k != VERSIONED_HISTORY_SOURCE_ENV}
        with patch.dict(os.environ, env, clear=True):
            self.expect_error('VERSIONED_SOURCE_NOT_GIT_WORKTREE')

    def test_invalid_history_fails_closed(self):
        self.ws = self.file_only_copy()
        with patch.dict(os.environ, {VERSIONED_HISTORY_SOURCE_ENV: str(self.root)}):
            self.expect_error('VERSIONED_HISTORY_NOT_WORKTREE_ROOT')

    def test_missing_provenance_fails_closed(self):
        self.ws = self.file_only_copy(drop=['a.txt'])
        with patch.dict(os.environ, {VERSIONED_HISTORY_SOURCE_ENV: str(self.history)}):
            self.expect_error('VERSIONED_SOURCE_PROVENANCE_MISSING')
