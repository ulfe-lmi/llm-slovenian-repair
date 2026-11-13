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


class ArchitectureRevisionReview(unittest.TestCase):
    """037-a requirement 6: narrow ordered architecture-revision opt-in.

    The default candidate review still rejects ARCHITECTURE.md in the
    allowlist. Only a pinned order carrying a valid ``architecture_revision``
    (authorized, literal trusted accepted ref, accepted-ref architecture
    digest) authorizes that single path; forged/mutated authorization and
    every other protected path fail closed.
    """
    setUp = base.Acceptance.setUp
    tearDown = base.Acceptance.tearDown

    def cli(self, sha, accepted='base'):
        args = ['candidate-review', '--repo-root', str(self.repo),
                '--order', ORDER_REL, '--order-sha256', sha,
                '--accepted-ref', accepted if accepted != 'base' else self.base,
                '--order-id', '000-a']
        holder = {'out': io.StringIO(), 'err': io.StringIO()}
        with contextlib.redirect_stdout(holder['out']), \
                contextlib.redirect_stderr(holder['err']):
            rc = oap_cli.main(args)
        return rc, holder

    def old_arch_sha(self):
        return digest(git_blob(self.repo, self.base, 'ARCHITECTURE.md'))

    def build_arch_order(self, *, bullets, arch_revision=None, governance_ref=None):
        m, data = order(self.repo, self.base, '000-a')
        m['governance_ref'] = governance_ref if governance_ref is not None else self.base
        if arch_revision is not None:
            m['architecture_revision'] = arch_revision
        data = replace_metadata(data, m)
        section = '## Governance\n' + '\n'.join('- ' + b for b in bullets)
        data = data.replace(b'## Governance\nSynthetic observed contract at the stated boundary.',
                            section.encode(), 1)
        write(self.repo / ORDER_REL, data)
        return m, data

    def arch_rev(self, *, authorized=True, accepted_ref=None, old_sha=None):
        return {'authorized': authorized,
                'accepted_ref': accepted_ref if accepted_ref is not None else self.base,
                'old_sha256': old_sha if old_sha is not None else self.old_arch_sha()}

    def reindex(self, *paths):
        manifest_path = self.repo / 'oap/governance/MANIFEST.json'
        m = jsread(manifest_path)
        for rel in paths:
            m['identities'][rel] = {'sha256': digest(read(self.repo / rel)),
                                    'bytes': len(read(self.repo / rel))}
        m['coding_bytes'] = sum(len(read(self.repo / p)) for p in READ_SET)
        write(manifest_path, json_bytes(m))

    def apply_synced_arch_revision(self):
        """Change ARCHITECTURE.md and keep its projections consistent."""
        old = self.old_arch_sha()
        arch = self.repo / 'ARCHITECTURE.md'
        write(arch, read(arch) + b'\nSynthetic authorized architecture revision.\n')
        new = digest(read(arch))
        write(self.repo / 'ARCHITECTURE-for-agents.md',
              read(self.repo / 'ARCHITECTURE-for-agents.md').replace(old.encode(), new.encode()))
        write(self.repo / 'oap/governance/DISTILLATION-MAP.md',
              read(self.repo / 'oap/governance/DISTILLATION-MAP.md').replace(old.encode(), new.encode()))
        self.reindex('ARCHITECTURE.md', 'ARCHITECTURE-for-agents.md',
                     'oap/governance/DISTILLATION-MAP.md')
        return old

    def test_architecture_path_without_revision_stays_protected(self):
        self.build_arch_order(bullets=['ARCHITECTURE.md', 'oap/governance/MANIFEST.json'])
        rc, holder = self.cli(digest(read(self.repo / ORDER_REL)))
        self.assertEqual(rc, 2)
        self.assertIn('PROTECTED_PATH_IN_ALLOWLIST', holder['err'].getvalue())

    def test_valid_architecture_revision_allows_path(self):
        self.build_arch_order(bullets=['ARCHITECTURE.md', 'oap/governance/MANIFEST.json'],
                              arch_revision=self.arch_rev())
        rc, holder = self.cli(digest(read(self.repo / ORDER_REL)))
        self.assertEqual(rc, 0, holder['err'].getvalue())
        payload = json.loads(holder['out'].getvalue())
        self.assertIn('ARCHITECTURE.md', payload['allowed_changes'])

    def test_valid_architecture_revision_full_synced_change(self):
        self.build_arch_order(
            bullets=['ARCHITECTURE.md', 'ARCHITECTURE-for-agents.md',
                     'oap/governance/DISTILLATION-MAP.md', 'oap/governance/MANIFEST.json'],
            arch_revision=self.arch_rev())
        old = self.apply_synced_arch_revision()
        self.assertNotEqual(old, digest(read(self.repo / 'ARCHITECTURE.md')))
        rc, holder = self.cli(digest(read(self.repo / ORDER_REL)))
        self.assertEqual(rc, 0, holder['err'].getvalue())
        payload = json.loads(holder['out'].getvalue())
        self.assertIn('ARCHITECTURE.md', payload['allowed_changes'])
        self.assertEqual(payload['governance']['mode'], 'candidate-review')

    def test_architecture_revision_not_authorized_fails_closed(self):
        self.build_arch_order(bullets=['ARCHITECTURE.md'],
                              arch_revision=self.arch_rev(authorized=False))
        rc, holder = self.cli(digest(read(self.repo / ORDER_REL)))
        self.assertEqual(rc, 2)
        self.assertIn('PROTECTED_PATH_IN_ALLOWLIST', holder['err'].getvalue())

    def test_architecture_revision_wrong_accepted_ref_fails_closed(self):
        git(self.repo, 'commit', '--allow-empty', '-m', 'Synthetic accepted advance')
        advanced = git(self.repo, 'rev-parse', 'HEAD').decode().strip()
        self.build_arch_order(bullets=['ARCHITECTURE.md'],
                              arch_revision=self.arch_rev(accepted_ref=advanced))
        rc, holder = self.cli(digest(read(self.repo / ORDER_REL)))
        self.assertEqual(rc, 2)
        self.assertIn('PROTECTED_PATH_IN_ALLOWLIST', holder['err'].getvalue())

    def test_architecture_revision_wrong_old_sha_fails_closed(self):
        self.build_arch_order(bullets=['ARCHITECTURE.md'],
                              arch_revision=self.arch_rev(old_sha='0' * 64))
        rc, holder = self.cli(digest(read(self.repo / ORDER_REL)))
        self.assertEqual(rc, 2)
        self.assertIn('PROTECTED_PATH_IN_ALLOWLIST', holder['err'].getvalue())

    def test_other_protected_paths_unaffected_by_arch_revision(self):
        self.build_arch_order(bullets=['ARCHITECTURE.md', 'PLAN.md'],
                              arch_revision=self.arch_rev())
        rc, holder = self.cli(digest(read(self.repo / ORDER_REL)))
        self.assertEqual(rc, 2)
        self.assertIn('PROTECTED_PATH_IN_ALLOWLIST', holder['err'].getvalue())

    def test_critical_source_lock_and_bootstrap_stay_protected_under_arch_optin(self):
        for other in ('CRITICAL.md', 'oap/bootstrap-sources.lock.json',
                      'docs/bootstrap'):
            with self.subTest(other=other):
                self.build_arch_order(bullets=['ARCHITECTURE.md', other],
                                      arch_revision=self.arch_rev())
                rc, holder = self.cli(digest(read(self.repo / ORDER_REL)))
                self.assertEqual(rc, 2)
                self.assertIn('PROTECTED_PATH_IN_ALLOWLIST',
                              holder['err'].getvalue())

    def test_architecture_authorization_mutation_after_pinned_digest_fails_closed(self):
        m, data = self.build_arch_order(bullets=['ARCHITECTURE.md'],
                                        arch_revision=self.arch_rev())
        pinned = digest(data)
        mutated_meta = dict(m)
        del mutated_meta['architecture_revision']
        write(self.repo / ORDER_REL, replace_metadata(data, mutated_meta))
        rc, holder = self.cli(pinned)
        self.assertEqual(rc, 2)
        self.assertIn('ORDER_DIGEST_MISMATCH', holder['err'].getvalue())


