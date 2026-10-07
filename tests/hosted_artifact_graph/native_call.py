"""Execute one explicitly requested qualification call, never a workflow sequence.

The operator fixes the client, endpoint, project and workspace in environment
names. This helper exists so a native host can approve one bounded command prefix
without approving arbitrary Python or shell execution. It supplies no draft text,
decision, next step, gate answer or recovery operation.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys
import urllib.parse
from pathlib import Path

OPERATIONS = ('status','read','import','draft-open','create-artifact','revise-artifact',
              'freeze','rehearse','export','operation')
MUTATIONS = ('import','draft-open','create-artifact','revise-artifact','freeze','rehearse','export')


def contained(root, supplied, *, new=False):
    root = root.resolve()
    path = Path(supplied)
    if not path.is_absolute():
        path = root/path
    if not path.resolve().is_relative_to(root):
        raise ValueError('Path must remain in the selected native workspace')
    cursor = path
    while cursor != root and cursor != cursor.parent:
        if cursor.is_symlink() or (hasattr(cursor, 'is_junction') and cursor.is_junction()):
            raise ValueError('Linked paths are not allowed')
        cursor = cursor.parent
    if new and path.exists():
        raise ValueError('Output already exists')
    return path


def remote_argv(config, root, args):
    endpoint = urllib.parse.urlsplit(config['endpoint'])
    if endpoint.scheme != 'http' or endpoint.hostname != '127.0.0.1' or endpoint.path or endpoint.username:
        raise ValueError('Only the selected loopback HTTP endpoint is allowed')
    argv = [config['client_python'],'-I','-m','se_harness','remote',args.operation,
            '--endpoint',config['endpoint'],'--project',config['project_id'],
            '--token-env','HAG_NATIVE_TEST_TOKEN','--json']
    if args.operation in MUTATIONS:
        argv += ['--client-wheel',config['client_wheel']]
    if args.operation in ('rehearse','export'):
        argv += ['--test-copy']
    if args.request:
        request = contained(root,args.request)
        if request.stat().st_size > 4*1024*1024:
            raise ValueError('Request exceeds 4 MiB')
        argv += ['--request',str(request)]
    if args.key:
        if args.operation != 'operation':
            raise ValueError('A key is used only for receipt lookup')
        argv += ['--key',args.key]
    if args.destination:
        if args.operation != 'export':
            raise ValueError('A destination is used only for export')
        argv += ['--destination',str(contained(root,args.destination,new=True))]
    return argv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='kind',required=True)
    remote = commands.add_parser('remote')
    remote.add_argument('operation',choices=OPERATIONS)
    for name in ('request','key','destination'):
        remote.add_argument('--'+name)
    remote.add_argument('--record',required=True)
    encoded = commands.add_parser('encode-file')
    encoded.add_argument('path')
    commands.add_parser('identity')
    assertion = commands.add_parser('assert-greeting')
    assertion.add_argument('--record',required=True)
    args = parser.parse_args()
    root = Path(os.environ['HAG_NATIVE_WORK_DIRECTORY']).resolve()
    config = json.loads(Path(os.environ['HAG_NATIVE_SELECTION']).read_text(encoding='utf-8'))
    if args.kind == 'encode-file':
        raw = contained(root,args.path).read_bytes()
        if len(raw)>1024*1024:
            raise ValueError('File exceeds 1 MiB')
        print(json.dumps({'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
                          'content_base64':base64.b64encode(raw).decode()}))
        return 0
    if args.kind == 'identity':
        wheel=Path(config['client_wheel'])
        print(json.dumps({'wheel':str(wheel),'sha256':hashlib.sha256(wheel.read_bytes()).hexdigest(),
                          'project_id':config['project_id'],'endpoint':config['endpoint']}))
        return 0
    record = contained(root,args.record,new=True)
    # Keep the original command record for independent replay. Give native file
    # tools a separate, unescaped copy of stdout; do not summarize the result or
    # choose the next operation for the agent. Check both destinations before
    # executing a potentially mutating request.
    stdout_file = contained(root,record.with_name(record.name + '.stdout.txt'),new=True)
    if args.kind == 'assert-greeting':
        source=Path(config['source_directory'])/'src/greeting.py'
        if hashlib.sha256(source.read_bytes()).hexdigest()!=config['greeting_sha256']:
            raise ValueError('Fixture source changed')
        argv=[config['client_python'],'-I','-B','-c',
              "import runpy,sys;assert runpy.run_path(sys.argv[1])['greeting']()=='Hello rehearsal';print('exact greeting passed')",str(source)]
    else:
        argv=remote_argv(config,root,args)
    outcome=subprocess.run(argv,cwd=root,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
    value={'argv':argv,'cwd':str(root),'exit':outcome.returncode,'stdout':outcome.stdout,'stderr':outcome.stderr}
    raw=json.dumps(value,indent=2)+'\n'
    token=os.environ.get('HAG_NATIVE_TEST_TOKEN','')
    if token and token in raw:
        raise ValueError('Refusing to retain or print a credential')
    record.parent.mkdir(parents=True,exist_ok=True)
    with record.open('x',encoding='utf-8',newline='') as stream:
        stream.write(raw)
    with stdout_file.open('x',encoding='utf-8',newline='') as stream:
        stream.write(outcome.stdout)
    print(json.dumps({'record':str(record),'exit':outcome.returncode,
                      'stdout_file':str(stdout_file),'stderr':outcome.stderr,
                      'instruction':'Read stdout_file for the complete unmodified command result.'}))
    return outcome.returncode


if __name__=='__main__':
    raise SystemExit(main())
