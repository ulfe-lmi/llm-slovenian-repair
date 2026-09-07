"""Process-level fakes and isolated tmux integration; no live model or remote."""
import concurrent.futures
import json
import os
from pathlib import Path
import shlex
import shutil
import stat
import subprocess
import sys
import time
import unittest
from unittest.mock import patch
import test_acceptance as base
from support import *
from oap_core import *
from oap_install import *
from oap_runtime import launch, role_context, tmux_plan, tmux_launch


class Processes(unittest.TestCase):
    setUp=base.Acceptance.setUp
    tearDown=base.Acceptance.tearDown
    error=base.Acceptance.error
    private=base.Acceptance.private
    active=base.Acceptance.active
    final=base.Acceptance.final

    def configured_fake(self):
        cfg=self.private()
        fake=self.root/'fake codex š'
        shutil.copyfile(SOURCE/'oap/tests/fake_codex.py',fake); fake.chmod(0o700)
        cfg.update(CODEX_BIN=str(fake),CODING_CODEX_MODEL='synthetic coding model č',STRATEGIC_CODEX_MODEL='synthetic strategic model ž',
                   OAP_ACK_START_LOOP='YES',OAP_ACK_DANGER_FULL_ACCESS='YES',OAP_ROLE_AUTH_READY='YES',
                   OAP_GITHUB_REPOSITORY='synthetic/project',OAP_ACCEPTED_REF=self.base,
                   OAP_MERGE_EFFECT='development-only',OAP_CLI_QUALIFIED_VERSION='codex-cli synthetic-1')
        git(self.repo,'remote','add','origin','https://github.com/synthetic/project.git')
        return cfg,fake

    def test_B28_any_Codex_version_policy_accepts_upgrade(self):
        cfg,fake=self.configured_fake()
        cfg['OAP_CLI_QUALIFIED_VERSION']='ANY'
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}):
            context=role_context(cfg,'coding',operational=True)
        self.assertEqual(context['argv'][context['argv'].index('--model')+1],'synthetic coding model č')
        cfg['OAP_CLI_QUALIFIED_VERSION']='codex-cli older-version'
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}):
            self.error('CLI_VERSION_UNQUALIFIED',role_context,cfg,'coding',operational=True)

    def test_B28_any_policy_still_rejects_unusable_Codex(self):
        cfg,fake=self.configured_fake()
        cfg['OAP_CLI_QUALIFIED_VERSION']='ANY'
        bad=write(self.root/'unusable codex', '#!/usr/bin/env python3\nraise SystemExit(9)\n')
        bad.chmod(0o700)
        cfg['CODEX_BIN']=str(bad)
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}):
            self.error('CLI_UNAVAILABLE',role_context,cfg,'coding',operational=True)

    def test_B11_scoped_backup_refresh_actual(self):
        new=self.root/'fresh'
        materialize(SOURCE,new,self.strategy,self.bootstrap)
        candidate=self.root/'generator-source'
        shutil.copytree(SOURCE,candidate,ignore=shutil.ignore_patterns('.git','__pycache__','*.lock','INSTALLATION.json'))
        old=read(new/'README.md'); write(candidate/'README.md',old+b'\nSynthetic generator revision.\n')
        m=jsread(candidate/'oap/GENERATED-FILES.json')
        m['files']['README.md']['sha256']=digest(read(candidate/'README.md'))
        m['files']['README.md']['bytes']=len(read(candidate/'README.md'))
        write(candidate/'oap/GENERATED-FILES.json',json_bytes(m))
        self.error('INSTALL_CONFLICT',materialize,candidate,new,self.strategy,self.bootstrap)
        materialize(candidate,new,self.strategy,self.bootstrap,refresh=True)
        self.assertEqual(read(new/'README.md'),read(candidate/'README.md'))
        backups=list((self.strategy/'bootstrap-backups').glob('*README.md'))
        self.assertEqual(len(backups),1)
        self.assertEqual(read(backups[0]),old)

    def test_B11_manifest_copy_includes_source_lock_and_owner_files(self):
        new=self.root/'manifest install'
        materialize(SOURCE,new,self.strategy,self.bootstrap)
        self.assertEqual(read(new/'oap/bootstrap-sources.lock.json'),read(SOURCE/'oap/bootstrap-sources.lock.json'))
        self.assertEqual(read(new/'.gitignore'),read(SOURCE/'.gitignore'))
        self.assertEqual(read(new/'LICENSE'),read(SOURCE/'LICENSE'))
        governance(new,strategy=self.strategy)

    def test_B17_B22_competing_locks_and_partial_append(self):
        _,data=self.final(); src=write(self.root/'000-a-synthetic.md',data)
        with lock(self.repo/'oap/.publish.lock'):
            self.error('LOCKED',publish,self.repo,src,'000-a',accepted_ref=self.base,remote=self.remote)
        self.assertIsNone(active_id(self.repo))
        payload=entry(); self.active('000-b',pr=1,decision='D1',payload=payload)
        ep=write(self.root/'entry.md',payload)
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}):
            with lock(self.repo/'oap/.critical.lock'):
                self.error('LOCKED',append_critical,self.repo,ep,'CRIT-0001',accepted_ref=self.base)
            write(self.repo/'CRITICAL.md',read(self.repo/'CRITICAL.md')+payload[:31])
            self.error('CRITICAL_STALE_OR_REWRITTEN',append_critical,self.repo,ep,'CRIT-0001',accepted_ref=self.base)

    def test_B18_send_short_io(self):
        p=self.root/'pipe'; os.mkfifo(p,0o600)
        actual=os.write
        def short(fd,data): return actual(fd,bytes(data)[:1])
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future=pool.submit(fifo,p,'wait',timeout=3)
            with patch('oap_core.os.write',side_effect=short):
                self.assertEqual(fifo(p,'send',timeout=3)['bytes'],2)
            self.assertEqual(future.result(4)['frame'],'OK')

    def test_B19_B29_one_actual_fake_invocation_after_real_FIFO(self):
        cfg,fake=self.configured_fake(); self.active()
        capture=self.root/'capture.jsonl'
        with patch.dict(os.environ,{'OAP_ROLE':'coding','FAKE_CODEX_CAPTURE':str(capture)}),patch('oap_runtime.GitHub',return_value=self.remote):
            def model(context):
                p=subprocess.run(context['argv'],cwd=context['cwd'],env=context['env'],capture_output=True)
                report(self.repo,self.remote)
                return p
            with patch('oap_runtime.run_model',side_effect=model) as run:
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future=pool.submit(launch,cfg,'coding',once=True,timeout=5)
                    time.sleep(.15)
                    self.assertFalse(capture.exists())
                    fifo(self.strategy/'control.fifo','send',timeout=3)
                    result=future.result(8)
                self.assertEqual(result['model_calls'],1)
                run.assert_called_once()
        rows=[json.loads(l) for l in read(capture).decode().splitlines()]
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['cwd'],str(self.repo))
        self.assertEqual(rows[0]['home'],cfg['CODING_CODEX_HOME'])
        self.assertEqual(rows[0]['role'],'coding')
        self.assertIn('--ephemeral',rows[0]['argv'])
        self.assertNotIn('canonical PLAN.md',rows[0]['read_set'])

    def test_B27_live_shell_returns_after_fake_CLI_exit(self):
        cfg=self.private()
        fake=self.root/'fake model'; shutil.copyfile(SOURCE/'oap/tests/fake_codex.py',fake); fake.chmod(0o700)
        for role in ('coding','strategic'):
            env=os.environ.copy()
            for key in ENV_KEYS | {'CODEX_HOME'}:
                env.pop(key, None)
            env.update(OAP_ROLE=role,FAKE_CODEX_EXIT='7')
            code=shlex.join([str(fake)])+"\nprintf 'SHELL_SURVIVED:%s:%s:%s\\n' \"$OAP_ROLE\" \"$PWD\" \"$CODEX_HOME\"\nexit\n"
            p=subprocess.run(['bash',str(self.repo/'oap/bin/launch-role-setup-shell.sh'),'--config',str(self.strategy/'runtime.env'),'--role',role],input=code,text=True,capture_output=True,env=env,timeout=8)
            self.assertEqual(p.returncode,0,p.stderr)
            expected=self.repo if role=='coding' else self.strategy
            self.assertIn(f'SHELL_SURVIVED:{role}:{expected}:{cfg[role.upper()+"_CODEX_HOME"]}',p.stdout)

    def test_B27_actual_isolated_tmux_panes_and_cleanup(self):
        if not shutil.which('tmux'): self.skipTest('tmux absent: real pane integration NOT RUN')
        cfg=self.private(); sock='oap-fixture-'+self.root.name
        with patch.dict(os.environ,{'OAP_ROLE':'strategic'}):
            plan=tmux_plan(cfg,False,config_path=self.strategy/'runtime.env')
        def run(args,check=True):
            p=subprocess.run(['tmux','-L',sock,*args],capture_output=True,text=True,timeout=5)
            if check: self.assertEqual(p.returncode,0,p.stderr)
            return p
        try:
            for cmd in plan['commands'][:-1]: run(cmd[1:])
            panes=run(['list-panes','-t',plan['session'],'-F','#{pane_index}|#{pane_current_path}|#{pane_left}']).stdout.splitlines()
            self.assertEqual(len(panes),2)
            self.assertIn(str(self.repo),panes[0]); self.assertIn(str(self.strategy),panes[1])
            self.assertEqual(panes[0].split('|')[-1],'0')
            self.assertGreater(int(panes[1].split('|')[-1]),0)
            marker=run(['show-option','-v','-t',plan['session'],'@oap_project']).stdout.strip()
            self.assertEqual(marker,plan['project_marker'])
        finally:
            run(['kill-server'],check=False)
        self.assertNotEqual(run(['has-session'],check=False).returncode,0)

    def test_B29_unrelated_tmux_session_refused(self):
        cfg=self.private()
        def fake_run(argv,**kwargs):
            if 'has-session' in argv: return subprocess.CompletedProcess(argv,0,'','')
            if 'show-options' in argv: return subprocess.CompletedProcess(argv,0,'OTHER PROJECT\n','')
            raise AssertionError('unexpected session mutation')
        with patch('oap_runtime.subprocess.run',side_effect=fake_run):
            self.error('UNRELATED_TMUX_SESSION',tmux_launch,cfg,False,self.strategy/'runtime.env')

    def test_B20_B31_fake_gh_executable_contract(self):
        self.active(); _,head,_=report(self.repo,self.remote)
        data={f'repos/synthetic/project/pulls/1':self.remote.prs[1]}
        data.update({'repos/synthetic/project/'+k:v for k,v in self.remote.responses.items()})
        responses=write(self.root/'gh.json',json_bytes(data))
        fake=self.root/'gh fake'; shutil.copyfile(SOURCE/'oap/tests/fake_gh.py',fake); fake.chmod(0o700)
        with patch.dict(os.environ,{'FAKE_GH_RESPONSES':str(responses)}):
            remote=GitHub('synthetic/project',str(fake))
            self.assertEqual(verify_report(self.repo,'000-a',remote=remote)['scope'],'remote')

    def test_B10_helper_help_and_real_entry_failures(self):
        for path in (self.repo/'oap/bin').iterdir():
            if path.suffix not in ('.py','.sh') or path.name.startswith('oap_') and path.name not in ('oap_cli.py','oap_fifo.py'): continue
            prefix=['bash'] if path.suffix=='.sh' else [sys.executable,'-B']
            p=subprocess.run([*prefix,str(path),'--help'],capture_output=True,timeout=5)
            self.assertEqual(p.returncode,0,(path.name,p.stderr[:120]))
            self.assertIn(b'usage:',p.stdout.lower())
        p=subprocess.run([sys.executable,'-B',str(self.repo/'oap/bin/check_state.py'),'--repo-root',str(self.repo)],capture_output=True,timeout=5)
        self.assertEqual(json.loads(p.stdout)['state'],'INACTIVE')
        write(self.repo/'oap/active',b'000-a')
        p=subprocess.run([sys.executable,'-B',str(self.repo/'oap/bin/check_state.py'),'--repo-root',str(self.repo)],capture_output=True,timeout=5)
        self.assertEqual(p.returncode,2)
        self.assertEqual(json.loads(p.stderr)['error'],'INVALID_ACTIVE')

    def test_B19_strategic_prompt_starts_inactive_development_loop(self):
        prompt=read(SOURCE/'oap/prompts/strategic-start.md').decode()
        self.assertIn('passed the operational launch gates',prompt)
        self.assertIn('state is INACTIVE',prompt)
        self.assertIn('finalize objective 000-a',prompt)
        self.assertIn('send the exact control signal',prompt)
        self.assertIn('live repair testing',prompt)
        self.assertIn('release and deployment retain their separate gates',prompt)
        self.assertNotIn('Bootstrap activation is disabled',prompt)

    def test_B16_extended_transitions_same_PR(self):
        for old,new in [('000-z','000-aa'),('000-az','000-ba')]:
            self.active(old,pr=1); report(self.repo,self.remote,old)
            m,data=self.final(new,pr=1)
            transition(self.repo,validate_order(data,self.repo),self.remote)
            m['pr']=2
            self.error('SAME_PR_REQUIRED',transition,self.repo,validate_order(replace_metadata(data,m),self.repo),self.remote)

    def test_B22_mitigation_append_preserves_gate(self):
        write(self.repo/'CRITICAL.md',read(self.repo/'CRITICAL.md')+entry())
        self.base=commit(self.repo,'Synthetic prior judgment')
        payload=mitigation()
        self.active('000-c',pr=1,payload=payload,action='UPDATE')
        src=write(self.root/'mitigation.md',payload)
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}):
            append_critical(self.repo,src,'CRIT-0001',accepted_ref=self.base)
        state=critical_state(read(self.repo/'CRITICAL.md'))
        self.assertEqual(state['mitigation_updates'],['CRIT-0001'])
        self.assertEqual(state['open'],['CRIT-0001'])

    def test_B32_matrix_cannot_redefine_audited_scope(self):
        m=metadata(read(self.repo/'oap/audit/ICA-REPORT-TEMPLATE.md'),'oap-ica')
        m.update(status='FINAL',main_sha=self.base,architecture_sha256=digest(read(self.repo/'ARCHITECTURE.md')),
                 plan_sha256=digest(read(self.repo/'PLAN.md')),auditor='Synthetic independent fixture',context_provenance='new synthetic context')
        path=write(self.root/'audit.md',b'```oap-ica\n'+json_bytes(m)+b'```\n')
        write(self.repo/'oap/audit/requirements.json',b'[]\n')
        self.error('ICA_MATRIX_SOURCE_DRIFT',check_ica,self.repo,path,self.base)
