"""Native-layout doctor and private-mode guards at the actual CLI boundary."""
import json
import os
import stat
import subprocess
import sys
import unittest
from unittest.mock import patch
import test_acceptance as base
from support import *
from oap_core import *
from oap_install import materialize, runtime_config
from oap_cli import doctor


class NativeLayoutDoctor(base.LayoutSelection, unittest.TestCase):
    """The current native+foreground layout passes ownership/type/mode/symlink
    guards and doctor with the exact fixture FIFO paths; the historical sync
    exception is proven NOT to apply to native roots."""
    setUp = base.Acceptance.setUp
    tearDown = base.Acceptance.tearDown
    error = base.Acceptance.error

    def _materialized(self):
        self.select_native_foreground()
        materialize(self.repo, self.repo, self.strategy, self.bootstrap)
        return runtime_config(self.strategy / 'runtime.env', environ={}, repo=self.repo)

    def _doctor(self, cfg):
        with patch.dict(os.environ, {'OAP_ROLE': 'strategic'}):
            return doctor(self.repo, self.strategy, cfg)

    def _cli(self):
        # Actual CLI boundary: the installed product entry point with
        # explicit repo-root/config/strategic-home, real exit status.
        env = {k: v for k, v in os.environ.items() if not k.startswith(('OAP_', 'CODEX_'))}
        env['OAP_ROLE'] = 'strategic'
        return subprocess.run(
            [sys.executable, '-B', str(SOURCE / 'oap/bin/oap_cli.py'), 'doctor',
             '--repo-root', str(self.repo),
             '--strategic-home', str(self.strategy),
             '--config', str(self.strategy / 'runtime.env')],
            capture_output=True, text=True, timeout=120, env=env)

    def test_cli_doctor_validates_native_layout(self):
        self._materialized()
        proc = self._cli()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result['bootstrap_structure'], 'valid', result['errors'])
        self.assertEqual(result['coding_dispatch'], 'foreground')
        self.assertEqual(result['strategic_storage'], 'native private modes')
        self.assertEqual(result['fifo_home'], str(self.pipes))
        self.assertEqual(result['models_started'], 0)
        self.assertEqual(result['signals_sent'], 0)

    def test_cli_doctor_fails_closed_on_fifo_home_mode_drift(self):
        self._materialized()
        self.pipes.chmod(0o755)
        proc = self._cli()
        self.assertNotEqual(proc.returncode, 0)
        # Either the structured invalid result (rc 1) or the fail-closed
        # error during the final fifo_home recomputation (rc 2): the
        # observed boundary must name the strict native mode violation.
        observed = proc.stdout + proc.stderr
        self.assertIn('PRIVATE_MODE', observed, observed)

    def test_cli_doctor_fails_closed_on_fifo_type_drift(self):
        self._materialized()
        (self.pipes / 'control.fifo').unlink()
        write(self.pipes / 'control.fifo', b'')
        proc = self._cli()
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result['bootstrap_structure'], 'invalid')
        self.assertTrue(any('WRONG_TYPE' in e for e in result['errors']), result['errors'])

    def test_doctor_validates_native_layout_and_fifos(self):
        cfg = self._materialized()
        result = self._doctor(cfg)
        self.assertEqual(result['bootstrap_structure'], 'valid', result['errors'])
        self.assertEqual(result['coding_dispatch'], 'foreground')
        self.assertEqual(result['strategic_storage'], 'native private modes')
        self.assertEqual(result['fifo_home'], str(self.pipes))
        for n in ('control.fifo', 'response.fifo'):
            st = (self.pipes / n).stat()
            self.assertTrue(stat.S_ISFIFO(st.st_mode))
            self.assertEqual(stat.S_IMODE(st.st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(self.pipes.stat().st_mode), 0o700)
        self.assertEqual(result['models_started'], 0)
        self.assertEqual(result['signals_sent'], 0)

    def test_doctor_rejects_fifo_type_drift(self):
        cfg = self._materialized()
        (self.pipes / 'control.fifo').unlink()
        write(self.pipes / 'control.fifo', b'')
        result = self._doctor(cfg)
        self.assertEqual(result['bootstrap_structure'], 'invalid')
        self.assertTrue(any('WRONG_TYPE' in e for e in result['errors']), result['errors'])

    def test_doctor_rejects_fifo_symlink(self):
        cfg = self._materialized()
        target = self.pipes / 'control.fifo.real'
        write(target, b'')
        (self.pipes / 'control.fifo').unlink()
        (self.pipes / 'control.fifo').symlink_to(target)
        result = self._doctor(cfg)
        self.assertEqual(result['bootstrap_structure'], 'invalid')
        self.assertTrue(any('UNSAFE_SYMLINK' in e for e in result['errors']), result['errors'])

    def test_doctor_rejects_fifo_home_mode_drift(self):
        # Fail-closed contract: a strict-mode violation on the native FIFO
        # home is raised by doctor itself (surfaced as the CLI's rc-2 error),
        # never downgraded to a lenient return shape.
        cfg = self._materialized()
        self.pipes.chmod(0o755)
        self.error('PRIVATE_MODE', self._doctor, cfg)

    def test_doctor_rejects_strategic_home_mode_drift(self):
        # Native roots keep strict 0700; the legacy sync exception must not
        # be applied to the selected native strategic home.
        cfg = self._materialized()
        self.strategy.chmod(0o755)
        result = self._doctor(cfg)
        self.assertEqual(result['bootstrap_structure'], 'invalid')
        self.assertTrue(any('PRIVATE_MODE' in e for e in result['errors']), result['errors'])
