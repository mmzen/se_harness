"""Mechanical observations only: content quality still needs independent review.

Never reproduce private reasoning. Do not infer provider timings or correctness
from a successful process or operation. Native denial events remain in the count.
"""
import argparse
import collections
import json
from pathlib import Path


def summarize(root):
    session = json.loads((root/'session.json').read_text(encoding='utf-8'))
    calls, messages, failures, reads = {}, {}, {}, []
    for line, raw in enumerate((root/'events.jsonl').read_text(encoding='utf-8').splitlines(), 1):
        event = json.loads(raw)
        message = event.get('message', {})
        if not isinstance(message, dict):
            continue
        usage = message.get('usage')
        if usage:
            tokens = sum(usage.get(k, 0) for k in ('input_tokens','cache_creation_input_tokens','cache_read_input_tokens'))
            messages[message['id']] = {'line': line, 'tokens': tokens}
        for block in message.get('content', []):
            if not isinstance(block, dict):
                continue
            if block.get('type') == 'tool_use':
                key = block['id']
                if key not in calls:
                    calls[key] = {'line': line, 'name': block['name']}
                    if block['name'] == 'Read':
                        reads.append({'line': line, 'path': block.get('input', {}).get('file_path')})
            if block.get('type') == 'tool_result' and block.get('is_error'):
                failures[block['tool_use_id']] = {'line':line,'call_id':block['tool_use_id'], 'source':'native tool_result is_error'}
        item = event.get('item', {})
        if event.get('type') == 'item.completed' and item.get('type') in ('command_execution','mcp_tool_call'):
            calls[item['id']] = {'line':line,'name':item['type']}
            if item.get('exit_code', 0) not in (None,0) or item.get('error'):
                failures[item['id']] = {'line':line,'call_id':item['id'],'source':'native failed item'}
    records=[]
    for path in sorted((root/'work').rglob('*.json')):
        if path.stat().st_size > 4*1024*1024:
            continue
        try:
            value=json.loads(path.read_text(encoding='utf-8'))
        except (ValueError,UnicodeError):
            continue
        if isinstance(value,dict) and {'argv','cwd','exit','stdout','stderr'} <= value.keys():
            records.append({'path':str(path),'exit':value['exit'],'elapsed_seconds':value.get('elapsed_seconds'),
                            'argv':value['argv']})
    peak=max((x['tokens'] for x in messages.values()),default=None)
    wall=session['elapsed_seconds']
    return {'wall_seconds':wall,'native_calls':len(calls),'calls_by_tool':dict(collections.Counter(x['name'] for x in calls.values())),
            'model_turns':len(messages) if messages else None,'peak_input_context':peak,
            'initial_input_context':next(iter(messages.values()))['tokens'] if messages else None,
            'goals':{'wall_under_180':'met' if wall<180 else 'missed','calls_at_most_15':'met' if len(calls)<=15 else 'missed',
                     'peak_under_40000':'unavailable' if peak is None else 'met' if peak<40000 else 'missed'},
            'native_failures':list(failures.values()),'command_records':records,
            'failed_command_records':[x for x in records if x['exit']!=0], 'file_reads':reads,
            'repeated_read_paths':{p:n for p,n in collections.Counter(x['path'] for x in reads).items() if n>1},
            'content_review':'not performed by this summary','provider_time':'unclassified',
            'limits':'Observed native calls and command captures only. No private reasoning exported. Provider usage is not billed-token total. Tool durations may overlap; they are not subtracted to infer model time.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    value=summarize(args.root)
    with args.output.open('x',encoding='utf-8') as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2)
        stream.write('\n')