class BootstrapSelfAuthorization(unittest.TestCase):
    """037-a requirement 6: candidate hashes cannot authorize themselves.

    A revised ARCHITECTURE.md with fully self-consistent mutable projections
    (manifest identities, compact source hash, distillation) must still fail
    bootstrap mode: the trusted seed is the only anchor, and bootstrap
    validation is presented with no accepted ref and no order.
    """
    setUp = base.Acceptance.setUp
    tearDown = base.Acceptance.tearDown

    def make_self_consistent_candidate_revision(self):
        """Revise ARCHITECTURE.md and re-pin every mutable projection to it."""
        arch = self.repo / 'ARCHITECTURE.md'
        old = digest(git_blob(self.repo, self.base, 'ARCHITECTURE.md'))
        write(arch, read(arch) + b'\nSynthetic self-authorized revision.\n')
        new = digest(read(arch))
        write(self.repo / 'ARCHITECTURE-for-agents.md',
              read(self.repo / 'ARCHITECTURE-for-agents.md').replace(old.encode(), new.encode()))
        write(self.repo / 'oap/governance/DISTILLATION-MAP.md',
              read(self.repo / 'oap/governance/DISTILLATION-MAP.md').replace(old.encode(), new.encode()))
        m = jsread(self.repo / 'oap/governance/MANIFEST.json')
        for rel in ('ARCHITECTURE.md', 'ARCHITECTURE-for-agents.md',
                    'oap/governance/DISTILLATION-MAP.md'):
            m['identities'][rel] = {'sha256': digest(read(self.repo / rel)),
                                    'bytes': len(read(self.repo / rel))}
        m['coding_bytes'] = sum(len(read(self.repo / p)) for p in READ_SET)
        write(self.repo / 'oap/governance/MANIFEST.json', json_bytes(m))
        return old, new

    def test_bootstrap_rejects_self_consistent_candidate_hashes(self):
        old, new = self.make_self_consistent_candidate_revision()
        self.assertNotEqual(old, new)
        # The trusted seed is untouched and the candidate no longer matches it...
        self.assertNotEqual(read(self.repo / 'ARCHITECTURE.md'),
                            read(self.repo / 'docs/bootstrap' / 'ARCHITECTURE.md'))
        # ...yet every mutable candidate projection is self-consistent.
        m = jsread(self.repo / 'oap/governance/MANIFEST.json')
        self.assertEqual(m['identities']['ARCHITECTURE.md']['sha256'], new)
        self.assertIn(new.encode(), read(self.repo / 'ARCHITECTURE-for-agents.md'))
        self.assertIn(new.encode(), read(self.repo / 'oap/governance/DISTILLATION-MAP.md'))
        # Bootstrap mode has no accepted ref and no order: the candidate
        # cannot authorize itself.
        with self.assertRaises(OAPError) as cm:
            governance(self.repo, mode='bootstrap')
        self.assertEqual(cm.exception.code, 'BOOTSTRAP_SOURCE_DRIFT')
        self.assertIn('ARCHITECTURE.md', str(cm.exception))
