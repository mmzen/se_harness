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
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

OPERATIONS = ('status','read','import','draft-open','create-artifact','revise-artifact',
              'freeze','rehearse','export','operation')
MUTATIONS = ('import','draft-open','create-artifact','revise-artifact','freeze','rehearse','export')
TYPED_OPTIONS = ('evaluator-file','source-manifest','operation-key','expected-project-version',
                 'work-order','domain','artifact-type','artifact','expected-revision','document-file',
                 'baseline','context','context-version')


def lookup_file(root, config, name):
    """Resolve one exact staged relative name, without selecting an instruction."""
    inventory = contained(root, config['inputs_inventory'])
    selected = read_json(root, inventory, '/files')['value']
    matches = [entry for entry in selected if entry['relative'] == name]
    if len(matches) != 1:
        raise ValueError('Expected one exact inventory name; use find-file BASENAME when the path is unknown')
    entry = matches[0]
    path = contained(root, entry['path'])
    expected = contained(inventory.parent, name)
    if path.resolve() != expected.resolve():
        raise ValueError('Inventory path does not match its relative name')
    raw = path.read_bytes()
    token = os.environ.get('HAG_NATIVE_TEST_TOKEN', '')
    if token and token.encode() in raw:
        raise ValueError('Refusing to locate a credential')
    if len(raw) != entry['bytes'] or hashlib.sha256(raw).hexdigest() != entry['sha256']:
        raise ValueError('Staged file no longer matches its inventory')
    return {'file':entry, 'inventory_sha256':hashlib.sha256(inventory.read_bytes()).hexdigest(),
            'lookup_only':True, 'content_read':False}


def find_file(root, config, name, under=''):
    """List bounded exact-basename matches; never select a file for the agent."""
    if not name or len(name)>128 or name in ('.','..') or any(c in name for c in '/\\\0'):
        raise ValueError('Use one filename without directories or wildcards')
    if '*' in name or '?' in name:
        raise ValueError('Wildcards are not supported')
    if under and (not under.endswith('/') or '\\' in under or under.startswith('/') or '..' in under.split('/')):
        raise ValueError('--under must be a relative directory prefix ending in /')
    inventory=contained(root,config['inputs_inventory'])
    entries=read_json(root,inventory,'/files')['value']
    names=sorted(x['relative'] for x in entries if x['relative'].split('/')[-1]==name and x['relative'].startswith(under))
    if len(names)!=len(set(names)):
        raise ValueError('Ambiguous duplicate inventory names')
    selected=[]
    for relative in names[:20]:
        entry=lookup_file(root,config,relative)['file']
        if len(json.dumps(selected+[entry],ensure_ascii=False).encode())>8192:break
        selected.append(entry)
    return {'matches':selected,'total_matches':len(names),'complete':len(selected)==len(names),
            'inventory_sha256':hashlib.sha256(inventory.read_bytes()).hexdigest(),
            'selection':None,'content_read':False,'instruction':'Choose one exact path. Narrow --under when incomplete; use native Read for content.'}


def result_fields(stdout):
    """Render bounded exact JSON fields; list every omitted subtree explicitly."""
    try:
        value = json.loads(stdout)
    except ValueError:
        return {'json':False, 'instruction':'Read stdout_file for the original output.'}
    shown, omitted, used = {}, [], 0
    def visit(value, pointer, depth):
        nonlocal used
        size = len(json.dumps({pointer:value}, ensure_ascii=False).encode())
        if size <= 2048 and used + size <= 8192:
            shown[pointer] = value
            used += size
        elif isinstance(value, dict) and depth < 2:
            for key, child in value.items():
                visit(child, pointer+'/'+key.replace('~','~0').replace('/','~1'), depth+1)
        else:
            omitted.append(pointer)
    visit(value, '', 0)
    result = {'json':True, 'fields':shown, 'omitted_pointers':omitted,
              'complete':not omitted, 'interpretation':False,
              'instruction':'Exact fields only. Read omitted fields needed for this action from stdout_file with read-json; command exit alone is not a gate verdict.'}
    if len(json.dumps(result,ensure_ascii=False).encode()) > 16*1024:
        return {'json':True,'fields':{},'omitted_pointers':[''],'complete':False,
                'interpretation':False,'instruction':'Use read-json on stdout_file; the field index exceeds 16 KiB.'}
    return result


