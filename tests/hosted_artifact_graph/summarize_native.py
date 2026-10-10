"""Mechanical observations only: content quality still needs independent review.

Never reproduce private reasoning. Do not infer provider timings or correctness
from a successful process or operation. Native denial events remain in the count.
"""
import argparse
import collections
import json
from pathlib import Path


def helper_reads(command, output, line):
    """Copy metadata from successful visible helper reads, never reread source files."""
    if 'native_call.py' not in command or not any(x in command for x in (' read-text ', ' instructions ')):
        return []
    try:
        value = json.loads(output)
    except (ValueError, TypeError):
        return []  # Truncated or non-JSON output is not a confirmed content read.
    if not isinstance(value, dict):
        return []
    items = value.get('resources', value.get('files', [value]))
    if not isinstance(items, list):
        return []
    reads = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get('path'), str):
            continue
        sections = item.get('sections', [])
        text_read = isinstance(item.get('text'), str)
        section_read = isinstance(sections, list) and any(
            isinstance(s, dict) and isinstance(s.get('content'), str) for s in sections)
        if not (text_read or section_read):
            continue
        row = {k:item[k] for k in ('path','sha256','bytes','offset','next_offset','complete','characters') if k in item}
        row.update(line=line, source='successful helper result')
        if section_read:
            row['sections'] = [{k:s[k] for k in ('heading','start_line','end_line','sha256','complete') if k in s}
                               for s in sections if isinstance(s, dict) and isinstance(s.get('content'), str)]
        reads.append(row)
    return reads


def summarize(root):
    complete = (root/'session.json').is_file()
    session = json.loads((root/'session.json').read_text(encoding='utf-8')) if complete else {}
    calls, messages, failures, reads = {}, {}, {}, []
    inputs, observed_reads, completed_reads = {}, [], set()
    non_json_lines = []
    lines = (root/'events.jsonl').read_text(encoding='utf-8').splitlines()
    partial_line = False
    for line, raw in enumerate(lines, 1):
        try:
            event = json.loads(raw)
        except ValueError:
            if not raw.lstrip().startswith(('{','[')):
                non_json_lines.append(line)
                continue
            if complete or line != len(lines):
                raise
            partial_line = True
            break
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
                    calls[key] = {'line': line, 'name': block['name'], 'description': block.get('input', {}).get('description')}
                    inputs[key] = block.get('input', {})
                    if block['name'] == 'Read':
                        reads.append({'line': line, 'path': block.get('input', {}).get('file_path')})
            if block.get('type') == 'tool_result' and block.get('is_error'):
                failures[block['tool_use_id']] = {'line':line,'call_id':block['tool_use_id'], 'source':'native tool_result is_error',
                    'call':calls.get(block['tool_use_id']), 'diagnostic':str(block.get('content',''))[-1000:]}
            if block.get('type') == 'tool_result' and not block.get('is_error'):
                key = block.get('tool_use_id')
                if key in completed_reads:
                    continue
                completed_reads.add(key)
                call, args = calls.get(key, {}), inputs.get(key, {})
                if call.get('name') == 'Read' and isinstance(args.get('file_path'), str):
                    observed_reads.append({'line':line,'source':'successful native Read',
                        'path':args['file_path'],'requested_offset':args.get('offset'),
                        'requested_limit':args.get('limit'),'complete':None})
                if call.get('name') == 'Bash':
                    content = block.get('content', [])
                    texts = [content] if isinstance(content, str) else [
                        x.get('text','') for x in content if isinstance(x,dict) and x.get('type') == 'text']
                    for text in texts:
                        observed_reads.extend(helper_reads(args.get('command',''),text,line))
        item = event.get('item', {})
        if event.get('type') == 'item.completed' and item.get('type') in ('command_execution','mcp_tool_call','file_change'):
            calls[item['id']] = {'line':line,'name':item['type']}
            if item.get('exit_code', 0) not in (None,0) or item.get('error'):
                failures[item['id']] = {'line':line,'call_id':item['id'],'source':'native failed item'}
            elif item['type'] == 'command_execution':
                observed_reads.extend(helper_reads(item.get('command',''),item.get('aggregated_output',''),line))
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
    wall=session.get('elapsed_seconds')
    # Codex JSON omits some orchestrated tool calls. Its item count is a lower
    # bound, not a complete native-call count or provider context measurement.
    count_complete=session.get('host') != 'codex' and bool(messages)
    return {'snapshot':'complete' if complete else 'in_progress', 'partial_event_line_omitted':partial_line,
            'non_json_diagnostic_lines':non_json_lines,
            'wall_seconds':wall,'native_calls':len(calls) if count_complete else None,
            'observed_tool_items':len(calls), 'native_call_count_complete':count_complete,
            'calls_by_tool':dict(collections.Counter(x['name'] for x in calls.values())),
            'model_turns':len(messages) if messages else None,'peak_input_context':peak,
            'initial_input_context':next(iter(messages.values()))['tokens'] if messages else None,
            'goals':{'wall_under_180':'unavailable' if wall is None else 'met' if wall<180 else 'missed',
                     'calls_at_most_15':'missed' if len(calls)>15 else 'met' if complete and count_complete else 'unavailable',
                     'peak_under_40000':'unavailable' if peak is None else 'missed' if peak>=40000 else 'met' if complete else 'unavailable'},
            'native_failures':list(failures.values()),'command_records':records,
            'failed_command_records':[x for x in records if x['exit']!=0], 'file_reads':reads,
            'observed_content_reads':observed_reads,
            'repeated_read_paths':{p:n for p,n in collections.Counter(x['path'] for x in reads).items() if n>1},
            'content_review':'not performed by this summary','provider_time':'unclassified',
            'limits':'Observed native calls and command captures only. file_reads lists attempts; observed_content_reads lists successful visible reads, not complete capture or proof of full-file reading. Metadata comes from the captured result, never a later source read. No private reasoning exported. Provider usage is not billed-token total. Tool durations may overlap; they are not subtracted to infer model time.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    value=summarize(args.root)
    with args.output.open('x',encoding='utf-8') as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2)
        stream.write('\n')
