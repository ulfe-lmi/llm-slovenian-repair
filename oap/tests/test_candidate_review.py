"""Order-pinned candidate-review CLI boundary (012-a requirement 2; CI gate).

The published order bytes are the only allowlist authority: a pinned digest
mismatch (including a mutated/expanded Governance bullet list), a wrong
trusted ref, a protected path, an unknown path or an unlisted worktree change
all fail closed before any governance mutation is accepted.
"""
import contextlib
import io
import json
import unittest
import test_acceptance as base
import oap_cli
from support import *

ORDER_REL = 'oap/orders/000-a-synthetic.md'


class CandidateReview(unittest.TestCase):
    setUp = base.Acceptance.setUp
    tearDown = base.Acceptance.tearDown
    error = base.Acceptance.error

    def build_order(self, *, bullets, governance_ref=None):
        m, data = order(self.repo, self.base, '000-a')
        # The candidate-review order always pins its literal trusted ref.
        m['governance_ref'] = governance_ref if governance_ref is not None else self.base
        data = replace_metadata(data, m)
        section = '## Governance\n' + '\n'.join('- ' + b for b in bullets)
        data = data.replace(b'## Governance\nSynthetic observed contract at the stated boundary.',
                            section.encode(), 1)
        write(self.repo / ORDER_REL, data)
        return m, data

    def reindex(self, *paths):
        manifest_path = self.repo / 'oap/governance/MANIFEST.json'
        m = jsread(manifest_path)
        for rel in paths:
            m['identities'][rel] = {'sha256': digest(read(self.repo / rel)),
                                    'bytes': len(read(self.repo / rel))}
        m['coding_bytes'] = sum(len(read(self.repo / p)) for p in READ_SET)
        write(manifest_path, json_bytes(m))

    def cli(self, sha, accepted, data=None):
        args = ['candidate-review', '--repo-root', str(self.repo),
                '--order', ORDER_REL, '--order-sha256', sha,
                '--accepted-ref', accepted, '--order-id', '000-a']
        holder = {'out': io.StringIO(), 'err': io.StringIO()}
        with contextlib.redirect_stdout(holder['out']), \
                contextlib.redirect_stderr(holder['err']):
            rc = oap_cli.main(args)
        return rc, holder

    def test_valid_candidate_review_cli(self):
        self.build_order(bullets=['AGENTS.md', 'oap/governance/MANIFEST.json'])
        agents = self.repo / 'AGENTS.md'
        write(agents, read(agents) + b'\nSynthetic candidate governance note.\n')
        self.reindex('AGENTS.md')
        rc, holder = self.cli(digest(read(self.repo / ORDER_REL)), self.base)
        self.assertEqual(rc, 0, holder['err'].getvalue())
        payload = json.loads(holder['out'].getvalue())
        self.assertEqual(payload['result'], 'candidate review valid')
        self.assertEqual(payload['allowed_changes'],
                         ['AGENTS.md', 'oap/governance/MANIFEST.json'])
        self.assertEqual(payload['governance']['mode'], 'candidate-review')

    def test_wrong_pinned_digest_fails_closed(self):
        m, data = self.build_order(bullets=['AGENTS.md'])
        rc, holder = self.cli(digest(data + b'x'), self.base)
        self.assertEqual(rc, 2)
        self.assertIn('ORDER_DIGEST_MISMATCH', holder['err'].getvalue())

    def test_mutated_allowlist_cannot_authorize(self):
        m, data = self.build_order(bullets=['AGENTS.md'])
        pinned = digest(data)
        mutated = data.replace(b'## Governance\n- AGENTS.md',
                               b'## Governance\n- AGENTS.md\n- oap/prompts/coding-round.md')
        write(self.repo / ORDER_REL, mutated)
        rc, holder = self.cli(pinned, self.base)
        self.assertEqual(rc, 2)
        self.assertIn('ORDER_DIGEST_MISMATCH', holder['err'].getvalue())

    def test_governance_ref_mismatch_fails_closed(self):
        git(self.repo, 'commit', '--allow-empty', '-m', 'Synthetic accepted advance')
        advanced = git(self.repo, 'rev-parse', 'HEAD').decode().strip()
        m, data = self.build_order(bullets=['AGENTS.md'], governance_ref=self.base)
        rc, holder = self.cli(digest(data), advanced)
        self.assertEqual(rc, 2)
        self.assertIn('ORDER_GOVERNANCE_REF_MISMATCH', holder['err'].getvalue())

    def test_protected_path_in_allowlist_fails_closed(self):
        m, data = self.build_order(bullets=['AGENTS.md', 'PLAN.md'])
        rc, holder = self.cli(digest(data), self.base)
        self.assertEqual(rc, 2)
        self.assertIn('PROTECTED_PATH_IN_ALLOWLIST', holder['err'].getvalue())

    def test_unknown_path_in_allowlist_fails_closed(self):
        m, data = self.build_order(bullets=['AGENTS.md', 'oap/unknown/candidate.txt'])
        rc, holder = self.cli(digest(data), self.base)
        self.assertEqual(rc, 2)
        self.assertIn('UNORDERED_GOVERNANCE_CHANGE', holder['err'].getvalue())

    def test_unlisted_worktree_change_fails_closed(self):
        self.build_order(bullets=['AGENTS.md', 'oap/governance/MANIFEST.json'])
        agents = self.repo / 'AGENTS.md'
        write(agents, read(agents) + b'\nSynthetic listed candidate note.\n')
        security = self.repo / 'SECURITY.md'
        write(security, read(security) + b'\nSynthetic unlisted candidate change.\n')
        # Identities are re-pinned for both so the drift gate passes first;
        # the unauthorized change is caught at the allowed-set boundary.
        self.reindex('AGENTS.md', 'SECURITY.md')
        rc, holder = self.cli(digest(read(self.repo / ORDER_REL)), self.base)
        self.assertEqual(rc, 2)
        self.assertIn('UNORDERED_GOVERNANCE_CHANGE', holder['err'].getvalue())