def read_json(root, supplied, pointer, keys=False, decode_base64=False):
    """Read one agent-selected JSON value; never infer a workflow field."""
    path = contained(root, supplied)
    if path.stat().st_size > 4*1024*1024:
        raise ValueError('JSON input exceeds 4 MiB')
    raw = path.read_bytes()
    token = os.environ.get('HAG_NATIVE_TEST_TOKEN', '')
    if token and token.encode() in raw:
        raise ValueError('Refusing to read a credential')
    value = json.loads(raw)
    if pointer.startswith('"'):
        # A JSON string preserves /field through Windows Bash path conversion.
        pointer = json.loads(pointer)
    if pointer and not pointer.startswith('/'):
        raise ValueError('JSON pointer must be empty or start with /')
    for part in pointer.split('/')[1:]:
        if re.search(r'~(?![01])', part):
            raise ValueError('Invalid JSON pointer escape')
        part = part.replace('~1', '/').replace('~0', '~')
        if isinstance(value, dict):
            if part not in value:
                raise ValueError('JSON pointer does not exist')
            value = value[part]
        elif isinstance(value, list) and re.fullmatch(r'0|[1-9][0-9]*', part):
            if int(part) >= len(value):
                raise ValueError('JSON pointer does not exist')
            value = value[int(part)]
        else:
            raise ValueError('JSON pointer does not exist')
    result = {'file':str(path), 'sha256':hashlib.sha256(raw).hexdigest(),
              'pointer':pointer, 'selection_only':True}
    if decode_base64:
        if keys or not isinstance(value,str):
            raise ValueError('Base64 decoding requires one string value, without --keys')
        decoded=base64.b64decode(value,validate=True)
        if base64.b64encode(decoded).decode()!=value:
            raise ValueError('Expected canonical base64')
        if token and token.encode() in decoded:
            raise ValueError('Refusing to decode a credential')
        value=decoded.decode('utf-8')
        result.update(decoded_bytes=len(decoded),decoded_sha256=hashlib.sha256(decoded).hexdigest(),conversion='base64 to UTF-8; exact bytes, no newline conversion')
    if keys:
        if isinstance(value, dict):
            result.update(type='object', keys=list(value))
        elif isinstance(value, list):
            result.update(type='array', length=len(value))
        else:
            result.update(type='scalar')
    else:
        result['value'] = value
    if len(json.dumps(result,ensure_ascii=False).encode()) > 64*1024:
        raise ValueError('Selected output exceeds 64 KiB; use --keys or a narrower pointer')
    return result


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
    if getattr(args,'typed',False):
        argv += ['--typed']
    for option in TYPED_OPTIONS:
        value = getattr(args,option.replace('-','_'),None)
        if value is not None:
            if option in ('evaluator-file','source-manifest','document-file'):
                value = str(contained(root,value))
            argv += ['--'+option,str(value)]
    if getattr(args,'compact',False):
        argv += ['--compact','--record-directory',str(contained(root,args.record+'.evidence',new=True))]
    if getattr(args,'include_document',False):
        argv += ['--include-document']
    return argv


