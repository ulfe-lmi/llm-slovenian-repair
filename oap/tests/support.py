"""Synthetic boundary fixtures; all writes stay inside owned TemporaryDirectory."""
import base64
import copy
import json
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'bin'))
from oap_core import *

SOURCE = Path(__file__).resolve().parents[2]


class FakeGitHub:
    repository = 'synthetic/project'
    def __init__(self, repo):
        self.repo = repo
        self.prs = {}
        self.peers = []
        self.responses = {}
        self.calls = []

    def branch_prs(self, branch):
        self.calls.append(('branch_prs', branch))
        return self.peers

    def pr(self, number):
        self.calls.append(('pr', number))
        require(number in self.prs, 'REMOTE_UNVERIFIED')
        return copy.deepcopy(self.prs[number])

    def api(self, path):
        self.calls.append(('api', path))
        require(path in self.responses, 'REMOTE_UNVERIFIED', path)
        return copy.deepcopy(self.responses[path])


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode())
    return path


def commit(repo, message='Synthetic fixture'):
    git(repo, 'add', '--', '.')
    git(repo, '-c', 'commit.gpgsign=false', 'commit', '-m', message)
    return git(repo, 'rev-parse', 'HEAD').decode().strip()


def order(repo, base, ident='000-a', pr=None, decision='D0', payload=None, action='APPEND'):
    obj = ident[:3]
    m = dict(id=ident, title='Synthetic bounded contract', objective=obj, status='FINAL',
             repository='synthetic/project', default_branch='main', base_sha=base,
             branch='oap/'+obj+'-synthetic', phase='DEMONSTRATOR',
             pr_mode='CREATE_NEW_PR' if ident.endswith('-a') else 'AMEND_EXISTING_PR', pr=pr,
             local_work='Preserve unrelated synthetic sentinel', prior_review='Observed synthetic prerequisite',
             provenance=[dict(kind='A',reference='ARCHITECTURE.md §6')], decision_class=decision,
             dependencies=[],lr=['LR-007'],relevant_gates=[],required_checks=['unit'],
             governance={p:v['sha256'] for p,v in jsread(repo/'oap/governance/MANIFEST.json')['identities'].items()})
    dha = 'NONE'
    payload_text = ''
    if payload:
        prior = git_blob(repo, base, 'CRITICAL.md')
        m.update(critical_payload_bytes=len(payload), critical_payload_sha256=digest(payload),
                 critical_prior_bytes=len(prior), critical_prior_sha256=digest(prior))
        dha = 'APPEND CRIT-0001' if action=='APPEND' else 'NONE\n- Mitigation update: UPDATE CRIT-0001'
        tag = 'critical-entry' if action=='APPEND' else 'critical-update'
        payload_text = '\n\n````'+tag+'\n'+payload.decode()+'````\n'
    sections = '\n\n'.join('## '+s+'\n'+('- Decision: '+dha if s=='Deferred human adjudication' else 'Synthetic observed contract at the stated boundary.') for s in ORDER_SECTIONS)
    data = '# Synthetic work order\n\n```oap-metadata\n'+json.dumps(m,indent=2)+'\n```\n\n'+sections+payload_text+'\n'
    return m, data.encode()


def replace_metadata(data, m, tag='oap-metadata'):
    old = fenced(data, tag)
    return data.replace(old, json_bytes(m), 1)


def entry(ident='CRIT-0001', objective='000-b', pr=1):
    f = {'Status':'OPEN — HUMAN ADJUDICATION REQUIRED','Introduced by':f'PR #{pr} / OAP objective {objective}',
         'Category':'architecture','Severity':'medium','Decision confidence':'medium',
         'Required human gate':'before synthetic external demo','Affected components':'Disposable fixture only'}
    text = '\n## '+ident+' — Synthetic contained choice\n\n'
    text += '\n'.join('- **'+k+':** '+v for k,v in f.items())+'\n'
    for s in CRIT_SECTIONS:
        val = {'Strategic attestation':'ALL FIVE CRITICAL-ENTRY CONDITIONS SATISFIED',
               'Human disposition':'PENDING — append separately; do not edit this entry.',
               'Resolution':'PENDING — cleared only by the latest appended human ACCEPTED disposition.'}.get(s, 'Synthetic alternative, bounded evidence and reversible test-only choice.')
        text += '\n### '+s+'\n'+val+'\n'
    return text.encode()


def mitigation():
    return b'\n## MITIGATION UPDATE \xe2\x80\x94 CRIT-0001 \xe2\x80\x94 synthetic evidence\n- Status: MITIGATED\n- Evidence: Synthetic regression passed\n- Mitigation: Bound disposable state\n- Remaining gate: before synthetic external demo\n- Objective: 000-c\n'


def human(decision='ACCEPTED', day='2026-09-07'):
    return f'\n## HUMAN ADJUDICATION — CRIT-0001 — {day}\n- Decision: {decision}\n- Authority: SYNTHETIC HUMAN FIXTURE (not owner)\n- Conditions or required follow-up:\n- Evidence/reference: Synthetic mocked provenance only\n'.encode()


def install_order(repo, data, ident='000-a'):
    path = write(repo/'oap/orders'/f'{ident}-synthetic.md', data)
    write(repo/'oap/active', ident+'\n')
    return path


def report(repo, remote, ident='000-a', *, extra=False, parent=None):
    opath = matching(repo,'orders',ident)
    od = read(opath)
    o = validate_order(od,repo,ident,opath.name)
    impl = commit(repo,'Synthetic implementation '+ident)
    r = dict(id=ident,result='COMPLETE',order_path=str(opath.relative_to(repo)),order_sha256=digest(od),governance=o['governance'],
             publication_commit='SELF',implementation_head=parent or impl,publication_verified=False,
             pr_mode=o['pr_mode'],pr=o['pr'] or 1,pr_url=f'https://github.com/synthetic/project/pull/{o["pr"] or 1}',
             pr_state='open',branch=o['branch'],base_sha=o['base_sha'],starting_remote_sha=o['base_sha'],no_merge=True,
             checks=[dict(command='synthetic unit',result='PASSED',sha=impl)],critical_action='NONE',
             pr_observed_at='2026-09-06T10:00:00+00:00',report_written_at='2026-09-06T10:01:00+00:00')
    for k in ('implementation','documentation','criteria','negative_paths','boundary_fidelity','setup','privacy','limits','human_gates','scope'):
        r[k] = 'Synthetic fixture observation, no actual product claim.'
    if o.get('critical_action'):
        r['critical_action'] = ('APPENDED ' if o['critical_action']=='APPEND' else 'MITIGATION UPDATED ')+o['critical_id']
    rp = write(repo/'oap/reports'/opath.name, '# Synthetic report\n\n```oap-report\n'+json.dumps(r,indent=2)+'\n```\n')
    if extra:
        write(repo/'unexpected.txt','synthetic unexpected mutation')
    head = commit(repo, 'Synthetic final report '+ident)
    rel = str(rp.relative_to(repo))
    remote.prs[r['pr']] = dict(number=r['pr'],state='open',merged=False,draft=False,
                              created_at='2026-09-06T09:59:00Z',head={'sha':head,'ref':o['branch']},
                              base={'repo':{'full_name':'synthetic/project'}})
    remote.responses['commits/'+head] = {'parents':[{'sha':impl}],'files':[{'filename':rel}]+([{'filename':'unexpected.txt'}] if extra else [])}
    remote.responses['contents/'+rel+'?ref='+head] = {'encoding':'base64','content':base64.b64encode(read(rp)).decode()}
    return r, head, rp
