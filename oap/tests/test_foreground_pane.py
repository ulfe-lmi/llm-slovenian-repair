"""Real tmux pane foreground process-group boundary (012-a requirement 4).

The pane-level class verifies the explicitly selected pane PID against its
own /proc chain and its exact Codex descendant (no Git/governance involved);
the dispatch class runs the real foreground-dispatch CLI/FIFO boundary on a
disposable native+foreground fixture, with only the external gh edge fake.
The pane hosts an inert argv-rewriting Python process that presents the exact
launch argv — a test stub, not a coding agent. The stub touches only its own
argv region (proc_pid_stat(5) arg_start/arg_end) and never another process.
"""
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'bin'))
import stat
from urllib.parse import quote
from unittest.mock import patch

import test_acceptance as base
import oap_cli
from support import *
from oap_core import OAPError, _proc_stat_fields, foreground_pane, fifo
from oap_install import materialize, runtime_config, env_bytes
from oap_runtime import foreground_dispatch, launch, role_context, tmux_plan

# Pane-matcher launch args: post-binary arguments of the exact relaunch argv.
LAUNCH_ARGS = ['--yolo', '--profile', 'early-beta']

STUB_PROGRAM = (
    'import ctypes,pathlib,time'
    '; s=pathlib.Path("/proc/self/stat").read_text().rsplit(")",1)[1].split()'
    '; a,b=int(s[45]),int(s[46])'
    '; v=b"codex\\0--yolo\\0--profile\\0early-beta\\0"'
    '; assert 0<len(v)<=b-a<100000'
    '; ctypes.memset(a,0,b-a); ctypes.memmove(a,v,len(v))'
    '; time.sleep(300)'
)


class ForegroundPaneBoundary(unittest.TestCase):
    def setUp(self):
        if not shutil.which('tmux'):
            self.skipTest('tmux absent: real pane boundary NOT RUN')
        self.root = Path(tempfile.mkdtemp(prefix='oap-fg-pane-'))
        self.addCleanup(self._retire_root)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.sock = 'oap-fg-pane-%d-%d' % (os.getpid(), threading.get_native_id())

    def _retire_root(self):
        sock = getattr(self, 'sock', None)
        if sock:
            subprocess.run(['tmux', '-L', sock, 'kill-server'], capture_output=True)
        for _ in range(5):
            try:
                shutil.rmtree(self.root)
                return
            except OSError:
                time.sleep(0.05)
        self.assertFalse(self.root.exists())

    def _pane(self, name, command):
        subprocess.run(['tmux', '-L', self.sock, 'new-session', '-d', '-s', name,
                        '-c', str(self.repo), command], check=True, capture_output=True)
        pane = int(subprocess.check_output(['tmux', '-L', self.sock, 'list-panes', '-t', name,
                                            '-F', '#{pane_pid}'], text=True).strip())
        time.sleep(0.5)
        return pane

    def _stub(self):
        return shlex.quote(sys.executable) + ' -c ' + shlex.quote(STUB_PROGRAM)

    def test_background_child_is_not_foreground(self):
        """A backgrounded stub ("& wait") in a non-interactive, job-control-off
        shell inherits the shell's process group: pgrp==tpgid==shell PID, not
        its own PID, so it must not be accepted as the foreground Codex."""
        pane = self._pane('bg', 'bash --noprofile --norc -c ' +
                          shlex.quote(self._stub() + ' & wait'))
        try:
            with self.assertRaises(OAPError) as cm:
                foreground_pane(self.repo, pane, LAUNCH_ARGS)
            self.assertEqual(cm.exception.code, 'PANE_NOT_FOREGROUND')
        finally:
            subprocess.run(['tmux', '-L', self.sock, 'kill-server'], capture_output=True)

    def test_foreground_job_leader_is_accepted(self):
        """An interactive pane shell (job control on) places its foreground
        job in its own group: the stub's pgrp==tpgid==its own PID, the
        unambiguous foreground job leader, and the pane is accepted."""
        pane = self._pane('fg', 'bash --noprofile --norc -i -c ' +
                          shlex.quote(self._stub()))
        try:
            matched = foreground_pane(self.repo, pane, LAUNCH_ARGS)
            fields = _proc_stat_fields(matched)
            self.assertIsNotNone(fields)
            _, pgrp, tty_nr, tpgid = fields
            self.assertEqual(pgrp, matched)
            self.assertEqual(tpgid, pgrp)
            self.assertNotEqual(tty_nr, 0)
        finally:
            subprocess.run(['tmux', '-L', self.sock, 'kill-server'], capture_output=True)

    def test_wrong_launch_argv_is_not_the_pane_match(self):
        """A stub presenting a different launch argv is not the selected
        pane's Codex descendant even when foreground."""
        program = STUB_PROGRAM.replace(
            'b"codex\\0--yolo\\0--profile\\0early-beta\\0"',
            'b"codex\\0--yolo\\0--profile\\0other-beta\\0"')
        pane = self._pane('argv', 'bash --noprofile --norc -i -c ' +
                          shlex.quote(shlex.quote(sys.executable) + ' -c ' + shlex.quote(program)))
        try:
            with self.assertRaises(OAPError) as cm:
                foreground_pane(self.repo, pane, LAUNCH_ARGS)
            self.assertEqual(cm.exception.code, 'PANE_ARGV_MISMATCH')
        finally:
            subprocess.run(['tmux', '-L', self.sock, 'kill-server'], capture_output=True)