def instructions(root, config, selectors):
    """Resolve selected staged files, then use the installed public section reader."""
    if not 1 <= len(selectors) <= 12:
        raise ValueError('Select 1-12 exact inventory-name#heading values')
    grouped = {}
    for selector in selectors:
        name,sep,heading=selector.partition('#')
        if not sep or not heading or not name.startswith('released-resources/'):
            raise ValueError('Select a staged released resource and exact heading')
        grouped.setdefault(name,[]).append(heading)
    selected=[]
    release=json.loads(contained(root,config['configuration']).read_text(encoding='utf-8'))['components']['evaluator']
    if release['version'] != config['evaluator_version']:
        raise ValueError('Selected instruction release differs from the evaluator')
    for name,headings in grouped.items():
        item=lookup_file(root,config,name)['file']
        selected.append({'raw':base64.b64encode(Path(item['path']).read_bytes()).decode(),
            'resource':name.removeprefix('released-resources/'),'path':item['path'],
            'release':release,'sha256':item['sha256'],'headings':headings})
    script=('import base64,json,sys; from se_harness.resources import section_view; '
            'items=json.load(sys.stdin); '
            'print(json.dumps({"resources":[section_view(base64.b64decode(x.pop("raw")),**x) for x in items]},ensure_ascii=True))')
    outcome=subprocess.run([config['client_python'],'-I','-c',script],input=json.dumps(selected),
        cwd=root,capture_output=True,text=True,encoding='utf-8',timeout=30)
    if outcome.returncode:
        raise ValueError('Selected instruction view failed: '+outcome.stderr)
    return json.loads(outcome.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='kind',required=True)
    remote = commands.add_parser('remote')
    remote.add_argument('operation',choices=OPERATIONS)
    remote.add_argument('--request',help='Path to the selected operation JSON request. Artifact reads use the revision shape from read-v1.json.')
    remote.add_argument('--key',help='Only for remote operation receipt lookup; never for remote read.')
    remote.add_argument('--destination',help='New destination, only for export.')
    remote.add_argument('--record',required=True)
    remote.add_argument('--typed',action='store_true')
    remote.add_argument('--compact',action='store_true')
    remote.add_argument('--include-document',action='store_true')
    for option in TYPED_OPTIONS:
        remote.add_argument('--'+option)
    instruction=commands.add_parser('instructions',help='Read complete selected released sections with provenance')
    instruction.add_argument('--section',action='append',required=True)
    encoded = commands.add_parser('encode-file')
    encoded.add_argument('path')
    selected = commands.add_parser('read-json', help='Read an exact JSON pointer from a saved result; empty pointer selects its root')
    selected.add_argument('path')
    selected.add_argument('--pointer', default='', help="JSON pointer, optionally encoded as a JSON string. Windows Bash: --pointer '\"/field\"' preserves the slash. Omit for root.")
    representation=selected.add_mutually_exclusive_group()
    representation.add_argument('--keys', action='store_true', help='Return object keys or array length, without field values')
    representation.add_argument('--decode-base64', action='store_true', help='Decode the selected canonical base64 string to exact UTF-8 text; returns its byte digest')
    lookup = commands.add_parser('lookup-file', help='Locate one exact relative name in the staged input inventory; does not read its content into context')
    lookup.add_argument('name')
    search=commands.add_parser('find-file',help='List up to 20 exact filename matches in the staged inventory; never chooses a file')
    search.add_argument('name')
    search.add_argument('--under',default='',help='Optional relative directory prefix ending in /')
    commands.add_parser('identity')
    assertion = commands.add_parser('assert-greeting')
    assertion.add_argument('--record',required=True)
    args = parser.parse_args()
    root = Path(os.environ['HAG_NATIVE_WORK_DIRECTORY']).resolve()
    config = json.loads(Path(os.environ['HAG_NATIVE_SELECTION']).read_text(encoding='utf-8'))
    if args.kind == 'instructions':
        print(json.dumps(instructions(root,config,args.section),ensure_ascii=True))
        return 0
    if args.kind == 'lookup-file':
        print(json.dumps(lookup_file(root,config,args.name),ensure_ascii=False))
        return 0
    if args.kind == 'find-file':
        print(json.dumps(find_file(root,config,args.name,args.under),ensure_ascii=False))
        return 0
    if args.kind == 'read-json':
        print(json.dumps(read_json(root,args.path,args.pointer,args.keys,args.decode_base64),ensure_ascii=False))
        return 0
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
    started=time.monotonic()
    outcome=subprocess.run(argv,cwd=root,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
    value={'argv':argv,'cwd':str(root),'exit':outcome.returncode,'stdout':outcome.stdout,'stderr':outcome.stderr,
           'elapsed_seconds':round(time.monotonic()-started,6)}
    raw=json.dumps(value,indent=2)+'\n'
    token=os.environ.get('HAG_NATIVE_TEST_TOKEN','')
    if token and token in raw:
        raise ValueError('Refusing to retain or print a credential')
    record.parent.mkdir(parents=True,exist_ok=True)
    with record.open('x',encoding='utf-8',newline='') as stream:
        stream.write(raw)
    with stdout_file.open('x',encoding='utf-8',newline='') as stream:
        stream.write(outcome.stdout)
    if getattr(args,'compact',False):
        # Pass through the client's evidence-backed view, without a second summary.
        print(json.dumps({'record':str(record),'exit':outcome.returncode,'elapsed_seconds':value['elapsed_seconds'],
                          'stdout_file':str(stdout_file),'stderr':outcome.stderr,'client_view':json.loads(outcome.stdout) if outcome.stdout else None}))
        return outcome.returncode
    print(json.dumps({'record':str(record),'exit':outcome.returncode,
                      'stdout_file':str(stdout_file),'stderr':outcome.stderr,
                      'result_fields':result_fields(outcome.stdout),
                      'instruction':'Read stdout_file for the complete unmodified command result.'}))
    return outcome.returncode


if __name__=='__main__':
    raise SystemExit(main())
