"""Owner-selected sync subtree with real FIFOs on a separate native filesystem."""
import concurrent.futures
import os
from pathlib import Path
import stat
import time
import unittest
from unittest.mock import patch
import test_acceptance as base
from support import *
from oap_core import *
from oap_install import *
from oap_runtime import role_context,launch
from oap_cli import doctor


class SplitLayout(unittest.TestCase):
    setUp=base.Acceptance.setUp
    tearDown=base.Acceptance.tearDown
    error=base.Acceptance.error

    def test_immutable_sync_fallback_preserves_existing_content(self):
        import errno
        path=self.root/'immutable.md'
        with patch('oap_core.os.link',side_effect=OSError(errno.EPERM,'synthetic unsupported link')):
            atomic(path,b'first',immutable=True)
            self.assertEqual(atomic(path,b'first',immutable=True),'identical')
            self.error('IMMUTABLE_CONFLICT',atomic,path,b'second',immutable=True)
        self.assertEqual(read(path),b'first')

    def test_immutable_sync_fallback_competing_writers(self):
        import errno
        path=self.root/'immutable-race.md'
        def write_one(data):
            try: return atomic(path,data,immutable=True)
            except OAPError as exc: return exc.code
        with patch('oap_core.os.link',side_effect=OSError(errno.EPERM,'synthetic unsupported link')):
            with concurrent.futures.ThreadPoolExecutor() as pool:
                results=list(pool.map(write_one,[b'first',b'second']))
        self.assertEqual(results.count('written'),1)
        self.assertTrue(set(results).issubset({'written','LOCKED','IMMUTABLE_CONFLICT'}))
        self.assertIn(read(path),(b'first',b'second'))

    def test_example_configuration_matches_selected_layout(self):
        path=write(self.root/'runtime.env',read(SOURCE/'oap/runtime.env.example'))
        path.chmod(0o600)
        cfg=runtime_config(path,environ={})
        layout=workspace_layout(SOURCE)
        self.assertEqual(cfg['OAP_STRATEGIC_HOME'],layout['strategic_home'])
        self.assertEqual(cfg['OAP_FIFO_HOME'],layout['fifo_home'])
        for key in ('OAP_ACK_START_LOOP','OAP_ACK_DANGER_FULL_ACCESS','REPAIR_ALLOW_LIVE_TESTS'):
            self.assertEqual(cfg[key],'NO')

    def select_layout(self):
        self.pipes=self.root/'native home č'/'pipes'
        path=self.repo/'oap/governance/WORKSPACE-LAYOUT.json'
        old=read(path)
        value=jsread(path)
        value.update(strategic_home=str(self.strategy),fifo_home=str(self.pipes),authority='Synthetic owner layout fixture')
        write(path,json_bytes(value))
        manifest=jsread(self.repo/'oap/governance/MANIFEST.json')
        manifest['identities']['oap/governance/WORKSPACE-LAYOUT.json']={'sha256':digest(read(path)),'bytes':len(read(path))}
        map_path=self.repo/'oap/governance/DISTILLATION-MAP.md'
        write(map_path,read(map_path).replace(digest(old).encode(),digest(read(path)).encode()))
        manifest['identities']['oap/governance/DISTILLATION-MAP.md']={'sha256':digest(read(map_path)),'bytes':len(read(map_path))}
        write(self.repo/'oap/governance/MANIFEST.json',json_bytes(manifest))
        # This is a disposable explicitly selected fixture, not runtime authority.
        files=jsread(self.repo/'oap/GENERATED-FILES.json')
        for rel in files['files']:
            files['files'][rel]['sha256']=digest(read(self.repo/rel))
            files['files'][rel]['bytes']=len(read(self.repo/rel))
        write(self.repo/'oap/GENERATED-FILES.json',json_bytes(files))

    def test_split_materialization_no_pipe_in_strategy_and_noop(self):
        self.select_layout()
        before=base.snapshot(self.root)
        materialize(self.repo,self.repo,self.strategy,self.bootstrap,dry_run=True)
        self.assertEqual(before,base.snapshot(self.root))
        self.assertFalse(self.pipes.exists())
        materialize(self.repo,self.repo,self.strategy,self.bootstrap)
        for n in ('control.fifo','response.fifo'):
            self.assertFalse((self.strategy/n).exists())
            self.assertTrue(stat.S_ISFIFO((self.pipes/n).stat().st_mode))
            self.assertEqual(stat.S_IMODE((self.pipes/n).stat().st_mode),0o600)
        self.assertEqual(stat.S_IMODE(self.pipes.stat().st_mode),0o700)
        cfg=runtime_config(self.strategy/'runtime.env',environ={},repo=self.repo)
        self.assertEqual(cfg['OAP_FIFO_HOME'],str(self.pipes))
        self.assertEqual(cfg['CODING_CODEX_HOME'],str(self.strategy/'codex-homes/coding'))
        before=base.snapshot(self.root)
        materialize(self.repo,self.repo,self.strategy,self.bootstrap)
        self.assertEqual(before,base.snapshot(self.root))

    def test_sync_mode_exception_is_exact_and_symlink_safe(self):
        self.select_layout()
        materialize(self.repo,self.repo,self.strategy,self.bootstrap)
        self.strategy.chmod(0o755)
        config=self.strategy/'runtime.env'; config.chmod(0o755)
        strategic_path(config,repo=self.repo,kind='file')
        elsewhere=write(self.root/'unapproved.env','synthetic'); elsewhere.chmod(0o755)
        self.error('PRIVATE_MODE',strategic_path,elsewhere,repo=self.repo,kind='file')
        link=self.strategy/'link'; link.symlink_to(config)
        self.error('UNSAFE_SYMLINK',strategic_path,link,repo=self.repo,kind='file')
        self.pipes.chmod(0o755)
        self.error('PRIVATE_MODE',fifo_home,self.repo,self.strategy)

    def test_split_runtime_routes_single_wait_and_keeps_all_gates(self):
        self.select_layout()
        materialize(self.repo,self.repo,self.strategy,self.bootstrap)
        cfg=runtime_config(self.strategy/'runtime.env',environ={},repo=self.repo)
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}):
            context=role_context(cfg,'coding')
            self.assertEqual(context['env']['OAP_FIFO_HOME'],str(self.pipes))
            self.error('ACTIVATION_ACK_REQUIRED',role_context,cfg,'coding',operational=True)
            bad=cfg.copy(); bad['OAP_FIFO_HOME']=str(self.strategy)
            self.error('FIFO_HOME_LAYOUT_CONFLICT',role_context,bad,'coding')
            with patch('oap_runtime.role_context',return_value=context),patch('oap_runtime.GitHub',return_value=self.remote),patch('oap_runtime.run_model') as model:
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    done=pool.submit(launch,cfg,'coding',once=True,timeout=3)
                    fifo(self.pipes/'control.fifo','send',timeout=3)
                    self.assertEqual(done.result(4)['state'],'INACTIVE')
                model.assert_not_called()

    def test_doctor_validates_native_fifos_with_selected_sync_modes(self):
        self.select_layout()
        materialize(self.repo,self.repo,self.strategy,self.bootstrap)
        self.strategy.chmod(0o755)
        cfg=runtime_config(self.strategy/'runtime.env',environ={},repo=self.repo)
        with patch.dict(os.environ,{},clear=False):
            result=doctor(self.repo,self.strategy,cfg)
        self.assertEqual(result['bootstrap_structure'],'valid',result['errors'])
        self.assertEqual(result['activation'],'blocked')
        self.assertEqual(result['fifo_home'],str(self.pipes))
        self.assertIn('POSIX private bits not asserted',result['strategic_storage'])
        (self.pipes/'control.fifo').unlink()
        write(self.pipes/'control.fifo','')
        result=doctor(self.repo,self.strategy,cfg)
        self.assertEqual(result['bootstrap_structure'],'invalid')
        self.assertTrue(any('WRONG_TYPE' in e for e in result['errors']))
