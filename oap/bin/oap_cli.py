#!/usr/bin/env python3
"""Read-only diagnostics and explicitly invoked OAP infrastructure operations."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import sys
from oap_core import *
from oap_install import materialize, runtime_config, refresh_governance
from oap_runtime import setup_shell, launch, tmux_launch


def doctor(repo, strategy=None, config=None, accepted_ref=None):
    checks, errors = {}, []
    try:
        checks['governance'] = governance(repo, 'accepted-runtime' if accepted_ref else 'bootstrap', accepted_ref, strategy=strategy)
        checks['state'] = protocol_state(repo, strategy=strategy)
    except OAPError as e:
        errors.append(str(e))
    blockers = []
    if config:
        for k in ('CODING_CODEX_MODEL','STRATEGIC_CODEX_MODEL'):
            if not (config[k] or config[k.replace('_MODEL','_PROFILE')]):
                blockers.append(k+' or PROFILE unresolved')
        for k in ('OAP_GITHUB_REPOSITORY','OAP_ACCEPTED_REF','OAP_CLI_QUALIFIED_VERSION','OAP_ROLE_AUTH_READY'):
            if not config[k] or (k == 'OAP_ROLE_AUTH_READY' and config[k] != 'YES'):
                blockers.append(k+' unqualified')
        for k in ('OAP_ACK_START_LOOP','OAP_ACK_DANGER_FULL_ACCESS'):
            if config[k] != 'YES':
                blockers.append(k+' disabled')
        if config['OAP_MERGE_EFFECT'] != 'development-only':
            blockers.append('merge deployment side effects not qualified')
        try:
            from oap_runtime import role_context
            for role in ('coding','strategic'):
                role_context(config, role, check_selected=False)
        except OAPError as e:
            errors.append(str(e))
    else:
        blockers.append('private runtime configuration not supplied')
    if strategy:
        for rel in ('control.fifo','response.fifo'):
            try:
                safe_path(Path(strategy)/rel, kind='fifo', private=True)
            except OAPError as e:
                errors.append(str(e))
    result = {'bootstrap_structure': 'invalid' if errors else 'valid', 'errors': errors,
              'fake_helper_tests': 'unproven by this read-only doctor; use recorded test receipt',
              'activation': 'blocked' if blockers or errors else 'prerequisites declared; requalify remote/client before start',
              'blockers': blockers, 'live_repair_testing': 'disabled' if not config or config['REPAIR_ALLOW_LIVE_TESTS'] != 'YES' else 'unverified',
              'product_milestone': 'NOT ASSESSED BY BOOTSTRAP', 'checks': checks,
              'tools_present': {t: bool(shutil.which(t)) for t in ('python3','git','gh','codex','tmux')},
              'signals_sent': 0, 'models_started': 0}
    return result


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    for name in ('state','governance','publish','append-critical','verify-report','ica','strategic-gate','doctor','materialize','refresh-governance'):
        q = sub.add_parser(name, help=name.replace('-',' ')+'; see options')
        q.add_argument('--repo-root', default=os.environ.get('OAP_REPO_ROOT', str(Path(__file__).resolve().parents[2])))
        if name in ('governance','publish','append-critical','doctor','refresh-governance'):
            q.add_argument('--accepted-ref')
        if name in ('state','governance','publish','doctor','materialize','refresh-governance'):
            q.add_argument('--strategic-home', default=os.environ.get('OAP_STRATEGIC_HOME'))
        if name in ('publish','append-critical','verify-report'):
            q.add_argument('--id', required=True)
        if name in ('publish','append-critical','ica'):
            q.add_argument('--source', required=True)
        if name in ('publish','append-critical','materialize','refresh-governance'):
            q.add_argument('--dry-run', action='store_true')
        if name in ('state','publish','verify-report','strategic-gate','refresh-governance'):
            q.add_argument('--repository')
            q.add_argument('--gh-bin', default='gh', help='read-only gh executable; fake only in disposable tests')
        if name == 'governance':
            q.add_argument('--mode', choices=('bootstrap','accepted-runtime','candidate-review'), default='bootstrap')
            q.add_argument('--allow-change', action='append', default=[])
        if name == 'verify-report':
            q.add_argument('--commit')
        if name == 'ica':
            q.add_argument('--current-main', required=True)
        if name == 'strategic-gate':
            q.add_argument('--pr', required=True, type=int)
            q.add_argument('--reviewed-sha')
            q.add_argument('--required-check', action='append', default=[])
            q.add_argument('--merge-effect', default='unverified')
            q.add_argument('--verify-merge', action='store_true')
            q.add_argument('--default-branch', default='main')
        if name == 'doctor':
            q.add_argument('--config')
        if name == 'materialize':
            q.add_argument('--source-repo', default=str(Path(__file__).resolve().parents[2]))
            q.add_argument('--bootstrap-root', required=True)
            q.add_argument('--refresh', action='store_true')
    q = sub.add_parser('fifo', help='exact ASCII OK on actual private named pipe')
    q.add_argument('action', choices=('send','wait'))
    q.add_argument('--fifo', required=True)
    q.add_argument('--timeout', type=float)
    for name in ('setup-shell','launch','tmux'):
        q = sub.add_parser(name)
        q.add_argument('--config', required=True)
        q.add_argument('--print-only', action='store_true')
        if name != 'tmux':
            q.add_argument('--role', required=True, choices=('coding','strategic'))
        if name == 'launch':
            q.add_argument('--resume-id')
            q.add_argument('--once', action='store_true', help='return after one verified/suppressed round; primarily fixture/recovery use')
            q.add_argument('--timeout', type=float)
            q.add_argument('--gh-bin', default='gh')
        if name == 'tmux':
            q.add_argument('--operational', action='store_true')
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    a, command = vars(args), args.command
    try:
        remote = GitHub(a['repository'], a['gh_bin']) if a.get('repository') else None
        if command == 'state':
            result = protocol_state(args.repo_root, strategy=args.strategic_home, remote=remote)
        elif command == 'governance':
            result = governance(args.repo_root, args.mode, args.accepted_ref, args.allow_change, args.strategic_home)
        elif command == 'publish':
            result = publish(args.repo_root, args.source, args.id, strategy=args.strategic_home, accepted_ref=args.accepted_ref, dry_run=args.dry_run, remote=remote)
        elif command == 'append-critical':
            result = append_critical(args.repo_root, args.source, args.id, accepted_ref=args.accepted_ref, dry_run=args.dry_run)
        elif command == 'verify-report':
            result = verify_report(args.repo_root, args.id, commit=args.commit, remote=remote)
        elif command == 'ica':
            result = check_ica(args.repo_root, args.source, args.current_main)
        elif command == 'strategic-gate':
            require(remote is not None, 'REMOTE_REQUIRED')
            result = verify_merge(remote, args.pr, args.default_branch) if args.verify_merge else strategic_gate(remote, args.pr, args.reviewed_sha, args.required_check, merge_effect=args.merge_effect)
        elif command == 'fifo':
            result = fifo(args.fifo, args.action, timeout=args.timeout)
        elif command == 'materialize':
            require(args.strategic_home, 'STRATEGIC_HOME_REQUIRED')
            result = materialize(args.source_repo, args.repo_root, args.strategic_home, args.bootstrap_root, dry_run=args.dry_run, refresh=args.refresh)
        elif command == 'refresh-governance':
            require(args.strategic_home, 'STRATEGIC_HOME_REQUIRED')
            result = refresh_governance(args.repo_root, args.strategic_home, args.accepted_ref, dry_run=args.dry_run, remote=remote)
        elif command == 'doctor':
            config = runtime_config(args.config) if args.config else None
            result = doctor(args.repo_root, args.strategic_home or (config['OAP_STRATEGIC_HOME'] if config else None), config, args.accepted_ref or (config['OAP_ACCEPTED_REF'] or None if config else None))
        else:
            config = runtime_config(args.config)
            if command == 'setup-shell':
                result = setup_shell(config, args.role, print_only=args.print_only)
            elif command == 'launch':
                result = launch(config, args.role, print_only=args.print_only, resume_id=args.resume_id, once=args.once, timeout=args.timeout, gh_bin=args.gh_bin)
            else:
                result = tmux_launch(config, args.operational, args.config, print_only=args.print_only)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if command == 'doctor' and result['bootstrap_structure'] == 'invalid' else 0
    except (OAPError, OSError, ValueError, KeyError, TypeError) as e:
        # Never print subprocess/env/config payloads, raw model output or secrets.
        print(json.dumps({'error': str(e) if isinstance(e,OAPError) else type(e).__name__, 'operation':command}), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print(json.dumps({'error':'INTERRUPTED','operation':command}), file=sys.stderr)
        return 130


if __name__ == '__main__':
    sys.exit(main())
