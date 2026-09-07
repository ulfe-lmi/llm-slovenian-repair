"""Repeatable B01–B36 acceptance, using real filesystem/Git/FIFOs and fake edges."""
import concurrent.futures
import contextlib
import copy
import json
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
from support import *
from oap_install import materialize, env_bytes, runtime_defaults, runtime_config, refresh_governance
from oap_runtime import role_context, launch, setup_shell, tmux_plan, tmux_launch
from oap_cli import doctor


def bootstrap_ignore(directory, names):
    relative = Path(directory).relative_to(SOURCE)
    ignored = {name for name in names if name in ('.git', '__pycache__', 'INSTALLATION.json') or name.endswith('.lock')}
    if relative == Path('oap'):
        ignored.add('active')
    if relative == Path('oap/orders'):
        ignored.update(name for name in names if name.endswith('.md'))
    if relative == Path('oap/reports'):
        ignored.update(name for name in names if name.endswith('.md'))
    return ignored


def snapshot(root):
    result = {}
    if root.exists():
        for p in root.rglob('*'):
            s=p.lstat()
            result[str(p.relative_to(root))]=(s.st_mode,s.st_mtime_ns, digest(p.read_bytes()) if p.is_file() else None)
    return result


class Acceptance(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='oap-owned-fixture-')
        self.root = Path(self.temp.name)
        self.repo = self.root/'coding ž space'
        shutil.copytree(SOURCE,self.repo,ignore=bootstrap_ignore)
        self.strategy = self.root/'strategy š space'
        self.bootstrap = self.root/'bootstrap č'
        self.bootstrap.mkdir()
        git(self.repo,'init','-b','main')
        git(self.repo,'config','user.name','Synthetic OAP fixture')
        git(self.repo,'config','user.email','synthetic@example.invalid')
        self.base = commit(self.repo,'Synthetic accepted baseline')
        self.remote = FakeGitHub(self.repo)
        self.remote.responses['branches/main']={'commit':{'sha':self.base}}
        self.env = patch.dict(os.environ,{'OAP_ROLE':'strategic'})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def error(self, code, fn, *args, **kwargs):
        with self.assertRaises(OAPError) as cm:
            fn(*args,**kwargs)
        self.assertEqual(cm.exception.code,code)

    def final(self, ident='000-a', **kw):
        return order(self.repo,self.base,ident,**kw)

    def private(self):
        materialize(SOURCE,self.repo,self.strategy,self.bootstrap)
        return runtime_config(self.strategy/'runtime.env',environ={})

    def active(self, ident='000-a', **kw):
        m,data=self.final(ident,**kw)
        install_order(self.repo,data,ident)
        return m,data

    def B01_source_integrity(self):
        for row in jsread(self.repo/'oap/bootstrap-sources.lock.json')['sources']:
            b=read(self.repo/row['installed'])
            self.assertEqual((len(b),digest(b)),(row['bytes'],row['sha256']))
        for p in ('PLAN.md','ARCHITECTURE.md','CRITICAL.md'):
            self.assertEqual(read(self.repo/p),read(self.repo/'docs/bootstrap'/p))
        governance(self.repo)

    def B02_topology_and_owner(self):
        topology(self.bootstrap,self.repo,self.strategy)
        self.error('NESTED_ROOTS',topology,self.bootstrap,self.repo,self.repo/'nested')
        link=self.root/'alias'; link.symlink_to(self.repo)
        self.error('UNSAFE_SYMLINK',topology,self.bootstrap,link,self.strategy)
        original=Path.lstat
        def wrong(p):
            s=original(p)
            if p==self.repo:
                fields=list(s); fields[4]=54321
                return os.stat_result(fields)
            return s
        with patch.object(Path,'lstat',wrong):
            self.error('WRONG_ANCESTOR_OWNER',safe_path,self.repo)

    def B03_router_and_unknown_role(self):
        b=read(self.repo/'AGENTS.md')
        self.assertLessEqual(len(b),2048)
        for v in (b'CODING:',b'STRATEGIC:',b'Missing/conflicting role'):
            self.assertIn(v,b)
        for v in (b'LR-001',b'BOOTSTRAP GENERATOR',b'56 objectives'):
            self.assertNotIn(v,b)
        cfg=self.private()
        self.error('UNKNOWN_ROLE',role_context,cfg,'unknown')

    def B04_full_and_dense(self):
        self.private()
        full=read(self.repo/'oap/strategic-instructions/AGENTS.md')
        self.assertEqual(full,read(self.strategy/'AGENTS.md'))
        self.assertGreater(len(full),len(read(self.repo/'oap/coding-instructions/AGENTS.md'))*1.5)
        for marker in ('S-DECIDE-03','S-MERGE-01','S-ICA-02','S-PRODUCT-04'):
            self.assertIn(marker,full.decode())
        self.assertNotEqual(full,read(self.repo/'docs/bootstrap/BOOTSTRAP-GENERATOR.md'))

    def B05_transitive_read_set_and_exceptions(self):
        cfg=self.private()
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}):
            c=role_context(cfg,'coding')
        self.assertEqual(c['read_set'][:4],READ_SET[:4])
        self.assertNotIn('PLAN.md',c['read_set'])
        self.assertNotIn('CRITICAL.md',c['read_set'])
        self.assertNotIn('ARCHITECTURE.md',c['read_set'])
        m=jsread(self.repo/'oap/governance/MANIFEST.json')
        m['coding_read_set'].append('PLAN.md')
        write(self.repo/'oap/governance/MANIFEST.json',json_bytes(m))
        self.error('GOVERNANCE_READ_SET',governance,self.repo)
        self.assertIn('bounded full-source',read(self.repo/'oap/coding-instructions/AGENTS.md').decode())

    def B06_role_retention(self):
        cfg=self.private()
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}):
            coding=role_context(cfg,'coding')
            # Reading foreign law is data; it does not mutate role or routing.
            read(self.repo/'oap/strategic-instructions/AGENTS.md')
            self.assertEqual(coding['env']['OAP_ROLE'],'coding')
            self.error('CONFLICTING_ROLE',role_context,cfg,'strategic')
        c=role_context(cfg,'strategic')
        read(self.repo/'AGENTS.md')
        self.assertEqual(c['env']['OAP_ROLE'],'strategic')
        self.assertEqual(c['cwd'],str(self.strategy))

    def B07_distillation_drift_and_coverage(self):
        m=jsread(self.repo/'oap/governance/MANIFEST.json')
        self.assertTrue({f'LR-{i:03}' for i in range(1,15)}.issubset(m['coverage']))
        path=self.repo/'ARCHITECTURE-for-agents.md'
        old=read(path); write(path,old+b'changed')
        self.error('GOVERNANCE_DRIFT',governance,self.repo)
        write(path,old)
        m['coverage']['MISSING-CLAUSE']={'file':'AGENTS.md','source':'synthetic source','comparison':'not a proof'}
        write(self.repo/'oap/governance/MANIFEST.json',json_bytes(m))
        self.error('MISSING_COMPACT_CLAUSE',governance,self.repo)
        self.assertIn('generator semantic review',read(self.repo/'oap/governance/DISTILLATION-MAP.md').decode())

    def B08_exact_budgets(self):
        m=jsread(self.repo/'oap/governance/MANIFEST.json')
        self.assertEqual(m['coding_bytes'],sum(len(read(self.repo/p)) for p in READ_SET))
        self.assertEqual(m['tokens'],'UNMEASURED')
        for rel,limit in zip(READ_SET[:4],[2048,12000,20000,10000]):
            self.assertLessEqual(len(read(self.repo/rel)),limit)
        self.assertLessEqual(m['coding_bytes'],50000)

    def B09_canonical_reference_no_reseed(self):
        self.private()
        for p in ('PLAN.md','ARCHITECTURE.md','CRITICAL.md'):
            self.assertFalse((self.strategy/p).exists())
            self.assertIn(str(self.repo/p),read(self.strategy/'SOURCE-REFERENCES.md').decode())
        (self.repo/'CRITICAL.md').unlink()
        self.error('MISSING_PATH',governance,self.repo)
        self.error('MISSING_LIVE_REGISTER_NO_RESEED',materialize,SOURCE,self.repo,self.strategy,self.bootstrap)
        self.assertFalse((self.repo/'CRITICAL.md').exists())

    def B10_inventory_links_drafts(self):
        docs=list((self.repo/'oap/strategic-instructions/initial-orders').glob('*.md'))
        self.assertEqual(len(docs),56)
        idx=jsread(self.repo/'oap/strategic-instructions/draft-index.json')
        self.assertEqual([r['id'] for r in idx],[f'{i:03}-a' for i in range(56)])
        for p in docs:
            data=read(p).decode()
            self.assertGreater(len(data.split()),450)
            for s in ORDER_SECTIONS:
                self.assertIn(s,section_map(data))
        self.assertGreater(len(jsread(self.repo/'oap/audit/requirements.json')),50)
        for p in self.repo.rglob('*.md'):
            if 'docs/bootstrap/' in str(p): continue
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',read(p).decode()):
                if '://' in target or target.startswith('#'): continue
                self.assertTrue((p.parent/target.split('#')[0]).exists(),(p,target))

    def B11_materializer_dry_noop_refresh(self):
        new=self.root/'fresh repo'
        before=snapshot(self.root)
        materialize(SOURCE,new,self.strategy,self.bootstrap,dry_run=True)
        self.assertEqual(before,snapshot(self.root))
        materialize(SOURCE,new,self.strategy,self.bootstrap)
        before=snapshot(self.root)
        materialize(SOURCE,new,self.strategy,self.bootstrap)
        self.assertEqual(before,snapshot(self.root))
        private=self.strategy/'drafts'/jsread(SOURCE/'oap/strategic-instructions/draft-index.json')[0]['path']
        write(private,'Human edited private draft\n')
        write(new/'unrelated.txt','keep me')
        materialize(SOURCE,new,self.strategy,self.bootstrap,refresh=True)
        self.assertEqual(read(private),b'Human edited private draft\n')
        self.assertEqual(read(new/'unrelated.txt'),b'keep me')

    def B12_worktree_unicode_dirty_fifo(self):
        wt=self.root/'linked worktree š'
        git(self.repo,'worktree','add','-b','fixture-linked',str(wt))
        self.assertTrue((wt/'.git').is_file())
        write(wt/'untracked.txt','preserve')
        from oap_install import inspect_repository
        self.assertEqual(inspect_repository(wt)['git'],'worktree')
        self.assertTrue(inspect_repository(wt)['dirty'])
        self.strategy.mkdir(mode=0o700)
        write(self.strategy/'control.fifo','not a FIFO')
        self.error('WRONG_TYPE',materialize,SOURCE,self.repo,self.strategy,self.bootstrap)
        self.assertEqual(read(self.strategy/'control.fifo'),b'not a FIFO')
        self.assertEqual(read(wt/'untracked.txt'),b'preserve')

    def B13_inactive_invalid_pointer(self):
        self.assertEqual(protocol_state(self.repo)['state'],'INACTIVE')
        for bad in (b'',b'000-a',b'000-a\n\n',b'000-a \n',b'000-A\n',b'000-a\n001-a\n'):
            write(self.repo/'oap/active',bad)
            self.error('INVALID_ACTIVE',protocol_state,self.repo)
        write(self.repo/'oap/active',b'000-a\n')
        self.error('ACTIVE_ORDER_MISSING',protocol_state,self.repo)

    def B14_order_schema_negative_metadata(self):
        m,data=self.final()
        validate_order(data,self.repo,'000-a','000-a-synthetic.md')
        cases=[('status','DRAFT','ORDER_NOT_FINAL'),('base_sha','VERIFY','ORDER_BASE_SHA'),
               ('provenance',[],'MISSING_PROVENANCE'),('governance',{},'ORDER_GOVERNANCE_IDENTITY'),
               ('title','VERIFY title','ORDER_UNRESOLVED_FIELD'),('objective','001','OBJECTIVE_MISMATCH')]
        for key,value,code in cases:
            changed=copy.deepcopy(m); changed[key]=value
            self.error(code,validate_order,replace_metadata(data,changed),self.repo)
        self.error('ORDER_FILENAME',validate_order,data,self.repo,'000-a','000-b-other.md')
        self.error('ORDER_SECTION',validate_order,data.replace(b'## Scope\n',b'## Removed scope\n'),self.repo)
        # Actual quoted test material may contain TODO, without becoming current state.
        validate_order(data.replace(b'## Requirements\n',b'## Requirements\n```text\nTODO synthetic fixture\n```\n'),self.repo)

    def B15_DHA_all_fields_and_D2(self):
        m,data=self.final()
        validate_order(data,self.repo)
        self.error('DHA_DECLARATION',validate_order,data.replace(b'- Decision: NONE',b'- Decision: MAYBE'),self.repo)
        for key in CRIT_FIELDS:
            b=entry().replace(('- **'+key+':**').encode(),('- **wrong '+key+':**').encode())
            self.error('CRITICAL_FIELD',critical_payload,b,'CRIT-0001')
        for section in CRIT_SECTIONS:
            b=entry().replace(('### '+section+'\n').encode(),('### missing '+section+'\n').encode())
            self.error('CRITICAL_SECTIONS',critical_payload,b,'CRIT-0001')
        b=entry().replace(b'ALL FIVE CRITICAL-ENTRY CONDITIONS SATISFIED',b'not attested')
        self.error('CRITICAL_ATTESTATION',critical_payload,b,'CRIT-0001')
        m['decision_class']='D2'
        self.error('D2_BOUNDARY_BLOCKED',validate_order,replace_metadata(data,m),self.repo)
        m.update(safe_preparation=True,real_boundary_blocked=True)
        validate_order(replace_metadata(data,m),self.repo)

    def B16_suffix_and_PR_continuity(self):
        for a,b in [('a','b'),('z','aa'),('az','ba')]:
            self.assertEqual(suffix_next(a),b)
        self.error('SUFFIX_EXHAUSTED',suffix_next,'zz')
        self.active(); report(self.repo,self.remote)
        m,data=self.final('000-b',pr=1)
        transition(self.repo,validate_order(data,self.repo),self.remote)
        m['branch']='other-branch'
        self.error('SAME_PR_REQUIRED',transition,self.repo,validate_order(replace_metadata(data,m),self.repo),self.remote)
        m,data=self.final('000-c',pr=1)
        self.error('ROUND_SEQUENCE',transition,self.repo,validate_order(data,self.repo),self.remote)

    def B17_publish_crash_retry_no_replay(self):
        _,data=self.final(); src=write(self.root/'000-a-synthetic.md',data)
        before=snapshot(self.repo)
        publish(self.repo,src,'000-a',accepted_ref=self.base,remote=self.remote,dry_run=True)
        self.assertEqual(before,snapshot(self.repo))
        def crash(stage): raise OAPError('SYNTHETIC_CRASH')
        self.error('SYNTHETIC_CRASH',publish,self.repo,src,'000-a',accepted_ref=self.base,remote=self.remote,fault=crash)
        self.assertTrue(matching(self.repo,'orders','000-a'))
        self.assertIsNone(active_id(self.repo))
        publish(self.repo,src,'000-a',accepted_ref=self.base,remote=self.remote)
        self.assertEqual(active_id(self.repo),'000-a')
        report(self.repo,self.remote)
        self.error('COMPLETED_REPLAY',publish,self.repo,src,'000-a',accepted_ref=self.base,remote=self.remote)

    def B18_real_fifo_framing(self):
        path=self.root/'synthetic.fifo'; os.mkfifo(path,0o600)
        def trial(chunks):
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future=pool.submit(fifo,path,'wait',timeout=3)
                fd=os.open(path,os.O_WRONLY)
                try:
                    for chunk in chunks:
                        os.write(fd,chunk)
                        time.sleep(.01)
                finally: os.close(fd)
                return future.result(4)
        self.assertEqual(trial([b'O',b'K'])['bytes'],2)
        for chunks in ([b'O'],[b'ok'],[b'OK\n'],[b'OKx']):
            self.error('FIFO_INVALID_FRAME',trial,chunks)
        self.error('FIFO_EMPTY_FRAME',trial,[])
        self.error('FIFO_TIMEOUT',fifo,path,'wait',timeout=.04)
        proc=subprocess.Popen([sys.executable,'-B',str(SOURCE/'oap/bin/oap_fifo.py'),'wait','--fifo',str(path)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        # Wait for the actual FIFO reader, including on a slower source mount,
        # rather than interrupting Python during imports before main's handler.
        import errno
        deadline=time.monotonic()+5
        ready_fd=None
        try:
            while ready_fd is None:
                try:
                    ready_fd=os.open(path,os.O_WRONLY|os.O_NONBLOCK)
                except OSError as exc:
                    if exc.errno!=errno.ENXIO: raise
                    self.assertLess(time.monotonic(),deadline,'FIFO reader did not start')
                    time.sleep(.01)
            proc.send_signal(signal.SIGINT)
            out,err=proc.communicate(timeout=3)
        finally:
            if ready_fd is not None: os.close(ready_fd)
            if proc.poll() is None:
                proc.kill(); proc.communicate(timeout=3)
        self.assertEqual(proc.returncode,130)
        self.assertIn(b'INTERRUPTED',err)

    def B19_single_control_and_duplicate_suppression(self):
        cfg=self.private()
        self.active(); report(self.repo,self.remote)
        context={'argv':['synthetic-model'],'cwd':str(self.repo),'env':{},'role':'coding'}
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}), patch('oap_runtime.role_context',return_value=context), patch('oap_runtime.GitHub',return_value=self.remote), patch('oap_runtime.fifo') as consume, patch('oap_runtime.run_model') as model:
            result=launch(cfg,'coding',once=True)
            self.assertEqual(result['model_calls'],0)
            consume.assert_called_once()
            model.assert_not_called()
        self.assertNotIn('control.fifo',read(self.repo/'oap/prompts/coding-round.md').decode())

    def B20_SELF_real_git_parent_and_only_path(self):
        self.active(); _,head,rp=report(self.repo,self.remote)
        self.assertEqual(verify_report(self.repo,'000-a',remote=self.remote)['scope'],'remote')
        self.assertEqual(verify_report(self.repo,'000-a')['scope'],'local only')
        original=read(rp); write(rp,original+b'forgery')
        self.error('REPORT_CONTENT_DRIFT',verify_report,self.repo,'000-a')
        write(rp,original)
        self.remote.prs[1]['head']['sha']=self.base
        self.error('REMOTE_HEAD_MISMATCH',verify_report,self.repo,'000-a',remote=self.remote)

    def B20b_SELF_reject_extra_and_wrong_parent(self):
        self.active(); report(self.repo,self.remote,extra=True)
        self.error('REPORT_ONLY_PATH',verify_report,self.repo,'000-a')

    def B20c_SELF_wrong_parent(self):
        self.active(); report(self.repo,self.remote,parent=self.base)
        self.error('REPORT_PARENT',verify_report,self.repo,'000-a')

    def B21_publication_chronology(self):
        _,od=self.active(); _,_,rp=report(self.repo,self.remote)
        r=metadata(read(rp),'oap-report'); o=validate_order(od,self.repo)
        r['publication_verified']=True
        self.error('FUTURE_PUBLICATION_CLAIM',validate_report,replace_metadata(read(rp),r,'oap-report'),o,od,'oap/orders/000-a-synthetic.md')
        r['publication_verified']=False; r['checks'][0]['publication_head_claim']=True
        self.error('FUTURE_CI_CLAIM',validate_report,replace_metadata(read(rp),r,'oap-report'),o,od,'oap/orders/000-a-synthetic.md')
        self.remote.prs[1]['created_at']='2026-09-06T10:02:00Z'
        self.error('PR_CREATED_AFTER_REPORT',verify_report,self.repo,'000-a',remote=self.remote)

    def B22_exact_critical_append_crash_and_idempotence(self):
        payload=entry(); self.active('000-b',pr=1,decision='D1',payload=payload)
        source=write(self.root/'entry.md',payload)
        prior=read(self.repo/'CRITICAL.md')
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}):
            append_critical(self.repo,source,'CRIT-0001',accepted_ref=self.base,dry_run=True)
            self.assertEqual(read(self.repo/'CRITICAL.md'),prior)
            def crash(stage):
                if stage=='after-append': raise OAPError('SYNTHETIC_CRASH')
            self.error('SYNTHETIC_CRASH',append_critical,self.repo,source,'CRIT-0001',accepted_ref=self.base,fault=crash)
            self.assertEqual(read(self.repo/'CRITICAL.md'),prior+payload)
            self.assertEqual(append_critical(self.repo,source,'CRIT-0001',accepted_ref=self.base)['result'],'already applied')
        self.assertEqual(critical_state(prior+payload)['ids'],['CRIT-0001'])

    def B23_critical_reject_invented_human_and_history(self):
        payload=entry(); self.active('000-b',pr=1,decision='D1',payload=payload)
        source=write(self.root/'entry.md',payload+b'changed')
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}):
            self.error('APPEND_BYTES_MISMATCH',append_critical,self.repo,source,'CRIT-0001',accepted_ref=self.base)
            write(source,payload)
            write(self.repo/'CRITICAL.md',read(self.repo/'CRITICAL.md')[:-2])
            self.error('CRITICAL_STALE_OR_REWRITTEN',append_critical,self.repo,source,'CRIT-0001',accepted_ref=self.base)
        self.error('AGENT_HUMAN_DISPOSITION',critical_payload,payload+human(),'CRIT-0001')
        self.error('DUPLICATE_CRITICAL_ID',critical_state,entry()+entry().replace(b'Synthetic contained choice',b'Another title'))

    def B24_human_values_latest_provenance(self):
        for decision in DISPOSITIONS:
            state=critical_state(entry()+human(decision))
            self.assertEqual(state['latest_human']['CRIT-0001']['decision'],decision)
            self.assertEqual(state['accepted'],[])
        self.error('HUMAN_DISPOSITION_VALUE',critical_state,entry()+human('SUPERSEDED'))
        first=human('ACCEPTED')
        # Explicit synthetic trusted provenance exercises mechanics, not owner authority.
        h=digest(first.lstrip(b'\n'))
        self.assertEqual(critical_state(entry()+first,verified_humans=[h])['accepted'],['CRIT-0001'])
        for decision in ('REJECTED','CHANGE REQUIRED','DEFERRED'):
            state=critical_state(entry()+first+human(decision,'2026-09-08'),verified_humans=[h])
            self.assertEqual(state['open'],['CRIT-0001'])
        self.assertEqual(critical_state(entry()+mitigation())['open'],['CRIT-0001'])

    def B25_scoped_gate_continuation(self):
        state=critical_state(entry())
        gate(state,[])
        self.error('OPEN_HUMAN_GATE',gate,state,['CRIT-0001'])
        self.error('UNKNOWN_CRITICAL_GATE',gate,state,['CRIT-9999'])
        self.error('SEPARATE_HUMAN_AUTHORITY_REQUIRED',gate,state,[],external=True)

    def B26_candidate_trusted_base_and_private_refresh(self):
        self.private()
        source='oap/strategic-instructions/AGENTS.md'
        old=read(self.repo/source); write(self.repo/source,old+b'\nS-FIXTURE-01. Synthetic accepted evolution.\n')
        m=jsread(self.repo/'oap/governance/MANIFEST.json')
        m['identities'][source]={'sha256':digest(read(self.repo/source)),'bytes':len(read(self.repo/source))}
        map_path=self.repo/'oap/governance/DISTILLATION-MAP.md'
        write(map_path,read(map_path).replace(digest(old).encode(),digest(read(self.repo/source)).encode()))
        m['identities']['oap/governance/DISTILLATION-MAP.md']={'sha256':digest(read(map_path)),'bytes':len(read(map_path))}
        write(self.repo/'oap/governance/MANIFEST.json',json_bytes(m))
        self.error('UNACCEPTED_GOVERNANCE',governance,self.repo,'accepted-runtime',self.base)
        self.error('UNORDERED_GOVERNANCE_CHANGE',governance,self.repo,'candidate-review',self.base)
        governance(self.repo,'candidate-review',self.base,[source,'oap/governance/DISTILLATION-MAP.md','oap/governance/MANIFEST.json'],self.strategy)
        accepted=commit(self.repo,'Synthetic reviewed governance merge')
        private_path=self.strategy/'drafts'/jsread(SOURCE/'oap/strategic-instructions/draft-index.json')[0]['path']
        write(private_path,'Human private draft')
        refresh_governance(self.repo,self.strategy,accepted)
        self.assertEqual(read(self.strategy/'AGENTS.md'),read(self.repo/source))
        self.assertEqual(read(private_path),b'Human private draft')
        self.assertTrue(list((self.strategy/'bootstrap-backups').iterdir()))
        governance(self.repo,'accepted-runtime',accepted,strategy=self.strategy)

    def B27_setup_shell_plan_no_model(self):
        cfg=self.private()
        before=snapshot(self.strategy)
        with patch.dict(os.environ,{},clear=True):
            # Plan function only needs inherited PATH for tmux discovery.
            os.environ['PATH']='/usr/bin:/bin'
            plan=tmux_plan(cfg,False,config_path=self.strategy/'runtime.env')
            for role in ('coding','strategic'):
                out=setup_shell(cfg,role,print_only=True)
                self.assertFalse(out['model_started'])
        self.assertIn('-h',plan['commands'][2])
        self.assertEqual([r['cwd'] for r in plan['roles']],[str(self.repo),str(self.strategy)])
        self.assertNotEqual(plan['roles'][0]['home'],plan['roles'][1]['home'])
        self.assertNotIn('--dangerously',str(plan))
        self.assertEqual(before,snapshot(self.strategy))

    def B28_operation_gates_and_quoting(self):
        cfg=self.private()
        self.error('ACTIVATION_ACK_REQUIRED',role_context,cfg,'strategic',operational=True)
        cfg.update(OAP_ACK_DANGER_FULL_ACCESS='YES',OAP_ACK_START_LOOP='YES',OAP_ROLE_AUTH_READY='YES')
        self.error('EXPLICIT_MODEL_OR_PROFILE_REQUIRED',role_context,cfg,'strategic',operational=True)
        cfg['STRATEGIC_CODEX_MODEL']='synthetic model š;$(never)'
        self.error('REMOTE_BASELINE_REQUIRED',role_context,cfg,'strategic',operational=True)
        cfg.update(OAP_GITHUB_REPOSITORY='synthetic/project',OAP_ACCEPTED_REF=self.base,OAP_MERGE_EFFECT='development-only',OAP_CLI_QUALIFIED_VERSION='codex-cli synthetic-1')
        fake=self.root/'fake codex ž'; shutil.copyfile(SOURCE/'oap/tests/fake_codex.py',fake); fake.chmod(0o700)
        cfg['CODEX_BIN']=str(fake)
        git(self.repo,'remote','add','origin','https://github.com/synthetic/project.git')
        c=role_context(cfg,'strategic',operational=True)
        self.assertEqual(c['argv'][c['argv'].index('--model')+1],cfg['STRATEGIC_CODEX_MODEL'])
        self.assertFalse((self.root/'never').exists())

    def B29_idle_nonzero_locks_no_resurrection(self):
        cfg=self.private(); self.active()
        context={'argv':['synthetic-model'],'cwd':str(self.repo),'env':{},'role':'coding'}
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}),patch('oap_runtime.role_context',return_value=context),patch('oap_runtime.GitHub',return_value=self.remote),patch('oap_runtime.fifo',side_effect=OAPError('FIFO_TIMEOUT')),patch('oap_runtime.run_model') as model:
            self.error('FIFO_TIMEOUT',launch,cfg,'coding',once=True)
            model.assert_not_called()
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}),patch('oap_runtime.role_context',return_value=context),patch('oap_runtime.GitHub',return_value=self.remote),patch('oap_runtime.fifo'),patch('oap_runtime.run_model',return_value=subprocess.CompletedProcess([],7)) as model:
            self.error('CODING_EXIT_RECOVERY',launch,cfg,'coding',once=True)
            model.assert_called_once()
            self.assertEqual(jsread(self.strategy/'workorders/incident.json')['exit_code'],7)
        with lock(self.strategy/'.coding.lock'):
            self.error('LOCKED',lambda: lock_probe(self.strategy/'.coding.lock'))

    def B30_recovery_same_id_and_unpublished_report(self):
        cfg=self.private(); self.active()
        write(self.strategy/'workorders/consumed.json',json_bytes({'id':'000-a'}))
        self.assertEqual(protocol_state(self.repo,strategy=self.strategy)['state'],'RECOVERY_REQUIRED')
        context={'argv':['synthetic-model'],'cwd':str(self.repo),'env':{},'role':'coding'}
        with patch.dict(os.environ,{'OAP_ROLE':'coding'}),patch('oap_runtime.role_context',return_value=context),patch('oap_runtime.GitHub',return_value=self.remote),patch('oap_runtime.fifo'),patch('oap_runtime.run_model') as model:
            self.error('EXPLICIT_SAME_ORDER_RECOVERY_REQUIRED',launch,cfg,'coding',once=True)
            model.assert_not_called()
        report(self.repo,self.remote)
        self.assertEqual(protocol_state(self.repo)['state'],'PUBLICATION_RECONCILIATION_REQUIRED')
        self.assertEqual(protocol_state(self.repo,remote=self.remote)['state'],'REVIEW_READY')
        self.assertEqual(active_id(self.repo),'000-a')

    def B31_strategic_head_CI_merge_effect(self):
        self.active(); _,head,_=report(self.repo,self.remote)
        key=f'commits/{head}/check-runs?per_page=100'
        self.remote.responses[key]={'total_count':1,'check_runs':[{'name':'unit','head_sha':head,'status':'completed','conclusion':'success'}]}
        strategic_gate(self.remote,1,head,['unit'],merge_effect='development-only')
        for value in ('pending','cancelled','failure',None):
            self.remote.responses[key]['check_runs'][0]['conclusion']=value
            self.error('REQUIRED_CHECK_NOT_GREEN',strategic_gate,self.remote,1,head,['unit'],merge_effect='development-only')
        self.error('REQUIRED_CHECK_MISSING',strategic_gate,self.remote,1,head,['missing'],merge_effect='development-only')
        self.error('MERGE_D2_EFFECT',strategic_gate,self.remote,1,head,['unit'],merge_effect='production')
        self.error('REVIEW_HEAD_CHANGED',strategic_gate,self.remote,1,self.base,['unit'],merge_effect='development-only')
        self.remote.prs[1].update(merged=True,merge_commit_sha=head)
        self.remote.responses['branches/main']={'commit':{'sha':head}}
        self.remote.responses['compare/'+head+'...'+head]={'status':'identical'}
        self.assertTrue(verify_merge(self.remote,1,'main')['merged'])

    def B32_ICA_coverage_freshness_independence(self):
        m=metadata(read(self.repo/'oap/audit/ICA-REPORT-TEMPLATE.md'),'oap-ica')
        m.update(status='FINAL',main_sha=self.base,architecture_sha256=digest(read(self.repo/'ARCHITECTURE.md')),
                 plan_sha256=digest(read(self.repo/'PLAN.md')),auditor='Synthetic independent fixture',context_provenance='fresh fixture, not actual audit')
        path=write(self.root/'audit.md',b'```oap-ica\n'+json_bytes(m)+b'```\n')
        out=check_ica(self.repo,path,self.base)
        self.assertTrue(out['gaps'])
        self.assertEqual(out['semantic_acceptance'],'NOT CERTIFIED')
        self.error('ICA_STALE_MAIN',check_ica,self.repo,path,'f'*40)
        m['matrix'][0]['class']='IMPLEMENTED'
        write(path,b'```oap-ica\n'+json_bytes(m)+b'```\n')
        self.error('ICA_EVIDENCE_MISSING',check_ica,self.repo,path,self.base)
        m['matrix']=m['matrix'][1:]
        write(path,b'```oap-ica\n'+json_bytes(m)+b'```\n')
        self.error('ICA_REQUIREMENT_COVERAGE',check_ica,self.repo,path,self.base)

    def B33_audit_requests_never_certify(self):
        for n in ('022','044','055'):
            path=next((self.repo/'oap/strategic-instructions/initial-orders').glob(n+'-a-*.md'))
            text=read(path).decode()
            self.assertIn('independent',text)
            self.assertIn('DRAFT UNTIL STRATEGIC RECONCILIATION',text)
        for p in (self.repo/'oap/audit/requests').glob('*.md'):
            self.assertIn('repeat',read(p).decode())
            self.assertNotIn('Status: FINAL',read(p).decode())
        self.assertIn('repeat',read(self.repo/'oap/audit/ICA-PROTOCOL.md').decode())

    def B34_private_config_canary_and_cleanup(self):
        cfg=self.private()
        canary='FAKE_KEY_PRIVATE_'+'CANARY_94731'
        cfg['STRATEGIC_CODEX_MODEL']=canary
        write(self.strategy/'runtime.env',env_bytes(cfg))
        (self.strategy/'runtime.env').chmod(0o600)
        self.assertEqual(runtime_config(self.strategy/'runtime.env',environ={})['STRATEGIC_CODEX_MODEL'],canary)
        self.error('CONFIG_AUTHORITY_CONFLICT',runtime_config,self.strategy/'runtime.env',environ={'STRATEGIC_CODEX_MODEL':'different'})
        for p in self.repo.rglob('*'):
            if p.is_file() and '.git' not in p.parts:
                self.assertNotIn(canary.encode(),p.read_bytes())
        for p in self.strategy.rglob('*'):
            if p.is_dir(): self.assertEqual(stat.S_IMODE(p.stat().st_mode),0o700)
        self.assertFalse(list(self.strategy.rglob('auth.json')))

    def B35_inactive_actual_structure_and_doctor(self):
        cfg=self.private(); before=snapshot(self.strategy)
        out=doctor(self.repo,self.strategy,cfg)
        self.assertEqual(out['bootstrap_structure'],'valid',out['errors'])
        self.assertEqual(out['activation'],'blocked')
        self.assertEqual(out['live_repair_testing'],'disabled')
        self.assertEqual(out['signals_sent'],0)
        self.assertEqual(before,snapshot(self.strategy))
        self.assertIsNone(active_id(self.repo))
        self.assertEqual(critical_state(read(self.repo/'CRITICAL.md'))['ids'],[])
        self.assertEqual(list((self.repo/'oap/orders').glob('*.md')),[])
        self.assertEqual(list((self.repo/'oap/reports').glob('*.md')),[])

    def B36_live_protocol_history_is_not_copied(self):
        self.assertTrue((SOURCE/'oap/active').is_file())
        self.assertTrue(list((SOURCE/'oap/orders').glob('*.md')))
        self.assertTrue(list((SOURCE/'oap/reports').glob('*.md')))

        self.assertFalse((self.repo/'oap/active').exists())
        self.assertEqual(list((self.repo/'oap/orders').glob('*.md')),[])
        self.assertEqual(list((self.repo/'oap/reports').glob('*.md')),[])
        self.assertTrue((self.repo/'oap/orders/.gitkeep').is_file())
        self.assertTrue((self.repo/'oap/reports/.gitkeep').is_file())
        self.assertTrue((self.repo/'oap/templates/REPORT-TEMPLATE.md').is_file())
        self.assertEqual(protocol_state(self.repo)['state'],'INACTIVE')


def lock_probe(path):
    with lock(path): pass


# Standard unittest discovery, while keeping acceptance IDs visible in test names.
for name in list(vars(Acceptance)):
    if re.match(r'B[0-9]{2}',name):
        setattr(Acceptance,'test_'+name,getattr(Acceptance,name))
        delattr(Acceptance,name)


if __name__=='__main__':
    unittest.main()