class ForegroundDispatchBoundary(base.LayoutSelection, unittest.TestCase):
    """Real foreground-dispatch CLI/FIFO boundary on the native+foreground
    layout: the dispatcher is the real product CLI, the pane is a real tmux
    pane with an inert stub, and only the external gh edge is fake."""
    setUp = base.Acceptance.setUp
    tearDown = base.Acceptance.tearDown
    error = base.Acceptance.error


    def _dispatch_fixture(self, *, peers=None, with_order=True, with_report=False):
        self.select_native_foreground()
        # Materialize private homes/FIFOs from the fixture itself (the
        # fixture is the source of this disposable topology).
        materialize(self.repo, self.repo, self.strategy, self.bootstrap)
        # The accepted baseline carries the layout selection.
        self.accepted = commit(self.repo, 'Synthetic owner layout selection')
        # Only now: activate the round referencing that baseline.
        if with_order:
            m, data = order(self.repo, self.accepted, '000-a')
            install_order(self.repo, data, '000-a')
        git(self.repo, 'remote', 'add', 'origin', 'https://github.com/synthetic/project.git')
        api = 'repos/synthetic/project/'
        responses = {}
        if with_report:
            # A fully valid prior report makes the durable state
            # PUBLICATION_RECONCILIATION_REQUIRED/REVIEW_READY.
            self.report_meta, self.report_head, self.report_path = \
                report(self.repo, self.remote, '000-a')
            rel = str(self.report_path.relative_to(self.repo))
            responses[api + 'pulls/1'] = self.remote.prs[1]
            responses[api + 'commits/' + self.report_head] = \
                self.remote.responses['commits/' + self.report_head]
            responses[api + 'contents/' + rel + '?ref=' + self.report_head] = \
                self.remote.responses['contents/' + rel + '?ref=' + self.report_head]
        cfg = runtime_config(self.strategy / 'runtime.env', environ={}, repo=self.repo)
        cfg.update(OAP_GITHUB_REPOSITORY='synthetic/project',
                   OAP_ACCEPTED_REF=self.accepted,
                   OAP_MERGE_EFFECT='development-only')
        # Defensive sentinel: any unintended model launch cannot reach a real
        # codex binary from this fixture.
        cfg.update(CODEX_BIN=str(self.root / 'sentinel-no-codex'))
        env_path = self.strategy / 'runtime.env'
        write(env_path, env_bytes(cfg))
        env_path.chmod(0o600)
        self.fake_gh = write(self.root / 'fake-gh', read(SOURCE / 'oap/tests/fake_gh.py'))
        self.fake_gh.chmod(0o700)
        responses[api + 'pulls?state=all&head=' +
                  quote('synthetic:oap/000-synthetic', safe='')] = \
            peers if peers is not None else []
        self._write_responses(responses)
        self.sock = 'oap-fd-%d-%d' % (os.getpid(), threading.get_native_id())
        return cfg

    def _stub(self):
        return shlex.quote(sys.executable) + ' -c ' + shlex.quote(STUB_PROGRAM)

    def _pane(self, name='fd', command=None):
        # Subshell wrapper: keeps the pane shell distinct from the stub
        # process (no bash -c single-command exec collapse), mirroring the
        # owner topology of a pane shell with one foreground Codex child.
        command = command or 'bash --noprofile --norc -i -c ' + \
            shlex.quote('(' + self._stub() + ')')
        subprocess.run(['tmux', '-L', self.sock, 'new-session', '-d', '-s', name,
                        '-c', str(self.repo), command], check=True, capture_output=True)
        self.pane_pid = int(subprocess.check_output(
            ['tmux', '-L', self.sock, 'list-panes', '-t', name, '-F', '#{pane_pid}'],
            text=True).strip())
        time.sleep(0.5)
        return self.pane_pid

    def _kill_pane(self):
        subprocess.run(['tmux', '-L', self.sock, 'kill-server'], capture_output=True)

    def test_dispatch_cli_consumes_one_ok_and_starts_zero_models(self):
        if not shutil.which('tmux'):
            self.skipTest('tmux absent: real pane integration NOT RUN')
        import contextlib
        import io
        cfg = self._dispatch_fixture()
        pane = self._pane()
        self.addCleanup(self._kill_pane)
        args = ['foreground-dispatch', '--config', str(self.strategy / 'runtime.env'),
                '--repo-root', str(self.repo), '--pane-pid', str(pane),
                '--timeout', '8', '--gh-bin', str(self.fake_gh)]
        holder = {'out': io.StringIO(), 'err': io.StringIO()}

        def run_cli():
            with contextlib.redirect_stdout(holder['out']), \
                    contextlib.redirect_stderr(holder['err']):
                holder['rc'] = oap_cli.main(args)

        with patch.dict(os.environ, {'OAP_ROLE': 'strategic',
                                     'FAKE_GH_RESPONSES': str(self.responses_file)}):
            t = threading.Thread(target=run_cli, daemon=True)
            t.start()
            try:
                fifo(self.pipes / 'control.fifo', 'send', timeout=8)
            except OAPError as e:
                t.join(20)
                self.fail('control wait boundary not reached (CLI %s); stderr: %s'
                          % (e.code, holder['err'].getvalue()))
            t.join(20)
        self.assertFalse(t.is_alive())
        self.assertEqual(holder['rc'], 0, holder['err'].getvalue())
        payload = json.loads(holder['out'].getvalue())
        self.assertEqual(payload['result'], 'handoff ready')
        self.assertEqual(payload['id'], '000-a')
        self.assertEqual(payload['models_started'], 0)
        self.assertEqual(payload['signals_sent'], 0)
        record_path = self.strategy / 'workorders' / 'consumed.json'
        self.assertTrue(record_path.exists())
        self.assertEqual(stat.S_IMODE(record_path.stat().st_mode), 0o600)
        record = jsread(record_path)
        self.assertEqual(record['id'], '000-a')
        self.assertEqual(record['branch'], 'oap/000-synthetic')
        self.assertIsNone(record['pr'])
        self.assertEqual(record['phase'], 'consumed')
        self.assertIs(record['recovery'], False)
        self.assertEqual(record['dispatch'], 'foreground')
        # The verified Codex descendant: exactly one, and the recorded pane
        # identity is that descendant, not the pane shell.
        matched = foreground_pane(self.repo, pane, LAUNCH_ARGS)
        self.assertEqual(record['pane_pid'], matched)
        self.assertNotEqual(record['pane_pid'], pane)

    # ---- dispatch gate negatives (pre-FIFO via the real function) -----------

    def _dispatch_direct(self, cfg, *, resume_id=None, role_env='strategic', pane_pid=None):
        with patch.dict(os.environ, {'OAP_ROLE': role_env,
                                     'FAKE_GH_RESPONSES': str(self.responses_file)}):
            return foreground_dispatch(cfg, pane_pid=pane_pid or self.pane_pid,
                                       resume_id=resume_id, gh_bin=str(self.fake_gh),
                                       timeout=4)

    def test_dispatch_requires_strategic_role(self):
        self._dispatch_fixture()
        self.error('ROLE_REQUIRED', self._dispatch_direct, {'OAP_REPO_ROOT': str(self.repo)},
                   role_env='coding', pane_pid=1)
        env = {k: v for k, v in os.environ.items() if k != 'OAP_ROLE'}
        env['FAKE_GH_RESPONSES'] = str(self.responses_file)
        with patch.dict(os.environ, env, clear=True):
            self.error('ROLE_REQUIRED', foreground_dispatch,
                       {'OAP_REPO_ROOT': str(self.repo)}, pane_pid=1, timeout=4)

    def test_dispatch_no_active_round(self):
        cfg = self._dispatch_fixture(with_order=False)
        self._pane()
        self.addCleanup(self._kill_pane)
        self.error('NO_ACTIVE_ROUND', self._dispatch_direct, cfg)
        self.assertFalse((self.strategy / 'workorders' / 'consumed.json').exists())

    def test_dispatch_completed_round_replay_refused(self):
        cfg = self._dispatch_fixture(with_report=True)
        self._pane()
        self.addCleanup(self._kill_pane)
        self.error('COMPLETED_REPLAY', self._dispatch_direct, cfg)
        self.assertFalse((self.strategy / 'workorders' / 'consumed.json').exists())

    def _write_consumed(self, pr):
        record_path = self.strategy / 'workorders' / 'consumed.json'
        record_path.parent.mkdir(parents=True, exist_ok=True)
        write(record_path, json_bytes({'id': '000-a', 'branch': 'oap/000-synthetic',
                                       'pr': pr, 'phase': 'consumed', 'recovery': False,
                                       'dispatch': 'foreground', 'pane_pid': 1}))
        record_path.chmod(0o600)
        return record_path

    def test_dispatch_unresumed_consumed_round_refused(self):
        cfg = self._dispatch_fixture()
        self._pane()
        self.addCleanup(self._kill_pane)
        self._write_consumed(None)
        self.error('EXPLICIT_SAME_ORDER_RECOVERY_REQUIRED', self._dispatch_direct, cfg)
        # The pre-existing record is untouched: no consumption without resume.
        record = jsread(self.strategy / 'workorders' / 'consumed.json')
        self.assertIsNone(record['pr'])
        self.assertIs(record['recovery'], False)

    def test_dispatch_peer_gates_fail_before_control(self):
        cases = (
            ([{'number': 1, 'state': 'open', 'merged': None},
              {'number': 2, 'state': 'open', 'merged': None}], 'DUPLICATE_PR'),
            ([{'number': 1, 'state': 'closed', 'merged': True}],
             'MERGED_PEER_REQUIRES_RECONCILIATION'),
            ([{'number': 1, 'state': 'open', 'merged': True}],
             'MERGED_PEER_REQUIRES_RECONCILIATION'),
            ([{'number': 1, 'merged': None}], 'MERGED_PEER_REQUIRES_RECONCILIATION'),
        )
        # One fixture/pane; only the fake peer responses change per case.
        cfg = self._dispatch_fixture()
        self._pane()
        self.addCleanup(self._kill_pane)
        for peers, code in cases:
            with self.subTest(code=code):
                self._set_peers(peers)
                self.error(code, self._dispatch_direct, cfg)
                self.assertFalse((self.strategy / 'workorders' / 'consumed.json').exists())

    def _peer_key(self):
        return ('repos/synthetic/project/pulls?state=all&head=' +
                quote('synthetic:oap/000-synthetic', safe=''))

    def _set_peers(self, peers):
        data = {}
        if getattr(self, 'responses', None) is not None:
            data = json.loads(read(self.responses_file).decode())
        data[self._peer_key()] = peers
        self._write_responses(data)

    def _write_responses(self, mapping):
        self.responses_file = write(self.root / 'fake-gh-responses.json',
                                    (json.dumps(mapping) + '\n').encode())

    def test_dispatch_resume_requires_consumed_pr_identity(self):
        cfg = self._dispatch_fixture(peers=[{'number': 7, 'state': 'open', 'merged': None}])
        self._pane()
        self.addCleanup(self._kill_pane)
        self._write_consumed(5)
        self.error('RECOVERY_PR_MISMATCH', self._dispatch_direct, cfg, resume_id='000-a')

    def test_dispatch_pane_gates_fail_before_control(self):
        cfg = self._dispatch_fixture()
        self.error('PANE_DEAD', self._dispatch_direct, cfg, pane_pid=999999999)
        proc = subprocess.Popen([sys.executable, '-c', STUB_PROGRAM], cwd=self.repo)
        try:
            time.sleep(0.5)
            self.error('PANE_NOT_TMUX_PANE', self._dispatch_direct, cfg, pane_pid=proc.pid)
        finally:
            proc.terminate()
            proc.wait()
        pane = self._pane('bg', 'bash --noprofile --norc -c ' +
                          shlex.quote(self._stub() + ' & wait'))
        self.error('PANE_NOT_FOREGROUND', self._dispatch_direct, cfg, pane_pid=pane)
        wrong = STUB_PROGRAM.replace(
            'b"codex\\0--yolo\\0--profile\\0early-beta\\0"',
            'b"codex\\0--yolo\\0--profile\\0other-beta\\0"')
        pane = self._pane('argv', 'bash --noprofile --norc -i -c ' +
                          shlex.quote('(' + shlex.quote(sys.executable) + ' -c ' +
                                      shlex.quote(wrong) + ')'))
        self.error('PANE_ARGV_MISMATCH', self._dispatch_direct, cfg, pane_pid=pane)
        self.assertFalse((self.strategy / 'workorders' / 'consumed.json').exists())

    def test_legacy_entry_points_refuse_foreground_runtime(self):
        cfg = self._dispatch_fixture()
        with patch.dict(os.environ, {'OAP_ROLE': 'coding'}):
            self.error('FOREGROUND_DISPATCH_ONLY', role_context, cfg, 'coding',
                       operational=True)
            self.error('FOREGROUND_DISPATCH_ONLY', launch, cfg, 'coding')
            self.error('FOREGROUND_DISPATCH_ONLY', tmux_plan, cfg, True,
                       config_path=self.strategy / 'runtime.env')

    # ---- FIFO boundary via the real CLI --------------------------------------

    def _run_cli(self, args, frame):
        import contextlib
        import io
        holder = {'out': io.StringIO(), 'err': io.StringIO()}

        def run_cli():
            with contextlib.redirect_stdout(holder['out']), \
                    contextlib.redirect_stderr(holder['err']):
                holder['rc'] = oap_cli.main(args)

        with patch.dict(os.environ, {'OAP_ROLE': 'strategic',
                                     'FAKE_GH_RESPONSES': str(self.responses_file)}):
            t = threading.Thread(target=run_cli, daemon=True)
            t.start()
            frame()
            t.join(20)
        self.assertFalse(t.is_alive())
        return holder

    def _cli_args(self, *extra):
        return ['foreground-dispatch', '--config', str(self.strategy / 'runtime.env'),
                '--repo-root', str(self.repo), '--pane-pid', str(self.pane_pid),
                '--timeout', '8', '--gh-bin', str(self.fake_gh)] + list(extra)

    def _wait_for_control_reader(self, timeout=15):
        """Deterministically wait until the dispatcher holds the control FIFO
        open for reading — i.e. it has captured its pre-wait state and is now
        blocked on control. Lets a mutation land inside the post-wait window."""
        fifo_abs = str(self.pipes / 'control.fifo')
        deadline = time.monotonic() + timeout
        while True:
            try:
                fds = os.listdir('/proc/self/fd')
            except OSError:
                fds = []
            for fd in fds:
                try:
                    if os.readlink('/proc/self/fd/' + fd) == fifo_abs:
                        return
                except OSError:
                    continue
            if time.monotonic() > deadline:
                raise AssertionError('dispatcher never opened the control FIFO')
            time.sleep(0.02)

    def test_dispatch_fifo_invalid_frame_fails_closed(self):
        if not shutil.which('tmux'):
            self.skipTest('tmux absent: real pane integration NOT RUN')
        cfg = self._dispatch_fixture()
        self._pane()
        self.addCleanup(self._kill_pane)
        args = ['foreground-dispatch', '--config', str(self.strategy / 'runtime.env'),
                '--repo-root', str(self.repo), '--pane-pid', str(self.pane_pid),
                '--timeout', '8', '--gh-bin', str(self.fake_gh)]

        def send_bad():
            fd = os.open(self.pipes / 'control.fifo', os.O_WRONLY | os.O_NOFOLLOW)
            try:
                os.write(fd, b'KO')
            finally:
                os.close(fd)

        holder = self._run_cli(args, send_bad)
        self.assertEqual(holder['rc'], 2)
        self.assertIn('FIFO_INVALID_FRAME', holder['err'].getvalue())
        self.assertFalse((self.strategy / 'workorders' / 'consumed.json').exists())

    def test_dispatch_resume_cli_preserves_consumed_pr(self):
        if not shutil.which('tmux'):
            self.skipTest('tmux absent: real pane integration NOT RUN')
        cfg = self._dispatch_fixture(
            peers=[{'number': 1, 'state': 'open', 'merged': None}])
        self._pane()
        self.addCleanup(self._kill_pane)
        self._write_consumed(1)
        args = ['foreground-dispatch', '--config', str(self.strategy / 'runtime.env'),
                '--repo-root', str(self.repo), '--pane-pid', str(self.pane_pid),
                '--timeout', '8', '--gh-bin', str(self.fake_gh), '--resume-id', '000-a']
        holder = self._run_cli(args, lambda: fifo(self.pipes / 'control.fifo', 'send', timeout=8))
        self.assertEqual(holder['rc'], 0, holder['err'].getvalue())
        payload = json.loads(holder['out'].getvalue())
        self.assertEqual(payload['result'], 'handoff ready')
        self.assertIs(payload['recovery'], True)
        self.assertEqual(payload['models_started'], 0)
        record = jsread(self.strategy / 'workorders' / 'consumed.json')
        self.assertIs(record['recovery'], True)
        self.assertEqual(record['pr'], 1)

    # ---- post-wait revalidation proofs (mutations inside the FIFO window) ---

    def test_dispatch_order_change_during_wait_fails_closed(self):
        if not shutil.which('tmux'):
            self.skipTest('tmux absent: real pane integration NOT RUN')
        self._dispatch_fixture()
        self._pane()
        self.addCleanup(self._kill_pane)
        order_path = self.repo / 'oap/orders/000-a-synthetic.md'

        def mutate():
            self._wait_for_control_reader()
            write(order_path, read(order_path) + b'\n# synthetic drift during wait\n')
            fifo(self.pipes / 'control.fifo', 'send', timeout=8)

        holder = self._run_cli(self._cli_args(), mutate)
        self.assertEqual(holder['rc'], 2)
        self.assertIn('ORDER_CHANGED_DURING_DISPATCH', holder['err'].getvalue())
        self.assertFalse((self.strategy / 'workorders' / 'consumed.json').exists())

    def test_dispatch_peer_change_during_wait_fails_closed(self):
        if not shutil.which('tmux'):
            self.skipTest('tmux absent: real pane integration NOT RUN')
        self._dispatch_fixture()
        self._pane()
        self.addCleanup(self._kill_pane)

        def mutate():
            self._wait_for_control_reader()
            self._set_peers([{'number': 9, 'state': 'open', 'merged': None}])
            fifo(self.pipes / 'control.fifo', 'send', timeout=8)

        holder = self._run_cli(self._cli_args(), mutate)
        self.assertEqual(holder['rc'], 2)
        self.assertIn('PR_CHANGED_DURING_DISPATCH', holder['err'].getvalue())
        self.assertFalse((self.strategy / 'workorders' / 'consumed.json').exists())

    def test_dispatch_state_change_during_wait_fails_closed(self):
        if not shutil.which('tmux'):
            self.skipTest('tmux absent: real pane integration NOT RUN')
        self._dispatch_fixture()
        self._pane()
        self.addCleanup(self._kill_pane)

        def mutate():
            self._wait_for_control_reader()
            meta, head, rp = report(self.repo, self.remote, '000-a')
            rel = str(rp.relative_to(self.repo))
            data = json.loads(read(self.responses_file).decode())
            data['repos/synthetic/project/pulls/1'] = self.remote.prs[1]
            data['repos/synthetic/project/commits/' + head] = \
                self.remote.responses['commits/' + head]
            data['repos/synthetic/project/contents/' + rel + '?ref=' + head] = \
                self.remote.responses['contents/' + rel + '?ref=' + head]
            self._write_responses(data)
            fifo(self.pipes / 'control.fifo', 'send', timeout=8)

        holder = self._run_cli(self._cli_args(), mutate)
        self.assertEqual(holder['rc'], 2)
        self.assertIn('STATE_CHANGED_DURING_DISPATCH', holder['err'].getvalue())
        self.assertFalse((self.strategy / 'workorders' / 'consumed.json').exists())
